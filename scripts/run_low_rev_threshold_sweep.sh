#!/usr/bin/env bash
# Response8: low-reverse-assim + threshold-resolution + extended migration window sweep.
#
# Purpose: determine whether any historically admissible cell clears the
# 80% rural-dominance threshold without millions of migrants. Adjudicates
# Fork-C (rigorous null) vs. a possible positive thesis within the
# current model.
#
# Grid (48 cells):
#   reverse_assimilation_rate ∈ {0.000, 0.0025, 0.005, 0.0075, 0.010, 0.015}  (6 values)
#   scenarios:                    slavic1 (~1M) + slavic2 (~3M)              (2)
#   substrate fraction:           {0.00, 0.30}                                (2)
#   migration window:             {100 yr default, 150 yr extended}          (2)
#
# Engine frozen at 37054ac per response7/8; sweep runs against a /tmp
# copy of the canonical engine with two sed substitutions per cell
# (reverse_assim rate; migration window). Canonical file at
# slavic_migration_submited_v1.py is byte-identical to its 37054ac state.
#
# Wall time estimate: ~3 hours.

set -e
start=$(date +%s)
elapsed() { echo "$(( ($(date +%s) - start) / 60 )) min"; }

CANONICAL=slavic_migration_submited_v1.py
PATCHED=/tmp/slavic_lowrev_patched.py

run_cell() {
    local scenario=$1
    local sub_frac=$2
    local rev_rate=$3
    local window=$4
    local tag="lowrev_${scenario}_sub${sub_frac}_rev${rev_rate}_win${window}"
    echo "=== START $tag at $(date +%H:%M:%S) (elapsed $(elapsed)) ==="

    # Two sed patches into a /tmp copy:
    #   (a) reverse_assim rate across all four scenarios in SCENARIOS dict
    #   (b) migration window 100 -> $window on the unique line `if year < 100:`
    sed -E "s/(\"reverse_assimilation_rate\":[[:space:]]*)[0-9.]+/\1${rev_rate}/g" "$CANONICAL" | \
        sed -E "s/if year < 100:/if year < ${window}:/" > "$PATCHED"

    if [ "$sub_frac" = "0.00" ]; then
        python "$PATCHED" --scenario "$scenario" --num_runs 10 --seed 42
    else
        python "$PATCHED" --scenario "$scenario" --num_runs 10 --seed 42 \
            --substrate --substrate_fraction "$sub_frac"
    fi
    cp "results_${scenario}.txt" "results_${tag}.txt"
    echo "=== DONE  $tag at $(date +%H:%M:%S) ==="
}

# Iteration order: scenario > window > rev > sub. This makes early-read of
# slavic1 results possible as soon as the slavic1 portion completes.
for scen in slavic1 slavic2; do
    for window in 100 150; do
        echo "########################################"
        echo "# ${scen} window=${window}yr (12 cells)"
        echo "########################################"
        for rev in 0.000 0.0025 0.005 0.0075 0.010 0.015; do
            for sub in 0.00 0.30; do
                run_cell "$scen" "$sub" "$rev" "$window"
            done
        done
    done
done

rm -f "$PATCHED"

echo "ALL DONE. Total elapsed: $(elapsed)"
