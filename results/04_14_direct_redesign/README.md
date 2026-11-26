# 04_14 — Direct GPT-6.2 Sol redesign

Run ID `04_14_direct`. Two pilot requests launched concurrently from the
connected project shell on rorqual2 without Slurm. Scope is all 40 Arm A and
29 Arm B parents from the 04_09 lineage indexes. Prompts cite the 02_04
reference screen. The first parents are A265 and B131. Exact humanized
reference-chain matching and standardized internal CDR numbering remain open
and are labeled uncertainties in the proposal inputs.

```bash
source config/hpc/rorqual.sh
python3 tools/04_design_sequence/04_13_gpt6_redesign.py A --run-id 04_14_direct --limit 1
python3 tools/04_design_sequence/04_13_gpt6_redesign.py B --run-id 04_14_direct --limit 1
```

Working records are in `work/04_13_gpt6_redesign/{A,B}_04_14_direct/`.
Each record links the parent input, reference evidence, prompt, model and
Codex thread ID. A verified response here denotes a checked response
record. Structural validation and measured binding are separate milestones.
