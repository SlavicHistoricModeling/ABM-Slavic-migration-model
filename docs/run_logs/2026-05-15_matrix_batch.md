# Matrix batch 1 — durable record (POST-FIX, canonical)

> Per-run trajectory tables for the matrix batch 1 runs, re-run on
> post-determinism-fix code (commit `66f1d6b`), 10 runs per
> scenario, seed 42. The `results_<scenario>_matrix.txt` files
> in the repo root are gitignored (overwritten by subsequent runs);
> this log is the tracked, immutable record.
>
> Headline numbers / prose framing live in
> [`2026-05-15_session_summary_for_prose.md`](2026-05-15_session_summary_for_prose.md) §6.
>
> **Note on the version history of this document:** an earlier
> version of this log was written against the pre-fix matrix
> numbers (commit `acd3ae3`, with the inherited set-iteration
> non-determinism bug at line 331). Once that bug was diagnosed
> and fixed in `66f1d6b`, the matrix was re-run as part of the
> `scripts/rerun_all_postfix.sh` cascade and this log was
> rewritten with the canonical post-fix numbers. See
> [`2026-05-15_determinism_fix.md`](2026-05-15_determinism_fix.md)
> for the bug story.

## Provenance

- Code: `slavic_migration_submited_v1.py` at commit `66f1d6b`
  (post-determinism-fix; includes the `sorted(set(...))` fix at
  line 331 plus the batch-2 CLI flags
  `--substrate_fraction` and `--non_slavic_plague_mortality`).
- Random seed: 42 (uniform across all six runs).
- Number of runs per scenario: 10.
- Output file naming: `results_<scenario>_matrix.txt` (or
  `results_<scenario>_<variant>_matrix.txt` for the two
  counterfactual runs).
- Captured here at: 2026-05-16 (post-cascade).

## Headline shifts vs pre-fix matrix

| scenario | pre-fix (acd3ae3) | post-fix (66f1d6b) | Δ |
|---|---|---|---|
| slavic1 | 18.35 % | **18.35 %** | 0 (exact — coincidence) |
| slavic2 | 49.24 % | **47.93 %** | −1.31 pp |
| slavic3 | 95.82 % | **93.99 %** | −1.83 pp |
| arabic  | 35.95 % | **35.95 %** | 0 (exact — Arabic has reverse_assim_rate = 0; bug never fired) |
| slavic3 + uniform mortality | 94.31 % | **93.96 %** | −0.35 pp |
| arabic + rule off | 41.51 % | **41.51 %** | 0 (exact — same reason as arabic) |

The differential plague-mortality contribution to slavic3
(slavic3 minus slavic3-uniformmort) is now **0.03 pp** (93.99 %
− 93.96 %) — down from the pre-fix 1.51 pp. The headline
finding is *stronger* post-fix: differential plague mortality
contributes essentially nothing to slavic3 dominance. **Migration
size is the only load-bearing parameter.**

## slavic1 — archaeologically-plausible migration

```
Scenario: slavic1 | Runs: 10 | Substrate: False | Birth Vary: +/-0.0% | migration_override: None | no_plague: False | uniform_mortality: False | inheritance_age_max: None | substrate_fraction: None | non_slavic_plague_mortality: None | seed: 42
Avg Final Proportion: 18.35% (+/-4.40%)
Population checkpoints (year_offset: mean [min..max]):
  year   0:    4480  [ 4454.. 4499]
  year  25:    3856  [ 3563.. 3989]
  year  50:    4100  [ 3711.. 4345]
  year 100:    4854  [ 4116.. 5322]
  year 150:    5011  [ 3996.. 5595]
  year 200:    5226  [ 4100.. 6160]
  year 260:    5344  [ 4058.. 6548]
Slavic-share checkpoints (year_offset: mean +/- SD):
  year   0: 11.11% +/- 0.17%
  year  25: 16.39% +/- 0.82%
  year  50: 17.70% +/- 1.08%
  year 100: 20.04% +/- 2.15%
  year 150: 16.63% +/- 2.48%
  year 200: 17.00% +/- 3.01%
  year 260: 18.35% +/- 4.40%
```

**Prose-ready summary:** at ~1 M migrants (10 / yr × 100 yr), the
model lands at **18.35 % ± 4.40 %** — statistically indistinguishable
from the **19.72 % ± 4.98 %** zero-migration / with-plague baseline.
Population trajectory dips to ~3,856 at year 25 (post-plague
depression), recovers to ~5,344 by year 260 (within ±10 % of
initial 5,000). The Slavic share plateaus around 17–20 % from year
50 onward and never approaches dominance.

**Key prose number:** *migration at archaeologically-plausible
scale produces no net Slavic linguistic effect in the model*
(slavic1 within sampling error of zero-migration baseline). The
single strongest finding in the paper.

## slavic2 — 3 × plausible migration

```
Scenario: slavic2 | Runs: 10 | Substrate: False | Birth Vary: +/-0.0% | ... | seed: 42
Avg Final Proportion: 47.93% (+/-4.96%)
Population checkpoints (year_offset: mean [min..max]):
  year   0:    4505  [ 4476.. 4521]
  year  25:    4406  [ 4316.. 4548]
  year  50:    5036  [ 4892.. 5269]
  year 100:    7286  [ 6804.. 7872]
  year 150:    7975  [ 7197.. 8753]
  year 200:    8915  [ 8013.. 9740]
  year 260:   10463  [ 9296..11505]
```

(Full Slavic-share trajectory recorded in
`results_slavic2_matrix.txt` post-cascade.)

**Prose-ready summary:** at ~3 M migrants (30 / yr × 100 yr, 3 ×
the upper archaeological envelope), the model lands at
**47.93 % ± 4.96 %**. Population doubles to ~10,500 by year 260.
The Slavic share reaches parity but not dominance — the
historical ~80 %+ outcome is nowhere near reachable.

**Key prose number:** *even at three times the archaeologically-
defensible migration rate, demographics reach parity (48 %),
not dominance.*

## slavic3 — extreme migration (the "implausible" arm)

```
Scenario: slavic3 | Runs: 10 | Substrate: False | Birth Vary: +/-0.0% | ... | seed: 42
Avg Final Proportion: 93.99% (+/-1.69%)
Population checkpoints (year_offset: mean [min..max]):
  year   0:    4342  [ 4307.. 4390]
  year  25:    4543  [ 4416.. 4655]
  year  50:    5694  [ 5503.. 5947]
  year 100:    9863  [ 9276..10498]
  year 150:   13202  [12164..14478]
  year 200:   18920  [17310..21167]
  year 260:   29846  [27070..33707]
```

**Prose-ready summary:** at ~5 M migrants (50 / yr × 100 yr,
doubling the pre-migration Balkan population), the model lands at
**93.99 % ± 1.69 %** — Slavic dominance is reached. Population
grows to ~30,000 by year 260 (6 × initial), reflecting the
implausibility of the scenario in pure demographic terms. The
migration size itself is the implausible quantity.

**Key prose number:** *dominance is reached, but only at a
migration scale (5 M against 5 M starting population) outside
any archaeological or logistical envelope (Curta 2001 caps total
Slavic migrants at < 2 M).*

## slavic3 uniform mortality — differential-isolation counterfactual

```
Scenario: slavic3 | Runs: 10 | Substrate: False | uniform_mortality: True | ... | seed: 42
Avg Final Proportion: 93.96% (+/-1.50%)
```

(Full trajectory in `results_slavic3_uniformmort_matrix.txt`.)

**Prose-ready summary:** at slavic3's migration scale, with the
Slavic group taking the **same** plague mortality as non-Slavic
(no differential), the model lands at **93.96 % ± 1.50 %**. The
**differential plague mortality contributes only 0.03 pp** to the
slavic3 result (93.99 → 93.96) — essentially zero. The migration
size and assimilation dynamics deliver dominance regardless of
the plague differential.

**Key prose number:** *the differential plague mortality is **not**
load-bearing for slavic3 dominance — the migration size itself
does all the work. The paper's negative-result claim therefore
does not depend on either side of the Mordechai-vs-plague-
maximalist debate.* (Even stronger post-fix than the originally-
predicted 1.5 pp contribution.)

## arabic — calibration / measurement run

```
Scenario: arabic | Runs: 10 | Substrate: False | ... | seed: 42
Avg Final Proportion: 35.95% (+/-2.18%)
Population checkpoints (year_offset: mean [min..max]):
  year   0:    4511  [ 4472.. 4535]
  year  25:    4408  [ 4304.. 4538]
  year  50:    4760  [ 4589.. 5017]
  year 100:    5535  [ 5289.. 5859]
  year 150:    5881  [ 5439.. 6314]
  year 200:    6027  [ 5660.. 6515]
  year 260:    6027  [ 5660.. 6515]  (year 170 used for Arabic)
```

**Prose-ready summary:** on a balanced engine with calibrated
literature inputs, the Arabic case lands at **35.95 % ± 2.18 %**
at year 170. The historical Arabic share is ~55 %. The **~19 pp
gap** is an *upper bound* on the combined contribution of
mechanisms the ABM does not model: institutional reinforcement
(Kennedy 2007; Versteegh 2014) AND bilingual transitional states
(Kandler 2010). The two cannot be separated without the
bilingualism workstream (queued, not on critical path).

**Key prose number:** *the ~15-19 pp Arabic gap is the upper bound
on combined non-demographic contributions, not "the institutional
premium" alone.* (Per `response4.md`; avoid the premature framing.)

## arabic rule-off — INHERITANCE_AGE_MAX = 99

```
Scenario: arabic | Runs: 10 | Substrate: False | inheritance_age_max: 99 | ... | seed: 42
Avg Final Proportion: 41.51% (+/-3.20%)
```

**Prose-ready summary:** Arabic with the mother-tongue rule
effectively disabled (`INHERITANCE_AGE_MAX = 99`) lands at
**41.51 % ± 3.20 %** at year 170. This is a bit-for-bit replication
of the H1 diagnostic at commit `aeedfb2` (same seed,
`docs/run_logs/2026-05-15_arabic_h1_diagnostic.md`) — confirms run
reproducibility for *this* scenario.

**Key prose number:** *the mother-tongue rule contributes
+5.56 pp on the Arabic side (41.51 % rule-off − 35.95 % rule-on);
the remaining ~13.5 pp gap vs. ~55 % historical is the combined
non-demographic ceiling.*

## Headline table (cross-reference for prose drafting)

| scenario | migrants | final Slavic share | gloss |
|---|---|---|---|
| slavic1 | ~1 M (archaeologically plausible) | **18.35 % ± 4.40 %** | Indistinguishable from zero-migration baseline (19.72 % ± 4.98 %). |
| slavic2 | ~3 M (3× plausible) | **47.93 % ± 4.96 %** | Parity, not dominance. |
| slavic3 | ~5 M (population-doubling, implausible) | **93.99 % ± 1.69 %** | Dominance reached, but at outside-envelope migration scale. |
| slavic3 + uniform mortality | as slavic3, no plague differential | **93.96 % ± 1.50 %** | Differential mortality contributes only **0.03 pp**. |
| arabic | ~1 M | **35.95 % ± 2.18 %** | ~19 pp short of ~55 % historical = upper bound on combined institutional + bilingual contributions. |
| arabic + rule off | as arabic, `INHERITANCE_AGE_MAX = 99` | **41.51 % ± 3.20 %** | Mother-tongue rule contributes +5.56 pp on Arabic side. |

## Determinism reproducibility — exact cross-checks

All four cross-checks of matrix-at-default vs. plague-sweep-at-
default-mortality value pass exactly post-fix (they didn't all
pass pre-fix, which was how the bug was found):

| scenario | matrix (default) | plague sweep (flag = default value) | match? |
|---|---|---|---|
| slavic1 (0.15) | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ EXACT |
| slavic2 (0.15) | 47.93 % ± 4.96 % | 47.93 % ± 4.96 % | ✓ EXACT |
| slavic3 (0.20) | 93.99 % ± 1.69 % | 93.99 % ± 1.69 % | ✓ EXACT |
| arabic  (0.12) | 35.95 % ± 2.18 % | 35.95 % ± 2.18 % | ✓ EXACT |

Reproducibility is restored. A reviewer running the code at
seed 42 with the fix in place gets identical numbers to those
recorded above.

## Cascade trace

The matrix re-run was Phase 1 of the four-phase
`scripts/rerun_all_postfix.sh` cascade, completed on 2026-05-16:

| phase | runs | wall time |
|---|---|---|
| 1: Matrix batch 1 (this log) | 6 | 42 min |
| 2: Plague-mortality sweep | 16 | 96 min |
| 3: Substrate response curve | 18 | 179 min |
| 4: INHERITANCE_AGE_MAX sweep | 12 | (incl. ~6 hrs system suspension) |

Total compute: ~6.5 hours actual + ~6 hours suspension. The
substrate response curve and inheritance sweep durable records
are at `2026-05-16_substrate_curve.md` and
`2026-05-16_inheritance_sweep.md` respectively.
