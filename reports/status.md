# Project status

Updated 2026-09-16.

## Completed milestone

Reviewed the scope, workflow, and runtime guidance of all 19 imported skills.
Adapted active instructions and converter templates to the analysis-first
contract; preserved upstream sources. Linked skills for project-local discovery,
added the task index and Rorqual environment, and reconciled key project docs.

## Scientific execution status

No antibody analyses or compute jobs were run for this setup. Predictor/model
paths and dependency-heavy analysis environments remain unverified; see
`config/hpc/README.md`. No new packages or model downloads were installed.
No active project jobs or transfer tasks were created.

## Next analysis

Use `binder-antibody-design` and relevant literature/structure references to
prepare B7-H3 target inputs under Step 1 of the scientific workflow. Resolve the
specific scientific scope and dependencies needed for that task. Preserve glycan
and membrane context when considering the upstream target-cropping example.

## Setup checks

All 19 skills passed the existing skill-format checker. Codex app-server
`skills/list` with a forced reload returned all 19 project skills enabled. The
relative discovery links resolve; the environment file passed Bash syntax checking
and exported the intended project paths and CPU/GPU accounts. Converter templates
match the maintained skill instructions. Upstream source files are unchanged.
These checks establish instruction discovery and environment configuration, not
scientific execution readiness.
