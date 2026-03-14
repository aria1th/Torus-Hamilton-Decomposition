# Torus Lean Formalization

This directory is a standalone Lean 4 + mathlib project for the formal side of
the low-dimensional torus program.

## Current verified status

- `TorusD4/`: complete `d=4` Hamilton decomposition formalization.
- `TorusD3Even/`: complete even-`d=3` Route E package.
- `TorusD3Odometer/`: active `d=3` odometer rewrite. The current completed
  files are `Color2Full.lean`, `Color1FullCaseI.lean`,
  `Color1FullCaseII.lean`, and `Color0FullCaseI.lean`. The live frontier is
  `Color0FullCaseII.lean`.
- `TorusD5/`: extracted-model support only. This is not the main D5 proof
  frontier; see `README-D5.md` and `D5_LEAN_PROGRESS.md`.

## What to read

- `README-D5.md` for the current D5 theorem/support split and the recommended
  Lean role.
- `D5_LEAN_PROGRESS.md` for the exact current `TorusD5/` implementation state.
- `../RoundY/README.md` for the live research frontier.

## CLI workflow

Build everything:

```bash
cd formal
source "$HOME/.elan/env"
lake build
```

Build focused targets:

```bash
cd formal
source "$HOME/.elan/env"
lake build TorusD3Odometer
lake build TorusD5
```

Check active files directly:

```bash
cd formal
source "$HOME/.elan/env"
lake env lean TorusD3Odometer/Color0FullCaseII.lean
lake env lean TorusD5/GroupedReturn.lean
```

## Directory layout

- `TorusD3Even/`
  even-`d=3` Route E formalization
- `TorusD3Odd/`
  odd-`d=3` return-map and cycle library
- `TorusD3Odometer/`
  full-map odometer rewrite for `d=3`
- `TorusD4/`
  complete `d=4` return-map / second-return / lift formalization
- `TorusD5/`
  extracted-model and specification scaffold for D5

Top-level umbrella imports:

- `TorusD3Even.lean`
- `TorusD3Odd.lean`
- `TorusD3Odometer.lean`
- `TorusD4.lean`
- `TorusD5.lean`
