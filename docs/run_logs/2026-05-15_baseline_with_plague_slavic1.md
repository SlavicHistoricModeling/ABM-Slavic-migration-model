# Run log — 2026-05-15_baseline_with_plague_slavic1

> Mandatory pre-flight baseline #1 of 2, **post geometric-age-init fix**.
> **VERDICT: needs your call.** Engine itself is clean (companion no-
> plague run holds within ±8 %), but the with-plague mean settles at
> **−27 %** of 5,000 and stays there for 260 yr — outside the ±20 %
> fence. Worst single run: −38 %. See §7 for the read on whether this
> is a model failure or an honest plague signature.

## 1. Provenance

| field           | value                                                       |
|-----------------|-------------------------------------------------------------|
| Date (UTC)      | 2026-05-15                                                  |
| Code commit     | `ad8cd05`                                                   |
| Branch          | `main`                                                      |
| Working tree    | clean at launch                                             |
| Script          | `slavic_migration_submited_v1.py`                           |
| Python          | local CPython (host: Windows 11)                            |

## 2. What this run was for

Re-run of the with-plague baseline after fixing initial age distribution
(commit `ad8cd05`). The previous version (`183f30f`) hid plague damage
behind a +24 % uniform-init transient — it ended at −16 % only because
the engine was drifting up at the same time the plague was knocking it
down. This run shows the plague signature on a balanced engine.

## 3. Command

```
python slavic_migration_submited_v1.py \
    --scenario slavic1 \
    --num_runs 5 \
    --seed 42 \
    --migration_override 0
```

## 4. Parameters that diverge from defaults

Identical to the previous with-plague log (see
`2026-05-14_baseline_with_plague_slavic1.md` §4). Only difference is
the agent-init fix in `ad8cd05`.

## 5. Population trajectory (engine health)

| year offset | mean pop | min..max     | drift vs 5,000 |
|-------------|----------|--------------|----------------|
| year 0      | 4,465    | 4,441..4,483 | −10.7 % (post first plague) |
| year 25     | 3,607    | 3,517..3,664 | **−27.9 %**    |
| year 50     | 3,619    | 3,422..3,684 | **−27.6 %**    |
| year 100    | 3,669    | 3,339..3,847 | **−26.6 %**    |
| year 150    | 3,646    | 3,162..3,865 | **−27.1 %**    |
| year 200    | 3,689    | 3,104..3,946 | **−26.2 %**    |
| year 260    | 3,638    | 3,106..3,957 | **−27.2 %**    |

**Baseline check status (with-plague):**
- `[X]` Mean breaches the ±20 % fence at every checkpoint from year 25
  onward and never recovers.
- `[X]` Worst single-run trajectory: 3,104 at year 200 = −38 %.
- This is *not* engine drift. It is a stable depressed equilibrium.
  After three plague years (0, 10, 25) at 15 % non-Slavic / 4 % Slavic
  mortality, the population sits ~27 % below the seed for the entire
  remaining 235 yr, because base fertility is calibrated to balance
  base mortality (`CBR_NON_SLAVIC = BASE_MORTALITY = 0.020`) — there
  is no surplus growth to recover from a shock.

### Delta vs previous run (commit `183f30f`, uniform-init)

| year | uniform-init pop | geometric-init pop | difference |
|------|------------------|--------------------|------------|
| 0    | 4,487            | 4,465              | −22        |
| 25   | 3,788            | 3,607              | −181       |
| 50   | 3,858            | 3,619              | −239       |
| 100  | 3,967            | 3,669              | −298       |
| 150  | 4,053            | 3,646              | −407       |
| 200  | 4,060            | 3,689              | −371       |
| 260  | 4,204            | 3,638              | −566       |

The whole trajectory shifted down by ~5–10 percentage points. Year 0
(post first plague tick) is barely changed; the gap opens up over
time as the missing intrinsic upward transient stops papering over
plague damage. This *is* the picture you'd expect once the engine is
balanced.

## 6. Headline numbers

| metric                                       | value (mean ± SD)    |
|----------------------------------------------|----------------------|
| Slavic linguistic proportion at end          | **19.72 % ± 4.98 %** |
| Slavic at year 260, run-by-run               | 25.9 %, 21.6 %, 21.5 %, 16.5 %, 13.1 % |
| Number of runs                               | 5                    |
| Wall time                                    | 32.5 s               |

Slavic share rises from the 10 % seed to ~20 % under zero migration —
slightly higher than the pre-fix run (18.4 %) because the surviving
non-Slavic population is smaller (the ratio shifts more for the same
absolute Slavic survival). All of this is the differential plague-
mortality input talking, not a model finding.

## 7. What surprised me / what to flag for prose

This run is the diagnostic moment. Three readings, all defensible.

### Reading A — "the rule was written assuming the buggy engine"

CLAUDE.md's ±20 % fence pre-dates the calibration fixes. With the
collapse bug in place, plague + collapse + recovery happened to land
inside ±20 %. With the calibration fixes, plague alone (under a
balanced engine, with no surplus fertility) lands at −27 %.

**Implication:** the rule was implicitly conditioned on engine drift
hiding plague damage. With a clean engine the rule needs to be
loosened to something like ±35 % for the with-plague baseline, or
restated as "plague drives a stable depressed equilibrium" rather than
a fence.

This is the most honest reading and the easiest path to unblock the
matrix.

### Reading B — "fertility should be slightly above replacement"

Medieval European populations did recover from the Justinian plague
over the 7th–8th centuries. Demographers typically use post-plague
TFR ~ 1.05–1.10 × replacement to model the recovery (Russell 1987,
Benedictow 2004). We could set `CBR_NON_SLAVIC` to 0.022 instead of
0.020, which would let the system slowly re-converge toward the seed
after the plague hits.

**Implication:** the with-plague baseline would land closer to the
±20 % fence by year 260, *and* the model would match the Procopius/
Russell qualitative story (population devastated, recovers gradually).
But this is one more tuning knob and it deserves a sensitivity sweep
of its own (CBR_NON_SLAVIC ∈ {0.020, 0.021, 0.022}).

### Reading C — "the plague mortality numbers are too high"

`non_slavic_plague_mortality = 0.15` × 3 plague years compounds to
~38 % loss. Procopius's lower bound is ~25 %, upper ~50 %. We're at
the high end. Reading the literature again, 0.10–0.12 might be a more
defensible point estimate.

**Implication:** drops the plague signature from −27 % to −18 % —
inside the fence — *and* sweeps in DECISIONS.md (substrate response
curve, scenario 3 uniform-mortality counterfactual) become more
sensitive to the plague-mortality knob.

### My recommendation

**Reading A + a parameter table footnote.** The ±20 % rule was a
correctness check on the engine, and the engine is now clean. With-
plague pop-loss is a *consequence* of the plague-mortality input and
should be reported as such, not used as a fence. CLAUDE.md should be
amended to:

> "Mandatory engine baseline: --no_plague run holds within ±10 % of
> 5,000 over 260 yr. With-plague mean depression of 25–35 % is
> expected and will be reported, not gated on."

Reading B is also worth keeping in reserve as a sensitivity sweep, but
not as the calibration default — it adds a knob that itself favours
the migration-recovery framing.

## 8. Artefacts produced

- `results_slavic1.txt` (will be overwritten by the next run)
- This log file.

## 9. Next action

**Awaiting user call between Reading A, B, or C.** Until that's
resolved, the scenario matrix is still blocked per the literal
CLAUDE.md rule, even though the engine itself has cleared.
