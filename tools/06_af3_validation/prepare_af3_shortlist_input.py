#!/usr/bin/env python3
"""Create one AF3 JSON input from a tracked RF2 shortlist row."""
import argparse, csv, json
from pathlib import Path

AA = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E',
      'GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F',
      'PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}

def sequences(pdb):
    chains, seen = {}, set()
    for line in Path(pdb).read_text().splitlines():
        if not line.startswith(('ATOM  ', 'HETATM')) or len(line) < 27:
            continue
        if line[0:6].strip() == 'HETATM' and line[17:20].strip() != 'MSE':
            continue
        chain = line[21].strip(); residue = line[22:26].strip()
        aa = AA.get(line[17:20].strip())
        if chain and residue and aa and (chain, residue) not in seen:
            chains.setdefault(chain, []).append(aa); seen.add((chain, residue))
    return chains

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tsv', required=True)
    ap.add_argument('--row', type=int, required=True, help='zero-based data row')
    ap.add_argument('--out', required=True)
    ap.add_argument('--seeds', type=int, nargs='+', default=[101, 202])
    args = ap.parse_args()
    with Path(args.tsv).open(newline='') as handle:
        rows = list(csv.DictReader(handle, delimiter='\t'))
    if args.row < 0 or args.row >= len(rows):
        raise SystemExit(f'row {args.row} outside {len(rows)} rows in {args.tsv}')
    row = rows[args.row]; pdb = row['file']; chains = sequences(pdb)
    missing = [c for c in ('H', 'L', 'T') if c not in chains]
    if missing:
        raise SystemExit(f'missing chains {missing} in {pdb}')
    arm = row['arm']; task = row['rf2_task']
    name = f'arm{arm}_rf2_task{task}'
    obj = {
        'name': name,
        'sequences': [{'protein': {'id': c, 'sequence': ''.join(chains[c]),
                                   'description': f'RF2 shortlist chain {c}; arm {arm}; task {task}'}}
                      for c in ('H', 'L', 'T')],
        'modelSeeds': args.seeds,
        'dialect': 'alphafold3', 'version': 4,
    }
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, indent=2) + '\n')
    print(json.dumps({'arm': arm, 'rf2_task': task, 'pdb': pdb,
                      'input': str(out), 'chain_lengths': {c: len(chains[c]) for c in ('H','L','T')}}))

if __name__ == '__main__':
    main()
