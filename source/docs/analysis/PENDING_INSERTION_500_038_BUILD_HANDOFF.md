# 038 누적 제품 빌드 — 2026-10-21

## 최종 갱신: 실제038 정상16 및 새NPC/board/hint 대표 경계 PASS

- 모든자체명령/Mesen종료.038ROM SHA `97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b` /20,122ID/독립repro일치 유지. 정적/전체쓰기/old578·carry496·정확500/CPU14,388image,45손상거부,자체038정상coldboot16 +기존대사·이동 PASS. 정규미반영초안10,424.
- 새세ID/4표시: board799314:1:0(2회),NPC7B5110:0:0,hint78AE58:10:0. 원본LZ→전체nativeRAM→실제각caller→038selector→한글font/OBJ/pixels→닫기·이동 연결. board는재열기도확인. NPC/hint는별도lookup/LZ와callerrun을전체nativepayload동일성으로연결한 **격리진단**,자연A4/A3/ShadowMan/바위진행획득이나전체500화면검증이아님. 지정read-result alias만/ROM·실제nativeRAM·플레이어·flags쓰기없음/진단state격리.
- `qualified_npc_hint_v1.json` SHA `4a96ff3897ce1768024ee100ce66a73eed4c2e910607eb6f1939bd6afe320e5c`; `board_qualified_v1.json` SHA `37dacaee500a2f2415fcbf8d99b1a3b6d630e33a8276ccc53d94c477ed2ab3fc`;직접19화면기록 `agent_visual_final_v1.json`(사람승인아님). 정확재개명령/상태는batch_status및HANDOFF맨위.
- **다음039 정확500개발준비 가능**,기준038현재fullcarryowner·canonicalpending10,424·원본primary. 실패/반증없이038검사반복불필요.정상seed038normal-v1-16만/옛037와진단state금지. packages0/사용자mGBA·원본·저장불변.한글commit-save-redisplay·일본어자판·지역명/전체게임·이미지·사람·실기·오디오는미완료,배포불가.
- 진단도구만v2수정:037import v2문자열을기계적038로바꾼NPCloadv1이실제없는selector038_v2를참조했다. 실행전발견,`capture_native_load038_v2.py`/`run_npc_runtime038_v2.py`/`verify_qualified038_v2.py`에서adopted038selector_v1사용. 도구/spec/실패조건보존,제품ROM코드·문구변경0. 아래모든실행중session은종료상태다.

## 갱신: 실제038 빌드/독립재현/통합 검사 완료

- 주96349와repro92251 모두exit0. 실제 `poc/output/pending500_038_v2.gba` / `_repro.gba` byte동일, SHA `97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b`, 12,847,864byte, 20,122ID(+500). 예상CPUfixture가 실제 출력과 일치함을 별도확인했다.
- 실제통합 `pending500_038_v2/integration.json` PASS / SHA `94888eec2c452938a207a984a1732d3187b1f55f7bfd72f3cfb0f46ff49dccbb`: 기존578·상속496·정확500·원본압축참조·전체쓰기/append·독립재현. 정규초안 ROM미반영10,424, 전체게임/이미지잔여 아님.
- **현재 실행: 정상 자체038 coldboot session31494; 실제 손상거부 session94586.** 중복실행하지말고poll. 완료뒤 `verify_normal038_v1.py`, board/hint/NPC qualified runtime/픽셀/직접화면검토. 자체038state만 사용. `HANDOFF.md` 상단과batch_status가 최신; 아래 원본빌드 실행중 설명은 이전단계다.
- 새 준비도구: `verify_board_qualified038_v1.py`, `run_hint_observe038_v1.py`, `run_hint_load038_v1.py`, `run_hint_boundary038_v1.py`, `run_npc_runtime038_v1.py load|boundary`. 아직실행 안됨/자동검사도구준비를runtimePASS로세지말것. hint target78AE58(A3/ShadowMan), NPC7B5110(A4)이며natural획득아님. Native source원본LZ와selector소비경계는별도run/fullpayload identity로연결, RAM/ROM/플래그쓰기없음, 진단state격리.
- 패키지0/사용자mGBA·저장·원본불변. 한글입력확정/저장/재표시등전체완료아님.

## 현재 진행

- 권위 `pending500_038_v2/batch_status.json`. **주빌드session96349/Python29152**, **독립재빌드session92251/Python28776**가실행중이다. 기존session부터완료확인하고중복시작금지. 두명령은`tools/build_layout500_038_v2.py`와`--repro`이며원본기반기존전체primary를실행한다.
- 현재확정ROM은계속037/19,622ID/SHA`b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd`. 새500제품적용/20,122확정아님. CPU메모리fixture 예상SHA`97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b`/12,847,864byte는**실제ROM이아니다**. 두실제출력이이를만족해야허용된다. 패키지0/사용자mGBA·저장불변.

## 이번에 완료한 경계

- native tail CPU10,536조건: 원본/실제037의F801/02 global24/25/26/27/28 모든byte값·word경계와실제코호트값,EE30 모든23내비·RAM원문/readonlyROM완전번역stream을실제dispatcher/getter/jump로실행. 분기context/offset/clear/기존변수/geometry보존. **0092C의두boundedEWRAM fill(02012F50,02013E50 각0xF00)만모델**,실제BIOS/GBA/timing/battle-outcome아님. v1은adjacent VRAMliteral을오독한filldomain가정으로거부되었고 v2가실제LDR literal55464에서정정했다. source/도구/실패보존.
- selector `field_native_rom_selector_038_v1.py`: 원본 NPC4F764/BL4F76E/LR4F773/root02039800,board6A4FC/BL6A502/LR6A507/root0203C800,**hint4F7FC/BL4F802/LR4F807/root0203D800** 세실제caller. unsignedscript/caller/root검사를scene역참조전에유지. 7word descriptor/fullnativebytes,one12Bstub/부모037wrapperentry연결,영구RAM쓰기0. 코드168byte(실행부분136),literal/finalplacement ARMv4T왕복.
- selector CPU **14,388조건**:66owner의모든유효script/실제3BL/부모ABI/잘못된root·caller·scene·script·nativebyte/null-scene조기거부,남은035/036/037대표소비자0/1. RAMnative를fixture로준비한CPU검사이지GBA획득아님.
- registry `pending_insertion_500_038_native_inputs_v1/manifest.json`:새500+기존496 모두 **원본TPL+핀된authoredasset**에서재구성하는66완전target. 이전ROM역추출은입력으로쓰지않는다. parentlineage정확일치/geometry/상태/글꼴/제어문자보존. source-only500/carry단계의설명은`PENDING_INSERTION_500_038_SOURCE_HANDOFF.md`.
- 제품component v2 진단fixture:66target를원본/선택asset에서재컴파일하고 fullcarry·미선택script·부모037完整projection·정확500/기존578record보존·전체CPUfixture SHA동일 PASS. 이진단은previousimage를fixture로준비했으므로**실제원본primary/repro 성공으로대체하지않는다**.
- primary `build_development_patch_038_v2.py`:기존037 primary의구조/쓰기검사유지+038component추가. 기존037 whole-image CPU hash gate는**새038의실제재생성prefix를원래stub로투영한정확037(해시검사)**에그대로적용;038전체는별도CPUfixture에일치해야한다. old37gate를삭제하지않았다.

## v1 메타데이터 결함과 정정

- componentv1은`cumulative038.supersedes_parent_record`에parent24개의전체clone metadata를복사해재귀consumerinventory가이력24개까지실제consumer로중복집계했다. compiledpayload/ROMbyte는정상이었으나fixture의old578+new66 검사가거부했다.
- 자체v1 주/재빌드4Python의정확PID/CommandLine를확인하고중단했다(session40563/86422 종료1). **아직ROM/work출력전**,인자manifest/도구/fixture compile폴더는보존했다. 삭제없음.
- v2는이력을archive/offset/hash만보관하여실제consumer와분리. v2component진단은old578+new66/새500/상속496를PASS. selector/imagebyte/SHA는변하지않았다. 도구고정명파일은수정하지않고새버전/버전명세생성.

## 완료 뒤 순서

1. 실제두빌드exitcode와`poc/output/pending500_038_v2.gba`, `_repro.gba`를확인. 성공전누적20,122나미반영10,424로확정하지말것.
2. `python -X utf8 tools/verify_native_product038_v2.py --rom poc/output/pending500_038_v2.gba --repro poc/output/pending500_038_v2_repro.gba --out analysis/pending500_038_v2/integration.json` —실제578priorrecord/원문압축참조/기존496/정확500/전체쓰기·append·header/CPUfixture/독립재빌드동일성.
3. 실제038 손상거부검사(새버전도구)와자체038coldboot→로드/세caller/새한글/font/OBJ/pixel/닫기·재진입·선택/branch·移動. **037state를038에사용금지**. 입력recipe만재사용. 사용자mGBA와저장은건드리지않는다. old正常seed는계속037normal-v1-16이며038에는불가.
4. 이번500 GBA경계가충분히검증되기전039로넘기지말것. 한글확정·저장·재표시/일본어자판·지역명/전체人검토·실기·오디오미완료,배포불가. 패치파일생성금지.
