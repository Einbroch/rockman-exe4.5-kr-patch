# 롤 전술 질문 2개 — 개발 문구 선택, 인간 승인 대기

| source unit | 일본어 원문 | 선택한 기존 문구 ID | 한국어 |
|---|---|---|---|
| 76C944:6:0 | どのてきを / ねらうの? | tactics.target | 어느 적을 / 노릴까? |
| 76C944:7:0 | あいてとの / まあいは? | tactics.distance | 적과의 / 거리는? |

/는 기존 줄바꿈. 현재5x2 mono 질문 소비자는 native20B48→212C8(group6)→554A4이고, 롤 질문6/7 다음의8..11에 Roll 초상이 명시된다. 첫 질문은 목표 적, 둘째 질문은 전투 중 상대와의 거리/간격을 묻는다. 시간 간격으로 옮기지 않는다. 일본어「の?」의 부드러운 질문을 기존 한국어 ‘노릴까?’로 표현해도 이 짧은 배틀 조작 질문의 의미/반말 톤을 유지한다는 개발 판단이다. 더 명시적인 ‘어느 적을 노릴까?’/‘상대와의 거리는?’는 의미 검토 대안이지만 현재 빌드는 기존 ID의 문구를 그대로 재사용한다.

원문은 고정된 TPL/원본 pool에서 가져온다. 새 `roll_tactics_wording_links.json`에는 문구를 복제하지 않고 stable unit→wording ID 선택 및 적용 근거를 기록했다. `prepare_roll_tactics.py`는 schema2로 이전14개 결과를 그대로 보존하고 새 두 source unit을 같은 두 wording ID에 연결한다. 신규16units에는14wordings이며 누적 단위 증가2는 새 문장2종을 만들었다는 뜻이 아니다.

원본 각 script raw bytes, pool/source SHA, TPL, 이전 asset·원 문구 asset·selection·serializer SHA는 파생 asset에 연결한다. 새 질문의 두 행, 명령 구조,5칸/행(40px),패딩 규칙은 유지한다. 전체 group0..11 중 dots12개는 그대로고 다른132script도 보호한다. 모든 wordings needs_review, release_eligible=false, NON-DISTRIBUTION.

실제 롤 선택 플레이 경로는 아직 없다. lookup-offset 진단은 록맨의 정상 전술 창0/1이 table을 읽을 때 새 ROM에 컴파일된6/7의 오프셋을 반환한다. native fixed-cell parser/폰트 provider/staging/upload/BG3를 그대로 쓰지만, 록맨 초상/플레이어는 바꾸지 않는다. 롤 초상 화면이나 정상 롤 경로로 주장하지 않는다. normal checkpoint는 진단 이후 격리한다.
