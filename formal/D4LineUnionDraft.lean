import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

open Function

/-!
Unverified draft skeleton for the `d = 4` line-union proof from
`d4_line_union_general_theorem_proof_v3.tex`.

This file was written without running Lean in the current environment, so the
import list and some statements may need small adjustments once typechecked.
The goal here is to package the proof into a Lean-friendly sequence of
coordinate definitions and intermediate lemmas.

Key design choice:
* everything is phrased over `ZMod m`;
* the only residue tests are against `0`, `1`, `2`, and `-1`;
* we avoid ordered representatives in `{0, ..., m - 1}`.

Suggested implementation order:
1. `delta_bijective`
2. `firstReturn_eq_R`
3. `secondReturn_eq_T`
4. `psi_conj_T`, `O_pow_m`, `O_exactPeriod`
5. `T_exactPeriod`, `R_exactPeriod`, `step_exactPeriod`
-/

namespace D4LineUnion

abbrev V (m : ℕ) := Fin 4 → ZMod m

def e {m : ℕ} (i : Fin 4) : V m :=
  Pi.single i (1 : ZMod m)

def S {m : ℕ} (x : V m) : ZMod m :=
  x 0 + x 1 + x 2 + x 3

def q {m : ℕ} (x : V m) : ZMod m :=
  x 0 + x 2

def P0 {m : ℕ} : Set (V m) :=
  {x | S x = 0}

def Q {m : ℕ} : Set (V m) :=
  {x | S x = 0 ∧ q x = (-1 : ZMod m)}

def ind {m : ℕ} (p : Prop) [Decidable p] : ZMod m :=
  if p then 1 else 0

/-- `(3,2,1,0)` -/
def t3210 : Fin 4 → Fin 4
  | 0 => 3
  | 1 => 2
  | 2 => 1
  | 3 => 0

/-- `(1,0,3,2)` -/
def t1032 : Fin 4 → Fin 4
  | 0 => 1
  | 1 => 0
  | 2 => 3
  | 3 => 2

/-- `(0,1,2,3)` -/
def t0123 : Fin 4 → Fin 4 :=
  fun i => i

/-- `(0,3,2,1)` -/
def t0321 : Fin 4 → Fin 4
  | 0 => 0
  | 1 => 3
  | 2 => 2
  | 3 => 1

/-- `(2,1,0,3)` -/
def t2103 : Fin 4 → Fin 4
  | 0 => 2
  | 1 => 1
  | 2 => 0
  | 3 => 3

/-- `(2,3,0,1)` -/
def t2301 : Fin 4 → Fin 4
  | 0 => 2
  | 1 => 3
  | 2 => 0
  | 3 => 1

/--
The line-union witness, rewritten entirely as residue tests in `ZMod m`.

* `S = 0`, `q = 0` gives `(3,2,1,0)`
* `S = 0`, `q ≠ 0` gives `(1,0,3,2)`
* `S = 1` gives `(0,1,2,3)`
* `S = 2`, `q = 0` applies the two commuting defect swaps
* everything else gives `(0,1,2,3)`.
-/
def delta {m : ℕ} (x : V m) : Fin 4 → Fin 4 :=
  if hS0 : S x = 0 then
    if hq0 : q x = 0 then t3210 else t1032
  else if hS1 : S x = 1 then
    t0123
  else if hH : S x = 2 ∧ q x = 0 then
    if hx0 : x 0 = 0 then
      if hx3 : x 3 = 0 then t2301 else t0321
    else
      if hx3 : x 3 = 0 then t2103 else t0123
  else
    t0123

/-- The color-`c` map on the full torus. -/
def step {m : ℕ} (c : Fin 4) (x : V m) : V m :=
  x + e (delta x c)

/-- Coordinates on `P0 = {S = 0}` via `(a,b,q) ↦ (a,b,q-a,-q-b)`. -/
structure P0Coord (m : ℕ) where
  a : ZMod m
  b : ZMod m
  qv : ZMod m
deriving DecidableEq

/-- Coordinates on `Q = {S = 0, q = -1}` via `(a,b)`. -/
structure QCoord (m : ℕ) where
  a : ZMod m
  b : ZMod m
deriving DecidableEq

namespace QCoord

/-- View a `Q`-coordinate as a `P0`-coordinate with `q = -1`. -/
def toP0Coord {m : ℕ} (u : QCoord m) : P0Coord m :=
  { a := u.a, b := u.b, qv := (-1 : ZMod m) }

end QCoord

/-- The `P0` parameterization `(a,b,q) ↦ (a,b,q-a,-q-b)`. -/
def phi {m : ℕ} (u : P0Coord m) : V m
  | 0 => u.a
  | 1 => u.b
  | 2 => u.qv - u.a
  | 3 => -u.qv - u.b

/-- The `Q` parameterization `(a,b) ↦ (a,b,-1-a,1-b)`. -/
def phiQ {m : ℕ} (u : QCoord m) : V m :=
  phi (u.toP0Coord)

/-- Recover `(a,b,q)` from a point on `P0`; correctness uses `S x = 0`. -/
def coordOfP0 {m : ℕ} (x : V m) : P0Coord m :=
  { a := x 0, b := x 1, qv := q x }

/-- Recover `(a,b)` from a point on `Q`; correctness uses `S x = 0` and `q x = -1`. -/
def coordOfQ {m : ℕ} (x : V m) : QCoord m :=
  { a := x 0, b := x 1 }

/-- The first return map on `P0`, written in `(a,b,q)` coordinates. -/
def R {m : ℕ} : Fin 4 → P0Coord m → P0Coord m
  | 0, u =>
      if hq0 : u.qv = 0 then
        { a := u.a - 1, b := u.b, qv := u.qv - 1 }
      else if hbranch : u.qv = (-1 : ZMod m) ∧ u.b = 1 then
        { a := u.a - 2, b := u.b + 1, qv := u.qv - 1 }
      else
        { a := u.a - 1, b := u.b + 1, qv := u.qv - 1 }
  | 1, u =>
      if hq0 : u.qv = 0 then
        { a := u.a, b := u.b - 1, qv := u.qv + 1 }
      else if hbranch : u.qv = (-1 : ZMod m) ∧ u.a = (-1 : ZMod m) then
        { a := u.a + 1, b := u.b - 2, qv := u.qv + 1 }
      else
        { a := u.a + 1, b := u.b - 1, qv := u.qv + 1 }
  | 2, u =>
      if hq0 : u.qv = 0 then
        { a := u.a, b := u.b + 1, qv := u.qv - 1 }
      else if hbranch : u.qv = (-1 : ZMod m) ∧ u.b = 2 then
        { a := u.a + 1, b := u.b, qv := u.qv - 1 }
      else
        { a := u.a, b := u.b, qv := u.qv - 1 }
  | 3, u =>
      if hq0 : u.qv = 0 then
        { a := u.a + 1, b := u.b, qv := u.qv + 1 }
      else if hbranch : u.qv = (-1 : ZMod m) ∧ u.a = 0 then
        { a := u.a, b := u.b + 1, qv := u.qv + 1 }
      else
        { a := u.a, b := u.b, qv := u.qv + 1 }

/-- The second return map on `Q`, written in `(a,b)` coordinates. -/
def T {m : ℕ} : Fin 4 → QCoord m → QCoord m
  | 0, u =>
      { a := u.a - ind (u.b = 1), b := u.b - 1 }
  | 1, u =>
      { a := u.a - 1, b := u.b - ind (u.a = (-1 : ZMod m)) }
  | 2, u =>
      { a := u.a + ind (u.b = 2), b := u.b + 1 }
  | 3, u =>
      { a := u.a + 1, b := u.b + ind (u.a = 0) }

/-- The standard odometer on `(ZMod m)^2`. -/
def O {m : ℕ} (u : QCoord m) : QCoord m :=
  { a := u.a + 1, b := u.b + ind (u.a = 0) }

/-- The conjugacies from the four `T`-maps to the odometer. -/
def psi {m : ℕ} : Fin 4 → QCoord m → QCoord m
  | 0, u => { a := 1 - u.b, b := -u.a }
  | 1, u => { a := -u.a - 1, b := -u.b }
  | 2, u => { a := u.b - 2, b := u.a }
  | 3, u => u

/-- Explicit inverses for `psi`. -/
def psiInv {m : ℕ} : Fin 4 → QCoord m → QCoord m
  | 0, u => { a := -u.b, b := 1 - u.a }
  | 1, u => { a := -u.a - 1, b := -u.b }
  | 2, u => { a := u.b, b := u.a + 2 }
  | 3, u => u

/-- Exact period packaged in the concrete form used by the paper. -/
def ExactPeriod {α : Type _} (f : α → α) (n : ℕ) : Prop :=
  ∀ x, (f^[n]) x = x ∧ ∀ t : ℕ, 0 < t → t < n → (f^[t]) x ≠ x

/-- The sign by which `R c` changes the `q`-coordinate. -/
def qSign {m : ℕ} : Fin 4 → ZMod m
  | 0 => -1
  | 1 => 1
  | 2 => -1
  | 3 => 1

section Skeleton

/-!
All proofs below are intended placeholders.

The most robust route is:
* prove the coordinate identities first (`phi`, `coordOfP0`, `coordOfQ`);
* prove the local step formulas;
* prove the displayed formulas for `R` and `T`;
* transfer exact period along `psi` and then lift from `Q` to `P0` to the full torus.
-/

theorem delta_bijective {m : ℕ} (x : V m) : Function.Bijective (delta x) := by
  have h3210 : Function.LeftInverse t3210 t3210 := by
    intro i
    fin_cases i <;> rfl
  have h1032 : Function.LeftInverse t1032 t1032 := by
    intro i
    fin_cases i <;> rfl
  have h0123 : Function.LeftInverse t0123 t0123 := by
    intro i
    rfl
  have h0321 : Function.LeftInverse t0321 t0321 := by
    intro i
    fin_cases i <;> rfl
  have h2103 : Function.LeftInverse t2103 t2103 := by
    intro i
    fin_cases i <;> rfl
  have h2301 : Function.LeftInverse t2301 t2301 := by
    intro i
    fin_cases i <;> rfl
  unfold delta
  split_ifs <;> first
    | exact ⟨h3210.injective, h3210.surjective⟩
    | exact ⟨h1032.injective, h1032.surjective⟩
    | exact ⟨h0123.injective, h0123.surjective⟩
    | exact ⟨h0321.injective, h0321.surjective⟩
    | exact ⟨h2103.injective, h2103.surjective⟩
    | exact ⟨h2301.injective, h2301.surjective⟩

theorem S_add_e {m : ℕ} (x : V m) (i : Fin 4) :
    S (x + e i) = S x + 1 := by
  fin_cases i <;> simp [S, e, Pi.single, add_assoc, add_left_comm, add_comm]

theorem S_step {m : ℕ} (c : Fin 4) (x : V m) :
    S (step c x) = S x + 1 := by
  simpa [step] using S_add_e x (delta x c)

theorem step_iterate_S {m : ℕ} (c : Fin 4) (x : V m) (t : ℕ) :
    S (((step c)^[t]) x) = S x + t := by
  induction t with
  | zero =>
      simp
  | succ t ih =>
      rw [iterate_succ_apply', S_step, ih, Nat.cast_add]
      ring

theorem phi_mem_P0 {m : ℕ} (u : P0Coord m) :
    phi u ∈ P0 (m := m) := by
  rcases u with ⟨a, b, qv⟩
  simp [P0, S, phi]
  ring

theorem phiQ_mem_Q {m : ℕ} (u : QCoord m) :
    phiQ u ∈ Q (m := m) := by
  rcases u with ⟨a, b⟩
  constructor
  · simp [phiQ, QCoord.toP0Coord, S, phi]
    ring
  · simp [phiQ, Q, q, phi, QCoord.toP0Coord]

theorem q_phi {m : ℕ} (u : P0Coord m) :
    q (phi u) = u.qv := by
  rcases u with ⟨a, b, qv⟩
  simp [q, phi]

theorem coordOfP0_phi {m : ℕ} (u : P0Coord m) :
    coordOfP0 (phi u) = u := by
  rcases u with ⟨a, b, qv⟩
  simp [coordOfP0, q_phi, phi, P0Coord.mk.injEq]

theorem phi_coordOfP0 {m : ℕ} (x : V m) (hx : S x = 0) :
    phi (coordOfP0 x) = x := by
  ext i
  fin_cases i
  · simp [phi, coordOfP0]
  · simp [phi, coordOfP0]
  · simp [phi, coordOfP0, q]
  · have hsum : x 0 + x 1 + x 2 = -x 3 := by
      have hsum0 : x 0 + x 1 + x 2 + x 3 = 0 := by
        simpa [S] using hx
      calc
        x 0 + x 1 + x 2 = (x 0 + x 1 + x 2 + x 3) - x 3 := by ring
        _ = 0 - x 3 := by rw [hsum0]
        _ = -x 3 := by ring
    calc
      phi (coordOfP0 x) 3 = -(q x) - x 1 := by simp [phi, coordOfP0]
      _ = -(x 0 + x 2) - x 1 := by simp [q]
      _ = -(x 0 + x 1 + x 2) := by ring
      _ = x 3 := by rw [hsum]; ring

theorem coordOfQ_phiQ {m : ℕ} (u : QCoord m) :
    coordOfQ (phiQ u) = u := by
  rcases u with ⟨a, b⟩
  simp [coordOfQ, phiQ, phi, QCoord.toP0Coord]

theorem phiQ_coordOfQ {m : ℕ} (x : V m) (hx0 : S x = 0) (hq : q x = (-1 : ZMod m)) :
    phiQ (coordOfQ x) = x := by
  ext i
  fin_cases i
  · simp [phiQ, coordOfQ, phi, QCoord.toP0Coord]
  · simp [phiQ, coordOfQ, phi, QCoord.toP0Coord]
  · calc
      phiQ (coordOfQ x) 2 = (-1 : ZMod m) - x 0 := by
        simp [phiQ, coordOfQ, phi, QCoord.toP0Coord]
      _ = q x - x 0 := by rw [hq]
      _ = x 2 := by simp [q]
  · have hsum : x 1 + x 3 = (1 : ZMod m) := by
      have hsum0 : x 0 + x 1 + x 2 + x 3 = 0 := by
        simpa [S] using hx0
      have hq' : x 0 + x 2 = (-1 : ZMod m) := by
        simpa [q] using hq
      calc
        x 1 + x 3 = (x 0 + x 1 + x 2 + x 3) - (x 0 + x 2) := by ring
        _ = 0 - (-1 : ZMod m) := by rw [hsum0, hq']
        _ = 1 := by ring
    calc
      phiQ (coordOfQ x) 3 = 1 - x 1 := by
        simp [phiQ, coordOfQ, phi, QCoord.toP0Coord]
      _ = x 3 := by
        rw [← hsum]
        ring

/-- First return to `P0`: this is the place where the 2-step local analysis lives. -/
theorem firstReturn_eq_R {m : ℕ} (c : Fin 4) (u : P0Coord m) :
    ((step c)^[m]) (phi u) = phi (R c u) := by
  sorry

/-- Second return to `Q`: sum the branch increments over one full `q`-turn. -/
theorem secondReturn_eq_T {m : ℕ} (c : Fin 4) (u : QCoord m) :
    ((R c)^[m]) (u.toP0Coord) = (T c u).toP0Coord := by
  sorry

theorem R_q_update {m : ℕ} (c : Fin 4) (u : P0Coord m) :
    (R c u).qv = u.qv + qSign (m := m) c := by
  sorry

theorem R_iterate_q {m : ℕ} (c : Fin 4) (u : P0Coord m) (t : ℕ) :
    (((R c)^[t]) u).qv = u.qv + (t : ZMod m) * qSign (m := m) c := by
  sorry

theorem psiInv_left {m : ℕ} (c : Fin 4) :
    Function.LeftInverse (psiInv (m := m) c) (psi (m := m) c) := by
  intro u
  rcases u with ⟨a, b⟩
  fin_cases c <;> simp [psi, psiInv]

theorem psi_left {m : ℕ} (c : Fin 4) :
    Function.RightInverse (psiInv (m := m) c) (psi (m := m) c) := by
  intro u
  rcases u with ⟨a, b⟩
  fin_cases c <;> simp [psi, psiInv]

theorem psi_bijective {m : ℕ} (c : Fin 4) :
    Function.Bijective (psi (m := m) c) := by
  exact ⟨(psiInv_left (m := m) c).injective, (psi_left (m := m) c).surjective⟩

theorem psi_conj_T {m : ℕ} (c : Fin 4) (u : QCoord m) :
    psi c (T c u) = O (psi c u) := by
  sorry

/-- In `m` odometer steps, the first coordinate resets and the second increases by `1`. -/
theorem O_pow_m {m : ℕ} (u : QCoord m) :
    ((O (m := m))^[m]) u = { a := u.a, b := u.b + 1 } := by
  sorry

theorem O_exactPeriod {m : ℕ} (hm : 3 ≤ m) :
    ExactPeriod (O (m := m)) (m ^ 2) := by
  sorry

theorem T_exactPeriod {m : ℕ} (hm : 3 ≤ m) (c : Fin 4) :
    ExactPeriod (T (m := m) c) (m ^ 2) := by
  sorry

theorem R_exactPeriod {m : ℕ} (hm : 3 ≤ m) (c : Fin 4) :
    ExactPeriod (R (m := m) c) (m ^ 3) := by
  sorry

theorem step_exactPeriod {m : ℕ} (hm : 3 ≤ m) (c : Fin 4) :
    ExactPeriod (step (m := m) c) (m ^ 4) := by
  sorry

/--
Draft final package:
* `delta x` is a permutation of the four directions for every `x`;
* each color map has exact period `m^4`, hence one orbit of full size.

This is the concrete theorem you can later repackage as a graph-theoretic
Hamilton decomposition statement if desired.
-/
theorem hamilton_decomposition_d4_draft (m : ℕ) (hm : 3 ≤ m) :
    (∀ x : V m, Function.Bijective (delta x)) ∧
    (∀ c : Fin 4, ExactPeriod (step (m := m) c) (m ^ 4)) := by
  constructor
  · intro x
    simpa using delta_bijective (m := m) x
  · intro c
    simpa using step_exactPeriod (m := m) hm c

end Skeleton

end D4LineUnion
