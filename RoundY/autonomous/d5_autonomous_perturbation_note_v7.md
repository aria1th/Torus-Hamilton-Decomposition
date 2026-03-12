Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after the reduced target is known
and the first endpoint-oriented local realization families have failed.

Current target:
Decide whether the `030` endpoint seeds can be rescued by the smallest possible
Latin repair:

- one repair class,
- one extra bit,
- or another equally tiny local fix.

Known assumptions:
- `025` gives the reduced target:
  omit-base plus omitted-edge cocycle defect.
- `028` identifies endpoint orientation as the right missing local signature.
- `029` kills the smallest static two-layer endpoint-controller family.
- `030` finds short nonbaseline endpoint words at the path level.
- `031` kills their smallest static three-layer promotion.

Attempt A:
  Idea:
  Extract exact collision certificates for the `030` seed pairs and rank the
  seeds by how small and how separable the Latin obstruction is.
  What works:
  `032` does this exactly.
  It finds that only `11` seed pairs are distinct at both layer 2 and layer 3.
  The best-ranked seed is:
  - left `[2,2,1]`
  - right `[1,4,4]`
  and it has balanced collision support:
  - `m=5`: `250` overfull, `250` holes
  - `m=7`: `490` overfull, `490` holes
  - `m=9`: `810` overfull, `810` holes
  Where it fails:
  The collision data do not point to a single missing separator bit. The
  colliders are already separable by the obvious local contexts.

Attempt B:
  Idea:
  Search the smallest repair families around the best seeds:
  one repair class, one extra bit, and then one best-seed two-class static
  probe.
  What works:
  `032` searches all of these exactly on the pilot range.
  Where it fails:
  Everything is negative:
  - one-gate search on the top `3` seeds:
    `208` candidates, `0` Latin survivors
  - one-bit search on the top `3` seeds:
    `4160` candidates, `0` Latin survivors
  - best-seed two-class static probe:
    `384` candidates, `0` Latin survivors
  So one-class repair is not enough, one bit is not enough, and even the
  smallest two-class static repair is still dead.

Candidate lemmas:
- [C] `032` identifies the best-ranked endpoint seed and its exact balanced
  hole/collision profile.
- [C] For the best seeds, the colliding sources are already separated by:
  - label plus any tested bit,
  - predecessor/current label pair,
  - current/successor label pair.
- [C] One-gate repair fails.
- [C] One-bit repair fails.
- [C] The best-seed two-class static repair probe also fails.
- [H] The next live branch must be at least a genuine multi-class transducer or
  another coupled Latin-repair mechanism.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- Use the ranked best seed from `032` as the default seed.
- Search the smallest genuinely multi-class repair, not another one-bit family.
- Honest next candidates:
  - a two-state transducer with more than one repair class,
  - a coupled repair on neighboring off-edge states,
  - or a defect-splice mechanism larger than one local gate.
- Keep the `025` grouped-orbit signature as the acceptance target.

Next branching options:
1. Main branch:
   a genuine multi-class endpoint transducer on the best-ranked `032` seed.
2. Secondary branch:
   a coupled Latin-repair on the best seed that explicitly addresses the
   balanced hole/collision pattern.
3. Only then:
   widen to lower-ranked seeds or longer endpoint words.

Claim status labels:
  [P] `019`, `025`
  [C] `028`, `029`, `030`, `031`, `032`
  [H] one-bit repair is exhausted; the next live branch must be multi-class
  [O] full D5 decomposition
