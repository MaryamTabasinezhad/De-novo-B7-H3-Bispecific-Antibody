# De-novo-B7-H3-Bispecific-Antibody

Computational design of two binders against distinct B7-H3/CD276 epitopes and
assembly into the biparatopic antibody construct described in the
[scientific workflow](doc/project-1-computational-first-process.md).

This is an analysis project. [AGENTS.md](AGENTS.md) defines the analysis-first
contract and milestone commit/push practice.

## Skills and HPC setup

Before an analysis, consult [skills/INDEX.md](skills/INDEX.md) and use the matching
skill and relevant examples. All 19 imported Biomni skills are linked under
`.agents/skills/` for automatic project-local Codex discovery; the maintained
instructions live in `skills/`. No global installation is needed.

```bash
source config/hpc/rorqual.sh
```

See [the Rorqual environment notes](config/hpc/README.md) for verified accounts,
paths, modules, and missing scientific dependencies. The environment file sets
project-scoped variables without installing tools or changing global shell state.
The skills supply methods; predictor software, model weights, and datasets are
not installed merely by enabling them.

Follow [ADAPTATION.md](ADAPTATION.md) for practical use and
[CONTRIBUTING.md](CONTRIBUTING.md) for changes. Use simple scripts, proportionate
scientific checks, and concise notes. Routine hashing, pytest, and generalized
adapter frameworks are not required.

## Included skills

| Category | Skills |
|---|---|
| Drug Discovery | `knowledge-graph-target-reasoning`, `cell-surface-antigen-discovery`, `direction-of-effect-concordance`, `open-targets`, `target-tractability-druggability`, `tissue-expression-specificity` |
| General | `literature-review`, `literature-preclinical` |
| Literature | `clinicaltrials-landscape`, `literature-deep-review`, `methods-landscape-review` |
| Molecular Design | `binding-affinity-ml-model`, `generative-molecule-design`, `ligand-binding-mode-analysis`, `sgrna-design`, `targeted-degrader-design`, `antibody-developability-humanization`, `binder-antibody-design`, `protein-structure-prediction` |

## Source material and historical bundle

`references/upstream-biomni/` inside each skill and `third_party/biomni/` preserve
the imported examples and archives. Read them selectively for methods; their
platform paths and operational contracts are not local instructions.

`tools/build_portable_biomni_skills.py` can rebuild into an isolated `build/`
directory when needed. It is not part of routine analysis. The archive in `dist/`
is the historical 2026-09-14 snapshot, not the current Rorqual-adapted skills.
Use this Git checkout for current instructions. Existing source/archive hashes
serve provenance only and do not require hashing scientific inputs/outputs.

The upstream packages contain no package-level license in the recorded imports;
retain their source notices and confirm redistribution rights before any new
public redistribution.
