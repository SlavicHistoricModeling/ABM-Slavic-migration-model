# Determinism fix — set-iteration bug in reverse-assimilation rule

> 2026-05-15. Third bug discovered in the inherited canonical code
> (after the birth-rate / mother-tongue bugs flagged in CLAUDE.md
> at session start). One-line fix in
> `slavic_migration_submited_v1.py` line ~331. All batch 1 +
> batch 2 results will be re-run on the fixed code; this log
> records the diagnosis and the resulting re-run plan.

## How it was discovered

The plague-mortality sweep launched in this session against HEAD
code (commit `132be63`, with the new `--non_slavic_plague_mortality`
CLI flag) produced slightly different numbers at default mortality
than the matrix batch 1 at `acd3ae3` (no flag):

| scenario | matrix (no flag) | plague sweep (flag = default) | Δ |
|---|---|---|---|
| slavic1 | 18.35 % | 16.82 % | −1.53 pp |
| slavic2 | 49.24 % | 49.24 % | exact |
| slavic3 | 95.82 % | 95.51 % | −0.31 pp |
| arabic  | 35.95 % | 35.95 % | exact |

slavic2 and arabic reproduced exactly. slavic1 and slavic3 didn't.
A diagnostic re-ran slavic1 twice on HEAD code:

| run | command | result |
|---|---|---|
| matrix | `python ... --scenario slavic1 --seed 42` (acd3ae3) | 18.35 % ± 4.40 % |
| Test A | `python ... --scenario slavic1 --seed 42` (HEAD)   | 18.35 % ± 4.40 % |
| plague | `python ... --scenario slavic1 --seed 42 --non_slavic_plague_mortality 0.15` (HEAD) | 16.82 % ± 3.90 % |
| Test B | `python ... --scenario slavic1 --seed 42 --non_slavic_plague_mortality 0.15` (HEAD) | 18.11 % ± 3.47 % |

Two runs of the **same command** (Test B vs. plague sweep) gave
different results — genuine non-determinism, not specific to the
new CLI flag.

## The bug

Line 331 of the canonical script (reverse-assimilation rule):

```python
chlangs = [l for l in neigh_langs if GROUPS[l]["christianized"]]
if chlangs:
    a["language"] = max(set(chlangs), key=chlangs.count)
```

When a Slavic agent's neighbourhood is majority-Christianised and
the reverse-assimilation roll fires, the agent adopts the
*most-common Christianised neighbour language*. The implementation
uses `max(set(chlangs), key=chlangs.count)` — but `set(...)`
iteration order in Python depends on the hash of its elements,
and Python string hashes are randomised per-process by default
(controlled by `PYTHONHASHSEED`, unset in this environment).

When two Christianised languages tie in count (e.g. neighbourhood
has 2 Greek + 2 Germanic + 1 Illyrian, two-way tie on Greek and
Germanic with count = 2), `max()` returns the first element of the
set-iteration order encountered with the maximum key — which is
hash-randomisation-dependent.

The cascading effect: a non-deterministic reverse-assimilation
choice changes the agent's language → changes the agent's
subsequent plague-mortality and assimilation rolls → changes the
RNG state from that point onward → diverges the simulation.

## Why slavic1 / slavic3 were affected but slavic2 / arabic weren't

Affected by reverse-assimilation rate (`reverse_assimilation_rate`):

| scenario | reverse rate | observed determinism |
|---|---|---|
| slavic1 | 0.03 | non-deterministic (largest Δ ~1.5 pp) |
| slavic2 | 0.02 | reproduced exactly (small sample, low rate) |
| slavic3 | 0.015 | non-deterministic (small Δ ~0.3 pp) |
| arabic  | **0.0** | reproduced exactly (rule never fires) |

Arabic has `reverse_assimilation_rate = 0.0`, so the affected code
block (lines 328–331) **never executes** in the Arabic scenario.
Therefore Arabic is fully deterministic regardless of the bug.
This is consistent with the cross-check pattern observed.

Slavic2's exact reproduction was likely fortuitous (low reverse
rate, fewer rolls hitting tied-count cases in this particular
seed trajectory) — running the sweep more times would reveal
slavic2 to be non-deterministic too.

## The fix

```diff
-                            a["language"] = max(set(chlangs), key=chlangs.count)
+                            a["language"] = max(sorted(set(chlangs)), key=chlangs.count)
```

`sorted(set(chlangs))` produces a list in alphabetical order
(strings sort lexicographically by Python's built-in comparison,
which is **not** hash-dependent). `max()` over a sorted sequence
with `key=chlangs.count` returns the first element encountered
with the maximum count — i.e. when counts tie, the
alphabetically-earliest neighbour-language wins. This is
deterministic across processes, machines, and `PYTHONHASHSEED`
settings.

The change is one-line and semantically equivalent for the
no-tie case (any unique max is returned the same way as before).
Only the tie-resolution rule changes — from
"hash-randomised" to "alphabetical".

The tie-resolution policy itself has no methodological
justification either way (real reverse-assimilation isn't
deterministically alphabetical), but **alphabetical is
reproducible**, which is the property the paper needs. A reviewer
running the code at seed 42 now gets the same numbers.

## Re-run cascade

All batch-1 and batch-2 results in this session were computed on
the pre-fix code (with the latent non-determinism). The bug's
quantitative impact is small (~0.3–1.5 pp on individual
scenario means, within sampling-error SD) but the integrity of
"identical code + identical seed → identical numbers" is
load-bearing for a reproducibility-conscious paper.

The following are being re-run on the fixed code:

| artefact | re-run? | reason |
|---|---|---|
| Matrix batch 1 (slavic1/2/3 + arabic + slavic3-uniformmort + arabic-ruleoff) | yes | foundational; six runs, ~45 min |
| Plague-mortality sweep (16 runs) | yes | numbers may shift ~1 pp on slavic1/3 cells; ~96 min |
| Substrate response curve (18 runs) | yes | not yet completed (killed mid-run for the fix); ~4 hrs |
| INHERITANCE_AGE_MAX sweep (12 runs) | yes | not yet started; ~2.5 hrs |
| Arabic H1 diagnostic (commit `aeedfb2`) | NO | reverse rate = 0 for Arabic, so the bug doesn't fire; numbers unchanged |
| Engine baselines at `ad8cd05` (no_plague, no_migration) | NO | reverse rate doesn't fire when there's nothing to convert; numbers unchanged |

Total re-run wall time estimate: ~8 hours.

## Provenance

- Diagnosis script: `scripts/diagnose_slavic1.sh` (committed in
  `b6df007`).
- Bug fix: commit pending in this session.
- Pre-fix matrix log: `docs/run_logs/2026-05-15_matrix_batch.md`
  — to be re-issued post-rerun with the fixed numbers.
- Pre-fix plague-sweep log: `docs/run_logs/2026-05-15_plague_sweep.md`
  — to be re-issued post-rerun.
