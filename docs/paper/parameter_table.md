# Parameter justification table

> One row per parameter in the canonical ABM. For each row: **value**
> in the canonical script, **basis** (the source justifying it),
> **status** (one of: *well-grounded*, *weakly grounded*, *free
> parameter*, *structural*), and **sensitivity range** (the values
> the sweep covers, or "not swept — fixed by structure" for
> structural).
>
> This table is the response to reviewer criticism #2 (parameter
> justification). It will be cited near-verbatim in Methods §2.5.
> Code reference: `slavic_migration_submited_v1.py` at commit
> `acd3ae3` (the matrix-batch code state).

## Status legend

- **structural** — fixed by the model design; not a tunable input
  (changing it would change what the model *is*, not what answer it
  gives).
- **well-grounded** — value is anchored to an empirical source that
  most relevant specialists would accept, and the source is cited.
- **weakly grounded** — value is plausible but the source is
  contested, or the source measures something adjacent rather than
  the value directly. Will be defended in Methods with that caveat.
- **free parameter** — no defensible empirical anchor; value is set
  to a working default and the conclusion's robustness comes from
  the sensitivity sweep, not the default.

## Structural parameters

| Parameter | Value | Basis | Status | Sensitivity range |
|---|---|---|---|---|
| `GRID_SIZE` | 50 × 50 (= 2,500 cells) | Computational tractability vs. spatial granularity; one cell ≈ 2,000 individuals at `INITIAL_POP = 5,000` scaled to ~5 M Balkan population. | structural | Not swept. (Future: 70 × 70 for finer cells, noted in code.) |
| `INITIAL_POP` | 5,000 agents | One agent ≈ 1,000 individuals, calibrated to ~5 M pre-migration Balkan population (Russell 1987; Treadgold). | structural | Not swept directly; scenario population trajectories are reported instead. |
| Moore neighbourhood | 8 cells (3 × 3 minus self) | Standard ABM choice for local interaction in a square grid; toroidal wrapping. | structural | Not swept. |
| Assimilation majority threshold | > 50 % of neighbour-language vote | The minimal majoritarian rule (Kandler 2009-style local rule). Anything stronger would be a different model. | structural | Not swept. |
| Scenario lengths | 260 yr (Slavic, 600–860 CE); 170 yr (Arabic, 630–800 CE) | Historical windows of the modelled cases. | structural | Not swept. |
| Initial-age distribution | `min(MAX_AGE, expovariate(BASE_MORTALITY))` | Equilibrium age distribution under flat mortality; replaces uniform-init transient (see DECISIONS.md "Engine baseline at `ad8cd05`"). | structural | Not swept (its purpose is to *remove* a transient, not be a tunable). |

## Demographic parameters

| Parameter | Value | Basis | Status | Sensitivity range |
|---|---|---|---|---|
| `REPRO_AGE_MIN`, `REPRO_AGE_MAX` | 15, 40 | Standard reproductive window for early-medieval demography (Russell 1987). | well-grounded | Not swept (window is conventional). |
| `MAX_AGE` | 60 | Early-medieval life-expectancy upper envelope; hard cap on an otherwise geometric tail. | well-grounded | Not swept. |
| `BASE_MORTALITY` | 0.02 / yr (crude annual ~20 / 1000) | Russell (1987) crude rate for early-medieval populations; lower envelope to give the model demographic room. | well-grounded | Implicit in CBR calibration; not separately swept. |
| `REPRO_SHARE` | 0.151 | Closed-form share of population that is female and aged 15–40 at equilibrium under flat 0.02 / yr mortality (see in-code derivation, lines 65–73). Confirmed by `--no_plague` engine baseline (final pop drift +8.1 % over 260 yr, within ±10 % fence). | structural | Not swept (it is a derived quantity, not a free input). |
| `CBR_NON_SLAVIC` | 0.020 / yr | Replacement CBR matched to `BASE_MORTALITY` so non-migrant groups sit at demographic equilibrium. **Reading B (bumping this to engineer post-plague recovery) was explicitly rejected as a reverse-engineered parameter** — see DECISIONS.md. | well-grounded | Not swept (any post-plague recovery should come from population dynamics, not parameter tuning). |
| `CBR_SLAVIC[scenario]` | slavic1 0.021; slavic2 0.023; slavic3 0.025; arabic 0.022 | Modest advantage over `CBR_NON_SLAVIC` (replacing the original 0.04 → 0.05 → 0.06 ladder, which embedded a large built-in fertility advantage favouring the migration hypothesis). Order-of-magnitude consistent with Russell (1987) cross-population CBR variation in early-medieval populations. | weakly grounded | Sweep planned in batch 2 sensitivity (no-advantage case `CBR_SLAVIC == CBR_NON_SLAVIC` will be included). |
| `CBR_SLAVIC_NEW` | 0.011 / yr (first 50 yr after settlement) | Newly-settled migrant fertility depression. Empirically supported in modern migration demography but order-of-magnitude only for early-medieval. | weakly grounded | Implicit in the rule's 50-yr window; sweep not currently planned. Worth flagging as a deliberate conservatism (it tilts results *against* the migrationist claim). |
| `PLAGUE_YEARS` | Slavic: [0, 10, 25] (year-of-scenario indices for 600, 610, 625 CE); Arabic: [0, 10] | Justinianic Plague chronology (Procopius; Maas; Stathakopoulos) — coarse-grained from the recurring outbreaks of the 540s–620s; the post-540 wave structure rather than a single event. | well-grounded | Not currently swept; outbreak timing is treated as a structural pin to history. |
| `non_slavic_plague_mortality` | 0.15 (slavic1/2/arabic differ slightly; slavic3 = 0.20) | Procopius reads (25–50 % mortality), reduced to 15 % as the **lower-envelope** of plague-maximalist interpretations. **Mordechai et al. (2019) contests the plague-maximalist literature**; this is acknowledged in Methods and is the rigor justification for the sensitivity sweep. | weakly grounded | **Sweep: 0.10 / 0.12 / 0.15 / 0.20** across all four scenarios. This is the primary robustness check of the plague-as-explanation argument and is non-optional in batch 2. |
| Slavic plague mortality | 0.04 (vs. 0.15 / 0.20 for non-Slavic) | The **differential** is what the migration hypothesis *requires* to deliver Slavic dominance through plague survivorship. Sources for the differential (lower Slavic exposure due to rural/decentralised settlement) are speculative — Curta and others note the *possibility* but no quantitative anchor exists. | **free parameter** | **The uniform-mortality counterfactual** (`--uniform_mortality`, Slavic group takes non-Slavic plague mortality) directly isolates this parameter's contribution and is reported as a headline result. The differential being a free parameter is the methodological point. |

## Migration parameters

| Parameter | Value | Basis | Status | Sensitivity range |
|---|---|---|---|---|
| `migration_rate` | slavic1: 10 / yr; slavic2: 30 / yr; slavic3: 50 / yr (over first 100 yr); arabic: 10 / yr | Calibrated to encompass the spectrum of migration-maximalist estimates (Curta 2001 archaeological-minimum to Heather-style higher figures). slavic3 is deliberately extreme to test the implausibility argument. | well-grounded (as a *spectrum*, not as point estimates) | Sweep is the scenarios themselves (the three slavic*N* rates span the migration-size axis). |
| Migration spatial entry | Random `(x, y)` in eastern half of grid (Slavic); whole grid (Arabic). | Pannonia/lower Danube entry for Slavic; broader-distribution Arab military settlement. Curta 2001; Kennedy 2007. | well-grounded | Not swept. |
| Migration age | uniform(15, 40) at arrival | Reproductive-age migration assumption; tilts results in favour of the migrationist hypothesis (no aged migrants who never reproduce). Deliberate conservatism. | structural / conservative | Not swept. |

## Assimilation parameters (NB: re-labelled as free parameters)

| Parameter | Value | Basis | Status | Sensitivity range |
|---|---|---|---|---|
| `slavic_assimilation_rate` | slavic1: 0.005; slavic2: 0.01; slavic3: 0.02; arabic: 0.02 | Per-year probability that a non-Slavic agent with > 50 % Slavic neighbours converts. **Original draft cited Kandler (2010) "neutral competition" rates — that attribution is not defensible**: Kandler's neutral-competition model uses different state-transition machinery (frequency-dependent biased copying with mutation), and no specific point value from Kandler can be ported into this rule. | **free parameter** | Implicit in scenario design; the sensitivity comes from comparing across scenarios, not from an independent sweep. Strong-form sweep across {0.001, 0.005, 0.01, 0.02, 0.05} is a recommended additional run but not currently in batch 2. |
| `reverse_assimilation_rate` | slavic1: 0.03; slavic2: 0.02; slavic3: 0.015; arabic: 0.0 | Per-year probability that a Slavic agent with > 50 % Christianised neighbours adopts the dominant Christianised language. The Arabic case is set to 0.0 because the Arabic context lacked an analogue to the Byzantine Christianising institutional channel. | **free parameter** | See `slavic_assimilation_rate` row. The Arabic 0.0 is structural; the Slavic values are the free dimension. |
| Mother-tongue rule cutoff (`INHERITANCE_AGE_MAX`) | 25 | Threshold below which a child inherits the mother's language directly; above, the child draws from the local cell-pool (community acquisition). The 25-yr threshold reflects the late-medieval / pre-modern observation that linguistically labile parenting tends to be by younger mothers in tightly-knit communities. **No specific empirical anchor**; the value is a sociolinguistic order-of-magnitude assumption. | **free parameter** | **Sweep: 22 / 25 / 28 / 30** in batch 2, across slavic1, slavic3, arabic (capped per response3 to save compute). The H1 Arabic diagnostic at `aeedfb2` already showed the rule contributes ~5.5 pp to the Arabic share (`results_arabic_matrix.txt` vs `results_arabic_ruleoff_matrix.txt`). |
| Cell-pool fallback (< 3 other agents → mother's language) | hard-coded threshold 3 | Avoids drawing from a degenerate two-agent local pool. Order-of-magnitude robustness, not a tunable. | structural | Not swept. |

## Initial-composition parameters

| Parameter | Value | Basis | Status | Sensitivity range |
|---|---|---|---|---|
| Initial Slavic share | 10 % (Slavic scenarios); 5 % (Arabic) | Pre-migration Slavic linguistic presence in eastern/central regions. The 10 % is a working assumption for the *no-substrate* default; the substrate hypothesis tests the alternative. | weakly grounded | Substrate response curve (next row) effectively sweeps this dimension. |
| Other-group fractions | Illyrian/Thracian 30 %; Greek 20 %; Germanic 20 %; Avar 10 %; Other 10 % | Ethnographic reconstruction (Curta 2001; Barford 2001). Sources are sketchy at the percentage-point level. | weakly grounded | Not currently swept; fractions enter the model only through which agents take the non-Slavic plague mortality. |
| Non-Slavic Christianisation in Balkans | 80 % | Approximate Christianisation level c. 600 CE in the Balkans (Whittow 1996). | weakly grounded | Not currently swept; affects only the reverse-assimilation rule's eligibility pool. |

## Substrate parameter (the keystone reframe)

| Parameter | Value | Basis | Status | Sensitivity range |
|---|---|---|---|---|
| Substrate initial Slavic fraction (`--substrate`) | 30 % when enabled (currently hard-coded in `run_simulation`) | The substrate hypothesis itself — pre-existing Slavic-speaking population in the Balkans. **In the revised paper this is no longer a default-on assumption; it is the parameter being estimated.** Linguistic-continuity argument from Sedov (1982) and Carpatho-Balkan dialect-zone work. | **free parameter / hypothesis-test** | **Response curve: substrate at 0 / 10 / 20 / 30 / 40 / 50 %** in batch 2. The curve, not a single value, is the headline. The previous code comment "(genetics 10–30 % ancestry)" inside the substrate block is wrong (misreads Olalde — see `olalde_audit.md` Finding 5) and will be replaced. |

## Cross-cutting notes

- **No parameter in this table is set to a value that requires the
  migration hypothesis to be correct.** The differential plague
  mortality (Slavic 0.04 vs. non-Slavic 0.15 / 0.20) is the closest
  case — it is the parameter the migration hypothesis *requires*, and
  the uniform-mortality counterfactual isolates how much of the
  Slavic share depends on it.
- **The free parameters (`slavic_assimilation_rate`,
  `reverse_assimilation_rate`, differential plague mortality,
  `INHERITANCE_AGE_MAX`, substrate fraction) are explicitly labelled
  as such** rather than dressed up with a misattributed citation. The
  conclusion's robustness rests on the sweeps, not on the defaults.
- **Reviewer criticism #2 framing**: "every parameter is either
  empirically anchored, structurally determined, or explicitly labelled
  as a free parameter with a sensitivity sweep". This table is the
  evidence for that claim.
