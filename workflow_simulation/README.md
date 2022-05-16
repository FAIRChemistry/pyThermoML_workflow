# workflow_simulation

This directory describes external needed to start the `MixtureMM` workflow.
---
The used molecules can be found in `molecules`.
---
The OpenMM readable force fields used are available in `force_fields` directory.
* Water: `tip4p-fb.xml`
* Methanol: `trappe_methanol.xml`
* Glycerol: `blieck_egorov.xml`
---
The jupyter-notebooks `Water_Methanol_HoreKa.ipynb`and `Water_Glycerol_HoreKa.ipynb` were used to create job-submission for HoreKA high-performance computing locally. The job-submissions were then executed on HoreKa. The jupyter-notebooks should only illustrate the used simulation input parameters and methods used of `MixtureMM` and are not executable. For setting your own simulation refer to [MixtureMM](https://coldcoffee97.github.io/mixturemm/). 
