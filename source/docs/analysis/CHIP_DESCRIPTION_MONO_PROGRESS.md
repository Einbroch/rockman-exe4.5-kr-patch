# 칩 설명문 mono 경로 조사

## 검증 기준

현재 고정 artifact는 폴더 v3 SHA256
`980f26a3de796f96cc8089fbb04082714794dd4c799dac96917f328d6351af35`다.
이 후보의 설명문은 아직 원문이다. 이름/헤더의 big-font 성공을 mono 설명문
성공으로 일반화하지 않는다. create-kr-patch font-strategy의 경로별 공급·
active buffer·palette·실제 소비 검증 기준을 적용했다.

## 원본 script부터 staging까지

`exe45_chip_description_mono_native_v1.json`은 정상 폴더에서 관찰한 stream
08769588이 원본 archive76937C의 script1 시작과 정확히 같음을 확인했다.
archive10467bytes/256scripts, TPI pointer words136796/863064/871692.
개발 ROM에서도 이 pool byte는 원본과 같다. 폴더 진입/복귀의 캐논 설명
3회에 대해 mono bank08619EF8, 448glyph×64bytes, 10×3 staging1920bytes,
30개 native glyph의 source→stage 32bit word-add tint transform을 확인했다.
원본 copier는 context가 선택한 word tint를 더한다. 직접 byte 복사라고
단정하지 않는다. upload target은06012800이다.

## 실제 OBJ와 palette

`exe45_chip_description_mono_pixels_v1.json`: 1920-byte VRAM upload가
staging과 같다. 하지만 실제 OBJ는 (10,88)에서 **9×3개** 8×16 sprite다.
각 staging row의 열9는 이 원문에서 blank이고 화면 OBJ에는 없다.
따라서 staging width10을 visible width10의 증거로 쓰지 않는다.
27개 sprite의 모든 pixel을 glyph role별 일정한 screenshot RGB와 대조했다.
원본 palette2에서 role1(background)과 role4(shadow)는 동일 색이다:
RGB193/189/211, BGR555777B. role3(ink)은 RGB8/8/8, BGR55514A5.
Mesen의 화면 RGB는 단순5bit left-shift와 같지 않아 그 변환 가정은 폐기했다.
현재 보고서는 source role→palette index→observed scanout color 관계를
검증한다. 하드웨어 색 변환 모델의 검증으로 보고하지 않는다.

## 구현 전 남은 조건

- 같은 description pool의 다른 세 pointer consumer와 9/10 staging 차이를
  확인한다. 일부 static code는9×3, 다른 code는10×3을 사용한다.
- 기존 fixedcell F9FC hook은 r6 원본 font와 무관하게 big Hangul bank를 고른다.
  mono에 그대로 번역을 넣으면 role0/1/2가 잘못 공급될 수 있다.
  native mono r6=08619EF8에만 대응하는 별도 bank/profile과 기존 fallback을
  구현·CPU 검증하고 나서 text를 넣는다.
- 원본 제어 명령, 숫자, description 의미를 유지한다. 소비 경로/실제 폭을
  명시한 development asset과 immutable-source build를 사용한다.
- 번역된 여러 줄 문장, 공백/숫자, 고밀도 한글의 실제 staging/OBJ/pixel,
  도감/폴더/다른 description 경로와 저장/재진입을 동일 새 ROM으로 검증한다.

mono 한글화·설명문 번역 또는 전체 게임 배포 완료를 아직 주장하지 않는다.

## 2026-10-02 첫 한글 문장 구현

`--mono-font-poc` 개발 옵션은 r6=08619EF8에서만 별도 full11172 mono
Hangul bank를 선택한다. 원본 mono font와 native copier는 그대로다.
big-font와 mono role1/3/4 profile은 같은 pinned Galmuri glyph ink geometry를
사용한다. 전체11172자×2provider, 경계 glyph×3tint, legacy F9 tail-call을
실제 native copier까지 실행한 CPU22390벡터가 통과했다. 해당 CPU 검사는
scanout이나 full legacy semantics 검증으로 계산하지 않는다.

provider만 추가한99unit 후보 SHA256
`3d87211edae14085c6878caeae293978306348ba162c7d43720a54f1098c6a4b`는
source rebuild 동일해시다. 옵션을 끈 v3 compatibility rebuild는 원래
`980f26a...af35` 그대로다.

캐논 계열 script1..3의 보호된 원문을 explicit shared wording asset
`translations/chip_descriptions_cannon_poc_ko.json`에서 번역했다:
“앞쪽의 적 1체를 / 공격할 수 있는 / 캐논포”. enemy count1과 원본 줄바꿈2개,
모든 control command, 253개 unselected script byte를 보존한다.
source archive의 TextPet grammar는 mmbn45이고 F9FC code table은 공유한다.
mono layout은 native observed visible9×3에 맞춰 각 line advance72/64/24px다.
기술 결함을 감추기 위해 원문 의미/숫자를 생략하지 않았다. wording은 needs_review다.

문장 포함102unit 후보 SHA256
`913561b98f8a329def8eb0afea96fa4320499d29cc89374e37a68f14b927a01a`:
v1 manifest의 과거 “mono remains native” 문구가 낡아 v2 별도 빌드에서
limit metadata를 고쳤다. ROM byte는 v1/v2 동일하고 두 artifact를 보존했다.
v2 exact cold boot→normal folder에서 actual compiled Cannon sentence,
30-cell stage/native padding, 27 visible OBJ, native palette, 모든 screenshot
pixel을 검사한 `exe45_chip_mono_cannon_runtime_v2.json` PASS.
기존 캐논/에어슛/발칸1 7행의 big-font pixel도 함께 PASS다.

도감 탭6captures, input foreign-font overwrite3captures, 폴더 재진입5captures의
새 ROM 실행은 완료했고 copy/cache/ABI positive도 PASS다. 통합 pixel report는
별도 진행 중이다. 새 ROM의 folder CPU34058/library CPU34054도 PASS다.
새 mono/layout/control5test를 포함한59unit test PASS.
save enter/commit/finish 완료 후 disk cold reboot 검증 중이다.

아직 shared description 다른 pointer consumer, script2/3 실제 소비, 새 ROM의
maximum-load timing 및 통합 save/reentry closure는 남아 있다. 이전 v3 runtime
보고서를 이 새 ROM의 증거로 재사용하지 않는다. 폴더의 캐논 문장 정상 표시
이외의 mono 번역 완성이나 배포 후보라고 보고하지 않는다.

### 102-unit 후보 회귀 완료 범위

`exe45_chip_mono_regressions_v2.json`: four big-font titles, library names,
mono Cannon sentence, 입력 화면의 foreign font overwrite→폴더 재진입의
glyph/OBJ/pixel PASS. `exe45_chip_mono_save_v2.json`: native disk save→cold
reboot→Cannon sentence redisplay PASS, SRAM SHA6de509...563b6 유지.
`exe45_chip_mono_scripts123_v2.json`: 실제 script1/2/3 compiled bytes를
lookup CPU read alias만 바꿔 소비하고 각 sprite/pixel을 검사했다. acquired
HiCannon/MegaCannon play로 계산하지 않으며 checkpoint를 quarantine했다.

`exe45_chip_mono_timing_v2.json`: 새 hash의 folder579groups/32424copies,
library314groups/17584copies/2198icons, 각 cadence1frame PASS.
정상 folder/menu0-phase16와 library/menu8-phase4의 caller stack을 실제로
관찰해 모두 source `080D4CE0`→`080554A4`→fixed-cell임을 확인했다.
원본 pool literal은 D4D0C다. 2165C/D2B58 consumer까지 통과했다고 하지 않는다.
현재 source로 재빌드한 v2_repro도913561...a01a다.

## 129-unit 설명문 batch01

`translations/chip_descriptions_batch01_ko.json`: script1..30의30개 설명을
추가했다. 21개 explicit wording과30개 stable unit이다. 최초3개 asset은
그대로 보존하며 registry의 명시적 scope_variant가30개 inventory를 선택한다.
기존 default3-script scope는 바뀌지 않는다. numeric guard는 product build에서
원문 숫자열이 바뀌면 실패한다. EXE4.5 발칸은3/5/7연발과1칸 관통이다.
mini bomb script29의 원본2줄 구조, HP, 전방/뒤/대각선/위아래 범위와 버그 조건을
보존했다. 암흑/라라뮤트/연쇄 폭발 용어는 따로 needs_review다.

새 ROM SHA256
`57e932ce8a0f232ca767f131cf24b08f84450efbbb04fa08a1a77d6058ba595d`
`exe45_ko_development_chip_mono_batch01_v1.gba` 및 `_repro.gba` 동일해시.
총129draft units,727untouched archives, 설명 archive의226unselected scripts
byte 보존. 65unit tests, provider CPU22390, folder CPU34058 PASS.

`exe45_chip_mono_batch01_runtime_v1.json`: 정상 입력으로 Cannon/Airshot/Vulcan1
설명과 이름을 선택해 source-bound stage/OBJ/pixel 검사 PASS.
별도 all30 진단은 source lookup table CPU read만 바꾸고 실제30compiled
설명문을 소비한다. 30/30개 held screenshots와 모두1920-byte stage,
27visible OBJ의 every-pixel 검증 PASS. 입력/획득/ROM/텍스트 byte/세이브 RAM을
편집하지 않았지만 설명 선택은 synthetic이므로 normal-play로 주장하지 않는다.

129-unit 후보의 도감 탭과 입력→foreign-font overwrite→재진입은
`exe45_chip_mono_batch01_regressions_v1.json`으로 새 hash에서 PASS했다.
`exe45_chip_mono_batch01_save_v1.json`은 native save 완료 화면, 디스크 저장,
cold reboot(상태파일 없음), 정상 폴더에서 Cannon 설명문의 stage/OBJ/pixel
재표시를 검증했다. 저장 SHA256은6de509...563b6이며 다른 후보 저장과 원본
survey 저장을 보존했다. 102-unit 결과를 새 ROM 검증으로 계산하지 않는다.

`exe45_chip_mono_batch01_parser_cpu_v1.json`: actual IWRAM fixed-cell parser,
F9 provider와 native glyph copier로30scripts×9/10columns=60vectors PASS.
줄바꿈/여백/2줄 원문/ASCII/숫자의 실제 glyph cursor와 stage 바이트를 검증했다.
전송 helper만 bounded byte-copy로 대체했으므로 DMA/타이밍/다른 소비자의
게임 내 도달성 검증은 아니다. 초기 fixture는 literal6898의080008E0를
전송 함수로 잘못 잡아 transfers=[]였고, 실제 LDR의 literal6894에 있는
08000850로 수정했다. ROM 수정은 없었다.

`exe45_chip_mono_batch01_timing_v1.json`: 새129-unit hash에서 folder579groups/
32424copies와 library314groups/17584copies/2198icons, 모든 group간격1frame
PASS. actual normal folder/library entry에서 outerLR080D4D09도 각각 확인했다.
정지한 폴더의 checkpoint에서 none/down/right-left로 시도한 세 parent probe는
calls=[]였다. 단순 버튼 변경이 parser 재호출을 보장하지 않아 PASS로 계산하지
않았으며, 검증된 reboot→정상 폴더 진입을 다시 수행해 actual call을 관찰했다.
65unit tests를 다시 통과했다.

shared2165C/D2B58 consumer runtime과 broader game closure는 여전히 미완료이며
배포를 주장하지 않는다. source21476의 직접 BL 후보는208EE/217D4/21812이며
선택 slot r5+0A(0..2)에서244F80/24F8A/24F94를 통해 chipID를 가져온다.
이 경로는 아래 정상 battle runtime으로 확인했다.

## 정상 전투의9×3 mono 소비 확인

동일129-unit ROM의 own saved reboot→인사 대화→정상 인터넷 접속→이동→
첫 tutorial battle을 controller input만으로 진행했다. 초기 전체 fixed-cell
관찰은 매 프레임3개 native big chip label 호출 때문에1000-entry budget에
도달했다. 이를 chip description 실패나 complete coverage로 계산하지 않는다.
새 `capture_chip_mono_battle.py`는 실제mono font08619EF8만 entry에서 필터하고
미관찰 big path exit는 무시한다. ROM/RAM/save/선택칩을 수정하지 않는다.

전술 선택(TACTICS) 화면에서 R을 누르면 설명 panel이 열린다. static source
21410의 button mask100와 실제 입력이 일치한다. 정상 현재 MiniBomb 두 slot을
left/right로 선택해 각 설명 call을 관찰했다. native outerLR0802164B,
wrapperLR080554BA, width9/height3, rootjob8, context0200F2C0이다.
pool literal2165C 소비를 정상 runtime에서 처음 확인했다.

`exe45_chip_mono_battle_runtime_v1.json`: script29 실제 compiled text를
source-bound lookup하여1728-byte stage/upload, 원문2줄+blank third row,
27visible OBJ와3 held screens의 모든 glyph pixel PASS. source-native ASCII3의
실제 bitmask로 battle palette12의 RGB roles를 보정하고 독립 BDF Hangul
bitmask와 대조했다. OBJ tile811부터 native odd tile이며 menu의 even tile
조건을 재사용하지 않는다. 패널은 slot별x4/84로 이동하며 text y80/96/112.

전투 chip names는 현재 library/folder name scope 밖의 native Japanese다.
이 검증은 MiniBomb 정상 tutorial만이며30개 battle 설명 전체나 audio/hardware
timing을 주장하지 않는다. D2B58 shared consumer는 아직 unresolved다.

추가 정상 route에서 Vulcan1 script15도 같은21628 경로의 stage/upload/27OBJ/
pixel을2 held screens로 확인했다(`exe45_chip_mono_battle_vulcan_runtime_v1.json`).
route directory `battle-airshot-info`는 시도 당시 예상 이름일 뿐, 실제 선택은
script15→49→15였다. parser lookup으로 실제script를 판단했으며 Airshot
검증이라고 계산하지 않는다. 사이에 unselected native script49가 표시되어
후속 fallback 회귀 대상이다. 이 route에는5×2전술 native text도 하나 있어
Vulcan report는 stream identity로 해당9×3 call만 필터한다.

`exe45_chip_mono_battle_native49_v1.json`으로 정상 Korean15→native49→Korean15
mixed fallback도 PASS했다. source49의 원본script bytes를 재삽입 clone과 비교하고,
독립 table(E4+low index 포함)에서 native27glyph sequence를 구성해 stage/upload,
palette12 identity,27OBJ의 pixel을 확인했다. 이 와이드소드 script49는 번역
inventory에 넣지 않았으며 원문 그대로라는 adjacent-path 회귀다.

## batch02: 첫60개 이름·설명,189-unit 후보

명시적 새 초안 seed `translations/chip_batch02_draft_seed.json`의 source31..60을
원본literal에 결합했다. EXE3 exact common name8개를 reference 후보로 재사용했고
동일source 숫자열, newline count, 이름8cells/설명9cells 범위를 검사했다.
first30의 source/translation/state는 단 하나도 변환하지 않았다. 블랙봄 새 초안의
10cell 문장을 재삽입 전에 발견해 수동으로9cell로 고쳤으며 불발탄·화염 폭발
조건을 보존했다. 일반 자동축약 규칙을 만들거나 기존 번역에 적용하지 않았다.

`prepare_chip_batch02_assets.py`는 file write 없이 composition JSON을 출력한다.
names/description batch02 asset은 apply_patch로 설치했다. source hash, seed/tool
hash, EXE3 reference hash와 exact candidates, needs_review를 기록했다.
registry에 explicit60-script variant만 추가하며 default3와 batch01 scope는 유지한다.
69unit tests, new-ROM provider22390/folder34058/library34054CPU PASS.

`exe45_ko_development_chip_mono_batch02_v1.gba`와 `_repro.gba`의 SHA256은
`2c58b1ec49cc80e8b4325a4ddc55b2f6181820025dbead6457d7b22b06a3aa4f`.
189draft units=69기존대사/menu+60names+60descriptions,5relocated archives,
727untouched archives이며 source pool의196unselected name/description scripts
보존. 새 runtime은 진행 중이며129-unit 결과를189-unit PASS로 옮기지 않는다.

첫53-action cold probe는 기본 Mesen timeout90에 도달해 captures0/2,
complete=false,rc4294967295였다. product defect라고 단정하지 않으며 실패
directory를 보존했다. 동일 ROM/입력을13+40actions로 나누고 explicit240s budget,
중간 capture를 넣어 경계를 찾았다. part1은 정상 title까지5/5capture PASS,
part2도5/5capture와 정상 Korean tournament prompt까지 PASS했다. ROM 변경 없이
전체53동일입력이 완료되어 첫실패는 관찰 시간 예산의 제한으로 기록한다.
원본ROM588a77...5ef8와 immutable survey save99bb57...b470 해시를 재확인했다.

`exe45_chip_mono_batch02_runtime_v1.json`: normal Cannon/Airshot/Vulcan 선택,
실제60개 compiled 설명문을 별도 source-table read alias로 각각 소비한60held
screens의 stage/upload/27OBJ/every-pixel PASS. acquired60개를 정상 플레이한
것으로 계산하지 않는다. 진단 checkpoint는 quarantine했다.

`exe45_chip_folder_names_batch02_v1.json`: 실제60name clone을 descriptor read
alias로 소비하여 모든60개 실제glyph copies/cache/rowABI와9held pages에서
60/60개 이름의 pixel masks를 검사했다. source196unselected scripts unchanged,
descriptor RAM도 unchanged다. 초안 이름을 native battle name으로 자동으로
옮기지 않는다. new-ROM parser9/10columns×60=120CPUvectors PASS.

`exe45_chip_mono_batch02_regressions_v1.json`:189-unit four big titles, library
name/mono sentence, input foreignfont→folder reentry pixel PASS. 첫input route는
기존 A count에서 실제 name editor가 아니라「천재인 사람은 누구?」의 대화
페이지에 머물러 source63ABF4 bank overwrite 조건이 false였다. 기존 입력
횟수를 새 scene 도달 증거로 간주하지 않고, 추가 A로 editor에 들어간 r2의
step5/6에서0x1000-byte font span의 실제 overwrite와 tag poisoning을 확인했다.
r2 재진입에서reset1+17misses와glyph/pixel 재복원 PASS. ROM 수정은 없었다.

첫save-enter의 native confirmation은 정상이나, 이후 입력 재현으로 own RTC
파일이 바뀌어 엄격한 disk chain을 이어갈 수 없었다. 원본기록을 보존하고
새 save-enter-r2부터 끊김 없는 persistence chain을 시작했다. 세이브 파일을
직접 편집하거나 다른 후보 저장을 복사하지 않는다.
`exe45_chip_mono_batch02_save_v1.json`: 새189-unit ROM의native 저장→finish→
상태파일 없는 cold reboot→정상 folder mono redisplay stage/OBJ/pixel PASS.
각disk snapshot/hash와 files-before/after가 연속이며 다른 저장/원본survey를
보존했다. 이 후보의 native saved SHA256은91dc859...c0110이다. 이전129-unit
6de509...563b6 해시를 새 후보에 강요하거나 저장파일을 복사하지 않는다.
`exe45_chip_mono_batch02_timing_v1.json`: new-ROM folder579groups/32424copies,
library314groups/17584copies/2198icons, 모든group간격1frame PASS. native
folder/library entry outerLR080D4D09를 새ROM에서 각각 확인했다. saved91dc859...
해시도 보존했다. muted Mesen synthetic workload 범위이며 audio/scanout tearing/
hardware timing claim은 아니다. new-ROM normal battle 재검증은 진행 중이다.
`exe45_description_roots_static_v2.json`의 raw opcode/address-word 조사에서
D2B58 direct Thumb/ARM literal reader와 aligned exact address word reference는
각각0이었다. 계산된 주소/레지스터 기반 read까지 배제하지 않아 unreachable
판정은 내리지 않는다. 2165C는21658의 literal이 그 주소를 담는 간접 root다.

### 2026-10-03: 189-unit normal battle description

새 ROM의 초기 tutorial TACTICS에서 바로 R을 누른 첫
`battle-tactics-info`는 captures3/3이나 native21628 description call이0이었다.
튜토리얼 대화가 계속되는 화면을 description proof로 계산하지 않고 보존했다.
이전129-unit에서 확인한104개의 정상 controller action을 새 ROM의 own
network-tutorial checkpoint에서 다시 실행한 `battle-tutorial-complete`는
captures6/6 PASS. RAM/progress 주입이나 다른 ROM checkpoint 복사는 없다.
그 뒤 `battle-tactics-info-r2`의 R/none/right/left에서 실제21628 consumer의
9x3 description3calls를 관찰했다. 새 source29 MiniBomb에 대해
`exe45_chip_mono_batch02_battle_minibomb_v1.json`은 stage1728bytes,
native upload06016560,27OBJ, 현재 battle palette로 보정한 전체pixel PASS다.
이는 실제 MiniBomb 정상 선택 경로의 검증이며 모든60개의 정상 획득/전투,
전투 chip name 한글화, full-game 또는 release 검증은 아니다.

이어서 normal draw/TACTICS 입력을 재현한 directory
`battle-vulcan-wide-info`는 계획 당시 이름과 달리 actual scripts4→29→4를
호출했다. 저장/RTC가 다른 후보의 draw 결과를 새 ROM의 결과로 추정하지 않는다.
`exe45_chip_mono_batch02_battle_hicannon_v1.json`은 actual source4 HiCannon
held screens3/5의9x3 stage/upload/27OBJ/allpixels PASS다. calibration은 첫
글자라고 가정하지 않고 unmodified native glyph 중 roles1/3/4를 모두 가진
cell을 선택한다. source-bound provider 선택은 전체27cells에 대해 검증한다.
directory 명칭의 Vulcan/WideSword는 현재 후보에서 증명된 항목이 아니다.
`battle-third-slot`에서도 더 오른쪽 입력은 두 번째 MiniBomb slot을 유지했고
추가 translated script coverage는 얻지 못했다. 같은 화면을 새 증거로 더
누적하지 않는다. 이후 own save SHA25691dc859...c0110을 재확인했다.

### 2026-10-03: next90-scope draft / 249-unit development candidate

`chip_batch03_draft_seed.json`의 새 source61..90 name/description 초안을
명시적으로 작성했다. Counter2/3, AirHockey1..3, CircleGun1..3,
TwinFang1..3, WhiteWeb1..3(각 위/중간/아래 줄 구분), Boomerang1..3,
SideBamboo1..3, BambooLance, DarkHole, wind/vacuum, BoysBomb1..3,
MetGuard1..3을 포함한다. EXE3 exact common7names는 후보이며 승인 아니다.
실제4.5의 방향/범위/숫자와3row controls를 유지한다. 새 초안을 수동 작성·
수정했으며 기존 번역의 자동 문구 변경은 없다. 기존60units/source/state는
verbatim composition test로 보호된다. 새 name90/description90 assets 모두
needs_review, NON-DISTRIBUTION이다.

`prepare_chip_batch03_assets.py`는 source-bound composition을 stdout으로만
출력하며 apply_patch로 설치했다. explicit scope variant는1..90이고 이전
variant/default 범위를 바꾸지 않는다. full73tests PASS. 5archives/249units/
727untouched archive 후보와 repro의 SHA256은 둘 다
`c9683edd7f4d1c877dfa4ef6a15a33e929083e6ae2d8f87b78f4509e83210701`이다.
기존189-unit artifact/report는 덮어쓰지 않았다. CPU provider22390,
folder34058/library34054vectors PASS. 새 후보 cold-part1은13actions,
5/5captures PASS; own checkpoint에서cold-part2가 진행 중이다.
이 새 ROM의90script pixel/runtime/save/timing 증거는 아직 미완료이며
189-unit의 PASS를249-unit의 PASS로 승계하지 않는다.

새 own cold-part2는40actions/5captures PASS. native parser9/10columns×90=
180CPUvectors PASS. `all90`는187normal controller actions와 source-table
read alias로 실제90compiled scripts를 소비했고90/90held screens를 수집했다.
diagnostic checkpoint는 quarantine했다. 첫 normal-scroll 캡처는 generic
library observer여서 folder_qa_environment가 누락되어 strict report가 실패했다.
ROM이나 검사를 완화하지 않고 `normal-scroll-r2`에서 folder observer를 실행해
같은16actions/4captures와 copy/cache/ABI를 검사했다.
`exe45_chip_mono_batch03_runtime_v1.json`은90/90stage/upload/27OBJ/allpixel,
정상 Cannon/Airshot/Vulcan의 설명·이름,166unselected scripts PASS다.
`names-all90`는21actions/13held pages,4466real clone row copies에서90개
name source IDs를 모두 소비했다. `exe45_chip_folder_names_batch03_v1.json`은
13pages의 glyph masks가90/90names를 포함하고166unselected clone scripts가
보존됨을 검사했다. source-table/descriptor aliases는 획득 증거가 아니다.
이 새249-unit ROM의 native save/reboot, foreign-font reentry, max-workload,
normal battle는 여전히 미완료다. 기존189-unit PASS로 대신하지 않는다.

첫 `library-tabs` 실행은 original byte-copy observer가 새word-copy hook에서
Korean evidence를 찾지 못해 tool이 실패했다. 경로의 captures6/6만으로 PASS
처리하지 않고 보존했다. 동일ROM/14actions를 adopted late-wait/copy/cache
observer로 다시 실행한 `library-tabs-r2`에서 환경검사를 확보했다.
`input-lifetime-r2`는own library-tabs-r2에서 실제editor의 foreign native bank
overwrite를 검사했고, `foreign-reentry-r2`는reset1+17real copies와 복원픽셀을
검사했다. `exe45_chip_mono_batch03_regressions_v1.json`의4titles/library/folder/
mono/foreign-font reentry PASS. ROM 변경은 없다. 현재native save chain은
`save-enter-r2`부터 시작하며 다른 ROM 세이브 복사/RAM 편집은 하지 않는다.

`exe45_chip_mono_batch03_save_v1.json`: own native 저장→finish→상태파일
없이 cold reboot→정상folder 한글 설명 재표시 stage/OBJ/allpixel PASS다.
enter/commit에서 실제 Korean confirmation/completed screenshots를 검토했고,
각files-before/after disk chain과 snapshots hashes가 연속적이다.
새 후보에서 실제 저장한65536-byte SAV의 SHA256은91dc859...c0110이며
189-unit과 같지만 복사하지 않았고 native commit의 변화/snapshot/reboot를
독립적으로 기록했다. 다른 후보 저장과 원본survey는 보존됐다.

`exe45_chip_mono_batch03_timing_v1.json`: folder579groups/32424copies,
library314groups/17584copies/2198icons, 모든group 간격1frame PASS다.
각native description caller D4D0C의 outerLR080D4D09를 own saved-reboot
origin에서 folder(menu0phase16)/library(menu8phase4)로 독립 관찰했다.
source/survey/save hashes는 유지됐다. diagnostic 최대 부하이지 전체 게임,
audio/hardware/scanout tearing 보장이 아니다. 새249-unit normal battle
route는own saved-reboot부터 현재 진행한다.

`exe45_chip_mono_batch03_battle_minibomb_v1.json`: own saved reboot→normal
NET42actions→native tutorial104actions→TACTICS R/none/right/left로 실제source29
description consumer21628에 도달했다. 3held screens의9x3 stage/upload/27OBJ/
current-palette allpixels PASS. 모든90chips의 정상 획득/전투 검증은 아니다.

다음 별도battle name 경로를 `capture_chip_battle_names.py`로 관찰했다.
ROM/RAM/진행 변경 없이 own normal tutorial checkpoint의none5frames에서
15calls. font08612E38,8x1,outerLR080166C3,wrapperLR080554BA,
root8/menu28/phase8,targets0600BE00/0600C000/0600C200였다. source pool765190
actual scripts29/29/221이므로 untranslated thirdRoll 이름도 관찰된다.
stage glyphroles는0/1/2이고 mono description의1/3/4와 다르다. 이 결과는
new battle-name 공급/clone selector를 설계할 근거이지 한글 구현 PASS가 아니다.
관찰된5x2/outer20B5F mono consumer는 이름card8x1과 별도로 취급한다.

`exe45_chip_battle_native_names_v1.json`으로 native15calls의 source29/29/221,
8cells×64bytes stage와 BG0 map/palette13 및 실제roles1/2 pixels를 대조했다.
밝은 ink1/dark shadow2는 기존big Hangul bank와 같아서 별도font bank나
provider 코드를 추가할 필요가 없었다. source glyph0 padding도 그대로 쓴다.

글로벌source name pool pointer를 바꾸면 다른8root-pair/렌더러가 같이 영향을
받는다. 따라서 name helper1F7D4 entry8bytes에서만callerLR080166AD를 구분하는
추가selector를 도입한다. 다른5개static BL caller, unselected main IDs,
secondary IDs는 native pool/normalized ID/registers/CPSR/SP를 그대로 반환한다.
caller166A8의1..90만 이미검증한 privateclone을 반환한다. native parser,
font612E38,8x1geometry,stage/upload,source continuation 및 모든shared pointer는
유지된다. `166A6..166BE`를 크게 재배치하는 대안은16674→166AC의 내부 진입을
옮겨야 하므로 채택하지 않았다. ARMv4T에서는 low→low nonflag MOV가 거부되어
ADD+마지막CMP 복원으로 원본 flags를 유지했고 byte pseudo-instruction은 없다.

새 candidate `exe45_ko_development_battle_names_v1.gba`/repro SHA256은
`0f40221f833afe835f9c5ad0eb7fac12570b8ca800fc9b5632916aa88742600e`이다.
249drafts와90/90names/descriptions의 문구는 바꾸지 않았다. 기존249-unit ROM과
다른source bytes는1F7D4..1F7DB의8bytes뿐이고,기존expanded payload/font/renderer
prefix는 byte-identical,새append는68bytes다. product delta/repro 및 원본helper와
각6caller×(512IDs+5high-bit inputs)=3102CPUvectors를 비교한
`exe45_battle_names_build_cpu_v1.json` PASS. 전체76unit tests PASS.
새 ROM 자체cold-part1은13actions/5captures PASS; own cold-part2 진행 중이다.
새 battle name 한글화의normal runtime/font/pixel/fallback 검증은 아직 미완료다.

새battle-name ROM의cold-part2는40actions/5captures PASS. own cold prompt에서
neutral61frames+기존NET 입력42actions로 native 저장/접속/첫NPC tutorial을
정상 입력으로 재현했다. 다른 ROM SAV/checkpoint 복사는 없다. 이어서104actions
native tutorial→TACTICS에 도달했다. `exe45_battle_names_parser_cpu_v1.json`은
own cold snapshot의 IWRAM/EWRAM을 사용해 실제native8x1 parser/provider/copier
90vectors PASS. CPU fixture/ bounded transfer contract이지 DMA/timing proof는 아니다.

`exe45_battle_names_normal_runtime_v1.json`: 정상twoMiniBomb/oneRoll의15calls.
MiniBomb source29는실제privateclone+big Hangul bank로미니봄을 표시하며,
unselected221Roll은 original source pool/glyphs로 유지된다. glyph/padding512bytes,
native BG0 charbase8000/mapE000/palette13 및24cells의ink/shadow screenshot masks
PASS. sourceplayer/menu/enemy/weapon controls와글꼴bank 자체는수정하지 않았다.

`exe45_battle_names_all90_runtime_v1.json`:name-only stack CPU-read alias로
1..90 실제clone을8frames씩유지하는30pages/720parsercalls의90/90stage/upload/
BG0/ink-shadow pixel masks PASS. underlying chipID reads는29/221 그대로다.
텍스트/ROM/descriptor/SAV RAM을 편집하지 않았고 진단checkpoint를quarantine했다.
이름만바꿔보이는진단이며90개chips 정상획득/진행 증거는아니다.

`exe45_battle_names_description_regression_v1.json`: own normal checkpoint에서
R/none/right/left로source29의9x3 mono description에들어가3screens stage/upload/
27OBJ/allpixels PASS. big-name(roles0/1/2)→mono-description(roles1/3/4) 전환에서
wrong bank/palette/stale glyph가 관찰되지 않았다. 전체76unit tests를재확인했다.
초안249units의wording/presentation은needs_review이고다른name consumer,
대부분의dialogue/graphics, 전체게임·오디오·실기·배포검증은완료되지않았다.

### 2026-10-03: battle-name native reboot and bounded TACTICS prompt draft

`battle-names-v1-native-reboot` completed11/11 normal-input captures without
loading a state. Terminal screenshot manually inspected: ordinary PET and native
speech, no observed boot error. Its own native-generated SAV0619f62e... remains
byte-identical, as do all existing .sav files in the isolated directory.
This is candidate-local native reboot evidence, not inherited batch03 save QA.

`exe45_tactics_prompt_source_audit_v1.json` pins76C944/4473bytes/SHA256
8dcf2727f8ddc7e0f1e35e45bc9790f0ab4253e5bae44275a599f57fbf6a971c:
144scripts, one aligned root212E8. Native212C8 selects Navi style*6+prompt;
20B48 uses5x2 mono output. Correction: this is Navi TACTICS speech, NOT enemy names.
Aligned root scanning does not prove absence of computed/unaligned consumers.

Added only observed Rockman scripts0/1: `어느 적을\n노릴까?` and
`적과의\n거리는?`, wording/layout stillneeds_review. Mixed archive usesmmbn45s
for selected questions butmmbn45 for escape dialogs; registry now explicitly pins
the selected literal language rather than deriving it from font type. First build
attempt failed closed on that grammar distinction; partial work retained.

`exe45_ko_development_tactics_prompts_v1.gba` and independent_repro are identical:
0170f1786c93819bb4d5363330c2a8dfa3c5b4eb5890dcb626beb65f72805254.
251draftunits/6relocated/726untouched archives. Native, semantic, binary roundtrips
PASS;142unselected prompt scripts preserved. Widths40/32 and24/32 fit5x2.
77unit tests PASS. Own cold-part1 completed13actions/5screens; own cold-part2
started from same-ROM checkpoint. Actual translated TACTICS pixels, CPU5x2,
cross-font regressions and new candidate save cycle remain pending. Do not treat
the new251-unit ROM as runtime-reviewed or release-ready.

Follow-up: own cold-part2(40actions), NET/tutorial(43actions), and battle tutorial
(104actions) completed. `exe45_tactics_prompt_parser_cpu_v1.json` PASS actualnative
5x2 parser/provider/copier for both drafts, bounded upload stub640bytes; no DMA claim.
Normaltarget screenshot104 and B→down menu selection screenshot2 show both drafts.
`exe45_tactics_target_runtime_v1.json` and `exe45_tactics_distance_runtime_v1.json`
PASS source-bound stage640bytes, glyph/padding cursor, actualVRAM upload, BG3
control1F09/charbase8000/mapF800/zero scroll/palette10,10cells exactpixels.
Earlier report attempted OBJ layout and correctlyfailedclosed: target06008A20
isBG3, notOBJ. Tutorial screenshot16/28 text is obscured by instructor overlay;
these were not accepted as visible pixel evidence. Two no-new-call input probes
remain failed observer evidence, not new runtime coverage.

New candidate `exe45_tactics_description_regression_v1.json` PASS normalR→9x3
MiniBomb stage/upload/27OBJ/fullpixel evidence on3screens.
`exe45_tactics_battle_names_regression_v1.json` PASS normal15calls of twoHangul
MiniBomb labels plus nativeRoll fallback8x1/BG0/pixels. Checks executed again on
this ROM, not prior candidate results. Tests77PASS rechecked.

Own native save created through controller save input in the new NET route;
native-reboot loaded no state and completed11screens. TerminalPET inspected;
newcandidate SAV0619f62e... and all priorSAV files remain unchanged on reboot.
OriginalROM588a77... and surveySAV99bb57... reverified unchanged.
`exe45_tactics_prompts_milestone_v1.json` reconciles exactROM0170f178...,
independent byte-identical rebuild,142unselectedscripts, fiveCPU/runtime reports,
and own native reboot. This is a bounded251-draft development milestone only.
Allwordings stillneeds_review; exhaustive90-script diagnostics, folder/library
timing, fullsave-commit regressions on this newROM, otherNavi/escape/mostscripts,
graphics/audio/hardware/whole-game/release QA remain pending.

### 2026-10-03: explicit chip91..120 development expansion

Added30explicit name/description pairs from exact source765190/76937C scripts91..120.
Prior90 names and descriptions are verbatim, source numeric identities/rows/controls
protected. EXE3 shared-name spellings supplied20unapproved candidates; not a term
approval. Five initial new lines exceeded9visiblecells; explicitly redrafted only
those new units before serialization (no rule-based prior prose rewriting).
All inputs remain needs_review / NON-DISTRIBUTION. New filesbatch04_seed/composer/
assets/tests and registeredmono-descriptions-batch04 scope do not replace older ones.

`exe45_ko_development_chip_batch04_v1.gba` and independent_repro byte hash:
181135d058fe9117e3e944f15461bd55b6835e65a7001b4610306ce5d1870c2b.
311draftunits:69intro/menu/header/save+120names+120descriptions+2TACTICS questions.
6relocatedarchives/726untouched,136unselected description scripts and142unselected
TACTICS scripts preserved. Tests79PASS. Existingbig/mono full11172fontbanks retained.

New-ROM CPU evidence:22390provider-selection/nativecopy vectors,34058folder and
34054library vectors with23318bounded glyphcopies each,240native9x3/10x3 description
parser vectors and120native8x1name parser vectors PASS. Actual120-scope battle helper
native differential3102vectors PASS, including all512IDs/sixcallers, registers/flags/
stack/sourcefallback. `battle_helper_cpu_v1_r2` additionally pinsUnicorn components;
earlier v1 retained but superseded for adopted evidence. These CPU results do not
prove normal120chip acquisition, DMA/timing or whole-game playability.

Own freshcold13+40actions and normalfolder16actions completed; no cross-ROM state or
savecopy. `chip-batch04-v1-all120` runs compiled-description source-table read aliases
through the actual folder renderer on this ROM. Diagnostic checkpoint must be
quarantined and all120 held pixel evidence checked before crediting that scope.
Folder names120 diagnostics and cumulative report still pending at this entry.
Whole-game coverage, human wording/presentation and release remain incomplete.

Follow-up completed on exactROM181135...: `chip-batch04-v1-all120` ran247actions,
120/120heldscreens,120real compiled-description calls, folder copy/cache/ABI PASS.
Diagnosticcheckpoint quarantined, no text-byte/ROM/SAV-RAM editing. The underlying
source-table read aliases select1..120; this is not120chips acquired in normal play.
`exe45_chip_batch04_runtime_v1.json` PASS normal Cannon/Airshot/Vulcan and120/120
description stage1920bytes/nativefont+Hangul+padding/upload/27visibleOBJ/fullpixel
checks; source136unselectedscripts unchanged and reproducible311unit build pinned.

`chip-batch04-v1-names-all120` completed26actions/18heldscreens,5516observedrows,
120/120names via guarded actualclone/descriptor CPU-read aliases. Its checkpoint
also quarantined. `exe45_chip_folder_names_batch04_v1.json` PASS all120heldname
glyph masks/sourceclone/unselected136scripts checks; not normal acquisition or
synthetic56changing-cell timing. Final tests79PASS.

`exe45_chip_batch04_milestone_v1.json` binds eight new-ROM CPU/runtime reports,
byte-identical rebuild, originalROM/surveySAV integrity, prior90verbatim assets,
136description/142prompt untouched scripts. All311wordings stillneeds_review;
new-ROM battle/Tactics/input/save/timing regressions and full-game coverage remain
pending. No distribution package or release approval was created.

### 2026-10-03: exact311-unit normal battle and120 battle-name regression

Own cold-part2 checkpoint→normal43-input NET/save/tutorial route→104-input battle
tutorial completed. `exe45_chip_batch04_tactics_target_v1.json` PASS normal5x2
question0 at screenshot104; B→down→A normalmenu route's screenshot2 provesquestion1
in `exe45_chip_batch04_tactics_distance_v1.json`. Exactsource/stage640/upload/BG3/
10cells/foreground+shadow+background pixels checked anew onROM181135... .

`exe45_chip_batch04_battle_names_normal_v1.json` PASS normal twoMiniBomb Hangul
labels and unselected nativeRoll fallback,15actual8x1calls/BG0/pixels.
`exe45_chip_batch04_battle_description_v1.json` PASS normalR→MiniBomb9x3mono
description,3heldscreens/1728stage/upload/27OBJ/fullpixels. Other battle description
scripts have CPU/folder evidence only; this is not a120battle-description claim.

First120 battle-name diagnostic timedout240seconds after33/40captures, with no
final-parent evidence; complete=false, not credited. Its report adapter also
rejected a sequential replacement anchor. Both failures preserved; noROM change.
Fresh `battle-names-all120-r2`, timeout600, completed40/40pages/960native8x1calls
below1000probe guard. `exe45_chip_batch04_battle_names_all120_v1.json` PASS all120
compiledsource names/provider/nativepadding512bytes/stage/upload/BG0/ink-shadow
pixel masks. Underlying stack sourceIDs29/221 unchanged; only name-read return
values aliased, noROM/text/descriptor/SAV-RAM injection. Diagnosticstate quarantined.
Not120normally acquired chips or new battle mechanics verification.

Own .sav was absent before initialcold1, generated71189f7f... there; unchanged through
cold2/normalfolder/both folderdiagnostics. Normal NET save input changed ownSAV to
0619f62e...; other existing SAVs unchanged (the expected own commit is not corruption).
The isolated own native reboot is now in progress; do not credit persistence until
result and terminal screen inspected. Tests79PASS rechecked. ROMunchanged311drafts,
wording/presentation/full-game/audio/hardware/release still incomplete.

Follow-up: own native-reboot completed11/11screens with no state loaded; terminal
PET manually inspected. OwnSAV0619f62e... and all other isolated SAVs byte-identical
before/after. Original588a77... and survey99bb57... rechecked unchanged.
`exe45_chip_batch04_battle_save_v1.json` PASS reconciles five exactROM battle/prompt
reports and12route disk inventories: none→native initial71189...→normal commit0619...
→unchanged battle anddiagnostic routes→native cold reboot. Failed timeout route was
not promoted. Other SAVs were preserved throughout; own commit is expected change.

`chip-batch04-v1-reboot-folder` normal16inputs from own reboot checkpoint completed.
Initial checker assumed step14/15/16 were three description selections and failed
closed: step14 had no mono description. Actual screenshot15/16 shows normalCannon
after openingdescription; noROM fix or rerun was necessary.
`exe45_chip_batch04_reboot_folder_v1.json` PASS those two heldCannon1920stage/upload/
27OBJ/fullpixels and seven-rowHangul names, own0619.../otherSAVunchanged.
This does not claim Airshot/Vulcan or120-acquired post-reboot coverage.
311draft ROM remains181135..., unchanged. Foreign-font/input lifetime and maximum
workload timing on this ROM, D2B58/shared consumers, remaining translations/graphics,
human wording/presentation/full-game/audio/hardware/release remain incomplete.

### 2026-10-03: user-directed untranslated-first drafting, no ROM rebuild

User explicitly prioritized untranslated text over further runtime loops. Added
batch05 scripts121..150, batch06 scripts151..180, batch07 scripts181..194:74new
names+74descriptions,148draft wordings. Prior120 pairs unchanged. Currentassets
hold194names/194descriptions plus prior71otherunits=459draftunits; actualROM stays
the311-unit181135... baseline. No newROM/runtime/release claim.

Explicitnewdrafts preserve source rows, numbers, directions, shotcounts, currentHP
last-two-digit rule, panel sacrifice boosts and trap trigger/damage subject. Common
EXE3 names remain unapproved candidates. DarkChip Katakana ominous style and new
terms need wording/presentation review. No rule-based existing prose rewrite.
195..200 source name literals absent: do not invent missing names.195/196 description
literals and201+ names/descriptions remain outside this paired prefix draft scope.

Added150/180/194 source-pinned registry variants and serialized assets; no build run.
80tests PASS: deterministic composition, priorpairs verbatim, protected controls,
source numbers/rows, Korean encoding/layout, native name-clone compilation and62
unselected name scripts preserved at194. Initial test incorrectly used the original
Japanese-only table and failed onHangul; corrected test fixture uses the existing
fullHangul plugin generator in isolatedtemporary directories. No translation or
font substitution to hide a missing glyph. Paired source/Korean review sheet:
`translations/CHIP_UNTRANSLATED_FIRST_121_194.md`. Allnewwordingsneeds_review.
