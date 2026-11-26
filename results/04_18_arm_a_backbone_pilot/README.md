# 04_18 — Arm A seeded backbone pilot

Submitted the first three seeds from the [04_17 plan](../04_17_arm_a_geometry/README.md).
Each runs one backbone with the verified RFantibody checkout
`8fe311415754e0276d1a39c87c57e69c88927a2d`, `RFdiffusion_Ab.pt`, HLT
framework, Q5ZPR3 4Ig AFDB v6 crop 29–169 and anchors T126–T129. The
existing worker now accepts optional counts, loop lengths, and start index.
Deterministic mode uses the start index as the seed for the first design.
The worker retains 50 diffusion steps, final step 1, and no trajectories.

| Seed | H3 / L1 / L3 | Slurm job | Scratch output under `04_18_arm_a_backbone_pilot/A/` |
| --- | --- | --- | --- |
| 101 | 6 / 9 / 9 | 27715194 | `27715194/ab_101.{pdb,trb}` |
| 201 | 9 / 11 / 10 | 27715195 | `27715195/ab_201.{pdb,trb}` |
| 301 | 12 / 13 / 11 | 27715196 | `27715196/ab_301.{pdb,trb}` |

Scratch root is `/scratch/ghaedi/mab`. Logs are under
`/scratch/ghaedi/mab/04_18_arm_a_backbone_pilot/logs/` as
`mab-arm-a-<seed>_<job>.{out,err}`. Each job uses one 40 GB H100 MIG slice
on `gpubase_bygpu_b1`, four CPUs, and 32 GiB RAM. Submission commands:

```bash
source config/hpc/rorqual.sh
run="$MAB_SCRATCH_ROOT/04_18_arm_a_backbone_pilot"
mkdir -p "$run/logs"
for spec in '101 6 9 9' '201 9 11 10' '301 12 13 11'; do
  read -r seed h3 l1 l3 <<< "$spec"
  sbatch --parsable --job-name="mab-arm-a-$seed" --time=00:30:00 \
    --output="$run/logs/%x_%j.out" --error="$run/logs/%x_%j.err" \
    tools/04_design_sequence/04_12_context_pilot_job.sh A 1 \
    "L1:$l1,L2:7,L3:$l3,H1:7,H2:6,H3:$h3" "$seed" 04_18_arm_a_backbone_pilot
done
```

## Completion and geometry decision

All three jobs completed with exit code 0 in 2:00–3:10 and produced
one PDB and one TRB each. The [scheduler record](04_18_scheduler.psv) and
seed PDBs are preserved here. The original TRBs and logs remain at the
scratch paths above.

The [geometry table](04_18_geometry.tsv) and [pairwise approach angles](04_18_approach_angles.tsv)
compare the poses with A0. All three have the requested loop lengths,
preserve both fixed HLT frameworks, cover every variable-domain Cα, and
have a maximum adjacent Cα distance below 3.86 Å. All avoid sub-2 Å
contacts outside the design crop. Fab clearance uses the four rigid
20G5 placements and membrane proxy from 04_17.

| Seed | Anchor contacts | Fv–antigen pairs below 2 Å | Fab membrane clearance (Å) | Angle from A0 |
| --- | ---: | ---: | ---: | ---: |
| 101 | 1 of 4 | 2 | −29.01 to −27.65 | 62.1° |
| 201 | 4 of 4 | 0 | −24.83 to −24.53 | 55.6° |
| 301 | 3 of 4 | 0 | −5.63 to −5.39 | 71.6° |

Seed 201 is the cleanest protein interface and seed 301 is the closest
to clearing the membrane plane. All three cross the plane across all
four placements. The 10° worst-azimuth tilt also leaves all three with
negative clearance. None shows a solvent-facing exit that clears the
proxy. The tested Fabs come within 13.16–20.85 Å of the closest
transferred first N104 NAG, using two local 9LME placements aligned on
Asn CG/OD1/ND2. This samples only the first sugar at the nearest site.

Hold the remaining nine seeds and sequence design. For a revised
pilot, review 301 as the least-occluded starting geometry. Evaluate
solvent-facing rigid Fv placements around the same FG-loop patch on
intact 4Ig, extending each to a Fab and retaining only placements that
clear the plane, preserve the anchor footprint, and avoid protein
clashes. Use any such placements to assess pose-conditioned backbone
sampling before launching another GPU batch. The current unconditional
worker does not enforce full-Fab membrane clearance. A revised sampling
method has not been run.

To regenerate the geometry metrics, source the Rorqual environment and
run the QC script with the three seed-to-job inputs. Standard output
contains geometry values and standard error lists pairwise angles.

```bash
source config/hpc/rorqual.sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  "$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/04_design_sequence/04_18_arm_a_backbone_qc.py \
  101:27715194 201:27715195 301:27715196
```
