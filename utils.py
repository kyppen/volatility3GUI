import platform

import subprocess
import shutil


def get_python_command():
    python_cmd = shutil.which('python')
    if python_cmd:
        result = subprocess.run([python_cmd, '--version'], capture_output=True, text=True)
        if 'Python 3' in result.stdout:
            return 'python'

    python3_cmd = shutil.which('python3')
    if python3_cmd:
        result = subprocess.run([python3_cmd, '--version'], capture_output=True, text=True)
        if 'Python 3' in result.stdout:
            return 'python3'

    raise RuntimeError('No suitable Python 3 interpreter found')
