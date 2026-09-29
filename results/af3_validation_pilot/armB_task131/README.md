# AlphaFold 3 Arm B pilot result

- Source RF2 structure: `rfantibody_b7h3_rf2_20260926/B/task_131/ab_0_dldesign_1_best.pdb`
- AF3 input chains: H (118 aa), L (105 aa), T (94 aa)
- Seeds: 101 and 202
- Diffusion samples per seed: 2
- Recycles: 3
- Slurm job: 21972327 array task 1
- Runtime: 1:01:22 on H100 node `rg31701`
- Status: completed successfully

The four sample ranking scores are in `armB_task131/armB_task131/armB_task131_ranking_scores.csv`; AF3 confidence JSON and model mmCIF files are retained in the seed directories. These are computational validation outputs, not experimental affinity or activity measurements.
