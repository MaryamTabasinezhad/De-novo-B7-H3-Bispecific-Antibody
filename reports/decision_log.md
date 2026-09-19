# Scientific decision log

Updated 2026-09-19. Source: `doc/project-1-computational-first-process.md`, Step 0 and related sections. Initial record: `STEP0-001`. User requirements and decisions recorded below in `STEP0-002` through `STEP0-007`.

| ID | Decision required | Existing evidence | State / question for user |
|---|---|---|---|
| S0-01 | Biological endpoint priority | Workflow lists binding, internalization, tumor-cell removal, and Fc-mediated function | Resolved at objective-policy level: all three are required; flag trade-offs to the user rather than deprioritizing an objective |
| S0-02 | Isoform/species and soluble-antigen scope | Human CD276 is the target; Step 1 names 4Ig and 2Ig, with context-dependent 2Ig inclusion | Resolved at scope-policy level: both units must recognize cell-surface human 4Ig; characterize optional human 2Ig binding; assess soluble-antigen interference without targeting neutralization; other-species binding not required |
| S0-03 | Exact architecture and Fc intent | Tandem-scFv-Fc dimer with 2A + 2B is the current assumption | Partially resolved: immune-effector recruitment is desired; architecture/valency confirmation, Fc species/isotype, hinge, exact effector mechanism, and FcRn intent remain unresolved |
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
