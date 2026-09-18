# Scientific decision log

Updated 2026-09-18. Source: `doc/project-1-computational-first-process.md`, Step 0 and related sections. Initial record: `STEP0-001`. User requirements recorded below in `STEP0-002`.

| ID | Decision required | Existing evidence | State / question for user |
|---|---|---|---|
| S0-01 | Biological endpoint priority | Workflow lists binding, internalization, tumor-cell removal, and Fc-mediated function | Partially resolved: user requires dual-epitope binding, internalization, and Fc-mediated tumor-cell killing; priority/trade-off policy remains unresolved |
| S0-02 | Isoform/species and soluble-antigen scope | Human CD276 is the target; Step 1 names 4Ig and 2Ig, with context-dependent 2Ig inclusion | Unresolved: required 4Ig/2Ig coverage, any additional species, and whether soluble antigen is an intended or excluded context |
| S0-03 | Exact architecture and Fc intent | Tandem-scFv-Fc dimer with 2A + 2B is the current assumption | Partially resolved: immune-effector recruitment is desired; architecture/valency confirmation, Fc species/isotype, hinge, exact effector mechanism, and FcRn intent remain unresolved |
| S0-04 | Cis binding | Step 0 explicitly asks whether binding both epitopes on one antigen is required | Unresolved: required, desirable, or irrelevant? |
| S0-05 | Candidate diversity and compute policy | Multiple diverse candidates required; funnel counts are explicitly provisional | Unresolved: minimum diversity, compute budget, promotion limits, and allowable initial scale |
| S0-06 | Developability priorities and disqualifying risks | Five risk classes and a retain/review/exclude record are specified; thresholds provisional | Partially resolved: stability and low aggregation explicitly required; quantitative criteria and other hard exclusions/review flags remain unresolved |
| S0-07 | Computational versus experimental decision criteria | Predictions are hypotheses; several properties explicitly require experimental follow-up | Unresolved: program-specific acceptance criteria and which purified-protein/cell measurements will establish them |

These questions prevent final scope locking and production-scale design. They do not prevent recording existing assumptions. No provisional answer is inferred from candidate rankings or workflow suggestions. Step 1 remains outside the present authorization even if a subset of these decisions is resolved.

Runtime dependency availability is a separate readiness limitation in `config/hpc/README.md`, not a scientific decision or evidence of an installed tool. Do not silently replace missing software or models.

User decisions should be appended with their date, source conversation or quoted instruction, rationale when supplied, and affected settings. Only the requirements explicitly recorded below are user-specified; remaining fields are unresolved.

## STEP0-002 — user requirements, 2026-09-18

Source: user message in the DEV conversation following the Step 0 endpoint question. The user requested all three listed objectives: binding two distinct B7-H3 epitopes, internalization into B7-H3-expressing cells, and Fc-mediated tumor-cell killing through immune-effector recruitment. The user also requested a stable, low-aggregation antibody and distinct epitopes that are well known for antibody development and sufficiently far apart to avoid binding interference.

Recorded requirements:

- Include all three biological objectives; do not silently drop one. Relative priority and trade-off handling have been asked but not yet answered.
- Stability and low aggregation are explicit developability requirements; assay conditions and acceptance thresholds have not been selected.
- Seek well-characterized antibody epitopes in later authorized epitope work. No particular antibody, epitope, residue range, or minimum evidence standard has been selected.
- Require a later assessment of whether epitope placement and construct geometry permit binding without interference. No distance cutoff is inferred, and separation is not treated as proof of simultaneous binding.
- Do not infer a requirement for cis binding on one antigen versus binding different antigen molecules from this statement alone.

Affected records: `reports/step0_scope.md`, `reports/status.md`, and PM coordination. These are design objectives, not evidence of achieved biological activity or developability. No Step 1 or epitope search is initiated by recording them.
