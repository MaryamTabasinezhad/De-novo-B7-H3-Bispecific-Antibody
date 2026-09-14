# Review of De-novo-B7-H3-Bispecific-Antibody

Reviewed 2026-09-14 at commit `9085bced77e6c1e289c5ab3570ede4cf87a538a0` on `main`.

The repository is a research specification for computational antibody discovery. It contains two tracked Markdown files: a two-line README and a detailed workflow document. There is no executable pipeline, configuration, input data, model output, candidate sequence, test suite, or experimental result in this checkout. The seven visible commits describe documentation development; the latest revisions clarify the roles of RF2, RF3, and AlphaFold 3. The clone has only one remote branch, `origin/main`.

This review covers every tracked file, the visible commit history, internal consistency of the workflow, and selected checks against primary software documentation and the cited RFantibody paper. It does not establish whether work exists outside this repository. No simulations or experiments were run. The repository was left unchanged; this review is stored beside it.

The principal source throughout is [the workflow](doc/project-1-computational-first-process.md). Line references below refer to the reviewed commit.

**What the project is trying to make**

The objective is to create two antibody binding units, A and B, recognizing distinct surface regions of human B7-H3/CD276, then combine them into a single molecular architecture. The intended biological questions involve cell-surface binding, internalization, and tumor-cell removal. These are objectives, with no demonstrated activity in the repository.

The precise term used by the workflow is *biparatopic*: two binding specificities directed at different epitopes on the same antigen. The repository title alone does not convey this distinction. The specified project does not introduce a second antigen-binding target.

Its proposed chain is `A-scFv–linker–B-scFv–hinge–Fc`, paired through an Fc dimer with another such chain. An scFv joins the heavy- and light-variable domains of an antibody into one polypeptide. The complete dimer therefore has four binding units: two A and two B. The workflow also explores reversing A and B. Exact sequences, framework choice, linkers, and Fc identity remain undecided.

“De novo” here applies primarily to designing the antibody binding loops and their poses on the target while retaining a selected human framework. It does not mean generating every part of the Fc-containing protein from scratch.

**How the proposed workflow fits together**

| Stages | Purpose | Intended output |
|---|---|---|
| 1–3 | Prepare target conformations, map residues, account for glycans and membrane access, select two epitopes and design anchors | Traceable target ensemble and epitope definitions |
| 4–5 | Generate binding-loop backbones with antibody-specific RFdiffusion and sequences with ProteinMPNN | Separate A and B candidate libraries |
| 6–8 | Repredict, filter, and preserve diverse parent families | Ranked parent antibodies with rejection history |
| 9–10 | Explore mutations and assess robustness across target states | Predicted optimized A and B variants |
| 11–15 | Combine domains, sample linkers, examine occupancy, add Fc dimer, assess full constructs | Geometrically plausible construct ensembles and risk records |
| 16–17 | Select candidates and controls and freeze provenance | Sequences, structures, scorecards, and experimental handoff |

RF2_ab provides the native RFantibody self-consistency check; AlphaFold 3 is the proposed primary additional structural filter; RF3 supplies supporting predictions and disagreement analysis. Rosetta and sequence analyses supply additional interface and developability features. These are planned integrations, not installed dependencies or existing wrappers.

**What is well considered**

The workflow separates computational optimization from experimentally measured affinity (line 7). It explicitly distinguishes measured contacts, epitope definitions, and predicted design anchors (lines 169–177). It recognizes that residue numbering, isoforms, glycans, and membrane orientation must be tracked before design (lines 79–119).

The selection scheme retains diverse sequences and poses instead of only a scalar-score winner. It includes mutation lineage, rejected candidates, independent prediction samples, and construct-level controls. Its distinction between simultaneous binding to one antigen molecule and binding to separate antigen molecules is useful (lines 517–548). Modeling the full Fc dimer is also necessary to assess whether favorable isolated-domain geometry survives assembly.

These are strengths of the proposed design. There are no artifacts showing that the gates have been satisfied.

**Prioritized findings**

1. **Execution blocker: the repository describes an entire system without implementing it.** The directory tree at lines 33–75 is aspirational. There are no schemas, commands, workflow runner, environment lockfiles, scheduler scripts, checkpoint records, or automated gate checks. A new operator cannot reproduce even Step 1 from the checkout alone. First implement a small path from frozen target input to validated metadata and a reproducible pilot report. Define unique identifiers and table relationships before generating large libraries.

2. **Scientific decision blocker: the biological endpoint is underspecified.** Line 127 groups binding, internalization, and tumor-cell removal; line 558 postpones locking Fc properties until Step 14. The plan does not specify which biological outcome takes priority, what experimental result would count as success, whether simultaneous occupancy of one antigen is necessary, or the intended isoform scope. These choices affect epitope selection and architecture early. Record them before committing to production design. This review identifies the decisions without choosing them on the project's behalf.

3. **High priority: computational scores have no local calibration dataset.** Lines 328–336 call for provisional RF2 thresholds and calibrated AF3 criteria, but no benchmark complexes, measured negatives, metric schemas, or acceptance policy exist. A positive structure is useful for testing coordinate and scoring code; it cannot establish a new-design success rate. Separate known measured nonbinders from synthetic decoys, which need not be true nonbinders. Select provisional filters explicitly, retain uncertainty, and reserve an experimental holdout for assessing their predictive value.

4. **High priority: prediction independence needs a precise definition.** Lines 279 and 305 prohibit reuse of the designed interface and describe predictions as independent. Specify allowed monomer templates, target conformational conditioning, MSA handling, model checkpoints, and any interface information supplied to each predictor. Running different models without the designed interface is a useful check but does not make their errors statistically independent. Also define how a target ensemble member is represented during reprediction: identical sequences alone do not request distinct fixed conformations.

5. **High priority: metric definitions and aggregation rules are incomplete.** “RMSD,” interface confidence, recovered contacts, and ensemble acceptance need atom selections, alignment rules, chain mappings, distance definitions, missing-data policies, and sample aggregation rules. For example, a global complex score can hide an incorrect antibody–antigen interface. AF3 reports interface-specific fields, but H/L/target and linked-scFv/target representations require deliberate interpretation. Freeze these definitions before examining candidate rankings. [AF3 output documentation](https://github.com/google-deepmind/alphafold3/blob/main/docs/output.md).

6. **High priority: full-target geometry should be an explicit early rejection check.** Step 4 uses cropped targets, while broad target-ensemble ranking appears at Step 10. Make back-mapping each promising dock to the full target, glycans, and membrane an explicit gate before expensive optimization. Cropping can remove steric obstacles. Step 2 already considers pair geometry, but coarse linker and Fc reachability should also inform parent selection so that assembly failures are found before the final stages.

7. **High priority: the computational search space needs a budget and stopping policy.** If all 10,000 backbones per epitope receive 5–20 sequences, the stated scale implies 100,000–400,000 sequence proposals across A and B before deduplication and filtering. This is arithmetic from the plan, not a runtime estimate. Pairing 20–50 parents on each side, with two orders and four linkers, would produce 3,200–20,000 combinations if enumerated exhaustively, before mutations, seeds, target states, or occupancy models. The plan does not require exhaustive pairing; it needs an explicit bounded pairing policy, measured pilot throughput, promotion caps, restart behavior, and storage estimates.

8. **Medium priority: lineage and deduplication requirements conflict unless modeled carefully.** Step 5 asks to deduplicate sequences while retaining backbone provenance, then requires each sequence to map to one backbone (lines 247–259). An identical sequence can originate from multiple designs. Store sequence identity separately from design-instance identity and preserve a many-to-many lineage relation. Otherwise deduplication can discard evidence or make the completion gate impossible to satisfy literally.

9. **Medium priority: late controls and unconstrained optimization increase interpretation risk.** Controls are mentioned in filtering but the final panel is specified at Step 16. Define the benchmark and control strategy before ranking so that the same processing rules apply throughout. Step 9 should also have explicit mutation-budget and stopping rules: repeated selection against prediction scores can improve scores without improving measured binding. The stated computational-first scope should be retained, while any later experimental feedback and recalibration are recorded as a separate stage.

10. **Medium priority: provenance is requested but its implementation is absent.** Add schemas for sequence identity, design instances, target states, predictions, rejection reasons, and construct lineage; pin dependency revisions and checkpoints; specify seeds and restart semantics. Infrastructure failures should remain distinguishable from scientific rejections. Selective smoke checks should verify numbering, fixed-framework preservation, chain identities, score parsing, and the two-A/two-B construct count. There is currently no testable implementation.

**Checks against the cited sources**

The RFantibody repository confirms the backbone-generation → ProteinMPNN → RF2 sequence of tools, the human framework example, and the provisional pAE/RMSD filtering guidance. It also explicitly describes filtering limitations and potentially large campaigns. Thus the project correctly identifies the upstream workflow, but upstream examples do not demonstrate performance on this target. [RFantibody documentation](https://github.com/RosettaCommons/RFantibody).

The cited Nature paper does support AF3-based enrichment of experimentally successful designs. Its VHH analysis is dominated by one target library, and its scFv analysis uses maximum ipTM over ten seeds with specific template/MSA inputs. Those conditions differ from an unspecified multi-seed consensus gate. This supports evaluating AF3 here, but does not establish a transferable B7-H3 cutoff or yield. [RFantibody paper](https://www.nature.com/articles/s41586-025-09721-5).

RF3 documentation confirms evolving input/confidence interfaces and multiple checkpoints, supporting the plan's insistence on pinning versions. An adapter must also distinguish early-stopped predictions from successful runs; upstream documentation describes early stopping that can produce metrics without a structure. [RF3 documentation](https://github.com/RosettaCommons/foundry/blob/production/models/rf3/README.md).

PDB 9LY5 is a real human B7-H3–20G5 Fab structure, reported at 2.98 Å resolution. Its associated publication concerns B7-H3/EGFR targeting. It is a relevant structural source, but that separate construct's results do not validate the proposed A+B architecture. The coordinate coverage and residue mapping still require inspection before using it as a target model. [RCSB 9LY5](https://www.rcsb.org/structure/9LY5).

AF3 code, model parameters, databases, and execution environment are separate setup requirements. The upstream project documents distinct CPU data preparation and GPU inference stages. No local readiness or throughput has been established in this review. [AF3 repository](https://github.com/google-deepmind/alphafold3).

**A practical first milestone**

Make the initial deliverable a reproducible target-preparation and pilot-readiness package. Record the biological objective, isoform scope, architecture constraints, and unresolved decisions; freeze input sequences and structures; establish canonical residue maps and target-state provenance; define machine-readable configurations and gate reports. Then verify a pinned upstream example and benchmark the smallest relevant pilot on the intended compute environment before selecting production counts.

Acceptance should mean that another operator can reproduce the target preparation, explain each model and residue mapping, run the environment smoke check, and see why a pilot is ready or blocked. Full candidate generation, affinity optimization, and experimental efficacy remain future milestones.
