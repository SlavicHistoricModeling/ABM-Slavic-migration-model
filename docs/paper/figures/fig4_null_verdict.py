"""Fig 4 — null-verdict figure.

The 24 archaeologically-admissible slavic1 cells from the response8
sweep (low-rev × substrate × window), plotted against the 80%
historical threshold. Every admissible cell falls below the
threshold; the single maximum (sub=0.30, rev=0.000, win=150 yr at
70.90% +/- 5.15%) is labelled and its 1-SD error bar shown so the
upper bound's sub-threshold position is visible.

Reads from canonical artefacts:
  results_lowrev_slavic1_sub<s>_rev<r>_win<w>.txt (24 files,
  gitignored; durable record in
  docs/run_logs/2026-05-17_low_rev_threshold_sweep.md)

Per response5: figures read from artefacts; no re-runs.

Output: docs/paper/figures/fig4_null_verdict.{pdf,png}
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent

SUBSTRATE = [0.00, 0.30]
REV_ASSIM = [0.000, 0.0025, 0.005, 0.0075, 0.010, 0.015]
WINDOWS = [100, 150]

FINAL_LINE = re.compile(r"Avg Final Proportion:\s+([\d.]+)%\s+\(\+/-([\d.]+)%\)")


def parse_final(path: Path) -> tuple[float, float]:
    text = path.read_text()
    m = FINAL_LINE.search(text)
    if not m:
        raise ValueError(f"Could not parse final share from {path}")
    return float(m.group(1)), float(m.group(2))


def main() -> None:
    # Two panels: window=100 (left), window=150 (right).
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.5), sharey=True)

    for ax, win in zip(axes, WINDOWS):
        for sub, marker, label in [
            (0.00, "o", "substrate = 0.00 (no substrate)"),
            (0.30, "s", "substrate = 0.30 (Olalde mid-range)"),
        ]:
            means, sds = [], []
            for rev in REV_ASSIM:
                rev_str = f"{rev:.3f}" if rev < 0.01 else f"{rev:.3f}"
                # All filenames use fixed-width formatting per the sweep script
                sub_str = f"{sub:.2f}"
                # The sweep script wrote files as rev=0.000, 0.0025, 0.005, 0.0075, 0.010, 0.015
                # Use the literal value strings the sweep script used:
                rev_lookup = {
                    0.000: "0.000", 0.0025: "0.0025", 0.005: "0.005",
                    0.0075: "0.0075", 0.010: "0.010", 0.015: "0.015",
                }[rev]
                fname = f"results_lowrev_slavic1_sub{sub_str}_rev{rev_lookup}_win{win}.txt"
                path = REPO_ROOT / fname
                if not path.exists():
                    raise FileNotFoundError(f"Missing canonical artefact: {path}")
                mean, sd = parse_final(path)
                means.append(mean)
                sds.append(sd)
            x = np.array(REV_ASSIM)
            means_arr = np.array(means)
            sds_arr = np.array(sds)
            ax.errorbar(
                x, means_arr, yerr=sds_arr, fmt=marker + "-",
                label=label, linewidth=2, markersize=7, capsize=4,
                alpha=0.9
            )

        # Reference lines
        ax.axhline(80, color="firebrick", linestyle="-", linewidth=1.5, alpha=0.85,
                   label="historical Slavic ~80 %+ threshold")
        ax.axhline(55, color="grey", linestyle=":", linewidth=1, alpha=0.6,
                   label="historical Arabic ~55 % (context)")

        ax.set_title(f"Slavic 1 (~1 M migrants), migration window = {win} yr")
        ax.set_xlabel("reverse-assimilation rate")
        if win == 100:
            ax.set_ylabel("Final Slavic share (%) at year 260")
        ax.set_ylim(0, 100)
        ax.set_xlim(-0.001, 0.016)
        ax.set_xticks(REV_ASSIM)
        ax.set_xticklabels([f"{r:.4f}".rstrip("0").rstrip(".") for r in REV_ASSIM],
                           rotation=0, fontsize=8)
        ax.grid(True, alpha=0.3)

        # Annotate the maximum cell only on the win=150 panel
        if win == 150:
            # Maximum is at sub=0.30, rev=0.000 (the leftmost square in win=150)
            ax.annotate(
                "max: 70.90 % ± 5.15 %\n(1-SD upper bound 76.05 %\nstill < 80 %)",
                xy=(0.000, 70.90),
                xytext=(0.005, 88),
                fontsize=8.5,
                ha="left",
                arrowprops=dict(arrowstyle="->", color="black", lw=1, alpha=0.7),
                bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow",
                          ec="grey", alpha=0.9)
            )

    axes[0].legend(loc="upper center", framealpha=0.95, fontsize=8.5)

    fig.suptitle(
        "Fig 4 — Every admissible cell falls below the historical Slavic threshold\n"
        "(24 cells: low-reverse-assim × substrate × migration window, slavic1 ~1 M migrants)",
        fontsize=11
    )
    plt.tight_layout(rect=[0, 0, 1, 0.93])

    for ext in ("pdf", "png"):
        out = OUT_DIR / f"fig4_null_verdict.{ext}"
        plt.savefig(out, dpi=200, bbox_inches="tight")
        print(f"Wrote {out}")
    plt.close(fig)


if __name__ == "__main__":
    main()
