"""Fig 3 — plague-mortality sensitivity sweep robustness panel.

Reads from canonical artefacts at HEAD:
  results_plague_<scenario>_<mortality>.txt (16 files, 4 scenarios x
                                              4 mortality values)
Parses the final-share line from each.

Generates docs/paper/figures/fig3_plague_sweep.{pdf,png}.

Per response5: no simulation calls; figures read from artefacts.
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent

SCENARIOS = [
    ("slavic1", "Slavic 1 (~1 M migrants)", "blue"),
    ("slavic2", "Slavic 2 (~3 M migrants)", "green"),
    ("slavic3", "Slavic 3 (~5 M migrants)", "red"),
    ("arabic",  "Arabic (~1 M migrants)",   "purple"),
]
MORTALITIES = [0.10, 0.12, 0.15, 0.20]

FINAL_LINE = re.compile(r"Avg Final Proportion:\s+([\d.]+)%\s+\(\+/-([\d.]+)%\)")


def parse_final(path: Path) -> tuple[float, float]:
    text = path.read_text()
    m = FINAL_LINE.search(text)
    if not m:
        raise ValueError(f"Could not parse final share from {path}")
    return float(m.group(1)), float(m.group(2))


def main() -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    for scen, label, color in SCENARIOS:
        means, sds = [], []
        for mort in MORTALITIES:
            mort_str = f"{mort:.2f}"
            path = REPO_ROOT / f"results_plague_{scen}_{mort_str}.txt"
            if not path.exists():
                raise FileNotFoundError(f"Missing canonical artefact: {path}")
            mean, sd = parse_final(path)
            means.append(mean)
            sds.append(sd)
        means_arr = np.array(means)
        sds_arr = np.array(sds)
        x = np.array(MORTALITIES)
        ax.errorbar(
            x, means_arr, yerr=sds_arr, fmt="o-", label=label,
            color=color, linewidth=2, markersize=6, capsize=4
        )

    ax.set_xlabel("Non-Slavic plague mortality (per agent per plague year)")
    ax.set_ylabel("Final Slavic share (%) — year 260 (Slavic), year 170 (Arabic)")
    ax.set_title(
        "Fig 3 — Final share across the plague-mortality range\n"
        "Mordechai low (0.10) to plague-maximalist high (0.20); 10 runs each, seed 42"
    )
    ax.set_ylim(0, 100)
    ax.set_xlim(0.085, 0.215)
    ax.set_xticks(MORTALITIES)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="center left", framealpha=0.95)
    # Reference lines
    ax.axhline(80, color="grey", linestyle=":", linewidth=1, alpha=0.6)
    ax.text(0.087, 81.5, "historical Slavic ~80 %+", fontsize=8, color="grey")
    ax.axhline(55, color="grey", linestyle=":", linewidth=1, alpha=0.6)
    ax.text(0.087, 56.5, "historical Arabic ~55 %", fontsize=8, color="grey")
    # Mark the default mortalities
    for mort, label in [(0.12, "Arabic default"), (0.15, "Slavic 1/2 default"), (0.20, "Slavic 3 default")]:
        ax.axvline(mort, color="black", linestyle="--", linewidth=0.5, alpha=0.3)

    plt.tight_layout()
    for ext in ("pdf", "png"):
        out = OUT_DIR / f"fig3_plague_sweep.{ext}"
        plt.savefig(out, dpi=200, bbox_inches="tight")
        print(f"Wrote {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
