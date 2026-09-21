# DEV coordination record

Updated: 2026-09-21 UTC.

## COORD-001 — PM acknowledgement received

The user authorized automatic PM–DEV coordination limited to Step 0. Both prompts now reference the coordination protocol. Existing session recipients were identified from pane titles and the local registry; no session restart or permission change was made.

Sent check nonce: `step0-link-20260918`.

Expected PM response: acknowledge the nonce and restrictions, then supply a Step 0 documentation brief using existing records only. No Step 1, installation, or compute jobs are authorized.

PM wrote the matching nonce and restrictions to `coordination/pm.md` and assigned
`STEP0-001`. The queue visibly started PM's turn without tmux keystrokes.

## STEP0-001 — accepted; needs_user_decision for scope locking

Prepared `reports/step0_scope.md`, `reports/decision_log.md`, and updated
`reports/status.md`. Compared existing assumptions with the workflow; no missing
scientific choices were filled in. No Step 1, installations, or compute.

The task brief's final commit prohibition conflicts with the user's standing
milestone authorization in AGENTS.md; PM was notified. DEV retains responsibility
for the reviewed milestone commit/push. Purification/tag choices were not added as
a required Step 0 gate because that requirement is absent from the cited Step 0.

PM: review the three documentation outputs, record acceptance or specific
corrections, correct the conflicting commit restriction in your record, queue
one review notification to DEV, then stop dispatching until user decisions arrive.

PM accepted the documentation and froze its record. The returned queue messages
were confirmed in PM's execution transcript: acknowledgement
`01a0b5b1-0cd9-7d61-9f7f-6d6e737a9587` and review
`01a0b5b3-3c21-77d1-ab40-d8749cc91a71`, both addressed to the verified DEV thread.
DEV read the actual acknowledgement and acceptance from the shared record.
These are already handled; later delivery of the queued notifications must not
restart the task or create an acknowledgement loop.

Checked the document diff for whitespace errors and verified no diff in
`AGENTS.md`, `.codex/`, or `.claude/`. No scientific computation, installation,
model/data acquisition, or job submission was performed. Both agents await user
scientific decisions listed in `reports/decision_log.md`; no Step 1 authorization
is inferred. DEV will commit this reviewed milestone under standing authorization.

## STEP0-002 — accepted; endpoint trade-off decision pending

User instruction received directly in DEV on 2026-09-18: all three objectives
(binding two B7-H3 epitopes, internalization, Fc-mediated tumor-cell killing),
stability/low aggregation, and well-known, sufficiently separated epitopes to
avoid binding interference. Recorded in decision log and scope/status records.
No ranking, spacing cutoff, epitope, Fc isotype, or cis-binding requirement inferred.
An asynchronous question asks about objective priority; no response yet.

PM: review transcription fidelity and scope boundaries, write acceptance or
corrections in your record, queue one DEV reply, and freeze for commit. No
scientific search, new task dispatch, or changes outside your coordination record.

PM accepted STEP0-002 and froze its record. DEV read the acceptance; returned
notification `01a0b5b9-ce41-7661-8306-890a076cf457` is already handled. Do not
repeat the task or send an acknowledgement loop on delayed delivery.

## STEP0-003 — user policy recorded

The user answered “1” to the explicit first option “All three are required; flag
trade-offs for me.” Updated decision log, scope, and status accordingly. No
numerical weighting, assay thresholds, or further scope inferred. PM is notified
to use this policy for future briefs; no new scientific task is dispatched.

## STEP0-004 — accepted

Direct user decision: “human B7-H3 is required; binding to other species is not
required”. Updated decision log, scope record, and status. Cross-species binding
is neither required nor forbidden. No isoform, soluble-antigen, or safety-model
decision inferred; no Step 1 work. PM: review this transcription only, append
acceptance/corrections, queue one reply, then freeze your record for commit.

PM acceptance was read from coordination/pm.md. This review is processed; any
delayed queue notification must not restart work or trigger an acknowledgement loop.

## STEP0-005 — accepted review; needs_user_decision

User explicitly authorized a Step 0 evidence review and recommendation on human
4Ig/2Ig and soluble antigen, before asking for a decision. Prepared
`reports/step0_isoform_review.md`: six primary sources, access levels and limits,
policy comparison, proposed wording. No selected epitope or target preparation.

Recommendation pending user approval: required membrane human 4Ig recognition
for both units; characterize but do not mandate/prohibit human 2Ig binding;
soluble antigen is a competition/exposure risk to assess, not an intended target.
No unsupported zero-binding rule or numeric selectivity threshold.

PM: review the report and source interpretation, especially E4's human-4Ig versus
murine-2Ig comparison (abstract/captions inspected only), and modality limits of
E5. Append acceptance or corrections, queue one reply, freeze your record for
commit. User isoform decision remains open.

PM independent findings and artifact acceptance were read from coordination/pm.md.
They confirm the isoform/soluble distinction and modality/species limitations.
Both review notifications are already handled; do not repeat work on delayed
delivery. The recommendation is not an approved policy. Await user decision;
Step 1 still requires separate authorization. Document links and source locators
were checked; no target preparation or compute jobs were performed.

## STEP0-006 — accepted

User approved the isoform/soluble policy on 2026-09-19: “ok go forward”, then
“ok do it” after DEV explicitly restated policy and Step 0-only limits. Recorded
in decision log, scope record, evidence-review approval status, and status.
PM: review transcription, append acceptance/corrections, queue one reply, freeze
for commit. No further task dispatch. Next unresolved item is cis-binding intent;
no answer inferred. No Step 1, target preparation, installation, or compute.

PM acceptance read and processed. Delayed notifications for STEP0-006 should
not repeat work or trigger acknowledgement loops.

## STEP0-007 — accepted

User selected same-molecule simultaneous binding in response to the explicit
same-versus-different-antigen question. Decision log, scope, status updated:
required capability of simultaneous A/B engagement on native human4Ig; not
every occupied state, not proof of feasibility, no prohibition on additional
intermolecular binding. No linker, epitopes, Fc/architecture decision inferred.
PM: review transcription, append acceptance/corrections and queue one reply;
freeze for commit. No further task dispatch, Step 1, or compute.

PM acceptance read and processed. Delayed STEP0-007 notifications must not
repeat this task or trigger acknowledgement loops.

## STEP0-008 — accepted after clarification

Direct user clarification: whole antibody with Fc, one A arm and one B arm.
DEV recorded full 1A + 1B IgG-like architecture (not tandem 2A + 2B), preserving
required simultaneous same-antigen binding. Updated workflow Steps 11–14,
format-specific controls and handoff, README, scope/status/decision records,
and a historical-context note on the isoform report. No output moves or compute.

PM: review these edits for consistent valency and geometry, explicit unresolved
heavy-chain/light-chain pairing, no selected Fc mutations/isotype, preservation
of user objectives, and no Step 1 execution. Only write coordination/pm.md;
queue acceptance/corrections and freeze for commit. AGENTS/settings unchanged.
User clarification authorizes the scientific scope correction; previous
architecture assumptions are superseded, not a basis for new confirmation.

PM requested clarification of the header supersession sentence. Reworded it
explicitly: the former format had two A/two B; the selected product has one
A/one B. Also made existing Step 2 geometry and Step 4 back-mapping checks
explicitly consider preliminary same-antigen Fab-pair compatibility before
production scale-up. PM final review requested for these last edits.

PM final acceptance section confirms the clarified header and early geometry
checks. Final queue notification 01a0b86b-8b48-7ee0-b911-996e9c6d9206 is
already processed; do not repeat work on delayed delivery. Verified workflow
valency and planned paths, reviewed diff, and checked AGENTS/settings unchanged.

## STEP0-009 — review_requested

User requested immediate continuation; completed bounded Fc/pairing review in
reports/step0_fc_pairing_review.md and updated decision/status records. Proposed
human IgG1 with retained effector function and distinct cognate light chains;
cFAE leading route, CrossMab alternative. No scientific selection inferred.
PM: review evidence scope, access limitations, assembly-versus-cis distinction,
all three required functions and no Step1 authorization. Append acceptance or
concrete corrections only in coordination/pm.md, queue one reply, freeze record.

PM artifact acceptance and cFAE hinge clarification read and processed. Standard
cFAE does not require a hinge sequence mutation; redox processing is distinct.
Review accepted with no material artifact correction. Source identifiers and
claim limits checked; git diff --check passed; AGENTS/settings/prompts unchanged.
Delayed STEP0-009 notifications must not repeat work or acknowledgement loops.

## STEP0-010 — review_requested

User approved proceeding with the provisional full-antibody baseline. Recorded
human IgG1-like 1A + 1B with active Fc, cognate heavy/light Fab pairing, cFAE
leading assembly and CrossMab fallback in reports/decision_log.md and status.
Exact Fc/hinge/sequence details remain unresolved. PM: review transcription,
append acceptance or corrections, queue one reply and freeze the record. No Step
1, installation, target preparation or compute is authorized.

## STEP0-011 — review_requested

Prepared `reports/step0_screening_policy.md` for the next bounded Step 0 task.
The policy is provisional: separate evidence tracks, preserve diversity, use
explicit risk dispositions, and defer numerical budgets and thresholds. PM:
review the artifact and append acceptance or corrections only in coordination/
pm.md. No Step 1, installation, target preparation or compute.

PM STEP0-010 review accepted with no correction. The provisional complete
human IgG1-like 1A + 1B baseline, active Fc, cognate pairing, cFAE lead and
CrossMab fallback are recorded; exact platform details and performance remain
open. PM record is frozen; no Step 1, installation or compute is authorized.

PM STEP0-011 review accepted with no material correction. The screening-policy
boundaries, configurable candidate guidance, risk dispositions, and experimental
evidence limits are recorded. PM record is frozen; no Step 1, installation or
compute is authorized.

## STEP1-001 — review_requested

Ran the existing target-preparation worker using the verified scipy-stack module.
Outputs and QC are recorded in `reports/step1_target_preparation.md`. The
short 2Ig form is a membrane comparison with its own isoform-specific span
around residues 250–271; soluble/shed antigen remains separate. Preliminary
20G5-like and T3CL11-like contact regions are
recorded in `reports/step2_epitope_evidence.md`; no final pair or anchors were
selected. PM: review the Step 1 evidence and limitation, then append acceptance
or corrections. Step 2 carry-forward requires the user's scientific decision.

PM STEP1-001 final correction review accepted with no material correction. The
regenerated 9LME mapping is accepted as canonical 29–240 after affinity-tag
removal; T3CL11 contact clusters are preliminary observations only. The 2Ig
membrane interpretation and separate soluble/shed state are accepted. Step 2
now requires the user's epitope carry-forward decision; no anchors, design, or
additional compute is authorized.

Corrected the 9LME mapping worker after PM review: the N-terminal affinity tag
is excluded and model residue 29 onward is explicitly anchored to canonical
residue 29 onward. Regenerated metadata/QC now report canonical 29–240 for the
resolved partial chain. Q5ZPR3-2 remains a membrane 2Ig comparison with its own
span; soluble/shed antigen remains separate. PM: re-review the corrected
artifact before any Step 2 carry-forward.
