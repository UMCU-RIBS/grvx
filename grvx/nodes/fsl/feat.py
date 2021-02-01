from pathlib import Path
from nibabel import load as niload

from bidso import Task
from bidso.utils import replace_underscore, read_tsv, replace_extension

DESIGN_TEMPLATE = Path(__file__).resolve().parents[1] / 'data/design_template.fsf'


def prepare_design(func, anat, output_dir):
    """You should set remove_unnecessary_outputs to False, otherwise it removes
    the events.tsv file
    """

    task = Task(func)

    events_fsl = output_dir / task.events.filename.name
    _write_events(task.events.filename, events_fsl)

    # collect info
    img = niload(str(task.filename))
    n_vols = img.header.get_data_shape()[3]
    tr = img.header['pixdim'][4]  # Not sure it it's reliable

    with DESIGN_TEMPLATE.open('r') as f:
        design = f.read()

    feat_dir = output_dir / replace_extension(Path(task.filename).name, '.feat')

    design_values = {
        'XXX_OUTPUTDIR': str(feat_dir),
        'XXX_NPTS': str(n_vols),
        'XXX_TR': str(tr),
        'XXX_FEAT_FILE': str(task.filename),
        'XXX_HIGHRES_FILE': str(anat),
        'XXX_EV1': 'active',
        'XXX_TSVFILE': str(events_fsl),
        }

    for pattern, value in design_values.items():
        design = design.replace(pattern, value)

    subj_design = output_dir / replace_underscore(Path(task.filename).name, 'design.fsf')

    with subj_design.open('w') as f:
        f.write(design)

    return subj_design


def _write_events(events_input, events_output):
    """
    TODO
    ----
    EVENTS should be in PARAMETERS
    """
    EVENTS = (
        'move',
        'verbgen',
        'music',
        )

    tsv = read_tsv(events_input)
    with events_output.open('w') as f:
        for event in tsv:
            if event['trial_type'] in EVENTS:
                f.write(f'{event["onset"]}\t{event["duration"]}\t1\n')
