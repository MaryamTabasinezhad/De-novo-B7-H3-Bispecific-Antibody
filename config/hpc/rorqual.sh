#!/usr/bin/env bash
# Source from an analysis shell or SLURM script; no installs or module changes.
# Project root follows this file, so another checkout uses its own data/results.
export MAB_PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
export MAB_CLUSTER=rorqual
export MAB_CPU_ACCOUNT=def-ghaedi_cpu
export MAB_GPU_ACCOUNT=def-ghaedi_gpu
export MAB_APPTAINER_MODULE=apptainer/1.4.5
export MAB_SKILLS_DIR="$MAB_PROJECT_ROOT/skills"
export MAB_DATA_DIR="$MAB_PROJECT_ROOT/data"
export MAB_RESULTS_DIR="$MAB_PROJECT_ROOT/results"
export MAB_REPORTS_DIR="$MAB_PROJECT_ROOT/reports"
export MAB_MODELS_DIR="${MAB_MODELS_DIR:-$MAB_PROJECT_ROOT/models}"
export MAB_SCRATCH_ROOT="${MAB_SCRATCH_ROOT:-/scratch/ghaedi/mab}"
export MAB_WORK_DIR="${MAB_WORK_DIR:-$MAB_SCRATCH_ROOT/work}"
export MAB_CACHE_DIR="${MAB_CACHE_DIR:-$MAB_SCRATCH_ROOT/cache}"
export MAB_TMP_DIR="${SLURM_TMPDIR:-$MAB_SCRATCH_ROOT/tmp}"
# Map tool-specific cache/TMP variables only in jobs that need them. No changes
# to HOME, PATH, CUDA_VISIBLE_DEVICES, TMPDIR, or other projects' environments.
# RFantibody, ProteinMPNN, RF2, AF3, RF3, Rosetta paths remain unset until found.
