#!/usr/bin/env bash
# Clean-room reproduction script for response5 step 1.
#
# Runs the verification subset from an isolated git worktree at the
# canonical commit (66f1d6b), under TWO different PYTHONHASHSEED
# values, to literally test the determinism fix's claim of
# bit-identical cross-process output.
#
# Subset per response5: slavic1, slavic3, slavic3-uniformmort, plus
# the full slavic1 substrate curve (0/10/20/30/40/50 %).
#
# Run from: d:\ABM migration theory (the main repo)
# Reads from: ../ABM-cleanroom (the git worktree at 66f1d6b)
# Writes results to: ../ABM-cleanroom/results_*.txt then copies to
#                   ../ABM-cleanroom/cleanroom_<seed>_<tag>.txt
#
# Total wall time estimate: ~170 min (85 min per PYTHONHASHSEED value).

set -e
start=$(date +%s)
elapsed() { echo "$(( ($(date +%s) - start) / 60 )) min"; }

WORKTREE=../ABM-cleanroom

for HSEED in 0 12345; do
    echo "========================================"
    echo "PYTHONHASHSEED=$HSEED at $(date +%H:%M:%S) (cumulative elapsed $(elapsed))"
    echo "========================================"

    pushd "$WORKTREE" > /dev/null

    # Matrix subset: slavic1, slavic3, slavic3-uniformmort
    for run in \
        "slavic1::--scenario slavic1 --num_runs 10 --seed 42" \
        "slavic3::--scenario slavic3 --num_runs 10 --seed 42" \
        "slavic3_uniformmort::--scenario slavic3 --num_runs 10 --seed 42 --uniform_mortality"; do
        tag="${run%%::*}"
        args="${run##*::}"
        echo "--- $tag (HSEED=$HSEED) at $(date +%H:%M:%S) ---"
        PYTHONHASHSEED=$HSEED python slavic_migration_submited_v1.py $args
        cp results_slavic*.txt /tmp/dummy.txt 2>/dev/null || true
        # Pick the right scenario file
        if [[ "$tag" == slavic1* ]]; then
            src=results_slavic1.txt
        else
            src=results_slavic3.txt
        fi
        cp "$src" "cleanroom_${HSEED}_${tag}.txt"
    done

    # slavic1 substrate curve, 6 fractions
    for f in 0.00 0.10 0.20 0.30 0.40 0.50; do
        tag="slavic1_substrate_${f}"
        echo "--- $tag (HSEED=$HSEED) at $(date +%H:%M:%S) ---"
        if [ "$f" = "0.00" ]; then
            PYTHONHASHSEED=$HSEED python slavic_migration_submited_v1.py \
                --scenario slavic1 --num_runs 10 --seed 42
        else
            PYTHONHASHSEED=$HSEED python slavic_migration_submited_v1.py \
                --scenario slavic1 --num_runs 10 --seed 42 --substrate --substrate_fraction "$f"
        fi
        cp results_slavic1.txt "cleanroom_${HSEED}_${tag}.txt"
    done

    popd > /dev/null
done

echo
echo "ALL DONE. Total elapsed: $(elapsed)"
echo "Result files in $WORKTREE/cleanroom_*.txt"
