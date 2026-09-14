# Contributing and Publishing

Changes should preserve the separation between immutable Biomni provenance,
portable Codex instructions, and site-specific runtime bindings.

## Change workflow

1. Synchronize the default branch and create a focused branch:

   ```bash
   git switch main
   git pull --ff-only
   git switch -c codex/<short-topic>
   ```

2. Edit the active Codex layer under `skills/<name>/`. Do not modify
   `references/upstream-biomni/` or `third_party/biomni/original/` to make a local
   tool work. Put site configuration in the consuming project; add reusable,
   host-neutral adapters only after target-host testing.
3. If a Biomni source package changes, preserve the new ZIP, exact extraction,
   source ID, retrieval date, SHA-256 checksum, and license observation. Keep the
   old evidence available through Git history. Regenerate into an isolated output
   root and review the diff rather than overwriting the repository in place.
4. Validate every changed skill:

   ```bash
   python3 /path/to/skill-creator/scripts/quick_validate.py skills/<skill-name>
   ```

5. Run relevant adapter fixtures or scientific smoke tests on the target host.
   Do not mark `runtime_binding` operational without recorded evidence.
6. Inspect exactly what will be committed:

   ```bash
   git status --short
   git diff --check
   git diff --cached --stat
   ```

7. Stage only the intended files, commit, and push:

   ```bash
   git add skills/<skill-name> ADAPTATION.md
   git commit -m "Adapt <skill-name> for <capability>"
   git push -u origin codex/<short-topic>
   ```

8. Open a pull request. Include the source/provenance impact, host-neutrality
   review, exact validation commands, smoke-test evidence, scientific limitations,
   and any unresolved licensing or runtime gaps.

## First GitHub publication

This repository should initially be private because the preserved Biomni exports
did not include a package-level license. After creating an empty private GitHub
repository, connect and publish the local repository with:

```bash
git remote add origin git@github.com:<owner>/<repository>.git
git branch -M main
git push -u origin main
```

For HTTPS, use the repository's HTTPS remote instead. Authenticate with a GitHub
credential manager, SSH key, or approved organization method; do not embed tokens
in the remote URL or commit secrets.

## Review boundaries

- `SKILL.md` descriptions must remain specific enough for reliable routing.
- `agents/openai.yaml` must match the skill and preserve invocation policy.
- Runtime discovery must occur before choosing paths, commands, or resources.
- Platform-specific assumptions must not leak into active instructions.
- Predictions, source facts, and experimental results must remain distinguishable.
- Missing capabilities and partial workflows must be reported, not fabricated.
- Redistribution and dependency licenses must be resolved before public release.
