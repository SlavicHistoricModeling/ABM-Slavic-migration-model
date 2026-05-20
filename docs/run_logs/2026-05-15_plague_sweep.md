# Batch 2 — plague-mortality sensitivity sweep (POST-FIX, canonical)

> Final shares across the four-value plague-mortality sweep
> (0.10 / 0.12 / 0.15 / 0.20) for all four scenarios. Code at
> commit `66f1d6b` (post-determinism-fix), 10 runs each, seed 42.
> Re-run wall time: 96 min as part of the
> `scripts/rerun_all_postfix.sh` cascade.
>
> The pre-fix version of this sweep (run at commit `132be63`,
> before the line-331 set-determinism fix) gave slightly different
> numbers on slavic1 / slavic3 cells; the bug was diagnosed via
> this sweep's mismatch with the matrix at default values. See
> [`2026-05-15_determinism_fix.md`](2026-05-15_determinism_fix.md).
> This log records the post-fix canonical numbers.

## Provenance

- Code: `slavic_migration_submited_v1.py` at HEAD (`66f1d6b`),
  with the `sorted(set(...))` determinism fix at line 331 plus
  the `--non_slavic_plague_mortality` CLI flag. Each sweep pair
  invoked as `python ... --scenario $s --num_runs 10 --seed 42
   --non_slavic_plague_mortality $m`.
- Random seed: 42 uniformly.
- Runs per pair: 10.
- Wall time: 96 minutes (Phase 2 of the post-fix cascade).
- Sequence: 4 mortality values × 4 scenarios = 16 runs in
  for-loop order (all 0.10 first, then 0.12, etc.).

## Results

### Final Slavic share, by mortality × scenario

| `non_slavic_plague_mortality` | slavic1 | slavic2 | slavic3 | arabic |
|---|---|---|---|---|
| 0.10 | 16.38 % ± 2.84 % | 37.80 % ± 4.41 % | 86.51 % ± 3.33 % | 36.72 % ± 3.33 % |
| 0.12 | 17.07 % ± 3.00 % | 42.35 % ± 5.72 % | 90.19 % ± 1.69 % | **35.95 % ± 2.18 %** (Arabic default) |
| 0.15 | **18.35 % ± 4.40 %** (s1/s2 default) | **47.93 % ± 4.96 %** (s2 default) | 93.01 % ± 2.33 % | 37.91 % ± 3.74 % |
| 0.20 | 19.96 % ± 4.32 % | 61.11 % ± 6.75 % | **93.99 % ± 1.69 %** (s3 default) | 43.68 % ± 4.67 % |

Cells marked **(default)** correspond to the scenario's default
plague mortality from `SCENARIOS`; the rest are sweep variants.

### Cross-check vs. matrix batch 1 — all exact

| scenario | matrix (no flag) | plague sweep at default (flag = default) | match? |
|---|---|---|---|
| slavic1 (default 0.15) | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ EXACT |
| slavic2 (default 0.15) | 47.93 % ± 4.96 % | 47.93 % ± 4.96 % | ✓ EXACT |
| slavic3 (default 0.20) | 93.99 % ± 1.69 % | 93.99 % ± 1.69 % | ✓ EXACT |
| arabic (default 0.12)  | 35.95 % ± 2.18 % | 35.95 % ± 2.18 % | ✓ EXACT |

All four cross-checks pass exactly post-fix. (Pre-fix, slavic1
and slavic3 cells differed by ~1.5 pp and ~0.3 pp respectively
due to the inherited set-iteration non-determinism. That
mismatch was the symptom that led to the fix.)

## Interpretation — what the sweep tells us

### slavic1 — robust to plague-mortality assumption

The slavic1 (~1 M migrants, archaeologically plausible) Slavic
share stays **within sampling error of the zero-migration baseline
(~19.7 %)** across the full plague-mortality range tested:

- mortality 0.10: 16.38 %
- mortality 0.12: 17.07 %
- mortality 0.15: 18.35 %
- mortality 0.20: 19.96 %

Even at the Mordechai-style lower-envelope (0.10), the model is
still in baseline range. The "no net Slavic effect from
archaeologically-plausible migration" finding **does not depend on
the plague-mortality input** — it holds whether or not the
plague-maximalist literature is correct.

### slavic2 — most plague-sensitive

slavic2 (~3 M migrants) shows the largest swing across the sweep
(37.80 % → 61.11 % from mortality 0.10 → 0.20). This is the regime
where demographic dynamics start to matter most: enough migrants
for the fertility edge to compound, but not enough that the
migration size overwhelms everything else.

Even at the highest mortality (0.20), slavic2 reaches only 61 % —
still short of the historical ~80 %+ Slavic share.

### slavic3 — robust to plague-mortality assumption (in the other direction)

slavic3 (~5 M migrants) reaches near-total dominance at every
plague-mortality value tested:

- mortality 0.10: 86.51 %
- mortality 0.12: 90.19 %
- mortality 0.15: 93.01 %
- mortality 0.20: 93.99 %

This confirms the matrix-batch finding that the differential
plague mortality is **not** load-bearing for slavic3 dominance.
Even at the lowest tested plague mortality (0.10), where the
differential collapses to 0.10 − 0.04 = 0.06 (vs the default
0.20 − 0.04 = 0.16), slavic3 still delivers 87 % Slavic.

The migration *size* (50 / yr × 100 yr = 5,000 agent-migrants
on a 5,000-agent starting population, i.e. doubling the pre-
migration Balkan population) is what's load-bearing — and is
itself the implausible quantity per Curta's archaeological
upper bound of < 2 M total.

### arabic — relatively flat across the sweep

The Arabic case is less plague-sensitive because Arabic has only
2 plague years vs. 3 in Slavic scenarios, and the scenario is
shorter (170 vs. 260 years). Final shares span 36–44 % across the
sweep, well below the historical ~55 %.

The Arabic gap framing **is unchanged by the plague sweep**: even
at the highest tested mortality (0.20, beyond the Arabic default
of 0.12), demographic dynamics deliver only ~44 %, still ~11 pp
short of the historical ~55 %. The combined institutional +
bilingual upper-bound ceiling (per `response4.md`) remains in
range.

## Prose-ready summary

This sweep is the response to the standard reviewer objection
"isn't the result driven by your plague-mortality assumption,
which the Mordechai et al. (2019) literature has contested?". The
answer is **no — the slavic1 / slavic2 / slavic3 / arabic
qualitative findings are robust across the full
plague-mortality range from Mordechai-style low (0.10) to
plague-maximalist high (0.20)**:

- slavic1 stays in baseline range (16–20 %) — no net migration
  effect at any tested mortality.
- slavic2 reaches at most 61 % at the high end — never dominance.
- slavic3 reaches at least 87 % at the low end — always dominance,
  i.e. the result is migration-size-driven, not plague-driven.
- arabic remains in the 36–44 % range, well short of the
  historical ~55 % — the combined non-demographic ceiling
  framing is robust.

**One sentence for the paper:** "Across the plague-mortality
range tested (0.10–0.20), the headline findings — slavic1
indistinguishable from baseline, slavic3 reaches dominance at
implausible migration size — are robust; the paper's negative
result for the migration hypothesis therefore does not rest on
either side of the Justinianic-plague-maximalist debate
(Mordechai et al. 2019 vs. Stathakopoulos 2004)."
