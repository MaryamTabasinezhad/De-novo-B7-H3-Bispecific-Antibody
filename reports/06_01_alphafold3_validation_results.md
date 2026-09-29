# AlphaFold 3 validation results for the B7-H3 arm pilot

**Report purpose.** This report records exactly what was validated, how the AlphaFold 3 (AF3) models were generated, which quality criteria were examined, what the numerical results were, and what can and cannot be concluded. It is written so that the analysis can be reconstructed after the project context is no longer fresh.

## 1. Scientific question and scope

The project is designing a biparatopic human IgG-like antibody. Arm A is intended for the selected exposed IgV1 FG-loop neighborhood; Arm B is intended for the selected exposed IgC1 patch 2 region. Before assembling a complete 1A+1B Fc-containing antibody, the computational workflow asks whether each arm can form a plausible complex with its intended B7-H3 target region when predicted independently by a model that did not generate the original RFantibody/RF2 design.

This AF3 run was therefore an **independent arm-level structural validation pilot**. It tested:

1. whether the input antibody heavy/light chains produce a coherent folded Fv-like unit;
2. whether the H and L chains remain mutually compatible;
3. whether AF3 repeatedly places the arm confidently against the supplied B7-H3 chain; and
4. whether the result is stable across independent random seeds and diffusion samples.

### 1.1 What was selected before AF3 and why

Before AF3, the project had a larger RF2 control-gate-passing pool: 42 Arm A
models and 30 Arm B models. After task-level deduplication, the reviewable
shortlists contained 40 Arm A and 29 Arm B representatives. Those numbers are
the RF2 structural-QC population; they are **not** the number of AF3 inputs in
this pilot.

The AF3 pilot deliberately used one representative RF2 structure from each
arm—Arm A task 265 and Arm B task 131. This bounded design addressed an
infrastructure and model-consistency question before the more expensive option
of running AF3 across the entire shortlist: can AF3 rebuild the antibody arm,
preserve heavy/light pairing, and repeatedly recover a credible
antibody–B7-H3 interface from representative RF2-derived inputs? It was a
diagnostic validation pilot, not an exhaustive validation of all RF2 survivors
and not a final candidate-selection run.

It did **not** validate the final whole antibody, Fc-mediated killing, internalization, aggregation, affinity, specificity in cells, or simultaneous binding of Arms A and B to one native B7-H3 molecule. The AF3 inputs contained only chains H, L, and T from the RF2 arm-level complexes; they did not contain an Fc, a linker, the other arm, membrane topology, glycans, or a full-length IgG assembly.

The four predictions per arm were repeated observations of the same input
sequence and structure under two seeds and two diffusion samples. They were not
four newly designed antibody sequences per arm. The eight AF3 outputs are not
eight final antibody candidates.

## 2. What the eight AF3 models are

There were two representative RF2-filtered input candidates:

| AF3 input | Intended arm | RF2 source structure | Input chains | Chain lengths (H/L/T) | Slurm task |
|---|---|---|---|---|---|
| `armA_task265` | Arm A | `rfantibody_b7h3_rf2_20260926/A/task_265/ab_0_dldesign_1_best.pdb` | H, L, T | 114 / 105 / 84 aa | `21972327_0` |
| `armB_task131` | Arm B | `rfantibody_b7h3_rf2_20260926/B/task_131/ab_0_dldesign_1_best.pdb` | H, L, T | 118 / 105 / 94 aa | `21972327_1` |

For each input, AF3 was run with two random seeds (`101` and `202`) and two diffusion samples per seed (`sample-0` and `sample-1`). Thus:

- Arm A: 2 seeds × 2 samples = **4 predicted complexes**.
- Arm B: 2 seeds × 2 samples = **4 predicted complexes**.
- Total: **8 AF3 predicted complexes**.

The term “model” here means an AF3 predicted three-chain complex. It does not mean eight newly designed antibodies. The antibody sequences were inherited from the RF2 candidates; AF3 only repredicted their complex structure.

The target chain T is the cropped B7-H3 target fragment carried by the RF2 input. It is not a full-length membrane B7-H3 molecule. Therefore, this run tests local arm–target geometry and cannot establish accessibility on the intact cell surface.

## 3. How the inputs and predictions were generated

### 3.1 Input lineage

The two structures were selected from the documented RF2 control-gate shortlist. Their PDB files contained antibody heavy chain H, light chain L, and target chain T. The input preparation script extracted the standard amino-acid sequence from each chain and wrote AF3 JSON inputs using the AF3 dialect, version 4. The target chain and antibody chains were supplied as separate protein entities; no designed interface coordinates or RF2 structure template was supplied to AF3.

The durable input-generation code is `tools/06_af3_validation/prepare_af3_inputs.py`. The two JSON inputs were staged at:

- `/scratch/ghaedi/mab/af3_validation_inputs/armA_task265.json`
- `/scratch/ghaedi/mab/af3_validation_inputs/armB_task131.json`

### 3.2 AF3 runtime

- AF3 source commit: `a66cc5226d5fbcf7b08af4495af6fd7262178e38`
- AF3 package: `3.0.5.dev1+ga66cc5226`
- GPU: NVIDIA H100 80 GB
- HMMER: `hmmer-alphafold3/3.4`
- Model parameters: official `af3.bin`, staged outside Git in scratch
- Databases: official AF3 versioned databases, including PDB mmCIF, PDB seqres, UniRef90, UniProt, BFD, MGnify, RNAcentral, NT-RNA, and RFam
- AF3 options: 2 diffusion samples per input seed, 3 recycles, Triton flash attention
- MSA/template searches: enabled using the full staged databases
- Input chains: H, L, T
- Output location: `/scratch/ghaedi/mab/af3_validation_pilot/`

The AF3 pilot worker is `tools/06_af3_validation/alphafold3_validation_pilot_job.sh`. The Slurm array job was accepted as `21972327`; task 0 ran on `rg21704` for 36:49 and task 1 ran on `rg31701` for 1:01:22. Both exited `0:0`.

## 4. Validation criteria

The criteria were separated into runtime validity, structural sanity, antibody-pair behavior, and target-interface evidence. No numerical AF3 cutoff was invented after seeing these results.

### 4.1 Runtime and input validity

A task was considered technically valid if it completed with exit code `0`, generated all requested seed/sample outputs, and ran the full MSA and inference stages. Both tasks met this criterion. The logs show Jackhmmer, Hmmbuild, and Hmmsearch execution against the staged databases and H100 inference.

### 4.2 Structural sanity checks

The following AF3 outputs were inspected for every sample:

- `has_clash`: a predicted severe steric-clash indicator;
- `fraction_disordered`: fraction of residues predicted disordered;
- `ptm`: global predicted template-modeling score;
- presence of model mmCIF and confidence JSON files.

These checks ask whether the predicted object is structurally coherent. They do not establish binding.

### 4.3 Antibody internal consistency

The H–L chain-pair ipTM and H–L pairwise PAE were used to ask whether the antibody chains form a consistent Fv-like unit across seeds and samples. High H–L values support internal antibody geometry, but they do not prove antigen recognition.

### 4.4 Antibody–target interface evidence

The H–T and L–T chain-pair ipTM values and corresponding pairwise PAE values were used as the primary target-interface evidence. A convincing validation result would require repeated, coherent antibody–T placement across seeds/samples together with stronger interface confidence and low interface PAE. Because this was a pilot and not a calibrated benchmark, the values are reported descriptively rather than converted into a pass/fail threshold.

The AF3 ranking score, pTM, and ipTM were retained as model confidence summaries. They are computational scores, not Kd, affinity, internalization, cytotoxicity, or Fc-effector measurements.

## 5. Arm A numerical results

All four Arm A predictions completed without a clash flag and with zero predicted disorder fraction.

| Seed | Sample | Ranking score | pTM | ipTM | H–L ipTM | H–T ipTM | L–T ipTM | H–T/L–T minimum PAE (Å) | Clash |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 101 | 0 | 0.61 | 0.72 | 0.59 | 0.84 | 0.17 | 0.17 | 9.78 / 15.63 | 0 |
| 101 | 1 | 0.61 | 0.71 | 0.58 | 0.83 | 0.17 | 0.16 | 10.04 / 16.74 | 0 |
| 202 | 0 | 0.61 | 0.71 | 0.58 | 0.84 | 0.16 | 0.16 | 10.24 / 16.60 | 0 |
| 202 | 1 | 0.61 | 0.72 | 0.59 | 0.84 | 0.18 | 0.18 | 9.49 / 15.10 | 0 |

**Arm A interpretation.** AF3 consistently formed a plausible H–L antibody unit: H–L ipTM was approximately 0.83–0.84 in every sample, and the structures had no clash flag. However, the antibody-to-target values were much weaker: H–T and L–T ipTM were only 0.16–0.18, and target-interface PAE remained high. Across the four samples, the model therefore reproduced the antibody fold more confidently than the intended B7-H3 interface. Arm A is **not validated as a confident B7-H3-binding pose by this pilot**.

## 6. Arm B numerical results

All four Arm B predictions completed without a clash flag. Three samples had zero predicted disorder fraction; one had a small fraction of 0.01.

| Seed | Sample | Ranking score | pTM | ipTM | H–L ipTM | H–T ipTM | L–T ipTM | H–T/L–T minimum PAE (Å) | Clash | Disorder |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 101 | 0 | 0.60 | 0.69 | 0.57 | 0.86 | 0.13 | 0.12 | 11.83 / 18.94 | 0 | 0.01 |
| 101 | 1 | 0.60 | 0.70 | 0.58 | 0.86 | 0.15 | 0.14 | 11.63 / 17.01 | 0 | 0.00 |
| 202 | 0 | 0.58 | 0.69 | 0.56 | 0.87 | 0.11 | 0.10 | 13.94 / 19.63 | 0 | 0.00 |
| 202 | 1 | 0.60 | 0.70 | 0.58 | 0.87 | 0.15 | 0.13 | 11.16 / 17.68 | 0 | 0.00 |

**Arm B interpretation.** AF3 again produced a coherent antibody H–L unit: H–L ipTM was approximately 0.86–0.87. Structural sanity was acceptable, with no clashes and almost no predicted disorder. The antibody-to-target interface was weaker than the internal antibody pair: H–T ipTM was 0.11–0.15 and L–T ipTM was 0.10–0.14, with target-interface PAE approximately 11–20 Å. Arm B is therefore **not validated as a confident B7-H3-binding pose by this pilot**.

## 7. Combined conclusion

The AF3 installation, database configuration, MSA pipeline, GPU runtime, and inference path are operational. The eight predicted complexes are complete and reproducible at the pilot settings.

Scientifically, the result separates two questions that must not be conflated:

- **Antibody structural plausibility:** supported in this pilot. Both candidate arms repeatedly formed internally coherent H–L units with strong H–L chain-pair confidence and no predicted steric clashes.
- **Intended B7-H3 interface recovery:** not supported by this pilot. Both arms showed low H–T and L–T interface confidence and high antibody–T PAE across all tested seeds and samples.

The current evidence therefore does not justify promoting either arm as an AF3-confirmed B7-H3 binder. It also does not prove that either sequence cannot bind B7-H3 experimentally. Possible explanations include incorrect arm design, insufficient target context, the use of cropped target fragments, an interface incompatible with AF3's preferred pose, or inadequate sampling. These possibilities must be distinguished by further controlled computational analysis and ultimately by experiments.

Because both arms were evaluated separately, this run says nothing about whether a complete 1A+1B Fc-containing antibody can bind both epitopes on the same native human 4Ig B7-H3 molecule. Whole-antibody geometry, cis reachability, Fc behavior, internalization, aggregation, and cell killing remain untested.

## 8. Durable output locations

The complete Arm A and Arm B pilot outputs are preserved under:

- `results/06_01_af3_validation_pilot/armA_task265/`
- `results/06_01_af3_validation_pilot/armB_task131/`

Each directory contains the AF3 input-derived data JSON, aggregate confidence files, ranking-score CSV, terms-of-use file, and all four per-seed/per-sample model mmCIF and confidence files. The computational outputs are retained as provenance and are not presented as experimental evidence.

## 9. Recommended next decision

Do not silently promote these two candidates to final antibody assembly. The next scientific choice is whether to:

1. analyze the AF3 poses and contact recovery in detail and compare them with the RF2 intended anchors;
2. repeat AF3 on a broader, explicitly defined subset of the RF2 shortlist and/or alternative B7-H3 structural contexts; or
3. return to arm design and generate new candidates before whole-antibody assembly.

That decision should be recorded separately because the present AF3 pilot provides a clear diagnostic result but does not establish a therapeutically credible binder.
