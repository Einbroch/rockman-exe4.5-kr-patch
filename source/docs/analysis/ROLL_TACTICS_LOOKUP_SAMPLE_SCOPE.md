# 롤 전술 질문 진단의 개입 경계

대상 BR4J 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
원본 TPL의 script6/7은 mmbn45s 두 행 질문이고 script8..11의 초상은 Roll이다. Native212C8 helper는 style*6+relative script를 반환한다. 이번 consumer는 다음과 같다.

```text
08020B48 push r4,r5,r6,r7,lr
08020B4A bl 080212C8
08020B52 r4=5
08020B54 r5=2
08020B56 r6=08619EF8
08020B5A bl 080554A4 (LR08020B5F)
080554A4 push lr
080554A6 r1*=2
080554A8 ldrh r1,[r0,r1]  // native script-table offset
080554AA r0+=r1          // actual parser stream
```

`capture_roll_tactics_samples.py`의 단일 read callback은 새 ROM76C944 base..base+3만 관측하며 execute PC554A8, r0=정확한 pool base, LR20B5F, r1=0/2일 때만 실제 컴파일된6/7 offset을 반환한다. 다른 소비자·스크립트 표·코드·ROM/RAM 데이터는 쓰지 않는다. 원본20B48..70,212C8..E8(root pointer는 제외),554A4..C4의 보호 코드 바이트도 새 ROM과 비교한다. scope/hash/alias call을 저장하고 checkpoint를 정상 플레이용에서 격리한다.

이것은 group6의 Roll 스타일을 선택하는 조건을 건너뛴 **진단**이다. native 록맨 초상과 플레이어/전투상태는 그대로다. 실제 롤을 선택한 화면/획득/진행 조건이나 롤 플레이 도주 결과를 증명하지 않는다. 정확한6/7 stream의 fixed-cell parser→provider→640-byte stage→VRAM06008A20→BG3→10셀/픽셀을 검사할 수 있다. 같은 문구인0/1의 정상 표시와 글자 모양이 같더라도 stream/offset/units ID로 별도 출처를 구분한다.
