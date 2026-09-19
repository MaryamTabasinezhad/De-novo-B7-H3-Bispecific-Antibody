# Step 0 — Fc and chain-pairing recommendation

Date: 2026-09-19. Task: STEP0-009. Status: recommendation, not a user-selected
sequence or permission to execute Step 1.

## Recommended baseline and rationale

Recommend human IgG1 with retained Fc effector competence, one Fab A and one Fab B,
and a pairing strategy that preserves each arm's own heavy/light variable pair.
Controlled Fab-arm exchange (cFAE) is the leading assembly option; CrossMab plus
heavy-chain heterodimerization is the alternative if single-cell coexpression is
a development requirement. This is a project-specific inference from the evidence
below, not a demonstrated superiority ranking for B7-H3.

Do not require a common light chain by default: that would constrain discovery
before either epitope-specific binder has been established. If selected later,
that constraint must be applied before independent A/B design, not retrofitted
without reassessing binding. Correct heavy-chain pairing alone is insufficient.

Recommend initially separating assembly engineering from effector enhancement:
retain effector activity, but do not yet mandate afucosylation or enhanced-Fc
mutations. The B7-H3 precedent below supports evaluating enhancement, not assuming
it is needed or safe for this new construct. Exact allotype, hinge, glycoform,
pairing substitutions and FcRn policy remain open. An effector-silent product
would conflict with the required killing objective; a silent comparator could
later help attribute mechanism.

## Evidence and trade-offs

| Source | Inspected evidence | Implication and limit |
|---|---|---|
| [Labrijn et al., 2014, DOI 10.1038/nprot.2014.169](https://pubmed.ncbi.nlm.nih.gov/25255089/) | Protocol abstract: separate parental IgG1 expression, complementary CH3 substitutions and exchange of half-molecules, followed by product analysis. | cFAE retains parental Fab pairs and gives a conventional 1+1 layout. Requires two parental production streams and an exchange/purification step. Final chain identity and purity still need measurement. |
| [Schaefer et al., 2011, DOI 10.1073/pnas.1019002108](https://pmc.ncbi.nlm.nih.gov/articles/PMC3131342/) | Retrieved indexed primary-text passage: CH1–CL domain crossover combined with knobs-into-holes enabled an Ang-2/VEGF bispecific with conventional expression and purification. | CrossMab addresses light pairing while heavy-chain engineering addresses heterodimerization; permits distinct variable pairs. Domain arrangement and construct-specific byproducts must be evaluated. Evidence is from different targets, not same-molecule B7-H3 binding. |
| [Merchant et al., 1998, DOI 10.1038/nbt0798-677](https://pubmed.ncbi.nlm.nih.gov/9661204/) | Abstract: engineered heavy-chain heterodimerization plus an identical light chain generated a HER3/cMpl bispecific; engineered heavy chains supported ADCC in an anti-HER2 example. | Common-light-chain assembly is credible but requires both binders to function with that light chain. This does not show an arbitrary pair of existing B7-H3 binders can share one. |
| [Nagase-Zembutsu et al., 2016, DOI 10.1111/cas.12915](https://pmc.ncbi.nlm.nih.gov/articles/PMC4970835/) | Retrieved Results, Figures 3–4 and Discussion: afucosylated anti-B7-H3 DS-5573a increased ADCC compared with its fucosylated parent and retained macrophage ADCP in tested cells. | Direct target-specific support for Fc-mediated activity and an enhancement comparison. It does not establish therapeutic safety, clinical benefit, internalization or cis engagement for this new 1A+1B antibody. |

No head-to-head B7-H3 comparison of these three assembly approaches was found in
this bounded review. No quantitative platform ranking or guarantee of stability,
low aggregation, Fc function or manufacturability is justified.

## What assembly cannot resolve

The selected product must simultaneously engage two epitopes on ONE native human
4Ig-B7-H3 molecule. All three approaches solve chain assembly questions; none
establishes the required Fab orientation, hinge reach, glycan/membrane clearance,
or simultaneous engagement for this target. Preserve the workflow's early
geometry compatibility gate before large-scale design and later full validation.

Internalization and Fc-mediated activity remain separate required endpoints.
Assess surface residence and immune-effector access alongside uptake rather than
treating stronger internalization as evidence of stronger killing. This is a
prospective mechanistic assessment need, not an observed conflict in this project.
Likewise, assess aggregation and stability on the actual assembled molecule.

## Decision package and continuation boundary

Proposed policy for user selection: human IgG1 with retained effector competence;
distinct cognate light chains; cFAE as the leading assembly route, with CrossMab
as an explicitly reviewed alternative; enhancement remains a comparison question.
This does not select exact sequences or establish platform availability for
manufacturing. No FcRn enhancement or numerical acceptance cutoff is inferred.

Until selected, retain these as recommendations in the decision log. Independent
Step 0 risk/budget planning can continue; work requiring a locked pairing strategy
must wait for that scientific choice. Step 1, acquisition, installation and
compute jobs remain excluded.

## Search and access notes

Used the project literature-review skill and browser scholarly search on
2026-09-19. Queries covered controlled Fab-arm exchange IgG1, CrossMab domain
crossover, common-light-chain/knobs-into-holes, and DS-5573a ADCC/ADCP. Included
primary platform studies/protocol and direct B7-H3 functional evidence; excluded
reviews and patents as support for the recommendation. Deduplicated by DOI.
The 2013 cFAE study (10.1073/pnas.1220145110) was identified but the 2014 protocol
abstract supplied the inspected assembly description. Merchant was read at
abstract level. PMC direct opens for cFAE and CrossMab encountered recaptcha;
CrossMab support is limited to the retrieved indexed passage. DS-5573a Results
and Discussion were returned by scholarly search. No inaccessible detail is
treated as verified. This is a bounded decision review, not an exhaustive
systematic review or a freedom-to-operate assessment. No analysis code or
scientific computation was needed.
