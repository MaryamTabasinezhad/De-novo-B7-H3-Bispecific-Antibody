# Project status

Updated 2026-09-24.

## Current work — Step 2 geometry and Step 3 anchor preparation

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
`bd0dc0b`. It was submitted as Slurm job `21741284` on 2026-09-24 with three
recycles per arm, official `RF2_ab.pt` weights, and seeds 101 (Arm A) and 202
(Arm B). Outputs are being written to
`/scratch/ghaedi/mab/rfantibody_b7h3_rf2_20260924/`. This is a bounded
sequence/structure validation pilot; it is not a final 1A+1B IgG or
same-antigen bispecific result.

The full pilot candidate accounting is recorded in
`reports/candidate_accounting.md`. In the corrected lineage, 2/2 input windows
passed QC, 2 arm backbones passed after the Arm A retry, ProteinMPNN produced 4
sequence candidates (2 per arm), and all 4 are awaiting RF2 validation. No RF2
survivor is confirmed yet. The workflow's approximately 10,000-backbone
production figure and 5–20 sequences per retained backbone are planning ranges,
not completed work or a current production run.

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
