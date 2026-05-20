# Slavic Migration ABM — Replication Package

This repository contains the agent-based model, sweep scripts, and canonical
run-log artefacts accompanying the paper:

**Trajkov, S.** "*[Paper title — TBD on acceptance]*." *Journal of Artificial Societies and Social Simulation*, 2026 (in submission).

The model is a demographic agent-based model in the Kandler family
([Kandler 2009](https://doi.org/10.1353/hub.0.0058); [Kandler & Steele 2008](https://www.jstor.org/stable/29639579)),
applied to the case of Slavic linguistic expansion in the early-medieval
Balkans (c. 600–860 CE) and calibrated against the documented Arabic
expansion (c. 630–800 CE). The paper reports a model-behaviour
characterisation across the joint space of migration rate, substrate
fraction, reverse-assimilation rate, plague mortality, mother-tongue
cutoff, and migration window, together with a systematic verification of
an inherited published implementation.

## Citing this work

If you use this code or its outputs, please cite the paper above and the
archived release of this repository:

- Paper: [DOI when assigned]
- Code archive: [Zenodo DOI to be added after first release]

A [`CITATION.cff`](CITATION.cff) file is provided at the repository root
for citation managers.

## Engine-frozen commit

All results in the paper are produced by the engine at commit **`37054ac`**,
with random seed **42** and ten runs per parameter combination, on
Python 3.13.x on x86-64. No model code has changed since this commit. The
[reproducibility document](REPRODUCIBILITY.md) documents five inherited
implementation defects identified and corrected before this commit, and
the clean-room cross-process verification of the corrected engine.

## Reproducing the headline numbers

From a fresh clone:

```bash
git clone <REPO_URL>
cd <repo>

# (recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate            # Linux / macOS
# .venv\Scripts\activate              # Windows PowerShell
pip install -r requirements.txt

# Reproduce the Slavic 1 matrix entry (the paper's most-cited number).
python slavic_migration_submited_v1.py --scenario slavic1 --num_runs 10 --seed 42
```

Expected output (final line of `results_slavic1.txt`):

```
Avg Final Proportion: 18.35% (+/-4.40%)
```

This number matches the Slavic 1 row of Table 1 in
[`docs/paper/results_tables.md`](docs/paper/results_tables.md) and the
canonical record in
[`docs/run_logs/2026-05-15_matrix_batch.md`](docs/run_logs/2026-05-15_matrix_batch.md).
Cross-process bit-identical reproduction across `PYTHONHASHSEED` values is
verified at
[`docs/run_logs/2026-05-16_cleanroom_repro.md`](docs/run_logs/2026-05-16_cleanroom_repro.md).

## Reproducing the full sweep matrix

The full sweep matrix that produced the paper's Tables 1–5 and Figures 1–4
can be reproduced by the four-phase cascade script:

```bash
bash scripts/rerun_all_postfix.sh
```

Total wall-time: approximately 6–8 hours on a single-core x86-64 host (the
slavic3 scenarios dominate; sub-second cascade overhead). The cascade
runs matrix → plague-mortality sweep → substrate response surface →
INHERITANCE_AGE_MAX sweep in order; per-cell results are written to
`results_*.txt` at the repository root. The two additional sensitivity
sweeps reported in the paper are:

```bash
bash scripts/run_substrate_revassim_sweep.sh   # substrate × reverse-assim 2D grid (~2.5 hours)
bash scripts/run_low_rev_threshold_sweep.sh    # low-rev × window threshold sweep (~3–5 hours)
```

## Regenerating the figures

The four figures in the paper are regenerated from the canonical
per-cell results files (which are committed at the repository root) by:

```bash
python docs/paper/figures/fig1_matrix_timeseries.py
python docs/paper/figures/fig2_substrate_curve.py
python docs/paper/figures/fig3_plague_sweep.py
python docs/paper/figures/fig4_null_verdict.py
```

Each script reads only from canonical artefacts and makes no
simulation calls. Output is written as both PDF and PNG to
`docs/paper/figures/`.

## Repository structure

```
.
├── README.md                       this file
├── MODEL_DESCRIPTION.md            ODD-protocol description of the engine
├── REPRODUCIBILITY.md              audit trail; five inherited defects and their fixes
├── DECISIONS_PUBLIC.md             public-facing decisions log
├── LICENSE                         MIT
├── CITATION.cff                    citation file
├── requirements.txt                Python dependencies (numpy, matplotlib)
├── .gitignore
├── slavic_migration_submited_v1.py the engine (frozen at commit 37054ac)
├── scripts/                        sweep scripts (run_*.sh)
├── results_*.txt                   ~150 canonical per-cell run artefacts
└── docs/
    ├── run_logs/                   per-sweep durable records
    └── paper/                      paper-ready prose + figures
        ├── ODD_protocol.md
        ├── parameter_table.md
        ├── olalde_audit.md
        ├── results_tables.md
        └── figures/
            ├── captions.md
            ├── fig1_matrix_timeseries.{pdf,png,py}
            ├── fig2_substrate_curve.{pdf,png,py}
            ├── fig3_plague_sweep.{pdf,png,py}
            └── fig4_null_verdict.{pdf,png,py}
```

## License

This work is released under the [MIT License](LICENSE).
