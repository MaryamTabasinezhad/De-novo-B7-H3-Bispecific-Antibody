# De-novo-B7-H3-Bispecific-Antibody

De Novo Development of a B7-H3–Targeting Bispecific Antibody

## Portable Biomni-to-Codex Skills

This repository contains 19 selected Biomni Lab skills converted into portable,
Codex-valid instruction packages. It preserves the downloaded Biomni sources for
provenance while keeping platform-specific commands out of the active Codex
instructions.

The conversion covers stages 1–4: source preservation, provenance, Codex skill
structure, and portable instruction-layer adaptation. It does **not** claim that
cluster runtimes, scientific software, datasets, models, or scheduler adapters
are already operational on a new host. Those bindings must be discovered and
tested by the Codex agent on that host.

## Included skills

| Category | Skills |
|---|---|
| Drug Discovery | `knowledge-graph-target-reasoning`, `cell-surface-antigen-discovery`, `direction-of-effect-concordance`, `open-targets`, `target-tractability-druggability`, `tissue-expression-specificity` |
| General | `literature-review`, `literature-preclinical` |
| Literature | `clinicaltrials-landscape`, `literature-deep-review`, `methods-landscape-review` |
| Molecular Design | `binding-affinity-ml-model`, `generative-molecule-design`, `ligand-binding-mode-analysis`, `sgrna-design`, `targeted-degrader-design`, `antibody-developability-humanization`, `binder-antibody-design`, `protein-structure-prediction` |

## Repository layout

```text
skills/<skill-name>/
├── SKILL.md                         active Codex instructions
├── agents/openai.yaml               display and invocation metadata
└── references/
    ├── runtime-discovery.md         host-discovery and binding protocol
    └── upstream-biomni/             preserved Biomni implementation example
third_party/biomni/
├── archives/                        original downloaded ZIP files
├── original/                        exact extracted packages
└── manifest.json                    source IDs, hashes, dates, status
tools/build_portable_biomni_skills.py
dist/                                portable release archive and checksum
```

The upstream `SKILL.md` in each reference package is deliberately renamed to
`UPSTREAM_SKILL.md`. This prevents Codex from discovering the Biomni-specific
instructions as a second active skill.

## Deploy to a Codex host

1. Clone this repository on the target host.
2. Read [ADAPTATION.md](ADAPTATION.md) and complete its read-only host inventory.
3. Keep host configuration and early adapters outside
   `references/upstream-biomni/`; that directory is immutable provenance.
4. Validate a skill before installing it:

   ```bash
   python3 /path/to/skill-creator/scripts/quick_validate.py skills/open-targets
   ```

5. Copy or link only the validated named skill directories into the active Codex
   skill directory, normally `$CODEX_HOME/skills` when `CODEX_HOME` is configured,
   or the user-level Codex skills directory used by that installation.
6. Start a fresh Codex session and test both explicit invocation, such as
   `$open-targets`, and representative natural-language routing.

For systems that ingest uploaded skills, the official OpenAI Skills API accepts
a skill directory or a single ZIP file. See the
[Create Skill API reference](https://developers.openai.com/api/reference/python/resources/skills/methods/create).

## Rebuild the conversion

The builder uses the preserved repository archives and writes to a separate,
ignored `build/` directory by default:

```bash
python3 tools/build_portable_biomni_skills.py
```

Use explicit paths when rebuilding elsewhere:

```bash
python3 tools/build_portable_biomni_skills.py \
  --source-archives /path/to/biomni-archives \
  --output-root /path/to/new-build
```

The builder refuses to overwrite an existing `skills/` or `third_party/` beneath
the selected output root. Compare a fresh build with the reviewed repository
version before replacing anything.

## Release artifact

The current bundle is `dist/biomni-codex-portable-skills-2026-09-14.tar.gz`.
Verify it before transfer:

```bash
cd dist
shasum -a 256 -c SHA256SUMS
```

## Provenance and redistribution

Every adapted skill links to its Biomni profile skill ID and source checksum in
`skills/biomni-source-manifest.json`. The downloaded packages did not include a
package-level license file. Keep the GitHub repository private unless and until
the right to redistribute the upstream packages has been confirmed. Dataset,
model, API, publication, and scientific-tool licenses must also be checked by the
target-host agent before use.

## Contributing and pushing changes

Follow [CONTRIBUTING.md](CONTRIBUTING.md). In short: make host-neutral changes on
a `codex/<topic>` branch, leave upstream examples unchanged, validate the affected
skills, commit only intended files, push the branch, and open a pull request with
the adaptation checklist completed.
