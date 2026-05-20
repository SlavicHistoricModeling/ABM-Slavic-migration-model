# Decisions log (public)

> Reverse-chronological log of the load-bearing decisions made during
> the model-behaviour reassessment of an inherited demographic ABM
> originally published in *Diachronica* (DIA-25063). This document
> records the substantive decisions — engine freeze, framing,
> methodological scope — in a form suitable for public release.
> Internal correspondence, working notes, and in-flight framing
> debates are intentionally not reproduced here; the substantive
> decisions and their rationales are captured below.

---

## 2026-05-17 — Publish the rigorous null. Model extension considered and rejected.

**Position.** The paper publishes the rigorous null. The engine
stays frozen at commit `37054ac`. No model extension. No further
sweeps. No further code.

**In plain language:**

- **The primary contribution is the negative result.** At every
  archaeologically-admissible parameter combination tested across
  the substrate × reverse-assimilation and low-rev × threshold ×
  migration-window sweeps, the demographic-ABM mechanism fails to
  produce historical Slavic rural dominance (~80 %+). The maximum
  across all admissible cells is **70.90 % ± 5.15 %** at the most
  favourable corner (Slavic 1 / substrate = 0.30 / reverse-assim
  = 0.000 / migration window = 150 yr); the 1-SD upper bound
  (76.05 %) is also below the threshold.

- **The substrate hypothesis is exhausted as a Results-level
  claim.** The substrate × reverse-assimilation adjudication
  sweep showed the substrate-curve non-monotonic shape ("U-shape")
  was mechanistically downstream of the
  `reverse_assimilation_rate` parameter, which has no independent
  empirical anchor. The low-rev / threshold sweep further showed
  that even the most-favourable substrate configuration does not
  reach the historical threshold within the admissible scale. In
  the paper, the substrate appears **only as a single fenced
  conjecture in the Discussion** — not as a Results-section
  finding.

- **The residual ~9 pp gap** between the most-favourable
  admissible cell (70.90 %) and the historical threshold (~80 %)
  is interpreted via the **Arabic-calibrated combined
  institutional + bilingual ceiling**: on the corrected engine,
  the model produces ~36 % Arabic linguistic share against the
  historical ~55 %, a ~19 pp gap that bounds the combined
  contribution of mechanisms the ABM does not implement
  (institutional reinforcement and bilingual transitional states).
  The Slavic residual fits comfortably within that ceiling.

- **Extending the model with a prestige term to reach 80 % was
  considered and rejected.** The prestige parameter is empirically
  unconstrained, the same defect that affects the
  reverse-assimilation rate. Adding it would relocate rather than
  resolve the underdetermination. A parameter-tuneable extension
  that hits the target by design is exactly the methodological
  pathology the reassessment was undertaken to expose, in a
  different costume. The null result is the honest finding; the
  extension would be reverse-engineering.

---

## 2026-05-18 — Paper framing: model-behaviour study with the historical case as motivation.

**Position.** The paper's stated subject is *the behaviour of a
Kandler-family demographic ABM across its parameter space*. The
Slavic case is the *motivating case* that supplies the parameter
ranges and the calibration target.

**Rationale.** The historical Slavic linguistic-expansion question
is the project's substantive motivation, but the model-behaviour
framing is the rigorous one. The model is verified to characterise
a regime of the Kandler family; the historical question is
addressed by interpreting that characterisation against the
empirical envelope (Curta's archaeological migration bounds;
Olalde's genetic-admixture bounds). The decision is recorded
explicitly so a future reader does not "restore" the
historical-causality framing thinking it was lost by accident.

---

## Engine-frozen state

**Commit:** `37054ac`.

**Code paths verified clean:** reproduction, mortality,
assimilation (forward and reverse), substrate initialisation,
migration accounting. Hash-order-dependent iteration replaced
with deterministic alphabetical tie-break. See
[`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) §4 for the five
inherited / found implementation defects and their corrections.

**Clean-room cross-process verification:** bit-identical at seed
42 across `PYTHONHASHSEED ∈ {0, 12345}` on x86-64. See
[`docs/run_logs/2026-05-16_cleanroom_repro.md`](docs/run_logs/2026-05-16_cleanroom_repro.md).
Cross-architecture verification (ARM, alternative CPython
implementations) is an open caveat disclosed honestly in
[`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) §6.

---

## Engine-stability baseline (frozen reference at `ad8cd05`)

- **No plague + no migration (engine stability gate, 260 yr):**
  mean final population 5,407 (+8.1 % drift from the initial
  5,000; within the ±10 % stability fence). Final Slavic share
  **11.84 % ± 1.31 %** (drift from the 10 % initial seed).
- **With plague + no migration (differential-mortality
  contribution isolated):** mean final population 3,638 (−27.2 %
  from initial). Final Slavic share **19.72 % ± 4.98 %** — zero
  migration, zero assimilation tuning, differential plague
  mortality alone roughly doubles the Slavic share (10 % → 20 %).

These reference numbers are quoted in the paper's results
section to anchor the slavic1 finding ("indistinguishable from
the zero-migration baseline at the default reverse-assim rate").

---

## What this document deliberately does not record

- Internal correspondence, working notes, in-flight framing
  debates. The substantive decisions above are the record;
  the path by which they were reached is not.
- Day-to-day implementation milestones below the level of the
  five inherited / found defects in
  [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md). The defects and
  their fixes are the publishable methodological contribution;
  the underlying commit-by-commit work history is preserved in
  the git log for any reviewer who wants it.
