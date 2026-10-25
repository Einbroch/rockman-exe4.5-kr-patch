# 037 통합 빌드 진행 기록

## 최신 종료 — 2026-10-21 /037 board 대표경로 격리 실행 PASS, 038 준비 가능

- 상태권위 `analysis/pending500_037_v2/batch_status.json`. 현재 ROM/SHA/19,622ID는유지,새ROM/추가번역0/패키지0. 자체Mesen종료/사용자mGBA불변. 정상seed는계속normal-v1-16.
- 새 `board_qualified_v1.json` SHA `3113df9aed5b7e351e911e38c25d7754d304a35d80f1533afada9faa9636466d`: 원본799314 lookup/LZ→511byte nativeRAM→같은-ROM 정상state ancestry→원본2DC68/F3 table선택→script3 provider→6A4FC/BL6A502/LR6A507→037clone→한글fontCPU/OBJ/pixel,close/reentry/movement PASS. 한개ID `799314:3:0`, 두번표시/5화면 직접검토. `board_agent_visual_review_v1.json`, `board_qualified_contact_v1.png`도참조.17,068 emulatedcycles는측정샘플만.
- 진단전용read aliases: 원본2DC6E의tile0→F3와287C4의해당disabledflag0x30→0x20, frame0/300 각각만. 원래RAM/원본boardpayload/scene값변경없음. `poc/runtime/pending500-037-board-qualified-v2/diagnostic_checkpoint.mss` 정상진행금지. 자연나무접근·플래그해제·진행검증아님. qualified-v1의tile만alias는flag때문에call0; 정상gate/stair route도call0이므로기존수험표script8실행추정은확정사실로사용금지.
- 원본대사/ROM수정없이관찰누락된boardlink를보완했으므로037 두변경소비자class 대표경로검증은PASS. next500 admission=true는**038 개발입력준비가능**이지500모든화면/자연획득/사람승인/배포가능아님. 다음038 정확500 정규ID·중복/원문/컨트롤/소비자/레이아웃검증후원본기반누적ROM생성. 한글확정저장재표시/일본어자판/하단지역명미완료유지. 정규미반영10,924유지.
- 재현: `python -X utf8 tools/run_board_qualified037_v2.py` (이미존재하는out에는재실행거부),검증 `python -X utf8 tools/verify_board_qualified037_v1.py` (기존frozen보고서보존;새판필요시새이름). 아래board0/admissionfalse표현은과거단계.

## 최신 종료 — 037 실제500·정적재현/무결성·정상16·새NPC 격리16ID 표시 PASS, board실행 미완료

- ROM/SHA/19,622ID는아래와동일. integrity25981/normal94602/qualified49749 **모두exit0종료**, 실행중자체명령/Mesen없음. 사용자mGBA/원본/이전ROM/저장불변. 새패키지0.
- `integrity_v1.json` SHA `48f733a762af3eebbe615decb9915d0bbbd5dc70107b2d082ff46e1024fc0b6a`: 실제ROM 84손상거부PASS.
- `normal_path_v1.json` SHA `bc154d34e520bfbddce3de5b443dcd35aa547a36cf284bcaa4a1496d3b8fa0d7`: 자체037 coldboot16정상segment/각header·stub·wrapper·descriptor loaded sentinel/이전036 NPC79CF04 및새board799314 각각2회 실제원본LZ→nativeRAM전체일치, 기존79CF04:3:0 context/root·닫기·재진입·이동PASS. 정상대사화면직접검토. 이것은새board caller/새한국어안내문 표시성공아님.
- `qualified_native_v1.json` SHA `4eb4147dcd0f392a1fb198f9892848a0bac4f2ba0d58136d33ba55e632d3fd47`: 실제037 A1 `7A7FC4`/A2 `7ADD74`/A3 `7B39D0` qualified lookup/LZ의전체1153/1255/1079byte를별도A0정상actor/caller→037selector→clone/font/OBJ/pixel과결합, **16ID/16페이지·선택화면/22화면**, 우측cursor/B취소/닫기·이동PASS. **격리읽기별칭이며자연A1/A2/A3도달아님.** observed selector39575/45317/41383 Mesen CPUcycles, 실기/오디오/worst-case 보장아님.
- contact22화면및초기date/name·정상NPC3화면을직접검토한 `agent_visual_review_v1.json` 추가. 한글읽기/창범위/clear는확인했지만 사람승인아님. 하단지역명 `インターネット1`, 일본어자판은미번역유지; 저장형식분류/한글확정·저장지원완료아님.
- 최신 **정상seed** `poc/runtime/pending500-037-normal-v1-16/checkpoint.mss` 및동일result.json, HP100/대화닫힘/175.75,146,0. 모든qualified state는`diagnostic_checkpoint.mss`로격리,정상진행seed금지.036state를037에쓰지말것.
- **다음500/038로넘기지말고** 현재037의 **board 실제원본6A4FC→BL6A502/LR6A507→037selector→한국어표시/닫기·재진입**부터보완. 현재A0 board799314 LZ/acquisition은자연경로에서fullbyte확인했지만board GBAcaller/한글소비는아직0. 자연A1/A2/A3 NPC도달/전체500화면·사람검수도미완료.
- 경로가불명확하면기존035/036컨트롤recipe·현재037실제좌표를대조하여재현비용/관찰범위를먼저설정할것. 과거green계단(-176,56)정지는799314:8의수험표조건이며, 무의미한반복충돌/진행flag·HP주입/이전state재사용금지. 같은source의script3(나무)등새번역실제object경로확인이우선. 필요시격리read-alias진단은실제board BL/인자제공명령을보존하고자연도달과구분한다. NPC LR을board LR로대입한가짜caller검증은금지.
- 상태권위 `batch_status.json`: ROM반영500/19,622,정규미반영10,924(whole-game/image아님),next500 admission false. 아래진행중/미확인내용은이전단계기록.

## 최신 — 실제037 통합/독립재빌드/정적/CPU 동일성 PASS, 자체GBA 실행 진행

- 두 빌드 session2302/41695 모두exit0 종료. 실제 **`poc/output/pending500_037_v2.gba`** 및 `_repro.gba` 각각12,694,596byte/SHA256 **`b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd`**, 누적 **19,622ID(+500)**.
- `analysis/pending500_037_v2/integration.json` SHA `ffb7c0a5f5c0b4f69c5c3afde69c3068158a3bdfa9408ab29cbb7afd1c37ca4f`: 실제정확500/기존508소비자·036prefix(12byte stub외)·428primary/304unchanged source·전체write/append/header·단일stub·독립재빌드·18,415 CPUfixture 전체이미지동일PASS.
- 실제이미지 `legacy_cpu_v1.json` SHA `2bb0973355e8e0d290137b2317747d2bc2d132f63335c9240ecc4f6cfac02110`: **1,992조건/498 raw clone root**, 무관LR/scene pointer0/4NZCV 입력의원래ctx216/ABI 비교PASS. 이것은508모든기존소비자의gameplay/rendering실행증거가 아니다.
- `verify_integrity037_v1.py` **session25981** 실행중. `run_normal037_v2.py` **session94602** 실행중.037자체첫boot segment01 성공. 이후segment/화면/신규target표시는아직확정하지말것. 두명령완료확인전중복실행금지. 실제새ROM반영500/미반영정규초안10,924로갱신하되whole-game/image잔여량아님.
- 현재상태권위 `analysis/pending500_037_v2/batch_status.json`. 아래빌드중/현재036/미반영11,424기록은이전단계다. 새패키지0,사용자mGBA불변.

현재 검증 완료 ROM은 `poc/output/pending500_036_v1.gba`, SHA256 `0d85748e6c8c9b6abd561972f319b2687d6791778092c5ff1e9b15abb868876a`, 누적 19,122 ID다. 아래037은 정확500개 개발용 통합 진행이며 출시 승인/전체 한글화 완료가 아니다. 새 BPS/xdelta/ZIP은 만들지 않는다.

## 이번 구현

- 기존037 소스v2 그대로 500 ID/228script/70archive(NPC363+board137). 새 문구 작성/변경 없이 기존 정규 초안의 검증된 LF 배치 사용.
- `field_native_rom_selector_037_v2.py`: descriptor28byte ×70. 원본 실제BL에서 유도한 NPC LR0804F773/root02039800, board LR0806A507/root0203C800. caller/root/unsigned8-bit script를 먼저 검사하여 다른 호출은 scene pointer를 읽지 않는다. 각 후보는 script_count/scene/원문 전체byte까지 확인한다. 기존036 wrapper에 원래r3를 stack으로 넘기며 영구RAM 쓰기0.
- A3 원본 `7B3120`, `7B3E60`, `7B450C`는 native561byte가 정확히 같다. 세 소유자 모두 이번500에 있으며 전체 번역binary SHA256도 `a30594eb1ca04141893f1416280ddf0e6cea486c889409d58fb1ecd5192c91d7`로 같다. 이 조건을 확인한 경우만 동등 alias로 인정한다. 첫 동일 descriptor clone이 실행되므로 주소별 독립 선택이라고 주장하지 않는다.
- `analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json`: 18,415 CPU조건 PASS. 원본 두 caller 실제BL부터 모든 유효script(NPC15,555+board190), ABI/ctx216/flags/RAM canary, 잘못된 root/caller/scene/script/오염/미초기화scene 조기제외, 기존036 표본 회귀. 216byte clear helper만 명시적으로 모델링. 실제GBA LZ획득/font/화면/timing 증거는 아니다.
- 같은 폴더 `guards_v1.json`: 잘못된 source BL/root/인자제공명령, counter/placement, 동일native의 소유자누락/번역binary·count불일치 등18조건 거부 PASS.
- `analysis/pending_insertion_500_037_native_inputs_v2/manifest.json`: 70개 source-bound asset/scope/metric, 기존 ROM 소유권 중복0, 정확500. v1 CPU/registry/code도 과거자료로 보존. 현 버전은 **selector/CPU/registry v2**, product/primary **v2**.
- `field_native_rom_product_037_v2.py`, `build_development_patch_037_v2.py`: 원본부터 전부 재생성, 이전036 prefix는 단일12byte stub 외 불변, 원본압축/포인터/RAM 크기 유지, 전체target SHA가 위 CPU memory fixture와 같아야 output 허용. 새 소비자 자료는 `keyitem_rom.npc037`에 등록한다. `npc037` 이름은 board도 포함한다.

## 실행 중 — 완료 여부를 먼저 확인

주빌드 `python -X utf8 tools/build_layout500_037_v2.py`: exec session **2302**, childPython PID **33052**.

독립재빌드 `python -X utf8 tools/build_layout500_037_v2.py --repro`: session **41695**, childPython PID **27672**.

두 빌드는2026-10-20 20:15:44 KST 시작. 기존 누적 입력 검증이 길고 마지막까지 stdout이 없을 수 있다. 완료 전 중복 빌드 금지. `poc/work/pending500_037_v2`/`_repro` 및 같은 output 이름을 재사용/삭제하지 않는다. 원본이 primary 입력이며036은 비교 기준뿐이다.

아직 이 기록 시점에는 새ROM/실제500 반영/19,622 집계를 확정하지 않았다. 검증된 현재19,122/정규 미반영11,424(준비500포함)를 유지한다.

## 빌드 완료 후 순서

### 준비된 추가 검사 도구(아직 실행 증거 아님)

- 현재18,415 CPU fixture의 예상 전체이미지는12,694,596byte/SHA256 `b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd`. 실제primary output 확인 전에는 ROM 적용 완료로 집계하지 않는다.
- 이번 턴에 기존036 metadata의 `build_tools_sha256` **1,844개 모두 불변**을 읽기전용으로 재검사했다. `native_inputs_v2/agent_literal_review_v1.json`은500쌍의 에이전트 원문/번역 대조 기록(의미상 blocker발견0/표기차이보류)이며 사람 승인·문구 변경·GBA검증이 아니다.
- **정상route는 새 `run_normal037_v2.py`를 우선 사용한다.** v1과 같은 정상16segment입력에 `native037_loaded_guards.py`가 header/stub/wrapper/70descriptor의 Mesen 실제ROM sentinel 검사를 추가한다. 전체loadedROM hash를 계산하는 것은 아니다. `guarded_runs037_v1_version.json`에기계적차이를기록했다.
- `bench_legacy037_v1.py`는 실제037과036의 raw clone들에 대해 무관한LR/scene pointer0에서216byte context 초기화/ABI를 비교한다. 전체기존소비자의실제gameplay/rendering증거로해석금지. 아직미실행.
- `run_qualified_native037_v2.py load a1` 및 `a2`,`a3`: 자체037정상06 seed에서원본NPC lookup의scene/sub/day 읽기만한정alias하고, 실제LZ출력을전체byte검사한다. 원본포인터/LZ/RAM쓰기없음. 해당scene자연획득/selector/표시승인아님. 결과 `pending500-037-qualified-load-{a1,a2,a3}-v1`.
- 그후 `run_qualified_native037_v2.py boundary a1` 및 `a2`,`a3`: 자체037정상16 seed와각load증거필수. A0 actor/script0/mode0/원본BL을유지하고037selector의scene/원문byte읽기만해당source와연결한다. 결과 `pending500-037-qualified-boundary-{a1,a2,a3}-v1`. 진단state는자동격리,정상seed불가.
- 위6회후 `verify_qualified_native037_v1.py`: 예정된16ID/16페이지·선택화면/fontCPU/OBJ/pixels/페이지clear/우측cursor/B취소/닫기·이동 검증,22화면contactsheet. 실제결과를확인하기전에는PASS로부르지말것. A1 `7A7FC4`, A2 `7ADD74`, A3 `7B39D0`. 별도LZ와reader실험의byte동일결합일뿐 자연A1/A2/A3 actor도달/전체500/board실행승인아님.

1. 두 세션의 종료코드와 `poc/output/pending500_037_v2.gba`, `_repro.gba` 실제 존재·메타·hash 확인.
2. `python -X utf8 tools/verify_native_product037_v1.py --rom poc/output/pending500_037_v2.gba --repro poc/output/pending500_037_v2_repro.gba --out analysis/pending500_037_v2/integration.json`. 이전508 consumer/전체source write/append ownership/정확500 delta/전체18,415 CPU fixture 동일성 검사. 완료 전 적용 성공 주장 금지.
3. `python -X utf8 tools/verify_integrity037_v1.py` 별도 actual-image 메모리 오염 거부검사. 파일ROM은 수정하지 않는다.
4. `python -X utf8 tools/run_normal037_v1.py`: 위 integration PASS 필요. 과거036 정상16segment의 **입력 recipe만** 재사용하고037을 coldboot한 뒤037 자체 state만 연쇄 사용한다. 이전ROM state/진단 alias state 금지. 새 `capture_field_loader_037_v1.py`는 actual037 wrapper와 NPC/board 두 caller를 읽기전용 관찰한다. script 종료는 route receipt이며 새 대사 표시 성공을 자동 의미하지 않는다.
5. NPC/board 신규 소비자의 실제LZ→원문residency→원본caller→037selector→clone→font/OBJ/페이지/닫기/재진입·timing을 확인하고, 자연 도달/격리 진단을 구분해서 기록한다. 아직새037 GBA실행0. 전체500 화면/의미/실기/저장 성공으로 일반화 금지.

한글 자동조합→확정→저장→재표시, 일본어자판/로고/기타미번역/환영graphics 줄겹침/전체사람검수는 계속 미완료다. 사용자 mGBA는 건드리지 않고 자체 `poc/runtime/isolated-mesen-chip-matrix/Mesen.exe`만 사용한다.
