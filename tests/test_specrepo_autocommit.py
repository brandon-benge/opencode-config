from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import importlib.machinery
import importlib.util
from io import StringIO
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / "tools" / "specrepo-autocommit.py"
)
LOADER = importlib.machinery.SourceFileLoader("specrepo_autocommit", str(SCRIPT_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
assert SPEC is not None
specrepo_autocommit = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(specrepo_autocommit)


class ConfigPathTests(unittest.TestCase):
    def test_unset_autocommit_params_fails_with_configuration_guide(self) -> None:
        stderr = StringIO()
        with mock.patch.dict(os.environ, {}, clear=True):
            with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
                specrepo_autocommit.get_config_path()

        self.assertEqual(raised.exception.code, 1)
        self.assertIn("AUTOCOMMIT_PARAMS is not set", stderr.getvalue())
        self.assertIn("#config-overrides", stderr.getvalue())

    def test_set_autocommit_params_announces_resolved_location(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "params.yaml"
            config_path.write_text("git: {}\n", encoding="utf-8")
            stdout = StringIO()

            with mock.patch.dict(
                os.environ, {"AUTOCOMMIT_PARAMS": str(config_path)}, clear=True
            ):
                with redirect_stdout(stdout):
                    resolved = specrepo_autocommit.get_config_path()

        self.assertEqual(resolved, config_path.resolve())
        self.assertIn(
            f"AUTOCOMMIT_PARAMS is set to: {config_path.resolve()}",
            stdout.getvalue(),
        )

    def test_missing_config_file_reports_location_and_guide(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "missing.yaml"
            stderr = StringIO()
            stdout = StringIO()

            with mock.patch.dict(
                os.environ, {"AUTOCOMMIT_PARAMS": str(config_path)}, clear=True
            ):
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    with self.assertRaises(SystemExit) as raised:
                        specrepo_autocommit.get_config_path()

        self.assertEqual(raised.exception.code, 1)
        self.assertIn(str(config_path.resolve()), stdout.getvalue())
        self.assertIn(
            f"AUTOCOMMIT_PARAMS location: {config_path.resolve()}",
            stderr.getvalue(),
        )
        self.assertIn("Update that file as needed", stderr.getvalue())
        self.assertIn("#config-overrides", stderr.getvalue())


class ExecutionTests(unittest.TestCase):
    def test_missing_summary_reports_set_config_location(self) -> None:
        config_path = Path("/tmp/params.yaml")
        stderr = StringIO()
        with mock.patch.object(
            specrepo_autocommit, "get_config_path", return_value=config_path
        ):
            with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
                specrepo_autocommit.main(["specrepo-autocommit"])

        self.assertEqual(raised.exception.code, specrepo_autocommit.EX_USAGE)
        self.assertIn("a summary of what changed is required", stderr.getvalue())
        self.assertIn(
            f"AUTOCOMMIT_PARAMS location: {config_path}", stderr.getvalue()
        )

    def test_single_line_summary_reaches_autocommit(self) -> None:
        config_path = Path("/tmp/params.yaml")
        with (
            mock.patch.object(
                specrepo_autocommit, "get_config_path", return_value=config_path
            ),
            mock.patch.object(
                specrepo_autocommit,
                "get_current_branch",
                return_value="feature/python-hook",
            ),
            mock.patch.object(
                specrepo_autocommit,
                "ensure_autocommit_installed",
                return_value="/usr/local/bin/autocommit",
            ),
            mock.patch.object(specrepo_autocommit, "run_autocommit") as run,
        ):
            result = specrepo_autocommit.main(
                ["specrepo-autocommit", "one-line summary"]
            )

        self.assertEqual(result, 0)
        run.assert_called_once_with(
            "/usr/local/bin/autocommit",
            config_path,
            "one-line summary",
            "feature/python-hook",
        )

    def test_main_branch_blocks_without_running_autocommit(self) -> None:
        config_path = Path("/tmp/params.yaml")
        with (
            mock.patch.object(
                specrepo_autocommit, "get_config_path", return_value=config_path
            ),
            mock.patch.object(
                specrepo_autocommit, "get_current_branch", return_value="main"
            ),
            mock.patch.object(
                specrepo_autocommit, "ensure_autocommit_installed"
            ) as install,
        ):
            result = specrepo_autocommit.main(
                ["specrepo-autocommit", "summary"]
            )

        self.assertEqual(result, 0)
        install.assert_not_called()

    def test_config_path_is_passed_to_autocommit(self) -> None:
        config_path = Path("/tmp/config with spaces.yaml")
        completed = subprocess.CompletedProcess([], 0)

        with mock.patch.object(
            specrepo_autocommit.subprocess, "run", return_value=completed
        ) as run:
            specrepo_autocommit.run_autocommit(
                "/usr/local/bin/autocommit",
                config_path,
                "summary",
                "feature/python-hook",
            )

        run.assert_called_once_with(
            [
                "/usr/local/bin/autocommit",
                "--yes",
                "--config-file",
                str(config_path),
                "-c",
                "summary",
            ],
            check=False,
        )

    def test_autocommit_failure_reports_config_location(self) -> None:
        config_path = Path("/tmp/params.yaml")
        completed = subprocess.CompletedProcess([], 7)
        stderr = StringIO()

        with mock.patch.object(
            specrepo_autocommit.subprocess, "run", return_value=completed
        ):
            with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
                specrepo_autocommit.run_autocommit(
                    "/usr/local/bin/autocommit",
                    config_path,
                    "summary",
                    "feature/python-hook",
                )

        self.assertEqual(raised.exception.code, 7)
        self.assertIn("Autocommit failed with exit code 7", stderr.getvalue())
        self.assertIn(
            f"AUTOCOMMIT_PARAMS location: {config_path}", stderr.getvalue()
        )
        self.assertIn("Update that file as needed", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
