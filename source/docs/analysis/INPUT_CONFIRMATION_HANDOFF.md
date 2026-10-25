# 공용 입력 확인창 — 2026-10-09

이전제품 기록. 현행제품/다음작업은 `INPUT_HEADING_HANDOFF.md`다. 아래제품의 입력저장 관찰은 해당hash에 한정하여 보존한다.

## 현재 기준과 완료 조건

사용자 요청은 전체 미번역/이미지 번역·ROM 적용·화면 검증이다. 아래3문구는 진행분이며 전체 완료가 아니다.
한글 입력·편집·확정·모든 재표시·native save/fresh reload·기존 save 호환을 여전히 완료 조건으로 유지한다.
개발 전용, needs_review; NON-DISTRIBUTION; release_eligible=false.

현재 실행ROM `poc/output/exe45_ko_development_input_confirmation_v1.gba`, SHA256 `68260ec96c118939efa66f24f077dd06d375bdebffb8246529bcdfd6c45e87a6`.
독립 `_repro`/`_r2`/`_r2_repro` 및 최종 도구고정 `_r3` 모두동일하다. 현행ROM은 `_r3.gba`, 실행증거는전체byte동일한최초_v1에귀속된다.
`input_confirmation_v1/final_identity.json` 최종 감사 PASS.742Python 도구pin drift=[], source/ledger/append/header·13unit/254script/59payload·폰트/이미지/keyitem39·실행/CPU회귀/새save/coldcontinue identity 확인.
asset SHA256 `94272bf515ad3d177ef44a0bfffd5ddcd322165b3e9e4758ef4f778a797b6a17`.
현행catalog은 `analysis/full_scope_input_confirmation_v1_r3/`이며 *_v1/_r2 catalog는이전해시기록으로보존한다.
상대outdir로생긴 `input_confirmation_v1/normal_subject_regression/`는같은보고서의초기경로출력이며보존한다. authoritative정상29 회귀는 `analysis/input_confirmation_v1/normal_subject_regression/`다.
이전 확정ROM은 `exe45_ko_development_gutsman_wishlist_v1_r2.gba`, SHA256 `cb0cc5dca0831bdd10adfed3eb4ed940b51f98d2c358fb13a87e56e6ab6a2c7e`.
원본ROM SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변.

## 적용 입력과 범위

`translations/input_confirmation_ko.json`, 공용6368E8:10:0..2:

- `これで よろしいですか?\n` → `이대로 정할까요?\n`
- `はい  ` → `예  ` (끝 공백2 유지)
- `いいえ` → `아니요`

공용 UI이므로 거츠맨 말투를 쓰지 않는다. 기존13unit는 parent `possessions_statistics_ko.json`에서 완전히 유지한다.
parent SHA256 `26f9ca2c323390ba8ce7107baa7dde6bd634ea4b62d7684f103d0e8836448cb0`를 검사한다.
혼합 fixed-cell-big/mono/normal profiles 유지; 신규script10만mmbn45 normal renderer다.
msgOpen/textSpeed/sound/positionOptionHorizontal width8/option graph/select three continue targets/BSeparate/end 바이트 유지.
공용255slots 중 기존제품 대비254scripts 동일, 나머지59archive payload와폰트/advance/이미지/keyitem39 동일.
전체60selected/672untouched archives, 누적2,548literal. Catalog732/31,907:미선택일본어27,500/기타1,859/errors0.
`input_confirmation.py`가 기존13 특수직렬화 후 신규3literal을 교체한다. source/newline/choice padding/controls 및 수평choice 총폭88·prompt184px 검사를 적용한다.
확인창은 실제 normal29 입력 경로에서 원점(52,110). 한글103px prompt와80px choice group이 맞는다. 일반무초상화 원점(8,110) 가정은 OAM 관찰로 기각했다.

## 재현 경로

기본 빌드:
`python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_input_confirmation_v1 --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation`
새 name으로 실행하며 기존work/output를 덮어쓰지 않는다.
`run_input_confirmation.py`는 동일ROM의 자체fresh cold/profile/save58/coldcontinue/PET/거츠맨/인터넷/질문29/일본어키보드부터 진행한다. 이전ROM checkpoint를 가져오지 않는다.
readonly `capture_input_confirmation.py`:공용root6368E8 native glyph/font 읽기·RAM/VRAM/화면, 후보record020010A6..AC write PC/인수 관찰. alias/외부RAM write 없음.
정상입력A로「あ」→Start 결정focus→A 확인창→Yes 또는 settled Right/No 또는 B. No와B는입력값 유지·확정record 미변경 상태로 키보드복귀. No 후 재확인창 열기도 검증했다.
prefix `input-confirmation-v1-`, savebasename 최초 `_v1`; 최종빌드로 실행증거를 옮기려면 전체ROM byte identity를 감사한다.

## 검증 증거와 기각한 실행

`analysis/input_confirmation_v1/confirmation_runtime.json` 및 `confirmation_pages.png`:3literal 정상fontCPU/OBJVRAM/픽셀, Yes/No 커서65/101, 정상 재확인창, native record전환.
No focus 화면은 same-ROM 부모의 실제 draw/font 증거와 현재 VRAM/screenshot으로 검증한다. cursor 이동이 글자를 재그리지 않으므로 새 CPU draw를 꾸며내지 않는다.
No/B 복귀시 entry-box 아래 keyboard body(8,54,232,130)17,024pixels가 같은ROM typed화면과 완전히 같다. 기존 확인창 글자도 지워졌다.
top entry-box blinking caret 및 bottom 선택cursor는 별도 소비자라 keyboard-body 범위에 포함하지 않는다. 편집값16bytes는 동일 유지한다.
최초 `...-no`는 checkpoint load 직후 Right가 수락되지 않아 cursor가Yes에남았고 A가확정했다. No 증거가 아니다.
이에 이어진 `...-edit-after-no`/`...-reconfirm-after-no`는 이미 확정된PET 분기이며 편집/재확인증거로 사용하지 않는다. 파일은 보존한다.
`...-focus-probe`에서 neutral7 후Right는101/Left는65로움직임을 확인했다. 현재검증recipe `...-no-settled`는neutral7/Right 후실제cursor101을 검증하고A를누른다.
checkpoint/input readiness 원인은 완전히 추적하지 않았다. 번역으로 option graph를 바꾼것은 아니다. 실제 수락된 입력/커서만 분기 증거로 채택한다.
PET22/거츠맨소개2/넘버맨3/native save58/coldcontinue, 정상29의3문구/일본어keyboard 및플러그아웃대표회귀PASS.
거츠맨95/keyitem20/confirmation10 fixture PASS. CPU624는합성helper계약이며실제상점02031000 정상실행이 아니다.

## 실제 입력 writer 조사: 관찰과 해석

옛wishlist동일ROM 확인checkpoint에서 `gutsman-wishlist-v1-native-writer-probe`로readonly 재생했다.
최종Yes frame6:020010A6=1 at0803500C,020010A7=9B at0803501E,020010A8=E5 at08035026.
frame23 native08032ACA가동일9B/E5를다시쓴다. 후속정규화/재표시 소비자 연결은 미확정.
새확인창ROM의Yes도같은PC/변경을관찰했다. native writer34FA0..35050 및후속정규화machine-code32AC6..32AD8의원본동일성을감사했다.
32AD8..32ADC는machine-code가아닌6368E8 root literal이다. 기존제품부터relocated commonroot로바뀌는등록된expected-write이며새ROM의08800000과15root검사를통과했다.
32AC0..32AE0 전체를unmodified code로간주한초기guard는이literal 때문에실패했다. 코드/데이터경계를분리하여재검증했으며위조된원본동일성예외를만들지않는다.
RAM0200FC5C는destination020010A6, editing0200FC80의16bytes는`9b989898e50000000000000000000000`.
source의관찰된짧은native함수08035000..08035030만Thumb 해독했고, literal353AC=0200FC40 및35034=02014E74는코드와별도로읽었다. 전체CFG/ISA지원/참조완전성 주장이 아니다.
함수는baseFC40+40에서바이트를읽고 [base+1C] 목적지에constant1을쓴뒤 다음바이트부터복사한다. 0xE5 또는0x98에서종료하여E5를쓴다. 뒤이어08032AC6을호출한다.
따라서 첫1은입력길이라고할수없다. constant marker이며 구체적flag 의미/전체field ABI는아직미확정이다.
이 복사기는바이트 단위로E5/98을검사한다. 한글다중바이트가이값을포함하면중간절단위험이있으므로 현재폰트추가만으로한글입력이된다고주장하지않는다.
02026080/02026100/02026180 descriptor는현재키보드편집영역이아니었다. 그영역쓰기0으로입력확정이없다고해석했던가설은기각했다.

## 후속 실제 입력·영구저장 관찰 (2026-10-09)

이번에는 번역 입력/제품ROM을 변경하지 않았다. `analysis/input_entry_v1/native_input_persistence.json` 감사 PASS, 화면 `native_input_pages.png`.
`tools/report_input_persistence.py`로 same-ROM 모든 checkpoint edge/캡처hash, 무개입Lua, 원본/최초_v1/현행_r3 identity, 저장 전후 보존본과 다른basename 파일불변을 검증한다.
신규 observer/report 도구는 별도hash로 묶었다. 위742도구pin drift=[]는 이전빌드 시점의 역사적 검증이며 현재 추가된 도구까지 고정했다는 뜻이 아니다.

native 정상29 어려운과목 field에서 A 네번→네글자 `9b9b9b9be5`가 들어간다. 다섯번째 A는 변화 없음, B로3글자→A로4글자 복원.
이는 일본어 single-byte 네글자 편집경계이지 한글 logical capacity나 모든 입력field의 경계 증명이 아니다.
확인창에서 아직 record `007e7e7ee50000`, 실제Yes 뒤 `019b9b9b9be500`와 거츠맨반응93을 관찰했다. 첫01은 계속 constant marker이며 길이4가 아니다.
native 저장질문25→기존저장 덮어쓰기26→저장완료28을 진행했다. 완료후 snapshot은 root0881A018/script28, 같은record를 유지한다.
격리 QA 전용 `_v1.sav`65536bytes: 이전 `5bc0c601068efe7ef6aabf0f20f6b99e11e4bce8c6e9cb9cbfd00bc50f70e618` → `ebe5584813e1bfca96dbaf5231257153d8f14ab8b62a419ce60bc6506ee2103a`.
이전 SAV/RTC는 각 실행의 `persistent_files_before/`에 보존했으며 게임이 실제 쓴 결과는 `persistent_files_after/`다. 외부 SAV 주입/RAM write 없음, 다른 basename 파일불변.
`input-entry-v1-cold-continue-snapshot`은 state_origin=null 새프로세스 cold boot/native continue다. 로드후020010A6..AC가 `019b9b9b9be500`으로 복원되고, 이어 `reloaded-pet-confirmed`로 실제 거츠맨 PET 소개까지 진입해 같은record를 유지했다.
따라서 해당 일본어 답변의 native 영구저장/새실행 로드를 확인했다. 답변을 대화에서 정상재표시하는 descriptor writer/한글저장/기존save호환 검증은 아직 아니다.

기각 실행: `input-entry-v1-save-enter`는 PET 선택index1이 남아 있어 Jack-in→취소→6Down→대회분기로 갔다. `save-commit`도 그분기의 연속이며 SAV불변, 저장증거로 사용하지 않는다.
원래 leave checkpoint에서5Down으로 index6 저장을 선택한 `save-enter-corrected` 이후만 native저장 경로로 채택한다. 기각파일은 보존한다.
공용6368E8:33 `にがてな かもくは?` 제목의 실제 fixed-cell 소비자를 `header-source`로 관찰: stream08800451→stage0201C800→VRAM0600B800, width2/height10/1280bytes, font08619EF8, caller080554BA.
기존 거츠맨 질문29의 `어려운 과목은`과 의미를 맞춰 제목 후보는 `어려운 과목은?`이다. 아직 번역/ROM선택하지 않았고, mono glyph supply/20cell 배치·지움 검증을 먼저 연결한다.

## 다음 판별 작업

약한과목 일본어4글자/삭제/다섯입력거부는 위에서 확인했다. FC40+1C의다른caller별목적지와각field record경계를 규명한다.
marker/종료값/정규화08032AC6/02014E74 temporary출력과 저장답변재질문script40..63의1C..1E descriptor생성 writer를연결한다.
이번후속save/coldcontinue는 실제4글자입력 이후이며 해당record의 영구저장/로드증거다. 다음은 같은필드의 대화상 정상재표시를검증한다. 이전 input-confirmation-v1 save58 회귀는 입력전으로 별도유지한다.
그후한글편집표현→native record변환/경계/E5-safe→각renderer재표시/저장/기존save호환의설계를수립한다. 성급한4byte원문슬롯의한글byte덮어쓰기는하지않는다.
공용invalid-input script11, keyboard 질문20..27 등, 다른내비/이미지/inline/fixed/RTC/상점/인간검토/배포검증도미완료.
