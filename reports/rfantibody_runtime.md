# RFantibody runtime record

Provisioning authorized by the user on 2026-09-21. The official
[RosettaCommons/RFantibody](https://github.com/RosettaCommons/RFantibody) source
was cloned outside the repository at scratch commit `8fe311415754e0276d1a39c87c57e69c88927a2d`.
An isolated `uv` environment was created under scratch with RFantibody 1.0.0,
PyTorch 2.3.1 + CUDA 11.8, DGL 2.4.0+cu118, and the declared dependencies.

The official model weights are now present under the scratch RFantibody
`weights/` directory: RFdiffusion_Ab, ProteinMPNN, RF2_ab, and the RF2
no-framework training-parameter file. Weights and environments are excluded
from Git. GPU job 21526195 reached an H100 but failed because `uv run` tried to
reach the DGL index from a compute node; the job was corrected to call the
installed `.venv` executables directly. Smoke job 21526260 is pending on
`gpubase_bygpu_b1` under `def-ghaedi_gpu`.

Project inputs prepared in scratch from the approved pair: a 12-A spatial crop
for Arm A hotspots T126–T129, a 12-A spatial crop for Arm B hotspots
T228/T229/T232/T234/T236/T238/T240/T241, and the official hu-4D5-8 Fv HLT
framework. The preparation implementation is tracked in
`tools/prepare_rfantibody_inputs.py`.

The corrected GPU smoke test completed successfully as job **21526260** on an
H100: PyTorch reported CUDA 11.8, CUDA was available, and the RFantibody CLI
loaded. The first smoke attempt (21526195) failed only because `uv run` tried to
resolve the DGL index from the compute node; the direct `.venv` invocation is
now used. Pilot job 21526329 reached the GPU but exposed a wrapper PATH issue
(the subprocess called system Python and could not import Hydra). The corrected
two-arm RFdiffusion pilot (two backbones per arm) is queued as job **21526409**
on `gpubase_bygpu_b1` with the virtual environment first on PATH.
