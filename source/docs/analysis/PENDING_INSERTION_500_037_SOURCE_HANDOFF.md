# 037 현재 소스500 준비·왕복·글꼴·실제 안내문 caller CPU PASS / ROM 미반영

## 현재 권위

- **`pending_insertion_500_037_source_only_v2/batch_status.json`**, `preflight_v2.json`이 현재 소스 권위. 정확 **500ID/228script/70archive**, 기존 정규초안 그대로 재사용, 단어·공백·control 변경 없음. NPC363 + 지역안내문(board)137, 모두 문구/라벨이며 기호전용0. 현재036 실제폰트525glyph/원문full binary·번역semantic/control/binary 왕복/미선택script 보존/원문·현재ROM 신원/기존ID·archive 중복0 PASS. 여전히 needs_review, NON-DISTRIBUTION, product admission 아님.
- 현재 실제ROM은 **`poc/output/pending500_036_v1.gba`**, SHA `0d85748e6c8c9b6abd561972f319b2687d6791778092c5ff1e9b15abb868876a`, 누적19,122. 이번 신규ROM반영 **0**, 준비500은 미반영정규초안11,424에 포함되며 그외미선정10,924. 전체게임/이미지 잔여량 아님. 새BPS/xdelta/ZIP 없음. 원본·기존ROM·세이브·초안·모든과거실험 보존.

## 036 추가 검증

- `pending500_036_v1/native_boundaries_v1.json` PASS, SHA `ebcf5b44dca66568280d5a5da7a7f0bf4d03df760948f745b702c9dec8073973`. A1=7AAF94 native1914byte/A3=7B469C native1695byte의실제게임조회/원본LZ77→RAM 결과와, 별도 정상A0 actor/caller를 빌린 selector-read 경계의 전체byte가 동일. 실제4F764/4F76E/LR4F773→036 clone→CPUfont/OBJVRAM/screen, 새10ID/10페이지·선택화면/좌우cursor/B취소/대화닫기/실제이동 PASS. selector63997/56805 Mesen cycles, worstcase·hardware·audio 보증아님.
- 두 실험을 연결한 **qualified boundary composition**이다. 자연A1/A3의지역도달·실제해당NPC/요일획득을검증한것이아니며기존bool false 유지. 모든diag state는diagnostic_checkpoint.mss/normal eligibility false. 현재정상재개는항상 **`pending500-036-sunday-natural-npc-v2/checkpoint.mss`**, 동일origin result.json, HP100/대화닫힘/175.75,146,0. 다른이번탐색branch를정상목표checkpoint로잘못선택금지.
- `native_boundary_contact_v1.png`14스크린직접검토, `agent_native_boundary_visual_v1.json`. 대사창의Yellow/Black는원본A1/A3 script portrait,배경Green는빌린A0 actor. 실제패치의캐릭터변경/자연A1/A3화면이라고보고금지.
- 최초 `qualified-native-a1-v1` 전체연결시도는원본조회/LZ는성공했으나강제첫튜토리얼진입으로selector0, **실패그대로보존**. A3-load-v1도load-only종료라전체연결실패상태유지. 네개읽기반환값(첫NPC표조회scene/sub/weekday와selector scene)만격리별칭,ROM/RAM/flag/actor write없음. 별도native-boundary-a1/a3는이미검증한decompression전체byte와동일한비영속read alias만주입,actor/script/mode/원래BL/LR/initializer/parser/font자체실행.
- 부수정상탐색 `shared-link-return-pet-v1`은R플러그아웃기본No인상태에서A만눌러복귀못함. v2는R/left/A로Yes후다음A에서PET로복귀. 첫전투후후속대사에서A다수를누르면친구이름편집기로들어가므로 `shared-link-home-v2`를검증seed로쓰지말것. 기존완료정상state에서portal역주행한 `shared-link-field-portal-v1`은랜덤전투진입,프로그램오류아님. 모두보존/사용자mGBA미접근.

## 소스500 선택을 조정한 이유

- 최초037 source-only v1도500/89archive/257script·549glyph 왕복PASS였지만클래스가 NPC363/board46/hint69/tournament21/reference미해결reward1로분산. `v1/loader_classification_v1.json`에실제불확실성보존. Reward7794EC는256script/직접ROM-pointer word미발견,실제caller/root 미해결. Silver대회6E93C8는254script/root02024000/별도47958reader. Hint69에는A3 Navi21/22 및NPCtable이null인A4 hinttable이포함되어자연획득을추정불가.
- 더좁은소비자집합에서500을구성할수있어 **v2로91ID 교체,409ID 유지**. 기존미해결문구를게임범위에서빼거나번역을고친것이아니며,이전500도ROM미반영이었다. 신규500선택은NPC363+board137만. v1/v2 두500을합산·중복적용하지말것. 현재선택500은v2뿐.
- `prepare_source037_v2_version.py`/`tools/specs/source037_v2_version.json`은고정v1의정확기계적버전변경과필터/boardlookup추가. `prepare_compile037_v2.py`는고정엄격compiler의import/self identity만변경,wording/guard/ID/offset/roundtrip 기준완화없음. `compile_v1`은v2폴더안의출력이고 `verification_v1.json`이엄격컴파일보고서다.

## 중요 — 안내문 실제 caller를 NPC와 혼동하지 말 것

- **`preflight_v1.json`의 board4F780/4F785 주석은잘못된추정이었다.** 4F780는공통RAW NPC의BL이며rootC800 cached board가아니다. 기존보고서는보존하고 `verify_source037_v3.py`/`preflight_v2.json`에서원본바이트/디스어셈블로수정. ROM작성·승인 전에발견되었고어떤ROM에도잘못된guard를넣지않았다.
- 실제확인된board entry **0806A4FC**: push → ldr r0, literal **0203C800**(source6A50C) → **ldrb r1,[r5,#4]** → source **BL0806A502→4FB4C**,실제복귀 **LR0806A507**,이후r0=0/pop. source와현재036의그범위동일. 모든possibleboardcaller완전성으로일반화하지말것.
- **`board_caller_cpu_v1.json` PASS/190조건**: 새board9archive의모든유효script에대해원본6A4FC부터직접실행,실제BL/LR/root/원문script offset/컨텍스트216/레지스터/CPSR/원문RAM·canary보존을원본과actual036비교. 제로필216 helper090C만명시모델링. 새037번역/GBA실행/게임분기증거아님.
- NPC363은sceneA1/A2/A3,root02039800/script0..254/native4F764→4F76E→LR4F773. Board137은sceneA0/A1/A2,root0203C800이며작은script count/다른caller 계약이다. 다음hook은각자의원본BL에서LR을유도하고type별script bound를적용해야한다. clone확장때nativeRAM을늘리거나원본압축을덮어쓰지말것.

## 다음 작업

1. v2입력500의registry/scope/현재폰트metrics/원본과미선택범위/기존036모든소비자 보존을제품입력으로등록. 원본이미지에서만재구축.
2. 새NPC(A2 포함)와board두class에대한단일composed install stub/이전036 wrapper chain ABI를설계·소스실제caller CPU로검증. 잘못된LR/scene/root/script/원문identity/메타손상거부. source-only PASS만으로build admission주장금지.
3. 새037 primary와독립재빌드,전체expected writes/append/이전전체소비자/정확500delta 감사 후실제037에대해서만native대사·페이지·선택·취소/닫기/재진입/이동을검증. 새BPS/xdelta/ZIP은명시요청전생성금지.

현재우리명령/격리Mesen은모두종료. 원본/036주·재SHA재확인동일. 한글자동조합→확정→저장→재표시/일본어자판·로고/환영이미지겹침/전체의미·시각사람승인은계속미완료다.
