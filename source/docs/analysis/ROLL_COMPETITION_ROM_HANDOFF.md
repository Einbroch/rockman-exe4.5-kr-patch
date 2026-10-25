# 롤 대회 결과·참가 안내 미번역 후속 작업

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 완역·배포 승인 아님.
한글패치 스킬에 따라 원문·제어 명령·닉네임 삽입·소비자와 격리 진단 증거를 구분했다.

## 현재 ROM

`poc/output/exe45_ko_development_roll_competition_v2.gba`
SHA256 `9d99325c9cd23536a8914b63d6a9cf8d1af379c9f3eec1ec9c61114a23814b35`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 유지.
1,065 선택 단위 / 기존 9그래픽. 17선택 / 715미선택 아카이브.
전체 게임의 미번역 분모 또는 완료율이 아니다.

소스 6615A8: 426바이트, 25스크립트 슬롯, 포인터 0x380F0.
SHA256 `65e0ba4d9dac0144755f1c5d8d9520df333533eeaf7552576b4d8dd68edea4b6`.
전체 원문 `analysis/tpl_baseline/6615A8.tpl` 확인.
선택 스크립트 1,2,10,20,21,22,23의 14리터럴을 직접 수동 초안 작성.
패배·재도전 격려 / 우승 축하 / 참가 등록 누락 / 대회 직전 응원이다.
닉네임 뒤의 첫 행 구두점과 줄바꿈을 보존해 한국어 조사 의존을 추가하지 않았다.
새 고유명사·선택지 없음. 기존 친근한 롤→플레이어 반말 초안 유지, 승인으로 승격하지 않았다.
`callCancelMenuTransition`, `flagClear3603`, nickname, keyWait, clearMsg, waitHold 전부 보존.
18 미선택 슬롯은 원문에서 모두 빈 슬롯이다. 빈 슬롯을 미번역 대사로 집계하지 않는다.

최종 compiled payload 666바이트, offset 0x8030BC.
SHA256 `ab0c1670514cf6dbe5204ac7326daf30bbb38c558c444aee3ab4b519c337651c`.
소스/native 재빌드, 의미·바이너리 round-trip, 보호 명령, 폰트 공급 검증 통과.
최대 정적 본문 폭 119px / 채택 범위 132px. 닉네임 ああくん44px+구두점11px=55px.
20..23은 첫 행103px, 다음 행 닉네임55px, 마지막 행58px.
이전 16개 선택 아카이브의 실제 compiled payload를 직전 ROM과 전체 바이트 대조해 동일함을 확인.
재배치로 포인터·폰트·hook 주소가 이동하므로 whole-ROM 동일 비교로 오인하지 않았다.
기존 칩 이름 hook은 새 Roll13 명령 위치에서 재구성, 32합성 CPU fallback/레지스터/CPSR 벡터 통과.
이번 ROM에서 새 칩 획득·퀘스트 정상 분기나 모든 이름 소비자 검증을 주장하지 않는다.

## 화면 증거

원문 source 진단: `poc/runtime/roll-competition-source-v1-script1`.
직전 7bfe… ROM의 own 정상 roll-intro 부모에서 격리 실행. 일본어 패배·격려 화면 확인.
새 binary의 정상 입력 체인:
`poc/runtime/roll-competition-v1-roll-cold-part1` → date → profile → navi-menu → select-roll → intro → equipment.
seed → prompts 및 intro → talk는 별도 정상 자식 경로.
기존 소개·PET 선택/취소/복귀·기본 대사·공격력/장비 안내의 정상 보고서 통과.
`greeting_regression/runtime.json`, `pet_regression/runtime.json`, `talk_runtime.json`,
`roll_caption/runtime.json` 및 그 guides_regression은 모두 새 ROM SHA에 결합.

대회 진단: `poc/runtime/roll-competition-v1-script{1,2,10,20,21,22,23}`.
모든 부모는 새 binary의 own 정상 intro. 다른 ROM의 상태를 가져오지 않았다.
PC0x08037F20의 0x0803810C 원본 포인터 읽기 한 번을 해당 대회 pool로 대체,
PC0x0804FB76의 native script0 table 읽기 한 번을 해당 엔트리로 대체했다.
ROM 파일/RAM/레지스터 직접 쓰기 없음. 실제 게임 제어 명령은 해당 진단 안에서 실행된다.
결과 receipt는 normal_play_checkpoint_eligible=false, 상태는 diagnostic_checkpoint.mss로 격리.
이 경로는 실제 대회 참가·승패 판정·flag 분기 선택의 정상 진행 증거가 아니다.

`competition_runtime.json`: 7경로 / 10페이지 / 14개 선택 리터럴 전부 소비 확인.
닉네임 RAM 9B9BA2CA E5, 원본 글꼴/폭/위치, 한글 stream/index/행·폭,
글꼴 CPU 읽기→OBJ VRAM→실제 화면 픽셀, keyWait 위치, 빈 본문 무잔상 검증 통과.
`competition_pages.png`의 전체10페이지를 직접 시각 검토했다.
정상 대회 진행, 다른 닉네임의 전체 집합, 한글 이름 입력, 저장, RTC 지속성,
실제 오디오, 하드웨어, 전체게임, 독립 문구 승인·배포 검증은 남아 있다.

## 재현성 / 보존

최종 v2 / v2_repro / v2_current_repro 세 빌드 SHA 동일.
`python -X utf8 -m unittest discover -s tools -p 'test_*.py'`:
207테스트 / 518.258초 / OK, exit0. `final_test_summary.txt`에 실행 결과를 기록했다.
기존 캡처를 재검사하는 테스트는 그 원래 ROM의 증거이며 이번 ROM에서 새 실행한 것으로 간주하지 않는다.
이번 ROM에 직접 결합된 집중 검증은 정상4보고서+대회진단1보고서로 `focused_runtime.json`에 기록했다.
`final_identity_audit.json`: 원본 SHA 동일 / Python380개 도구 해시 drift=[] 통과.
v1 및 그 독립 빌드, 모든 원문·이전 ROM·캡처·상태를 보존했다.
v2는 설명의 잘못된 root-index 표기를 제거하고 최신 도구 해시를 결합한 최종 metadata다.
문구/ROM 바이트는 v1과 동일한 SHA이므로 새 binary의 v1-prefix 런타임 캡처를 v2에 결합할 수 있다.
이 사실은 다른 SHA ROM의 과거 런타임 증거 전이를 허용하지 않는다.

재빌드 선택은 기존 최신 옵션에 `--roll-competition`을 추가한다:
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout
--roll-subjects --roll-pet-chipquest --roll-mail-alert --roll-dialogue-chip-name --roll-competition`.
항상 fresh work/out 경로를 사용한다. 캡처 재실행은 fresh PREFIX로 분리한다.
관련 도구: capture_roll_competition.py / run_roll_competition.py / report_roll_competition.py.

## 다음 범위

661754 전체 원문은 읽었다. 일정명을 printScheduleBuffer로 동적 삽입하고,
시각/AMPM/등록 일정 조회 루프를 사용하므로 일정명·AMPM의 원본 소비자/RAM 경계를 먼저 확인한다.
아직 해당 아카이브를 번역·선택·ROM에 포함하지 않았다.
661858의 다른 개인 질문과 한글 입력, 기존 다른 동적 칩 이름·정상 이벤트 분기도 별도 미완료다.
