# 019 개발 ROM: 실제018 기준500개 반영과 동적 이름 대사 검증

현행 상태: **019 통합 ROM의500개 실제 반영·독립 재현·전체artifact 감사·정상 초기설정/첫메일 회귀와 새 이름 quick-box2개 진단 PASS; 새 이름 전체runtime gate는 미완료**. 새 작업 제품은 `poc/output/pending500_019_v1.gba`, SHA256 `38118847f8deeec0586b7c5b400a9dd15ec32a1875c174657fad3ee8029b8042`,11,922,628bytes,누적10,622unit/398primary archive/334untouched catalog archives다. 아래 이전 ‘새 ROM 없음/통합 전/독립repro 미완료’ 문구는 당시 단계의 기록이며 현행 제품 상태로 해석하지 않는다. 이전018 `poc/output/exe45_ko_development_pending500_018_v1.gba`, SHA256 `a8d39423bbd4792d948af4bea991dd8c56bb6d34dac8c1a7c570f0c3938f3241`은 보존했다. 사용자500개 단위 정책과 새 BPS/xdelta/ZIP 금지 유지.

## 현행019 결과와 다음 재개 지점

### 후속 원래 메뉴/메일알림 재열기

`poc/runtime/pending500-019-v1-name-food-reentry/result.json`은own019 six-complete에서같은food2page진단을재실행후R/B로이어진12action/8capture다. root/table readalias는진입각1회로고정했고step7/8/9/10/11/12에도counter증가없음. R은원래mail-alert65E8B8 script10/root380D0로진입해‘인터넷을 더\n탐색해 보자!’를표시하고B는원래PET65A608/3809C로돌아온다. step008/010/012직접확인. food진단사건을자연적으로재개하는경로가아니며‘한번진단선택한뒤의원래native메뉴/알림재열기’로한정한다.

`verify_cumulative500_019_reentry.py`→`pending500_019_v1/name_reentry_runtime.json` PASS:exactROM/emulator/receipt/artifacthash·격리checkpoint·aliascounter·source/actual원래lookup·nativewait/root/origin·기존owner14동일·PET text crop동일. 새reentryarchive의실제OBJ/화면pixels를ROMfont및literal에서독립계산한배치와대조했다. 이경로의CPU glyph observer는foodroot에만묶였으므로reentry CPU trace verified=false를명시하며계산한drawgeometry를실제CPUtrace로보고하지않는다. 다른내비provider/221개모든profile·자연사건·한글입력/save/humanapproval은남았다.

다음500개조사권위는 `PENDING_INSERTION_500_020_HANDOFF.md`다.019검증을020번역/새ROM반영으로세지않는다.

### 후속 큰 창/페이지 전환 검증

`capture_cumulative500_019_name.py`에source prefix F4002BE700을 지닌66BF44:23 food 진단을 추가했다. `poc/runtime/pending500-019-v1-name-food/result.json`:own019 six-complete checkpoint→B/R→첫대기→A→둘째대기→A→PET복귀,7action/6capture 종료0. native context reset와원래mugshot/msgOpen/name/control을 실행하고 source root/table read alias만 사용했다. caller의Navi0와원래이름호칭은 유지하며 진단script의원래portrait는그대로다. 자연 식사알람/해당내비 사건선택 증거로 세지 않는다. 결과 checkpoint는격리했다.

`pending500_019_v1/full_name_runtime.json` PASS:첫page native6glyph+ちゃん99px/ASCIIcomma12px=111px·‘식사 시간이다’,둘째page‘남기지 말고\n먹어야 한다...’의 CPUfont read/ROMglyph/실제geometry/OBJ→pixels/nativeorigin52,110/keyWait E600F1/빈영역clear 검증. 마지막 A이후 원래Rockman PET archive65A608/실제lookup3809C/root범위/quickorigin92,110 복귀 확인. step003/005/007을직접열어 잘림·겹침·이름잔상 없음을확인했다. 별도 읽기별칭 재진입이나 자연루트/save 검증은아니다.

첫checker는귀환archive를Roll65FA58로가정해실패했다. nativeRAM actualroot를제품catalog/source reference와대조해Rockman65A608/3809C로수정했다. 중간380D0 가정도실패했으며380D0는실험진입mail-alert65E8B8,귀환PET3809C와다르다. 표본root만 허용하는 우회 대신source의 두lookup identity와제품의귀환pointer/extent를검사한다. ROM/문구수정0,실패를PASS로세지않았다. 첫capture CLI의--emulator 오기는argparse에서실행전거부,공식--mesen으로다시실행했다.

`test_cumulative500_019_full_name.py -v`:foreignROM receipt/wrongscript/wrongglyph/wrongwait 4fixture 거부PASS. 원본증거는수정하지않고메모리상의검사입력만바꾸며실패가최종reportwrite전에발생함을확인한다. 다른내비호칭provider·221개전체template·자연식사알람/소개루트·재열기·한글자동입력/저장·인간검수는남았다. 다음은귀환후재열기/새readalias 없는 정상경로회귀와다른consumer 경계확인이다. 신규500개추가/새ROM/새패치생성0;019제품SHA38118847…는그대로다.

`pending_insertion_500_019_cumulative_v1/preflight.json`:133archive/112carry+21new,신규500,221nickname capacity profiles. parent를 기존 consumer scope로 재컴파일해 실제018 payload 동일 재현,병합 후 non-new scripts 동일 보존 PASS. PROFILE019/recipe/roll builder/primary builder의019 flag와018 prerequisite를 연결했다. source-only v3 및 cumulative v1을 소비한 원본 기반 전체 제품 빌드가 종료 코드0으로 완료됐다. 이전 ROM에 직접 덧쓰기하지 않았다.

`pending500_019_v1/lineage.json` PASS:실제 old/new IDs 차이가 정확500,누락old ID 없음,모든carry/new scope·asset·source storage·최종 layout/capacity proof 및 hash-bound build arguments를 검증했다. `selector_cpu.json`:composed mail/keyitem selector ABI3,195 vectors PASS. `normal_runtime_receipts.json`:같은019 새 boot→native keyboard3page→native 입력·초기 프로필→록맨·메일→첫IPC메일 body/list reentry→4native Navi 선택/취소 경로의5segment80capture receipt/hash PASS. source/ROM/RAM alias나진행 flag 주입은 없다. title step002/초기메일 step034/IPC첫body step010을 직접 열어 Korean text와 원래 portrait를 확인했다. receipt 실행 성공은 모든500개 렌더링 검증이나23개 body 페이지의 별도 완전 QA 판정과 같지 않다.

독립 product `pending500_019_v1_repro.gba`가 원본과 같은 전체flags/019에서 종료0으로 완료됐다. SHA뿐 아니라 전체11,922,628bytes 동일 비교 PASS. `pending500_019_v1/integration.json`은 실제500delta/모든133archive 포인터/carry/source storage/Expected Writes/header/ISA/ancestry/repro/합성CPU3,195조건을 검증했다. 첫 감사는 `first_mail.audit_layer`가019 새21archive pointer write population을 아직 등록하지 않아 실패했다. `first_mail.py`에019의parent 없는 명시적source pointer tuple만 추가했다. equality gate/원래expected bytes는 그대로 유지했으며 ROM/번역 변경0. 재실행 PASS이며 이 실패를 제품성공으로 세지 않았다.

`pending500_019_v1/normal_runtime.json`:같은019의native keyboard3페이지 VRAM/map/초기설정,21-name card bank 및4selectable OAM identity,첫IPC메일23개 순서keyWait/3native RAM archive bytes/page bookmarks/목록복귀·재열기 PASS. `first_mail_pages_v1.png`를 직접 열어23쪽의 한글과프레임/화살표/잘림·겹침을 확인했다. 이 정상회귀는 신규500개 자연이벤트 확인이나 한글이름 지원이 아니다.

`poc/runtime/pending500-019-v1-name-six-entry` 및 `...-name-six-complete`:다른ROM checkpoint 이식 없이 own019boot→실제6native glyph 입력/7번째 거부/삭제·재입력/확정→성별1·록맨·메일알림 경로를 controller로 실행했다. owner14 `019d9d9d9d9d9de5000000000000`,nickname `9d9d9d9d9d9dabe406cae5`의6글자‘う’+원래‘ちゃん’9glyph/99px가 남아 있다. 한글 입력/저장 증거가 아니다.

`capture_cumulative500_019_name.py` 및 `verify_cumulative500_019_names.py`→`pending500_019_v1/name_display_runtime.json` PASS:archive65B74C script2 comma111px,6B5A70 script1‘ 님께’131px 두quick-box 페이지. CPU provider/renderer 관찰·native RAM/name/index(E406→234)·ROM glyph identity/font reads·aggregate geometry·OBJ→화면pixels·native E600F1 keyWait·빈영역 이전페이지 잔상 검증. step003/005를 직접 보아 잘림 없음 확인했다. 읽기 전용 source root/table alias 진단이며 ownNavi0 록맨/portrait를 변경하지 않았다. Knight wording의 자연 Knight 소개/토너먼트 우승 이벤트로 보고하지 않는다. 각각 diagnostic_checkpoint.mss로 격리,normal_play_checkpoint_eligible=false;source/RAM writes 없음.

다음 재개 지점은 same019의 새 이름 full-box·최종대기 이후 제어/clear/return/reentry·negative controls,다른Navi/호칭 경계와221개 profile 및 자연 source caller/portrait의 범위 확대다. 한글이름 자동조합/commit/save/redisplay 통합 및 human semantic review도 미완료다. 이 개발본을 release나500개 전체runtime 완료로 승격하지 않는다. 원본/018/기존ZIP SHA는 각각588a77da…/a8d39423…/24404787… 동일 확인. 새patch 없음.

## 실제 잔여 재대조

`pending_insertion_500_019_survey_v1/survey.json`은 source/TPI/고정 draft-first corpus/검증된018의 실제 적용 ID와 연결된다. 고정 초안 변경·누락0. 기존 raw/known-pointer/mmbn45/local-window/비선택지·비변수/3행132px 비교에서23 script/23 unit만 후보였다.

`pending_insertion_500_019_layout_survey_v1/survey.json`은018에서 채택한 same-row word-preserving placement 및 source edge LF/padding 검사까지 적용한 새 결과다. 80 script/86 unit, 신규 untouched 후보21unit. 이는 전체 게임 잔여수가 아니며 아직500개 source-only/cumulative preflight가 된 것도 아니다. 이전586 후보를 현행 잔여수로 재사용하지 않았다.

## 다음 범위: 변수 삽입의 분류

현재 단일 거부 이유가 variable_insertion인1852 script/4978unit을 분류했다. `survey_batch500_019_variables.py`와 `pending_insertion_500_019_variable_survey_v1/survey.json`이 조사 권위다. top-level 한 탭의 print 명령만 세며 `printN = false` 인수는 별도 print 명령으로 오인하지 않는다. 실제 고정 source TPL·초안 해시/ID/source를 대조하고 중복 source-ID의 서로 다른 wording/state는 실패시킨다. ROM·prose 변경0.

nickname만 한 번 삽입하는 후보289script/636unit을 따로 확인했다. 이것도 즉시 삽입 가능하거나 해당 인물의 자연 플레이가 검증됐다는 뜻은 아니다. 다른 변수는 일정명/취미/꿈/학교/좋아하는 칩/상대/동적 버퍼 등으로 분리했고 일반 literal132px 검사만으로 그 결합 폭을 승인하지 않았다.

좁은 구조 모델은 정확한 false/false/false nickname 인수, 앞선 msgOpen/clearMsg, 이름 직전0열(없거나 LF로 끝난 단일 prefix), 바로 뒤 suffix,3행 이내 결합, source edge/padding, 조사 의존 없는 punctuation-only suffix 및 source보다 정적 폭이 늘지 않는 조건을 검사한다. 결과18script/42unit은 **구조상 후보**다. native nickname 값의 최대 폭/제어 state·이름 출력·전체 consumer capacity/compile/단일 writer/runtime proof는 아직 남았다. 86개와42개를 준비 완료128개로 합치지 않는다.

나머지 nickname 단독 script는 suffix row/폭 성장178, 미선택 nonJapanese suffix16, same-row prefix5, 조사/단어 suffix 문맥71, 사이 명령1로 구분했다. 다른/복수 변수1563script도 별도 미해결이다. source command/flag/wait/lookup을 삭제하거나 이름을 고정 literal로 치환하지 않았다.

## 1px 쉼표 경계

실제 기존 공급 정의 `tools/korean_codec.py`에서 ASCII comma`,`는 F9FC extra glyph이며 advance12px다. native `、`의 사용 모델은11px이다. 예:7C802C:7:0 및65B74C:2:1의 원문 첫행 `、`→기존 초안`,`는 의미상 쉼표여도 폭이1px 증가한다. 따라서 현재 non-growing nickname 검사를 통과하지 못한다. 이를 같은 폭으로 취급하거나 원래 초안을 자동 치환하지 않았다. 폰트 metric을 전역으로 바꾸지도 않았다.

기존 `validate_nickname_suffix`는 첫행 동일/명시적 source-target pair 및 비성장 검사를 제공하지만, 이것만으로 모든 nickname 값의 길이나 합산132px 적합성을 증명하지 않는다. player owner14/표시13byte와 nickname21byte, calendar22byte는 서로 다른 ABI다. 21byte buffer라는 사실만으로 표시 글자 수/폭을 추정하지 않는다. source의 실제 입력 길이 제한·인코딩·출력 reader를 확인하고 max-value/경계값 runtime이 다음 구별 관찰이다. 실제 한글 이름 commit/save/redisplay는 여전히 미완료다.

고정 TextPet 정의에서 printPlayerNickname은 base F9 0C 01, plen3이며 설명은 player name 뒤 honorific suffix를 붙이는 출력이다. 이는 native consumer를 확인할 조사 단서이지 디스어셈블/실행 증거 대신 채택한 결론이 아니다. 단순한 owner 문자열 길이만으로 nickname 폭을 결정하지 말고 실제 suffix 생성과 출력 읽기까지 확인한다. 처음부터 이름 ‘あ’ 저장/재부팅을 관찰한 과거 증거도 한 값의 저장 회귀이며 최대 길이/모든 honorific/한글 입력 증거로 일반화하지 않는다.

## 보호 계약 검사와 재개

### 후속: 원래 nickname 생성/읽기 CPU 증거

`tools/analyze_nickname_native_019.py` → **`pending_insertion_500_019_variable_survey_v1/native_nickname_v2.json`**가 현재 native CPU 분석 결과다. 이전 `native_nickname.json`은 E4 continuation을256 기반으로 해석했던 이전 가설의 보존 기록이며 현행 입력으로 사용하지 않는다. 실제 renderer에서 E406→glyph234를 관찰해228 기반으로 수정했다. 기존 glyph advance가 동일해99px 수치는 바뀌지 않았지만 glyph identity 자체는 수정이 필요했다. 원본과 실제018 제품의 해당 코드·literal·descriptor·선택 suffix·legacy width 표가 동일함을 확인했다. 명시한 ARMv4T Thumb 범위의 전체 instruction extent 및 assembler/disassembler roundtrip을 검사했다. 신규 product code나 hook은 만들지 않았다.

- `08038F60`은 `08000CEC` 결과의 두 배에 `08035E62` 결과를 더해 source suffix 표 `0863720C`의 index를 선택한다. 후자는 `02000952` 바이트를 읽는다. 전자의 정상 호출자는 이번 실험에서 실행하지 않고0..20 Navi fixture로 모델링했다. gender도0..1 fixture다.
- owner `02000E50`에서 raw E5 copy를 실행해 marker를 포함하여 `02000E5E`로 옮기고, 원래 terminator 위치부터 suffix를 덮어쓴다. 따라서 descriptor의 `02000E5F`는 marker 다음 글자다.
- `080517D0`의 F90C01 consumer는 실제 descriptor의21bytes를 `02010AC0 + (context+64의 깊이)*128`로 복사한다. 원래 `0800094C` byte-copy 실행, context+5/+2C/+44/+64와 r4의 복귀값도 검사했다. terminator 뒤의 stale padding까지 그대로 복사하는 기존 동작이며 그 padding을 글자로 해석하지 않았다.
- 두 native glyph 표현 `9B` 및 `E406`, 이름 길이0..6,42 suffix 선택을 원본/018 각각 실행했다. writer1,176 + reader1,176회 PASS. 각 단계 전체 EWRAM과 허용 write 범위·SP·복귀를 비교했다. isolated caller evidence이지 정상 플레이/저장 증거가 아니다.
- `08039E2C..08039E66` 초기 이름 경로는 initializer 인수 r0=6, r2=`02000E50`를 준비한다. 해당 initializer 자체 및 실제6글자 입력은 이번 실험에서 실행하지 않았다.
- E406은2bytes/1glyph다. suffix 최대3glyph/33px,441 source glyph metric 최대11px. **6개의 유효 native glyph/선택 suffix0..41 조건**이면 합산 상한99px, 기존 ASCII comma12px까지111px이다. 21bytes를21글자로 보거나 reserved index441을 native repertoire로 세지 않았다. 이 조건부 상한은 모든 입력/임의 save/한글 이름/모든 print flag를 검증한 결과가 아니다.

이에 따라1px 증가를 무조건 overflow로 일반화하는 가정은 배제할 수 있다. 기존 non-growing 빌드 게이트는 그대로이며, 새 aggregate 계약·실제 native 최대 입력/출력 경계·translated page CPU→glyph→OBJ→pixels/keyWait를 확인한 뒤에만 게이트 전환을 채택한다. source 의미/쉼표 metric/초안/018ROM/세이브/BPS/xdelta/ZIP 변경0. 현재 구조 후보42개 및 layout 후보86개의 삽입 승인 상태도 바꾸지 않았다.

### 후속: 정상 입력의6글자 경계와 실제 메일 출력

`pending_insertion_500_019_variable_survey_v1/native_name_runtime.json`이 이 관찰의 자동 검증 결과다. 같은018 정상 boot checkpoint에서 controller만 사용했다. `poc/runtime/pending500-019-native-name-six-v1`에서 실제 이름 자판1..6글자 입력,7번째 거부, B삭제→5글자,재입력→6글자,결정을 캡처했다. cursor/16bit editor body/capacity6을 비교했다. `...-profile-v1`은 정상 성별 선택과 초기 프로필→록맨→메일 알림 경로의 snapshot 기록이다.

`...-mail-v1`에서는 같은 입력 확정 전 checkpoint에서 읽기 전용 observer를 추가해 정상 경로를 재실행했다. RAM/flag/ROM 수정 및 read alias가 없다. `capture_nickname_mail_019.py`는 원래 producer 진입/복귀, F90C01 consumer 진입/복귀, IWRAM renderer와 ROM font read를 기록한다. 실제 owner `019d9d9d9d9d9de5000000000000`, nickname `9d9d9d9d9d9dabe406cae5`, 성별1과 실제 일본어 호칭을 관찰했다. 초기 입력 이름은 일본어 ‘う’6글자이며 한글 입력 증거가 아니다.

`verify_nickname_mail_019.py` PASS: 정상6/7입력 경계·삭제/재입력·commit→원래 이름 생성→21byte provider→RAM glyph stream→ROM glyph read→OBJ VRAM→화면 pixels. glyph16개/2,160pixel을17·18 두 대기 캡처에서 각각 검사했다. name9glyph/99px + 기존 `、`11px = 첫행110px, 한글 `메일이야!!`가 다음행에 표시된다. 같은 keyWait/E600F1 위치, 빈 영역 잔상 없음도 확인했다. `step_018.png`를 직접 열어 이름/일본어 호칭·한글 문구·화살표·프레임의 잘림 없음을 확인했다. 신규 ASCII comma12px 문구, 모든 이름 글자/내비, native save/reset/fresh reload, Hangul 입력·저장까지 일반화하지 않는다.

### 다음 후보의 조건부 합산 폭 조사

`survey_batch500_019_variables.py`의 기본 호출은 기존 비성장 구조 검사를 그대로 유지한다. 새 `--bounded-native-cpu ...native_nickname_v2.json --native-runtime ...native_name_runtime.json --out ...conditional_width_survey.json`은 두 evidence의018 baseline/tool identity와6/7/delete/E4 조건을 검사한 별도 조사 모드다. source/초안/command/edgeLF/column-zero/punctuation-only 조건은 유지하고 첫행 `99px+suffix advance<=132px`만 조건부로 평가한다. 원래 초안이나 제품 빌드 게이트를 수정하지 않았다.

결과190script/322unit **조건부 구조 후보**. 기존42unit 조사 결과를 교체한 현행 조사 모드의 결과이지322개 신규 번역/ROM 반영이 아니다. 다른·복수 변수1,563script, suffix 미선택16, same-row prefix7, 조사/단어 suffix71, 중간명령1, 줄바꿈 없는 suffix4는 남았다. layout86개와도 아직500개 frozen selection/preflight를 구성하지 않았으며 합계를 실제 잔여/준비 완료로 보고하지 않는다. 조건부 쉼표 수용/정확132px 수용/추가 glyph overflow 거부3fixture를 추가해 총8fixture PASS. 현재 완료 조건은 소비 계약 채택·500개 비중복 선택·원본 기반 compile/단일 writer·신규 aggregate 페이지 runtime 및 한글 입력/저장 통합이다.

### 후속: invariant suffix 조사와 정확500개 입력 고정

현행 추가 조사 `pending_insertion_500_019_variable_survey_v1/invariant_width_survey.json`은 `--invariant-suffixes`를 조건부 native evidence와 함께 사용했다. 원래 punctuation-only 모드는 보존했다. 명시한 first-line form은 `의`, `도`, `님의`, `님은`, `님이`, `님께`, leading-space 있는 네 가지 ` 님의/ 님은/ 님이/ 님께`뿐이다. 이름 자체에 직접 붙이는 `은/는/이/가/을/를/과/와/로/으로`는 여전히 거부한다. `님` 뒤의 consonant 조건과 `의/도`의 이름 받침 비의존성이 검사의 구조적 근거이며 자연스러움/원문 의미/호칭 중복의 human approval을 대신하지 않는다. 기존 초안 first line과 이후 원문/한국어 문맥을 대조했다. prose 변경0, semantic_approval=false,needs_review를 유지했다.

추가108unit/33script가 `99+정적 첫행<=132px`, source edge LF/padding, column-zero, 즉시 suffix 및3행 조건을 만족했다. 최종223script/430unit 조건부 이름 후보. 이름 suffix의 `의` 뒤에 LF가 없고 추가 literal이 이어지는 경우, 긴 `말이야/말이다/말입니다`의 폭, same-row prefix는 승인하지 않았다. 모든 나머지 변수 및 source caller/저장 범위도 미해결 상태다. 총11fixture PASS(명시적10형식 수용, 이름 받침 의존10형식 거부, native bound 없는 invariant 모드 거부 포함).

`tools/select_batch500_019.py`가 위 조사와 layout86unit을 same018 baseline/고정 parent hash로 결합했다. 516개의 상호 비중복 구조 후보 중 **500개 조건부 계획**을 고정했다. source의 전체 script 단위를 유지하고018 실제 layout ID와 겹치지 않는 것을 검증했다. `pending_insertion_500_019_selection_v1/combined_survey.json`, `selection.json`, `translations/pending_insertion_500_019_layout_v1.json`가 고정 입력이다. 선택133archive, 이름221script/428unit + 일반72unit, same-wording 명시적 placement44unit. 이는 새로 번역한500개나 compiler-admitted500개/ROM 반영 결과가 아니다.

`tools/prepare_batch500_019_inputs.py`가 고정 selection에서 native literal 순서로 `pending_insertion_500_019_inputs_v1/`에133archive/500개 한국어 초안을 materialize했다. per-unit parent path/hash/ID/source를 유지하고 원래 초안은 변경하지 않았다. `inputs.json`에 consumer_admission=false와 미완료 gate를 명시했다. `tools/audit_batch500_019_inputs.py` → `protected_input_audit.json` PASS:500 IDs 비중복/018 미적용, 원본 TPL/source identity,needs_review, LF/edge/padding,44개 정확 같은-wording placement, static3행132px,전체 unselected literals와 command/argument/order skeleton 보존. TPL substitution 검사이며 TextPet binary compile/roundtrip/제품 preflight가 아니다.

**현재 재개 지점:** 고정500개 입력에서 nickname capacity profile을 source-only compiler와 누적 단일-writer 경로에 등록하고 검증해야 한다. 기존 non-growing profile을 무조건 끄지 않는다. 새 conditional native6/호칭0..41 계약은 원래 command/parameter·column-zero·page와 source bytes에 묶여야 한다. compiled binary/unselected scripts·parent 재현·carry metrics·신규 root/Expected Writes·normal/quick renderer 결합 페이지·negative controls를 통과한 뒤 원본 기반 전체019 ROM과 독립 repro를 순차 빌드한다. 기존500묶음018/원본/세이브/패키지는 그대로며 아직019 ROM/패치 없음. 한글 이름 입력·저장 지원 통합과 인간 의미/화면 승인은 여전히 별개 미완료 조건이다.

### 후속: source-only compiler 검증 완료, 누적 통합 전

후속 상태 변경: **누적 compiler preflight도 완료했다.** 아래 source-only 결과와 별개로 `pending_insertion_500_019_cumulative_v1/preflight.json`이133archive/신규500unit/기존112+새21의 통합 결과다. `PROFILE019` 및 `cumulative_batch500_019.py`, 기본 recipe/roll builder/primary builder의 `--pending-batch500-019`를 등록했다. 누적 scope에221개 nickname capacity profile를 연결했고 parent 재컴파일에서는 새 script profile만 제외해 기존 소비 계약으로018 payload를 동일 재현했다. 새 병합 후 미변경 script byte 보존도 전부 PASS. 018 부모 단일 writer를 명시적으로 선택하고 이전 read-only provenance는 writer로 취급하지 않았다. 새019 없이 이전 flags의 동작은 유지한다.

누적 denominator3fixture 및 nickname capacity7/template11fixture PASS, 관련 Python syntax PASS. 전체 빌드는 원본에서 `build_keyitem_full_rom.py --name pending500_019_v1`에 기존018의 전체 flags와019를 추가해 시작했다. 출력 목표는 `poc/output/pending500_019_v1.gba`, 작업 폴더는 `poc/build/pending500_019_v1`이다. **빌드 시작은 성공/ROM 반영 확인이 아니다.** 빌드 완료·독립repro·Expected Writes/lineage·CPU·동일제품 화면 검증까지 최신 검증 제품은018이다. 새 배포 patch는 만들지 않았다.

**현행 source-only 결과는 `pending_insertion_500_019_preflight_v3/preflight.json`**이다. `tools/prepare_pending500_019.py`가133archive/정확500unit을 기존 `compile_archive`로 컴파일했다. 원본 payload→TPL→동일 binary, 한국어 TPL→binary→동일 decoded literals/command skeleton→동일 binary,16bit archive extent,unselected scripts byte 보존 모두 PASS. 고정 selection/layout/parent source hash를 유지했다. 모든221개 이름 template를 실제 source TPL 및 최종 translated TPL에 대조하고 compiler가 검사했다. 최종 ROM 작성은0이며 이 결과 자체를 playable ROM으로 취급하지 않는다.

채택한 개발용 검사 구현은 `tools/nickname_capacity.py`이며 `build_development_patch.compile_archive`가 명시한 `nickname_capacity_profiles`가 있을 때 호출한다. source revision·선언한 원래 code ranges/literals·21byte descriptor·42suffix bytes를 대조하고, 실제441 source glyph metrics와 suffix 해석(E4 continuation228 기반)으로6glyph 상한을 매번 계산한다. nickname command 정확false/false/false 인수,단일 print population,pinned source/target first line,직전 page reset,0열 또는 LF로 끝나는 단일 prefix,즉시 suffix,source literal ID,3행132px를 검사한다. suffix 다음의 같은 페이지에 예상하지 않은 추가 literal이 있으면 실패한다. 기존 nickname 비성장 게이트는 수정하지 않았고 기존 profile의 metadata 결과에는 새 필드를 추가하지 않았다.

이는 **native6glyph 이름 및 원래 호칭 공급의 개발용 계약**이다. 새로운 한글 이름 format/provider/길이 제한/hook을 설치하면 source/native provider 조건을 재평가해야 한다. 한글 입력·저장 기능이나 모든 caller/임의 save를 이 검사로 승인하지 않는다. 새 이름 template의 `nickname_capacity_proof`에는 runtime_verification_pending=true를 남겼다.

7개 compiler-capacity fixture PASS: comma1px 성장 수용/132px 정확 경계/overflow 거부/추가 same-page literal 거부/이름 받침 의존 조사 거부/명령 인수 변경 거부/source first-line 불일치 거부. 기존 codec6개 및 template11개도 PASS. 첫 v1/v2 시도는 analyzer의 literal.end 속성을 메서드로 호출한 도구 오류로 중단됐으며 실패 디렉터리를 보존했다. 속성 접근을 고친 뒤7 fixture를 다시 통과하고 새v3 위치에서 전체를 실행했다. source protection나 capacity gate를 완화해서 실패를 숨기지 않았다.

**다음 재개 지점은 누적 통합이다.** PROFILE019/source batch link 및 primary flag는 아직 등록하지 않았다. source-only preflight의 `nickname_capacity_profiles`를 새 literal profile/누적 scope로 옮기고 selected_scope 허용 필드·parent 재현·carry old metrics/metadata·all old IDs·단일 writer/Expected Writes를 검증해야 한다. 누적 compiler에서도 같은 gate를 호출하고 positive/negative controls를 남긴 뒤 전체019 ROM/repro를 순차 생성한다. 그 제품에서 새comma/님의 경계 페이지와 정상 초기설정/메일 회귀를 실행한다. 기존018 `a8d39423bbd4792d948af4bea991dd8c56bb6d34dac8c1a7c570f0c3938f3241`과 원본 해시는 그대로 확인했다. 새 BPS/xdelta/ZIP 없음.

`test_nickname_template_survey.py`5 fixture PASS: 비성장 punctuation 수용,1px comma 성장 거부, 조사/단어 suffix 미승인, 추가 변수 거부, nickname 인수 보호. syntax PASS. 분석을 다시 실행해 동결 JSON 동일 재현도 확인했다. 테스트는 live nickname capacity나 신규500개 ROM 반영 증거가 아니다.

다음 순서: 실제 nickname writer/reader 및 최대 native 값 증거 확인 → 1px 증가와 같은 행 prefix의 실제 aggregate 모델 → 필요한 source-only/cumulative product 게이트와 positive/negative controls → 미적용500개 고정 선택(부족하면 다른 별도 소비 계약 조사) → 원본 기반 전체 제품과 독립 빌드 순차 실행 → 같은 제품의 합산 렌더/초기설정·메일 회귀. 후보 scan은 제품 빌드에 넣지 않는다. 조건을 무시하거나 이미 적용한 ID를 재집계해500을 만들지 않는다.

018 결과·세이브·증거·패키지를 보존했다. 끝 해시 대조:018 `a8d39423bbd4792d948af4bea991dd8c56bb6d34dac8c1a7c570f0c3938f3241`,원본 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`,기존 ZIP `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`, 모두 동일. 새 patch/ROM 없음, 의미·화면 사람 승인이나 release 판정도 없음.
