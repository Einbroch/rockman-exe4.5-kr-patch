# 롤 일정 알림의 독립 안내 대사 5개

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 완역·배포 승인 아님.
한글패치 스킬에 따라 동적 일정명·시각 삽입과 독립 안내문을 분리해 후자를 먼저 작업했다.

## 현재 빌드

`poc/output/exe45_ko_development_roll_schedule_v1.gba`
SHA256 `c1838a5e877e6a726733a8e9797cc9487fa065312627b9131650c9df80c112ed`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 보존.
누적 1,070 선택 단위 / 기존 9그래픽, 18선택 / 714미선택 아카이브.
전체 게임의 미번역 분모나 완료율이 아니다.

661754 소스는260바이트 / 14스크립트 슬롯 / 포인터0x380F8.
소스 SHA256 `5bafb1c9666c968c595f3f41f48cc5787afced8ea224335658fe97dd6318f33c`.
전체 원문12리터럴을 읽고, 스크립트1/3/10/12의5리터럴을 직접 수동 초안 작성.
`그러고 보니 곧`, `할 시간이네!`, `오늘 등록된 / 일정은・・・`,
`아무것도 없어`, `이런 일정이 있어!`.
마지막 대사는 앞선 오늘의 일정 목록을 맺는 표현이다. 원문 흐름과 친근한 롤 말투에 맞춘 개발 초안이며 승인으로 승격하지 않았다.
선택된 페이지에는 동적 삽입 문자가 없다.
callBufferReminders, callFindSoonEvent, callFindTodayEvent 분기·인수,
keyWait/clearMsg/waitHold와 모든 창 제어 명령을 보존했다.
미선택10슬롯과7리터럴 보존, 특히 script2와11의 이벤트명·시각 삽입 전체 바이트는 그대로다.
7미선택 리터럴에는 따옴표·구두점도 있으므로 이를7개 미번역 문장으로 집계하지 않는다.

compiled payload353바이트 / offset0x803358,
SHA256 `6610d979cb9ba0f2ad67a9c2cb8c05e3d2f6771cf9ff96b9b39d228033ff6da3`.
원문/native 재빌드, 의미·바이너리 round-trip, 보호 명령, 한글 공급, 채택132px 폭 검사 통과.
정적 행 폭:88 /79 /68·69 /80 /111px. 최대111px.
이전17개 선택 archive payload는 실제 전체 바이트 대조로 동일함을 검사한다.
‘빅해머1’ 선택hook을 새 Roll13 명령 위치에서 재구성한다.

## 증거 및 구분

원문 격리 진단: `poc/runtime/roll-schedule-source-v1-script10`.
직전9d99… ROM의 own 정상 intro 부모. 원문 오늘 일정 소개→없음→복귀 화면을 확인했다.
새 ROM 정상 체인은 `poc/runtime/roll-schedule-v1-roll-` prefix의
cold-part1→date→profile→navi-menu→select-roll→intro→equipment,
별도 seed→prompts와 intro→talk 경로다. 다른 ROM 상태를 가져오지 않는다.

새 일정 진단: `poc/runtime/roll-schedule-v1-script{1,3,10,12}`.
PC0x08037F20 /0x0803810C 포인터읽기1회와 PC0x0804FB76 native0 table읽기1회만 alias.
ROM 파일/RAM/레지스터 직접 쓰기 없음. 게임의 원래 제어 명령은 실행된다.
각 결과는 normal_play_checkpoint_eligible=false, diagnostic_checkpoint.mss로 격리한다.
script1은 첫 keyWait에서 멈춰, 등록 이벤트 없이 script2를 호출하지 않는다.
script10은 원본 callFindTodayEvent의 ‘없음’ 분기만 관측 대상이다.
script3/12는 기존 창 제어를 통해 독립 종료 페이지를 표시한다.
실제 일정 등록·알림 발생·시각 분기·목록 루프 정상 진행 증거가 아니다.

완료된 화면/회귀 결과는 `analysis/roll_schedule_v1/`의 보고서에 결합한다.
`schedule_runtime.json`:5리터럴 /4진단경로 /5페이지 전부 stream·index·행 폭·context·keyWait/clearMsg 경계 검증 통과.
ROM 글꼴→CPU읽기→OBJ VRAM→화면 픽셀 대조와 빈 본문 무잔상 검사 통과.
script10 두 화면의 없음 분기 및3/10/12 확인키 후 종료 검사 통과.
`schedule_pages.png` 전체5페이지를 직접 시각 검토했다.
`greeting_regression/runtime.json`, `pet_regression/runtime.json`, `talk_runtime.json`,
`roll_caption/runtime.json`의 정상4보고서와 일정진단1보고서가 `focused_runtime.json`에 결합된다.
이전17개 번역 payload 실제바이트 동일, 새 ROM name selector32합성 CPU 벡터 통과.
`final_test_summary.txt`: 기존18관련 테스트+신규3테스트를 포함한21테스트 /7.051초 /OK exit0.
앞서18테스트 실행은 같은 테스트의 예비 실행이며 중복 합산하지 않는다.
직전207개 전체 테스트는 이번 턴에 재실행하지 않았다.
과거 캡처를 재검사하는 테스트는 그 원래 ROM의 증거이며 새 ROM 실행으로 간주하지 않는다.
전체 게임, 한글 이름/일정 입력, 저장, RTC 지속성, 실제 오디오, 하드웨어,
모든 이벤트·동적 변수, 독립 문구 검토·승인과 배포 검증은 남아 있다.

## 재현성

main / _repro / _current_repro 세 독립 빌드 SHA 동일.
`final_identity_audit.json`: 원본 동일 / Python384도구 drift=[] 통과.
원본·이전 ROM·상태·캡처 모두 보존, fresh work/out 경로 사용.
누적 옵션에 `--roll-schedule`을 추가:
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout
--roll-subjects --roll-pet-chipquest --roll-mail-alert --roll-dialogue-chip-name
--roll-competition --roll-schedule`.
새 런타임 재실행 시 PREFIX도 fresh 값으로 변경한다.

## 다음 미완료 경계

source script2: FC032D00 → 「 → F90C43 → 」,
script11: FC032800/F9038201 → : → FC032900/F903C201 → space →
FC032B00/F90C43 → ` から\n` → FC032D00/「/F90C43/」.
TextPet 설명은 F90C43을 reminder-name buffer67,
FC032B를 AM/PM, FC032D를 event name 저장으로 지칭하지만 이는 타깃 runtime RAM/작성자 경계 확인을 대신하지 않는다.
다음에는 기존 정상 입력으로 등록된 이벤트를 만드는 경로부터 확인하고,
해당 버퍼 작성→RAM→원본 글꼴 소비와 길이·시각·분기 경계를 연결한다.
현재 ` から\n` 및 삽입되는 원문 일정명 등은 미번역/미검증으로 남는다.
