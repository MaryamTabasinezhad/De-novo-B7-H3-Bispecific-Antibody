# Step 1 — target-preparation result

Reviewed and regenerated 2026-09-21.

Date: 2026-09-21. The existing project worker was run with
`source config/hpc/rorqual.sh; module load scipy-stack/2023b`.

## Produced inputs and checks

The run used human UniProt Q5ZPR3 sequence/feature data, AlphaFold DB models
for Q5ZPR3 and Q5ZPR3-2, and RCSB structures 9LY5, 9LY6, and 9LME. It produced
`metadata/target_features.json`, `metadata/structure_manifest.csv`,
`metadata/numbering_map.csv`, mapped/oriented PDB files under
`data/processed/target_ensemble/`, and `work/01_target_preparation/ensemble_qc.csv`.

The canonical 4Ig record retains extracellular residues 29–466, the
transmembrane span 467–487, cytoplasmic residues 488–534, and six annotated
N-linked glycosylation sites (104, 189, 215, 322, 407, 433). Experimental
target chains were mapped to canonical numbering and placed into the common
AlphaFold-derived membrane frame. Resolved-glycan and unglycosylated controls
were emitted for the experimental structures.

## Required limitation

The short Q5ZPR3-2 sequence is a 2Ig comparison isoform with an isoform-specific
hydrophobic membrane span around residues 250–271; it must be mapped and
oriented using its own numbering rather than the canonical 4Ig 467–487
coordinates. Its generated file is therefore a membrane 2Ig comparison model,
not a soluble-antigen model. Soluble/shed B7-H3 remains a separate antigen
state. The 9LME affinity tag was also removed from canonical alignment: model
residue 29 onward is anchored to canonical residue 29 onward, yielding a
corrected target range of canonical 29–240 for the resolved partial chain. This
does not affect the required native cell-surface 4Ig baseline.

Representative modeled glycoforms, loop repair/relaxation, 4Ig oligomer
hypotheses, and a validated membrane-tilt ensemble were not fabricated. The
current 4Ig files are suitable for preliminary surface/epitope analysis, but
the full Step 1 gate remains conditional on those limitations being addressed
or explicitly accepted for the next analysis.

No antibody sequence design, installation, or compute job was performed.

## Public clinical and preclinical B7-H3 binders

This table is a bounded public-literature catalog, not an exhaustive inventory
of patent-only clones. Many named discovery binders have no publicly disclosed
residue-level epitope. Development status can change; the entries below record
the evidence and resolution available when reviewed on 2026-09-21.

| Binder or asset | Development context | Public epitope evidence and resolution |
|---|---|---|
| 8H9 / omburtamab | Clinical-stage radiolabeled antibody platform | IgV FG loop, approximately residues 126–129 (`IRDF`); in 4Ig, the homologous V1 and V2 regions. Residue-level mapping was experimentally supported. [Primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4705981/) |
| 376.96 | Preclinical antibody, radioimmunotherapy and CAR applications | Overlaps an IgV peptide region approximately 110–137, including the FG-loop neighborhood; exact conformational footprint unresolved. |
| G8 | Camelid nanobody used in CAR studies | Competes with 376.96 and recognizes overlapping IgV peptides around 110–137; exact conformational contacts unresolved. |
| C4 | Camelid nanobody/CAR binder | Distinct conformational epitope in an IgC domain; exact residues unresolved. |
| B12 | Camelid nanobody/CAR binder | Distinct conformational IgC-domain epitope from C4; exact residues unresolved. [Primary study](https://www.nature.com/articles/s41467-023-41631-w) |
| 20G5 | Structural and therapeutic-development antibody | IgC epitope involving approximately F177, Q179, D180, Q182, V184, P185 and R223 in IgC1, with the corresponding IgC2 site; Q179 is especially important. [Primary structural study](https://www.nature.com/articles/s41467-026-69703-7) |
| T3CL11 | Preclinical imaging nanobody | Membrane-distal IgV epitope. Corrected project mapping gives preliminary canonical clusters 64–89 and 123–130; these are not yet a final contact map. [PDB 9LME](https://www.rcsb.org/structure/9LME) |
| A6 | Synthetic nanobody/Fc preclinical binder | Overlaps a13 but does not compete with 8H9; exact residues unresolved. [Primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047927/) |
| a13 | Synthetic nanobody/Fc preclinical binder | Overlaps A6 and is distinct from 8H9 by competition; exact residues unresolved. |
| 7C4 | Preclinical B7-H3×CD3 bispecific component | Membrane-proximal IgC-region placement; exact contact residues require direct extraction of the mapping data. |
| 8H8, 11A7, 8D9 | Preclinical B7-H3×CD3 binders | Reported as membrane-distal relative to 7C4; exact residue maps are not clearly disclosed in the accessible primary text. [CC-3 primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC10124076/) |
| DS-5573a | Clinical-stage/developmental afucosylated anti-B7-H3 IgG1 | Binding and Fc-mediated activity are reported, but the primary development paper does not provide a residue-level epitope map. [Primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4970835/) |
| Enoblituzumab / MGA271 | Clinical Fc-enhanced anti-B7-H3 antibody | Exact epitope is not publicly resolved in the primary development report. [Primary report](https://aacrjournals.org/clincancerres/article/18/14/3834/77015/Development-of-an-Fc-Enhanced-Anti–B7-H3) |
| MGC018 | Clinical-stage B7-H3 antibody-drug conjugate | Public reports establish B7-H3 binding and ADC activity; residue-level epitope is not disclosed. [Primary report](https://aacrjournals.org/mct/article/19/11/2235/92689/Preclinical-Development-of-MGC018-a-Duocarmycin) |
| DS-7300a / ifinatamab deruxtecan | Clinical-stage B7-H3 ADC | Binds human and cynomolgus B7-H3 isoforms; the primary report does not define a residue-level epitope. [Primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC9377751/) |
| MGD009 | Clinical B7-H3×CD3 DART | Target and format are described, but the public epitope is not disclosed. |
| 36H7 | Preclinical diagnostic rabbit monoclonal antibody | Blocking places binding within ectodomain residues approximately 29–245; this is a broad interval, not a fine epitope. [Primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12876247/) |

For the planned biparatopic whole antibody, the best-supported pair of
distinct regions is currently a **20G5-like IgC epitope** plus an **IgV
epitope**. The 20G5 site has the strongest structural and mutational support;
8H9 has the clearest residue-level IgV reference, while T3CL11 remains a
useful domain-level and project-specific structural hypothesis pending further
validation.

## B7-H3 domain architecture and surface-design anchors

The common human 4Ig B7-H3 extracellular architecture is:

```text
outside of cell
  IgV1 — IgC1 — IgV2 — IgC2 — transmembrane helix — cytoplasm
  membrane-distal                                  membrane-proximal
```

IgV and IgC identify immunoglobulin-like domain types within B7-H3; they do
not refer to antibody variable and constant regions. The 2Ig isoform contains
one V–C repeat. Antibody design should focus on exposed extracellular loops,
while checking native membrane geometry, glycosylation, and simultaneous access
to both sites.

| Candidate epitope | Surface location | Better-supported residues | Confidence |
|---|---|---|---|
| 20G5-like site | Exposed IgC surface, mainly IgC1; a corresponding IgC2 site may also bind | Approximately **F177, Q179, D180, Q182, V184, P185 and R223**; broader project region approximately **177–188 and 214–230** | Strong structural and mutational evidence |
| 8H9-like site | Exposed FG loop of membrane-distal IgV | Approximately **126–129 (`IRDF`)**; the homologous region occurs in the second V domain of 4Ig | Strong biochemical epitope mapping |
| T3CL11-like site | Membrane-distal IgV surface, opposite two N-glycosylation sites | Preliminary project regions **64–89 and 123–130** | Good domain-level structure; residue-level map remains preliminary |

For the planned whole-antibody design, the strongest starting pair is a
**20G5-like IgC site** and an **8H9-like IgV FG-loop site**. T3CL11 remains an
alternative IgV hypothesis. The project records N-glycosylation sites at 104,
189, 215, 322, 407 and 433; nearby glycans may alter access and must be tested
on native, glycosylated, membrane-bound human 4Ig B7-H3.

These residues are design-analysis anchors rather than final validated antibody
contacts. Before sequence design, confirm that both surfaces are accessible on
the same B7-H3 molecule and that the selected IgG geometry permits simultaneous
binding.
