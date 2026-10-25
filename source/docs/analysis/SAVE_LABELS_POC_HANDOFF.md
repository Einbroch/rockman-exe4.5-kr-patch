# 저장 항목명 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 결과와 정확한 범위

`poc/output/exe45_ko_development_save_labels_poc_v1.gba`
SHA256 `08ead564156407b7d9c17e1579accf60a958b06410213607edfd68d8b038054e`.
추가4/누적1,112선택 텍스트 단위,14기존 그래픽 문구,21선택·711미선택 archive. 전체 완역률 아님.
`タイム→시간`, `チップ→칩`, `カップ→컵`, `クレジット→크레딧`.

지난번 그래픽으로 가정한 네 항목은 실제로 6DA21C scripts10..13의 mmbn45s 문자열이었다.
`save-labels-source-v1`은 직전 롤 저장 ROM의 own-intro에서 저장 로드를 다시 통과한 읽기전용 정상 입력 조사다.
첫 네 fixedcell calls가 relocated scripts10..13, source font08601738,6×8px/1행,384byte,targets06008400/8600/8800/8A00,caller080554BA로 연결된다.
상단 セーブ는 이 네 문자열과 별개다. 이 작업은 이미지4개 번역으로 집계하지 않는다.

## 빌드와 보호

`rockman_roll_save_labels_ko.json`의 처음32units는 직전 록맨/롤 저장 assets의 resolved units와 필드 동일하다.
등록 variant `rockman-roll-save-labels-v1`은 14 scripts,기존8choice groups,네 fixed-cell-big profiles를 명시한다.
네 라벨의 adopted range는 실제6칸인48px/1행이다. 시간2칸,칩1칸,컵1칸,크레딧3칸이며 나머지는 native blank clear로 채운다.
숫자/printBuffer/코드/flags/callSave/선택/전원 경고를 변경하지 않는다. 새로운 코드 hook은 없다.
source9008bytes와106미선택slots,직전116save slots(10..13외),다른20archive payload 불변 검사를 통과했다.
기존 normal dialogue 초안, 기본명 counter PoC, 전체글꼴 공급과14그래픽 변경은 기존 누적 설계를 유지한다.
재현: 이전 roll-save 누적 flags에 `--save-labels` 추가. 단독 save-labels 선택은 거부한다.

## 새 ROM 실제 실행

`save-labels-poc-v1-cold-part1 → date → profile → navi-menu → select-roll → intro → save-labels → save-commit`.
최초 state_origin=null; 모든 checkpoint는 동일 새ROM SHA에서 생성한다. old-ROM checkpoint/수동 RAM/save import 없음.
`save-labels`는 로드 이전 intro에서 다시 저장 메뉴를 연다. step11의 네 라벨을 다음과 같이 검사했다.

- relocated script lookup와 F9FC 각 한글음절 코드
- big Hangul BDF의64-byte glyph와 실제 fixedcell glyph selection
- 6glyph/384byte staging·VRAM 업로드,줄어든 네이티브 문자 뒤 native blank clear
- BG0 4bpp,unscrolled32×32,charbase8000,palette9,상하tile pair
- 타일map이 실제 glyph를 소비하는지와 화면각8×16 cell의 ink/shadow mask·색상 구분

화면 좌표는 x104부터, y24/40/56/72이며6칸 범위 x104..151를 유지한다. adjacent 숫자영역을확장하지않는다.
`analysis/save_labels_poc_v1/save_labels.png`를직접검토했다. 미번역일본어 뒤잔상 없음.
`save-commit`은 실제 native save를 수행하여64KB allFF SHA71189f...→e0dbfe...로갱신했고 native script23 완료를확인했다.
완료스크린샷도직접검토했다. 다른 테스트save는변경하지않았다.
이검사는이ROM의save operation/완료분기이며 fresh persistence reload/기존save호환 지원으로일반화하지않는다.

`report_save_labels.py`가 source/selected boundaries/old payload/glyph-stage-BG-pixel/native disk edge를검증한다.
관련54unittest(5.836초)통과. historical runtimefixtures는새ROM 실행 증거가아니다.
main/_repro는같은SHA. 최종현재tools/3build/source audit는 `save_labels_poc_v1/final_identity_audit.json` 참조.
원본·직전ROM·조사캡처·testsave는보존한다.

## 남은 우선 작업

이 버전에서는 상단 セーブ 그래픽 제목, numeric cup unit16의 コ가 원문이었다. 후속 save_surface_poc_v1에서 번역·검증했다. `SAVE_SURFACE_POC_HANDOFF.md` 참조. 이전 실행 기록을 새 ROM의 증거로 합산하지 않는다.
공통 scripts10..13은 다른 Navi의 저장에도 사용될 수 있으나 이번 정상실행은 Roll만검증했다.
가장큰미해결은 한글 이름입력/편집/저장·재표시 소비자 전체와기존save호환이다.
전체게임,RTC/alarm,실기,오디오,완전한 인간리뷰와 배포는미완료다. 완역/출시후보로승격하지않는다.
