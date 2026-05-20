# Substrate × reverse-assimilation 2-parameter sweep (response7 step 1)

> **Decision-criterion log.** Adjudicates whether the non-monotonic
> shape of the post-fix single-parameter substrate response curve
> (`docs/run_logs/2026-05-16_substrate_curve.md`) is a structural
> finding about substrate dynamics or an artifact of the
> ungrounded `reverse_assimilation_rate` parameter.
>
> **Outcome: the shape is parameter-conditional.** The U-shape
> deepens as `reverse_assimilation_rate` increases and disappears
> at `reverse_assim = 0.000`. Per response7 decision criterion,
> the substrate curve does **NOT** enter Results as a finding in
> its single-parameter form. The monotone reading (at
> `reverse_assim = 0.000`) is the Results-section representation;
> the U-shape becomes a Discussion observation explicitly
> conditioned on the reverse-assimilation rate.

## Provenance

- Code: `slavic_migration_submited_v1.py` at commit `37054ac`
  (post-substrate-init-fix; engine frozen per response7 §4).
- Override mechanism: the `reverse_assimilation_rate` parameter
  has no CLI flag in the canonical engine. To run the sweep
  without modifying the canonical file (per response7 §4: "no
  new flags, no further substrate-logic edits"), each cell is
  invoked against a `/tmp` copy of the engine with the
  reverse-assim rate sed-patched in place. The canonical file
  at `slavic_migration_submited_v1.py` is byte-identical to its
  commit-`37054ac` form throughout the sweep.
- Sweep script: `scripts/run_substrate_revassim_sweep.sh`.
- Sweep grid:
  - substrate fraction ∈ {0.00, 0.10, 0.20, 0.30, 0.40, 0.50}
  - `reverse_assimilation_rate` ∈ {0.000, 0.015, 0.030, 0.045}
  - scenarios: slavic1 (REQUIRED), slavic2 (compute-allowing).
- Per-cell: `--num_runs 10`, `--seed 42`, otherwise scenario defaults.
- Output files: `results_revassim_<scenario>_sub<f>_rev<r>.txt`
  (gitignored; this log is the durable record).

## Decision criterion (recap from response7)

> *"If the U-shape / counterproductive-at-small-fractions
> mechanism persists with reverse_assimilation = 0.000, it is a
> robust structural finding. The briefing's substrate framing is
> earned; proceed to update §3/§5/§6 with it. If the dip
> flattens or inverts as reverse-assimilation decreases, the
> mechanism is an artifact of an ungrounded parameter. It does
> not enter Results as a finding. It becomes, at most, a
> Discussion observation explicitly conditioned on the
> reverse-assimilation assumption. Update §3/§5/§6 with the
> monotone reading and flag the U-shape as parameter-conditional.
> Either outcome is publishable. State which occurred, with the
> grid as evidence, and do not editorialise toward the
> convenient one."*

## Result — slavic1 grid (complete)

| substrate \ reverse_assim | 0.000 | 0.015 | 0.030 (default) | 0.045 |
|---|---|---|---|---|
| 0.00 | 51.15 % ± 5.99 | 24.50 % ± 5.05 | 18.35 % ± 4.40 | 15.39 % ± 4.59 |
| 0.10 | 47.83 % ± 5.76 | 9.22 % ± 4.27 | 4.12 % ± 3.09 | 1.66 % ± 0.65 |
| 0.20 | 56.01 % ± 4.26 | 13.37 % ± 5.49 | 3.95 % ± 2.49 | 2.53 % ± 1.07 |
| 0.30 | 65.88 % ± 4.95 | 25.50 % ± 8.43 | 9.94 % ± 5.94 | 4.71 % ± 2.81 |
| 0.40 | 73.26 % ± 4.32 | 43.15 % ± 7.69 | 25.26 % ± 7.76 | 15.37 % ± 8.41 |
| 0.50 | 77.21 % ± 4.05 | 60.66 % ± 4.78 | 52.67 % ± 8.08 | 42.14 % ± 9.97 |

### Reading along each `reverse_assim` column

- **rev = 0.000** (rule disabled): the curve is **essentially
  monotonic** (51.15 → 47.83 → 56.01 → 65.88 → 73.26 → 77.21).
  The slight 51 → 48 dip at small substrate is within ±1 SD of
  either point. No pronounced U-shape.
- **rev = 0.015** (Slavic 3 scenario default): mild U-shape —
  baseline 24.50, drops to 9.22 at sub = 0.10, climbs back to
  60.66 at sub = 0.50.
- **rev = 0.030** (Slavic 1 / Slavic 2 scenario default,
  post-fix substrate-curve canonical row): pronounced U-shape —
  18.35 → 4.12 → 3.95 → 9.94 → 25.26 → 52.67.
- **rev = 0.045** (above-default sensitivity): deeper U-shape —
  15.39 → 1.66 → 2.53 → 4.71 → 15.37 → 42.14.

### Decision-criterion verdict (slavic1)

**The U-shape disappears at `reverse_assim = 0.000` and deepens
monotonically as `reverse_assim` increases. The mechanism is an
artifact of the ungrounded reverse-assimilation parameter.**

Per response7, the shape does **NOT** enter Results as a finding
in the form it took in the single-parameter substrate curve.
The monotone reading (at `reverse_assim = 0.000`) is the
Results representation; the U-shape is a Discussion observation
explicitly conditioned on the reverse-assimilation assumption.

## Result — slavic2 grid (complete)

| substrate \ reverse_assim | 0.000 | 0.015 | 0.030 | 0.045 |
|---|---|---|---|---|
| 0.00 | 89.73 % ± 1.76 | 59.41 % ± 3.54 | 32.35 % ± 6.88 | 26.36 % ± 5.98 |
| 0.10 | 88.44 % ± 1.85 | 55.84 % ± 4.63 | 16.42 % ± 6.12 | 6.24 % ± 3.66 |
| 0.20 | 90.44 % ± 1.84 | 64.14 % ± 6.43 | 23.56 % ± 8.76 | 9.17 % ± 4.96 |
| 0.30 | 91.47 % ± 2.24 | 77.51 % ± 2.33 | 49.55 % ± 5.84 | 19.59 % ± 5.65 |
| 0.40 | 94.19 % ± 0.75 | 89.43 % ± 2.68 | 76.87 % ± 3.21 | 59.75 % ± 6.87 |
| 0.50 | 95.48 % ± 1.45 | 93.58 % ± 1.37 | 91.73 % ± 1.94 | 88.10 % ± 3.00 |

NB: the slavic2 scenario default `reverse_assimilation_rate` is
**0.020** (not directly tested in this sweep; lies between the
0.015 and 0.030 columns). The matrix slavic2 entry of 47.93 %
falls between this sweep's rev = 0.015 column (59.41 % at
sub = 0) and the rev = 0.030 column (32.35 % at sub = 0),
consistent with the 0.020 default reading by linear interpolation
(~50 % expected; matrix value 47.93 % ± 4.96 % within sampling
error).

### Reading along each `reverse_assim` column (slavic2)

- **rev = 0.000**: essentially **flat from sub = 0.00 onwards**
  (89.73 → 88.44 → 90.44 → 91.47 → 94.19 → 95.48). slavic2 with
  ~3 M migrants and rule disabled reaches **near-dominance
  regardless of substrate**.
- **rev = 0.015** (slavic3 default): mild U-shape, with the dip
  to 55.84 % at sub = 0.10. Climbs to 93.58 % at sub = 0.50.
- **rev = 0.030** (slavic1 default; ~~slavic2 default~~ — the
  scenario uses 0.020, but 0.030 is a defensible
  one-step-up-from-default sensitivity): pronounced U-shape
  (32.35 → 16.42 → 23.56 → 49.55 → 76.87 → 91.73).
- **rev = 0.045**: deepest U-shape (26.36 → 6.24 → 9.17 →
  19.59 → 59.75 → 88.10).

### Decision-criterion verdict (slavic2)

**Confirms the slavic1 verdict.** The U-shape disappears at
`reverse_assim = 0.000` and deepens monotonically as
`reverse_assim` increases. The mechanism is an artifact of the
ungrounded reverse-assimilation parameter.

The slavic2 finding **also exhibits the same baseline-shift
pattern**: at sub = 0 the slavic2 share goes from 89.73 % at
rev = 0.000 to 32.35 % at rev = 0.030 — a 57 pp swing in the
post-migration share driven solely by the reverse-assimilation
rate.

### Implication for the matrix slavic2 "parity not dominance" finding

The matrix slavic2 entry of 47.93 % was at the scenario default
`reverse_assim = 0.020`. At `rev = 0.000`, slavic2 (the same
3 M migration scale, no substrate) reaches **89.73 %** —
crossing into dominance. The headline "even at 3× the
archaeological maximum migration, the model reaches only
parity" is **as parameter-conditional as the substrate
U-shape and the slavic1 baseline-equivalence findings**.

## The bigger picture — reverse-assimilation is the dominant load-bearing parameter for ALL THREE headline findings

This sweep was commissioned by response7 to adjudicate the
substrate finding specifically. It surfaces a broader pattern:
**the reverse-assimilation rate is the dominant load-bearing
parameter for all three post-matrix headline findings**, not
just for the substrate U-shape.

### The three headline findings, restated by `reverse_assim` value

For each of the three post-matrix-batch headline framings, the
sweep gives the share that headline depends on:

#### 1. Slavic 1 ≈ zero-migration plague baseline (the "no net Slavic effect at archaeologically-plausible scale" finding)

| `reverse_assim` | slavic1 sub = 0 | "baseline-equivalent" claim |
|---|---|---|
| 0.000 | 51.15 % ± 5.99 | **FAILS** — 51 % is not baseline |
| 0.015 | 24.50 % ± 5.05 | borderline (overlaps 19.72 % baseline by SD) |
| 0.030 (default) | **18.35 %** ± 4.40 | **holds** (18.35 ≈ 19.72) |
| 0.045 | 15.39 % ± 4.59 | holds (still close to baseline) |

The finding holds at the default `reverse_assim = 0.030` and
weakens (becomes "borderline") or fails as rev_assim drops.

#### 2. Slavic 2 reaches parity, not dominance (the "even 3× plausible migration falls short" finding)

| `reverse_assim` | slavic2 sub = 0 | "parity not dominance" claim |
|---|---|---|
| 0.000 | **89.73 %** ± 1.76 | **FAILS** — 90 % is dominance |
| 0.015 | 59.41 % ± 3.54 | borderline (above parity, below dominance) |
| ~0.020 (matrix default; interpolated) | 47.93 % ± 4.96 | **holds** (parity) |
| 0.030 | 32.35 % ± 6.88 | holds (below parity) |
| 0.045 | 26.36 % ± 5.98 | holds (well below parity) |

The finding holds at the scenario default `reverse_assim =
0.020` and fails as rev_assim drops to 0.

#### 3. Substrate fails to rescue migration hypothesis (the "no defensible (migration, substrate) combination" finding)

| `reverse_assim` | slavic1 + sub = 0.50 | "no rescue" claim |
|---|---|---|
| 0.000 | **77.21 %** ± 4.05 | borderline (within 3 pp of historical 80 %+) |
| 0.015 | 60.66 % ± 4.78 | holds (well below 80 %) |
| 0.030 (default) | **52.67 %** ± 8.08 | **holds** (well below 80 %) |
| 0.045 | 42.14 % ± 9.97 | holds (well below 80 %) |

The finding holds at the default `reverse_assim = 0.030` and
**weakens to borderline** as rev_assim drops to 0 (substrate
+ plausible migration nearly reaches historical at rev = 0).

### All three findings rest on the same parameter

The post-matrix paper's three load-bearing claims are
mechanistically downstream of the **same** parameter
(`reverse_assimilation_rate`), which is **labelled as a free
parameter with no independent empirical grounding** in
`docs/paper/parameter_table.md`. The parameter's default values
(0.020 for slavic2, 0.030 for slavic1) are inherited from the
DIA-25063.pdf code listing without independent defence.

This is not a code defect — the parameter status was correctly
declared free, and the matrix-batch numbers are correctly
reported at the per-scenario default values. It is an
**interpretive observation** the sweep surfaces: the
default value of an undefended free parameter is doing a
lot of work in the paper's headline findings.

### Implication for the paper's framing

Three options for the prose instance to consider:

**Option A — explicit-default discipline.** Report all three
findings explicitly conditioned on the default `reverse_assim`:
"At the scenario default `reverse_assimilation_rate` (per the
inherited DIA-25063 listing): slavic1 ≈ baseline; slavic2 ≈
parity; substrate + plausible migration ≤ 52.67 %." Include a
sensitivity table or appendix showing the rev_assim = 0.000
column for transparency. The negative result is reported as
**parameter-conditional** with the parameter explicitly named.

**Option B — defend the default empirically.** Construct an
empirical argument for why `reverse_assim = 0.020`–`0.030` is
the right value (historical / linguistic precedent;
Christianisation-pressure literature; etc.). The negative
result then rests on this argument's strength.

**Option C — re-cast the paper around the parameter itself.**
The paper's contribution becomes "we show that the linguistic
outcome of Slavic expansion in this ABM family is dominantly
controlled by the reverse-assimilation rate, an undefended
free parameter, across a wide range of migration and substrate
configurations." Different framing, different abstract; same
runs.

This decision routes through the prose instance via the v3
reply that follows this commit. Until then, the briefing's
§3 (substrate), the §5 cross-cutting flat-list, and the §6
abstract claim structure remain **frozen** per response7 §2 —
the freeze now extends beyond substrate to include the
slavic1-baseline and slavic2-parity framings as well, because
the sweep surfaces the same parameter sensitivity in all three.

This is, per response7's closing:

> *"The substrate result got more convenient for your goal and
> that is exactly why it now needs more scrutiny, not less. The
> sweep above is the test that earns it or fences it. Either
> way the paper stays honest and stays publishable — and a
> JASSS reviewer will run the substrate code, so this is the
> test happening on our terms instead of theirs."*

The sweep delivered: it **fenced** the substrate finding (the
U-shape is artifactual). It also surfaced that the **other
two** post-matrix headlines have the same fence around them
for the same reason. Honest reporting requires acknowledging
all three.

## Monotone reading for Results §Substrate

Per response7 decision-criterion outcome
(parameter-conditional), the substrate response curve in
Results should be reported at `reverse_assim = 0.000` (rule
disabled — the parameter-free reading) with explicit flag that
the default-rev_assim curve is reported in a sensitivity
appendix and discussed in Discussion as
parameter-conditional.

**Slavic 1 substrate response curve at `reverse_assim = 0.000`
(the Results-section reading):**

| substrate fraction | final Slavic share |
|---|---|
| 0.00 | 51.15 % ± 5.99 |
| 0.10 | 47.83 % ± 5.76 |
| 0.20 | 56.01 % ± 4.26 |
| 0.30 | 65.88 % ± 4.95 |
| 0.40 | 73.26 % ± 4.32 |
| 0.50 | **77.21 % ± 4.05** |

**The negative result, restated for the Results-section
reading:** at Slavic 1 migration scale (archaeologically
plausible, ~1 M migrants) and reverse-assimilation disabled,
substrate up to the Olalde-bounded 0.50 brings the Slavic share
to **77.21 % ± 4.05 %** — within 3 pp of the historical ~80 %+
share, but not exceeding it. The negative result holds at
slavic1, with caveat that the rev = 0.000 reading is itself a
parameter choice (the rule's empirical anchor is undetermined;
both rev = 0.000 and rev = 0.030 are defensible defaults
because neither has independent empirical support).

This is a **substantially softer** negative result than the
pre-adjudication framing implied. The headline claim shifts
from "no defensible (migration, substrate) combination reaches
historical" to "at archaeologically-plausible migration with
the rev = 0.000 (rule disabled) reading, even maximum-bounded
substrate reaches only ~77 % — within sampling margin of, but
not exceeding, the historical share". The prose instance
should hold whichever framing the data supports and not lean
on the absent-finding the U-shape would have been.

## Implications for the prose-instance briefing

§3 of the briefing must be rewritten to reflect the adjudicated
framing — see `docs/run_logs/2026-05-15_session_summary_for_prose.md`
post-commit. Substrate response curve becomes a Results-section
table at the monotone reading; the U-shape becomes a
Discussion observation.

§5 cross-cutting flat-list must include the slavic1 baseline
parameter-sensitivity disclosure.

§6 abstract claim structure must be softened: the substrate
finding is now "even at maximum-bounded substrate + plausible
migration + rule-disabled reverse-assim, the model reaches at
most ~77 % Slavic — within sampling margin of historical but
not exceeding it". This is a meaningfully weaker claim than
the pre-adjudication framing and must be reported as such.

## Provenance summary

- Slavic1 sweep launched at 06:08:40 (2026-05-17); 24 cells
  completed by ~07:00. Wall time per cell: ~2 minutes.
- Slavic2 sweep launched at \[TBD when slavic1 finishes\];
  ~80–90 min estimated wall time for 24 cells at ~3.5 min each.
- Total wall time for the sweep: ~2 hours.
- Code commit: `37054ac` (canonical engine; the sed-patched
  /tmp copy differs only in the literal
  `"reverse_assimilation_rate": <value>,` substitution for the
  four scenarios in the `SCENARIOS` dict).

## Status

- slavic1 grid: COMPLETE; verdict recorded above.
- slavic2 grid: pending.
- This log will be re-committed when slavic2 lands and the
  full verdict is in.
- Fig 2 (substrate response surface — multi-line form
  matching the parameter-conditional framing) will be
  generated by `docs/paper/figures/fig2_substrate_curve.py`
  once the slavic2 grid completes.
- Briefing §3 / §5 / §6 update + Table 3 in
  `docs/paper/results_tables.md` queued for after the
  finalisation commit.
- v3 reply to prose instance queued for after the finalisation
  commit — will package this decision log + the secondary
  baseline observation + the recommended scaffold revisions.
