import TorusD4.ReturnLifts
import TorusD4.Cycles
import TorusD4.Lifts

namespace TorusD4

theorem cycleOn_RMap_of_cycleOn_TMap [Fact (0 < m)] (hm : 3 ≤ m) (c : Color)
    {u : QCoord m} (hc : CycleOn (m * m) (TMap (m := m) c) u) :
    CycleOn (m * (m * m)) (RMap (m := m) c) (sliceQ (m := m) u) := by
  letI : NeZero m := ⟨Nat.ne_of_gt Fact.out⟩
  letI : Fact (0 < m * m) := ⟨Nat.mul_pos Fact.out Fact.out⟩
  letI : Fintype (P0Coord m) := inferInstance
  refine ⟨?_, ?_⟩
  · have hinj :
        Function.Injective fun i : Fin (m * (m * m)) =>
          ((RMap (m := m) c)^[i.1]) (sliceQ (m := m) u) := by
        intro i j hij
        let ti : ℕ := i.1 / m
        let tj : ℕ := j.1 / m
        let ri : ℕ := i.1 % m
        let rj : ℕ := j.1 % m
        have hi_decomp : i.1 = m * ti + ri := by
          dsimp [ti, ri]
          exact (Nat.div_add_mod i.1 m).symm
        have hj_decomp : j.1 = m * tj + rj := by
          dsimp [tj, rj]
          exact (Nat.div_add_mod j.1 m).symm
        have hti_lt : ti < m * m := by
          dsimp [ti]
          have hi_bound : i.1 < (m * m) * m := by
            simpa [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using i.2
          exact (Nat.div_lt_iff_lt_mul Fact.out).2 hi_bound
        have htj_lt : tj < m * m := by
          dsimp [tj]
          have hj_bound : j.1 < (m * m) * m := by
            simpa [Nat.mul_assoc, Nat.mul_left_comm, Nat.mul_comm] using j.2
          exact (Nat.div_lt_iff_lt_mul Fact.out).2 hj_bound
        have hri_lt : ri < m := by
          dsimp [ri]
          exact Nat.mod_lt _ Fact.out
        have hrj_lt : rj < m := by
          dsimp [rj]
          exact Nat.mod_lt _ Fact.out
        change
          ((RMap (m := m) c)^[i.1]) (sliceQ (m := m) u) =
            ((RMap (m := m) c)^[j.1]) (sliceQ (m := m) u) at hij
        rw [hi_decomp, iterate_add_mul_RMap_sliceQ (m := m) hm c ti ri u,
          hj_decomp, iterate_add_mul_RMap_sliceQ (m := m) hm c tj rj u] at hij
        have hq :
            (-1 : ZMod m) + (ri : ZMod m) * qSign (m := m) c =
              (-1 : ZMod m) + (rj : ZMod m) * qSign (m := m) c := by
          simpa using congrArg (qCoord (m := m)) hij
        have hq' : (ri : ZMod m) * qSign (m := m) c = (rj : ZMod m) * qSign (m := m) c := by
          exact add_left_cancel hq
        have hcast : ((ri : ℕ) : ZMod m) = ((rj : ℕ) : ZMod m) := by
          fin_cases c
          · exact neg_injective (by simpa [qSign, mul_comm] using hq')
          · simpa [qSign] using hq'
          · exact neg_injective (by simpa [qSign, mul_comm] using hq')
          · simpa [qSign] using hq'
        have hrem_mod : ri % m = rj % m := by
          exact (ZMod.natCast_eq_natCast_iff' ri rj m).1 hcast
        have hrem : ri = rj := by
          rwa [Nat.mod_eq_of_lt hri_lt, Nat.mod_eq_of_lt hrj_lt] at hrem_mod
        have hij_shift :
            ((RMap (m := m) c)^[m - ri])
                (((RMap (m := m) c)^[ri]) (sliceQ (m := m) (((TMap (m := m) c)^[ti]) u))) =
              ((RMap (m := m) c)^[m - ri])
                (((RMap (m := m) c)^[rj]) (sliceQ (m := m) (((TMap (m := m) c)^[tj]) u))) := by
          exact congrArg ((RMap (m := m) c)^[m - ri]) hij
        have hleft :
            ((RMap (m := m) c)^[m - ri])
                (((RMap (m := m) c)^[ri]) (sliceQ (m := m) (((TMap (m := m) c)^[ti]) u))) =
              sliceQ (m := m) (((TMap (m := m) c)^[ti + 1]) u) := by
          calc
            ((RMap (m := m) c)^[m - ri])
                (((RMap (m := m) c)^[ri]) (sliceQ (m := m) (((TMap (m := m) c)^[ti]) u)))
                = ((RMap (m := m) c)^[m - ri + ri])
                    (sliceQ (m := m) (((TMap (m := m) c)^[ti]) u)) := by
                      symm
                      simpa using
                        (Function.iterate_add_apply (RMap (m := m) c) (m - ri) ri
                          (sliceQ (m := m) (((TMap (m := m) c)^[ti]) u)))
            _ = ((RMap (m := m) c)^[m]) (sliceQ (m := m) (((TMap (m := m) c)^[ti]) u)) := by
                  rw [Nat.sub_add_cancel (Nat.le_of_lt hri_lt)]
            _ = sliceQ (m := m) (TMap (m := m) c (((TMap (m := m) c)^[ti]) u)) := by
                  rw [iterate_m_sliceQ_eq_sliceQ_TMap (m := m) hm c (((TMap (m := m) c)^[ti]) u)]
            _ = sliceQ (m := m) (((TMap (m := m) c)^[ti + 1]) u) := by
                  rw [Function.iterate_succ_apply']
        have hright0 :
            ((RMap (m := m) c)^[m - rj])
                (((RMap (m := m) c)^[rj]) (sliceQ (m := m) (((TMap (m := m) c)^[tj]) u))) =
              sliceQ (m := m) (((TMap (m := m) c)^[tj + 1]) u) := by
          calc
            ((RMap (m := m) c)^[m - rj])
                (((RMap (m := m) c)^[rj]) (sliceQ (m := m) (((TMap (m := m) c)^[tj]) u)))
                = ((RMap (m := m) c)^[m - rj + rj])
                    (sliceQ (m := m) (((TMap (m := m) c)^[tj]) u)) := by
                      symm
                      simpa using
                        (Function.iterate_add_apply (RMap (m := m) c) (m - rj) rj
                          (sliceQ (m := m) (((TMap (m := m) c)^[tj]) u)))
            _ = ((RMap (m := m) c)^[m]) (sliceQ (m := m) (((TMap (m := m) c)^[tj]) u)) := by
                  rw [Nat.sub_add_cancel (Nat.le_of_lt hrj_lt)]
            _ = sliceQ (m := m) (TMap (m := m) c (((TMap (m := m) c)^[tj]) u)) := by
                  rw [iterate_m_sliceQ_eq_sliceQ_TMap (m := m) hm c (((TMap (m := m) c)^[tj]) u)]
            _ = sliceQ (m := m) (((TMap (m := m) c)^[tj + 1]) u) := by
                  rw [Function.iterate_succ_apply']
        have hright :
            ((RMap (m := m) c)^[m - ri])
                (((RMap (m := m) c)^[rj]) (sliceQ (m := m) (((TMap (m := m) c)^[tj]) u))) =
              sliceQ (m := m) (((TMap (m := m) c)^[tj + 1]) u) := by
          simpa [hrem] using hright0
        have hslice :
            sliceQ (m := m) (((TMap (m := m) c)^[ti + 1]) u) =
              sliceQ (m := m) (((TMap (m := m) c)^[tj + 1]) u) := by
          calc
            sliceQ (m := m) (((TMap (m := m) c)^[ti + 1]) u)
                = ((RMap (m := m) c)^[m - ri])
                    (((RMap (m := m) c)^[ri]) (sliceQ (m := m) (((TMap (m := m) c)^[ti]) u))) := by
                      symm
                      exact hleft
            _ = ((RMap (m := m) c)^[m - ri])
                  (((RMap (m := m) c)^[rj]) (sliceQ (m := m) (((TMap (m := m) c)^[tj]) u))) :=
                    hij_shift
            _ = sliceQ (m := m) (((TMap (m := m) c)^[tj + 1]) u) := hright
        have ht_eq : ((TMap (m := m) c)^[ti + 1]) u = ((TMap (m := m) c)^[tj + 1]) u := by
          simpa using congrArg (abCoord (m := m)) hslice
        have ht_mod : ti + 1 ≡ tj + 1 [MOD m * m] :=
          TorusD4.cycleOn_iterate_modEq (N := m * m) (f := TMap (m := m) c) (x := u) hc ht_eq
        have ht'_mod : ti ≡ tj [MOD m * m] := Nat.ModEq.add_right_cancel' 1 <| by
          simpa [Nat.add_comm] using ht_mod
        have ht : ti = tj := by
          simpa [Nat.ModEq, Nat.mod_eq_of_lt hti_lt, Nat.mod_eq_of_lt htj_lt] using ht'_mod
        apply Fin.eq_of_val_eq
        calc
          i.1 = m * ti + ri := hi_decomp
          _ = m * tj + rj := by rw [ht, hrem]
          _ = j.1 := hj_decomp.symm
    exact (Fintype.bijective_iff_injective_and_card _).2
      ⟨hinj, by simp [P0Coord]⟩
  · calc
      ((RMap (m := m) c)^[m * (m * m)]) (sliceQ (m := m) u)
          = sliceQ (m := m) (((TMap (m := m) c)^[m * m]) u) := by
              rw [iterate_mul_RMap_sliceQ_eq_sliceQ_TMap_iterate (m := m) hm c (m * m) u]
      _ = sliceQ (m := m) u := by rw [hc.2]

theorem hasCycle_RMap [Fact (0 < m)] (hm : 3 ≤ m) (c : Color) :
    HasCycle (m * (m * m)) (RMap (m := m) c) := by
  fin_cases c
  · rcases cycleOn_T0 (m := m) with ⟨u, hu⟩
    exact ⟨sliceQ (m := m) u, cycleOn_RMap_of_cycleOn_TMap (m := m) hm 0 hu⟩
  · rcases cycleOn_T1 (m := m) with ⟨u, hu⟩
    exact ⟨sliceQ (m := m) u, cycleOn_RMap_of_cycleOn_TMap (m := m) hm 1 hu⟩
  · rcases cycleOn_T2 (m := m) with ⟨u, hu⟩
    exact ⟨sliceQ (m := m) u, cycleOn_RMap_of_cycleOn_TMap (m := m) hm 2 hu⟩
  · rcases cycleOn_T3 (m := m) with ⟨u, hu⟩
    exact ⟨sliceQ (m := m) u, cycleOn_RMap_of_cycleOn_TMap (m := m) hm 3 hu⟩

theorem hasCycle_RMap_cube [Fact (0 < m)] (hm : 3 ≤ m) (c : Color) :
    HasCycle (m ^ 3) (RMap (m := m) c) := by
  simpa [pow_succ, pow_two, Nat.mul_assoc] using hasCycle_RMap (m := m) hm c

end TorusD4
