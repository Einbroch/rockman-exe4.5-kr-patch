# 롤 일정 등록 안내·선택지 9단위 추가

2026-10-04. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

ROM: `poc/output/exe45_ko_development_roll_calendar_dialogue_v1.gba`.
SHA256: `36dd3af596c01f5ce251c3527b3e8b475d0445a4c3a87a555d1c282fc61c576a`.
원본 SHA256: `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
누적 1,084 선택 텍스트단위 / 기존 9그래픽 / 21선택·711미선택 archive.
전체 완역률이 아니며 이번에 그래픽은 새로 수정하지 않았다.

## 번역·구조 보존

65F11C의 script 1/2/20/21/24, 9리터럴을 수동 번역했다.
날짜 선택 질문, 무엇을 등록할지와 일정/기념일 선택, 시작 시각 질문,
종류 질문, 최종 확인과 예/아니오를 포함한다.
`translations/roll_calendar_dialogue_ko.json`은 모두 검토 대기 초안이다.
원본 2,190바이트·255슬롯·root 0x0322E0를 검증하고 나머지 250슬롯은 바이트 보존했다.
날짜 삽입, 기본 일정명, 입력·저장 구조와 제어 명령은 바꾸지 않았다.
줄바꿈·끝 공백·분기 기본값·대상·wait 보존, 폰트 커버리지와 왕복 검사 통과.
최장 번역 행 111px. 이전 20번역 archive payload는 동일하다.

## 정상 실행 근거

`run_roll_calendar_dialogue.py`가 새 ROM에서 cold/date/profile/Roll 선택/intro/장비를 생성한 뒤
같은 ROM의 정상 패드 입력으로 calendar/time/meal/list를 진행했다.
이전 ROM checkpoint, read alias, ROM/RAM/register 수정은 사용하지 않았다.
read-only observer는 선택 archive 스트림·활성 script·root·CPU 글꼴 공급을 확인한다.

`calendar_dialogue_runtime.json`의 5화면·9단위는 정상 활성 script와 직접 대응한다:
calendar step4=1, step5=2, step6=20, time step5=21, meal step5=24.
한글 글꼴→타일/화면 픽셀·리터럴 내 글자 위치·빈 영역 무잔상 검사 통과.
선택 커서 sprite16/3은 기존 ROM 같은 화면의 OAM tuple과 동일하며 PET sprite0 계약은 유지한다.
`calendar_dialogue_pages.png` 5화면을 직접 시각 검토했다.

처음 보고서는 PET 전용 커서 가정을 거부해 중지했다. 이후 time step6의 실제 script22도 거부했다.
source OAM에 한정한 계약 및 실제 script21의 step5로 검증 표본만 수정했다.
ROM·번역·원본·캡처 변경으로 오류를 감추지 않았다.

새 안내 1 + 달력 메뉴 1 + 소개/PET/기본대사/장비 4 + 등록 일정 시각 조회 1 = 집중 7정상 보고서.
새 alias 진단은 없다. 빅해머1 selector32의 기존 합성 CPU 검사도 통과했으나 실제 퀘스트 실행 근거가 아니다.
AM2:00 일회 식사 등록의 기본 ‘예’ 진행과 같은 세션 조회를 확인했다.
‘아니오’ 선택/취소 독립 경로, 영구 저장·재로드·RTC 일관성의 검증은 아직 하지 않았다.

## 재현·남은 작업

관련 37테스트 최종 재실행 통과(15.052초). 과거 캡처 테스트는 해당 과거 ROM 근거로만 취급한다.
전체 프로젝트 테스트는 재실행하지 않았다.
최종 빌드·현재 도구 pin·원본 보존의 정본은 `roll_calendar_dialogue_v1/final_identity_audit.json`.
최종 비교 대상은 main / _repro / _current_repro2이며 이전 중간 빌드도 보존한다.
최종 3독립 ROM SHA256 동일, 현재 Python 402도구 drift=[], 원본 SHA256 불변 확인 통과.
누적 기존 옵션에 `--roll-calendar-dialogue`를 추가한다. 항상 새 work/out/PREFIX를 사용한다.

기본 ‘ごはん’/‘じゅく’, 빈도·종류 메뉴, 날짜 안내와 다른 달력 대사는 아직 일본어다.
기본 이름→입력→확정 자료→여러 소비자→저장/재로드 경계가 가장 중요한 열린 과제다.
한글 입력·자연 RTC 알림·다중 이벤트·전체 게임·실제 오디오/하드웨어·인간 승인·배포 검증 미완료.
