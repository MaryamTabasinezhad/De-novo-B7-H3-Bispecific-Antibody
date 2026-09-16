# Using the Biomni skills on Rorqual

This is an analysis project. Follow `AGENTS.md`: simple scripts, scientific sanity
checks, concise notes, and no routine hashing, pytest, generalized adapters, or
mandatory wrapper-promotion process.

1. Select a method from [skills/INDEX.md](skills/INDEX.md). Read the active skill
   and the relevant preserved example before writing new code.
2. Consult [config/hpc/README.md](config/hpc/README.md), then source
   `config/hpc/rorqual.sh` in the shell or batch script performing the analysis.
3. Check only the required tool, data, and model locations. Reuse known findings.
   Scientific runtimes that remain unavailable are listed in the host notes.
4. Use a suitable example directly when its interface works locally, or adapt
   it into a simple project analysis script. Keep the preserved source unchanged.
5. Inspect scientifically consequential outputs; pilot expensive runs before
   scaling up. Record commands, versions, parameters, seeds when relevant, and
   output locations in concise notes. Stop only stages with unresolved methods
   or scientific decisions.
6. Commit and push completed milestones using the existing project practice.

## Discovery and maintenance

The 19 relative links in `.agents/skills/` expose the maintained `skills/`
folders to Codex in this repository. `allow_implicit_invocation: true` is retained
for every skill. The agent must also consult the index at task startup, even if a
client omits some skills from its displayed catalogue. Updates should appear on
subsequent turns; restart Codex if they do not.

This layout follows [official Codex skill discovery documentation](https://learn.chatgpt.com/docs/build-skills).
Do not install duplicate global copies or activate `third_party/biomni/original/`.

The archive in `dist/` is the historical 2026-09-14 portable snapshot and contains
older guidance. Use the current Git checkout here. The archive and upstream
source checksums are provenance records, not analysis hashing requirements.
The converter has been aligned with the current lightweight instructions; use
an isolated output directory if rebuilding, and review changes before replacing
maintained files. Rebuilding is not a prerequisite for scientific work.
