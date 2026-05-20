# Run log — 2026-05-14_baseline_with_plague_slavic1

> Mandatory pre-flight baseline #1 of 2 per CLAUDE.md. Numbers below are
> filled after the run completes. **Until that happens, treat this file as
> a stub** — do NOT paste it into the prose instance yet.

## 1. Provenance

| field           | value                                                       |
|-----------------|-------------------------------------------------------------|
| Date (UTC)      | 2026-05-14 (run launched ~23:30 UTC)                        |
| Code commit     | `183f30f` (post-optimisation rerun)                          |
| Branch          | `main`                                                      |
| Working tree    | clean at launch                                             |
| Script          | `slavic_migration_submited_v1.py`                           |
| Python          | local CPython (host: Windows 11)                            |

## 2. What this run was for

Mandatory pre-flight baseline per CLAUDE.md:
> *"BEFORE any full scenario run: run a no-migration, no-substrate baseline
> and confirm population stays within ±20 % of 5,000 agents over 260 years."*

This run keeps `PLAGUE_YEARS` at the slavic1 default (`[0, 10, 25]`). The
companion engine-sanity baseline with `--no_plague` follows in a separate
log; that one should hold population *nearly flat*, which is what
confirms `REPRO_SHARE = 0.151` is right.

If population drifts outside ±20 %, every scenario run is blocked until
the engine is fixed.

## 3. Command

```
python slavic_migration_submited_v1.py \
    --scenario slavic1 \
    --num_runs 5 \
    --seed 42 \
    --migration_override 0
```

## 4. Parameters that diverge from defaults

| parameter                       | scenario default | this run     |
|---------------------------------|------------------|--------------|
| `migration_rate`                | 10               | **0** (`--migration_override 0`) |
| `slavic_birth_rate` (per-female)| `per_female_rate(0.021) ≈ 0.139` | unchanged |
| `slavic_birth_rate_new`         | `per_female_rate(0.011) ≈ 0.073` | unchanged |
| `INHERITANCE_AGE_MAX`           | 25               | 25           |
| `REPRO_SHARE`                   | 0.151            | 0.151        |
| `PLAGUE_YEARS`                  | `[0, 10, 25]`    | `[0, 10, 25]`|
| `substrate`                     | False            | False        |
| `birth_vary`                    | 0.0              | 0.0          |
| `seed`                          | 42               | 42           |
| `num_runs`                      | 10               | **5** (baseline only)  |

GROUPS untouched. Substrate flag not passed.

## 5. Population trajectory (engine health)

| year offset | mean pop | min..max     | drift vs 5,000 |
|-------------|----------|--------------|----------------|
| year 0      | 4,487    | 4,445..4,565 | −10.3 %        |
| year 25     | 3,788    | 3,731..3,857 | **−24.2 %**    |
| year 50     | 3,858    | 3,779..3,932 | **−22.8 %**    |
| year 100    | 3,967    | 3,791..4,158 | **−20.7 %**    |
| year 150    | 4,053    | 3,882..4,374 | −18.9 %        |
| year 200    | 4,060    | 3,714..4,492 | −18.8 %        |
| year 260    | 4,204    | 3,707..4,803 | −15.9 %        |

> "Year 0" in the trace is the snapshot at the **end** of the first
> year-loop iteration, which already includes one round of plague-year
> mortality on year 0 ∈ `PLAGUE_YEARS = [0, 10, 25]`. So the pre-loop
> initial population was 5,000; the −10 % already reflects plague at
> year 0.

**Baseline check status (with-plague):**
- `[~]` mean breaches the −20 % fence between year 25 and ~year 100,
  worst case −24.2 % at year 25, then recovers to −16 % by year 260.
- `[!]` worst single-run end-state pop = 3,707 (run 2) = −25.9 %; one
  other run (run 4) ended at −24.8 %. 2 of 5 runs ended outside the
  fence.
- This run alone is **not sufficient** to clear the engine. The
  companion `--no_plague` baseline (separate log) is the one that
  actually evaluates `REPRO_SHARE`.

## 6. Headline numbers

| metric                                       | value (mean ± SD)   |
|----------------------------------------------|---------------------|
| Slavic linguistic proportion at end          | **18.42 % ± 4.46 %** |
| Slavic proportion mid-run (visible from progress lines, run-by-run) | runs 1..5 at year 260: 17.1 %, 20.8 %, 12.0 %, 18.1 %, 24.0 % |
| Number of runs                               | 5                   |
| Wall time                                    | 36.5 s              |

There is no calibration target for this run. The Slavic share rises
from the 10 % seed to ~18 % entirely from differential plague mortality
(`slavic.plague_mortality = 0.04` vs `non_slavic = 0.15`). That is by
construction, not a finding — and per CLAUDE.md the plague-mortality
asymmetry is an INPUT the migration hypothesis requires, not a result
the model produces.

## 7. What surprised me / what to flag for prose

- **The plague is doing the heavy lifting on the Slavic share even
  with zero migration.** Going from 10 % to 18 % over 260 yr in a no-
  migration baseline is purely the differential-mortality input talking.
  The size of that asymmetry needs to be a named, swept input in the
  Methods text, not buried.
- **Pop drift is plague-driven, not engine-driven** — the dip
  bottoms at year 25 (immediately after the last plague year) and
  recovers monotonically thereafter. The engine itself looks well-
  behaved *in this run*, but only the no-plague baseline can confirm
  `REPRO_SHARE`.
- **The min-run end-state of 3,707 is a wide-ish run-to-run band.**
  At `num_runs = 5` the SD on year-260 pop is roughly ±450. For the
  full scenario matrix we should bump runs to 10+ so per-scenario SDs
  are narrow enough to compare.

## 8. Artefacts produced

- `results_slavic1.txt`  *(overwritten — keep an eye out, see §9)*
- This log file.

## 9. Next action

1. Companion engine-sanity baseline: same command + `--no_plague`,
   logged separately as `2026-05-14_baseline_no_plague_slavic1.md`.
2. If both baselines hold, unblock the full scenario matrix (DECISIONS.md
   item).
3. **Note for housekeeping:** every run currently overwrites
   `results_<scenario>.txt`. Once we move from baselines to the matrix,
   the script needs a per-run output filename or we lose artefacts. Track
   in DECISIONS.md.
