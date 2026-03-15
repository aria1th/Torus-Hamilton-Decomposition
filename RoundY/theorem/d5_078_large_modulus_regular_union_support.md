# D5 078 Large-Modulus Regular-Union Support

This note promotes the stable larger-modulus regular-union compute support from
the `078` C-track material in `tmp/`.

It records what was already known on the regenerated regular unions for
`m = 13,15,17,19,21` before the later `079–083` closure.

## 1. Full regular boundary coverage

On the reconstructed actual regular-source unions through `m = 21`:

- every boundary label in `Z/m^2 Z` is realized;
- each regular source contributes a `delta`-interval of length `m(m-3)`;
- the union of those regular intervals covers the full `m^2` boundary grid.

So there is no regular-source coverage gap at the boundary level on those
moduli.

## 2. Heavy repeated-`delta` overlap

Repeated realized `delta` values are ubiquitous on the reconstructed regular
union.

In fact, every realized `delta` occurs with multiplicity either `m-5` or
`m-4`, and every pair of regular source charts overlaps.

So the overlap graph is not merely connected; it is already complete on the
regular chart model.

## 3. No regular chart-level dead-end witness

For every regular chart endpoint `delta_end` on the checked range:

- the chart itself provides the unique terminal occurrence at that endpoint;
- the same endpoint also appears in many continuing regular charts.

So the larger-modulus regular chart model shows no chart-level fixed-`delta`
obstruction.

This is the larger analogue of the smaller frozen-range actual-union picture.

## 4. The only unresolved regular-start edge

The compressed regular carry-jump chain graph has the expected internal law:

`(u,w) -> (u,w+1)`

inside a source, and the final-chain edge:

`u -> u-3 mod m`

between source starts.

The unique unresolved regular-start edge is the expected exceptional one:

`6 -> 3`.

So the larger regular support isolates the same patched splice as the only
missing structural edge.

## 5. Interpretation

The `078` larger-modulus compute signal was already strongly pro-globalization:

- repeated realized `delta` values were everywhere;
- the regular charts all followed the same `delta -> delta+1` odometer law;
- every apparent regular endpoint already had continuing same-`delta`
  witnesses;
- the only unresolved structural place was the exceptional splice.

## 6. Later status

This note is now historical support for:

- `theorem/d5_079_exceptional_interface_support.md`
- `theorem/d5_081_regular_union_and_gluing_support.md`

## 7. Promoted references

This note promotes the substance of:

- `tmp/d5_078_rC.md`
