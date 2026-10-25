# 거츠맨 일정 확인·달력 홈 ROM 인수인계

날짜: 2026-10-07

후속 누적판(2026-10-08): `GUTSMAN_CALENDAR_ANNIVERSARY_CONFIRMATION_ROM_HANDOFF.md`. 이 문서의 home ROM과 검증 기록은 이전 기준선으로 보존한다. 최신 개발 ROM은 후속 문서 참조.

## 최신 개발 ROM

- 파일: `poc/output/exe45_ko_development_gutsman_calendar_home_v1.gba`
- SHA-256: `dba4a8792f15225df552dcd61b9a7fddcb8d1e5c800aae818b93e08390d4dd9a`
- 원본 SHA-256: `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`
- 상태: `development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false`
- 누적 범위: 58개 선택 아카이브, 2,293개 선택 literal, 674개 원본 유지 아카이브

## 이번 반영

- `665698:24:0` → `이렇게 하면 되거스?\n\n`
- `665698:24:1` → `예  ` — 원문의 가로 선택지용 후행 공백 2개 유지
- `665698:24:2` → `아니오`
- `665698:0:0` → `오늘은 `
- `665698:0:1` → `월`
- `665698:0:2` → `일이거스\n뭘 할 거스?`
- script0의 현재 월/일 buffer 호출, 두 자리 왼쪽 padding, script24의 option/select/B/clear/target 제어와 모든 비선택 span을 보존했다.

## 검증 결과

- 정상 조작 경로로 거츠맨 선택 → 달력 → 1월 1일 → 식사 → 확인창까지 도달했다.
- 기본 `예` 커서 `(85,136)`, `아니오` 커서 `(121,136)`와 한글 선택지를 화면에서 확인했다.
- `아니오` 확정과 B 취소는 script22로 복귀하고 `02001310..132F` 기록을 변경하지 않았다.
- 기본 `예` 확정은 script0으로 복귀하고 식사 일정 기록 `03000001010602000002f9fcdd16f9fcac14e500000000000000000000000000`을 만들었다.
- 확정 직후 `오늘은 1월 1일이거스 / 뭘 할 거스?`가 동적 숫자와 함께 출력됐다.
- 글리프 CPU 공급, OBJ VRAM, 화면 픽셀, 잔상 제거, 거츠맨 초상과 창 경계, 누적 질문20~23 및 기존 넘버맨/거츠맨 회귀가 통과했다.
- 직전 확인 ROM 대비 컴파일 내용이 달라진 아카이브는 `665698` 하나이며 새로 선택된 script0 외 비선택 script는 동일하다.
- 42개 거츠맨 테스트, 3개 chip-name 테스트, 644개 Python AST 검사가 통과했다.
- main, `_repro`, `_current_repro_r1` 세 빌드가 모두 최신 SHA-256과 일치했고 최종 감사의 tool drift는 빈 목록이다.

## 증거

- 달력 홈: `analysis/gutsman_calendar_home_v1/calendar_home.png`
- 확인/분기 합성: `analysis/gutsman_calendar_home_v1/confirmation_choices.png`
- 런타임 판정: `analysis/gutsman_calendar_home_v1/runtime.json`
- 최종 동일성 감사: `analysis/gutsman_calendar_home_v1/final_identity_audit.json`
- 전체 인벤토리: `analysis/full_scope_gutsman_calendar_home_v1/`

## 남은 범위

이번 증거는 1월 1일 식사 preset과 기본 Yes, 대체 No/B 분기에 한정된다. 다른 날짜와 일정 종류, 직접 내용·사람 이름 입력, 충돌·덮어쓰기·삭제, 영구 저장 후 재로드, 기존 save 호환, 실제 RTC 알림과 C40 producer는 아직 검증하지 않았다. 미선택 일본어 literal은 27,755개이며 이미지·inline·fixed population도 전체 완료가 아니다.
