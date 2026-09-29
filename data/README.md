# Target-data stream

Target data are organized by lifecycle within this foundational input stream:

| Order | Directory | Meaning |
|---|---|---|
| `01` | `raw/` | Retrieved structures and UniProt records preserved as inputs |
| `02` | `processed/` | Oriented/mapped target ensemble files used by later steps |

Target preparation is documented in `reports/01_01_target_preparation.md`; the durable mapping and QC records are in `metadata/` and `work/01_target_preparation/`.
