# 달력 날짜 안내3리터럴 추가

2026-10-04. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

ROM `poc/output/exe45_ko_development_calendar_date_v1.gba`.
SHA256 `afc8a779872ad6e81db8a6b29f96af9423540ed14062e2940953afebd78bf7c1`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
누적1,090선택 텍스트단위 / 기존9그래픽 /21선택·711미선택 archive. 전체 완역률은 아니다.

## 조사·번역 경계

미번역 빈도 선택기를 먼저 조사했다. `CALENDAR_FREQUENCY_SOURCE_BOUNDARY.md`에
독립 정상2경로의 source/relocated119..123 관찰과0read events, 해당 소비 경로 미확정을 기록했다.
원문의 빈도 이름을 번역해 해당 화면이 바뀔 것이라고 가정하지 않고 그대로 유지했다.
이 조사는 빈도 한글화 완료나 그래픽 저장 위치 확정이 아니다.

대신 실제 달력 진입에서 보이는65F11C script0의3리터럴을 수동 번역했다:
`今日は `→`오늘은 `, `月`→`월`, `日!!\nなにをしよっか?`→`일!!\n무엇을 할까?`.
`translations/roll_calendar_date_ko.json`은 기존11초안의 모든 필드를 유지하며 `date-content-v1` variant를 선택한다.
원본 월/일 callBufferCurrentMonth/Day, printBuffer 인수·순서·제어·끝공백·줄바꿈은 보존한다.
날짜 숫자·입력·이름·저장 자료를 수정하지 않았다. 새 hook/그래픽 수정은 없다.
255슬롯 중8스크립트·14리터럴 선택,247미선택 스크립트 바이트 보존 및 폰트/왕복 검사 통과.

## 정상 실행·픽셀 증거

새 ROM own-cold/date/profile/Roll선택/intro/PET→calendar/time/meal/list/promise/types-scroll을 실행했다.
같은 ROM의 own-roll-intro에서 추가 date 및 date-font2를 정상 패드로 진행했다.
이전 다른SHA의 checkpoint, read alias, CPU/ROM/RAM/register 수정은 사용하지 않았다.

처음 date 보고서는 월/일이 같은 버퍼일 것이라는 가정을 거부했다.
실제 CPU glyph 관찰은 month02010AC0/1, day02010B40/1이며 각각 [공백,1,E5]이다.
정확한 별도 버퍼/종료자·날짜 glyph offset 계약으로 수정했다. 그 실패 캡처/ROM은 보존한다.
이후 픽셀 보고서는 색 관찰값 누락을 거부했고, 관찰기에 context+0x9c read만 추가했다.
기존 캡처를 편집하지 않고 fresh `calendar-date-v1-date-font2`로 같은 정상 진입을 재실행했다.

`date_runtime.json`은 script0/root/3리터럴과4native숫자·공백draws를 확인한다.
원본 숫자 font→CPU read→native RAM→한글/숫자 배치→OBJ VRAM/화면 픽셀, 빈 영역 무잔상 검사 통과.
step2/3 두 화면을 직접 시각 검토했다. 정상1월1일만 확인했으며12월31일·날짜 rollover·RTC 정확성을 주장하지 않는다.
사진 `poc/runtime/calendar-date-v1-date-font2/step_002.png`.

새 날짜1 + 종류목록1 + 등록안내1 + 달력메뉴1 + 소개/PET/기본대사/장비4 + 등록시각조회1 = 집중9정상보고서 통과.
등록안내 보고서가 표시하는 normal11단위와 날짜 보고서의 새3단위를 분리해14선택리터럴을 확인했다.
새 alias 진단은 없다. 합성 CPU 회귀는 실제 해당퀘스트 플레이로 합산하지 않는다.
종류 스크롤 arrow의 source/current screenshot RGB 동일성 미확정은 이전 경계대로 유지한다.

## 보존·재현

직전 types-v2 ROM의65F11C 제외20archive payload는 직접 바이트 대조 동일.
기존 종류/달력메뉴6368E8과9그래픽,기존11calendar wordings/controls 보호 검사가 통과했다.
관련44테스트 /11.910초 /OK. 역사적 캡처 테스트는 해당 과거 ROM 근거로만 취급하며 전체suite는 재실행하지 않았다.
최종 main/_repro/_current_repro2 독립3ROM SHA 동일,현재Python414도구 drift=[],원본 SHA 불변 확인.
정본 `analysis/calendar_date_v1/final_identity_audit.json`; 관찰기 보완 전 `_current_repro`도 보존한다.
누적 옵션의 `--roll-calendar-content` 대신 `--roll-calendar-date`, `--calendar-types`는 유지한다.

## 열린 완료 조건

빈도 선택기·원본 기본이름ごはん/じゅく·다른달력 대사/월요일 등 UI는 아직 미번역이다.
기본 이름→입력편집→확정자료→여러소비자→저장/재로드 연결은 가장 중요한 열린 과제다.
한글 입력/영구저장/재로드,RTC 자연알림,다중이벤트,전체게임,오디오/하드웨어,인간 검토/배포 미완료.
