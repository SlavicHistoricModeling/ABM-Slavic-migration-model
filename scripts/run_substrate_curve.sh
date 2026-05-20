#!/usr/bin/env bash
# Batch 2 — substrate response curve
# 6 substrate fractions x 3 Slavic scenarios = 18 runs, num_runs=10, seed=42.
# (Arabic excluded: substrate is a Slavic-specific concept; the code
# only applies --substrate to the slavic group's initial_fraction.)
# Output: results_substrate_<scenario>_<fraction>.txt per pair.
# Total wall time estimate: ~4 hours.

set -e
start=$(date +%s)

# Substrate fraction 0.00 is the no-substrate baseline (already covered
# by the matrix, but re-run here for the same-conditions response curve).
for f in 0.00 0.10 0.20 0.30 0.40 0.50; do
    for s in slavic1 slavic2 slavic3; do
        tag="substrate_${s}_${f}"
        echo "=== START $tag at $(date +%H:%M:%S) (elapsed $(( ($(date +%s) - start) / 60 )) min) ==="
        if [ "$f" = "0.00" ]; then
            # 0% substrate: don't pass --substrate at all (so the scenario's
            # default initial_fraction 0.1 applies, matching the matrix).
            python slavic_migration_submited_v1.py \
                --scenario "$s" \
                --num_runs 10 \
                --seed 42
        else
            python slavic_migration_submited_v1.py \
                --scenario "$s" \
                --num_runs 10 \
                --seed 42 \
                --substrate \
                --substrate_fraction "$f"
        fi
        cp "results_${s}.txt" "results_${tag}.txt"
        echo "=== DONE  $tag at $(date +%H:%M:%S) ==="
    done
done

echo "ALL DONE. Total elapsed: $(( ($(date +%s) - start) / 60 )) min"
