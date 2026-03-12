import TorusD5.Basic
import Mathlib.Tactic.Ring

namespace TorusD5

/-- Shifted section coordinates used to present the extracted carry law in the
more standard `qHat = q + 1` form. -/
def shiftQ (x : SectionCoord m) : SectionCoord m :=
  let (q, w, u) := x
  (q + 1, w, u)

/-- The same extracted first-return base map, written in the shifted `qHat`
coordinate. -/
def shiftedFirstReturnBase (x : SectionCoord m) : SectionCoord m :=
  let (qHat, w, u) := x
  (qHat + 1, w + delta m (qHat = (-1 : ZMod m)), u + 1)

@[simp] theorem shiftQ_apply (q w u : ZMod m) :
    shiftQ (m := m) (q, w, u) = (q + 1, w, u) := rfl

@[simp] theorem shiftedFirstReturnBase_apply (qHat w u : ZMod m) :
    shiftedFirstReturnBase (m := m) (qHat, w, u) =
      (qHat + 1, w + delta m (qHat = (-1 : ZMod m)), u + 1) := rfl

/-- The extracted carry slice `q = -2` is the shifted carry slice `qHat = -1`
after the coordinate change `qHat = q + 1`. -/
@[simp] theorem topCarry_eq_shiftedDelta (q : ZMod m) :
    topCarry (m := m) q = delta m (q + 1 = (-1 : ZMod m)) := by
  by_cases hq : q = (-2 : ZMod m)
  · have hq' : q + 1 = (-1 : ZMod m) := by
      calc
        q + 1 = (-2 : ZMod m) + 1 := by simp [hq]
        _ = (-1 : ZMod m) := by ring
    rw [topCarry, delta, if_pos hq, delta, if_pos hq']
  · have hq' : q + 1 ≠ (-1 : ZMod m) := by
      intro h
      apply hq
      calc
        q = (q + 1) - 1 := by ring
        _ = ((-1 : ZMod m) - 1) := by simp [h]
        _ = (-2 : ZMod m) := by ring
    rw [topCarry, delta, if_neg hq, delta, if_neg hq']

/-- After shifting `qHat = q + 1`, the extracted D5 first return becomes the
standard carry form with the carry slice at `qHat = -1`. -/
theorem shiftQ_conj_firstReturnBase (x : SectionCoord m) :
    shiftQ (m := m) (firstReturnBase (m := m) x) =
      shiftedFirstReturnBase (m := m) (shiftQ (m := m) x) := by
  rcases x with ⟨q, w, u⟩
  rw [firstReturnBase_apply, shiftQ_apply, shiftQ_apply, shiftedFirstReturnBase_apply,
    topCarry_eq_shiftedDelta]

@[simp] theorem shiftedFirstReturnBase_q (x : SectionCoord m) :
    qCoord (m := m) (shiftedFirstReturnBase (m := m) x) = qCoord (m := m) x + 1 := by
  rcases x with ⟨qHat, w, u⟩
  rfl

@[simp] theorem shiftedFirstReturnBase_w (x : SectionCoord m) :
    wCoord (m := m) (shiftedFirstReturnBase (m := m) x) =
      wCoord (m := m) x + delta m (qCoord (m := m) x = (-1 : ZMod m)) := by
  rcases x with ⟨qHat, w, u⟩
  rfl

@[simp] theorem shiftedFirstReturnBase_u (x : SectionCoord m) :
    uCoord (m := m) (shiftedFirstReturnBase (m := m) x) = uCoord (m := m) x + 1 := by
  rcases x with ⟨qHat, w, u⟩
  rfl

end TorusD5
