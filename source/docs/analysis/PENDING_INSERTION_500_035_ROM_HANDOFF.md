# 035 신규500개 실제ROM 반영·재현성/정적/기존경로/표본화면 PASS — nativeA0 선택 실행 미완료

> 2026-10-19 재개 조사에서 v1의 NPC guard 오류 확정. 실제 Thumb BL4F76E의 LR은4F773인데 v1은4F76F를 검사했다. 아래 CPU2,832는 직접 지정한LR 조건의 과거 검사이며 실제 caller 성공 증거가 아니다. 현재 상태는 `batch_status.json`; 원인/교정CPU 비교 `native_caller_cause_v1.json` 및 정상 필드 획득 `native_field_progress_v2.json` 참조. 같은500개를 유지한035_v2를 immutable source에서 주/독립 재빌드 중. 아직 v2 완성/실행 통과로 보고하지 않는다.

## 현재 실제 산출물 / 권위

- ROM `poc/output/pending500_035_v1.gba`, SHA256 `41c598d4d056b76eaacab3b111cadfa4767f2dd584ae729d03cfe09b0b859bdd`, **12,503,760bytes / 누적18,622개(+500)**.
- 독립 `poc/output/pending500_035_v1_repro.gba` 바이트 동일. 원본SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 재확인. 원본/034/이전자료/저장/배포자료 보존. 새BPS/xdelta/ZIP 없음.
- 현재 상태 권위 **`analysis/pending500_035_v1/batch_status.json`**. 상태는 `ROM_APPLIED_STATIC_REPRO_NORMAL_AND_DIAGNOSTIC_DISPLAY_PASS_NATIVE_A0_LINK_PENDING`이며 전체한글화/릴리스 완료가 아니다.
- 500ID/160script/9NPC아카이브 =462문구·라벨+38시간차점기호. 새번역500문장을 작성한 것으로 과장하지 않는다. 기존 정규초안의 문구/공백/needs_review 유지,4개 내부LF 배치만 변경. 소스준비의 상세는 이전 `PENDING_INSERTION_500_035_SOURCE500_HANDOFF.md`.

## 채택한 저장/읽기 구현

- 큰 번역을 원본 압축slot이나 RAM에 덮어쓰지 않는다. 원본압축파일/포인터/로더/RAM해제크기는 그대로 두고, 원본 해제payload 신원 사본과 번역raw clone을 ROM 뒤에 추가했다.
- **`field_npc_rom_selector_035_v2.py`**: native cached NPC caller `0804F76E`의LR `0804F76F`,root`02039800`,sceneA0,script0..254를 확인한 뒤9개 source-native payload 전체byte 신원을 검사한다. sourceA0의4sub×7압축slot=28개와의 full/prefix 모호성 없음. 다른 원문/다른scene/root/caller/script는 기존034 reader chain으로 되돌린다. 새 영구RAM0bytes,임시stack32bytes.
- 초기 v1은 현재selector/sub-area로 descriptor를 골랐다. 로드 이후 시각/지역 상태가 먼저 바뀔 경우 불필요한 fallback을 유발할 수 있어 제품에는 미채택.2,775CPU 실험은 보존. v2는 현재selector/sub-area를 읽지 않고 현재 RAM에 남은 원문 신원을 식별한다. 바뀐 selector/sub 상태에도 로드된 원문에 맞는clone 유지/다른19원문fallback을 포함2,832CPU 통과.
- `field_npc_rom_product_035.py`: 입력500/원본·초안·제어·엄격배치 검증,주빌드에서9개TPL을 다시컴파일하고 preflight와 일치 확인. 원본신원/번역/descriptor/code 각1회append. 기존4FB4C writer를 새stub와 합성하여 **writer1개**로 계획. 이전keyitem/A3/B0 구현은 원본에서 생성한 선행component이며 새wrapper가 바깥에서 감싼다.
- `verify_final`은 실제 새stub/새code·descriptor·신원/clone·원본보존을 검사한다. 이전component 검증은 **메모리 내 predecessor-stub view**로 명시적으로 수행한다. 옛stub가 실제로 설치되어 있다는 뜻이 아니다. 독립제품감사는 최종stub의 새code target도 재어셈블해 확인했다.
- `keyitem_rom.npc035.placements`는 배치정보만,`keyitem_rom.npc035.archives`는 literal/metrics 소유기록이다. 기존034finalize를 먼저 수행하고9소비자기록/500count를 추가했다. recursive `layout_records/clones`가 새9개를 찾는다.428기존primary/304원본catalog 유지,기존479compiled consumers+9신규.

## 제품 및 검사 완료 범위

- `tools/specs/primary035_version.json`은034→035의5개 정확한 수정점,recipeSHA `862dc5c04fbe96416a678c2625a78ed89ee0ab53fcb281bdd9421ab9e3bcae1a`.
- `build_layout500_035.py`와`--repro`가 각각 immutable original에서 주빌드.034ROM은 비교 oracle뿐,후속ROM 입력으로 복사하지 않았다. 주/재빌드 세션84939/4618 정상종료.
- `analysis/pending_insertion_500_035_npc_inputs_v1/manifest.json`:500source-bound asset/scope/metrics.547글꼴,원문전체/번역literal·control·binary왕복,255offset/미선택script보존.
- `...npc_preallocation_v1/verification.json`: 메모리내append/정확500/기존기록보존/단일stub·7손상거부.034tail은 이 실험 fixture에서만 사용했으며 게임ROM 미출력. 실제 주빌드는 원본 재구축.
- `analysis/pending500_035_v1/integration_pre_repro.json`, `integration.json`: 정확500delta/18,622total,479기존소비자 bytes·rich metrics·ownership 보존,034 전체prefix(설명된12byte stub외) 동일,헤더/원본압축·모든원본참조·전체쓰기·append/유일writer·독립재빌드 PASS. ROM크기 증가61,240bytes.
- `npc_cpu.json`: 실제035최종배치에서2,832조건 PASS. 기존034 chain과 비교하되CPU실험에서 entry stub만 전환. native216byte context clear helper를 모델링했으므로 실제GBA 전체 실행/시간 증거가 아니다. source/copy ROM 사후동일.
- `integrity.json`: 실제035의 기존A3/B0 16+새NPC9=25손상거부 PASS. 일반 악성metadata 완전검증 주장 아님.
-035metadata에 고정된 기존 `.py` **1,796개 모두 hash 재확인**,모두 변경 없음. 이후 새검사도구가 추가됐어도 기존고정파일은 보존. 수리는 새version filename으로.

## 실제035 실행과 직접 화면 검토

- `run_runtime_035.py`: 자체035 coldboot→pagecycle→complete→read→selection,다른ROM 상태 재사용 없음. `normal_runtime.json` PASS: kana3bank/map와overlay,환영/하단graphics상주,Navi4종,첫메일23orderedwait+native3loads+exit/reentry. 네비0(록맨) 유지; 자동한글자판 저장 통합 증거 아님.
- 새NPC clone sample: `poc/runtime/pending500-035-v1-npc-display-{plaza,portraits,weekend}`. `capture_npc_displays_035_v2.py`의 **PET root/script read-alias 진단**이며 checkpoint는격리. PLAZA7A32A8:21 4페이지,79D650:61 4페이지,7A4DD4:30 2페이지.61은 실제source의 무조건 문구/초상변경 구간이며v1의60은시간분기 때문에 사용하지않음(실행실패가아니라미실행초안보존).
- `npc_displays.json` PASS: 신규10ID/10page,원래msgOpen/초상·clear·wait,글꼴BDF→ROMbyte→CPU최소24word읽기→OBJ/화면pixel·3행/180·180·168extent/정확E600wait 확인.
- `agent_visual_review_v1.json`: startup22+mail23+새NPC10=**55화면**,3contact sheet를 실제view_image로 직접검토. 이번NPC10page에 뚜렷한 잘림/겹침 없음,원문초상전환보존. **사람의 의미/표현/출시 승인 아님.** 환영graphics4줄겹침,일본어 자판/로고/입력된일본어이름 등 미완료 그대로.
- `verify_layout500_normal_035.py`는 옛first_mail checker가oldstub를기대하는 경로가 있어 미실행보존. 실제검사는 **`verify_layout500_normal_035_v2.py`→`verify_first_mail_runtime_035.py`**로새합성component 검증을사용. ROM변경 없이 검사바인딩만 새버전으로 정정.

##034에서 조사한 정상 필드 경로(035 신규 NPC 실행 증거 아님)

- `pending500-035-baseline034-weekday-{boot,pagecycle,complete}`은 이름에035가있지만 **ROM034**. 옛022 자료의 입력열만 재사용,034자체새부팅/새상태.2000/1/3 UI→B0홈페이지 진입.
- `capture_field_loader_035.py` v1의 selector관측주소는4D57로 잘못 적혀있었다. loader주소/인수/전체RAM스냅샷은 그대로 유효하나selector값 증거로쓰지않는다. **v2는 source2E434literal=02003D40+0x17=02003D57**로수정. source-native getter는2E42C/2E42E의byte읽기. selector0관측을월요일수치로 해석하거나요일writer로승인하지않는다.
- normal walk-v2→walk-v3→portal-v1→portal-v2에서 source sceneA0/sub0로실제진입. portal-v2는0804F724에서source79CF04→02039800,다른두asset→0203C800/0203D800 기록/동일실행 즉시RAMdump 보존.79CF04는이번9개가아닌510byte 원본이다. 현숫자0을선정9개의로드검증으로세지않는다.
- 이후 internet-intro→tutorial-battle-v1/v2/v3→tutorial-exit-v1은 **정상버튼만**. L1800에서기본공격/전투진행 후메시지/필드복귀 관측. 컨트롤 후보참고로GameFAQs34214/33108 검색결과를봤으며,그설명을제품사실로승인한것아님. 출처후보 https://gamefaqs.gamespot.com/gba/921255-rockman-exe-45-real-operation/faqs/33108 .
- npc-approach-v1..v4로필드이동했으나 **0804F76E/780 관측0회**. 이는 reader가미사용/불필요하다는 증거가 아니다. 마지막034조사 상태는 `poc/runtime/pending500-035-baseline034-npc-approach-v4/checkpoint.mss`(정상ROM034/원문객체,035에그대로사용금지).좌우이동/올바른 ramp는up+right로관측. 새035 정상상태와혼동금지.

## 다음 필수 작업 —036으로 넘어가지 말 것

1. **현재035를 고정한 채**,원본 압축로딩→native cached NPC caller0804F76E→035loaded-payload selector선택→실제새clone/font/page/exit-reentry 및cycle/timing을 GBA에서연결. 현PET read-alias10page는이것을우회했다. static/CPU/기존글꼴증거를반복하며native실행완료로바꾸지않는다.
2. 자연A0 NPC 획득과달력/selector의의미를추가확인. 필요시source로유효성을증명한진단개입만사용하고,요일·scene/객체·script개입이우회한조건을분리한다. RTC/게임진행을맞추려고임의RAM·PC·flags를주입하지않는다. 사용자mGBA는건드리지않고전용격리Mesen직렬실행.
3.035의source/native28개 범위와9개full/prefix분리검사는adoptedfinite계약. 기타scene/비정상clock/importedstate지원으로확대금지. 추가관련callers가발견되면필요한원문/호출범위로재평가,단순unknowncaller전부허용금지.
4. 그다음미반영정규초안재집계/새036 정확500선정. 이전035준비census12,424는이번500반영전수치이며현재잔여량으로재보고금지. `6FE8D4:23:0` 안전후보1개는여전히이번500에미포함.
5. 배포파일은별도요청전생성금지. 자동한글조합→확정→저장→재표시,환영graphics겹침,일본어자판·로고/별도이미지·텍스트,전체의미·사람검수 등미완료유지. 개발용NON-DISTRIBUTION만.

현재 모든주/재빌드·검사·런타임명령이정상종료. 진행중shell/에뮬레이터세션없음.
