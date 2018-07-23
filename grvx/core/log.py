from datetime import datetime
from functools import wraps
from logging import (DEBUG,
                     INFO,
                     FileHandler,
                     Formatter,
                     getLogger,
                     StreamHandler)
from pprint import pformat
from socket import gethostname
from subprocess import check_output
from shutil import rmtree

from .constants import LOGSRC_PATH, PROJECT, IMAGES_PATH, PARAMETERS

import grvx
MODULE = grvx


def git_hash(package):
    """Return git log including hash, log message, and local date and time"""
    package_path = package.__path__[0] + '/../.git'
    log_msg = check_output("git --git-dir " + package_path +
                           " log --pretty='%t %s (%ad)' --date=local -1",
                           shell=True).decode('utf-8')
    return log_msg.strip()


def git_info(lg):

    lg.info('{}: {} '.format(PROJECT, git_hash(MODULE)))
    lg.info(check_output('pip freeze', shell=True).decode('utf-8'))


def with_log(function):
    """lg.info goes onto the screen and in the file.
    lg.debug goes into the file only (e.g. for plotly figures)
    print goes only onto the screen.
    """
    @wraps(function)
    def add_log():
        log_file = LOGSRC_PATH / (function.__name__ + '.md')
        if log_file.exists():
            log_file.unlink()

        images_dir = IMAGES_PATH / function.__name__
        try:
            rmtree(str(images_dir))
        except (FileNotFoundError, OSError):
            pass
        images_dir.mkdir(parents=True, exist_ok=True)

        lg = getLogger('boavus')
        lg.setLevel(DEBUG)

        FORMAT = '{asctime:<10}{module:<20}(l.{lineno: 6d}): {message}'
        DATE_FORMAT = '%H:%M:%S'
        formatter = Formatter(fmt=FORMAT, datefmt=DATE_FORMAT, style='{')

        lg.handlers = []

        fh = FileHandler(str(log_file))
        fh.setFormatter(formatter)
        lg.addHandler(fh)

        ch = StreamHandler()
        ch.setFormatter(formatter)
        lg.addHandler(ch)

        """Use external script for plotly"""
        plotly_js_script = '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>'
        lg.info(plotly_js_script)

        lg.info('# {}'.format(function.__name__.replace('_', ' ')))

        git_info(lg)

        lg.info(pformat(PARAMETERS, indent=2))

        lg.info('## Started')
        t0 = datetime.now()
        lg.info('{} on {}'.format(t0.strftime('%Y-%m-%d %H:%M:%S'),
                                  gethostname()))

        output = function(lg, images_dir)

        lg.info('## Finished')
        t1 = datetime.now()
        lg.info('{} after {}'.format(t1.strftime('%Y-%m-%d %H:%M:%S'),
                                     str(t1 - t0)[:-7]))

        fh.close()

        with open(str(log_file), 'r') as f:
            s = f.read()
        s = s.replace('\n#', '\n\n#')
        with open(str(log_file), 'w') as f:
            f.write(s)

        return output

    return add_log
