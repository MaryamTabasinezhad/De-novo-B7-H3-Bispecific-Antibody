# Step 0 scope record

Initial record 2026-09-18; updated 2026-09-19 through `STEP0-007`.

**State: documentation prepared; scientific scope gate not satisfied.** This record does not authorize Step 1 or production computation.

## Existing objective and assumptions

| Item | Recorded scope | Status and source |
|---|---|---|
| Target and objective | Two independent antibodies against distinct human B7-H3/CD276 epitopes, combined as a biparatopic construct | Existing objective; workflow, Objective |
| Architecture | Tetravalent tandem-scFv-Fc dimer, two A and two B units | Current assumption, not a finalized product specification; workflow, Current Architecture Assumption |
| Order | Both A–linker–B and B–linker–A constructs are planned for later evaluation | No order selected; workflow, Step 11 |
| Coordinates | Canonical human CD276 numbering, with explicit chain/residue mapping | Existing reporting rule; workflow, Agent Execution Rules |
| Target context | Preserve isoform, glycan, membrane, provenance, and structure-quality assumptions | Existing requirements for later preparation; workflow, Step 1 |
| Prediction limits | Computational binding and in-silico optimization remain hypotheses pending measurement | Existing interpretation rule; workflow, Objective and Agent Execution Rules |
| Diversity | Preserve structurally and sequence-diverse candidates at every stage | Existing principle; numerical minimum remains unresolved; workflow, Agent Execution Rules and Step 0 |

Source: [scientific workflow](../doc/project-1-computational-first-process.md).

## User requirements recorded 2026-09-18

The user explicitly requests dual-epitope B7-H3 binding, internalization into B7-H3-expressing cells, and Fc-mediated tumor-cell killing through immune-effector recruitment. The user selected all three as required and asked that trade-offs be flagged for their decision; no objective may be silently deprioritized. Stability and low aggregation are explicit requirements, with acceptance thresholds and measurement conditions still to be defined.

The user wants distinct epitopes well characterized for antibody development and sufficiently separated to avoid binding interference. Later authorized work must evaluate the evidence for candidate epitopes and their binding compatibility in the intended construct. The user subsequently required simultaneous A/B engagement of two distinct epitopes on the same human 4Ig-B7-H3 molecule (`STEP0-007`). Feasibility is unverified; binding separate molecules alone does not satisfy this criterion. No epitope, reference antibody, residue range, or numerical spacing cutoff is selected here. This requirement does not authorize an epitope search or Step 1 work.

Source and interpretation boundaries: decision log, `STEP0-002`. These are requirements, not claims of demonstrated performance.

## Decisions still needed

The workflow's Step 0 requires an endpoint priority, isoform/species scope, exact architecture/Fc intent, cis-binding requirement, candidate-budget policy, and developability risk policy. Their unresolved parts are recorded in [decision_log.md](decision_log.md). No values have been invented or promoted from assumptions to final choices.

Human B7-H3 is the documented target. The user approved cell-surface human 4Ig recognition by both units, optional human 2Ig binding to characterize, and soluble-antigen interference assessment without an intended neutralization goal (`STEP0-006`). No zero-binding rule or numerical cutoff is imposed. The user confirmed that human B7-H3 binding is required and binding to other species is not required (`STEP0-004`). Lack of cross-species binding is not a rejection criterion; avoiding such binding is not a requirement either. This does not settle a later safety-testing strategy.

The provisional funnel gives suggested counts, including 100–500 pilot backbones per anchor/CDR configuration, approximately 10,000 production backbones per epitope, 5–20 sequences per retained backbone, and approximately 20–50 parents per epitope. These are workflow suggestions, **not an approved compute budget or production instruction**.

## Existing developability principles

The workflow identifies five risk classes: sequence/chemical liabilities, conformational stability, colloidal behavior, format/process risk, and immunogenicity/human-sequence context. Assess them separately from interface evidence; preserve predictor disagreements and avoid a falsely precise combined score. Cutoffs remain provisional until appropriately calibrated.

Expression yield, formulation aggregation, viscosity, polyspecificity, and immunogenicity cannot be established by computational triage alone. The workflow calls for experimental follow-up and a risk record containing method, result, interpretation, confidence, action, and rationale. Stability and low aggregation are now explicit user priorities; numerical criteria and hard exclusions remain unresolved.

Source: workflow, Cross-Cutting Developability Assessment. No new risk thresholds are set here.

## Readiness and authorization

The September 16 status and [HPC notes](../config/hpc/README.md) record setup completion but no scientific runs, and unverified predictor/model dependencies. The current workspace inspection found no `data/`, `metadata/`, `work/`, or `results/` directories. No runtime verification, data retrieval, analysis, installation, or compute submission was performed for this documentation task.

The current authorization covers Step 0 documentation and PM–DEV coordination only. `config/project.yaml` is not created as a finalized scientific configuration while required choices remain unresolved. After user decisions, DEV can record approved settings within authorized scope; Step 1 requires separate authorization.

## Validation

Compared this record with the workflow's Objective, Current Architecture Assumption, Step 0, Step 1, Cross-Cutting Developability Assessment, Step 11, and Provisional Computational Funnel, plus existing status and HPC notes. Documented assumptions are separated from unresolved choices. Documentation completion does not satisfy the Step 0 scientific scope gate.
