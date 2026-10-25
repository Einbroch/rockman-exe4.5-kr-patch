# 가나 입력 화면 기능 버튼 한글화 후속

## 현재 결과

원본에서 재빌드한 누적 개발 ROM `poc/output/exe45_ko_development_native_keyboard_labels_v1.gba`.
SHA256 `ec6fe6a156c0ec379866267fa2094b85773eb2f471723cc915c02e5ed8bbe40c`.
독립 `_repro.gba` 전체 바이트 동일. 크기는 이전 startup_ui_v1_r7과 동일한 11,218,012바이트.
기존 텍스트 2,648개는 그대로이고 그래픽 기능 라벨 18개를 추가 번역했다.

- 히라가나 페이지: 가타카나 / 기호 / 오른쪽 / 왼쪽 / 공백 / 확인.
- 가타카나 페이지: 히라가나 / 기호 / 오른쪽 / 왼쪽 / 공백 / 확인.
- 영숫자·기호 페이지: 히라가나 / 가타카나 / 오른쪽 / 왼쪽 / 공백 / 확인.

가나 글자 자체, 키 선택표, 조합·확정·저장 코드는 원본 그대로다. **한글 자동 조합 자판이나 한글 이름 저장 구현이 아니다.**
내비 카드의 일본어 그림 글자는 아직 저장/선택/표시 경로 미확정으로 변경하지 않았다.

## 소스와 기본 계약

원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
세 페이지는 `356E8`의 16바이트 native transfer descriptor와 `356C0`의 맵 포인터가 선택한다.
타일/맵의 소스 크기·해시와 포인터 모집단을 빌드가 검사한다. 새 타일도 같은 슬롯 크기로 저장하고 원래 포인터·전송 크기를 보존한다.
페이지 슬롯 용량 300/295/226타일에 실제 290/285/214타일이 들어간다.
원본 글자판과 프레임 등 편집 영역 `x196..223/y56..151` 밖 모든 픽셀을 보존한다. 줄무늬 배경은 원본의 5/9 팔레트 규칙으로 재생성한다.
Galmuri7의 원래 7픽셀 글자 모양을 변형 없이 사용해 네 음절 페이지 이름도 28픽셀 폭에 넣었다. 작은 버튼 글자의 미적 검토는 needs_review다.
기존 r7 대비 변경은 타일/맵 여섯 슬롯에 한정됨을 전체 ROM 비교로 검사한다. 기존 코드·아카이브·추가 영역·폰트·날짜/PET 이미지와 저장 ABI는 바이트 동일하다.

## 빌드와 검사

이전 startup_ui_v1_r7 빌드 명령의 `--name`을 새 이름으로 지정하고 `--native-keyboard-labels`를 추가한다.
`tools/native_keyboard_labels.py`와 `translations/native_keyboard_labels_ko.json`이 실제 primary builder 입력이다. 옛 `prepare_keyboard_labels.py`의 조합 자판 후보를 설치한 것이 아니다.

- `python -X utf8 tools/test_native_keyboard_labels.py`: 세 페이지 픽셀/슬롯 보존, 결정성, 잘못된 원본/descriptor/font/policy/wording 거부 2개 테스트 PASS.
- `python -X utf8 tools/test_startup_assets.py`: 기존 startup 이미지/압축 회귀 3개 PASS.
- `tools/audit_startup_ui.py`: source/final write/기존 번역/새 그래픽 배치/독립 재빌드 및 r7 대비 쓰기 경계 PASS.

## 실제 화면과 입력

정확히 위 ROM을 격리 Mesen에서 일반 버튼 입력으로 실행했다. 사용자 ROM/SAV는 변경하지 않았다.

- `poc/runtime/native-keyboard-labels-v1-boot`: 초기 설정을 지나 이름 입력까지 10/10 캡처. 기존 날짜·PET 안내 유지.
- `poc/runtime/native-keyboard-labels-v1-pagecycle`: START로 확인 버튼에 이동 후 UP 5회로 첫 기능 버튼 접근. 가타카나→기호→히라가나 전환, 재진입 및 선택 표시 11/11 캡처.
- `poc/runtime/native-keyboard-labels-v1-complete`: 원래 가나 `い` 입력/확정, 프로필 재표시, 록맨 선택/첫 안내/메일 알림까지 19/19 캡처.
- `native-keyboard-labels-v1-pages`, `...-switch`는 처음 탐색한 방향키 경로의 진단 기록이다. 이 경로는 페이지 전환에 도달하지 않았고 정상 전환 증거로 사용하지 않는다.

실제 세 페이지의 전체 native VRAM 타일 은행이 ROM과 바이트 동일하다.
BG2 맵은 32셀 행 간격으로 배치된다. 원본 30x20 맵 중 560셀은 ROM과 동일하며, 위쪽 질문/입력 필드 40셀은 native UI가 렌더링 뒤 교체하는 `A1C0/B180` 규칙과 정확히 일치한다. 전체 맵을 그대로 비교해 실패한 결과를 성공으로 바꾼 것이 아니라 원본과 동일한 dynamic field 동작을 분리 검증한 것이다.
정확한 ROM/스크린샷/덤프/입력/체크포인트 해시는 `poc/runtime/native-keyboard-labels-v1-verification.json`에 연결되어 있다.

## 패치와 남은 작업

개인 시험용 ZIP: `patches/exe45_ko_development_native_keyboard_labels_20261012.zip`.
ZIP SHA256 `42d106cf7af358f3558e00b21f23ad25f3be0cd5cd91a187c9ebe567c5f639a4`.
BPS SHA256 `e1a527d89b1f01b73d3d780f4c4bff3bdf9e17687c5ffd88d691efdf4a4c1416`.
xdelta SHA256 `4d3da0547ac8d0344acafa629bfd073c316ecbac6c8f5c6066b74f184fbc4604`.
BPS 또는 xdelta 중 하나만 무패치 원본에 적용한다. 전체 결과 동일/결정성/손상 패치·잘못된 원본 거부/래퍼 덮어쓰기 거부를 패키지 생성기가 검증한다.

남은 중요한 조건: 실제 한글 입력·자동 조합·확정·저장·재표시 통합, 내비 카드 그림 글자와 전체 게임 미등록 초안, 다른 내비 경로와 전체 플레이/저장 회귀. 공개 릴리스나 초기 메뉴 전체 완료 선언은 하지 않는다.
