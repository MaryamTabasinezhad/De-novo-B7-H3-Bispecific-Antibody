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
export CMAKE_ARGS="-DFETCHCONTENT_SOURCE_DIR_PYBIND11=$DEPS/pybind11 -DFETCHCONTENT_SOURCE_DIR_ABSEIL-CPP=$DEPS/abseil-cpp -DFETCHCONTENT_SOURCE_DIR_PYBIND11_ABSEIL=$DEPS/pybind11_abseil -DFETCHCONTENT_SOURCE_DIR_CIFPP=$DEPS/cifpp -DFETCHCONTENT_SOURCE_DIR_DSSP=$DEPS/dssp -DFETCHCONTENT_SOURCE_DIR_MY-EIGEN3=$DEPS/my-eigen3 -DFETCHCONTENT_SOURCE_DIR_BOOST-RX=$DEPS/boost-rx -DFETCHCONTENT_SOURCE_DIR_LIBMCFP=$DEPS/libmcfp -DCIFPP_DOWNLOAD_CCD=OFF"
cd "$AF3"
"$UV" sync --no-dev --no-install-project --offline
"$UV" pip install --offline --python "$AF3/.venv/bin/python" scikit-build-core pybind11==2.12.0 'cmake>=3.28' ninja setuptools_scm
"$UV" sync --no-dev --no-build-isolation --offline
"$UV" run python run_alphafold_data_test.py
printf 'alphafold3_install_complete commit=%s venv=%s\n' "$(git rev-parse HEAD)" "$AF3/.venv"
