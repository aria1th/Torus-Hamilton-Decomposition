import TorusD5.Basic
import Mathlib.Tactic.Ring

namespace TorusD5

/--
Bundle-backed coordinate model for the `S = 0` slice used in the `017`
extraction code.

The extraction scripts encode section points as

`(-q-w-v-u, q, w, v, u)`,

so the clean-frame section state is obtained by forgetting the `v` coordinate.
-/
abbrev SliceCoord (m : ℕ) := ZMod m × ZMod m × ZMod m × ZMod m

def sliceQ (x : SliceCoord m) : ZMod m := x.1
def sliceW (x : SliceCoord m) : ZMod m := x.2.1
def sliceV (x : SliceCoord m) : ZMod m := x.2.2.1
def sliceU (x : SliceCoord m) : ZMod m := x.2.2.2

def S (x : Point m) : ZMod m := x 0 + x 1 + x 2 + x 3 + x 4

def slicePoint (x : SliceCoord m) : Point m :=
  let (q, w, v, u) := x
  ![-q - w - v - u, q, w, v, u]

def coordOfSlicePoint (x : Point m) : SliceCoord m := (x 1, x 2, x 3, x 4)

def sectionStateOfSlice (x : SliceCoord m) : SectionCoord m :=
  (sliceQ (m := m) x, sliceW (m := m) x, sliceU (m := m) x)

def groupedStateOfSlice (x : SliceCoord m) : GroupedCoord m :=
  (sliceW (m := m) x, sliceU (m := m) x)

def sectionStateOfPoint (x : Point m) : SectionCoord m :=
  (x 1, x 2, x 4)

def groupedStateOfPoint (x : Point m) : GroupedCoord m :=
  (x 2, x 4)

@[simp] theorem sliceQ_mk (q w v u : ZMod m) : sliceQ (m := m) (q, w, v, u) = q := rfl
@[simp] theorem sliceW_mk (q w v u : ZMod m) : sliceW (m := m) (q, w, v, u) = w := rfl
@[simp] theorem sliceV_mk (q w v u : ZMod m) : sliceV (m := m) (q, w, v, u) = v := rfl
@[simp] theorem sliceU_mk (q w v u : ZMod m) : sliceU (m := m) (q, w, v, u) = u := rfl

@[simp] theorem slicePoint_apply_0 (x : SliceCoord m) :
    slicePoint (m := m) x 0 =
      -sliceQ (m := m) x - sliceW (m := m) x - sliceV (m := m) x - sliceU (m := m) x := by
  rcases x with ⟨q, w, v, u⟩
  simp [slicePoint]

@[simp] theorem slicePoint_apply_1 (x : SliceCoord m) :
    slicePoint (m := m) x 1 = sliceQ (m := m) x := by
  rcases x with ⟨q, w, v, u⟩
  simp [slicePoint]

@[simp] theorem slicePoint_apply_2 (x : SliceCoord m) :
    slicePoint (m := m) x 2 = sliceW (m := m) x := by
  rcases x with ⟨q, w, v, u⟩
  simp [slicePoint]

@[simp] theorem slicePoint_apply_3 (x : SliceCoord m) :
    slicePoint (m := m) x 3 = sliceV (m := m) x := by
  rcases x with ⟨q, w, v, u⟩
  simp [slicePoint]

@[simp] theorem slicePoint_apply_4 (x : SliceCoord m) :
    slicePoint (m := m) x 4 = sliceU (m := m) x := by
  rcases x with ⟨q, w, v, u⟩
  simp [slicePoint]

@[simp] theorem S_slicePoint (x : SliceCoord m) : S (slicePoint (m := m) x) = 0 := by
  rcases x with ⟨q, w, v, u⟩
  simp [S, slicePoint]
  ring

@[simp] theorem coordOfSlicePoint_apply (q w v u : ZMod m) :
    coordOfSlicePoint (m := m) (slicePoint (m := m) (q, w, v, u)) = (q, w, v, u) := by
  simp [coordOfSlicePoint, slicePoint]

theorem slicePoint_coordOfSlicePoint {x : Point m} (hS : S x = 0) :
    slicePoint (m := m) (coordOfSlicePoint (m := m) x) = x := by
  ext i
  fin_cases i
  · have h0 :
        (-x 1 - x 2 - x 3 - x 4 : ZMod m) = x 0 := by
        calc
          (-x 1 - x 2 - x 3 - x 4 : ZMod m) = -(x 1 + x 2 + x 3 + x 4) := by
            ring
          _ = x 0 := by
            symm
            exact
              (eq_neg_iff_add_eq_zero.mpr (by
                simpa [S, add_assoc, add_left_comm, add_comm] using hS))
    simpa [coordOfSlicePoint, slicePoint] using h0
  · simp [coordOfSlicePoint, slicePoint]
  · simp [coordOfSlicePoint, slicePoint]
  · simp [coordOfSlicePoint, slicePoint]
  · simp [coordOfSlicePoint, slicePoint]

@[simp] theorem sectionStateOfSlice_mk (q w v u : ZMod m) :
    sectionStateOfSlice (m := m) (q, w, v, u) = (q, w, u) := rfl

@[simp] theorem groupedStateOfSlice_mk (q w v u : ZMod m) :
    groupedStateOfSlice (m := m) (q, w, v, u) = (w, u) := rfl

@[simp] theorem sectionStateOfPoint_slicePoint (x : SliceCoord m) :
    sectionStateOfPoint (m := m) (slicePoint (m := m) x) = sectionStateOfSlice (m := m) x := by
  rcases x with ⟨q, w, v, u⟩
  rfl

@[simp] theorem groupedStateOfPoint_slicePoint (x : SliceCoord m) :
    groupedStateOfPoint (m := m) (slicePoint (m := m) x) = groupedStateOfSlice (m := m) x := by
  rcases x with ⟨q, w, v, u⟩
  rfl

@[simp] theorem sectionStateOfPoint_eq (x : Point m) :
    sectionStateOfPoint (m := m) x = (x 1, x 2, x 4) := rfl

@[simp] theorem groupedStateOfPoint_eq (x : Point m) :
    groupedStateOfPoint (m := m) x = (x 2, x 4) := rfl

end TorusD5
