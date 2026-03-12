import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Data.Fin.VecNotation

namespace TorusD5

/--
Minimal D5 scaffolding for the extracted return-map model from artifact
`D5-RETURN-MAP-MODEL-017`.

This file does not yet connect the formulas below to the full `mixed_008`
witness in Lean. It only records the section/grouped-return coordinate systems
and the extracted model maps that later proof files should target.
-/
abbrev Coord := Fin 5
abbrev Color := Fin 5
abbrev Point (m : ℕ) := Coord → ZMod m

abbrev SectionCoord (m : ℕ) := ZMod m × ZMod m × ZMod m
abbrev GroupedCoord (m : ℕ) := ZMod m × ZMod m
abbrev SkewCoord (m : ℕ) := ZMod m × ZMod m × ZMod m

def delta (m : ℕ) (p : Prop) [Decidable p] : ZMod m := if p then 1 else 0

/-- In the extracted D5 first-return coordinates, the carry occurs on `q = m - 2`,
which is represented uniformly in `ZMod m` by `q = -2`. -/
def topCarry (q : ZMod m) : ZMod m := delta m (q = (-2 : ZMod m))

/-- Extracted first-return base model on the section coordinates `(q,w,u)`. -/
def firstReturnBase (x : SectionCoord m) : SectionCoord m :=
  let (q, w, u) := x
  (q + 1, w + topCarry (m := m) q, u + 1)

/-- Extracted grouped-return base model on `(w,u)`. -/
def groupedReturnBase (x : GroupedCoord m) : GroupedCoord m :=
  let (w, u) := x
  (w + 1, u)

/-- Abstract skew-product over the grouped-return base. The cocycle is left
symbolic until the D5 grouped cocycle is understood. -/
def groupedSkew (phi : GroupedCoord m → ZMod m) (x : SkewCoord m) : SkewCoord m :=
  let (w, u, t) := x
  (w + 1, u, t + phi (w, u))

def qCoord (x : SectionCoord m) : ZMod m := x.1
def wCoord (x : SectionCoord m) : ZMod m := x.2.1
def uCoord (x : SectionCoord m) : ZMod m := x.2.2

def groupedW (x : GroupedCoord m) : ZMod m := x.1
def groupedU (x : GroupedCoord m) : ZMod m := x.2

def skewBase (x : SkewCoord m) : GroupedCoord m := (x.1, x.2.1)
def skewTwist (x : SkewCoord m) : ZMod m := x.2.2

@[simp] theorem delta_true (m : ℕ) : delta m True = 1 := by
  simp [delta]

@[simp] theorem delta_false (m : ℕ) : delta m False = 0 := by
  simp [delta]

@[simp] theorem qCoord_mk (q w u : ZMod m) : qCoord (m := m) (q, w, u) = q := rfl
@[simp] theorem wCoord_mk (q w u : ZMod m) : wCoord (m := m) (q, w, u) = w := rfl
@[simp] theorem uCoord_mk (q w u : ZMod m) : uCoord (m := m) (q, w, u) = u := rfl

@[simp] theorem groupedW_mk (w u : ZMod m) : groupedW (m := m) (w, u) = w := rfl
@[simp] theorem groupedU_mk (w u : ZMod m) : groupedU (m := m) (w, u) = u := rfl

@[simp] theorem skewBase_mk (w u t : ZMod m) : skewBase (m := m) (w, u, t) = (w, u) := rfl
@[simp] theorem skewTwist_mk (w u t : ZMod m) : skewTwist (m := m) (w, u, t) = t := rfl

@[simp] theorem topCarry_eq_delta (q : ZMod m) :
    topCarry (m := m) q = delta m (q = (-2 : ZMod m)) := rfl

@[simp] theorem firstReturnBase_apply (q w u : ZMod m) :
    firstReturnBase (m := m) (q, w, u) = (q + 1, w + topCarry (m := m) q, u + 1) := rfl

@[simp] theorem groupedReturnBase_apply (w u : ZMod m) :
    groupedReturnBase (m := m) (w, u) = (w + 1, u) := rfl

@[simp] theorem groupedSkew_apply (phi : GroupedCoord m → ZMod m) (w u t : ZMod m) :
    groupedSkew (m := m) phi (w, u, t) = (w + 1, u, t + phi (w, u)) := rfl

@[simp] theorem firstReturnBase_q (x : SectionCoord m) :
    qCoord (m := m) (firstReturnBase (m := m) x) = qCoord (m := m) x + 1 := by
  rcases x with ⟨q, w, u⟩
  rfl

@[simp] theorem firstReturnBase_w (x : SectionCoord m) :
    wCoord (m := m) (firstReturnBase (m := m) x) =
      wCoord (m := m) x + topCarry (m := m) (qCoord (m := m) x) := by
  rcases x with ⟨q, w, u⟩
  rfl

@[simp] theorem firstReturnBase_u (x : SectionCoord m) :
    uCoord (m := m) (firstReturnBase (m := m) x) = uCoord (m := m) x + 1 := by
  rcases x with ⟨q, w, u⟩
  rfl

@[simp] theorem groupedReturnBase_w (x : GroupedCoord m) :
    groupedW (m := m) (groupedReturnBase (m := m) x) = groupedW (m := m) x + 1 := by
  rcases x with ⟨w, u⟩
  rfl

@[simp] theorem groupedReturnBase_u (x : GroupedCoord m) :
    groupedU (m := m) (groupedReturnBase (m := m) x) = groupedU (m := m) x := by
  rcases x with ⟨w, u⟩
  rfl

@[simp] theorem groupedSkew_base (phi : GroupedCoord m → ZMod m) (x : SkewCoord m) :
    skewBase (m := m) (groupedSkew (m := m) phi x) =
      groupedReturnBase (m := m) (skewBase (m := m) x) := by
  rcases x with ⟨w, u, t⟩
  rfl

@[simp] theorem groupedSkew_twist (phi : GroupedCoord m → ZMod m) (x : SkewCoord m) :
    skewTwist (m := m) (groupedSkew (m := m) phi x) =
      skewTwist (m := m) x + phi (skewBase (m := m) x) := by
  rcases x with ⟨w, u, t⟩
  rfl

end TorusD5
