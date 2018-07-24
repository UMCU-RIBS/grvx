from json import load
from pathlib import Path

PROJECT = 'grvx'

HOME = Path('/Fridge/users/giovanni')

PROJECT_PATH = HOME / 'projects' / PROJECT
SCRIPTS_PATH = PROJECT_PATH / 'scripts'
GROUP_PATH = PROJECT_PATH / 'group'
DATA_PATH = PROJECT_PATH / 'subjects'
DERIVATIVES_PATH = PROJECT_PATH / 'derivatives'
LOG_PATH = GROUP_PATH / 'log'
LOGSRC_PATH = LOG_PATH / 'src'

# All parameters should be read in this module, for consistency
PARAMETERS_PATH = SCRIPTS_PATH / 'parameters.json'
with PARAMETERS_PATH.open('r') as f:
    PARAMETERS = load(f)


LOGSRC_PATH.mkdir(parents=True, exist_ok=True)
DATA_PATH.mkdir(parents=True, exist_ok=True)
DERIVATIVES_PATH.mkdir(parents=True, exist_ok=True)


# DERIVATIVES -----------------------------------------------------------------#
FREESURFER_PATH = DERIVATIVES_PATH / 'freesurfer'
FREESURFER_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = DERIVATIVES_PATH / 'report'
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
NIPYPE_PATH = DERIVATIVES_PATH / 'nipype'
NIPYPE_PATH.mkdir(parents=True, exist_ok=True)
