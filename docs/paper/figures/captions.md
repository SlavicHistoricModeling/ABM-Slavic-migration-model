# Figure captions

> Conservative captions for the three Results-section figures.
> Locked to the §9 narrative-discipline note in the prose-instance
> briefing — describes what the figure shows, no interpretive
> lean, no overstatement. The Discussion section carries the
> interpretive weight.

## Fig 1 — Matrix batch time-series

**File:** `fig1_matrix_timeseries.{pdf,png}`
**Source:** `results_<scenario>_matrix.txt` (gitignored;
canonical record in `docs/run_logs/2026-05-15_matrix_batch.md`).
**Code commit:** `66f1d6b`.

**Caption:**

> **Figure 1.** Slavic linguistic share over the simulation
> period for the four scenarios (Slavic 1, 2, 3 spanning 600–860 CE;
> Arabic spanning 630–800 CE), means across 10 runs with ±1 SD
> bands at seven checkpoints (years 0, 25, 50, 100, 150, 200, 260
> from scenario start). Slavic 1 (≈1 M migrants over 100 years —
> within Curta's (2001) archaeological upper bound) ends at
> 18.35 % ± 4.40 %, within the sampling margin of the
> zero-migration plague baseline (19.72 % ± 4.98 %; see Methods §3.1).
> Slavic 2 (≈3 M migrants, 3× the archaeological maximum) ends at
> 47.93 % ± 4.96 %. Slavic 3 (≈5 M migrants, doubling the
> pre-migration Balkan population) ends at 93.99 % ± 1.69 %.
> Arabic (≈1 M migrants) ends at 35.95 % ± 2.18 % at year 170.
> Horizontal reference lines mark the historical Slavic (~80 %+)
> and Arabic (~55 %) shares. Random seed: 42.

## Fig 2 — Substrate response surface (parameter-conditional)

**File:** `fig2_substrate_curve.{pdf,png}`
**Source:** `results_revassim_<scenario>_sub<f>_rev<r>.txt`
(48 files, gitignored; canonical record in
`docs/run_logs/2026-05-16_substrate_revassim_sweep.md`).
**Code commit:** `37054ac` (post-substrate-init-fix); sweep
runs against a `/tmp` copy of the engine with `reverse_assim`
patched per cell.

**Caption:**

> **Figure 2.** Substrate response curve for Slavic 1 (left;
> ~1 M migrants, archaeologically plausible) and Slavic 2
> (right; ~3 M migrants, 3× the archaeological maximum) across
> four reverse-assimilation rates: 0.000 (rule disabled),
> 0.015 (Slavic 3 scenario default), 0.030 (Slavic 1 scenario
> default), 0.045 (above-default sensitivity). Substrate
> fraction varied across {0.00, 0.10, 0.20, 0.30, 0.40, 0.50};
> error bars show ±1 SD across 10 runs. The non-monotonic
> ("U-shaped") substrate response that appears at the scenario
> default reverse-assimilation rates (0.030, 0.045) does not
> persist at `reverse_assim = 0.000`, where both scenarios show
> essentially monotonic (Slavic 1) or near-saturated (Slavic 2)
> responses. The shape of the substrate response curve is
> therefore parameter-conditional on the
> `reverse_assimilation_rate`, which is a labelled free
> parameter without independent empirical grounding (see
> Methods §Parameters). Light-yellow shading marks the
> Olalde (2023) Slavic-related admixture upper-bound range
> (~30–50 %); horizontal reference line marks the historical
> ~80 %+ Slavic share. Random seed: 42.

## Fig 3 — Plague-mortality sensitivity sweep

**File:** `fig3_plague_sweep.{pdf,png}`
**Source:** `results_plague_<scenario>_<mortality>.txt` (16 files,
gitignored; canonical record in
`docs/run_logs/2026-05-15_plague_sweep.md`).
**Code commit:** `66f1d6b`.

**Caption:**

> **Figure 3.** Final Slavic share across the plague-mortality
> sensitivity sweep, four scenarios. Non-Slavic plague mortality
> varied across {0.10, 0.12, 0.15, 0.20} — bracketing the
> contested literature on Justinianic-plague mortality from the
> Mordechai et al. (2019) lower envelope (~0.10) to the
> plague-maximalist reading (~0.20). Error bars show ±1 SD across
> 10 runs. Each scenario's position across the sweep:
> Slavic 1 spans 16.38–19.96 % (no value reaches the historical
> ~80 %+ share); Slavic 2 spans 37.80–61.11 % (no value reaches
> ~80 %+); Slavic 3 spans 86.51–93.99 % (every value reaches
> dominance, including the lowest tested plague mortality);
> Arabic spans 35.95–43.68 % (no value reaches the historical
> ~55 % share). Vertical dashed lines mark each scenario's
> default plague mortality. Horizontal reference lines mark the
> historical Slavic (~80 %+) and Arabic (~55 %) shares. Random
> seed: 42.

## Fig 4 — Null-verdict figure

**File:** `fig4_null_verdict.{pdf,png}`
**Source:** `results_lowrev_slavic1_sub<s>_rev<r>_win<w>.txt`
(24 files, gitignored; canonical record in
`docs/run_logs/2026-05-17_low_rev_threshold_sweep.md`).
**Code commit:** `37054ac`; sweep runs against a `/tmp` copy of
the engine with two sed substitutions per cell
(reverse-assimilation rate; migration window).

**Caption:**

> **Figure 4.** Final Slavic share at scenario end (year 260)
> for the 24 archaeologically-admissible parameter combinations
> of the Slavic 1 scenario (≈1 M migrants, the upper bound
> Curta 2001 admits): substrate fraction ∈ {0.00, 0.30}
> (no-substrate baseline and the Olalde mid-range value),
> reverse-assimilation rate ∈ {0.000, 0.0025, 0.005, 0.0075,
> 0.010, 0.015} (the low-rate strip), and migration window ∈
> {100 yr default, 150 yr extended}. Means across 10 runs with
> ±1 SD error bars. Horizontal lines mark the historical
> Slavic ~80 %+ rural-dominance threshold (solid, red) and the
> historical Arabic ~55 % share for context (dotted, grey).
> Every admissible cell falls below the Slavic threshold. The
> maximum cell (substrate = 0.30, reverse-assim = 0.000,
> migration window = 150 yr) is labelled at 70.90 % ± 5.15 %;
> the 1-SD upper bound (76.05 %) is also below the threshold.
> Random seed: 42.

## Notes on caption discipline

- "Slavic 1 ends at 18.35 % ± 4.40 %, within the sampling margin
  of the zero-migration plague baseline" is the precise statement.
  Do **not** rewrite as "Slavic 1 produces no effect" — the latter
  overstates and is rejected by the §9 narrative discipline note.
- "Slavic 2 reaches 47.93 %" not "Slavic 2 fails to reach dominance"
  — describe what was measured, not what wasn't.
- Plague-mortality sweep caption deliberately does NOT use the
  word "robust" or "robustness". Robustness is an interpretive
  claim that belongs in Results-text, not in the figure caption.
- Scale claims ("within Curta's archaeological upper bound", "3×
  the archaeological maximum", "doubling the pre-migration
  Balkan population") are tied to the empirical-envelope work
  that Methods §Sources should establish; the captions assume
  Methods has done that work and only quote the comparison.
- Random seed and code commit are explicit in every caption — a
  reviewer running the code at the cited commit should reproduce
  the figure exactly. Per the determinism fix at `66f1d6b` and
  the verification at `docs/run_logs/2026-05-16_cleanroom_repro.md`,
  bit-identical reproduction is now possible across
  PYTHONHASHSEED values on x86-64.
