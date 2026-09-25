# Scientific decision log

Updated 2026-09-21. Source: `doc/project-1-computational-first-process.md`, Step 0 and related sections. Initial record: `STEP0-001`. User requirements and decisions recorded below in `STEP0-002` through `STEP0-011`.

| ID | Decision required | Existing evidence | State / question for user |
|---|---|---|---|
| S0-01 | Biological endpoint priority | Workflow lists binding, internalization, tumor-cell removal, and Fc-mediated function | Resolved at objective-policy level: all three are required; flag trade-offs to the user rather than deprioritizing an objective |
| S0-02 | Isoform/species and soluble-antigen scope | Human CD276 is the target; Step 1 names 4Ig and 2Ig, with context-dependent 2Ig inclusion | Resolved at scope-policy level: both units must recognize cell-surface human 4Ig; characterize optional human 2Ig binding; assess soluble-antigen interference without targeting neutralization; other-species binding not required |
| S0-03 | Exact architecture and Fc intent | User selected a full 1A + 1B IgG-like antibody with Fc (STEP0-008) | Partially resolved: full 1A + 1B IgG-like architecture and immune-effector recruitment required; Fc isotype/sequence, hinge, heavy/light-chain pairing strategy, exact effector mechanism, and FcRn intent remain unresolved |
| S0-04 | Cis binding | Step 0 explicitly asks whether binding both epitopes on one antigen is required | Resolved: simultaneous binding of the two distinct epitopes on the same human B7-H3 molecule is required (STEP0-007) |
| S0-05 | Candidate diversity and compute policy | Multiple diverse candidates required; funnel counts are explicitly provisional | Unresolved: minimum diversity, compute budget, promotion limits, and allowable initial scale |
| S0-06 | Developability priorities and disqualifying risks | Five risk classes and a retain/review/exclude record are specified; thresholds provisional | Partially resolved: stability and low aggregation explicitly required; quantitative criteria and other hard exclusions/review flags remain unresolved |
| S0-07 | Computational versus experimental decision criteria | Predictions are hypotheses; several properties explicitly require experimental follow-up | Unresolved: program-specific acceptance criteria and which purified-protein/cell measurements will establish them |

These questions prevent final scope locking and production-scale design. They do not prevent recording existing assumptions. No provisional answer is inferred from candidate rankings or workflow suggestions. Step 1 remains outside the present authorization even if a subset of these decisions is resolved.

Runtime dependency availability is a separate readiness limitation in `config/hpc/README.md`, not a scientific decision or evidence of an installed tool. Do not silently replace missing software or models.

User decisions should be appended with their date, source conversation or quoted instruction, rationale when supplied, and affected settings. Only the requirements explicitly recorded below are user-specified; remaining fields are unresolved.

## STEP0-002 — user requirements, 2026-09-18

Source: user message in the DEV conversation following the Step 0 endpoint question. The user requested all three listed objectives: binding two distinct B7-H3 epitopes, internalization into B7-H3-expressing cells, and Fc-mediated tumor-cell killing through immune-effector recruitment. The user also requested a stable, low-aggregation antibody and distinct epitopes that are well known for antibody development and sufficiently far apart to avoid binding interference.

Recorded requirements:

- Include all three biological objectives; do not silently drop one. The user subsequently selected option 1: all three are required; flag trade-offs to the user.
- Stability and low aggregation are explicit developability requirements; assay conditions and acceptance thresholds have not been selected.
- Seek well-characterized antibody epitopes in later authorized epitope work. No particular antibody, epitope, residue range, or minimum evidence standard has been selected.
- Require a later assessment of whether epitope placement and construct geometry permit binding without interference. No distance cutoff is inferred, and separation is not treated as proof of simultaneous binding.
- Do not infer a requirement for cis binding on one antigen versus binding different antigen molecules from this statement alone.

Affected records: `reports/step0_scope.md`, `reports/status.md`, and PM coordination. These are design objectives, not evidence of achieved biological activity or developability. No Step 1 or epitope search is initiated by recording them.

### STEP0-003 — endpoint trade-off policy, 2026-09-18

The user replied “1” to the DEV question whose first option was “All three are required; flag trade-offs for me.” Record all three objectives as required, without an inferred numerical weighting or permission to sacrifice one. Escalate conflicts between them to the user. This resolves the objective-level trade-off policy, not quantitative efficacy or assay acceptance criteria. Other scope decisions and the Step 1 boundary remain unchanged.

### STEP0-004 — species requirement, 2026-09-18

Source: direct user instruction in DEV: “human B7-H3 is required; binding to other species is not required”.

Human B7-H3 recognition is required. Cross-species binding is not a design requirement, and candidates must not be rejected solely for lacking it. This is not a requirement to eliminate cross-species reactivity or proof that any candidate is human-specific. It does not decide a later safety-testing strategy, human isoform coverage, or soluble-antigen policy. No animal-target design, cross-species screening, or Step 1 work is initiated by recording this decision.

### STEP0-005 — evidence recommendation, not a user decision

The user authorized PM and DEV to review isoform coverage and soluble-antigen
policy within Step 0. See [evidence review](step0_isoform_review.md). Proposed:
require membrane human 4Ig recognition, characterize but do not require/exclude
human 2Ig binding, and assess soluble antigen as a potential interference risk
rather than intentionally target it. No zero-binding rule or numerical cutoff
is proposed. At review time acceptance was pending; subsequently approved in STEP0-006 below.

### STEP0-006 — isoform and soluble-antigen policy approved, 2026-09-19

Source: after the reviewed recommendation, the user said “ok go forward”. DEV
explicitly restated approval of the proposed policy and the Step 0-only boundary;
the user confirmed “ok do it”.

Approved: both binding units must recognize distinct accessible epitopes on native
cell-surface human 4Ig-B7-H3. Characterize human 2Ig binding, but neither require
nor prohibit it. Soluble B7-H3 is not an intended therapeutic neutralization
target; assess its interference with binding, internalization, Fc-mediated
activity, and disposition when those studies are authorized. Prefer low functional
interference without an unsupported zero-binding rule or numerical threshold.
Revisit if a selected cancer indication supplies compelling contrary evidence.

This resolves S0-02 at policy level. It does not choose epitopes, cis-binding
requirements, Fc details, assay cutoffs, or an indication; it does not authorize
Step 1, target preparation, installations, or compute jobs.

### STEP0-007 — same-antigen simultaneous binding required, 2026-09-19

Source: after DEV contrasted binding the same B7-H3 molecule with binding
different molecules, the user selected: “Must both antibody units bind two
epitopes on the same B7-H3 molecule”.

Record simultaneous engagement of two distinct epitopes on one native human
4Ig-B7-H3 molecule by the A and B binding units as required (cis binding in the
workflow terminology). Binding separate antigen molecules alone is insufficient
to satisfy this criterion. This is a required capability, not a claim that every
occupied construct always adopts this state, and it does not prohibit additional
intermolecular binding by the proposed multivalent construct.

Feasibility remains unverified. Later authorized evaluation must establish
compatible epitope access, binder orientation and full-construct geometry; mere
epitope separation or independent binding by A and B is insufficient evidence.
No epitope pair, linker, Fc detail, numerical spacing cutoff, or final architecture
is chosen here. If this requirement conflicts with another required objective,
raise the trade-off with the user rather than silently relax it. Step 1 and
compute remain outside the present authorization.

### STEP0-008 — full IgG-like 1A + 1B architecture, 2026-09-19

Source: user clarified a whole antibody with Fc, one arm binding site A on B7-H3
and the other arm binding site B. The antigen sites are epitopes; antibody binding
sites are paratopes. Record one Fab A and one Fab B with Fc (1A + 1B), replacing
the earlier 2A + 2B tandem-scFv-Fc assumption. Preserve STEP0-007: both arms must
be capable of simultaneous engagement of the same native human 4Ig-B7-H3 molecule.

Exact Fc isotype/sequence, hinge, heavy-chain heterodimerization and light-chain
pairing strategy remain unresolved; no common light chain or pairing mutations
are selected. Correct assembly and same-antigen geometry require later validation.
If the chosen pairing strategy constrains variable-region design, resolve that
before independent A/B production. No epitope pair or linker sequence is chosen.

Revised the primary workflow, especially Steps 11–14 and format-dependent
controls/handoff, plus README and current scope/status. Planned output directories
change from 11_fusion_assembly, 12_linker_optimization, 14_fc_dimer_models to
11_fab_assembly, 12_hinge_geometry, 14_full_igg_models. No existing analysis output
was moved; no design runs exist. Historical review/coordination records retain
the prior assumption as history. AGENTS.md and permission settings remain
unchanged by the user's earlier boundary; its old architecture description is
superseded by this explicit user instruction. At that milestone Step 1 remained
unauthorized; later authorization and execution are recorded in STEP1-001.

### STEP0-009 — Fc/pairing recommendation, 2026-09-19

Authorized literature review completed in `reports/step0_fc_pairing_review.md`.
Proposed: effector-competent human IgG1, preserve distinct cognate light chains,
cFAE as leading assembly option; CrossMab plus heavy-chain heterodimerization is
an alternative. Common-light-chain constraints would need early incorporation.
Effector enhancement is a comparison question, not selected. This is a DEV
recommendation awaiting user scientific selection, not an approved sequence,
mutation, glycoform, hinge, FcRn policy or Step 1 authorization. Assembly evidence
does not establish same-antigen geometry, internalization, safety or efficacy.

### STEP0-010 — provisional full-antibody baseline, 2026-09-21

User said “ok go” after the full-antibody explanation and recommendation. Record
the working baseline as a complete human IgG1-like 1A + 1B antibody with active
Fc: one Fab-A arm, one Fab-B arm, and Fc retained in the final product. Preserve
each arm's cognate heavy/light variable pair. Controlled Fab-arm exchange (cFAE)
is the leading assembly route; CrossMab remains the fallback comparison.

This is a provisional development baseline, not exact sequences or a claim that
cFAE is superior for B7-H3. Exact Fc mutations, hinge sequence, allotype,
glycoform, FcRn intent, and construct-specific geometry remain open. No common
light chain is required by this baseline. Cis reachability, internalization,
Fc-mediated killing, stability, and low aggregation still require later testing.
Step 1 remains separately gated.

### STEP0-011 — provisional screening policy, 2026-09-21

Prepared `reports/step0_screening_policy.md` as the next bounded Step 0 task.
It proposes staged evidence tracks, preservation of sequence/structure diversity,
approximately 20–50 parents per epitope when supported by the pool, and explicit
hard-exclusion, review-flag, and context-dependent risk dispositions. Numerical
budgets, thresholds, assay conditions, and promotion cutoffs remain open; no
scientific run or Step 1 authorization is inferred.

### STEP1-001 — preliminary target preparation accepted, 2026-09-21

The target-preparation worker produced a preliminary human 4Ig/2Ig ensemble,
canonical numbering metadata, membrane-frame structures, glycan controls, and
QC. PM accepted the corrected artifact: Q5ZPR3-2 is a membrane 2Ig comparison
with its own shifted transmembrane span; soluble/shed antigen remains distinct;
and 9LME model residues 29–240 map to canonical 29–240 after affinity-tag
removal. The 20G5-like and T3CL11-like regions remain approximate preliminary
contact observations. No epitope pair, design anchor, cis result, or antibody
sequence is selected. Step 2 carry-forward awaits the user's decision.

### STEP2-001 — preliminary epitope pair confirmed, 2026-09-21

The user confirmed the preliminary design pair recorded in
`reports/step2_epitope_evidence.md`: Arm A targets the exposed 8H9-like IgV1
FG-loop region around canonical 126–129 (`IRDF`), and Arm B targets the
coordinate-derived exposed IgC1 patch 2 around Q228, Q229, H232, S234, T236,
T238, Q240 and R241. Arm A is supported by experimental 8H9 mapping plus the
independent coordinate exposure screen. Arm B is a structure-derived surface
hypothesis, adjacent to and partly overlapping the edge of the broader 20G5
region, not an assertion that it is identical to the 20G5 footprint.

This decision authorizes carry-forward to the preliminary same-antigen Fab-pair
geometry check only. It does not authorize antibody sequence design, production,
compute, or a claim of simultaneous cis binding. Glycan shielding, membrane
clearance, approach vectors, competition, native-cell accessibility, and
whole-IgG reachability remain validation gates.

### STEP2-002 — preliminary pair geometry recorded, 2026-09-21

The confirmed Arm A/Arm B pair was screened on the oriented unbound 4Ig model
and the oriented 9LY6 antigen chain. Centroid separation was approximately
61.6 Å and minimum heavy-atom separation approximately 33.5 Å in the unbound
model; corresponding 9LY6 values were approximately 62.0 Å and 34.2 Å. These
measurements support distinct surface locations but do not establish Fab reach,
approach-vector compatibility, or simultaneous cis binding. Outputs are in
`metadata/epitope_pair_geometry.csv` and `reports/step2_geometry_check.md`.

### STEP3-001 — preliminary design-anchor candidates recorded, 2026-09-21

Candidate anchor sets were prepared without generating antibody sequences:
Arm A sets A1 (127,129), A2 (127,128,129), and A3 (126,127,129); Arm B sets B1
(228,232,240,241), B2 (229,236,240,241), and B3 (228,229,238,241). These remain
pilot candidates, with evidence classes and canonical mappings in `metadata/`.
Arm B is a polar-rich coordinate-derived surface hypothesis and requires
interaction-diversity and developability review. No RFantibody, ProteinMPNN, or
other sequence-design run is authorized by this record.

### STEP4-001 — breadth pilot scope approved, 2026-09-25

The user approved moving from the tiny setup/diagnostic run to a bounded
Step 4–5 breadth pilot. For each active epitope/hotspot definition, generate
100–300 RFantibody backbone designs and approximately four ProteinMPNN
sequences per retained backbone. The current scope contains one Arm A
definition (8H9-like exposed IgV1 FG-loop) and one Arm B definition (exposed
IgC1 patch 2 around Q228–R241), giving an expected planning range of 200–600
backbones and approximately 800–2,400 sequences before filtering.

The RFantibody, ProteinMPNN, and RF2 toolchain is accepted as operational for
this pilot based on the official runtime/control checks. The earlier four-
sequence B7-H3 RF2 run remains diagnostic and excluded from ranking; its
coordinate failures remain visible in the QC reports. This decision authorizes
documentation and the bounded pilot scope, not production-scale generation or
whole-IgG assembly. Pilot gates, provenance requirements, and planned outputs
are defined in `reports/step4_backbone_sequence_pilot.md`.
