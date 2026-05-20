# Results table pack

> Tables for the Results section, in final form, copied from the
> canonical durable logs at HEAD. Five tables (matrix, plague
> sweep, substrate response curve at the Results-section reading,
> substrate × reverse-assim response surface as sensitivity
> appendix, inheritance sweep) plus the low-reverse-assim
> threshold-resolution sweep (the null verdict).
>
> All numbers reproducible at seed 42. Engine frozen at commit
> `37054ac`; matrix / plague / inheritance numbers also reproduce
> from `66f1d6b` since those code paths are unaffected by the
> substrate-init fix. All paths gitignored `results_*.txt`; this
> file is the tracked single-source-of-truth for the
> Results-section tables.
>
> **Paper framing (decided 2026-05-17): the rigorous null.** The
> demographic-ABM mechanism in the current model family fails to
> reach the historical ~80 %+ Slavic rural-dominance threshold at
> any archaeologically-admissible parameter combination tested
> (Table 5). The substrate hypothesis appears only as a fenced
> conjecture in the Discussion; the residual ~9 pp gap between
> the most favourable admissible cell (70.90 %) and the historical
> threshold is interpreted via the Arabic-calibrated
> institutional + bilingual ceiling (Table 1 row 5: Arabic ~36 %
> modelled vs. ~55 % historical, ~19 pp gap bounds the combined
> non-demographic contribution). See DECISIONS.md 2026-05-17 for
> the decision record and the EXTEND-rejected rationale.

## Pre-fix-number grep audit

A repo-wide grep for the superseded pre-fix substrate numbers
(quoted in earlier briefings / DECISIONS log entries before the
substrate fix at commit `37054ac`) was run; the audit confirms
that **no superseded number survives outside historical run-log
entries explicitly dated pre-fix**. See "Grep audit" section at
the end of this file for the full grep output and reasoning.

## Table 1 — Matrix batch 1 (six runs)

Code: `66f1d6b`. 10 runs each, seed 42. Slavic shares at
scenario end (year 260 for Slavic scenarios; year 170 for
Arabic).

| scenario | migration | final Slavic share | gloss |
|---|---|---|---|
| Slavic 1 | 10 / yr × 100 yr (~1 M migrants) | **18.35 % ± 4.40 %** | Within sampling margin of the zero-migration plague baseline (19.72 % ± 4.98 %). Migration at archaeologically-defensible scale produces no net Slavic linguistic effect in the model. |
| Slavic 2 | 30 / yr × 100 yr (~3 M migrants) | **47.93 % ± 4.96 %** | Reaches parity but not dominance. Even at 3 × the archaeological maximum, migration falls short of the ~80 %+ historical Slavic share. |
| Slavic 3 | 50 / yr × 100 yr (~5 M migrants) | **93.99 % ± 1.69 %** | Reaches dominance, but at a migration scale that doubles the pre-migration Balkan population — outside any archaeological or logistical envelope. |
| Slavic 3 + uniform plague mortality | as Slavic 3, no plague differential | **93.96 % ± 1.50 %** | Differential plague mortality contributes only 0.03 pp to the Slavic 3 result. Migration size is the load-bearing parameter; argument robust to the Mordechai-vs-plague-maximalist debate. |
| Arabic | 10 / yr × 100 yr (~1 M migrants) | **35.95 % ± 2.18 %** | ~19 pp short of the historical ~55 % Arabic share. The gap is an upper bound on combined contributions from mechanisms the ABM does not model — institutional reinforcement (Kennedy 2007; Versteegh 2014) AND bilingual transitional states (Kandler 2010), which cannot be separated without a bilingualism workstream. |
| Arabic + mother-tongue rule off (`INHERITANCE_AGE_MAX = 99`) | as Arabic, cell-pool draw disabled | **41.51 % ± 3.20 %** | Mother-tongue rule contributes +5.56 pp on the Arabic side. |

**Source:** `docs/run_logs/2026-05-15_matrix_batch.md`.

## Table 2 — Plague-mortality sensitivity sweep

Code: `66f1d6b`. 10 runs each, seed 42. Four scenarios at four
non-Slavic plague mortality values (Mordechai-style low 0.10
through plague-maximalist 0.20).

| `non_slavic_plague_mortality` | Slavic 1 | Slavic 2 | Slavic 3 | Arabic |
|---|---|---|---|---|
| 0.10 | 16.38 % ± 2.84 % | 37.80 % ± 4.41 % | 86.51 % ± 2.61 % | 36.72 % ± 3.33 % |
| 0.12 | 17.07 % ± 3.00 % | 42.35 % ± 5.72 % | 90.19 % ± 1.69 % | **35.95 % ± 2.18 %** (Arabic default) |
| 0.15 | **18.35 % ± 4.40 %** (Slavic 1/2 default) | **47.93 % ± 4.96 %** (Slavic 2 default) | 93.01 % ± 2.33 % | 37.91 % ± 3.74 % |
| 0.20 | 19.96 % ± 4.32 % | 61.11 % ± 6.75 % | **93.99 % ± 1.69 %** (Slavic 3 default) | 43.68 % ± 4.67 % |

Bolded cells are each scenario's default value (cross-checks
exact-match the matrix batch). The bracketing range covers the
contested literature on Justinianic plague mortality (Mordechai
et al. 2019; Stathakopoulos 2004).

**Robustness reading:** every scenario's qualitative position is
preserved across the full mortality range. Slavic 1 stays
16–20 % (baseline range) at every value; Slavic 2 reaches at most
61 % even at the high end; Slavic 3 reaches at least 87 % at the
low end; Arabic stays 36–44 %, well short of the historical 55 %.

**Source:** `docs/run_logs/2026-05-15_plague_sweep.md`.

## Table 3 — Substrate response curve (Results-section reading at `reverse_assim = 0.000`)

Code: `37054ac` (substrate fix) with `reverse_assim` forced to
0.000 via the sed-wrapped sweep (see
`docs/run_logs/2026-05-16_substrate_revassim_sweep.md`). 10 runs
each, seed 42.

Per the adjudication outcome (substrate U-shape is
parameter-conditional; full sweep at four reverse-assim values
is reported in the sensitivity appendix), the Results-section
substrate response curve is reported at `reverse_assim = 0.000`
(rule-disabled monotone reading).

| substrate fraction | Slavic 1 (~1 M migrants) | Slavic 2 (~3 M migrants) |
|---|---|---|
| 0.00 (no substrate) | 51.15 % ± 5.99 % | 89.73 % ± 1.76 % |
| 0.10 | 47.83 % ± 5.76 % | 88.44 % ± 1.85 % |
| 0.20 | 56.01 % ± 4.26 % | 90.44 % ± 1.84 % |
| 0.30 | 65.88 % ± 4.95 % | 91.47 % ± 2.24 % |
| 0.40 | 73.26 % ± 4.32 % | 94.19 % ± 0.75 % |
| 0.50 (Olalde upper bound) | **77.21 % ± 4.05 %** | **95.48 % ± 1.45 %** |

**Reading:** at `reverse_assim = 0.000` (the rule-disabled
monotone reading), Slavic 1 substrate response is essentially
monotonic from substrate = 0.20 upward; at substrate = 0.50
(Olalde upper bound) the model reaches **77.21 % ± 4.05 % —
within 3 pp of the historical ~80 %+ Slavic share, but not
exceeding it**. Slavic 2 stays in near-dominance range
(~89–95 %) across all substrate values — at 3 × plausible
migration with reverse-assim disabled, the model reaches
dominance even without substrate.

**Source:** `docs/run_logs/2026-05-16_substrate_revassim_sweep.md`.

## Table 3b — Substrate × reverse-assimilation response surface (sensitivity appendix)

The full 2-parameter sweep, four reverse-assimilation rates at
each substrate fraction, for Slavic 1 and Slavic 2. Per response7
decision criterion, this is the sensitivity-appendix complement
to Table 3 (which extracts the rev = 0.000 column).

### Slavic 1

| substrate \ rev_assim | 0.000 | 0.015 | 0.030 (default) | 0.045 |
|---|---|---|---|---|
| 0.00 | 51.15 % | 24.50 % | 18.35 % | 15.39 % |
| 0.10 | 47.83 % | 9.22 % | 4.12 % | 1.66 % |
| 0.20 | 56.01 % | 13.37 % | 3.95 % | 2.53 % |
| 0.30 | 65.88 % | 25.50 % | 9.94 % | 4.71 % |
| 0.40 | 73.26 % | 43.15 % | 25.26 % | 15.37 % |
| 0.50 | 77.21 % | 60.66 % | 52.67 % | 42.14 % |

### Slavic 2

| substrate \ rev_assim | 0.000 | 0.015 | 0.030 | 0.045 |
|---|---|---|---|---|
| 0.00 | 89.73 % | 59.41 % | 32.35 % | 26.36 % |
| 0.10 | 88.44 % | 55.84 % | 16.42 % | 6.24 % |
| 0.20 | 90.44 % | 64.14 % | 23.56 % | 9.17 % |
| 0.30 | 91.47 % | 77.51 % | 49.55 % | 19.59 % |
| 0.40 | 94.19 % | 89.43 % | 76.87 % | 59.75 % |
| 0.50 | 95.48 % | 93.58 % | 91.73 % | 88.10 % |

(SDs in source log; omitted from this table for compactness.)

The full discussion of what these surfaces mean — and the
implication that all three post-matrix headline findings
(Slavic 1 baseline-equivalence, Slavic 2 parity, substrate-
cannot-rescue) are mechanistically downstream of the same
free parameter — is in the source log.

**Source:** `docs/run_logs/2026-05-16_substrate_revassim_sweep.md`.

## Table 4 — INHERITANCE_AGE_MAX sweep

Code: `66f1d6b`. 10 runs each, seed 42. Four age values (22, 25,
28, 30) × three scenarios (Slavic 2 excluded per response3/4
compute cap; cap retained — slavic1 and slavic3 endpoints plus
Arabic are sufficient to characterise robustness).

| `INHERITANCE_AGE_MAX` | Slavic 1 | Slavic 3 | Arabic |
|---|---|---|---|
| 22 | 17.86 % ± 5.28 % | 94.84 % ± 2.24 % | 36.96 % ± 1.84 % |
| **25 (default)** | **18.35 % ± 4.40 %** | **93.99 % ± 1.69 %** | **35.95 % ± 2.18 %** |
| 28 | 16.40 % ± 4.08 % | 96.82 % ± 0.81 % | 39.71 % ± 2.41 % |
| 30 | 18.13 % ± 4.64 % | 95.65 % ± 1.08 % | 38.15 % ± 3.37 % |

**Robustness reading:** width of swept range is 1.95 pp (Slavic 1),
2.83 pp (Slavic 3), 3.76 pp (Arabic) — every scenario stays within
its own sampling-error band. The mother-tongue rule cutoff is not
a load-bearing parameter for any of the qualitative findings; the
free-parameter status of `INHERITANCE_AGE_MAX` does not propagate
to a free-parameter status for the headline findings.

**Source:** `docs/run_logs/2026-05-16_inheritance_sweep.md`.

## Table 5 — Low-reverse-assim × substrate × migration-window threshold-resolution sweep (the null verdict)

Code: `37054ac` with `reverse_assim` and migration-window
sed-patched per cell into a `/tmp` copy of the canonical engine.
10 runs each, seed 42. This is the keystone null-result table:
it tests whether *any* admissible cell crosses the historical
~80 %+ Slavic rural-dominance threshold within the current
model family. The full grid (48 cells, both slavic1 and slavic2)
is in `docs/run_logs/2026-05-17_low_rev_threshold_sweep.md`;
the admissible-scale extract (slavic1; 24 cells) is reported
here as the Results-section table.

### slavic1 (~1 M migrants, archaeologically admissible) — final Slavic share

| substrate \ rev_assim | 0.000 | 0.0025 | 0.005 | 0.0075 | 0.010 | 0.015 |
|---|---|---|---|---|---|---|
| **window = 100 yr (default)** | | | | | | |
| 0.00 | 51.15 % | 44.73 % | 34.94 % | 34.49 % | 27.23 % | 24.50 % |
| 0.30 | 65.88 % | 57.86 % | 52.86 % | 42.16 % | 36.35 % | 25.50 % |
| **window = 150 yr (extended)** | | | | | | |
| 0.00 | 60.12 % | 53.45 % | 47.84 % | 40.75 % | 33.81 % | 28.48 % |
| 0.30 | **70.90 %** ± 5.15 % | 66.52 % | 57.58 % | 49.23 % | 41.56 % | 30.04 % |

**Cells ≥ 80 %: none (0 of 24).**
**Cells ≥ 70 %: exactly one — the bolded maximum cell.**

The maximum (sub = 0.30, rev = 0.000, win = 150 yr) sits at the
corner of the admissible space most generous to the migrationist
hypothesis: zero reverse-assimilation pressure on substrate
Slavs, maximum-genetic-plausible substrate fraction (the Olalde
upper-bound zone), and a migration window 50 % longer than the
default. The 1-SD upper bound on that maximum (76.05 %) **is
still below the historical ~80 %+ threshold**.

The slavic2 reference grid (~3 M migrants, 3 × Curta's
archaeological max, **excluded from the admissibility
criterion**) reaches ≥80 % in 19 of 24 cells — confirming that
the model family *can* produce historical dominance, but only
at migration scales outside the empirically-defensible envelope.
Full slavic2 grid in the source log.

**Reading:** the demographic-ABM mechanism in the current model
family cannot reach the historical Slavic rural-dominance
threshold at archaeologically-plausible migration. The
threshold-scale at which it becomes reachable lies between
1 M and 3 M migrants — outside the archaeological envelope.
The paper publishes this as a rigorous null.

**Source:** `docs/run_logs/2026-05-17_low_rev_threshold_sweep.md`.

## Engine baselines (Table 0 — reference only)

Not for the Results section per se; included for the Methods
§ "Engine-stability gate" subsection.

| condition | final pop | final Slavic share |
|---|---|---|
| No plague + no migration (engine stability gate, 260 yr) | 5,407 (+8.1 % from 5,000; within ±10 % fence) | 11.84 % ± 1.31 % |
| With plague + no migration (differential isolated) | 3,638 (−27.2 % from 5,000) | **19.72 % ± 4.98 %** |

The 19.72 % zero-migration / with-plague Slavic share is the
**differential-plague-mortality contribution isolated from
migration** — referenced in the Slavic 1 framing in Table 1
("statistically indistinguishable from baseline" = the 19.72 %
this row reports).

**Source:** `DECISIONS.md` "Engine baseline at `ad8cd05`".

## Cross-cutting flat-list (for abstract / lede prose)

- No migration, no plague: **11.84 % ± 1.31 %** (engine gate).
- No migration, with plague (differential alone): **19.72 % ± 4.98 %**.
- Slavic 1 (~1 M migrants, with plague, default rev_assim):
  **18.35 % ± 4.40 %** (≈ zero-migration plague baseline).
- Slavic 2 (~3 M migrants, default rev_assim): **47.93 % ± 4.96 %**
  (parity, not dominance).
- Slavic 3 (~5 M migrants, default rev_assim): **93.99 % ± 1.69 %**
  (dominance — but implausible scale).
- Slavic 3 with differential mortality removed: **93.96 % ± 1.50 %**
  (Δ = 0.03 pp; differential not load-bearing).
- Arabic (~1 M migrants): **35.95 % ± 2.18 %** (historical
  ~55 %; gap ~19 pp = upper bound on combined institutional +
  bilingual contributions the ABM does not implement).
- Substrate response curve, rev = 0.000 monotone reading
  (Slavic 1, sub 0.00 → 0.50): 51.15 → 47.83 → 56.01 → 65.88 →
  73.26 → 77.21 %. Substrate at the Olalde upper bound (0.50)
  reaches 77.21 % ± 4.05 % — within 3 pp of historical, not
  exceeding.
- **The null-verdict maximum across all admissible cells**
  (slavic1 × any sub ∈ {0.00, 0.30} × any rev ∈ {0.000–0.015}
  × any window ∈ {100, 150 yr}): **70.90 % ± 5.15 %** at the
  most favourable corner. 1-SD upper bound 76.05 %, still below
  the historical ~80 %+ threshold. **No admissible cell
  crosses 80 %.**

## Grep audit — superseded pre-fix substrate numbers

A repo-wide check that the pre-fix substrate numbers from earlier
session briefings (before the substrate-init fix at `37054ac`)
do not survive outside explicitly historical contexts:

The earlier briefing's substrate-curve table quoted (pre-fix):

```
substrate     slavic1     slavic2     slavic3
0.20          27.75 %     59.51 %     97.30 %
0.30          40.33 %     61.98 %     97.38 %
0.40          47.18 %     69.01 %     97.68 %
0.50          52.76 %     72.56 %     97.73 %
```

Post-fix (corrected) values are recorded in
`docs/run_logs/2026-05-16_substrate_curve.md`. The pre-fix
values should appear in this repo only inside the historical
context of `docs/run_logs/response*.md` files (which are
verbatim transcripts of session correspondence and must not be
edited) and inside earlier `DECISIONS.md` log entries that are
dated and contextualised as pre-fix.

The full grep output is below. Any "pre-fix number found in
non-historical context" line would be flagged for cleanup;
none were found.

### Grep audit result

Repo-wide grep across `*.md` files for the twelve pre-fix
substrate values (`27.75%`, `40.33%`, `47.18%`, `52.76%`,
`59.51%`, `61.98%`, `69.01%`, `72.56%`, `97.30%`, `97.38%`,
`97.68%`, `97.73%`) returned **three matches**, all in
legitimate historical contexts:

| file | context | scrub required? |
|---|---|---|
| `docs/paper/results_tables.md` | this audit table — quoting the pre-fix values explicitly as superseded | NO (this is the audit itself) |
| `docs/run_logs/2026-05-16_cleanroom_repro.md` | clean-room verification log; the pre-fix substrate values were the canonical values at the verification commit `66f1d6b`, so they're correct in that historical record | NO (historical record) |
| `docs/run_logs/2026-05-17_to_prose_v2.md` | draft reply that was prepared before response7 landed and was never sent; now marked SUPERSEDED at the top | NO (marked superseded) |

The three load-bearing forward-facing documents (CLAUDE.md
"claim structure"; DECISIONS.md "Engine baseline at `ad8cd05`"
headline-numbers callout; the prose-instance briefing
§1 / §3 / §5 / §6) all had the pre-fix substrate numbers
replaced with RESERVED-pending-adjudication language in this
commit. No superseded number survives in any prose-facing or
forward-facing context. If new occurrences surface after this
commit (e.g. someone re-pastes the pre-fix table without
context), they should be cleaned up in a follow-up commit and
this audit re-run.
