#!/usr/bin/env bash
# Batch 2 — INHERITANCE_AGE_MAX sweep
# 4 age values x 3 scenarios = 12 runs, num_runs=10, seed=42.
# (slavic2 deliberately excluded per response3/4 cap: robustness check
# is sufficient with slavic1 + slavic3 endpoints plus Arabic.)
# Output: results_inheritance_<scenario>_<age>.txt per pair.
# Total wall time estimate: ~2.5 hours.

set -e
start=$(date +%s)

for a in 22 25 28 30; do
    for s in slavic1 slavic3 arabic; do
        tag="inheritance_${s}_${a}"
        echo "=== START $tag at $(date +%H:%M:%S) (elapsed $(( ($(date +%s) - start) / 60 )) min) ==="
        python slavic_migration_submited_v1.py \
            --scenario "$s" \
            --num_runs 10 \
            --seed 42 \
            --inheritance_age_max "$a"
        cp "results_${s}.txt" "results_${tag}.txt"
        echo "=== DONE  $tag at $(date +%H:%M:%S) ==="
    done
done

echo "ALL DONE. Total elapsed: $(( ($(date +%s) - start) / 60 )) min"
