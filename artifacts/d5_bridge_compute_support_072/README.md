# D5 Bridge Compute Support 072

This artifact answers the narrow `071` compute-support prompt without reopening broad search.

## Main result

The checked data support a sharper exact reduction picture:

1. **Slice-chain bridge:** on the regular carry_jump slice union, the expected affine offset normalization
   `q = s - source_u - w (mod m)` is exact for the carry mark and deterministic on successor.
   The other natural candidates tested here (`s`, `s-source_u`, `s-w`) all fail.
2. **Larger-modulus support:** the bundled `068B` artifact already keeps the marked length-`m` chain,
   beta drift, and `(B,beta)` exactness alive on regenerated full rows through `m=21`, with branch-local
   scheduler support through `m=41`.
3. **State-level union of chains:** the bare normalized `m`-state beta quotient is **not** exact for current
   `epsilon4` or the short-corner detector on the frozen exhaustive range `m=5,7,9,11`.
   Its first collisions occur exactly at the two early post-carry positions.
4. **Supported sharper object:** on that same frozen range, a decorated `4m`-state beta-chain quotient
   `(m,beta,a,b)` is exact for current `epsilon4`, deterministic on successor, and exact for the short-corner detector.
   The decorations satisfy
   - `a = 1` iff `q = m-1`
   - `b = 1` iff `(q + sigma = 1 mod m)` or `(q = m-1 and sigma != 1)`, where `sigma = source_u + w mod m`.

So the checked data **contradict** the candidate bridge “offset normalization alone gives one exact `m`-state beta quotient for current `epsilon4`”, but they **support** a slightly richer decorated union-of-chains quotient.

## Files

- `data/analysis_summary.json`
- `data/offset_normalization_checks.json`
- `data/state_chain_union_quotients.json`
- `data/chain_type_formula_validation.json`
- `logs/summary.log`
- `scripts/torus_nd_d5_bridge_compute_support_072.py`
