import TorusD4.SecondReturn
import TorusD4.Lifts

namespace TorusD4

def splitP0Equiv : P0Coord m ≃ QCoord m × ZMod m where
  toFun x := (abCoord (m := m) x, qCoord (m := m) x)
  invFun z := (z.1.1, z.1.2, z.2)
  left_inv x := by
    rcases x with ⟨a, b, q0⟩
    rfl
  right_inv z := by
    rcases z with ⟨u, q0⟩
    rcases u with ⟨a, b⟩
    rfl

@[simp] theorem splitP0Equiv_apply (x : P0Coord m) :
    splitP0Equiv (m := m) x = (abCoord (m := m) x, qCoord (m := m) x) := rfl

@[simp] theorem splitP0Equiv_symm_apply (z : QCoord m × ZMod m) :
    (splitP0Equiv (m := m)).symm z = (z.1.1, z.1.2, z.2) := rfl

@[simp] theorem splitP0Equiv_sliceQ (u : QCoord m) :
    splitP0Equiv (m := m) (sliceQ (m := m) u) = slicePoint (-1 : ZMod m) u := by
  rcases u with ⟨a, b⟩
  rfl

@[simp] theorem splitP0Equiv_symm_slicePoint (u : QCoord m) :
    (splitP0Equiv (m := m)).symm (slicePoint (-1 : ZMod m) u) = sliceQ (m := m) u := by
  rcases u with ⟨a, b⟩
  rfl

def pairRMap (c : Color) : QCoord m × ZMod m → QCoord m × ZMod m :=
  fun z => splitP0Equiv (m := m) (RMap (m := m) c ((splitP0Equiv (m := m)).symm z))

theorem splitP0Equiv_semiconj_pairRMap (c : Color) :
    Function.Semiconj (splitP0Equiv (m := m)) (RMap (m := m) c) (pairRMap (m := m) c) := by
  intro x
  rfl

theorem splitP0Equiv_symm_semiconj_RMap (c : Color) :
    Function.Semiconj (splitP0Equiv (m := m)).symm (pairRMap (m := m) c) (RMap (m := m) c) := by
  exact (splitP0Equiv_semiconj_pairRMap (m := m) c).inverse_left
    (splitP0Equiv (m := m)).left_inv (splitP0Equiv (m := m)).right_inv

theorem iterate_m_pairRMap_slicePoint (hm : 3 ≤ m) (c : Color) (u : QCoord m) :
    ((pairRMap (m := m) c)^[m]) (slicePoint (-1 : ZMod m) u) =
      slicePoint (-1 : ZMod m) (TMap (m := m) c u) := by
  have hsemi := splitP0Equiv_semiconj_pairRMap (m := m) c
  calc
    ((pairRMap (m := m) c)^[m]) (slicePoint (-1 : ZMod m) u)
        = splitP0Equiv (m := m) (((RMap (m := m) c)^[m]) (sliceQ (m := m) u)) := by
            symm
            simpa using (hsemi.iterate_right m).eq (sliceQ (m := m) u)
    _ = splitP0Equiv (m := m) (sliceQ (m := m) (TMap (m := m) c u)) := by
          rw [iterate_m_sliceQ_eq_sliceQ_TMap (m := m) hm c u]
    _ = slicePoint (-1 : ZMod m) (TMap (m := m) c u) := by
          simp [slicePoint]

theorem iterate_mul_pairRMap_slicePoint (hm : 3 ≤ m) (c : Color) :
    ∀ t u, ((pairRMap (m := m) c)^[m * t]) (slicePoint (-1 : ZMod m) u) =
      slicePoint (-1 : ZMod m) (((TMap (m := m) c)^[t]) u) := by
  letI : Fact (0 < m) := ⟨by omega⟩
  exact iterate_mul_slicePoint (m := m)
    (F := pairRMap (m := m) c) (T := TMap (m := m) c) (q0 := (-1 : ZMod m))
    (hreturn := iterate_m_pairRMap_slicePoint (m := m) hm c)

theorem iterate_mul_RMap_sliceQ_eq_sliceQ_TMap_iterate
    (hm : 3 ≤ m) (c : Color) (t : ℕ) (u : QCoord m) :
    ((RMap (m := m) c)^[m * t]) (sliceQ (m := m) u) =
      sliceQ (m := m) (((TMap (m := m) c)^[t]) u) := by
  have hsemi := splitP0Equiv_symm_semiconj_RMap (m := m) c
  calc
    ((RMap (m := m) c)^[m * t]) (sliceQ (m := m) u)
        = ((RMap (m := m) c)^[m * t]) ((splitP0Equiv (m := m)).symm (slicePoint (-1 : ZMod m) u)) := by
            rfl
    _ = (splitP0Equiv (m := m)).symm (((pairRMap (m := m) c)^[m * t]) (slicePoint (-1 : ZMod m) u)) := by
          symm
          simpa using (hsemi.iterate_right (m * t)).eq (slicePoint (-1 : ZMod m) u)
    _ = (splitP0Equiv (m := m)).symm (slicePoint (-1 : ZMod m) (((TMap (m := m) c)^[t]) u)) := by
          rw [iterate_mul_pairRMap_slicePoint (m := m) hm c t u]
    _ = sliceQ (m := m) (((TMap (m := m) c)^[t]) u) := by
          rfl

theorem iterate_add_mul_RMap_sliceQ
    (hm : 3 ≤ m) (c : Color) (t r : ℕ) (u : QCoord m) :
    ((RMap (m := m) c)^[m * t + r]) (sliceQ (m := m) u) =
      ((RMap (m := m) c)^[r]) (sliceQ (m := m) (((TMap (m := m) c)^[t]) u)) := by
  calc
    ((RMap (m := m) c)^[m * t + r]) (sliceQ (m := m) u)
        = ((RMap (m := m) c)^[r]) (((RMap (m := m) c)^[m * t]) (sliceQ (m := m) u)) := by
            simpa [Nat.add_comm] using
              (Function.iterate_add_apply (RMap (m := m) c) r (m * t) (sliceQ (m := m) u))
    _ = ((RMap (m := m) c)^[r]) (sliceQ (m := m) (((TMap (m := m) c)^[t]) u)) := by
          rw [iterate_mul_RMap_sliceQ_eq_sliceQ_TMap_iterate (m := m) hm c t u]

end TorusD4
