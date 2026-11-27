"""Smoke checks for the local configuration and development setup."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "configs.example"


@pytest.mark.parametrize("config_mode", ["default", "absolute", "relative"])
def test_example_configuration_can_be_loaded(tmp_path, config_mode):
    env = {**os.environ, "SCRIPT_DIR": str(tmp_path)}
    env.pop("CONFIGS_DIR", None)
    config_dir = tmp_path / (
        "configs" if config_mode == "default" else "configs-custom"
    )
    shutil.copytree(EXAMPLE, config_dir)
    if config_mode == "absolute":
        env["CONFIGS_DIR"] = str(config_dir)
    elif config_mode == "relative":
        env["CONFIGS_DIR"] = os.path.relpath(config_dir, ROOT)
    script = """
from pathlib import Path
from src.config import settings
from src.helper import expand_settings_variable

assert settings.default.tioj_url == ''
assert settings.default.tioj_username == ''
assert settings.default.tioj_password == ''
assert settings.path.sample == 'tests/0-*'
assert settings.path.public_sample == 'public/examples/*'
for field in ('metadata_schema', 'solutions_schema', 'subtasks_schema'):
    assert Path(expand_settings_variable(settings.default[field])).is_file()
"""
    subprocess.run([sys.executable, "-c", script], cwd=ROOT, env=env, check=True)


def test_cli_help_does_not_require_local_credentials(monkeypatch):
    from typer.testing import CliRunner

    import tioj

    def unexpected_login(*args, **kwargs):
        pytest.fail("Help must not log in to TIOJ")

    monkeypatch.setattr(tioj, "open_session", unexpected_login)
    result = CliRunner().invoke(tioj.app, ["--help"])
    assert result.exit_code == 0
    assert "upload-problem" in result.stdout
