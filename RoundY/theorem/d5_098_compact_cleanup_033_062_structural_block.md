# D5 098: Compact cleanup of the remaining 033/062 structural block

This note handles the last localized structural block that still sat outside the
cleaned odd-`m` D5 package after `092` and the reproof notes `095`--`097`.
It does **not** address the separate compact-bridge task around `076`.

It treats `033` and `062` asymmetrically.

- `062` is fully rewritten as a compact first-exit theorem with the pre-exit
  patch-avoidance argument written out.
- `033` is compressed to the only theorem content later notes actually use:
  the exact trigger-family formula for `H_{L1}`.

The note does **not** attempt to rebuild the full defect-template quotient of
`033` from scratch. That larger classification project is separate from the D5
odd-`m` globalization chain.

## 1. Scope and status

Fix odd `m` in the accepted D5 regime and the best-seed channel

`R1 -> H_{L1}`

with seed words

`L = [2,2,1]`, `R = [1,4,4]`.

Use current coordinates `(q,w,u,Theta)` along the active branch after the
alternate-`2` entry out of `R1`.

The downstream use of the old `033/062` block is only:

1. identify the exact trigger family `H_{L1}`;
2. derive the universal family-dependent first-exit targets;
3. prove that the actual active branch agrees with the candidate branch up to
   first exit.

So the real question is not whether the entire defect-template analysis must be
rebuilt. The real question is whether the odd-`m` package still needs a separate
structural theorem package. After this note, the answer is essentially no:
`062` is inlined, and `033` is reduced to one exact trigger-family lemma. The
separate compact-bridge task around `076` is not addressed here.

## 2. The only 033 theorem content needed downstream

### Proposition 2.1 (exact trigger family)
For the unresolved best-seed channel `R1 -> H_{L1}`, the target hole family is
exactly

`H_{L1} = {(q,w,u,Theta) = (m-1,m-1,u,2) : u != 2}`.

Equivalently:

1. the target layer is `Theta = 2`;
2. the target current coordinates satisfy `q = w = m-1`;
3. the only excluded fiber is `u = 2`.

### Proof status
This is the promoted theorem content of `033`. The present note does not try to
re-prove the full defect-template classification from the raw artifact; it
isolates the exact formula that later theorems use.

### Proposition 2.2 (pilot-range exact verification)
The artifact file

`artifacts/d5_defect_splice_transducer_033/data/best_seed_defect_templates.json`

matches Proposition 2.1 exactly on the saved pilot moduli:

| `m` | target count | parameter values | representative `(q,w,u,Theta)` |
|---|---:|---|---|
| `5` | `20 = 5·4` | `{0,1,3,4} = Z_5 \ {2}` | `(4,4,4,2)` |
| `7` | `42 = 7·6` | `{0,1,3,4,5,6} = Z_7 \ {2}` | `(6,6,4,2)` |
| `9` | `72 = 9·8` | `{0,1,3,4,5,6,7,8} = Z_9 \ {2}` | `(8,8,4,2)` |

So the saved defect-family artifact matches exactly the formula

`H_{L1} = {(m-1,m-1,u,2) : u != 2}`

on the pilot range.

This is an exact saved-data verification, not a replacement for a general proof
of the full defect-template classification.

## 3. Candidate orbit and phase-1 invariant

Define the source residue

`rho := u_source + 1 (mod m)`

where `u_source` is the source-`u` label of the chosen `R1` family.
Start at the alternate-`2` entry

`E = (m-1,1,u_source,2)`.

Define the candidate orbit `xhat_n = (q_n,w_n,u_n,Theta_n)` by

- `Fhat(q,w,u,0) = (q+1,w,u,1)`
- `Fhat(q,w,u,1) = (q,w,u+1,2)`
- `Fhat(q,w,u,2) = (q, w + 1_{q=m-1}, u, 3)`
- `Fhat(q,w,u,Theta) = (q,w,u,Theta+1)` for `3 <= Theta <= m-1`

On the section `Theta = 2`, this induces the odometer return map

`(q,w) -> (q+1, w + 1_{q=m-1})`.

Equivalently, with

`eta(q,w) := q + m(w-1) - (m-1)`,

one has `eta -> eta + 1`.

The only two phase-`1` states whose direction-`2` or direction-`1` successor can
reach `(q,w) = (m-1,m-1)` are

- `A = (m-1,m-2,1)`
- `B = (m-2,m-1,1)`

with indices

- `eta(A) = m(m-3)`
- `eta(B) = m(m-2)-1`

so `A` is encountered before `B`.

### Lemma 3.1 (phase-1 source-residue invariant)
Along the candidate orbit, every phase-`1` current state satisfies

`q = u - rho + 1 (mod m)`.

Hence

- `u(A) = rho - 2 (mod m)`
- `u(B) = rho - 3 (mod m)`.

#### Proof
The first phase-`1` state after entry is `(0,2,u_source,1)`, so the relation
holds there because `u_source = rho - 1`.

From one phase-`1` state to the next, the phase-`1` witness step increments `u`
by `1`, the later phase-`0` witness step increments `q` by `1`, and no other
step changes either coordinate. So the congruence is preserved.

### Lemma 3.2 (phase-1 trigger criterion)
Let `x` be a phase-`1` current state on the candidate orbit.
An alternate step from `x` lands in `H_{L1}` if and only if one of the
following holds:

1. `x = A = (m-1,m-2,1)` and `u(x) != 2`, in which case direction `2` lands in
   `H_{L1}`;
2. `x = B = (m-2,m-1,1)` and `u(x) != 2`, in which case direction `1` lands in
   `H_{L1}`.

#### Proof
By Proposition 2.1, the successor must satisfy

`(q',w',Theta') = (m-1,m-1,2)` and `u' != 2`.

Only phase-`1` states can step to layer `2`, and only directions `1` and `2`
change `q` or `w`. So the only two ways to reach `(q',w') = (m-1,m-1)` are:

- direction `2` from `(q,w) = (m-1,m-2)`;
- direction `1` from `(q,w) = (m-2,m-1)`.

Those are exactly `A` and `B`. Directions `1` and `2` preserve `u`, so the only
extra condition is `u != 2`.

## 4. Universal first exits and pre-exit patch avoidance

### Proposition 4.1 (candidate first exits)
On the candidate orbit:

1. if `rho != 4` (regular family), the first exit to `H_{L1}` occurs at
   `A = (m-1,m-2,1)` by direction `2`;
2. if `rho = 4` (exceptional family), the state `A` does not exit and the first
   exit to `H_{L1}` occurs at `B = (m-2,m-1,1)` by direction `1`.

Equivalently,

- `T_reg = (m-1,m-2,1)`
- `T_exc = (m-2,m-1,1)`.

#### Proof
By Lemma 3.2, only `A` and `B` can trigger an exit to `H_{L1}`. Since `A` is
encountered first, it is enough to test whether `u(A) = 2`.

By Lemma 3.1,

`u(A) = rho - 2 (mod m)`.

So `u(A) = 2` iff `rho = 4`.

- If `rho != 4`, then `u(A) != 2`, so the first exit is at `A` by direction `2`.
- If `rho = 4`, then `u(A) = 2`, so `A` is blocked.

Still in the exceptional case, Lemma 3.1 gives

`u(B) = rho - 3 = 1 (mod m)`.

So `u(B) != 2`, and the first exit is at `B` by direction `1`.

### Lemma 4.2 (only patch-table facts used)
For the pre-exit argument, only the following coarse patch-table facts are used:

1. the classes `R1, R2, R3, L2` require `w = 0`;
2. the class `L3` requires `w = 1`;
3. a pre-exit occurrence of `L1` would require the branch to have already
   reached the `w = m-1` edge of the corridor.

No finer information from the patch table is needed.

### Lemma 4.3 (pre-exit patch avoidance on the candidate orbit)
Let `N_f` be the first-exit time of the candidate orbit in the chosen source
family `f`. For every `0 <= n < N_f`, the candidate state `xhat_n` avoids all
patched current classes.

#### Proof
The value `w` starts at `1` and changes only by the increment `w -> w+1` at
phase `2` with `q = m-1`. So `w` never decreases, and `w = 0` never occurs
before exit. By Lemma 4.2(1), the classes `R1, R2, R3, L2` are impossible.

The value `w = 1` occurs only at the entry state `(m-1,1,u_source,2)`, because
the first phase-`2` wrap immediately creates `w = 2` and thereafter `w` never
decreases. So by Lemma 4.2(2), the class `L3` cannot occur after entry. Since
the entry state itself is the alt-`2` start state rather than a patched class,
`L3` is absent on the whole pre-exit segment.

On a regular family, Proposition 4.1 says the branch exits already at
`A = (m-1,m-2,1)`, before `w` can ever reach `m-1`. So `L1` is impossible.

On the exceptional family, the first creation of `w = m-1` occurs at phase `3`
from `(m-1,m-2,2)`. The next phase-`1` state then has `(q,w) = (0,m-1)`, not
`(m-1,m-1)`. The first later phase-`1` state with `w = m-1` that could also
carry `q = m-1` would occur strictly after `B = (m-2,m-1,1)`, but
Proposition 4.1 says the branch exits already at `B`. So `L1` is impossible
before exceptional exit as well.

Thus no patched current class is encountered before first exit.

### Theorem 4.4 (actual first exits and pre-exit B-region invariance)
For each source family:

1. the actual active branch agrees with the candidate orbit up to first exit;
2. every pre-exit actual current state is `B`-labeled;
3. the first exit to `H_{L1}` occurs at the universal family-dependent target
   `T_reg = (m-1,m-2,1)` or `T_exc = (m-2,m-1,1)`, with regular families
   exiting at `T_reg` by direction `2` and the exceptional family exiting at
   `T_exc` by direction `1`.

#### Proof
Fix a source family and let `N_f` be the candidate first-exit time from
Proposition 4.1. Prove by induction on `n <= N_f` that the actual state `x_n`
agrees with the candidate state `xhat_n` in the full current coordinates
`(q,w,u,Theta)`.

At `n = 0`, both states are the same entry state

`E = (m-1,1,u_source,2)`.

By Lemma 4.3, it is not patched, hence it is `B`-labeled.

Now assume `x_n = xhat_n` for some `n < N_f`. Lemma 4.3 says `xhat_n` is not
patched, so the actual state `x_n` is `B`-labeled. Therefore its witness update
is the unmodified mixed-witness update, which induces exactly the candidate step
on `(q,w,u,Theta)`: direction `1` changes only `q`, direction `4` changes only
`u`, direction `2` changes only `w`, and the other anchors leave `(q,w,u)`
fixed while increasing `Theta` by `1`. So `x_{n+1} = xhat_{n+1}` in full current
coordinates.

Thus the actual and candidate branches agree for all `n <= N_f`, and every
pre-exit actual state is `B`-labeled.

For `n < N_f`, Proposition 4.1 and Lemma 3.2 show that the candidate state does
not exit to `H_{L1}`; because the trigger test depends only on the current
coordinates `(q,w,u,Theta)`, the actual state does not exit either. At time
`N_f`, Proposition 4.1 gives an exit from the candidate orbit at the stated
universal target and direction, so the actual branch exits there as well.

## 5. Consequence for the package

### Corollary 5.1
The theorem-level content of `062` is now inlined: no separate `062` support
note is needed for the odd-`m` D5 package.

The old `033/062` block now survives inside the package only as the exact
trigger-family lemma isolated in Proposition 2.1 and the broader defect-template
provenance behind it.

## 6. Exact m=5 reference slice

### Proposition 6.1 (`m=5` specialization)
At `m=5`,

- `H_{L1} = {(4,4,u,2) : u != 2}`,
- `T_reg = (4,3,1)`,
- `T_exc = (3,4,1)`.

So the two possible first-exit states are exactly

- `A = (4,3,1)`,
- `B = (3,4,1)`.

The exceptional family is the source residue class `rho = 4`.

## 7. Bottom line

After `098`, the odd-`m` D5 package no longer needs `062` as a separate support
theorem. Together with `095`--`097`, this leaves the compact concrete bridge
package around `076` as the main remaining imported theorem layer.

What survives of the old `033/062` block inside the package is only the exact
trigger-family lemma now isolated in Proposition 2.1 and its broader
defect-template provenance. It is no longer a structural or dynamical
bottleneck for the globalization proof chain.
