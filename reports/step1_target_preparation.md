# Step 1 — target-preparation result

Date: 2026-09-21. The existing project worker was run with
`source config/hpc/rorqual.sh; module load scipy-stack/2023b`.

## Produced inputs and checks

The run used human UniProt Q5ZPR3 sequence/feature data, AlphaFold DB models
for Q5ZPR3 and Q5ZPR3-2, and RCSB structures 9LY5, 9LY6, and 9LME. It produced
`metadata/target_features.json`, `metadata/structure_manifest.csv`,
`metadata/numbering_map.csv`, mapped/oriented PDB files under
`data/processed/target_ensemble/`, and `work/01_target_preparation/ensemble_qc.csv`.

The canonical 4Ig record retains extracellular residues 29–466, the
transmembrane span 467–487, cytoplasmic residues 488–534, and six annotated
N-linked glycosylation sites (104, 189, 215, 322, 407, 433). Experimental
target chains were mapped to canonical numbering and placed into the common
AlphaFold-derived membrane frame. Resolved-glycan and unglycosylated controls
were emitted for the experimental structures.

## Required limitation

The short Q5ZPR3-2 sequence is a 2Ig comparison isoform with an isoform-specific
hydrophobic membrane span around residues 250–271; it must be mapped and
oriented using its own numbering rather than the canonical 4Ig 467–487
coordinates. Its generated file is therefore a membrane 2Ig comparison model,
not a soluble-antigen model. Soluble/shed B7-H3 remains a separate antigen
state. The 9LME affinity tag was also removed from canonical alignment: model
residue 29 onward is anchored to canonical residue 29 onward, yielding a
corrected target range of canonical 29–240 for the resolved partial chain. This
does not affect the required native cell-surface 4Ig baseline.

Representative modeled glycoforms, loop repair/relaxation, 4Ig oligomer
hypotheses, and a validated membrane-tilt ensemble were not fabricated. The
current 4Ig files are suitable for preliminary surface/epitope analysis, but
the full Step 1 gate remains conditional on those limitations being addressed
or explicitly accepted for the next analysis.

No antibody sequence design, installation, or compute job was performed.
