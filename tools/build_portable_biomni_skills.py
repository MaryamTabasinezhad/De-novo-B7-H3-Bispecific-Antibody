#!/usr/bin/env python3
"""Build portable Codex skill sources from the selected Biomni Lab exports.

The generated bundle deliberately separates immutable upstream material from the
active Codex instruction layer.  Upstream scripts are retained as implementation
examples under references/upstream-biomni; they are not presented as executable
Codex scripts until the target host has supplied and tested a runtime binding.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_ARCHIVES = PROJECT_ROOT / "third_party" / "biomni" / "archives"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "build"
SOURCE_URL = "https://biomni.phylo.bio/skills"
RETRIEVED_AT = "2026-09-14"


@dataclass(frozen=True)
class SkillSpec:
    name: str
    skill_id: str
    category: str
    display_name: str
    short_description: str
    description: str
    default_prompt: str
    purpose: str
    boundaries: tuple[str, ...]
    workflow: tuple[str, ...]
    outputs: tuple[str, ...]


SPECS = (
    SkillSpec(
        "knowledge-graph-target-reasoning", "skill_c18b5e3fe7db49728f7bfd77e3f4bdd7",
        "Drug Discovery", "Knowledge-Graph Target Reasoning",
        "Rank disease targets using interpretable graph paths",
        "Discover and rank therapeutic targets for a disease using biomedical knowledge graphs, network propagation, and interpretable evidence paths. Use for disease-target nomination or network-based prioritization; account explicitly for dataset provenance and licensing.",
        "Use $knowledge-graph-target-reasoning to rank therapeutic targets for this disease and explain the supporting graph paths.",
        "Prioritize disease-associated genes or proteins with graph structure while preserving the provenance, license class, and biological meaning of every edge and seed source.",
        (
            "Do not treat graph proximity as causal evidence or proof of tractability.",
            "Do not mix academic-only and commercial-safe graph layers without labeling the run.",
            "Do not claim complete graph coverage when required datasets are absent or version-mismatched.",
        ),
        (
            "Resolve the disease identity and define the intended licensing mode.",
            "Discover available graph datasets, schemas, versions, and provenance fields before choosing a ranker.",
            "Select disease anchors and run a transparent propagation or random-walk method with recorded parameters.",
            "Apply face-validity checks, enumerate evidence paths, and validate leading candidates against independent literature or structured sources.",
            "Report sensitivity to seeds, graph version, excluded sources, and edge-license filters.",
        ),
        ("ranked target table", "interpretable evidence paths", "run manifest", "method and licensing notes"),
    ),
    SkillSpec(
        "cell-surface-antigen-discovery", "skill_522578a78cb54c8fa5d7eb3fdcd7e09b",
        "Drug Discovery", "Cell-Surface Antigen Discovery",
        "Rank tumor-selective antibody-accessible antigens",
        "Discover and rank tumor-selective, antibody-accessible cell-surface antigens for ADC, CAR-T, bispecific, engager, or radioligand programs. Use when expression, topology, normal-tissue safety, and modality tractability must be evaluated together.",
        "Use $cell-surface-antigen-discovery to prioritize accessible tumor antigens for this modality and disease context.",
        "Integrate tumor expression, extracellular topology, normal-tissue expression, and modality-specific constraints into an auditable antigen ranking.",
        (
            "Do not substitute gene essentiality for cell-surface accessibility or tumor selectivity.",
            "Do not infer antibody accessibility from RNA expression alone.",
            "Keep known positive controls in the analysis when they are available.",
        ),
        (
            "Clarify tumor type, modality, input data, cell labels, and antigen search breadth.",
            "Discover available single-cell, surfaceome, topology, and normal-tissue resources and freeze their versions.",
            "Quantify malignant-compartment specificity, apply topology gates, and assess normal-tissue liabilities.",
            "Score candidates transparently, run sensitivity checks, and attach source-grounded evidence to leading candidates.",
            "Separate validated antigens, plausible novel candidates, and candidates limited by missing evidence.",
        ),
        ("ranked antigen table", "normal-tissue safety table", "topology evidence", "analysis manifest"),
    ),
    SkillSpec(
        "direction-of-effect-concordance", "skill_b973718932a54ffb8b326f7f157e7036",
        "Drug Discovery", "Direction-of-Effect Concordance",
        "Decide whether a target should be inhibited or activated",
        "Assess whether a therapeutic target should be inhibited or activated by reconciling human genetics, functional screens, drug mechanisms, animal phenotypes, and literature. Use for target-directionality decisions and explicit discordance analysis.",
        "Use $direction-of-effect-concordance to determine whether this target should be activated or inhibited and explain conflicts.",
        "Build a per-evidence-axis direction matrix and derive a qualified activate, inhibit, mixed, or insufficient-evidence conclusion.",
        (
            "A null loss-of-function phenotype does not by itself support activation.",
            "Do not hide conflicting evidence or collapse incompatible disease contexts.",
            "Do not invent directionality when an evidence axis is unavailable.",
        ),
        (
            "Resolve target and disease identifiers and define the therapeutic context.",
            "Discover structured genetics, perturbation, drug-mechanism, and phenotype sources available in the environment.",
            "Retrieve directional literature and preserve stable citations or record locators.",
            "Construct the evidence matrix, apply explicit direction rules, and expose discordance.",
            "Assign a confidence tier tied to evidence completeness rather than narrative strength.",
        ),
        ("direction evidence matrix", "consensus call", "discordance flags", "citation-verification record"),
    ),
    SkillSpec(
        "open-targets", "skill_53ea5bef4333422681930c9edc9f9fcd",
        "Drug Discovery", "Open Targets",
        "Query and interpret Open Targets evidence",
        "Query and interpret the Open Targets Platform for disease-target associations, evidence rows, drugs, studies, variants, and credible sets. Use when Open Targets is the requested or appropriate primary structured source.",
        "Use $open-targets to retrieve and interpret Open Targets evidence for this disease-target question.",
        "Produce bounded, schema-aware Open Targets results with pagination, release metadata, completeness labels, and provenance.",
        (
            "Do not equate the overall association score with validated therapeutic efficacy.",
            "Preserve datasource and datatype semantics instead of merging unlike evidence rows.",
            "Report pagination or retrieval limits whenever the result is not exhaustive.",
        ),
        (
            "Resolve disease, target, drug, study, and variant identifiers as required.",
            "Discover whether live API access, cached fixtures, or a local snapshot is available.",
            "Record API or snapshot version metadata and apply bounded pagination.",
            "Validate returned records against the expected schema and serialize source evidence before interpretation.",
            "Create deterministic summaries and figures from the serialized records.",
        ),
        ("normalized evidence records", "ranked association table", "coverage metadata", "provenance manifest"),
    ),
    SkillSpec(
        "target-tractability-druggability", "skill_8de1ad6db2524087b4588d1c20d65422",
        "Drug Discovery", "Target Tractability and Druggability",
        "Assess target tractability across therapeutic modalities",
        "Assess whether a human target is tractable and which therapeutic modality is most viable using known drugs, structural evidence, pockets, safety, essentiality, and modality-specific constraints. Use for druggability or modality-selection questions.",
        "Use $target-tractability-druggability to assess this target across relevant therapeutic modalities.",
        "Combine orthogonal evidence into a transparent modality scorecard without treating any single database or pocket predictor as decisive.",
        (
            "Do not assume a structural pocket makes an extracellular antibody target more or less viable.",
            "Do not silently substitute a predicted structure for an experimental structure.",
            "Separate target biology, modality feasibility, safety, and evidence quality.",
        ),
        (
            "Resolve the target and intended disease or modality context.",
            "Discover available target, drug, safety, essentiality, and structure resources.",
            "Retrieve structured tractability evidence and choose the best justified structures.",
            "Run pocket analysis only when relevant and when a validated implementation is available.",
            "Score modalities transparently and document missing or contradictory evidence.",
        ),
        ("modality scorecard", "structure and pocket evidence", "safety and essentiality notes", "decision rationale"),
    ),
    SkillSpec(
        "tissue-expression-specificity", "skill_6555e1f8055e4a49bcc909a8fd84b635",
        "Drug Discovery", "Tissue Expression Specificity",
        "Assess tissue expression and on-target safety",
        "Assess where a human target is expressed and identify expression-based on-target safety liabilities using normal-tissue RNA and protein atlases. Use for tissue specificity, vital-organ exposure, and cross-atlas concordance questions.",
        "Use $tissue-expression-specificity to assess normal-tissue expression and on-target safety for this target.",
        "Resolve the target, compare available normal-tissue atlases, quantify specificity, and surface organ-level liabilities with source provenance.",
        (
            "RNA expression alone is not proof of cell-surface protein abundance.",
            "Do not compare atlas values as if their measurement scales were identical.",
            "Flag missing tissues, version differences, and discordant RNA/protein evidence.",
        ),
        (
            "Resolve gene, Ensembl, or UniProt identifiers.",
            "Discover local GTEx/HPA resources or permitted live access and record release versions.",
            "Load and normalize each atlas without erasing source-specific measurement semantics.",
            "Compute specificity and cross-atlas summaries and inspect vital-organ expression.",
            "Ground biological interpretation in retrievable literature where needed.",
        ),
        ("tissue expression table", "specificity metrics", "cross-atlas comparison", "on-target safety flags"),
    ),
    SkillSpec(
        "literature-review", "skill_36c19691710c4e16a088fb810be15460",
        "General", "Scientific Literature Review",
        "Find and synthesize scientific literature",
        "Find and synthesize evidence across multiple scientific or biomedical papers. Use for general literature reviews, key-paper searches, state-of-the-art summaries, or evidence synthesis that does not require the audit depth of a claim-by-claim deep review.",
        "Use $literature-review to produce a source-grounded review of this scientific question.",
        "Answer a bounded scientific question using retrieved peer-reviewed records and open full text when available.",
        (
            "Do not cite papers that were not actually retrieved and inspected.",
            "Distinguish abstract-level support from full-text support.",
            "Use the deep-review skill when exact quotations, stable locators, or figure-level evidence are required.",
        ),
        (
            "Define the question, date range, study types, and inclusion boundaries from existing context.",
            "Use available scholarly databases or web search with several complementary queries.",
            "Deduplicate records and retain stable identifiers, retrieval dates, and source URLs.",
            "Extract claims, methods, limitations, and contradictions only from inspected records.",
            "Synthesize the evidence and state important coverage gaps.",
        ),
        ("cited narrative", "structured evidence table", "search and inclusion summary", "limitations"),
    ),
    SkillSpec(
        "literature-preclinical", "skill_845c829245474c4091703e01e627aa00",
        "General", "Preclinical Literature Review",
        "Synthesize target-disease preclinical evidence",
        "Synthesize preclinical evidence for a target-disease pair, including in-vitro assays, in-vivo models, dosing, efficacy, PK/PD, toxicity, concordance, and IND-enabling gaps. Use when the question is specifically preclinical rather than a general literature overview.",
        "Use $literature-preclinical to assess the preclinical evidence for this target-disease program.",
        "Create an auditable preclinical evidence map that separates model type, intervention, exposure, efficacy, safety, and translational limitations.",
        (
            "Do not combine cell, animal, ex-vivo, and human evidence without labeling the evidence level.",
            "Do not infer dose comparability across studies without PK or exposure support.",
            "Distinguish peer-reviewed evidence from conference, patent, or company claims.",
        ),
        (
            "Define target, disease, intervention class, species, model types, and time window.",
            "Search available scholarly sources with separate in-vitro, in-vivo, PK/PD, and safety queries.",
            "Deduplicate and extract model, dose, route, schedule, endpoints, effect direction, and limitations.",
            "Assess cross-model concordance and identify translational or IND-enabling gaps.",
            "Report evidence strength and unresolved contradictions.",
        ),
        ("preclinical evidence table", "cross-model synthesis", "PK/PD and toxicity summary", "development gaps"),
    ),
    SkillSpec(
        "clinicaltrials-landscape", "skill_7d39cb6745524d1d9e4493c12c265a4a",
        "Literature", "Clinical Trials Landscape",
        "Map a bounded ClinicalTrials.gov landscape",
        "Map a bounded, disease-centric set of ClinicalTrials.gov records by condition, purpose, intervention type, phase, status, or sponsor. Use for auditable registered-trial landscapes; not for exhaustive asset, company-pipeline, or commercial-development inventories.",
        "Use $clinicaltrials-landscape to map registered trials for this disease and intervention scope.",
        "Retrieve, classify, and summarize a reproducible set of ClinicalTrials.gov records with explicit query coverage.",
        (
            "Registry status is not proof of current asset development or clinical efficacy.",
            "Do not infer commercial ownership or pipeline status beyond registry fields.",
            "Report query terms, filters, retrieval date, pagination, and coverage limits.",
        ),
        (
            "Clarify condition, intervention, study purpose, status, phase, sponsor, and date boundaries.",
            "Discover live API access or a supplied offline export and record the mode used.",
            "Retrieve all pages within the declared scope and preserve raw normalized records.",
            "Classify mechanisms and study purposes with auditable rules and unresolved categories.",
            "Generate summary tables and deterministic figures from the frozen record set.",
        ),
        ("trial-level dataset", "coverage record", "classification table", "landscape summary"),
    ),
    SkillSpec(
        "literature-deep-review", "skill_18ead39ed464498b83ebe9fbcbfb7666",
        "Literature", "Literature Deep Review",
        "Build audit-ready claim-level evidence reviews",
        "Produce an audit-ready biomedical review with exact quotations or stable locators, claim-evidence tables, contradiction checks, and optional figure evidence. Use when ordinary narrative review is insufficient and every delivered claim needs traceable support.",
        "Use $literature-deep-review to build a claim-level, auditable evidence review of this biomedical question.",
        "Freeze a review corpus, acquire permissible source text, construct claim-level evidence, independently verify anchors, and deliver reproducible review artifacts.",
        (
            "Do not claim full-text support when only metadata or an abstract was inspected.",
            "Respect access and reuse rights for every source and figure.",
            "Do not fabricate quotations, page numbers, figure interpretations, or execution provenance.",
        ),
        (
            "Select an effort mode and define the review question, evidence types, and stopping rule.",
            "Discover available scholarly search and document-retrieval capabilities, then freeze the corpus.",
            "Acquire and parse permitted text and figures with a ledger recording source and rights state.",
            "Build atomic claims and evidence anchors; separate unsupported, contradicted, and ambiguous claims.",
            "Cross-check consequential claims against the inspected sources; additional agents are not required.",
            "Write the requested review with a concise evidence table and unresolved questions.",
        ),
        ("corpus ledger", "claim-evidence matrix", "quotation and figure anchors", "verified review artifact"),
    ),
    SkillSpec(
        "methods-landscape-review", "skill_5c16bd4ae5fc49b199405080a847165e",
        "Literature", "Methods Landscape Review",
        "Compare computational methods using published benchmarks",
        "Compare computational methods, tools, algorithms, or analytical approaches using published benchmarks. Use to produce a method matrix, benchmark catalog, performance scorecard, and regime-specific recommendation.",
        "Use $methods-landscape-review to compare methods for this task and recommend an approach from benchmark evidence.",
        "Build an evidence-grounded comparison that distinguishes task regime, dataset, metric, compute cost, licensing, and implementation maturity.",
        (
            "Do not compare headline metrics measured on incompatible datasets or splits.",
            "Do not treat popularity as benchmark superiority.",
            "Separate published performance from local runtime availability.",
        ),
        (
            "Define the computational task, regimes, candidate families, metrics, and constraints.",
            "Search benchmark papers and authoritative method documentation with recency and citation-bias controls.",
            "Extract comparable evidence into a normalized benchmark catalog.",
            "Score methods by regime and expose missing, incompatible, or weak comparisons.",
            "Inventory locally available implementations only after the literature comparison is stable.",
        ),
        ("method comparison matrix", "benchmark catalog", "performance scorecard", "regime-specific recommendation"),
    ),
    SkillSpec(
        "binding-affinity-ml-model", "skill_0c841f13357d45b0ac471169e58a535d",
        "Molecular Design", "Small-Molecule Binding Affinity ML",
        "Train honest target-specific small-molecule affinity models",
        "Train and benchmark target-specific small-molecule affinity or potency models from IC50, Ki, or Kd data, then screen compounds with scaffold-split and applicability-domain checks. Use only for small-molecule QSAR or affinity modeling, not antibody or protein-protein binding prediction.",
        "Use $binding-affinity-ml-model to curate this target's small-molecule data and benchmark affinity models honestly.",
        "Curate endpoint-consistent compound data, evaluate models with leakage-resistant splits, and restrict screening claims to the validated applicability domain.",
        (
            "Do not use this skill to estimate antibody affinity or protein-protein binding.",
            "Do not mix IC50, Ki, and Kd values without an explicit justified model.",
            "Do not silently replace a requested framework or report random-split performance as scaffold generalization.",
        ),
        (
            "Resolve the target and define endpoint, units, assay scope, and modeling objective.",
            "Discover accessible ChEMBL or supplied datasets and freeze source versions.",
            "Standardize structures, censoring, duplicates, and assay context; pass a data-reality gate.",
            "Benchmark suitable models with scaffold and random splits, uncertainty, and applicability-domain checks.",
            "Screen external compounds only with the selected validated model and report novelty and domain limitations.",
        ),
        ("curated assay dataset", "benchmark results", "model bundle or specification", "screened candidate table"),
    ),
    SkillSpec(
        "generative-molecule-design", "skill_2c67771543d14271bbdda3c903d773f1",
        "Molecular Design", "Generative Small-Molecule Design",
        "Generate and triage goal-directed small molecules",
        "Generate, filter, and rank goal-directed de novo small molecules or scaffold hops using explicit activity, drug-likeness, novelty, synthesizability, and makeability objectives. Use only for small-molecule design, not antibody or protein-binder sequence design.",
        "Use $generative-molecule-design to design and triage small molecules for this target and objective profile.",
        "Run a reproducible multi-objective small-molecule campaign with an explicitly qualified activity backend and honest synthesis limitations.",
        (
            "Do not use for antibody, peptide, or protein binder generation.",
            "Generated structures are hypotheses and are not synthesized, active, or safe by default.",
            "Do not substitute an unvalidated generic oracle for target-specific activity.",
        ),
        (
            "Define target, seed chemistry, allowed transformations, objective weights, and forbidden motifs.",
            "Discover installed chemistry packages, activity backends, synthesis tools, and model caches.",
            "Choose and validate an activity backend before generation.",
            "Generate with recorded seeds and parameters, then standardize, deduplicate, filter, and rank molecules.",
            "Run retrosynthesis only when a validated local implementation and models are available; otherwise report the proxy used.",
        ),
        ("generated molecule table", "objective and filter audit", "novelty analysis", "qualified synthesis assessment"),
    ),
    SkillSpec(
        "ligand-binding-mode-analysis", "skill_ebf89d293f8c49058111727a00675dce",
        "Molecular Design", "Ligand Binding-Mode Analysis",
        "Map small-molecule contacts in protein structures",
        "Analyze how a small-molecule ligand binds in an experimental or supplied protein-ligand structure, including pocket residues and geometric interactions. Use for observed ligand poses; not protein-protein interfaces, de novo docking, or binding-affinity prediction.",
        "Use $ligand-binding-mode-analysis to map and compare the observed contacts in this protein-ligand structure.",
        "Produce a reproducible contact map from a specified structure while separating observed geometry from energetic or affinity claims.",
        (
            "Do not use for antibody-antigen or other protein-protein interfaces.",
            "Do not present geometric contacts as binding energies.",
            "Do not invent a pose when no bound ligand structure is available.",
        ),
        (
            "Resolve the structure, ligand identifier, chain scope, interaction depth, and comparison set.",
            "Discover installed parsing, protonation, interaction, and rendering tools.",
            "Fetch or validate the structure and identify the intended ligand unambiguously.",
            "Run a validated interaction engine or documented geometry fallback and label confidence and source.",
            "Compare structures only after establishing residue and ligand mappings.",
        ),
        ("pocket contact table", "interaction classifications", "cross-structure comparison", "visualization inputs"),
    ),
    SkillSpec(
        "sgrna-design", "skill_8450f18da5c947caabf0a26d3f262389",
        "Molecular Design", "sgRNA Design",
        "Find and rank CRISPR guide RNAs",
        "Find or design CRISPR guide RNAs for knockout, CRISPRi, or CRISPRa with supported nucleases. Prefer experimentally validated guides, then licensed precomputed resources, then transparent rule-based design.",
        "Use $sgrna-design to find or design guides for this target, organism, nuclease, and perturbation mode.",
        "Select guides through a tiered evidence strategy with explicit genome build, transcript, nuclease, PAM, off-target method, and licensing provenance.",
        (
            "Do not mix genome builds or transcript coordinates.",
            "Do not treat an in-silico score as experimental validation.",
            "Respect commercial-use and material-transfer restrictions of guide resources.",
        ),
        (
            "Resolve organism, genome build, gene or transcript, perturbation mode, nuclease, and delivery constraints.",
            "Search bundled and literature-derived validated guides first.",
            "Discover whether permitted precomputed design resources are locally available.",
            "Use de novo design only when higher-evidence tiers are unavailable and a validated scorer/reference genome exists.",
            "Export selected guides with sequence, PAM, coordinates, scores, evidence tier, and provenance.",
        ),
        ("ranked guide table", "design and off-target metadata", "resource licensing notes", "selection rationale"),
    ),
    SkillSpec(
        "targeted-degrader-design", "skill_c8d77a80500548a5ad07d8756469814d",
        "Molecular Design", "Targeted Degrader Design",
        "Design and triage small-molecule targeted degraders",
        "Design and computationally triage heterobifunctional PROTACs or targeted degraders using target warheads, E3 ligands, linkers, physicochemical filters, docking, and optional ternary modeling. Use for small-molecule degrader programs, not antibody-mediated degradation.",
        "Use $targeted-degrader-design to define and triage a targeted-degrader campaign for this protein.",
        "Build a transparent degrader design space and rank candidates without overstating degradation, permeability, or ternary-complex predictions.",
        (
            "Do not use for antibody, lysosome-targeting chimera, or protein-binder design unless explicitly adapted.",
            "A binary warhead binder is not automatically a functional degrader.",
            "Do not use non-commercial software in a commercial workflow without an appropriate license or substitution.",
        ),
        (
            "Define target, degradation mechanism, cellular context, warhead evidence, and allowed E3 ligases.",
            "Discover licensed structure-preparation, chemistry, docking, property, and modeling tools.",
            "Validate warhead pose and exit vector before enumerating E3 ligands and linkers.",
            "Assemble candidates reproducibly and score physicochemical, permeability, synthesis, and structural criteria.",
            "Use ternary-complex modeling only as a qualified optional tier and preserve uncertainty.",
        ),
        ("candidate degrader table", "component and linker provenance", "property and docking scorecard", "assumption log"),
    ),
    SkillSpec(
        "antibody-developability-humanization", "skill_96d2106323804eb8ad9fe07bd476ff4d",
        "Molecular Design", "Antibody Developability and Humanization",
        "Assess and humanize antibody variable regions",
        "Assess or humanize existing mAb, Fv, scFv, VHH, or nanobody sequences using antibody numbering, sequence liabilities, humanness, immunogenicity, CDR grafting, and framework back-mutation analysis. Use for existing antibody sequences, not de novo binder generation.",
        "Use $antibody-developability-humanization to assess these antibody sequences and propose traceable humanization variants.",
        "Produce numbered, auditable sequence assessments and conservative humanization variants while separating predicted liabilities from measured developability.",
        (
            "Do not change CDRs or structurally important framework residues without explicit rationale.",
            "Do not claim reduced immunogenicity or improved developability without experimental validation.",
            "Licensed predictors such as NetMHCIIpan must never be downloaded automatically.",
        ),
        (
            "Ingest and validate chain identity, species, format, and antibody numbering.",
            "Discover installed numbering, liability, humanness, and immunogenicity tools and their licenses.",
            "Run sequence-liability and biophysical proxy analysis with recorded methods.",
            "When humanization is requested, select documented human germlines, graft CDRs, and propose justified framework back-mutations.",
            "Reassess every proposed construct and preserve a residue-level change ledger.",
        ),
        ("numbered sequence table", "liability assessment", "humanization variants", "change and rationale ledger"),
    ),
    SkillSpec(
        "binder-antibody-design", "skill_5c0f0561b5724ede838bd08b047af399",
        "Molecular Design", "Binder and Antibody Design",
        "Design protein binders and antibodies against structures",
        "Design de novo protein binders, antibodies, nanobodies, scFv, or VHH against a structured target using RFdiffusion or RFantibody, ProteinMPNN, structure validation, interface analysis, and candidate ranking. Use for new binder generation from a defined target and epitope.",
        "Use $binder-antibody-design to plan and execute a reproducible binder-design campaign for this target and epitope.",
        "Run a staged, reproducible binder campaign that preserves target numbering, design-anchor provenance, sequence diversity, independent validation, and honest confidence interpretation.",
        (
            "Do not begin production design until target structure, chain mapping, epitope, and design anchors are explicit.",
            "Predicted interface confidence is not measured binding affinity.",
            "Do not use upstream container paths or command flags until they are verified against the target installation.",
        ),
        (
            "Freeze the target structure, canonical numbering map, epitope, design anchors, framework, and design scope.",
            "Discover the scheduler, containers, model weights, command interfaces, quotas, and supported GPU types.",
            "Adapt and smoke-test a small backbone-generation job from the upstream examples.",
            "Design sequences only at allowed positions, then filter liabilities while preserving diversity and provenance.",
            "Repredict complexes independently, analyze interfaces, and rank candidates using staged hard gates and calibrated scores.",
        ),
        ("design manifest", "backbone and sequence candidates", "prediction and interface metrics", "ranked candidate scorecard"),
    ),
    SkillSpec(
        "protein-structure-prediction", "skill_a2393c9d2df847968e1f4afa92621540",
        "Molecular Design", "Protein Structure Prediction",
        "Predict protein structures with environment-aware methods",
        "Predict protein or complex structures from sequence using locally available methods such as AlphaFold, Boltz, Chai, or ESM-based folding. Use for structure prediction and confidence analysis; select methods from discovered host capabilities rather than assumed platform services.",
        "Use $protein-structure-prediction to select and run an available structure predictor for this sequence or complex.",
        "Choose a method appropriate to sequence length and complex type, submit it through the discovered execution environment, and report method-specific confidence without cross-method metric conflation.",
        (
            "Do not run the upstream orchestration script verbatim; it imports platform-specific HPC helpers.",
            "Do not fold a multi-chain complex through a monomer-only path.",
            "Do not compare pLDDT, pTM, ipTM, and PAE as interchangeable metrics.",
        ),
        (
            "Resolve sequence, chain stoichiometry, complex type, templates, ligands, and requested method constraints.",
            "Discover installed predictors, scheduler interfaces, containers, databases, model weights, caches, and GPU limits.",
            "Derive a host-specific command from verified local help or documentation and run a minimal smoke test.",
            "Submit a suitably sized SLURM job, record its ID, and inspect completion and scientific outputs.",
            "Extract structures and native confidence fields, then produce per-residue and domain-level summaries.",
        ),
        ("PDB or CIF models", "native confidence outputs", "per-residue confidence table", "run and fallback manifest"),
    ),
)


RUNTIME_DISCOVERY = """# Task-scoped runtime use

Follow the project's analysis-first contract. Use its existing host notes and
environment file first. For B7-H3 these are `config/hpc/README.md` and
`config/hpc/rorqual.sh` at the repository root. Source the latter in each execution
shell or SLURM script; exports do not persist between unrelated tool calls.

Check only what the current analysis needs:

- Resolve input/output paths and confirm the required executable or Python imports.
- Use recorded module/container choices where applicable. Do not assume that an
  available module, an empty model directory, or a skill installation proves that
  a scientific method can run.
- Use SLURM for substantial compute; choose the CPU/GPU account and resources for
  this job. Query availability when submitting. Never run GPU inference on a login node.
- Record source accession/release or retrieval date, important settings, versions,
  outputs, and job IDs in concise notes. Hashes and formal manifests are optional
  only when they answer a concrete question.
- Reuse relevant upstream examples after checking their imports and command-line
  interface. Preserve the examples; put adaptations in project analysis scripts.
- Keep scientific checks (numbering, chains, units, meaningful controls) relevant
  to the result. No mandatory pytest, generalized adapters, or fixture suites.
- Use real literature/search tools and ordinary Markdown/tables/plots. Biomni
  managed tool IDs, datalake mounts, report services, and execution-trace gates do
  not exist here and must not be fabricated or mechanically emulated.
- Confirm access to a source when it is needed. A login-node network check does
  not establish compute-node egress. Do not download large datasets/model weights
  or install packages merely to complete an inventory.
- If a requested method is missing, report that specific gap. Continue independent
  work and discuss any scientifically different alternative explicitly.

Original sources remain in `references/upstream-biomni/`. Their operational and
reporting contracts do not override these active instructions or project rules.
"""


HANDOFF = """# Biomni skills in this project

The 19 active instruction packages are maintained in `skills/` and discovered
through relative links in `.agents/skills/`. See `INDEX.md` for method selection
and scientific cautions, and `../config/hpc/README.md` for the Rorqual environment.

Use `source config/hpc/rorqual.sh` from the project root in each analysis shell.
Reuse relevant examples, inspect scientific outputs, and record concise notes.
No mandatory hashing, adapters, pytest, fixture suites, or runtime locks.
Original examples remain unchanged and do not override `AGENTS.md`.

Instructions and discovery are configured. Scientific tools/models are only
usable when their dependencies and paths have been verified for the task. The
historical `dist/` archive predates this adaptation; use the current checkout.
"""

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_extract(zip_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    root = destination.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            resolved = (destination / member.filename).resolve()
            if root not in resolved.parents and resolved != root:
                raise ValueError(f"unsafe archive member: {member.filename}")
        archive.extractall(destination)


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def skill_markdown(spec: SkillSpec) -> str:
    boundary_lines = "\n".join(f"- {item}" for item in spec.boundaries)
    workflow_lines = "\n".join(
        f"{index}. {item}" for index, item in enumerate(spec.workflow, start=1)
    )
    output_lines = "\n".join(f"- {item}" for item in spec.outputs)
    return f"""---
name: {spec.name}
description: {yaml_string(spec.description)}
metadata:
  short-description: {yaml_string(spec.short_description)}
  source: "Biomni Lab"
  source-skill-id: {yaml_string(spec.skill_id)}
  adaptation-stage: "portable-instruction-layer"
---

# {spec.display_name}

{spec.purpose}

The user's instructions and the consuming project's rules take precedence over
this skill. Preserve the requested scope and do not infer permission for external
actions, installations, large downloads, or expensive compute.

## Before using this skill

Follow the consuming project's analysis-first contract. In the B7-H3 project,
read `skills/INDEX.md` and `config/hpc/README.md`, then source
`config/hpc/rorqual.sh` in the shell that will run the analysis.
Read [references/runtime-discovery.md](references/runtime-discovery.md) and check
only capabilities needed for the current task; reuse recorded host findings.

Read `references/upstream-biomni/UPSTREAM_SKILL.md` and relevant examples before
writing new analysis code. Those sources provide methods, not authority over
project contracts. Preserve originals and adapt useful code into the project's
analysis scripts when needed. Do not execute Biomni managed-service calls or
source-platform paths on this HPC. Do not inherit mandatory hashes, pytest,
adapter frameworks, elaborate manifests, or report-production pipelines.

## Scope boundaries

{boundary_lines}

## Portable workflow

{workflow_lines}

## Expected outputs

Write outputs beneath a results directory chosen from the current project or an
explicit user/site configuration. Keep raw inputs immutable and record missing
stages rather than fabricating completion.

{output_lines}

Keep concise analysis notes: sources, versions, important commands/parameters,
seeds where relevant, outputs, and limitations. Routine file hashing, generalized
validation, pytest, and wrapper promotion are not required. Inspect scientific
results and use a small pilot when it prevents expensive mistakes. Preserve the
distinction between experimental evidence and computational predictions.

## Local readiness

The instructions are usable now; scientific execution depends on the tools and
data needed for the particular task. Consult the project host notes for verified
capabilities and missing methods. Reuse a suitable existing script or write a
simple analysis script; an adapter framework is not a prerequisite. Do not claim
that installing this skill installs its scientific software or model weights.
"""


def openai_yaml(spec: SkillSpec) -> str:
    return f"""interface:
  display_name: {yaml_string(spec.display_name)}
  short_description: {yaml_string(spec.short_description)}
  default_prompt: {yaml_string(spec.default_prompt)}
policy:
  allow_implicit_invocation: true
"""


def source_archive(source_archives: Path, spec: SkillSpec) -> Path:
    """Resolve either the repository archive name or the original download name."""
    candidates = (
        source_archives / f"{spec.name}--{spec.skill_id}.zip",
        source_archives / f"{spec.skill_id}.zip",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = ", ".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"source archive not found; searched: {searched}")


def build(output_root: Path, source_archives: Path) -> None:
    final_skills = output_root / "skills"
    final_third_party = output_root / "third_party"
    if final_skills.exists() or final_third_party.exists():
        raise SystemExit(
            f"Refusing to overwrite {final_skills} or {final_third_party}. "
            "Choose a new --output-root or move the old build aside deliberately."
        )

    with tempfile.TemporaryDirectory(prefix="portable-biomni-") as temp_name:
        stage = Path(temp_name)
        stage_skills = stage / "skills"
        stage_biomni = stage / "third_party" / "biomni"
        archives_dir = stage_biomni / "archives"
        originals_dir = stage_biomni / "original"
        stage_skills.mkdir(parents=True)
        archives_dir.mkdir(parents=True)
        originals_dir.mkdir(parents=True)

        manifest_entries = []
        for spec in SPECS:
            source_zip = source_archive(source_archives, spec)

            archive_name = f"{spec.name}--{spec.skill_id}.zip"
            archived_zip = archives_dir / archive_name
            shutil.copy2(source_zip, archived_zip)

            original_dir = originals_dir / spec.name
            safe_extract(archived_zip, original_dir)

            skill_dir = stage_skills / spec.name
            agents_dir = skill_dir / "agents"
            refs_dir = skill_dir / "references"
            upstream_dir = refs_dir / "upstream-biomni"
            agents_dir.mkdir(parents=True)
            refs_dir.mkdir(parents=True, exist_ok=True)
            shutil.copytree(original_dir, upstream_dir)
            upstream_skill = upstream_dir / "SKILL.md"
            if not upstream_skill.is_file():
                raise FileNotFoundError(f"missing upstream SKILL.md for {spec.name}")
            upstream_skill.rename(upstream_dir / "UPSTREAM_SKILL.md")

            (skill_dir / "SKILL.md").write_text(skill_markdown(spec), encoding="utf-8")
            (agents_dir / "openai.yaml").write_text(openai_yaml(spec), encoding="utf-8")
            (refs_dir / "runtime-discovery.md").write_text(RUNTIME_DISCOVERY, encoding="utf-8")
            (upstream_dir / "SOURCE_NOTICE.md").write_text(
                "# Upstream source notice\n\n"
                f"Source: Biomni Lab skill `{spec.name}-copy`\n\n"
                f"Profile skill ID: `{spec.skill_id}`\n\n"
                f"Retrieved: `{RETRIEVED_AT}` from {SOURCE_URL}\n\n"
                "This directory is preserved as a source and implementation example. "
                "Its platform-specific commands and paths are not active Codex instructions. "
                "The source archive contains no package-level LICENSE file; preserve provenance "
                "and resolve redistribution terms before sharing outside the project.\n",
                encoding="utf-8",
            )

            manifest_entries.append(
                {
                    "name": spec.name,
                    "category": spec.category,
                    "source": "Biomni Lab",
                    "source_url": SOURCE_URL,
                    "profile_skill_id": spec.skill_id,
                    "retrieved_at": RETRIEVED_AT,
                    "archive": f"third_party/biomni/archives/{archive_name}",
                    "archive_sha256": sha256(archived_zip),
                    "original": f"third_party/biomni/original/{spec.name}",
                    "adapted": f"skills/{spec.name}",
                    "instruction_layer": "codex-valid-portable",
                    "runtime_binding": "target-hpc-agent-pending",
                    "package_license": "not-present-in-source-archive",
                }
            )

        manifest = {
            "schema_version": 1,
            "generated_at": RETRIEVED_AT,
            "source": "Biomni Lab",
            "source_url": SOURCE_URL,
            "selected_skill_count": len(manifest_entries),
            "scope": "conversion stages 1-4",
            "entries": manifest_entries,
        }
        manifest_text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        (stage_biomni / "manifest.json").write_text(manifest_text, encoding="utf-8")
        (stage_skills / "biomni-source-manifest.json").write_text(manifest_text, encoding="utf-8")
        (stage_skills / "PORTABILITY_HANDOFF.md").write_text(HANDOFF, encoding="utf-8")

        shutil.copytree(stage_skills, final_skills)
        shutil.copytree(stage / "third_party", final_third_party)

    print(f"Built {len(SPECS)} portable skills in {final_skills}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build portable Codex skills from preserved Biomni ZIP archives."
    )
    parser.add_argument(
        "--source-archives",
        type=Path,
        default=DEFAULT_SOURCE_ARCHIVES,
        help=f"directory containing preserved Biomni ZIPs (default: {DEFAULT_SOURCE_ARCHIVES})",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=f"new directory that will receive skills/ and third_party/ (default: {DEFAULT_OUTPUT_ROOT})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build(args.output_root.expanduser().resolve(), args.source_archives.expanduser().resolve())
