# D5 Proof-Direction Compute Support 052

This note records what the compute branch now supports for the two proof
directions.

It does not change the theorem object.
The proof still stays on

`(B,tau,epsilon4)`.

## Positive route

The compute branch now supports two positive proof directions.

### 1. Theorem-side carrier coding

By `048`, `tau` already has exact internal countdown dynamics away from the
boundary.
By `050`, the boundary reset law remains exact through `m=19` on the same
small current quotients:

- `wrap -> 0`
- `carry_jump` on `(s,v,layer)`
- `other` on `(s,u,layer)`

So the positive theorem-side target is now very clean:
realize the countdown carrier, or just the reset law plus internal decrement.

### 2. Constructive `rho` route

By `049`, the stronger current-memory refinement persists through `m=19`:

- `tau` exact on `(s,u,v,layer,rho)`
- `next_tau` exact on `(s,u,layer,rho,epsilon4)`
- `c` exact on `(u,rho,epsilon4)`

So a constructive proof could still try to initialize and transport enough of
`rho`.

But this remains a refinement, not a theorem-object change.

## Negative route

The compute branch now supports a much sharper no-go direction.

By `052`, through `m=19`:

- the first exact tau truncation stays `m-3`
- the first exact transition-sheet horizons stay
  `m-4`, `m-3`, `m-1`
- the boundary is genuinely `3`-way for every tested `m>=7`

By `050`, the explicit witness family also persists through `m=19` with the
same `h < m-4` lower-bound shape.

So the right reduction-lemma target is now:

> show the intended local class factors through bounded grouped
> transition/reset data.

If that reduction is proved, the current witness family is already strong
enough to attack it.

## Practical conclusion

The compute branch has done the useful support work.

- positive route:
  boundary reset / countdown carrier is stable enough to target directly
- negative route:
  bounded-horizon and bounded-transition no-go now have stable larger-modulus
  evidence

So the next main effort should be proof packaging, not reopening broad search.

## Optional symbolic polish: 053

The optional reset-formula probe `053` adds one small useful fact without
changing the proof direction.

Through `m=19`, within the tested small-coefficient candidate family:

- no exact single affine law exists for either boundary reset map
- no exact two-stage piecewise law exists in the tested family
- but on `carry_jump`, the zero-reset fiber is exactly
  `s + v + layer ≡ 2 (mod m)`

So `053` is worth citing as symbolic support for the boundary-reset theorem
discussion, but it does not change the theorem object or the current frontier.
