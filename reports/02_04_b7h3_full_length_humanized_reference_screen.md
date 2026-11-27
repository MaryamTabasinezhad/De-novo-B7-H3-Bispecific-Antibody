# 02_04 — Full-length humanized B7-H3 antibody reference screen

Screened the 15 entries in the [reference inventory](02_03_b7h3_antibody_reference_inventory.md).
Eligibility requires an experimentally tested humanized intact Y-shaped IgG
with complete public mature heavy and light chains for the same tested variant.
The evidence for each arm's epitope is evaluated separately from IgG format.

## Arm A — IgV1 FG loop

Ahmed et al. Fig. 7 and Table 10 report ch8H9 IgG SPR against recombinant
human **2Ig-B7-H3-Fc**. R127A retained 0.1% of the wild-type response and
D128A retained 60%. The paper maps the tested IRDF motif to canonical human
4Ig CD276 positions 126–129 in IgV1 and 344–347 in IgV2. These results
support FG-loop dependence in the assay. IgV1 preference on intact 4Ig
remains a project hypothesis. The L1–R127 and H3–D128 contacts come from
docking. 5CMA is the isolated ch8H9 Fab. The paper reports humanized
mutant-binding results without showing the underlying data. Transfer the
antigen-side evidence to parent review as lineage-level guidance. Exact
humanized IgG chain-pair qualification remains open.
[Primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4705981/#F7)

| Reference | Developer or research origin | Modality and sequence evidence | 3D evidence | Verdict and rationale |
|---|---|---|---|---|
| 8H9 | Memorial Sloan Kettering; Y-mAbs developed radiolabeled omburtamab | Humanized IgG1 variants. Patent pairs H1L2 with HC 10/LC 3 and H2L1 with HC 11/LC 2. | Experimental ch8H9 Fab alone, [5CMA](https://www.rcsb.org/structure/5CMA). | **Lead lineage.** H1L2 and H2L1 each showed 34.8 nM binding to 4Ig in patent Table 4. Verify full mature domain coverage and the exact selected pair before release. FG-loop binding evidence is lineage-level. [Patent](https://patents.justia.com/patent/10316093) · [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4705981/) |
| 8H8 | University Hospital Tübingen | Mouse IgG1κ VH 36/VL 40. Tested humanized IgG1 8H8_WT and 8H8_SDIE. | No experimental structure located. | **Backup.** Parental mutant binding implicates R127. The disclosed parental pair does not verify the tested humanized HC/LC sequence. [Mapping](https://doi.org/10.1016/j.ymthe.2023.02.010) · [Humanized variants](https://pmc.ncbi.nlm.nih.gov/articles/PMC9585277/) · [Patent](https://patents.google.com/patent/EP3822288A1/en) |
| 376.96 | Ferrone lineage; MilliporeSigma supplied the study reagent | Mouse mAb; derived scFv disclosed. | Docking model. | FG-loop peptide and competition comparator. [Study](https://doi.org/10.1038/s41467-023-41631-w) · [Sequence disclosure](https://patents.google.com/patent/WO2025101807A1/en) |
| G8 | NIH/NCI collaborators | Camelid VHH, Fc format tested; RWG8 SEQ ID 2. | Docking model. | Regional comparator; VHH format. [Study](https://doi.org/10.1038/s41467-023-41631-w) · [Patent](https://patents.google.com/patent/US12552865B2/en) |
| B11 | University of Pittsburgh and East China University of Science and Technology collaborators | Human scFv and IgG-format engager. Exact chain pair unverified. | No experimental structure located. | 8H9 competition comparator. [Study](https://pubmed.ncbi.nlm.nih.gov/34601396/) |
| 8D9 | University Hospital Tübingen | Mouse IgG1κ; VH 20/VL 24. | No experimental structure located. | G130-sensitive comparator; mouse format. [Study](https://doi.org/10.1016/j.ymthe.2023.02.010) · [Patent](https://patents.google.com/patent/EP3822288A1/en) |
| 11A7 | University Hospital Tübingen | Mouse IgG1κ; VH 12/VL 16. | No experimental structure located. | Independent G130-sensitive comparator; mouse format. [Study](https://doi.org/10.1016/j.ymthe.2023.02.010) · [Patent](https://patents.google.com/patent/EP3822288A1/en) |
| T3CL11 | Nanyang Technological University collaborators | Llama VHH sequence in 9LME. | 2.4 Å experimental co-crystal with one module. | Structural comparator; exact Arm A overlap awaits canonical mapping. [Study](https://pubmed.ncbi.nlm.nih.gov/42525538/) · [9LME](https://www.rcsb.org/structure/9LME) |

## Arm B — IgC1 patch around Q228–R241

| Reference | Developer or research origin | Modality and sequence evidence | 3D evidence | Verdict and rationale |
|---|---|---|---|---|
| 20G5 / IBI334 lineage | Innovent | Experimental 20G5 Fab chains in PDB; humanized Hz20G5.26 bispecific arm HC 35/LC 36 in EP4545565A1. | Experimental cryo-EM 9LY5 and 9LY6. | **Structural lead.** Q228 at 3.001 Å in 9LY5 and 5.169 Å in 9LY6. The full bispecific arm disclosure and the deposited complexes describe different constructs. Exact variant footprint transfer remains unverified. [Paper](https://doi.org/10.1038/s41467-026-69703-7) · [Patent](https://patents.google.com/patent/EP4545565A1/en) |
| 7C4 | University Hospital Tübingen | Mouse IgG1κ; VH 4/VL 8; CC-3 engager lineage. | No experimental structure located. | Q179-sensitive neighboring site comparator. [Study](https://doi.org/10.1016/j.ymthe.2023.02.010) · [Patent](https://patents.google.com/patent/EP3822288A1/en) |
| 24F | Zhengzhou University collaborators | Humanized 24F-Hu-WT IgG and Fc variants. Chain and constant-region disclosures in CN118598997A require exact variant reconciliation. | 24F-Hu-WT docking model. | **Whole-IgG format lead.** Patent Table 4 reports 0.80 nM binding of 24F-Hu-WT to 4Ig. IgC binding supports its comparator role. Exact patch overlap remains unresolved. [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC10732625/) · [Patent](https://patents.google.com/patent/CN118598997A/en) |
| C4 | NIH/NCI collaborators | Camelid VHH, Fc format tested; RWC4 SEQ ID 3. | Docking model. | IgC1/IgC2 comparator; residue overlap unresolved. [Study](https://doi.org/10.1038/s41467-023-41631-w) · [Patent](https://patents.google.com/patent/US12552865B2/en) |
| B12 | NIH/NCI collaborators | Camelid VHH, Fc format tested; RWB12 SEQ ID 1. | Docking model. | Independent IgC1/IgC2 comparator; residue overlap unresolved. [Study](https://doi.org/10.1038/s41467-023-41631-w) · [Patent](https://patents.google.com/patent/US12552865B2/en) |
| A6 | Sun Yat-sen University; resources from Shenzhen Qiyu Biotechnology | Synthetic nanobody, Fc format tested; exact public VHH unverified. | No experimental structure located. | Competition bin distinct from 8H9; exact site unresolved. [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047927/) |
| a13 | Sun Yat-sen University; resources from Shenzhen Qiyu Biotechnology | Synthetic nanobody, Fc format tested; exact public VHH unverified. | No experimental structure located. | Shares A6 competition bin; exact site unresolved. [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047927/) |

## Release status

The selected leads are conditional. Release requires exact tested mature HC/LC
validation and internal framework/CDR coverage for the 69 parents. For Arm B,
retain 24F for format evidence and 20G5 for partial structural evidence. The
review has not established a single whole humanized IgG reference that covers
the broader intended patch experimentally.
