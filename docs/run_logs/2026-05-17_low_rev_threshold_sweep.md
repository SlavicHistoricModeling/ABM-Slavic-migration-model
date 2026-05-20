# Low-reverse-assimilation threshold-resolution sweep (response8)

> 2026-05-17. Fine-grained sweep of the low-reverse-assimilation
> strip the response7 sweep skipped, with two migration-window
> settings (default 100yr and extended 150yr). Adjudicates whether
> any admissible cell crosses the 80 % historical Slavic-dominance
> threshold within the current model — i.e. whether the paper
> publishes a rigorous null or has a positive thesis to defend.
>
> **Verdict — Slavic1 (the archaeologically-admissible scale,
> ~1 M migrants): NO cell reaches ≥80% across the full
> low-reverse-assim × substrate × migration-window grid (24 cells).**
> Maximum is **70.90 % ± 5.15 %** at the most favorable
> configuration (sub = 0.30, rev = 0.000, win = 150 yr); 1-SD upper
> bound 76.05 %, still below the threshold.
>
> Per response8 decision criterion: **the demographic mechanism
> as implemented cannot produce historical rural dominance at
> archaeologically-plausible migration, full stop.** The paper
> publishes the rigorous null (decision recorded in DECISIONS.md
> 2026-05-17).

## Provenance

- Code: `slavic_migration_submited_v1.py` at commit `37054ac`
  (engine frozen per response7/8).
- Override mechanism: per-cell, two sed substitutions into a
  `/tmp` copy of the canonical engine — (a) `reverse_assim`
  rate across all scenarios in the SCENARIOS dict, (b) the
  migration window line (`if year < 100:` → `if year <
  $window:`). Canonical file unmodified throughout.
- Sweep script: `scripts/run_low_rev_threshold_sweep.sh`.
- Grid (48 cells):
  - `reverse_assim_rate` ∈ {0.000, 0.0025, 0.005, 0.0075, 0.010, 0.015}
  - scenarios: slavic1 (~1 M, admissible), slavic2 (~3 M, reference)
  - substrate ∈ {0.00, 0.30}
  - migration window ∈ {100 yr default, 150 yr extended}
- Per cell: `--num_runs 10`, `--seed 42`, otherwise scenario
  defaults.
- Output files: `results_lowrev_<scen>_sub<f>_rev<r>_win<w>.txt`
  (gitignored; this log is the durable record).

## Decision criterion (recap from response8)

> *"If no admissible cell (slavic1, any low reverse-assimilation,
> either window, substrate ≤0.30) reaches ≥80%: the paper is C —
> the demographic mechanism as implemented cannot produce
> historical dominance at plausible migration, full stop.*
>
> *If some slavic1 cell reaches ≥80%: identify it precisely; that
> cell is a candidate positive mechanism and we examine what it
> assumes before believing it.*
>
> *Do not editorialize toward either outcome. Report the grid."*

## Result — slavic1 (the admissible scale)

24 cells complete. Final Slavic share at scenario end (year 260),
mean ± SD across 10 runs at seed 42.

### slavic1, migration window = 100 yr (default)

| substrate \ reverse_assim | 0.000 | 0.0025 | 0.005 | 0.0075 | 0.010 | 0.015 |
|---|---|---|---|---|---|---|
| 0.00 | 51.15 % | 44.73 % | 34.94 % | 34.49 % | 27.23 % | 24.50 % |
| 0.30 | **65.88 %** | 57.86 % | 52.86 % | 42.16 % | 36.35 % | 25.50 % |

(SDs in source files; max-cell ±SD in summary below.)

### slavic1, migration window = 150 yr (extended, "slow vernacularization over generations")

| substrate \ reverse_assim | 0.000 | 0.0025 | 0.005 | 0.0075 | 0.010 | 0.015 |
|---|---|---|---|---|---|---|
| 0.00 | 60.12 % | 53.45 % | 47.84 % | 40.75 % | 33.81 % | 28.48 % |
| 0.30 | **70.90 %** | 66.52 % | 57.58 % | 49.23 % | 41.56 % | 30.04 % |

### Threshold flagging (slavic1)

**Cells ≥80%:** none (out of 24).
**Cells ≥70%:** one — slavic1 sub=0.30, rev=0.000, win=150 yr at
70.90 %.

The single ≥70% cell sits at the **most extreme corner** of the
admissible space: zero reverse-assimilation, maximum-genetic-
plausible substrate (0.30), and a migration window 50% longer
than the archaeological default. Even this configuration falls
~9 pp short of the 80% threshold.

### Maximum-cell ± SD

The slavic1 maximum (sub=0.30, rev=0.000, win=150 yr):

```
results_lowrev_slavic1_sub0.30_rev0.000_win150.txt
Avg Final Proportion: 70.90% (+/-5.15%)
year   0: 32.25% +/- 0.13%
year  25: 38.78% +/- 0.69%
year  50: 40.79% +/- 1.31%
year 100: 51.33% +/- 2.22%
year 150: 61.86% +/- 3.10%
year 200: 66.76% +/- 4.34%
year 260: 70.90% +/- 5.15%
```

The SD on the maximum cell is **5.15 %**, so the upper bound of
the 1-SD range (76.05 %) **still does not reach 80%**.

### Slavic1 verdict — no admissible cell reaches the threshold

**No slavic1 cell reaches ≥80% Slavic share.** Per response8
decision criterion, the verdict is: *the demographic mechanism
as implemented cannot produce historical rural dominance at
archaeologically-plausible migration, full stop*.

The result is robust across:
- The full low-reverse-assim strip {0.000–0.015}.
- Both substrate values {0.00, 0.30}.
- Both migration windows {100 yr, 150 yr}.

The maximum at 70.90% is at the corner of the admissible space
that is most generous to the migration hypothesis (no reverse
assimilation, maximum substrate, extended migration window).
That corner closes the gap to within ~9 pp of historical, but
does not bridge it. The 1-SD upper bound on that maximum cell
(76.76 %) is also below the threshold.

## Result — slavic2 (the reference scale, EXCLUDED from admissibility)

24 cells complete. Slavic2 is included per response8 for
**reference only** — it is excluded from the admissibility
criterion (~3 M migrants is 3× Curta's archaeological upper
bound, so a slavic2 finding does not constitute an
archaeologically-plausible positive thesis).

### slavic2, migration window = 100 yr (default)

| substrate \ reverse_assim | 0.000 | 0.0025 | 0.005 | 0.0075 | 0.010 | 0.015 |
|---|---|---|---|---|---|---|
| 0.00 | **89.73 %** ≥80 | **87.09 %** ≥80 | **83.43 %** ≥80 | 76.81 % ≥70 | 71.75 % ≥70 | 59.41 % |
| 0.30 | **91.47 %** ≥80 | **91.60 %** ≥80 | **89.47 %** ≥80 | **88.31 %** ≥80 | **84.66 %** ≥80 | 77.51 % ≥70 |

### slavic2, migration window = 150 yr (extended)

| substrate \ reverse_assim | 0.000 | 0.0025 | 0.005 | 0.0075 | 0.010 | 0.015 |
|---|---|---|---|---|---|---|
| 0.00 | **93.13 %** ≥80 | **91.40 %** ≥80 | **88.43 %** ≥80 | **85.70 %** ≥80 | **81.58 %** ≥80 | 68.59 % |
| 0.30 | **93.89 %** ≥80 | **94.60 %** ≥80 | **92.94 %** ≥80 | **92.21 %** ≥80 | **89.57 %** ≥80 | **85.44 %** ≥80 |

### Threshold flagging (slavic2)

**Cells ≥80%:** 19 of 24 (≈79%).
**Cells ≥70%:** 23 of 24 (≈96%; only slavic2 sub=0.00 rev=0.015
win=100 at 59.41% falls below).

The slavic2 reference grid shows that the model **does** reach
historical Slavic dominance across most of the low-rev_assim ×
substrate × window grid — at the ~3 M migrant scale. At
sub = 0.30 and rev ≤ 0.010 (window-irrespective), every cell
clears 80%. Even at sub = 0.00 (no substrate) the rev = 0.000
column clears 80% in both windows (89.73% at win=100, 93.13% at
win=150).

### Slavic2 verdict — reference context (NOT admissibility)

**Slavic2 reaches ≥80% in 19/24 cells, but slavic2 is excluded
from the admissibility criterion.** A 3 M migrant scenario is 3×
Curta's archaeological upper bound. The slavic2 result is
recorded as reference context — it demonstrates that the model
*can* produce historical Slavic dominance at low rev_assim, but
only at migration scales outside the empirically-defensible
envelope.

This reinforces (rather than contradicts) the slavic1 verdict:
dominance is reachable in the model family, but the threshold
scale at which it becomes reachable is *higher than the
archaeological envelope*.

## Observed limitation (per response8 scope)

Response8 explicitly directed: *"If the results suggest the model
needs [a prestige term or transmission-rule change] to reach
80% (likely), state that as an observed limitation in the log —
do not implement it."*

**Observed limitation, recorded explicitly:** at the
archaeologically-admissible migration scale, the current model
family — even at the corner of the admissible space most
generous to the migrationist hypothesis (rev_assim = 0.000,
sub = 0.30, win = 150 yr) — reaches at most ~71% Slavic share.
Closing the remaining ~9 pp to the historical ~80%+ rural
dominance threshold would require either:

1. **A prestige / institutional channel** — a transmission rule
   where Slavic carries asymmetric adoption pressure beyond
   majority-neighborhood alignment (something analogous to the
   Arabic case's institutional reinforcement that the Arabic
   matrix Fig 1 calibrates at ~15-19 pp). The current model has
   no such channel.
2. **A different transmission rule** — for example, a probabilistic
   bilingualism intermediate state rather than discrete language
   labels, or a generational age-graded acquisition that differs
   from the current cell-pool draw rule.
3. **Migration outside the admissible scale** — slavic2 (~3 M, 3×
   archaeology) or slavic3 (~5 M, 5× archaeology; population-
   doubling). Slavic3 reaches dominance in matrix batch 1; but
   the migration scale itself is implausible on independent
   archaeological grounds (Curta 2001).

Per response8 scope discipline: **these are not implemented or
tested here**. They are observed as limitations of the current
modelling family with respect to the historical outcome. The decision
to extend the model or publish the null is the user's and is
not triggered by this sweep. **(Resolved 2026-05-17: publish
the null. Engine remains frozen at `37054ac`. See
DECISIONS.md.)**

## Implications for the paper

The verdict has direct implications for the paper's framing:

- **The negative result is the paper's primary contribution.**
  At every archaeologically-admissible parameter combination
  tested across the response7 and response8 sweeps, the model
  fails to reach historical Slavic linguistic dominance. The
  paper is a **rigorous null**: demographic-ABM mechanisms of
  the Kandler family — even with substrate, even with extended
  migration windows, even with reverse-assimilation rates
  varied from 0 to default — cannot produce ~80%+ rural Slavic
  dominance at the ~1 M migrant scale Curta's archaeology
  allows.
- **The substrate hypothesis is exhausted as a Results-level
  claim.** The response7 adjudication showed the substrate
  U-shape was an artifact of reverse-assimilation; the
  response8 sweep shows even the *most favorable* substrate
  configuration (sub = 0.30, rev = 0.000) does not reach
  historical. The substrate-as-rescue argument fails
  empirically within the model.
- **The Arabic 15-19 pp "combined institutional + bilingual"
  ceiling becomes the most likely interpretation.** The
  ~9 pp gap from 71% to 80% in the most-favorable slavic1
  cell is within the Arabic-calibrated ceiling, which is
  consistent with — though not direct evidence of — the
  hypothesis that the historical Slavic case required
  non-demographic channels (institutional, bilingual,
  or both) to close.

## Status

- Slavic1 grid: COMPLETE (24/24). Verdict: **rigorous null** —
  no admissible cell reaches ≥80%; max 70.90% at the most
  favorable corner (sub=0.30, rev=0.000, win=150).
- Slavic2 grid: COMPLETE (24/24). Reference context only; 19/24
  cells ≥80% but slavic2 is excluded from admissibility.
- Total sweep wall time: 324 min (5.4 hrs) — extended past the
  initial ~3 hr estimate by what appears to be an overnight
  suspension on the host (typical pattern for long unattended
  runs on the Windows machine; the SSH pool fix would mitigate
  this for future heavy sweeps but is not blocking).
- All slavic1 + slavic2 results files committed implicitly
  via the gitignored `results_lowrev_*.txt`; this log is the
  durable record.

## What this sweep settles for the paper

1. **The paper publishes the rigorous null.** At every
   archaeologically-admissible parameter combination tested
   across response7 + response8 sweeps, the demographic-ABM
   mechanism fails to reach historical Slavic linguistic
   dominance. The negative result is the paper's primary
   contribution. (Decision recorded 2026-05-17 — see
   DECISIONS.md.)
2. **The substrate hypothesis is empirically exhausted as a
   Results-level rescue.** Even at the maximum-genetic-
   plausible substrate (0.30) combined with the most generous
   rev_assim = 0.000 and the extended 150 yr migration window,
   the model lands at 70.90% — ~9 pp short of historical and
   with 1-SD upper bound 76.05% still below 80%.
3. **The Arabic-calibrated 15-19 pp "combined institutional +
   bilingual" ceiling** (the Arabic gap from Fig 1 / matrix
   batch 1) becomes the most natural reading of where the
   missing ~9 pp lives: in mechanisms the current ABM does
   not implement.
4. **Extend-vs-publish-null decision: RESOLVED 2026-05-17 in
   favour of publishing the null.** Implementing a prestige
   parameter or transmission-rule change to reach 80 % was
   considered and rejected because the prestige parameter is
   empirically unconstrained and would relocate rather than
   resolve the underdetermination — a parameter-tuneable
   extension that hits the target by design is exactly the
   methodological pathology the reassessment was undertaken to
   expose. The decision is recorded in DECISIONS.md. Engine
   remains frozen at `37054ac`; no further sweeps; no further
   code.
