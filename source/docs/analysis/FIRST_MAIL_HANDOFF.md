# 첫 I.P.C. 메일 한글화 후속 (2026-10-13)

## 산출물

누적 ROM: `poc/output/exe45_ko_development_first_mail_v2.gba`.
SHA256 `40d99164e2f0651f8e190afa7f7c1f73758117fe17bf111dbc86924840204635`, 11,227,648바이트.
독립 `_repro.gba`와 전체 바이트 동일. 원본 ROM은 변경하지 않았다.
선택 번역 2,678개/66아카이브, 미선택 아카이브 666개.
직전 내비 카드 이름 ROM의 2,648개 번역·글꼴·이미지·입력 기능을 보존했다.

추가 적용: 첫 I.P.C. 안내 메일 본문 23쪽, 메일함/록맨 안내/제목 등 7개.
전체 번역 초안 통합이나 한글 자동 조합·이름 저장 완료본이 아니다.
development-draft; NON-DISTRIBUTION, needs_review, 공개 릴리스 승인 없음.

## 입력·저장·소비 경로

기존 해시 고정 번역 초안에서 선택했으며 새 문구를 임의로 재작성하지 않았다.
`tools/first_mail.py`의 `SPECS`에 초안 해시·원본 포인터·용량·소비자 계약을 고정했다.
선택 입력은 `analysis/first_mail_v2/*_selected_asset.json`.
마지막 본문은 `translations/first_mail_layout_v2.json`으로 단어/순서 유지, 줄바꿈만 조정했다.

- `6DD9AC`: script0, 23개. 원래 본문 RAM `0202B2F4`, 8,192바이트 상한, 다음 자산 `0202D2F4`.
- `6DD0B8`: scripts0/1/9/10/11, 5개. RAM `02024000`, 8,192바이트 상한, 다음 자산 `020262F4`.
- `6DD63C`: scripts1/41, 2개. RAM `020262F4`, 4,096바이트 상한, 다음 자산 `020272F4`.
- 세 아카이브는 BIOS type-10 압축, 원래 디코더 `080EC158` (`11DF7047`)와 RAM 목적지 유지.
- 원래 압축 슬롯을 덮어쓰지 않고 확장 ROM에 4바이트 정렬로 배치. 원래 포인터 24+23+24개를 재지정했다.
- 본문 normal-dialogue 3줄/152픽셀, 세 번째 줄은 진행 화살표를 피하도록 132픽셀 상한.
- 메일함 목록/제목은 fixed-cell-big, 1줄/88픽셀. 록맨 안내는 normal-dialogue 2줄/132픽셀.
- 이전 선택 아카이브의 컴파일 해시/제어/배치 계약, 기존 글꼴 은행, 예상 원본 쓰기 집합을 독립 감사했다.

## 실패 후보와 수정

`first_mail_v1`은 마지막 페이지 세 번째 줄이 148픽셀로 진행 화살표와 겹쳤다.
실패 화면 `poc/runtime/first-mail-v1-read/step_032.png`, v1 ROM은 보존하되 패키지에서 제외했다.
v2 마지막 페이지는 `부디 주의하시며, / 쾌적한 넷 배틀러 생활을 / 즐기시길 바랍니다`.
세 번째 줄 104픽셀, 실제 `first-mail-v2-read/step_032.png`에서 겹침 해소 확인.

첫 자동 검증은 context+34를 고정 script 시작, +2C를 keyWait 이후로 오인했다.
실제 23페이지 RAM에서 +2C는 대기 중 E6 opcode 자체, +34는 페이지별 bookmark임을 확인했다.
다음 bookmark는 이전 대기 opcode 주소+3이며 원래 E6 00 F1 경계를 검사한다.
실패 보고서 `runtime_verification.json`, `_r2.json`은 first_mail_verified가 없으며 패키지 근거로 사용하지 않았다.
유효 근거는 `analysis/first_mail_v2/runtime_verification_r3.json`이다.

## 실제 검증

핀 고정 격리 Mesen, 이번 ROM의 일반 패드 입력과 이번 ROM에서 만든 상태만 사용했다.
RAM/캐릭터/해금/진행도 치환 없음. 사용자 SAV는 수정하지 않았다.

- `poc/runtime/first-mail-v2-boot`: 처음부터, 날짜/환영/이름 입력.
- `...-pagecycle`: 가나 세 페이지 전환·재진입, 기능 버튼/VRAM/BG2 맵.
- `...-complete`: 일본어 한 글자 이름 확정·프로필·록맨 확인·PET 초기 메일 알림.
- `...-read`: 7 메일함, 8 목록/새 메일, 10..32 본문 23쪽, 33 읽기 완료/목록, 34 첫 페이지 재열기.
- 모든 23쪽의 실제 화면을 검토했다. 전체 본문/메일함/제목 아카이브 RAM이 현재 ROM의 해제 결과와 동일했다.
- 모든 본문 keyWait 주소와 페이지 bookmark, 순서/누락 없음 및 재열기를 검사했다.
- `...-selection`: 록맨·롤·거츠맨·넘버맨 이동·확인·취소, 전체 21개 이름 은행 업로드 및 OAM ID 검증.
- 독립 재빌드 동일, 선택 데이터 3개 테스트 통과, 기본 원본/제어/압축/포인터/최종 배치 감사 통과.

재현: 이전 내비 카드 빌드의 모든 플래그에 `--first-mail`을 추가한다.
`tools/run_first_mail_regression.py`, `tools/verify_first_mail_runtime.py`로 새 이름의 런타임 증거를 생성한다.
기존 ROM·보고서·폴더는 덮어쓰지 않는다.

## 패키지

`patches/exe45_ko_development_first_mail_20261013.zip` 및 동명 폴더.
ZIP SHA256 `b07542648064479d3a0e9ad95e078c81089880d45edc8a5f563de3a131069d1e`.
BPS SHA256 `f3b6743824ca9e009ef9e93a47fb91947af8efd0678e719975b86bd1d8d181fe`.
xdelta SHA256 `0eae99b01ff3ea1a9191ca05e17da50763000b59ddcbd05663d2f68a84764a47`.
두 패치는 대체 형식이다. 둘 중 하나만 지정 무패치 원본에 적용하며 이전 패치 ROM에 겹쳐 적용하지 않는다.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
두 형식의 재적용 전체 바이트 동일/확장 크기/결정적 생성/다른 원본·손상 패치 거부 PASS.
적용 스크립트의 전체 바이트 동일/출력 덮어쓰기 거부/패치 ROM 소스 거부 PASS.
패키지에는 ROM/SAV/실행 파일이 없으며 원본을 변경하지 않는다.

## 남은 작업

다른 메일 본문과 다른 내비의 메일함 대사, 가나 글자판과 자동 한글 조합/저장, 전체 초안 통합은 미완료.
이번 ROM에서 새 저장·이어하기/새 프로세스 저장 재로드는 수행하지 않았다.
동적 일본어 이름과 접미사, NAVI SELECT 제목은 원래대로이다.
잠긴 17개 내비의 실제 해금/플레이와 전체 플레이/공개 릴리스 승인도 미검증이다.
다음 적용은 기존 초안의 다른 메일 본문을 원래 소비 경로와 조건별로 선택·검증하는 것이 적절하다.
