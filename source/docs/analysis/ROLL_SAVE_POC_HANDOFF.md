# 롤 저장 문구 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 정확한 아티팩트와 변경 범위

`poc/output/exe45_ko_development_roll_save_poc_v1.gba`
SHA256 `7f121d4acb5c3ea2eb5c9379d0b855234f676699e7dd9a5f17ad7862343248c5`.
21selected/711untouched archives; 1,108selected text units; 14prior graphic labels. 전체 완역률이 아니다.

원본6DA21C script0 checkNaviAll의Roll branch20과실제롤저장확인/완료화면으로스피커/기능을확정했다.
`rockman_roll_save_ko.json`은기존Rockman0..4의16resolved units를그대로보존하고Roll20..24의16units를추가한다.
등록variant의10스크립트/8choice group을명시선택하고3행/144px 제한,선택공백,개행과모든명령·flag·callSave·branch·wait를보존한다.
빌드최대정적본문121px. wordings/human presentation 승인미완료이며리뷰완료로승격하지않는다.
재현: 기존누적calendar-presets-poc 빌드flags에`--roll-save`를추가한다.
원본9008-byte storage와110미선택slots,이전save115slots(20..24외),다른20archive payload불변검사통과.
일반이름counter·fontprovider·그래픽패치는직전설계를유지하지만후속ROM에서모든이전route를재검증했다고주장하지않는다.

## 실제 실행 검증

`roll-save-poc-v1-cold-part1 → date → profile → navi-menu → select-roll → intro → save-enter → save-commit → save-overwrite`.
각segment는동일새ROM SHA만허용한다. 최초segment state_origin=null. 원본/이전ROM의save-state를import하지않았고정상controller입력만사용했다.

- enter11: 확인20,세리터럴전체.
- overwrite6: 덮어쓰기21,세리터럴전체.
- commit6: 저장중22 첫리터럴과전원경고.
- commit7: 완료23 첫리터럴.

네페이지의실제stream/glyph index/CPU폰트read/96byte glyph/OBJ VRAM/화면role픽셀·선택커서/범위를검증했다.
`save_pages.png` 네스크린샷을직접시각검토했다.
nativecallSave가테스트64KB save를allFF에서다른SHA로갱신했고복사증거를보존했다.
덮어쓰기‘아니요’에서nativecursor x144를확인했고디스크save SHA불변을확인했다. 다른testsave는불변.
실패·재시도/invalid-data는원본명령/분기/번역font검사를통과했지만실제오류화면은유발하지않았다.
미관찰8Roll units를`save_runtime.json`의open_roll_units에남긴다.

`capture_roll_save.py`는기존읽기전용font observer의archive만6DA21C로선택하고격리save folder/BIOS/ROM/도구를검사하며디스크before/after를기록한다.
`report_roll_save.py`가현재아티팩트·정상경로·glyph픽셀·native disk edge·기존payload불변을검사한다.
관련52unittest(21.032초)통과;historicalfixture실행은새ROM의플레이증거로합산하지않는다.
main/_repro 동일SHA이며최종현재도구독립build/audit는`final_identity_audit.json`으로확인한다.

## 직전 기본명 ROM의 영구저장 증거

정확한대상은`exe45_ko_development_calendar_presets_poc_v1.gba` SHA08d40d...이며후속save ROM의실행증거가아니다.
`calendar-presets-persist-v1-save-commit`: native완료메시지+64KB save allFF SHA71189f...→8659a8... 갱신.
`reboot`는state_origin=null의새프로세스. before/after save동일SHA.
`reboot → reload-direct → reload-calendar3 → reload-final-query`는자체cold에서만파생된정상경로다.
저장전과동일한record02001310의32bytes `03000001010602000003f9fc5929f9fcd01ae500000000000000000000000000` 복원확인.
1월1일2:00AM목록의`학원`은mono-provider의2glyph→stage→0600A400 VRAM일치와직접스크린샷확인.
이목록은정상font detail-dialogue와다른fixed-cell소비자다. 직접detail재조회는이번영구저장증거에포함하지않는다.
보고서`calendar_presets_poc_v1/persistence_runtime.json`.
최초PET새해인사/잘못된날짜/빈목록/잘못된메뉴경로등failed observation은보존하고성공chain에서제외했다. state/RAM/save를수동수정하지않았다.

## 미해결과 다음 작업

이 아티팩트에서 저장화면title(セーブ),タイム/チップ/カップ/クレジット는원문으로남아있다.
후속 조사에서 네 항목은 이미지가아닌6DA21C scripts10..13의고정폭문자열로확인되어save_labels_poc_v1에번역했다. `SAVE_LABELS_POC_HANDOFF.md` 참조.
상단title그래픽은별도소비자이며픽셀/압축·tilemap/실제loader경계를확정해야한다.
일정`식사`의영구재로드/후속ROM에서의학원저장·재로드는별도검증이필요하다.
가장큰미해결은한글이름입력/편집/모든copy·storage·재표시소비자및기존save호환이다.
전체게임/RTC-alarm/실기/오디오/인간검토·배포는미완료. 기존ROM/실패작업폴더/캡처/원본을덮어쓰거나삭제하지않는다.

처음작성한saveasset는schema2에직접unit을넣어wordings누락검사에실패했고제품이생성되지않았다.
기존schema1 직접unit계약으로고쳤다. listglyph검사도처음big-provider가정이거부됐고실제trace의mono-provider로범위를바로잡았다.
