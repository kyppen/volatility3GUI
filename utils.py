import platform

import subprocess
import shutil
import random


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


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def yiq_contrast_color(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    yiq = ((r*299) + (g*587) + (b*114)) / 1000
    return '#000000' if yiq >= 128 else '#ffffff'
def generate_hex_color():
    # Generate random values for R, G, B components
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Format as hex and return
    return f'#{r:02x}{g:02x}{b:02x}'