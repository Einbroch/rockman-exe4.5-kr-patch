# 롤 식사·학원 알림 3문장 ROM 반영

2026-10-04. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

최신 ROM: `poc/output/exe45_ko_development_roll_schedule_alarm_v1.gba`
SHA256 `6e59764c4fc951eb0b1c3f07c739ed19b6e06fd99d228856f0c213f4ac01f634`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
직전 baseline: `exe45_ko_development_roll_schedule_time_v1.gba`, SHA35d20055….
누적1,074선택 텍스트단위 / 기존9그래픽 /19선택·713미선택 archive. 이 분모는 전체 완역률이 아니다.

## 이번 선택

`660D90` source717바이트, 28슬롯, root pointer `0x0380E8`.
소스 archive SHA256 `4d138a8dca3d82a9e40fb7a8855506a616fe86c691231e60eb7df521d14fbdd8`.
`translations/roll_schedule_alarm_ko.json` 수동 초안3개:

- 3:0: `ね~ぇ! / ゴハンの じかんだよ!` → `저기~! / 밥 먹을 시간이야!`
- 4:0: 학원에 갈 시각·빨리 준비하지 않으면 지각한다 → `학원 갈 시간이야 / 얼른 준비하지 않으면 / 지각하겠어!`
- 6:0: `えっと、それから・・・` → `음, 그리고・・・`

132px/3행 개발 경계, 실제 행 폭3:[46,111],4:[100,124,71],6:[101].
모든 window/position/flag/keyWait/clearMsg/waitHold, callCheckNowEvent 및 callFindNowEventType 명령 보존.
25미선택 슬롯 바이트 동일. 동적 이름과 다른 이벤트 대사1/2/5, 별도 mugshot23/24/26 소비자는 아직 미번역이다.
원문 재추출→바이너리/의미 round-trip, 한글 BDF/원본 문장부호 글꼴, 보호 명령, 최종 쓰기 계획 검증을 빌드와 정적 보고서가 통과했다.

## 검증과 범위

`roll-schedule-alarm-v1-roll-*`에서 새 ROM cold boot→날짜/프로필→롤 선택→소개/장비를 생성.
같은 ROM 정상 부모에서 seed→PET prompts→talk를 실행했다.
`normal_regressions.json`은 소개/PET/기본 대사/장비4정상 보고서다.
또 `...-calendar/time/meal/list` 정상 입력으로 AM2:00 1회 식사를 등록·L조회·목록·복귀했고,
`time_runtime.json`으로 RAM 시각/AM/원본 ごはん, ‘부터’82px 직후 배치·106px행·55px이름행, 픽셀/무잔상/keyWait/복귀를 새 ROM에서 재검증했다.
정상 보고서 합계5; 자연 발생 알림 검증과는 다르다.

신규 알림 `...-script3/script4/script6`는 같은 ROM 정상 intro에서 출발하되,
`capture_roll_schedule_alarm.py`의 1회 root/table **read alias**로 선택 소비자에 들어간 격리 진단이다.
ROM에는 alias가 저장되지 않는다. diagnostic_checkpoint.mss로 격리하고 정상 부모로 쓰지 않는다.
각 step2/3, 총6페이지가 font CPU읽기→ROM글꼴→OBJ VRAM→화면 픽셀, 정확한 행/폭,
본문 빈 영역 무잔상, 원문 keyWait/clearMsg 경계를 통과했다.
script6은 동적 이벤트 분기 전 keyWait에서 멈췄다. 알림 자연 발생이나 RTC/플래그 진행 증거가 아니다.
보고서 `alarm_runtime.json`; 비교 화면 `alarm_pages.png`. 세 화면과 정상 목록 화면을 직접 시각 검토했다.

이전18 archive 번역 payload byte-identical, 기존 PET 그래픽 동일, 기존9그래픽 재사용.
기존 빅해머1 이름 selector는 새 ROM에서32합성 CPU 벡터 통과; 실제 해당 퀘스트 진행을 재검증한 것은 아니다.
관련26자동 테스트 /35.483초 /OK. 과거 schedule/time runtime 테스트는 과거 ROM의 재검사이며 새 ROM 실행으로 합산하지 않는다.
초기 새 테스트의 Literal dataclass 접근 오류는 고쳐3개 통과했다. 전체 프로젝트 테스트는 재실행하지 않았다.

## 재현 및 다음 경계

최종 독립 ROM main / `_repro` / `_current_repro2` 해시 동일.
394 Python 도구를 최종 `_current_repro2` metadata에 대조, drift=[]; `final_identity_audit.json`.
앞선 `_current_repro`는 보고서 결합 코드 정리 전의 보존 빌드이며 현재 도구 pin은 `_current_repro2`를 사용한다.
원본·이전 ROM·조사·실패·성공 캡처 모두 보존. 원본 직접 덮어쓰기 없음.

빌드 옵션은 직전 누적 옵션에 `--roll-schedule-alarm` 추가:
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout
--roll-subjects --roll-pet-chipquest --roll-mail-alert --roll-dialogue-chip-name
--roll-competition --roll-schedule-time --roll-schedule-alarm`.
새 work/out/PREFIX를 사용한다.

가장 중요한 열린 조건은 기본 일정명/일정 메뉴의 입력·저장·여러 표시 소비자 연결이다.
`analysis/SCHEDULE_PRESET_SOURCE_BOUNDARY.md`에 원본 ROM 읽기→등록 임시 버퍼 및 조회 32바이트 전송을 기록했다.
기본 ごはん/じゅく를 한글로 바꾸지 않았으며 메뉴·확인·입력·확정 자료·재표시·저장/로드까지 검증해야 한다.
그 외 자연 시각 알림, 복수 이벤트, 별도 mugshot 소비자, 다른 Navi/전체게임, 오디오/하드웨어,
한글 입력·저장/재시작·RTC 지속성·인간 문구 검토·배포 승인 미완료.
