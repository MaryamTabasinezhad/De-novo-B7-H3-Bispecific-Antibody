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


## 00_03 — Domain-specific Fab contacts (precise vector revision)

At the user's explicit authorization, the selected final version uses manual
SVG/vector geometry rather than an image-generated redraw. Its base image is
**00_01**, as requested; 00_02 and all original images are preserved.

- `00_03_b7h3_domain_specific_fab_binding.png`: new 2382 × 2642 PNG.
- `00_03_b7h3_domain_specific_fab_binding.svg`: original raster background plus editable vector overlays for the revised antibody-containing interiors, antibody overview and color key. It is a mixed raster/vector file, not an entirely vector recreation of the original illustration.
- `00_03_build_domain_specific_figure.py`: direct, reproducible builder.
- `00_03_fab_domain_geometry.json`: coordinates and domain-contact assignments used to check the requested drawing geometry; not a structure-derived epitope mapping.
- `00_03_generation_prompts.txt`: records the initial abandoned image-generation request and final vector method.

**Contact convention:** each redrawn B7-H3 ectodomain has four blue beads.
Counting from the extracellular outer tip toward the membrane, green Fab
contacts bead/domain 1 and purple Fab contacts bead/domain 3. Each intact
antibody is drawn with exactly one green Fab, one purple Fab and one gray Fc
stem. Clustering uses two antibodies bridging three neighboring antigens;
internalization shows a bridged complex in a membrane pit. Some panels show
cis binding to two domains of one antigen, while clustering illustrates trans
crosslinking. These are conceptual geometries, not demonstrated conformations.
In ADCC/ADCP, FcγR attaches at Fc; in CDC, C1q attaches at Fc.

Rebuild from the repository root:

```bash
python3 results/pic_fig/00_03_build_domain_specific_figure.py
```

Rendering uses existing `rsvg-convert` 2.56.1; Pillow is used to inspect the
source and verify PNG decoding. No software was installed. The source canvas
and preserved panel headings remain at their original resolution; only the
vector overlays acquire additional raster detail in the 2× export.

Validation: inspected the finished full figure; checked all 10 intact antibody
symbols and 13 redrawn four-domain antigens, verified every bound green endpoint
on domain 1 and every bound purple endpoint on domain 3, and verified PNG
dimensions/decoding. Original mechanism headings, nine-panel layout, tumor
overview, degradation/cell-cycle artwork and hypothesis/validation qualifiers
remain. Only the antibody-containing interiors and explanatory color key are
redrawn. The builder includes small coordinate checks to prevent the specific
Fab/domain errors encountered in generated drafts.

**Scientific boundary:** domain numbers here are the user's schematic drawing
instructions. This figure does not redefine the project's experimental or
computational residue mappings, select new epitopes, validate cis/trans reach,
or establish affinity, clustering, internalization or Fc effector activity.
Next: use this domain-consistent schematic for communication with the original
hypothesis caveats retained; validate actual contacts and mechanisms separately.


## 00_04 — Original visual artwork with corrected molecular foregrounds

`00_04_b7h3_original_style_corrected_binding.png` is the requested combination:
00_01 supplies the visual base and 00_03 supplies the green/domain-1 and
purple/domain-3 contact convention. No earlier image is overwritten.

The top overview, tumor illustrations, NK-cell/macrophage artwork, lipid
bilayer textures, C1q/MAC artwork, lysosome, cell-cycle diagram, panel borders,
labels and hypothesis caveats come from **00_01**. Edits are confined to
molecular foreground fields and their immediate background cleanup. Existing
FcγR/C1q attachment artwork is retained, with new gray Fc endpoints aligned to
it. Antibodies are redrawn using the original's paired-chain appearance,
gray constant domains, green/purple binding tips and shaded tubular material.
Blue ectodomain beads use matching shaded surfaces, with four explicit domains
where the generated source had inconsistent domain counts. This is a local
composite edit, not an AI regeneration or wholesale replacement of panel interiors.

**Scientific drawing rules retained from 00_03:** exactly one green Fab and one
purple Fab per antibody; green contacts domain 1 and purple contacts domain 3,
counting extracellular domains from the distal tip toward the membrane.
Clustering and endocytosis show intermolecular crosslinks; the blockade,
modulation and Fc-effector examples show schematic dual-domain engagement.
Gray Fc connects to FcγR or C1q. The original overview antibody is already
one-green/one-purple and is retained unchanged. These remain conceptual
positions, not experimentally established or residue-mapped epitopes.

Files:

- `00_04_b7h3_original_style_corrected_binding.png`: 2382 × 2642 PNG.
- `00_04_b7h3_original_style_corrected_binding.svg`: cleaned original raster base and editable shaded vector molecular overlays; a mixed raster/vector file.
- `00_04_build_style_preserved_figure.py`: direct builder using the existing Pillow 10.0.0 and rsvg-convert 2.56.1.
- `00_04_local_edit_geometry.json`: drawing coordinates, domain assignments and edit-scope check; not a structure-derived molecular model.

Reproduce: `python3 results/pic_fig/00_04_build_style_preserved_figure.py`.
No installations, AI generation, GPU inference or new scientific analyses
were required. The 2× raster export improves vector-edge sampling; it does
not increase the information content of the original raster cell artwork.

Validation: inspected the final composite, including domain contacts and Fc
attachments; checked 15 corrected mechanism-panel antibodies plus the retained
overview antibody, 18 four-domain antigen mappings, green/1 and purple/3
endpoint assignments, SVG XML and PNG dimensions/decoding. The builder also
confirms that every source-base pixel outside its local cleanup mask is
unchanged before overlays are added. Titles and mechanism qualifiers are
retained; this does not establish efficacy, binding geometry or mechanism.
Next: use this new original-style revision for the user's intended figure.

Temporary inspection crops were `/tmp/b7h3_00_04_cluster_reference.png`,
`/tmp/b7h3_00_04_internal_reference.png`, `/tmp/b7h3_00_04_effector_reference.png`
and `/tmp/b7h3_00_04_cdc_reference.png`. They were made with Pillow by cropping
00_01 at (15,405,384,615), (20,705,380,928), (812,425,1168,615), and
(815,1007,1168,1242), respectively, and enlarging 3× for visual inspection.
They are temporary previews, not durable project outputs; the final composite,
SVG, builder and coordinate record are preserved here.
