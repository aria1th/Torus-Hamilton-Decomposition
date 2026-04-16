import TorusD5.FullCoordinates
import Mathlib.Data.Finset.Basic

namespace TorusD5

/--
The theorem-side D5 notes work with the full five-coordinate state and the
visible four-tuple `(a,c,d,e)` on the `Σ = 0` section, with the hidden `b`
coordinate reconstructed from the section equation.
-/
abbrev State5 (m : ℕ) := Point m

def sigma (x : State5 m) : ZMod m := S x

abbrev SigmaZero (m : ℕ) := {x : State5 m // sigma x = 0}

/-- Visible theorem-side coordinates `(a,c,d,e) = (x₀,x₂,x₃,x₄)`. -/
abbrev VisibleState (m : ℕ) := ZMod m × ZMod m × ZMod m × ZMod m

def aCoord (x : VisibleState m) : ZMod m := x.1
def cCoord (x : VisibleState m) : ZMod m := x.2.1
def dCoord (x : VisibleState m) : ZMod m := x.2.2.1
def eCoord (x : VisibleState m) : ZMod m := x.2.2.2

/-- Hidden `b = x₁` recovered from the `Σ = 0` section equation. -/
def hiddenB (x : VisibleState m) : ZMod m :=
  -aCoord (m := m) x - cCoord (m := m) x - dCoord (m := m) x - eCoord (m := m) x

/-- Reconstruct a full `Σ = 0` section state from the visible theorem-side coordinates. -/
def sigmaZeroPoint (x : VisibleState m) : State5 m :=
  ![aCoord (m := m) x, hiddenB (m := m) x, cCoord (m := m) x, dCoord (m := m) x, eCoord (m := m) x]

def sigmaZeroState (x : VisibleState m) : SigmaZero m :=
  ⟨sigmaZeroPoint (m := m) x, by
    rcases x with ⟨a, c, d, e⟩
    simp [sigma, S, sigmaZeroPoint, hiddenB]
    ring⟩

def visibleOfPoint (x : State5 m) : VisibleState m := (x 0, x 2, x 3, x 4)

@[simp] theorem aCoord_mk (a c d e : ZMod m) : aCoord (m := m) (a, c, d, e) = a := rfl
@[simp] theorem cCoord_mk (a c d e : ZMod m) : cCoord (m := m) (a, c, d, e) = c := rfl
@[simp] theorem dCoord_mk (a c d e : ZMod m) : dCoord (m := m) (a, c, d, e) = d := rfl
@[simp] theorem eCoord_mk (a c d e : ZMod m) : eCoord (m := m) (a, c, d, e) = e := rfl

@[simp] theorem sigmaZeroPoint_apply_0 (x : VisibleState m) :
    sigmaZeroPoint (m := m) x 0 = aCoord (m := m) x := by
  rcases x with ⟨a, c, d, e⟩
  simp [sigmaZeroPoint]

@[simp] theorem sigmaZeroPoint_apply_1 (x : VisibleState m) :
    sigmaZeroPoint (m := m) x 1 = hiddenB (m := m) x := by
  rcases x with ⟨a, c, d, e⟩
  simp [sigmaZeroPoint]

@[simp] theorem sigmaZeroPoint_apply_2 (x : VisibleState m) :
    sigmaZeroPoint (m := m) x 2 = cCoord (m := m) x := by
  rcases x with ⟨a, c, d, e⟩
  simp [sigmaZeroPoint]

@[simp] theorem sigmaZeroPoint_apply_3 (x : VisibleState m) :
    sigmaZeroPoint (m := m) x 3 = dCoord (m := m) x := by
  rcases x with ⟨a, c, d, e⟩
  simp [sigmaZeroPoint]

@[simp] theorem sigmaZeroPoint_apply_4 (x : VisibleState m) :
    sigmaZeroPoint (m := m) x 4 = eCoord (m := m) x := by
  rcases x with ⟨a, c, d, e⟩
  simp [sigmaZeroPoint]

@[simp] theorem sigma_sigmaZeroPoint (x : VisibleState m) :
    sigma (m := m) (sigmaZeroPoint (m := m) x) = 0 := by
  exact (sigmaZeroState (m := m) x).2

@[simp] theorem visibleOfPoint_sigmaZeroPoint (x : VisibleState m) :
    visibleOfPoint (m := m) (sigmaZeroPoint (m := m) x) = x := by
  rcases x with ⟨a, c, d, e⟩
  simp [visibleOfPoint, sigmaZeroPoint]

theorem hiddenB_visibleOfSigmaZero (x : SigmaZero m) :
    hiddenB (m := m) (visibleOfPoint (m := m) x.1) = x.1 1 := by
  have hσ : sigma (m := m) x.1 = 0 := x.2
  have h1 :
      (-x.1 0 - x.1 2 - x.1 3 - x.1 4 : ZMod m) = x.1 1 := by
    calc
      (-x.1 0 - x.1 2 - x.1 3 - x.1 4 : ZMod m) = -(x.1 0 + x.1 2 + x.1 3 + x.1 4) := by
        ring
      _ = x.1 1 := by
        symm
        exact
          (eq_neg_iff_add_eq_zero.mpr (by
            simpa [sigma, S, add_assoc, add_left_comm, add_comm] using hσ))
  simpa [hiddenB, visibleOfPoint] using h1

/-- The theorem-side base section `H_m = {c = 0, d = 0}`. -/
def IsHm (x : VisibleState m) : Prop :=
  cCoord (m := m) x = 0 ∧ dCoord (m := m) x = 0

/-- The theorem-side base subset `B_m = {c = 0, d = 0, e = 0}`. -/
def IsBm (x : VisibleState m) : Prop :=
  IsHm (m := m) x ∧ eCoord (m := m) x = 0

abbrev Hm (m : ℕ) := {x : VisibleState m // IsHm (m := m) x}
abbrev Bm (m : ℕ) := {x : VisibleState m // IsBm (m := m) x}

def hmA (x : Hm m) : ZMod m := aCoord (m := m) x.1
def hmE (x : Hm m) : ZMod m := eCoord (m := m) x.1

def bmA (x : Bm m) : ZMod m := aCoord (m := m) x.1

def hmPoint (a e : ZMod m) : Hm m :=
  ⟨(a, 0, 0, e), by simp [IsHm]⟩

def bmPoint (a : ZMod m) : Bm m :=
  ⟨(a, 0, 0, 0), by simp [IsBm, IsHm]⟩

def bmToHm (x : Bm m) : Hm m :=
  ⟨x.1, x.2.1⟩

@[simp] theorem hmA_hmPoint (a e : ZMod m) : hmA (m := m) (hmPoint (m := m) a e) = a := rfl
@[simp] theorem hmE_hmPoint (a e : ZMod m) : hmE (m := m) (hmPoint (m := m) a e) = e := rfl
@[simp] theorem bmA_bmPoint (a : ZMod m) : bmA (m := m) (bmPoint (m := m) a) = a := rfl
@[simp] theorem bmToHm_bmPoint (a : ZMod m) :
    bmToHm (m := m) (bmPoint (m := m) a) = hmPoint (m := m) a 0 := rfl

/-- Residue-family split used by the common `m = 15r + 9` packet notes. -/
inductive CommonResidueFamily
  | r8s
  | r8sPlus4
  | r16uPlus2
  | r16uPlus6
  | r16uPlus10
  | r16uPlus14
  deriving DecidableEq, Repr, Inhabited

/-- The two stable packet geometries identified in the common exact-classification note. -/
inductive StablePacketGeometry
  | typeA
  | typeB
  deriving DecidableEq, Repr, Inhabited

def stablePacketGeometryOfFamily : CommonResidueFamily → StablePacketGeometry
  | .r8s => .typeA
  | .r8sPlus4 => .typeA
  | .r16uPlus2 => .typeB
  | .r16uPlus6 => .typeB
  | .r16uPlus10 => .typeB
  | .r16uPlus14 => .typeB

@[simp] theorem stablePacketGeometry_r8s :
    stablePacketGeometryOfFamily .r8s = .typeA := rfl

@[simp] theorem stablePacketGeometry_r8sPlus4 :
    stablePacketGeometryOfFamily .r8sPlus4 = .typeA := rfl

@[simp] theorem stablePacketGeometry_r16uPlus2 :
    stablePacketGeometryOfFamily .r16uPlus2 = .typeB := rfl

@[simp] theorem stablePacketGeometry_r16uPlus6 :
    stablePacketGeometryOfFamily .r16uPlus6 = .typeB := rfl

@[simp] theorem stablePacketGeometry_r16uPlus10 :
    stablePacketGeometryOfFamily .r16uPlus10 = .typeB := rfl

@[simp] theorem stablePacketGeometry_r16uPlus14 :
    stablePacketGeometryOfFamily .r16uPlus14 = .typeB := rfl

end TorusD5
