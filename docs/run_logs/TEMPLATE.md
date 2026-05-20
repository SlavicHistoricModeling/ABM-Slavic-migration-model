# Run log — `<short slug, e.g. 2026-05-14_baseline_with_plague>`

> Drop a copy of this file into `docs/run_logs/`, rename, fill out, commit.
> One log per scenario *config*, not per individual run inside a config —
> `--num_runs N` is just a field below.
>
> The whole file is meant to be pasted into the Claude.ai web instance as
> a self-contained briefing — so write it for a reader who has not seen
> the terminal output and does not have the repo open. Quote actual numbers,
> not impressions.

## 1. Provenance

| field           | value                                                       |
|-----------------|-------------------------------------------------------------|
| Date (UTC)      | `YYYY-MM-DD HH:MM`                                          |
| Code commit     | `git rev-parse --short HEAD` → `xxxxxxx`                    |
| Branch          | `main`                                                      |
| Working tree    | `clean` / `dirty (list of modified files)`                  |
| Script          | `slavic_migration_submited_v1.py`                           |
| Python          | `python --version` → `Python 3.x.x`                         |

If the working tree was dirty, **say what was uncommitted and why**. Per
CLAUDE.md, no scenario matrix on uncommitted code.

## 2. What this run was for

One paragraph. What question is this run answering? Which earlier log /
decision does it follow up on?

Examples:
- "Mandatory pre-flight baseline per CLAUDE.md — confirm population stays
  ±20 % of 5 000 over 260 yr with no Slavic migration, no substrate."
- "Sweep INHERITANCE_AGE_MAX ∈ {22, 25, 28, 30} on slavic2 to test
  sensitivity of the headline proportion to the mother-tongue cutoff."

## 3. Command

```
python slavic_migration_submited_v1.py \
    --scenario <slavic1|slavic2|slavic3|arabic|all> \
    --num_runs <int> \
    --seed <int> \
    [--substrate] \
    [--birth_vary <float>] \
    [--migration_override <int>] \
    [--no_plague] \
    [--plot]
```

## 4. Parameters that matter for *this* run

Only list parameters whose value diverges from the SCENARIOS default for
the scenario, or are baseline-relevant. Don't dump the whole config dict.

| parameter                       | scenario default | this run     |
|---------------------------------|------------------|--------------|
| `migration_rate`                |                  |              |
| `slavic_birth_rate` (per-female)|                  |              |
| `slavic_birth_rate_new`         |                  |              |
| `INHERITANCE_AGE_MAX`           | 25               |              |
| `REPRO_SHARE`                   | 0.151            |              |
| `PLAGUE_YEARS`                  | scenario-derived |              |
| `substrate`                     | False            |              |
| `birth_vary`                    | 0.0              |              |
| `seed`                          | 42               |              |
| `num_runs`                      | 10               |              |

Also note: any change to GROUPS' `initial_fraction`, region rules, or
plague mortality. If you didn't touch those, write "GROUPS untouched".

## 5. Population trajectory (engine health)

Per CLAUDE.md, every run has to demonstrate engine health, not just report
proportions. Capture total population at:

| year offset | total agents (mean across runs) | range across runs   |
|-------------|---------------------------------|---------------------|
| year 0      |                                 |                     |
| year 25     |                                 |                     |
| year 50     |                                 |                     |
| year 100    |                                 |                     |
| year 150    |                                 |                     |
| year 200    |                                 |                     |
| year 260    |                                 |                     |

**Baseline check status:**
- `[ ]` population stays within ±20 % of 5 000 across 260 yr (mandatory baseline only)
- `[ ]` `--no_plague` baseline stayed nearly flat (engine-sanity check only)
- `[ ]` n/a — this is a scenario run, baselines already passed at commit `xxxxxxx`

## 6. Headline numbers

| metric                                       | value (mean ± SD)   |
|----------------------------------------------|---------------------|
| Slavic linguistic proportion at end          |                     |
| Slavic proportion at year 100                |                     |
| Slavic proportion at year 200                |                     |
| Number of runs                               |                     |
| Wall time                                    |                     |

For Arabic scenario the calibration target is **~55 %** at year 170. For
Slavic scenarios there is no fixed target — the question is *what shape*
the trajectory takes.

## 7. What surprised me / what to flag for prose

Free text. Things to call out for the Claude.ai prose instance:
- shape of the curve (S-curve, plateau, collapse, oscillation)
- divergence between scenarios that "should" behave alike
- anything that contradicts a claim in the current Methods text
- anything that makes the negative claim (mass migration implausible)
  *stronger* or *weaker*

Be honest about uncertainty. "Looks consistent with X" is fine; don't
upgrade it to "shows X".

## 8. Artefacts produced

- `results_<scenario>.txt`
- `<scenario>_proportions.csv` *(if extended; the v1 script does not
  emit this by default — note if you added it)*
- `figure1.png` *(if `--plot`)*
- Log file: `docs/run_logs/<this filename>`

## 9. Next action

One sentence. What does this log unlock or block?
