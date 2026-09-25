# Project status

Updated 2026-09-25 16:41 UTC.

**Reporting contract:** `reports/status.md` is the single canonical project
status report. All future job submissions, completions, QC results, blockers,
and next-step updates must be recorded here and pushed to GitHub.

## Current work — Step 4–5 breadth pilot planning

Automatic PM–DEV handoffs are authorized for Step 0 only. The existing Codex
session queue delivered the coordination check to PM, which acknowledged nonce
`step0-link-20260918` and assigned `STEP0-001`. Protocol and role-owned records
are under `coordination/`.

The following paragraphs summarize the initial Step 0 coordination history;
later execution updates appear below.

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

Step 0 baseline and screening policy are recorded. Step 1 target preparation is
complete as a preliminary mapped ensemble, with PM acceptance after correcting
the Q5ZPR3-2 isoform interpretation and 9LME affinity-tag mapping. The user has
now confirmed the Step 2 preliminary pair: Arm A is the 8H9-like exposed IgV1
FG-loop region and Arm B is the coordinate-derived exposed IgC1 patch 2 around
Q228–R241. No antibody sequence design has started. AGENTS.md, prompts, and
permission settings remain unchanged.

## Completed milestone

Reviewed the scope, workflow, and runtime guidance of all 19 imported skills.
Adapted active instructions and converter templates to the analysis-first
contract; preserved upstream sources. Linked skills for project-local discovery,
added the task index and Rorqual environment, and reconciled key project docs.

## Scientific execution status

Step 1 target preparation ran locally with the verified `scipy-stack/2023b`
module. It produced mapped target metadata, membrane-frame PDB outputs, glycan
controls, and QC records. No antibody sequence design, SLURM job, installation,
model download, or production-scale compute run has occurred.

## Current next analysis — preliminary same-antigen geometry check

The confirmed Arm A/Arm B pair has been carried into a preliminary same-antigen
geometry check. The oriented unbound model gives approximately 61.6 Å centroid
separation and 33.5 Å minimum heavy-atom separation; the 9LY6 model gives 62.0 Å
and 34.2 Å. These are distinct-surface measurements, not Fab-reach or
simultaneous-binding evidence. Preliminary Step 3 anchor sets are recorded for
both arms, while sequence design remains gated on glycan/membrane-aware Fab-pair
geometry.

The Step 1 worker was rerun on 2026-09-21 with the verified
`scipy-stack/2023b` module. The canonical mappings, five-model manifest, and
798-row numbering map were regenerated and inspected. Remaining Step 1
ensemble tasks—representative modeled glycoforms, loop repair/relaxation,
4Ig oligomer hypotheses, and a validated membrane-tilt ensemble—remain blocked
by unverified scientific runtimes; no substitute software or installation was
used.

RFantibody provisioning is authorized and complete outside the repository. The
official RosettaCommons source, isolated uv environment, CUDA 11.8 PyTorch
stack, and official weights are installed in scratch. GPU smoke job 21526260
completed successfully. The bounded two-arm pilot then completed: RFdiffusion
21526509, ProteinMPNN 21526896, and RF2 21526897 all exited 0. The pilot
produced backbones, sequences, and RF2 structures. QC found severe sub-angstrom
heavy-atom overlaps between antibody and target chains in the output structures;
RF2 also reported no interface residues for the B-arm inputs and disabled
hotspots. These outputs are rejected for design ranking and are not evidence of
target binding. Diagnosis identified the previous pilot's non-default
`diffuser.T=50` override as a likely contributor to the large motif RMSD and
clashes. A one-design-per-arm corrected RFdiffusion pilot using the model
default diffusion horizon was submitted as SLURM job 21563096. It completed,
but the follow-up still reported approximately 24–28 Å motif RMSD and produced
sub-angstrom H/L–T overlaps for both arms. It therefore also fails geometry QC;
the diffusion-horizon override was not the sole cause. Dependent ProteinMPNN and
RF2 jobs remain unsubmitted while RFantibody target and motif handling are
diagnosed against a known-good example.

`21666857` passed the tracked input-pipeline QC after correcting two preparation
errors: the wrong source chain had been selected from the 20G5 complex, and the
spatial crop had disconnected Cα segments. Corrected contiguous AFDB-target
windows now pass chain, hotspot, continuity, and pre-existing clash checks. The
next gated task is an official runtime control, followed by one corrected
RFantibody backbone design per arm.

The tracked official runtime-control job `21666899` was submitted on 2026-09-23
to the H100 MIG partition and is pending scheduler priority. No B7-H3 design,
ProteinMPNN, or RF2 job has been submitted while this control is pending.

Runtime control `21666899` has now completed successfully (exit 0). The
official RSV example produced motif RMSD 0.13 Å, H/L/T chains, and no runtime
errors. The next gated task is one corrected B7-H3 RFantibody backbone design
per arm using the passing input-pipeline crops.

Corrected B7-H3 RFantibody pilot job `21670962` was submitted on 2026-09-23
using the passing input crops, one design per arm, default diffusion horizon,
and the approved Arm A/Arm B hotspots. Slurm terminated it at the one-hour time
limit before either arm produced an output PDB. This is an execution-time
failure, not a scientific result. ProteinMPNN and RF2 remain unsubmitted.

The retry was split into independent two-hour arm jobs: Arm A `21676743` and
Arm B `21676744`. Both completed successfully. Motif RMSD was below 0.35 Å for
both arms and hotspot sequences were IRDF (A) and QQHSTTQR (B). Arm B has a
3.047 Å minimum H/L–T distance and is a provisional backbone-QC pass. Arm A
has one 1.758 Å H/L–T atom pair and is held for a fresh backbone draw. No
ProteinMPNN or RF2 job has been submitted yet.

Fresh nondeterministic Arm A retry job `21681492` was submitted with a separate
two-hour allocation. Arm B remains at its provisional backbone-QC pass while
this retry is pending.

Arm A retry `21681492` completed successfully. It reported motif RMSD
0.21–0.25 Å, minimum H/L–T distance 2.768 Å, and no pair below 2.0 Å. Both
arms now pass the preliminary backbone QC and are eligible for a bounded
ProteinMPNN sequence pilot. No sequence-design job has started yet.

ProteinMPNN pilot job `21719319` completed successfully with two deterministic
CDR-loop sequences per accepted backbone (four candidates total). The tracked
RF2 wrapper `tools/rfantibody_b7h3_rf2_job.sh` was committed and pushed as
`bd0dc0b`. RF2 job `21741284` completed successfully on 2026-09-24 with three
recycles per arm, official `RF2_ab.pt` weights, and seeds 101 (Arm A) and 202
(Arm B). It produced four best PDBs, but all four failed the preliminary
geometry screen: each had a minimum H/L–T heavy-atom distance below 2.0 Å.
Therefore 0/4 candidates pass RF2 QC. Results and the scratch paths are
recorded in `reports/rfantibody_b7h3_rf2_qc.md`; no candidate advances to
independent validation or whole-IgG assembly until coordinate handling is
diagnosed.

The full pilot candidate accounting is recorded in
`reports/candidate_accounting.md`. In the corrected lineage, 2/2 input windows
passed QC, 2 arm backbones passed after the Arm A retry, ProteinMPNN produced 4
sequence candidates (2 per arm), and RF2 evaluated all 4; 0/4 passed the RF2
geometry screen. The workflow's approximately 10,000-backbone
production figure and 5–20 sequences per retained backbone are planning ranges,
not completed work or a current production run.

To distinguish a model/input problem from a B7-H3-specific result, the tracked
official RF2 H/L/T example control
(`tools/rfantibody_rf2_official_control_job.sh`) was committed and pushed as
`5aa41c9`, then completed successfully as Slurm job `21747881`. With the same
RF2_ab weights, three recycles, cautious mode, and shared geometry checker, the
official output had pLDDT `0.903`, minimum heavy-atom H/L–T distance `3.167 Å`,
6 contacts below 4.5 Å, and zero overlaps below 2.0 Å. The shared checker was
corrected to recognize digit-prefixed hydrogen atom names, and both the
official control and B7-H3 outputs were recomputed. The control still passes
and points to a B7-H3 input/output representation issue rather than a
universal RF2 or checker failure. Details are in
`reports/rfantibody_rf2_official_control.md`.

## Current refresh — 2026-09-25

No project Slurm jobs are active. The official RF2 control `21747881` and the
B7-H3 RF2 pilot `21741284` both completed successfully at the scheduler level.
The official control passed the corrected heavy-atom geometry check, while the
four B7-H3 RF2 outputs remain rejected for sub-2 Å overlaps. The coordinate
audit confirms that the accepted backbones and ProteinMPNN inputs are clean and
that the problematic overlaps are introduced in the RF2 B7-H3 outputs.

The project was previously paused at this diagnostic gate: no candidate
advances to AF3, RF3, whole-IgG assembly, or production-scale generation. That
diagnostic-only next step is superseded by the user's later STEP4-001 breadth
pilot decision below. This refresh was written on 2026-09-25 so the tracked
status reflects the current scheduler and scientific state.

The user has now approved a bounded Step 4–5 breadth pilot. The scope is
100–300 RFantibody backbones per active epitope/hotspot definition and
approximately four ProteinMPNN sequences per retained backbone. The current
two-definition scope is Arm A and Arm B, for a planning range of 200–600
backbones and approximately 800–2,400 sequences before filtering. This is a
documentation and authorization milestone only; no jobs have been launched for
this breadth pilot. The complete scope and promotion gates are in
`reports/step4_backbone_sequence_pilot.md`, and the decision is recorded as
`STEP4-001` in `reports/decision_log.md`.

The first breadth-pilot execution has now been submitted through the tracked
array wrapper `tools/rfantibody_b7h3_backbone_pilot_array.sh` (commit
`fe5da2d`). Arm A array `21799356` and Arm B array `21799357` each contain 100
one-design GPU tasks with a maximum concurrency of 20 and a two-hour task
limit. They use the corrected target crops, the fixed H/L/T framework, the
approved Arm A/Arm B hotspot sets, the RFdiffusion antibody weights, one design
per task, and independent nondeterministic tasks for pilot diversity. Outputs
are written under
`/scratch/ghaedi/mab/rfantibody_b7h3_backbone_pilot_20260925/{A,B}/task_<id>/`.
No ProteinMPNN or RF2 expansion has been submitted for this breadth pilot yet;
those stages remain gated on backbone output inspection and QC.

## Pilot execution refresh — 2026-09-25 15:22 UTC

Arm A array `21799356` has completed all 100/100 tasks successfully and has
produced 100 backbone PDBs with per-task metadata. Arm B array `21799357` has
completed 12/100 tasks, has 6 tasks running, and has 82 tasks pending scheduler
priority; 12 backbone PDBs with metadata are currently available for Arm B.
No task failures or timeouts are recorded so far. Output inspection and
backbone QC will begin only after the corresponding arm's task set is complete;
ProteinMPNN remains unsubmitted for this pilot.

The user expanded the pilot to the upper bound of **300 backbones per arm**.
Additional array `21802537` (Arm A, tasks 100–299) and array `21802538` (Arm B,
tasks 100–299) were submitted with the same tracked wrapper and resources.
Together with the original 0–99 arrays, these will produce 300 Arm A and 300
Arm B backbone tasks without duplicating completed task IDs. The additional
arrays are currently pending scheduler priority.

## Pilot execution refresh — 2026-09-25 16:03 UTC

The original Arm A array `21799356` and original Arm B array `21799357` are
complete at 100/100 tasks each. The additional Arm A array `21802537` has
159/200 tasks completed, 10 running, and 31 pending; Arm A currently has 259
backbone PDBs and metadata records available out of the 300 target. The
additional Arm B array `21802538` remains pending, so Arm B currently has 100
backbone PDBs out of the 300 target. No array task failures are recorded.

Both expanded arrays have now completed successfully: Arm A array `21802537`
and Arm B array `21802538` each completed 200/200 additional tasks, with no
array task failures recorded. The full breadth pilot therefore contains 300/300
Arm A backbone PDBs and 300/300 Arm B backbone PDBs, each with per-task
metadata. Backbone QC is the current gate. No ProteinMPNN jobs have been
submitted for the breadth pilot yet.

The next stage is a traceable ProteinMPNN array: approximately four
deterministic CDR-loop sequences per backbone, up to 1,200 Arm A and 1,200 Arm
B sequences (2,400 total) before sequence QC. RF2 remains downstream of
ProteinMPNN outputs and will not be submitted in advance.

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
construct-specific performance remain unresolved. PM accepted the Step 0
baseline with no material correction.

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
