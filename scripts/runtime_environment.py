"""Select an installed Studio-required Node runtime without changing global settings."""
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def environment(config):
    env = os.environ.copy()
    requirements = config.get('runtime_requirements', [])
    if isinstance(requirements, str):
        requirements = requirements.splitlines()
    node = next((str(value) for value in requirements if re.match(r'^node\b', str(value), re.I)), None)
    if not node:
        return env
    match = re.fullmatch(r'node\s+(\d+)(?:\.\d+(?:\.\d+)?)?', node.strip(), re.I)
    if not match:
        raise ValueError('Studio must specify a Node requirement such as node 22.')
    major = int(match.group(1))
    home = Path.home()
    candidates = [shutil.which('node')]
    candidates += list((home / '.nvm/versions/node').glob('v*/bin/node'))
    candidates += list((home / '.local/share/fnm/node-versions').glob('v*/installation/bin/node'))
    if os.environ.get('NVM_HOME'):
        candidates += list(Path(os.environ['NVM_HOME']).glob('v*/node.exe'))
    for candidate in candidates:
        if not candidate or not Path(candidate).is_file():
            continue
        try:
            version = subprocess.run([str(candidate), '--version'], capture_output=True, text=True, timeout=5, check=True).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            continue
        if re.match(r'^v' + str(major) + r'\.', version):
            env['PATH'] = str(Path(candidate).parent) + os.pathsep + env.get('PATH', '')
            return env
    raise ValueError(f'Node {major} is required but not installed. Ask permission to install it; do not start with another version.')


if __name__ == '__main__':
    # Managed launches use this wrapper so child processes inherit the selected
    # runtime even when the desktop app was opened with a different shell PATH.
    major, executable, *arguments = sys.argv[1:]
    env = environment({'runtime_requirements': ['node ' + major]})
    raise SystemExit(subprocess.call([executable, *arguments], env=env))
