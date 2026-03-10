# d=5 progress note v5

Problem:
Prove the `d=5` case: for every `m >= 3`, the directed torus
`D_5(m) = Cay((Z_m)^5, {e_0,e_1,e_2,e_3,e_4})`
admits a Hamilton decomposition into five arc-disjoint directed Hamilton cycles.

Current target:
Exploit the `m=5` 26-move witness by extracting exact return-map formulas in the color-covariant frame, and isolate any branch that already closes for all odd `m`.

New partial theorem:
- [P] For every odd `m >= 5`, the fixed 26-move witness already makes **color 3** Hamilton.
  Equivalently, if `f_3` is the color-3 step map defined by that witness, then `f_3` is a single directed Hamilton cycle on `D_5(m)`.

Why this matters:
- This is the first branch in the current d=5 project that is no longer merely computational pattern-hunting.
- It shows the affine-pinned low-layer architecture is genuinely correct: one whole Hamilton color can already be proved from it for all odd `m >= 5`.
- The proof also exposes a clean nested-skew-product structure
  `P0 -> (q,w,u)-base -> v-cocycle`,
  which is exactly the kind of mechanism expected from the d=3/d=4 notes.

Setup:
Use the known 26-move witness with support semantics
- `plane(t) := {S = t}`,
- `line1(t,i,a) := {S=t, x_i = a}`,
- `line2(t,[i,j],[a,b]) := {S=t, x_i=a, x_j=b}`.

Fix color `c=3`. On `P0 = {x : S(x)=0}` use relative coordinates
`(q,w,v,u) = (x_4, x_0, x_1, x_2)`,
so `x_3 = -(q+w+v+u)`.

Exact layer-by-layer rule for color 3:
Let `d_t(q,w,u)` be the direction used by color 3 on layer `t` during the first return from `P0` back to `P0`.
Then for every `m >= 5` these formulas are exact:

- [P] layer 0:
  `d0 = 2` if `(q,w)=(0,0)`;
  else `d0 = 1` if `u=3` or `(u=0 and q=1)`;
  else `d0 = 3`.

- [P] layer 1:
  `d1 = 4` if `(w,u)=(1,0)`;
  else if `w=4` then `d1 = 2` when `q=3`, and `d1 = 1` otherwise;
  else `d1 = 3`.

- [P] layer 2:
  Let `x4^(2) = q + 1_{(w,u)=(1,0)}` be the current `x_4` entering layer 2.
  Then
  `d2 = 2` if `(x4^(2)=4 and w=0)` or `(x4^(2) != 4 and w=2)`;
  else `d2 = 1` if `x4^(2)=4`;
  else `d2 = 3`.

  Equivalently, directly in `(q,w,u)`:
  - `d2 = 2` for `(w=0,q=4)` or `(w=2,q != 4)`;
  - `d2 = 1` for `(w=1,u=0,q=3)` or `(q=4 and w != 0 and not (w=1 and u=0))`;
  - otherwise `d2 = 3`.

- [P] layer 3:
  `d3 = 0` always.

Thus the color-3 first return on `P0` is
`R_3(q,w,v,u) = (q + 1_{(w,u)=(1,0)}, w+1, v + beta(q,w,u), u + gamma(q,w))`,
where
- `gamma(q,w) = 1` iff
  `(w=0 and q in {0,4}) or (w=2 and q != 4) or (w=4 and q=3)`,
- `beta(q,w,u)` is the number of indices `t in {0,1,2}` with `d_t(q,w,u)=1`.

Immediate consequences:
- [P] `R_3` is independent of `v` except for the additive cocycle `beta`.
- [P] The base map on `(q,w,u)` is
  `B(q,w,u) = (q + 1_{(w,u)=(1,0)}, w+1, u + gamma(q,w))`.

First nested return:
Let `U = B^m |_{w=0}`. Then:
- [P] `U` acts on `(q,u)` by the explicit row rules

  - row `q=0`:
    `(0,u) -> (0,u+2)` for `u != m-1`, and `(0,m-1) -> (1,1)`;

  - row `q=1`:
    `(1,0) -> (2,1)`, and `(1,u) -> (1,u+1)` for `u != 0`;

  - row `q=2`:
    `(2,0) -> (3,2)`, and `(2,u) -> (2,u+1)` for `u != 0`;

  - row `q=3`:
    `(3,0) -> (4,0)`, and `(3,u) -> (3,u+2)` for `u != 0`;

  - row `q=4`:
    `(4,m-1) -> (5 mod m, 1)`, and `(4,u) -> (4,u+1)` for `u != m-1`;

  - rows `q=5,...,m-1`:
    `(q,0) -> (q+1 mod m, 1)`, and `(q,u) -> (q,u+1)` for `u != 0`.

- [P] For odd `m`, this `U` is a single `m^2`-cycle:
  starting from `(0,0)` it traverses
  1. row `0` on the even residues,
  2. rows `1` and `2` completely,
  3. row `3` on all nonzero residues by step `+2`, then `0`,
  4. rows `4,5,...,m-1` completely,
  5. row `0` on the odd residues,
  and returns to `(0,0)`.

Therefore:
- [P] `U` one cycle on `(q,u)` implies `B` one cycle on `(q,w,u)` of length `m^3`, because `w` is an absolute clock incremented by `+1` each step.

Final lift:
Since `R_3(q,w,v,u) = (B(q,w,u), v + beta(q,w,u))`,
color-3 Hamiltonicity reduces to the cocycle sum of `beta` over the unique `B`-cycle.
Because `B` is one cycle, this sum is the full-space sum over `(q,w,u)`.

Counting:
- [P] `d0=1` on `m^2 + m - 1` states;
- [P] `d1=1` on `m(m-1)` states;
- [P] `d2=1` on `m(m-1)` states.

Hence
`sum beta = (m^2 + m - 1) + m(m-1) + m(m-1) = 3m^2 - m - 1`,
so
`sum beta ≡ -1 (mod m)`.

By the standard skew-product lifting lemma:
- [P] Since `B` is one cycle on `m^3` states and the total `beta` increment over that cycle is a unit mod `m`, `R_3` is one cycle on `m^4` states.
- [P] Since `S` is an absolute clock, `f_3` itself is one cycle on all `m^5` vertices.

Computational checks:
- [C] The exact formulas above were matched against the reconstructed witness for `m = 5,7,9,11,13`.
- [C] For these `m`, the induced color-3 first return on `P0` has exactly one cycle of length `m^4`.
- [C] The `(q,w,u)` base map `B` has exactly one cycle of length `m^3`.
- [C] The section map `U` on `w=0` has exactly one cycle of length `m^2`.
- [C] The total `beta` sum is `m-1`.

Current interpretation:
- [P] The affine-pinned route is not just philosophically correct; it already yields one full odd-`m` Hamilton color from the fixed 26-move witness.
- [H] The remaining problem is now to extend this from one color to a full 5-color decomposition, probably by extracting analogous stable branches for the other colors or by replacing the asymmetric witness with a cyclically organized affine-pinned family.
- [O] Full `d=5` remains open.

Next branching options:
1. Derive equally explicit return formulas for color 0/1/4 and identify why they fail on `m=7,9`.
2. Search for a small affine-pinned modification that preserves the proven color-3 branch while repairing the other four colors.
3. Try to repackage the color-3 proof into a rotationally organized template that can be cloned across colors.
