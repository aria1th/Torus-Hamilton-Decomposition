# D5 Autonomous Perturbation Note v25

Artifact `050` gives the two narrow proof-support checks that were worth doing
immediately after `049`.

Both persist through `m=19`.

First, the `048` reset law is not just a pilot-range phenomenon:

- countdown still has zero failures,
- `wrap -> 0`,
- `carry_jump` stays exact on `(s,v,layer)`,
- `other` stays exact on `(s,u,layer)`.

Second, the lower-bound witness pair from the `047/048` theorem direction is
now visibly stable:

- `x^-_m = (m-2,2,1,2,0)`,
- `x^+_m = (m-1,2,1,2,0)`,
- common `B = (3,1,2,0,regular)`,
- `tau = m-3` and `m-4`,
- common future-binary prefix length `m-5`.

So the proof side now has larger-modulus support for both its positive small
reset law and its negative bounded-horizon witness family, while the theorem
object itself stays unchanged.
