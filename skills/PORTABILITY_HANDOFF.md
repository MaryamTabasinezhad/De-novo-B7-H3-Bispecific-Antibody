# Portable Biomni-to-Codex Skill Bundle

This directory contains 19 Codex-valid instruction-layer skills adapted from the
selected Biomni Lab exports. The active skill instructions are portable and do
not assume a scheduler, cluster, filesystem layout, container runtime, GPU, model
cache, datalake, or network policy.

## Bundle layout

- Each named subdirectory is a discoverable Codex skill.
- `references/runtime-discovery.md` teaches the agent how to inspect a new host.
- `references/upstream-biomni/` contains the exact source package as an example;
  its `SKILL.md` is renamed `UPSTREAM_SKILL.md` to prevent nested discovery.
- `biomni-source-manifest.json` maps every adapted skill to its source ID, ZIP,
  checksum, and adaptation state.
- Exact archives and extracted originals also live under
  `../third_party/biomni/` when this bundle is kept inside the source repository.

## Completed here

1. Preserved the selected source archives and extracted originals.
2. Recorded source IDs, retrieval date, SHA-256 checksums, and adaptation state.
3. Created independent Codex-facing skills with clear names and supported
   frontmatter.
4. Replaced active source-platform assumptions with portable runtime discovery,
   capability mapping, fallback, and provenance instructions.

## Work intentionally left for the target HPC Codex agent

The target agent should continue only after inspecting the actual host:

1. Define locked runtime profiles or containers for the required skill groups.
2. Implement and test host-specific adapters for scheduler jobs, datasets,
   literature retrieval, report generation, and GPU tools.
3. Run unit, fixture, and scientific smoke tests, then promote tested wrappers
   from examples into each skill's active `scripts/` directory.
4. Install or link the validated skill directories into the target Codex skills
   location and test automatic routing with representative prompts.

Do not edit the upstream examples. Place all target-specific configuration in
the consuming project or a host-local configuration layer. Do not claim a skill
is operational merely because its `SKILL.md` validates.
