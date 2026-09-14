# Adapting the Skills to a New HPC Environment

This guide is for the Codex agent that receives the repository on a workstation
or HPC system. The goal is to discover the host, bind only verified capabilities,
and leave a reproducible, reviewable implementation. Do not assume Slurm, GPUs,
containers, module names, storage mounts, databases, model weights, or internet
access from the examples in the Biomni source packages.

## 1. Read the instruction layer and relevant example

For each requested skill:

1. Read its `SKILL.md`.
2. Read `references/runtime-discovery.md` completely.
3. Read `references/upstream-biomni/UPSTREAM_SKILL.md` and only the supporting
   files relevant to the current scientific task.
4. Treat upstream paths, tool IDs, managed services, and commands as semantic
   examples. Never execute them until the local interface has independently been
   verified.

## 2. Produce a read-only host inventory

Record the following in a project-owned host profile, without changing the
system:

- scheduler and job commands, queues or partitions, limits, and accounting;
- module system, available environments, package managers, and versions;
- Apptainer, Singularity, Docker, Podman, or other supported containers;
- CPU architecture, GPU types and drivers, memory, quotas, and scratch policy;
- approved project, scratch, result, cache, database, and model locations;
- compute-node network rules and approved data-transfer mechanisms;
- available literature APIs, local datasets, database releases, and licenses;
- verified scientific executables, their help output, versions, and test data.

Prefer administrator documentation, project configuration, and narrow capability
checks. Do not crawl shared filesystems or install packages merely to complete the
inventory.

## 3. Define host bindings outside the upstream source

Create a project-local configuration layer that maps the skill's concepts to the
host. A useful binding normally records:

- explicit input, output, temporary, cache, data, and model paths;
- executable, module, environment, or immutable container reference;
- scheduler resource request and bounded timeout behavior;
- software, database, model, and schema versions;
- secrets supplied through the site's approved mechanism, never committed;
- licensing or access constraints and unavailable workflow stages.

Keep the first adapters in the consuming project. Do not edit
`references/upstream-biomni/`, and do not place an untested wrapper in an active
skill `scripts/` directory.

## 4. Implement one thin adapter at a time

Each wrapper should accept explicit paths and parameters, expose a dry-run or
command-preview mode, and record:

- the complete command or API request;
- scheduler job IDs and terminal state;
- versions, parameters, seeds, and container digest;
- input and output checksums;
- dataset/model releases and retrieval date;
- fallbacks, skipped stages, errors, cancellation, and timeout outcomes.

If a replacement method changes the scientific meaning, stop that stage and
report the missing capability. Offer an alternative explicitly; never substitute
it silently.

## 5. Test before promotion

Use the smallest meaningful fixture or smoke case first. Verify the observable
scientific and operational invariants, not just successful process exit:

- expected schema and identifiers;
- deterministic behavior where expected;
- required positive and negative controls;
- provenance completeness;
- bounded scheduler or API behavior;
- honest handling of missing data and unsupported stages;
- outputs located only in approved project paths.

After a wrapper passes target-host tests, move a reviewed, host-neutral form into
`skills/<name>/scripts/` only if it will be reused. Keep site-specific values in
external configuration. Document required arguments in the skill or a focused
reference and re-run skill validation.

## 6. Validate and activate

Locate the `quick_validate.py` shipped with the Codex `skill-creator` skill and
run it against every changed skill:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

Then install or link the validated skill folders into the active Codex skills
directory and start a new Codex session. Test:

1. explicit invocation with `$<skill-name>`;
2. an in-scope natural-language request;
3. a nearby out-of-scope request that should not route to the skill;
4. an unavailable-capability case that should stop or degrade honestly;
5. a minimal scientific smoke run when execution is authorized.

Update `runtime_binding` in the manifests only after the relevant runtime binding
and smoke tests are real. A valid `SKILL.md` alone does not make a scientific
workflow operational.

## Target-host completion record

For each activated skill, capture:

- host/profile identifier and review date;
- installed skill commit;
- validated runtime/container lock;
- dataset and model releases;
- adapter tests and expected results;
- remaining gaps and responsible owner;
- rollback or disable procedure.
