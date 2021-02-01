
{
 "paths": {
  "input": "",
  "freesurfer_subjects_dir": null,
  "nipype": "",
  "plots": ""
 },
 "corr": {
  "pvalue": 0.05
 },
 "fmri": {
  "read": {
   "active_condition": [
       "move"
   ]
  },
  "fmri_compare": {
   "measure": "zstat",
   "normalize_to_mean": true
  },
  "at_elec": {
   "distance": "gaussian",
   "kernel_start": 1,
   "kernel_end": 20,
   "kernel_step": 0.25
  },
  "upsample": false,
  "graymatter": true
 },
 "ieeg": {
  "read": {
   "active_conditions": [
       "move"
   ],
   "baseline_conditions": [
       "rest"
   ],
   "minimalduration": 20
  },
  "preprocess": {
   "duration": 2,
   "reref": "average",
   "offset": false
  },
  "powerspectrum": {
   "method": "spectrogram",
   "taper": "hann",
   "duration": 1
  },
  "ecog_compare": {
   "frequency": [8, 12],
   "baseline": false,
   "measure": "zstat",
   "method": "3c"
  }
 }
}
