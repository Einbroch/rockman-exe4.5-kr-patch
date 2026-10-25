# 035 동일500개 native caller 판별 수정 — 정적/CPU·격리 GBA 표시 PASS, 자연 NPC 선택 검증 중

## 최신 후속 결과

`PENDING_INSERTION_500_036_SOURCE_HANDOFF.md` 참조. 035자연NPC선택은여전히미완료이나반복충돌조사와분리해다음500개의소스준비검사만완료했다(ROM적용0/게이트해제아님). 중앙계단접근은원본799314:0 item0수험표검사와실제799314:8 안내로식별. 현재정상state `pending500-035-fixed-green-route-v14`,(-176.25,56,0),대화닫힘. 추가14정상segment/누적36별도실행,모든명령종료. 현재ROM/누적18,622 그대로.

## 2026-10-19 추가 검증 — 현재 권위

- **종료 시점:** 위/아래의 전투 진행 중 기술은 완료로 대체. 전투 v2 정상종료(53action,HP80), 후속 정상 route-v5/v6도 완료. 현재 정상 checkpoint는 `poc/runtime/pending500-035-fixed-coordinate-route-v6/checkpoint.mss`/동일폴더 `result.json`, 좌표(142.75,-144,0), 대화창 닫힘. 새 `normal_field_progress_v2.json`은 추가8개 segment의 receipt/artifact/parent/checkpoint hash 검증 PASS. 7개필드에서source79D650 원문2,127bytes 일치; route-v4는실제전투중이므로필드payload residency주장에서제외. cached 정상호출0은변함없음. 원본/주ROM/재빌드SHA 재확인, 실행중Mesen/명령/브라우저없음.
- 경로 재평가: actorABB8는이동중이며현재(132,-220) mode0/script0. 현재redbridge끝에서NW직진은충돌한다. 참고Internet1지도에는red/green통로가분리되어있으므로이곳에서직진/미세이동반복금지. 입구의정상 `...-program-v2` 또는 `...-inner-v7` checkpoint에서green통로접근을계획할수있다. 지도는위링크,이번숨긴IAB탭열람후닫음. 자연선택은여전히미검증이다.
- 새 도구/보고서 `verify_native_npc_mode_035_v1.py`→`native_mode_display_v1.json`, `verify_field_progress_035_v2.py`→`normal_field_progress_v2.json` 고정. 후속 수정은 새 버전으로 한다. 036 선정/새500 ROM적용은 이번에 진행하지 않았다.

- ROM035_v2와 누적18,622개는 그대로다. 새 번역 ID0, 배포 패키지0. 아래의 cached 호출0/화면 미검증 기술은 **이전 시점**이다.
- `native_mode_display_v1.json` PASS: 실제 source6EDEC→4F764→4F76E→교정 selector(LR4F773)→79D650 ROM clone→글꼴 CPU 읽기→OBJ VRAM→화면 픽셀 연결 확인. 두 문구 `79D650:1:0`, `79D650:1:1`을 닫기/재열기 포함 네 페이지로 검증(92 glyph occurrences/12,624 pixel comparisons), 이전 페이지 지우기·닫힌 뒤 text OBJ 비활성·실제 필드 이동 PASS. emulated selector cycles70,470/70,474; 전체9개 worst-case/hardware/audio 검증 아님.
- **증거 한계:** 정상 자체 부팅에서 실제 해제된79D650 원문2,127bytes/actor와 source caller를 유지하되, actor0200AAE0의 +9C mode1을 source0806EDEA에서 읽는 순간에만0으로 반환했다. ROM/RAM의 actor mode는1 그대로. 이 actor-specific mode 획득 조건만 우회한 진단이며 **정상 NPC 선택 증거가 아니다**. `diagnostic_checkpoint.mss`로 격리, normal origin으로 재사용 금지. 해당 receipt의 일반 field_observation 문자열보다 scope/mode_alias와 검증 보고서가 정확한 분류다.
- 새 도구 `capture_field_loader_035_v7.py`는 source4F764 진입 레지스터 관측만 추가. 정상 공통NPC는 r0=0/r1=1/r5=0200AAE0/LR0806EDF1. source6EDE6에서 script=actor+1C,6EDEA에서 mode=actor+9C,6EDEC BL4F764 확인. 후보 cached actorABB8(mode0/script0/좌표140,-220), AD68(mode0/script20), AE40(mode0/script30); 전체 actor population 확정 주장은 아님.
- 정상 좌표 접근 v1~v4 완료. v4에서 (-144.25,190)→(175.75,190)로 빨간 다리 통과 후 (175.75,166)에서 랜덤 전투 발생. `pending500-035-fixed-coordinate-battle-v2` 정상 버튼 전투 segment 진행 중. v1 실행은 capture54 범위 오류로 에뮬레이터 시작 전 거부; 완료 증거에서 제외. 사용자의 mGBA에는 접근하지 않았다.
- 다음: 전투 종료/정상 state를 확인한 뒤 worldX140 근처로 정렬하고 cached actor(140,-220) 접근. 자연 선택0/진단 cached2를 혼합하지 말 것. 현재 baseline의 변경 경로 표시 검증은 확보했지만 전체500/자연선택/저장/출시는 미완료다.

## 2026-10-19 이번 실행 종료 시점

- 주/독립재빌드 모두정상종료,두ROM의SHA `41fdee5673329c00f80989e5de2d98db6b3b0980c9a30c5e4b8202fd8dd4d95d` 바이트동일. `integration.json` 전체정적/재현PASS, `integrity.json`26손상거부PASS. 실제caller CPU2,333/ABI CPU2,841PASS. 새번역ID0/같은500개/누적18,622 유지.
- `normal_field_progress_v1.json`: 수정제품자체freshboot 1/4 오전9시→route→battle→approach→정상필드14segment/선정원본79D650(2,127bytes)실제해제전체일치.13화면직접관찰. **cached4F76E관측0,공통RAW4F780관측1**. 실제새clone의native NPC폰트/화면·재진입·timing은여전히미검증. 이결과를전체500 GBA PASS로승격금지.
- 입구MrProgGreen/NightOfficialNavi는공통RAW 대사를쓴다. 안내판은다른RAM root0203C800/source799314로일본어미번역이남아있음(이번9NPC와별도). 다른NPC나주간상태를봤다는이유로cached경로라고추정하지말것.
- 최신수정제품정상상태 **`poc/runtime/pending500-035-fixed-daytime-v2-inner-v7/checkpoint.mss`**,origin동일폴더result.json. 대화창닫힌필드,입구플랫폼에서북서쪽/센터입구근처. 공통대화·안내판닫기후대각이동에서충돌/경로불확실. 부모state들은모두동일수정ROM. 모든shell/에뮬레이터명령종료,진행중세션없음.
- 지도참고 https://www.therockmanexezone.com/game-guides/mmbn4-5-map-guides/ 의Internet1이미지를웹/숨긴IAB에서확인후탭닫음. 지도는후보경로일뿐실제NPC획득/조건증거아님. 사용자mGBA변경없음.
- 다음은무작정일반NPC/안내판을더보는대신 **source4F764 진입의실제 r0/r1/호출자와 NPC선택원천을관측**하여cached호출조건을확정. 필요한경우source로입력·호출·복귀계약을입증한진단만격리해원본해제→native4F76E→새selector→글꼴/페이지를연결하고,우회한actor/요일획득조건은별도미검증유지. 임의flag/PC/RAM주입·옛ROM상태재사용·unknowncaller전부허용금지. `verify_native_npc_display_035_v1.py`는그관측이실제로만들어진후에만실행(아직미실행도구).
-035v1도오류증거로보존. 최신권위는035v2 batch_status. 아래진행중세션기술은과거단계이며현재모두종료. 036/다음500선정으로아직넘어가지않았음. 패키지생성없음.

현재 권위: `analysis/pending500_035_v2/batch_status.json`. ROM은 `poc/output/pending500_035_v2.gba`, SHA256 `41fdee5673329c00f80989e5de2d98db6b3b0980c9a30c5e4b8202fd8dd4d95d`, 12,503,760bytes/누적18,622개. 새번역ID0, 이전035의500개 유지. 기존ROM/v1/원본/저장/배포자료 보존. 새 BPS/xdelta/ZIP 없음.

## 원인과 교정

- 원본 cached NPC 함수4F764에서4F76E의Thumb BL은4FB4C를호출하고LR4F773을 만든다. v1 selector는BL주소|1인4F76F를잘못허용해실제호출을전부fallback한다.
- 원본caller명령부터실행하는 `native_caller_cause_v1.json`은2,333조건에서기존선택0/교정fixture선택2,295,비대상38fallback을확인. 과거2,832CPU조건은LR직접지정이었으므로실제caller증거로쓰지않는다.
- 새 `field_npc_rom_selector_035_v3.py`는원본BL을검증/디코딩한address+size|1로LR을유도. 같은길이/배치, ROM주소0xBECAC0의literal1byte만6F→73. 번역본문/폰트/압축원본/포인터/loader/모든다른byte동일.
- `field_npc_rom_product_035_v2.py`, `build_development_patch_035_v2.py`, `build_layout500_035_v2.py` 및 `tools/specs/primary035_v2_version.json`으로immutable original에서재구축. 주빌드44917정상종료. 재빌드83976진행중.

## 현재 통과 범위

- `integration_pre_repro.json`: source전체쓰기/헤더/append,034prefix단일stub외보존,기존479소비자bytes·metrics·소유/428primary·304untouched,정확500동일,035v1대비허용1byte외차이0.
- `native_caller_product_v1.json`: 실제수정제품을원본4F764부터실행2,333조건,타깃2,295선택/비대상38보존. CPU-only이며GBA시간·화면증거아님.
- `npc_cpu.json`: 실제최종주소의2,841 ABI/전체255scriptoffset/오염원문/scene/root/caller/변경된시각·sub/이전A3B0·keyitem·mail경로. 옛잘못된LR거부추가. CPU-only.
- `verify_layout500_integrity_035_v2.py`: 실제수정제품26오염거부검사58744진행중(옛LR로되돌린literal포함).

## 실제 필드 진입 조사 및 다음 작업

-035v1 자체freshboot 정상버튼경로16segment,1/4새벽경로 및NPC대화기록은 `native_field_progress_v2.json`. source2E316의전날분기r0=1→A0 source79D108 native2020byte실제로드일치. 새벽blueNPC는공통RAW4F780/script4,아직cached호출아님. 157action단일segment300초실패는보존/완료증거에서제외. 이후bounded정상경로완료.
- `run_field_fixed035_v2.py` 실행13504진행중:035v2 자체freshboot에서정상날짜/시각입력1/4오전9시→route→battle→approach. 이전ROM상태재사용없음. `pending500-035-fixed-daytime-v2-*`만실제수정제품의경로.
- 다음은실제NPC앞정상버튼으로cached4F76E→selectorのLR4F773→clone선택/실제glyph/page/exit-reentry/CPUcycle관측연결. `capture_field_loader_035_v6.py`는읽기전용loader/selector/cycle+9NPC범위글꼴trace이며alias없음.
- 이전새벽NPC접근입력은 `pending500-035-current-day4-talk-v1/v2/v3`의정상버튼레시피만재사용가능(NE70→right20/up12→right14/NE2). 그들의savestate는035v1이므로수정ROM에직접사용금지. 주간NPC위치/대화조건재확인필수.
- 독립재빌드완료후 `verify_npc_product_035_v2.py --rom poc/output/pending500_035_v2.gba --repro poc/output/pending500_035_v2_repro.gba --out analysis/pending500_035_v2/integration.json`. oldchecker는oldguard를기대하므로새버전사용.
-036선정은native교정경로판정후. 자동한글입력확정/저장/재표시·환영graphics겹침·일본어자판/로고/기타미번역·전체의미와사람검수미완료유지. 출시완료/전체500 GBA검증으로과장금지.
