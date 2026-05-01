import TorusD4.Lifts

namespace Shared

open TorusD4

theorem iterate_add_mul_slicePoint
    [Fact (0 < m)]
    {α : Type*} {F : α × ZMod m → α × ZMod m} {T : α → α} {q0 : ZMod m}
    (hreturn : ∀ a, (F^[m]) (slicePoint q0 a) = slicePoint q0 (T a))
    (t r : ℕ) (a : α) :
    (F^[m * t + r]) (slicePoint q0 a) =
      (F^[r]) (slicePoint q0 ((T^[t]) a)) := by
  calc
    (F^[m * t + r]) (slicePoint q0 a)
        = (F^[r]) (((F^[m * t]) (slicePoint q0 a))) := by
            simpa [Nat.add_comm] using
              Function.iterate_add_apply F r (m * t) (slicePoint q0 a)
    _ = (F^[r]) (slicePoint q0 ((T^[t]) a)) := by
          rw [iterate_mul_slicePoint (m := m) (F := F) (T := T)
            (q0 := q0) hreturn t a]

end Shared
