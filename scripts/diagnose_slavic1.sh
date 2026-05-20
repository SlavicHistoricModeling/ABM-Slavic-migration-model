#!/usr/bin/env bash
# Diagnostic: does --non_slavic_plague_mortality 0.15 (= default) at
# HEAD give the same result as no flag? Matrix slavic1 (acd3ae3, no
# flag) = 18.35%. Plague_slavic1_0.15 (HEAD, with flag at default) =
# 16.82%. Both should be 18.35% if my flag is a no-op when value
# matches default. This diagnostic determines which is right.

set -e

echo "=== Test A: slavic1 at HEAD, NO flag ==="
python slavic_migration_submited_v1.py --scenario slavic1 --num_runs 10 --seed 42
cp results_slavic1.txt results_diag_slavic1_noflag.txt
head -2 results_diag_slavic1_noflag.txt

echo
echo "=== Test B: slavic1 at HEAD, WITH --non_slavic_plague_mortality 0.15 ==="
python slavic_migration_submited_v1.py --scenario slavic1 --num_runs 10 --seed 42 --non_slavic_plague_mortality 0.15
cp results_slavic1.txt results_diag_slavic1_flag015.txt
head -2 results_diag_slavic1_flag015.txt

echo
echo "=== COMPARISON ==="
echo "Matrix (acd3ae3, no flag):        Avg Final Proportion: 18.35% (+/-4.40%)"
echo "Test A (HEAD, no flag):           $(head -2 results_diag_slavic1_noflag.txt | tail -1)"
echo "Plague sweep (HEAD, flag 0.15):   Avg Final Proportion: 16.82% (+/-3.90%)"
echo "Test B (HEAD, flag 0.15):         $(head -2 results_diag_slavic1_flag015.txt | tail -1)"
