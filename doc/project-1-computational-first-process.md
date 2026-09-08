# Project 1: Computational-First Design Process

Two independent B7-H3-binding antibodies are designed and optimized computationally before being combined into a biparatopic construct.

> **Important:** Before experimental measurement, this stage should be described as **in-silico affinity optimization**, not confirmed affinity maturation. High affinity remains a prediction until it is measured experimentally.

## Revised Computational-First Process

1. Prepare a glycan- and membrane-aware B7-H3 structural ensemble.
2. Select two accessible, non-overlapping epitopes: A and B.
3. Define hotspot residues for each epitope.
4. Generate antibodies against epitope A and epitope B independently using RFantibody.
5. Design CDR sequences with ProteinMPNN.
6. Predict the antibody–B7-H3 complexes using replicated AlphaFold 3 and/or RoseTTAFold2 runs.
7. Filter designs for:
   - Interface confidence
   - Hotspot contacts
   - Steric clashes
   - Binding-pose consistency
   - Structural stability
   - Humanness
   - Aggregation risk
8. Retain several structurally diverse parent antibodies for each epitope.
9. Perform in-silico affinity optimization independently for the epitope-A and epitope-B antibodies:
   - Select interface-facing CDR positions for mutation.
   - Generate single and combinatorial variants.
   - Score variants using Rosetta ΔΔG/InterfaceAnalyzer and ProteinMPNN.
   - Repredict the complexes using AlphaFold 3 and/or RoseTTAFold2.
   - Reject variants that change the intended epitope or binding pose.
10. Rank optimized antibodies using consensus scores across the B7-H3 structural ensemble.
11. Join the best epitope-A and epitope-B variants as both A–linker–B and B–linker–A constructs.
12. Optimize linker length and sequence computationally.
13. Model each fusion binding:
    - Epitope A only
    - Epitope B only
    - Epitopes A and B simultaneously
14. Add Fc computationally and model the complete **2A + 2B dimer**.
15. Filter complete constructs for:
    - Steric accessibility
    - Developability
    - Aggregation risk
    - Unwanted B7-H3 crosslinking
16. Select a diverse experimental panel rather than only the top-scoring design. Include:
    - A-only antibody
    - B-only antibody
    - Parental A+B construct
    - In-silico-optimized A+B constructs
17. Proceed to experimental expression, binding, affinity, simultaneous-binding, internalization, and functional testing.
