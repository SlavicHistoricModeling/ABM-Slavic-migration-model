# Run log — 2026-05-14_baseline_no_plague_slavic1

> Mandatory pre-flight baseline #2 of 2 per CLAUDE.md.
> **VERDICT: REPRO_SHARE looks correct, but the uniform age-init
> transient pushes population +24 % over 260 yr. Engine drift fails
> the "nearly flat" check. Fix age-init before running the scenario
> matrix.** See §7.

## 1. Provenance

| field           | value                                                       |
|-----------------|-------------------------------------------------------------|
| Date (UTC)      | 2026-05-14                                                  |
| Code commit     | `183f30f`                                                   |
| Branch          | `main`                                                      |
| Working tree    | clean at launch                                             |
| Script          | `slavic_migration_submited_v1.py`                           |
| Python          | local CPython (host: Windows 11)                            |

## 2. What this run was for

The engine-sanity baseline mandated by CLAUDE.md:
> *"Also run one baseline with `PLAGUE_YEARS = []` — should come out
> nearly flat; that confirms `REPRO_SHARE` is right."*

Strips plague entirely so the only mortality is `BASE_MORTALITY = 0.02`,
balanced against the per-female birth-rate calibration. If
`REPRO_SHARE = 0.151` and `CBR_NON_SLAVIC = 0.020` are correctly
matched, population should hold near 5,000 across 260 yr.

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

| parameter                       | scenario default | this run     |
|---------------------------------|------------------|--------------|
| `migration_rate`                | 10               | **0** (`--migration_override 0`)  |
| `PLAGUE_YEARS`                  | `[0, 10, 25]`    | **`[]`** (`--no_plague`) |
| `slavic_birth_rate` (per-female)| `per_female_rate(0.021) ≈ 0.139` | unchanged |
| `slavic_birth_rate_new`         | `per_female_rate(0.011) ≈ 0.073` | unchanged |
| `INHERITANCE_AGE_MAX`           | 25               | 25           |
| `REPRO_SHARE`                   | 0.151            | 0.151        |
| `substrate`                     | False            | False        |
| `birth_vary`                    | 0.0              | 0.0          |
| `seed`                          | 42               | 42           |
| `num_runs`                      | 10               | **5** (baseline only)  |

GROUPS untouched. Substrate flag not passed.

## 5. Population trajectory (engine health)

| year offset | mean pop | min..max     | drift vs 5,000 |
|-------------|----------|--------------|----------------|
| year 0      | 5,045    | 5,029..5,064 | +0.9 %         |
| year 25     | 5,306    | 5,147..5,430 | +6.1 %         |
| year 50     | 5,510    | 5,258..5,851 | +10.2 %        |
| year 100    | 5,708    | 5,259..6,261 | +14.2 %        |
| year 150    | 5,897    | 5,459..6,443 | +17.9 %        |
| year 200    | 6,152    | 5,461..6,792 | **+23.0 %**    |
| year 260    | 6,194    | 5,543..6,939 | **+23.9 %**    |

**Baseline check status (no-plague):**
- `[X]` Population is *not* nearly flat — it climbs steadily and
  passes the +20 % fence around year 200, ending at +24 % mean
  (worst-run +38.8 % at 6,939).
- The growth rate decays over time (Δ year 200→260 is only +42 mean
  agents over 60 yr) — i.e. the system is still approaching a higher
  equilibrium, not running away. So `REPRO_SHARE = 0.151` itself is
  approximately right *for the equilibrium age structure*.
- The drift is the **uniform-age-init transient** that the inline
  comment in `slavic_migration_submited_v1.py` flagged as a known
  trade-off and that DECISIONS.md lists as an open question.

## 6. Headline numbers

| metric                                       | value (mean ± SD)   |
|----------------------------------------------|---------------------|
| Slavic linguistic proportion at end          | 12.59 % ± 4.06 %    |
| Slavic proportion at year 260, run-by-run    | 8.5 %, 13.8 %, 12.5 %, 18.7 %, 9.4 % |
| Number of runs                               | 5                   |
| Wall time                                    | 58.3 s              |

No target. The Slavic share drifts gently up from the 10 % seed (8–19 %
across runs) under the cell-pool mother-tongue rule plus a small
fertility nudge (CBR_SLAVIC[slavic1] = 0.021 vs CBR_NON_SLAVIC = 0.020).
With no plague and no migration this is just demographic noise around
the seed.

## 7. What surprised me / what to flag for prose

This is the important part of the run.

### Diagnosis — why the population drifts up

The script initialises agent ages uniformly on `[0, 60]`. The equilibrium
age structure under `BASE_MORTALITY = 0.02` is geometric: `N(a) ∝ 0.98^a`,
mean ≈ 49 yr. The two distributions differ a lot in the reproductive
band:

- Uniform[0,60]: fraction in repro age 15–40 = 26/61 ≈ **0.426**
- Equilibrium 0.98^a, a = 0..∞: same fraction ≈ **0.302**

So at year 0 there are ~40 % more reproductive-age females than the
calibration assumes. Crude births in year 0 are
`pop × 0.5 × 0.426 × per_female_rate(0.020) ≈ pop × 0.0282`, against
crude deaths of `pop × 0.020`. That is a +0.8 %/year intrinsic growth
rate at the start, decaying to ~0 as the cohort ages out. Integrated
over 260 years that gives roughly the observed +24 %.

So `REPRO_SHARE` is right; the *initial age structure* is off.

### Recommended fix (NOT yet applied)

Initialise ages from the equilibrium geometric distribution instead of
uniform — one line in the agent-init loop. Smallest possible patch:

```python
# inside the agent-init loop, replace:
"age": random.randint(0, 60),
# with:
"age": min(MAX_AGE, int(random.expovariate(BASE_MORTALITY))),
```

Expected effect: the no-plague baseline holds 5,000 ± a few percent
across the full 260 yr.

### Alternatives considered (and why I'm not taking them)

- **Reduce `CBR_NON_SLAVIC`** to compensate: counter-physical (the
  CBR is meant to match Russell 1987 ~0.02), and would distort the
  modest-Slavic-advantage framing.
- **Raise `BASE_MORTALITY`** to compensate: same problem, plus it
  would invalidate the `REPRO_SHARE = 0.151` derivation.
- **Accept the drift and quote results in proportions only**: the
  whole point of the negative claim is demographic plausibility — we
  cannot afford a +24 % engine drift contaminating headline numbers.

### What this means for the scenario matrix

**Blocked.** Per CLAUDE.md "If the engine drifts, fix it before running
anything bigger." Apply the geometric age-init fix, re-run both
baselines, then unblock the matrix.

## 8. Artefacts produced

- `results_slavic1.txt` (now reflects this run; the with-plague
  numbers are preserved in the companion log
  `2026-05-14_baseline_with_plague_slavic1.md` §5)
- This log file.

## 9. Next action

1. Apply geometric-age-init fix as a single small commit.
2. Re-run both baselines under the new commit hash, write fresh logs.
3. Once both baselines pass, scenario matrix is unblocked.
