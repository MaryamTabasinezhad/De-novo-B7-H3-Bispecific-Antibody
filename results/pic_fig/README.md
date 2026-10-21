# Conceptual project figures

## 00_01 — B7-H3 biparatopic antibody mechanisms

Input: user-provided `bipara_lrg.jpg`, retrieved from GitHub commit `3dd8f2c` on 2026-10-20. The reference depicts HER2 biparatopic-antibody mechanisms. The original is preserved.

Output: `00_01_b7h3_biparatopic_mechanisms.png`, a reference-based redraw using the built-in image-generation tool. The generation prompt is recorded in `00_01_generation_prompt.txt`. Layout follows the reference's tumor overview and three-column, nine-panel mechanism grid; graphic styling and target labels are refreshed.

Scientific interpretation: this is a conceptual illustration, not a prediction result, a structural model, or experimental evidence for the project's antibodies. B7-H3 is not a HER2-family receptor tyrosine kinase. HER3/EGFR heterodimerization and HER2 homodimerization cannot simply be relabeled as established B7-H3 mechanisms. The corresponding center panels are therefore explicitly hypothetical. Clustering, internalization/degradation, signaling effects, ADCC, ADCP and CDC depend on construct, epitope, Fc, antigen density and biological context. Their inclusion does not demonstrate that the project construct produces these effects. Confirm membrane-protein and Fc interactions experimentally; generated molecular drawings are schematic rather than atomic representations.

Sources consulted for the scientific adaptation (2026-10-20):

- [Targeting site-specific N-glycosylated B7H3 induces potent antitumor immunity](https://www.nature.com/articles/s41467-025-58740-3): primary study supporting internalization/degradation for a particular glycosylation-specific antibody; not evidence for all B7-H3 antibodies or for the present construct.
- [Molecular Pathways: Targeting B7-H3 (CD276) for Human Cancer Immunotherapy](https://pmc.ncbi.nlm.nih.gov/articles/PMC4947428/): biological context, unresolved receptor biology and Fc-mediated therapeutic approaches.

Status and next stage: conceptual artwork only; not a scientific completion gate. Next, use for communication with the hypothesis labels retained, and validate any claimed mechanism independently of the illustration. No protein-design jobs or experiments are run for this figure.

Validation: inspected the generated image for the top overview and nine-panel ordering, B7-H3 wording and hypothetical mechanism labels; verified PNG decoding. The final file is copied from the tool output into this tracked directory. Built-in generation was used, not the CLI/API fallback. This artwork is not a scientifically validated molecular rendering.


## 00_02 — Consistent epitope-specific antibody arms

Output: `00_02_b7h3_biparatopic_consistent_arms.png`. This separately named
revision preserves `00_01_b7h3_biparatopic_mechanisms.png` and the reference JPG.
The user's correction is represented by purple antigen-binding arms for
epitope A and green antigen-binding arms for epitope B on every intact
biparatopic antibody, with gray Fc stems. A color key is provided above the
mechanism panels. Clustering is illustrated by two antibodies bridging
three neighboring B7-H3 molecules through differently colored contact patches.
Internalization maintains this dual-specificity convention. ADCC/ADCP show
Fc receptor engagement through Fc, and C1q engages Fc in the CDC panel.
Degraded lysosomal fragments are not intact antibody icons.

Generated using the built-in image-generation tool with iterative local
corrections; prompt history is in `00_02_generation_prompts.txt`. Earlier
intermediate generations were not selected because their Fab/Fc drawings or
epitope badges were inconsistent. The selected source is
`/home/ghaedi/.codex/generated_images/01a159bd-02ff-76f2-8575-8e6ea8b2ede6/exec-6eeb83a0-b7a0-49dc-a69c-3886712b3ff0.png`.

Validation: visually followed the two antigen-binding colors and gray Fc
branches across the overview and mechanism panels, checked crosslinking
and Fc receptor/C1q attachments, and verified PNG decoding. Shapes and contact
patches are schematic, not atomic structures, residue-mapped epitopes or a
validated demonstration of clustering geometry. All original hypothesis
qualifiers remain applicable. Next: use this revised illustration in place
of version 00_01 when communicating the intended dual-epitope concept.
