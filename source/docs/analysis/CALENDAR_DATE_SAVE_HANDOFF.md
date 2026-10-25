# 날짜 변경·저장 안내17 ROM 반영 — 2026-10-11

개발 후보 `poc/output/exe45_ko_development_calendar_date_save_v1_r2.gba`,11157340bytes.
SHA256 `675d6c977a0138fcf47050ca841fef056fd0be384c099e041247ef54528fe833`.
독립 `_r2_repro.gba` 전체byte동일. 원본과 기존 검증ROM은 덮어쓰지 않았다.
NON-DISTRIBUTION, needs_review, release_eligible=false. 신규17개 실제 화면 검증 전에는 runtime 기준을 자동 교체하지 않는다.

## 선택과 보호

authored authority는 `translations/calendar_date_save_draft_ko.json`17개다.
6368E8:76/90..94: 오류, 날짜 변경 제한, 사전저장/크레딧0/이벤트 중단,
확인/전원금지/저장 실패·재시도·완료·부정변경 데이터 거부.
기존parent `analysis/input_remaining_v1/selected_asset.json`38개와 합쳐 common55개를 선택한다.
누적60archive/2587literal/672원본유지archive. 파생 `calendar_date_save_v1/selected_asset.json`은 빌드 생성 read-only이며 직접 편집하지 않는다.
parent hash/문구/17ID/source/control/default/재시도분기·숫자0/[z] 토큰을 보존한다.
`callChangeTimeDate`/`callSave`/flag3629는 그대로이며96 이후 저장 초기화 스크립트는 선택하지 않는다.

최초 `_v1` 빌드는 일반문자검사가 `[z]`를 잘못 처리해 중단했다. 실패 작업디렉터리는 보존하고 ROM은 생성되지 않았다.
후속은 literal91:1만 legacy99 토큰을 허용하고 table mapping을 검사한다. 다른 임의토큰은 허용하지 않는다.
통화width11·normal3행132px/선택 width8 88px는 정적 제안배치다.76 custom-window 실제가용폭 및caller는 미확정이다.

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name UNIQUE --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save
python -X utf8 tools/report_calendar_date_save.py
```

## 검증과 남은 범위

draft8+integration6+기존input22+catalog lineage3=39tests PASS. Python 소스 컴파일 PASS.
`artifact_audit.json`: 원본 expected writes/비중첩/전체prefix/append/header·common roots/왕복/control,
다른59archive 및249미선택common script·normal/big/mono font/advance·기존이미지/keyitem39 보존 PASS.
`rebuild_boot_catalog.json`: 독립재빌드 전체byte동일, 자체coldboot receipt와catalog identity PASS.
catalog732/31907literal: 선택2587, 미선택일본어27461, 기타검토1859, parse errors0.
authority/parent는 동일선택을 중복집계하지 않도록 명시적으로 검증한다.

`poc/runtime/calendar-date-save-v1-coldboot`: 정상controller+readonlysnapshot, oldROM state/RAM injection 없음.
3capture complete=true이며 step003에서 실제 일본어 타이틀/‘처음부터’ 항목을 확인했다.
Mesen SHA `af60a18859e3253f09c8fd32f6b1c04637efbd98780f1427dd94d4629474f640`.
타이틀 도달은 신규17개가 표시된 증거가 아니다. 날짜변경/저장초기화/사용자save쓰기 미실행.

다음은 새17개 정상caller/76 별도창/91·92·94 선택창·통화glyph/font→VRAM/pixels,
취소·복귀·지움과 안전한QA 저장/freshload 회귀다. 기존21개 실제화면검증도 미완료다.
원작 일본어 자판 및 미채택F8 한글저장 후보는 이번 ROM 변경에 포함하지 않았다.
전체미번역·이미지·실제한글입력/저장·사람검토·배포는 여전히미완료다.
`create-kr-patch`의 원본보호/누적재현빌드와 정적·runtime 증거 구분을 적용했다.
