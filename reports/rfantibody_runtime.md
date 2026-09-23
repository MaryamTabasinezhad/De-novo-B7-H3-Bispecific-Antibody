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
two-arm RFdiffusion pilot **21526509** then completed successfully on
`gpubase_bygpu_b1` using a 40-GB H100 MIG resource, with the virtual environment
first on PATH. It produced two backbones for each arm.

The dependent ProteinMPNN **21526896** and RF2 **21526897** pilot jobs also
completed successfully (exit 0). ProteinMPNN produced four sequences per arm;
RF2 produced four predicted structures per arm. RF2 reported “No interface
residues found, not using hotspots” for every input, so these outputs are
runtime/format evidence only and are not accepted as binding designs. The pilot
outputs remain in scratch under `/scratch/ghaedi/mab/rfantibody_pilot/`; a
representative-output review is required before any larger campaign.

Pilot QC identified a likely configuration issue: the first RFdiffusion pilot
overrode the trained diffusion horizon with `diffuser.T=50`; its logs showed
large motif RMSD and the resulting structures had sub-angstrom inter-chain
overlaps. A corrected one-design-per-arm RFdiffusion-only pilot was submitted
as **21563096** using the model default horizon (T=200). It is pending scheduler
priority. No dependent sequence or RF2 job has been submitted for this
corrected pilot.

The tracked official runtime-control job **21666899** was submitted on
2026-09-23 using the RFantibody RSV example and hu-4D5-8 Fv framework. It is
pending scheduler priority; no B7-H3 design job has been submitted while the
control is pending.

Runtime control **21666899** completed successfully (exit 0). The official RSV
example reported motif RMSD 0.13 Å, retained H/L/T chains, and wrote a valid
output structure without runtime errors. The next gated task is a one-design
per-arm B7-H3 RFdiffusion pilot using the corrected input crops.
