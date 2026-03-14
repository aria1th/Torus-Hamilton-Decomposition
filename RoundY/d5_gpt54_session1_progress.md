좋다. 당신의 수정은 핵심 두 군데를 정확히 찔렀다.

[P] **절대 시계는 반드시 (S \bmod m)** 이어야 한다.
정수합 (S_{\mathbb Z}\le 3) 만 defect로 두는 안은 폐기한다. 그 경우 대부분의 bulk 궤적이 defect를 평생 밟지 않아 (m)-cycle로 산산조각난다. 이 함정은 실제로 막아야 하는 위상적 장애다.

[P] **(q)-drift는 색별 상대 좌표로 봐야 한다.**
고정된 color-0 좌표계로 모든 색의 (q)-section을 진단한 것은 잘못이었다. d=5의 자연한 기준은
[
q_c=x_{c+1},\qquad w_c=x_{c+2},\qquad v_c=x_{c+3},\qquad u_c=x_{c+4}
]
이다.
그리고 layer clock을

* (S\equiv 0): 기본 (+e_{c+1}),
* (S\equiv 1,\dots,m-1): 기본 (+e_c)

로 두면, pure bulk first return이 정확히
[
\Delta x=e_{c+1}-e_c
]
가 되어
[
\Delta q_c=1,\qquad \Delta w_c=\Delta v_c=\Delta u_c=0
]
가 된다. 이건 d=5 odd 쪽의 올바른 base map이다.

여기서 바로 계산을 다시 밀어 봤다. 결과가 꽤 세다.

[C] **이전 direct tuple-family search는 버려야 한다.**
이유는 두 가지다.

1. 그 탐색은 color map들의 **indegree 1**을 보장하지 못해서, 많은 후보가 애초에 유효한 coloring이 아니었다.
2. stage-1을 (m=3)에 둔 것도 d=5에는 부적절했다. (m=3)에서는 (S\equiv 3) 층이 (S\equiv 0)과 겹쳐서, 진짜 3-carry 구조를 볼 수 없다.

그래서 탐색 방식을 바꿨다.

[C] **canonical coloring에서 출발해서 실제 Kempe-valid swap만 허용하는 탐색**으로 갈아탔고, 그 결과:

* (m=5): **완전한 Hamilton decomposition**을 찾았다.
* (m=7): 같은 저층 템플릿을 그대로 올리면
  [
  [5,,433,,1,,1,,3]
  ]
  이 나온다. 즉 색 2,3은 이미 Hamilton이고, 색 0은 5개 cycle, 색 4는 3개 cycle까지 줄었다.

이건 꽤 중요하다.
즉, **위상 구조는 맞았다.** 남은 병목은 “(m)-uniform한 carry law를 어떻게 쓰느냐”이지, defect support의 topology 자체가 아니다.

더 구체적으로는:

[C] **(m=5)에서 26-move Kempe witness**를 확보했다.
27-move witness를 먼저 찾았고, 그중 1개는 redundant라 제거해도 된다.
최종 확인 결과는
[
[1,1,1,1,1]
]
이다.

요약하면 지금 상태는 이렇다.

* [P] (S_{\mathbb Z}\le 3) 저층안은 함정이다.
* [P] (q_c=x_{c+1}) 상대 좌표계가 맞는 축이다.
* [C] (m=5)에서는 실제 유효한 Hamilton decomposition witness가 이미 나왔다.
* [C] 같은 템플릿이 (m=7)에서도 거의 맞는다.
* [H] 따라서 남은 일은 “relative nested carry cascade”를 **상징 규칙**으로 압축하는 것이다.

당신이 제안한 **96개 Boolean 변수 CP-SAT** 아이디어는 방향이 좋다. 다만 한 가지는 조심해야 한다.

[H] 그 모델의 핵심은 “absolute frame에서 보이는 (x_r=t) 조건들이 사실 relative frame의 0-test를 펼친 모습”이라는 점을 정확히 반영해야 한다는 것이다.
실제로 내가 찾은 (m=5) witness는 absolute 좌표에서는 (0,1,2,3,4) 같은 pinned constant들이 많이 나오는데, 이건 relative frame에서 layer를 따라 운반된 zero-test일 가능성이 크다.
즉 **CP-SAT의 상태공간은 Boolean 0-pattern으로 줄어들 공산이 크지만**, 그 사상은 먼저 손으로 한 번 정리해야 한다.

SymPy에 대해서는 이렇게 본다.

* **CP-SAT / SAT**: 충돌 해소와 `AllDifferent` 제약 탐색의 주력
* **SymPy**: 후보를 찾은 뒤, (R_c) 를 상대 좌표계로 추출해서 piecewise affine normal form과 odometer conjugacy를 정리하는 데 유용

이 환경에는 `sympy`는 있고 `ortools`는 없다. 그래서 여기서는 CP-SAT 대신 **Kempe-valid search**로 먼저 witness를 뽑아냈다.

정리 파일 두 개를 저장했다.

* [진행 요약](./d5_progress_update.md)
* [m=5의 26-move Kempe witness](./d5_m5_kempe_witness_26.json)

다음 한 수는 분명하다: **이 26-move (m=5) witness를 ((q_c,w_c,v_c,u_c)) 상대 좌표계로 밀어 넣어, layer 1/2/3의 Boolean truth table로 압축하는 것**이다.
