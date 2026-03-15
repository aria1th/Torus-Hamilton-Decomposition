# Exact verifiable sample solution for `d=5`, odd `m`

## Global odd-`m` theorem-level solution

The exact verifiable theorem now supported by the accepted D5 chain is:

> On the true accessible boundary union for odd `m`, raw global `(beta,delta)` is exact.

Equivalent form:

> every actual lift of the exceptional cutoff row `delta = 3m-3` continues through
> `3m-2 -> 3m-1`
> and lies in the regular continuing endpoint class there.

Equivalent consequences:

- `rho = rho(delta)` globally;
- fixed realized `delta` determines endpoint class / future word;
- there is no hidden second endpoint sheet over `delta = 3m-1`.

Concrete bridge coordinates:

- `sigma = w + u - q - 1 mod m`
- `delta = q + m sigma`
- componentwise splice law: `delta' = delta + 1 mod m^2`

Minimal proof chain used for that theorem:

1. `033` explicit trigger family
2. `062` universal first-exit targets
3. `076` componentwise concrete bridge
4. `077` tail-length reduction
5. `079` exceptional interface
6. `081` regular continuation
7. `082` exceptional-row reduction
8. `083` final theorem proof

## Concrete finite sample at `m=5`

The bundled file `RoundY/d5_m5_kempe_witness_26.json` gives an explicit finite witness with:

- `sequence_length = 26`
- `cycle_counts_m5 = [1, 1, 1, 1, 1]`

So the recorded `m=5` instance closes with one cycle in each of the five color classes.

The same JSON also records that the identical 26-move sequence does **not** extend uniformly to `m=7`:

- `same_sequence_m7.cycle_counts = [5, 433, 1, 1, 3]`

So this is an exact finite sample witness for `m=5`, not a uniform odd-`m` family by itself.
