# Clean-room reproduction — response5 step 1

> 2026-05-16. Verifies the canonical post-fix matrix and substrate-curve
> numbers from an isolated git worktree at commit `66f1d6b` under
> two different `PYTHONHASHSEED` values. **Result: all nine scenarios
> bit-identical between hash seeds AND digit-exact against canonical.**

## Methodology

1. **Worktree isolation.** A separate git worktree was created at
   `../ABM-cleanroom`, detached-HEAD at commit `66f1d6b` (the
   determinism-fix commit). The worktree shares the `.git`
   directory with the main repo but has its own working tree, so
   no session-state files (e.g., gitignored `results_*.txt` from
   earlier in this session) can pollute the verification.
2. **Cross-process determinism test.** Each scenario was run twice
   from the worktree, with explicit `PYTHONHASHSEED=0` for the
   first run and `PYTHONHASHSEED=12345` for the second. The
   determinism-fix claim is "bit-identical output across processes
   regardless of hash randomisation"; this is the literal test.
3. **Canonical cross-check.** Each scenario's numbers were also
   compared digit-exact to the canonical numbers recorded in
   `2026-05-15_matrix_batch.md` and `2026-05-16_substrate_curve.md`
   (which were produced on the same Windows host under random
   `PYTHONHASHSEED`).
4. **Verification subset** per response5 step 1: slavic1 matrix,
   slavic3 matrix, slavic3 uniform-mortality counterfactual, and
   the full slavic1 substrate response curve (6 fractions). Each
   at seed 42, `--num_runs 10`.
5. **Wall time:** 94 minutes total (9 scenarios × 2 hash seeds =
   18 runs).

## Limitation: same-machine

response5 specified "ideally on a different machine/architecture
than the cascade ran on (the Fedora box or Talos, not the Windows
host that produced the numbers)". This was **not possible** in
this session because the SSH pool fix is still blocked on
host-side ACL changes (see DECISIONS.md "Pool-onboarding" entry;
`scripts/POOL_SETUP.md` §1 for the commands).

The available substitute was:

- Worktree isolation (clean filesystem state, no session pollution).
- Two explicitly-set `PYTHONHASHSEED` values (the load-bearing test
  for the *specific* bug that was fixed — hash-randomisation
  non-determinism).

**What this verifies:** the determinism fix correctly removes the
process-to-process variability that the bug introduced. Two
different `PYTHONHASHSEED` values produce bit-identical output
from a clean checkout, and that output matches the canonical
numbers exactly.

**What it does not verify:** cross-platform reproducibility
(CPython version differences, OS-level float behaviour, ARM vs
x86, etc.). For a paper claim of "reproducible on any machine,"
an additional run on Fedora or another architecture remains
desirable. Cross-platform reproducibility is recommended for
the reproducibility statement to claim more than "Windows /
Python 3.13.2 / x86-64."

## Results — bit-identity test (PYTHONHASHSEED=0 vs 12345)

For each scenario, the full per-year trajectory was compared
(everything after the run-config header line, which is expected
to differ in trivial ways like flag values). Verdict:

| scenario | PYTHONHASHSEED=0 final | PYTHONHASHSEED=12345 final | trajectory bit-identical? |
|---|---|---|---|
| slavic1 matrix | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ YES |
| slavic3 matrix | 93.99 % ± 1.69 % | 93.99 % ± 1.69 % | ✓ YES |
| slavic3 uniform mortality | 93.96 % ± 1.50 % | 93.96 % ± 1.50 % | ✓ YES |
| slavic1 substrate 0 % | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ YES |
| slavic1 substrate 10 % | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ YES |
| slavic1 substrate 20 % | 27.75 % ± 4.50 % | 27.75 % ± 4.50 % | ✓ YES |
| slavic1 substrate 30 % | 40.33 % ± 2.62 % | 40.33 % ± 2.62 % | ✓ YES |
| slavic1 substrate 40 % | 47.18 % ± 4.11 % | 47.18 % ± 4.11 % | ✓ YES |
| slavic1 substrate 50 % | 52.76 % ± 2.93 % | 52.76 % ± 2.93 % | ✓ YES |

**9/9 scenarios bit-identical across hash seeds.** The
determinism-fix's cross-process claim is verified.

## Results — digit-exact match to canonical

The canonical numbers (recorded in `2026-05-15_matrix_batch.md`
and `2026-05-16_substrate_curve.md`) were produced on the same
Windows host under random `PYTHONHASHSEED` during the
`scripts/rerun_all_postfix.sh` cascade. The cleanroom outputs
match each canonical number digit-exact:

### Matrix subset

| scenario | canonical | cleanroom (both hash seeds) | match? |
|---|---|---|---|
| slavic1 | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ EXACT |
| slavic3 | 93.99 % ± 1.69 % | 93.99 % ± 1.69 % | ✓ EXACT |
| slavic3 uniform mortality | 93.96 % ± 1.50 % | 93.96 % ± 1.50 % | ✓ EXACT |

### slavic1 substrate response curve

| substrate fraction | canonical | cleanroom (both hash seeds) | match? |
|---|---|---|---|
| 0.00 | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ EXACT |
| 0.10 | 18.35 % ± 4.40 % | 18.35 % ± 4.40 % | ✓ EXACT |
| 0.20 | 27.75 % ± 4.50 % | 27.75 % ± 4.50 % | ✓ EXACT |
| 0.30 | 40.33 % ± 2.62 % | 40.33 % ± 2.62 % | ✓ EXACT |
| 0.40 | 47.18 % ± 4.11 % | 47.18 % ± 4.11 % | ✓ EXACT |
| 0.50 | 52.76 % ± 2.93 % | 52.76 % ± 2.93 % | ✓ EXACT |

**9/9 scenarios digit-exact match to canonical.**

## Conclusion

Step 1 of response5 **passes**:

1. The determinism fix's "bit-identical cross-process output"
   claim is verified literally: two different `PYTHONHASHSEED`
   values produce identical trajectories on all 9 tested
   scenarios.
2. The canonical numbers reported in the prose-instance briefing
   reproduce digit-exact from a clean worktree at the engine-
   frozen commit `66f1d6b`.
3. No bug-4 candidate is surfaced by this verification. The
   numbers in the briefing are reproducible by anyone who has
   the repository at `66f1d6b` and runs at seed 42.

**Caveat retained:** same-machine verification only (Windows /
Python 3.13.2 / x86-64). Cross-architecture verification still
desirable for the published reproducibility statement; see
"Limitation" above.

**Next step:** response5 step 2 (deliberate code audit) is now
unblocked. Steps 3 / 4 / 5 (figures, results table pack,
reproducibility statement) can run in parallel after step 2.

## Provenance

- Worktree: `../ABM-cleanroom`, detached HEAD at `66f1d6b`.
- Script: `scripts/cleanroom_repro.sh`.
- Log: `scripts/cleanroom_repro.log`.
- Result files: `../ABM-cleanroom/cleanroom_<HSEED>_<tag>.txt`
  (gitignored alongside the regular `results_*.txt` files).
- Python: 3.13.2 on Windows / x86-64.
- Wall time: 94 minutes.
- Date: 2026-05-16.
