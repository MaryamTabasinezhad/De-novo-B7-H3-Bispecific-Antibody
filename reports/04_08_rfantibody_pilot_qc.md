# RFantibody pilot output QC

Updated 2026-09-21 after completion of pilot jobs 21526509, 21526896, and
21526897. This is a format and geometry QC of scratch outputs; it is not an
affinity or activity measurement.

## Inputs and outputs

- Arm A input target crop: chain T, residues 228–274 in the RFantibody crop.
- Arm B input target crop: chain T, residues 228–310 in the RFantibody crop.
- RFdiffusion produced two backbones per arm.
- ProteinMPNN produced two sequences per backbone (four per arm).
- RF2 produced one structure per ProteinMPNN sequence (four per arm), using
  three requested recycles and deterministic seeds 101 (A) and 202 (B).

All output PDBs retained the expected H/L/T chain labels and target-chain
residue spans. The raw files are in
`/scratch/ghaedi/mab/rfantibody_pilot/` and are not copied into Git.

## RF2 confidence and interface screening

| Arm | Candidate | Best RF2 pLDDT | RF2 hotspot/interface message | Heavy-atom minimum H/L–T distance |
|---|---|---:|---|---:|
| A | `ab_1_dldesign_0` | 0.747 | interface mask present | 0.38 Å |
| A | `ab_1_dldesign_1` | 0.735 | interface mask present | 0.38 Å |
| A | `ab_0_dldesign_1` | 0.780 | interface mask present | 0.38 Å |
| A | `ab_0_dldesign_0` | 0.746 | interface mask present | 0.38 Å |
| B | `ab_1_dldesign_0` | 0.763 | no interface residues; hotspots disabled | 0.15 Å |
| B | `ab_1_dldesign_1` | 0.771 | no interface residues; hotspots disabled | 0.11 Å |
| B | `ab_0_dldesign_1` | 0.806 | no interface residues; hotspots disabled | 0.25 Å |
| B | `ab_0_dldesign_0` | 0.790 | no interface residues; hotspots disabled | 0.48 Å |

The distance screen used heavy atoms from chains H/L against chain T with the
standard PDB coordinate columns. Distances below 1 Å are physically impossible
for non-bonded antibody–antigen atoms and indicate severe steric overlap,
coordinate collapse, or an output/input-format problem. They cannot be treated
as evidence of a productive interface. RF2's explicit B-arm warning also means
that the intended hotspot-guided validation was not applied to those inputs.
The pLDDT values are model confidence outputs, not binding-affinity estimates.

## QC decision

**Pilot rejected for design ranking.** No candidate is carried forward as a
binder, and no production-scale campaign is authorized by this QC. The next
technical action is to diagnose the RFantibody input/output geometry and hotspot
encoding (including chain order, target crop preparation, and coordinate
interpretation), then rerun only a corrected representative pilot if needed.
The approved Arm A and Arm B target residues remain unchanged; this QC does not
select epitopes or antibody sequences.

## Corrected RFdiffusion-only pilot

Follow-up job `21563096` removed the previous `diffuser.T=50` override and used
the model default horizon (T=200), with one design per arm. The change did not
resolve the failure: the RFdiffusion log still reported motif RMSDs of about
24–28 Å, and the output PDBs had minimum H/L–T heavy-atom distances of 0.38 Å
(Arm A) and 0.17 Å (Arm B). Both corrected backbones therefore also fail
geometry QC. The Arm A output target is renumbered T228–T274 and Arm B to
T228–T310; this is output-local numbering, while canonical hotspot mapping is
recorded separately. No ProteinMPNN or RF2 job was launched for this follow-up.

The diffusion-horizon override was not the sole cause. The next diagnostic must
compare RFantibody's expected target/framework coordinate and motif handling with
a known-good example or revise target-crop preparation; no candidate is eligible
for sequence design yet.
