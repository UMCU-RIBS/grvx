```JSON
{
 "paths": {
  "input": "/Fridge/users/giovanni/projects/grvx_tmp/subjects",
  "freesurfer_subjects_dir": null,
  "output": "/Fridge/users/giovanni/projects/grvx_tmp/output/pkg_dpss"
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
   "taper": "dpss",
   "duration": 1
  },
  "ecog_compare": {
   "frequency": [65, 95],
   "baseline": false,
   "method": "3c",
   "measure": "zstat"
  }
 },
 "fmri": {
  "read": {
   "active_conditions": [
       "move"
   ]
  },
  "fmri_compare": {
   "measure": "zstat",
   "normalize_to_mean": true
  },
  "upsample": false,
  "graymatter": true,
  "at_elec": {
   "distance": "gaussian",
   "kernel_start": 1,
   "kernel_end": 20,
   "kernel_step": 0.25
  }
 },
 "corr": {
  "pvalue": 0.05
 },
 "plot": {
  "surface": {
    "kernel": 8
  }
 }
}
```

# Parameters

- `paths`
  - `input`:
  - `freesurfer_subjects_dir`:
  - `output`:
- **`plot`**
  - **`surface`**:
    - **`kernel`**: size of the kernel to use to compute smoothing for the surface plot of BOLD data

