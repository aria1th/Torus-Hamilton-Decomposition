# d=5 joined quotient: dynamic-collapse branch note

## Executive decision
The new joined quotient `Theta_AB` changes the diagnosis.

- `Theta_AB` is **Latin-feasible**: cyclic-equivariant Latin master fields exist on the joined quotient.
- The stable field found by the join search is still **dynamically degenerate**.
- Therefore the next obstruction to isolate is **not Latin infeasibility on the current quotient**.
- The next obstruction to isolate is a **dynamic collapse core**: why every feasible field we have seen on `Theta_AB` still yields trivial section return (`U_0 = id` on the base and monodromy `0`).

So the right next step is not “free anchor more”.
It is:

1. extract a minimal **dynamic-collapse motif** on the current quotient,
2. identify the exact missing information that separates the collapsed predecessor contexts,
3. add exactly one phase / flux bit encoding that information.

## Stable joined field: exact formula
For the stable field saved in `d5_join_quotient_001`, the local permutation palette collapses to a pure layer rule:

- layer `0`: `12340`, i.e. `c -> c+1`
- layer `1`: `34012`, i.e. `c -> c+3`
- layers `2,3,4+`: `01234`, i.e. identity

Hence for every color `c`, one full `m`-step return from `S=0` uses

- one step in direction `c+1`,
- one step in direction `c+3`,
- the remaining `m-2` steps in direction `c`.

So the total first-return displacement is

`Delta = e_{c+1} + e_{c+3} - 2 e_c`.

For color `0`, with relative coordinates

`(q,w,v,u) = (x_1,x_2,x_3,x_4)`,

this gives the exact first-return formula

`R_0(q,w,v,u) = (q+1, w, v+1, u)`.

Consequences:

- clean `v`-fiber: yes,
- strict `q`-clock: yes,
- section return `U_0` on `(w,u)`: identity,
- orbitwise monodromy: `0` on every orbit,
- full color maps: `m^3` cycles of length `m^2`.

So the joined quotient succeeds at Latin coupling but collapses dynamically to a translational skew product with trivial base and trivial monodromy.

## Why the previous “minimal Latin conflict” plan must be updated
That plan was correct for the earlier anchored / non-Latin quotients.
It is no longer the primary bottleneck for `Theta_AB`, because `Theta_AB` already admits Latin fields.

The main question has shifted to:

> Which predecessor / phase contexts are still merged by `Theta_AB` and thereby force the representative-color return to collapse to `(q+1,w,v+1,u)`?

So the next “minimal forbidden motif” should be a **minimal dynamic-collapse core**, not merely a minimal Latin conflict.

## What the missing bit should explain
A useful extra bit must distinguish quotient states that are currently identical in `Theta_AB` but ought to produce different return contributions for the representative color.

The bit should be chosen only after identifying one of the following on the current quotient:

- a minimal predecessor pattern whose two realizations force different admissible return increments,
- a minimal orbit motif where outgoing/incoming Latin is compatible but the induced return contribution must split,
- a minimal local flux class that predicts whether the layer-1 / layer-2 carry should contribute to base motion or to fiber monodromy.

So the extra bit is not “one more atom” in the abstract.
It should encode the **cause** of the collapse.

## Recommended next computations
1. Build a **compatibility hypergraph** on `Theta_AB` whose local labels encode simultaneously:
   - outgoing Latin,
   - incoming Latin,
   - representative-color one-step return contribution.
2. Enumerate the quotient states / predecessor motifs on which all saved feasible fields agree.
3. Extract a minimal set of motifs forcing the stable field’s return law `(q+1,w,v+1,u)`.
4. From that core, propose one explicit refinement bit, ideally one of:
   - predecessor-side orientation,
   - carry / no-carry status,
   - local flux parity,
   - defect-side orientation.
5. Re-run the master-field search on the one-bit refined quotient, with the same Latin constraints and with representative-color return diagnostics attached.

## Branch status
- `[P]` Joined quotient `Theta_AB` is Latin-feasible.
- `[P]` The stable joined field has exact return law `R_0(q,w,v,u) = (q+1,w,v+1,u)`.
- `[P]` Therefore `U_0 = id` and every monodromy is `0`.
- `[H]` The next useful refinement is a one-bit **dynamic** refinement, not further anchor relaxation.
- `[O]` The precise minimal dynamic-collapse core on `Theta_AB` remains to be extracted.
