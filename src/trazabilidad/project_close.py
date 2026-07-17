"""Cierre seguro de un proyecto: Git, Notion y publicación."""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .closing import CloseResult, SessionCloseService, validate_close_payload


class ProjectCloseError(RuntimeError):
    """El proyecto no cumple una precondición de cierre."""


@dataclass(frozen=True)
class GitCloseState:
    project: str
    branch: str
    head: str
    tag: str
    remote: str
    remote_branch: bool
    local_tag: bool
    remote_tag: bool


@dataclass(frozen=True)
class PreparedClose:
    status: str
    git: GitCloseState
    notion: CloseResult


@dataclass(frozen=True)
class FinalizedClose:
    status: str
    git: GitCloseState
    notion: CloseResult
    published: bool


class ProjectCloseCoordinator:
    """Aplica las barreras que vuelven transaccional el cierre asistido."""

    def __init__(self, service: SessionCloseService) -> None:
        self.service = service

    def prepare(
        self,
        project: Path,
        payload: dict[str, Any],
        *,
        remote: str = "origin",
        branch: str = "main",
    ) -> PreparedClose:
        validate_close_payload(payload)
        git = inspect_git_close(
            project,
            payload,
            remote=remote,
            branch=branch,
            allow_matching_tag=False,
        )
        notion = self.service.execute(payload, dry_run=True)
        return PreparedClose("prepared", git, notion)

    def finalize(
        self,
        project: Path,
        payload: dict[str, Any],
        *,
        remote: str = "origin",
        branch: str = "main",
        tag_message: str | None = None,
    ) -> FinalizedClose:
        validate_close_payload(payload)
        git = inspect_git_close(
            project,
            payload,
            remote=remote,
            branch=branch,
            allow_matching_tag=True,
        )
        self.service.execute(payload, dry_run=True)
        if not git.local_tag:
            message = tag_message or f"{git.tag} — cierre de {payload['session']['name']}"
            _git(project, "tag", "-a", git.tag, "-m", message)
            git = inspect_git_close(
                project,
                payload,
                remote=remote,
                branch=branch,
                allow_matching_tag=True,
            )

        notion = self.service.execute(payload)
        if notion.status != "completed":
            raise ProjectCloseError(
                f"Notion devolvió status={notion.status!r}; no se publicará Git."
            )

        _git(
            project,
            "push",
            "--atomic",
            remote,
            f"HEAD:refs/heads/{branch}",
            f"refs/tags/{git.tag}",
        )
        return FinalizedClose("completed", git, notion, True)


def inspect_git_close(
    project: Path,
    payload: dict[str, Any],
    *,
    remote: str,
    branch: str,
    allow_matching_tag: bool,
) -> GitCloseState:
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise ProjectCloseError(f"No existe el proyecto: {project}")

    root = Path(_git(project, "rev-parse", "--show-toplevel")).resolve()
    if root != project:
        raise ProjectCloseError(f"--project debe ser la raíz Git: {root}")

    current_branch = _git(project, "symbolic-ref", "--short", "HEAD")
    if current_branch != branch:
        raise ProjectCloseError(
            f"Se esperaba la rama {branch!r}, pero la rama actual es {current_branch!r}."
        )

    dirty = _git(project, "status", "--porcelain=v1", "--untracked-files=all")
    if dirty:
        raise ProjectCloseError(
            "El árbol de trabajo no está limpio; documentación, Graphify y código "
            "deben quedar en el commit final."
        )

    session = payload["session"]
    head = _git(project, "rev-parse", "HEAD")
    if head != session["git_commit"].lower():
        raise ProjectCloseError(
            f"El payload apunta a {session['git_commit']}, pero HEAD es {head}."
        )
    _validate_graphify_snapshot(project, head)

    _git(project, "remote", "get-url", remote)
    remote_branch = bool(
        _git(project, "ls-remote", "--heads", remote, f"refs/heads/{branch}")
    )
    if remote_branch:
        _git(project, "fetch", "--quiet", "--no-tags", remote, branch)
        try:
            _git(project, "merge-base", "--is-ancestor", f"{remote}/{branch}", "HEAD")
        except ProjectCloseError as exc:
            raise ProjectCloseError(
                f"{remote}/{branch} no es ancestro de HEAD; integra los cambios "
                "remotos antes de cerrar."
            ) from exc

    tag = session["git_tag"]
    local_ref = _git_optional(project, "rev-parse", "--verify", f"refs/tags/{tag}")
    local_tag = local_ref is not None
    if local_tag:
        tag_type = _git(project, "cat-file", "-t", f"refs/tags/{tag}")
        peeled = _git(project, "rev-parse", f"refs/tags/{tag}^{{}}")
        if tag_type != "tag" or peeled != head:
            raise ProjectCloseError(
                f"El tag local {tag} ya existe y no es el tag anotado esperado para HEAD."
            )
        if not allow_matching_tag:
            raise ProjectCloseError(f"El tag local {tag} ya existe.")

    remote_refs = _git(
        project,
        "ls-remote",
        "--tags",
        remote,
        f"refs/tags/{tag}",
        f"refs/tags/{tag}^{{}}",
    )
    remote_tag = bool(remote_refs)
    if remote_tag:
        refs = dict(
            line.split(maxsplit=1)[::-1]
            for line in remote_refs.splitlines()
            if len(line.split(maxsplit=1)) == 2
        )
        direct = refs.get(f"refs/tags/{tag}")
        peeled = refs.get(f"refs/tags/{tag}^{{}}")
        matches = local_tag and direct == local_ref and peeled == head
        if not allow_matching_tag or not matches:
            raise ProjectCloseError(
                f"El tag remoto {tag} ya existe; los tags publicados son inmutables."
            )

    return GitCloseState(
        project=str(project),
        branch=current_branch,
        head=head,
        tag=tag,
        remote=remote,
        remote_branch=remote_branch,
        local_tag=local_tag,
        remote_tag=remote_tag,
    )


def _validate_graphify_snapshot(project: Path, head: str) -> None:
    graph_path = project / "graphify-out" / "graph.json"
    if not graph_path.exists():
        return
    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProjectCloseError("graphify-out/graph.json no es JSON válido.") from exc
    built = graph.get("built_at_commit")
    if not isinstance(built, str) or not built:
        raise ProjectCloseError("Graphify no declara built_at_commit.")
    try:
        _git(project, "merge-base", "--is-ancestor", built, head)
        changed = _git(project, "diff", "--name-only", f"{built}..{head}").splitlines()
    except ProjectCloseError as exc:
        raise ProjectCloseError(
            f"Graphify declara un commit inválido o ajeno al cierre: {built}."
        ) from exc
    if any(not path.startswith("graphify-out/") for path in changed):
        raise ProjectCloseError(
            "Graphify está desactualizado: desde built_at_commit cambiaron archivos "
            "fuera de graphify-out/. Regenera el grafo después del commit de código."
        )
    report = project / "graphify-out" / "GRAPH_REPORT.md"
    if report.exists() and built[:8] not in report.read_text(encoding="utf-8"):
        raise ProjectCloseError(
            "GRAPH_REPORT.md no identifica el mismo snapshot que graph.json."
        )


def _git(project: Path, *args: str) -> str:
    env = os.environ.copy()
    env.update({"GIT_PAGER": "cat", "GIT_TERMINAL_PROMPT": "0"})
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=project,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ProjectCloseError("Git no está instalado o no está disponible.") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout).strip()
        raise ProjectCloseError(
            f"Falló git {' '.join(args)}" + (f": {detail}" if detail else ".")
        ) from exc
    return result.stdout.strip()


def _git_optional(project: Path, *args: str) -> str | None:
    try:
        return _git(project, *args)
    except ProjectCloseError:
        return None
