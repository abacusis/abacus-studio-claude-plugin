"""Locate setup's private Python environment without installing packages."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys


def find_helper_python():
    if importlib.util.find_spec('keyring') is not None:
        return Path(sys.executable)
    root = Path.home() / '.abacus-studio' / 'venv'
    for candidate in (root / 'Scripts' / 'python.exe', root / 'bin' / 'python3', root / 'bin' / 'python'):
        if not candidate.is_file():
            continue
        try:
            check = subprocess.run([str(candidate), '-c', 'import keyring'],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   timeout=15, check=False)
        except (OSError, subprocess.TimeoutExpired):
            continue
        if check.returncode == 0:
            return candidate
    raise ValueError('Studio helper Python environment is missing or incomplete. '
                     'Run workspace setup to repair ~/.abacus-studio/venv with the bundled requirements.')


def ensure_helper_runtime(script, arguments):
    interpreter = find_helper_python()
    # Do not resolve the executable symlink: that would lose the venv context.
    if os.path.abspath(str(interpreter)) != os.path.abspath(sys.executable):
        os.execv(str(interpreter), [str(interpreter), str(script), *arguments])
