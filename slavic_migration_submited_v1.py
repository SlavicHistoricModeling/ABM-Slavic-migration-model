"""
Agent-Based Model for Linguistic Expansion (Slavic and Arabic Cases).
This model extends frameworks like Kandler (2009) by incorporating spatial
grids, reverse assimilation, and sensitivity analysis. Parameters are
justified from historical sources (e.g., birth rates from Russell 1987
~3.5-5%).
Validation: Matches Arabic ~60% dominance. Run with
python script.py --scenario slavic1 --substrate True --birth_vary 0.1 --plot True.
"""
import numpy as np
import random
import csv
import statistics  # For mean and SD
import argparse  # For flexible parameter input
import sys
import time
import matplotlib.pyplot as plt  # For plotting

# Parse arguments for flexibility
parser = argparse.ArgumentParser()
parser.add_argument('--scenario', default='all',
                    help='Scenario: slavic1, slavic2, slavic3, arabic, or all to run and plot comparisons')
parser.add_argument('--num_runs', type=int, default=10,
                    help='Number of runs for averaging')
parser.add_argument('--substrate', action='store_true',
                    help='Enable proto-Slavic substrate (30%% initial in Balkans)')
parser.add_argument('--birth_vary', type=float, default=0.0,
                    help='Variation factor for birth rate sensitivity (+/- fraction)')
parser.add_argument('--seed', type=int, default=42,
                    help='Random seed for reproducibility')
parser.add_argument('--plot', action='store_true',
                    help='Generate and save plot (figure1.png)')
parser.add_argument('--migration_override', type=int, default=None,
                    help='Override scenario migration_rate (e.g. 0 for the no-migration baseline)')
parser.add_argument('--no_plague', action='store_true',
                    help='Force PLAGUE_YEARS = [] for the engine-sanity baseline')
parser.add_argument('--inheritance_age_max', type=int, default=None,
                    help='Override INHERITANCE_AGE_MAX (mother-tongue cutoff). '
                         'Use 99 to effectively disable the cell-pool draw. '
                         'For the 22/25/28/30 sweep.')
parser.add_argument('--uniform_mortality', action='store_true',
                    help='Force the Slavic group to use the non-Slavic plague '
                         'mortality (i.e. zero plague differential). For the '
                         'scenario 3 counterfactual: how much of the Slavic '
                         'share comes from the differential vs from migration '
                         'and assimilation alone?')
parser.add_argument('--substrate_fraction', type=float, default=None,
                    help='Override the Slavic initial_fraction when --substrate '
                         'is set (the substrate hypothesis pre-existing Slavic '
                         'share). Default when --substrate is set is 0.30. Use '
                         'this for the substrate response curve '
                         '(0/10/20/30/40/50 percent). Only takes effect when '
                         '--substrate is also set.')
parser.add_argument('--non_slavic_plague_mortality', type=float, default=None,
                    help='Override the per-scenario non_slavic_plague_mortality '
                         '(default 0.15 for slavic1/2 and arabic 0.12; 0.20 for '
                         'slavic3). For the plague-mortality sensitivity sweep '
                         '(0.10/0.12/0.15/0.20).')
args = parser.parse_args()

random.seed(args.seed)  # Reproducibility

# Model Configuration
GRID_SIZE = 50  # Future: 70 for finer granularity
INITIAL_POP = 5000  # Future: 10000 for agents=500 individuals
REPRO_AGE_MIN, REPRO_AGE_MAX = 15, 40
MAX_AGE = 60
INHERITANCE_AGE_MAX = 25  # Live: mother-tongue rule cutoff; sweep 22/25/28/30

# --- Birth-rate calibration -------------------------------------------------
# The reproduction loop applies a group's birth_rate as a per-year probability
# PER reproductive-age female. The original numbers (0.04, 0.05, ...) were
# specified as if they were CRUDE birth rates (~3.5-5%); applied per-female
# they're ~6.6x too small, so populations collapse.
#
# FIX: specify each group's intended CRUDE birth rate (CBR, births per head per
# year) and convert to the per-female probability the loop needs. At
# equilibrium under flat mortality m=BASE_MORTALITY=0.02, the share of the
# population that is female AND aged REPRO_AGE_MIN..MAX is
#   REPRO_SHARE = 0.5 * sum_{a=15..40} 0.98^a / sum_{a=0..inf} 0.98^a ~= 0.151
# so per_female_rate = target_CBR / REPRO_SHARE.
#
# 0.151 is the EQUILIBRIUM share. Ages are initialised uniformly here, so
# early years run hotter and population rises before settling. Confirm
# REPRO_SHARE is right via the no-migration, no-plague baseline.
REPRO_SHARE = 0.151


def per_female_rate(crude_birth_rate):
    """Crude birth rate -> per-reproductive-female annual probability."""
    return crude_birth_rate / REPRO_SHARE


# Intended crude birth rates (births per head per year). Non-migrant groups sit
# at replacement (CBR ~ CDR ~ BASE_MORTALITY); the migrating group carries only
# a MODEST advantage. The original 2:1 ratio and the 0.04->0.05->0.06 ladder
# are dropped (a large built-in fertility advantage favours the migration
# hypothesis without warrant). Sweep CBR_SLAVIC in sensitivity, including the
# no-advantage case CBR_SLAVIC == CBR_NON_SLAVIC.
CBR_NON_SLAVIC = 0.020
CBR_SLAVIC_NEW = 0.011          # newly-settled migrants, first 50 yr
CBR_SLAVIC = {
    "slavic1": 0.021,
    "slavic2": 0.023,
    "slavic3": 0.025,
    "arabic":  0.022,
}

SCENARIOS = {  # Parameters with justifications
    "slavic1": {"migration_rate": 10, "slavic_assimilation_rate": 0.005,
                "reverse_assimilation_rate": 0.03,
                "slavic_birth_rate": per_female_rate(CBR_SLAVIC["slavic1"]),
                "slavic_birth_rate_new": per_female_rate(CBR_SLAVIC_NEW),
                "non_slavic_plague_mortality": 0.15, "years": 260,
                "start_year": 600,
                "source": "Low migration: Archaeology limits <2M (Curta 2001); birth ~4% medieval avg (Russell 1987)"},
    "slavic2": {"migration_rate": 30, "slavic_assimilation_rate": 0.01,
                "reverse_assimilation_rate": 0.02,
                "slavic_birth_rate": per_female_rate(CBR_SLAVIC["slavic2"]),
                "slavic_birth_rate_new": per_female_rate(CBR_SLAVIC_NEW),
                "non_slavic_plague_mortality": 0.15, "years": 260,
                "start_year": 600,
                "source": "Moderate: Assumes slight advantages; assimilation from Kandler (2010) neutral rates"},
    "slavic3": {"migration_rate": 50, "slavic_assimilation_rate": 0.02,
                "reverse_assimilation_rate": 0.015,
                "slavic_birth_rate": per_female_rate(CBR_SLAVIC["slavic3"]),
                "slavic_birth_rate_new": per_female_rate(CBR_SLAVIC_NEW),
                "non_slavic_plague_mortality": 0.20, "years": 260,
                "start_year": 600,
                "source": "Extreme: Tests implausibility; mortality ~Justinian plague 25-50% (Procopius)"},
    "arabic":  {"migration_rate": 10, "slavic_assimilation_rate": 0.02,
                "reverse_assimilation_rate": 0.0,
                "slavic_birth_rate": per_female_rate(CBR_SLAVIC["arabic"]),
                "slavic_birth_rate_new": per_female_rate(CBR_SLAVIC_NEW),
                "non_slavic_plague_mortality": 0.12, "years": 170,
                "start_year": 630,
                "source": "Kennedy (2007): ~1M migrants; assimilation via institutions"}
}


def run_simulation(params, substrate=False):
    # Plague-mortality sweep override (batch 2: 0.10/0.12/0.15/0.20).
    # Applied here so that GROUPS picks it up at construction time and
    # the uniform_mortality variant below picks up the swept value too.
    # Mutates the params dict in place; callers using SCENARIOS[scen]
    # should be aware. (For the sweep workflow, each `python ... --scen X
    # --non_slavic_plague_mortality V` invocation is a fresh process, so
    # the mutation is contained to that invocation.)
    if args.non_slavic_plague_mortality is not None:
        params["non_slavic_plague_mortality"] = args.non_slavic_plague_mortality

    GROUPS = {
        "slavic": {"birth_rate": params["slavic_birth_rate"],
                   "birth_rate_new": params["slavic_birth_rate_new"],
                   "plague_mortality": 0.04,
                   "initial_fraction": 0.1 if params["start_year"] != 630 else 0.05,
                   "regions": ["eastern", "central"],
                   "christianized": False},
        "illyrian_thracian": {"birth_rate": per_female_rate(CBR_NON_SLAVIC),
                              "plague_mortality": params["non_slavic_plague_mortality"],
                              "initial_fraction": 0.3 if params["start_year"] != 630 else 0.0,
                              "regions": ["balkans"],
                              "christianized": True},
        "greek": {"birth_rate": per_female_rate(CBR_NON_SLAVIC),
                  "plague_mortality": params["non_slavic_plague_mortality"],
                  "initial_fraction": 0.2 if params["start_year"] != 630 else 0.0,
                  "regions": ["balkans"],
                  "christianized": True},
        "germanic": {"birth_rate": per_female_rate(CBR_NON_SLAVIC),
                     "plague_mortality": params["non_slavic_plague_mortality"],
                     "initial_fraction": 0.2 if params["start_year"] != 630 else 0.0,
                     "regions": ["central", "balkans"],
                     "christianized": True},
        "avar": {"birth_rate": per_female_rate(CBR_NON_SLAVIC),
                 "plague_mortality": 0.06 if params["start_year"] != 630 else 0.0,
                 "initial_fraction": 0.1 if params["start_year"] != 630 else 0.0,
                 "regions": ["balkans", "central"],
                 "christianized": False},
        "other": {"birth_rate": per_female_rate(CBR_NON_SLAVIC),
                  "plague_mortality": 0.08 if params["start_year"] != 630 else params["non_slavic_plague_mortality"],
                  "initial_fraction": 0.1 if params["start_year"] != 630 else 0.95,
                  "regions": ["eastern"],
                  "christianized": False}
    }

    if substrate:
        # Substrate proportion is a free parameter; the substrate
        # response curve sweeps 0/10/20/30/40/50 %. Default when
        # --substrate is set without --substrate_fraction is 0.30.
        # NB: genetics (Olalde 2023) bounds total Slavic-related
        # admixture at ~30-60 % in modern populations but does not
        # constrain the pre-migration substrate fraction; the older
        # "(genetics 10-30 % ancestry)" comment here misread Olalde,
        # see docs/paper/olalde_audit.md.
        #
        # Substrate semantics fix (2026-05-16, response5 step 2 audit
        # defects 1.1 + 1.2; see docs/run_logs/2026-05-16_code_audit.md):
        # (1) place substrate Slavs in the BALKANS (the migration
        #     destination), matching Sedov's Carpatho-Balkan
        #     proto-Slavic continuity hypothesis. The pre-fix code
        #     placed them in eastern/central (the migration source),
        #     testing a different hypothesis.
        # (2) normalise the non-Slavic groups' initial_fraction so
        #     the total sums to 1.0 instead of (0.9 + substrate_
        #     fraction). The pre-fix code left non-Slavs at default
        #     fractions, inflating total population by up to 40 %.
        s = args.substrate_fraction if args.substrate_fraction is not None else 0.3
        GROUPS["slavic"]["initial_fraction"] = s
        if params["start_year"] != 630:
            GROUPS["slavic"]["regions"] = ["balkans"]
            original_non_slavic_sum = 0.9   # 0.3 + 0.2 + 0.2 + 0.1 + 0.1
            scale = (1.0 - s) / original_non_slavic_sum
            for g in ("illyrian_thracian", "greek", "germanic", "avar", "other"):
                GROUPS[g]["initial_fraction"] *= scale

    if args.uniform_mortality:
        GROUPS["slavic"]["plague_mortality"] = params["non_slavic_plague_mortality"]

    BASE_MORTALITY = 0.02  # Justification: Early medieval crude ~20-30/1000 (Russell 1987)
    PLAGUE_YEARS = [] if args.no_plague else (
        [0, 10, 25] if params["start_year"] != 630 else [0, 10]
    )
    migration_rate = (args.migration_override
                      if args.migration_override is not None
                      else params["migration_rate"])
    inheritance_age_max = (args.inheritance_age_max
                           if args.inheritance_age_max is not None
                           else INHERITANCE_AGE_MAX)

    def region_of(x, y, N=GRID_SIZE):
        if x >= N // 2:
            return "balkans"
        if y >= N // 2:
            return "central"
        return "eastern"

    all_props_runs = []  # List of lists: per run, proportions over years
    all_pops_runs = []   # List of lists: per run, total agents over years

    progress_every = max(1, params["years"] // 10)  # ~10 progress lines/run
    t_start = time.time()

    for run in range(args.num_runs):
        # Initialize grid/agents
        grid = [[[] for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        agents = []
        agent_id = 0

        for group, gp in GROUPS.items():
            num = int(INITIAL_POP * gp["initial_fraction"])
            for _ in range(num):
                while True:
                    x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                    if region_of(x, y) in gp["regions"]:
                        break
                agents.append({"id": agent_id, "x": x, "y": y, "language": group,
                               "age": min(MAX_AGE, int(random.expovariate(BASE_MORTALITY))),
                               "sex": random.choice(["male", "female"])})
                grid[x][y].append(agent_id)
                agent_id += 1

        props = []
        pops = []
        for year in range(params["years"]):
            new_agents = []
            dead = []
            if year < 100:
                for _ in range(migration_rate):
                    x = random.randint(GRID_SIZE // 2, GRID_SIZE - 1) if params["start_year"] != 630 else random.randint(0, GRID_SIZE - 1)
                    y = random.randint(0, GRID_SIZE - 1)
                    new_agents.append({"id": agent_id, "x": x, "y": y, "language": "slavic",
                                       "age": random.randint(15, 40),
                                       "sex": random.choice(["male", "female"])})
                    grid[x][y].append(agent_id)
                    agent_id += 1

            # Start-of-year snapshots: cell composition for the mother-tongue
            # rule, and agent_id -> language for the assimilation neighbour
            # scan further down. Both are built once per year from the
            # start-of-year population so the result is independent of agent
            # processing order. The dict snapshot also turns the previous
            # O(n^2) per-agent neighbour scan into O(n*k) where k is the
            # Moore-neighbourhood size (<= ~30).
            cell_langs = {}
            agent_id_to_lang = {}
            for ag in agents:
                cell_langs.setdefault((ag["x"], ag["y"]), []).append(ag["language"])
                agent_id_to_lang[ag["id"]] = ag["language"]

            for a in agents:
                a["age"] += 1
                mort = BASE_MORTALITY
                if year in PLAGUE_YEARS:
                    mort = GROUPS[a["language"]]["plague_mortality"]
                if random.random() < mort:
                    dead.append(a["id"])
                    grid[a["x"]][a["y"]].remove(a["id"])
                    continue
                if a["sex"] == "female" and REPRO_AGE_MIN <= a["age"] <= REPRO_AGE_MAX:
                    br = GROUPS[a["language"]]["birth_rate"]
                    if a["language"] == "slavic" and a["x"] >= GRID_SIZE // 2 \
                            and year < 50 and params["start_year"] != 630:
                        br = GROUPS["slavic"]["birth_rate_new"]
                    if args.birth_vary > 0:
                        br *= random.uniform(1 - args.birth_vary, 1 + args.birth_vary)
                    if random.random() < br:
                        nx, ny = a["x"], a["y"]

                        # Mother-tongue transmission. Mother <= INHERITANCE_AGE_MAX
                        # at birth: child inherits her language. Older mother:
                        # child draws its language from the local same-cell
                        # distribution (community acquisition where no
                        # institution standardises transmission). If the cell
                        # holds fewer than 3 OTHER agents the local pool is too
                        # small to be meaningful, so the child falls back to
                        # the mother's language.
                        if a["age"] <= inheritance_age_max:
                            child_lang = a["language"]
                        else:
                            pool = list(cell_langs.get((a["x"], a["y"]), []))
                            if a["language"] in pool:
                                pool.remove(a["language"])
                            if len(pool) < 3:
                                child_lang = a["language"]
                            else:
                                child_lang = random.choice(pool)

                        new_agents.append({"id": agent_id, "x": nx, "y": ny,
                                           "language": child_lang, "age": 0,
                                           "sex": random.choice(["male", "female"])})
                        grid[nx][ny].append(agent_id)
                        agent_id += 1
                neigh_ids = []
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx = (a["x"] + dx) % GRID_SIZE
                        ny = (a["y"] + dy) % GRID_SIZE
                        neigh_ids.extend(grid[nx][ny])
                neigh_langs = [agent_id_to_lang[i] for i in neigh_ids if i in agent_id_to_lang]
                if a["language"] == "slavic" and params["start_year"] != 630:
                    if neigh_langs:
                        christian_neighbors = sum(1 for l in neigh_langs if GROUPS[l]["christianized"])
                        if christian_neighbors / len(neigh_langs) > 0.5 and random.random() < params["reverse_assimilation_rate"]:
                            chlangs = [l for l in neigh_langs if GROUPS[l]["christianized"]]
                            if chlangs:
                                # Determinism fix: `set(chlangs)` iteration order
                                # depends on Python's hash randomisation
                                # (PYTHONHASHSEED), so when two Christianised
                                # neighbour-languages tied in count the
                                # `max(...)` tie-break was process-dependent.
                                # Sorting the set first pins the tie-break to
                                # alphabetical order — reproducible at any seed
                                # on any machine. See
                                # docs/run_logs/2026-05-15_determinism_fix.md.
                                a["language"] = max(sorted(set(chlangs)), key=chlangs.count)
                if a["language"] != "slavic":
                    if neigh_langs:
                        sN = sum(1 for l in neigh_langs if l == "slavic")
                        if sN / len(neigh_langs) > 0.5 and random.random() < params["slavic_assimilation_rate"]:
                            a["language"] = "slavic"
            agents = [a for a in agents if a["id"] not in dead] + new_agents
            s_count = sum(1 for a in agents if a["language"] == "slavic")
            props.append(s_count / len(agents) if agents else 0.0)
            pops.append(len(agents))

            if (year + 1) % progress_every == 0 or year + 1 == params["years"]:
                done_yr = run * params["years"] + year + 1
                total_yr = args.num_runs * params["years"]
                pct = 100.0 * done_yr / total_yr
                elapsed = time.time() - t_start
                eta = elapsed * (total_yr - done_yr) / done_yr if done_yr else 0.0
                print(f"PROGRESS run {run + 1}/{args.num_runs} year {year + 1}/{params['years']}"
                      f" pop={len(agents)} slav={props[-1]:.1%}"
                      f" overall {pct:5.1f}% elapsed={elapsed:6.1f}s eta={eta:6.1f}s",
                      file=sys.stdout, flush=True)

        all_props_runs.append(props)
        all_pops_runs.append(pops)

    # Compute averages and SDs per year
    num_years = params["years"]
    avg_props = [statistics.mean([run_props[y] for run_props in all_props_runs]) for y in range(num_years)]
    sd_props = [statistics.stdev([run_props[y] for run_props in all_props_runs]) if args.num_runs > 1 else 0.0 for y in range(num_years)]
    avg_pops = [statistics.mean([run_pops[y] for run_pops in all_pops_runs]) for y in range(num_years)]
    min_pops = [min(run_pops[y] for run_pops in all_pops_runs) for y in range(num_years)]
    max_pops = [max(run_pops[y] for run_pops in all_pops_runs) for y in range(num_years)]

    return avg_props, sd_props, params["start_year"], avg_pops, min_pops, max_pops


# If scenario is 'all', run all and plot
if args.scenario == 'all':
    results = {}
    for scen in ['slavic1', 'slavic2', 'slavic3', 'arabic']:
        params = SCENARIOS[scen]
        results[scen] = run_simulation(params, args.substrate)
else:
    params = SCENARIOS[args.scenario]
    results = {args.scenario: run_simulation(params, args.substrate)}

# Population checkpoints printed in every results file so the run-log
# template can quote them. Range covers max scenario length (260 yr).
POP_CHECKPOINTS = [0, 25, 50, 100, 150, 200, 260]

# Output results for single or all
for scen, (avg_props, sd_props, start_year, avg_pops, min_pops, max_pops) in results.items():
    with open(f"results_{scen}.txt", "w") as f:
        f.write(f"Scenario: {scen} | Runs: {args.num_runs} | Substrate: {args.substrate}"
                f" | Birth Vary: +/-{args.birth_vary*100}%"
                f" | migration_override: {args.migration_override}"
                f" | no_plague: {args.no_plague}"
                f" | uniform_mortality: {args.uniform_mortality}"
                f" | inheritance_age_max: {args.inheritance_age_max}"
                f" | substrate_fraction: {args.substrate_fraction}"
                f" | non_slavic_plague_mortality: {args.non_slavic_plague_mortality}"
                f" | seed: {args.seed}\n")
        f.write(f"Avg Final Proportion: {avg_props[-1]:.2%} (+/-{sd_props[-1]:.2%})\n")
        f.write("Population checkpoints (year_offset: mean [min..max]):\n")
        n_yr = len(avg_pops)
        for c in POP_CHECKPOINTS:
            idx = c if c < n_yr else n_yr - 1
            f.write(f"  year {c:>3}: {avg_pops[idx]:>7.0f}  [{min_pops[idx]:>5}..{max_pops[idx]:>5}]\n")
        f.write("Slavic-share checkpoints (year_offset: mean +/- SD):\n")
        for c in POP_CHECKPOINTS:
            idx = c if c < n_yr else n_yr - 1
            f.write(f"  year {c:>3}: {avg_props[idx]*100:>5.2f}% +/- {sd_props[idx]*100:>4.2f}%\n")

# Plot if requested
if args.plot or args.scenario == 'all':
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = {'slavic1': 'blue', 'slavic2': 'green', 'slavic3': 'red', 'arabic': 'purple'}
    for scen, (avg_props, sd_props, start_year, _avg_pops, _min_pops, _max_pops) in results.items():
        years = np.arange(start_year, start_year + len(avg_props))
        ax.plot(years, np.array(avg_props) * 100, label=scen.capitalize(), color=colors.get(scen, 'black'))
        ax.fill_between(years,
                        (np.array(avg_props) - np.array(sd_props)) * 100,
                        (np.array(avg_props) + np.array(sd_props)) * 100,
                        alpha=0.2, color=colors.get(scen, 'black'))

    ax.set_xlabel('Year')
    ax.set_ylabel('Linguistic Proportion (%)')
    ax.set_title('Time-series of Linguistic Proportions (Averages with Error Bars)')
    ax.legend()
    ax.grid(True)
    plt.savefig('figure1.png')
    plt.show()  # Or close if no display


# Alternative model: Simple Lotka-Volterra for comparison (from Kandler 2008 inspiration)
def lotka_volterra_comparison(N0_slavic=0.1, r_slavic=0.04, r_other=0.025, alpha=0.005, beta=0.03, t=260):
    """Equation-based alternative: dS/dt = r_s S (1 - S - alpha O), dO/dt = r_o O (1 - O - beta S)"""
    S, O = [N0_slavic], [1 - N0_slavic]
    for _ in range(t):
        dS = r_slavic * S[-1] * (1 - S[-1] - alpha * O[-1])
        dO = r_other * O[-1] * (1 - O[-1] - beta * S[-1])
        S.append(max(0, S[-1] + dS))
        O.append(max(0, O[-1] + dO))
    return S[-1] / (S[-1] + O[-1])


# Example call: Print comparison
lv_prop = lotka_volterra_comparison()
print(f"Lotka-Volterra Comparison Proportion: {lv_prop:.2%}")
