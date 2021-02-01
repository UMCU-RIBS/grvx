from os import environ, pathsep
from subprocess import CompletedProcess

def _remove_python3_from_PATH(path):
    return pathsep.join(x for x in path.split(pathsep) if 'miniconda' not in x and 'venv/bin' not in x and 'python3' not in x)


ENVIRON = {
    'PATH': _remove_python3_from_PATH(environ.get('PATH', '')),
    }
ENVIRON = {**environ, **ENVIRON}


def check_subprocess(p):
    if p.returncode:

        if isinstance(p, CompletedProcess):
            stdout = p.stdout
            stderr = p.stderr
        else:
            stdout, stderr = p.communicate()

        raise RuntimeError(f'Command \'{" ".join(p.args)}\' failed:\n---stdout---\n{stdout.decode()}------------\n---stderr---\n{stderr.decode()}------------')
