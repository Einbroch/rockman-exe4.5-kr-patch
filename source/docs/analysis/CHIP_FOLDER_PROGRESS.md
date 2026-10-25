# 도감 밖 칩 이름 소비자 — 아직 구현하지 않은 범위

2026-10-02. 검증용 ROM은 99단위 초안 `16afa15f…`이며 폴더 이름은 일본어 원본이다.
EXE3의 이름 풀/타일맵 분리 분석을 참고하되 주소와 인코딩은 EXE4.5 원본에서 확인했다.

## 원본 연결과 정상 진입

- 9개 원본 이름 root-pair의 static 후보를
  `exe45_chip_name_consumers_static_v1.json` / `exe45_chip_name_direct_readers_v1.json`에 보존.
- `0801F7D4`는 9비트 칩 ID의 bank root를 선택하고 `0801F7E8`에서 복귀한다.
  근처 다음 함수의 BL을 이 함수 호출로 계산하지 않는다.
- `0803864C`는 두 bank의 uint16 offset으로 script pointer를 돌려준다.
- 장비 → 칩 폴더의 정상 패드 진입에서 **별도 `0803CBB0`** parser를 실행했다.
  `0803CB76`의 BL, 복귀 `0803CB7A`, 원본 source pool streams를 대조했다.
- 7행 버퍼는 `0202A680..0202A75F`, 상하 간격16/행 stride32, r6 base=`2010`.
  native glyph마다 `base + code*2` / `base + code*2+1`의 halfword map을 쓰고,
  8칸 미만은 zero로 지운다. 도감의 `0201E600`/팔레트 E000과 다르다.
- 정상 폴더 경로 4,305호출에서 캐논 3행, 에어슛 3행, 발칸1 1행의 일본어
  source bytes·호출 ABI·buffer/padding을 비교했다. 오른쪽 이동의 빈 목록도 관찰했다.
  `root-selector`의 호출은 이 경로에서 0회였으며 전체 비도달성을 뜻하지 않는다.

## VRAM 수명 조사

`folder-lifetime-v2`: 장비 메뉴에서 시작해 폴더 진입·이동·빈 목록·복귀·종료,
1,158프레임 전체 active BG map과 helper copy/write inventory를 관찰했다.
native parser는 4,956회. 원래 ROM과 source pointers는 변경하지 않았다.

- `06008000..06008FFF`에 **928회 write**가 있어 항상 비어 있지 않다.
- 초기화 frame84에 native helper `08000956`이 `0201C004`의 1,792바이트를
  `06008020`으로 복사했다. caller=`080291A5`. `06008040`부터의 도감
  working cells 일부와 겹친다. 초기화 완료/캐시 reset 계약이 필수다.
- BG map의 관측 참조는 `06008000` tile뿐이었다. `06008040..06008EAF`
  56셀/tag 범위 참조는 이 경로에서 0회다. 제어 map write도 positive다.
- 처음 BG0 charbase=`06008000`만 보고 현재 working cells가 active map에서
  사용될 것이라고 추정했으나 실제 snapshot/전 프레임 map 검사는 0이었다.
  이 추정은 폐기한다. 비어 있다는 반대의 전역 주장도 하지 않는다.

보고서 `exe45_chip_folder_native_runtime_v1.json`와
`exe45_chip_folder_lifetime_v1.json`은 정확한 ROM·입력 계보·observer 해시·데이터를 묶는다.

## 실패/보완을 분리

`folder-survey` 첫 observer는 source `0803CB62`의 빈 행 clear → `0803CB7A`
직접 분기를 실제 parser 복귀와 잘못 짝지었다. ROM이 아니라 observer의
null-entry 처리를 별도 v2 adapter에서 고쳤고 실패 artifact는 보존했다.

`folder-lifetime` 첫 composition은 dump 함수 이름 불일치로 캡처를 못 했다.
해당 `segment.lua` 경로를 확인한 이 작업 소유 Mesen 프로세스만 종료했다.
ROM/세이브를 직접 편집하지 않았고, failed result를 보존한 뒤 v2 adapter에서
함수명을 연결하여 별도 폴더에 재실행했다. 실패를 정상 QA로 계산하지 않는다.

## 다음 구현 전 확인할 것

1. 메뉴 dispatch: root job28, menu0. `0803B918[0]`→`0803C1C0`, phase
   table `0803C1D4[16]`→`0803D854`; folder subphase table `0803D868`의
   0번→`0803D878` 초기화다. 이 관계는 원본 코드와 실제 RAM을 대조했다.
   폴더 화면 phase16/subphase8, 빈 오른쪽 목록 +3 byte4를 관찰했다.
2. `0803D878` 초기화의 그래픽 전송 완료와 `0803CB76` 첫 이름 소비 사이
   정확한 reset 설치 위치를 입증한다. 일반 scene-loader 전체에 blanket reset하지 않는다.
3. native base2010의 낮은16은 resident font offset이다. 한글 cell은 palette
   high bits와 private tile514를 별도로 사용해야 하며 native 숫자의 +16은 유지한다.
4. 폴더 전용 guard/buffer/continuation, 원본 five-row/other-bank fallback,
   폴더→PET→도감→입력→재진입, 전체56-cell 변화 부하를 검증한 후에만 채택한다.

도감용 late-wait는 menu8/phase4만 허용하므로 menu0/phase16 폴더를 우회하지 않는다.
폴더 수정에 새 timing 요구가 생기면 별도 재현/원인/수정을 검사한다.
현재 폴더 한글화를 완료했다고 보고하지 않는다.

## 2026-10-02 재개: 폴더 전용 렌더러와 소유권 가드

원본 초기화의 마지막 `0803D978`에 태그 reset을 설치했다. 관찰상 전송은
frame84에 끝나고 첫 이름 소비는 frame86이다. 원래 상수 store와 POP PC는
재현하며, reset 루프의 조건 플래그는 호출자에서 사용 전에 덮어써진다.
한글에만 native tile bias16을 제거하고 숫자/원문 fallback은 보존한다.

v2 SHA256 `6790782b403f07f5f850cb985e6aedf012dc8334736b4f9988e4f74379a6fd41`:
폴더 7행의 실제 glyph/palette/화면 픽셀, 빈 목록 clear, 복귀를 통과했다.
실제 복사17회, cache hit8908회, reset1회다. 도감 탭과 이름 입력의 foreign
font overwrite 후 폴더 재진입도 별도 runtime/pixel 보고서에서 통과했다.

v3 SHA256 `980f26a3de796f96cc8089fbb04082714794dd4c799dac96917f328d6351af35`:
selector와 reset 모두 r10=0200F2C0/root job28/menu0/phase16을 명시적으로
확인한다. 다른 소유권이면 native fallback과 기존 태그를 유지한다.
CPU 34058개 벡터와 reset15개 벡터, 원본 기반 재빌드 동일 해시를 확인했다.
v2의 가드 없는 옵션도 원래 v2 해시로 재현된다. 99개 draft unit이며
폴더와 도감이 같은 30개 이름 번역을 재사용한다(중복 번역 수로 계산하지 않음).

v3 cold boot는 완료됐고 `chip-folder-v3-normal-r1` 정상 입력 검사는
5/5 캡처와 실제 복사/cache/ABI 검사를 통과했다. 도감 탭 6/6 캡처도
완료했다. 이름 입력→재진입, 별도 v3 픽셀 보고서, v3 저장/재부팅,
폴더 전체56-cell 변화 부하는 진행 중이다. 기존 v2 보고서를 v3 증거로
간주하지 않는다. 잘못된 CLI 옵션으로 시작하지 못한 normal 디렉터리는
실패 흔적으로 보존하고 정상 실행은 별도 normal-r1에 기록했다.

전체 게임/오디오/실기 검증 또는 배포 완료를 의미하지 않는다.

### v3 재개 검증 누적

`exe45_chip_folder_pixels_v3.json`, `exe45_chip_folder_reentry_v3.json`:
정상 폴더 및 도감→이름 입력→폴더 재진입의 실제 glyph/화면 픽셀 검증 PASS.
`exe45_chip_folder_save_v3.json`: native 저장 확인/완료, 별도 disk cold boot,
저장된 게임에서 폴더 재진입 픽셀 PASS. SRAM65536bytes SHA256
`6de509d736812dab55b6828088c750496e701bf2690763ba14f65f519a4536b6`.
다른 후보와 원본 조사 세이브가 바뀌지 않았는지 디스크 inventory로 검사했다.
새해 인사 대화가 입력을 가로챈 첫 재진입 route는 폴더 hit가 없어서 제외했다.
그 incomplete checkpoint를 다음 실행에 쓰려던 시도도 runner가 거부했다.
검증된 saved-reboot부터 정상 입력으로 재실행했으며 진행 RAM을 편집하지 않았다.

`exe45_chip_folder_names_batch_v3.json`: 실제 clone 이름1..30 모두 6153행의
진단 소비를 통과했다. descriptor CPU read만 대체하고 실제 ROM 이름 byte와
glyph를 사용했다. 30-update 고정 페이지 3개의 glyph/화면 pixel mask도 PASS.
이 진단 checkpoint는 이름을 바꾸고 정상 play 사용을 금지했다. 획득30개
정상 플레이 또는 이름 승인 증거로 계산하지 않는다. 기존54개 unit test PASS.

56-cell changing fixture 첫 두 시도는 observer가 selector의 LR을 원래 값으로
보존한다고 잘못 가정해 실패했다. 실제 계약은 LR=0803CB7B이며 CPU와 정상
observer가 이미 이를 확인한다. product ROM은 변경하지 않고 fixture 계약만
수정해 changing56-r2를 별도 실행했다. 실패 폴더는 보존했다.

`exe45_chip_folder_changing_v3.json`: 579개 group, 4053행, 32424회 실제
64-byte inline copy, post-group glyph와 태그 검증 PASS. 578개 갱신 간격은
모두1프레임이다. mute Mesen의 해당 synthetic folder route에만 적용하며
실기/오디오/전체 scanout tearing 또는 전체 게임 timing 완료는 주장하지 않는다.
