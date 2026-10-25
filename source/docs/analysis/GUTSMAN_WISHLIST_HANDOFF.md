# 거츠맨 희망 물건 질문 — 2026-10-09

전체 미번역 작업의 진행분이다. fixed literals153 전부 선택과 사용자 입력·저장 기능 완성을 혼동하지 않는다.
needs_review; development-draft; NON-DISTRIBUTION; release_eligible=false.

## 제품과 번역 입력

최초ROM `poc/output/exe45_ko_development_gutsman_wishlist_v1.gba`, 독립 `_repro.gba`.
최종도구 고정 제품 `_r2.gba`/`_r2_repro.gba`까지4개 ROM bytes/hash 동일.
SHA256 `cb0cc5dca0831bdd10adfed3eb4ed940b51f98d2c358fb13a87e56e6ab6a2c7e`.
2,545선택literal/60선택archive/672원본유지archive; previous answers 제품보다3문구 증가.
`translations/gutsman_profile_wishlist_ko.json` SHA `f4159141473cba171026a9584221a16be144ff7abb4ec6cb22d2de693d43170d`.
parent asset `gutsman_profile_answers_ko.json` SHA `e04a02a87e2ca4d5d86caa686965df2abde660ff4a14e93cc9e57fc9705a9b1f`,150unit 정확히 유지.
새3문구는 주 에이전트 수동 초안이며 의미/표현/시각에 대한 인간 승인과 배포 검토는 미완료다.

## 범위와 빌드

667044:31:0..2의 강한 칩·거츠맨이 원하는 칩·플레이어의 희망 물건 질문.
3페이지의 기존 줄바꿈/기다림/지움/닉네임 명령을 보존한다. nickname suffix는받침에 의존하지 않는동일 폭쉼표.
입력 초기화flags3605/3606와waitHold는 그대로다. 별도 사용자 문자열은 이153고정literal에 포함하지 않는다.
원본5225bytes/97slots/루트0x38138;63literal scripts 선택,34원본비literal slots 유지.
선택unit와TextPet 원본literal 전체집합의 동등성을 검증한다. 새로운 정상wishlist선택/한글입력 증거는 아니다.

`python -X utf8 tools/build_keyitem_full_rom.py --name <새 이름> --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist`
원본부터primary빌더를 실행한다. old patchedROM 입력/수동hex변경없음. 이전제품·native save·캡처보존.

## 실행과 증거 책임

`run_gutsman_wishlist.py`: 자체freshROM cold/profile/native save58/coldcontinue→PET/소개/넘버맨→internet/정상29 질문·키보드→profile-seed.
seed는667044가 아직로드되지않은같은ROM 정상checkpoint.
31진입은native reader0804FB76의29 table-read만한번alias한격리진단이다. source header 일치/skip0,ROM/RAM write없음.
step2/3/4에서3페이지를표시한뒤 마지막keyWait에서정지,flags3605/3606 이전이다. 진단checkpoint는정상부모로재사용하지않는다.
`report_gutsman_wishlist.py`:fontCPU/OBJVRAM/픽셀·native nickname·행배치/지움·keyWait/input-init바이트 검증.
`wishlist_runtime.json`, `wishlist_pages.png`는진단표시범위만소유한다. 이전150의전체화면을재실행했다고주장하지않는다.
`audit_gutsman_profile.main(...wishlist=True)`는prior150/96profile scripts/59다른archive payload·폰트/advance/이미지/keyitem39·ledger/원본/재현·CPU/새save/회귀를감사한다.
실행prefix/native save는최초_v1로유지한다. r2로의실행증거이관은완전한ROM byte identity를감사한다.

## 입력 기록 관찰

`capture_gutsman_input_records.py`는normal29의native keyboard에서동작하는readonly관찰자다.
static descriptor포인터에서확인한02026080..0202637F 쓰기PC/CPU인수,080517D0의buffer command,0800094C의512byte copy를기록한다.
snapshot으로768byte descriptor주변영역/512byte transient출력을보존하며별도RAM/ROM write와alias를하지않는다.
관찰범위가전체keyboard editing buffer나영구record전체라는주장은하지않는다. 이벤트 부재를확정/저장부재로해석하지않는다.
`gutsman_wishlist_v1/native_input_observation.json`이9snapshot/ROM/RAM/화면/observer hashes와관찰한계를소유한다.
정상29→키보드에서A로「あ」선택→Start는決定 focus→A는확인창→defaultYes A는반응93을실행했다.
확인창은6368E8:10:0..2, relocated root08800000; prompt와Yes/No가아직일본어다. 다음번역대상으로남긴다.
최종Yes 전후RAM020010A6..020010AC가007e7e7ee50000→019be57ee50000으로바뀌었다. 9B=あ와상관된record후보지만field identity/ABI/writer PC는미확정.
02026080..descriptor영역768bytes는모든9snapshot에서같았으며watched write/copy/command0이다.
이는입력확정이없었다는증거가아니다:바뀐record후보는watch범위밖이었다. 임의값주입없이정상native동작만관찰했다.
다음은`gutsman-wishlist-v1-native-input-confirm/checkpoint.mss`에서같은ROM으로최종Yes를재생하며020010A6..AC의native writer를관찰한다.
그후길이/삭제/취소/복수문자와field-specific정상재표시·save/freshreload를검증한다. 현재한글입력·영구저장검증은아니다.

## 현재 검증 상태

4빌드동일ROM,153unit static/font/control/roundtrip/34비literal원본slot PASS.
거츠맨95+keyitem20 fixture/736AST PASS; CPU624는합성helper계약으로상점02031000 정상경로아님.
신규3페이지/fontCPU→OBJVRAM→픽셀·native nickname·줄배치/지움/keyWait/input-init전정지 PASS.3화면직접확인.
정상29의3문구/일본어키보드crop·새native save58/coldcontinue·PET22/소개2/넘버맨3/플러그아웃대표회귀 PASS.
`final_identity.json`:원본/ledger/append·기존150unit/96profile scripts/59다른archive payload·폰트/advance/이미지/keyitem39/CPU624/재현/실행identity PASS.
736Python buildpins drift=[] /745전체도구pin. 원본SHA588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8 불변.
최초_v1과_repro/_r2/_r2_repro 전체ROM동일성을검증했으며runtime_stem/native save basename을명시적으로보존했다.
현행catalog/input hash는`analysis/full_scope_gutsman_wishlist_v1_r2/`다.

## 전체 남은 범위

catalog732/31,907literal:선택2,545/미선택일본어27,503/기타검토1,859/errors0.
667044 고정literal미선택0이되어도dynamic stored answers/한글키보드·입력/편집/확정/모든재표시/영구reload/기존save호환은미완료.
다른archive/내비·이미지/inline/fixed/날짜·RTC·상점02031000 정상경로와인간의미/용어/시각검토/배포검증도미완료다.
