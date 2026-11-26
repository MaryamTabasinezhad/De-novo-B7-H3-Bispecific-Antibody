# 04_17 — Arm A Fab geometry and backbone pilot plan

## A1 geometry on intact 4Ig

The [clearance table](04_17_fab_clearance.tsv) uses the existing A0 and A1
backbones from RFantibody job 27635726 and the oriented AFDB v6 canonical
human Q5ZPR3 model. A1 retains all four intended contacts from the prior
4.5 Å screen and approaches 63.7° from A0. Its only Fv–ectodomain atom pair
below 2 Å is H102 carbonyl O against canonical Arg127 backbone carbonyl O
at 1.707 Å. Both atoms are backbone oxygens. Clearing this overlap would
require local backbone or pose movement. A0's Ser125 side-chain rotation
result applies to the separate A0 overlap.

A rigid full-Fab estimate retained the modeled Fv and placed the observed
CH1 and CL atoms of 20G5 from local 9LY5 A/B and 9LY6 B/C coordinates. The
fits jointly aligned the last eight or ten variable-domain Cα atoms per
chain, ending at template VH 118 and VL 106. These fits give 1.26–1.37 Å RMSD.
The template atoms include only resolved coordinates. The two structures
represent the same antibody lineage and sample a limited elbow geometry.

| Pose | Lowest Fv z (Å) | Lowest estimated Fab z (Å) | Fab clearance to membrane proxy (Å) | Closest constant-domain atom to 4Ig ectodomain (Å) |
| --- | ---: | ---: | ---: | ---: |
| A0 | 24.11 | 4.67 to 5.07 | −10.68 to −10.29 | 26.81 |
| A1 | 11.19 | −18.74 to −18.25 | −34.09 to −33.60 | 31.00 |

The membrane proxy is a plane at z = 15.35 Å, the top of the oriented
transmembrane Cα span (canonical 467–487). Negative clearance means
crossing that plane. Even A1's Fv alone extends about 4.16 Å below it.
A 10° worst-azimuth sensitivity check around the TM Cα centroid, with the
same plane offset from that centroid, gives −40.22 to −39.94 Å for A0 and
−52.49 to −52.23 Å for A1. The tilt and plane are geometric assumptions.
Neither establishes native membrane position or Fab elbow flexibility.
The combined models place the closest heavy atom about 20 Å from N104
ND2 in both poses. That is an attachment-site distance. Native glycan
occupancy and full glycoform clearance remain open.

Hold both poses at the geometry gate. Keep A0 as the benchmark for anchor
coverage and the closest existing comparison on membrane clearance. Keep
A1 as a distinct approach and a reference for backbone overlap and membrane
crossing. The constant-domain placements are geometric estimates. The
shared Fab format and assembly details still require confirmation.

Reproduce from the project root with NumPy 1.26.4 and SciPy 1.15.3 in the
existing RFantibody environment:

```bash
source config/hpc/rorqual.sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  "$MAB_SCRATCH_ROOT/third_party/RFantibody/.venv/bin/python" \
  tools/04_design_sequence/04_17_arm_a_fab_clearance.py \
  > results/04_17_arm_a_geometry/04_17_fab_clearance.tsv
```

Inputs include `/scratch/ghaedi/mab/04_12_context_pilot/A/27635726/{target.pdb,ab_0.pdb,ab_1.pdb}`,
`data/processed/target_ensemble/human_4ig_afdb_v6_oriented.pdb`, and the two
local experimental PDBs under `data/raw/structures/`.

## Next Arm A backbone pilot

Plan 12 backbones across three loop configurations within the audited
ranges. Keep the HLT VH/VL scaffold, target crop 29–169, anchors T126–T129,
checkpoint, 50 diffusion steps and final step 1 from the
[expanded-context worker](../../tools/04_design_sequence/04_12_context_pilot_job.sh).
Fix H1/H2/L2 at 7/6/7 residues. Each row reserves four independent seeds
and a distinct output prefix.

| Configuration | H3 / L1 / L3 (residues) | Design indices and seeds |
| --- | --- | --- |
| Short H3 | 6 / 9 / 9 | 101–104 |
| Midlength H3 | 9 / 11 / 10 | 201–204 |
| Long H3 | 12 / 13 / 11 | 301–304 |

The verified checkout accepts `--deterministic --extra inference.design_startnum=N`
and seeds each design with its design index. Reuse the existing crop and
worker settings when preparing the jobs. Log the checkpoint, checkout,
configuration, seed, job ID and output paths.

Replay each pose on intact 4Ig and compare it with A0 under the same checks.

1. Verify fixed VH/VL blocks, Cα coverage and chain continuity. Count
   contacts to each intended anchor at 4.5 Å and inspect all protein
   atom pairs below 2 Å, with outside-crop overlaps identified separately.
2. Estimate full-Fab clearance with the same template and tilt screen.
   Inspect nearby glycosites and any available resolved glycans. Record
   modeled glycan distances and unresolved sites with their evidence.
3. Compare approach angles against A0 and between candidates. Inspect loop
   backbone overlays and anchor-contact patterns before counting distinct
   lineages. Seed and loop length alone do not establish structural diversity.
4. Advance several distinct lineages if they pass the same geometry checks
   and the shared Fab criteria are confirmed. If zero or one qualifies,
   review the dominant failures and revise the next backbone pilot before
   scaling. In particular, assess whether the designs repeatedly point
   their constant domains toward the membrane.

The existing A0 and A1 geometry was reviewed. The 12-backbone pilot is
planned. No Slurm jobs, new backbones or sequence designs were started.
