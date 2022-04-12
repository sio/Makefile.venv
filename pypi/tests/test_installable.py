import pytest

from subprocess import run
from pathlib import Path

import Makefile_venv


def test_makefile_is_installed():
    makefile = Path(Makefile_venv.path())
    assert makefile.name == 'Makefile.venv'
    assert makefile.exists()
    with open(makefile, 'r') as f:
        content = f.read()
        assert 'SEAMLESSLY MANAGE PYTHON VIRTUAL ENVIRONMENT WITH A MAKEFILE' in content


def test_shell_entrypoint():
    shell = run(['Makefile.venv'], capture_output=True, check=True, text=True, shell=True)
    assert Makefile_venv.path() == shell.stdout.strip()
