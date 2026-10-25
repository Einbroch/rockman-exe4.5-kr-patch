# 주말 대회 메뉴 (2026-10-12)

현재 추가 적용 범위는 메인 메뉴 세 번째 항목 `どにちのたいかい` → `주말 대회`이다.
원본 픽셀과 [공식 설명서](https://www.nintendo.co.jp/data/software/manual/manual_pc5j_00.pdf)의
토·일 공식 대회 설명을 대조했다. `translations/title_menu_weekend_graphics_ko.json`을
별도 입력으로 추가하여 이전 두 메뉴 번역 입력도 재현 가능한 상태로 보존했다.

`tools/title_menu_graphics.py`는 기존 열 0..5, 10..15의 48×16 라벨 외에 열 16..25의
80×16 라벨을 지원한다. 배경/글자/그림자 역할은 0/1/2이며 다른 팔레트·메타데이터·
로고·커서·중간 빈 타일은 변경하지 않는다. 기존 두 한글 라벨의 해제된 타일은 같다.
LZ10 결과 592바이트를 기존 657바이트 슬롯 안에 넣는다. 위치·포인터·로더·
해제 크기·VRAM 소비 규칙·참가 조건을 변경하지 않는다.

## 빌드와 정체성

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_weekend_menu_v1 --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --title-weekend-menu
```

`--name exe45_ko_development_weekend_menu_v1_repro`로 원본부터 다시 빌드해 전체 동일성을 확인했다.
SHA-256은 두 번 모두 `4b9ed3427001e08931fce46f76fed7d1e220553b15e8297f81e53ac51f0a50b7`이다.
60아카이브/2596텍스트 문구/672미변경 아카이브를 유지한다. 직전 ROM과 다른 405바이트는
모두 0x7CEA94..0x7CED24의 원래 압축 공간에 한정되며 그 밖의 전체 ROM은 같다.

## 런타임

- `poc/runtime/weekend-menu-v1-nosave`: 무저장 coldboot, 처음부터 표시와 A 진입.
  날짜 초기 설정 화면까지 관측. 세 캡처 모두 생성됐고 4번 화면 직접 확인했다.
- `poc/runtime/weekend-menu-v1-withsave`: 기존 개발판이 생성했던 native SAV/RTC를
  이번 ROM만의 격리 이름에 복사하고 체크포인트 없이 coldboot.
  2이어하기→3처음부터→4이어하기→5주말 대회→6이어하기→7내비 선택으로 정상 입력.
  전체 타일 시트의 VRAM 동일성, OAM 소비 및 3항목 선택/비선택 팔레트를 검증했다.
  2/3/5/7번 화면 직접 확인했다.
- `poc/runtime/weekend-menu-v1-observer`: 읽기 전용 native 해제/복사 관측 포함.
  2이어하기→3주말 대회→4A 진입→5B 입력. 3/4/5번 화면 직접 확인했다.
  날짜 설정 및 날짜 변경 전 저장 안내로 정상 전환됐다. 5번 B 입력은 타이틀 복귀를
  증명하지 않으며 안내의 다음 페이지로 진행했다. 날짜 수정·확정을 하지 않았다.
- native 해제 전체 payload와 VRAM 전체 시트가 기대값과 일치한다.
  첫 4바이트 헤더 제외 1664바이트 복사 ABI도 기존과 같다.
- 사용한 SAV SHA-256은 실행 전후
  `5f21f85bf13ec7b4ce5a37aaa511fe674760c17454974870161fc98701d39440`으로 같다.
  무저장 실행 후 테스트용 SAV/RTC는 해당 nosave 증거 폴더에 먼저 보존했다.
  사용자 세이브를 수정하거나 다른 에뮬레이터를 종료하지 않았다.
- `tools/report_title_menu.py --weekend`의 초기 실행은 로컬 변수 이름 충돌로 재빌드
  비교 경로를 잘못 계산해 보고서를 생성하지 못했다. 변수 수정 후 모든 검증 PASS.
  이것은 ROM 수정이나 런타임 실패가 아니며 최종 증거는 observer/verification.json이다.
- title 그래픽 테스트 6개 PASS. 실제 대회 출전·완료, 다른 저장 파일 호환성,
  전체 번역·한글 입력/저장 완료를 주장하지 않는다.

## 패치와 남은 범위

```powershell
python -X utf8 tools/package_tested_development_bps.py --name exe45_ko_development_weekend_menu_20261012 --rom poc/output/exe45_ko_development_weekend_menu_v1.gba --runtime-evidence poc/runtime/weekend-menu-v1-observer/verification.json
```

BPS/xdelta 두 대체 형식 모두 적용 결과 전체 동일성, 반복 생성, 잘못된 원본·손상 패치 거부,
Windows 적용 스크립트의 해시 검사/덮어쓰기 방지를 검증한다. 무패치 일본판에 하나만 적용한다.
개발판 개인 테스트 패키지이며 공개 릴리스나 전체 번역 완성본이 아니다.
사용자가 이번에 첨부한 12장에 남은 일본어는 `USER_SCREENSHOT_UNTRANSLATED_20261012.md`에서
따로 추적한다. 초기 설정·프로필·키보드·록맨 대사는 이번 패치에서 추가 번역하지 않았다.
