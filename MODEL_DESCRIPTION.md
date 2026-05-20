# Model Description — ODD Protocol

> Model description in the ODD-protocol form of Grimm et al.
> (2006, 2010, 2020): the seven elements in order, with parameter
> material located in the Input data and Submodels elements per
> the protocol's convention. This document is the model-side
> companion to [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md), which
> documents the engine's verification audit and the five
> inherited implementation defects identified and corrected
> during the reassessment.
>
> Engine frozen at commit `37054ac`. All numbers in the paper
> are reproducible at random seed 42 with ten runs per
> parameter combination on Python 3.13.x on x86-64. The
> companion paper-prose tables and figures are in
> [`docs/paper/`](docs/paper/) and
> [`docs/paper/figures/`](docs/paper/figures/).

## §1 — Purpose and patterns (ODD element 1)

### Purpose

This is a model-behaviour study of a Kandler-family demographic
ABM, motivated by the Slavic case and calibrated against the
Arabic case. The paper's primary contribution is a
characterisation of what the demographic mechanism in this model
family can and cannot produce across its parameter space, and a
systematic verification of an inherited published implementation.
The historical Slavic linguistic-expansion question motivates the
parameter ranges and the calibration target, but the paper's
stated subject is the model's behaviour rather than the
historical event.

### Patterns the model is required to reproduce

The model is required to clear two engine-stability patterns
before any scenario claim is made:

1. **No-plague / no-migration stationarity.** Under
   `--no_plague --migration_override 0`, the population must
   sustain within ±10 % of the initial 5,000 agents across the
   260-year Slavic scenario length. Confirmed at commit
   `ad8cd05`: terminal drift +8.1 %.
2. **With-plague depression (observed, not validated against).**
   Under the configured differential plague mortality (15 %
   non-Slavic, 4 % Slavic, compounded over three plague years),
   the no-migration population settles at approximately 73 % of
   initial. This is reported as a model output, not a
   validation target — the differential-mortality parameter
   itself is one of the things being studied.

The Arabic-case calibration is **not** a pattern the model is
required to match. On the corrected engine, the model produces
~36 % Arabic linguistic share at year 170 against the historical
~55 % observed share. The ~19 pp gap is interpreted in the
Results as an upper bound on the combined contribution of
mechanisms the ABM does not implement (institutional
reinforcement and bilingual transitional states).

## Methods §2 — Entities, state variables, and scales (ODD element 2)

### Entity types

Two entity types: **agents** (representing local population
aggregates) and **grid cells** (representing spatial locations).

### Agent state variables

| Variable | Range / type | Role |
|---|---|---|
| `id` | integer | Unique stable identifier (used for start-of-year language snapshots — see §3). |
| `x`, `y` | integers in `[0, GRID_SIZE)` | Cell coordinates on a toroidal 50 × 50 grid. |
| `language` | one of {slavic, illyrian_thracian, greek, germanic, avar, other} | Language label; changes through assimilation. |
| `age` | integer in `[0, MAX_AGE]` | Initialised from the equilibrium geometric distribution under flat 2 % / yr mortality; incremented by 1 each tick. |
| `sex` | {male, female} | Determines reproductive eligibility. |

Each agent represents approximately 1,000 individuals: 5,000
agents ≈ 5 M pre-migration Balkan population at scenario start.

### Cell state variables

Grid cells hold a list of resident agent IDs. Each cell is
implicitly labelled with one of three **regions** (`balkans`,
`central`, `eastern`) determined by `(x, y)` position. The
region partition constrains which initial groups can be placed
where.

### Environmental variables (global)

| Variable | Value | Role |
|---|---|---|
| Current year offset | `[0, params["years"])` | Drives plague-year mortality switching and the 50-yr Slavic-newcomer fertility depression window. |
| `PLAGUE_YEARS` | `[0, 10, 25]` (Slavic) / `[0, 10]` (Arabic) | Scenario-relative years in which the alternate `plague_mortality` applies. |

### Spatial and temporal scales

- **Spatial extent**: 50 × 50 toroidal grid = 2,500 cells.
- **Spatial resolution**: one cell ≈ 2,000 individuals at the
  canonical 1:1000 scaling.
- **Temporal extent**: 260 yr (Slavic scenarios, 600–860 CE) or
  170 yr (Arabic, 630–800 CE).
- **Temporal resolution**: one year per tick.

## Methods §3 — Process overview and scheduling (ODD element 3)

### Tick (one model year) — process order

Each tick proceeds in the following order:

1. **Migration** (years 0–99 only). Add `migration_rate` Slavic
   agents per year at random coordinates in the eastern half of
   the grid (Slavic scenarios) or anywhere (Arabic). Migrant
   ages uniform on [15, 40]; sex random.
2. **Start-of-year snapshots**. Build two dictionaries from the
   current agent list: `cell_langs` (cell → list of languages
   present) and `agent_id_to_lang` (id → language). These
   snapshots fix the language landscape for the rest of the
   tick so within-tick processing is order-independent.
3. **Per-agent updates** (single pass through the agent list):
   age increment; mortality roll; reproduction (with the
   mother-tongue rule for child-language assignment, §7);
   assimilation (two-way: forward Slavic-adoption and reverse
   Christianised-non-Slavic-adoption, §7).
4. **Bookkeeping**. Born + migrated agents appended; dead
   agents removed. Per-year share and population recorded.

### Run structure

Each scenario runs `args.num_runs` independent runs (10 for the
headline matrix and all sensitivity sweeps), each seeded
deterministically from `args.seed = 42`. Reported outputs are
per-year means and standard deviations across runs.

### Within-tick ordering and the start-of-year snapshot design

The start-of-year snapshots are a deliberate scheduling choice:
they make within-tick processing order-independent (an agent
processed late in the agent-list pass sees the same language
landscape as one processed early). They also reduce the
assimilation neighbour scan from O(*n*²) to O(*n* · *k*), where
*k* ≤ ~30 is the Moore-neighbourhood agent count at canonical
scale.

## Methods §4 — Design concepts (ODD element 4)

### Basic principles

The model encodes the standard demographic-ABM frame (Kandler
2009; Kandler and Steele 2008) — births, deaths, local copying —
with three model-family-specific additions:

1. **Migration as exogenous input**, not a derived dynamic.
   The migration rate is a scenario parameter; the model studies
   *consequences* of migration sizes, not their endogenous
   determination.
2. **Reverse assimilation**. Slavic agents in majority-
   Christianised neighbourhoods can adopt the dominant
   non-Slavic language — the symmetric counterpart to Slavic
   assimilation. Absent from prestige-biased models that assume
   one-way drift toward the high-status language.
3. **Mother-tongue rule with a sociolinguistic threshold**.
   Younger mothers transmit their own language; older mothers'
   children draw language from the local community.

### Emergence

The scenario-end Slavic share is the emergent quantity of
interest. It is not programmed in; it falls out of the per-tick
balance among migration inflow, plague-mortality differential,
fertility differential, mother-tongue draws, and two-way
assimilation flux.

### Adaptation, objectives, fitness, learning

None. Agents have no objectives and do not optimise. Birth,
death, and language-switch are stochastic events governed by
per-tick probabilities.

### Sensing

Each agent senses only its own state and the Moore-neighbourhood
language composition (via the start-of-year snapshot).

### Interaction

Local. Assimilation is the only cross-agent interaction and
operates within the 8 Moore-cell neighbourhood. Births deposit
the new agent in the mother's cell; migration deposits the new
agent in a random cell of the entry region.

### Stochasticity

All within-tick events (mortality, birth, language switch,
mother-tongue cell-pool draw, migration entry coordinates) are
stochastic. Random seed (`args.seed`, default 42) makes runs
fully reproducible; reported uncertainty is mean ± SD across
`args.num_runs` independent runs.

### Collectives

The implicit collective is **group** (the six language labels),
which determines per-group birth rate, plague mortality, region
eligibility, and Christianisation status. Groups have no
positional identity beyond their members.

### Observation

Per-year per-run population and per-year per-run Slavic share.
Outputs are written per scenario to `results_<scenario>.txt`
with checkpoints at year offsets {0, 25, 50, 100, 150, 200, 260},
both as mean ± SD across runs.

## Methods §5 — Initialization (ODD element 5)

### Grid and agent placement

5,000 agents are placed at scenario start. Each agent is
assigned a group by the initial-fraction allocation (§6), then
placed at random `(x, y)` coordinates with rejection sampling
to enforce region eligibility:

- Illyrian-Thracian, Greek: Balkans only.
- Germanic: central or Balkans.
- Avar: Balkans or central.
- Other: eastern only (Slavic scenarios); eastern (Arabic
  scenario, where "other" carries the majority initial fraction
  representing the pre-migration Caliphal population).
- Slavic: eastern or central (no-substrate default); Balkans
  only when `--substrate` is set.

### Initial ages

Ages are drawn from `min(MAX_AGE, expovariate(BASE_MORTALITY))`
— the equilibrium geometric distribution under flat 2 % / yr
mortality. This replaces an earlier uniform-age initialisation
that produced a ~24 % drift transient over 260 yr; the
geometric initialisation reduces the drift to within ±10 % (see
the engine-stability pattern in §1).

### Sex

Random uniform {male, female} per agent.

### Substrate option

When `--substrate` is set, the initial Slavic fraction is raised
to the swept substrate-fraction value (default 0.30; sensitivity
range 0.10–0.50 per the substrate response surface), Slavic
agents are placed in the Balkans region, and the non-Slavic
group fractions are scaled to preserve the total at 1.0. This
implements the proto-Slavic substrate hypothesis (Sedov 1982 —
pre-existing Slavic speakers in the Balkans) for the
substrate-response-curve experiments. See `methods_reproducibility.md`
for the substrate-initialisation defect history and fix.

## Methods §6 — Input data (ODD element 6)

The model takes no exogenous time-series inputs. All inputs are
fixed scalar parameters or scenario-defined parameter sets,
listed in §7.1 of the parameter table below. Sources for the
parameter values are summarised here; the full per-parameter
justification with empirical / structural / free-parameter
status is in §7.

### Initial group fractions

| Scenario start | slavic | illyrian_thracian | greek | germanic | avar | other |
|---|---|---|---|---|---|---|
| 600 CE (Slavic) | 0.10 | 0.30 | 0.20 | 0.20 | 0.10 | 0.10 |
| 630 CE (Arabic) | 0.05 | 0.00 | 0.00 | 0.00 | 0.00 | 0.95 |

Substrate variant: the 600-CE Slavic fraction is raised to the
swept value (default 0.30) and the non-Slavic fractions scaled
by `(1 − s) / 0.9` to preserve total = 1.0.

Sources: ethnographic-historical reconstruction (Curta 2001;
Barford 2001); population scale from demographic-history
sources (Russell 1987). The DIA-25063 listing mis-sourced the
population scale to Olalde 2023 and Ralph & Coop 2013 — both
ancestry-composition studies, not demographic-count sources;
the correction is documented in `docs/paper/olalde_audit.md`.

### Per-scenario parameter inputs

| Parameter | slavic1 | slavic2 | slavic3 | arabic |
|---|---|---|---|---|
| `migration_rate` (yr⁻¹, first 100 yr) | 10 | 30 | 50 | 10 |
| `slavic_assimilation_rate` | 0.005 | 0.01 | 0.02 | 0.02 |
| `reverse_assimilation_rate` | 0.03 | 0.02 | 0.015 | 0.0 |
| `CBR_SLAVIC` (per head·yr) | 0.021 | 0.023 | 0.025 | 0.022 |
| `non_slavic_plague_mortality` | 0.15 | 0.15 | 0.20 | 0.12 |
| Scenario length (yr) | 260 | 260 | 260 | 170 |

All non-Slavic groups use `CBR_NON_SLAVIC = 0.020` per
head·year. `BASE_MORTALITY = 0.02 / yr` uniformly. Slavic plague
mortality is fixed at 0.04 (or, under `--uniform_mortality`,
raised to match `non_slavic_plague_mortality` — a counterfactual
used in the uniform-mortality run reported in Results).

## Methods §7 — Submodels (ODD element 7)

This section describes each submodel in turn and gives the full
parameter justification table for the model's free, weakly-
grounded, well-grounded, and structural parameters. Sensitivity
sweeps that exercise each free parameter are noted at the end
of each submodel description and tabulated in §7.7.

### §7.1 Submodel — initial population placement

See §5 (Initialization) above for the rejection-sampling
procedure. Two parameters control this submodel:

| Parameter | Value | Basis | Status | Sensitivity |
|---|---|---|---|---|
| `INITIAL_POP` | 5,000 agents | One agent ≈ 1,000 individuals; ~5 M pre-migration Balkan population (Russell 1987). | structural | Not swept; scenario population trajectories are reported as model outputs. |
| `GRID_SIZE` | 50 × 50 | Computational tractability; one cell ≈ 2,000 individuals. | structural | Not swept. |
| Initial-age distribution | `min(MAX_AGE, expovariate(BASE_MORTALITY))` | Equilibrium age distribution under flat mortality. | structural | Not swept (its purpose is to remove a transient, not be a tunable). |

### §7.2 Submodel — crude-birth-rate to per-female calibration

Birth rolls are per reproductive-age female per year. Naïvely
applying a crude birth rate (CBR ≈ 2 %) per female would
under-supply births by a factor of ~6.6, because the share of
the population that is female and aged 15–40 at equilibrium
under flat 2 %/yr mortality is

```
REPRO_SHARE = 0.5 × Σ_{a=15..40} 0.98^a / Σ_{a=0..∞} 0.98^a ≈ 0.151.
```

The model therefore exposes a CBR constant per group
(`CBR_NON_SLAVIC = 0.020`, `CBR_SLAVIC[scenario]`,
`CBR_SLAVIC_NEW = 0.011`) and converts via
`per_female_rate(cbr) = cbr / REPRO_SHARE`. The conversion is
verified by the engine-stability pattern in §1.

| Parameter | Value | Status | Sensitivity |
|---|---|---|---|
| `REPRO_AGE_MIN`, `REPRO_AGE_MAX` | 15, 40 | well-grounded (Russell 1987) | Not swept. |
| `BASE_MORTALITY` | 0.02 / yr | well-grounded (Russell 1987) | Implicit in CBR calibration. |
| `REPRO_SHARE` | 0.151 | structural (derived) | Not swept. |
| `CBR_NON_SLAVIC` | 0.020 | well-grounded | Not swept (kept at replacement). |
| `CBR_SLAVIC[scenario]` | 0.021 / 0.023 / 0.025 / 0.022 | weakly grounded | The four scenarios vary the Slavic-group CBR across a narrow range above the non-Slavic replacement value (`CBR_NON_SLAVIC = 0.020`); the advantage is order-of-magnitude consistent with cross-population CBR variation in Russell (1987). Not directly swept; the sensitivity-to-fertility-advantage analysis is implicit in the matrix scenarios themselves (slavic1 / slavic2 / slavic3 span the migration-rate dimension at a fixed modest CBR advantage). |
| `CBR_SLAVIC_NEW` | 0.011 / yr (first 50 yr after settlement) | weakly grounded | Implicit in the 50-yr window; deliberate conservatism (tilts against migrationist claim). |

### §7.3 Submodel — plague mortality

In years listed in `PLAGUE_YEARS`, the per-agent mortality roll
uses the agent's group `plague_mortality` instead of
`BASE_MORTALITY`. The Slavic group has 0.04 vs. the non-Slavic
0.15 / 0.20 differential. Under `--uniform_mortality`, the
Slavic group's plague mortality is raised to the non-Slavic
value — a counterfactual that isolates how much of the Slavic
share depends on the mortality differential vs. on migration
and assimilation alone.

| Parameter | Value | Status | Sensitivity |
|---|---|---|---|
| `PLAGUE_YEARS` | [0, 10, 25] (Slavic) / [0, 10] (Arabic) | well-grounded (Justinianic-plague chronology) | Not swept. |
| `non_slavic_plague_mortality` | 0.15 (slavic1/2/arabic ≈ 0.12) / 0.20 (slavic3) | weakly grounded (Procopius lower envelope; **Mordechai et al. 2019 contests the plague-maximalist literature**) | **Swept** ∈ {0.10, 0.12, 0.15, 0.20} (Table 2 / Fig 3). |
| Slavic plague mortality | 0.04 | **free parameter** (differential has no independent empirical anchor) | Counterfactual `--uniform_mortality` reported alongside the matrix; contributes only 0.03 pp to the slavic3 result. |

### §7.4 Submodel — migration

For each year in [0, 100), `migration_rate` Slavic agents are
inserted. Insertion coordinates are uniform over the eastern
half of the grid (Slavic scenarios) or the full grid (Arabic).
Each inserted migrant has uniform age in [15, 40] and random
sex. Total migrants over the scenario window: `migration_rate ×
100`; for slavic1 this is 1,000 agents = ~1 M individuals at
canonical scaling.

| Parameter | Value | Status | Sensitivity |
|---|---|---|---|
| `migration_rate` | scenario-defined (10, 30, 50, 10) | well-grounded (as a spectrum; Curta 2001 archaeological maximum ≈ slavic1) | Sweep is the scenarios themselves. |
| Migration window | 100 yr | weakly grounded | **Swept** ∈ {100, 150} yr (Table 5 / Fig 4). |
| Migration age | uniform(15, 40) | structural / conservative (no aged migrants who never reproduce — tilts in favour of migrationist hypothesis) | Not swept. |
| Migration entry region | eastern half (Slavic) / full grid (Arabic) | well-grounded (Curta 2001 lower-Danube entry; Kennedy 2007 Arabic distribution) | Not swept. |

### §7.5 Submodel — mother-tongue inheritance

On a birth:

- If mother's age ≤ `INHERITANCE_AGE_MAX` (= 25), the child's
  language equals the mother's.
- Otherwise the child's language is drawn (`random.choice`)
  from the cell-pool — the list of co-located other agents'
  languages, with the mother's own contribution removed. If the
  cell-pool has fewer than 3 other agents, the child falls back
  to the mother's language.

| Parameter | Value | Status | Sensitivity |
|---|---|---|---|
| `INHERITANCE_AGE_MAX` | 25 | **free parameter** (sociolinguistic order-of-magnitude only) | **Swept** ∈ {22, 25, 28, 30} (Table 4); range width ≤ 4 pp across all scenarios — not load-bearing. |
| Cell-pool fallback threshold | < 3 other agents | structural | Not swept. |

### §7.6 Submodel — two-way assimilation

For each agent each year, build the Moore-cell neighbour-language
list from the start-of-year snapshot:

- **Forward (non-Slavic → Slavic)**: if Slavic > 50 % of
  neighbours, roll against `slavic_assimilation_rate` to switch
  to Slavic.
- **Reverse (Slavic → Christianised non-Slavic)**: if
  Christianised non-Slavic > 50 % of neighbours, roll against
  `reverse_assimilation_rate` to switch to the most-common
  Christianised neighbour language (alphabetical tie-break for
  deterministic resolution; see `methods_reproducibility.md`
  for the determinism-fix history). The Arabic scenario sets
  `reverse_assimilation_rate = 0` because the Arabic context
  lacked an analogue to the Byzantine Christianising channel.

| Parameter | Value | Status | Sensitivity |
|---|---|---|---|
| Majority threshold | > 50 % of neighbour vote | structural (minimal majoritarian rule) | Not swept. |
| `slavic_assimilation_rate` | scenario-defined (0.005 / 0.01 / 0.02 / 0.02) | **free parameter** (inherited; original Kandler 2010 attribution not defensible) | Implicit in scenario design. |
| `reverse_assimilation_rate` | scenario-defined (0.03 / 0.02 / 0.015 / 0.0) | **free parameter** (inherited; no independent empirical anchor) | **Swept** ∈ {0.000, 0.0025, 0.005, 0.0075, 0.010, 0.015, 0.030, 0.045} (Fig 2 / Table 3b / Table 5). |

### §7.7 Submodel — substrate option

When `--substrate` is set with substrate fraction `s`:

1. Slavic `initial_fraction` is set to `s`.
2. The Slavic group's region list is `["balkans"]` (substrate
   Slavs are placed in the Balkans, the migration destination,
   per Sedov 1982's proto-Slavic Carpatho-Balkan continuity
   hypothesis).
3. Non-Slavic group fractions are scaled by `(1 − s) / 0.9` to
   preserve the total initial population at `INITIAL_POP = 5000`.

| Parameter | Value | Status | Sensitivity |
|---|---|---|---|
| Substrate fraction | 0 (no `--substrate`) / 0.30 (default with flag) / any `--substrate_fraction` | **free parameter / hypothesis-test** | **Swept** ∈ {0.00, 0.10, 0.20, 0.30, 0.40, 0.50} (Table 3 / Table 3b / Fig 2). |
| Substrate placement region | Balkans only | well-grounded (Sedov 1982; corrected from pre-fix eastern/central per `methods_reproducibility.md`) | Not swept. |

### §7.8 Sensitivity-sweep summary

The sweeps reported in the Results section are:

| Sweep | Parameter axes | Grid size | Source table |
|---|---|---|---|
| Plague mortality | `non_slavic_plague_mortality` × 4 scenarios | 16 | Table 2 / Fig 3 |
| INHERITANCE_AGE_MAX | age cutoff × 3 scenarios | 12 | Table 4 |
| Substrate response surface | substrate fraction × `reverse_assimilation_rate` × 2 Slavic scenarios | 48 | Table 3 (rev = 0.000 slice) / Table 3b / Fig 2 |
| Low-rev / threshold / window | substrate × low-`reverse_assim` strip × migration window × 2 Slavic scenarios | 48 | Table 5 / Fig 4 |

Per-sweep durable logs are at `docs/run_logs/2026-05-15_plague_sweep.md`,
`docs/run_logs/2026-05-16_inheritance_sweep.md`,
`docs/run_logs/2026-05-16_substrate_revassim_sweep.md`, and
`docs/run_logs/2026-05-17_low_rev_threshold_sweep.md`.

## Methods §8 — Reproducibility

See `docs/paper/methods_reproducibility.md` for the
reproducibility subsection. It documents the systematic
verification of the inherited DIA-25063 implementation: five
identified defects, their fixes, the commit-by-commit audit
trail, and the clean-room cross-process verification at the
engine-frozen commit `37054ac`.

## References (Methods section subset)

- Curta, F. (2001). *The Making of the Slavs.* Cambridge.
- Grimm, V., et al. (2006, 2010, 2020). The three ODD-protocol
  papers (full citations in main bibliography).
- Kandler, A. (2009); Kandler & Steele (2008); Kandler, Unger
  & Steele (2010) — the Kandler-family demographic-ABM
  references (full citations in main bibliography).
- Kennedy, H. (2007). *The Great Arab Conquests.*
- Mordechai, L., et al. (2019). "The Justinianic Plague: An
  inconsequential pandemic?" *PNAS* 116, 25546–25554.
- Russell, J. C. (1987). *Medieval Demography.*
- Sedov, V. V. (1982). *The Slavs in the Migration Period.*
- Versteegh, K. (2014). *The Arabic Language*, 2nd ed.

**Note on citations.** This document lists only the references most
directly cited by the ODD body above; the companion paper carries the
fuller bibliography, including the plague-mortality literature
(Mordechai et al. 2019; Stathakopoulos 2004) and the Christianisation
context (Whittow 1996) that informs the reverse-assimilation rule.

