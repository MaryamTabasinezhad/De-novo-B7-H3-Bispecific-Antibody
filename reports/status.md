# Project status

Updated 2026-09-27 04:36 UTC.

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

The detailed RF2_ab scientific explanation is recorded in
`reports/rf2_ab_review.md`. It documents why RF2_ab is the antibody-specific
post-ProteinMPNN validation gate, what it can and cannot establish, and how the
earlier B7-H3 diagnostic result is interpreted. The separate RF3 note remains
in `reports/rf3_ab_review.md` for future independent-validation planning.

The ProteinMPNN wrapper `tools/rfantibody_b7h3_proteinmpnn_array.sh` was
committed and pushed as `def2020`. Arm A array `21807824` and Arm B array
`21807825` were submitted with 300 one-backbone tasks each, maximum concurrency
20, one-hour task limits, CDR loops H1/H2/H3/L1/L2/L3, temperature 0.1, four
sequences per backbone, and the official
`ProteinMPNN_v48_noise_0.2.pt` weights. The original arrays completed at the
Slurm level, but output inspection found 22 Arm A tasks and 34 Arm B tasks with
zero sequence PDBs. Their logs show a `FileNotFoundError` from the RFantibody
wrapper's shared relative `temp.pdb`; concurrent tasks on the same node could
collide even though Slurm reported exit 0. The wrapper was corrected in commit
`6b962a3` to run each task from its unique output directory.

Before retry, 278 Arm A tasks produced four sequences each (1,112 PDBs) and
266 Arm B tasks produced four each (1,064 PDBs). Retry arrays `21836469` (Arm A,
22 missing task IDs) and `21836470` (Arm B, 34 missing task IDs) were submitted
with the corrected wrapper. Outputs and metadata remain under
`/scratch/ghaedi/mab/rfantibody_b7h3_proteinmpnn_20260925/{input,output}/`.
RF2 remains gated until all 2,400 sequence outputs are present and checked.

The user authorized RF2 on the sequence models already available, without
waiting for the missing ProteinMPNN retries. The tracked wrapper
`tools/rfantibody_b7h3_rf2_array.sh` was committed and pushed as `434773c`.
Arm A RF2 array `21836656` and Arm B RF2 array `21836657` were submitted with
300 task slots each, three recycles, `RF2_ab.pt`, task-specific seeds, and
empty-task skipping. At submission, 1,128 Arm A and 1,064 Arm B sequence PDBs
were available; the arrays process each existing task directory and record
skipped empty directories. Both RF2 arrays are currently pending scheduler
priority. RF2 outputs will be QC'd before any candidate ranking or whole-IgG
assembly.

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

## RF2 execution update — 2026-09-27 04:03 UTC

The authorized RF2_ab arrays completed successfully at the scheduler level:
Arm A job `21836656` and Arm B job `21836657` completed all 300/300 task
slots with Slurm exit code 0. RF2 processed the currently available
ProteinMPNN outputs and wrote 1,176 Arm A `*_best.pdb` structures and 1,188
Arm B structures, 2,364 RF2 structures total. The RF2 metadata records six
Arm A and three Arm B task directories as skipped because their input sequence
directory was empty; this reflects the earlier ProteinMPNN output shortfall,
not a successful design result.

No non-empty RF2 stderr files were found for these arrays. The structures have
not yet passed the project geometry/interface QC or candidate-ranking gate.
RF2 completion therefore does not authorize AF3/RF3, whole-IgG assembly, or
experimental claims. The next computational gate is a traceable QC summary
over the 2,364 RF2 outputs, with rejected structures and reasons preserved.

The QC worker was committed as `57925db` and submitted to Slurm as CPU job
`21885138`. It loads the verified `scipy-stack/2026b` environment and writes
separate Arm A and Arm B TSV summaries under
`results/rfantibody_b7h3_rf2_qc_20260927/`. The job was pending at submission;
its completion and scientific pass/reject counts will be recorded here before
any downstream ranking.

The first submission failed immediately because `scipy-stack/2026b` is listed
by module discovery but is not available on this cluster (`21885138`, exit
`1:0`). The worker was corrected to use the available `scipy-stack/2025a`
module; no scientific QC calculation ran in the failed attempt. A replacement
submission is required and will supersede the failed job.

Replacement QC job `21885145` was submitted with the corrected module and was
pending at the scheduler check. Its Slurm result and QC counts remain pending.

Replacement job `21885145` completed successfully in 34 seconds (Slurm exit
`0:0`). It processed 1,176 Arm A and 1,188 Arm B RF2 structures and wrote the
durable TSV summaries under `results/rfantibody_b7h3_rf2_qc_20260927/`. Under
the current hard geometry screen (minimum heavy-atom distance at least 2.0 Å
and zero antibody–target pairs below 2.0 Å), direct inspection found 167/1,176
Arm A and 155/1,188 Arm B structures meeting that geometry criterion. The
remaining structures contain 55,880 Arm A and 70,993 Arm B sub-2.0 Å overlap
pairs. The mean minimum distances across all models were 1.047 Å and 0.975 Å,
respectively. These are computational geometry results, not claims about
measured binding. The pass subset is eligible for the next screening report;
the overlap-rejected structures remain excluded from ranking and downstream
AF3/RF3 or whole-IgG work.

The initial report incorrectly stated zero passes because its shell count did
not strip carriage returns from the TSV status field. The QC worker now writes
Unix line endings, and the job is being rerun to replace the durable summaries
and verify the corrected counts.

Corrected QC rerun `21885271` was submitted and was pending at the scheduler
check. Its output will supersede the earlier line-ending-affected summaries.

Corrected QC rerun `21885271` completed successfully in 25 seconds (Slurm exit
`0:0`). The Unix-line-ending summaries now count 167/1,176 Arm A models and
155/1,188 Arm B models as geometry passes; 1,009 Arm A and 1,033 Arm B models
remain rejected for at least one sub-2.0 Å antibody–target overlap. Among the
passes, 50 Arm A and 37 Arm B have minimum distances at least 3.0 Å, and 11
Arm A and 13 Arm B are at least 4.0 Å. The pass subset is now the valid input
for the next interface-screening stage, while the rejected structures remain
excluded.

The interface-screening worker was committed as `ab5ffc5` and submitted as
CPU Slurm job `21885408`. It uses the canonical crop mappings (Arm A target
86–169 and Arm B target 188–281) to translate RF2's renumbered target chain
back to the selected Arm A residues 126–129 and Arm B residues 228, 229, 232,
234, 236, 238, 240 and 241. It screens only the 322 geometry-passing models
and writes durable per-model TSV files under
`results/rfantibody_b7h3_interface_20260927/`. The job was pending at
submission; its completion and contact-coverage counts will be recorded here.

Interface screen job `21885408` completed successfully in four seconds (Slurm
exit `0:0`). Of the 167 Arm A geometry passes, 162 contacted some target
residue and 70 contacted at least one selected Arm A residue; 37 contacted at
least two selected residues. Of the 155 Arm B geometry passes, 148 contacted
some target residue and 129 contacted at least one selected Arm B residue; 98
contacted at least two selected residues. H/L chain contact counts were 98/167
for Arm A and 107/155 for Arm B. The detailed method and per-model records are
in `reports/rfantibody_b7h3_interface_screen.md` and
`results/rfantibody_b7h3_interface_20260927/`. These are contact-coverage
observations, not affinity or biological validation; no final interface cutoff
has been selected.

## Current RF2 gate interpretation — 2026-09-27 04:31 UTC

There are 322 geometry-passing RF2 models in total (167 Arm A plus 155 Arm B).
“Passing” here means that the generated coordinates do not contain the defined
sub-2.0 Å antibody–target steric overlap; it does not establish affinity,
epitope engagement, internalization, Fc activity, or developability. The next
step is interface screening of these 322 models: confirm H/L/T chain integrity,
count meaningful target contacts, map contacts to the selected Arm A and Arm B
B7-H3 regions, and preserve per-model rejection reasons. That interface screen
is now complete. No Slurm jobs are active. The next gate is to define a
transparent diversity/contact shortlist from these records and run independent
structure validation on that shortlist; no affinity, internalization, Fc, or
developability claim has been made.

The workflow contract now explicitly records AlphaFold 3 as the required
independent validation method for the RF2-filtered shortlist. It must be run
with documented local availability, multiple seeds/samples, and retained
confidence/interface metrics; AlphaFold 3 predictions remain computational
hypotheses and do not establish affinity or biological activity.

The official-control-equivalent shortlist worker was committed as `01fd0cf` and
submitted as CPU Slurm job `21886323`. It applies the control's observed
minimum H/L–T distance of 3.167 Å and zero sub-2.0 Å overlaps, requires the
existing H/L/T and sequence-mapping checks, and keeps one strongest
interface-scored model per RF2 task. B7-H3 outputs have no pLDDT field matching
the control, so no pLDDT cutoff is invented. The job was running at submission;
its shortlist counts will be recorded here after completion.

Control-equivalent shortlist job `21886323` completed successfully in one
second (Slurm exit `0:0`). It found 42 Arm A and 30 Arm B models meeting the
official-control geometry gate, then retained one strongest interface-scored
representative per RF2 task: 40 Arm A and 29 Arm B models. Among those
representatives, 11 Arm A and 19 Arm B contact at least one selected epitope
residue; 4 Arm A and 11 Arm B contact at least two. The durable shortlist and
full criteria are recorded in
`reports/rfantibody_b7h3_control_shortlist.md` and
`results/rfantibody_b7h3_control_shortlist_20260927/`. This is a structural
shortlist only; the next independent validation gate remains AlphaFold 3.

## AlphaFold 3 runtime check — 2026-09-27

The required AF3 validation cannot be submitted on the current cluster yet.
Runtime discovery found the module `hmmer-alphafold3/3.4`, but it provides only
the `jackhmmer` executable; no AlphaFold 3 runner, model weights, or supported
AF3 command is installed or visible. No AF3 job was submitted, no software was
installed, and no alternative predictor was silently substituted. The 40 Arm A
and 29 Arm B shortlist files remain the frozen input for AF3 once an authorized
and verified runtime is available.

The user authorized AlphaFold 3 installation and required model/runtime setup
on 2026-09-27. Planned scratch locations are
`/scratch/ghaedi/mab/alphafold3_src`, `/scratch/ghaedi/mab/alphafold3_model`,
and `/scratch/ghaedi/mab/alphafold3_db`; no source, container, model weights, or
databases will be committed to Git. The installation will use a cluster-
compatible container/runtime if available, and commands, versions, paths, and
job IDs will be recorded here.

The first direct `uv sync --no-dev` attempt used the shallow source checkout and
reached CMake configuration, but the login-node build failed at Ninja process
creation with `posix_spawn: Operation not permitted`. No package install was
completed by that attempt. The tracked worker
`tools/alphafold3_install_job.sh` moves the same build and AF3 data test into a
CPU Slurm allocation with eight build CPUs; it does not download databases or
model weights.

The Slurm installation/data-test job `21934560` was submitted with the
authorized CPU account and is now running on compute node `rc32308`. Its build,
data-test result, and any infrastructure failure will be recorded before model
weights or databases are considered.

Job `21934560` failed with exit `1:0` after 6:41. The AF3 source and Python
dependency resolution started, but CMake attempted to clone `pybind11` from
GitHub on the compute node and failed after three connection timeouts. This is
a compute-node network restriction, not an AF3 model or scientific result. No
model weights or databases were downloaded. The next installation attempt must
prefetch the C++ dependencies from the login environment and build without
compute-node network access.

The five pinned C++ dependencies (`pybind11`, `abseil-cpp`, `pybind11_abseil`,
`libcifpp`, and `dssp`) were prefetched into
`/scratch/ghaedi/mab/alphafold3_deps` from the login environment at the exact
commits declared by the AF3 CMake file. The installation worker now points
CMake at those local source trees so the retry does not require compute-node
network access.

On the login environment, the AF3 runtime lock was resolved and its 69 Python
runtime packages were cached in the scratch virtual environment. The build
requirements were restored afterward, and the Slurm worker now uses
`--no-build-isolation` so it does not ask PyPI for build packages on the compute
node.

Retry installation/data-test job `21935156` was submitted with the prefetched
dependency paths and was pending at the scheduler check. Its build and AF3 data
test result will be recorded separately from failed job `21934560`.

After `21935156` failed on compute-node PyPI access, the runtime and build
requirements were cached on the login environment and the worker was changed
to `--no-build-isolation`. A new installation/data-test job `21935549` was
submitted and was pending at the scheduler check. This job is the next AF3
installation attempt; no prediction job has been submitted.

## Job-result notification contract — 2026-09-28

After every Slurm, installation, validation, or analysis job, DEV must notify
the user with the exact job ID, success/failure state, inspected evidence, and
the next plan. DEV must update this canonical status report and any relevant
report, commit and push the durable record to GitHub, and report the commit and
push status. A job remains open until its result, blocker or failure
disposition, and next plan are both recorded and communicated.

AF3 retry job `21935156` failed with exit `2:0` after 48 seconds. The local C++
dependency paths were accepted, but `uv` attempted to fetch the Python build
requirements from PyPI on the compute node and timed out. No AF3 package was
installed and no prediction ran. The next plan is to pre-cache the pinned
Python build requirements on the login environment, then rerun the Slurm build
with offline resolution and the already prefetched C++ sources.

Job `21935549` failed with exit `1:0` after two seconds. AF3 reached its build
metadata stage but raised `ModuleNotFoundError: setuptools_scm`, an undeclared
build dependency in the current AF3 `pyproject.toml`. No AF3 package, data test,
model weights, or prediction was produced. The next plan is to cache
`setuptools_scm` in the scratch environment and rerun the same offline build.

`setuptools_scm` and its supporting packages were installed into the scratch
AF3 virtual environment from the login environment. Retry installation/data-
test job `21957223` was then submitted and was pending at the scheduler check.
This retry still performs installation and the official AF3 data test only; no
model parameters, databases, or antibody predictions are involved.

Job `21957223` failed with exit `1:0` after 6:39. Although the dependency
clones were present, CMake did not consume the environment-only source hints and
again attempted a compute-node GitHub clone of `pybind11`. The worker also
needed to restore build requirements after `uv sync`. The next worker revision
passes explicit `CMAKE_ARGS` source directories, performs offline sync, restores
the build requirements offline, and then builds without isolation.

Corrected installation/data-test job `21958028` was submitted with the explicit
offline dependency configuration and was pending at the scheduler check. It is
the current AF3 installation attempt; no prediction job has been submitted.

Job `21958028` failed with exit `1:0` after 6:53. The explicit local override
worked for `pybind11`, but CMake's content-name normalization leaves the
`abseil-cpp` hyphen in its cache variable, so the incorrect underscore form was
ignored and compute-node GitHub access was attempted. The next retry corrects
that one CMake variable; no AF3 package or prediction has succeeded yet.

Retry installation/data-test job `21959184` was submitted with the corrected
`FETCHCONTENT_SOURCE_DIR_ABSEIL-CPP` setting and is pending scheduler priority.

Job `21959184` failed with exit `1:0` after 6:55. The Abseil override worked;
the next nested dependency was Eigen 3.4.0, fetched by `libcifpp` from GitLab,
and compute-node network access failed again. Eigen 3.4.0, Boost Regex 1.83.0,
and libmcfp 1.3.1 were prefetched on the login environment. The next retry
adds explicit local overrides for these nested CMake dependencies.

Retry installation/data-test job `21960071` was submitted with the nested
dependency overrides and is pending scheduler priority. No AF3 prediction job
has been submitted.

Job `21960071` started at `2026-09-28 10:26:18 UTC` and failed at
`10:28:54 UTC` with exit `1:0` after 2:36. All prefetched C++ dependencies
were accepted; configuration then failed because `libcifpp` attempted to
download the wwPDB chemical-component dictionary from a compute node. The
current protein-only AF3 validation does not require that optional CCD download,
so the next retry disables `CIFPP_DOWNLOAD_CCD` during configuration.

Retry installation/data-test job `21960360` was submitted with the CCD
download disabled. It started at `2026-09-28 10:36:18 UTC` on compute node
`rc32421` and is currently running the AF3 C++ build. No model weights,
databases, or AF3 predictions are involved in this retry.


Job `21960360` failed at `2026-09-28 10:43:16 UTC` on `rc32421` with Slurm exit `1:0` after 6:58. The CCD download was successfully disabled and the prefetched C++ dependencies were accepted. Configuration then entered the optional `libcifpp` test directory, which attempted to clone Catch2 v2.13.9 from GitHub and failed because compute nodes have no outbound GitHub access. No AF3 package, data test, model weights, databases, or predictions were produced. The next retry sets `BUILD_TESTING=OFF`; this skips optional dependency tests that are not required for the AF3 runtime/data-test installation and avoids downloading Catch2.

Retry installation/data-test job `21961067` was submitted with `BUILD_TESTING=OFF` to skip optional Catch2 tests. It is the next offline AF3 installation attempt; no model weights, databases, or AF3 predictions are involved. The preceding milestone commit is `7e3ba16`; its push was rejected because GitHub denied the configured account `hamidghaedi` access to the repository, so the commit remains preserved locally pending authentication/remote authorization.

Job `21961067` started at `2026-09-28 10:56:15 UTC` on `rc32121` and failed at `10:57:34 UTC` with exit `1:0` after 1:19. The AF3 package build completed successfully, but the official data test failed at import because `libcifpp` could not find `components.cif`. Disabling the CCD download avoided the blocked wwPDB fetch but also removed this runtime resource. Per the user instruction, no further job is to be submitted now. No model weights, databases, or antibody predictions were produced.


The official wwPDB chemical-component dictionary was downloaded on the login environment from `https://files.wwpdb.org/pub/pdb/data/monomers/components.cif` (518,315,101 bytes) and staged at `/scratch/ghaedi/mab/alphafold3_deps/cifpp/rsrc/components.cif`. The repair worker now copies this staged file into the libcifpp source tree and enables CCD installation while retaining `BUILD_TESTING=OFF`; compute nodes do not need external network access.

Repair installation/data-test job `21963372` was submitted with the staged wwPDB CCD file and offline C++ dependencies. This is the single authorized retry after failure `21961067`; no prediction job is part of it.
