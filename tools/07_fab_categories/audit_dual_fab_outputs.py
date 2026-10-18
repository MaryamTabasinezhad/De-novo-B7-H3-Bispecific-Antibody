#!/usr/bin/env python3
"""Audit expected AF3 files, following analyze_af3_shortlist.py's layout.

Checks execution artifacts only; does not establish binding or geometry QC.
"""
import argparse
import csv
import json
from pathlib import Path

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--root', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()
rows = []
for index in range(1160):
    directory = args.root / f'index_{index}'
    ranks = list(directory.glob('*/*_ranking_scores.csv'))
    issues = []
    if len(ranks) != 1:
        status = 'absent' if not directory.exists() else 'incomplete'
        rows.append((index, status, 0, 'missing or ambiguous ranking file'))
        continue
    rank = ranks[0]
    name = rank.parent.name
    with rank.open() as handle:
        scores = list(csv.DictReader(handle))
    if len(scores) != 4:
        issues.append('ranking row count differs from four')
    count = 0
    for seed in (101, 202):
        for sample in (0, 1):
            prefix = rank.parent / f'seed-{seed}_sample-{sample}' / f'{name}_seed-{seed}_sample-{sample}'
            paths = [Path(str(prefix) + suffix) for suffix in
                     ('_model.cif', '_summary_confidences.json', '_confidences.json')]
            if not all(p.is_file() and p.stat().st_size for p in paths):
                issues.append(f'missing sample {seed}/{sample}')
                continue
            summary = json.loads(paths[1].read_text())
            if len(summary.get('chain_pair_iptm', [])) != 5:
                issues.append(f'confidence chain count {seed}/{sample}')
            count += 1
    for suffix in ('_model.cif', '_summary_confidences.json'):
        p = rank.parent / f'{name}{suffix}'
        if not p.is_file() or not p.stat().st_size:
            issues.append(f'missing top {suffix}')
    rows.append((index, 'complete' if not issues else 'incomplete', count, '; '.join(issues)))
args.out.parent.mkdir(parents=True, exist_ok=True)
with args.out.open('w') as handle:
    writer = csv.writer(handle, delimiter='\t')
    writer.writerow(('index', 'artifact_status', 'samples_present', 'issues'))
    writer.writerows(rows)
print(json.dumps({status: sum(r[1] == status for r in rows)
                  for status in ('complete', 'incomplete', 'absent')}))
