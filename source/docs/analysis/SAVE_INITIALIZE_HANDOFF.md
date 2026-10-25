# 저장 데이터 초기화 안내9 — 2026-10-11

개발 ROM `poc/output/exe45_ko_development_save_initialize_v1.gba`,11157488bytes.
SHA256 `906f374acaabe9a37c70fddcae364f07c55545ae1d81b57953d727bb881415be`.
독립 `_v1_repro.gba` 전체byte동일. NON-DISTRIBUTION; needs_review; release_eligible=false.
원본 및 기존검증ROM 보존. 새로운일부화면관측만으로 전체runtime 기준을자동교체하지 않는다.

## 번역과 선택

authority `translations/save_initialize_draft_ko.json`,6368E8:96/97/98,9literal.
저장데이터 초기화 질문/예/아니요, 초기화 중 전원금지, 실패, 재시도 질문/예/아니요, 완료 안내를 수동작성했다.
‘저장 데이터를 / 초기화할까요?’는 원문의대상을유지한다. 모든명령/default/targets/flag3629/wait60/callSaveErase 보존.
초기기본선택96=No1, 실패재시도97=Yes0. 원문질문행구조와width8 선택그룹의 제안88px를 검사한다.
사람의의미/표현/화면검토는 대기다. 표시폭132px/3행은개발배치이며화면모든경로의검증을뜻하지 않는다.

parent55 `analysis/calendar_date_save_v1/selected_asset.json`은 SHA
`d9cdea229702446a1c841e5aaba7cbbdc0210dbc0404618d4bbe5852e13e19a4` 그대로유지했다.
common64 선택, 누적2596literal/60선택archive/672원본유지archive.
`analysis/save_initialize_v1/selected_asset.json`은 빌드가만드는read-only입력이다. 직접수정하지 않는다.
이미 번역한38/17 authority 및parent는manifest에역할을기록하고 catalog에서중복집계하지 않는다.

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name UNIQUE --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize
python -X utf8 tools/report_save_initialize.py
python -X utf8 tools/report_save_initialize_runtime.py
```

원본 expected writes/비중첩/전체prefix/header/append 및common15root/control/왕복,
이전55literal/252미선택script/다른59archive/normal·big·mono font/advance/주요이미지/keyitem39 보존 PASS.
신규10계약+3catalog lineage+기존39=52tests PASS. 도구컴파일 PASS.
독립재빌드 byte identity와 catalog732/31907literal/선택2596/미선택일본어27452/기타검토1859/errors0 PASS.
정적 보고서는 `save_initialize_v1/artifact_audit.json`, 초안검사는 `save_initialize_draft_v1/report.json`이다.

## 실제 관측과 세이브 보호

진입 후보는 [공식 설명서](https://www.nintendo.co.jp/data/software/manual/manual_pc5j_00.pdf)의 ‘처음부터’ 항목을 참고했다.
설명서의후보경로와실제검증은별개다. 새ROM 정상controller 입력으로 아래경로를관측했다.

`capture_save_initialize.py`는 기존QA native SAV를새ROM basename의검증용파일로명시적복사한다.
원본fixture: `poc/runtime/input-entry-v1-cold-continue/persistent_files_after/exe45_ko_development_input_confirmation_v1.sav`,65536bytes.
SHA256 `ebe5584813e1bfca96dbaf5231257153d8f14ab8b62a419ce60bc6506ee2103a`.
fixture생성ROM SHA `68260ec96c118939efa66f24f077dd06d375bdebffb8246529bcdfd6c45e87a6`.
SRAM fixture import는숨기지않는다. oldROM savestate/게임RAM주입/저장ABI변환은하지않았다.
복사 대상은 `poc/runtime/chip-matrix-saves/exe45_ko_development_save_initialize_v1.sav`만이며,
기존target이있거나 사용자경로/넓은runtime root이면거부한다. 기존fixture/다른basename 파일은미변경이다.
seed evidence는 `save_initialize_v1/runtime_seed.json`이다.

`save-initialize-v1-title`: coldboot→Start에서실제‘계속하기’ 선택,3captures.
`save-initialize-v1-prompt`: neutral7→Up2→neutral7→A2에서실제96확인창,5captures.
script96/root08800000와선택cursor101/136, ‘저장 데이터를 / 초기화할까요?’ 및예/아니요를확인했다.
`save-initialize-v1-cancel`: neutral7→B2로타이틀복귀,3captures.
모든segment own-ROM hash/ancestry/retained artifacts 검증 PASS.
QA SAV 전후같은SHA, 다른basename persistence 전후불변. 새ROM자체rtc만변경되어별도기록한다.
QA SAV 사전복사본은 각route `qa_save_before.sav`로 보존한다. 사용자save는미변경이다.
Mesen SHA `af60a18859e3253f09c8fd32f6b1c04637efbd98780f1427dd94d4629474f640`.

`save_initialize_v1/runtime.json`은 이3문구/No/B/파일보호범위만검증한다.
예 선택/실제초기화/97·98 성공실패6문구/저장freshload는미실행이며증거를만들려고사용자save를삭제하지 않는다.
직접스크린샷관측은전체font-read→VRAM→픽셀연결검사나사람의표현승인을대신하지 않는다.
앞선17/21 실제화면검증, 모든미번역/이미지/실제한글입력·저장/기존save호환·배포는미완료다.
`create-kr-patch`의source/제어/기본선택보호와재현빌드·runtime증거경계기준을적용했다.
