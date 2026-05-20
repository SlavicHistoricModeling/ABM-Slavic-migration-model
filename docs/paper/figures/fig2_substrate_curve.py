"""Fig 2 — Substrate response surface (parameter-conditional reading).

Reads from canonical artefacts at HEAD:
  results_revassim_<scenario>_sub<f>_rev<r>.txt
    (6 substrate fractions x 4 reverse_assim rates per scenario)

Generates a multi-line plot: substrate fraction on x-axis, Slavic
share on y-axis, one line per reverse_assim value, for slavic1
(and slavic2 if available). Makes the parameter conditionality
of the corrected substrate-curve shape visible per the
response7 step-1 adjudication.

Per response7: Fig 2 reflects the adjudicated framing. Per the
decision criterion outcome recorded in
docs/run_logs/2026-05-16_substrate_revassim_sweep.md (U-shape
flattens at rev=0; mechanism is parameter-conditional), Fig 2
is the multi-line form, NOT a single-curve form.

Output: docs/paper/figures/fig2_substrate_curve.{pdf,png}
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent

SUBSTRATE_FRACTIONS = [0.00, 0.10, 0.20, 0.30, 0.40, 0.50]
REVERSE_ASSIM = [0.000, 0.015, 0.030, 0.045]
REV_COLORS = {0.000: "#1b9e77", 0.015: "#7570b3", 0.030: "#d95f02", 0.045: "#e7298a"}
REV_LABELS = {
    0.000: "rev_assim = 0.000 (rule disabled)",
    0.015: "rev_assim = 0.015 (Slavic 3 default)",
    0.030: "rev_assim = 0.030 (Slavic 1 default)",
    0.045: "rev_assim = 0.045 (above-default sensitivity)",
}

FINAL_LINE = re.compile(r"Avg Final Proportion:\s+([\d.]+)%\s+\(\+/-([\d.]+)%\)")


def parse_final(path: Path) -> tuple[float, float]:
    text = path.read_text()
    m = FINAL_LINE.search(text)
    if not m:
        raise ValueError(f"Could not parse final share from {path}")
    return float(m.group(1)), float(m.group(2))


def plot_scenario(ax, scenario, title):
    for rev in REVERSE_ASSIM:
        means, sds = [], []
        for sub in SUBSTRATE_FRACTIONS:
            sub_str = f"{sub:.2f}"
            rev_str = f"{rev:.3f}"
            path = REPO_ROOT / f"results_revassim_{scenario}_sub{sub_str}_rev{rev_str}.txt"
            if not path.exists():
                raise FileNotFoundError(f"Missing canonical artefact: {path}")
            mean, sd = parse_final(path)
            means.append(mean)
            sds.append(sd)
        means_arr = np.array(means)
        sds_arr = np.array(sds)
        x = np.array(SUBSTRATE_FRACTIONS) * 100
        color = REV_COLORS[rev]
        ax.errorbar(x, means_arr, yerr=sds_arr, fmt="o-", label=REV_LABELS[rev],
                    color=color, linewidth=2, markersize=5, capsize=3, alpha=0.9)

    ax.set_title(title)
    ax.set_xlabel("Substrate fraction (%)")
    ax.set_ylabel("Final Slavic share (%)")
    ax.set_ylim(0, 100)
    ax.set_xlim(-3, 53)
    ax.grid(True, alpha=0.3)
    ax.axhline(80, color="grey", linestyle=":", linewidth=1, alpha=0.6)
    # Olalde envelope shading (~30 - 60 % admixture upper bound)
    ax.axvspan(30, 50, color="lightyellow", alpha=0.3, zorder=0)
    ax.text(40, 5, "Olalde upper-\nbound range", fontsize=7, color="dimgrey", ha="center")


def main(scenarios=("slavic1", "slavic2")):
    available = [s for s in scenarios
                 if (REPO_ROOT / f"results_revassim_{s}_sub0.00_rev0.000.txt").exists()]
    if not available:
        raise RuntimeError("No revassim sweep results found")

    n = len(available)
    fig, axes = plt.subplots(1, n, figsize=(7 * n, 5.5), squeeze=False)

    for ax, scenario in zip(axes[0], available):
        scen_label = {
            "slavic1": "Slavic 1 (~1 M migrants)",
            "slavic2": "Slavic 2 (~3 M migrants)",
            "slavic3": "Slavic 3 (~5 M migrants)",
        }.get(scenario, scenario)
        plot_scenario(ax, scenario, scen_label)

    # Single legend across panels
    axes[0][0].legend(loc="upper left", framealpha=0.95, fontsize=9)

    fig.suptitle(
        "Fig 2 — Substrate response curve at four reverse-assimilation rates\n"
        "(adjudication per response7 step 1: shape is reverse_assim-conditional)",
        fontsize=11
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    for ext in ("pdf", "png"):
        out = OUT_DIR / f"fig2_substrate_curve.{ext}"
        plt.savefig(out, dpi=200, bbox_inches="tight")
        print(f"Wrote {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
