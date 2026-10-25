# 거츠맨 저장 문구 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 결과와 범위

`poc/output/exe45_ko_development_gutsman_save_poc_v1.gba`
SHA256 `35e9c751134d8016f1e81144a996632a060f06cf01dad97211c9b7773161d08b`.
추가16개 / 누적1,129선택 텍스트 /15기존 그래픽 /21선택·711미선택 archive. 전체 완역률이 아니다.
6DA21C script0의 checkNaviAll jumpIfGutsMan=25에 연결되는 scripts25..29만 추가했다.
확인25, 덮어쓰기26, 저장 중·실패/재시도27, 완료28, 잘못 변경된 데이터29이다.
전원 경고와 실패/성공 구분, 재시도 선택, 원본 flags3651/7686, callSave 성공28·실패/invalid 분기를 유지했다.

`rockman_roll_gutsman_save_ko.json`의 첫37단위는 직전 save_surface asset과 필드 동일하다.
말끝 `でガス→거스`, `ガッツ→거츠`는 캐릭터 말투를 보존하려는 검토 대기 초안이며 공식 한국어 번역/인간 승인으로 주장하지 않는다.
예: `지금까지의 활약을 / 저장해 둘 거스?`, `저장 중이거스 / 전원을 끄면 / 안 된다, 거츠!!`.
실패를 성공으로 바꾸지 않고 invalid-data 설명도 유지한다. 모든 원본 줄 수/마지막 빈 줄/선택 공백을 보존한다.

## 화면 구조와 빌드 보호

거츠맨26은 세 줄 덮어쓰기 안내→keyWait→clearMsg→별도 선택 행이다.
롤21의 안내와 선택이 같은 페이지인 검증을 그대로 적용한 첫 빌드는 selection-row 검사에서 거부됐다.
문구나 control을 바꾸지 않고 `standalone_choice_rows`의 기존 검증을 적용했다(prefix24, literals1/2).
25/27/29의 prompt/selection group은 원본의 마지막 빈 행과 실제3행을 유지한다.
`rockman-roll-gutsman-save-v1`은53단위,20scripts,11prompt groups와1standalone row를 명시한다.
원본 archive9008bytes·100미선택slots, 직전115slots(25..29외), 다른20archive payload가 동일하다.
상단6333A4의256-byte `저장` 그래픽과 기존 개수·항목명 scripts10..16은 직전 ROM과 동일하다.
새 코드 hook/입력/저장 포맷 변경은 없다. 원본에서 누적 flags `--gutsman-save`로 생성한다.
`--save-surface` 없이 선택하면 거부한다. 최초 실패 work폴더와 모든 이전 ROM/캡처를 보존한다.

## 실제 새 ROM 실행

`gutsman-save-poc-v1-cold-part1 → date → profile → navi-menu → select-gutsman → intro → save-enter → save-commit → save-overwrite`.
최초 state_origin=null, 모든 checkpoint는 동일 새 ROM SHA다. 원본 input recipe만 재생하며 다른 ROM state/RAM/save import 없음.
Navi 선택의 정상 right 두 번으로 거츠맨을 선택했다. 일본어 일반 소개/PET 대사는 아직 미번역이다.
저장 진입은 정상 버튼 입력이며 script25와 실제 거츠맨 portrait를 확인한다.

`report_gutsman_save.py`의 실제 페이지 검사:

- save-enter step11: script25 확인·예/아니요3단위.
- save-overwrite step6: script26 세 줄 안내1단위.
- save-overwrite step9: clear 후 script26 예/아니요2단위.
- save-timing step8: script27 전원 경고1단위.
- save-commit step7: script28 완료1단위.

정상 관측8단위의 모든 translated stream, normal BDF glyph 및 CPU font read, OBJ VRAM, 실제 화면 ink/shadow/background mask와 위치를 검증했다.
`save_pages.png`, 전원 경고/완료, overwrite step11 ‘아니요’ 커서와 step12 PET 복귀 화면을 직접 검토했다.
기존 `저장/시간/칩/컵/크레딧/0개`도 실제 거츠맨 저장 화면에서 보인다. 모든 Navi 검증으로 일반화하지 않는다.

첫 save-commit step6은 font draws가23개 모두 기록됐지만 화면 전송/표시가 끝나기 전이어서 픽셀 검사가 실패했다.
동일 ROM/own-save-enter checkpoint에서 정상 입력 `save-timing`으로 프레임을 추가 관측했다.
steps3..5 stage/VRAM 갱신 중,6..7 화면 불일치,8..12 완성된3행의 glyph/VRAM/pixel mask 일치를 확인했다.
게임 코드나 waits를 바꾸지 않았으며, 실패 프레임도 보존했다. 이것은 표시 완료 시점의 증거이며 실기/오디오 타이밍 보증이 아니다.
timing 경로는 이미 만들어진 이 후보의 전용 테스트 파일에 정상 save를 다시 수행한다. 다른 테스트 save는 불변이다.

첫 native save:64KB allFF SHA `71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063`
→ `501f01fc59a8bc3012cc18d3856f761c7a3982b43f6f401db6ad018ecf40c80d`, native script28 완료.
이 첫 disk edge는 save-commit의 불변 receipt/파일 snapshot으로 검증한다. 후속 timing replay의 파일 상태와 혼동하지 않는다.
덮어쓰기 ‘아니요’는 당시 save hash 불변이다. 영구 재로드/이전 save 호환성은 이번 실행에서 검사하지 않았다.

## 재현 및 남은 작업

관련60unittest 통과(15.665초). historical fixtures는 이번 runtime 증거와 구분한다.
main/_repro/최종 _current_repro_r2의 동일성, 현재 도구와 원본 SHA는 `gutsman_save_poc_v1/final_identity_audit.json` 참조.
_current_repro도 같은 ROM이지만 최종 timing-report 수정 전 tool manifest이며 버리지 않는다.
report의 정적 normal-font 검사는53문구의 normal glyph 공급을 확인한다. fixed-cell labels 실제 공급 증거는 이전 별도 report와 이번 화면을 구분한다.

오류 관련8단위(27:1..4,29:0..3)는 구조·인코딩·글꼴·레이아웃 정적 검증만 완료, 실제 오류를 유발하지 않았다.
다른 Navi 저장/PET 일반 대사 등 미번역을 이어서 처리한다.
가장 큰 완료 위험은 한글 이름 입력/편집/저장·재표시 소비자 전체와 기존 save 호환성이다.
전체게임·RTC/alarm·실기·오디오·독립 의미 검토/인간 승인·배포는 미완료이며 완역/출시후보로 승격하지 않는다.
