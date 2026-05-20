#!/usr/bin/env bash
# Master re-run script for all batch 1 + batch 2 results post-fix.
# Executes sequentially in priority order:
#   1. Matrix batch 1 re-run (6 runs, ~45 min)
#   2. Plague-mortality sweep (16 runs, ~96 min)
#   3. Substrate response curve (18 runs, ~4 hrs)
#   4. INHERITANCE_AGE_MAX sweep (12 runs, ~2.5 hrs)
# Total estimate: ~8 hours.
#
# All output files (results_*.txt) are gitignored; the durable
# logs in docs/run_logs/ are updated separately after this completes.

set -e
start=$(date +%s)

elapsed() { echo "$(( ($(date +%s) - start) / 60 )) min"; }

echo "========================================"
echo "PHASE 1: Matrix batch 1 re-run (6 runs)"
echo "========================================"

for s in slavic1 slavic2 slavic3 arabic; do
    echo "=== MATRIX $s at $(date +%H:%M:%S) (elapsed $(elapsed)) ==="
    python slavic_migration_submited_v1.py --scenario "$s" --num_runs 10 --seed 42
    cp "results_${s}.txt" "results_${s}_matrix.txt"
done

echo "=== MATRIX slavic3 + uniform_mortality at $(date +%H:%M:%S) (elapsed $(elapsed)) ==="
python slavic_migration_submited_v1.py --scenario slavic3 --num_runs 10 --seed 42 --uniform_mortality
cp results_slavic3.txt results_slavic3_uniformmort_matrix.txt

echo "=== MATRIX arabic + ruleoff at $(date +%H:%M:%S) (elapsed $(elapsed)) ==="
python slavic_migration_submited_v1.py --scenario arabic --num_runs 10 --seed 42 --inheritance_age_max 99
cp results_arabic.txt results_arabic_ruleoff_matrix.txt

echo
echo "========================================"
echo "PHASE 2: Plague-mortality sweep (16 runs)"
echo "========================================"
bash scripts/run_plague_sweep.sh

echo
echo "========================================"
echo "PHASE 3: Substrate response curve (18 runs)"
echo "========================================"
bash scripts/run_substrate_curve.sh

echo
echo "========================================"
echo "PHASE 4: INHERITANCE_AGE_MAX sweep (12 runs)"
echo "========================================"
bash scripts/run_inheritance_sweep.sh

echo
echo "ALL DONE. Total elapsed: $(elapsed)"
