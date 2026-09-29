# AlphaFold 3 Arm A pilot result

- Source RF2 structure: `rfantibody_b7h3_rf2_20260926/A/task_265/ab_0_dldesign_1_best.pdb`
- AF3 input chains: H (114 aa), L (105 aa), T (84 aa)
- Seeds: 101 and 202
- Diffusion samples per seed: 2
- Recycles: 3
- Slurm job: 21972327 array task 0
- Runtime: 36:49 on H100 node `rg21704`
- Status: completed successfully

The four sample ranking scores are in `armA_task265/armA_task265/armA_task265_ranking_scores.csv`; AF3 confidence JSON and model mmCIF files are retained in the seed directories. These are computational validation outputs, not experimental affinity or activity measurements.
