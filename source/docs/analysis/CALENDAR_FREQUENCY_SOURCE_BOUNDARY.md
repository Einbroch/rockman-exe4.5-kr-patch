# 빈도 선택기 조사 — 미번역 유지

이 문서는 calendar_types_v2/date_v1 시점의 조사 기록이다.
후속 calendar_frequency_v1에서 실제 그래픽 저장/로더/VRAM/선택 경계를 확인하여5문구를 번역했다.
`CALENDAR_FREQUENCY_ROM_HANDOFF.md`와 `calendar_frequency_v1/frequency_runtime.json` 참조.
아래0read 관찰을 ‘문자열의 전게임 미사용’으로 확대하지 않는다.119..123 자체는 당시 계속 원본이었다.

## 2026-10-08 후속: 일반 대사의 동적 반복 주기

`gutsman_calendar_schedule_delete_v1` 정상 일정 삭제50 첫페이지에서는119를 실제로 읽는다.
`poc/runtime/calendar-frequency-source-20261008-r3/`는 같은ROM/정상parent checkpoint에서
RAM/ROM/register를 쓰지 않고 lookup→E5 copy→32byte native transfer→문자 draw를 관측했다.
6368E8 relocated root08800000, id119, 원문0880088D의6bytes `02e49db3bae5`가
02014E54 staging에 복사되고, 원본 descriptor080528E8의source02014E54/length32에 따라
native memcpy0800094C/LR08051805로02010C40에32bytes 전송된다. 일반대사font 경로가 이를 소비한다.
빈도선택기의 그래픽 경로와 이 일반 대사의119..123 문자열은 별도 consumer다.

후속 `calendar_frequency_names_v1`은119..123을 `1회만/매일/매주/매월/매년`으로 번역했다.
새ROM SHA256 `9a635be2e6f26ff835bdafd742a2042143183c337e04dc1d5d77884a18bae06b`.
각9~10bytes/E5 포함,32byte capacity 내. 이전7개선택문구와243미선택script span은 보존했다.
현재 런타임 검증 상태는 `CALENDAR_FREQUENCY_NAMES_ROM_HANDOFF.md`를 따른다.

실패기록: 기존 `calendar-frequency-source-v1` 폴더 재사용은 거부돼 증거를 덮어쓰지 않았다.
20261008-r1은 Lua local declaration 순서 오류로 dumpFrequency=nil,0/2캡처였으므로 PASS가 아니다.
r2에서선언순서를수정했고 r3에lookup/stage/transfer를 추가했다. 관측기에는 expected capture수 검사도 추가했다.
이 도구수정은 ROM/게임상태/허용오차 변경이 아니다. 아래는 이전 시점의 기록 그대로다.

2026-10-04. development-draft; NON-DISTRIBUTION; release_eligible=false.

고정 source 개발 ROM: `exe45_ko_development_calendar_types_v2.gba`.
SHA256 `903858514f23de53ce5ce5def2c07527ff3461d216e3fa6a06d47ef92eb6e883`.
기존v1과 전체ROM 바이트 동일성이 확인됐으므로 같은 SHA의 own normal checkpoint로 관찰했다.

원본6368E8 script119..123은 `1回のみ / 毎日 / 毎週 / 毎月 / 毎年`이다.
`capture_calendar_frequency.py`는 원본/relocated script spans를 계산해 각각 read callback으로 관찰하고,
기존 fixed-cell parser/copier callback과 RAM/VRAM/OAM/screenshot을 함께 수집한다.
CPU/ROM/RAM/register/read alias를 바꾸지 않는 read-only 도구다.

`calendar-frequency-source-v1`은 정상 calendar checkpoint에서 시간 확정/A와 right4회로
1회→매일→매주→매월→매년 표시를 관찰했다.9캡처 모두 완료, 관찰된 script119..123 read events는0이다.
이 구간 fixed-cell calls도0이다.
`calendar-frequency-source-v2`는 더 이른 own-roll-intro checkpoint에서 달력 진입→등록→시간→빈도까지
7개 정상 입력/캡처를 실행했다. 해당 빈도 문자열 read events0, fixed-cell call은 작업메뉴0의24셀만 관찰됐다.
전자는 너무 늦게 관찰을 시작해 선로드를 놓쳤을 가능성이 있어 후자의 경로도 확인했다.

이 결과만으로 전체게임에서119..123이 안 쓰인다거나 그래픽의 정확한 저장 위치/loader를 확정하지 않는다.
해당 source read callback이 빈도 화면의 실제 소비자를 포괄한다고 아직 증명하지 못했으므로,
‘빈도 메뉴는 이 script를 번역하면 된다’는 가설은 채택하지 않았다.
화면의 VRAM 타일→원본 asset/loader 경계를 후속 조사해야 한다.
문자열119..123과 빈도 그래픽/선택/등록 자료는 이번 ROM에서도 원본을 유지한다.

원래 목표의 미번역 빈도 표시는 계속 열린 과제이며, 다른 대사 번역/테스트 통과로 닫지 않는다.
이번 독립 번역은 일반 대사65F11C의 날짜 intro0 3리터럴이다.
