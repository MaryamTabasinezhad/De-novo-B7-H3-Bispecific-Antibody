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

## STEP0-004 — PM review

Reviewed 2026-09-18 UTC:

- `coordination/dev.md`
- `reports/decision_log.md`
- `reports/step0_scope.md`
- `reports/status.md`

**Disposition: accepted.** The records faithfully transcribe that human B7-H3
binding is required and binding to other species is not required. They correctly
avoid converting that statement into a prohibition on cross-species binding.

No human isoform, soluble-antigen, safety-model, epitope, or Step 1 decision was
inferred. The Step 0 boundary remains intact. This PM record is frozen for the
DEV milestone commit. No further task is dispatched.

## STEP0-005 — independent evidence review (PM findings)

Reviewed 2026-09-18 UTC at the user's request, before any user decision. Sources
inspected:

- [Unraveling the dynamics of B7-H3-targeting therapeutic antibodies in cancer through PET imaging and antibody pharmacokinetics](https://pmc.ncbi.nlm.nih.gov/articles/PMC11830545/) (PMC11830545; publisher DOI 10.1016/j.jconrel.2025.01.030).
- [Anti-cancer immune priming with beta-radioligand therapy using a novel high affinity antibody selectively targeting the 4Ig-isoform of B7-H3](https://pmc.ncbi.nlm.nih.gov/articles/PMC13080693/) (PMC13080693).

### Findings and limitations

1. Keep three concepts separate: membrane-associated human molecular isoforms
(4Ig and 2Ig), a soluble or shed extracellular antigen, and the assay reagent
used to represent either one. A shorter 2Ig membrane isoform is not itself proof
that a soluble species is present, absent, or structurally identical. Soluble
material can arise through ectodomain shedding or alternative splicing, and the
species and processing state matter.

2. PMC11830545 reports Ab-1 binding both 4Ig and 2Ig and Ab-2 as 4Ig-selective
in the tested binding panel. Its in-vivo work is PET/biodistribution in mouse
xenografts; the authors explicitly note that their imaging study could not
distinguish 2Ig from 4Ig expression in tumors. The washout and internalization
observations therefore inform antibody pharmacokinetics and assay-context target
engagement, but do not establish soluble-antigen concentration, human isoform
distribution, or behavior of the proposed tandem-scFv-Fc.

3. PMC13080693 describes MIL33B as having high affinity for 4Ig and lower,
measurable binding to 2Ig, with an 8–18-fold selectivity range in the reported
assays. That is discrimination, not a no-binding guarantee. The paper itself
treats shed 2Ig ectodomain as a possible pharmacokinetic sink. “4Ig-selective”
must not be transcribed as “does not bind soluble B7-H3.”

4. Neither paper demonstrates that isoform coverage or selectivity yields human
clinical benefit. The RLT study's tumor killing is caused by radionuclide
deposition (with immune-priming observations), whereas this project requires
internalization and Fc-mediated tumor-cell killing by a tandem-scFv-Fc.
Radioligand uptake/retention is supporting evidence for target accessibility,
trafficking, and possible sink risks; it is not a surrogate for simultaneous
dual-epitope binding, construct geometry, Fc-receptor engagement, ADCC/ADCP, or
clinical efficacy.

5. The evidence supports making soluble-antigen policy and desired human isoform
coverage explicit user choices. A reasonable recommendation for the next scope
record is to evaluate 4Ig-only and 4Ig-plus-2Ig coverage as separate hypotheses,
and to state whether soluble/shed antigen should be excluded, tolerated, or
treated as a pharmacokinetic liability. This is a recommendation boundary only;
no option is selected here and no Step 1 work is authorized.

**Disposition:** findings recorded for DEV's STEP0-005 artifact preparation.
No scientific decision was made, no isoform or soluble-antigen policy was
selected, and no computation or Step 1 activity was performed. PM will wait for
DEV's `review_requested` notification before reviewing `reports/step0_isoform_review.md`.

## STEP0-005 — artifact review and disposition

Reviewed 2026-09-18 UTC after DEV's `review_requested` notification:

- `coordination/dev.md`
- `reports/step0_isoform_review.md`
- `reports/status.md`
- `reports/decision_log.md`

**Disposition: accepted with no material correction.** The report preserves the
required distinction between human 4Ig/2Ig membrane isoforms and soluble or shed
forms, and it does not convert 4Ig preference into a zero-soluble-binding claim.
It correctly records E4's access limitation and the human-4Ig versus murine-2Ig
confound, and it treats E5's approximately eightfold human preference as
measurable discrimination rather than absence of human 2Ig binding. The report
also correctly notes that naked-antibody activity in the described E5 model was
not significant and that radioligand efficacy cannot stand in for the requested
tandem-scFv-Fc internalization, Fc-mediated killing, or clinical benefit.

The proposed wording is appropriately conditional: require native cell-surface
human 4Ig recognition, characterize human 2Ig without mandating or prohibiting
it, and treat soluble antigen as a competition/exposure risk rather than an
intended target. It keeps all three user-required objectives active, does not
select epitopes or thresholds, and leaves the policy as a user decision. The
source table, modality limitations, uncertainty statements, and absence of Step
1 authorization are adequate for this milestone. No new scientific decision is
made by this review.

This PM record is frozen for DEV's milestone commit. No further task is
dispatched; Step 1 remains excluded pending the user's decision.

## STEP0-006 — PM transcription review

Reviewed 2026-09-19 UTC after DEV's `review_requested` notification:

- `coordination/dev.md`
- `reports/decision_log.md`
- `reports/step0_scope.md`
- `reports/step0_isoform_review.md`
- `reports/status.md`

**Disposition: accepted.** The records faithfully transcribe the user's two-step
approval (“ok go forward”, followed by “ok do it” after DEV restated the policy
and Step 0-only boundary). The approved policy is correctly limited to required
recognition of native cell-surface human 4Ig by both binding units; human 2Ig is
to be characterized but is neither required nor prohibited; soluble B7-H3 is an
interference/disposition risk to assess, without an intended neutralization goal,
zero-binding rule, or numerical cutoff.

The records correctly leave cis-binding intent as the next unresolved Step 0
choice and do not infer an epitope pair, architecture/Fc details, assay
thresholds, indication, target preparation, or Step 1 authorization. No material
transcription correction is required. This PM record is frozen for DEV's
milestone commit; no further task is dispatched.

## STEP0-008 — final PM acceptance after correction

Reviewed 2026-09-19 UTC after DEV's correction notification:

- Workflow architecture header and supersession wording.
- Step 2, Task 5: preliminary same-antigen Fab-pair compatibility and approach/
  reach considerations before production scale-up.
- Step 4, Task 9: preliminary A/B Fab-pair compatibility after full-target
  back-mapping before expensive scale-up, with later full-antibody validation.
- `coordination/dev.md` final clarification.

**Disposition: accepted.** The header now unambiguously states that the former
tandem format had two A and two B sites, while the selected product has one A
and one B site. Step 2 Task 5 and Step 4 Task 9 consistently require only
preliminary compatibility evidence before scale-up; they preserve full
same-antigen geometry validation as a later stage and do not present a pilot
check as proof of simultaneous binding.

The 1A + 1B valency, Fab/hinge geometry, and required cis capability are now
consistent across the reviewed workflow. No design, compute, epitope, linker,
Fc, pairing, or experimental decision was added. This PM record is frozen for
DEV's milestone commit; no further task is dispatched and Step 1 remains outside
the current authorization.

## STEP0-007 — PM transcription review

Reviewed 2026-09-19 UTC after DEV's `review_requested` notification:

- `coordination/dev.md`
- `reports/decision_log.md`
- `reports/step0_scope.md`
- `reports/status.md`

**Disposition: accepted.** The records faithfully transcribe the user's choice
that both antibody units must be capable of simultaneously engaging two distinct
epitopes on the same native human 4Ig-B7-H3 molecule. They correctly state that
binding separate antigen molecules alone is insufficient, while preserving the
important boundary that feasibility is unverified and that the requirement does
not mean every occupied construct state must be cis or prohibit additional
intermolecular binding.

No epitope pair, linker, Fc detail, final architecture, spacing cutoff, or other
scientific choice was inferred. The records retain the distinction between a
required capability and demonstrated performance, and they leave Step 1 and
compute outside authorization. This PM record is frozen for DEV's milestone
commit; no further task is dispatched.

## STEP0-008 — PM architecture transcription review

Reviewed 2026-09-19 UTC after DEV's `review_requested` notification:

- `doc/project-1-computational-first-process.md` (updated header, controls,
  handoff, and Steps 11–14)
- `README.md`
- `reports/decision_log.md`
- `reports/step0_scope.md`
- `reports/status.md`
- historical-format note in `reports/step0_isoform_review.md`
- `coordination/dev.md`

**Disposition: accepted with one concrete correction required before commit.**
The records consistently transcribe the user's clarification as a full IgG-like
1A + 1B antibody with Fc: one Fab A arm and one Fab B arm, replacing the former
tandem-scFv-Fc 2A + 2B assumption. Fab/hinge geometry appropriately replaces
tandem-linker geometry; simultaneous same-antigen binding is preserved; and
heavy-chain heterodimerization, light-chain pairing, hinge, Fc isotype/sequence,
and Fc mutations remain unresolved. No epitope, linker, Fc mutation, or new
architecture choice was inferred, and no Step 1 activity or run is authorized.

The updated workflow header still contains a valency contradiction at its
architecture supersession sentence: it says the new choice replaces the prior
format “with two A and two B sites.” That phrase must be corrected to state one A
and one B binding site (or equivalent 1A + 1B wording) before the milestone is
committed. This is a documentation correction only; the README, decision log,
scope record, status, and Steps 11–14 otherwise use the correct valency. The
historical tandem wording in the isoform review is explicitly labeled as such
and does not change the current architecture.

This PM record is frozen pending that concrete correction and DEV's milestone
commit. No further task is dispatched.

## STEP0-009 — independent Fc and chain-pairing evidence review

Reviewed 2026-09-19 UTC as a Step 0 literature-only task. No sequence, target
preparation, installation, computation, or design run was performed. Primary
records inspected:

- [Shields et al., 2001, human IgG1 Fc receptor mapping and Fc variants](https://pubmed.ncbi.nlm.nih.gov/11096108/), which mapped human FcγRI, FcγRIIA/IIB, FcγRIIIA and FcRn contacts and showed selected IgG1 variants increasing human-effector-cell ADCC.
- [Merchant et al., 1998, common-light-chain plus heavy-chain heterodimerization](https://pubmed.ncbi.nlm.nih.gov/9661204/), which reported approximately 95% heterodimerization, simultaneous HER3/cMpl binding, and retained ADCC in an anti-HER2 IgG1 context.
- [Labrijn et al., 2013, controlled Fab-arm exchange (cFAE)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3612680/), with [scale-up evidence](https://www.tandfonline.com/doi/abs/10.4161/mabs.26233), which reported stable bispecific IgG1, high exchange efficiency, normal IgG architecture, and retained Fc-mediated function.
- [Schaefer et al., 2011, CrossMab domain crossover](https://pubmed.ncbi.nlm.nih.gov/21690412/), which combined heavy-chain heterodimerization with Fab-domain crossover to prevent cognate light-chain mispairing while retaining dual binding and stability in Ang-2/VEGF-A examples.
- [Ridgway et al., 1996, original knobs-into-holes CH3 engineering](https://doi.org/10.1093/protein/9.7.617), the primary basis for engineered heavy-chain heterodimerization.

### Findings and trade-offs

1. A native human IgG1 Fc is a plausible effector-competent starting class for
   the required Fc-mediated tumor-cell killing. FcγR and C1q engagement, Fc
   glycosylation at N297, Fc sequence, antigen density, antibody orientation,
   and effector-cell context all affect ADCC, ADCP, and CDC. IgG1 class alone
   does not guarantee killing for a B7-H3 construct, and these studies do not
   establish activity on B7-H3-positive cells.

2. **Controlled Fab-arm exchange:** preserves a near-native full-IgG shape and
   each parental Fab's cognate H-L pair during exchange. It offers a direct route
   to one A arm plus one B arm with evidence for Fc function, stability, and high
   exchange efficiency. Costs include separately produced parental antibodies,
   engineered CH3/hinge exchange residues, controlled redox processing, and
   product/side-product characterization. Exchange efficiency does not establish
   same-antigen cis reachability or internalization.

3. **Knobs-into-holes plus common light chain:** strongly favors the desired
   heavy-chain heterodimer and removes most light-chain mispairing by using one
   light chain. Merchant et al. demonstrated high heterodimerization, dual
   binding, and retained ADCC. The common-light-chain requirement constrains
   discovery because both B7-H3 paratopes must work with the same VL, potentially
   excluding useful epitope solutions or affinity.

4. **CrossMab:** combines heavy-chain heterodimerization with a Fab-domain
   crossover so distinct cognate light chains can be retained without ordinary
   combinatorial H-L mispairing. Primary data support production, simultaneous
   binding, and stability. The crossover adds non-native domain topology and
   junction/interface liabilities that can affect Fab orientation, glycan or
   membrane clashes, and the reach needed for same-molecule B7-H3 cis binding.

5. No platform is intrinsically proven superior for simultaneous binding of two
   B7-H3 epitopes, internalization, or Fc killing. cFAE minimizes permanent
   format changes but adds an exchange step; KiH/common-LC simplifies pairing but
   narrows variable-domain search; CrossMab permits distinct light chains but
   adds crossover geometry and interface risk. Each must be judged on 1A + 1B
   valency, cognate H-L pairing, Fab accessibility, same-human-4Ig cis
   reachability, target-cell internalization, Fc-receptor engagement, and
   developability.

6. Correct chain assembly does not establish cis binding. A molecule can be
   correctly paired, bind both epitopes separately, and retain Fc activity while
   failing to engage both epitopes on one B7-H3 molecule. Preliminary Fab-pair
   checks can triage formats before scale-up; full-antibody and experimental
   validation remain necessary.

**Recommendation boundary:** retain human IgG1 as the effector-competent Fc
class under consideration, keep cFAE, KiH/common-LC, and CrossMab as explicit
alternatives, and compare them using the project's cis-binding, internalization,
Fc-killing, pairing, and developability criteria. Do not select an Fc sequence,
mutation set, pairing platform, common light chain, or architecture variant in
this review. DEV may prepare a Step 0 comparison artifact; PM will wait for
`review_requested` before reviewing it.

## STEP0-009 — artifact review and disposition

Reviewed 2026-09-19 UTC after DEV's `review_requested` notification:

- `reports/step0_fc_pairing_review.md`
- `reports/decision_log.md`
- `reports/status.md`
- `coordination/dev.md`

**Disposition: accepted with no material correction.** The artifact clearly
labels human IgG1 with retained effector competence, cognate Fab pairing, cFAE,
and CrossMab/KiH as recommendations rather than user-selected settings. It
keeps the common-light-chain option as a constrained alternative and does not
select an Fc sequence, allotype, hinge, glycoform, mutation set, FcRn policy, or
pairing platform.

The source-access limits are explicit and appropriate: Merchant is treated at
abstract level, cFAE and CrossMab direct PMC access encountered recaptcha, and
the report does not claim inaccessible details as verified. The direct B7-H3
DS-5573a evidence is correctly limited to target-specific Fc activity and does
not establish internalization, cis engagement, safety, or clinical benefit.

The artifact correctly separates assembly from biology: none of the three
pairing approaches establishes same-human-4Ig cis reachability, internalization,
or Fc-mediated killing in this construct. It preserves the preliminary geometry
gate before scale-up and later full validation, and it keeps all three required
objectives and developability risks visible. No selection, design, Step 1 work,
installation, or compute is inferred.

This PM record is frozen for DEV's milestone commit. No further task is
dispatched.

## STEP0-010 — PM transcription review

Reviewed 2026-09-21 UTC after DEV's `review_requested` notification:

- `reports/decision_log.md`
- `reports/status.md`
- `coordination/dev.md`

**Disposition: accepted.** The records faithfully transcribe the user's approval
to proceed with a provisional complete human IgG1-like 1A + 1B baseline: one
Fab-A arm, one Fab-B arm, retained active Fc, and each arm's cognate heavy/light
variable pairing. They correctly record cFAE as the leading assembly route and
CrossMab as the fallback comparison, without converting that baseline into a
final platform selection.

The remaining boundaries are correctly preserved: exact Fc sequence and
mutations, hinge sequence, allotype, glycoform, FcRn intent, construct-specific
geometry and performance remain unresolved. No common light chain is required by
the baseline. Same-antigen cis reachability, internalization, Fc-mediated
killing, stability, and low aggregation remain hypotheses requiring later
assessment. No Step 1, exact-sequence design, installation, or compute is
authorized or inferred.

This PM record is frozen for DEV's milestone commit. No further task is
dispatched.

## STEP0-009 — cFAE wording clarification

Clarification recorded 2026-09-19 after the independent findings were read:
standard IgG1 controlled Fab-arm exchange is driven by matched CH3 mutations
(the commonly used F405L/K409R pair) and controlled reducing/reoxidizing
conditions. The native IgG1 hinge sequence need not be mutated as a mandatory
part of cFAE. “Hinge” in this context refers to the inter-heavy-chain disulfide
and its redox susceptibility during processing; it is distinct from mandatory
hinge-sequence engineering. Alternative hinge engineering may be explored in a
separate construct-specific comparison, but none is selected here.

This corrects the earlier shorthand in the PM findings that grouped “CH3/hinge
exchange residues.” The STEP0-009 artifact's conditional recommendation and
unselected status are unchanged. No platform, sequence, Fc mutation, hinge
variant, Step 1 activity, or compute is authorized by this clarification.
