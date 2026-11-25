# 02_03 — Human B7-H3 antibody reference inventory for Paths A and B

Search snapshot, 2026-11-25 UTC. This inventory counts named antibody clones
or clinical assets and records aliases together. Clinical assets can share
a binder lineage with an experimental clone or another product. Keep those
relationships visible and confirm variable-domain identity before counting
them as independent redesign templates.

## Search coverage and eligibility

Searched public full-text scientific literature, PubMed, RCSB PDB,
ClinicalTrials.gov, regulator and sponsor records, and selected research
reagent catalogs. Searches combined B7-H3, B7H3 and CD276 with antibody,
nanobody, 4Ig, IgV, IgC1, FG loop, Q228–R241, epitope, mutagenesis,
competition, structural complex, clinical trial, and marketing approval.
Expanded by clone names and aliases from the primary papers and trial
records. Included positive binding assays against human B7-H3, structural
complexes, and named clinical assets with a documented B7-H3 binding
component. Included selected commercial controls with traceable identities.
There was no paginated registry export. The scope is publicly identifiable
binders found in this search. Unpublished sequences, uncharacterized clone
lists, and the full universe of catalogs and patent-only claims remain
outside the inventory.

## Arm A — IgV1 FG-loop evidence

| Antibody or clone | Evidence and limits | Primary source |
|---|---|---|
| **8H9 lineage** (murine, chimeric, humanized and 6m variants; omburtamab clinical lineage) | Mutant binding and modeling support FG-loop dependence. Keep variant and 2Ig/4Ig assay context separate. | [Experimental paper, epitope mapping](https://pmc.ncbi.nlm.nih.gov/articles/PMC4705981/) |
| **8H8** | Mutant ELISA implicates R127 in the intended patch. | [Zekri et al., Fig. 1D–E](https://doi.org/10.1016/j.ymthe.2023.02.010) |
| **376.96** | Peptide binding and competition with G8 support the IgV FG-loop region. | [Yang et al., Fig. 3A–B](https://doi.org/10.1038/s41467-023-41631-w) |
| **G8** | Nanobody. Competes with 376.96 and binds the same two FG-loop peptides. These assays support regional overlap. | [Yang et al., Fig. 3A–B](https://doi.org/10.1038/s41467-023-41631-w) |
| **B11** | Fully human scFv. Competes with 8H9 on 4Ig, supporting overlapping or sterically adjacent binding. | [B11 characterization and epitope mapping](https://pmc.ncbi.nlm.nih.gov/articles/PMC8493583/) |
| **8D9** | Mutant ELISA implicates G130, adjacent to the project patch. | [Zekri et al., Fig. 1D–E](https://doi.org/10.1016/j.ymthe.2023.02.010) |
| **11A7** | Mutant ELISA independently implicates G130. | [Zekri et al., Fig. 1D–E](https://doi.org/10.1016/j.ymthe.2023.02.010) |
| **T3CL11** | Nanobody co-crystal with one IgV–IgC module. Useful structural comparator. Verify canonical footprint overlap before applying residue-level guidance. | [Paper](https://pubmed.ncbi.nlm.nih.gov/42525538/) · [9LME](https://www.rcsb.org/structure/9LME) |

Use 8H9, 8H8 and 376.96 as the conventional-antibody evidence core.
Use B11 and G8 for regional corroboration, 8D9 and 11A7 for the adjacent
FG-loop edge, and T3CL11 for structural comparison after mapping. Mutant
sensitivity and competition assays constrain the region with different
precision from an experimental complex.

## Arm B — IgC1 patch around Q228–R241

| Antibody or clone | Evidence and limits | Primary source |
|---|---|---|
| **20G5** (related clinical format IBI334) | Partial direct match. Q228 is 3.001 Å from the Fab in 9LY5 and 5.169 Å in 9LY6. Five other resolved 9LY5 sites exceed 4.5 Å. Q240 and R241 are unresolved in 9LY5. The paper's functional mapping chiefly supports the neighboring Q179-centered footprint. | [Li et al., Fig. 3](https://doi.org/10.1038/s41467-026-69703-7) · [9LY5](https://www.rcsb.org/structure/9LY5) · [9LY6](https://www.rcsb.org/structure/9LY6) · [Local contact table](../results/04_12_design_inputs/04_12_9ly5_canonical_contacts.tsv) |
| **7C4** | Conventional IgC antibody. Mutant ELISA implicates Q179, providing a neighboring-site comparator. | [Zekri et al., Fig. 1D–E](https://doi.org/10.1016/j.ymthe.2023.02.010) |
| **24F lineage** (24F-Mu, 24F-Hu-WT and Fc variants) | IgC1/IgC2 binding by ELISA. Reported pose and individual contacts are docking hypotheses. | [24F study, Fig. 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC10732625/) |
| **C4** | Nanobody. 4Ig fragment binding implicates IgC context. Residue-level overlap unresolved. | [Yang et al., Fig. 3](https://doi.org/10.1038/s41467-023-41631-w) |
| **B12** | Distinct nanobody. 4Ig fragment binding implicates IgC context. Residue-level overlap unresolved. | [Yang et al., Fig. 3](https://doi.org/10.1038/s41467-023-41631-w) |
| **A6** | Human B7-H3-binding nanobody with a competition bin distinct from 8H9. Candidate comparator. The study discusses IgC possibilities without confirming the project patch. | [A6/a13 study, Fig. 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047927/) |
| **a13** | Distinct nanobody that shares the A6 competition bin. Exact site unresolved. | [A6/a13 study, Fig. 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047927/) |

Use 20G5 for the partial Q228 observation. Use 7C4, 24F, C4 and B12 to
compare IgC binding, and A6/a13 as an independent competition-bin pair.
No reviewed antibody establishes coverage of the full intended Arm B patch.
The eight project residues remain a design hypothesis with limited direct
experimental reference coverage.

## Other experimentally tested binders with unresolved arm assignment

| Named binders | Evidence | Primary source |
|---|---|---|
| **B2, H5** | Distinct nanobody clones with human 4Ig binding reported in Fig. 2. | [Yang et al.](https://doi.org/10.1038/s41467-023-41631-w) |
| **11G5, 12G5, A2H4** | Cell-surface human B7-H3 binding, with different relative signals. | [Glioblastoma preclinical study, Fig. 2B](https://jitc.bmj.com/content/13/1/e010083) |
| **MIL33B** | Preclinical binder selected for human 4Ig isoform specificity in the reported assays. | [MIL33B experimental study](https://thno.org/v16p5370.htm) |
| **CD276-3, CD276-8** | Experimentally distinct competition behavior. CD276-3 shared a bin with DS-7300, whereas CD276-8 differed. | [ADC study, Supplementary Fig. S2b](https://pmc.ncbi.nlm.nih.gov/articles/PMC13118972/) |
| **5C2, 38G9, 19A2, 6C2, 1C5, 20E4, 7B6** | Additional anti-B7-H3 clones in the experimental panel used to develop IBI334. Carry forward as panel leads pending clone-by-clone footprint review. | [Li et al., screening and Methods](https://doi.org/10.1038/s41467-026-69703-7) |
| **6A1** | Available research clone used as an experimental control in the 8H9 study. Weak wild-type 2Ig binding in the reported mutant comparison limits its value as a benchmark for that assay. | [8H9 experimental paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4705981/) · [Research product](https://www.abcam.co.jp/products/primary-antibodies/cd276-antibody-6a1-ab105922) |

## Clinical assets and market status

**Market search outcome.** No therapeutic marketing authorization was
confirmed in the sources reviewed. The U.S. application for ifinatamab
deruxtecan in previously treated ES-SCLC was voluntarily withdrawn on
September 25, 2026. Sponsor records show Chinese filing acceptance for
risvutatug rezetecan and tambotatug pelitecan. This is a bounded search
finding, with regulatory coverage outside the retrieved records unresolved.
Research reagents such as clone **7-517** and **FM276** are commercially
available controls. Their vendor records do not establish suitability as
epitope templates. [FDA oncology approvals](https://www.fda.gov/drugs/drug-approvals-and-databases/cancer-approvals) · [Ifinatamab sponsor update](https://daiichisankyo.us/press-releases/-/article/ifinatamab-deruxtecan-biologics-license-application-for-certain-patients-with-previously-treated-extensive-stage-small-cell-lung-cancer-voluntarily-withdrawn) · [Hansoh filing update](https://www.hspharm.com/news/news-detail-513502.htm) · [Roche filing update](https://www.roche.com/media/releases/med-cor-2026-09-13) · [7-517 catalog](https://www.bdbiosciences.com/en-us/products/reagents/flow-cytometry-reagents/research-reagents/single-color-antibodies-ruo/buv496-mouse-anti-human-cd276.749897) · [FM276 datasheet](https://static.miltenyibiotec.com/asset/150655405641/document_44tan7ihjl4urf26gc48vjdb0k?content-disposition=inline)

| Clinical antibody-containing asset | Evidence anchor | Path relevance |
|---|---|---|
| ¹³¹I-omburtamab | [NCT03275402](https://clinicaltrials.gov/study/NCT03275402) | 8H9 lineage, counted with Arm A reference. |
| IBI334 | [NCT05774873](https://clinicaltrials.gov/study/NCT05774873) · [Development paper](https://doi.org/10.1038/s41467-026-69703-7) | 20G5 lineage, counted with Arm B reference. |
| Enoblituzumab (MGA271) | [NCT02475213](https://clinicaltrials.gov/study/NCT02475213) | Binding benchmark. |
| Ifinatamab deruxtecan (I-DXd, DS-7300) | [NCT06203210](https://clinicaltrials.gov/study/NCT06203210) | Binding and competition benchmark. |
| Risvutatug rezetecan (HS-20093, GSK5764227) | [NCT07099898](https://clinicaltrials.gov/study/NCT07099898) | Binding benchmark. |
| Tambotatug pelitecan (YL201) | [NCT05434234](https://clinicaltrials.gov/study/NCT05434234) · [Primary clinical study](https://doi.org/10.1038/s41591-025-03600-2) | Binding benchmark. |
| Vobramitamab duocarmazine (MGC018) | [NCT05551117](https://clinicaltrials.gov/study/NCT05551117) | Binding benchmark. |
| MGC026 | [Sponsor clinical update filed with SEC](https://www.sec.gov/Archives/edgar/data/1125345/000112534526000066/a992mgc026clinicalupdate.htm) | Clinical asset. Verify binder identity and epitope before assigning a path. |
| BNT345 (DB-1311) | [NCT05914116](https://clinicaltrials.gov/study/NCT05914116) | Binding benchmark. |
| MHB088C | [NCT06951243](https://clinicaltrials.gov/study/NCT06951243) | Binding benchmark. |
| Mirzotamab clezutoclax (ABBV-155) | [NCT03595059](https://clinicaltrials.gov/study/NCT03595059) | Binding benchmark. |
| Obrindatamab (MGD009) | [NCT02628535](https://clinicaltrials.gov/study/NCT02628535) | Historical clinical B7-H3 × CD3 comparator. |
| IBI3001 | [NCT06349408](https://clinicaltrials.gov/study/NCT06349408) | Clinical B7-H3/EGFR asset. Verify the B7-H3 binding component before assigning a path. |

## Use in the four-path plan

Use the reference panel to guide the existing cohort-wide GPT-6 redesign
scope of 40 Arm A and 29 Arm B parents. Keep exact clone identity, antigen
isoform, residue mapping, experimental resolution and design rationale in
each redesign record. Use the documented measurements to support only the
contacts or epitope region they establish. Binding benchmarks can inform
assay comparisons while their exact footprints remain unresolved. No Slurm
jobs, sequence redesign or model generation were run for this review.
