# 04_10 — Parallel readiness jobs

Submitted separately on Rorqual on 2026-11-25 UTC. Each job used the
[shared worker](../../tools/04_design_sequence/04_10_readiness_job.sh),
one CPU, 2 GiB, and a 15-minute limit. The exact submission loop was:

```bash
for job in references coverage pilot; do
  sbatch --parsable --job-name="mab-$job" \
    --output="$PWD/work/04_10_parallel_readiness/${job}_%j.out" \
    --error="$PWD/work/04_10_parallel_readiness/${job}_%j.err" \
    tools/04_design_sequence/04_10_readiness_job.sh "$job"
done
```

| Job ID | Work | Result |
|---|---|---|
| 27635091 | Retrieve ClinicalTrials.gov, Europe PMC, and Drugs@FDA search results | Slurm exit 0; all three requests failed (network unreachable or timeout). See the retrieval log and browser-checked references below. |
| 27635092 | Compare the 69 parents' AF3 input VH/VL with the coordinate-derived RF2 sequences | Completed, exit 0. All 138 chains matched exactly. |
| 27635093 | Verify prior RFantibody crop numbering and identify the baseline checkout | Completed, exit 0. Arm A residues 86–169 and Arm B residues 188–281 match the intact 4Ig reference sequence. |

The coverage result establishes that AF3 input sequences reproduce the RF2
parent coordinates. Both inputs were prepared as variable-domain chains.
Numbered framework/CDR completeness and any loss within individual AF3
sample models remain to be checked. The pilot output records the crop paths
and RFantibody checkout. The intact-4Ig comparison remains to be run.

## Starting antibody evidence

| Reference | Evidence and planned use |
|---|---|
| 8H9 variants and omburtamab | Experimental FG-loop dependence for Arm A. Track the experimental variants separately from the radiolabeled clinical product. [Experimental paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4705981/) · [Trial](https://clinicaltrials.gov/study/NCT03275402) |
| 20G5 and IBI334 | 20G5 has experimental IgC complexes. IBI334 is the related clinical construct. The local 9LY6 contact check found no direct overlap at 4.5 Å with the eight designated Arm B residues. Use as a neighboring IgC interface reference. [Study](https://doi.org/10.1038/s41467-026-69703-7) · [9LY6](https://www.rcsb.org/structure/9LY6) · [Trial](https://clinicaltrials.gov/study/NCT05774873) |
| T3CL11 | Published nanobody complex for comparison in the IgV region. Its exact overlap and relevance to the Fab format require review. [9LME](https://www.rcsb.org/structure/9LME) |
| Ifinatamab deruxtecan | Registered clinical ADC and a targeting benchmark. Exact contact overlap remains to be verified. [Phase 3 trial](https://clinicaltrials.gov/study/NCT06203210) |
| Enoblituzumab (MGA271) | Clinical antibody benchmark. Exact contact overlap remains to be verified. [Completed combination trial](https://clinicaltrials.gov/study/NCT02475213) |

For the local 20G5 calculation, used the raw 9LY6 PDB coordinate frame,
canonical mapping from `metadata/numbering_map.csv`, and minimum Euclidean
distance from each designated chain A residue's nonhydrogen ATOM coordinates
to any nonhydrogen ATOM coordinate in chains B–E. Q228 was closest at 5.169 Å.
The oriented project file transforms the antigen chain without transforming
the Fab chains, so it cannot be used directly for interchain distances.

Next, extend trial and regulatory coverage, resolve residue-level Arm B
reference evidence, verify numbered variable-domain completeness, and prepare
the matched baseline-versus-early-4Ig pilot. No redesign or generation was run.
