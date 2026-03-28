# D5 298 Resonant Late Mod-30 Routing Note

This note promotes the `2026-03-26` late-atlas integration memo into the
stable RoundY layer.

It is still a **research-routing note**, not a theorem claim.
Its purpose is to combine:

1. the earlier exact late `B_m/H_m` winner notes at
   `123,129,141,147,153,159,171,177`; and
2. the corrected exact zero-state atlas now saved in
   [d5_297_resonant_late_zero_return_atlas.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_297_resonant_late_zero_return_atlas.md).

The new conclusion is not a new global law.
It is a sharper **promotion order** and a cleaner campaign map for the late
resonant pure color-`1` branch.

## 1. The late branch is now best read as a two-family atlas

Keep the same late families
\[
\mathcal C_m = \{A_{r-2,3},A_{r,3}\},
\qquad
\mathcal F_m = \{A_{r-1,3},A_{r,3}\},
\qquad r=(m-1)/2,
\]
but read them with the corrected toggle semantics recorded in
[d5_297_resonant_late_zero_return_atlas.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_297_resonant_late_zero_return_atlas.md).

With that correction in place, the late branch is no longer well described as
“find the one universal late 2-line family”.
The checked data now support a **two-family atlas**:

- central wins on some moduli;
- flank wins or repairs on others;
- some moduli show coexistence;
- and some moduli are shared defects.

## 2. Exact late ledger before the new atlas

The already checked exact late notes give:

| modulus | `m mod 30` | central | flank | status |
|---:|---:|---|---|---|
| `123` | `3` | exact win | not promoted there | central lane starts |
| `129` | `9` | exact win | not promoted there | central still wins |
| `141` | `21` | exact win | not promoted there | central still wins |
| `147` | `27` | exact fail | exact win | flank repairs first puncture |
| `153` | `3` | exact win | not promoted there | central reappears |
| `159` | `9` | exact win | not promoted there | central reappears |
| `171` | `21` | exact win | exact win | coexistence modulus |
| `177` | `27` | exact fail | exact fail | shared defect modulus |

So even before the atlas extension, the late branch was already more structured
than a single punctured family law.

## 3. What the corrected zero-state atlas adds

The saved atlas in
[zero_calibration.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_297_resonant_late_campaign/zero_calibration.json)
extends exact zero-state first-return data to
\[
171,177,183,189,201,207,213.
\]

The `B_m` routing table is:

| modulus | `m mod 30` | promoted `+` | central | flank | cheapest |
|---:|---:|---:|---:|---:|---|
| `171` | `21` | `6,023,526` | `4,006,094` | `2,017,475` | flank |
| `177` | `27` | `14,473,936` | `2,224,421` | `1,127,720` | flank |
| `183` | `3` | `4,922,782` | `3,683,909` | `4,922,828` | central |
| `189` | `9` | `4,072,222` | `4,072,222` | `4,072,175` | near tie |
| `201` | `21` | `9,776,901` | `6,504,752` | `3,272,300` | flank |
| `207` | `27` | `23,138,491` | `3,556,643` | `1,799,513` | flank |
| `213` | `3` | `7,758,088` | `5,807,264` | `7,758,035` | central |

The same atlas also shows that `H_m` is not the discriminating object:

- central has the same zero-state `H_m` image as promoted `+`;
- flank lands at `a = 1` on the first `H_m` return throughout the checked late
  range.

So the operational late discrimination really lives on `B_m`.

## 4. Tentative mod-30 routing picture

This is still a **heuristic routing law**, not a theorem.
But it is currently the cleanest organization of the exact late data.

### `m ≡ 3 (mod 30)`

Observed data:

- `123`: central exact win;
- `153`: central exact win;
- `183`: central-favored in the atlas;
- `213`: central-favored in the atlas.

Current read:

> `3 mod 30` is the cleanest current **central-first lane**.

### `m ≡ 9 (mod 30)`

Observed data:

- `129`: central exact win;
- `159`: central exact win;
- `189`: near tie in the atlas.

Current read:

> `9 mod 30` is the current **crossover lane**.

### `m ≡ 21 (mod 30)`

Observed data:

- `141`: central exact win;
- `171`: coexistence;
- `201`: flank-favored in the atlas.

Current read:

> `21 mod 30` looks like a **drift lane**:
> central -> coexistence -> flank-favored.

### `m ≡ 27 (mod 30)`

Observed data:

- `147`: central fails, flank repairs;
- `177`: both fail, but flank is cheaper in the atlas;
- `207`: flank-favored in the atlas.

Current read:

> `27 mod 30` is the clearest current **flank-first but fragile lane**.

## 5. Promotion order implied by the integrated atlas

This note does not claim new exact winners.
It does claim a sharper order for the next full exact `B_m` promotions.

### Tier A: branch-defining promotions

1. `183`, central
2. `201`, flank
3. `207`, flank
4. `213`, central

### Tier B: crossover anchor

5. `189`, central and flank

### Tier C: already-known anchors to keep in view

6. `171`, coexistence modulus
7. `177`, shared defect modulus

The first new full exact promotions should therefore be:

- `183` central
- `201` flank

That is the best current next pair.

## 6. What this settles and what it does not

Settled at campaign level:

- the late branch should be treated as a two-family atlas;
- the corrected zero-state atlas is good enough to route the next exact jobs;
- a tentative mod-`30` organization is now the best working map;
- the next full `B_m` promotions can be chosen sharply.

Not settled:

- no new full exact `B_m` decomposition is claimed here;
- no all-`m` theorem is claimed for the late branch;
- no donor-color (`0,2`) closure is added.

## 7. Bottom line

The combined exact ledger and corrected atlas now support the following
operational picture:

\[
\begin{array}{c|c}
 m \bmod 30 & \text{first family to promote} \\
\hline
3 & \text{central} \\
9 & \text{both / crossover} \\
21 & \text{flank} \\
27 & \text{flank (fragile lane)}
\end{array}
\]

This is not yet the final theorem.
But it is a much better resonant late campaign map than a blind family sweep,
and it makes the next exact promotions concrete.
