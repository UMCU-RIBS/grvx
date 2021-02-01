from wonambi.attr import Surf, Channels, Freesurfer
from numpy import hstack, vstack, array, median
from bidso import Electrodes
from bidso import file_Core
from bidso.utils import read_tsv
from bidso.find import find_in_bids

from pathlib import Path

results_dir = Path('/Fridge/users/giovanni/projects/grvx/derivatives/nipype/grvx/corr_fmri_ecog_summary/output/ecog')
plots_dir = Path('/Fridge/users/giovanni/projects/grvx/derivatives/plots/surfaces')

pvalue = 0.05  # TODO: PARAMETERS


def plot_surfaces():
    for results_path in results_dir.glob('*.tsv'):
        results = read_tsv(results_path)

        r = file_Core(results_path)

        fs = Freesurfer(f'/Fridge/users/giovanni/projects/grvx/derivatives/freesurfer/sub-{r.subject}')
        brain = fs.read_brain()

        electrodes_file = find_in_bids(Path('/Fridge/users/giovanni/projects/grvx/subjects/'), subject=r.subject, acquisition='*alctmrregions', modality='electrodes')
        electrodes = Electrodes(electrodes_file)

        labels = electrodes.electrodes.get(map_lambda=lambda x: x['name'])
        chan_xyz = array(electrodes.get_xyz())
        elec = Channels(labels, chan_xyz - fs.surface_ras_shift)

        colors = array([0, 0, 0]) * (results['pvalue'] <= pvalue).astype(float)[:, None]
        colors += array([0.8, 0.8, 0.8]) * (results['pvalue'] > pvalue).astype(float)[:, None]

        v = Viz3()
        v.add_chan(elec(lambda x: x.label in results['channel']), color=colors)
        if median(chan_xyz[:, 0]) > 0:
            v.add_surf(brain.lh)
            v.add_surf(brain.rh)
            v._view.camera.azimuth = 120
        else:
            v.add_surf(brain.rh)
            v.add_surf(brain.lh)
            v._view.camera.azimuth = -120

        v._view.camera.elevation = 20
        v.save(plots_dir / (r.subject + '.png'))
        v.close()
