# DEV coordination record

Updated: 2026-09-18 UTC.

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
