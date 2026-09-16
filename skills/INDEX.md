# Skill selection for B7-H3 analysis

Before writing analysis code, scan this index, select a matching skill, and read
its `SKILL.md`, runtime note, and relevant upstream examples. Reuse suitable
methods or code. If none fits, say why and use a direct analysis script.
`AGENTS.md` and the user's scientific scope take precedence over imported rules.

All 19 instruction packages were reviewed and linked under `.agents/skills/`
for project-local Codex discovery. Automatic invocation remains enabled. The
links point to these maintained folders, so a Git pull also updates the skills.
Original examples are preserved; their engineering/reporting gates are not local
contracts. Skills are instructions, not evidence of installed scientific tools.

## Priorities and scientific cautions

- Start target preparation with `binder-antibody-design`, supplemented by
  `literature-review` and relevant structure references.
- The upstream `prepare_target.py` removes heteroatoms (including glycans) and
  waters. Keep the original glycan/membrane-aware target ensemble; use a stripped
  crop only as a documented design input, with canonical residue mapping and
  full-target steric assessment. It is not a complete implementation of Step 1.
- Use RFantibody for the specified antibody campaign; generic RFdiffusion binder
  examples do not define antibody frameworks or the project's scientific choices.
- `protein-structure-prediction` supports method selection and result assessment.
  Its upstream `fold_orchestrate.py` calls Biomni-managed HPC helpers and contains
  foreign model paths. Do not execute that orchestrator here. Native confidence
  fields must retain their chain/residue mapping; generic per-residue parsers
  require inspection before use on multi-chain complexes.
- `antibody-developability-humanization` is for existing sequences. Assess
  liabilities without changing CDRs/frameworks or running humanization unrequested.
- `binding-affinity-ml-model`, `generative-molecule-design`,
  `ligand-binding-mode-analysis`, and `targeted-degrader-design` concern small
  molecules, not antibody affinity or antibody-antigen interfaces.
- `sgrna-design` is relevant only if a guide-design task is requested. Imported
  target-discovery skills must not change this project's selected B7-H3 target.
- Literature and target-evidence skills can guide searches now using available
  retrieval tools. Their local scripts/APIs and data access are task-dependent.
- GPU design/prediction and dependency-heavy analysis are not execution-ready
  until their required environments/data are found. See `../config/hpc/README.md`.

## Available methods

| Skill | When it applies |
|---|---|
| [antibody-developability-humanization](antibody-developability-humanization/SKILL.md) | Assess or humanize existing mAb, Fv, scFv, VHH, or nanobody sequences using antibody numbering, sequence liabilities, humanness, immunogenicity, CDR grafting, and framework back-mutation analysis. Use for existing antibody sequences, not de novo binder generation. |
| [binder-antibody-design](binder-antibody-design/SKILL.md) | Design de novo protein binders, antibodies, nanobodies, scFv, or VHH against a structured target using RFdiffusion or RFantibody, ProteinMPNN, structure validation, interface analysis, and candidate ranking. Use for new binder generation from a defined target and epitope. |
| [binding-affinity-ml-model](binding-affinity-ml-model/SKILL.md) | Train and benchmark target-specific small-molecule affinity or potency models from IC50, Ki, or Kd data, then screen compounds with scaffold-split and applicability-domain checks. Use only for small-molecule QSAR or affinity modeling, not antibody or protein-protein binding prediction. |
| [cell-surface-antigen-discovery](cell-surface-antigen-discovery/SKILL.md) | Discover and rank tumor-selective, antibody-accessible cell-surface antigens for ADC, CAR-T, bispecific, engager, or radioligand programs. Use when expression, topology, normal-tissue safety, and modality tractability must be evaluated together. |
| [clinicaltrials-landscape](clinicaltrials-landscape/SKILL.md) | Map a bounded, disease-centric set of ClinicalTrials.gov records by condition, purpose, intervention type, phase, status, or sponsor. Use for auditable registered-trial landscapes; not for exhaustive asset, company-pipeline, or commercial-development inventories. |
| [direction-of-effect-concordance](direction-of-effect-concordance/SKILL.md) | Assess whether a therapeutic target should be inhibited or activated by reconciling human genetics, functional screens, drug mechanisms, animal phenotypes, and literature. Use for target-directionality decisions and explicit discordance analysis. |
| [generative-molecule-design](generative-molecule-design/SKILL.md) | Generate, filter, and rank goal-directed de novo small molecules or scaffold hops using explicit activity, drug-likeness, novelty, synthesizability, and makeability objectives. Use only for small-molecule design, not antibody or protein-binder sequence design. |
| [knowledge-graph-target-reasoning](knowledge-graph-target-reasoning/SKILL.md) | Discover and rank therapeutic targets for a disease using biomedical knowledge graphs, network propagation, and interpretable evidence paths. Use for disease-target nomination or network-based prioritization; account explicitly for dataset provenance and licensing. |
| [ligand-binding-mode-analysis](ligand-binding-mode-analysis/SKILL.md) | Analyze how a small-molecule ligand binds in an experimental or supplied protein-ligand structure, including pocket residues and geometric interactions. Use for observed ligand poses; not protein-protein interfaces, de novo docking, or binding-affinity prediction. |
| [literature-deep-review](literature-deep-review/SKILL.md) | Produce an audit-ready biomedical review with exact quotations or stable locators, claim-evidence tables, contradiction checks, and optional figure evidence. Use when ordinary narrative review is insufficient and every delivered claim needs traceable support. |
| [literature-preclinical](literature-preclinical/SKILL.md) | Synthesize preclinical evidence for a target-disease pair, including in-vitro assays, in-vivo models, dosing, efficacy, PK/PD, toxicity, concordance, and IND-enabling gaps. Use when the question is specifically preclinical rather than a general literature overview. |
| [literature-review](literature-review/SKILL.md) | Find and synthesize evidence across multiple scientific or biomedical papers. Use for general literature reviews, key-paper searches, state-of-the-art summaries, or evidence synthesis that does not require the audit depth of a claim-by-claim deep review. |
| [methods-landscape-review](methods-landscape-review/SKILL.md) | Compare computational methods, tools, algorithms, or analytical approaches using published benchmarks. Use to produce a method matrix, benchmark catalog, performance scorecard, and regime-specific recommendation. |
| [open-targets](open-targets/SKILL.md) | Query and interpret the Open Targets Platform for disease-target associations, evidence rows, drugs, studies, variants, and credible sets. Use when Open Targets is the requested or appropriate primary structured source. |
| [protein-structure-prediction](protein-structure-prediction/SKILL.md) | Predict protein or complex structures from sequence using locally available methods such as AlphaFold, Boltz, Chai, or ESM-based folding. Use for structure prediction and confidence analysis; select methods from discovered host capabilities rather than assumed platform services. |
| [sgrna-design](sgrna-design/SKILL.md) | Find or design CRISPR guide RNAs for knockout, CRISPRi, or CRISPRa with supported nucleases. Prefer experimentally validated guides, then licensed precomputed resources, then transparent rule-based design. |
| [target-tractability-druggability](target-tractability-druggability/SKILL.md) | Assess whether a human target is tractable and which therapeutic modality is most viable using known drugs, structural evidence, pockets, safety, essentiality, and modality-specific constraints. Use for druggability or modality-selection questions. |
| [targeted-degrader-design](targeted-degrader-design/SKILL.md) | Design and computationally triage heterobifunctional PROTACs or targeted degraders using target warheads, E3 ligands, linkers, physicochemical filters, docking, and optional ternary modeling. Use for small-molecule degrader programs, not antibody-mediated degradation. |
| [tissue-expression-specificity](tissue-expression-specificity/SKILL.md) | Assess where a human target is expressed and identify expression-based on-target safety liabilities using normal-tissue RNA and protein atlases. Use for tissue specificity, vital-organ exposure, and cross-atlas concordance questions. |
