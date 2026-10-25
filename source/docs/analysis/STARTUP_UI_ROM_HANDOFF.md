# 새 게임 초기 설정 ROM 후속

개발판만 확인한 기록이며 공개 릴리스 또는 초기 메뉴 전체 한글화 완료가 아니다.

## 채택한 결과

- 원본 SHA256: `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
- ROM: `poc/output/exe45_ko_development_startup_ui_v1_r7.gba`.
- ROM SHA256: `1c0b9e9ba71d7a53d81e20b09f5fb95a74a903835de083059678f7bbef5e32de`.
- 독립 `_repro.gba`와 전체 바이트 동일.
- 기존 2,596개와 모든 선택 자산 보존; 초기 설정 41개, 내비 이름 4개, 록맨 메일 알림 7개 추가. 누적 2,648개/63개 아카이브, 미선택 669개 아카이브 보존.
- PET 첫 구매 감사/이름 입력 요청 BG와 날짜 화면 OBJ 버튼 설명을 원래 글꼴에서 생성한 한글 타일로 적용. 버튼·판정·입력 저장 형식은 미변경.

## 원인과 구현

초기 UI 아카이브 `70904C`가 기존 적용 목록에서 누락되었다. 그 화면은 고정셀 `080554A4`가 아닌 별도의 비례폭 경로 `080556B8`로 출력된다.
따라서 텍스트만 추가한 r2는 원본 F9 디스패처가 확장 토큰 FC를 지원하지 않아 날짜 화면에서 잘못된 주소로 분기했다. r2는 실패 후보이며 패치로 배포하지 않는다.
r3부터 해당 경로에만 ARM7 Thumb 확장 디스패치/두 폭 테이블을 연결한다. 원본 하위 명령은 기존 핸들러로 보내고 각 한글 글리프 출력 뒤 원래 폰트 포인터를 복원한다. 코드/리터럴 풀 검증 및 원본 슬롯 핀 적용.

PET 안내는 텍스트 아카이브가 아닌 `63466C/634BB8`의 압축된 타일/맵이다. 원본 제목·프레임·배경·팔레트·편집 영역 밖 픽셀을 보존하고 새 압축 스트림을 ROM 뒤에 배치했다. 원본을 참조하던 주소의 전체 모집단 두 곳만 변경했다. 타일 수/맵 크기/원래 로더는 동일.
날짜 설명은 `539E54`의 35개 OBJ 타일이다. 실행 중 `06015200`의 전체 1120바이트가 원본과 일치하는 것을 먼저 확인했다. Galmuri7의 8픽셀 셀로 `늘림·줄임 / 다음 / 뒤로`를 만들고 같은 슬롯에 삽입한다. 방향키·A·B 아이콘과 sprite 프레임/팔레트는 보존한다.

## 빌드 및 검증

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_startup_ui_v1_r7 --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --title-weekend-menu --startup-ui
python -X utf8 tools/test_startup_assets.py
```

이미 존재하는 이름은 덮어쓰지 않으며 재실행은 새로운 이름으로 한다.
압축 독립 디코드/결정성/한도 초과 거부, 그래픽 원본 드리프트/잘못된 문구/정책 거부 회귀 3개 테스트 통과.
기존 선택 자산과 컴파일 결과 보존, 원본 헤더·계획된 모든 쓰기·겹침·추가 영역·입력/확정 코드 보존, 실제 컴파일 바이트와 포인터, 폰트/이미지 배치 및 독립 재빌드 감사 통과.

정확히 위 ROM의 Mesen 일반 입력 재생:

- `poc/runtime/startup-ui-v1-r7-newgame`: cold boot, 날짜 입력/확인, PET 구매 인사, 이름 `あ` 정상 입력, 성별/나이/직업/프로필 확인, 록맨 선택 및 첫 인사. 28/28 캡처.
- `poc/runtime/startup-ui-v1-r7-mail`: 같은 ROM 진단 체크포인트에서 초기 메일 알림. 5/5 캡처.
- `poc/runtime/startup-ui-v1-r7-verification.json`: 모든 증거 해시와 ROM 해시 연결. 날짜 OBJ 전체 VRAM 동일, PET 타일 전체 VRAM `8000` 및 맵 전체 EWRAM `1C800` 동일.
- `startup-ui-v1-r7-reload-title`: 별도 프로세스 타이틀 도달. 저장 완료/이어하기 검증은 아니며 당시 타이틀은 처음부터만 표시.
- `startup-ui-v1-r7-save`: 저장 메뉴 접근을 시도했지만 일반 입력이 메일함으로 진입했다. 저장 성공·재로드 증거로 사용하지 않는다. 메일 본문에 남은 일본어도 후속 대상이다.

## 개인 테스트 패치

`patches/exe45_ko_development_startup_ui_20261012.zip`

- ZIP SHA256: `7ff2decc42a459eea7a0ae612d785c4166f2c7e603e2ccaacdb6b57900e2ab28`.
- BPS SHA256: `a82e5ab874dc0dd06d135dd537389dfe4587bfaa59a1deb6f3482e86340d1c9d`.
- xdelta SHA256: `de2b2f5632dd78cec4b556caf357d79261cf087ca15d97ae8d132dacb9de3dfc`.
- 원본 재적용 시 전체 ROM 동일, 패치 결정성, 잘못된 원본/손상 패치 거부 및 PowerShell 래퍼 결과 동일/덮어쓰기 거부 통과.
- ROM/SAV/실행 파일은 ZIP에 포함하지 않는다. 원본에 BPS 또는 xdelta 중 하나만 적용한다.

## 가장 중요한 남은 조건

이름 입력의 가나판·기능 버튼, 내비 카드 그림 글자는 아직 원본. 자동 조합 한글 자판과 한글 이름/별명 확정·저장·재표시는 통합하지 않았다. 기존 자모 글꼴 공급을 실제 한글 입력 구현으로 설명하지 않는다.
새로 반영된 내비 이름 네 개 중 실제 선택 확인은 록맨 경로만 수행했다. 메일 호칭 `あくん`은 원래 동적 별명 그대로이며 다른 내비/분기와 전체 플레이 검증은 별도다.
번역은 needs_review이고 전체 게임 초안의 일괄 ROM 등록/공개 릴리스 승인도 남았다.
