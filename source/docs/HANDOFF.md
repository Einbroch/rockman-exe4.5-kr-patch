# 작업 재개 기록

Claude Code 재개용 짧은 진입 문서: **`CLAUDE_CODE_HANDOFF.md`**. 프로젝트의 `CLAUDE.md`에서도 이 문서를 안내한다.
현재 진행 상태의 권위는 계속 `analysis/pending_insertion_500_041_source_v8/batch_status.json`이다.

## 현재 진행 — 2026-10-23 /041 v8 소스500·기존156 보존·native 경로 조사 완료, ROM 통합 전

최신 구현: **서브칩102/21archive용 selector와 immutable-source component 쓰기계획 API완료**. `subchip_rom_selector041_v1.py` / `subchip_rom_component041_v2.py`, 근거 `subchip_selector_cpu_v3.json` **1,113CPU cases PASS** + `subchip_component_inputs_v1.json` 정상입력/독립동일계획/잘못된입력22종거부 PASS. 102선택script만clone으로전환,318나머지script·잘못된caller/root/outer/손상native는040wrapper로복귀,원래41D84→4FB90prefix registers/context/flags동등. 새ROM/GBA화면아님. 원래23-slot table의13/14는NULL,21유효archive와구분·0그대로유지. 다음은나머지398/32archive+기존156을같은500 primarygraph로통합(102단독ROM금지); 완료한서브칩원래경로/CPU/소스검사재반복금지. 실제041반영0/040불변/패키지0.

최신 후속: **subchip_boundary_v1 PASS /서브칩102개·21archive 원래consumer 연결확인**. 자연입력 field-intro-v1→플러그인PET→subchip-v11로 원래LZ6F9B4C→02026C00 확인. count-v3는 아이템39 availability47→82/수량0→1을 원래read PC에서 각1회만alias; 실제HP100/100분기→원래일본어6F9B4C:6/common4F7BD/outer41D8F/default·실제draw52,110/대기/PET복귀 PASS. 모든실제48byte아이템/상태record와HP불변. 102개는같은23-Navi table/reader에정적으로연결한계약,새102한글표시/사용성공/획득/저장승인아님. 다음은이계약을041 composedselector/CPU·500전체등록으로연결할것. 기존소스검사·입력지도·서브칩원래loader검사재반복금지. 실제ROM040/21,122·041신규반영0·미반영9,424·패키지0유지.

- **현재 작업 권위 `analysis/pending_insertion_500_041_source_v8/batch_status.json`**, 상세 `analysis/PENDING_INSERTION_500_041_HANDOFF.md`. 실제ROM040/21,122ID/SHA bf97f861… 유지. 미반영9,424에 준비500 포함. **041 ROM반영0 /배포패키지0**.
- v8 정확500/445script/**53archive**. 호출미확인 debug7794EC:247은전체잔여에남겨두고 canonical mail6DD0B8:14로교체. 문구변경·축약·음절분리0. source v3/글꼴468/기존156의8물리consumer 재생성·현재미선택script보존·합친8왕복 PASS. `source_handoff_v3.json` 1,348고유파일hash 대조.
- source native_contracts_v2는491개 lookup참조만확인, full ABI승인아님.41F38는folder가아닌서브칩/loader·reader026C00. B2 ten-subarea 인덱스73개확인,실제진입미확인. raw9·메일14/77·대회secondary reader·오류대사의 기본위치/분기·상단position/choice 검증남음.
- 자체040 정상입력 장비60/메일intro9 LZ·RAM·실제common/outer caller·기존ROM guide선택확인, native_observations_v1 PASS. 초기52→표시92는두스크립트의명시적positionText92 때문; 기본52오류로단정한가설기각. PET root08803460의script23은65B9E8이며6FE8D4가아님. 장비폴더진입화면관찰(v7),새041표시검증아님.
- 후속 **native_callers_v1/quick_native_v1 PASS**: 원래trader6AAF8/root6AD80/LR6AB03, tutorial5(4개)20444→213A2/LR213AB 소스확인; tutorial14(4개)호출미확인. secondary는47958/LR47963공유,15/60/62직접호출확인·50선택미확인. 실제장비편집30→29개로원래일본어경고70발생: nativeRAM0202BA7C/outer3EFBF/default·실제draw52,110/페이지·선택지RAM유지확인.71..75와첫10소스초기화bytes동일,단새5개한글표시/모든Navi승인아님. 하드웨어Start는039A에03F7로10회정상도달(입력없음03FF),필드메뉴미진입을API문제로단정금지. v8/v9/v10/input-v1전부종료·사용자저장불변.
- 모든시작명령종료·자체Python/Mesen/session없음. 사용자mGBA/원본/저장불변. 다음은미확인실제consumer부터; 끝난source/carry/font재반복금지. old guidehook이Navi0/1에서미리ROMroot선택함을새selector에반영필요. 원본부터누적primary/repro/새041 coldboot검증후반영완료보고. new-only진단파일직접주입금지.

아래040 완료 기록은 실제ROM의 검증 근거로 계속 유효하다.

## 현재 권위 — 2026-10-23 /040 실제500 적용·대표 runtime QA 완료

- 실제 누적 ROM `poc/output/pending500_040_v2.gba`, SHA **bf97f861fc244861d2728c67eff4adaf84e532bc321665073908b9e621add570**, 13,030,312bytes /21,122ID(+500). 독립 재현 동일, 원본부터 빌드. 정규 미반영 draft9,424는 전체게임/이미지/자판 잔여량이 아니다.
- 현재 권위 `analysis/pending500_040_v2/batch_status.json`; 종합 `runtime_closure_v1.json`: 정적통합/32손상거부/자체040 coldboot16/기존통신 회귀/신규통신2page/대회소개4page/게시판10page·목록복귀·재진입·필드탈출 PASS. 158개 근거 참조 hash 대조, 28장 agent 직접 검토(사람 승인 아님). 500개 전부 화면 관찰한 것은 아니다.
- 게시판 마지막 A는 원래 caller가 자동으로 목록복귀. 039의 미변경 일본어 본문도 같은 동작. v2 입력은 목록에서A26으로 실제 재진입. field전환 이후 공유RAM은 원래 재사용되고039/040 동일: v3 checker가 수명 경계를 확인한다. v1/v2 거부·캡처는 보존, ROM 수정0. 통신16은step3/15는step4; 기존 v1의 화면번호 예상 오류도 보존.
- 모든 자체 Python/Mesen 종료 확인, 진행중 session/PID 없음. 사용자 mGBA/원본/저장 무변경, 배포패키지0. 039state를040에 쓴 적 없음; qualified diagnostic상태는 정상진행용으로 사용 금지.
- 다음500 admission부터 진행 가능. 정상 출발점040 normal16; 새ROM에는 새coldboot/동일ROM 입력재현 원칙. 일본어 소형메뉴·게시판 제목/목록·대회배너·지역명·이미지·자판/한글저장·전체게임·실기/오디오/멀티·사람검토는 여전히 미완료.

아래의 실행중/미검증 표현은 이전 단계의 이력이며 현재 상태가 아니다.

## 최신 진행 — 040 실제500 ROM·독립재현·정적통합 PASS /자체040 coldboot 실행 중

- **실제ROM `poc/output/pending500_040_v2.gba` / SHA bf97f861fc244861d2728c67eff4adaf84e532bc321665073908b9e621add570 /13,030,312byte/누적21,122ID(+500)**,독립_repro byte동일. source500+carry8/old661물리consumer+663메타·전체write/append/header/source참조/CPUfixture전체이미지 PASS. 실제감사 `analysis/pending500_040_v2/integration.json` SHA8418c0b6… . 정규미반영9,424(전체게임·이미지잔여 아님).
- **현재권위 `analysis/pending500_040_v2/batch_status.json`**, 상세 `analysis/PENDING_INSERTION_500_040_BUILD_HANDOFF.md`. 주70221/재93593 종료0. **정상runtime91695/parentPython4168**, **손상검사28700/Python31216** 실행중; 먼저결과확인/중복실행금지. 새040 GBA확인완료로오인금지,마지막완전runtime검증은039. 첫040 coldboot부터입력재현/8sentinel,039state사용0.
- 다음normal040 verify→communication040 preserved039회귀→own040 BBS/tournament/new communication qualified probe/verifier. 전부준비·syntax검사됐지만아직새500화면검증0. 기록의새500적용과GBA검증을구별할것. 패키지0/사용자mGBA·저장·원본불변/한글저장·자판·소형라벨·지역명·이미지·전체게임·실기·오디오미완료. 아래source/빌드실행중은이전단계다.

## 최신 진행 — 040 누적제품 component PASS /원본 주·재빌드 실행 중

- **먼저실행중session70221/93593 및Python32772/34224 종료확인**,중복빌드금지. `tools/build_layout500_040_v2.py` / `--repro`, output `pending500_040_v2.gba`/`_repro.gba`. 아직실제040ROM확정아님,현재039/20,622/미반영9,924유지. 상세 **`analysis/PENDING_INSERTION_500_040_BUILD_HANDOFF.md`**,권위 기존040source_v2/batch_status. 새패키지0/사용자mGBA·저장불변.
- `typed_rom_product040_v2.py`·기계생성primary040_v2: 원본부터039재생성→새500+carry8/10typedclone/one12Bstub→039wholeimageprojection·기존gates전부유지. `bench_product_component040_v2.py` PASS/보고서SHA82ecc66d…: fullcarry8/기존661물리consumer+663메타record/정확500/독립targetcompile/전체CPUfixture이미지·JSON metadata동일. **예상fixture**bf97f861…/13,030,312byte/21,122는실제출력아님.
- v1의663전체기록/661위치있는실데이터 혼동을v2에서분리,양쪽모두보존/기준완화·ROM변경0. v1 primary실행전실패/자료보존. v2입력개발채택만,040GBA승인아님.
- 완료후 `verify_typed_product040_v1.py` actual/repro/fullwrite/old661/carry8/CPUimage동일→`verify_typed_corruption040_v1.py`→`run_normal040_v1.py`/`verify_normal040_v1.py` 자체coldboot16. 통신old039회귀run/verify040와대회040qualifiedcapture준비(아직실행0). 039state사용금지/새500통신·BBS·대회한글표시추가검증필요. 아래대회선행검증종료는완료된이전단계다.

## 최신 종료 — 040 대회 원본 PET 진입·LZ·실제caller·소개4페이지 검증 PASS /다음은 누적ROM 통합

- 권위 `analysis/pending_insertion_500_040_source_v2/batch_status.json`, 상세 **`analysis/PENDING_INSERTION_500_040_TOURNAMENT_HANDOFF.md`**. 현ROM039/20,622ID/SHA bfb80e29… 유지, 새040적용0/정규미반영9,924/패키지0. 모든자체명령·Mesen종료/사용자mGBA·원본·저장불변.
- `verify_tournament_route040_v1.py`→`tournament_boundary_v1.json` SHA **fdd8efd11efe489d44414a7ac847030b4c532857e3fbf0ac5f49d4481cb49e44**. 자체039 PET에서 등록flag92 **읽기만0→8을3회alias**(02004BF7/원래PC287C4/LR49721/mask8). 원래PET확인→493B4/46530→mode24→원래46650/47968/LZ47976(6E93C8→024000)→466AA/47958/BL4795E→common/root024000/script0/LR47963→원본소개4page/원래E600wait/font/OBJ/pixel→원본후속script5 PASS. source일본어경계이며040한글/자연등록·메일획득/골드·오피셜·대회결과증거 아님. 모든진단state격리, RAM/ROM/PC/caller직접쓰기0.
- 입력만 control v2는등록없어진입0(정상조건); v1과도한broad-read관측은자체PID검증후중단/미완료보존. v3는alias성공했으나JSON의intervention표기오류/alias목록누락이라증거로불채택, v4에서수정·실제진입. 기본ROM변경0. 6화면직접agent검토(사람승인아님).
- **대회원본live경계 미확인 문제는해결**. 기존500컴파일/601글꼴/CPU1937/BBS원본2page를반증없이재반복하지말것. 다음은040 product component/원본누적primary·독립repro/661oldconsumer·carry8·500new·전체write/CPUfixture동일→040자체coldboot/통신·BBS·대회한글실행. 039state를040에로드금지. 소형라벨/자판/저장/지역명/이미지/전체게임·실기·오디오 미완료. 아래대회live미실행은이전단계다.

## 최신 종료 — 040 typed 연결부 CPU1,937·게시판 원본 두 페이지·authored500+8 registry PASS /ROM039 유지

- **현ROM039/20,622ID/SHA bfb80e29… 그대로**,040실제반영0/새패키지0/모든자체명령·Mesen 종료/사용자mGBA·원본·저장불변. 권위는 기존 `analysis/pending_insertion_500_040_source_v2/batch_status.json`에 최신필드 갱신, 상세 `analysis/PENDING_INSERTION_500_040_TYPED_HANDOFF.md`. 새500의통합ROM/한글게시판/대회실행완료로오인금지.
- `consumer_links040_v1.py` / `typed_rom_selector040_v1.py` / `fixture_typed040_v1.py` / `bench_typed_selector040_v1.py`: 원본함수·literal·Thumb1조립/역조립/전용typed3domain을검증. 새160byte wrapper는one12Bstub/원r3stack→039wrapper ABI유지. commroot024000/LR4F7BD/저장outer448C7, BBSroot032000/LR4B5AF, 대회root024000/LR47963. 전체21comm+6BBS+1대회=28원본/선택10의native prefix모호성없음. CPU1,937조건 PASS; **common4FB90이후미실행/PREFIX검사**이며GBA초기화·폰트·UI·타이밍증거아님.
- 실제 **039 qualified BBS**: 정상039field16에서환경tile읽기1회0→F4만alias. 원본A0sub0 table56944[4]=10→script799314:10/startBBS0→실제원본header700F6C를0202E000/body7000AC를02032000으로LZ→실제4B5AA→4FB4C/LR4B5AF/script9→일본어본문2pages/3표시font/OBJ/pixel/빈영역지우기 PASS. **자연접근·040한글화증거아님**,진단state격리. `bbs_boundary_v2.json` 및 `verify_bbs_boundary040_v2.py`. v1검사는잘못된배경표본215,100(테두리)을잡아서거부, v2는직접픽셀증거로본문205,100으로정정했으며검사범위완화/ROM변경0. B는원본keyWait를진행했으므로최종닫기/EDFF/재진입미검증.
- `prepare_typed_inputs040_v1.py`→`analysis/pending_insertion_500_040_typed_inputs_v1/manifest.json`: **500+carry8/10authoredasset** 등록, source/canonical/ref·profile·typedTPI포인터집합·metric재검증. 제품입력후보등록이지runtime admission아님(`consumer_runtime_prerequisites_complete=false`). 기존500sourcecompile/601글꼴/문구·어절LF동일결과반복불필요.
- 남은핵심: `6E93C8`는Ribitta **실버/골드등 토너먼트소개 대사**. 254script/23내비table 전부같은source, loader47968/BL47976→024000, reader47958/BL4795E→common/LR47963은정적+CPU확립. **원래토너먼트 live loading/entry/context 관찰 미실행**. 이사실은기존 `classify_source037_v1.py`에도정적확립되어있었으므로다시기초분석하지말것. 인위적으로공통LR만위조하지말고유효한원본mode/reader경로를확립할것. 무근거PC/RAM쓰기·전역필터완화금지.
- 이후source누적040 product component/primary/repro/전체write와carry/661기존consumer보존→040자체boot·통신/게시판/대회 대표실행. 현재039state는040에로드금지. 일본어소형메뉴라벨은현재500에서미선정/추가ROM변경0,한글입력저장/지역명/전체게임·사람·실기·오디오·멀티플레이 미완료. 아래040 source-only기록은이전단계.

## 최신 종료 — 040 정확500+기존8 보존 source 컴파일·601글꼴 PASS, 통신 소형라벨 경로 확인 /ROM은039 유지

- **현재 적용ROM은039/20,622ID**,SHA `bfb80e29c8f72ed4595a0453ca43fa6445a94d98d6d2054158f886fde2b38430`. 이번040 새ROM반영0/패키지0/모든자체명령·Mesen 종료/사용자mGBA·원본·저장불변. 현재정규미반영은여전히9,924(040500포함)이며9,424로줄이지말것.
- 새 권위 `analysis/pending_insertion_500_040_source_v2/batch_status.json`, 상세 `analysis/PENDING_INSERTION_500_040_SOURCE_HANDOFF.md`. **500ID/188scripts/10archives**: 통신151+BBS336+compressed-normal13. 원문/target 왕복·보호명령·숫자·미선택현재script·원본부터재생성한039 carry8·현재039글꼴601 PASS. `selection.json` SHAd386fed7… / `verification_v1.json` SHAeaf27934…. 문구변경0/음절내LF0. **제품입력채택/040ROM/새대사화면검증 아님**.
- BBS `7000AC,7011F0,701ED8,7028FC`: color9/원본origin32,68/arrow202,108/계속표시waitHold. 168px×3은보수적 **레이아웃시험조건**일뿐실제capacity확정아님. `6E93C8` scripts0/1/2=4+4+5는표준msgOpen모델이나compressed loader/consumer별도확인필요. 통신기존039 archive6F89D0의8개문구는authoredasset에서재생성했고현재ROM과바이트/metrics동일. source_v1은통신151+BBS339=490뿐이라선정0으로보존, v2에서정확500을별도선정.
- **일본어통신상단라벨은 baked image가 아니라 mmbn45s 소형텍스트**임을실제039에서확인. own039 v6(pre-LZ)→A,read-only관측2회; native6F56B8 RAM1723bytes 유지. smallparser03006824/문자readPC0300684E/복사0300689C,callerLR080554BA. 통계1회mono08619EF8/13×1관측,옵션4회08601738/11×1관측;glyph59=각7/52. **관측r4/r5는capacity확정아님**,두font의Korean role/색·metrics/새labelroot연결 미구현. `communication_labels_boundary_v1.json`은원본일본어소비경계만이며한글화증거아님. 현재040500에는소형라벨ID 미포함;넣으려면선정v3+보존/왕복/글꼴재검증필요.
- 다음: 이미완료한500 sourcecompile은반증없이반복하지말고 BBS/6E93C8의원본compressed loader→RAM/reader/initializer/실제창범위확립, 통신151+기존8 fullcarry 제품등록→typedselector CPU→원본누적primary/repro/기존661consumer보존→040자체부팅·대표화면. 현재039 checkpoint를다른ROM에로드금지. 소형라벨은generic parser전역변경하지말고통신전용원본caller/root/data경계부터확립. 한글자판확정/저장/재표시·지역명·이미지·전체게임·사람·실기·오디오·멀티플레이 미완료.

## 최신 종료 — 039 실제500 ROM 적용·독립재현·정상16·자연 통신 한글 안내 PASS

- **실제039 `poc/output/pending500_039_v1.gba` / SHA `bfb80e29c8f72ed4595a0453ca43fa6445a94d98d6d2054158f886fde2b38430` /12,930,632byte /20,622ID(+500)**. 원본 primary/repro 모두 완료/바이트 동일. `analysis/pending500_039_v1/integration.json`: 기존644소비자·원본압축/참조·전체source writes/append·정확500·17새소비자·CPU PREFIX fixture 동일 PASS. 정규 ROM 미반영9,924(전체게임/이미지 총잔여 아님). 런타임 검증된 이전본038은 보존.
- **자체 명령/Mesen 모두 종료**, 정상16+통신8구간 완료. 권위 `analysis/pending500_039_v1/batch_status.json`, 상세 `analysis/PENDING_INSERTION_500_039_BUILD_HANDOFF.md`. 정상보고 SHA b16109b8…: 원래LZ/기존NPC대사root/닫기·이동 PASS. 통신보고 SHA ec8dc4b0…: 자연source6F56B8 LZ1723byte→실제nestedLR/원래공유RAM→새ROMroot→6F56B8:16:0 한글stream/font/OBJ/pixels→F000/EDFF→B취소PET PASS. **대표1페이지이며500전체화면/모든Navi·멀티플레이 증거 아님**. 이전038 state사용0, 별칭/강제호출/gameRAM쓰기0. 새패키지0/사용자mGBA·저장·원본 불변.
- 신규 `communication_rom_selector039_v1.py`: 원래 공통4FB4C의 one12Bstub만 composed; root024000+innerLR4F7BD+저장outerLR448C7+u8/perarchive scriptbound+전체native bytes. 원래LZ/4493C literal/helper8bytepreset 유지. 전체23table/21unique 중17선택, 모든다른21native-prefix 모호성 거부. `selector_cpu_v2.json` **2,818조건**: 유효2,006선택+472미선택, wrongroot/inner/outer/script/native각68. **initializer4FB90..4FC20은 CPU에서 건너뜀**, 전체초기화/그래픽/오디오/런타임 증거가 아님. 실패v1과 모든시도파일 보존.
- authored registry `analysis/pending_insertion_500_039_communication_inputs_v1/manifest.json` /17asset: 원본TPL+핀된정규초안+명시적 어절LF만; carry0/문구변경0/음절내줄바꿈0. component source 재컴파일17/기존644/정확500/검증된038투영·부모gate PASS. 새 primary `build_layout500_039_v1.py`→`build_development_patch_039_v1.py`는 원본에서 누적재생성, 이전ROM은 비교용뿐.
- **42 실제이미지 손상 거부 PASS**, 직접7화면검토(사람승인 아님). 최신 동일039 정상checkpoint `poc/runtime/pending500-039-communication-v1-08/checkpoint.mss`+동일result, 통신취소후PET 알림 상태. 다른ROM에로드금지. 다음040 정확500의 적용가능한 소비자/정규초안을 조사하되 총661기존consumer/모든owner보존. 동일039검증을 이유없이 반복하지 말 것. 통신fixed-cell 일본어옵션은 이500에 미포함, 실제화면에서 확인/후속작업으로 남김. 한글입력확정·저장·재표시/지역명/이미지·전체게임·사람·실기·오디오·멀티플레이 미완료. 아래039 source-only 종료는 이전단계임.

## 최신 종료 — 039 통신 안내 정확500 source·글꼴·native제어CPU·기존메뉴경계 PASS, ROM은038 유지

- **현재ROM은 계속038/20,122ID**,SHA `97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b`. 새ROM반영0/새패키지0/자체명령·Mesen모두종료/사용자mGBA·원본·저장불변. 다음500의실제ROM통합을끝낸것이아님.
- 권위 `analysis/pending_insertion_500_039_communication_words_v1/batch_status.json`;상세 **`analysis/PENDING_INSERTION_500_039_COMMUNICATION_HANDOFF.md`**. 기존정규초안500/372script/17통신안내archive 선정, source/target왕복·보호명령·숫자·미선택원본·실제038글꼴310 PASS. 최종묶음은기존LF/space 어절경계만/음절내줄바꿈0/문구변경0. `selection` SHA966a22ec…/`verification` SHAc838e808…. 미반영정규초안10,424에이500포함(다른미선정9,924는적용후잔여가아님).
- **새 소비자**: source23내비/21통신asset table448E0→LZ448D6→공유root02024000. 원본reader448BC/BL448C2→4F7B6(outerLR448C7)→4FB4C(innerLR4F7BD);공통entry원래SP+16=outerLR448C7. 기존038 세domain은root024000을처리하지않음. **4F7B6가4FB4C를안거친다는초기해석은정정**,새통신guard를추가하되기존fieldscene조건전역완화금지. 공유4493C literal을ROM주소로변경하면LZ쓰기대상도바뀌므로금지.
- 실제own038 v7/8 원본통신메뉴:6F56B8 LZ1723byte→nativeRAM전체→실제nestedcaller/script16→원래F000/EDFF·origin92/110·소비전residency→B복귀 PASS. `baseline_boundary_v2.json` SHA0761e337…. **038일본어원본경계/039한글실행아님**,별칭/강제호출/RAM쓰기없음. 원본source6F56B8은Navi0/13/14공유/단일Navi추정금지. mmbn45s 일본어메뉴라벨은이500에포함안됨.
- native F000/EDFF draw/width **768 RAM/readonlyROM쌍**/실제helper native실행(모델0) PASS, SHA cb32a06e…. 새selectorCPU·GBA/render/link대전증거아님. 일반quickvalidator변경0,zero-speed/visiblehold 별도sourcegeometry분석.
- **다음은17 authored입력registry→정밀communication root/innerLR/저장outerLR/sourceidentity selector CPU→원본누적039 primary/repro→own039통신한글검증**. 재현된source500컴파일/038원본메뉴관찰은반증없이반복불필요.038state를039에로드금지,source기존프로필(임시분류)·음절줄바꿈대안은보존된비선택이력임. 최신handoff의정정과source명칭을따르고아래038종료기록은완료된이전단계.

## 최신 종료 — 038 실제500 ROM 적용·독립재현·정상16·세 소비자 대표 한글 표시 PASS

- **현재ROM `poc/output/pending500_038_v2.gba` / SHA `97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b` / 12,847,864byte / 누적20,122ID(+500)**. 독립repro동일, 실제578기존consumer/상속496/정확500/전체writes·append·source참조/CPU14,388fixture 동일 PASS. 45손상거부, 자체038 coldboot16 +기존대사context·재진입·닫기·이동 PASS. 정규미반영초안10,424(전체게임/이미지잔여 아님).
- 세 수정소비자 **대표 격리진단**: board799314:1:0은원본LZ511byte→원본event/tableF1/실제BL6A502→038selector→한글font/OBJ/pixel/2회표시·닫기·재열기·이동; NPC7B5110:0:0은원본A4 lookup/LZ561byte→별도원래A0actor/LR4F773→038selector→한글36glyph/4,884pixels/닫기·이동; hint78AE58:10:0은원본A3/ShadowMan lookup/LZ1841byte→별도원래Lprovider/BL4F802/LR4F807→038selector→한글17glyph/2,316pixels/닫기·이동. 세ID/4표시이며 **전체500화면/자연A4/A3/ShadowMan·바위획득 증거 아님**. 지정읽기결과만alias,원본ROM/nativeRAM/실제플레이어MegaMan0/진행플래그불변,모든진단state격리.
- 권위 `analysis/pending500_038_v2/batch_status.json`. `qualified_npc_hint_v1.json` SHA `4a96ff3897ce1768024ee100ce66a73eed4c2e910607eb6f1939bd6afe320e5c`; `board_qualified_v1.json` SHA `37dacaee500a2f2415fcbf8d99b1a3b6d630e33a8276ccc53d94c477ed2ab3fc`. **19화면 직접검토** `agent_visual_final_v1.json`, 기술검사와사람승인구별. 정상seed `pending500-038-normal-v1-16/checkpoint.mss`/동일result,HP100/175.75,146,0/창닫힘. 037·진단state 재사용금지.
- **모든자체명령/Mesen종료/배포패키지0**,사용자mGBA·저장·원본불변. 한글입력확정·저장·재표시/일본어자판배열·하단지역명/전체게임·이미지·사람·실기·오디오 미완료. 마지막 두미번역은실제038에서도직접관찰/보존했다.
- 다음은 **039 기존정규초안 정확500 준비**:038현재owner/supersession/미선택script·기존번역보존을기준으로 원본부터누적빌드.038세소비자계약은검증범위내재사용,이유없이038sourcecompile/runtime반복금지. source-only절차를전체검증완료나새번역작성으로오인금지. NPC검사v1의기계적selector038_v2 import오류는에뮬실행전발견,v2도구에서실제adoptedselector_v1로정정/원ROM변화0/구파일보존. 아래진행중표기는과거기록.

## 최신 진행 — 038 실제500 적용·독립 재빌드·정적 통합 PASS, 자체038 실행 중

- 현재 아티팩트 `poc/output/pending500_038_v2.gba`, SHA `97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b`, 12,847,864byte / 누적20,122ID(+500). 원본 primary/repro 둘 다 종료0/byte 동일. `analysis/pending500_038_v2/integration.json` SHA `94888eec2c452938a207a984a1732d3187b1f55f7bfd72f3cfb0f46ff49dccbb`: 기존578소비자/496상속/정확500/전체write·append/원문참조/CPU전체이미지동일 PASS. 정규 미반영10,424(전체게임·이미지 총잔여 아님).
- 권위 `analysis/pending500_038_v2/batch_status.json`. **정상runtime session31494**, **손상거부 session94586** 실행 중. 먼저poll/중복실행 금지. 주빌드96349/repro92251은 완료됨. 마지막 정상runtime 완료본은 아직037이며,038의500 화면검증 완료를 뜻하지 않는다.
- 다음 `verify_normal038_v1.py` 후 `run_board_qualified038_v1.py`→`verify_board_qualified038_v1.py`; `run_hint_observe038_v1.py`→`run_hint_load038_v1.py`→`run_hint_boundary038_v1.py`; `run_npc_runtime038_v1.py load|boundary`(A4 7B5110 새 welcome). 신규진단 도구 syntax 확인만 완료/실행 결과로 오인 금지. 자체038state만, 모든 read-alias 진단state 격리/자연획득 주장 금지. 037 L 정상경로 확인은 별도 `hint_route_prerequisite037_v1.json`이고038증거 아님.
- 사용자 mGBA·원본·저장 불변/패키지0. 한글 확정·저장·재표시/일본어 자판·지역명/전체게임·이미지·사람검수 미완료. 아래 빌드 실행중/037유지 표기는 과거 단계.

## 최신 진행 — 038 nativeCPU·registry·제품component PASS, 원본 주/재빌드 실행 중

- 권위 `analysis/pending500_038_v2/batch_status.json`,상세 `analysis/PENDING_INSERTION_500_038_BUILD_HANDOFF.md`. **주session96349/Python29152**,**reprosession92251/Python28776** 실행중. 먼저종료확인/중복실행금지. 현재확정037/19,622/SHA b98d… 유지;새500/20,122실제적용확정아님. 새패키지0/사용자mGBA·저장불변.
- native store/Navi-tail CPU10,536 +실제3caller selector CPU14,388 PASS. hint4F7FC→BL4F802/LR4F807/root0203D800 추가, earlycaller/root/script필터·전체native동일성·one12Bstub·원래r3stack부모037entryABI유지. registry66완전asset는원본TPL+핀된authoredold496/new500로재생성.
- v2제품component 진단재컴파일66/fullcarry/정확500/old578/부모037wholeimagegate/전체CPUfixture동일PASS. CPUfixture **예상**SHA `97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b`/12,847,864byte는실제ROM아님. 제품빌드는원본에서037전체를재생성해야한다.
- v1메타데이터에parent24 전체clone사본을이력으로넣어재귀집계가90개consumer로보는문제를독립component검사에서포착. v1자체빌드만PID검증후중단/출력전,도구·인자·실패자료보존. v2는이력archive/offset/hash만보관;ROMbyte/selector/500문구변화0. source038500/carry검사는재반복불필요.
- 완료후 `verify_native_product038_v2.py` 실제ROM/repro/fullwrite/old578/carry/CPUimage동일→손상거부→**038자체coldboot/세consumer GBA검증**. 037state금지,039진입금지,한글입력저장/이미지잔여미완료유지. 아래038 sourceonly는이전단계다.

## 최신 종료 — 2026-10-21 /038 정확500 source·fullcarry PASS, ROM은037 유지

- 새권위 `analysis/pending_insertion_500_038_source_only_v5/batch_status.json`,상세 `analysis/PENDING_INSERTION_500_038_SOURCE_HANDOFF.md`. 기존정규초안 **500ID/271script/66archive**(NPC199+board224+hint77),문구변경0/보호제어문자·원본전체/target semantic/binary왕복·미선택원본·실제037글꼴468 PASS. 새500문장작성아님.
- fullcarry분석은기존owner24개 **상속496ID/모든미선택script byte동일**,선택script는sourcecompile과동일. 새owner42개포함완전66payload검사. preflight SHA `454a4a63b8964ee04d0039015bef986ef3a7389b2e2ad2f1ef02e4e38a831162`, nativealias2쌍(A4의7B5110/7B5AA8)은전체target도동일/미해결0. carry는analysis파생물이지제품빌드입력승인아님.
- **현재ROM은계속037/19,622ID**,SHA `b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd`. 이번새ROM반영0/패키지0/실행중명령없음. 미반영정규초안10,924에이500포함(나머지미선정10,424),전체게임/이미지잔여아님. 사용자mGBA·저장불변.
- 다음은 **tail nativeCPU/branch후속초기화→hint root0203D800/LR4F807 포함3class registry·selectorCPU→원본기반037재생성+fullcarry/supersession/단일write누적038제품빌드**. 검사전500부분적용·carrymsg로기존번역되돌림금지. 037state를038에사용금지. 정상seed는계속normal-v1-16;한글확정저장재표시/자판·지역명미완료.
- **사실정정:** 과거prose의A4 NPC-null은오류. 원본53790=08053B18이며기존classification JSON도false. 자연A4도달증거는여전히없다. v1/v3/v4후보미달·carryv1입력파일명header거부·preflightv1helper shadowing 자료보존,최종v5/carryv2/preflighttoolv2사용. 새500sourcecompile을반복하지말고제품admission경계부터이어갈것.

## 최신 종료 — 2026-10-21 /037 board 원본 이벤트·caller·한글 표시 격리검증 PASS

- 현재 ROM은 계속 `poc/output/pending500_037_v2.gba`, SHA `b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd`, 12,694,596byte/19,622ID. **이번 회차 새 번역·ROM 변경0**, 배포패키지0. 자체 Mesen 실행 종료, 사용자 mGBA/저장/원본 불변.
- 새 권위 `analysis/pending500_037_v2/board_qualified_v1.json` SHA `3113df9aed5b7e351e911e38c25d7754d304a35d80f1533afada9faa9636466d`: 정상037 원본799314 LZ 511byte부터 같은-ROM state ancestry/full nativeRAM→원본2DC68 이벤트/table F3→script3→실제6A4FC/BL6A502/LR6A507→037 selector→한글 글꼴/OBJ/픽셀까지 연결. `799314:3:0` 1ID를2회 표시,닫기/재열기/이동/5화면 직접검토 PASS. selector17,068 Mesen emulatedcycles, worst-case/실기/오디오 아님.
- **격리 진단**: 원본2DC6E의 지형읽기0→F3, 287C4의 해당 disabled-flag 읽기0x30→0x20을 frame0/300에서만 alias. 실제 RAM의 tile0/flag0x30/nativepayload/scene 유지 확인. 자연 나무도달·진행조건 검증 아님. state는 `pending500-037-board-qualified-v2/diagnostic_checkpoint.mss`로격리. 다음 정상seed는 계속 normal-v1-16, 진단seed/036state 사용금지.
- 실패/음성관찰 보존: board-gate-route-v1·board-stair-route-v1·board-dispatch-observe-v1 정상입력은boardcall0, qualified-v1은tile alias만2회 해도disabledflag0x10으로boardcall0. 따라서 이 경계에서 **수험표script8이 실행된다는 기존 추정은 관찰근거 없음**. 반복 충돌하지 말것. qualified-v2에서 flag읽기만 추가로clear하여 원본boardcall2회 확인; ROM 수정으로 위장하지 않음.
- `batch_status.json` next500 admission을 **true(개발038 준비만)** 로갱신. 두 수정소비자class의 representative runtime link를확보했기때문이며, 자연A1/A2/A3·나무진행/전체500실제화면/사람승인/한글확정저장재표시는미완료. **다음은038 정규초안 정확500 선정·중복/원문/소비자/레이아웃검증부터**, 원본에서누적빌드. 지역명·일본어자판 backlog유지,패치생성금지. 정규미반영10,924/누적19,622유지(전체게임/이미지총잔여아님). 아래 board실행0/admissionfalse는과거기록.

## 최신 종료 — 037 실제500 적용·재현/무결성/정상16·격리 새NPC16ID 표시 PASS, board실행 보완 필요

- 현재 **`poc/output/pending500_037_v2.gba`**, SHA **`b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd`**,12,694,596byte/누적**19,622ID(+500)**/독립repro동일. 기존508·전체source write/append·18,415 CPUfixture동일/1,992 legacy초기화CPU/84손상거부PASS. 모든자체명령/Mesen종료,새패키지0/사용자mGBA불변.
- 자체037 coldboot16정상segment,이전NPC79CF04·새board799314의원본LZ→nativeRAM전체각2회,기존NPC한글대사context/재진입·닫기·이동PASS。新NPC A1/A2/A3 qualified LZ全byte→別A0actor/원본caller→037selector/font/OBJ/pixel **16ID/16페이지·선택/22화면**검사와직접시각검토PASS. **격리진단이며자연A1/A2/A3획득/전체500화면승인아님.** 일본어자판·하단지역명도그대로미번역임을시각기록.
- 정상seed **`poc/runtime/pending500-037-normal-v1-16/checkpoint.mss`/동일result.json**,HP100/닫힘/175.75,146,0. qualified state는모두진단격리.036state를037에쓰지말것.
- **다음500/038 admission은false**. 다음은현재037 **board 원본6A4FC→실제BL6A502/LR6A507→selector→한국어안내표시·닫기/재진입** 검증부터. 실제A0원문board획득은확인했지만GBAboard caller/새한글표시는아직0. 기존green계단수험표조건막힘을반복하지말고source799314:3등실제object경로/관찰방식을설정할것.
- 권위 **`analysis/pending500_037_v2/batch_status.json`**, 상세 **`analysis/PENDING_INSERTION_500_037_BUILD_HANDOFF.md`** 최신종료단락. 정규미반영10,924(전체게임/이미지아님),한글확정·저장·재표시/전체사람검수미완료,배포불가. 아래진행중표현은과거단계.

## 최신 — 037 실제500 ROM통합/독립재빌드/정적·CPU PASS, 자체GBA 실행 진행

- **`poc/output/pending500_037_v2.gba`** 및 `_repro.gba`: SHA256 **`b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd`**,12,694,596byte/누적**19,622ID(+500)**. NPC363+board137/70archive. 기존508소비자·036prefix(합성12byte stub외)·원본LZ/참조/전체쓰기·append/header/독립재빌드/18,415 CPUfixture 전체이미지동일PASS. actual037 legacy 초기화CPU1,992/498rawroots도PASS(모든기존소비자의실행증거아님).
- 주·재빌드session2302/41695 둘다exit0종료. **무결성검사session25981**, **자체정상coldboot16recipe session94602** 실행중(현재segment01성공). 완료부터확인하고중복실행금지. 신규NPC/board실제획득·표시/GBA전체승인은아직아님. 다음은자체route결과·필드/새대사확인,준비된A1/A2/A3 qualified실험과board native consumer확인.037에036state금지.
- 권위 **`analysis/pending500_037_v2/batch_status.json`**, 상세 **`analysis/PENDING_INSERTION_500_037_BUILD_HANDOFF.md`**. 미반영정규초안10,924(전체게임/이미지잔여량아님). 새BPS/xdelta/ZIP0/사용자mGBA불변/배포불가·한글확정저장재표시미완료. 아래037빌드중/036유지기록은과거단계다.

## 최신 — 037 두 소비자500 입력/CPU PASS, 주빌드·독립재빌드 진행 중

- 권위 **`analysis/PENDING_INSERTION_500_037_BUILD_HANDOFF.md`**, **`analysis/pending500_037_v2/batch_status.json`**. selector/registry/CPU v2, primary/product v2. NPC363+board137/70archive/정확500, 원본 실제 두BL부터18,415 CPU조건 및18 source/alias 거부 PASS. A3 동일 native3개는 전체target도 byte동일한 경우만 동등alias 인정. 원본압축/RAM유지, 영구RAM쓰기0, 전체ROM이 CPUfixture와동일해야output허용.
- 주빌드session2302/Python33052, 독립session41695/Python27672가2026-10-20 20:15:44 시작. **종료부터확인하고중복실행금지.** 아직새ROM/실제500적용/19,622확정아님. 검증된현재036/19,122/미반영정규초안11,424유지. 새배포패키지0,사용자mGBA불변.
- 완료후 `verify_native_product037_v1.py` 실제ROM+repro/fullwrite/old508/CPUfixture 검사, `verify_integrity037_v1.py`, `run_normal037_v1.py` 자체coldboot16입력route 순. 새037 GBA실행/신규consumer표시는아직0. 이전036state를037에쓰지말것. 상세명령·한계는새BUILD_HANDOFF참조.

## 최신 — 036 qualified A1/A3 경계 보강 /037 소스500 준비 PASS, ROM은036 유지

- 권위 **`analysis/PENDING_INSERTION_500_037_SOURCE_HANDOFF.md`**, 소스권위 **`analysis/pending_insertion_500_037_source_only_v2/batch_status.json`**. 정확500/228script/70archive·현재글꼴525/원문·target control/binary왕복·미선택보존·기존ID중복0 PASS. NPC363+board137. 기존정규초안그대로,새500문장작성/ROM반영아님. 현재036/누적19,122/신규ROM0/미반영정규초안11,424(준비500포함) 유지,새패키지0.
- 실제036의추가 `native_boundaries_v1.json` PASS: A1/A3실제LZ→RAM전체1914/1695byte를별도정상actor/caller/036selector 경계와byte동일로연결,10ID/10화면·fontCPU/OBJ/pixel/B취소/닫기/이동 확인.14스크린직접검토. **격리read-alias 진단이며자연A1/A3도달증거아님**,해당bool false유지. 기존PET별칭샘플보다nativecaller/selector범위강화,범위밖진행·저장·오디오/hardware보증아님.
- 037최초소스v1은별도5소비자/미해결reward를포함해서v2의두필드소비자500으로91ID교체(문구변경0),v1자료보존/두500합산금지. 원래미해결reward/tournament/A4 hint문구는백로그보존.
- **주의:** board는4F780 commonRAW NPC가아니다. 잘못된source-only preflight_v1 주석을preflight_v2로수정. 원본board **6A4FC→BL6A502→LR6A507/root0203C800/r1=[r5+4]**,actual036와원본190유효script CPU 비교PASS. 새ROM은만들지않았으며이정보로다음037제품코드/registry/ABI/독립재빌드/실행검증부터진행해야한다.
- 최신검증된정상seed는계속 **`pending500-036-sunday-natural-npc-v2/checkpoint.mss`/동일result.json** (HP100,대화닫힘)。이번진단checkpoint·친구이름편집기/랜덤전투분기는seed로쓰지말것. 우리명령/격리Mesen종료,사용자mGBA불변. 아래036빌드중/추가검증전기록은과거단계다.

## 최신 — 2026-10-20 /036 정확500개 실제ROM 반영·독립재빌드·표시 진단 PASS

- **종료 갱신:** 아래 진행중89204/18192 및후속Mesen모두정상종료. 실제036정상16segment chain에서source79CF04 두번native획득/976byte유지,actor0200ABB8 script0/mode0→source4F764/4F76E→036clone→시간분기script3의한글글꼴·OBJ·화면,닫기·재진입·실제이동PASS(`natural_cached_display_v1.json`,`normal_field_progress_v2.json`). selector32360/32361 emulatedcycles. 새39손상거부PASS. 최신036정상state `poc/runtime/pending500-036-sunday-natural-npc-v2/checkpoint.mss`/동일result.json,1/2일09:14/HP100/대화닫힘/175.75,146,0. alias/상태주입없음. **A1/A3자연경로·전체500화면/의미·worst timing으로일반화금지.** 다음작업은이036경로범위보완이며037즉시승인아님.
- 현재 ROM **`poc/output/pending500_036_v1.gba`**, SHA256 `0d85748e6c8c9b6abd561972f319b2687d6791778092c5ff1e9b15abb868876a`, 12,573,028 bytes, 누적 **19,122 literal ID(+500)**. 463문구·라벨+37기호/162script/20NPC archive. 기존488소비자·035prefix(합성stub12byte외)·원본 압축/포인터/전체쓰기/append/헤더 보존, 독립재빌드 byte동일, CPU8,423조건을 실행한 fixture 전체이미지와 byte동일 PASS. 새 BPS/xdelta/ZIP 없음.
- 권위 **`analysis/pending500_036_v1/batch_status.json`**, 상세 **`analysis/PENDING_INSERTION_500_036_BUILD_HANDOFF.md`**의최상단 갱신. 자체036 coldboot·자판3bank·초기설정 residency PASS; 격리 PET 읽기별칭 진단에서 새12ID/12페이지·선택화면의글꼴CPU/OBJ/픽셀/clear/좌우cursor/B취소·PET복귀 PASS. 34스크린/2시트 직접검토. **이것은036 자연NPC획득/selector 실행 증거가 아니다.**
- 035 자연 검증은 실제 완료: `analysis/pending500_035_v2/natural_cached_display_v2.json` PASS. 정상 actor0200AD68/script20/mode0→원본cached caller→LR4F773→clone→4문구8페이지·닫기/재진입/실제이동, alias/상태주입없음. 아래035미완료/036소스전용 기록은 과거 단계다. 035의실행증거를036 전체경로로 자동 전이하지 않는다.
- 현재036 자체 Sunday1/2 오전9시 정상경로 실행 중(`run_field036_sunday_v1.py`, session89204), 자체boot20입력/2화면완료, route진행중. `verify_integrity036_v1.py`의실제ROM메모리손상거부검사(session18192)도진행중. 종료/실패 확인 전 중복실행금지. 사용자mGBA 불변, isolated Mesen만사용.
- 기존정규초안 기준 미반영11,424ID(전체게임·이미지 잔여량 아님). 한글자동조합→확정→저장→재표시, 일본어자판·로고/기타일본어·환영이미지줄겹침·전체사람검수 여전히미완료. 현재개발용 NON-DISTRIBUTION. 036자연연결 확인 전037선정/새500집계금지.

## 최신 — 036 소스500 준비 PASS, 실제ROM은035_v2 유지

- 상세 **`analysis/PENDING_INSERTION_500_036_SOURCE_HANDOFF.md`**. 정확500개/162script/20archive의원문·control·binary왕복/미선택보존/532현재글꼴/geometry PASS,84원문population에서lookup/9오염거부PASS. 기존초안재사용이며신규500문장작성/ROM적용이아님. 430 A0 +70 A1/A3;새selector제품통합필요. 현재누적18,622/신규ROM반영0/패키지0.
- 035 자연NPC선택미완료유지. 새14정상경로중중앙계단은원본799314:0의수험표item0조건→실제script8안내로확인. 같은계단충돌반복금지. 최신정상state `poc/runtime/pending500-035-fixed-green-route-v14/checkpoint.mss`,(-176.25,56,0),대화닫힘。기존036제품반영게이트는해제하지않고독립소스준비만진행했다. 모든명령종료/사용자mGBA불변.

## 최신 추가 검증(2026-10-19,035_v2 동일ROM)

- **종료 갱신:** 추가8정상 segment(누적22), 전투/후속v5/v6 모두완료. 최신정상state `pending500-035-fixed-coordinate-route-v6/checkpoint.mss`,좌표142.75/-144,대화닫힘. `normal_field_progress_v2.json` PASS. 정상cached호출0/격리진단2 분리. 실행중명령·Mesen·임시브라우저없음. 아래 전투'진행중'표현은 이 갱신으로 대체됨. 빨간통로끝NW직진충돌을반복하지말고별도green통로접근계획필요.

- `analysis/pending500_035_v2/native_mode_display_v1.json` PASS. source native cached caller→교정 clone→글꼴/OBJ/화면, 두 문구 네 페이지/닫기·재열기·이동 확인. **actor mode 읽기1→0을 한정 우회한 격리 진단**이며 자연 NPC 선택 검증과 구별한다. 원본 actor mode/RAM/ROM 불변, 진단 state 재사용 금지. 누적18,622/신규0/패키지0 유지.
- 현재 권위는 `analysis/pending500_035_v2/batch_status.json`, 경로와 다음 동작은 `analysis/PENDING_INSERTION_500_035_FIX_ROM_HANDOFF.md` 최상단. 아래 cached 호출0/표시 미검증 기록은 과거 단계다. 정상 좌표 경로에서 랜덤 전투 발생, `pending500-035-fixed-coordinate-battle-v2` 진행 중.

## 현재035 수정본 권위(2026-10-19)

- **종료시점갱신:** 주/재빌드둘다동일SHA로완료,정적재현/26오염/실제caller2,333+ABI2,841CPU PASS. 자체오전9시정상14segment로source79D650 원본로드일치확인. **cachedNPC호출0회라nativeclone/GBA글꼴·페이지·재진입·timing은미검증**. 최신상태 `pending500-035-fixed-daytime-v2-inner-v7/checkpoint.mss`/동일result.json. 모든명령종료/실행중세션없음. 상세FIX_ROM_HANDOFF최상단참조; 아래'진행중'은과거기록.

- `analysis/pending500_035_v2/batch_status.json` 및 **`analysis/PENDING_INSERTION_500_035_FIX_ROM_HANDOFF.md`** 참조. 실제035_v2/SHA `41fdee5673329c00f80989e5de2d98db6b3b0980c9a30c5e4b8202fd8dd4d95d` 생성/정적PASS,실제nativecaller2,333+ABI2,841 CPU PASS. 같은500개/누적18,622 유지,0xBECAC0한byte만6F→73. 독립재빌드83976/26오염58744/자체오전9시GBA경로13504진행중. 아래9:57빌드중기록은이전단계.

## 2026-10-19 —035 실제 caller 복귀주소 오류 확정, 같은500개 수정본 재빌드 중

- 원인: source BL0804F76E는LR0804F773을 만들지만035_v1 guard는0804F76F를 검사. `analysis/pending500_035_v1/native_caller_cause_v1.json`: 실제 원본 caller 진입2,333조건에서v1선택0/수정fixture선택2,295(나머지38비대상fallback) 확인. 원본명령부터 실행하지 않았던 과거CPU2832를 실제caller성공으로 해석하지 말 것.
- 실제035_v1 새부팅/정상버튼으로 날짜1/4 설정, 오전6시전 source전날분기2E316(r0=1)→A0 source79D108 native2020byte 로드/전체일치 확인. `native_field_progress_v2.json`은16정상기본경로와day4경로를 결합,미완료300초longsegment는제외. 현재까지cachedNPCreader0,blueNPC는공통RAW reader4F780 사용. 주간NPC경로검사 필요.
- 새 `field_npc_rom_selector_035_v3.py`는 decoded BL address+size|1로LR유도. `field_npc_rom_product_035_v2.py`, `build_development_patch_035_v2.py`, `build_layout500_035_v2.py`, `tools/specs/primary035_v2_version.json`에서같은500개/기존18,622 유지하며1byte literal교정. 주빌드session44917/독립session83976 진행 중. 아래의 '모든명령종료'는과거상태.
- 수정후검사도구 `verify_npc_product_035_v2.py`(v1과12503744의1byte외동일 필수), `bench_npc_product_035_v2.py`(추가oldLR거부), `run_field_fixed035_v2.py`(자체freshboot에서1/4 오전9시를정상입력), `capture_field_loader_035_v6.py`(읽기전용native selector/cycles+새NPC glyph/font관측). 기존고정tools변경 없음, 원본/v1/034/저장/과거자료 보존, 새배포파일 없음.
- 권위 `analysis/pending500_035_v1/batch_status.json`은오류확정/수정빌드중으로갱신. **036진입 금지**: 수정035의주/재빌드/정적/CPU/nativecached호출→clone→glyph화면/재진입·timing확인후재개. Hangul저장/완전번역/출시승인미완료 유지.

## 2026-10-18 —035 신규500개 실제ROM 반영·독립재빌드·기존경로/새NPC표본 PASS, nativeA0 선택 실행 미완료

- 실제ROM **`poc/output/pending500_035_v1.gba`**, SHA256 `41c598d4d056b76eaacab3b111cadfa4767f2dd584ae729d03cfe09b0b859bdd`,12,503,760bytes/누적 **18,622개(+500)**.독립재빌드동일.462문구·라벨+38시간차기호/160script/9NPC source-bound clone.원본/034/이전자료보존,새BPS/xdelta/ZIP없음.
- 원본압축/포인터/loader/RAM크기는그대로;현재RAM원문전체신원으로ROM번역선택(v2),시각/sub mutable값미사용.479기존소비자·034prefix(단일합성stub12byte외) 전체보존/정확500delta/전체쓰기·헤더·append·독립재빌드 PASS.실제최종CPU2,832/25손상거부 PASS.기존고정tools1,796hash불변.
-035자체 coldboot·kana3bank·네비4종·첫메일23wait+3load+재진입 PASS.새NPC10ID/10page PET read-alias진단의fontCPU/OBJ/pixel/wait/extent PASS.3sheet55화면직접검토.**PET표본은nativeA0 loader→cachedNPCcaller→새selector의실행증거아님**,그연결/자연획득/timing은다음필수.036선정으로넘어가기전에현재035에서검증할것.
- 권위 **`analysis/pending500_035_v1/batch_status.json`**,상세 **`analysis/PENDING_INSERTION_500_035_ROM_HANDOFF.md`**.모든명령종료/진행중세션없음.한글조합·저장재표시/환영graphics줄겹침/일본어자판·로고·기타미번역/사람검수미완료.개발용NON-DISTRIBUTION.아래source500/034기록은과거상태.

## 2026-10-18 —035 다음500개 압축NPC대사 소스·글꼴·정적loader 검증, 실제ROM 미반영

- actual034 기준 미반영 정규초안12,424ID 재집계(전체게임/이미지 잔여량 아님). 압축1,972ID 기존화면모델통과 중 **정확500ID/160script/9압축아카이브** 선정.462문구·라벨+38시간차점기호,4LF-only배치;기존문구 단어·공백·제어 보존.
- 원문전체byte왕복/번역literal·control·binary왕복/미선택script보존/16bitoffset/actual034의547글꼴 PASS.9개압축 self+별도decoder왕복 PASS. 새payload는원본보다증가하여네이티브변환·RAM다른writer/수명·caller·제품저장등록/빌드·실행 검증 필수;아직적용준비500/ROM완료 아님.
- 정적0804F712→sceneA0/sub-area/8way조회→02039800 연결/Thumb1왕복/10손상거부 PASS.뒤loader0203C800과의거리12288내최대6780은필요조건뿐,전체gap의free/수명승인 아님.기존다른4pointer는보존.기존RAW안전1개6FE8D4:23:0은별도보류,이번500에미포함.
- 실제ROM034/SHA256 `4727b8dfcee840b81d45ed156a9e0613f128f4090f8659b58351d6a9c0a17751` 유지;신규ROM반영0/새BPS·xdelta·ZIP없음.모든명령종료/에뮬레이터미실행.상세 **`analysis/PENDING_INSERTION_500_035_SOURCE500_HANDOFF.md`**,소스권위 `analysis/pending_insertion_500_035_source_compile500_v1/verification.json`.

## 2026-10-18 —034 신규500개 실제ROM 반영·독립재빌드·실행/화면 샘플 검증 완료(개발용)

- 현재ROM **`poc/output/pending500_034_v1.gba`**, SHA256 `4727b8dfcee840b81d45ed156a9e0613f128f4090f8659b58351d6a9c0a17751`,12,442,520bytes/누적 **18,122개(+500)**. 독립재빌드바이트동일. 원본/033/이전자료보존. 새BPS/xdelta/ZIP없음.
- 441유지+새59=500/243script/30RAW,기존3187개·7혼합script14기존문구/기타449소비자 보존. 전체쓰기·포인터·헤더·append·입력소유·정확500delta PASS. 입력91/사전759/단일배치4/실제손상16거부 PASS.9freshCPU45,680+SFX2,048+세로폭144/A3B0 11,993조건 PASS.
- 자체034 coldboot·자판3쪽·초기설정·네비4종·첫메일23wait+재진입 PASS. 보정v2진단4경로/신규7literal·7페이지 글꼴CPU/OBJ/화면픽셀/선택좌우/미션한쪽전환 PASS.3contact sheet53화면 직접검토. 초기환영문구겹침/일본어자판·로고·입력된일본어이름 유지. 한글자동조합·저장재표시 미완료.
- 권위 **`analysis/pending500_034_v1/batch_status.json`**, 상세 **`analysis/PENDING_INSERTION_500_034_HANDOFF_FINAL.md`**. 모든명령종료/진행중세션없음. v1진단은추가A입력으로목표wait를넘겨검사실패;보존하고동일ROM의v2로정정검증. 자연프로필편집/목록전체수명·Yes저장/미션결과 증거아님.
- 다음035는actual034/cumulative034.scope부터034선정ID제외. `6FE8D4:23:0` 추가안전후보1개보존. 아래빌드진행·441준비기록은과거상태.

## 2026-10-18 —034 정확500개 준비·입력검증 완료, 원본 기반 주빌드/재빌드 진행 중

- 기존441유지+새59=500/243script/30RAW.307글꼴/원문왕복/243부모script실제033일치/기존3187개·7혼합script14기존문구보존/759손상거부 PASS.59는미션58+트레이더1이며6FE8D4:23의추가1개는다음묶음으로보존.
- source-bound exact500입력관문 및21기존append경로(이번변경0)/4거부/주빌드버전recipe PASS. `build_layout500_034.py` 세션38166, 독립`--repro` 세션57034 진행중;중복실행금지. 아직실제034전체쓰기·재현성·실행검증/적용완료로보고하지않는다.
- 준비권위 `analysis/pending_insertion_500_034_preflight500_v1/verification.json`, 상세 **`analysis/PENDING_INSERTION_500_034_BUILD_IN_PROGRESS_HANDOFF.md`**. 이전완료본033/17,622개 유지. 새BPS/xdelta/ZIP없음. 아래441은과거상태.

## 2026-10-17 —034 목록문구166개 추가, 합계441개 소스·누적 병합 검증 /ROM 신규적용0개

- 기존275+신규166= **441 literal ID/235script/28RAW** 준비(문구·라벨423+시간차기호18). 정확500까지59추가필요. 실제ROM033/17,622개/SHA256 `7b8c060e97b1eba154327750a7474d001211a68ed1b451363d265256aae26041` 유지. 새ROM·배포패키지없음.
- 네이티브 목록생성08038CD8의 모든활성mask/길이/2byte최대경계 source/033 각각10,512조건(v1/v2별도),생성→실제Navi0분기→VM초기화일부/EE03 global5/F90C512복사82조건 PASS.82조건은정확BIOS CpuSet32 zero216만모델링;페이지clear/그래픽/편집기/저장/실제GBA신규한글표시증거아님. 미사용버퍼stale와3/6개경계의직전byte E5 기록,임의512글자폭선언없음.
- 엄격목록모델6정상/21거부;166/159script(19LF-only배치) 기존문구보존.677F64:58의2문구는3줄초과로제외,6368E8:61은다른경로로제외.441 원문·번역왕복/237글꼴/235부모script실제033바이트일치/기존2734개·7혼합script14literal·richmetrics/scope보존/733손상거부 PASS.
- 현재권위 **`analysis/pending_insertion_500_034_preflight441_v1/verification.json`**, 상세 **`analysis/PENDING_INSERTION_500_034_PARTIAL441_HANDOFF.md`**.441에이전275/59/216포함;중복합산금지. 모든명령종료/실행중세션없음.정확500입력·제품빌드등록/자체ROM검증아직미실시. 아래275는과거상태.

## 2026-10-17 — 034 프로필질문216개 추가, 합계275개 소스·누적 병합 검증 /ROM 신규적용0개

- 기존59+신규216= **275 literal ID/76script/18RAW** 준비(문구·라벨257+기호18),정확500까지225추가필요. 실제ROM033/17,622개/SHA256 `7b8c060e97b1eba154327750a7474d001211a68ed1b451363d265256aae26041` 유지. 새ROM·패키지없음.
- 새PET132px 2항질문 모델5정상/19거부,원문제어·문구고정/52script기존배치+8LF-only배치. EB01여백8/16/24와실제11flag의E900/01 처리212 source/033CPU조건 PASS(네이티브도우미대체없음). EA/EC·외부편집기·자연플래그효과/신규한글GBA표시 승인이아님.
-275원문·번역왕복/229현재사용글꼴/76부모script실제033바이트일치 PASS. 누적기존1692개보존,7부분script의기존14literal·scope/richmetrics불변,228부모바이트손상+18중복scope거부 PASS. 신규runtime는500제품ROM미생성으로미실시.
- 권위 **`analysis/pending_insertion_500_034_preflight275_v1/verification.json`**, 상세 **`analysis/PENDING_INSERTION_500_034_PARTIAL275_HANDOFF.md`**.275에59와216이포함되므로합산중복금지. 모든명령완료/실행중세션없음. 아래59기록은과거상태.
- StringBuffer169개는기존512byte descriptor를글자폭으로간주하지말것:실제버퍼생성·종결·scratch슬롯/페이지수명검증미완료.225추가선정전기존기준완화금지. 한글저장통합·환영문구겹침등기존미완료유지.

## 2026-10-17 — 034 추가59개 소스·누적 병합 검증 /실제ROM 신규적용0개

- 실제 ROM033/17,622개 유지, SHA256 `7b8c060e97b1eba154327750a7474d001211a68ed1b451363d265256aae26041`. 정확500개가모이면적용 정책 유지:59준비/441추가필요. 새ROM·BPS/xdelta/ZIP없음.
- 새033기준 미반영정규초안12924 literal ID 조사:기존RAW5228/신규RAW534/압축7137/참조미해결25. 이미지등전체게임잔여량아님. 일부기호포함, 완료율계산금지.
-59/16script/11RAW source·target왕복/147현재글꼴 PASS. 이미부분번역된7script의기존14literal을고정한컴파일이실제033부모script바이트와일치. 누적기존1176개+59신규 병합보존 PASS;기존문구·richmetrics·scope불변/48부모손상+11중복scope거부 PASS.
-59중41문장·라벨+18시간차점기호를별도분류. 독립59문장번역으로과장하지않는다. 권위 `analysis/pending_insertion_500_034_preflight59_v1/verification.json`, 상세 **`analysis/PENDING_INSERTION_500_034_PARTIAL59_HANDOFF.md`**. 아직제품입력·ROM반영·실행승인아님.
- 모든명령종료/프로세스없음. 실패한컴파일생성v1은실행전구문오류로중단됐고원문보존;v2성공.033고정도구/이전자료보존. 다음441선정시미확인StringBuffer/통신상대이름/압축·고정셀소비자에임의폭부여금지.

## 2026-10-17 — 033 신규500개 ROM 반영·독립재빌드·선택지 샘플 검증 완료(개발용)

- 현재 ROM **`poc/output/pending500_033_v1.gba`**, SHA256 `7b8c060e97b1eba154327750a7474d001211a68ed1b451363d265256aae26041`,12,432,588bytes/누적 **17,622개(+500)**. 원본/032/이전자료 보존. 새BPS/xdelta/ZIP없음.
-500/153script/37RAW 병합,기존3,126개+기타442소비자 보존/전체쓰기·포인터·입력소유·정확delta·독립재빌드 PASS.9CPU45,680+FD09 2,048+세로폭144/A3+B0 11,993/손상16거부 PASS.
-033자체 coldboot·자판3쪽·네비4종·메일23wait+재진입 PASS. 새3항선택 확인0/1/2·별도취소3,프로필취소1→기존95→PET복귀,19선택화면 글꼴CPU/OBJ픽셀 PASS.122스크린/11시트 직접검토. 진단읽기별칭은 격리상태이며 자연전투/프로필Yes편집·저장 증거가아님.
- 권위 **`analysis/pending500_033_v1/batch_status.json`**, 상세 **`analysis/PENDING_INSERTION_500_033_HANDOFF_FINAL.md`**. 모든명령정상종료/실행중세션없음. 아래 빌드진행·272준비 기록은과거상태. 다음은cumulative033.scope부터미반영정확500선정;033선정ID중복반영금지.
- 한글자동조합·저장·재표시/환영문구겹침/일본어자판·로고등미번역/전체의미·표현승인 여전히미완료. 개발용NON-DISTRIBUTION이며전체한글화/출시완료아님.

## 2026-10-17 — 033 신규500개 실제ROM 생성·전체감사·독립재빌드 PASS, 실행검증 진행 중

- `poc/output/pending500_033_v1.gba`: SHA256 `7b8c060e97b1eba154327750a7474d001211a68ed1b451363d265256aae26041`,12,432,588bytes/17,622개(+500).428주아카이브/304원본미변경. 독립재빌드 바이트동일. 원본/032/이전자료 보존. 새패키지없음.
- `analysis/pending500_033_v1/integration.json` PASS: 정확500delta/37병합/기타442소비자 보존/전체쓰기·헤더·append·포인터·유효입력소유 검증.9 freshCPU45,680조건+FD09 2,048+세로폭144, A3/B0 11,993벡터와16손상거부 PASS. 원문명령/기존번역 보존.
- 주빌드20355/재빌드49427/감사93758·20456/CPU36253·64301 모두 정상종료. 실행 드라이버 `run_runtime_033_v2.py` 세션38423 진행 중:033자체 coldboot→자판3쪽→초기설정→메일→네비4종→3항선택지/프로필취소 진단. 아직 실행/픽셀/직접스크린검토 완료로 보고하지 않는다. 실패시 원본재빌드가아닌 해당증거·검사·경로를 먼저진단.
- 신규준비권위 및 미완료항목은 `analysis/PENDING_INSERTION_500_033_EXACT500_BUILD_HANDOFF.md`. 한글자동조합·저장·재표시/남은일본어·이미지/환영문구겹침/실제프로필편집Yes경로/전체의미승인 미완료. 기존272/빌드진행 기록은아래과거상태.

## 2026-10-17 — 033 정확500개 소스·병합 검증 완료, 원본 기반 주빌드/재빌드 진행 중

- 신규500개/153script/37RAW 선정, 기존3,126개 보존/427사용글꼴/원문·번역왕복/11입력유형·77오류거부/21append단일배치 사전검증 PASS. 아직 ROM적용완료나 실행검증 결과가 아니다. 현재 승인된 이전제품032/17,122개 유지.
- 주빌드 세션20355, 독립재빌드49427 진행 중. 중복실행/기존산출물덮어쓰기 금지. 완료후 전체쓰기·포인터·기존소비자·정확500delta/재빌드동일성 검증 필요. 새패키지없음.
- 상세 `analysis/PENDING_INSERTION_500_033_EXACT500_BUILD_HANDOFF.md`. 실행준비 v2는 신규3항선택지/프로필메뉴만 사용. v1의미선정2항샘플은 미실행·보존. 진단읽기별칭/정상진행증거를분리한다. 아래272기록은과거스냅샷.

## 2026-10-17 — 033 준비272개(+19), 기존3,035개 보존 /실제ROM 적용0개

- 현재 실제ROM은032/17,122개 유지. 신규ROM/패키지없음. 사용자결정 **정확500개가모이면ROM적용** 유지, 부분253/272 적용금지.
- 추가일정13+일반6개 원문·번역왕복/미선택바이트/70글꼴/누적032기존285개 병합보존 PASS. 기존253과합쳐 **272개/103script/35archive, 기존3,035개 보존**, 안전한228개 추가필요. 현재준비권위 `analysis/pending_insertion_500_033_preflight272_v2/status.json`, 상세 **`analysis/PENDING_INSERTION_500_033_SUPPLEMENT19_HANDOFF.md`**.
- Aqua50..52 초기FD09는 실제명령위치변경없이공간모델만별도처리:2,048nativeCPU조건/정상3+오류12/실제초기12byte보존 PASS. 아직한국어실화면·음성/선택결과승인이아니다.
- 다음세로선택지224개/61script/3기존RAW주아카이브는조사만완료,준비272에미포함.폭11..13/normalflags2·0x82/origin52의F608 CPU144조건 PASS.이제2·3선택지EA/EC/navigation/BSeparate/cancel/target/행위치·번역폭을검증할별도모델필요. 기존2노드폭10모델검사를완화해통과시키지않는다.
- 모든세션종료.원본/이전보호파일/032고정도구보존.새도구도보고서해시에고정되어후속수정은새버전필요.아래253상태는이전스냅샷이다.

## 2026-10-17 — 사용자 결정: 정확500개가 준비되면 ROM 적용

- 사용자가 **“500개가 모이면 적용해줘”**라고 결정했다.253개 선반영은 하지 않는다. 다음033부터 신규·비중복500개 선정/소스 기반 누적빌드/독립재빌드/정적·실화면 검증 순서로 진행한다. 묶음 크기를 다시 묻지 않는다.
- 결정 권위 `analysis/pending_insertion_500_033_batch_policy_v1/decision.json`. 기존253개 소스컴파일·병합 준비는 보존, 추가247개 안전 후보 필요. 별도 일반대사6개는 분석 단계일 뿐 아직 준비/ROM 적용 수에 더하지 않는다.
- 현재 ROM은032/누적17,122개 유지. 이번 정책 기록으로 신규 ROM 적용0개/새 패키지없음. 아래 ‘선택 대기’는 과거 상태이며 이 결정으로 해소됐다. 배포용 BPS/xdelta/ZIP은 별도 요청 전 생성 금지.

## 2026-10-17 — 033 ROM 입력·단일 배치 경로 보완,253 선반영 여부 선택 대기

- 실제 ROM은032/17,122개 그대로, 이번 신규 적용0개/새ROM·패키지없음. 사용자에게253개 선반영 또는 기존500단위 유지 선택을 비차단 질문으로 보냈으며 아직 답변없음.
-253 신규+2,750 기존/31RAW source-bound 입력 관문 및6소비 유형/42손상입력거부 PASS. 기존21append 경로의 소스 기반 메모리 합성/단일배치 검증 PASS:20변경아카이브의 신규222ID와 나머지1개 기존바이트 보존,4오류거부. 기존032guard그대로. 아직 새주빌드/recipe등록·ROM생성·실행검증이 아니다.
- 일반창 추가6개/2스크립트는 분석만 통과,253선정에 포함하지않음. 상세 **`analysis/PENDING_INSERTION_500_033_ROM_GATE_HANDOFF.md`**. 묶음답변후 partial253또는exact500 경로를명시해 새주빌드/재빌드/전체쓰기·실화면검증으로 진행한다. 모든 명령 종료, 기존도구/산출물 보존.

## 2026-10-17 — 다음033의253개 소스·누적 병합 사전 검증, 신규 ROM적용0개

- 실제 ROM은032/누적 **17,122개** 유지. `poc/output/pending500_032_v1.gba`, SHA256 `cc2d02d3fda6ab27601d1735015b24b11d869308dff3e08f0fd4f06f31518f64`. 새033 ROM/BPS/xdelta/ZIP 없음.
- 동적 이름·프로필·칩 폭까지 합산한 LF-only 배치로 **253개/97스크립트/31아카이브** 확보. 기존 문장/단어 공백/보호 LF·패딩/제어 보존,103개 명시 배치 변경. 합성 정상7/거부7, 원문·번역 왕복컴파일/미선택 바이트/390사용글꼴 PASS. 기존 **2,750개**도 원본·고정 입력에서 재구성해 병합 보존 확인. 아직 ROM 적용/실화면 검증 결과가 아니다.
- 준비 권위 `analysis/pending_insertion_500_033_preflight_v1/status.json`, 상세 **`analysis/PENDING_INSERTION_500_033_HANDOFF.md`**. 500개 묶음에는 안전한247개 추가 필요. 20개 기존027/028/030 append 아카이브는 다음 주 빌드에서 단일 배치 전 명시 합성이 필요하며,032 보호 검사 우회 금지.
- 원본/이전 보호 파일/032 고정 도구 해시 보존 확인. 모든 세션 종료. 이번 도구·출력도 고정됐으므로 후속 수정은 새 버전/새 경로로 진행한다. 한글 저장 통합·환영문구 겹침 등 기존 미완료 유지.

## 2026-10-16 — 최신032 일정·기념일500개 실제ROM 반영/검증 완료

- 현재 ROM **`poc/output/pending500_032_v1.gba`**, SHA256 `cc2d02d3fda6ab27601d1735015b24b11d869308dff3e08f0fd4f06f31518f64`,12,418,796bytes/누적**17,122개(+500)**. 독립재빌드바이트일치/원본·이전ROM보존. 새BPS/xdelta/ZIP없음.
- 날짜·기념일152+메뉴348,191스크립트/20RAW누적병합,기존697개보존. 전체정적감사/9CPU45,680조건/A3+B0 11,993조건/손상16조건거부/정상초기설정·자판3쪽·네비4종·메일23쪽/일정·소지품·기념일경로 PASS.
- 실제신규한글16ID의글꼴CPU/OBJ픽셀과4248픽셀지움 PASS,64스크린직접검토. 슬롯고정가정검사기는v2로보완했고게임ROM변경없음. 남은일본어/환영문구겹침/한글자동조합·저장통합등미완료유지.
- 권위 **`analysis/pending500_032_v1/batch_status.json`**, 다음 **`analysis/PENDING_INSERTION_500_032_HANDOFF.md`**. 아래152source-only준비기록은과거상태이며그152개도이번500개에포함해반영됐다. 032selectedIDs재반영금지,cumulative032.scope부터재개. 현재진행중세션없음.

## 2026-10-16 — 최신031 ROM 유지 /032 날짜·기념일152개 사전 검증

- 실제 적용 ROM은 `poc/output/pending500_031_v1.gba`, SHA256 `d8c60b15b23ab27f72158243aa863aa071db25462e588834b5fe726e49d00227`,누적16,622개. 이번032 준비에서 신규 ROM적용0개/패키지0개.
- 21일정아카이브의 미적용 일본어513개를 식별했다. 전체게임잔여수는 아니다. 날짜·요일1,500 CPU조건과 실제031기념일10글자입력/21바이트등록/삭제51의5버퍼·글꼴·OBJ픽셀·예/아니요 PASS.
- 날짜·기념일152개/38스크립트/19아카이브의 기존한글초안 구조·원문보존·왕복컴파일/34글꼴검증 PASS. source-only이며031누적번역을포함하는ROM아님. 500개묶음반영을위해348개추가안전후보가필요하다.
- 현재사전검증 `analysis/pending_insertion_500_032_preflight_v1/status.json`. 다음 상세기록 **`analysis/PENDING_INSERTION_500_032_HANDOFF.md`**. 실제완료ROM권위는031batch_status유지. 원본/이전ROM/저장/번역/패키지보존, 새BPS/xdelta/ZIP금지 유지.

## 2026-10-13 — 가운데점 지원 ROM 및 다음500개 준비

- 현재 ROM `poc/output/exe45_ko_development_middle_dot_v1.gba`, SHA256 `bd16c794be18178e84e0d473c0faff43c78eb1d492f8c7b9137265ff5aef3f0c`. 누적5,837개 유지/신규 번역 적용0개.
- `·` 인코딩11173/normal 글꼴 공급 추가. 기존 쉼표11172/전체 한글·모든 번역 페이로드 보존. 자모 mapping은 기존 identity를 유지하면서 한 칸 이동하며 mixed 표시 후보도 동기화했다.
- 독립 재빌드/선택기3,195조건/혼합 표시380 CPU조건/정상 초기 설정·첫 메일23쪽/격리 가운데점의 실제 글꼴·OBJ 화면 픽셀 PASS.
- 다음500개는 미등록 아카이브249개만으로 불충분해13개 기존 부분 적용 아카이브의 미적용 script를 선정했다. source-only 사전 검사 PASS지만 ROM 적용0개. 기존 번역 및 소비 profile/특수 구현을 보존하는 누적 병합이 먼저 필요하다.
- 가운데점 보류19문구는 encoding gap만 보완됐고 아직 ROM 미적용. 새 BPS/xdelta/ZIP 없음. 다음 상세 기록 `analysis/MIDDLE_DOT_HANDOFF.md`.

## 2026-10-13 — 묶음006 신규500개 실제 ROM 반영 완료

- 현재 ROM `poc/output/exe45_ko_development_pending500_006_v1.gba`, SHA256 `02d14a3ead55aa2d52f9458b095384c50c7c92683f82ae08a685c794bb8edc69`,5,837개/주270아카이브.
- 기존 초안500개/87 raw 아카이브 반영. 기존 주 및 별도 소비자 source-ID 제외, 원문 명령·숫자·줄 수 및 번역 단어·순서 유지.
- 준비v1은 `7A7000:0:1`의 미지원 `·`에서 거부됐다. 입력을 치환하지 않고 미지원 문구19개를 기록, 해당 script 전체를 제외해 준비v2로 정확한500개를 다시 구성했다. 7A7000 script0은 원본대로 보존.
- 실제500-ID 추가/이전183개 주 및 모든 별도 페이로드 보존/독립 재빌드 동일/누적 감사/3,195 CPU조건/정상 초기 설정·첫 메일23쪽 PASS.
- 실제 넘버맨8 상태에서 복귀2리터럴·무승부2리터럴의 격리 대기/글꼴/OBJ 화면 픽셀/지움 PASS. 자연 패배/무승부·보상/저장 증거 아님.
- 다음 작업 `analysis/PENDING_INSERTION_500_006_HANDOFF.md`. 가운데점 지원, 이전4미해결/장비 실화면/한글 조합·저장 미통합 한계 유지. 새 패치 패키지 없음.

## 2026-10-13 — 묶음005 신규500개 실제 ROM 반영 완료

- 현재 ROM `poc/output/exe45_ko_development_pending500_005_v1.gba`, SHA256 `ed3b526e6b5b11e9c68c6d26562784d97aa69f5ee617bb1d83fac8ef3a685bea`,5,337개/주183아카이브.
- 기존 미적용 초안500개/31 raw 아카이브 실제 반영. 기존 모든 소비자 source-ID 제외, 원문 명령·숫자·줄 수 및 번역 단어·순서 유지.
- 실제500-ID 추가/이전152개 주 및 별도 페이로드 보존/독립 재빌드 동일/누적 감사/3,195 CPU조건/정상 초기 설정·첫 메일23쪽 PASS.
- 신규 통신 오류3리터럴 선택 커서 이동과 아쿠아맨3리터럴은 격리 화면/글꼴/OBJ 픽셀/대기·선택 포인터·페이지 지움 PASS. 실제 통신 오류 발생·선택 확정·보상/저장 증거 아님.
- 다음 작업은 `analysis/PENDING_INSERTION_500_005_HANDOFF.md`. 이전4미해결/장비 실화면/한글 조합·저장 미통합 한계 유지. 새 패치 패키지 없음.

## 2026-10-13 — 묶음004 신규500개 실제 ROM 반영 완료

- 현재 ROM: `poc/output/exe45_ko_development_pending500_004_v1.gba`, SHA256 `9492ab8b6ba422ad629784e312a990c0683f43983d6e504f9f3699bdd79ef427`,4,837개/주152아카이브.
- 기존 초안500개/27 raw 아카이브를 단어·순서·숫자·명령·줄 수 변경 없이 적용했다. 주 및 모든 별도 clone의 기존 source-ID를 선정에서 제외했다.
- 실제500-ID 추가/기존 누락0/이전125개 주 및 모든 별도 페이로드 보존/독립 재빌드 동일/누적 감사/3,195 CPU조건/정상 초기 설정·첫 메일23쪽 PASS.
- 실제 넘버맨8 선택 상태에서 신규 알림6리터럴의 pointer/table read alias 화면 진단 PASS. 자연 발생·날짜·대회 진행/저장 증거 아님. 원래 넘버맨 초상/상태는 유지되며 진단 체크포인트는 격리돼 있다.
- 다음 작업은 `analysis/PENDING_INSERTION_500_004_HANDOFF.md`에서 이어간다. 이전4미해결/장비 실화면/한글 조합·저장 미통합 한계 유지. 새 배포 패키지 없음.

## 2026-10-13 — 묶음003 신규500개 실제 ROM 반영 완료

- 현재 누적 ROM: `poc/output/exe45_ko_development_pending500_003_v2.gba`, SHA256 `2cddc59ca723ce789c7e935a09ab1742c5a347df41583224fb07c78394c26f04`,4,337개/주125아카이브.
- 기존 미적용 초안500개를 실제 적용했다. 장비39+스타맨6+다른raw455. 이미 공통 이름으로 표시되는 장비111별칭은 신규로 세지 않았다. 이전 이월160=111별칭+이번45+미해결4다.
- 독립 재빌드 동일/source-ID 실제500개 추가/기존 모든 페이로드 보존/선택기3,195 CPU조건/누적 감사/정상 초기 설정·첫 메일23쪽/거츠맨 장비 안내3종의 ROM→글꼴→OBJ 픽셀 PASS.
- 전체500개의 자연 진행·보상·저장 QA, 파이어맨/블루스 장비 실화면 및 오류70..75는 아직 미검증. 한글 조합·저장 ABI 미통합. 새 패치 패키지 없음.
- 다음500개 선정 시 이번500 및 기존 적용 ID를 반드시 제외한다. 상세 계약/명령/근거/미해결4는 `analysis/PENDING_INSERTION_500_003_HANDOFF.md`.

## 2026-10-13 — 500개 실제 반영 완료 및 재개점

- 현재 누적 ROM: `poc/output/exe45_ko_development_pending500_002_v1.gba`, SHA256 `25c04c4e04dd92c1a1a8d9a6f977ee6631c9a8ec16eed468381f2ecfac3cf6a4`,3,837개.
- 이번500개 실제 반영/독립 재빌드 동일/기존 번역 보존/1,072 CPU조건/정상부팅·첫메일·추가페이지 대표 검사 PASS. 전체 자연 진행·보상·저장 QA 미완료.
- 기존 장비153+내비7은 보존·이월했으며 이번500은 메일340+다른raw160이다. 세부 기록과다음500 재개점은 `analysis/PENDING_INSERTION_500_002_REPARTITION_HANDOFF.md`.
- 아래 적용0개 기록은 이전 관찰 시점의 역사 기록이다. 새 BPS/xdelta/ZIP은 생성하지 않았다.

## 2026-10-13 — 500개 단위 실제 ROM 반영 요청

- 사용자 요청: 번역/사전 검사만 반복하지 않고 500개씩 실제 누적 ROM에 반영한다. 별도 패치 패키지는 재요청 전까지 만들지 않는다.
- 현황: 묶음002의500개를 선정/컴파일했으나 실제 ROM 적용은0개다. 누적 ROM은3,337개 적용본 `poc/output/exe45_ko_development_pending500_arrow_v2.gba` 그대로다.
- 진행 근거: `analysis/PENDING_INSERTION_500_002_HANDOFF.md`, r4 준비 검사, capacity_v2 감사/CPU 검사.
- 완료 기준:500개 주 빌드 통합→원본 기반 누적 ROM→독립 재빌드 및 소비 경로별 테스트. 파일에 문자열을 넣었거나 CPU bench가 통과한 것만으로500개 적용 완료라고 세지 않는다.
- 남은 핵심: 장비 공통 텍스트의 이미 분리된 ROM 복제와 내비별 정상 대사 경로를 함께 등록/검증한다. 압축 포인터만 변경하거나 근거 없는 RAM 용량을 선언하지 않는다.

## 2026-10-13 — 신규 윤문 스킬 입력 계약 점검

- 유형: gap
- 관찰: 기존 GBA 프로젝트는 `project.json`/원본 고정 JSON 초안/소비 범위 registry를 사용한다. gt-text-translate의 `PROJECT.md`, canonical TSV, glossary 및 플랫폼 어댑터 입력 계약은 현재 프로젝트에 없다.
- 영향: 해당 스킬에 의존하는 신규 문구 윤문/TSV 병합은 수행하지 않았다. 기존 초안을 조용히 새 canonical 입력으로 선언하거나 포맷을 일괄 이주하지 않았다.
- 결정: 기존 GBA 후속 ROM/표시 구현은 create-kr-patch와 현재 검증된 JSON 체계로 진행하며, 이번 세 문구는 **말을 고치지 않고** 명시적 줄/페이지 배치만 조정했다. 새로운 번역 작성으로 세지 않는다.
- 증거: `translations/pending_insertion_500_002_pages.json`, `tools/pending500_002_pages.py`, `tools/test_pending500_002_pages.py`.
- 상태: open — 신규 번역 프로세스 이주는 별도 계약 검증이 필요하며, 현재 기술 작업을 완료 또는 승인으로 승격하지 않는다.
