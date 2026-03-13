# D5 Unified Handoff 064

This note merges the `064` cluster into one handoff document for researchers
joining the current D5 frontier.

Source notes:

- [d5_theorem_part_after_063_support_064.md](./d5_theorem_part_after_063_support_064.md)
- [d5_constructive_route_064.md](./d5_constructive_route_064.md)
- [d5_positive_route_alpha_sharpening_20260313_064.md](./d5_positive_route_alpha_sharpening_20260313_064.md)
- [d5_negative_route_064.md](./d5_negative_route_064.md)

It is meant to answer:

1. what the current theorem target is,
2. what the positive constructive target is,
3. what the negative theorem target is,
4. what different researchers should aim at next.

## 1. Global picture

After `062`, the structural branch is close to closed.

After `063A`, the stronger constructive formulas are explicitly exact through
`m=19`.

So the D5 frontier is now best split into three branches:

- **theorem branch:** prove the phase-corner machine cleanly;
- **positive constructive branch:** realize a transported cyclic carrier,
  preferably in the `alpha` gauge;
- **negative branch:** prove the intended local class collapses to a bounded
  quotient, then rule it out by a cyclic-section lower bound.

## 2. The theorem-side object stays minimal

The main theorem object remains

- `B = (s,u,v,layer,family)`
- `tau`
- `epsilon4`

The auxiliary coordinates

- `rho = u_source + 1`
- `alpha = rho - u`
- `delta = rho - (s+u+v+layer)`
- `kappa = q+s+v+layer`

are proof or constructive coordinates only.

They should not replace `(B,tau,epsilon4)` in the main theorem statement.

## 3. The main theorem target

The clean theorem slogan is:

> **On the active best-seed branch, D5 is an odometer with one corner.**

### Theorem A (phase-corner theorem; manuscript target)

Fix odd `m >= 5` and the best seed. On the active nonterminal best-seed branch,
define

- `kappa = q+s+v+layer mod m`.

Then:

1. `kappa' = kappa + 1 mod m`;
2. the current event `epsilon4` is determined by:
   - `kappa = 0 -> wrap`
   - `kappa = 1 -> carry_jump`
   - `kappa = 2 -> other_1000` iff `c=1`, else `flat`
   - `kappa = 3 -> other_0010` iff `(c=0 and s=2) or (c=1 and s!=2)`, else `flat`
   - `kappa = 4,...,m-1 -> flat`
3. among flat states, the only short reset occurs at the corner `(kappa,s)=(2,2)`.

So the active branch is an odometer with one corner.

### Immediate corollaries

From Theorem A one should derive:

- **countdown law**
  - `tau = 0` on nonflat states
  - on flat states:
    - `tau = 1` at `(kappa,s)=(2,2)`
    - `tau = m-kappa` otherwise
  - hence `tau' = tau-1` whenever `tau>0`
- **CJ reset**
  - `0` on the zero-reset fiber
  - `1` in the short case
  - `m-2` otherwise
- **OTH resets**
  - `other_1000 -> m-3` if `s=1`, else `0`
  - `other_0010 -> m-4`
- **finite-cover compatibility**
  - the phase machine is compatible with
    `B <- B+c <- B+c+d`

## 4. Best theorem-side proof spine

Conditional on the explicit `033` trigger family theorem, the clean proof spine
is still:

- `033 -> 062 -> 059`

with `061` useful as a check and auxiliary bootstrap picture.

Concretely:

1. import the exact `H_{L1}` trigger family from `033`;
2. use the phase-1 source-residue invariant to derive the universal first-exit
   targets (`062`);
3. show the candidate orbit agrees with the actual active branch up to first
   exit;
4. conclude every pre-exit active current state is `B`-labelled;
5. on `B`, the mixed witness rule yields the current-state scheduler in
   `kappa`;
6. promote that scheduler to Theorem A.

This is cleaner than proving `CJ` and `OTH` separately and interpreting them
later.

## 5. Positive constructive route

The positive route should now be stated much more aggressively than “transport
source residue somehow.”

### 5.1 First sharpening: use `alpha = rho-u`

Define

- `rho = u_source + 1`
- `alpha = rho - u`
- `delta = alpha - (s+v+layer)`
- `J = 1_{epsilon4 = carry_jump}`

Then the checked current-state formulas simplify to:

- `q ≡ -alpha + J mod m`
- `c = 1_{alpha = 1 + J}`

So `q` and `c` are exact from `(alpha,epsilon4)` alone.

The exact countdown formulas become:

- `tau = 0` on nonflat states
- on flat states:
  - `tau = 1` if `(s,delta)=(2,m-2)`
  - `tau = delta` otherwise

The exact update formulas become:

- `tau' = tau-1` on flat states
- `tau' = 0` on wrap
- on carry_jump:
  - `0` if `alpha=2`
  - `1` if `alpha!=2` and `s=1`
  - `m-2` otherwise
- on other:
  - `m-3` if `delta=m-2` and `s=1`
  - `0` if `delta=m-2` and `s!=1`
  - `m-4` if `delta=m-3`

The important gain is:

> `u` disappears from the readout formulas once one passes to `alpha`.

### 5.2 Universal birth

At the post-entry active state:

- `u = u_source`
- `rho = u_source + 1`

so

- `alpha = 1`.

That means the carrier birth is universal in the `alpha` gauge.

This is much better than the raw `rho` wording, where birth looked
source-dependent.

### 5.3 Best constructive theorem target

The best positive theorem target is now:

> **Alpha-transport theorem.**
> There exists a local/admissible carrier `alpha` on the active branch such
> that:
> - at entry, `alpha=1`;
> - `alpha+u` is invariant mod `m`;
> - equivalently, `alpha' = alpha - (u'-u)`;
> - `q`, `c`, `tau`, and `next_tau` are given by the alpha-gauge formulas.

This is a smaller target than “transport arbitrary source residue.”

### 5.4 Straightened phase carrier

The alpha-sharpening note suggests the even straighter carrier

- `beta = alpha - (s+v+layer) - J`

with `J = 1_{epsilon4 = carry_jump}`.

Then

- `beta ≡ -kappa mod m`.

So if the phase-corner theorem is right and `kappa' = kappa+1`, then

- `beta' = beta - 1`.

This is the clean constructive reformulation:

> the carrier can be viewed as a plain cyclic clock with unit drift.

That is probably the best positive-route slogan after `064`.

## 6. Negative route

The negative route should now be phrased as one clean theorem, not as a vague
“bounded horizon fails” statement.

### Proposition B (cyclic section lower bound)

Suppose on the active branch there is a cyclic return section

- `Sigma_m = {x_0,...,x_{m-1}}`

with first-return map

- `R_m(x_q) = x_{q+1} mod m`

and carry label

- `c_m(x_q) = 1_{q=m-1}`.

Suppose a candidate local/admissible mechanism induces a quotient

- `pi_m : Sigma_m -> Q`

with induced return map `Rhat_m` and readout `chi` such that

- `pi_m o R_m = Rhat_m o pi_m`
- `c_m = chi o pi_m`.

Then necessarily:

- `|Q| >= m`.

So any bounded quotient independent of `m` is impossible.

### Negative-route consequence

If the intended local class can be shown to factor through a bounded quotient of
the active section dynamics, then it cannot recover carry uniformly in odd `m`.

This is stronger than the old bounded-horizon witness argument:

- the witness pair kills bounded lookahead;
- the cyclic-section proposition kills any bounded quotient at all.

## 7. Best division of labor for different researchers

### Researcher A: theorem / manuscript proof

Aim:

- prove the phase-corner theorem cleanly from the `033 -> 062 -> 059` spine;
- package countdown and reset formulas as corollaries;
- keep `(B,tau,epsilon4)` as the theorem object.

Best files:

- [d5_first_exit_target_proof_062.md](./d5_first_exit_target_proof_062.md)
- [d5_phase_machine_summary_058.md](./d5_phase_machine_summary_058.md)
- [d5_theorem_part_after_063_support_064.md](./d5_theorem_part_after_063_support_064.md)

### Researcher B: positive constructive route

Aim:

- prove or realize an `alpha` carrier with universal birth `alpha=1`;
- or equivalently realize the straightened `beta` phase clock.

Best files:

- [d5_constructive_route_064.md](./d5_constructive_route_064.md)
- [d5_positive_route_alpha_sharpening_20260313_064.md](./d5_positive_route_alpha_sharpening_20260313_064.md)
- [artifacts/d5_constructive_source_residue_support_063a/README.md](../../artifacts/d5_constructive_source_residue_support_063a/README.md)

### Researcher C: negative / impossibility route

Aim:

- define the intended admissible/local class precisely;
- prove it factors through a bounded quotient of the active cyclic section;
- then apply Proposition B.

Best files:

- [d5_negative_route_064.md](./d5_negative_route_064.md)
- [d5_063_route_organization.md](./d5_063_route_organization.md)
- [d5_boundary_reset_and_tau_proof_052.md](./d5_boundary_reset_and_tau_proof_052.md)

### Researcher D: compute / stress-test support only

Aim:

- do not reopen broad search;
- only stress-test whichever of the three branches becomes proof-critical.

Good support jobs:

- larger-modulus branch-local checks of explicit identities,
- validating `alpha` / `beta` transport identities if needed,
- section-extraction support for the negative route.

## 8. Honest open point

The `064` cluster does not solve D5.

What it does is replace one vague frontier with three very explicit ones:

- prove the phase-corner theorem,
- realize the `alpha`/`beta` carrier,
- or prove bounded-quotient impossibility.

That is the clean handoff state.
