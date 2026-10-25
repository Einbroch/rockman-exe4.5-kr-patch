# 롤 PET — 44문구 개발 반영, 정상 화면 검증

2026-10-03. development-draft; NON-DISTRIBUTION. 문구·시각 needs_review.
release_eligible=false. 전체 게임 완역·배포·하드웨어/오디오 검증이 아니다.

## 산출물과 범위

`poc/output/exe45_ko_development_roll_pet_v2.gba`
SHA256 `28f7d52dc6d09a13b6c91e4a29950f6fa443225049328c70bdc4023657cffd24`.
불변 원본에서 `_repro.gba` 독립 재빌드 동일. 최종 도구 재현은
`_current_repro.gba`와 해당 입력/도구 해시 메타데이터로 확인한다.
845텍스트 단위(추가44), 그래픽9개 그대로. 전체 게임 분모가 아니다.

`translations/roll_pet_menu_ko.json`: source65FA58, 원본1126바이트
SHA256 `dc93dba5b3147299e83df4a9b89acdf46e1c63229ae2b8694353f80145875720`.
22스크립트의 실제44문자열 전체. 선택 script1..8/10..16/20과
비문자 script0/9/17/18/19/21의6개 보존. 명령/인수/분기/선택지 순서,
줄바꿈과 마지막 빈 선택 행, 예의 뒤 공백2개를 유지했다.
원본 풀은 그대로 두고 카탈로그의32-bit root380D8만 새 ROM 풀로 재배치한다.
새 게임 코드 훅이나 RAM 버퍼 확대는 없다. 기존 글꼴/장비 훅은 누적 유지한다.

번역 예: `뭘 할까?`, `토너먼트에 / 참가할까?`, `내 장비를 / 바꾸려는 거야?`,
`메일을 / 확인할 거야?`, `통신 대전을 / 할 거야?`.
`/`는 기존 줄바꿈. script5는 원문의 진술형 `볼게.`를 유지하고,
script8 저장 화면 진입과 script16 기존 데이터 저장 질문은 구분한다.
뜻·말투의 인간 승인은 아직 없다.

## 닉네임 첫 행 보정 / 보존한 V1

script1은 printPlayerNickname 후 쉼표+개행을 출력한다.
초기 V1은 ASCII 쉼표를 새 확장 글꼴로 그려12px가 되어 원본11px보다1px 늘었다.
최대 길이 닉네임의 여유를 가정하지 않도록 V2에서는 **원본 `、` 0x87 바이트와
11px 폭을 그대로 유지**했다. 이는 남긴 일본어 단어가 아니라 보호한 기존 문장부호다.
닉네임도 원본 입력값/소비 방식을 그대로 유지하며 한글 이름 입력을 추가하지 않았다.
제품 빌드는 dynamic nickname suffix의 첫 행 변경을 거부한다.
원본/이전 ROM/V1 및 그 상태·스크린샷은 삭제하지 않았다.
`analysis/roll_pet_v1_input_snapshot.json`은 변경 전 입력이고 V1은 검증 완료판이 아니다.
V1 상태를 V2에서 사용하지 않았다.

## 기술 / 정상 실행 검증

- 44문구 각각 인코딩·재추출·바이너리 roundtrip, 구조/비선택6스크립트 바이트,
  필요한 전체 한글 BDF 및 native 문자 글꼴 기록을 검증했다.
- 채택한 한 행132px/3행 범위에 최대123px. 14개 선택 행의 위치/빈 행/
  예·아니요 패딩과 합산 폭을 제품 빌드에서 검사한다.
- 같은 V2 cold boot에서 날짜/프로필 입력→정상 Roll Navi Select→롤 PET
  →대기/확인창. 상태 강제 변경·다른 ROM 체크포인트·호출 강제 전환 없음.
- `roll-pet-v2-roll-intro` 및 `roll-pet-v2-prompts`는22개 단위(script1..8)를
  실제 소비했다. 각 글리프의 코드/ROM 공급·CPU 읽기→OBJ VRAM→전체 글자 픽셀 일치.
- No 포커스 커서 OBJ0/tile1020이 원래 Yes 뒤 빈 패딩 배경에 겹친다.
  글리프 VRAM 전부를 비교하고, 커서의 불투명 픽셀에 가려진 **배경만** 화면
  색 검사에서 구분한다. 번역 잉크/그림자가 커서에 가려지면 실패한다.
- 29단계에서 동일 새 풀과 현재 script, Yes/No 커서 위치108/144, No 및
  B 취소→idle1의 커서220/복귀를 검사했다. 메뉴 확인창이 끝까지 한글로 표시된다.
- 메뉴7 통신과 메뉴8 저장은 No만 선택했다. 실제 통신·실제 세이브는 수행하지 않았다.
- 롤/록맨 장비, 원래 코드 ABI·스택, 장비 재진입 및 새 롤 PET script1 전환,
  공격력 이미지 BIOS 해제/상주/VRAM/픽셀과 숫자 보존 회귀 통과.
  록맨 폴더·공통 무기·PET7 이미지(`통신`)도 같은 V2 ROM에서 통과.

보고서:
`analysis/roll_pet_v2/runtime.json` (PET 정적44, 실제22, 열린22 구분),
`rockman_regression/runtime.json`, `roll_caption/runtime.json`.
비교 화면: `analysis/roll_pet_v2/pet_prompts.png`.
자동 테스트130개 통과(38.807초, OK). `_current_repro.gba`도 같은 SHA256이며
해당 메타데이터의 모든 도구 파일 해시가 현재 소스와 일치한다.
전체 실제 경로/도구/에뮬레이터/ROM/상태/각 파일 해시는 각각의 result.json과
재귀 체크포인트 검증으로 묶었다. 단순 캡처 완료만으로 화면 통과를 선언하지 않는다.

## 재현

```powershell
python -X utf8 tools/build_roll_pet.py --work NEW_WORK --out NEW_OUTPUT.gba
python -X utf8 tools/run_roll_equipment_guides_matrix.py --stem exe45_ko_development_roll_pet_v2 --prefix NEW_PREFIX-roll- --pet-probe
python -X utf8 tools/run_roll_pet_prompts.py --origin OWN_SAME_ROM_TOURNAMENT_PROMPT --out NEW_PROMPTS
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

입력 레시피만 재사용하고 새 실행의 cold chain을 만든다. PET 확인창 seed는
자기 ROM의 롤 intro 상태에서 `none:1:60,b:2:90,a:2:180,none:1:180` 정상 입력.
seed의 complete 및 화면/현재 script2를 확인한 다음 prompts를 실행한다.
보고서 main(stem,prefix,outdir)에는 자기 경로 접두사를 넣는다.
이전 결과를 덮어쓰지 않도록 work/out/prefix는 새 경로를 지정한다.

## 미완료

script10..16의21문구와 script20 반응1문구는 번역/정적 검증했지만 실제 표시
검증은 아직 열려 있다. 이22개를 실제 실행했다고 주장하지 않는다.
롤 첫 인사/날짜별 이야기, 다른 내비의 대사/장비 안내, 전체 게임 미번역과
전체 분모·진행·세이브/통신·하드웨어·오디오·인간 문구/시각/배포 승인은 남아 있다.
