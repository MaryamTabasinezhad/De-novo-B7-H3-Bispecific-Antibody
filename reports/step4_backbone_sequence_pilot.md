# Step 4–5 RFantibody/ProteinMPNN pilot plan

Status: approved scope, documentation only; no pilot jobs launched under this
plan. Updated 2026-09-25.

## Purpose

Run a meaningful pilot to test docking productivity, CDR geometry, sequence
diversity, and early structural plausibility before any production-scale
campaign. The pilot treats Arm A and Arm B as independent discovery problems.

## Approved scope

| Component | Arm A | Arm B |
|---|---|---|
| Target definition | Exposed IgV1 FG-loop region, 8H9-like; anchors 126–129 | Exposed IgC1 patch 2, Q228–R241 neighborhood; anchors 228, 229, 232, 234, 236, 238, 240, 241 |
| RFantibody backbone target | 100–300 designs per active epitope/hotspot definition | 100–300 designs per active epitope/hotspot definition |
| ProteinMPNN sequences | Approximately 4 per retained backbone | Approximately 4 per retained backbone |
| RF2 validation | All deduplicated pilot sequences that pass sequence/format QC | All deduplicated pilot sequences that pass sequence/format QC |

The current first pilot scope contains one active Arm A definition and one
active Arm B definition. Any additional anchor or hotspot definition must be
listed in the run manifest before execution; the 100–300 range applies to each
definition that is actually run.

Expected upper-bound scale for the current two-definition pilot is 200–600
backbones and approximately 800–2,400 ProteinMPNN sequences before downstream
filtering. These are planning bounds, not completed outputs.

## Stage rules

### RFantibody backbones

- Keep the human H/L framework and HLT chain convention fixed for the core
  comparison.
- Preserve canonical-to-target residue mappings and the broad structural context
  around each epitope.
- Record seed, anchor definition, CDR lengths, input crop, model/checkpoint,
  output ID, and QC disposition for every design.
- Retain productive docking orientations and CDR geometry; reject malformed,
  undocked, framework-disrupting, or severely clashing structures.
- Preserve diversity across seeds, poses, anchor definitions, and CDR geometry;
  do not select only the top model score.

### ProteinMPNN sequences

- Design only the approved CDR positions and preserve framework positions.
- Generate approximately four sequences per retained backbone for this pilot.
- Record sequence score, sampling settings, seed, parent backbone, exact
  mutation lineage, numbering, and liability flags.
- Deduplicate exact sequences while retaining all parent/backbone provenance.
- Apply sequence-format and preliminary liability review before RF2.

### RF2 structural validation

- Run RF2 independently for each retained sequence–target complex.
- Apply the shared H/L–T chain and heavy-atom geometry checker.
- Inspect target-chain movement, chain numbering, interface contacts, and severe
  overlaps; pLDDT is confidence evidence, not affinity.
- Do not advance a candidate with unresolved severe coordinate artifacts.

## Promotion gates

1. **Input gate:** target chain, hotspot mapping, H/L/T labels, continuity, and
   provenance pass.
2. **Backbone gate:** productive docking, acceptable CDR geometry, no severe
   antibody–target overlap, and sufficient structural diversity.
3. **Sequence gate:** valid numbering, allowed-position changes only, no
   unexplained severe liability, and preserved parent provenance.
4. **RF2 gate:** structurally plausible output, recovered target region, and no
   unresolved severe heavy-atom overlap.

No pilot candidate is a confirmed binder. The pilot does not establish
internalization, Fc-mediated killing, aggregation behavior, or clinical
benefit. Whole human IgG-like 1A+1B assembly remains downstream of arm-level
validation.

## Relationship to prior diagnostic work

The earlier two-backbone/four-sequence B7-H3 run was a setup and diagnostic
pilot, not this approved breadth pilot. Its four RF2 outputs remain excluded
from ranking because of coordinate overlaps. The official RF2 control passed,
and the current pilot is intended to assess productive design distributions at
the approved scale using the accepted toolchain.

## Planned durable outputs

- `work/04_rfantibody_backbones/A/` and `B/`
- `work/04_rfantibody_backbones/design_manifest.csv`
- `work/04_rfantibody_backbones/pilot_summary.md`
- `work/05_proteinmpnn_sequences/A_sequences.qv` and `B_sequences.qv`
- `work/05_proteinmpnn_sequences/sequence_metadata.csv`
- `work/06_structure_predictions/rf2/`
- Pilot QC tables and status updates in `reports/status.md`

No production-scale campaign is implied until the pilot completion gates are
reviewed.
