# Working on this analysis project

`AGENTS.md` defines the project contract. Prefer useful analyses, clear scripts,
scientific outputs, and concise notes over software infrastructure.

- Check `skills/INDEX.md` and reuse the relevant skill/examples before creating
  new analysis code. Maintain active instructions under `skills/`.
- Preserve `references/upstream-biomni/` and `third_party/biomni/` as source
  material. Put local analysis scripts and environment settings in the project.
- Review the actual change and perform proportionate checks. Skill frontmatter
  can be checked with the existing skill-creator `quick_validate.py`; scientific
  scripts need relevant output inspection, not mandatory pytest or adapter suites.
- Do not add routine hashes, formal manifests, or generic wrappers. Retain
  important scientific source/version information and method limitations.
- Commit coherent milestones with concise imperative subjects, then push to the
  tracked remote/branch as authorized. A branch or pull request is optional when
  useful or required by remote policy, not a mandatory workflow here.
- Keep secrets, caches, weights, and large analysis outputs out of Git.

The retained upstream exports have no package-level license recorded. Their
source notices remain applicable; this setup makes no new redistribution claim.
