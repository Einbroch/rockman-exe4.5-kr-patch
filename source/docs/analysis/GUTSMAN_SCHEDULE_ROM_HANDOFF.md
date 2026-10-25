# 거츠맨 일정 안내 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_schedule_v1.gba`, SHA256 `b41a0a423c4fe07f2be59d1b30421fc87a4bff96b1fda3b6f51272601bec04ba`. 누적2,241선택 literal/54선택·678원본 유지 archive. 신규12항목=6번역 표현+6원문 유지 punctuation. 전체 요청 완료 아님.

## 원본·번역·정적 범위

666F38:265bytes/14slots/root038134=intro+36. Source payload SHA `2facebf606327d4cf9df68310b945d90285de9b168999aef17c3697dd5ff4464`; TPL SHA `2f11d47888bf9857742cf94aa049c347dea49595302b2ddafed1c8affb9a5c64`.
전체TPL 원문과 원본root038134=08666F38을 확인했다. 거츠맨 group의 upcoming1→2event loop→3, today10→11clock/event loop→12 또는10 no-event 문맥이다. 이전 rollout661754는 참고로만 사용했으며 대상 source11 hour/minutes/AMPM/name 명령 배열과 소비 경계를 확인해 non-growing clock suffix 모델의 적용을 등록했다.
자산 `translations/gutsman_schedule_ko.json`; 개별 작성 초안 직렬화 `tools/draft_gutsman_schedule.py`.1/3/10:0/10:1/11:2/12의6표현 번역,2:0/2:1/11:0/11:1/11:3/11:4의6quote/colon/space 원문 유지. 기존 거츠/거스 말투 후보 유지/인간 검토 대기. source IDs/원문/숫자/newline/모든 command·hour/minute pad 규칙·AMPM·event-name buffer/lookup/loop·keyWait/clear/waitHold 보존.14slot 중8nonliteral 보존. 넘버맨4649 승인 재사용 없음.
11:2 ‘ から\n’ 원문 첫행30px→‘부터\n’24px. 앞선 콜론·공백·AMPM 명령/뒤newline·event quotes를 보존하며 시간 prefix 수요를 늘리지 않는다. build-owned `non-growing-clock-suffix-v1` 모델은 적용 archive를661754/666F38로 명시 제한하고 source/translated skeleton·punctuation·행 경계와 실측advance 비증가를 검사한다. 기존 Roll default key 및 테스트 유지. 아직 Guts 동적 time/event population 실행 증거는 아니다.
11의 scalar colon/space는 단순 byte 문자열 찾기 대신 원본 printBuffer→callBufferEventMinutes/AMPM consumer anchor로 유일하게 구분한다. source·compiled 양쪽 anchor1회와 source-identical punctuation 요구, 다른0byte 명령값을 글자로 오인하지 않는다. 새 픽셀 예외/게임 코드 변경 없음.
160관련 tests PASS, 기존 Roll clock runtime checker 회귀도 통과. 전체12literal/47glyph의 source·제어·숫자·glyph 공급·geometry·roundtrip 검사 PASS,8nonliteral slots 보존. 최대103px는10:1 ‘아무것도 없거스!’이다. immutable original에서 기존 competition 누적 flags+`--gutsman-schedule`으로 빌드하며 patched ROM을 입력으로 쓰지 않는다. main/repro/current_repro 동일 SHA, 대기·종료 snapshot 구분을 위해 checker에 명시exit_step 인자(기존 기본end+1 유지)를 추가한 뒤 최종current_repro_r2/감사 실행 중이다. 원본·과거 ROM·실험·실패·테스트 saves 보존.

## 실행 검증 상태

정상 native L 오늘 일정10의 no-event2페이지와 PET복귀 `tools/run_gutsman_schedule.py`/`tools/report_gutsman_schedule.py` PASS. 자체 freshFF저장/cold 이어하기/넘버맨3페이지·거츠맨 첫 인사2페이지·PET8장면22항목/29focus·No수락·B취소 회귀 PASS. 실제 ROM의 정상 입력만 사용하고 `tools/capture_gutsman_schedule.py`는 읽기 observer로만 동작, ROM/RAM 쓰기·read alias·RTC 강제 변경 없음. 다른 후보 save/state 수입 없음.
today step2의10:0/12glyph와 step4의10:1/9glyph가 native script10/root08809008을 통해 소비됐다. strict CPU font read/ROM glyph→OBJ VRAM→화면 픽셀·clearing·native arrow와 footprint 분리·오른쪽 border·page 순서 PASS. 빈 영역3,955/4,363pixel 확인. step3/5는 같은 대기 상태를 추가 기록했고 step6이 A후 종료 snapshot, step7은PET08807EF0/script1 복귀다. 명시 exit_step=6은 실제 exit snapshot을 선택하며 calls/draws 동일 및 target pool 종료를 요구한다. 기존 함수 기본end+1과 검사 조건은 유지했다. 메인 에이전트가 두 일정페이지 composite/PET composite/복귀 화면을 직접 확인했다. 결과 `analysis/gutsman_schedule_v1/runtime.json`, 화면 `normal_today_no_events.png`; 회귀 `pet_regression/runtime.json`/`normal_pet_prompts.png`. 전환 중 모든 프레임·음성·하드웨어 검증 아님.
자체 FF64KiB에서 native save success58, 생성save SHA `046446bad3e5069b17009058279c2a291af9a683effb0d9da149c8444e6cc970`, 직후snapshot/현재디스크 일치, 다른 테스트 saves 보존. 이전 후보와 같은 SHA여도 이번 자체 FF시작·입력 receipt로 생성, 수입한save 아님. 넘버맨 save/cold continue 회귀이며 한글 이름 persistence/거츠맨 save 증거 아님.
기존53archive payload·선택 자산/그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 수정 유지. native roots 거츠맨intro038110→08807E1C/PET038114→08807EF0/schedule038134→08809008, 넘버맨seasonal0382AC→0880DE14, 포르테seasonal03857C→088159A0. 각각 자기 pool, 이전 초상 진단 alias는ROM에 없음.
main/repro/최종current_repro_r2 동일 SHA, 현재593Python tools drift=[]/원본 SHA 보존 PASS. 마지막 감사 `analysis/gutsman_schedule_v1/final_identity_audit.json`.160관련 tests 재실행 PASS.
upcoming1→2→3와11등록 시각·AMPM·동적 이름·다중일정→12는 별도 미검증이다. 원문 event name/AMPM 공급 전체와 한글 이름 persistence를 고정문구 검증으로 대체하지 않는다.

## 미해결

최신 inventory `analysis/full_scope_gutsman_schedule_v1/`: 선택2,241/미선택 일본어 포함27,807/기타1,859. Catalogue 전체732archives/31,907canonical literals는 전체ROM 번역 분모가 아니다.
다음 거츠맨 알림66651C는 PET(0..6)와 mugshot(20..26)의 두 consumer 및 dynamic event-name/nickname/flag3658 분기다. 전체28slotTPL 원문 읽음, 아직 등록/새 번역 입력 미작성. 별도 renderer의capacity/변수경계를 확인하고 전체 literal population을 정한 뒤 진행한다. 단일132px 모델로 두 renderer를 통합하지 않는다.
한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환이 가장 어려운 미해결 조건이다. 전체graphics/inline/fixed population, 미실행 날짜/성별/이벤트·재질문·중단, 이전 native wait-arrow53pixel 차이도 미해결. 전체 완료·배포 선언 없음.
