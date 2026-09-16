# Rorqual analysis environment

Verified 2026-09-16 on login host `rorqual2`, cluster `rorqual`.

```bash
source config/hpc/rorqual.sh
```

Source this in each analysis shell and SLURM script. It exports project-scoped
`MAB_*` paths and accounts without installing anything or changing shell startup
files. Codex must source it before analysis commands; sourcing once in a separate
tool call cannot configure later processes. Create only the directories needed
by the current analysis with `mkdir -p`. Scratch defaults are reserved locations,
not claims that data or models have been downloaded.

| Setting | Value / meaning |
|---|---|
| Project | Root derived from environment file; current resolved root `/project/def-ghaedi/ghaedi/mab` |
| CPU account | `def-ghaedi_cpu` |
| GPU account | `def-ghaedi_gpu` |
| Scratch | `/scratch/ghaedi/mab`, with work/cache/tmp beneath it |
| Durable files | `data/`, `results/`, `reports/`, and optional `models/` under project root |
| Temporary job files | `MAB_TMP_DIR` prefers `SLURM_TMPDIR` inside an allocation |
| Container module | `apptainer/1.4.5`; load explicitly when needed |

## Observed capabilities

- `sbatch`, `squeue`, `sacct`, `sinfo`, and `srun` are available. Account names above
  come from `sacctmgr -n -P show assoc where user=ghaedi format=Account%40,Partition%40`.
- `sinfo` reports CPU partitions and H100 GPU partitions, including MIG slices.
  Choose resources for the analysis; no fixed partition, GPU count, or memory
  request is imposed. Recheck current availability at submission time.
- `StdEnv/2023` is loaded. Default Python is 3.11.4. Modules advertise Python
  3.11.5 and other versions, CUDA, RDKit, HMMER, and `hmmer-alphafold3/3.4`.
  A HMMER module is not an AlphaFold installation.
- `module load apptainer/1.4.5; apptainer --version` returned version 1.4.5.
  It was not initially on PATH; the environment file does not load it globally.
- Default Python can locate `requests` and `yaml`; it cannot locate `numpy`,
  `pandas`, `matplotlib`, `Bio`, `torch`, or `rdkit`. Other environments/modules
  may provide them; check the selected environment for each analysis.
- Login-node GitHub access worked. No compute-node network or GPU inference test
  was performed, and no scientific jobs were submitted for this setup.

## Unresolved scientific runtime paths

RFantibody/RFdiffusion, ProteinMPNN, RF2, AlphaFold 3, RF3, Rosetta, antibody
numbering tools, model weights, and large reference datasets have not been
located or verified. No working predictors were found on the inspected PATH.
Do not fill in invented paths or use another project's containers by assumption.
Inspect relevant modules or user-provided locations when a method is needed;
report a missing dependency before that stage. Installing skills does not install
these programs. No new packages, environments, containers, or models were installed.

Use `sbatch --account="$MAB_CPU_ACCOUNT" ...` for CPU jobs or
`sbatch --account="$MAB_GPU_ACCOUNT" ...` with explicit GPU resources for GPU jobs.
This profile is not an automatic batch submitter.
