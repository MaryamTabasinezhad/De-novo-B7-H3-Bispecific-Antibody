# AGENTS.md — B7-H3 Antibody Project

Last checked: 2026-09-16.

## Maintainer and authority

**Project maintainer: Codex**, appointed by the user on 2026-09-14. Codex maintains the project layout, development contracts, implementation, configuration documentation, validation, and continuity notes. The user owns the project and retains final authority over scientific objectives and material changes to scope.

Carry authorized work through implementation and appropriate verification. Resolve routine engineering choices locally; ask the user only for missing decisions that affect scientific validity, scope, or actions outside existing authorization. The user has given standing authorization to commit and push completed project milestones. Other external communications, software installation, and unrelated project changes still require authorization covering that work.

This file is the local agent contract. Keep it current when the layout, responsibilities, or development conventions change. Explicit user instructions take precedence over these local conventions.

## Session startup

1. Read this file and inspect the current workspace and relevant settings.
2. Read the relevant sections of `doc/project-1-computational-first-process.md` before scientific implementation. Read `reports/decision_log.md` and `reports/status.md` if they exist.
3. Check existing outputs and recorded jobs before starting or resuming compute work. Do not duplicate an active or verified run.
4. Verify which directories and tools actually exist; the workflow includes planned infrastructure.
5. Before planning or writing analysis code, consult `skills/INDEX.md`. Use a matching imported skill and inspect its relevant examples before inventing a method. Read its `SKILL.md` and runtime note; if no skill fits, state the gap and proceed with a suitable direct analysis.
6. For analysis execution, consult `config/hpc/README.md` and source `config/hpc/rorqual.sh` in the same shell or SLURM script as the command. Reuse verified findings and check only task-specific gaps. Never assume environment exports persist across tool calls.

## Workspace and layout

- Project root is `mab/`, supplied as `/lustre09/project/6089454/ghaedi/mab` and resolved in this environment to `/project/def-ghaedi/ghaedi/mab`.
- Project files now live directly here. Do not assume a nested `De-novo-B7-H3-Bispecific-Antibody/` directory exists.
- `README.md`: project title and short description.
- `ADAPTATION.md`: procedure for binding the portable skills to this HPC environment.
- `CONTRIBUTING.md`: validation, change-control, and GitHub push instructions for the skill bundle.
- `skills/`: 19 Biomni-derived skills adapted to the analysis-first contract; `skills/INDEX.md` maps tasks and records scientific cautions.
- `.agents/skills/`: relative links for automatic project-local Codex discovery, with implicit invocation enabled.
- `config/hpc/`: sourceable Rorqual environment and verified capability notes. Scientific runtime paths remain unverified unless explicitly recorded.
- `third_party/biomni/`: preserved source archives, exact extractions, and provenance manifest. The source packages did not include a package-level license; keep the repository private until redistribution rights are confirmed.
- `tools/build_portable_biomni_skills.py`: reproducible, host-neutral converter that reads preserved archives and writes to an isolated output root.
- `dist/`: historical portable transfer archive from 2026-09-14. It predates the lightweight HPC adaptation; use the current Git checkout, not that archive, for active instructions.
- `doc/project-1-computational-first-process.md`: primary research workflow and its execution rules.
- `De-novo-B7-H3-review.md`: historical review of commit `9085bced77e6c1e289c5ab3570ede4cf87a538a0`; its Git/history observations describe that earlier checkout.
- Git tracking is restored at this root. The local `main` branch tracks `origin/main`; preserve the existing repository history.
- HPC configuration now exists in `config/hpc/`, and setup progress is recorded in `reports/status.md`. Scientific `data/`, `metadata/`, `work/`, and `results/` are created only as analyses need them. No antibody design or prediction runs have been completed.

## Settings locations

- `.claude/settings.json`: Claude permissions and presentation/effort settings.
- `.codex/config.toml`: project Codex configuration; currently `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`.
- `.codex/rules/claude-equivalent.rules`: explicit command restrictions adapted from Claude settings; inspect before relevant operations.
- `/home/ghaedi/.codex/config.toml`: user-level Codex configuration and project trust entries. It retains a historical trust entry for the former nested directory.
- `codex-permissions-setup/`: staged Codex config, rules, installer, and setup notes. The installer targets the project root relative to its location and also updates user-level trust configuration when run. Do not run it merely to inspect settings.
- References to `/scratch/ghaedi/mohcc_rorqual/` in setup comments document the original permission source, not this project's location.

## Research context

The specification concerns two binders to distinct B7-H3/CD276 epitopes, combined into a biparatopic construct. Its current architecture assumption is a tandem-scFv-Fc dimer with two A and two B binding units. Planned tools and outputs in the workflow are not evidence of installed dependencies or completed experiments. Consult the workflow's execution rules and completion gates before implementing scientific work.

## Analysis-first contract and standing memory

User clarification, 2026-09-14: this is a computational research and analysis project, not a software-development project. The deliverables are the analyses, structures, candidate designs, tables, figures, and reports specified in the README and workflow document.

- Prefer direct, readable analysis scripts, notebooks, and existing scientific tools. Use deterministic code where appropriate; record seeds and relevant settings for stochastic design or prediction tools without implying that all analyses are deterministic.
- Do not build software frameworks, generalized validation layers, pytest suites, CI systems, or packaging infrastructure by default. Add engineering only when it solves a concrete analysis need or the user requests it.
- Do not routinely hash every input/output or create elaborate provenance manifests. Record source/accession, version or retrieval date, tool/model version, commands, important parameters, and output locations at a useful level. Use a checksum only for a concrete integrity or identity question.
- Keep checks focused on scientific correctness: correct target/isoform, residue and chain mapping, plausible counts and units, interpretable structures, and whether the requested analysis finished successfully. Avoid repetitive input validation and tests that merely restate the script.
- Inspect representative results and use a small pilot before expensive runs when useful. Match verification effort to the scientific consequence and compute cost.
- This user clarification overrides blanket checksum, input/output validation, and software-engineering requirements elsewhere in project documents, including the historical review. Preserve the workflow's scientific decisions and completion criteria while implementing them proportionately.
- Skills should capture project-relevant methods, working examples, and scientific decision criteria. Do not import another project's contracts wholesale.

## Analysis execution contracts

### Script reuse and change control

- Before creating a script, search this project's existing code and applicable reference implementations. Reuse a suitable implementation and record its source and version.
- When porting a validated worker, initially limit changes to paths and environment bindings. Preserve scientific arguments, versions, output naming, and restart checks unless the current task requires a deliberate change.
- For a behavioral change, document the reason, affected inputs/outputs, and relevant validation. Do not silently substitute a tool, model checkpoint, reference, or scientific parameter.
- If no applicable reference exists, Codex may develop a project-specific implementation within the user's authorized task. Reuse working examples when useful and inspect representative results before scaling up. Missing scientific decisions remain subject to the workflow's gates.
- Use `#!/usr/bin/env bash` and `set -euo pipefail` for Bash workers. Keep paths and run parameters configurable; avoid embedding another project's paths.
- Keep edits focused, preserve user changes, and update usage documentation when behavior changes. Verify Git availability before attempting commits or branches.

### Software and configuration

- Inspect available modules, environments, containers, and project settings before choosing how to execute a tool.
- Follow the existing command restrictions. Do not install software or create environments without authorization that covers the operation; do not bypass a restricted command through an alternate executable.
- Record the software, model, and reference versions needed to interpret and repeat an analysis; reuse a known working environment when available.
- Place scientific settings in the workflow's planned `config/` files as they are implemented. Agent permission settings remain in `.codex/` and `.claude/`.
- Keep work scoped to this project. Changes to other projects require their own authorization.

### Validation and compute execution

- Use lightweight checks appropriate to the analysis or document change. Inspect scientific outputs rather than adding automated test infrastructure by default. Report what was actually checked.
- Before an expensive batch, run a small representative analysis and inspect its outputs when useful. For GPU work, verify GPU visibility inside the selected runtime within a suitable allocation.
- Use SLURM for substantial cluster compute. Use `--account=def-ghaedi_cpu` for CPU jobs and `--account=def-ghaedi_gpu` for GPU jobs on Rorqual (verified scheduler associations on 2026-09-16); inspect current partition and resource availability before submission.
- Size resources from the antibody workload and pilot measurements.
- Capture submission commands, job IDs, logs, exit status, and validation outcomes. Distinguish infrastructure failures from scientific filter rejections.
- Mark an analysis complete after confirming successful execution and inspecting the relevant scientific outputs. Reuse prior results when the inputs and method still match the current question.

### Run provenance and progress

- Keep concise analysis notes with sources, commands, important parameters, relevant seeds, tool/model versions, output locations, and candidate lineage where scientifically needed. A machine-readable run manifest is optional, not a prerequisite to analysis.
- Maintain `reports/status.md` once implementation or compute work begins: timestamp, current work, completed work, failures/blockers, active job IDs, and next steps. Report milestones and failures to the user in the current conversation.

### Data preservation

- Preserve raw inputs and their provenance. Write derived artifacts separately.
- Validate downstream outputs and any required archive or transfer before removing staged inputs. Verify the actual destination and transfer result; a filename or manifest entry alone is not proof of archival.
- Keep durable results, manifests, and decisions in project storage. Treat scratch as temporary storage and check current site retention rules when planning scratch use.
- Scope cleanup to known project-owned temporary paths. Do not alter unrelated directories.

### Scientific decisions

- Use human canonical CD276 numbering for reporting and preserve explicit residue mappings.
- Keep experimental contacts, region-defining residues, and computational design anchors separate.
- Keep numerical cutoffs configurable in `config/filters.yaml`; label provisional values and preserve rejection reasons and candidate diversity.
- Treat predicted binding and in-silico affinity optimization as computational hypotheses. Experimental affinity or biological activity requires measurement.
- Record unresolved scientific choices in `reports/decision_log.md` and stop only the work dependent on the relevant gate. Continue independent authorized work.

## Milestone commits and pushes

The user explicitly requested this standing practice on 2026-09-14: **commit and push after each completed milestone**, without asking for routine confirmation again.

- A milestone is a coherent, reviewable result: for example, a completed documentation update, a validated workflow stage, or a working fix. Avoid commits for every small edit and avoid accumulating unrelated milestones.
- Before committing, review the diff and run checks appropriate to the change. Stage only intended project files; preserve unrelated user edits. Keep credentials, caches, model weights, and large generated artifacts out of commits.
- Follow the repository's existing commit style when history is available. Otherwise use concise imperative subjects with a type and scope, such as `docs(agents): focus contracts on antibody workflow` or `feat(target): add target preparation validation`. Add a body when needed to explain scientific or behavioral changes and validation.
- Push the milestone commit to the verified project remote and appropriate tracked branch. Inspect upstream changes and integrate safely when necessary; do not force-push or rewrite shared history without explicit authorization.
- Verify the push result and report the commit hash, branch, and any failure. A local commit is not a completed push. If authentication, remote information, or branch policy blocks delivery, preserve the work and state the exact blocker.
- Keep the remote URL and branch information below current after verifying them. Never guess a remote from the project title or store credentials in this file.

### Git memory

- Working directory: `/lustre09/project/6089454/ghaedi/mab` (resolved path `/project/def-ghaedi/ghaedi/mab`).
- Remote `origin`: `https://github.com/MaryamTabasinezhad/De-novo-B7-H3-Bispecific-Antibody` (provided by the user and verified on 2026-09-14).
- Active branch: `main`; upstream: `origin/main`.
- Git tracking was restored after flattening the layout, preserving history through `9085bced77e6c1e289c5ab3570ede4cf87a538a0` and all local project files.
- Existing commit style: concise imperative subjects without mandatory type prefixes, for example `Refine RF2, RF3, and AlphaFold 3 validation roles`. Follow that style for milestones.
- Use Codex as the author for maintainer commits when no user-specified Git identity is configured; do not impersonate prior authors.

## Continuous GitHub synchronization

The user authorizes Codex to commit and push every project-file change without
asking for confirmation again. After every change, including small
documentation, configuration, script, report, or workflow edits:

1. Review the diff.
2. Commit the change to the tracked branch.
3. Push it to the verified GitHub remote.
4. Verify the push succeeded.
5. Report the commit hash, changed files, and push status.

Do not accumulate multiple unrelated changes before pushing. If a push fails,
report the exact failure immediately and preserve the local commit.

## Traceable workspace requirement

All project work must occur in a traceable project workspace or a documented,
version-controlled worktree. Do not keep durable project work only in an
untracked local directory, temporary session storage, or undocumented scratch
location.

Scratch space may be used only for temporary computation, downloaded software,
model weights, intermediate files, or Slurm outputs. For every scratch use:

- record the exact path;
- record the command, job ID, and relevant runtime details;
- copy required results or summaries into the tracked project workspace;
- commit and push the durable record immediately.

Before reporting work as complete, verify that the relevant code, reports,
decisions, metadata, and results are present in the tracked workspace and
available on GitHub.

A task is not considered complete until its durable artifacts and status record
have been committed, pushed, and verified on GitHub.

## Scope of these contracts

Deliver the artifacts specified by `README.md` and `doc/project-1-computational-first-process.md`, with the workflow's inputs, outputs, and completion gates guiding implementation. Keep contracts proportional to that work.

The scratch project's `CLAUDE.md` was consulted for general development practices. It is not an authority for this project. Adopt an external convention only when it serves a concrete requirement here; do not import another project's operational structure. These contracts are self-contained and require no scratch-project documents at session startup.
