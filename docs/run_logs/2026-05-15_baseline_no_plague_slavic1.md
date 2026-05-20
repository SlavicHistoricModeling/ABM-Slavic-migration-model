# Run log — 2026-05-15_baseline_no_plague_slavic1

> Engine-sanity baseline #2 of 2, **post geometric-age-init fix**.
> **VERDICT: passes the engine check.** Drift down from +24 % to +8 %
> over 260 yr; comfortably inside the ±20 % fence. `REPRO_SHARE = 0.151`
> confirmed correct under the equilibrium age structure.

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

Re-run of the engine-sanity baseline after fixing initial age
distribution from uniform `[0, 60]` to geometric
`expovariate(BASE_MORTALITY)` (commit `ad8cd05`). The previous run at
`183f30f` drifted +24 %; this is the verification.

## 3. Command

```
python slavic_migration_submited_v1.py \
    --scenario slavic1 \
    --num_runs 5 \
    --seed 42 \
    --migration_override 0 \
    --no_plague
```

## 4. Parameters that diverge from defaults

Identical to the previous engine-sanity log (see
`2026-05-14_baseline_no_plague_slavic1.md` §4). Only difference is
the agent-init fix in `ad8cd05`.

## 5. Population trajectory (engine health)

| year offset | mean pop | min..max     | drift vs 5,000 |
|-------------|----------|--------------|----------------|
| year 0      | 4,989    | 4,967..5,001 | −0.2 %         |
| year 25     | 5,012    | 4,935..5,106 | +0.2 %         |
| year 50     | 5,066    | 5,002..5,226 | +1.3 %         |
| year 100    | 5,114    | 4,966..5,443 | +2.3 %         |
| year 150    | 5,269    | 4,986..5,716 | +5.4 %         |
| year 200    | 5,308    | 4,970..5,632 | +6.2 %         |
| year 260    | 5,407    | 5,067..5,673 | **+8.1 %**     |

**Baseline check status (no-plague):**
- `[X]` Holds within ±20 % across the full 260 yr (max drift +8.1 %).
- `[X]` Year 0 mean is 4,989 — initial agent-init now lands almost
  exactly on the seed.
- The slow remaining drift comes from a small structural bias:
  newborns escape mortality in their year of birth, which adds ~0.05 %
  to the per-year balance (compounded over 260 yr ≈ +13 % theoretical
  ceiling; observed +8 % shows the system is still well below ceiling).
  Could be neutralised by raising `REPRO_SHARE` from 0.151 to ~0.154,
  but that change is cosmetic at this scale and not worth a knob.

## 6. Headline numbers

| metric                                       | value (mean ± SD)    |
|----------------------------------------------|----------------------|
| Slavic linguistic proportion at end          | **11.84 % ± 1.31 %** |
| Slavic at year 260, run-by-run               | 11.3 %, 11.4 %, 14.2 %, 11.2 %, 11.1 % |
| Number of runs                               | 5                    |
| Wall time                                    | 63.7 s               |

Compared to the pre-fix run (`183f30f`): final Slavic was 12.59 % ± 4.06 %,
now 11.84 % ± **1.31 %**. The SD collapsed by 3× because the population
is no longer drifting — runs converge instead of fanning out.

## 7. What surprised me / what to flag for prose

- **The geometric init fix did exactly what was predicted.** No
  cliff-edge adjustments, no second knob — the math worked the first
  time. Worth noting in Methods that initial age distribution choice
  matters at this scale.
- **Run-to-run SD shrank dramatically.** With uniform init the
  trajectory variance was dominated by *when* each run hit its plague
  /transient peaks; with geometric init the runs are tightly bunched.
  This is good for headline confidence intervals.
- **Slavic share drifts ~+1.8 pp from the 10 % seed under no plague,
  no migration.** That's the residual signature of the small CBR_SLAVIC
  edge (0.021 vs CBR_NON_SLAVIC 0.020) plus the cell-pool mother-tongue
  rule. Should be quoted as "~12 % under pure baseline" in the Methods
  validation paragraph — it's the floor any scenario sits on top of.

## 8. Artefacts produced

- `results_slavic1.txt` (will be overwritten by the next run)
- This log file.

## 9. Next action

Engine clears its sanity check. Companion with-plague baseline at the
same commit `ad8cd05` is in the sister log
`2026-05-15_baseline_with_plague_slavic1.md` — and that one needs
your call.
