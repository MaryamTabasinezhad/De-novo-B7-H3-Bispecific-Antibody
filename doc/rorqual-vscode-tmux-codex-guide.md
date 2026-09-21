# Reconnect to Rorqual, `mab`, tmux, and Codex

Last checked: 2026-09-21. This guide records the working arrangement we verified together: the existing `dev` and `pm` tmux sessions were found on **`rorqual2`**. A new VS Code connection landed on `rorqual1`, where `tmux ls` showed unrelated new sessions named `0` and `1`.

## Quick route back to `dev`

1. In VS Code, reconnect to your saved Rorqual SSH host and open **Terminal → New Terminal**.
2. At the first remote shell prompt, check the host:

   ```bash
   hostname -f
   ```

3. If it says `rorqual1.rorqual.calcul.quebec`, connect to the host that has your old sessions:

   ```bash
   ssh rorqual2
   ```

   **Wait** for a new prompt such as `[ghaedi@rorqual2 ~]$`. The long multifactor-authentication notice may appear during login; it is a banner, not a failure, if the `rorqual2` prompt appears. Do not paste `ssh rorqual2` and `tmux attach` as one block without waiting for the new prompt.

4. On `rorqual2`, confirm the host and sessions:

   ```bash
   hostname -f
   tmux ls
   ```

   Look for `dev` and `pm`. If you are **already** on `rorqual2`, skip the `ssh rorqual2` step.

5. Open the existing `dev` session:

   ```bash
   tmux attach -t dev
   ```

If Codex is already open in `dev`, continue in that screen. Do **not** start a second Codex process or resume the same conversation elsewhere.

## Project directory and Codex inside a tmux session

The antibody project directory is:

```text
/project/def-ghaedi/ghaedi/mab
```

Its equivalent physical path is `/lustre09/project/6089454/ghaedi/mab`. The project is directly in `mab`; do not add a nested `De-novo-B7-H3-Bispecific-Antibody` directory.

If `dev` opens to a **normal shell prompt**, run these commands **inside `dev`**, one line at a time:

```bash
cd /project/def-ghaedi/ghaedi/mab
pwd
git status
module load StdEnv/2023
module load nodejs/24.15.0
node --version
codex resume
```

`pwd` should show the `mab` project directory. `codex resume` lets you select the saved conversation. Use `codex resume --last` only when you are certain the most recent conversation is the one you want and it is not open in another app or terminal. If you want a **new, separate** Codex conversation, run `codex` instead of `codex resume`.

The module commands above are the ones you used previously; run them only when you are at a shell prompt and need to start Codex. An existing tmux session keeps its own shell environment: changing directory or loading modules **before** attaching does not change the shell already running inside `dev` or `pm`. If Codex is already on screen, there is no need to repeat these shell commands.

## Open `pm`

There are two convenient ways to use your other existing session.

### Switch from `dev` in the same terminal

While viewing `dev`, press **Ctrl+B**, release both keys, then press **s**. Select `pm` and press Enter. Use the same keys to switch back to `dev`.

### Use a second VS Code terminal

Open **Terminal → New Terminal**. From `rorqual1`, connect to `rorqual2` and wait for the new prompt:

```bash
ssh rorqual2
```

Then, on `rorqual2`, attach to `pm`:

```bash
tmux attach -t pm
```

If `pm` shows a shell prompt and you need the project and Codex there, use the same `cd`, module, and version-check commands listed above **inside `pm`**. Keep `dev` and `pm` on different Codex conversations; trying to open the same conversation in both can produce the “This conversation is open in another app” lock.

## Leave safely and reconnect later

- To **detach** from the current tmux session without stopping what is running: press **Ctrl+B**, release, then press **d**. You should return to the `rorqual2` shell. It is then safe to close the VS Code terminal or disconnect.
- From the `rorqual2` shell, type `exit` only if you want to return to the `rorqual1` shell. Do not type `exit` inside `dev` or `pm` when you mean to keep that shell running; detach instead.
- On your next visit, repeat the quick route above. Reattach with `tmux attach -t dev` or `tmux attach -t pm`; do not run `tmux new -s dev` or `tmux new -s pm`, because those commands create new sessions.
- `tmux2` was the **name of an older tmux session**, not a different version of tmux. It was not in the `rorqual2` listing when `dev` and `pm` were found.

## If something looks wrong

| What you see | What to do |
| --- | --- |
| `tmux ls` shows only `0` and `1` | Run `hostname -f`. That was the listing on `rorqual1`, not the older `dev`/`pm` listing on `rorqual2`. Connect with `ssh rorqual2`, wait for its prompt, and run `tmux ls` again. |
| `tmux attach -t dev` says it cannot find the session | Confirm `hostname -f` says `rorqual2.rorqual.calcul.quebec`, then run `tmux ls`. Session availability can change; do not create a replacement until you know where the original is. |
| SSH prints the multifactor-authentication notice | Wait for the shell prompt. The earlier `ssh rorqual2` command succeeded despite printing this notice. If no prompt appears or authentication actually fails, follow the login instructions shown by SSH. |
| Codex says “This conversation is open in another app” | The same conversation is active elsewhere. Check `dev`, `pm`, and the VS Code Codex sidebar. Continue in the already-open conversation, or close it there before pressing **r** at the lock screen. Do not delete files in `~/.codex` or kill an unidentified process. |
| The Codex screen will not scroll normally | Press **Ctrl+T** to open the Codex transcript. For tmux scrollback, press **Ctrl+B**, then **[**; use arrow or Page Up/Down keys, and press **q** to leave copy mode. |
| You are in a new tmux session on `rorqual1` and want to avoid nested tmux | Detach from it with **Ctrl+B**, then **d**, before running `ssh rorqual2` and attaching to `dev` or `pm`. Detaching does not destroy it. |

## Important distinction

VS Code is the window you use on your computer. `rorqual1` and `rorqual2` are different Rorqual login hosts. `mab` is your project directory on the shared project filesystem. `dev` and `pm` are tmux sessions on `rorqual2`. Codex is the assistant program running **inside** a terminal or in VS Code; a Codex conversation is not the same thing as a tmux session. Reconnecting to the correct host and reattaching tmux restores the live terminal; `codex resume` is only needed when Codex itself is no longer open in that terminal.

## References

- [Official OpenAI documentation: projects and chats](https://learn.chatgpt.com/docs/projects) — start Codex from the intended project directory and resume a saved chat.
- [Official OpenAI documentation: Codex CLI](https://learn.chatgpt.com/docs/codex/cli) — CLI workflow and resume command.
- [Rorqual user portal: login nodes](https://metrix.rorqual.calculquebec.ca/logins/) — current Rorqual login-node list.
