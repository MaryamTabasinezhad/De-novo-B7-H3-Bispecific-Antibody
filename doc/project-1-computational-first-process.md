# Project 1: Computational-First B7-H3 Biparatopic Antibody Design

## Objective

Design two independent antibodies against distinct human B7-H3/CD276 epitopes, optimize each antibody computationally, combine them as a biparatopic construct, and complete full-construct modeling before experimental testing.

> **Terminology:** Before experimental measurement, the maturation stage is **in-silico affinity optimization**, not confirmed affinity maturation. High affinity cannot be claimed until measured by SPR, BLI, or an equivalent method.

## Current Architecture Assumption

The planned **2A + 2B Fc dimer** corresponds to a tetravalent tandem-scFv-Fc architecture:

```text
(A-scFv–linker–B-scFv)–hinge–Fc
                  │
                  Fc dimer
                  │
(A-scFv–linker–B-scFv)–hinge–Fc
```

This is different from a conventional heterodimeric IgG containing one A Fab and one B Fab, which is normally **1A + 1B**. The architecture must be locked in `config/project.yaml` before fusion modeling.

## Agent Execution Rules

- Record software versions, model weights, commands, parameters, random seeds, input checksums, and output checksums.
- Use human canonical CD276 numbering as the reporting coordinate system.
- Keep experimental contacts, region-defining residues, and computational design anchors in separate fields.
- Do not treat one predicted structure or one score as proof of binding or affinity.
- Never silently replace a missing scientific decision. Write unresolved items to `reports/decision_log.md` and stop at the relevant gate.
- Keep multiple structurally and sequence-diverse candidates through every stage.
- Make every numerical cutoff configurable in `config/filters.yaml`.

## Required Repository Structure

```text
config/
  project.yaml
  epitopes.yaml
  filters.yaml
  compute.yaml
data/
  raw/structures/
  raw/sequences/
  processed/target_ensemble/
  processed/frameworks/
metadata/
  structure_manifest.csv
  residue_ledger.csv
  candidate_regions.csv
  source_library.csv
work/
  01_target_preparation/
  02_epitope_selection/
  03_design_anchors/
  04_rfantibody_backbones/
  05_proteinmpnn_sequences/
  06_structure_predictions/
  07_primary_filtering/
  08_parent_selection/
  09_affinity_optimization/
  10_consensus_ranking/
  11_fusion_assembly/
  12_linker_optimization/
  13_binding_scenarios/
  14_fc_dimer_models/
  15_full_construct_filtering/
results/
  candidates/
  controls/
  scorecards/
reports/
  decision_log.md
  run_manifest.json
  final_computational_report.md
```

---

## Step 1 — Prepare a Glycan- and Membrane-Aware B7-H3 Ensemble

### Inputs

- Reviewed human CD276 sequence: UniProt `Q5ZPR3`, with the accession version and retrieval date frozen in the manifest.
- Canonical 4Ig isoform and the shorter 2Ig isoform.
- Experimental human B7-H3 structures, including antibody-bound states where appropriate.
- Predicted models only where experimental coverage is incomplete.

### Tasks

1. Retrieve and freeze the human canonical sequence, isoform sequences, domain boundaries, signal peptide, transmembrane region, and known N-linked glycosylation sites.
2. Map every structure to canonical human numbering using an explicit residue-mapping table.
3. Build an ensemble containing:
   - Human 4Ig monomer conformations.
   - Plausible 4Ig dimer/oligomer hypotheses, clearly labeled as hypotheses.
   - Human 2Ig conformations if cross-isoform binding or soluble-antigen sink matters.
   - Experimental antibody-bound conformations with the antibody removed for surface analysis.
   - Conservative inter-domain, hinge, and membrane-tilt states.
4. Define a common type-I membrane orientation and membrane plane.
5. Create glycan treatments for each relevant state:
   - Resolved experimental glycans.
   - Conservative glycan-exclusion envelopes.
   - Representative modeled glycoforms.
   - An unglycosylated control only for comparison.
6. Repair missing side chains or loops without changing experimentally resolved regions unnecessarily.
7. Relax repaired structures conservatively and reject models with distorted Ig domains.

### Outputs

- `metadata/structure_manifest.csv`
- `metadata/numbering_map.csv`
- `data/processed/target_ensemble/*.cif`
- `data/processed/target_ensemble/*.pdb`
- `work/01_target_preparation/ensemble_qc.csv`

### Completion Gate

- Canonical numbering is unambiguous.
- Each model has valid chain identity, isoform, glycan state, membrane orientation, provenance, quality metrics, and checksum.
- No murine, predicted, or antibody-stabilized conformation is mislabeled as an unqualified native human state.

## Step 2 — Select Two Accessible, Non-Overlapping Epitopes

### Inputs

- Accepted target ensemble from Step 1.
- Literature and structural evidence for known B7-H3 binders.
- Intended mechanism: cell-surface binding, internalization, and tumor-cell removal.

### Tasks

1. Enumerate contiguous three-dimensional surface patches rather than linear sequence segments.
2. For each patch calculate or annotate:
   - Solvent accessibility across the ensemble.
   - Membrane distance and outward-facing orientation.
   - Glycan proximity and occlusion frequency.
   - Conformational persistence.
   - Local curvature, hydrophobicity, electrostatics, and designability.
   - 4Ig/2Ig coverage or selectivity.
   - Overlap with known structural or mapped epitopes.
   - Evidence relevant to native-cell binding and internalization.
3. Apply hard gates for verified numbering, extracellular accessibility, glycan assessment, isoform scope, native-surface accessibility, membrane geometry, and provenance.
4. Rank candidate regions with a transparent multi-criteria score and weight-sensitivity analysis.
5. Select epitope A and epitope B only if they are spatially distinct and can support the intended biparatopic geometry.
6. Retain at least one alternative pair in case the primary pair proves poorly designable.

### Outputs

- `metadata/candidate_regions.csv`
- `metadata/binder_epitope_evidence.csv`
- `work/02_epitope_selection/ranked_candidate_regions.csv`
- `work/02_epitope_selection/epitope_pair_geometry.csv`
- `config/epitopes.yaml`

### Completion Gate

- Both epitopes pass all biological hard gates.
- Their relationship is classified as non-overlapping by structural geometry, not only by competition data.
- The intended isoform behavior and membrane geometry are explicit.

## Step 3 — Define Design-Anchor Residues for Each Epitope

### Inputs

- Approved epitopes A and B.
- Surface and glycan measurements from Steps 1–2.

### Tasks

1. Maintain three separate residue classes:
   - `experimental_contact_residues`
   - `region_defining_residues`
   - `predicted_design_anchor_residues`
2. Select small anchor sets that are exposed across accepted ensemble states, separated in three-dimensional space, and unlikely to be glycan-occluded.
3. Prefer anchors capable of supporting mixed hydrophobic and polar interactions; avoid anchor sets composed only of highly charged or flexible residues.
4. Create several anchor combinations per epitope for pilot design runs.
5. Convert canonical residue numbers to the RFantibody target-chain labels used in each cropped target.
6. Although RFantibody calls the `-h` inputs “hotspots,” label computational choices as **predicted design anchors** unless experimental energetic evidence exists.

### Outputs

- `metadata/residue_ledger.csv`
- `work/03_design_anchors/anchor_sets_A.csv`
- `work/03_design_anchors/anchor_sets_B.csv`
- `work/03_design_anchors/canonical_to_target_map.csv`

### Completion Gate

- Every anchor has canonical numbering, source-model numbering, exposure frequency, glycan distance, evidence class, and rationale.
- No anchor is exposed only in a minority conformation unless that state is intentionally targeted.

## Step 4 — Generate Antibody Backbones Independently with RFantibody

### Inputs

- Cropped target structures that preserve the epitope and approximately 10 Å of surrounding structure.
- HLT-formatted human antibody framework.
- Anchor sets and CDR-length ranges.

### Tasks

1. Lock one human antibody framework for the core comparison; the RFantibody example scFv framework is `hu-4D5-8_Fv`, but the final choice must be documented.
2. Convert the framework to RFantibody HLT format:
   - Heavy chain `H`.
   - Light chain `L`.
   - Target chain `T`.
   - Correct HLT CDR remarks.
3. Define CDRs to redesign and allowable length ranges. Use conservative, naturally common lengths for initial runs.
4. Run small pilot campaigns across anchor sets to detect undocked outputs, framework clashes, or unproductive orientations.
5. Select productive anchor/CDR configurations.
6. Run independent production campaigns for epitope A and epitope B. Plan for thousands of backbone designs; RFantibody notes that campaigns near 10,000 designs may be required in general.
7. Store designs as Quiver files when practical and assign globally unique IDs.

### Outputs

- `data/processed/frameworks/framework_HLT.pdb`
- `work/04_rfantibody_backbones/A/*.qv`
- `work/04_rfantibody_backbones/B/*.qv`
- `work/04_rfantibody_backbones/design_manifest.csv`
- `work/04_rfantibody_backbones/pilot_summary.md`

### Completion Gate

- Pilot runs produce correctly docked antibodies against the intended surface.
- Production runs include multiple anchor sets, CDR-length combinations, poses, and random seeds.
- Framework identity and non-designed positions remain fixed.

## Step 5 — Design CDR Sequences with ProteinMPNN

### Inputs

- RFantibody backbone designs from Step 4.
- Fixed framework positions and designable CDR masks.

### Tasks

1. Use the RFantibody ProteinMPNN wrapper so only intended CDR positions are redesigned.
2. Preserve framework sequence and structurally important residues outside the design mask.
3. Generate multiple sequences per backbone using several configurable sampling temperatures; a practical initial panel is 5–20 sequences per backbone across low-to-moderate temperatures.
4. Save per-position probabilities and sequence scores.
5. Exclude or penalize sequence liabilities unless structurally justified:
   - Unpaired cysteine.
   - New N-linked glycosylation sequons in CDRs.
   - Excessive hydrophobic or charged clusters.
   - Easily oxidized, deamidated, or isomerized motifs at exposed sites.
   - Strongly repetitive or low-complexity sequences.
6. Number every antibody with a standard antibody-numbering tool and preserve the H/L/CDR mapping.
7. Deduplicate exact sequences while retaining backbone and seed provenance.

### Outputs

- `work/05_proteinmpnn_sequences/A_sequences.qv`
- `work/05_proteinmpnn_sequences/B_sequences.qv`
- `work/05_proteinmpnn_sequences/sequences.fasta`
- `work/05_proteinmpnn_sequences/sequence_metadata.csv`
- `work/05_proteinmpnn_sequences/liability_flags.csv`

### Completion Gate

- Each sequence maps to one backbone and one epitope.
- Only allowed positions changed.
- CDR and framework numbering is valid.
- Sequence diversity is sufficient for downstream structural prediction.

## Step 6 — Repredict Antibody–B7-H3 Complexes with RF2 and AlphaFold 3

### Inputs

- Designed antibody sequences.
- Relevant B7-H3 target models.

### Tasks

1. Run antibody-finetuned RF2 as the native RFantibody validation stage.
2. Run AlphaFold 3 independently using multiple seeds and samples.
3. Avoid feeding the designed complex pose back as an interface template during independent validation.
4. Evaluate all predictions, not only the top-ranked sample.
5. Calculate:
   - RF2 predicted alignment error at the interface.
   - Antibody–antigen chain-pair confidence from AlphaFold 3.
   - Interface PAE summaries.
   - CDR backbone RMSD between design and reprediction.
   - Antibody rigid-body/pose RMSD after aligning B7-H3.
   - Fraction of anchor contacts recovered.
   - Interface contact-map consistency across seeds.
6. Repeat predictions against representative ensemble members for candidates surviving the first pass.

### Outputs

- `work/06_structure_predictions/rf2/`
- `work/06_structure_predictions/af3/`
- `work/06_structure_predictions/prediction_metrics.csv`
- `work/06_structure_predictions/contact_consistency.csv`

### Completion Gate

- Predictions are independent of the original designed interface.
- Multiple seeds support the same epitope and broadly consistent binding pose.
- All raw confidence fields and derived metrics are retained.

## Step 7 — Apply Primary Structural, Interface, and Developability Filters

### Inputs

- RF2 and AlphaFold 3 predictions.
- Sequence-liability results.

### Tasks

1. Use staged filtering rather than one composite score:
   - Correct target and intended epitope.
   - No severe backbone or inter-chain clashes.
   - Stable CDR and binding-pose recovery.
   - Adequate interface confidence.
   - Anchor-contact recovery.
   - Favorable interface packing and buried surface.
   - Low buried-unsatisfied-polar burden.
   - Acceptable sequence developability.
2. Use RFantibody’s published starting filters as provisional defaults:
   - RF2 interface pAE `< 10`.
   - Design-versus-RF2-predicted RMSD `< 2 Å`.
3. Calculate Rosetta InterfaceAnalyzer metrics such as `dG_separated`, `dSASA_int`, `packstat`, cross-interface hydrogen bonds, and buried unsatisfied hydrogen bonds.
4. Treat Rosetta `ddG < -20` as an optional RFantibody enrichment feature, not as a universal physical affinity threshold.
5. Calibrate thresholds using score distributions and known positive/negative antibody–antigen complexes when available.
6. Record every rejection reason instead of deleting failed designs.

### Outputs

- `config/filters.yaml`
- `work/07_primary_filtering/all_scores.csv`
- `work/07_primary_filtering/pass_fail.csv`
- `work/07_primary_filtering/rejection_reasons.csv`
- `work/07_primary_filtering/survivors_A.qv`
- `work/07_primary_filtering/survivors_B.qv`

### Completion Gate

- Every retained design passes all hard filters.
- No candidate is retained because of one favorable score while failing epitope, clash, or pose-consistency gates.

## Step 8 — Select Structurally Diverse Parent Antibodies

### Inputs

- Filtered epitope-A and epitope-B designs.

### Tasks

1. Cluster separately by:
   - CDR sequence identity.
   - CDR backbone geometry.
   - Antibody orientation on B7-H3.
   - Interface contact map.
2. Remove near-duplicate candidates that do not add independent information.
3. Select representatives from multiple Pareto-optimal clusters rather than only the best scalar score.
4. Retain a configurable parent panel, initially approximately 20–50 candidates per epitope if the design pool supports it.
5. Include some moderate-scoring but geometrically distinct candidates to reduce model-selection bias.

### Outputs

- `work/08_parent_selection/clusters_A.csv`
- `work/08_parent_selection/clusters_B.csv`
- `work/08_parent_selection/parents_A.fasta`
- `work/08_parent_selection/parents_B.fasta`
- `work/08_parent_selection/parent_scorecards/`

### Completion Gate

- Parent panels span multiple sequences, CDR geometries, and binding orientations.
- No single RFdiffusion trajectory or backbone family dominates the panel.

## Step 9 — Perform In-Silico Affinity Optimization Independently for A and B

### Inputs

- Selected parent antibodies.
- Parent complex ensembles and residue-level interface maps.

### Tasks

1. Identify first-shell CDR residues contacting B7-H3 and second-shell CDR residues supporting their geometry.
2. Keep framework residues fixed unless a separate developability/humanness campaign is explicitly approved.
3. Generate a focused single-mutant scan at permitted CDR positions.
4. Score single mutants using a consensus of:
   - ProteinMPNN conditional sequence probabilities.
   - Rosetta Flex ddG or an equivalently sampled interface ΔΔG method.
   - InterfaceAnalyzer metrics after local repacking/minimization.
   - Independent RF2/AlphaFold 3 pose recovery.
5. Eliminate mutations that create sequence liabilities, clashes, new glycan motifs, unstable CDR conformations, or altered epitope specificity.
6. Combine favorable single mutations into double and higher-order variants only after explicit structural modeling; do not assume additivity.
7. Repredict every combination and test for epistasis, binding-pose drift, and loss of framework stability.
8. Run negative-design checks against unintended B7-family or relevant off-target surfaces when structural data are available.
9. Maintain an explicit mutation lineage from each parent to each optimized child.

### Outputs

- `work/09_affinity_optimization/mutation_positions.csv`
- `work/09_affinity_optimization/single_mutants.csv`
- `work/09_affinity_optimization/combinatorial_variants.csv`
- `work/09_affinity_optimization/mutation_lineage.csv`
- `work/09_affinity_optimization/optimized_A.fasta`
- `work/09_affinity_optimization/optimized_B.fasta`

### Completion Gate

- Optimized variants retain the intended epitope and binding orientation across independent predictions.
- Predicted improvement is supported by multiple methods and does not depend on one model or one structure.
- Results are labeled as predictions, not measured affinity changes.

## Step 10 — Rank Optimized Antibodies Across the B7-H3 Ensemble

### Inputs

- Parent and optimized antibody designs.
- Full target ensemble.

### Tasks

1. Evaluate each design across all target states relevant to its intended isoform scope.
2. Calculate minimum, median, and worst-case interface metrics across the ensemble.
3. Require persistence of the intended epitope, pose, and anchor contacts.
4. Penalize glycan clashes, membrane-facing approaches, conformation-specific failures, and unintended isoform behavior.
5. Compare affinity-related scores separately from stability, specificity, and developability.
6. Produce Pareto rankings and weight-sensitivity analyses; do not collapse all evidence into one opaque score.
7. Retain several optimized variants per parent lineage.

### Outputs

- `work/10_consensus_ranking/ensemble_scores.csv`
- `work/10_consensus_ranking/robustness_summary.csv`
- `work/10_consensus_ranking/pareto_front.csv`
- `results/candidates/optimized_A_ranked.csv`
- `results/candidates/optimized_B_ranked.csv`

### Completion Gate

- Selected antibodies remain acceptable across relevant B7-H3 states.
- The ranking is robust to reasonable score-weight changes.
- Diversity is preserved for fusion assembly.

## Step 11 — Assemble A–Linker–B and B–Linker–A Constructs

### Inputs

- Ranked optimized A and B scFvs.
- Locked tandem-scFv-Fc architecture.

### Tasks

1. Pair multiple top A and B lineages; do not pair only the two top scalar scores.
2. Build both orientations:
   - `A-scFv–linker–B-scFv–hinge–Fc`
   - `B-scFv–linker–A-scFv–hinge–Fc`
3. Define exact VH–VL orientation and intramolecular scFv linkers for each antibody.
4. Preserve domain boundaries, disulfide-forming cysteines, and correct termini.
5. Assign stable construct IDs encoding orientation, parent IDs, linker ID, Fc ID, and version.
6. Generate FASTA, annotated GenBank, and initial structural models for every construct.

### Outputs

- `work/11_fusion_assembly/fusions.fasta`
- `work/11_fusion_assembly/fusions.gb`
- `work/11_fusion_assembly/fusion_manifest.csv`
- `work/11_fusion_assembly/initial_models/`

### Completion Gate

- Every fusion is traceable to its A and B parents.
- Chain order, linkers, termini, and Fc junctions are sequence-valid.
- Both A–B and B–A orientations are represented.

## Step 12 — Optimize Linker Length and Sequence Computationally

### Inputs

- Fusion constructs from Step 11.
- Single-arm binding poses for A and B.

### Tasks

1. Create a linker panel spanning several flexible lengths; an initial computational panel can include approximately 10, 15, 20, and 25 residues.
2. Use low-complexity Gly/Ser-rich linkers as the baseline and add alternatives only with a stated purpose.
3. Sample linker conformational ensembles rather than relying on one AlphaFold structure for a flexible region.
4. Test whether each linker permits:
   - Independent folding of both scFvs.
   - Access of A and B to their epitopes.
   - Intended same-antigen or two-antigen occupancy scenarios.
   - Minimal inter-domain and Fc clashes.
5. Evaluate linker liabilities, protease-sensitive motifs, unwanted glycosylation motifs, and exposed hydrophobicity.
6. Retain multiple linker/orientation combinations.

### Outputs

- `work/12_linker_optimization/linker_library.fasta`
- `work/12_linker_optimization/linker_ensemble_metrics.csv`
- `work/12_linker_optimization/accepted_linkers.csv`

### Completion Gate

- Both binding domains remain structurally stable and accessible.
- Acceptance is supported by an ensemble of linker conformations.
- At least two linker/orientation solutions survive when possible.

## Step 13 — Model Separate and Simultaneous Binding Scenarios

### Inputs

- Accepted fusion/linker constructs.
- B7-H3 target ensemble and membrane plane.

### Tasks

1. Model A-only binding with the B domain unbound.
2. Model B-only binding with the A domain unbound.
3. Model two different simultaneous scenarios separately:
   - **Cis/intramolecular:** A and B bind two epitopes on one B7-H3 molecule.
   - **Intermolecular:** A and B bind different B7-H3 molecules.
4. Do not require cis binding if the project only needs heterogeneous or intermolecular occupancy.
5. Sample target spacing, receptor tilt, membrane separation, and flexible linker conformations.
6. Calculate epitope reachability, linker strain, domain clashes, membrane clashes, and unbound-domain accessibility.
7. Record which occupancy states are geometrically feasible, unfavorable, or unresolved.

### Outputs

- `work/13_binding_scenarios/A_only/`
- `work/13_binding_scenarios/B_only/`
- `work/13_binding_scenarios/cis_AB/`
- `work/13_binding_scenarios/intermolecular_AB/`
- `work/13_binding_scenarios/scenario_scores.csv`

### Completion Gate

- A-only and B-only binding remain feasible.
- Any claim of simultaneous binding is supported by a feasible structural ensemble, not one hand-positioned model.
- Cis and intermolecular interpretations are never mixed.

## Step 14 — Add Fc and Model the Complete 2A + 2B Dimer

### Inputs

- Accepted tandem-scFv constructs.
- Exact Fc/hinge sequence and intended Fc behavior.

### Tasks

1. Lock Fc isotype, hinge, species, allotype, effector-function mutations, FcRn-related mutations, and purification tags.
2. Build the covalent Fc dimer with correct hinge and inter-chain disulfides.
3. Include representative Fc N-glycan states or conservative glycan-exclusion envelopes.
4. Generate full dimer ensembles rather than one static model.
5. Model zero-, one-, two-, three-, and four-antigen occupancy where computationally tractable.
6. Check scFv–scFv, scFv–Fc, antigen–Fc, antigen–antigen, glycan, and membrane clashes.
7. Measure arm reach, inter-paratope distance distributions, exit vectors, symmetry, and unoccupied-site accessibility.
8. Verify that the model actually contains two A and two B paratopes.

### Outputs

- `work/14_fc_dimer_models/full_dimer_models/`
- `work/14_fc_dimer_models/occupancy_models/`
- `work/14_fc_dimer_models/dimer_geometry.csv`
- `work/14_fc_dimer_models/clash_report.csv`

### Completion Gate

- Covalent architecture, disulfides, glycans, and valency are correct.
- At least one low-strain ensemble supports both A and B accessibility.
- Full-dimer geometry does not invalidate the single-chain fusion results.

## Step 15 — Filter Complete Constructs for Geometry and Developability

### Inputs

- Full Fc-dimer ensembles.
- Sequence and interface results from earlier steps.

### Tasks

1. Evaluate full-construct properties:
   - Domain folding confidence.
   - Inter-domain clashes and linker strain.
   - Exposed hydrophobic patches.
   - Charge distribution and predicted pI.
   - Aggregation and self-association risk.
   - Chemical sequence liabilities.
   - Non-human or potentially immunogenic sequence features.
   - Fc and glycan accessibility.
2. Evaluate unwanted receptor networking or B7-H3 crosslinking using multiple antigen-density and spacing scenarios.
3. Distinguish potentially useful clustering for internalization from uncontrolled higher-order networking.
4. Confirm that neither domain is consistently occluded by the other domain or Fc.
5. Run negative controls through the same scoring pipeline to identify score artifacts.
6. Create a per-construct risk register and do not hide unresolved high-risk features inside a total score.

### Outputs

- `work/15_full_construct_filtering/developability_scores.csv`
- `work/15_full_construct_filtering/crosslinking_scenarios.csv`
- `work/15_full_construct_filtering/risk_register.csv`
- `results/scorecards/final_construct_scorecards/`

### Completion Gate

- No unresolved severe clash, folding, aggregation, or sequence-liability flag.
- Intended and unintended crosslinking scenarios are explicitly distinguished.
- Remaining uncertainties are documented for experimental testing.

## Step 16 — Select the Computational Candidate and Control Panel

### Inputs

- Final construct scorecards and risk register.

### Tasks

1. Select a diverse panel rather than only the top-ranked construct.
2. Include several A+B candidates spanning:
   - A–B and B–A orientations.
   - More than one linker.
   - More than one A and B parent lineage.
   - Different predicted affinity/developability trade-offs.
3. Include controls processed through the same computational pipeline:
   - A-only construct.
   - B-only construct.
   - Parental, non-optimized A+B construct.
   - Optimized A+B constructs.
   - Nonbinding or paratope-disrupted control for later experiments.
4. Freeze exact amino-acid sequences and calculate checksums.
5. Record the reason each candidate or control was selected.

### Outputs

- `results/candidates/final_panel.fasta`
- `results/controls/control_panel.fasta`
- `results/candidates/final_panel.csv`
- `results/scorecards/final_selection_matrix.csv`
- `reports/decision_log.md`

### Completion Gate

- The panel tests architecture, orientation, linker, parent, and optimization effects.
- Every construct has a frozen sequence, unique ID, checksum, provenance, and selection rationale.

## Step 17 — Produce the Experimental Handoff Package

### Inputs

- Frozen candidate and control panel.
- Complete computational provenance.

### Tasks

1. Package final sequences as annotated FASTA and GenBank files.
2. Provide predicted structures in PDB/mmCIF format with chain definitions.
3. Provide residue numbering, CDR definitions, epitope assignments, design-anchor contacts, and mutation lineages.
4. Provide the complete score table, uncertainty estimates, and rejection history.
5. Define the later experimental questions without claiming results:
   - Expression and monodispersity.
   - A-only and B-only binding.
   - Measured affinity and kinetics.
   - Simultaneous-binding behavior.
   - Native cell-surface binding.
   - Internalization.
   - Tumor-cell removal and Fc-dependent function, where intended.
6. Create a blinded construct key if unbiased experimental comparison is desired.
7. Freeze the computational release with a version tag and reproducibility manifest.

### Outputs

- `reports/final_computational_report.md`
- `reports/run_manifest.json`
- `results/experimental_handoff/`
- `results/experimental_handoff/construct_key.csv`
- `results/experimental_handoff/experimental_questions.md`

### Completion Gate

- A second operator or agent can trace every final sequence back to its inputs, commands, models, and decisions.
- All constructs are clearly labeled as computational predictions pending experimental validation.

---

## Provisional Computational Funnel

The exact numbers remain configurable and should be revised after pilot runs.

| Stage | Suggested starting scale per epitope |
|---|---:|
| RFantibody pilot backbones | 100–500 per anchor/CDR configuration |
| RFantibody production backbones | Approximately 10,000 total |
| ProteinMPNN sequences | 5–20 per retained backbone |
| RF2 primary validation | All deduplicated sequences |
| AlphaFold 3 validation | Filtered subset, multiple seeds/samples |
| Parent antibodies | Approximately 20–50 diverse designs |
| Affinity-optimization variants | Configured by mutable positions and compute budget |
| Final A+B constructs | Diverse, experimentally manageable panel |

## Core References and Software Documentation

- [Human CD276/B7-H3, UniProt Q5ZPR3](https://www.uniprot.org/uniprotkb/Q5ZPR3/entry)
- [RFantibody repository and practical design guidance](https://github.com/RosettaCommons/RFantibody)
- [Atomically accurate de novo design of antibodies with RFdiffusion](https://www.nature.com/articles/s41586-025-09721-5)
- [ProteinMPNN repository](https://github.com/dauparas/ProteinMPNN)
- [AlphaFold 3 repository](https://github.com/google-deepmind/alphafold3)
- [AlphaFold 3 input specification](https://github.com/google-deepmind/alphafold3/blob/main/docs/input.md)
- [AlphaFold 3 output-confidence specification](https://github.com/google-deepmind/alphafold3/blob/main/docs/output.md)
- [Rosetta InterfaceAnalyzer](https://docs.rosettacommons.org/docs/latest/application_documentation/analysis/interface-analyzer)
- [Rosetta Flex ddG](https://docs.rosettacommons.org/docs/latest/flex-ddG)
- [Human B7-H3–20G5 complex, PDB 9LY5](https://www.rcsb.org/structure/9LY5)
