# PM coordination record

Updated: 2026-09-18 UTC.

## COORD-001 — acknowledged

Acknowledged nonce: `step0-link-20260918`.

The user-authorized coordination scope is limited to Step 0. PM may write this
coordination record and queue the assigned notification only. DEV may execute the
bounded Step 0 documentation task using existing records. Neither agent may make
new scientific decisions, begin Step 1, install software, acquire models or data,
submit or modify compute jobs, change `AGENTS.md`, alter permission settings, or
create replacement agents/models. No commit or push is requested from PM.

This record is an acknowledgement and task brief, not a scientific decision.

## STEP0-001 — document existing scope assumptions and unresolved choices

**State:** assigned for DEV review/execution under the 2026-09-18 Step 0
authorization. This is a documentation task only.

### Objective

Create a concise project scope record from the existing workflow and status
documents. Make documented assumptions and unresolved decisions visible without
choosing among them.

### Scope

Include only Step 0 documentation: existing architecture assumptions, biological
scope, developability criteria already present in the workflow, candidate-budget
questions, and runtime/readiness limitations. Explicitly exclude target retrieval,
structure preparation, residue mapping, epitope selection, design generation,
software installation, model/data acquisition, and compute submission.

### Existing assumptions to preserve

- The project is intended to design two independent binders against distinct
  human B7-H3/CD276 epitopes and combine them into a biparatopic construct.
- The current architecture assumption is a tetravalent tandem-scFv-Fc dimer:
  `(A-scFv–linker–B-scFv–hinge–Fc)₂`, with two A and two B binding units.
- Human canonical CD276 numbering is the reporting system.
- Target preparation must preserve isoform identity, glycan context, membrane
  orientation, and structure-quality assumptions.
- The workflow treats predicted binding and in-silico optimization as hypotheses,
  and includes staged developability risks rather than a single score.
- No antibody analysis, design run, or prediction job has been completed; required
  predictor runtimes and model weights remain unverified in the Rorqual notes.

### Unresolved choices to record, not answer

- Priority among binding, internalization, tumor-cell removal, and Fc-mediated
  function.
- Human B7-H3 isoforms and species scope, including treatment of soluble antigen.
- Exact Fc species/isotype, hinge, effector-function intent, and FcRn intent.
- Whether cis binding to two epitopes on one B7-H3 molecule is required,
  desirable, or unnecessary relative to intermolecular occupancy.
- Candidate-library scale, compute budget, promotion limits, and stopping rules.
- Which developability risks are hard exclusions versus review flags, and which
  properties are computational triage versus purified-protein or cell-based
  measurements.
- Required RFantibody, ProteinMPNN, RF2, RF3, AlphaFold 3, Rosetta, numbering,
  reference-data, and model-weight capabilities for later stages.

### Inputs

- `doc/project-1-computational-first-process.md`
- `README.md`
- `reports/status.md`
- `AGENTS.md`
- `skills/INDEX.md`
- `config/hpc/README.md`
- `config/hpc/rorqual.sh` (inspect only; do not run analyses or jobs)

### Method

Compare the existing documents, preserve their wording where possible, and label
each item as an existing assumption, unresolved choice, or runtime limitation.
Do not infer an endpoint, epitope, Fc format, threshold, budget, or dependency.
Do not execute scripts, source environments for analysis, or inspect external
services as part of this task.

### Outputs

- A Step 0 scope record at the project location chosen by DEV, following existing
  project conventions.
- `reports/decision_log.md` entries only for the unresolved choices actually
  documented; do not fill them with invented answers.
- An updated `reports/status.md` describing the documentation task and its limits,
  if DEV determines that a status update is needed under the existing contract.

### Validation and completion criteria

- Existing assumptions are traceable to the workflow or status documents.
- Unresolved choices remain explicitly unresolved and are not silently converted
  into configuration values.
- The record contains no Step 1 outputs, newly retrieved data, scientific runs,
  installations, or job IDs.
- The Step 0 scope gate remains open for user decisions; documentation completion
  must not be reported as scientific readiness.

### Dependencies and stop conditions

Stop and report if documents conflict materially, if a requested field requires a
new scientific decision, or if the task would require Step 1, installation, data
acquisition, or compute. Do not modify `AGENTS.md`, prompts, settings, skills, or
permission files.

### Report back

Report the files reviewed, documentation outputs, unresolved choices preserved,
validation findings, and any blocker. Include no job IDs unless an unrelated job
is observed; do not submit one. The standing `AGENTS.md` authorization to commit
and push completed milestones remains in force for DEV after review; this brief
does not revoke it.

## STEP0-001 — PM review

Reviewed 2026-09-18 UTC:

- `coordination/dev.md`
- `reports/step0_scope.md`
- `reports/decision_log.md`
- `reports/status.md`

**Disposition: accepted.** The documentation satisfies the brief. Existing
assumptions are traceable to the workflow, unresolved choices remain explicitly
unresolved, the provisional funnel is not promoted to an approved compute budget,
runtime limitations remain separate from scientific decisions, and the Step 0
scope gate remains open. No Step 1 work, installation, data/model acquisition,
scientific run, or job submission is evidenced in these records. Purification and
tag assumptions were correctly excluded from the required Step 0 gate.

The apparent commit restriction is corrected: DEV retains the standing
`AGENTS.md` authorization to commit and push a completed milestone after this
review. PM does not commit or push. This PM record is now frozen for DEV's
milestone commit review. No further task is dispatched pending the user's
scientific decisions.

## STEP0-002 — PM review

Reviewed 2026-09-18 UTC:

- `coordination/dev.md`
- `reports/decision_log.md`
- `reports/step0_scope.md`
- `reports/status.md`

**Disposition: accepted.** The user requirements are transcribed faithfully:
dual-epitope B7-H3 binding, internalization, Fc-mediated tumor-cell killing,
stability/low aggregation, and well-characterized epitopes with sufficient
separation to avoid binding interference. The records correctly distinguish these
objectives from demonstrated performance.

The remaining boundaries are correctly preserved: relative endpoint priority and
trade-offs, exact epitope identity, reference antibody, residue range, numerical
spacing criterion, cis-binding requirement, isoform/species scope, Fc details,
budget, and quantitative developability criteria remain unresolved. No epitope
was selected and no Step 1 work was initiated. Purification/tag assumptions were
not added as a Step 0 gate.

The standing `AGENTS.md` authorization for DEV to commit and push completed
milestones remains active. This PM record is frozen for the milestone commit and
review cycle. No new task is dispatched pending the user's scientific decisions.
