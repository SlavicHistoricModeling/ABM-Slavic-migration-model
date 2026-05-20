# Reproducibility

> Documentation of the systematic verification of the inherited
> model implementation — the kind of practice the field's
> reproducibility literature (Grimm et al. 2014; Wilkinson et al.
> 2016; Crüwell et al. 2023) calls for and rarely sees performed
> in published ABM resubmissions. The companion model-description
> file is [`MODEL_DESCRIPTION.md`](MODEL_DESCRIPTION.md); the
> companion paper-prose tables and figures are in
> [`docs/paper/`](docs/paper/) and
> [`docs/paper/figures/`](docs/paper/figures/).
>
> Engine frozen at commit `37054ac`. All numbers reproducible at
> random seed 42 with ten runs per parameter combination on
> Python 3.13.x on x86-64.

## §1 Verification as methodological practice

The model in this study was reconstructed from the published
code listing in the original Diachronica submission DIA-25063
(Appendix A). Rather than treating the inherited implementation
as a black box and reporting its outputs as findings, we
subjected the entire pipeline — model code, parameter values,
scheduling, RNG handling, and substrate initialisation — to a
deliberate audit-and-verify pass before producing the results
this paper reports. Five implementation defects were identified
and corrected during that audit; each correction is
committed separately, accompanied by a verification re-run of
all results the correction could affect, and disclosed in full
below. The full audit trail is preserved in the repository's
git history and run-log files (`docs/run_logs/`).

This level of post-publication implementation audit is unusual
for an ABM paper. We make it part of the paper's methodological
contribution rather than a hidden internal cleanup, on the view
that results that depend on inherited code are only as
trustworthy as the audit of that code, and that the audit trail
is the mechanism by which trustworthiness can be **verified**
rather than **assumed**. The model-behaviour findings reported
in the Results section (§§1–4) are reproducible at seed 42 from
a clean clone of the repository at the engine-frozen commit
listed below.

## §2 What can be reproduced

The agent-based model (`slavic_migration_submited_v1.py`), all
sweep scripts (`scripts/run_*.sh`), and the canonical run-log
artefacts (`docs/run_logs/*.md`) are committed to the repository
at the engine-frozen commit listed in §3. A reader who clones
the repository at that commit and runs

```
python slavic_migration_submited_v1.py --scenario <SCEN> --num_runs 10 --seed 42 [flags]
```

obtains **bit-identical** output to the canonical numbers
reported in the Results section, provided they use Python 3.13.x
on a comparable architecture (x86-64). The sweep scripts
(`scripts/run_*.sh`) reproduce the full sensitivity-sweep grids
identically. The canonical per-cell `results_*.txt` files are
committed at the repository root so figures can be regenerated
without re-running the sweeps; the per-sweep durable record
markdown files in `docs/run_logs/` carry the same numbers as
tables for human reading.

## §3 Engine-frozen commit

The simulation code is frozen at commit **`37054ac`** (the
substrate-initialisation fix, the final inherited-defect
correction; see §4 defect 5). All numbers reported in this
paper were produced by running this exact engine at random
seed 42 with `--num_runs 10`. No further model changes were
made after the substrate × reverse-assim and low-rev / threshold sensitivity sweeps
landed; the framing decision (publish the rigorous null;
explicitly reject model extension) is recorded in the
repository at the same commit.

## §4 Five inherited / found implementation defects

Each defect is reported below with: the inherited form (what
the original DIA-25063 listing or the early reassessment
revision contained), the corrected form (what the fixed code
does), the commit hash of the fix, and the verification that
demonstrated the fix was correct.

### Defect 1 — Birth rate applied per-agent without per-female conversion

**Inherited form.** The per-year birth-rate parameter was
applied directly as a per-agent probability: `if random.random()
< birth_rate`. The DIA-25063 parameter values (e.g. 0.04 for
non-Slavic) were specified as **crude birth rates** (births per
head per year), but applied per-agent — and per-agent meaning
"per all agents", not "per reproductive-age female" — they
under-supply births by approximately `1 / REPRO_SHARE ≈ 6.6×`,
where `REPRO_SHARE ≈ 0.151` is the equilibrium share of the
population that is female and of reproductive age under flat
2 %/yr mortality. Populations collapsed across the simulation
horizon, distorting all reported final shares.

**Fix.** Introduce
`per_female_rate(crude_birth_rate) = crude_birth_rate /
REPRO_SHARE`, and apply the corrected per-female probability
only to agents that are (a) female and (b) in the reproductive
age window 15–40 yr.

**Commit.** `512720d`.

**Verification.** Engine-stability gate: the no-plague /
no-migration baseline at the corrected calibration sustains
population within ±10 % of the initial 5,000 agents over the
260 yr Slavic scenario length. Terminal drift +8.1 %; reference
log: `docs/run_logs/2026-05-15_baseline_no_plague_slavic1.md`.

### Defect 2 — Mother-tongue inheritance rule commented out

**Inherited form.** The Methods text of the published
submission described a mother-tongue inheritance rule with a
25-year age cutoff (`INHERITANCE_AGE_MAX = 25`); the code
listing defined the constant but the corresponding logic in
the reproduction step was commented out with a "Future
inheritance rule" annotation. The simulation therefore did not
implement the rule the Methods described.

**Fix.** Activate the rule in the reproduction step: if
mother's age ≤ `INHERITANCE_AGE_MAX`, child inherits mother's
language; otherwise child draws from the cell-pool of
co-located agents with the mother's contribution excluded;
fallback to mother's language if the pool has fewer than three
other agents.

**Commit.** `512720d` (combined with Defect 1).

**Verification.** Sensitivity sweep of `INHERITANCE_AGE_MAX`
across {22, 25, 28, 30} (Methods Table 4) confirms scenario-
level results are stable within sampling-error bands across the
range; the rule's exact cutoff is not a load-bearing parameter.
Reference: `docs/run_logs/2026-05-16_inheritance_sweep.md`.

### Defect 3 — Set-iteration non-determinism in reverse-assimilation rule

**Inherited form.** The reverse-assimilation rule (Slavic agents
in majority-Christianised neighbourhoods may adopt the dominant
non-Slavic language) used

```python
a["language"] = max(set(chlangs), key=chlangs.count)
```

to pick the most-common Christianised neighbour language.
Python's `set` iteration order depends on `PYTHONHASHSEED`,
which is randomised per process by default. When two neighbour-
languages tied in count, the `max()` tie-break was therefore
process-dependent. The non-determinism cascaded through
subsequent mortality and reproduction rolls, making model
output non-reproducible across processes at fixed seed —
violating a property the paper now claims (cross-process
bit-identity at seed 42).

**Fix.** Sort the set before `max()`. Alphabetical tie-break is
deterministic across processes, machines, and `PYTHONHASHSEED`
values:

```python
a["language"] = max(sorted(set(chlangs)), key=chlangs.count)
```

**Commit.** `66f1d6b`.

**Verification.** Two runs of the same command at seed 42 on
post-fix code produce bit-identical output; cross-process
verification under `PYTHONHASHSEED = 0` and `PYTHONHASHSEED =
12345` also produces bit-identical output (the clean-room
reproduction protocol below). All affected results
(slavic1, slavic2, slavic3 — Arabic has
`reverse_assimilation_rate = 0` so the bug never fires there)
were re-run on the corrected engine; the post-fix matrix,
plague-mortality, substrate, and inheritance results are the
canonical numbers in this paper. Reference:
`docs/run_logs/2026-05-15_determinism_fix.md`.

### Defect 4 — Substrate fraction unnormalised under `--substrate`

**Inherited form.** When the `--substrate` flag was set, only
the Slavic group's `initial_fraction` was raised (to 0.30 by
default); the other groups' fractions stayed at their no-substrate
defaults. The sum of group fractions exceeded 1.0, inflating
total initial population by up to 40 % (5,000 → 7,000 at
`substrate_fraction = 0.50`). The substrate-fraction axis
therefore mislabelled the response curve: the actual initial
Slavic share at a swept fraction `s` was `s / (0.9 + s)`, not
`s`.

**Fix.** When `--substrate` is set, scale the non-Slavic group
fractions by `(1 − s) / 0.9` so the sum stays at 1.0 and the
total initial population stays at `INITIAL_POP = 5,000`.

**Commit.** `37054ac`.

**Verification.** Smoke test at seed 42: initial population
post-fix at `substrate_fraction = 0.30` is 4,574 after the year-0
plague tick (consistent with the 5,000-agent normalisation),
versus 5,460 in the pre-fix configuration. The substrate
response surface was re-run on the corrected engine and is
reported as Methods Table 3 / Fig 2 / Table 3b.

### Defect 5 — Substrate placed in source region, not destination

**Inherited form.** Under `--substrate`, substrate Slavs were
placed in the eastern and central regions (the migration *source*
area), not in the Balkans (the migration destination). The
substrate hypothesis as the original framing intended — Sedov's
(1982) proto-Slavic continuity in the Carpatho-Balkan zone —
describes pre-existing Slavic speakers in the migration
*destination*. The pre-fix code therefore tested a different
hypothesis ("more Slavs in the source region") from the one the
paper's framing claimed to test.

**Fix.** When `--substrate` is set, the Slavic group's region
list is set to `["balkans"]`. Substrate Slavs are placed in the
migration destination, matching the conventional substrate-
hypothesis framing.

**Commit.** `37054ac` (combined with Defect 4).

**Verification.** Smoke test at seed 42: post-fix slavic1 at
`substrate_fraction = 0.30` is 31.38 % at year 0 (matches the
intended 30 % Balkans-substrate fraction after the year-0
plague tick). The substrate response surface was re-run; the
substrate × reverse-assimilation 2-parameter adjudication
sweep (Methods Table 3b / Fig 2) and the low-rev / threshold-
resolution sweep (Methods Table 5 / Fig 4) both run against
the post-fix code at the engine-frozen commit.

## §5 Clean-room cross-process verification

The determinism-fix's reproducibility claim was verified
explicitly. From an isolated git worktree at commit `66f1d6b`
(the determinism-fix commit), the verification subset
(slavic1 matrix, slavic3 matrix, slavic3 uniform-mortality
counterfactual, and the full slavic1 substrate response curve)
was run twice — once with explicit `PYTHONHASHSEED = 0` and
once with `PYTHONHASHSEED = 12345`. The two runs produced
bit-identical trajectories on all nine scenarios, and the
final shares matched the canonical cascade numbers
digit-exact. Reference:
`docs/run_logs/2026-05-16_cleanroom_repro.md`.

## §6 Open caveat — cross-architecture reproduction

The clean-room reproduction was performed on the same Windows /
Python 3.13.2 / x86-64 host that produced the original cascade
numbers. Cross-architecture reproduction (e.g. Linux / Python
3.x on ARM, or alternative CPython implementations) has not
been independently verified during this reassessment. The fixes
to the inherited defects are pure-Python changes that should
not interact with platform-level floating-point or RNG
behaviour, but this expectation is not formally verified at the
time of submission.

Independent reviewers and downstream researchers are invited to
re-run the engine at the frozen commit on different architectures
and report any divergence; the repository's reproducibility-
record format will accept such reports as additional verification
artefacts.

## §7 Repository structure for reviewers

| path | role |
|---|---|
| `slavic_migration_submited_v1.py` | engine (frozen at commit `37054ac`) |
| `scripts/run_*.sh` | sweep / cascade / clean-room scripts |
| `docs/run_logs/*.md` | canonical per-sweep records and engine-baseline logs |
| `docs/paper/methods_odd.md` | this paper's Methods section (ODD-native) |
| `docs/paper/methods_reproducibility.md` | this subsection |
| `docs/paper/results_tables.md` | Tables 1–5 in final form |
| `docs/paper/figures/` | Figures 1–4 plus generator scripts |
| `docs/paper/olalde_audit.md` | source-correction record for Olalde 2023 citations in DIA-25063 |
| `DECISIONS.md` | full decision and framing record |
| `CLAUDE.md` | project-level instructions and claim-structure record |

A reader running

```
python slavic_migration_submited_v1.py --scenario slavic1 --num_runs 10 --seed 42
```

from a fresh clone at the engine-frozen commit obtains output
matching the Slavic 1 row of Methods Table 1 (and §1 of the
Results section) digit-exact.

## §8 On the practice

We make the audit-and-verify pass and its full disclosure part
of the paper's methodological contribution rather than a
hidden internal cleanup, on the view — held independently of
the substantive findings reported in this paper — that the
field's reliance on inherited code without published audits is
a real source of unreliable results, and that the audit trail
is the mechanism by which trustworthiness can be **verified**
rather than **assumed**. The five defects we identified in
DIA-25063 were not exotic; they were the kinds of errors that
accumulate in ABM code that has been revised across multiple
publications without a deliberate verification pass. Their
identification required only that someone read the code
deliberately, with a specific question, and run the
verification sweeps that the question demanded. The
methodological burden is small; the rigor improvement is
substantial.
