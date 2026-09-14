# Project permission setup

Installed 2026-09-14 at the user's explicit request, based on `/scratch/ghaedi/mohcc_rorqual/.claude/settings.json` and its local overrides. This was the only Claude settings project found under `/scratch/ghaedi`.

The project now lives directly in `mab/`; the former nested `De-novo-B7-H3-Bispecific-Antibody/` directory is absent. The current `.codex/config.toml` specifies `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`. These settings permit unsandboxed filesystem and network operations without routine approval prompts in future sessions. They do not change the already-running session or override administrator-enforced policy.

The adjacent `.codex/rules/claude-equivalent.rules` file adapts explicit Claude command blocks for administration, package/environment installation, and the listed root/home deletion commands. Prefix rules match command tokens, not arbitrary shell semantics; these rules are not a comprehensive security boundary. No broad allow rules or unrelated scratch-project paths were imported.

The original installation added trust entries for the workspace and former nested repository in `/home/ghaedi/.codex/config.toml`. Other projects' permission defaults were not changed. The prior user configuration is backed up as `/home/ghaedi/.codex/config.toml.before-mab-permissions`.

Validation: TOML parsed successfully; the Codex rule checker blocked representative restricted commands and left normal Git/Python commands unmatched. Codex Doctor loaded the workspace configuration and reported unrestricted filesystem, enabled network, and approval Never. Its provider-connectivity checks ran inside the old session's restricted network and did not establish future-session connectivity.

The installer now derives the project root from its own location and targets only that root; it does not recreate the former nested directory. It leaves existing user trust entries intact.

Restart Codex from `mab/` to load these settings. To revert project permissions, remove the two settings from the project config; remove the added rules if also reverting the imported command restrictions. The staged files and installer here provide the settings and installer for the current layout.

References: [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-basic), [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference), [command rules](https://learn.chatgpt.com/docs/agent-configuration/rules).
