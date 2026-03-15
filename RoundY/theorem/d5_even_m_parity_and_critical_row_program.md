# D5 Even-`m` Parity Barrier And Critical-Row Program

This note records the current theorem-shaped even-`m` D5 picture.

For a separate condition check on what is necessary or sufficient for the
finite-splice proof route, see:

- `theorem/d5_even_m_finite_splice_conditions.md`

It separates three layers:

1. what already looks rigorous now;
2. what follows formally from the odd-`m` boundary theorem once an even
   upstream package is supplied;
3. what still looks like the right new theorem target for the even case.

The point is not that even `m` is nearly solved. The point is that the even
branch is now shaped well enough that broad witness search should no longer be
the default.

## 1. Status split

The safest current reading is:

- **already rigorous in shape:** a Kempe parity barrier for even `m`;
- **already rigorous as a conditional theorem:** the odd final gluing proof is
  parity-blind once the same upstream boundary package is rebuilt;
- **current programmatic target:** a finite-splice "critical-row" theorem on
  regular source windows.

So the new work is upstream. It is not a fresh globalization theorem.

## 2. Parity barrier for Kempe-from-canonical

The `d=3` even case already showed that parity can kill the naive
Kempe-from-canonical route before the real proof starts.

The same sign-product argument extends to `D_5(m)`:

- the product of permutation signs over all colors is invariant under Kempe
  swaps;
- when `m` is even, the canonical coloring has total sign product `+1`;
- a decomposition into five Hamilton cycles would have total sign product `-1`.

Therefore:

> For even `m`, no Kempe-from-canonical route can produce a Hamilton
> decomposition of `D_5(m)`.

This does not say that the even case is false. It says the direct odd-style
Kempe continuation is blocked at the starting point.

## 3. Formal extension theorem

The final odd-`m` D5 gluing proof uses only the following ingredients on the
true accessible boundary union:

1. the same first-exit theorem with universal targets;
2. the same componentwise concrete bridge
   `delta = q + m sigma` with splice law `delta' = delta + 1 (mod m^2)`;
3. the same tail-length reduction at fixed realized `delta`;
4. regular continuation for every realized regular label;
5. the same exceptional chart/interface landing
   `3m-3 -> 3m-2 -> 3m-1`.

No odd-parity-specific calculation occurs in the final gluing step itself.

So the correct conditional theorem is:

> If an even-`m` D5 package supplies the same upstream boundary data, then the
> current odd-`m` final globalization proof carries over unchanged.

This is the formal reason the even case should be treated as an upstream repair
problem rather than as a new boundary-globalization problem.

## 4. Critical-row program

The current bundled interval summaries suggest that the regular source windows
obey a rigid arithmetic pattern. Treated as a theorem target, that pattern is:

- regular source window start:
  `s_u = m(u+2)-1 (mod m^2)`
- regular source window endpoint:
  `e_u = m(u-1)-2 (mod m^2)`
- generic splice:
  `e_u + 1 = s_{u-3}`

So the generic window-to-window successor is the cyclic source shift

`u -> u-3 (mod m)`.

On the checked odd range, the unique non-generic source is `u = 3`, whose
endpoint is the exceptional cutoff `3m-3`, and the distinguished regular
interface is

`3m-2 -> 3m-1`.

This suggests the right D5 analogue of `d=3` even Route E:

> Preserve the bulk odometer law `delta -> delta + 1`, prove the regular
> source-window splice `u -> u-3`, and isolate source `3` as the unique finite
> splice defect.

That is the row-level version of the old critical-lane picture.

## 5. Critical-row reduction principle

The right theorem target is not "find an even witness". It is closer to the
following reduction principle:

Assume that on the true accessible boundary union:

1. the regular sector splits into source windows `I_u`;
2. inside each `I_u`, the successor law is the generic odometer step
   `delta -> delta + 1`;
3. each regular window starts at `s_u` and ends at `e_u`, with
   `e_u + 1 = s_{u-3}`;
4. the unique missing source is `u = 3`;
5. the exceptional window ends at `3m-3` and continues through
   `3m-2 -> 3m-1`.

Then the hypotheses of the formal extension theorem are satisfied, and the
odd-`m` final gluing proof applies.

So the even case should be attacked by proving a finite-splice theorem for the
source windows, not by reopening the final bridge.

## 6. What this changes operationally

Bad first question:

> Which new even witness works?

Better first question:

> What is the even-`m` return object whose bulk is still an odometer and whose
> only non-generic behavior is a finite source-window splice defect?

That leads to the right concrete tasks:

1. sharpen the parity / invariant obstruction for naive direct routes;
2. identify the reduced even return object;
3. extract the bulk clock and splice defects on small even moduli
   `m = 6, 8, 10, 12`;
4. formulate the smallest critical-row repair theorem;
5. only then search for implementations.

## 7. What is proved vs. what is still a target

Safe to treat as theorem-level guidance now:

- the parity barrier against Kempe-from-canonical;
- the formal extension theorem saying the odd final proof is parity-blind once
  the same upstream boundary package exists.

Still only a programmatic target:

- the critical-row reduction itself as a proved even theorem;
- the claim that the even return object really has exactly one finite splice
  defect;
- the existence of the repaired even upstream corridor.

So the even branch remains open, but the theorem target is now much smaller and
better shaped.

## 8. Bottom line

The safest current even-`m` D5 summary is:

1. the naive Kempe continuation is blocked by parity;
2. the odd final boundary theorem already has the right formal shape for all
   moduli;
3. the real new work is a Route-E-style critical-row repair theorem upstream.

In short:

> The even case should be treated as a finite-splice repair problem whose bulk
> is still an odometer, not as a fresh witness-search problem.
