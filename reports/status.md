# Project status

Updated 2026-09-21.

## Current work — Step 0 documentation and coordination

Automatic PM–DEV handoffs are authorized for Step 0 only. The existing Codex
session queue delivered the coordination check to PM, which acknowledged nonce
`step0-link-20260918` and assigned `STEP0-001`. Protocol and role-owned records
are under `coordination/`.

DEV prepared `reports/step0_scope.md` and `reports/decision_log.md` from existing
documents. PM accepted `STEP0-001` and returned its review through the session
queue, completing a task-and-review cycle. The Step 0 scientific scope gate remains open:
Fc/architecture details, budget/diversity, and risk
policies require user decisions. No target preparation, installation, model/data
acquisition, or scientific run was performed. No active jobs were found in the
startup scheduler check; no jobs were submitted by this work.

`STEP0-002`: recorded the user's requirements for dual-epitope binding,
internalization, Fc-mediated tumor-cell killing, stability, low aggregation, and
well-characterized, sufficiently separated epitopes. PM accepted the transcription.
The user then selected all three objectives as required, with trade-offs flagged
for their decision (`STEP0-003`). Numerical criteria and other scope choices stay open.

`STEP0-004`: user confirmed human B7-H3 binding is required and cross-species
binding is not required. Isoform/soluble policy was later resolved in STEP0-006.
PM accepted this transcription.

`STEP0-005`: literature-only isoform/soluble-antigen recommendation prepared in
`reports/step0_isoform_review.md`; PM accepted the evidence review. No target preparation or
compute. The policy was subsequently approved in STEP0-006.

`STEP0-006`: user approved required cell-surface human 4Ig binding for both
units, characterization of optional 2Ig binding, and soluble-antigen interference
assessment without a neutralization goal or zero-binding rule. PM accepted the
transcription.

`STEP0-007`: user requires simultaneous A/B engagement of distinct epitopes on
the same human 4Ig-B7-H3 molecule. Feasibility is unverified; independent binding
or binding different molecules alone is insufficient. PM accepted the transcription.

`STEP0-008`: user clarified a full IgG-like 1A + 1B antibody with Fc, replacing
the tandem-scFv-Fc 2A + 2B assumption. Workflow Steps 11–14, controls/handoff,
README, and scope/decision records updated; PM accepted the final revision. No target
preparation or compute. Historical architecture descriptions are superseded.

Next: resolve Fc isotype/hinge and heavy/light-chain pairing implementation,
then remaining quantitative policies. Same-antigen binding remains required.
Step 1 requires separate authorization. AGENTS.md and permission settings remain
unchanged. The September 16 setup history below remains applicable.

## Completed milestone

Reviewed the scope, workflow, and runtime guidance of all 19 imported skills.
Adapted active instructions and converter templates to the analysis-first
contract; preserved upstream sources. Linked skills for project-local discovery,
added the task index and Rorqual environment, and reconciled key project docs.

## Scientific execution status

No antibody analyses or compute jobs were run for this setup. Predictor/model
paths and dependency-heavy analysis environments remain unverified; see
`config/hpc/README.md`. No new packages or model downloads were installed.
No active project jobs or transfer tasks were created.

## Previously recorded next analysis — not currently authorized

Use `binder-antibody-design` and relevant literature/structure references to
prepare B7-H3 target inputs under Step 1 of the scientific workflow. Resolve the
specific scientific scope and dependencies needed for that task. Preserve glycan
and membrane context when considering the upstream target-cropping example.

## Setup checks

All 19 skills passed the existing skill-format checker. Codex app-server
`skills/list` with a forced reload returned all 19 project skills enabled. The
relative discovery links resolve; the environment file passed Bash syntax checking
and exported the intended project paths and CPU/GPU accounts. Converter templates
match the maintained skill instructions. Upstream source files are unchanged.
These checks establish instruction discovery and environment configuration, not
scientific execution readiness.

## 2026-09-16 plan-hardening milestone

Revised `doc/project-1-computational-first-process.md` after a full workflow
review. Added a pre-production scope gate, full-target back-mapping before
RFantibody scale-up, and an explicit developability assessment spanning sequence
and chemical liabilities, conformational stability, colloidal behavior, format
and process risk, and immunogenicity hypotheses. Integrated the risk assessment
through mutation, ensemble ranking, linker selection, and complete Fc-dimer
filtering. Added construct-level risk records and fit-for-purpose experimental
follow-up categories, while keeping computational predictions distinct from
measurements. Plan references now include antibody developability and
immunogenicity guidance.

`STEP0-009`: Fc/pairing evidence review prepared in
`reports/step0_fc_pairing_review.md`. Recommends effector-competent human IgG1 and
preservation of cognate Fab pairs, with cFAE the leading assembly route and
CrossMab an alternative. Recommendations remain unselected; PM artifact review
requested. No scientific runs, installations, target preparation or Step 1 work.
PM accepted STEP0-009 with no material artifact correction. The independent PM
record clarifies that standard cFAE need not mutate the native IgG1 hinge.

`STEP0-010`: the user approved proceeding with the recommended provisional
baseline. The working product is a complete human IgG1-like 1A + 1B antibody
with active Fc, cognate Fab pairing, cFAE as leading assembly, and CrossMab as
fallback. Exact sequences, Fc mutations, hinge, glycoform, FcRn policy and
construct-specific performance remain unresolved. PM review is pending.

`STEP0-011`: prepared a provisional screening and developability policy. It
keeps binding, cis geometry, internalization, Fc activity, and developability
as separate evidence tracks; preserves diversity; and keeps numerical budgets,
thresholds and assay cutoffs open. PM review requested.

`STEP1-001`: ran the existing target-preparation worker with the verified
scipy-stack module. Canonical human 4Ig inputs, mapped experimental structures,
membrane-frame outputs, glycan controls, and QC metadata were produced. The
short 2Ig form is retained as a membrane comparison using its own
isoform-specific span around residues 250–271; soluble/shed antigen remains a
separate state. Preliminary 20G5-like and T3CL11-like contact regions are
documented for Step 2; final epitope carry-forward remains a scientific
decision.

PM review found and DEV corrected an N-terminal affinity-tag alignment issue in
9LME: the regenerated map anchors model residue 29 onward to canonical residue
29 onward (resolved range 29–240). The 2Ig membrane interpretation was also
corrected; soluble/shed antigen remains separate. PM accepted the corrected
artifact with no material correction. Step 2 still requires a user decision on
which preliminary candidate regions to carry forward.
