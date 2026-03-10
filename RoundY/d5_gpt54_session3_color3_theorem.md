좋다. 이번엔 **부분정리 하나를 실제로 닫았다.**

**[P] 고정된 26-move witness는 모든 홀수 (m\ge 5) 에 대해 color 3을 Hamilton으로 만든다.**
즉, 전체 5색 분해는 아직 [O] 이지만, 이 witness 안에 들어 있는 한 색은 이미 “전 모듈러스 odd family”로 올라간다.

핵심은 (P_0={S=0}) 위 first return을 완전히 뜯어낸 것이다.
color (3)에 대해 상대좌표를
[
(q,w,v,u)=(x_4,x_0,x_1,x_2),\qquad x_3=-(q+w+v+u)
]
로 두면, first return 동안 layer (0,1,2,3)에서의 방향은 정확히 다음이다.

[
d_0=
\begin{cases}
2,& (q,w)=(0,0),\
1,& u=3\ \text{or}\ (u=0,\ q=1),\
3,& \text{otherwise},
\end{cases}
]

[
d_1=
\begin{cases}
4,& (w,u)=(1,0),\
2,& w=4,\ q=3,\
1,& w=4,\ q\neq 3,\
3,& \text{otherwise},
\end{cases}
]

[
d_2=
\begin{cases}
2,& (w=0,\ q=4)\ \text{or}\ (w=2,\ q\neq 4),\
1,& (w=1,u=0,q=3)\ \text{or}\ (q=4,\ w\neq 0,\ \neg(w=1,u=0)),\
3,& \text{otherwise},
\end{cases}
]

[
d_3=0.
]

따라서 (R_3=f_3^m|*{P_0}) 는
[
R_3(q,w,v,u)=\bigl(q+\mathbf 1*{(w,u)=(1,0)},\ w+1,\ v+\beta(q,w,u),\ u+\gamma(q,w)\bigr)
]
꼴의 **skew product** 가 된다. 여기서
[
\gamma(q,w)=1
\iff
\bigl(w=0,\ q\in{0,4}\bigr)\ \lor\ \bigl(w=2,\ q\neq 4\bigr)\ \lor\ \bigl(w=4,\ q=3\bigr).
]

이제 (v)를 떼고 base map
[
B(q,w,u)=\bigl(q+\mathbf 1_{(w,u)=(1,0)},\ w+1,\ u+\gamma(q,w)\bigr)
]
를 보면, (w)가 절대시계처럼 항상 (+1) 된다.
그래서 section (w=0) 위의
[
U:=B^m|_{{w=0}}
]
만 보면 된다.

여기서 아주 깔끔한 2D 행(row) 동역학이 나온다.

* (q=0) 행에서는 (u\mapsto u+2), 단 (u=m-1)에서 ((1,1))로 점프
* (q=1) 행에서는 (u\mapsto u+1), 단 (u=0)에서 ((2,1))
* (q=2) 행에서는 (u\mapsto u+1), 단 (u=0)에서 ((3,2))
* (q=3) 행에서는 (u\mapsto u+2), 단 (u=0)에서 ((4,0))
* (q=4) 행에서는 (u\mapsto u+1), 단 (u=m-1)에서 ((5 \bmod m,1))
* (q=5,\dots,m-1) 행에서는 (u\mapsto u+1), 단 (u=0)에서 다음 행의 ((q+1 \bmod m,1))

홀수 (m)에서는 (+2)가 unit이므로, 이 (U)의 궤도는

* row 0의 짝수 residue들,
* row 1, row 2 전체,
* row 3의 전 nonzero residue,
* row 4부터 row (m-1)까지 전체,
* 마지막으로 row 0의 홀수 residue들

을 정확히 한 번씩 훑고 시작점으로 돌아온다. 따라서
[
U \text{ 는 } m^2\text{-cycle},\quad
B \text{ 는 } m^3\text{-cycle}.
]

마지막 lift는 (v)-cocycle이다.
(\beta)의 전체 합은
[
\sum \beta
==========

# #{d_0=1}+#{d_1=1}+#{d_2=1}

(m^2+m-1)+m(m-1)+m(m-1)
\equiv -1 \pmod m.
]
즉 base 한 바퀴를 돌 때 (v)가 unit만큼 이동한다. 그래서 standard skew-product lifting으로
[
R_3 \text{ 는 } m^4\text{-cycle},
]
그리고 (S)가 절대시계이므로
[
f_3 \text{ 는 전체 } m^5 \text{ 꼭짓점 위의 Hamilton cycle}.
]

계산 검증도 붙였다.

* (m=5,7,9,11,13) 에서 위 layer 공식이 witness와 정확히 일치
* 같은 (m)들에서 (U)는 (m^2)-cycle
* (B)는 (m^3)-cycle
* (R_3)는 (m^4)-cycle
* (\sum \beta \equiv m-1)

정리하면 현재 상태는 이렇다.

* **[P]** affine-pinned route가 맞다는 수준을 넘어서, **odd (m\ge 5)에서 한 색은 완전히 닫혔다.**
* **[C]** 나머지 색들 중 color 2는 (m=5,7)에서는 같이 Hamilton이지만 (m=9)에서 깨진다.
* **[O]** 전체 5색 decomposition은 아직 남아 있다.
* **[H]** 다음 작업은 이 color-3 skeleton을 보존하면서 color (0,1,4)를 고치는 affine-pinned repair를 찾는 것이다.

업데이트한 자료는 여기 있다.

* [progress note v5](sandbox:/mnt/data/d5_progress_note_v5.md)
* [검증 스크립트](sandbox:/mnt/data/d5_color3_partial_theorem_check.py)
* [검증 요약 JSON](sandbox:/mnt/data/d5_color3_partial_theorem_summary.json)
* [기존 26-move witness](sandbox:/mnt/data/d5_m5_kempe_witness_26.json)

다음은 **color 0/1/4의 first-return을 같은 방식으로 해체해서, 어디서 exact obstruction이 생기는지 분해**하겠다.
