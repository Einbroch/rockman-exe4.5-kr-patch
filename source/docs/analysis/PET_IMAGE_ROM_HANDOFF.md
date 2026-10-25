# PET 이미지 미번역 및 ROM 화면 검증

2026-10-03 / development-draft; NON-DISTRIBUTION

## 후속: 사용자 통신 오독 수정 및 ROM 삽입 요청

내장 image_gen으로 `pet_labels_v1/candidate_02_tongsin.png` 수정 시안을 만들었다. 6번째 통신의
통(U+D1B5=ㅌ+ㅗ+ㅇ)에 초성 가운데 획을 추가하도록 명시했다. 원본 생성 결과는
`C:/Users/<user>/.codex/generated_images/01a0ce89-71de-7110-8cdb-aef5aa012c8d/exec-9f91136a-1d03-497c-a26c-f78e0229d9be.png`에 보존했다.

원본 문자 띠는 y1..8의 8픽셀이고 y0/y9/y10은 프레임이다. 생성 시안의 글자 마스크만
원본 팔레트4로 변환하는 adapter를 작성했고 threshold112/64 두 변환을 각각
`translations/pet_graphics_v2`, `pet_graphics_v3`에 보존했다. 두 출력 모두 한글 획의
소실/합침이 있어 manifest review를 REJECTED로 기록했다. 프레임/아이콘 보존 및
무변경 왕복이 통과해도 가독성 실패를 상쇄하지 않는다. 두 블록은 ROM에 삽입하지 않았다.

사용자에게 글자만 소형 한글 픽셀폰트로 재작성하는 방향과 이미지 시안 형태를 계속 조정하는
방향 중 선택을 요청했다. 아직 선택 결과나 ROM 화면에서의 통 교정 완료를 가정하지 않는다.

로딩 조사는 동일 ROM의 메뉴 로딩 이전 cold-part1에서 `poc/runtime/pet-graphics-load-v1`를 실행했다.
read-only callback이 원본0x086303B8부터 연속160개의32비트 읽기를 BIOS PC0xC18에서 기록했다.
r0의32바이트 선증가/r1의VRAM0x06011000 그룹 기준을 관측했고, step040 전체0x1200바이트
VRAM과 원본 블록도 일치했다. `pet_labels_v1/load_runtime.json` PASS는 이 원본 읽기/목적지
연결에 한정되며 새 이미지 삽입 검증이나 로더 전체 제어 흐름/게임 측 호출자 확정은 아니다.

## 이번 작업 결과

- 텍스트 누적은 기존 758개 그대로다. 이번 작업에서는 추가 대사 번역이나 ROM 변경을 하지 않았다.
- PET 일본어 메뉴 7개는 BG 폰트가 아니라 4bpp OBJ 그래픽이다. BG 4개를 분리해 메뉴 글자가 포함되지 않음을 확인하고, 실제 OAM과 OBJ VRAM에서 원본을 추출했다.
- 원본 ROM `[0x6303B8,0x6315B8)`의 0x1200바이트와 메뉴 화면 VRAM `[0x11000,0x12200)`이 정확히 같다. 이는 바이트 출처 증거이며, 아직 로더 명령어 추적 완료 증거는 아니다.
- 실제 OBJ의 16x16 아이콘 + 32x16 문자 2개 + 16x16 우측 테두리를 96x16 스트립으로 추출했다. 7개를 96x112 atlas로 묶었으며 확대본은 정확한 8배 nearest-neighbor 참고용이다. 원본 이미지 수정 없음.
- 문구 후보: 토너먼트 / 플러그인 / 장비 / 데이터 라이브러리 / 메일 / 통신 / 저장. 기존 PET 대사 용어를 유지했다. 긴 라이브러리 문구의 64px 영역 가독성은 미확정이다.

## 이미지 시안 검사

`pet_labels_v1/candidate_01.png`는 내장 image_gen으로 원본 8배 참고 이미지를 편집한 시안이다.
원본 생성 파일은 그대로 보관했고, 프로젝트에는 사본을 저장했다. 생성 요청은 7개 일본어 라벨만
한글로 교체하고 아이콘/테두리/팔레트/투명도/8배 픽셀 격자를 보존하도록 지정했다.

시안 실제 크기는 **1160x1355**로 요청한 **768x896**과 다르고 원본 팔레트에도 없는 색이 있다.
`candidate_01_qa.json`은 technical_pass=false다. 크기가 달라 보호 영역/알파 대응/8배 격자 검사는
미평가(null)이며, 통과로 간주하지 않는다. 임의 리사이즈·양자화·아이콘 복원으로 불합격을 숨기지 않았다.
ROM 삽입 없음. 이 시안은 전수 이미지 번역 완료나 에뮬레이터 화면 증거가 아니다.

## ROM 화면 확인

검증 ROM: `poc/output/exe45_ko_development_roll_tactics_v1.gba`

SHA256: `1ca65635bcfb92ff3845bf7b75cf6491a045f32cceda5ec16eca977d7d45f31f`

`poc/runtime/pet-labels-v1-focus/`는 동일 ROM의 기존 검증된 cold-part2 체크포인트에서
B로 확인 대사를 닫고 Down을 6회 입력한 새 실행이다. 다른 ROM 세이브/진행도 주입 없음.
7/7 캡처 및 정상 종료. 실제 화면 step001/007을 직접 검토했다.

`focus_runtime.json`은 7개 focus 각각 원본 OBJ 블록 일치와 선택 라벨의 x=137/palette8을 확인한다.
비선택 라벨은 x=141/palette9다. OAM 인덱스는 대사/커서 상태에 따라 이동하므로 고정 인덱스가
아니라 실제 타일·크기·y·팔레트로 라벨을 찾는다. 초기 고정 인덱스 검사는 실패했고, 실패를 PASS로
저장하지 않았다. 타일 기반 검사를 적용한 뒤 다시 확인했다.

전체 자동 테스트: 97개 통과. 새 테스트는 정상 참고 이미지의 gate 통과 및 생성 시안의 거부를 확인한다.
오디오 muted, 실제 기기/전체 플레이/새 한글 그래픽 렌더링은 이번 검증 범위가 아니다.

## 이어갈 작업과 한계

1. PET 그래픽이 로드되기 전 동일 ROM 상태에서 실제 source-read/upload 로더를 추적한다.
2. palette8/9 및 선택/비선택 상태를 모두 보존하는 native 64x16 문자 영역 후보를 재작성·검사한다.
3. 통과 후보만 원본 입력 기반 새 ROM에 삽입하고, 새 해시의 cold-chain부터 메뉴 7항목을 다시 검증한다.
4. PET 외 타이틀/서브화면/전투/통신 등 텍스트 이미지 전수 목록을 계속 확장한다.

gt-image-analyze 정식 단계는 전수 컨테이너 이미지 목록 및 text-review/font handoff가 없어 BLOCKED다.
이번에는 create-kr-patch의 그래픽 조사와 generic imagegen의 비배포 시안 작업만 진행했으며,
정식 image analysis/translation/review 완료로 승격하지 않았다. 사용자 이미지 번역 요청 자체는 중단하지
않았으나, 실패한 시안의 ROM 반영은 fail-closed 검사에 따라 보류했다.
