# Project 1: Computational-First B7-H3 Biparatopic Antibody Design

## Objective

Design two independent antibodies against distinct human B7-H3/CD276 epitopes, optimize each antibody computationally, combine them as a biparatopic construct, and complete full-construct modeling before experimental testing.

> **Terminology:** Before experimental measurement, the maturation stage is **in-silico affinity optimization**, not confirmed affinity maturation. High affinity cannot be claimed until measured by SPR, BLI, or an equivalent method.

## User-Selected Architecture — 2026-09-19

The required product is a **1A + 1B IgG-like biparatopic antibody with Fc**:
one Fab arm recognizes epitope A on human B7-H3 and the other Fab arm recognizes
epitope B. The antigen sites are epitopes; the corresponding antibody binding
sites are paratopes.

```text
Fab A (VH-A/VL-A)       Fab B (VH-B/VL-B)
           \             /
             hinge region
                  Fc
      one A site + one B site
```

Both arms must be capable of simultaneously binding their distinct epitopes on
one native cell-surface human 4Ig-B7-H3 molecule. This geometry is required but
unverified. Binding different antigen molecules alone does not satisfy it.

The former tandem-scFv-Fc assumption had two A and two B sites. The user-selected
product instead has one A and one B site. Historical descriptions of the former format, including the
unchanged AGENTS.md research-context paragraph, are superseded for architecture
by this user decision (reports/decision_log.md, STEP0-008).

Exact Fc isotype/sequence, hinge, heavy-chain heterodimerization and light-chain
pairing strategy remain unresolved. Do not infer a common light chain, particular
pairing mutations, or a different format. Record approved implementation settings
in `config/project.yaml` before format-dependent design and assembly. Fv models
may remain intermediate design inputs; they do not define the final product.

## Agent Execution Rules

- Record sources, software/model versions, commands, important parameters, relevant random seeds, and output locations in concise analysis notes. Use checksums only when they answer a concrete identity or integrity question.
- Use human canonical CD276 numbering as the reporting coordinate system.
- Keep experimental contacts, region-defining residues, and computational design anchors in separate fields.
- Do not treat one predicted structure or one score as proof of binding or affinity.
- Never silently replace a missing scientific decision. Write unresolved items to `reports/decision_log.md` and stop at the relevant gate.
- Keep multiple structurally and sequence-diverse candidates through every stage.
- Make every numerical cutoff configurable in `config/filters.yaml`.
- Treat developability as a staged risk assessment, not as a single score. Separate computational hypotheses from measurements that require purified protein.

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
  11_fab_assembly/
  12_hinge_geometry/
  13_binding_scenarios/
  14_full_igg_models/
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

## Step 0 — Lock Scientific Scope and Development Criteria

Before collecting a large design library, record the decisions that change what
counts as a useful molecule:

- intended biological endpoint and its priority among binding, internalization,
  tumor-cell removal, and Fc-mediated function;
- B7-H3 isoforms and species to be covered, including whether soluble antigen is
  an intended sink or an excluded context;
- the selected 1A + 1B IgG-like architecture, heavy/light-chain pairing strategy, Fc species/isotype, hinge, effector
  function, FcRn intent, and acceptable valency;
- whether cis bivalent binding to one antigen is required, merely desirable, or
  irrelevant to the program;
- minimum candidate diversity, computational budget, and promotion limits at
  each funnel stage;
- developability priorities and disqualifying risks, including expression,
  folding, aggregation/self-association, chemical stability, polyspecificity,
  immunogenicity, viscosity, and manufacturability;
- which properties are computational triage only and which will require purified
  protein or cell-based measurements.

Record unresolved choices in `reports/decision_log.md`. Do not let an affinity
ranking silently choose the product format or biological endpoint.

### Scope Gate

The project has an explicit architecture, isoform scope, endpoint priority,
developability risk policy, and candidate-budget policy before production-scale
design begins. A pilot may proceed with provisional values when those values are
clearly labeled and revisited after the pilot.

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
- Each model has valid chain identity, isoform, glycan state, membrane orientation, provenance, and quality notes.
- No murine, predicted, or antibody-stabilized conformation is mislabeled as an unqualified native human state.
- Glycan and membrane assumptions are preserved in the model labels; an unglycosylated or cropped model is not treated as the native target.

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
5. Select epitope A and epitope B only if they are spatially distinct and have preliminary support for simultaneous engagement of one human 4Ig-B7-H3 molecule by the two Fab arms of the 1A + 1B antibody. Separation alone is insufficient; consider approach vectors and available Fab/hinge reach. Reassess with designed poses before production scale-up.
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

1. Lock one human antibody framework for the core comparison; the RFantibody example scFv framework is `hu-4D5-8_Fv`, but the final choice must be documented. An example Fv/scFv input does not prescribe a tandem-scFv product. Resolve whether the selected chain-pairing strategy constrains light-chain design before independent A/B production.
2. Convert the framework to RFantibody HLT format:
   - Heavy chain `H`.
   - Light chain `L`.
   - Target chain `T`.
   - Correct HLT CDR remarks.
3. Define CDRs to redesign and allowable length ranges. Use conservative, naturally common lengths for initial runs.
4. Run the approved breadth pilot: generate 100–300 backbone designs for each active epitope/hotspot definition (currently one Arm A and one Arm B definition), across documented seeds and CDR configurations, to measure docking productivity, CDR geometry, and structural diversity.
5. Select productive anchor/CDR configurations using the documented backbone QC gates while preserving diversity and parent provenance.
6. Run independent production campaigns for epitope A and epitope B. Plan for thousands of backbone designs; RFantibody notes that campaigns near 10,000 designs may be required in general.
7. Store designs as Quiver files when practical and assign globally unique IDs.
8. Reject designs with obvious framework disruption, buried unpaired cysteines, extreme loop geometry, or target approaches that are incompatible with the full glycan/membrane context before sequence design.
9. Back-map promising cropped-target poses to the full glycan- and membrane-aware ensemble before promoting an anchor/CDR configuration to production. Check preliminary A/B Fab-pair compatibility with the required same-antigen 1A + 1B geometry before expensive scale-up; later full-antibody validation remains necessary.

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
3. For the approved breadth pilot, generate approximately 4 sequences per retained backbone. Broader 5–20-sequence panels remain configurable for later optimization campaigns.
4. Save per-position probabilities and sequence scores.
5. Exclude or penalize sequence liabilities unless structurally justified:
   - Unpaired cysteine.
   - New N-linked glycosylation sequons in CDRs.
   - Excessive hydrophobic or charged clusters.
   - Easily oxidized, deamidated, or isomerized motifs at exposed sites.
   - Strongly repetitive or low-complexity sequences.
6. Number every antibody with a standard antibody-numbering tool and preserve the H/L/CDR mapping.
7. Record whether each liability is a hard exclusion, a review flag, or a context-dependent risk. Do not discard a candidate solely because of a weak proxy without recording the rationale.
8. Deduplicate exact sequences while retaining backbone and sampling provenance; identical sequences from multiple backbones remain separate design instances.

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
- Initial sequence triage has identified candidates with no unexplained severe liability; unresolved risks remain visible for later assessment.

## Cross-Cutting Developability Assessment

Developability is evaluated from the first sequence library onward and revisited
after every mutation, Fab assembly, hinge, chain-pairing, and Fc decision. The assessment is a risk
register, not a claim that a computationally favorable sequence will express or
formulate successfully.

### Risk classes

1. **Sequence and chemical liabilities:** unpaired cysteine, noncanonical residues,
   N-linked glycosylation sequons in exposed or functionally disruptive locations,
   deamidation/isomerization/oxidation-prone motifs, protease-sensitive motifs,
   and sequence changes that disturb canonical disulfides or processing sites.
2. **Conformational stability:** framework integrity, CDR strain, domain packing,
   local unfolding risk, and whether mutations preserve the intended VH/VL
   interface and Fab domain organization.
3. **Colloidal behavior:** exposed hydrophobic patches, asymmetric charge patches,
   predicted self-interaction, polyspecificity/polyreactivity proxies, aggregation
   propensity, and concentration-dependent viscosity risk.
4. **Format and process risk:** hinge cleavage or flexibility, domain swapping,
   Fab/Fc interference, incorrect chain pairing, disulfide mispairing, clipping,
   glycan heterogeneity, expression burden, and purification complexity.
5. **Immunogenicity and human sequence context:** non-human framework features,
   unusual exposed motifs, T-cell epitope hypotheses, and back-mutations that may
   restore structure while increasing immune-risk hypotheses. These are risk flags,
   not predictions of clinical immunogenicity.

### Assessment rules

- Apply cheap sequence and structure triage before expensive prediction; reassess
  every promoted sequence and every assembled construct.
- Keep affinity/interface evidence separate from developability evidence. A strong
  predicted interface does not compensate for an unresolved severe liability.
- Use several complementary proxies where available and report disagreement. Do
  not sum correlated predictors into a falsely precise developability score.
- Treat thresholds as provisional until calibrated against an appropriate antibody
  reference set or local measurements. Preserve candidates with different risk
  profiles when the evidence does not justify a hard exclusion.
- Mark properties that cannot be inferred reliably in silico—especially viscosity,
  polyspecificity, expression yield, aggregation under formulation conditions, and
  immunogenicity—for experimental follow-up.

### Required assessment record

For each sequence or construct, retain a compact table with the risk class, method
or proxy used, result, interpretation, confidence, action (`retain`, `review`, or
`exclude`), and rationale. Include the exact mutation lineage for optimized
variants and identify liabilities introduced or removed by each mutation.

This framework follows the risk-based principle that early computational and
biophysical triage should reduce development risk without replacing measurements.

## Step 6 — Repredict Antibody–B7-H3 Complexes with RF2, RF3, and AlphaFold 3

### Inputs

- Designed antibody sequences.
- Relevant B7-H3 target models.

### Tasks

1. Confirm that the candidates originated from antibody-finetuned RFdiffusion backbone generation followed by ProteinMPNN sequence design; RF2 is a validator, not the antibody generator.
2. Run antibody-finetuned RF2 (`RF2_ab`) as the native, high-throughput RFantibody self-consistency stage.
3. Apply the documented RF2-specific confidence and pose-recovery filters before the more expensive independent predictors.
4. Run AlphaFold 3 independently on RF2 survivors using multiple seeds and samples. Use AlphaFold 3 as the primary independent validation model because published RFantibody data show that its interface confidence enriches experimental binders.
5. Run RoseTTAFold3 (RF3) as a complementary independent prediction and disagreement-analysis layer on the AF3-evaluated subset.
6. Pin the RF3 Foundry version, checkpoint, input schema, inference steps, diffusion batch size, and random seeds because the RF3 inference API and confidence outputs are still evolving.
7. Do not provide the designed antibody–antigen interface as a structural template during RF3 or AlphaFold 3 validation.
8. Evaluate all generated predictions, not only the top-ranked sample.
9. Calculate:
   - RF2 interface predicted alignment error and RF2 design-to-prediction RMSD.
   - RF3 model confidence, interface confidence, clash metrics, and design-to-prediction RMSD using metrics available in the pinned RF3 release.
   - AlphaFold 3 antibody–antigen chain-pair confidence and interface PAE summaries.
   - CDR backbone RMSD between design and reprediction.
   - Antibody rigid-body/pose RMSD after aligning B7-H3.
   - Fraction of anchor contacts recovered.
   - Interface contact-map consistency across samples, seeds, and predictors.
   - Agreement or disagreement among RF2, RF3, and AlphaFold 3.
10. Repeat AlphaFold 3 predictions against representative B7-H3 ensemble members for candidates surviving the primary pass.
11. Use RF3 to identify agreements, disagreements, alternative poses, and possible failure modes; do not require an RF3 pass for advancement until it is calibrated on experimentally tested RFantibody designs.
12. Do not apply RF2_ab or AlphaFold 3 thresholds directly to RF3 outputs.

### Outputs

- `work/06_structure_predictions/rf2/`
- `work/06_structure_predictions/rf3/`
- `work/06_structure_predictions/af3/`
- `work/06_structure_predictions/prediction_metrics.csv`
- `work/06_structure_predictions/contact_consistency.csv`
- `work/06_structure_predictions/predictor_agreement.csv`

### Completion Gate

- Predictions are independent of the original designed interface.
- Multiple AlphaFold 3 seeds support the same epitope and a broadly consistent binding pose for final survivors.
- RF3 agreement strengthens confidence, while RF3 disagreement triggers review rather than automatic rejection.
- All raw confidence fields and derived metrics are retained.

## Step 7 — Apply Primary Structural, Interface, and Developability Filters

### Inputs

- RF2, RF3, and AlphaFold 3 predictions.
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
3. Use calibrated AlphaFold 3 interface-confidence and pose-recovery criteria as the primary independent filtering layer.
4. Record RF3 metrics from the pinned release as supporting evidence, but do not use RF3 as a hard pass/fail filter until experimental calibration is available.
5. Use cross-predictor agreement as a ranking feature while retaining designs with interpretable RF3 disagreement for review.
6. Calculate Rosetta InterfaceAnalyzer metrics such as `dG_separated`, `dSASA_int`, `packstat`, cross-interface hydrogen bonds, and buried unsatisfied hydrogen bonds.
7. Treat Rosetta `ddG < -20` as an optional RFantibody enrichment feature, not as a universal physical affinity threshold.
8. Calibrate RF2 and AlphaFold 3 thresholds using score distributions and known positive/negative antibody–antigen complexes when available; calibrate RF3 separately when suitable experimental design data become available.
9. Apply the cross-cutting developability risk classes before promotion, with hard exclusion only for defined severe risks.
10. Record every rejection reason instead of deleting failed designs.

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
   - RF2_ab self-consistency and independent AlphaFold 3 pose recovery.
   - RF3 agreement or disagreement as supporting evidence, not a hard gate.
5. Eliminate mutations that create sequence liabilities, clashes, new glycan motifs, unstable CDR conformations, or altered epitope specificity.
6. Combine favorable single mutations into double and higher-order variants only after explicit structural modeling; do not assume additivity.
7. Repredict every combination and test for epistasis, binding-pose drift, and loss of framework stability.
8. Run negative-design checks against unintended B7-family or relevant off-target surfaces when structural data are available.
9. Re-run the complete developability risk assessment for every promoted mutation and reject mutations that improve a proxy while creating an unresolved severe liability.
10. Maintain an explicit mutation lineage from each parent to each optimized child.

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
5. Compare affinity-related scores separately from stability, specificity, and each developability risk class.
6. Produce Pareto rankings and weight-sensitivity analyses; do not collapse all evidence into one opaque score.
7. Retain several optimized variants per parent lineage.
8. Ensure that ensemble ranking does not hide a severe sequence, chemical, colloidal, or format liability behind a favorable mean score.

### Outputs

- `work/10_consensus_ranking/ensemble_scores.csv`
- `work/10_consensus_ranking/robustness_summary.csv`
- `work/10_consensus_ranking/pareto_front.csv`
- `results/candidates/optimized_A_ranked.csv`
- `results/candidates/optimized_B_ranked.csv`

### Completion Gate

- Selected antibodies remain acceptable across relevant B7-H3 states.
- The ranking is robust to reasonable score-weight changes.
- Diversity is preserved for Fab-arm assembly.

## Step 11 — Assemble the Two Distinct Fab Arms

### Inputs

- Ranked optimized A and B variable-domain pairs and their target-binding poses.
- User-selected 1A + 1B IgG-like architecture.
- Approved constant-domain identities and heavy/light-chain pairing strategy.

### Tasks

1. Pair multiple top A and B lineages; do not pair only the two top scalar scores.
2. Assemble VH-A/CH1 with its intended light chain and VH-B/CH1 with its intended light chain. Preserve parent lineage and explicit chain identities.
3. Document how the product will favor A/B heavy-chain pairing and correct heavy/light pairing. Do not silently substitute a common light chain or mutate a validated variable region.
4. Preserve domain boundaries, disulfide-forming cysteines, and correct termini. Reassess each parent binding pose in Fab context.
5. Assign stable construct IDs encoding A/B parents, constant domains, pairing strategy, hinge/Fc identifiers, and version.
6. Generate chain-resolved FASTA, annotated GenBank, and initial Fab models when assembly is authorized.

### Outputs

- `work/11_fab_assembly/fab_chains.fasta`
- `work/11_fab_assembly/fab_chains.gb`
- `work/11_fab_assembly/chain_manifest.csv`
- `work/11_fab_assembly/initial_models/`

### Completion Gate

- Each Fab maps to its A or B parent, with valid chain/domain boundaries and disulfides.
- Heavy/light-chain pairing and the intended A/B assembly strategy are explicit.
- Neither Fab context nor pairing changes invalidate the parent binding hypothesis.
- There is one A arm and one B arm; no tandem A–B scFv chain is introduced.

## Step 12 — Assess Hinge and Fab-Arm Geometry

### Inputs

- Fab constructs and chain definitions from Step 11.
- Single-arm binding poses for A and B.
- Approved hinge/Fc candidates and native target/membrane context.

### Tasks

1. Sample plausible Fab elbow and hinge conformations within the approved format; do not assume a flexible region has one fixed predicted conformation.
2. Assess whether both Fab arms can engage their respective epitopes on the same human 4Ig-B7-H3 molecule without excessive strain or steric interference.
3. Assess Fab–Fab, Fab–Fc, glycan, and membrane clashes in the intended geometry.
4. Evaluate hinge/disulfide integrity, protease-sensitive and chemical liabilities, and exposure of hydrophobic regions.
5. Retain diverse feasible conformations and, where authorized, hinge variants. Do not add arbitrary tandem-scFv linkers as a geometry workaround.
6. If no feasible geometry remains, report the conflict with the required same-antigen binding capability rather than silently switching to two-antigen binding or another format.

### Outputs

- `work/12_hinge_geometry/hinge_candidates.fasta`
- `work/12_hinge_geometry/geometry_ensemble_metrics.csv`
- `work/12_hinge_geometry/accepted_geometries.csv`

### Completion Gate

- Both Fab arms remain structurally plausible and accessible.
- An ensemble supports low-strain same-antigen A/B binding within the approved hinge/Fc context.
- Hinge/pairing choices and uncertainties remain explicit; geometry feasibility is not measured simultaneous binding.

## Step 13 — Model Separate and Simultaneous Binding Scenarios

### Inputs

- Accepted Fab-arm/hinge arrangements.
- B7-H3 target ensemble and membrane plane.

### Tasks

1. Model A-only binding with Fab B unbound.
2. Model B-only binding with Fab A unbound.
3. Model simultaneous scenarios separately:
   - **Required cis/intramolecular capability:** A and B engage distinct epitopes on one B7-H3 molecule.
   - **Additional intermolecular scenario:** A and B engage different B7-H3 molecules.
4. Do not accept intermolecular binding alone as fulfillment of the user's cis-binding requirement.
5. Sample target spacing, receptor tilt, membrane geometry, and plausible hinge/Fab conformations.
6. Calculate epitope reachability, hinge strain, domain clashes, membrane clashes, and unbound-arm accessibility.
7. Record which occupancy states are geometrically feasible, unfavorable, or unresolved.

### Outputs

- `work/13_binding_scenarios/A_only/`
- `work/13_binding_scenarios/B_only/`
- `work/13_binding_scenarios/cis_AB/`
- `work/13_binding_scenarios/intermolecular_AB/`
- `work/13_binding_scenarios/scenario_scores.csv`

### Completion Gate

- A-only and B-only binding remain feasible.
- Required simultaneous same-antigen binding has support from a plausible structural ensemble, not one hand-positioned model.
- Cis and intermolecular interpretations are never mixed; feasibility is not experimental validation.

## Step 14 — Model the Complete 1A + 1B IgG-like Antibody with Fc

### Inputs

- Accepted Fab arms and hinge/occupancy ensembles.
- Exact approved Fc/hinge sequences and intended Fc behavior.
- Explicit heavy-chain heterodimer and light-chain pairing strategy.

### Tasks

1. Lock Fc isotype, species, allotype, effector-function and FcRn intent, hinge, pairing implementation, and any production tags before full assembly.
2. Assemble the complete chain-defined antibody with correct intra- and inter-chain disulfides. Keep shared versus distinct light-chain identities explicit if a corresponding strategy has been approved.
3. Include representative Fc N-glycan states or conservative glycan-exclusion envelopes.
4. Generate full-antibody ensembles rather than one static model.
5. Model zero-, one-, and two-antigen occupancy, distinguishing one-antigen A-only/B-only states from simultaneous A+B engagement of one antigen. Do not model three/four specific antigen occupancies as properties of this two-site product.
6. Check Fab–Fab, Fab–Fc, antigen–Fc, antigen–antigen, glycan, and membrane clashes.
7. Measure arm reach, inter-paratope distance distributions, hinge geometry, and unoccupied-site accessibility without imposing false A/B symmetry.
8. Verify exactly one A and one B binding site. Evaluate incorrect chain-pairing risks separately from the intended product model.

### Outputs

- `work/14_full_igg_models/full_antibody_models/`
- `work/14_full_igg_models/occupancy_models/`
- `work/14_full_igg_models/antibody_geometry.csv`
- `work/14_full_igg_models/clash_report.csv`
- `work/14_full_igg_models/chain_pairing_assessment.csv`

### Completion Gate

- Chain pairing, covalent architecture, disulfides, glycans, and 1A + 1B valency are correct in the intended model.
- Full-antibody geometry preserves required same-antigen simultaneous binding and independent arm access in plausible ensembles.
- Sequence/model checks do not substitute for later experimental confirmation of correct assembly and product purity.

## Step 15 — Filter Complete Constructs for Geometry and Developability

### Inputs

- Full 1A + 1B antibody ensembles.
- Sequence and interface results from earlier steps.

### Tasks

1. Evaluate full-construct properties:
   - Domain folding confidence.
   - Inter-domain clashes, hinge strain, and incorrect chain-pairing risks.
   - Exposed hydrophobic patches.
   - Charge distribution and predicted pI.
   - Aggregation and self-association risk.
   - Chemical sequence liabilities.
   - Non-human or potentially immunogenic sequence features.
   - Fc and glycan accessibility.
2. Separate sequence-derived, structure-derived, and format-derived developability evidence in the scorecard.
3. Evaluate unwanted receptor networking or B7-H3 crosslinking using multiple antigen-density and spacing scenarios.
4. Distinguish potentially useful clustering for internalization from uncontrolled higher-order networking.
5. Confirm that neither domain is consistently occluded by the other domain or Fc.
6. Run negative controls through the same scoring pipeline to identify score artifacts.
7. Create a per-construct risk register with severity, confidence, mitigation, and experimental follow-up; do not hide unresolved high-risk features inside a total score.
8. Identify which risks are intrinsic to the molecule and which depend on formulation, concentration, expression system, or intended route of administration.

For constructs that reach experimental planning, the risk register should nominate
fit-for-purpose follow-up such as expression and SEC profile, thermal unfolding,
monomer/aggregate and sub-visible-particle assessment, charge heterogeneity,
hydrophobicity or self-interaction screens, polyspecificity/polyreactivity assays,
chemical-stability or forced-degradation studies, and concentration-dependent
viscosity. The exact panel depends on format and intended use; computational
scores do not replace these measurements.

### Outputs

- `work/15_full_construct_filtering/developability_scores.csv`
- `work/15_full_construct_filtering/developability_risk_register.csv`
- `work/15_full_construct_filtering/crosslinking_scenarios.csv`
- `work/15_full_construct_filtering/risk_register.csv`
- `results/scorecards/final_construct_scorecards/`

### Completion Gate

- No unresolved severe clash, folding, aggregation, or sequence-liability flag is accepted without an explicit decision and mitigation rationale.
- Intended and unintended crosslinking scenarios are explicitly distinguished.
- Remaining uncertainties are documented for experimental testing.
- The selected constructs have an interpretable risk profile across all five developability classes; no single composite score is the sole basis for selection.

## Step 16 — Select the Computational Candidate and Control Panel

### Inputs

- Final construct scorecards and risk register.

### Tasks

1. Select a diverse panel rather than only the top-ranked construct.
2. Include several A+B candidates spanning:
   - Feasible Fab-arm/hinge geometries within the approved 1A + 1B format.
   - Approved hinge or pairing variants where relevant.
   - More than one A and B parent lineage.
   - Different predicted affinity/developability trade-offs.
3. Include controls processed through the same computational pipeline:
   - A-only binding control with explicit valency/Fc matching or documented mismatch.
   - B-only binding control with explicit valency/Fc matching or documented mismatch.
   - Parental, non-optimized A+B construct.
   - Optimized A+B constructs.
   - Nonbinding or paratope-disrupted control for later experiments.
4. Freeze exact amino-acid sequences and record stable construct IDs and sequence versions.
5. Record the reason each candidate or control was selected.

### Outputs

- `results/candidates/final_panel.fasta`
- `results/controls/control_panel.fasta`
- `results/candidates/final_panel.csv`
- `results/scorecards/final_selection_matrix.csv`
- `reports/decision_log.md`

### Completion Gate

- The panel tests Fab/hinge geometry, approved pairing variants, parent lineage, and optimization effects within the 1A + 1B architecture.
- Every construct has a frozen sequence, unique ID, provenance, developability risk summary, and selection rationale.

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
   - Required simultaneous A/B engagement of one antigen, distinct from separate-antigen occupancy.
   - Correct heavy/light-chain pairing, A/B assembly, and product purity.
   - Native cell-surface binding.
   - Internalization.
   - Tumor-cell removal and Fc-dependent function, where intended.
6. Create a blinded construct key if unbiased experimental comparison is desired.
7. Freeze the computational release with a version tag and concise analysis notes; a machine-readable manifest is optional.

### Outputs

- `reports/final_computational_report.md`
- `reports/run_manifest.json`
- `results/experimental_handoff/`
- `results/experimental_handoff/construct_key.csv`
- `results/experimental_handoff/experimental_questions.md`

### Completion Gate

- A second operator or agent can trace every final sequence back to its inputs, important commands, models, and decisions.
- All constructs are clearly labeled as computational predictions pending experimental validation.

---

## Provisional Computational Funnel

The approved Step 4–5 breadth pilot is documented in
`reports/step4_backbone_sequence_pilot.md`. Its values are fixed for this
pilot and may be revised only after the pilot is reviewed.

| Stage | Suggested starting scale per epitope |
|---|---:|
| RFantibody pilot backbones | 100–300 per active epitope/hotspot definition |
| RFantibody production backbones | Approximately 10,000 total |
| ProteinMPNN sequences | Approximately 4 per retained backbone in the approved pilot; 5–20 remains configurable later |
| RF2 primary validation | All deduplicated sequences |
| AlphaFold 3 primary independent validation | RF2-filtered subset, multiple seeds/samples |
| RF3 complementary analysis | AF3-evaluated subset, multiple samples; not a hard gate |
| Parent antibodies | Approximately 20–50 diverse designs |
| Affinity-optimization variants | Configured by mutable positions and compute budget |
| Final A+B constructs | Diverse, experimentally manageable panel |

## Core References and Software Documentation

- [Human CD276/B7-H3, UniProt Q5ZPR3](https://www.uniprot.org/uniprotkb/Q5ZPR3/entry)
- [RFantibody repository and practical design guidance](https://github.com/RosettaCommons/RFantibody)
- [Atomically accurate de novo design of antibodies with RFdiffusion](https://www.nature.com/articles/s41586-025-09721-5)
- [ProteinMPNN repository](https://github.com/dauparas/ProteinMPNN)
- [RoseTTAFold3 documentation in RosettaCommons Foundry](https://github.com/RosettaCommons/foundry/blob/production/models/rf3/README.md)
- [RosettaCommons Foundry repository](https://github.com/RosettaCommons/foundry)
- [AlphaFold 3 repository](https://github.com/google-deepmind/alphafold3)
- [AlphaFold 3 input specification](https://github.com/google-deepmind/alphafold3/blob/main/docs/input.md)
- [AlphaFold 3 output-confidence specification](https://github.com/google-deepmind/alphafold3/blob/main/docs/output.md)
- [Rosetta InterfaceAnalyzer](https://docs.rosettacommons.org/docs/latest/application_documentation/analysis/interface-analyzer)
- [Rosetta Flex ddG](https://docs.rosettacommons.org/docs/latest/flex-ddG)
- [Human B7-H3–20G5 complex, PDB 9LY5](https://www.rcsb.org/structure/9LY5)
- [Blueprint for antibody biologics developability](https://pmc.ncbi.nlm.nih.gov/articles/10012935/)
- [Developability considerations for bispecific and multispecific antibodies](https://pmc.ncbi.nlm.nih.gov/articles/PMC11352713/)
- [FDA: Immunogenicity Assessment for Therapeutic Protein Products](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/immunogenicity-assessment-therapeutic-protein-products)
