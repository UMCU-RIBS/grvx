from wonambi.attr import Surf, Channels, Freesurfer
from wonambi.viz import Viz3
from numpy import hstack, vstack, array
from bidso.utils import read_tsv

from pathlib import Path

results_dir = Path('/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/corr_fmri_ecog_summary/output/ecog')

results_path = next(results_dir.glob('*.tsv'))
results = read_tsv(results_path)

from bidso import file_Core


r = file_Core(results_path)

fs = Freesurfer(f'/Fridge/users/giovanni/projects/grvx/derivatives/freesurfer/sub-{r.subject}')
brain = fs.read_brain()


electrodes = Electrodes('/Fridge/users/giovanni/projects/grvx/subjects/sub-bunnik/ses-UMCUECOGday04/ieeg/sub-bunnik_ses-UMCUECOGday04_acq-clinicalctmrregions_electrodes.tsv')


labels = electrodes.electrodes.get(map_lambda=lambda x: x['name'])
chan_xyz = array(electrodes.get_xyz())
elec = Channels(labels, chan_xyz - fs.surface_ras_shift)

colors = array([0, 0, 0])  * (results['pvalue'] <= 0.05).astype(float)[:, None]
colors += array([0.8, 0.8, 0.8])  * (results['pvalue'] > 0.05).astype(float)[:, None]

v = Viz3()
# v.add_chan(elec(lambda x: x.label in results['channel']), color=colors)
v.add_surf(brain.lh)
v.add_surf(brain.rh)
