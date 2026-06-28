from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from trazabilidad.config import ConfigurationError, load_settings


class SettingsTests(unittest.TestCase):
    def test_environment_takes_precedence(self) -> None:
        with patch.dict(os.environ, {"NOTION_API_KEY": "from-env"}, clear=True):
            settings = load_settings(Path("/missing/key.txt"))
        self.assertEqual(settings.token, "from-env")
        self.assertEqual(settings.credential_source, "NOTION_API_KEY")

    def test_reads_fallback_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            key_file = Path(directory) / "key.txt"
            key_file.write_text(" local-token \n", encoding="utf-8")
            with patch.dict(os.environ, {}, clear=True):
                settings = load_settings(key_file)
        self.assertEqual(settings.token, "local-token")

    def test_reads_utf16_fallback_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            key_file = Path(directory) / "key.txt"
            key_file.write_text("local-token", encoding="utf-16")
            with patch.dict(os.environ, {}, clear=True):
                settings = load_settings(key_file)
        self.assertEqual(settings.token, "local-token")

    def test_reads_public_toml_without_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config_file = Path(directory) / "notion.toml"
            config_file.write_text(
                'api_version = "2026-03-11"\ntimeout_seconds = 7\nmax_retries = 1\n',
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"NOTION_API_KEY": "from-env"}, clear=True):
                settings = load_settings(Path("/missing/key.txt"), config_file)
        self.assertEqual(settings.timeout_seconds, 7)
        self.assertEqual(settings.max_retries, 1)

    def test_missing_credentials_has_safe_error(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigurationError):
                load_settings(Path("/missing/key.txt"))
