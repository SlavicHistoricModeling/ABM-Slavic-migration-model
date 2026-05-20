#!/usr/bin/env bash
# Batch 2 — plague-mortality sensitivity sweep
# 4 mortality values x 4 scenarios = 16 runs, num_runs=10, seed=42.
# Output: results_plague_<scenario>_<value>.txt per pair.
# Total wall time estimate: ~3 hours.

set -e
start=$(date +%s)

for m in 0.10 0.12 0.15 0.20; do
    for s in slavic1 slavic2 slavic3 arabic; do
        tag="plague_${s}_${m}"
        echo "=== START $tag at $(date +%H:%M:%S) (elapsed $(( ($(date +%s) - start) / 60 )) min) ==="
        python slavic_migration_submited_v1.py \
            --scenario "$s" \
            --num_runs 10 \
            --seed 42 \
            --non_slavic_plague_mortality "$m"
        cp "results_${s}.txt" "results_${tag}.txt"
        echo "=== DONE  $tag at $(date +%H:%M:%S) ==="
    done
done

echo "ALL DONE. Total elapsed: $(( ($(date +%s) - start) / 60 )) min"
