Task ID:
D5-CARRY-SWAP-U-CARRY-020

Question:
Can the explicit mixed-witness return model be perturbed by a
state-dependent carry-slice `2↔4` swap that introduces grouped `u`-carry
while preserving the already-correct reduced dynamics on `(q,s,v)`?

Purpose:
The current obstruction is explicit: grouped return is already correct on
`(s,v)` and leaves `u` passive. The smallest perturbation that can change `u`
without changing the `s` carry law is a carry-slice `2↔4` substitution. The
next job is to study that reduced family directly before any broader search.

Inputs / Search space:
- canonical mixed witness `mixed_008`
- reduced first-return model from `019`
- candidate carry-swap selectors on the `q = m-2` carry slice
- Stage 1 requirement:
  - keep `dv(q,s)` and grouped `phi(s)` fixed
- existing one-bit layer-2 atoms:
  - `q=-1`
  - `q+u=1`
  - `w+u=2`
  - `q+u=-1`
  - `u=-1`
- checked odd moduli:
  - `m in {5,7,9,11,13,15,17,19}`

Allowed methods:
- symbolic reduced-model derivation
- grouped-base map analysis on `(s,u)` and `(s,d)` with `d = u-w = 2u-s`
- exact finite verification of permutation constraints
- control / candidate classification in reduced coordinates
- no broad torus search

Success criteria:
1. Derive the grouped base map induced by a single binary carry-slice swap.
2. Verify the exact constraint for maps of the form `u -> u + beta_s(u)` with
   `beta_s(u) in {0,1}`.
3. Classify the obvious one-bit selector candidates as:
   - still one-dimensional over `s`,
   - invalid because they break bijectivity,
   - or genuinely promising.
4. Identify the first plausible extra base coordinate candidate.
5. State the smallest viable next family if single-swap selectors are too weak.

Failure criteria:
- the binary-permutation obstruction fails,
- or a simple one-bit selector already gives a genuine new valid second base
  coordinate, contradicting the current structural reading.

Artifacts to save:
- code
- raw logs
- summary report
- symbolic grouped-base derivation
- permutation diagnostics
- candidate-selector classification

Return format:
- exact grouped base map for carry-swap perturbations
- exact binary-permutation obstruction
- classification of one-bit selector candidates
- recommended next family

Reproducibility requirements:
- fixed moduli `5,7,9,11,13,15,17,19`
- deterministic symbolic derivation
- saved JSON for permutation counts and candidate classifications
