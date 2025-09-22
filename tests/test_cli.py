import json
import subprocess
import sys
import pytest
from pathlib import Path

from openpyxl.styles.builtins import output

CLI = ["python", "cli/cache_cli.py"]


def test_cli_with_json(tmp_path):
    output_file = tmp_path / "out.json"
    cmd = CLI + ["-H", "http://localhost:8000", "-j", '{"list_1":["x"], "list_2":["y"]}', "-o", str(output_file)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert isinstance(data, list)
    