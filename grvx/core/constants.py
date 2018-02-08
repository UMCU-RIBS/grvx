from collections import OrderedDict
from json import dump, load
from os import remove
from pathlib import Path
from tempfile import NamedTemporaryFile

PROJECT = 'grvx'

HOME = Path('/Fridge/users/giovanni')

PROJECT_PATH = HOME / 'projects' / PROJECT
SCRIPTS_PATH = PROJECT_PATH / 'scripts'
GROUP_PATH = PROJECT_PATH / 'group'
DATA_PATH = PROJECT_PATH / 'subjects'
DERIVATIVES_PATH = PROJECT_PATH / 'derivatives'
IMAGES_PATH = GROUP_PATH / 'images'
LOG_PATH = GROUP_PATH / 'log'
LOGSRC_PATH = LOG_PATH / 'src'

# All parameters should be read in this module, for consistency
PARAMETERS_PATH = SCRIPTS_PATH / 'parameters.json'
with PARAMETERS_PATH.open('r') as f:
    PARAMETERS = load(f)

def write_parameters(parameters):
    with PARAMETERS_PATH.open('w') as f:
        dump(parameters, f, ensure_ascii=False, indent=' ')


class Parameters_Json:
    def __init__(self, parameters):
        with NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmpfile:
            dump(parameters, tmpfile)

        self.name = tmpfile.name

    def delete(self):
        remove(self.name)


IMAGES_PATH.mkdir(parents=True, exist_ok=True)
LOGSRC_PATH.mkdir(parents=True, exist_ok=True)
DATA_PATH.mkdir(parents=True, exist_ok=True)
DERIVATIVES_PATH.mkdir(parents=True, exist_ok=True)


# FUNCTION NAMES -------------------------------------------------------------#
ALL_FUNC = OrderedDict([
    ('-r', 'Read_As_Bids'),
    ('-s', 'Run_FreeSurfer'),
    ('-f', 'Run_fMRI_feat'),
    ('-t', 'Compare_Feat'),
    ('-p', 'Project_Elec_On_Surf'),
    ('-g', 'Compare_ECoG'),
    ('-e', 'Corr_fMRI_to_Elec'),
    ])


# DERIVATIVES -----------------------------------------------------------------#
FREESURFER_PATH = DERIVATIVES_PATH / 'freesurfer'
FREESURFER_PATH.mkdir(parents=True, exist_ok=True)
ANALYSIS_PATH = DERIVATIVES_PATH / 'analysis'
ANALYSIS_PATH.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = DERIVATIVES_PATH / 'grvx'
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
