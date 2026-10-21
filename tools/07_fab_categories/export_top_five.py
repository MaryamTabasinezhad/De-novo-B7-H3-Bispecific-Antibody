#!/usr/bin/env python3
"""Export distinct category inputs by best AF3 ranking score, not binding QC.

Uses the ranking/sample layout in tools/06_af3_validation/analyze_af3_shortlist.py.
"""
import argparse
import csv
import json
import shutil
from pathlib import Path
import os

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--snapshot', default='20261018', help='Output snapshot YYYYMMDD; default preserves the original export location')
args = parser.parse_args()
if len(args.snapshot) != 8 or not args.snapshot.isdigit():
    parser.error('--snapshot must be YYYYMMDD')
snapshot_label = f'{args.snapshot[:4]}-{args.snapshot[4:6]}-{args.snapshot[6:]}'
root = Path(os.environ['MAB_SCRATCH_ROOT'])
project = Path(os.environ['MAB_PROJECT_ROOT'])
categories = [('fab_A_only', '07_01_fab_A_only'),
              ('fab_B_only', '07_02_fab_B_only'),
              ('fab_AB_pairs', '07_03_fab_AB_pairs')]
for category, destination in categories:
    candidates = []
    for ranking in (root / 'fab_category_outputs' / category).glob('index_*/*/*_ranking_scores.csv'):
        index = int(ranking.parent.parent.name.split('_')[1])
        with ranking.open() as handle:
            scores = list(csv.DictReader(handle))
        if len(scores) != 4:
            continue
        # Require all expected sample artifacts before including an input.
        name = ranking.parent.name
        if not all((ranking.parent / f'seed-{seed}_sample-{sample}' /
                    f'{name}_seed-{seed}_sample-{sample}_model.cif').is_file()
                   for seed in (101, 202) for sample in (0, 1)):
            continue
        best = max(scores, key=lambda r: float(r['ranking_score']))
        inp = root / 'fab_category_inputs' / category / f'index_{index}.json'
        data = json.loads(inp.read_text())
        sequences = tuple((s['protein']['id'], s['protein']['sequence'])
                          for s in data['sequences'] if s['protein']['id'] != 'T')
        candidates.append((float(best['ranking_score']), index, ranking, best, sequences, inp))
    candidates.sort(key=lambda r: (-r[0], r[1]))
    out = project / 'results' / destination / f'07_04_top_five_{args.snapshot}'
    out.mkdir(parents=True, exist_ok=True)
    seen = set()
    records = []
    for score, index, ranking, best, sequences, inp in candidates:
        if sequences in seen:
            continue
        seen.add(sequences)
        rank = len(records) + 1
        name = ranking.parent.name
        sample = f'seed-{best["seed"]}_sample-{best["sample"]}'
        prefix = f'{name}_{sample}'
        source = ranking.parent / sample / f'{prefix}_model.cif'
        summary = source.with_name(f'{prefix}_summary_confidences.json')
        confidence = json.loads(summary.read_text())
        # Inspect actual coordinate chain IDs, rather than confidence array labels.
        lines = source.read_text().splitlines()
        start = lines.index('_atom_site.group_PDB')
        headers = []
        while lines[start].startswith('_atom_site.'):
            headers.append(lines[start].split('.', 1)[1]); start += 1
        chain_column = headers.index('label_asym_id')
        chains = {line.split()[chain_column] for line in lines[start:]
                  if line.startswith(('ATOM ', 'HETATM '))}
        expected = {'HA', 'LA', 'HB', 'LB', 'T'} if category == 'fab_AB_pairs' else ({'HA', 'LA', 'T'} if category == 'fab_A_only' else {'HB', 'LB', 'T'})
        if chains != expected:
            raise SystemExit(f'Unexpected chains {chains} in {source}')
        base = f'07_04_rank{rank:02d}_index{index}_{name}'
        shutil.copy2(source, out / f'{base}_model.cif')
        shutil.copy2(summary, out / f'{base}_summary_confidences.json')
        shutil.copy2(inp.with_suffix('.lineage.json'), out / f'{base}_lineage.json')
        shutil.copy2(ranking, out / f'{base}_ranking_scores.csv')
        records.append(dict(rank=rank, index=index, name=name, seed=best['seed'],
                            sample=best['sample'], ranking_score=score,
                            iptm=confidence['iptm'], ptm=confidence['ptm'],
                            has_clash=confidence['has_clash'], chains=','.join(sorted(chains)),
                            source=str(source), model=f'{base}_model.cif'))
        if len(records) == 5:
            break
    if len(records) != 5:
        raise SystemExit(f'Only {len(records)} distinct inputs for {category}')
    with (out / '07_04_selection.tsv').open('w') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader(); writer.writerows(records)
    (out / 'README.md').write_text(
        f'# Top five {category} inputs by AF3 ranking score\n\n'
        f'{snapshot_label} snapshot: {len(candidates)} completed inputs considered.\n'
        'Inputs are ranked by their maximum native ranking_scores.csv score across\n'
        'seeds 101/202 and samples 0/1; ties use ascending input index. Antibody\n'
        'sequence tuples are deduplicated (AB identity is the ordered A/B pair).\n'
        'One winning sample CIF per distinct input is copied with native summary,\n'
        'all four ranking scores, and RF2 source lineage. Coordinates retain antigen T.\n'
        'Coordinate chain IDs were checked; copies were compared byte-for-byte.\n\n'
        'This is a confidence-ranked export, not interface/epitope acceptance,\n'
        'experimental binding validation, or a complete Fc-containing antibody.\n'
        'AB ranking is provisional while the remaining campaign is queued.\n'
        'See 07_04_selection.tsv for provenance and scores. Native JSON scores are\n'
        'rounded by AF3; ordering uses the more precise ranking CSV values.\n'
        'Next: interface, clash, and simultaneous-epitope geometry assessment.\n')
    for record in records:
        assert Path(record['source']).read_bytes() == (out / record['model']).read_bytes()
    print(category, 'considered', len(candidates), 'selected',
          [(r['index'], round(r['ranking_score'], 4)) for r in records])
