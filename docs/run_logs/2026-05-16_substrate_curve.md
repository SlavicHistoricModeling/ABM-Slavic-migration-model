# Batch 2 — substrate response curve (POST-FIX, raw data)

> Substrate fraction sweep (0/10/20/30/40/50 %) across the three
> Slavic scenarios, **re-run on the post-substrate-fix engine at
> commit `37054ac`**. 10 runs each, seed 42. Phase 3 of the
> two-substrate-defect re-run (per response5 step 2 audit).
>
> **Interpretive framing is FROZEN per response7 step 2** pending
> the substrate × reverse-assimilation 2-parameter adjudication
> sweep currently running. This log records the per-fraction
> numbers as raw data only; the directional reading (whether the
> shape is a finding or an artifact of the ungrounded
> reverse_assim parameter) will be added after the sub × rev
> sweep completes and the decision criterion in
> `docs/run_logs/2026-05-16_substrate_revassim_sweep.md`
> resolves.

## Provenance

- Code: `slavic_migration_submited_v1.py` at commit `37054ac`
  (substrate-init fix: substrate Slavs placed in Balkans;
  non-Slavic fractions normalised to sum to 1.0).
- Random seed: 42 uniformly.
- Runs per pair: 10.
- Sweep script: `scripts/run_substrate_curve.sh`.
- Wall time: ~12 hrs wall clock (includes an overnight system
  suspension; clean cadence was ~3 hrs without suspension).
- Output files: `results_substrate_<scenario>_<fraction>.txt`
  (gitignored).
- Arabic excluded: substrate is a Slavic-specific concept; the
  code only mutates the slavic group's initial_fraction.

## Configuration relative to pre-fix run

Pre-fix substrate runs (recorded in earlier sessions, now
superseded) had two implementation defects (per
`docs/run_logs/2026-05-16_code_audit.md`):

- 1.1 The slavic group's `initial_fraction` was raised when
  `--substrate` was set, but the other groups' fractions were
  not scaled. Total initial population inflated up to 40 % at
  substrate = 0.50.
- 1.2 Substrate Slavs were placed in eastern / central regions
  (migration source), not in the Balkans (migration destination).

Post-fix configuration:
- Slavic initial_fraction = substrate_fraction (the swept value).
- Non-Slavic group fractions scaled by `(1 − s) / 0.9` so the
  total sums to 1.0 (preserving the relative ratios:
  illyrian : greek : germanic : avar : other = 3:2:2:1:1).
- Slavic agents placed in the Balkans only when `--substrate` is
  set (regions = ["balkans"]).

## Raw results — final Slavic share by substrate × scenario

| substrate fraction | slavic1 (~1 M migr) | slavic2 (~3 M migr) | slavic3 (~5 M migr) |
|---|---|---|---|
| 0.00 (no --substrate; default placement) | 18.35 % ± 4.40 % | 47.93 % ± 4.96 % | 93.99 % ± 1.69 % |
| 0.10 | 4.12 % ± 3.09 % | 34.55 % ± 5.20 % | 94.69 % ± 1.82 % |
| 0.20 | 3.95 % ± 2.49 % | 51.53 % ± 5.83 % | 96.11 % ± 0.68 % |
| 0.30 | 9.94 % ± 5.94 % | 68.04 % ± 7.20 % | 97.47 % ± 0.54 % |
| 0.40 | 25.26 % ± 7.76 % | 86.47 % ± 3.48 % | 98.23 % ± 0.63 % |
| 0.50 | 52.67 % ± 8.08 % | 93.36 % ± 1.33 % | 98.53 % ± 0.38 % |

The 0.00 row is the no-`--substrate` baseline (default
eastern / central placement of the standard 0.1 Slavic fraction)
and is identical to the matrix-batch-1 entry for each scenario
— confirming the fix does not affect non-substrate runs.

## Shape observations (description only — no interpretation)

The slavic1 column is **non-monotonic** across the swept
substrate range: 18.35 at 0.00, ~4 at 0.10–0.20, then
climbing through 0.30 → 0.50.

The slavic2 column is also **non-monotonic**: 47.93 at 0.00,
34.55 at 0.10, climbing through 0.20 → 0.50 to reach 93.36.

The slavic3 column is **monotonic** and shows small effect
(93.99 → 98.53 across the full range) — slavic3 is at near-
saturation from migration alone and the substrate adds at
most ~5 pp.

## Interpretive framing — RESERVED

Per response7 step 2:

> "Do not finalise `docs/run_logs/2026-05-16_substrate_curve.md`
> with directional language. The corrected per-fraction numbers
> can be recorded as raw data; the *interpretation* waits for
> step 1 [the sub × rev_assim sweep]."

The non-monotonic shape of the slavic1 and slavic2 columns is
**mechanistically downstream of the reverse-assimilation rule**,
which has `reverse_assimilation_rate` as a labelled **free
parameter** with no independent empirical grounding (see
`docs/paper/parameter_table.md`). The substrate × reverse-assim
2-parameter sweep at `scripts/run_substrate_revassim_sweep.sh`
adjudicates whether the observed shape:

- (a) **persists at reverse_assim = 0.000**: a structural finding
  about substrate dynamics independent of the ungrounded
  parameter, *or*
- (b) **flattens or inverts as reverse_assim → 0**: an artifact
  of the ungrounded parameter, becoming a Discussion observation
  conditioned on the reverse_assim assumption rather than a
  Results finding.

The decision criterion outcome will be recorded in
`docs/run_logs/2026-05-16_substrate_revassim_sweep.md` once the
2-parameter sweep completes (~3 hrs wall time after launch).

Until that adjudication lands, no directional language attaches
to these numbers in the prose-instance briefing or any other
paper-facing artefact. This durable log holds the raw data only.

## Cross-cut against empirical envelopes (raw, no
directional reading)

Two empirical envelopes are relevant to the eventual
interpretive reading:

- **Migration envelope** (Curta 2001): total Slavic migrants
  ≤ ~2 M (archaeologically defensible upper bound).
  - slavic1 (~1 M) is within envelope.
  - slavic2 (~3 M) is 3 × envelope (outside).
  - slavic3 (~5 M) is 5 × envelope (outside).
- **Substrate envelope** (Olalde 2023): Slavic-related ancestry
  in modern Balkan populations ~30–60 % (bounds genetic
  admixture, not initial substrate fraction directly).

Per-cell flag whether the (migration, substrate) combination
sits inside both envelopes:

| substrate | slavic1 in env? | slavic2 in env? | slavic3 in env? |
|---|---|---|---|
| 0.30 | yes (s ≤ 0.6, migr ≤ 2 M) | no (migr ~3 M outside) | no (migr ~5 M outside) |
| 0.50 | yes | no | no |
| 0.60 (not swept) | yes | no | no |

This cross-cut is recorded for completeness; interpretation
defers as above.

## Determinism cross-check

The 0.00 column for each scenario (no `--substrate`) reproduces
the matrix-batch entry digit-exact:

| scenario | matrix entry | substrate-curve 0.00 entry | match? |
|---|---|---|---|
| slavic1 | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ EXACT |
| slavic2 | 47.93 % ± 4.96 % | 47.93 % ± 4.96 % | ✓ EXACT |
| slavic3 | 93.99 % ± 1.69 % | 93.99 % ± 1.69 % | ✓ EXACT |

Reproducibility confirmed: the substrate fix is contained inside
`if substrate:` and does not affect runs where the flag isn't
passed.

## Status

- Raw data: recorded above (this commit).
- Interpretive framing: pending sub × rev_assim sweep
  adjudication (see queued log
  `docs/run_logs/2026-05-16_substrate_revassim_sweep.md`).
- Prose-instance briefing §3: will be updated *after*
  adjudication, with framing matched to whichever outcome
  the decision criterion produces.
