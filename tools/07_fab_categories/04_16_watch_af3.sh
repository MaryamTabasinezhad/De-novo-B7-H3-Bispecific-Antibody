#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname -- "${BASH_SOURCE[0]}")/../.."
source config/hpc/rorqual.sh
work=work/04_16_watch_af3
report=results/04_16_loop_hypotheses/04_16_completion.md
mkdir -p "$work"
exec 9>"$work/lock"
flock -n 9
while true; do
    states=$(sacct -X -j 27674443,27674444 -n -P -o JobID,State,Elapsed,ExitCode) || states=
    count=$(printf '%s\n' "$states" | awk -F'|' '$2 ~ /^(COMPLETED|FAILED|CANCELLED|TIMEOUT|OUT_OF_MEMORY|NODE_FAIL|BOOT_FAIL|DEADLINE|PREEMPTED|REVOKED)/ {n++} END {print n+0}')
    (( count == 2 )) && break
    sleep 60
done
{
    printf '# 04_16 — AlphaFold 3 completion\n\nChecked %s.\n\n' "$(date -u)"
    printf '| Job | Slurm state | Elapsed | Exit code | Verified samples |\n|---|---|---|---|---|\n'
    while IFS='|' read -r job state elapsed status; do
        output="$MAB_SCRATCH_ROOT/04_16_loop_hypotheses/$job"
        count=0
        : > "$work/$job.models"
        if [[ -d "$output" ]]; then
            while IFS= read -r -d '' cif; do
                summary=${cif%_model.cif}_summary_confidences.json
                if [[ -s "$summary" ]] && rg -q '^ATOM ' "$cif" &&
                    python3 -c 'import json, sys; json.load(open(sys.argv[1]))' "$summary"; then
                    count=$((count + 1))
                    printf -- '- %s\n' "$cif" >> "$work/$job.models"
                fi
            done < <(find "$output" -type f -path '*/seed-*_sample-*/*_model.cif' -print0)
        fi
        printf '| %s | %s | %s | %s | %d/4 |\n' "$job" "$state" "$elapsed" "$status" "$count"
    done <<< "$states"
    for job in 27674443 27674444; do
        printf '\n## Job %s\n\n' "$job"
        printf 'Scheduler logs under %s/jobs/fab_category_%s_*.\n\n' "$MAB_SCRATCH_ROOT" "$job"
        cat "$work/$job.models"
    done
} > "$work/completion.md"
cp "$work/completion.md" "$report"
git add -- "$report"
git -c user.name=Codex -c user.email=codex@users.noreply.github.com commit --only -m 'Record matched AlphaFold 3 job completion' -- "$report"
for attempt in 1 2 3; do
    if git push origin main; then
        remote=$(git ls-remote origin refs/heads/main | cut -f1)
        [[ "$remote" == "$(git rev-parse main)" ]] && exit 0
    fi
    sleep 60
done
exit 1
