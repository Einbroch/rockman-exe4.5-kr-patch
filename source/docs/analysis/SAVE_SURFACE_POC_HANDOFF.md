# 저장 제목·개수 단위 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 결과

`poc/output/exe45_ko_development_save_surface_poc_v1.gba`
SHA256 `303319827a54790b1b81100c37c6f1a8ebe67675dbe781cd51cd94d1033868a6`.
`セーブ→저장` 그래픽1문구와 `コ→개` 텍스트1단위를 추가했다.
누적1,113선택 텍스트 단위,15그래픽 문구,21선택·711미선택 archive. 전체 완역률이 아니다.
원본 ROM과 이전 후보, 조사 캡처, 테스트 저장 파일을 보존한다.

## 개수 단위 보호

6DA21C script16의 두 컵 아이콘은 문자열 추출상 `fg`지만 실제 원본 glyph242/243이다. 번역 대상에서 제외했다.
원본 `printBuffer buffer0 minLength2 padZeros=false padLeft=true`, 아이콘과 terminator를 그대로 보존한다.
`rockman_roll_save_surface_ko.json`의 첫36단위는 직전 항목명 asset과 필드 동일하다. 추가 단위는 `6DA21C:16:1`뿐이다.
`rockman-roll-save-surface-v1` variant는 이 script를 fixed-cell-big 40px/1행으로 명시한다. 개수 표시는 원래5칸이다.
source9008bytes·105미선택 save slots, 직전119save slots(script16외), 다른20archive payload가 불변이다.
숫자 영역을 늘리거나 새 코드 hook을 추가하지 않았다.

## 상단 그래픽

원본6333A4의256-byte/64×8/4bpp block, ink15/background0이다.
원본 block SHA256 `f4807ae7a8c34336901a3715b2042505b7f817a953b30f89be3cc8626e9cf7a1`.
native read-only source 조사 `save-surface-source-v1`에서 실제 128halfword CPU read와 OBJ 전송을 확인했다.
`save_title_graphics_ko.json`과 `save_title_graphics.py`는 기존 project BDF의 원배율 픽셀로 `저장`을 구성한다.
source decode/encode round-trip, x21..43/y0..7 밖 픽셀 불변, roles0/15·canvas·slot256bytes를 강제한다.
최종 block SHA256 `635d55af41e7dd3ca7675d845368f16975bd10455fa31cde9d5f0210ee823c3e`.
같은 슬롯을 교체해 위치·길이·native lookup/loader를 유지한다. AI 이미지 생성이나 글자 재디자인이 아니다.

## 새 ROM 실제 실행과 화면

`save-surface-poc-v1-cold-part1 → date → profile → navi-menu → select-roll → intro → save-labels → save-commit`.
최초 state_origin=null, 모든 checkpoint는 새 ROM SHA로 생성했다. 다른 ROM checkpoint, 수동 RAM/save 수정 없음.
intro는 제목이 로드되기 전 상태다. 정상 버튼 입력으로 저장 메뉴에 재진입한다.

- 제목: ROM086333A4에서128halfword read, native pc0B92, destination06010A00, VRAM256bytes 일치.
- OAM: (86,2)/(118,2)의32×8 두 OBJ, tiles50/54, palette12. 원본/한글 각각 실제 화면 잉크·배경 mask 일치.
- `0개`: native script16 lookup,5glyph/320byte stage→VRAM06009A00→BG 상하tile pair 확인.
- 앞4cells는 원본 provider08601738의 아이콘·숫자/공백, 마지막 cell은 기존 big Hangul provider의 `개`이다.
- 화면 x216,y56의8×16 cell ink/shadow mask가 BDF glyph와 정확히 일치한다.
- 기존 네 항목명의 font→6칸 blank clear→BG→pixel 회귀 검사 통과.

`analysis/save_surface_poc_v1/save_surface.png`와 save-commit step007을 직접 검토했다.
상단 `저장`, `0개`, 기존 `시간/칩/컵/크레딧`, 저장 확인·완료 문구가 표시된다.
정상 native save로 새 전용64KB allFF 파일을 갱신했고 relocated archive의 script23 완료 분기를 확인했다. 다른 테스트 save 불변.
저장은 disk 변경·완료 전환 검증이며 fresh persistence reload나 기존 save 호환성 검증이 아니다.

## 재현·검증

`report_save_surface.py`가 own-ROM ancestry·protected slots·기존 labels·title CPU/OBJ/pixel·cup font/BG/pixel·native save를 검증한다.
관련58unittest 통과(12.638초). 역사적 fixtures는 새 ROM 실제 실행 증거와 구분한다.
main/_repro/_current_repro의 최종 동등성·현재 Python tools·원본 SHA 검사는 `save_surface_poc_v1/final_identity_audit.json` 참조.
재현은 기존 save-labels 누적 flags에 `--save-surface` 추가. `--roll-save --save-labels` 없이 사용하면 거부한다.
읽기전용 capture 최초 호출의 잘못된 SHA 옵션은 실행 전 거부되었으며, 올바른 `--expect-rom-sha256`으로 새 경로를 생성했다.

## 미검증·다음 작업

실행한 컵 수치는0뿐이다. 다른 수치의 숫자 명령은 보존했지만 실제 게임에서 유도해 검사하지 않았다.
공유 저장 제목·항목명이 다른 Navi에도 쓰일 수 있으나 이번 실행은 정상 Roll 경로다. 모든 Navi 실행을 주장하지 않는다.
실패·잘못 변경된 데이터 경고는 이전 정적 번역 범위이며 이번에 오류를 유발하지 않았다.
가장 큰 미해결은 한글 이름 입력/편집/저장·재표시 및 모든 소비자와 기존 save 호환성이다.
전체게임·RTC/alarm·오디오·실기·인간검토·배포는 미완료다. 완역/출시후보로 승격하지 않는다.
