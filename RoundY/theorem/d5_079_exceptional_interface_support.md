# D5 079 Exceptional Interface Support

This note promotes the stable `079` exceptional-continuation support from
`tmp/`.

Its purpose is to freeze what is already known about the patched exceptional
continuation before the later `080–082` reductions.

## 1. Larger-range chart / chain-label conclusion

### Theorem 1.1

On the larger actual regular-source unions for `m = 13,15,17,19,21`, the
exceptional continuation is forced in chart / odometer coordinates to pass
through

`3m-2 -> 3m-1`.

These two labels have the distinguished regular interpretations:

- `3m-2` is the unique terminal regular source-`4` occurrence;
- `3m-1` is the unique regular source-`1` start.

So the checked exceptional continuation is:

`3 -> (terminal chain of 4) -> 1`.

## 2. Larger regular quotient already closes

At chart / chain-label level on `m = 13,15,17,19,21`:

- every `delta in Z/m^2 Z` is realized;
- every regular `delta` has continuing chart realizations;
- the grouped chart quotient already closes to the full odometer step
  `delta -> delta+1`.

This means the exceptional landing location is no longer vague. The only
remaining question is whether the exceptional realization at that interface
belongs to the same endpoint / future-word class as the regular one.

## 3. Safe theorem interpretation

The strongest safe statement after `079` is:

- chart-level exceptional landing is settled;
- global endpoint compatibility is not yet settled.

So `079` removes the landing-location problem but does not yet prove the final
raw-state globalization theorem.

## 4. Promoted references

This note promotes the substance of:

- `tmp/d5_078_079_rA_exceptional_addendum.md`
- `tmp/d5_079_rC_followup.md`
- `tmp/d5_079_B_review.md`
- `tmp/d5_079_D_review.md`
