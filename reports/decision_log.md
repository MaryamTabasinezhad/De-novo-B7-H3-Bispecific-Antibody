# Scientific decision log

Updated 2026-09-18. Source: `doc/project-1-computational-first-process.md`, Step 0 and related sections. Recorded by DEV for `STEP0-001`; no new scientific choices have been made.

| ID | Decision required | Existing evidence | State / question for user |
|---|---|---|---|
| S0-01 | Biological endpoint priority | Workflow lists binding, internalization, tumor-cell removal, and Fc-mediated function | Unresolved: which endpoint has priority, and which are secondary? |
| S0-02 | Isoform/species and soluble-antigen scope | Human CD276 is the target; Step 1 names 4Ig and 2Ig, with context-dependent 2Ig inclusion | Unresolved: required 4Ig/2Ig coverage, any additional species, and whether soluble antigen is an intended or excluded context |
| S0-03 | Exact architecture and Fc intent | Tandem-scFv-Fc dimer with 2A + 2B is the current assumption | Unresolved: confirm architecture/valency and specify Fc species/isotype, hinge, effector function, and FcRn intent |
| S0-04 | Cis binding | Step 0 explicitly asks whether binding both epitopes on one antigen is required | Unresolved: required, desirable, or irrelevant? |
| S0-05 | Candidate diversity and compute policy | Multiple diverse candidates required; funnel counts are explicitly provisional | Unresolved: minimum diversity, compute budget, promotion limits, and allowable initial scale |
| S0-06 | Developability priorities and disqualifying risks | Five risk classes and a retain/review/exclude record are specified; thresholds provisional | Unresolved: program-specific priorities and hard exclusions versus review flags |
| S0-07 | Computational versus experimental decision criteria | Predictions are hypotheses; several properties explicitly require experimental follow-up | Unresolved: program-specific acceptance criteria and which purified-protein/cell measurements will establish them |

These questions prevent final scope locking and production-scale design. They do not prevent recording existing assumptions. No provisional answer is inferred from candidate rankings or workflow suggestions. Step 1 remains outside the present authorization even if a subset of these decisions is resolved.

Runtime dependency availability is a separate readiness limitation in `config/hpc/README.md`, not a scientific decision or evidence of an installed tool. Do not silently replace missing software or models.

User decisions should be appended with their date, source conversation or quoted instruction, rationale when supplied, and affected settings. No approval has been recorded for the unresolved choices above.
