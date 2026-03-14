# D5 positive route: beta-controller sharpening

This note records one further sharpening of the positive route after the `064`
unified handoff.

## 1. Starting point from `064`

The unified handoff already proposes the constructive coordinates

- `rho = u_source + 1`,
- `alpha = rho - u`,
- `delta = alpha - (s+v+layer)`,
- `J = 1_{epsilon4 = carry_jump}`,
- `beta = alpha - (s+v+layer) - J`.

It also records the checked formulas

- `q ≡ -alpha + J (mod m)`,
- `c = 1_{alpha = 1 + J}`,
- `tau = 0` on nonflat states,
- on flat states, `tau = 1` at `(s,delta)=(2,m-2)` and `tau = delta` otherwise,
- and the branchwise `next_tau` formulas.

## 2. Stronger positive target: beta-controller theorem

The positive route can be sharpened from an `alpha`-transport theorem to a
`beta`-controller theorem.

### Proposed theorem

There exists a local/admissible carrier `beta in Z/mZ` on the active branch such that:

1. `beta` is born at a universal post-entry value (checked data suggest `beta_0 = m-2`);
2. `beta' = beta - 1 (mod m)` at every active step;
3. the current readouts are exact on `(B,beta)`:
   - `q ≡ -beta - s - v - layer (mod m)`;
   - `c = 1_{beta + s + v + layer = 1}`;
   - `epsilon4`, `tau`, and `next_tau` are exact current functions of `(B,beta)`.

If proved, this would close the constructive branch more cleanly than the raw
source-residue wording.

## 3. Why the beta-controller theorem follows formally from the `064` formulas

From

- `q ≡ -alpha + J`,
- `beta = alpha - (s+v+layer) - J`,

one gets immediately

- `q ≡ -beta - s - v - layer (mod m)`.

Hence

- `c = 1_{q = m-1} = 1_{beta + s + v + layer = 1}`.

So once `beta` is present, `q` and `c` no longer need `epsilon4`.

Also

- `beta = delta - J`.

Therefore, on flat states (where `J=0`), one has `beta = delta`, and the
countdown formula becomes a direct `(B,beta)` formula.

The theorem-side phase coordinate is `kappa = q+s+v+layer`, so algebraically

- `beta ≡ -kappa (mod m)`.

Thus the phase-corner theorem and the beta-controller theorem are the same clock
in opposite gauges.

## 4. Exact `(B,beta)` readouts implied by the phase-corner theorem

Using `beta ≡ -kappa`, the phase-corner scheduler translates to:

- `beta = 0  -> wrap`,
- `beta = m-1 -> carry_jump`,
- `beta = m-2 -> other_1000` iff `c=1`, else flat,
- `beta = m-3 -> other_0010` iff `(c=0 and s=2) or (c=1 and s!=2)`, else flat,
- all other `beta` values -> flat.

Then `tau` becomes an exact current-state function of `(B,beta)`:

- `tau = 0` on the nonflat `beta` fibers above;
- `tau = 1` at `(beta,s,c)=(m-2,2,0)`;
- `tau = beta` on every other flat state.

So the whole controller collapses from `(B,alpha,epsilon4)` to `(B,beta)`.

## 5. Direct checked support from the frozen `047` data

I directly checked the frozen `047` one-step transitions for `m=5,7,9,11`
(total checked transitions with recorded successors: `15160`). On that scope:

- `alpha' = alpha - 1_{epsilon4 = carry_jump}` held with zero exceptions;
- equivalently, `u' - u = 1_{epsilon4 = carry_jump}` held with zero exceptions;
- `beta' = beta - 1 (mod m)` held with zero exceptions.

By contrast, the uncorrected variable

- `beta0 = alpha - (s+v+layer)`

fails to have unit drift on the same checked scope, so the `-J` correction is
not cosmetic; it is essential.

## 6. Best constructive proof spine now

A clean positive route would be:

1. prove universal birth `alpha=1` (equivalently checked `beta_0=m-2`);
2. prove the event-transport identity `u'-u = 1_{epsilon4=carry_jump}`;
3. deduce `alpha' = alpha - 1_{epsilon4=carry_jump}`;
4. define `beta = alpha-(s+v+layer)-J` and prove `beta' = beta-1`;
5. recover `q,c,epsilon4,tau,next_tau` as exact current functions of `(B,beta)`.

At that point the positive route is no longer “transport source residue” but:

> realize a universal cyclic clock with unit drift, then read out the entire
> controller from `(B,beta)`.

## 7. Honest status

This does not prove local realizability.

What it does prove is that the positive route can be compressed one step
further:

- from `rho` to `alpha`,
- and then from `alpha` to a straightened `beta` clock whose drift is exactly
  `-1` on every checked transition.
