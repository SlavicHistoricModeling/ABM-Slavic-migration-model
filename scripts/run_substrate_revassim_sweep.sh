#!/usr/bin/env bash
# Substrate × reverse-assimilation 2-parameter sweep (response7 step 1).
#
# substrate fraction:    {0.00, 0.10, 0.20, 0.30, 0.40, 0.50}
# reverse_assim_rate:    {0.000, 0.015, 0.030, 0.045}
# scenarios:             slavic1 (REQUIRED), slavic2 (if compute allows)
#
# The reverse_assim_rate parameter has no CLI override in the canonical
# engine. To avoid modifying the canonical file (per response7 §4
# "no new flags, no further substrate-logic edits, no refactors"), we
# sed-patch a TEMPORARY copy of the engine in /tmp per sweep cell and
# run that copy. The canonical file at $CANONICAL is untouched.
#
# This is the explicit substrate-conjecture adjudication run per
# response7 step 1; output to docs/run_logs/2026-05-16_substrate_revassim_sweep.md
# (decision-criterion log written separately).
#
# Wall time estimate:
#   slavic1: 24 cells × ~2 min = ~48 min
#   slavic2: 24 cells × ~5 min = ~120 min
#   total:   ~3 hours

set -e
start=$(date +%s)
elapsed() { echo "$(( ($(date +%s) - start) / 60 )) min"; }

CANONICAL=slavic_migration_submited_v1.py
PATCHED=/tmp/slavic_revassim_patched.py

run_cell() {
    local scenario=$1
    local sub_frac=$2
    local rev_rate=$3
    local tag="revassim_${scenario}_sub${sub_frac}_rev${rev_rate}"
    echo "=== START $tag at $(date +%H:%M:%S) (elapsed $(elapsed)) ==="

    # Patch the reverse_assimilation_rate across all scenarios in a
    # /tmp copy; only the scenario we're invoking uses the patched
    # value. The canonical file is not modified.
    sed -E "s/(\"reverse_assimilation_rate\":[[:space:]]*)[0-9.]+/\1${rev_rate}/g" \
        "$CANONICAL" > "$PATCHED"

    if [ "$sub_frac" = "0.00" ]; then
        # No --substrate; default Slavic placement (eastern/central),
        # default Slavic initial_fraction (0.1 for Slavic scenarios).
        python "$PATCHED" --scenario "$scenario" --num_runs 10 --seed 42
    else
        python "$PATCHED" --scenario "$scenario" --num_runs 10 --seed 42 \
            --substrate --substrate_fraction "$sub_frac"
    fi
    cp "results_${scenario}.txt" "results_${tag}.txt"
    echo "=== DONE  $tag at $(date +%H:%M:%S) ==="
}

# REQUIRED: slavic1 sweep (24 cells)
echo "########################################"
echo "# slavic1 sub × rev sweep (REQUIRED, 24 cells)"
echo "########################################"
for rev in 0.000 0.015 0.030 0.045; do
    for sub in 0.00 0.10 0.20 0.30 0.40 0.50; do
        run_cell slavic1 "$sub" "$rev"
    done
done

# OPTIONAL: slavic2 sweep (24 cells) if compute allows
echo "########################################"
echo "# slavic2 sub × rev sweep (optional, 24 cells)"
echo "########################################"
for rev in 0.000 0.015 0.030 0.045; do
    for sub in 0.00 0.10 0.20 0.30 0.40 0.50; do
        run_cell slavic2 "$sub" "$rev"
    done
done

# Clean up the patched temp file
rm -f "$PATCHED"

echo "ALL DONE. Total elapsed: $(elapsed)"
