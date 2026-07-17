from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from trazabilidad.closing import CloseResult
from trazabilidad.project_close import ProjectCloseCoordinator, ProjectCloseError


class FakeCloseService:
    def __init__(self) -> None:
        self.calls: list[bool] = []

    def execute(self, payload: dict, *, dry_run: bool = False) -> CloseResult:
        self.calls.append(dry_run)
        return CloseResult(
            status="dry_run" if dry_run else "completed",
            session_action="would_create" if dry_run else "created",
            session_page_id=None if dry_run else "session-1",
            session_url=None,
            activities_created=0 if dry_run else 1,
            activities_existing=0,
            activities_planned=1,
        )


class ProjectCloseCoordinatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.project = root / "project"
        self.remote = root / "remote.git"
        self._run(root, "git", "init", "--bare", str(self.remote))
        self._run(root, "git", "init", "-b", "main", str(self.project))
        self._run(self.project, "git", "config", "user.name", "Test")
        self._run(self.project, "git", "config", "user.email", "test@example.com")
        (self.project / "file.txt").write_text("contenido\n", encoding="utf-8")
        self._run(self.project, "git", "add", "file.txt")
        self._run(self.project, "git", "commit", "-m", "initial")
        self._run(self.project, "git", "remote", "add", "origin", str(self.remote))
        self._run(self.project, "git", "push", "-u", "origin", "main")
        self.head = self._run(self.project, "git", "rev-parse", "HEAD").stdout.strip()
        self.service = FakeCloseService()
        self.coordinator = ProjectCloseCoordinator(self.service)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_prepare_validates_git_and_notion_without_writing(self) -> None:
        result = self.coordinator.prepare(self.project, self._payload())
        self.assertEqual(result.status, "prepared")
        self.assertEqual(result.git.head, self.head)
        self.assertEqual(self.service.calls, [True])
        self.assertEqual(
            self._run(self.project, "git", "tag", "--list").stdout.strip(), ""
        )

    def test_prepare_rejects_dirty_tree_before_notion(self) -> None:
        (self.project / "file.txt").write_text("cambio\n", encoding="utf-8")
        with self.assertRaisesRegex(ProjectCloseError, "no está limpio"):
            self.coordinator.prepare(self.project, self._payload())
        self.assertEqual(self.service.calls, [])

    def test_prepare_rejects_existing_tag(self) -> None:
        self._run(self.project, "git", "tag", "-a", "V1.1", "-m", "ocupado")
        with self.assertRaisesRegex(ProjectCloseError, "tag local V1.1 ya existe"):
            self.coordinator.prepare(self.project, self._payload())
        self.assertEqual(self.service.calls, [])

    def test_prepare_rejects_when_remote_branch_diverged(self) -> None:
        other = Path(self.temp.name) / "other"
        self._run(
            Path(self.temp.name),
            "git",
            "clone",
            "-b",
            "main",
            str(self.remote),
            str(other),
        )
        self._run(other, "git", "config", "user.name", "Other")
        self._run(other, "git", "config", "user.email", "other@example.com")
        (other / "remote.txt").write_text("remoto\n", encoding="utf-8")
        self._run(other, "git", "add", "remote.txt")
        self._run(other, "git", "commit", "-m", "remote")
        self._run(other, "git", "push", "origin", "main")

        with self.assertRaisesRegex(ProjectCloseError, "no es ancestro de HEAD"):
            self.coordinator.prepare(self.project, self._payload())
        self.assertEqual(self.service.calls, [])

    def test_prepare_accepts_empty_remote(self) -> None:
        empty = Path(self.temp.name) / "empty.git"
        self._run(Path(self.temp.name), "git", "init", "--bare", str(empty))
        self._run(self.project, "git", "remote", "set-url", "origin", str(empty))

        result = self.coordinator.prepare(self.project, self._payload())
        self.assertFalse(result.git.remote_branch)
        self.assertEqual(self.service.calls, [True])

    def test_finalize_tags_closes_notion_and_pushes_atomically(self) -> None:
        result = self.coordinator.finalize(self.project, self._payload())
        self.assertEqual(result.status, "completed")
        self.assertTrue(result.published)
        self.assertEqual(self.service.calls, [True, False])
        remote_tag = self._run(
            self.project,
            "git",
            "ls-remote",
            "--tags",
            "origin",
            "refs/tags/V1.1^{}",
        ).stdout.split()[0]
        self.assertEqual(remote_tag, self.head)

    def test_finalize_creates_branch_and_tag_on_empty_remote(self) -> None:
        empty = Path(self.temp.name) / "empty.git"
        self._run(Path(self.temp.name), "git", "init", "--bare", str(empty))
        self._run(self.project, "git", "remote", "set-url", "origin", str(empty))

        result = self.coordinator.finalize(self.project, self._payload())
        self.assertFalse(result.git.remote_branch)
        refs = self._run(
            self.project,
            "git",
            "ls-remote",
            "origin",
            "refs/heads/main",
            "refs/tags/V1.1^{}",
        ).stdout
        self.assertEqual(refs.count(self.head), 2)

    def test_prepare_rejects_graph_built_before_code_changes(self) -> None:
        graph_dir = self.project / "graphify-out"
        graph_dir.mkdir()
        (graph_dir / "graph.json").write_text(
            json.dumps({"built_at_commit": self.head}), encoding="utf-8"
        )
        (graph_dir / "GRAPH_REPORT.md").write_text(
            f"snapshot {self.head[:8]}\n", encoding="utf-8"
        )
        (self.project / "file.txt").write_text("código nuevo\n", encoding="utf-8")
        self._run(self.project, "git", "add", "file.txt", "graphify-out")
        self._run(self.project, "git", "commit", "-m", "stale graph")
        self.head = self._run(self.project, "git", "rev-parse", "HEAD").stdout.strip()

        with self.assertRaisesRegex(ProjectCloseError, "Graphify está desactualizado"):
            self.coordinator.prepare(self.project, self._payload())
        self.assertEqual(self.service.calls, [])

    def test_prepare_accepts_graph_artifact_commit_after_snapshot(self) -> None:
        graph_dir = self.project / "graphify-out"
        graph_dir.mkdir()
        (graph_dir / "graph.json").write_text(
            json.dumps({"built_at_commit": self.head}), encoding="utf-8"
        )
        (graph_dir / "GRAPH_REPORT.md").write_text(
            f"snapshot {self.head[:8]}\n", encoding="utf-8"
        )
        self._run(self.project, "git", "add", "graphify-out")
        self._run(self.project, "git", "commit", "-m", "graph artifacts")
        self.head = self._run(self.project, "git", "rev-parse", "HEAD").stdout.strip()

        result = self.coordinator.prepare(self.project, self._payload())
        self.assertEqual(result.status, "prepared")
        self.assertEqual(self.service.calls, [True])

    def _payload(self) -> dict:
        return json.loads(
            json.dumps(
                {
                    "session": {
                        "name": "project",
                        "start": "2026-06-30T13:00:00-05:00",
                        "end": "2026-06-30T14:00:00-05:00",
                        "session_date": "2026-06-30",
                        "duration_minutes": 60,
                        "hours": 1,
                        "challenge": "Cerrar de forma segura",
                        "resolved": True,
                        "summary": "Cambio terminado y validado.",
                        "version": "V1.1",
                        "git_tag": "V1.1",
                        "git_commit": self.head,
                    },
                    "activities": [
                        {
                            "title": "Implementación",
                            "category": "Documentación",
                            "reported_at": "2026-06-30",
                            "hours": 1,
                            "description": "Coordinación del cierre.",
                            "status": "Done",
                        }
                    ],
                    "quality": {
                        "offline_audit": "0 vulnerabilidades",
                        "known_alerts": [],
                        "online_validation": "no requerida",
                    },
                }
            )
        )

    @staticmethod
    def _run(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            args,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
