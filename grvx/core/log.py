from base64 import b64encode
from datetime import datetime
from functools import wraps
from logging import (DEBUG,
                     INFO,
                     FileHandler,
                     Formatter,
                     getLogger,
                     StreamHandler)
from pprint import pformat
from re import sub
from socket import gethostname
from subprocess import check_output, check_call
from shutil import rmtree

from .constants import (ALL_FUNC, LOG_PATH, LOGSRC_PATH, PROJECT, IMAGES_PATH,
                        PARAMETERS)

import grvx
MODULE = grvx

"""import plotly here, because at least it doesn't show all the warnings
when import ipython and plotly"""
import plotly


def run_pandoc(export='pdf'):
    """Convert log files to html or pdf"""

    t = datetime.now()

    # Prepare pandoc file
    md_files = []
    for func_name in ALL_FUNC.values():
        one_md_file = LOGSRC_PATH / (func_name + '.md')
        if one_md_file.exists():
            md_files.append(str(one_md_file))

    LOGOUTPUT_PATH = LOG_PATH / export
    LOGOUTPUT_PATH.mkdir(exist_ok=True)

    output_name = t.strftime(PROJECT + '_%y%m%d_%H%M%S') + '.' + export
    output_file = str(LOGOUTPUT_PATH / output_name)

    # Convert with pandoc
    cmd = ['pandoc', '-s', '-f', 'markdown+smart', '--toc']
    if export == 'pdf':
        cmd.extend(['-V', 'documentclass=report'])
        cmd.extend(['-V', 'geometry:margin=1cm'])
    cmd.extend(md_files)
    cmd.extend(['-o', output_file])
    check_call(cmd)

    if export == 'html':
        embed_images_in_html(output_file)


def embed_images_in_html(html_file):
    """read images from png file and embed them into the html.

    Parameters
    ----------
    html_file : path to file
        path to html file

    """
    with open(html_file, 'r') as f:
        s = f.read()

    s1 = sub('<img src="([a-zA-Z0-9_/\.]*)" ', _embed_png, s)

    with open(html_file, 'w') as f:
        f.write(s1)


def _embed_png(matched):
    """Take a regex object with img tag and convert the png path to base64 data.

    Parameters
    ----------
    matched : regex match object
        matched regex of the img tag

    Returns
    -------
    str
        string to replace the whole img tag.
    """
    string = matched.group(0)
    image_path = matched.group(1)

    with open(image_path, 'rb') as f:
        image_data = b64encode(f.read()).decode()

    return string.replace(image_path, 'data:image/png;base64,' + image_data)


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


def from_pandas_to_table(df, float_format='%g'):
    """Convert pandas dataframe to markdown table.
    """
    txt = ['',
           '|'.join(df.columns),
           '|'.join(['---'] * len(df.columns)),
           df.to_csv(index=False, header=False,
                     float_format=float_format, sep='|'),
           ]
    return '\n'.join(txt)
