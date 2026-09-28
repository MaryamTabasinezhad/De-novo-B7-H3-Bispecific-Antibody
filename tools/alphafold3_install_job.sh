#!/usr/bin/env bash
#SBATCH --job-name=mab-af3-install
#SBATCH --account=def-ghaedi_cpu
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/scratch/ghaedi/mab/jobs/alphafold3_install_%j.out
#SBATCH --error=/scratch/ghaedi/mab/jobs/alphafold3_install_%j.err

set -euo pipefail
source /lustre09/project/6089454/ghaedi/mab/config/hpc/rorqual.sh
module load StdEnv/2023
module load python/3.12.4
export CMAKE_BUILD_PARALLEL_LEVEL="${SLURM_CPUS_PER_TASK}"
AF3="$MAB_SCRATCH_ROOT/alphafold3_src"
UV="$MAB_SCRATCH_ROOT/uv"
DEPS="$MAB_SCRATCH_ROOT/alphafold3_deps"
export FETCHCONTENT_SOURCE_DIR_PYBIND11="$DEPS/pybind11"
export FETCHCONTENT_SOURCE_DIR_ABSEIL_CPP="$DEPS/abseil-cpp"
export FETCHCONTENT_SOURCE_DIR_PYBIND11_ABSEIL="$DEPS/pybind11_abseil"
export FETCHCONTENT_SOURCE_DIR_CIFPP="$DEPS/cifpp"
export FETCHCONTENT_SOURCE_DIR_DSSP="$DEPS/dssp"
cd "$AF3"
"$UV" sync --no-dev
"$UV" run python run_alphafold_data_test.py
printf 'alphafold3_install_complete commit=%s venv=%s\n' "$(git rev-parse HEAD)" "$AF3/.venv"
