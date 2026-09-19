# Step 0 recommendation: human B7-H3 isoforms and soluble antigen

Reviewed 2026-09-18. Task `STEP0-005`. Status: evidence review accepted by PM; policy approved by the user on 2026-09-19 (decision log, STEP0-006). Literature/document review only; no target preparation, biological data generation, software installation, or compute jobs.

## Recommendation

**Require both binders to recognize distinct accessible epitopes on native, cell-surface human 4Ig-B7-H3. Characterize human 2Ig binding, but make it neither mandatory nor an automatic exclusion. Treat soluble B7-H3 as a potential competing antigen and exposure risk, not an intended therapeutic target in this campaign.**

Prefer candidates that retain tumor-cell binding and function despite relevant soluble antigen. Do not impose an unvalidated zero-soluble-binding rule or numerical isoform-selectivity cutoff. This recommendation is an interpretation of the evidence below, conditional on the user's broad solid-cancer objective; no particular cancer indication has yet been selected.

This keeps all three user-required objectives—binding, internalization, and Fc-mediated killing—active, alongside stability and low aggregation. Isoform selection alone does not establish any of those properties. Trade-offs must still be presented to the user.

## Terms that must stay separate

4Ig and 2Ig refer to extracellular immunoglobulin-domain organization: two IgV–IgC pairs versus one. Cell-surface versus soluble describes presentation. Soluble preparations can differ in origin, domain content, glycosylation, oligomerization, and experimental tags. **Do not equate all 2Ig with soluble antigen, or all 4Ig with exclusively membrane-bound antigen.** The evidence includes cell-surface 2Ig constructs, a secreted splice product, and soluble recombinant 4Ig used in binding/competition assays [E1, E2, E3].

## Primary evidence and limits

| ID / source | Evidence inspected | Relevance and limitation |
|---|---|---|
| E1. [Camel nanobody-based B7-H3 CAR-T cells show high efficacy against large solid tumours](https://www.nature.com/articles/s41467-023-41631-w.pdf), Nature Communications 2023; DOI 10.1038/s41467-023-41631-w | Full-text PDF, Results on isoform expression, Fig. 1 and Supplementary Fig. 1 discussion; binding/competition results in Figs. 2 and 4. 4Ig predominated in most examined tumor transcript datasets and protein analyses. Ovarian transcript data were an exception; a purported 2Ig protein band also appeared in negative controls. Recombinant 4Ig inhibited one CAR's cytotoxicity in competition experiments. | Supports 4Ig as the primary target but cautions against inferring cell-surface 2Ig abundance from RNA or one antibody band. Soluble recombinant 4Ig can retain a relevant epitope. CAR-T outcomes do not establish Fc-mediated killing or internalization for our construct. |
| E2. [Origination of New Immunological Functions in the Costimulatory Molecule B7-H3](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0024751), PLOS ONE 2011; DOI 10.1371/journal.pone.0024751 | Full text, Results and Fig. 3: engineered cells expressing human 2Ig released detectable soluble material; wild-type 4Ig transfectants did not in that system. Sequence changes altered release. | Demonstrates that membrane 2Ig and soluble material are distinct states, and that release is context-dependent. The transfection result does not prove that every human 4Ig-containing context lacks soluble antigen. |
| E3. [Characterization of a Soluble B7-H3 Spliced from the Intron](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0076965), PLOS ONE 2013; DOI 10.1371/journal.pone.0076965 | Full text, Results/Fig. 1 and Discussion: cloned a 248-residue soluble splice product lacking a transmembrane domain; serum assays and tissue transcript measurements were examined in hepatocellular carcinoma. | Supports an alternative source of soluble antigen. The serum assay did not uniquely distinguish every molecular form, so it does not establish that all circulating B7-H3 is this product. Its emphasis on splicing differs from cleavage-based explanations in other studies. |
| E4. [Unraveling the dynamics of B7-H3-targeting therapeutic antibodies](https://pubmed.ncbi.nlm.nih.gov/39814321/), Journal of Controlled Release 2025; DOI 10.1016/j.jconrel.2025.01.030 | PubMed abstract and displayed figure captions inspected; full-text access was blocked through the attempted PMC/publisher routes. Two radiolabeled antibodies differed in uptake and retention: one had higher initial uptake with declining retention, the other lower uptake with more stable retention. Fig. 1 compares human 4Ig with **murine** 2Ig. | Supports examining distribution/retention rather than affinity alone. The species difference means the reported comparison is not clean proof of human 4Ig-versus-human 2Ig selectivity. Shedding as the explanation is presented as likely, not established as the sole cause. Not a tandem-scFv-Fc efficacy comparison. |
| E5. [Anti-cancer immune priming with β-radioligand therapy using a novel high affinity antibody selectively targeting the 4Ig-Isoform of B7-H3](https://www.thno.org/v16p5370.htm), Theranostics 2026; DOI 10.7150/thno.123285 | Full text, Table 1, binding results and Discussion: MIL33B bound human 4Ig at a reported BLI KD of 72.3 pM and human 2Ig at 580 pM, approximately eightfold preference. Radiolabeled antibody showed preclinical activity; non-radioactive antibody did not show significant efficacy in the described comparison. | Preference is not absence of 2Ig binding. Radiotherapy, antibody dose, and model context limit transfer to an unconjugated Fc construct. The study supports evaluating soluble competition, not assuming that its magnitude, clinical benefit, or an eightfold selection threshold transfers to this project. |
| E6. [Dimerization of the 4Ig isoform of B7-H3 in tumor cells mediates enhanced proliferation and tumorigenic signaling](https://www.nature.com/articles/s42003-023-05736-8), Communications Biology 2024; DOI 10.1038/s42003-023-05736-8 | Full-text abstract/results description: 4Ig knockout/re-expression and experimentally induced dimerization in gynecological cancer models supported context-dependent tumor-cell signaling effects. | Binding or crosslinking cannot simply be equated with beneficial signaling blockade. These experiments do not demonstrate that our unbuilt biparatopic antibody would stimulate or inhibit the same pathways. |

## Trade-offs between policies

These are project recommendations and design implications, not head-to-head clinical conclusions.

| Policy | Potential advantage | Cost or uncertainty | Recommendation |
|---|---|---|---|
| Require 4Ig; characterize 2Ig | Focuses development on the best-supported primary tumor-surface form while retaining informative comparators | Could miss an indication in which authentic surface 2Ig is important | Preferred starting policy; revisit with indication-specific protein evidence |
| Require both 4Ig and 2Ig | Broader potential isoform coverage | Adds epitope/geometry constraints; benefit depends on actual tumor-surface expression; soluble competition still needs measurement | Do not require without a defined reason |
| Require 4Ig binding and absolutely no 2Ig/soluble binding | Attempts to reduce competing binding | Could discard useful candidates; soluble 4Ig can share target epitopes; no validated zero-binding criterion | Do not impose now |
| Intentionally bind/neutralize soluble B7-H3 | Could address a separate biological hypothesis | Adds a mechanism, exposure demands, and validation burden not established for the current objectives | Not recommended as a current goal |

## Soluble-antigen policy and relevance to the construct

Treat soluble binding as a risk to characterize, not as proof a candidate fails. A clinically meaningful antigen sink depends on molecular form, concentration, affinity, dose, and disposition. The studies support the concern but do not quantify that risk for this proposed construct [E3–E5]. No clinical concentration or tolerable competition threshold is selected here.

For later authorized experimental planning, assess membrane 4Ig binding by A, B, and the assembled construct; human 2Ig binding; and binding/competition with defined soluble species. Evaluate effects on cell binding, internalization, and Fc-dependent killing separately. Assess soluble-antigen immune-complex behavior separately from the antibody's intrinsic aggregation propensity. These are proposed assessment categories, not executed protocols or a new experimental authorization.

Do not infer normal-tissue safety from 4Ig preference, dual binding, or isoform RNA abundance. No normal-tissue safety atlas was reviewed in this task. Do not infer that rapid internalization optimizes Fc-mediated activity: the two user-required functions need separate evidence and any conflict must be escalated. No epitope pair, spacing cutoff, domain assignment, or cis-binding decision is made by this recommendation.

## Search, contradictions, and confidence

Bounded web search on 2026-09-18 using combinations of `B7-H3 4Ig 2Ig human cancer isoforms antibody internalization soluble`, `soluble B7-H3 shedding`, `B7-H3 alternative splicing`, and exact study titles/identifiers. Included six unique primary studies with retrievable relevant results; counted the 2026 paper once rather than also counting its preprint/conference records. Patents and reviews were discovery aids, not evidence for the recommendation. No sequence/structure datasets were downloaded or analyzed. No analysis code was needed.

Main limitations: selected studies span different indications and modalities; no systematic pooled estimate or indication-specific prevalence analysis was performed. Evidence for 2Ig protein abundance and soluble-antigen origin is not uniform. E4 was limited to abstract/figure-caption access, explicitly identified above. Published affinity assays use different formats and cannot be treated as interchangeable rankings. There is no direct validation of the requested combined internalization/Fc/stability profile for this tandem-scFv-Fc.

Confidence: moderate for prioritizing cell-surface human 4Ig; lower for the value of mandatory human 2Ig coverage without a chosen indication, and for any quantitative soluble-binding exclusion threshold. PM's independent review is recorded in `coordination/pm.md`.

## Policy approved after review — 2026-09-19

Approved scope wording:

> Human cell-surface 4Ig-B7-H3 recognition is required for both binding units. Human 2Ig binding will be characterized but is neither required nor prohibited. Soluble B7-H3 is not an intended therapeutic target; its effects on binding, internalization, Fc-mediated activity, and disposition will be assessed when those studies are authorized. Prefer low functional interference without imposing an unsupported zero-binding rule. Revisit this policy if the selected cancer indication provides compelling contrary evidence.

The user approved this policy in STEP0-006. It does not authorize Step 1.
