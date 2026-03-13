Optional narrow proof-support check for the next parallel run:

1. Verify the carry_jump explicit formula
   
   R_cj(s,v,layer) = 0 if s+v+layer ≡ 2,
                      1 if s=1 and not zero-reset,
                      m-2 otherwise
   
   on the active boundary through at least m=21 or m=23.

2. Verify the branchwise other-subtype description through the same range:
   - dn=(0,0,1,0) always gives next_tau = m-4
   - dn=(1,0,0,0) gives next_tau = m-3 iff s=1, else 0

3. If possible, record whether the current-state discriminator
   
   r = layer + 3((s-u)-1) mod m
   
   continues to organize the other branch in the same way.

This is only symbolic-proof support. It does not change the theorem object.
