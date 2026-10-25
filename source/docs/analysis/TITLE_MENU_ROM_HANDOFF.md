# 메인 메뉴 처음부터·이어하기 (2026-10-12)

사용자가 첨부한 mGBA 화면의 `はじめから` 및 저장 상태의 `つづきから`를
각각 `처음부터`, `이어하기`로 교체한다. 기존 누적 번역과 자모 공급은 보존한다.

## 구조와 적용

원본 SHA-256은 project.json의 일본판 프로필이다. 메뉴 그래픽은 ROM 0x7CEA94의
657바이트 BIOS LZ10 스트림이며 1668바이트로 해제된다. 처음 4바이트
`00840600`은 변경하지 않는다. 나머지는 26×2개의 4bpp OBJ 타일이다.
위·아래 행의 열 0..5가 처음부터, 10..15가 이어하기이다.
두 라벨의 48×16 영역만 수정하고 다른 타일, 메타데이터, 팔레트, 커서 및
로고는 보존한다. Galmuri11에서 변환한 11px 자형을 원배율로 넣었다.
재압축은 648바이트이며 기존 657바이트 슬롯에 패딩해 넣는다.

메뉴 포인터는 0x2910C이며 네이티브 로더 0x08029164가 0x0201C000으로 해제하고
헤더를 제외한 1664바이트를 0x06010800에 복사한다. 읽기 전용 observer에서
해제된 전체 payload, 복사 ABI, 메뉴에서 유지되는 전체 VRAM sheet가 일치했다.

## 원본부터 누적 빌드

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_title_menu_v1 --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --title-menu-graphics
```

같은 명령의 `--name`을 `exe45_ko_development_title_menu_v1_repro`로 바꿔 재빌드했다.
두 ROM 모두 SHA-256 `d99dca6bb308cba81b481a0f0865bb0138290c4dd5ecf6e5e08a6afdbe49e66b`.
60아카이브/2596문구/672미변경 아카이브를 유지한다. 직전 ROM과 다른 629바이트는
전부 메뉴 압축 슬롯 안에 있고 나머지 전체 ROM 바이트는 같다.

## 실행 검증

- `poc/runtime/title-menu-v1-nosave`: 체크포인트 없는 coldboot, 무저장 처음부터 표시,
  A 선택 후 날짜 초기 설정 화면 정상 진입. 2/3/4번 화면 직접 확인.
- `poc/runtime/title-menu-v1-withsave`: 직전 기준 ROM이 생성했던 native SAV/RTC를
  이 ROM만의 격리 테스트 이름에 복사하여 coldboot. 2/3/4번은 이어하기→처음부터→
  이어하기의 포커스 및 흰색/회색 팔레트 전환, 5번은 A 선택 후 내비 선택 화면.
  네 화면 직접 확인. 사용자 세이브는 변경하지 않았다.
- 원래 테스트 이름의 초기화 SAV/RTC는 `title-menu-v1-nosave/native_after_newgame.*`에
  먼저 보존했다. 재사용 SAV SHA-256은
  `5f21f85bf13ec7b4ce5a37aaa511fe674760c17454974870161fc98701d39440`.
- `poc/runtime/title-menu-v1-observer`: 정상 coldboot와 컨트롤러 입력에 읽기 전용
  native 해제/복사 관측을 추가. 검증은 같은 폴더 verification.json에 결합.
- 초기 광범위 VRAM write callback 조사 `title-menu-source-loader-v1`은 timeout으로
  실패했으며 성공 증거에 포함하지 않는다. 좁은 native PC observer로 대체했다.
- title 그래픽 5개 테스트 PASS. 새 저장 커밋, 전체 플레이, 한글 입력/저장은
  이번 회귀의 검증 범위가 아니다. 전체 번역·자동 한글 자판은 여전히 미통합이다.

## 패치 생성

```powershell
python -X utf8 tools/package_tested_development_bps.py --name exe45_ko_development_title_menu_20261012 --rom poc/output/exe45_ko_development_title_menu_v1.gba --runtime-evidence poc/runtime/title-menu-v1-observer/verification.json
```

BPS와 xdelta는 각각 무패치 원본에서 같은 전체 결과를 재현하는 대체 형식이다.
둘 중 하나만 적용한다. 원본/패치/결과 SHA 검사와 덮어쓰기 방지 스크립트를 제공한다.
두 형식의 재적용, 반복 생성, 잘못된 원본 및 손상 패치 거부를 패키지 생성 단계에서
검사한다. 개발판 개인 테스트 패키지이며 공개 릴리스나 전체 번역 완성본이 아니다.
