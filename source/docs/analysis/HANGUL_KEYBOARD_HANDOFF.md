# 실제 한글 자판 — 현재 작업 인계

## 2026-10-25 저장 형식 결정 (Claude Code 이어받음) — 아래 모든 절보다 우선

사용자 결정 `exe45.hangul-keyboard.record-format-A`: **첫 바이트 한글 표시 + 글자마다 7비트 두 바이트, 글자 수는 일본어와 같게.**

- 칸 한도 N자 기록(2N+2바이트) = `80` + 글자당 (hi7, lo7) + `E5` + `00` 채움.
- 값 = 음절 순번(0..11171) 또는 11172+원작 1바이트 문자(0x00..0xE3, 영문·숫자·기호·공백).
- 두 바이트가 모두 0x80 미만이라 E5(종료)·98(입력 빈칸)·E4..FF(제어)와 겹치지 않는다. 코덱스 후보(LE16 순번)는 「곥」 등에서 E5가 섞여 원작 importer 0803558C가 빈 문자열로 읽던 문제가 있었는데, 이 형식에서는 생기지 않는다.
- 음절이 하나도 없으면 원작 형식(표시 1)으로 쓴다. 원작 reader 루프는 표시 0만 빈 기록으로 본다(record_markers.json).
- 표시할 때만 F9FC+LE16(korean_codec)으로 펼친다. 최대 4N+1바이트.
- 기준 구현 `tools/hangul_record_v2.py`, 전수 검사 `tools/test_hangul_record_v2.py`: 왕복 79,800건·거부 30건 통과.
  - 4/6/8자 칸에서 모든 음절을 첫 칸과 꽉 찬 마지막 칸에 넣어 봤다.
  - 원작 1바이트 문자 228종을 한글 앞·뒤에 섞어 봤다.
- 표시 경로 조사(10/25):
  - 모든 입력값 출력은 F9 0C xx 한 계열이고, 설명자 71개 표는 ROM 0x526D0([포인터, 크기]×71)에 있다.
  - 표를 읽는 코드는 0x35D7C·0x38DE8·0x3A160·0x5181C 네 곳이다.
  - 31(이름 0x2000E51)·1(별명)·2·8·10~13·15·16·18·20·22~27·32~64는 기록 첫 바이트 바로 뒤를 가리킨다. 그래서 `포인터-1 == 80` 이면 한글 기록이다.
  - 3~7·9·14·17·19·21은 여러 기록 중 하나를 골라 0x20293E0부터 32바이트 간격의 버퍼에 **본문만** 복사한다. 그래서 표시 바이트가 사라진다. 이 복사(0x38BB4 → 08032AC6 계열)에서 한글 여부를 넘길 방법을 다음에 정해야 한다.
  - N=8 표시 확장은 33바이트로 32바이트 간격을 넘으므로, 복사 버퍼에 펼친 형태를 그대로 쓰지 않는다.
- **표시 훅 v1** (`tools/hangul_display_hooks_v1.py`, 10/25). 원본 명령 12바이트를 push{r3}/ldr/bx 스텁으로 바꾸는 두 곳이다.
  - 복사 0x38BF8(선택기 0x08038B94):
    - 설명자 조회를 재현한 뒤 원작 E5 복사 0x08032AC6을 그대로 부른다. A형식 본문에는 E5가 없어서 그대로 정확히 복사된다.
    - 원 기록 표시가 80이고 검증을 통과하면, 버퍼의 [크기] 위치에 서명 `80, 체크섬`을 쓴다. 아니면 그 바이트를 지운다.
    - 이 영역은 다른 화면에서 그림 데이터로 재사용되므로 한 바이트 표시만으로는 부족해서 체크섬을 쓴다.
  - 출력 0x517F8(F9 0C 처리기 0x080517D0, 128바이트 출력 칸 0x02010AC0+n×128):
    - 복사 버퍼이고 서명이 맞거나, 프로필 기록 영역(0x02000E51~0x020011E1)이고 앞 바이트가 80이면 F9FC로 펼친다.
    - 그 밖이나 검증 실패면 원작 memcpy 0x0800094C를 쓴다.
  - 크기: 복사 136B, 출력 296B. 추가 RAM은 없다.
  - CPU 검사 `tools/bench_hangul_display_hooks_v1.py` → `hangul_keyboard_v1/cpu_display_hooks_v1/report.json`. 원본 ROM+스텁, 실제 원작 복사·memcpy 실행.
    - 복사 한글 25,344 / 일본어 3,000 / 거부 40
    - 출력 한글 57,488 / 원작 3,052 / 거부 50
    - r4~r7·SP 보존 통과
  - 별명(설명자 1, 0x2000E5F)은 이름+호칭을 합쳐 만드는 코드(0x08032AB6 계열)가 따로 있다. 그 결과도 A형식이 되도록 다음에 확인해야 한다.
- **훅 v2** (`tools/hangul_display_hooks_v2.py`, 10/25). 출력 v2 488B, 확정 216B, 복사는 v1 그대로.
  - 출력: v1에 두 가지를 더했다.
    - 32바이트 작업 버퍼(0x0200FC80 편집 평탄 문자열·0x02014E54 일정·0x02014E74 확정 메아리)는 +30/31 서명으로 판정한다.
    - 프로필 기록 영역은 짝 뒤에 0x80 이상 바이트가 오면, 거기서부터 E5까지 원작/F9FC 꼬리로 그대로 복사한다. 별명 조립기 0x08038F60이 이름 기록(표시 바이트 포함)을 0x02000E5E에 복사하고 호칭(065부터 F9FC)을 이어 붙이기 때문이다.
  - 확정: 0x08035000 함수 전체를 스텁으로 바꿨다. 호출자는 BL 0x08034FA0 하나뿐이다.
    - 평탄 버퍼에 서명이 있으면 기록을 `80+본문+E5`로 쓰고, 메아리 0x02014E74에도 서명을 남긴다.
    - 서명이 없으면 원작과 똑같이 동작하고(표시 1, E5/98에서 멈춤), 메아리 서명은 지운다.
  - Keystone 함정: 조건 분기가 ±256B를 넘으면 경고 없이 Thumb-2 .w 분기를 틀린 대상으로 만든다. `far()`로 "반대 조건 + b"로 바꾼다.
  - CPU 검사 `tools/bench_hangul_display_hooks_v2.py` → `cpu_display_hooks_v2/report.json`. 기준은 066 ROM(호칭 한글)+스텁 3개.
    - 출력 한글 45,144 / 거부 155
    - 별명(실제 조립기, 호칭 번호 0~3) 3,000
    - 확정 한글 1,500 / 원작·무서명·체크섬 오류 4,500건은 수정 전 066 함수와 바이트 동일
    - 작업 버퍼 4,000
  - 남은 위험: 원작 모드 편집에서 평탄 버퍼 +30/31의 낡은 서명은 자판 UI(편집 시작)에서 반드시 지워야 한다. 체크섬 우연 일치 확률은 1/256이다.
  - 달력 이름(일정 기록 22B=10자)은 A형식이 들어가도 달력 쪽 복사기(33344/3335A/3336E 등)가 아직 서명을 모른다. 자판을 달력에서 쓰기 전에 연결해야 한다.
- **자판 통합 설계 (10/25, 코덱스의 editor96/compact76 대체 방식 대신 원작 편집기 재사용)**
  - 원작 편집기:
    - 상태 0x0200FC40. +4 한도 N, +0x10 칸 시작 0x0200FC60, +0x18 끝, +0x1C 목적지.
    - 칸은 16비트 word다. 하위 바이트가 문자이고, E4면 상위 바이트까지 2바이트 문자다.
    - 매 프레임 0x080355F6이 빈칸을 0x0098로 채우고 E5를 붙이고, 0x0803562C가 칸을 바이트로 펴서 0x0200FC80에 쓴다.
  - 한글 칸 word = `(0x80|lo7)<<8 | hi7`.
    - 값 v는 A형식 값과 같다. 음절 0..11171, 원작 1바이트 11172+code.
    - 낱자모만 새 값 11400+j(j=0..39)로 쓰며, 표시할 때 F9FC 11174+j가 된다(현재 ROM 자모 글꼴, 065 메타 `hangul_keyboard_glyphs`).
    - 원작 word는 상위 바이트가 0이거나 하위 바이트가 E4라서 겹치지 않는다.
  - 고칠 곳:
    1. 평탄화 0x0803562C 훅: 한글 word가 있으면 A형식 짝 + 98 꼬리 + E5 + 서명을 쓰고, 없으면 원작대로 하고 서명을 지운다.
    2. 출력 v3: 작업 버퍼에 98 꼬리와 낱자모 값을 허용한다.
    3. 확정 v3: 98/E5에서 멈추고, 낱자모는 버린다.
    4. A/B 처리기(0x08034F08 BL 0x080353B0) 훅: 한글 쪽이면 격자 → 자모 → 산술 조합기가 마지막 칸을 바꾸고, B는 자모 단위로 지운다(표준 분해 순서).
    5. 자판 쪽 그림: kana_replacement page0 후보를 쓰되, 원작 쪽 전송(356D0) 위치를 확인해야 한다.
  - 조합은 rank=(L×21+V)×28+T 산술과 작은 결합표(겹모음 7, 겹받침 11)로 한다. 코덱스의 1.79MB 전이표는 쓰지 않는다.
- **구현 완료(CPU 검사까지, 10/25)**
  - `tools/hangul_record_v3.py`(형식 A v3):
    - 저장값을 값+1로 바꿨다. 원작 빈 입력 검사(0x00 건너뜀) 때문에 「가」 단독이 빈 입력으로 보이던 문제를 막는다.
    - 2바이트 원작 문자 E4 xx를 11440+xx로 넣었다(기호 쪽 3자).
  - `tools/hangul_editor_v1.py`: 원작 편집기 위 조합 기준 모델.
    - 코덱스 모델과 무작위 입력 2만 건이 일치했다.
    - 11,172 음절 전부 입력 → B로 0까지 지우기 통과.
  - `tools/hangul_keyboard_hooks_v1.py`: 복사·출력·확정·평탄화·자판(A/B) 훅 5개 + 조합표, 3,252B. 조합은 산술로 하고 BIOS 나눗셈은 쓰지 않는다.
  - `tools/keyboard_page_v1.py`: 쪽 0 격자(열 2~23)만 코덱스 자모 칸으로 바꾸고, 명령 라벨 열(24~27, 한글)은 유지한다. 빈 타일 칸은 139개 남는다.
  - CPU 검사:
    - `bench_hangul_keyboard_hooks_v1.py`:
      - 입력 세션 4,000, 한글 키 61,388(수락 13,600·규칙 거부 13,868), 한글 B 6,092
      - 원작 넘김 19,937건은 066과 바이트 동일
      - 평탄화 87,417 / 입력창 출력 48,719 / 확정 48,719
    - `bench_hangul_keyboard_records_v1.py`: 기록 경로(v2 검사 이식) 모두 통과.
  - 함정:
    - 원작 사운드 함수 0x08000534는 `bx lr`로 돌아온다. `mov lr,pc` 호출은 ARM으로 튀므로 lr에 Thumb 비트를 넣는다.
    - Thumb-1 `adds Rd,Rn,#imm`은 0~7만 받는다.
  - 설치 단계 `tools/keyboard_stage068_v1.py`(+`make_keyboard_stage068_v1.py`, `run_normal_keyboard068_v1.py`)는 067 위에 쌓는다. 066 ROM으로 미리 돌려 보니 검증·되돌림 모두 통과했다.
- **068 실기(격리 Mesen) 결과 (10/25)**
  - `pending500_068_v1.gba`(8609ee44…, repro 동일)에서 정상 진행 16구간이 모두 끝났다.
  - 이름 자판 화면에 자모 격자가 나오고, 명령 라벨은 한글로 유지된다.
  - `run_keyboard_probe068_v1.py`로 068 자체 체크포인트에서 「한글」(ㅎㅏㄴㄱㅡㄹ)을 입력했다.
    - 조합이 단계별로 맞게 됐다.
    - 확정 → 성별·나이·직업 → 확인 → 내비 선택까지 정지 없이 진행됐다.
  - RAM 확인:
    - 이름 기록 `80 525d 0401 E5`(「한글」), 메아리 서명, 평탄 버퍼 서명 모두 정상이다.
    - 표준 진행 레시피는 「ㄱ」만 치고 확정해서 빈 이름(01 E5)이 됐다. 낱자모를 버리는 설계대로다.
  - 화면 문제: 입력창과 프로필 확인창이 A형식 바이트를 가나로 보여 줬다(예: 「ベヴ30」).
    - 원인은 고정 칸 파서(IWRAM, ROM 사본 0x1EF900)의 자체 F9 0C 처리기 0x03006A1C였다. memcpy 리터럴 ROM 0x1EF96C를 쓰고, 읽기 감시로 확인했다.
  - **069**: `hangul_keyboard_hooks_v2.fcopy`(memcpy 규약, v1 출력 훅과 같은 판정·전개)로 그 리터럴만 바꾼다.
    - 차분 CPU 20,000건이 v1 출력 훅과 바이트 동일했다.
  - 남은 화면: 일정 화면 날짜 「(木)」는 또 다른 글꼴이다(PET 상단 요일 띠와 다름).
- 아직 ROM 설치 전이다. 남은 일:
  - 이 형식을 쓰는 확정(commit)·불러오기(import)·표시(provider) 훅
  - 자판 화면 교체(kana_replacement 후보)
  - 조합기 연결
  - 세이브·재실행 확인

## 2026-10-12 실제 native 저장 회귀 후속

같은 `save_keyboard_fonts_v1` ROM에서 이름 ‘あ’를 저장하고 Control reset 후 확인했다.
게임 생성64KB SAV를 보존한 뒤 pinned isolated testRunner의 새 프로세스에서 cold boot/
이어하기/록맨/PET까지 진행했다. state 없이 시작한3개 EWRAM snapshot 모두
초기 이름14byte 필드 `0x02000E50`가 `019be57ee5000000000000000000`로 일치했다.
SAV 전체 bytes도 동일했다. 근거: `poc/runtime/save-keyboard-fonts-v1-save-regression/`
및 `save-keyboard-fonts-v1-fresh-reload-r2/`. 자체 PET state 로드도 성공했다.
자동 한글 자판과 한글 저장의 완료가 아니다. ROM 추가 변경은 없다.
입력 read BP로 실제 Down 전달과 native 선택 index6을 확인해 저장 메뉴에 진입했다.
이름 필드14/표시13 및 nickname21bytes는 달력22byte 저장 ABI와 구분해야 한다.
상세 실패/재시도, launcher의 portable 초기화, 자체 SAV 이동, 환경 차이를 README에 기록했다.

## 2026-10-12 실제 ROM 중간 통합·실행

`poc/output/exe45_ko_development_save_keyboard_fonts_v1.gba`를 원본에서 생성했다.
SHA256 `ba12b55165e2c50c2779ba098b9066140cf95572241cb8dcf7ab04ae984489d7`.
기존 저장 UI를 포함한 2,596 선택 번역과 자모 글꼴을 함께 공급했다.
`poc/runtime/save-keyboard-fonts-v1/README.md`, `static_audit.json`,
`runtime_evidence.json`에 실제 실행/화면/범위와 두 자체 state를 기록했다.
이름 입력·삭제·확정·프로필 재표시·PET/달력 진입까지 정상 입력으로 관찰했다.
한글 이름/확정 UI는 표시되지만 자판과 입력은 일본어이다. 자동 조합·저장 hook과
미등록 새 번역은 미반영이며 native SAV commit/reload도 미완료다.
이 중간 ROM을 한글 자판 통합 완료본이나 새 플레이 기준으로 승격하지 않는다.
실제 ROM test를 CPU PASS 또는 이전 baseline boot로 대신하지 않았다.
다음 시험은 이 ROM 자체 `pet_menu.mss`에서 재개할 수 있으나 state 로드 검증은 아직 없다.

ID: `exe45.hangul-keyboard.v1` / 2026-10-09 / 구현 진행 중, ROM 통합 미완료.

## 사용자 결정

결정 ID `exe45.hangul-keyboard.automatic-composition`.
사용자의 요청은 일본어 글자판의 표시만 번역하는 것이 아니라 실제 한글 입력 기능이다.
질문은 “자음·모음을 누르면 자동으로 음절이 조합되는 두벌식 방식으로 진행할까요?
게임패드에서 조작할 수 있도록 글자판 배치는 별도로 맞추겠습니다.”였고,
사용자는 **“자동 조합 방식으로 진행”**을 선택했다.
자동 자모 조합을 채택한다. 초기/중성/종성 각각 고르는 다른 UX로 축소하지 않는다.
아래 40선택자 게임패드 배치는 구현 후보이며 사용자 승인된 최종 배치라는 뜻이 아니다.
저장 공간 때문에 지원 음절 범위를 축소하는 결정도 내려진 적 없다.
전체 입력·삭제·수정·확정/취소·대사 재표시·저장/재실행 경로가 완료 조건이다.

## 기준 ROM과 변경 범위

현재 누적 제품은 `poc/output/exe45_ko_development_input_heading_v1_r2.gba`.
SHA256 `5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4`.
동일 bytes인 `_v1.gba`로 정상 입력 추적을 실행했다.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
기존 제품 ROM/번역 원문/사용자 세이브는 보존한다. 아래 글꼴 공급 후보 ROM만 별도 생성했다.
현재 제품의 한글 입력 지원을 주장하지 않는다. NON-DISTRIBUTION.
이전 제품 검증은 `INPUT_HEADING_HANDOFF.md`에 유지한다.
그 제품의 748 도구 고정은 당시 빌드의 기록이며 이번 신규 도구까지 고정했다는 뜻이 아니다.

## 확립한 구현과 검증

`tools/hangul_keyboard_model.py`는 호스트 자동 조합 기준 구현이다.
19초성/21중성/28종성, 겹초성·복합모음·겹받침과 다음 모음 입력 시 받침 이동을 처리한다.
유효하지 않은 선택/초성 없는 모음/용량 초과는 상태와 삭제 이력을 변경하지 않는다.
B는 새 입력의 마지막 자모 동작을 되돌린다. 확정 후보 조회도 편집 상태를 변경하지 않는다.
외부에서 불러온 완성형 문자열은 마지막 음절을 조합 상태로 열어 수정할 수 있다.
불러오기에는 원래 키 이력이 없으므로 B는 명시된 표준 분해 순서를 사용한다
(예: 괙→괘→과→고→ㄱ→빈 문자열). 이 API는 실제 게임 저장 데이터 해독기가 아니다.
현재 단독 모음 입력 거부/미완성 초성 확정 거부는 기준 구현 동작이며 실제 게임 UX 검증 전이다.

`tools/test_hangul_keyboard_model.py`: 11개 계약 검사 PASS.
현대 한글 11,172개 각각의 생성/입력 되돌리기, 불러온 11,172개 각각의 삭제/재입력 검사 포함.
4글자 용량 검사는 명시적 호스트 매개변수 검사이며 모든 게임 입력 필드의 한글 용량 보증이 아니다.

`tools/bench_hangul_input_encoder.py`: Thumb-1 완성 음절 인코더 11,187 CPU 벡터 PASS.
L/V/T→기존 F9FC+16비트 음절 인덱스, 유효 음절 11,172개 및 잘못된 인덱스 표본 15개.
ABI/쓰기 경계/반환값 검증은 독립 CPU 픽스처 범위다.
자동 조합 상태 머신 전체의 네이티브 구현 또는 설치된 ROM 훅이 아니다.

`tools/prepare_hangul_keyboard_candidates.py`: 기존 Galmuri 고정 셀 기준으로 40자모 후보 뱅크 생성.
15열×7행 105선택지 중 40활성/65비활성 후보, 8×16 셀 2,560 bytes.
`hangul_keyboard_v1/candidates/layout_preview.png`는 정적 미리보기이며 게임 스크린샷이 아니다.
실제 공급자/팔레트/VRAM 업로드/비활성 칸 선택 거부는 아직 설치·검증하지 않았다.

## 정상 실행 관찰과 저장 경계

두 격리 경로는 현행 동일 ROM의 자체 빈 입력창 체크포인트에서 일반 패드 입력만 재생했다.
RAM/플래그/레코드 강제 변경 및 read alias 없음.

- `poc/runtime/hangul-keyboard-v1-native-edit/`: あ→い→B→い→결정→예, 15/15 캡처.
- `poc/runtime/hangul-keyboard-v1-record-readers-r2/`: 같은 정상 경로, 입력 필드 CPU 읽기 관찰.

편집어는 0200FC60의 16비트 칸, 평탄화 출력은 0200FC80.
08035000은 목적지 020010A6의 첫 바이트에 constant marker 1을 쓰고
평탄화된 일본어 bytes를 +1부터 E5/98까지 복사한다.
08032AC6의 정상 호출은 020010A7→02014E74로 9B9CE5를 복사하고 r0=2를 반환했다.
최종 10바이트 관찰창은 `019b9ce5e50000000000`이다.

추가 CPU reader 08038BB4에서 r6=0803B1B0,
원본과 동일한 16바이트 메타데이터 `011004211d0a000a5d0a2d0ba40e5607`를 관찰했다.
그 루틴은 메타데이터 +2의 값 4로 `2*4+2=10`의 레코드 간격을 계산한다.
+14 오프셋 0756과 루트 02000950의 합은 실제 필드 020010A6과 일치한다.
출력 descriptor index 16의 포인터는 020010A7로,
후속 08032AC6 호출은 **원래 레코드 내부에 제자리 복사**하는 경로다.
이 메타데이터/루틴의 원본 bytes 보존을 검증했다.

따라서 이번 질문의 네이티브 10바이트 간격은 단순 인접 마커 추정에서 확인된 소비자 계산으로 승격했다.
하지만 모든 입력 필드/모든 reader/저장 검증 규칙의 조사는 완료되지 않았다.
전체 CFG/ISA 분석 완료도 아니다. 실제 관찰 reader의 첫 명령만 자동 감사한다.
제자리 경로를 그대로 두고 저장된 한글을 4바이트 표시 코드로 펼치면 옆 칸을 침범할 수 있다.
F9FC 코드 4글자=16 bytes를 기존 기록에 그대로 넣는 방법은 배제한다.
새 marker/packed 저장 표현/안전한 작업 RAM/표시 변환 ABI는 아직 채택하지 않았다.

## 재검증과 다음 작업

통합 기반 보고서: `hangul_keyboard_v1/foundation.json`.
ROM/원본/tool/후보/CPU/정상 trace 해시, 검사 출력과 제한을 연결한다.
재검증: `python -X utf8 tools/verify_hangul_keyboard_foundation.py`.
이 PASS는 기반 구현·관찰에 한정되며 ROM readiness나 사용자 한글 입력 지원 PASS가 아니다.

다음은 아래 새 소비자 조사와 저장 변환 후보를 기준으로, 전용 입력 descriptor와
별도 공용 문자열 descriptor28..30 공급 경로를 구분해 저장 표현과 표시 확장을 연결하는 것이다.
descriptor16 제자리 복사를 범용 확장 훅으로 쓰지 않는다.
이어 자판 셀 선택/조합 상태 초기화·취소 수명/편집 표시/평탄화 훅의 실제 호출 계약과
예약 RAM을 확인한 뒤, 원본 기반 누적 빌드에 설치한다.
완료 검증은 실제 자모 조작, 겹받침 이동, B/재입력, 최대치와 초과 입력,
확정/아니요, 대사 재표시, 실제 저장→savestate 없는 재실행 복원,
기존 일본어 세이브 호환을 포함한다. 아직 어느 것도 한글 ROM 실행 증거로 확보하지 않았다.

## 후속 구현: 고정 크기 기록 변환 후보와 소비자 구분

`tools/analyze_keyboard_consumers.py`가 원본 추출 inventory 해시로 고정한
732개 canonical TPL 전체에서 문자열 리터럴을 제외한 named F90Cxx 명령을 조사했다.
3,803개 참조 중 printWorstSubject는 68개다.
`printWorstSubject`는 F90C10 / descriptor16이고, `printStringBuffer1..3`는
descriptor28..30이다. 따라서 앞서 모든 입력을 공용 문자열 버퍼로 표시할 것처럼
다루었던 후보 설명은 수정한다. 같은 근본 입력 기능이라도 서로 다른 공급자 경로다.
named 명령의 전체 source 조사이지 variable buffer ID/전체 네이티브 reader 조사가 아니다.
메타데이터 26행의 구조적 조사도 추가했다. 각 행은 count/4·6·8 logical limit/
record 간격/필드 범위/descriptor 포인터를 기록한다. 전체 게임의 record population을
확정한 것이 아니며 정상 실행으로 메타데이터를 확인한 행은 기존 row14다.
근거는 `hangul_keyboard_v1/consumer_inventory.json`이다.

`tools/hangul_record_candidate.py`는 새 고정 크기 표현을 **실험 후보**로 구현했다.
최대 logical_limit을 N(1..8)이라고 할 때 정확히 2*N+2 bytes를 사용한다.
marker=80h|글자수, 유효 음절 rank를 little-endian 16비트로 저장,
미사용 word=FFFFh, 마지막 byte=E5h로 제안했다.
표시 시에만 기존 F9FC 코드를 만들어 4*글자수+1 bytes로 확장한다.
빈 입력/자모/범위 밖 rank/잘못된 marker·종결자·빈 칸·길이는 거부한다.
**81h..88h marker는 네이티브 소비자와 저장 검증의 안전성이 아직 증명되지 않았다.**
이 표현은 저장 ABI로 채택하지 않았고, ROM이나 실제 세이브에 쓰지 않았다.
5개 호스트 계약 검사가 통과했다. 현대 한글 전부의 4·8글자 필드 각 위치 roundtrip,
16비트 occupied rank와 empty word의 전체 값 영역, marker/terminator 전체 256값 검사 포함.

`tools/bench_hangul_record_decoder.py`는 이 후보를 표시 코드로 풀어내는
162-byte Thumb-1 함수를 실제 기계어로 생성하고 독립 CPU에서 실행했다.
유효 134,136 / 거부 291 벡터 PASS. 4·8칸의 모든 위치에 현대 한글11,172개를
각각 배치했고, 다른 크기는 occupancy/용량/인접경계/잘못된 데이터 표본을 검사했다.
모든 구조를 검증한 뒤에만 출력한다. 부족한 목적지 용량/겹치는 버퍼/잘못된 데이터는
출력 무변경이며 callee registers와 SP를 보존한다. 입력/출력 포인터의 유효 메모리와
길이는 CPU 픽스처의 호출 계약이며 게임 RAM 예약 증거가 아니다.
`hangul_keyboard_v1/cpu_record_decoder/report.json`이 기계어와 도구 해시를 고정한다.
자동 조합 상태 머신 전체를 Thumb으로 옮긴 것은 아니고 실제 ROM hook도 아니다.

`tools/bench_native_keyboard_storage.py`는 현행 ROM의 실제 08035000 writer와
08032AC6 복사 코드를 독립 CPU에서 실행해, F9FC를 그대로 저장하는 실패를 재현했다.
한 음절 전체11,172개 중 87개가 payload의98h/E5h 때문에 중간에서 끊겼다.
`가가가가`는 marker 포함18bytes를 써서 관찰된10byte칸을8bytes 넘었다.
이것은 예상한 위험의 재현 PASS이지 한글 기능 PASS가 아니다.
`hangul_keyboard_v1/native_storage_risks.json`에 해당87개와 bytes·해시를 남겼다.
게임 상태를 강제 수정한 실행이 아니며 네이티브 저장/재실행 검증도 아니다.

다음 우선 작업은 candidate marker에 영향을 받는 제자리 정규화/입력 확정/
전용 descriptor 복사/영구저장 검증 경계를 확인하는 것이다.
단순하게 08032AC6 전역에서 확장하거나 descriptor16의9byte한계를 변경하지 않는다.
한글8글자의 표시 출력은33bytes가 필요해 기존 editing descriptor0의32bytes만으로도
부족하다. editor buffer 수명과 새 작업 공간은 별도로 증명해야 한다.
원본 일본어 기록은 기존 경로로 보존하고 후보만 별도 경로로 처리하는 호출 계약을
확립한 뒤 실제 빌드·한글 키 입력·표시·저장·fresh-load 검증으로 넘어간다.

## 후속 구현: GBA 자동 조합 코드와 작업 상태 압축

`tools/hangul_composer_thumb.py`에 자동 자모 입력과 B 삭제의 Thumb-1 구현을 추가했다.
feed304bytes / undo344bytes. 11,172개 완성 음절 +19개 미완성 초성 +빈 상태의
11,192행×40선택자 표를 읽는다. 전이표1,790,720bytes, 기본 삭제표22,382bytes.
이 표는 호스트 규칙에서 파생된 후보이며 사람이 글자판 배치/조작감을 승인한 것은 아니다.
직접 자모 선택, 겹초성/모음/받침, 받침 이동, 입력 이력에 따른 역순 삭제,
불러온 문자열의 표준 분해 삭제, 용량/잘못된 상태 거부를 처리한다.
마지막 셀이 아직 조합 중인지 구별하는 active-tail flag를 유지한다.
이를 생략하면 뒤 글자를 지운 뒤 앞의 확정 음절이 재조합되어 기준 편집 의미와 달라진다.

`tools/bench_hangul_composer_thumb.py`는 emit된 코드와 저장 후 다시 읽은 표를
독립 CPU에서 실행한다. 모든447680 행/키 조합, 현대 한글11172개의 실제 입력·삭제·
불러온 문자 삭제 경로, 마지막 칸/다른 용량/잘못된 상태 표본을 검사했다.
feed485720 / undo105148 =590868 CPU검사 PASS, 그중 거부31309(잘못된 상태표본30 포함).
호출자의 r4..r11/SP, 상태 경계/거부 시 무변경을 검증한다.
CPU 픽스처의 코드와 표 메모리는 쓰기 금지로 설정했다.
보고서 `hangul_keyboard_v1/cpu_composer/report.json`에 기계어/표/도구 해시가 있다.
이 구현의 **영구 작업 상태276bytes는 독립 픽스처 ABI이고 게임 RAM 예약이 아니다.**
자판 선택·폰트/편집 화면·확정/저장용 game hook은 아직 설치하지 않았다.

작업 메모리를 찾기 위해 `poc/runtime/hangul-keyboard-v1-workspace-r2/`에서
현행 동일ROM의 자체 question29 체크포인트→입력→일본어 편집/B→확정→반응93을
일반 패드 입력으로 추적했다(23actions/9캡처, RAM/기록/플래그 변경 없음).
입력 상태 뒤의 FCA0h부터276bytes 후보는 기존 CPU접근17그룹과 겹쳤다.
특히0200FCA0의0804A466 읽기와 FD10/FD30/FD50/FD60/FD70 인접 사용이 관찰됐다.
따라서 “입력 상태 뒤니까 비어 있을 것”이라는 후보는 배제한다.
`hangul_keyboard_v1/workspace.json`은 이 양성 충돌 증거만 주장한다.
전체 RAM 소유권이나 다른 미관찰 영역의 여유 공간을 증명한 것은 아니다.
해당 루트의 No 입력 시도는 step17에서 script10에 머물러 취소 복귀를 확립하지 못했다.
따라서 이 루트에 No 회귀 PASS를 부여하지 않는다. 기존 제품의 별도 검증은 유지한다.
초기 workspace 루트는 보존하고, 계수 가드/명시 JSON 범위를 수정한 r2가 현재 근거다.

이 충돌 때문에 별도276byte 고정 RAM을 가정하는 설계 대신,
`tools/hangul_compact_state.py`에서 **64byte 상태 후보**를 만들었다.
header4 +현재8음절 word16 +최대56개의6bit선택자42 +기준 문자열 삭제횟수1 +reserved0 한byte.
불러온 기준 문자열은 외부에 읽기 전용으로 유지하고, 삭제횟수와 실제 입력 이력으로
기준 조합 상태를 재생한다. 불러온 글자를 전부 지운 뒤 최대 입력을 새로 해도64bytes다.
삭제횟수와 새 입력 이력을 분리하므로 단순 누적 이벤트 로그의112개 이력 문제를 피한다.
원래 레코드의 동일한 baseline을 편집·No·복귀 동안 보존하는 것은 미래 game adapter 계약이다.
현재 기존 레코드를 한글 baseline으로 읽는 decoder/기존 세이브 호환은 구현한 것이 아니다.

`tools/test_hangul_compact_state.py`의4개 호스트 계약 검사 PASS:
현대 한글 전체의 입력/삭제/불러오기 삭제 뒤 매 단계64byte serialize→restore,
최대8음절/56키, loaded baseline56회삭제 뒤56키 재입력, 음절간 받침 이동,
잘못된 header/키/순서/정규화/다른 baseline 거부를 검사했다.
이것은 **64byte wrapper의 실제 기계어 검사나 게임 RAM 채택 증거가 아니다.**

위 호스트 검사 단계 이후64byte native wrapper를 구현했다. 현재 결과는 다음 절을 따른다.
그 뒤 기존 native editing/flat buffer를 함께 바꾸는 후보와 별도 allocator 경로를 비교한다.
FC60/FC80 사이 틈이나 주변 미관찰 RAM을 여유 공간으로 채택하지 않는다.
stack 예산/실제 entry ABI/원래 공급자·모든 writer·No 수명/자모 glyph 공급을 확인해야
원본 기반 누적 ROM에 설치할 수 있다. 기존 제품 ROM/사용자 세이브는 이번에도 불변이다.

## 현재 후속 결과: 64byte 네이티브 재생 wrapper

ID `exe45.hangul-keyboard.native-compact.v1` / CPU 픽스처 PASS, ROM 미채택.
`tools/hangul_compact_thumb.py`는604bytes의 ARMv4T Thumb 코드다.
기존276byte 조합 상태를 임시 stack에서 재생하며 영구 입력 상태는64bytes다.
외부 읽기 전용 baseline20bytes(완성형 rank8개까지)와 신뢰된16byte 함수/표 descriptor를 받는다.
이는 기존 세이브 표현이나 실제 game caller ABI가 아니다.
selector0..39 / B40 / 검증만41을 처리한다. baseline 삭제횟수와56개의6bit키를 재생하고,
전체 header/rank/unused bit 정규화를 확인한 뒤 성공한 결과만64byte에 반영한다.
잘못된 상태·키·용량 초과·비정렬·baseline/state 겹침은 원자적으로 거부한다.
유효한 pointer 범위/stack 공간/descriptor와 표의 신뢰성은 호출자 전제다.

기존2byte 명령 전용 verifier는 변경하지 않았다. 전용 검증기가 최종 배치에서 모든
명령을 재조립하고,4byte 명령은 ARMv4T BL의 두 halfword 패턴만 허용한다.
BLX/Thumb-2는 허용하지 않는다. caller r4..r11/SP를 보존한다.
임시 stack은 wrapper384 +call shim8 +backend52 =최대444bytes다.
이 계산과 stack 하단 canary 검사는 게임의 stack/IRQ 예산 보증이 아니다.

`tools/bench_hangul_compact_thumb.py`: **154592 CPU검사 PASS**, 거부22827,
잘못된 상태 표본167 포함. 전체11172 음절 생성/입력 역순 삭제/불러온 음절 표준 삭제,
1..8글자 용량,56baseline 삭제 뒤56새 입력, 모든56 packed slot의 잘못된 키 및 padding,
다른 baseline/비정렬/겹침/거부 후 무변경을 검사했다.
코드/표/baseline은 CPU 읽기 전용 영역이며 fixture state 경계와 반환 ABI도 검증한다.
모든 잘못된 입력의 전수 검사는 아니며 조작감에 대한 독립 인간 승인도 아니다.
증거 `hangul_keyboard_v1/cpu_compact/report.json`은 wrapper 기계어·도구·기존 backend 보고서
해시를 결속한다. foundation 검증기는 이 증거와 도구/산출물 identity를 확인한다.

현재 ROM SHA256은 위 기준 그대로이며 사용자 세이브 변경 없음.
다음 distinguishing action은 native entry의 SP/호출 관계와 editor state/flat buffer 전체
writer의 수명을 확인하여64byte 소유권 및444byte 임시 stack을 안전하게 연결하는 것이다.
baseline 변환·No 복귀 수명·자모 glyph·선택자 연결·확정/저장 호환은 아직 미완료다.

## 현재 연결 조사: 정상 native 편집/No/확정의 소유권

ID `exe45.hangul-keyboard.adapter-observation.v1`, 권위 기록
`hangul_keyboard_v1/adapter.json`. 현재 ROM 불변, RAM/record/progress 주입 없음.
`tools/capture_keyboard_adapter.py`로 같은 question29 자체 체크포인트에서23actions/9캡처.
입력2글자→B로1글자→확정 질문→No→편집창→Yes→반응93 정상 조작을 관찰했다.
No는 neutral7/right60/A120으로 실행했다. step14 editor mode16→step17 mode12,
편집 words/cursor/end가 B후 상태 그대로 유지되며 화면에서도 편집창 복귀를 확인했다.
이 경로의 script10은 대화창 공통 상태이므로 script ID만으로 복귀 실패를 판정하지 않는다.
이전 workspace-r2의 No미확립 기록은 당시 근거로 보존하며, 새 경로가 현재 양성 근거다.
실제 최종 native 기록은 일본어「あ」 한글자(019be5...)이며 한글 저장 PASS가 아니다.

매프레임080355F6 padding→0803562C flattening을08034E34 caller가 실행한다.
FC60..FC9F 접근 관찰에서 padding/insert와 flattening/validation/commit이 겹친다.
특히03006A4A caller→0800094C byte copy가 FC80..FC9F 전체32bytes를 읽는다.
descriptor0은 pointer0200FC80/length32이며 해당 IWRAM caller는 snapshot slice 해시로 고정했다.
따라서 기존64byte 입력/flat 영역을 compact state로 바꾸는 것만으로는 렌더러에 상태 bytes가
문자열로 흘러간다. descriptor/display 공급 경계와 per-frame pad/flatten을 함께 교체해야 한다.
native init080355B6은 FC40부터96bytes clear를 정적 코드로 확인했다.
하지만 체크포인트가 이미 초기화된 상태여서 이번 루트에서 init 진입은 미관찰이다.

080353B0 entry의 관찰SP는030076C8(8byte정렬), 직접 wrapper 호출 시 계산하단0300750C.
이는 실제444byte 임시 공간을 쓸 수 있다는 증명이 아니다. IRQ/stack최대깊이/인접 데이터
소유권과 hook shim을 확인해야 한다. 기존 입력 words/flat 영역64bytes는 **미채택 후보**다.
정상 경로에서 관찰한 writer/reader와 호출자는 bounded census이며 전체 writer graph가 아니다.

다음 우선순위는 descriptor0의 편집 표시 공급자를 상태→표시 변환으로 바꾸는 경계,
원래 init/import/confirm caller와baseline 수명, wrapper 호출 stack 안전성을 함께 연결하는 것이다.
이후 자모 선택/중간 표시/최종 저장과 fresh-load를 원본 기반 누적 ROM에서 검증한다.
한글패치 스킬의 전체 input→record→display→persistence 기준 때문에 조사 PASS와 ROM지원은
계속 분리한다. 이번에도 제품ROM/사용자 세이브를 수정하지 않았다.

## 현재 후속 구현: 편집 상태→표시 문자열 변환

ID `exe45.hangul-keyboard.editor-display.v1`, 독립 CPU/생성자 후보 PASS, ROM 미설치.
`tools/hangul_editor_display.py`는64byte 상태의 표시 surface를 검증하여 F9FC 문자열을 만든다.
동일 상태의 기준 문자열/packed 입력 이력은 upstream compact wrapper로 먼저 검증하는 계약이다.
이 helper만으로 packed 이력의 정규화가 증명된다고 주장하지 않는다.
완성 음절은 기존 rank0..11171 그대로이며 미완성 초성은 마지막 active cell에서만 허용한다.
편집 모드는 빈 문자열 E5와 미완성 초성 표시를 허용하고, 확정 모드는 빈 입력/초성을 거부한다.
확정용 표시 결과는 저장 레코드가 아니므로 기존 native writer에 넘기지 않는다.

**기존 쉼표가 F9FC index11172**이므로 내부 partial rank11172..11190을 그대로 표시하면
첫 초성이 쉼표로 보인다. glyph identity를 분리하여 후보40자모를11173..11212에 배정했다.
이 후보는 현재 ROM에 공급하지 않았다. 기존 production codec/쉼표 매핑은 변경하지 않았다.
`cpu_editor_display/jamo_normal.bin`은 기존 pinned Galmuri11에서 만든40×96=3840bytes다.
선택판용 기존 Galmuri 고정셀 뱅크2560bytes와는 별도 소비자 표현이며 픽셀 크기도 다르다.
glyph source/license/변환 도구/선택자 순서와 proposed mapping은 보고서에 결속했다.

Thumb 코드242bytes(+끝 정렬2bytes, helper.bin244bytes), 외부 함수 호출 없음.
r0=readable state64/r1=destination/r2=capacity/r3=편집0 또는확정1,
성공 시 E5포함 bytecount/실패0. r4..r11/SP와 원본 상태를 보존하며 실패는 output 무변경이다.
unaligned source는 byte 읽기로 처리한다. source64와 destination의 겹침·pointer overflow·
잘못된 count/capacity/flag/rank/빈 slot과 output 용량을 검사한다. 유효 pointer 범위는 호출자 전제다.
최대8셀 결과는33bytes라서 native descriptor0의32byte를 그대로 사용하면 안 된다.
미완성 초성 뒤공간/커서/밑줄/선택 강조/clear 수명은 다음 game provider 연결 작업이다.

`tools/bench_hangul_editor_display.py`: **201959 display CPU검사 PASS**, 거부55947.
한 셀의 uint16 rank65536 전체와 capacity4/8 모든12slot×11172 완성음절,
모든 길이/마지막 미완성19초성/확정 거부/겹침/용량/구조 경계 표본 포함.
CPU에 설치된 compact native wrapper의 출력 상태를 이어서 display helper로 읽는57경로도 PASS.
이57경로는 host 상태를 대신 써 넣은 연결 검사가 아니라 실제 wrapper 기계어 결과를 소비한다.
그러나 CPU fixture의 caller-owned 메모리이며 emulator 입력창/실제 save 경로가 아니다.
코드/전이표/baseline은 CPU read-only이며 glyph 가독성에 대한 인간 승인은 별도다.
증거 `hangul_keyboard_v1/cpu_editor_display/report.json`, foundation 검증에 포함했다.

다음은 이 표시 공급자를 실제 descriptor0 소비자와 연결할 stack/cache 수명 및
init/import/confirm baseline bridge를 확립하는 것이다. 후보자모 출력은 현재 ROM에서 미공급
glyph index를 참조하므로 공급/연결 전에는 실행 경로에 내보내지 않는다.
한글패치 스킬의 소비자별 glyph 공급 기준에 따라 CPU PASS를 화면 PASS로 승격하지 않았다.
원본/누적 제품ROM 해시와 사용자 세이브는 불변이다.

## 현재 후속 결과: 자모 글꼴을 누적 개발 ROM에 공급

ID `exe45.hangul-keyboard.glyph-supply.v1`, 권위 기록 `hangul_keyboard_v1/glyph_supply.json`.
기존 플레이 기준 r2 ROM을 수정/대체하지 않고 원본에서 별도 font-only 후보를 만들었다.
`poc/output/exe45_ko_development_keyboard_glyphs_v1.gba`,11165876bytes,
SHA256 `bc3af1afc5855f8e1161d6a5e5f6cffcfeb66952beb86edcc875107fb9e0d4bd`.
주 빌드 `tools/build_keyitem_full_rom.py`에 기존8개의 Gutsman/input 누적 옵션과
`--hangul-keyboard-glyphs`를 추가한다. 내부 roll/development builder로 명시적으로 전달한다.
초기 전달 누락으로 첫 실행은 argparse에서 종료되었고 제품을 생성하지 않았다. 전달을 수정해 재실행했다.

일반 글꼴은 기존 쉼표11172 뒤40자모11173..11212를 공급했다(3840bytes+width160bytes).
입력창의 fixed-cell 공급자는 일반 글꼴과 다르므로 big/mono 각각 쉼표+40자모41×64=2624bytes를
별도 공급했다. mono의 색 역할은 기존 pin된 profile 그대로다. 원래 glyph/지정 초성 mapping은 보존한다.
41글자의 bank extent/연속 index/normal·big·mono parity와 최종 ROM slice 해시를 빌드에서 검사한다.
source expected writes, header/source extent 차이 감사, archive pointers, 압축 재해독 등 기존 경로를 유지했다.
원래60 selected/672 untouched archives,2549 literals 그대로이며 추가 번역 문구는 없다.
자동조합 상태/자모 선택/편집 표시/확정/저장 hook은 이 ROM에도 **설치하지 않았다**.

`tools/bench_fixedcell_mono_provider.py --keyboard-glyphs`에서 이 최종 ROM의 provider 코드와
source의 실제 native pixel copier0300689C를 실행했다. **22718 CPU검사 PASS**:
big/mono 전체11172 음절, 기존 tint 경계36, 원래 non-FC tailcall10,
추가41glyph×2provider×4tint=328의 실제 복사 픽셀/출력 경계/ABI 검사.
normal40자모 최종 pixels는 pinned Galmuri11 변환으로 별도 대조했다.
증거 `hangul_keyboard_v1/glyph_provider_cpu.json` / 실제 emulator scanout·timing 증거가 아니다.

`poc/runtime/hangul-keyboard-glyphs-v1-boot/`에서 state 없이 부팅한 뒤 같은 ROM의 자체 체크포인트로
`...-boot-menu/`를 이어 정상 Start 입력으로 타이틀까지 관찰했다. 타이틀 screenshot을 육안 확인했다.
이 관찰은 cold-boot 동작만 증명하며 아직 게임이 새 자모를 lookup/render한 것은 아니다.
원래 자판/사용자 세이브를 조작하지 않았고 기존 ROM state를 새 ROM에 재사용하지 않았다.
`tools/report_keyboard_glyph_supply.py`는 product/tool/font pins, CPU, route chain을 결속한다.

옵션을 끈 주 빌드도 원본에서 별도 `...input_heading_v1_regression_r3.gba`로 재생성했다.
ROM SHA256은 기존 r2의 `5e7bee...31f4`와 완전히 동일했다. generated manifest 도구 해시는 최신이다.
기존 제품의748도구 pins는 과거 기록으로 보존하며 이번 신규 기능의 pins로 오인하지 않는다.
현재 플레이 기준은 r2 그대로이고 font-only 후보는 NON-DISTRIBUTION, glyph-runtime-pending이다.

다음은 이미 CPU 검증한 state→display 공급자를 descriptor0/cache에 연결하고,
초기화/기존 기록 불러오기/확정 baseline 수명 및 stack 안전성을 맞추는 것이다.
일반/고정셀 자모 bank의 실제 lookup→load→residency→화면과 정상 입력·No·저장/fresh-load는 미완료다.
한글패치 스킬의 소비자별 글꼴 공급 기준에 따라 font-only ROM 생성·CPU·부팅과 자판 완성을 분리했다.

## 현재 후속 결과: descriptor0 표시 캐시와 소비 수명 확인

ID `exe45.hangul-keyboard.display-cache-observation.v1`, 권위 기록
`hangul_keyboard_v1/display_cache.json`. 기존 플레이 ROM 그대로, 사용자 세이브 변경 없음.
`tools/capture_keyboard_display_cache.py`는 정상 패드 입력만으로 기존 B/No/Yes 경로를
추적한다. 현재 근거는 `poc/runtime/hangul-keyboard-v1-display-cache-r3/`의23actions/9캡처다.
첫 cache 루트와 r2에는 snapshot 옵션이 없어 RAM 덤프가 누락됐다. 해당 시도는 보존하며
현재 검증 근거로 승격하지 않았다. observer는 이후 `--probe snapshot` 없으면 실행을 거부한다.

**860회 실제 copy→동일 렌더링 호출의 소비를 연결했다.**
IWRAM03006A40에서 source0200FC80/length32/destination020155F0,
context0200FBE0와 cache slot0을 관찰했다. copy 호출03006A4A→0800094C,
복귀03006A4C 후 context+24에 destination을 기록하고 +30의 slot을1로 증가한다.
copy 전후32bytes가 완전히 같고 native parser0300684A가 그 캐시의
4개 일본어/빈칸 glyph와 E5를 순서대로 읽었다. 모든860회에서 frame과 bytes가 일치했다.
렌더러 시작03006838와 종료030068E2에서 slot은0으로 초기화된다.
따라서 이 경로의 캐시는 편집 기록 자체가 아니라 매 렌더링 호출에 다시 생성되는 표시 공급이다.
No 뒤 편집창 복귀/입력 유지와 Yes의 native record019be5 및 반응93도 재확인했고,
step17 실제 screenshot에서 일본어 자판과 편집값「あ」를 확인했다. 한글 입력 화면은 아니다.

캐시 literal020155F0/context0200FBE0/descriptor table080526D0와
slot×128 산술을 resident 코드와 원본 ROM의 동일 slice로 결속했다.
예:03006A1C..6A78은 원본 ROM1EF91C..1EF978과 일치한다.
128byte **stride**가 확인된 것이지 모든 slot의 소유권/전체 allocator 용량을 증명한 것은 아니다.
8한글의33byte 표시를 이 캐시에 직접 만들면 별도 영구33byte 버퍼를 줄일 수 있는 후보지만,
이번 관찰은 기존32byte/5byte 소비만 증명한다. 실제 F9FC33byte 출력과 후속 glyph 소비는 미검증이다.
전역0800094C나 descriptor0의 length만 늘리는 수정은 적용하지 않았다.

`tools/report_keyboard_display_cache.py`는 route/state-origin/artifact/observer 해시,
source→cache→parser byte identity, counter 갱신, resident 코드 출처와 정상 B/No/Yes를 검사한다.
foundation 검증에 이 보고서를 추가했다. 전체 foundation PASS, 현재33개 도구 identity를 결속한다.
기존 CPU 조합/표시 backend의 대규모 전수 검사는 이번에 다시 실행하지 않고 기존 고정 증거를 확인했다.

다음은 **이 실제 destination/수명 계약을 이용하는 coordinated display bridge**다.
init/import/No 동안 immutable baseline 소유권, 기존 per-frame padding/flattening 대체,
입력 handler stack/IRQ 예산과 compact 상태 초기화를 먼저 맞춰야 한다.
표시 bridge만 설치하면 기존 writer가 compact 상태를 덮어쓰므로 단독 설치하지 않는다.
선택자/자동조합/확정 record/save/fresh-load와 실제 자모 화면은 여전히 미완료다.
한글패치 스킬의 runtime-assets 기준에 따라 캐시 연결 관찰을 한글 지원으로 확대하지 않았다.

## 현재 후속 결과: 실제 초기화 관찰과 record→baseline 연결 코드

ID `exe45.hangul-keyboard.lifecycle-observation.v1`, 권위 기록
`hangul_keyboard_v1/lifecycle.json`. 이전 체크포인트는 이미 초기화된 상태였으므로,
이번에는 동일 ROM의 `input-heading-v1-jackin` 자체 체크포인트에서 정상15actions를 먼저
재생하고 B/No/Yes23actions를 연결했다. `poc/runtime/hangul-keyboard-v1-lifecycle/`에
38actions/12캡처, RAM/record/progress 주입 없음. 원본/플레이ROM/사용자 세이브 불변.

080355B6 초기화 진입을 실제로 관찰했다. caller08038DA2의 BL, LR08038DA7,
r0=4(용량), r1=33(**입력 제목 script**, field ID로 해석하지 않는다),
r2=020010A6(기록 목적지), r3=0, entrySP03007690이다.
080355C4에서는 FC40부터96bytes clear 결과가0이고,080355F4에서는
FC40+10/+14/+18=FC60, +1C=020010A6과 용량/제목이 설정된다.
이 초기화 SP는 편집 handler의444byte 임시 stack 안전성 증거가 아니다.

입력 전 원래 기록은 `007e7e7ee50000000000`(marker0, 미등록)이다.
편집/B/No 뒤까지 같은 bytes이며, 관찰창의 첫 write는 Yes확정의08035000 진입과 같은
frame3442에서 발생했다. marker1/9B/E5를 쓰고 반응93으로 진행한다.
step32 screenshot에서 No후 입력창/값「あ」를 직접 확인했다. 한글 화면은 아니다.
원래 기록을 baseline source로 다시 읽는 후보가 이 **빈 기록 정상 경로**에서는 성립한다.
기존 nonempty import0803558C는 이 경로에서 실행되지 않았으므로 수명/호환 PASS를 부여하지 않는다.

ID `exe45.hangul-keyboard.baseline-bridge.v1`, 독립 CPU 후보.
`tools/hangul_baseline_bridge.py`는 **180byte Thumb 코드**로 record→baseline20을 만든다.
빈 native marker0은 payload를 사용하지 않고 빈 기준 상태로 변환한다.
이 정책은 위 관찰에 근거한 후보이며 모든 field에서 채택한 저장 규격은 아니다.
marker1은 일본어 기존 기록 분기값2를 반환하며 output을 변경하지 않는다.
이는 일본어 기록의 완전한 구조 검증/편집 지원이 아니라 오인 방지를 위한 분기다.
후보 한글 record81..88은 기존 `hangul_record_candidate.py` 계약대로 count/occupied rank/
unused FFFF/E5/width를 모두 확인한 뒤 complete syllable rank와 canonical loaded active flag를
baseline20에 기록한다. 해당 marker는 여전히 미채택 save ABI다.

ABI r0=readable record(2*r1+2), r1=capacity1..8, r2=destination, r3=output bytes>=20.
반환1=baseline 생성/2=legacy 분기/0=거부. 반환0/2는 output 무변경, source/r4..r11/SP 보존.
source/output 겹침과 pointer overflow를 거부하며 비정렬 주소는 byte 읽기/쓰기로 처리한다.
stack20bytes, 외부 함수 호출 없음. 실제 baseline20은 미래 caller의 임시 stack에 만들 수 있어
새 영구20byte RAM을 예약하지 않는 설계 후보다. wrapper444bytes와 shim/baseline을 합친
실제 호출 최대깊이/IRQ 예산은 아직 확립하지 않았다.

`tools/bench_hangul_baseline_bridge.py`: **190793 CPU검사 PASS**
(생성134144/거부56641/legacy 무변경8). capacity4/8 모든12slot×11172음절,
한 칸 occupied uint16 전체65536 도메인, count/marker/terminator/padding/overlap/용량 경계 포함.
코드 영역은 CPU 읽기 전용이다. readable/writable pointer extent는 fixture caller 전제다.
baseline byte가 native 출력인 채로 기존 compact wrapper 기계어에 전달되는 **35경로**도 PASS:
빈 기준/가/국어/꽭/8×힣에서 검증/B/재입력/삭제를 실행하며 state/baseline/source/ABI/stack 경계를 확인했다.
이는 emulator 입력과 저장 증거가 아니다. 기존 wrapper/backend 대규모 전수 검사는 재실행하지 않고
보고서·기계어·표·도구 identity를 확인했다. 출력 `cpu_baseline_bridge/report.json`, `helper.bin`.

foundation에 lifecycle과 baseline bridge를 추가했다. 플레이ROM과 원본은 이전 hash 그대로다.
다음은 nonempty import의 caller/기존 기록 처리와 실제 handler stack budget,
compact 초기화·per-frame writer 교체·descriptor0 bridge를 함께 설치하는 것이다.
일본어 기존 저장값을 지우거나 한글로 잘못 해석하는 처리는 적용하지 않는다.
선택판·정상 한글 입력·확정/재표시·저장/fresh-load는 여전히 미완료이며,
한글패치 스킬의 전체 input→record→display→persistence 기준 때문에 이 후보를 ROM 지원으로 승격하지 않았다.

## 현재 후속 결과: 기념일10글자 경로 발견과 확장 조합 구현

ID `exe45.hangul-keyboard.extended-scope.v1`, 권위 기록 `hangul_keyboard_v1/extended_scope.json`.
원본의 선택된 caller 조사에서08031012가 r0=10,08031014가 제목 script39를 설정하고
0803101C에서 초기화080355B6를 호출한다. 원문 제목39는 기념일 내용이다.
이 경로의 목적지/staging record는02026280이다. 기존 capacity4/6/8 metadata 조사와
8글자 독립 helper는 이 별도 caller를 포함하지 않았다. 따라서 **8글자를 게임 전체 상한으로
채택하지 않는다.** 사용자에게 원래 입력 길이를 줄이는 승인을 받은 적도 없다.
8글자 backend/wrapper/display/record/baseline은 기존 범위의 후보로 보존하며 보편 지원으로 승격하지 않는다.

선택된 import caller08030ED4와08031028은 r5+0A의 호출자 상태에 따라0803558C를 실행한다.
둘 다02026280 staging record를 읽는다. 이는 record marker를 보고 불러오기 여부를 결정하는
weak-subject 경로와 다르다. marker0=빈 baseline 정책은 지난 빈 weak-subject 관찰 범위에만
적용한 후보다. staging import 전체에 일괄 적용하면 원래 임시/재편집 문자열을 버릴 수 있다.
이번은 source BL/인자/literal의 정적 양성 증거이며 **실제 nonempty import 런타임은 아직 미검증**이다.
scan 범위 내 BL 후보를 찾은 뒤 선택된 경계를 확인한 조사이며 전체 코드/입력/호출 그래프 완전성은 주장하지 않는다.

startup ARM 코드에서 IRQ/SVC/system 모드와 stack top을 별도로 설정한다.
literal1B0/1B4/1B8은03007BA0/03007FE0/03007700이다.
이것은 초기 top 증거일 뿐 하단 ownership/최대깊이/IRQ중첩 예산 증거가 아니다.
미관찰 IWRAM 영역을 빈 stack으로 채택하지 않았다. 기존 입력 handlerSP030076C8 결과는 유지한다.

ID `exe45.hangul-keyboard.keylog64.candidate.v1`, 호스트 계약 후보.
`tools/hangul_keylog_state.py`는 기존64byte 영구 상태 크기를 유지하며 최대10글자/70키를 담는다.
versionA1/capacity1..10/keycount0..70/baseline삭제0..70의4byte header,
70개6bit키53bytes(마지막4unused bits=0), reserved7bytes=0이다.
**cached rank를 저장하지 않으며**, 외부 immutable baseline에서 임시 조합 상태를 재생한다.
따라서 예전 cached-rank64 ABI와 호환되지 않는다. 두 후보를 동시에 game memory에 설치하지 않는다.
새표현에 맞는 native replay/display/record bridge를 연결하기 전에는 ROM에 내보내지 않는다.

`tools/test_hangul_keylog_state.py`4개 호스트 계약 PASS:
마지막10번째 칸에서 전체11172음절,10개최대복합음절의70baseline 삭제→70키 입력→전체삭제,
1..8용량에서 기존 CompactComposer와 동일한 입력/삭제 의미, packed70slot/unused bit/header/키 거부.
최초 테스트의 depth1/zero key를 잘못된 상태로 분류했지만 key0=ㄱ이라 유효하다.
해당 잘못된 기대값을 제거했으며 구현을 정상 입력 거부로 바꾸지 않았다. 현재4tests가 권위 결과다.
호스트 serialize→restore 후 state/history를 대조한 검사이며 실제 CPU replay나 emulator 결과가 아니다.

ID `exe45.hangul-keyboard.extended-composer.v1`, 독립 CPU 후보.
`tools/hangul_extended_composer_thumb.py`는 기존 조합 전이/삭제 표를 그대로 사용하고
임시 backend layout을 header4+10words20+70undo280=**304bytes**로 확장한다.
별도 영구304byte RAM을 예약한 것은 아니다. 기존8글자 도구·코드·보고서를 수정하지 않았다.
cap10/history70/word10/history offset24/state304를 명시적으로 생성하며 원래 source 문자열
경계가 다르면 실패한다. 새 emit의 최종 배치 assemble/disassemble 검증을 다시 실행했다.
feed304bytes/undo344bytes, callee r4..r11/SP와52byte stack 계약은 기존 방식이다.

`tools/bench_hangul_extended_composer.py`: **120468 CPU검사 PASS**, feed37615/undo82853,
거부24 포함.10번째 칸의 전체11172음절 생성/입력역순삭제/loaded표준삭제,
10글자70키 상한/초과거부와 cap1/4/8/9/10·malformed header/부족한state bytes 경계 표본 포함.
새 코드와 공유 전이/삭제 표는 CPU 읽기 전용이고 state/stack 경계·거부 후 무변경을 검사한다.
새 backend의 모든 row/key/capacity 조합을 전수 재검사했다고 주장하지 않는다.
공유 표의 이전 전수 증거와 tool/artifact pins를 결속하고 새 slot10/상한 영향 범위를 직접 실행했다.
출력 `cpu_extended_composer/report.json`, `feed.bin`, `undo.bin`.

foundation 전체 PASS. 새 key-log 호스트 계약/source scope 및 확장 native backend의 해시를 추가했다.
ROM 생성/교체는 하지 않았으며 원본/플레이ROM/사용자 세이브를 보존했다.
다음 우선순위는 **native keylog64 replay**와 cap10 baseline24/최대41byte display/record bridge다.
기존 candidate의 최대33byte display는8글자 범위이며 새10글자 경로에는41byte가 필요하다.
caller-flag-driven import/legacy 처리, stack/IRQ 예산과 per-frame writer 교체를 함께 확립한 뒤
원본 기반 누적 ROM에 설치한다. 한글패치 스킬의 완전한 입력 경로 기준 때문에
8글자로 조용히 축소하거나 marker0 처리 규칙을 다른 caller로 확대하지 않았다.

## 현재 후속 결과: 10글자 keylog64 네이티브 재생 연결

ID `exe45.hangul-keyboard.native-keylog.v1`, 독립 CPU 후보이며 ROM 미설치.
`tools/hangul_keylog_thumb.py`는 기존8글자 wrapper의 명시적으로 확인한 구조를 재사용하되
변경 대상 문자열이 다르면 생성에 실패한다. 이전 도구/기계어/보고서는 수정하지 않았다.
604byte ARMv4T Thumb-1 코드의 최종 배치 assemble/disassemble round-trip과 내부 branch 경계를 검사했다.
ABI r0=keylog64, r1=immutable baseline24, r2=selector0..39/B40/check41,
r3=trusted descriptor16(feed/undo/transitions/deletions). aligned valid pointer extent와
descriptor는 caller 전제이며 state/baseline overlap·overflow는 거부한다.
baseline24는 count/cap1..10/history0/loaded-active header와10개 rank word다.
상태 versionA1/70개 packed키/삭제수/unused bits/reserved bytes/기준 rank를 검증하고,
304byte 임시 backend에 baseline 삭제 후 accepted keys를 재생한다.
행동이 성공한 뒤에만 proposal64를 상태에 복사하므로 거부 후 상태는 원래 값이다.
완성 rank cache가 없어 기존 cached-rank64 ABI와 다르며 두 후보를 동시에 설치하지 않는다.
check41은 무변경 검증만 수행한다. 재구성한24byte 표시 상태를 caller에 반환하는 bridge는 아직 없다.
다른 유효 baseline과의 교체는 이 keylog만으로 탐지할 수 없으므로 caller가 editing 동안
동일한 원본 baseline 수명을 결속해야 한다. 이것은 원본 저장값을 무시해도 된다는 뜻이 아니다.

`tools/bench_hangul_keylog_thumb.py`: **154574 CPU검사 PASS**, 거부11613/malformed191 포함.
전체11172음절의 fresh 생성·check·accepted-key 역순 삭제와 cap10 loaded 마지막칸의
전체11172음절 check/표준삭제를 실행했다. cap1..10 각각40키 full-field 경계,
10개최대복합음절70baseline삭제→70키재입력→초과거부→전체삭제를 확인했다.
packed70slot 각각잘못된키/unused키, version/cap/count/delete/highbits/reserved/header/rank,
정렬/overlap/invalid action 경계 표본을 거부했다. malformed 전체 도메인 전수 주장은 하지 않는다.
코드/표/baseline은 CPU 읽기 전용, state 양끝/r4..r11/SP/baseline 무변경/stack 하단 guard 검사.
성공한 호출마다 임시304byte backend의 rank·active flag·undo history를 호스트 모델과 대조했다.
이는 검사 전용 dead fixture stack 읽기이며 반환 후 game caller가 쓸 pointer로 내보내지 않는다.
공유 backend120468 및 이전 표 전수 보고서의 tool/artifact/dependency pins도 확인했다.
출력 `hangul_keyboard_v1/cpu_keylog/report.json`, `wrapper.bin`.

임시 stack은 backend304+proposal64+locals24+saved20=412bytes,
call shim8+backend52까지 **최대472bytes**. put-key의12bytes 중첩은 이 상한 이하다.
fixture에서 이 공간이 안전한 것은 실제 game stack/IRQ ownership 증거가 아니다.
기존 handlerSP030076C8에서 계산상 하단030074F0이나 해당 범위를 예약하지 않았다.
게임 실행 시간/최대 call depth/IRQ 중첩과 baseline 생성 caller의 stack을 추가로 검증해야 한다.
source/현재 플레이ROM/사용자 세이브 변경 없음. foundation에 연결 코드·검사·기계어의 identity를 추가했다.
최종 foundation 전체 PASS이며 원본/플레이ROM hash 재확인도 통과했다.
재구성304byte 대조를 추가하는 중 먼저 실행한 verifier는 검사 도구의 stale hash를 거부했다.
검사 재실행으로 새 보고서를 생성한 뒤 최종 verifier를 다시 실행하여 PASS했다.
다음은 baseline24와 caller-sensitive legacy/import, keylog→41byte display의 연결,
실제 stack 예산 및 coordinated editor/per-frame/commit hooks다.
한글패치 스킬의 input→edit→commit→redisplay→save→fresh-load 기준에 따라
이번 CPU 결과를 실제 한글 자판·저장 지원으로 승격하지 않았다.

## 현재 후속 결과: keylog64 → 10글자 표시 코드 연결

ID `exe45.hangul-keyboard.ten-cell-display.v1`, 독립 CPU 연결 후보, ROM 미설치.
`tools/hangul_ten_cell_display.py`: **228byte** Thumb helper.
r0=24byte reconstructed surface, r1=output, r2=output capacity, r3=edit0/commit1.
surface header=count/cap1..10/history0..70/active +10LE rank words이며
upstream full replay가 canonical history를 보증해야 한다. 이 helper만으로 history를 검증하지 않는다.
빈 edit는 E5 한 바이트, 빈 commit/partial commit은 거부한다.
마지막 active partial initial19개는 기존 자모 index11173..11191로 변환한다.
완성음절 rank0..11171/쉼표11172/자모 공급 규칙은 기존 폰트 후보와 동일하다.
occupied/unused word·모드·header·출력 크기/주소 overflow·surface overlap을 검증한 뒤
F9FC+LE index/E5를 출력한다. 최대10글자×4+1=**41bytes**, reject는 output 무변경.
surface/output은 비정렬 byte 접근을 허용하며 r4..r11/SP를 보존한다. stack28bytes.

`tools/hangul_keylog_display_thumb.py`: **496byte** read-only replay bridge.
r0=keylog64, r1=immutable baseline24, r2=output,
r3=trusted aligned descriptor28(feed/undo/transitions/deletions/display ptrs/capacity/mode uint32LE).
canonical keylog를 임시304byte backend에 재생하고, stack가 유효한 동안 native helper를 호출한다.
이전처럼 반환 후 dead stack pointer를 caller에 넘기지 않는다. state와 baseline은 쓰지 않는다.
output 최대41byte 영역은 keylog64/baseline24/descriptor28과 겹치면 거부한다.
신뢰 descriptor/pointer extent와 output이 함수 stack workspace 외부라는 조건은 caller 책임이다.
출력 크기·mode·partial 등은 display helper가 실제 count 기준으로 확인한다.
반환은1..41byte/거부0. 편집 wrapper의 proposal64를 제거하여
backend304+locals24+saved20=348, shim8+backend52까지 **최대408byte stack**으로 줄였다.
편집 wrapper472bytes는 바꾸지 않았으며 두 경로 모두 실제 game stack/IRQ/timing은 미검증이다.
최종 ARMv4T Thumb-1 배치의 assemble/disassemble/branch 검증과
08006000/08B00000/09F00000 위치 재생성을 확인했다. 설치 주소를 채택한 것은 아니다.

`tools/bench_hangul_ten_cell_display.py`: **241025 CPU호출 PASS**.
surface180794/replay-display60231, 거부56844 포함.
surface 한 칸의 uint16 rank 전체65536과 **10개각칸×11172 완성음절=111720**을 실행했다.
cap1..10/count별19partial initial·commit rejection·capacity·source overlap·빈 상태·invalid header를 포함한다.
read-only native bridge가 fresh 전체11172음절 각입력단계/commit과
loaded10번째 칸의 전체11172음절을 실제 재생하여 표시 helper에 전달한다.
70baseline삭제→70키재입력→삭제, commit partial,32/40byte부족,
reserved/packed padding/key/잘못된mode/주소overflow/overlap·정렬 경계도 실행했다.
범위 내 baseline삭제 count1은 유효하게 재생될 수 있으므로 무조건 malformed로 거부하지 않는다.
native 출력과 별도 host restore/display 결과를 대조하며 전체 fixture RAM의 Expected Write,
baseline/descriptor/state 무변경, r4..r11/SP/408byte stack guard를 검사했다.
코드·표·baseline·descriptor는 CPU 읽기 전용이다. invalid 전체 도메인 전수 주장은 하지 않는다.
출력 `hangul_keyboard_v1/cpu_ten_cell_display/{report.json,helper.bin,bridge.bin}`.
기존 backend/keylog/editor-display 보고서와 기계어·표·도구 pins를 결속했다.

기존 descriptor0은32bytes이며 새 최대41byte 출력을 그대로 연결할 수 없다.
128byte cache stride 관찰은 목적지 소유권/slot lifetime 전체 증거가 아니므로 해당 영역을 임의로 예약하지 않는다.
다음 완료-critical 단계는 caller별 baseline24/legacy import/committed record 규격과
실제 stack budget, per-frame writer/flat reader 교체,41byte cache 소비 및 cursor/padding다.
현재 플레이ROM/원본/사용자 세이브 변경 없음. 한글패치 스킬의 전체 입력·확정·재표시·저장·fresh-load
기준에 따라 CPU 표시 연결만으로 ROM 한글 자판 지원을 선언하지 않는다.
최종 foundation 전체 PASS.47개 도구 identity와 새 표시 report/binaries 및 원본/플레이ROM 해시를 재확인했다.

## 현재 후속 결과: 호출자 선택형 10글자 baseline24 연결

ID `exe45.hangul-keyboard.ten-cell-baseline.v1`, 독립 CPU 후보, ROM 미설치/저장규격 미채택.
`tools/hangul_ten_cell_baseline.py`: **196byte** ARMv4T Thumb-1 helper, stack20bytes.
ABI r0=record, r1=cap1..10 | (import-selected <<8), r2=output, r3=output capacity>=24.
r1의bit8 외 상위bits는 거부하며 source/output pointer extent는 caller 책임이다.
byte 접근으로 비정렬 주소를 허용하고24byte output과 source candidate width2*cap+2의
overlap/주소 overflow를 확인한다. 반환1=baseline24,2=legacy 분기,0=거부.
상태2/0은 output 무변경이며 source/r4..r11/SP도 보존한다.

불러오기 여부는 **caller가 명시적으로 전달**한다. flag0이면 새 빈 baseline을 생성하고
record payload를 무시하되 원래 record를 수정하지 않는다. 이것은 caller가 새 입력을 요청한 경우에만 맞다.
flag1일 때 marker0/1은 기존 일본어/임시기록 route2로 반환하며 빈 한글값으로 변환하지 않는다.
이는 source `extended_scope.json`의 r5+0A staging import와 구별 가능한 계약을 위한 후보이며
실제 caller에 hook한 결과가 아니다. marker0/1의 일본어 문법·길이 검증/재편집은 여전히 미구현이다.
무조건 marker0=empty였던 이전8글자 baseline helper는 빈 weak-subject 관찰 범위로 보존한다.
새helper는 그 정책을 호출자 조건 없이 다른 필드에 확대하지 않는다.

후보 한글 record는 cap1..10, count marker81..8A,LE완성음절rank,unusedFFFF,E5를 엄격히 검사한다.
검증 후 count/cap/history0/active(count!=0)+10rank words=24byte immutable baseline을 생성한다.
host pack/unpack/baseline도 같은 인터페이스를 제공하며 cap1..8에서 기존 후보와 byte가 같다.
후보 width2*cap+2나 marker81..8A가 실제 calendar 저장 공간/원래 save consumer에서 안전하다는
증거는 아니므로 아직 primary ROM build/save ABI로 채택하지 않는다.

`tools/bench_hangul_ten_cell_baseline.py`: **207604 CPU호출 PASS**.
converter182980(거부57273/legacy무변경80),native initializer11178,
native edit1137,native display12309. converter의reject 수와 nativeedit의거부를 합산하지 않았다.
occupied rank1칸 uint16전체65536과10개각칸×11172=111720 완성음절을 확인했다.
host pack→unpack/expected baseline,cap1..10/count별boundary/legacy0·1payload/256marker×import양분기,
unknownmode/highbits/terminator/padding/용량부족/overlap/overflow 경계 표본을 포함한다.
flag0은 stale/알수없는marker도 caller 결정대로 빈 편집을 시작하되 record는 무변경이다.
이 동작은 malformed record를 valid Hangul로 인정하는 것이 아니라 import를 하지 않는 것이다.

native helper가 생성한 baseline을 hostbytes로 교체하지 않은 채 keylog/native display로 전달했다.
10번째칸 전체11172음절의 initializer→keylog→display와
빈값/가/국어/꽭/10×힣/10최대복합음절에서 check·70회B·최대70키재입력·삭제를 실행했다.
fixture RAM 전체의 Expected Write를 대조하고 record/baseline/descriptor보존,
callee registers/SP와helper20/edit472/display408byte stack guard를 확인했다.
code/transition/deletion/descriptor는 CPU 읽기 전용이다. invalid 전체 도메인 전수 주장은 하지 않는다.
출력 `hangul_keyboard_v1/cpu_ten_cell_baseline/{report.json,helper.bin}`.
기존 source/플레이ROM/사용자 세이브는 변경하지 않았다.

다음 완료-critical 검증은 **실제 nonempty Japanese/staging import의 문자 표현과 재편집 보존**,
calendar record의 실제 폭·소비자/save 경로, game stack/IRQ와coordinated writer/hooks다.
후보끼리 연결됐다고 실제 일본어 저장 호환이나 ROM 한글자판을 지원한다고 선언하지 않는다.
한글패치 스킬의 기록·재표시·저장/fresh-load 기준 때문에 이러한 미완료 조건을 유지한다.
최종 foundation 전체 PASS. 새 helper/report와 기존 dependent tools/artifacts,
원본/현재 플레이ROM 해시를 재확인했다. 실제 nonempty import 런타임 PASS는 부여하지 않았다.

## 현재 후속 결과: 원본 일본어 import와 중간 편집의 구별 증거

ID `exe45.hangul-keyboard.legacy-edit-source.v1`, 권위 `hangul_keyboard_v1/legacy_edit.json`.
`tools/analyze_keyboard_legacy_edit.py`는 immutable 원본을 읽기 전용 CPU ROM에 올려
0803558C import/08035620 count/0803562C flatten leaf를 호출했다.
080353C0..08035408 삭제와080354C8..080354EC 덮어쓰기는 sound call 직전까지만 실행했다.
후자는 함수 전체 ABI/게임 상호작용을 검증한 것이 아니다. source literal과 각선택block에 hash,
Thumb-1 disassembly→assembly byte 동일 검사를 결속했다. 전체CFG/참조 완전성을 주장하지 않는다.
원본·현재 플레이ROM의 해당명령bytes는 같다. TPL selector literal은6368E8→800000으로
기존제품에서 relocate되어 있어 단순byte 동일 검사를 처음 거부했다.
이후 code/editorliteral 동일과 relocate된각page token 동일을 따로 검증했다.
주소차이를 무시한 것이 아니라 source/product 각table/page guard hash를 보고서에 보존했다.

원본3page token수는85/85/75, distinct218개다. 기존105셀40자모 plan은 후보 좌표표이며
원작105활성셀 또는 모든row가 실제 도달 가능하다는 증거가 아니다. 네이티브grid/navigation은 별도 연결해야 한다.
source token corpus를 각10칸에 배치하고 import→count→flatten을 정확히 대조했다.
**10900 CPU호출 PASS**: import3337/count3337/flatten3337/delete17/overwrite872.
각256marker의 동일문자 import,0..10개의2byte문자,모든218token×10slot,
가변cursor 삭제/덮어쓰기와guard를 포함했다. 게임 nonempty import/runtime 증거는 아니다.

확립된 원본 동작:
- import는 marker를 읽지 않고 record+1부터 E5까지 처리한다.
- single byte b는word00bb, E4 xx는wordxxE4(LE)에 저장된다. 실제selector corpus는 flatten 왕복byte가 같다.
- import는 end pointer를 갱신하지만 **cursor는 초기 start 그대로**다.
- B는cursor앞칸을 삭제하고뒤occupied칸을왼쪽이동한다. cursor0/nonempty에서는첫칸삭제한다.
- A 선택은existing칸을덮어쓰며end에서만append한다. cursor는한칸전진한다.
- 원본import leaf는capacity를검사하지 않는다. fixture에서cap4에5문자를불러와count5가 되는 것을 재현했다.
  이는 upstream caller 검증 유무나 실제게임overflow발생을 증명하지 않는다. 실제 입력buffer전체를 넘기지 않았다.

현재 pure-Hangul keylog는 loaded 마지막칸을 active로 보고 tail edit만 처리하므로
이 cursor/중간편집 계약과 기존opaque 일본어값을 보존하지 못한다. 따라서현설계를 원작editor에
그대로 설치하는 가정을 배제한다. 원작기능축소를사용자가승인한적은없으며자동조합선택만 있다.
혼합native-token/Hangul identity와 cursor-aware replay가 필요한 구현 방향이며
실제 UI에서 커서/active조합 표시·삭제·확정까지 일관되게 연결해야 한다.

`tools/hangul_native_tokens.py`는 **내부표현 후보**를 추가했다:
한글complete0..11171/partialinitial11172..11190은유지하고,
native single00..E3→8000..80E3, E4 xx→8100..81FF로tag한다.
실제nativeword↔tag↔originalbytes 왕복을source218token의10칸CPU출력과 대조했다.
host484개structural token 왕복과uint16 tag전체65536 rejection/acceptance 검사에서한글rankcollision0.
예컨대あ의native009B를한글rank155로해석하지않고tag809B로구별할수있다.
이것은font membership·저장ABI·혼합nativebackend구현이 아니다. 구조상가능한484개중실제glyph소비를
증명한범위는아니며,원본writer의98/E5 byte scan도남아 있어tag를nativecommit에그대로넣지않는다.

fixtureRAM Expected Write·원래record/주변buffer보존과leafcallee registers/SP/짧은blockstack경계를 확인했다.
특히import후cursor를임의로끝으로바꿔검사를통과시키지않았다. 실제game RAM/stack할당은없다.
원본/플레이ROM/사용자save 변경없음. 다음은cursor-aware mixed editor와실제nonempty import,
각field/temporaryrecord 폭 및 stack/IRQ/저장경로다. 한글패치 스킬의기존값/상호작용보존 기준에 따라
tail-only CPU후보의성공을범용한글자판지원으로확대하지않는다.
최종 foundation 전체 PASS.51개 도구와 bounded 원본 실행/내부표현 증거를 결속하고
원본·현재 플레이ROM hash를 다시 확인했다. 실제 nonempty import 런타임은 여전히 미검증이다.

## 현재 후속 결과: 커서 인식 혼합 편집 호스트 모델

ID `exe45.hangul-keyboard.mixed-editor-host.v1`, 권위 `hangul_keyboard_v1/mixed_editor_host.json`.
`tools/hangul_mixed_editor.py`는 **host reference 후보**다. native machine code나저장ABI는아니다.
cap1..10,10개 mixed word/커서/active 조합 위치를 분리하고 불러온cursor0을 유지한다.
native단독선택은caret에서덮어쓰고끝에서append, B는cursor앞칸(커서0에서는첫칸)을제거한다.
기존일본어word는opaque tag로 유지하며 한글rank로 해석하지 않는다.
한글새initial은caret칸을대체한후cursor를한칸전진시키고, 추가jamo는cursor바로앞active칸을조합한다.
carry시다음칸을덮어쓰며다른칸을밀지않는다. full-field에서도기존칸조합은가능하지만끝넘는carry는원자적으로거부한다.

successful좌우이동은active/keyhistory를sealed로전환하되partialinitial포함모든보이는글자를보존한다.
boundary이동/invalidselector/용량초과는cursor/cells/history무변경이다.
B는acceptedjamo역순undo를우선하고history없으면한글canonicalcomponent를삭제한다.
기존native글자는component로분해하지않고원작whole-cell삭제를한다.
첫overwrite의undo가원래대체된일본어칸을복원하는등새한글조합UX는implementation후보이며
실제cursor/active표시와삭제피드백·presentation검토를마친채택UX가아니다.
빈값이나partialinitial이**어느위치에있든**candidate확정을거부한다.
candidate는검증된internalwordtuple을반환할뿐nativecommit/save record를생성하지않는다.

`tools/test_hangul_mixed_editor.py`: **6개host계약 PASS**.
서로다른native10칸의각위치에서모든11172음절=111720경로를생성하고주변칸/커서와
accepted키전체undo후원래일본어칸을포함한exact상태복원을확인했다.
3가지native토큰의cursor0..3 삭제/덮어쓰기oracle는지난원본block관찰의효과를직접기대한다.
carry시기존다음칸대체/주변preservation/undo,partialcursor이동/확정거부/atomiccapacity,
불러온괙canonical삭제/invalidimport도확인했다.
484structuralnative토큰×cap1..10=4840경로에서full-field끝입력거부/삭제/재입력을확인했다.
10최대복합음절70키/초과거부/70undo→empty와빈B거부도PASS.
이수치는CPU호출이나실제게임화면검사수가아니다. 484토큰fontmembership/oldcommit안전성을주장하지않는다.

`tools/report_hangul_mixed_editor.py`가host검사를실행하고legacy source evidence·도구hash를결속한다.
이hostmodel의이력은최대70개의**전체상태snapshot**이다. 물리크기는아직64byte로구현되지않았으며
이전pure-Hangul keylog64를reuse할수있다고선언하지않는다. 새 boundedstate/undo ABI 설계가필요하다.
기존순수한글nativebackend/wrapper/display 후보는해당범위의검증결과로보존하고범용editor로설치하지않는다.
다음완료-critical은bounded 혼합상태·undo 저장표현과nativecursor-aware코드,
혼합display/legacyrecord/실제nonemptyimport/stack·IRQ·저장/fresh-load다.
한글패치 스킬의interaction/기존값보존기준에따라cursor를끝으로강제하거나미완성자음을조용히버리지않았다.
이번작업에서ROM/원본/사용자save 변경없음.
최종 foundation 전체 PASS. 혼합 커서 호스트 모델의 6개 계약 검사와 기존 native CPU/원본 동작
증거를 함께 재검증했다. ROM 통합은 여전히 미완료이며, 이 통과를 실제 게임 한글 자판 검증으로
표현하지 않는다.

## 현재 후속 결과: 고정폭 혼합 상태/undo HOST codec

ID `exe45.hangul-keyboard.mixed-state-host.v1`, 증거 `hangul_keyboard_v1/mixed_state_host.json`.
`tools/hangul_mixed_state.py`는 ROM 저장레코드가 아닌 **편집 상태 직렬화 host 후보**다.
LE588byte: version B1/cap/count/cursor/active/depth/reserved16의8byte,
10개의word20byte, 70개의undo delta각8byte다. active없음FF, 비점유wordFFFF,
비사용history와reserved는0이어야 한다. partialinitial은편집용으로보존되며확정용이아니다.
각delta는이전count/cursor/active/reserved와대체위치의원래최대2word를저장한다.
현재caret또는active로대체위치를복원해일본어overwrite와carry를원복한다.
후속칸전체를복사하지않으므로host전체snapshot70개보다작지만,기존64byte ABI에맞지않는다.

decoder는전체extent/모든구조필드/word영역/비점유padding/비사용history를검증한다.
이력을역순복원할때각단계가40자모중실제accepted전이로현재상태를만들수있는지확인한다.
구조만맞고전이불가능한위조undo도거부한다. pack→독립byte읽기unpack의상태/이력동일성을검사한다.
host `apply`는decoder검증후명령을처리하고성공한전체상태만반환한다.
거부명령은입력byte와완전히동일한값을반환하며malformed입력은예외로실패한다.
호스트decoder와전이모델의결합검사이며native machine code검증으로확대하지않는다.

`tools/test_hangul_mixed_state.py`: 4개host계약 PASS.
전체11172완성음절에서기존E4 native칸대체→직렬화→복원→모든키undo→원래칸정확복원을검사했다.
10각위치carry/마지막칸overflow/undo,커서이동후partial보존/확정거부,
70키최대이력저장/복원/삭제와71번째입력무변경을검사했다.
occupied uint16전체65536의허용/거부와588개의모든짧은extent,
reserved/active/count/cursor/version/unused/history 및불가능한전이결함을거부했다.
`report_hangul_mixed_state.py`가원래혼합편집증거/toolhash에결속하고foundation에연결한다.

**588byte는메모리필요량이지확보된game RAM이아니다.** 기존FC60..FC9F나기각된인접276byte에
배치하지않았고공용512byte버퍼도free RAM으로채택하지않았다. host apply의임시메모리사용은
native stack상한증거가아니다. game수명/IRQ/호출자문맥의소유권검증이필요하다.
다음은delta형native혼합편집/undo code를실행검증하고실제할당가능범위·수명을확정하는것이다.
혼합display/legacyrecord·실제nonemptyimport·save/fresh-load도완료조건으로유지한다.
한글패치스킬에따라비정상상태를조용히보정하거나기존값을손실시키지않고원자적으로거부했다.
원본/현재플레이ROM/사용자save 변경없음. foundation전체 PASS,57개 도구hash와고정폭혼합상태
호스트증거를결속하고원본/현재제품hash도재확인했다. native혼합자판통합은여전히미완료다.

## 현재 후속 결과: 혼합 B/undo Thumb 실행 후보

ID `exe45.hangul-keyboard.mixed-undo-cpu.v1`, 증거 `hangul_keyboard_v1/cpu_mixed_undo/report.json`.
`tools/hangul_mixed_undo_thumb.py`는508byte Thumb1 명령의 **신뢰된입력전용 kernel**이다.
ABI: r0 aligned canonical588byte state,r1 availablebytes,r2 pinned canonical deletion table22382byte.
return r0=1/0,r4..r11/SP preserved,52byte stack. pointer/table extent와stack비중첩은caller전제다.
이력있으면마지막delta의이전count/cursor/active/최대2word를복원하고끝padding/사용한delta를초기화한다.
이력없으면caret앞(커서0에서는첫칸)/active칸의한글canonical조합요소를삭제하거나,
nativeopaque칸은원작처럼한칸삭제하고뒤occupied칸을왼쪽이동한다.
기존E4 token/partial이동후B/full-field/carry 덮어쓴다음칸도보존/복원한다.

current surface/version/reserved/cap/count/cursor/active/word/padding와비사용history0,
top-delta count/cursor/active/word/reserved/bounds를검사하고거부시무변경이다.
**전체history의accepted-forward-transition검증은구현되지않았다.** 기존hostcodec의unpack검증과
동일한decoder로취급하지않으며,호출자가이미canonical상태를보장해야한다.
한initial입력이력의결과partial을완성가로위조하면구조는유효하여이kernel이undo를허용한다.
이반례를CPU에서직접실행/기록했다. native검증연결전에는import/save/untrusted상태에사용하지않는다.

`tools/bench_hangul_mixed_undo.py`:109090 독립CPU호출 PASS(accepted54616/rejected54474).
uint16occupied전체65536허용/거부,11172완성음절의37506역순키undo,
484structuralnative토큰×cursor0..10=5324whole-cell삭제경로,
10각위치carry/undo·70history/emptyB·partial이동후삭제·612malformed extent/header/delta검사를실행했다.
이것은원래glyph membership/실제게임import/save검증을증명하지않는다.
emitted artifact를다시읽어실행하고코드/table RO,전체4096bytefixtureRAM Expected Write,
callee register/SP 및52byte하한canary를검사했다. ISA 조립/역조립/배치근거는report에결속했다.

현재게임RAM을할당하거나ROM에설치하지않았다. CPU의52byte stack증거는game IRQ안전예산이아니다.
다음은native mixed feed/전체canonical history검증과상태수명·소유권확정이다.
혼합display/legacyrecord·실제nonemptyimport·save/fresh-load의연결도완료조건으로유지한다.
한글패치스킬에따라성공한CPU경로와거부하지못하는반례의범위를분리했다.
원본/현재플레이ROM/사용자save 변경없음. foundation 전체 PASS.
59개 도구hash와새 emitted B/undo artifact/반례를결속하고원본/현재제품hash를재확인했다.
ROM 한글자판통합·실제화면검증은여전히미완료다.

## 현재 후속 결과: 커서 인식 혼합 feed/undo CPU 연결

ID `exe45.hangul-keyboard.mixed-feed-cpu.v1`, 증거 `hangul_keyboard_v1/cpu_mixed_feed/report.json`.
`tools/hangul_mixed_feed_thumb.py`는기존B kernel의구조검증prefix를명시적으로reuse하는
**신뢰된canonical입력전용**자모feed404byte후보다. ABI r0 aligned588byte state,r1 key0..39,
r2 pinned transitiontable1790720byte,r3 availablebytes;return1/0,r4..r11/SP보존,52byte stack.
실제주소/데이터/table수명/비중첩과전체history의canonical성은caller전제다.
이미active인칸은그칸의한글row,새조합은EMPTY_ROW11191을선택해기존40자모전이표를소비한다.
새글자는caret칸을덮어쓰고carry는다음칸을덮어쓴다. 삽입이나주변칸shift는없다.
capacity와70history한도및모든table결과범위를검사한뒤에만이전최대2word/metadata의
8byte delta와새word/count/cursor/active/depth를함께반영한다. 실패는전체상태무변경이다.

`bench_hangul_mixed_feed.py`는1266270 독립CPU호출 PASS(feed890115/undo376155/rejected63188).
기존원본/플레이ROM이나게임RAM을수정하지않고
synthetic RAM과RO code/table에서emitted feed→기존emitted B의연결을검사한다.
범위는11192row×40키447680,10각위치의11172완성음절111720경로/모든중간입력과역순undo,
occupieduint16전체65536,cap1..10/caret경계에서실제CPU상태를hostcodec로decode하는연속입력220경로,
610malformed extent/selector/header/address거부다.70history/초과입력거부/partialsealed전이도검사했다.
연속220경로는입력/삭제사이에host상태로CPU RAM을덮어쓰지않고emitted코드결과를다음코드가소비한다.
Code/table RO,4096bytefixture전체ExpectedWrite,callee register/SP/52byte하한canary도검사했다.
전체history decoder가아니라는범위를유지한다. 위조history에신규legal전이를추가해도과거의
불가능전이는검증하지못한다는반례를보존하며,import/save reader로사용하지않는다.
게임cursor/native선택·초기화,메모리소유권/수명,혼합display/record/save/fresh-load는미연결이다.
한글패치스킬에따라standalone CPU통과와실제ROM조작/저장을분리한다.
foundation전체 PASS.61개 도구hash와새 emitted feed/연속입력·삭제증거를결속하고
원본/현재플레이ROM hash도재확인했다.원본/현재제품/사용자save 변경없음.
다음완료-critical은실제state RAM소유권·수명과nativecursor/초기화연결이며,
588byte상태를기존96byte editor에설치가능하다고가정하지않는다. 추가코드의로컬통과가메모리문제를
해결하지않으므로실제배치가불가능하면동일mixed UX를보존하는더작은표현으로재설계해야한다.

## 현재 후속 결과: 외부 baseline 없는76byte 혼합 replay 후보

ID `exe45.hangul-keyboard.mixed-replay-host.v1`, 증거 `hangul_keyboard_v1/mixed_replay_host.json`.
588byte delta는원작의관찰된96byte editor에맞지않으며추가game RAM도확보되지않았다.
따라서현재설치방향은같은혼합UX를보존하는 **self-contained76byte replay HOST 후보**다.
이전588byte codec/native feed/B는해당독립증거로보존하며game state로채택하지않는다.
이전pure-Hangul64byte+externalbaseline도opaque값/중간커서계약을보존하지못하므로reuse하지않는다.

`tools/hangul_mixed_replay_state.py`:
byte0 cap(low4)/baselinecount(high4),byte1 baselinecursor(low4)/active(high4,없음F),byte2 keycount0..70.
byte3..22는10개LEword(비점유FFFF),byte23..75는70개6bitaccepted자모key(420bits)다.
마지막byte상위4bit B는version이며key에포함되지않는다. 미사용keybits는0이어야한다.
첫80byte안은UI16에destination4byte가추가되어100byte가필요하므로채택하지않았고,
version을남은4bit에배치해76byte로줄였다. UI/timer등기존first16byte를줄이지않는다.
완전한mixed baseline을자체보관해외부원래record수명에의존하지않는다.
restore는baseline/count/cursor/active/word/padding/version/unusedbits를검증하고모든key가
실제accepted전이인지재실행한다. 현재cells/active/cursor와전체undo는baseline+key로복원된다.
move/native선택과키이력없는canonical B는현재상태를baseline으로rebase하고keylog를비운다.
move후partialinitial도보존하며확정은어느칸의partial이든거부한다.
key이력이있으면B는마지막키를제거하므로덮어쓴기존native칸도정확히복원한다.
원자적실패/carryoverwrite/10칸/70키/원래cursor0/기존일본어값은축소하지않았다.

`tools/test_hangul_mixed_replay_state.py`:5 HOST계약검사 PASS.
10각위치×11172완성음절111720경로왕복/전키undo→원래native10칸정확복원,
seed4545의cap1..10별500회=5000혼합명령을기존reference의state/history와비교했다.
carry/lastslot/no-write·sealedpartial·70key/overflow/70undo·occupieduint16전체65536,
모든76개짧은extent·header/padding/version/unusedbits·key40..63·불가능전이/overflowreplay를검사했다.
이검사는native CPU/game RAM/runtime증거가아니다.

96byte 배치 **수치상후보**: originalfirst16 UI보존 + destination4(offset16) + state76(offset20).
observed initializer080355F4의first16bytes와old+28 destination020010A6를실제evidence에서읽어
candidate에결속했다. targetspan0200FC40..0200FC9F는관찰된clear96과일치한다.
**실제game소유권/새layout호환성은미채택.** 이전+16/+20/+24word pointers와+28destination은
새값과겹치며원래editor code를그대로실행할수없다. initializer/import/cursor/padding/flatten/
per-frame descriptor/commit/destination readers를함께재설계·검증해야한다.
16byte UI를모두보존하지만모든UI/caller 접근을감사했다는주장도하지않는다.

다음은76byte에서 **current surface만**재구성하는native replay decoder다.
588byte전체history를stack에만드는wrapper는메모리문제를옮기는것이므로설치방향으로채택하지않는다.
자모B는키수를1줄이고replay,move/native/canonicalB는current surface를baseline에반영하는방향이다.
실제tempstack/IRQ/metadata수명과모든기존writer교체,혼합display/record/save/fresh-load는미완료다.
한글패치스킬의기존상호작용보존/증거범위기준에따라수치상fit를freeRAM/ROM통합성공으로확대하지않았다.
원본/현재플레이ROM/사용자save 변경없음. foundation전체 PASS.
64개도구hash와76byte혼합replay/observed96byte배치후보를결속하고원본/현재제품hash도재확인했다.
실제메모리layout채택·native compact decoder·ROM한글자판통합은여전히미완료다.

## 현재 후속 결과: compact76 → mixed current24 Thumb decoder (2026-10-10)

ID `exe45.hangul-keyboard.mixed-replay-cpu.v1`, 증거 `hangul_keyboard_v1/cpu_mixed_replay/report.json`.
중단된검사세션의도구핸들은없으나완료report가남아있었고,report의tool/artifact/CPUtable/
hostdependency 해시를모두재확인했다. report결과를근거없이재실행성공으로표현하지않는다.
`tools/hangul_mixed_replay_thumb.py`: emitted428byte ARMv4T Thumb1 decoder.
ABI r0source76,r1output24,r2 sourceAvailable(low16)|outputAvailable(high16),r3 pinnedtransitiontable.
모든pointer는bytealignment가능하며return1/0,r4..r11/SP preserved,stack68byte다.
임시current surface24+locals24+saved20으로동작하고588bytehistory scratch는만들지않는다.
실제readable/writableextent·pinnedtable1790720byte·stack비중첩은caller전제다.

baseline cap/count/cursor/active/word/padding와lastbyteversionB,70key영역의모든unusedbits를검증한다.
각packed key를baseline부터순서대로재실행하여key40..63/불가능한조합/마지막칸carry넘침을거부한다.
성공시만전체24byte출력을copy하며실패시source/output/주변fixtureRAM은변하지않는다.
baseline의sealedpartial와nativeopaque값을보존하고,carry는다음칸overwrite/원작중간cursor계약을유지한다.
이것은편집상태decoder다. arbitrarybaseline의commit자격/원래glyph membership/저장레코드검증은아니다.

출력24byte: count/cap/cursor/active(없음FF) +10LEword(비점유FFFF).
**기존pure-Hangul24byte의count/cap/depth/activebool과ABI가다르다.** 이전displayhelper에
그대로넘기지않는다. mixed display변환과pointer/cache/commit reader의동시교체가남아있다.

`bench_hangul_mixed_replay_thumb.py`:627595 CPU호출 PASS(accepted563148/rejected64447).
11192row×40key447680,10각칸×11172음절111720완성경로,occupieduint16전체65536을실행했다.
70키이력의각prefix/역순키제거상태,cap1..10/cursor위치별carry/native선택/canonicalB,
sealedpartialbaseline을복원했다.1972malformed extent/overlap/header/version/unusedkey/invalidkey/overflow를거부했다.
각70key위치의invalid40..63검사는그앞에실제accepted최대복합음절prefix를두어앞선잘못된키로
조기거부되는검사로대체하지않았다. source/output 각각4가지bytealignment도실행했다.
CPU code/table RO,일반sourcepage RO,전체8192bytefixture ExpectedWrite,callee/SP 및68byte하한canary를검사했다.
33개대표경로는read-hook으로source76/stack68/table실제extent밖read가없음을확인했다.
이33개읽기감사범위를전체627595경로의read-hook감사로확대하지않는다.
ISA assemble/disassemble/최종배치와artifact재읽기실행증거는report에결속했다.

ROM/game RAM/사용자save 변경없음.68byte는이decoder자체stack경계이며게임IRQ/전체callchain예산은미확정이다.
다음완료-critical은compact 편집명령/혼합display→실제editor의pointer·padding·flatten·dest writer교체,
96byte배치수명과stack/IRQ검증이다. 실제nonemptyimport·save/fresh-load도완료조건으로유지한다.
한글패치스킬의native실행/consumer경계기준에따라standalone통과를실제ROM한글자판동작으로확대하지않았다.
foundation전체 PASS.68개도구hash/제품identity를재확인했다(뒤의추가편집코드이전기준).

## 현재 후속 결과: mixed current24 → display Thumb 연결 (2026-10-10)

ID `exe45.hangul-keyboard.mixed-display-cpu.v1`, 증거 `hangul_keyboard_v1/cpu_mixed_display/report.json`.
`tools/hangul_mixed_display.py`:292byte Thumb1 helper,host reference converter.
ABI r0surface24,r1dest,r2available,r3edit0/candidate1;return outputlength includingE5 or0.
r4..r11/SP preserved,36byte stack,bytealignment지원;caller는source24/dest실제extent와stack비중첩을보장한다.
current24의count/cap/cursor/activeFF를검증하며기존pure-Hangul표시ABI로해석하지않는다.
완성rank0..11171→F9FC+LErank,partialinitial11172..11190→F9FC+LE(rank+1)로변환한다.
partial은편집mode에서어느칸에있든표시하고candidate mode에서모두거부한다.빈candidate도거부한다.
일반폰트의기존comma11172를유지하고공급후보의19initialjamo11173..11191과mapping을대조했다.
nativeopaque8000..80E3/8100..81FF는각각원래single/E4payload byte로왕복하고주변한글을보존한다.
전체surface를먼저검증/출력크기를계산한뒤최대41byte를반영한다.부족용량/overlap/overflow/invalid은무변경이다.

`bench_hangul_mixed_display.py`:259347표시CPU호출 PASS(rejected108076).
occupieduint16전체65536×edit/candidate=131072,10각칸×11172완성음절111720,
19partial×10각칸×2mode380,484structuralnative토큰×10각칸4840을검사했다.
별도로전체11172음절의마지막10번째칸에서 **nativecompactdecoder출력→nativedisplayhelper**를연결했다.
두CPU호출사이에host가decoded24바이트를rewrite하지않았고실제CPU출력을다음helper가소비한다.
mixed output바이트와source/주변8192byteExpectedWrite,code/table/source RO,callee/SP 및36/68byte하한을검사했다.
41byte capacity경계,source/output4가지alignment,64개overlap,mode/header/padding/주소overflow도검사했다.
이것은실제cache/descriptor나자모화면/glyphmembership/저장검증이아니다.
특히E4payload98/E5를표시에그대로보존하지만원래byte-scanning save writer의위험은해결되지않는다.
새codec를그save writer로확정하지않는다.새committedrecord변환/legacy discrimination은별도완료조건이다.

### 재현성 결함 수정

foundation재실행에서hostreport의unittest `Ran ... tests in ...s` 실행시간이매번바뀌어
새nativecompactreport가참조하는hostdependency hash와맞지않는결함을재현했다.
ROM/decoder의기능실패가아니라보고서identity의비결정성이원인이었다.
`report_hangul_mixed_editor.py`, `report_hangul_mixed_state.py`, `report_hangul_mixed_replay.py`에서
성공검사시간만정규화하고tests/status/toolhash/semantic증거는보존했다.
3hostreport를순서대로새로검사/생성하고nativecompact627595 CPU호출을다시실행해dependency를새로결속했다.
기존report의dependency hash를수동으로바꾸거나mismatch검사를제거하지않았다.
mixed display증거도그새nativecompactreport의hash를참조한다.이번foundation재실행으로재현성을검사한다.

ROM/gameRAM/사용자save 변경없음.각helper의36/68byte경계는게임wrapper/IRQ전체예산을대신하지않는다.
다음은76byte compact편집명령과mixed display/cache(41byte)/nativecursor/dest reader의동시연결,
96byte영역수명·기존writer회귀·실제nonemptyimport·save/fresh-load다.
한글패치스킬의consumer/runtime경계에따라CPU연결통과를실제한글자판이나세이브지원으로표현하지않는다.
foundation전체 PASS.68개도구hash/제품identity를재확인했다(뒤의추가편집코드이전기준).

## 현재 후속 결과: compact76 accepted-key append/pop → replay → display (2026-10-10)

ID `exe45.hangul-keyboard.mixed-keyedit-cpu.v1`, 증거 `hangul_keyboard_v1/cpu_mixed_keyedit/report.json`.
`tools/hangul_mixed_keyedit_thumb.py`: emitted600byte ARMv4T Thumb1(BL포함) 후보.
ABI r0in-place76,r1key0..39/history-pop40,r2available,r3pinnedtransitiontable,return1/0.
bytealignment/r4..r11/SP보존;wrapper128+중첩decoder68=최대196byte stack이며588history는없다.
먼저원래76byte전체를decoder로검증한뒤packedkey추가/삭제를임시proposal에적용하고,
새proposal의전체replay가성공한경우만원래76byte를copy한다. invalid원본을B로정상화하지않는다.
packed6bit의이웃키와끝versionB를보존하고마지막칸carry/key70overflow/불가능조합을무변경거부한다.
**이helper의B는accepted-keyhistory pop만지원한다.** keycount0에서return0;
일반글자canonicalB를삭제불가로제품채택한것이아니며별도handler가아직필요하다.

`bench_hangul_mixed_keyedit.py`:26421편집CPU호출 PASS(rejected2079).
전체11172음절의10번째칸마지막key추가와historypop,70packed위치×40키2800,
70위치원상복구와1000연속CPU편집을검사했다. cap1..10carry/빈이력B/4alignment/
짧은capacity/주소overflow/invalidaction/header/version/unusedbits/invalidkey 등도검사했다.
65malformed경로는원래상태를거부한다. 불가능한마지막키를pop해위조입력을받는경로도거부했다.
전체8192byte fixture의ExpectedWrite와code/tableRO,callee/SP/196byte하한canary를검사했다.
모든11172음절에 **native edit출력76→native replay출력24→native display**를추가연결했다.
helper사이에host가76/24byte를rewrite하지않고실제CPU출력을다음helper가소비한다.
뒤의decoder/display추가22344 CPU호출은26421편집호출과별도다.
이는실제게임입력창/cache/자모glyph소비/저장증거가아니다.

원본/현재플레이ROM/gameRAM/사용자save 변경없음.
다음작업: current24에서canonicalB/move/nativewrite 후compactbaseline으로rebase하는handler;
원래96byte editor의initializer/pointer/padding/flatten/per-frame/dest를함께교체하는설계와
196byte중첩stack/IRQ수명검증. commitrecord/legacydiscrimination/nonemptyimport/save/fresh-load도미완료다.
한글패치스킬의기존상호작용보존기준상historypop을전체B지원으로확대하지않으며,
독립CPU pipeline통과를ROM한글자판동작으로확대하지않았다. 추가편집코드포함foundation전체 PASS.
71개도구/56개증거artifact의hash를재확인했고원본/현재제품identity도전체검증에서보존확인했다.

## 현재 후속 결과: compact cursor/native/canonical B rebase + native command dispatcher (2026-10-10)

ID `exe45.hangul-keyboard.mixed-rebase-cpu.v1`, 증거 `hangul_keyboard_v1/cpu_mixed_rebase/report.json`.
`tools/hangul_mixed_rebase_thumb.py`:804byte ARMv4T Thumb1(BL포함) 후보.
ABI r0in-place76,r1left41/right42/canonicalB43 또는nativeopaque word,r2available,r3alignedcontext.
context앞8byte는pinnedtransition/deletion의LEpointer. own128+nesteddecoder68=196byte stack,
bytealignment/r4..r11/SP preserved. 원본과proposalcompact을replay검증하여성공시만76byte를반영한다.
move/nativeoverwrite는current24를새baseline으로rebase하여keys를clear하고sealedpartial을보존한다.
canonicalB는keycount0만처리하며active또는cursor직전(0이면first)을대상으로한다.
Hangul은기존canonicaldeletiontable로한단계되돌린다. native는한cell을삭제하고뒤쪽을shift한다.
원작중간편집계약을보존하는후보이며실제원작UI/record는변경하지않았다.

`tools/hangul_mixed_dispatch_thumb.py`:56byte native명령dispatcher후보.
ABI r0compact76,r1jamo0..39/B40/left41/right42/nativeword,r2available,r3alignedcontext16.
context추가8byte는keyedit/rebase의verifiedThumbentry. B는keycount로accepted-keypop/
canonicalB를선택하며selectedhelper가malformedoriginal을검증한다. capacity와wrap은dispatch전에거부한다.
temporary4bytepush를tailcall전에복구하므로nestedpeak는196byte를유지한다. context/entry/table의
extent/identity/residency/stack비중첩은caller전제다. gameplacement/RAM소유권은아직미채택이다.

`tools/bench_hangul_mixed_rebase.py`:214664명령CPU검사 PASS(rejected71872).
rebase분류213191/keyedit분류1473(earlydispatcherreject를포함한명령시도수이며,
실제nestedhelper호출수는아니다). 전체11191complete/partialword×10slot=111910canonicalB,
uint16actiondomain65536(484structuralnative+3commands),cap1..10/cursor별native31460,
move130,각70keyprefix의move/native/거부canonicalB를확인했다.
native dispatcher5035호출,seed7646으로각cap500회=5000연속mixed명령을실행했다.
helper사이에host가compact76을다시쓰지않고실제CPU출력을다음명령이소비한다.
160malformed,짧은capacity/invalidaction/wrap/4alignment,전체8192byteExpectedWrite,
code/table/contextRO,callee/SP/196byte하한canary를확인했다.
484structuralnative는실제glyph/inputmembership/저장자격을증명하지않는다.

assembler는기존BLcapablekeyedit검증함수에code인자를추가하여재사용했다.
keyeditartifact는600byte를유지하며기존26421검사/11172edit→replay→display를재실행PASS하여toolhash를갱신했다.
새rebase는그새keyeditreport에결속했다. dependencyhash를수동변경하지않았다.

원본/현재playROM/gameRAM/사용자save 변경없음. 다음completion-critical은실제96byteeditor의
initializer/import/pointer/padding/flatten/per-frame/cursor/dest전체writer의동시교체와cache41byte,
196byte/IRQ예산·lifetime확인이다. committedrecord/legacydiscrimination/실제nonemptyimport/save/fresh-load미완료.
한글패치스킬의기존상호작용/consumer경계에따라CPU편집명령연결을ROM자판지원으로확대하지않았다.
추가rebase/dispatcher포함foundation전체 PASS.74개도구/59개artifact hash를재확인했고,
원본/현재playROM identity도전체검증에서보존확인했다. 실제gamehook미설치상태를유지한다.

## 현재 후속 결과: bounded legacy record → compact76 import/init (2026-10-10)

ID `exe45.hangul-keyboard.mixed-legacy-import-cpu.v1`, 증거 `hangul_keyboard_v1/cpu_mixed_legacy_import/report.json`.
`tools/hangul_mixed_legacy_import.py`:196byte ARMv4T Thumb1 helper/host reference.
ABI r0legacyrecord,r1output76,r2inputAvailable(low16)|outputAvailable(high16),r3cap1..10;
return1/0,bytealignment/r4..r11/SP preserved,stack96byte. caller가실제extent와stack비중첩을보장한다.
전체입력을검증한뒤만76byte출력을반영한다. cap넘침/짧은escape/종료없음/unknowncontrol/
짧은출력/overlap/주소wrap은출력과source를변경하지않는다.
최대읽기범위는min(inputAvailable,2*cap+2)로제한하고E4payload를별도소비한뒤E5종료를인식한다.
E4payload98/E5도그대로opaque값으로보존한다. 원래byte-scanningcommit위험해결은아니다.
원본import처럼marker는무시하고cursor0/activeNone/keys0으로초기화한다. terminator후padding은무시한다.
빈legacyrecord(marker+E5)로emptycompact초기화도지원한다.
**caller-selectedlegacy 전제**: 새Hangulrecord판별/legacydiscrimination이아니다.
원래initializer의UI16/destination/전체96byte메타데이터초기화도이helper의범위가아니다.

`tools/bench_hangul_mixed_legacy_import.py`:97506importCPU호출 PASS(rejected13028).
484structuralnative×cap1..10의모든slot=26620,body첫두byte전체65536,marker256,
각cap의empty/max/overflow,짧은input/output,4×4alignment/overlap/wrap를검사했다.
원본immutableROM의0803558C leaf를실행하여484token×10slot=4840사례의word/cursor계약을대조했다.
source_profile hash를확인하고원작import를ROM수정없이CPUfixture에서호출했다.
원작capacity-blindleaf와달리overflow는안전하게거부한다. 원작의실제gameoverflow발생주장은아니다.

484token×cap1..10=4840경로에서실제nativeimport출력76을native명령dispatcher가그대로소비했다.
자모ㄱ이기존nativecell을덮어쓴뒤B가정확한원래compactbytes를복구한다(추가편집CPU9680호출).
helper사이에host가output76을rewrite하지않는다. 전체8192byteExpectedWrite/sourceRO/code/table/contextRO,
callee/SP/import96byte 및연결editor196byte하한canary를검사했다.
fixture에배치한keyedit/rebase/dispatcher는그주소에서다시assemble/disassemble하여branch를검증했다.
이것은실제게임nonemptyimport/한글자판화면/세이브fresh-load증거가아니다.

원본/현재playROM/gameRAM/사용자save 변경없음.
다음completion-critical: 실제editor96byte의UI/dest초기화및모든기존pointer/padding/flatten/
per-frame/cursor/commitwriter의동시교체,41byte표시cache와stack/IRQ수명확인.
새mixedcommittedrecord/legacydiscrimination,실제nonemptyimport/save/fresh-load는계속미완료다.
한글패치스킬의consumer/runtime경계에따라importfixture성공을기존세이브지원완료로확대하지않았다.
추가importhelper포함foundation전체 PASS.76개도구/61개artifact hash를재확인했고,
원본/현재playROM identity도보존확인했다. 실제gamehook미설치상태를유지한다.

### 2026-10-10 후속: 원작 initializer register ABI 연결 후보

`tools/hangul_mixed_editor_init_shim.py`: Thumb60byte 연결 후보.
원작 인수 r0=capacityFlag/r1=heading/r2=destination/r3=callerValue를
stack params16에 보존한 뒤 staging initializer를 호출한다. 실제 game hook은 설치하지 않았다.
허용 cap1..10/129..138에서 출력 editor96은 staging과 같으며 r0=1, r1=flag,
r2=0200FC60, r3=원래 callerValue, NZCV=0을 원작 body와 대조했다.
**r2는 복귀 ABI 호환값일 뿐, 새 배치의 legacy wordbuffer로 사용할 수 없다.**
old pointer reader가 이 값을 사용하거나 old initializer 후 old consumer가 실행되면
새 destination/compact와 충돌하므로 전체 consumer 교체 전에는 ROM에 삽입하지 않는다.

`bench_keyboard_editor_init_contract.py` 갱신/재실행:
원작 10,240조건과 shim 정상 10,240조건의 r0..r3/NZCV/출력/앞뒤 canary PASS.
shim 전체10,479호출, 지원외 용량239개를 r0=0/편집 버퍼 무변경으로 거부했다.
own stack24 + 실제 nested staging116 =140byte 하한 canary, callee/SP 보존,
CPU write hook으로 editor96/stack140 이외 쓰기 금지를 검사했다.
코드/helper ROM mapping은 read-only다. 원작 clear service는 이전처럼 모사했고
전체 BIOS/원작 clear 실행이나 실제 game stack/IRQ 예산을 증명하지 않는다.
원작 caller에는 이 새 실패값의 처리 코드가 연결되어 있지 않다.

원본8MiB의 2byte 정렬 Thumb BL encoding scan에서 target080355B6 후보5개:
08030EC8/0803101C/08038DA2/08039E3E/0803A1DE.
각 명시적 코드창을 원본/현재ROM 동일 hash 및 ARMv4T assemble/disassemble로 결속했다.
마지막 창의 trailing4byte BL은 경계에서 자르지 않았다.
이는 bounded instruction 증거다. data false positive 가능성이 있는 encoding scan이며,
간접 호출의 완전성/전체 caller 실행/동적 capacity 영역/전체 writer 감사가 아니다.
고정 cap10/calendar와 cap6 caller 외 metadata/dynamic cap caller는 여전히 범위 증명이 필요하다.

한글패치 스킬의 원작 ABI·동시 consumer 교체 기준에 따라 후보와 실제 적용을 분리했다.
원본/현재 playROM/사용자 save 변경 없음. 자모 게임 화면/저장·재시작 검증 미완료.
다음 연결 대상은 pointer_count/표시 cache41byte/answer_compare/확정 record 및 legacy 판별이다.
foundation 전체 재검증 PASS, 79개 tool/64개 artifact hash 결속 재확인 PASS.
원본/current ROM hash 보존 확인. 세 새/갱신 Python 도구 py_compile PASS.

### 2026-10-10 후속: 새 편집 데이터의 현재 caret/count 계산

`tools/hangul_mixed_count_thumb.py`: Thumb486byte. compact76을 검증된 decoder로 복원한 후,
selector20이면 현재 cursor, selector24이면 현재 logical count를 반환한다.
compact header의 count/cursor는 baseline이므로 입력 후 값으로 직접 읽지 않는다.
새 ABI r0=compact/r1=selector20 또는24/r2=available0..65535/r3=전이표,
성공 r0=value/r1=1, 실패 r0=0/r1=0. 빈 문자열/첫 커서의 0과 오류를 구분한다.
byte alignment 허용, source read-only, callee/SP 보존. own32+nested decoder68=100byte.
source/table extent·identity 및 stack과 disjoint lifetime은 caller 책임이다.
**새 value/status ABI이며 원작 pointer_count register live-out ABI로 설치할 수 없다.**
기존 r1=startpointer/r3=editor 등과 pixel cursor 사용자는 별도로 교체해야 한다.

`bench_hangul_mixed_count.py`: 25,180query CPU호출, 실패262 PASS.
원작08035620 leaf를 실제CPU로 실행해 cap1..10/count0..cap/cursor0..count의
285상태×20/24 query=570조건에서 기존 count/caret와 대조했다. 원작 valid pointer 조건만의 증거다.
한글11172종은 HOST가 마지막 키 이전 compact를 준비한 후 실제 native keyedit로 마지막 키를 처리,
그 CPU결과를 host가 덮어쓰지 않은 상태에서 현재 caret/count query2회(22344회)를 연결했다.
query 중 전체8192byte가 불변이며 write hook으로 stack100 외 쓰기를 금지했다.
22591개 성공 query에서는 baseline header값과 현재 계산값이 달라 header shortcut 오류를 구별했다.
모든 query에 callee/SP/100byte 하한 canary, native edit에196byte canary/ExpectedWrites 검사.
별도 seed1045의1000회 mixed edit 후 query2000회는 HOST 편집 모델 기반으로 native 편집 경로와 구분한다.
76byte별 xor mutation152query/잘못된selector/짧은extent/고비트extent/wrap/4alignment도 포함했다.
mutation은 모두 invalid라는 주장이 아니며 host validator의 허용·거부와 비교했다.

전원본 ROM의 정렬된 BL encoding scan에서08035620 direct 후보4개:
08035350(cursor draw),08035486/08035496(input handler),080355FA(padding).
각16byte 명시적 코드창을 원본/current ROM hash/ARMv4T instruction roundtrip으로 결속했다.
raw scan은 data/간접호출/전체reference의 완전성이나 caller 전체 실행을 증명하지 않는다.
cursor draw는 count 결과에8을 곱한다. 이것은 확인된 원작 동작이며 한글12pixel와의
폭·위치 동등성은 미완료다. logical count PASS를 화면·glyph·cache PASS로 확대하지 않는다.

한글패치 스킬의 consumer-boundary 기준에 따라 현재 count 후보와 원작 pointer/pixel ABI를 분리했다.
ROM/game RAM/사용자 save 변경 없음. 실제 입력 화면/확정·저장·재시작 검증 미완료.
다음은 원작4 caller의 동시교체와 표시/cache41byte 연결, pixel cursor advance, commit/legacy 판별이다.
추가 query 포함 foundation 전체 PASS. 81개 tool/67개 artifact hash 결속 재확인 PASS.
원본/current playROM identity 보존 확인. 새/갱신3 Python 도구 py_compile PASS.

## 이전 결과 보존: editor96 초기화계약과 bounded 교체경계 (2026-10-10)

ID `exe45.hangul-keyboard.editor-init-contract.v1`, 증거 `hangul_keyboard_v1/cpu_editor_init/report.json`.
`tools/hangul_mixed_editor_init.py`:180byte ARMv4T Thumb1 staginghelper/host model.
ABI r0params16,r1output96,r2inputAvailable(low16)|outputAvailable(high16),r3zero;
params는4LEuint32(capacityFlag,heading,destination,callerValue)다. return1/0,
bytealignment/r4..r11/SP preserved,stack116byte. caller가extent/stack비중첩을보장한다.
cap1..10과80|cap를지원하며원본initializer의UI16을재현한다: byte4cap,byte5headinglow8,
byte9capacityhighflag,byte10callerlow8,byte14=1,나머지UI0.
destination은opaque4bytes로+16에복사하고compactempty76은+20..95에만든다.
destination을dereference하지않는다. 원래+16/+20/+24pointer와+28dest는이새layout과호환되지않는다.
잘못된capacity/mode/짧은extent/overlap/wrap은source/output을변경하지않고거부한다.
**stagingABI이며원본r0/r1/r2/r3registercall ABI의hook은아니다. 실제96byteRAM배치미채택.**

`bench_keyboard_editor_init_contract.py`:새staging10491CPU호출 PASS(rejected235).
20cap/flag조건마다heading전체256/callerlowbyte전체256=10240조건을원본080355B6 body와대조했다.
heading/caller의highbyte패턴도넣어low8동작을확인했다. 원래96byte clear서비스0800090C는
**모사하였다**: 실제CPU가그서비스에넘긴editor주소/96byte길이를검사하고fixture에서zeroing후복귀한다.
따라서전체clear/BIOS코드실행이나원본최대stack을증명하지않는다. 원본bodystack24하한만검사했다.
그조건에서원래전체96byte결과(UI16+3pointer+dest+zero64)와앞뒤canary를검사하고,
새CPU출력UI16/opaque목적지/compact76/전체8192byteExpectedWrite를host와비교했다.
input짧은extent16가지/output96가지/invalidcapacity/flags/4×4alignment/overlap/wrap도검사했다.
새helper116byte stack하한canary와callee/SP를확인했다. 게임wrapper/IRQ예산은별도다.

원본과현재ROM에서동일한13개명시적consumer코드영역을hash/ARMv4T assemble-disassemble로결속했다.
per_frame_input/commit/answer_compare/cursor_draw/input_handler/legacy_import/caller_option/
initializer/padding/pointer_count/flatten/page_draw/page_transfer다. inline table/pool은코드와구분했다.
이것은그영역의instructioninventory이며전체ROM의reference/controlflow/writer완전성주장이아니다.
현재교체시함께확인할조건:

- initializer의capacityflag/heading/callerValue를유지하고destinationreader를함께옮긴다.
- pointer_count는원래+16start에서+20cursor/+24end까지의word차이를계산한다.
- padding은빈칸0098word와E5종료를원래wordbuffer에쓴다. 새compact에그대로실행할수없다.
- flatten은원래wordbuffer→+40flat를생성한다. descriptor0는그flat32byte를소비한다.
- answer_compare는rawflatbyte의zero/98/E5를특별처리한다. mixedF9FC를그대로넘기는것은동등하지않다.
- commit은원래+28dest로byte-scanningcopy한뒤32AC6정규화를호출한다. 새표시bytes의저장경로로쓰지않는다.

원본/현재playROM/gameRAM/사용자save 변경없음.
다음completion-critical은새initializer를원본ABI/각caller에연결하는shim과전영역writer감사,
41byte표시cache/확정검증/새record·legacydiscrimination의동시교체및196byte+wrapper/IRQ수명이다.
실제nonemptyimport/자모입력화면/대사재표시/save/fresh-load는미완료다.
한글패치스킬의hook/consumer증거기준에따라모사clear검사를원작전체실행이나ROM통합으로확대하지않았다.
추가초기화계약포함foundation전체 PASS.78개도구/63개artifact hash를재확인했고,
원본/현재playROM identity도보존확인했다. 실제gamehook미설치상태를유지한다.

## 현재 후속 결과: 표시 CPU출력과 원작 fixed-cell parser 연결 (2026-10-10)

ID `exe45.hangul-keyboard.editfield-parser.v1`, 증거 `hangul_keyboard_v1/cpu_editfield_parser/report.json`.
`tools/bench_keyboard_editfield_parser.py` 실행 PASS. 기존 glyph-only ROM
`poc/output/exe45_ko_development_keyboard_glyphs_v1.gba` SHA bc3af1afc5855f8e1161d6a5e5f6cffcfeb66952beb86edcc875107fb9e0d4bd
를 read-only CPU fixture로 사용했다. 새 ROM 빌드나 playROM promotion은 하지 않았다.
기존 mixed display helper를 새 fixture 주소08F00000에 재배치/ISA 검증한 뒤,
그 실제CPU 출력 stream을 host가 덮어쓰지 않은 상태에서 원작03006824 parser에 넘겼다.
실제 resident dispatch table030067AC의 F9 slot030067FC를 거쳐 기존 ROM의
F9FC handler, big/mono font 선택, 원작0300689C copier, E5 padding을 실행했다.
IWRAM fixture는 후보 ROM offset1EE700의 overlay에서 읽었다. 원본 대비 차이3곳은
기존 build manifest의 expected source/final writes로 전부 설명하고 hash 결속했다.
단일 F9 write만 있었다는 가정은 배제했다. parser/copy/E5 code3영역은 bounded ARMv4T roundtrip PASS.

24584 parser호출: 완성11172종×2provider22344, 미완성 자음19×2provider×4tint152,
native structural484×2provider968, cap1..10의 각 자리 complete/partial×4tint880,
전체cap complete/partial×4tint160 및 빈 문자열 전체cap/tint80이다.
최대10한글의41byte stream을 실제 소비했다. return logical count, copier cap회,
64byte×cap 최종 pixels·빈칸·tint, 앞뒤 canary, 입력stream 불변,
object metadata, stage/object/stack외 write 금지를 확인했다.
최대 parser fixture stack40byte canary PASS. 이전 provider CPU의 독립 raster 검증 report도 결속했다.

**전송08000850은 실제 실행하지 않았다.** 호출의 stage/fixture VRAM destination06010000/length를
검사하고 Thumb same-mode return을 모사했다. mov-lr-pc caller의 LR은 even이며
BX LR처럼 ARM으로 전환하는 방식이 아니라 Thumb 복귀로 모사했다.
따라서 VRAM 업로드/화면 scanout/타이밍/원작 전체 stack 또는 실제 입력 경로 검증이 아니다.
render context/width/height/font는 직접 준비했으므로 게임이 keyboard에서 해당 font를 선택했다는 증거도 아니다.

판단 갱신: fixed-cell glyph profile은8pixel advance/64byte cell이다.
이전 기록의 ‘원래 cursor8 대 한글12’는 normal dialogue의12pixel provider를 섞은 미검증 가정이었다.
이 fixed-cell 경로에서는12pixel로 cursor를 고치는 방향을 채택하지 않는다.
logical count에8을 곱하는 기존 cursor식은 후보이나 실제 keyboard font/cursor 경로까지 확인해야 한다.
한글패치 스킬의 provider별 연결 증거 기준이 이 방향 수정에 영향을 주었다.

원본/current playROM/glyph-onlyROM/사용자 save 변경 없음. 실제 한글 자판 ROM 통합 미완료.
다음 completion-critical은 기존 descriptor0의32byte source/copy를 새 compact→41byte cache bridge로
연결할 때의 용량·writer·수명, 실제 font/cursor 선택, 확정·record 판별·save/fresh-load다.
추가 static 관찰: 모사한08000850의48byte 코드(850..880) source SHA
73f3bac9af8baa32c8e98d62f3b83d34bc3ddbce67c5fe3c98988223c0d1d6cd의
bounded instruction roundtrip을 확인했다. r0/r1/r2 인수를20byte 항목의+0/+4/+8에
저장하고 mov pc,lr로 복귀한다. 따라서 즉시전송으로 간주하지 않으며,
이 요청 항목의 실제 소비 시점까지 stage pixels 수명도 추적해야 한다.
이는 static 관찰이고 해당 함수/소비자의 실제 실행·완전성 증거는 아니다.
새 parser 증거 포함 foundation 전체 PASS. 82개 tool/69개 artifact hash 재확인 PASS.
원본/current playROM identity 보존 확인. 두 새/갱신 Python 도구 py_compile PASS.

## 현재 후속 결과: 실제 전송 수명과 compact 표시 cache 연결 후보 (2026-10-10)

tools/capture_keyboard_transfer_lifetime.py는 동일 playROM 및 검증된 동일ROM checkpoint에서
정상 controller 입력만으로 실행했다. 관찰 callback은 RAM/PC/save를 주입하지 않았다.
poc/runtime/hangul-keyboard-v1-transfer-lifetime의9캡처/23입력 구간/1232프레임 완료.
tools/report_keyboard_transfer_lifetime.py 및 hangul_keyboard_v1/transfer_lifetime.json PASS.
860개 전송의 원작 font 픽셀과 stage·큐 소비 시점·실제 VRAM 복사 후 pixels가 모두 일치했다.

실제 입력창 font는08619EF8 mono8, stage0201E800, 목적지0600B000,
전송 크기1280byte=20×64byte이다. 선택된 질문의4글자 제한과 별개로20셀 렌더 영역이다.
0300684A parser read →08000850 queue 등록 →다음 프레임0800082E의 실제 copy →
08000832 복사 완료를 추적했다. queue02012730은20byte 항목,
counter02010724, nominal limit96, type2다. 관찰된 tint는0뿐이다.
원본 코드7D4..846/848..880의 bounded ARMv4T roundtrip 및 원본/current 동일성 확인.
이로써 입력창 실제 mono8 선택과 deferred 전송은 확인했다.
중간 write-and-restore 부재, 전체 writer 소유권, queue 포화/다른 타입/다른 경로는 증명하지 않았다.
일본어 정상 입력창 관찰이며 한글 화면·fresh-load 또는 새 cache41byte 지원의 증거가 아니다.

tools/hangul_mixed_cache_bridge.py는 compact76을 복원한 뒤 현재24byte surface를
stack에 만들고 편집 표시 stream을 별도 caller-owned cache에 생성한다.
804byte ARMv4T Thumb-1/BL 코드, caller ABI r0=compact/r1=cache,
r2=input available low16|cache available high16/r3=transition table이다.
성공 반환은E5 포함 stream 길이, 실패는0이며 cache 쓰기 없음.
입력 최소76/출력 최소41byte, wrap 및 두 버퍼 겹침 거부, r4..r11/SP 보존.
두 helper는 순차 호출하므로 own44+replay68=중첩112byte다.
table/source/cache/stack 소유권·분리는 caller 전제이며 게임 stack/IRQ 예산 확정이 아니다.

tools/bench_hangul_mixed_cache_bridge.py 852호출/거부311 PASS.
cap1..10/모든 길이의 완성·sealed partial·native token,
70개 연속 accepted key history, compact76 모든 byte 변이,
짧은 입력/출력, 겹침116조건, byte alignment16조건, pointer wrap을 검사했다.
최대41byte, 성공 stream외 cache 변경 없음/실패 atomic/stack canary/예상외 write 거부 PASS.
sealed partial fixture는 저장 import가 아니라 편집 중 이동 후 상태로 구성했다.
committed import의 미완성 자음 거부 규칙은 완화하지 않았다.
증거 hangul_keyboard_v1/cpu_cache_bridge/report.json 및 helper.bin.

create-kr-patch의 실제 실행·수명 증거 분리 기준에 따라 native JP runtime 관찰과
새 한글 CPU 후보를 구분했다. 기존32byte descriptor/copy를 실제로 교체하거나
새 cache와 deferred pixel buffer의 소유권을 채택한 것은 아니다.
원본/current playROM/glyph-onlyROM/사용자 save 변경 없음.
다음 completion-critical은 descriptor0 연결 ABI/41byte cache writer·수명,
전체 구 editor consumer 교체, 실제 커서/확정/record 판별/저장·재불러오기다.
새 runtime/cache 증거 포함 foundation 전체 PASS. 86개 tool/75개 artifact hash 재확인 PASS.
원본/current playROM/glyph-onlyROM identity 보존 확인. 새4개 및 갱신 verifier py_compile PASS.

## 현재 후속 결과: 조합 편집부터20셀 픽셀/전송 큐까지 CPU 연결 (2026-10-10)

tools/bench_keyboard_cache_pipeline.py 및 hangul_keyboard_v1/cpu_cache_pipeline/report.json PASS.
기존 glyph-only ROM bc3af1afc5855f8e1161d6a5e5f6cffcfeb66952beb86edcc875107fb9e0d4bd를
read-only CPU fixture로 사용했다. 이전 parser report의 manifest/overlay, cache/keyedit/composer
도구와 binary, 원작 실제 transfer-lifetime 관찰 및 source/current playROM identity를 결속했다.
cache helper804byte는 이전 helper.bin과 동일함을 확인했다.
keyedit600byte는 fixture08F02000에 재배치하고 ARMv4T final-placement roundtrip 검증했다.

CPU keyedit →compact76 →cache helper →E5 포함41byte 이하 stream →
원작03006824 parser/resident F9FC dispatch/mono glyph provider/0300689C copier →
20셀1280byte stage →원작08000850 enqueue →080007DC drain →
0800097C wrapper →CpuFastSet service 모델의 연결을 실행했다.
기존 parser fixture처럼 전송 함수 return을 가로채지 않았다.
080EC140의 BIOS SVC0C만 explicit service 모델로 처리했고 BX LR 복귀는 원작 코드를 실행했다.
따라서 새 결과의 VRAM 메모리는 CPU/model 결과이며 에뮬레이터 화면·실제 BIOS 실행 증거가 아니다.
원작 queue/BIOS wrapper4영역의 source identity/bounded Thumb roundtrip을 검증했다.

639회 렌더링: cap1..10×모든 길이×7종 word455,
각 capacity×4tint의 full-field40,143회 native edit 시도 후 렌더링,
queue saturation1회. 143 edit는70 accepted-key append +70 history pop +
지원외41/65535 및 history없는B의3거부다. 최대41byte를 실제 parser가 소비했다.
초기 fixture 준비 이후 accepted-key edit/cache/parser/stage 사이에서 host는
compact/cache/stage를 expected 값으로 덮어쓰지 않았다. host oracle은 비교에만 사용했다.

매회 완성/미완성/native 픽셀과20셀 나머지 빈칸/tint를 정확한 ROM bank와 대조했다.
cache/source 불변성, stage/VRAM 앞뒤 canary, callee saved/SP/stack canary,
예상외 RAM 쓰기 거부, enqueue entry(stage,target,1280,FFFFFFFF,2),
소비 전 VRAM 미변경 및 drain 후 counter0을 확인했다.
포화 counter96에서는 등록과 복사를 생략하고 기존 queue1920byte를 보존했다.
parser+enqueue 최대 fixture stack56byte, drain+BIOS wrapper48byte;
edit196/cache112는 앞선 helper 계약이다. 실제 upstream/IRQ 예산 증명이 아니다.

스킬 create-kr-patch의 연결 경계 기준에 따라 분리된 helper 결과를 실제 전송 큐 코드까지
연결했으나 CPU/model·runtime·product build 증거는 구분했다.
실제 게임의 descriptor0 copy32 교체, cache41byte 전체 writer/수명과 hook live-state 계약,
자판 선택/커서/확정·record 판별·저장/새 프로세스 재불러오기는 아직 미완료다.
이번 작업에 새 ROM 빌드/설치나 사용자 save 변경은 없다.
새 pipeline 결속 후 foundation 전체 PASS, 87개 tool/78개 artifact hash 재검증 PASS.
새 bench/갱신 verifier py_compile PASS. 원본/current playROM/glyph-onlyROM 해시 유지 확인.

## 현재 후속 결과: 원작 표시 provider ABI와 선택적 복사 연결 (2026-10-10)

tools/hangul_keyboard_copy_shim.py 및 tools/bench_keyboard_copy_shim.py 추가.
hangul_keyboard_v1/cpu_copy_shim/report.json PASS, ARMv4T Thumb-1/BL924byte.
원작 resident provider03006A1C 본문을 그대로 실행했고, fixture의03006A6C 복사 포인터만
0800094D에서08F03001로 바꿨다. source offset1EF96C expected4d090008,
fixture final0130f008. 이 write는 Unicorn fixture에만 존재하며 새 ROM/build write가 아니다.
원작 provider와 memcpy 코드 source/current 동일성 및 bounded instruction roundtrip을 확인했다.

선택 조건은 r0=0200FC80/r1=020155F0/r2=32/LR=03006A4C다.
조건 밖 호출은 원작0800094C에 tail-enter한다. 입력창 slot0에만 새 연결을 허용한
CPU 후보이며 이것은 legacy/new record 또는 editor format의 자동 판별이 아니다.
caller가 이미 새96byte editor layout을 선택/초기화했다는 전제가 필요하다.
선택된 호출은 old source-44=0200FC54 compact76을 table09000000으로 복원한다.
출력은 caller-owned 최소41byte cache. 잘못된 compact은 별도 정책으로 E5 한 byte를
기록해 stale text를 남기지 않는다. 앞선 cache helper의 실패 atomic 계약 자체는 변경하지 않았다.
이 fallback은 메모리 안전 후보이지 플레이어 오류 표시/확정 정책을 채택한 것이 아니다.

원작32개 descriptor의 slot0/1/3 조합에서 새 route1개를 제외한95개를 원본 provider와 대조했다.
descriptor28..30의512byte 공통 버퍼도 원래 byte copy로 유지했다.
이 때문에 공통 copier 전체를 한글 변환기로 대체하는 방식은 사용하지 않았다.
cap1..10/모든 길이×완성·partial·native7종455조건,
compact76 각 byte XOR FF76조건으로 새 route531호출/빈 fallback76회 PASS.
최대41byte, cache 이외 source/context/stack 쓰기 경계 및 canary를 확인했다.
provider의 r1..r12 보존/최종r0cache/NZCV0,
context+24cache/+28script+3/+2Cincrement/+30slotincrement가 원작 계약과 일치했다.

provider 마지막 ADDS가 leaf flag 오류를 가릴 수 있어 direct copy ABI7조건도 따로 실행했다.
원래 r0/r1/LR/r4..r12, 최종r2=0/r3=원래source[0]/NZCV60000000 일치 PASS.
일치·불일치 gate와512byte 복사를 포함했다. direct leaf stop은 instruction callback으로
반환 지점 도착만 감지한다. PC/return 값을 주입하지 않았다.
이전에 provider를 실행한 Unicorn translated block은 다른 종료 지점의 direct fixture에서
재사용하지 않도록 영향 코드의 translation cache를 비웠다. 잘못된 중간 종료를 숨긴 것이 아니다.

own20+cache112=중첩132byte, 원작 provider의 saved32+source/destination8+context4를
포함한 최대 fixture176byte canary PASS. 실제 game upstream/IRQ stack 예산 증명은 아니다.
code/overlay는 CPU 실행 중 read-only로 보호했다.
create-kr-patch의 hook live-state/다른 consumer 보존 기준이 이 선택적 연결 설계에 영향을 주었다.
현재 실제 cache41byte 전체 writer/수명과 모든 descriptor0 slot/caller, 구 editor consumer
동시 교체·실제 선택/커서/확정·record/save/fresh-load는 여전히 미완료다.
이 shim을 옛 editor가 살아 있는 ROM에 설치하면 안 된다. ROM/사용자 save 변경 없음.
새 shim 포함 foundation 전체 PASS, 89개 tool/80개 artifact 해시 재확인 PASS.
새2개 도구/갱신 verifier py_compile PASS. 원본/current playROM/glyph-onlyROM identity 보존 확인.

## 현재 후속 결과: 실제 cache/stage writer 및 보호 구간 관찰 (2026-10-10)

tools/capture_keyboard_buffer_writers.py는 기존 동일 playROM/checkpoint/input route로
1232프레임/23입력/9캡처를 완료했다. ROM/RAM/PC/save 내용 주입 없이 controller 입력만 실행했다.
관찰 범위 cache020155F0..020157EF512byte 및 stage0201E800..0201ECFF1280byte.
poc/runtime/hangul-keyboard-v1-buffer-writers 및
analysis/hangul_keyboard_v1/buffer_writers.json, tools/report_keyboard_buffer_writers.py가 증거다.

원작 provider860회 모두 descriptor0/slot0. source0200FC80/length32,
result/destination020155F0, nextslot1, source==cache bytes, parser5byte read 확인.
실제 provider entrySP03007698/LR030069E6, copy 준비 SP=entry-40,
pop 직전SP=entry-32. 이는 선택된 route의 값이지 모든 caller/IRQ budget 증명이 아니다.
cache copy 완료부터 pixel enqueue까지860구간, stage enqueue부터 native copy return까지
860구간을 callback으로 추적해 보호 구간 write0건을 확인했다. 최종 pending 없음.
이전 enqueue/consume snapshot 비교에서 놓칠 수 있는 write-and-restore도
이 관찰 범위의 CPU write-start callback에는 기록되지 않았다.

관찰 방법의 positive calibration: cache08000950 STRB r3,[r1,r2]27520=860×32건,
stage030068B6 STR r7,[r2,r1]275200=860×320건. 두 instruction은 원본/current
코드와 동일하며 ARMv4T Thumb roundtrip PASS.
관찰된 cache writes는first32byte, stage write-start는0201E800..0201ECFC.
cache의 추가9byte는 모든 provider snapshot에서0이고 이 route에는 쓰기가 없었다.
이것을41byte 할당/전역 free RAM/전체 writer 소유권으로 채택하지 않는다.
callback 범위 밖에서 시작하는 wider write/다른 DMA 경로/미실행 IRQ·다른 game route
부재를 증명한 것도 아니다. 현재 실제 동작과 관찰 방법의 한계를 구분했다.

이전 transfer-lifetime 실행과 immutable ROM/emulator/checkpoint hash 및
actions/frames/captures를 같게 맞춘 뒤 회귀 비교했다.
9캡처×cache512/stage1280/editor96/record10=36구간 byte identity PASS.
전체 EWRAM/IWRAM/VRAM/palette/OAM45개 snapshot 중27개는 달랐다.
첫 캡처의 RTC hour/minute/second/lastUpdateTime과 CPU cycle/pipeline/IRQ 값이 달랐다.
각 RAM 차이의 전체 인과 설명은 미확정이며 RTC 하나로 모두 설명했다고 주장하지 않는다.
전체 메모리 byte-identical 회귀 검사는 NOT PASS로 report/foundation에 명시했다.
차이를 지우거나 비교에서 숨기지 않았다. 관찰 증거는 지정된36구간과 writer trace에 한정된다.

create-kr-patch의 관찰법 검증/부재 증거 기준과 회귀 범위 분리에 따라
positive write를 확인하고 scoped 결과만 credit했다.
이 결과는 native 일본어4글자 입력 경로이며 한글 자판 화면/새 cache41byte 사용 결과가 아니다.
ROM/사용자 save 변경 없음. 실제 layout/모든 consumer 교체·cache41 소유권·IRQ/stack,
한글 선택/커서/확정·record discrimination·save/fresh-load는 미완료다.
새 bounded writer 증거 포함 foundation 검증 완료. 전체 snapshot NOT PASS 상태를 그대로 유지했다.
91개 tool/84개 artifact hash 재확인 PASS, 새 observer/verifier 및 foundation verifier py_compile PASS.
원본/current playROM/glyph-onlyROM identity 보존 확인.

## 현재 후속 결과: mixed 고정 레코드 native 저장·불러오기 후보 (2026-10-10)

tools/hangul_mixed_record.py 및 cpu_mixed_record/report.json:
완성 한글과 structural native484태그를 width2*cap+2, cap1..10의 고정 레코드로 직렬화.
marker80|count, cap개의 little-endian words, 마지막E5; 미사용FFFF, 미완성/빈 기록 거부.
Thumb encoder408byte, own60/nested96stack, 최대22byte. 실패 시 외부 write 없음.
77393 CPU호출/거부54273, 단일 occupied-word65536domain,
full-cap10 마지막 칸 완성11172종, HOST selected-import/redisplay23120회 PASS.
기존 pure-Hangul 후보와72조건 wire-byte 동일. 새 형식은 채택하지 않았다.

새 native importer는 별도 tools/hangul_mixed_record_import.py,
cpu_mixed_record_import/report.json에 기록했다. Thumb486byte, own88/nested124stack.
caller가 새 형식을 명시한 경우에만 fixed record→compact76으로 초기화한다.
marker/count/terminator/occupied-word/padding을 먼저 검증하고 성공 시에만76byte를 쓴다.
cursor0/activeNone/history0으로 복원하며 partial/empty는 확정된 기록으로 받지 않는다.
83262 CPU호출/거부60058, 단일 occupied-word65536domain PASS.
완성11172종이 가득 찬10글자 마지막 칸에 들어가는 native encoder→native importer를 연결했다.
두 CPU 단계 사이 HOST 메모리 재기록 없음. HOST는 예상 byte/identity 비교만 수행했다.
이 연결은 native 게임의 commit/save 호출이 아니라 독립 CPU fixture다.

자동 legacy 판별의 반례: rank229 '곥', cap4의 새 record는81e500ffffffffffffe5.
기존 importer0803558C는 첫 marker를 무시하고 byte1의E5에서 끝나 빈 문자열로 해석한다.
원본/current 동일 leaf0803558C..355BD를 실제 CPU 실행해E500 및 변경 경계를 확인했다.
따라서 marker만으로 legacy와 새 형식을 구분한다는 가정은 채택하지 않았다.
format caller selection/metadata 또는 migration의 실제 연결은 여전히 필요하다.

create-kr-patch name-entry의 입력/저장/재표시/지속성 분리 기준을 적용했다.
structural native484태그는 실제 자판/글꼴 membership 증명이 아니다.
모든 게임 field의 extent/adopted format, 원작 normalize/commit/read consumer 교체,
UI에 보이는 미완성 확정 거부, stack/IRQ budget, ROM설치 및 save/fresh-load는 미완료다.
기존 whole-memory byte-identical 회귀 NOT PASS 상태도 그대로 유지한다.

foundation 재검증 PASS. 새 encoder/importer/bench4개 및 foundation verifier py_compile PASS.
원본/current playROM/glyph-onlyROM 해시는 이전 값 그대로이며 사용자 save 수정 없음.

## 현재 후속 결과: 실제 marker 선택 의미 및 compact 확정 연결 후보 (2026-10-10)

tools/analyze_keyboard_record_markers.py → record_markers.json:
원본 reader loop08038BAA..38BD1을 실행해26 metadata의57 slot×256marker=14592조건 확인.
0은57조건 모두 제외, 나머지255값은14535조건 모두 유효 기록 index로 선택했다.
CPU는 prerequisite flag 검사 후부터 시작하고 RNG/BIOS 나눗셈/normalize 전에 종료한다.
전체 reader 호출 규약/실제 flag 조건/선택 랜덤성/문자열 재표시 실행을 주장하지 않는다.
실행된40byte 명령은 ARMv4T Thumb semantic roundtrip 및 원본/current 동일성 확인.
정상 buffer-writers route9 EWRAM캡처에서26 항목의513record 관찰: marker0=511, marker1=2.
원작 writer는0803500A..3500C에서1을 쓴다. 그러나 모든 legacy writer/초기값/save 값은 아니다.
높은 marker가 관찰되지 않았다는 이유로80계열을 새 형식용으로 예약하지 않는다.
RAM 관찰은 persistent save representation이나 migration 증거도 아니다.
첫 검증에서 normalize 뒤 font literal까지 포함한 범위가 현재 ROM과 달라 중단했다.
실제 normalize body는08032AC6..32AD7로 분리했고, 이미 패치된 다음 literal을 body에서 제외했다.
변경 차이를 무시하지 않고 instruction/data 경계를 바로잡았다.

tools/hangul_mixed_commit_bridge.py → cpu_commit_bridge/report.json:
compact76을 native replay로 surface24에 복원한 후 native encoder로 고정 레코드를 만든다.
HOST 중간 변환 없이 두 Thumb 단계가 연결된다. 외부 저장대상 쓰기는 전체 검증 성공 후에만 발생.
Thumb944byte, own44/nested140stack(encoder96, replay68은 순차 호출).
23202 CPU호출/거부467, cap4 및cap10 full field 마지막 칸 각각 완성11172종=22344paths.
70키 입력 history와70 history B되돌리기 상태140단계에서 미완성/빈 기록 확정 거부 검사.
입력 compact는 HOST fixture가 만들며, 실제 게임 keypad/hook 입력 경로의 결과는 아니다.
완성/native structural tokens, 미완성 자음, malformed compact, 모든 짧은 source,
short destination, source/destination 겹침, byte alignment에서 ABI/atomic write/stack 경계 PASS.
caller가 새 record형식과 buffer/table/stack 소유권을 확보한 경우만 사용하는 후보다.
원작08035000 commit register ABI·정답 비교·확정 UI·temporary normalizer는 아직 대체하지 않았다.

create-kr-patch의 실제 reader 기반 형식 판단과 machine-code 실행 기준을 적용했다.
automatic discrimination/adopted save format/ROM설치/한글 화면·fresh-load 완료 주장은 보류한다.

새 marker/compact commit 증거 포함 foundation 재검증 PASS. 새3tool+foundation py_compile PASS.
원본/current play/glyph-only ROM SHA256 보존 확인. 사용자 save 수정 없음.
기존 전체 snapshot byte-identical NOT PASS 상태를 유지했다.

## 현재 후속 결과: native 확정 분기 관찰 및 새 handler 후보 (2026-10-10)

tools/capture_keyboard_confirm.py / report_keyboard_confirm.py:
immutable current ROM에서 동일 controller/checkpoint 기준23actions/1232frames/9captures.
handler08034F84..34FB3를212회 관찰. r5=0200FC40, entrySP030076CC.
No choice1(frame875)은 state0C 복귀 후 기록007e7e7ee50000000000이 그대로다.
Yes choice0(frame1075)은 commit08035000(entrySP030076C8/LR08034FA5),
원작+28dest020010A6에019be57ee50000000000을 쓴 뒤 state14로 넘어간다.
08034FA4의 r0=1은 flat 문자열 길이이며, 다음 명령은 반환값 검사 없이 movs r0,#14다.
따라서 새 저장 함수만 교체하면 실패 반환0도 state14로 종료된다. 별도 확정 분기가 필요하다.
원본8MiB aligned BL encoding scan의35000 target 후보는08034FA0 한 곳이다.
데이터/간접호출 포함 완전한 caller 그래프라는 주장은 하지 않는다.
handler48byte의 전체 명령 범위 ARMv4T Thumb roundtrip/current-source 동일성 PASS.
step017/021 PNG 직접 확인: No 후 일본어 원작 자판, Yes 후 넘버맨 대화 복귀.
이것은 Hangul 자판 스크린샷이 아니다. 전체 RAM 회귀 동일성 검증은 새로 주장하지 않는다.

tools/hangul_keyboard_confirm_shim.py / bench_keyboard_confirm_shim.py:
새 layout UI16+dest4+compact76을 caller가 선택한 상태만 사용하는 Thumb152byte handler 후보.
원작 busy/choice/sound 주소를 사용하되 CPU에서는 서비스 호출 결과를 모사했다.
성공은 mixed record 직렬화 후 sound80/state14, 실패/No/Cancel은 sound7F/state0C.
미완성/빈 기록/잘못된 UI capacity/compact-cap 불일치/malformed 데이터는 record를 쓰지 않는다.
record가 editor96 전체와 겹치거나 주소가 wrap하면 compact 밖 UI/dest 영역도 보호하며 거부한다.
원작 임시 buffer02014E74 normalize를 호출하지 않으므로 downstream packed-reader/display 교체가 필요하다.
12579호출: 성공11703, 거부616, busy256, 취소4; 완성11172종 fullcap4 마지막 슬롯 PASS.
원작 handler와 busy/cancel258조건의 r0..r3/NZCV 대조 PASS.
모든 선택 byte256종, UI capacity256종, count/native/partial, malformed76byte,
editor 겹침105조건 및 destination wrap1조건에서 지정 write/stack/reg 경계 PASS.
own8+commit140=148stack는 fixture 상한이며 실제 caller/IRQ 전체 예산은 아니다.
처음 서비스 모사에서 host PC 대입이 even LR을 ARM 모드로 바꿔 unmapped write가 발생했다.
원작 ARMv4T Thumb return 의미를 유지하도록 모사 return의 Thumb bit를 명시한 뒤 전체 rerun PASS.
실제 generated handler→commit helper는 CPU에서 실행하며 host가 그 중간 결과를 재작성하지 않는다.

create-kr-patch의 caller live-state/실패 경계 및 runtime 대 CPU-fixture 구분을 적용했다.
원작 handler-table/ROM 교체는 미설치. 새 layout adoption/format discrimination/consumer graph,
기존 temporary text 재표시/실제 한글 확정 UI/IRQ·stack 및save/fresh-load는 미완료다.

native dispatch의34F78 literal은08034F7C 2-entry table을 가리킨다.
첫 pointer는08034F85(85 4f 03 08), 두 번째는08034FB5이며 관찰된 handler LR은08034F74.
새 handler로의 pointer0 교체 위치를 좁혔지만, 기존 editor와 호환되지 않아 단독 설치하지 않는다.

최종 source와 새 dispatch 위치를 포함해 foundation 재검증 PASS.
새4tool 및 foundation verifier py_compile PASS. 원본/current play/glyph-only ROM hash 보존.
사용자 save 변경 없음. 기존 whole-memory byte-identical 회귀 NOT PASS 상태 유지.

## 현재 후속 결과: packed record→표시 문자열 및 downstream 저장 영역 충돌 (2026-10-10)

tools/hangul_mixed_record_display.py / bench_hangul_mixed_record_display.py:
caller가 선택한 mixed 고정 레코드를 surface24로 staging한 뒤 display(mode1)로 확장한다.
별도 compact76/history/transition table 불필요. Thumb428byte, own44+display36=80stack.
실패 시 외부 write 없음, 전체 declared output extent는 consumed record와 분리해야 한다.
82820 CPU호출/거부59494, occupied-word65536domain, fullcap10 마지막 음절11172종 PASS.
실제 CPU encoder가 만든22byte 레코드를 native display 변환이 소비하며 단계 사이 HOST 재기록 없음.
max41byte, marker/terminator/padding/미완성/빈 기록/잘못된 cap/짧은 입출력/겹침/wrap/bytealignment 검사.
실제 대사 provider나 화면 렌더러는 이 fixture에 연결하지 않았다.

현재 ROM과 같은 원작 raw copier08032AC6..32AD7를 추가 실행했다:
'곥' 표시f9fce500e5→f9fce5만 복사, returned length2.
structural E4/E5 token 표시e4e5e5→e4e5만 복사, returned length1.
새 record/display 사이에는 이 바이트 종료 복사를 사용할 수 없다.
실행은 이미 생성된 CPU 표시 버퍼를 그대로 읽었으며 대상/원본/stack write 경계를 확인했다.
native structural 태그가 실제 glyph/input 지원이라는 뜻은 아니다.

tools/analyze_keyboard_record_redisplay.py → record_redisplay.json:
08038B94 reader는 선택 record+1과 descriptor pointer를 raw copier에 넘긴다.
26 metadata의 source/current descriptor 및 code/literal identity/Thumb roundtrip 확인.
16 descriptor는 첫 record body를 가리키므로 packed record를 같은 자리에 문자열로 확장하면 저장값이 손상된다.
나머지10 descriptor는 별도 주소지만 확보된 free/확장 가능 공간으로 채택하지 않았다.
26개 모두 provider copy bound=2cap+1에 비해 full Hangul stream4cap+1이 크다.
이 bound는 소비 한도이지 allocation 크기 증명이 아니다. bound만 늘려서 설치하지 않는다.
선택 record와 표시 cache를 분리하고 reader/provider 두 경로를 함께 바꿔야 한다.
형식 판별/전체 consumer 및 writer 소유권/실제 대사/저장·fresh-load는 미완료.

create-kr-patch의 저장 identity와 표시 surface 분리/consumer 기반 buffer 판단을 적용했다.
원본/current play/glyph-only ROM 및 사용자 save는 변경하지 않았다.

최종 record/display 및 redisplay 보고서 binding을 포함한 foundation 재검증 PASS.
새 3개 tool과 foundation verifier py_compile PASS. 원본/current play/glyph-only ROM hash 보존.
기존 whole-memory byte-identical 회귀 NOT PASS 상태는 그대로 유지하며 ROM 통합 완료로 판정하지 않는다.

## 현재 후속 결과: native 확정 후 갱신과 임시 문자열 확장 불가 (2026-10-10)

tools/capture_keyboard_redisplay.py / report_keyboard_redisplay.py → native_redisplay.json.
같은 ROM/checkpoint에서25개 정상 입력1422frame 경로를 관찰했다.
frame1075 확정 시 record020010A7→temporary02014E74 raw copier, returned length1/9be5 확인.
frame1092 복귀 시 reader08038B94에 metadata0..25가 모두 진입하고,
selectedRecord+1=020010A7→동일020010A7 raw copier를 호출하는 것을 실제 관찰했다.
fixed-cell provider860건 모두 descriptor0/slot0/32byte→020155F0; descriptor16 소비는 관찰되지 않았다.
step021/025 스크린샷은 넘버맨 대사/네비 화면이며 입력 이름이 실제 대사에 출력되었다는 증거는 아니다.

frame1242의08036A74가02014E94를4byte ldr로 읽었다.
immutable source/current body와 literal36AAC=02014DD0, adds r4,#C4를 확인했고
비제로 분기는02014E98부터 후속 word list를 읽는다. 전체 구조/수명 규명은 아직 아니다.
02014E94는 임시 문자열 시작+32이므로 fullcap8의33byte 문자열은 count 첫byte,
fullcap10의41byte 문자열은 count4byte와 후속 공간을 덮는다.
이 때문에 임시 문자열 기존 공간의41byte 확장은 거부하며 cap4/6 이하 공간도 자동 채택하지 않는다.

create-kr-patch의 consumer 및 공유 상태 소유권 기준을 적용해 별도 버퍼 필요성을 runtime으로 좁혔다.
관찰 read6건은 addressed callbacks이며 전체 bus/write/IRQ lifetime 또는 save 소비 그래프가 아니다.
기존 ROM/사용자 save 변경 없음. 실제 한글 자판·확정 대사·저장 후 fresh-load는 미완료다.

이 native 관찰 보고서 및 source/artifact binding을 포함해 foundation 재검증 PASS.
capture/report/foundation verifier py_compile PASS. 원본/current play/glyph-only ROM hash 보존.
기존 whole-memory byte-identical NOT PASS 상태 유지; 이번 PASS는 한글 ROM 통합 완료가 아니다.

## 현재 후속 결과: native 대사 provider에 직접 레코드 변환 연결 CPU 후보 (2026-10-10)

tools/hangul_dialogue_record_copy.py / bench_dialogue_record_copy.py → cpu_dialogue_record_copy/report.json.
원작 printStringBuffer handler080517D0..5181B는 descriptor를 읽고02010AC0+slot*128로 복사한다.
F90C index에 bit80이 켜진 변수형 경로는 context+4C에서 index를 읽는다.
해당 native handler/literals/descriptor16/source-current identity 및 Thumb1+BL roundtrip을 확인했다.

새80byte copy 후보는 r0=020010A7/r2=9/LR=08051805일 때만 source-1의 cap4 mixed record를
별도 caller-owned128byte cache로 변환한다. 그 외에는 원작0800094C memcpy로 tail-enter한다.
이 gate는 형식 판별이 아니므로 caller가 new record format임을 별도로 보장해야 한다.
선택 record 검증 실패 때 emptyE5만 출력하며 원본 record는 보존한다. 사용자 rejection UX는 미채택.
callee own12+display80=92, 원작handler12 포함104byte stack은 CPU fixture 값이다.

CPU가 원작 handler의 lookup/copy 이후 context+2C/cache pointer, +44/script resume,
+64/slot increment, r4=cache pointer, r0=1 및 return을 실제 실행했다.
11172종 fullcap4 마지막 음절, slots0..7, 변수 selector8건,
legacy9indices×8slots×2selector=144조건의 전체 registers/CPSR/EWRAM 대조 PASS.
selected11198호출, mutated record9건 거부, source record 및 temporary/counter 보존.
입력 record는 이 bench에서 HOST pack_surface로 준비한다. 실제 CPU editor/commit→provider 연속 실행은 아니다.

fixtureBL은08051800에4byte만 바꿨다. 처음08F0A000 호출은 ARMv4T BL 범위를 넘어서 실패했고,
범위·prefix 검사를 추가한 뒤08300000 source-clone 범위에 helper를 둬 검증했다.
08300000은 Unicorn fixture 전용이며 free ROM 공간/실제 설치 장소가 아니다.
실제 append된 helper로 연결하려면 검증된 long-call/veneer 및 Expected Writes가 필요하다.

create-kr-patch의 저장 identity/표시 surface 분리 기준으로 임시32byte 확장을 피하는 경로를 구현했다.
descriptor16 한 레코드만 해당. 전체 selected-record/RNG 갱신 연결, format 판별,
cache 전체 소유권/수명/IRQ·stack, 실제 한글 대사·저장 fresh-load는 미완료다.
원본/current ROM 및 사용자 save 변경 없음.

최종 dialogue copy CPU report/tool/helper binding 포함 foundation 재검증 PASS.
새 helper/bench/foundation verifier py_compile PASS. 원본/current play/glyph-only ROM hash 보존.
기존 whole-memory byte-identical NOT PASS와 실제 한글 ROM 미통합 상태는 유지한다.

## 현재 후속 결과: CPU 입력부터 native 대사 버퍼까지 무재기록 연속 검증 (2026-10-10)

tools/bench_keyboard_to_dialogue.py → cpu_keyboard_to_dialogue/report.json / keyedit.bin.
초기 compact76 cap4/완성3글자/cursor3와 native 대사 context/script는 fixture로 준비한다.
그 뒤37,506 자모 action을 실제 keyedit Thumb로 실행하여 마지막 슬롯11172음절을 만든다.
각 첫 초성 직후 compact commit을 실행해11172회 반환0/레코드 write 없음 검증.
완성 후 native compact commit→fixed record10byte→원작 printStringBuffer provider를 연속 실행한다.
compact, record, 표시 stream은 CPU 단계 사이 HOST 재기록하지 않는다.
HOST 모델/oracle은 읽은 출력과 전체 EWRAM을 비교할 뿐 출력값을 대신 넣지 않는다.

11172 complete pipelines / partial rejection / successful record commits / provider calls 모두 PASS.
cap4 full field 표시17byte, provider slots0..7, source/temporary/counter 보존,
각 stage whole EWRAM/허용 write intervals/stack canaries/return 및 preserved register 검사.
keyedit는08F0B000에 다시 assemble/disassemble final-placement 검증해 실행했다.
부품 report/tool/artifact 해시와 원본/current ROM revision을 묶는다.

create-kr-patch의 입력→저장 identity→redisplay 연결 기준을 적용한 CPU 통합 결과다.
실제 game keyboard/confirm handler/선택 레코드 갱신/marker 자동판별이 아니다.
초기3글자와 editor/context는 fixture이며 마지막 슬롯 조합 경로만 전수 검증했다.
ROM 설치/실제 glyph pixels/전체 cache writer 및 IRQ 수명/native save/fresh-load는 미완료.
원본/current play/glyph-only ROM 및 사용자 save 변경 없음.

연속 CPU pipeline report와 모든 dependency/tool/artifact binding을 포함한 foundation 재검증 PASS.
새 bench 및 foundation verifier py_compile PASS. 실제 ROM 미통합 및 기존 whole-memory NOT PASS 경계 유지.

## 현재 후속 결과: descriptor 삭제/설정 경로 추가 및 형식 정보 수명 제약 (2026-10-10)

tools/analyze_keyboard_descriptor_mutators.py → descriptor_mutators.json.
08035D66은 descriptor[index].pointer-1에0을 쓰고 system default47을 pointer에 raw-copy한다.
source/current default table pointer는086368E8/08800000으로 다르지만 default47 bytes7e7e7ee5는 같다.
0803A0F4는0200F550의16byte 설정 상태를 clear한 뒤 descriptor pointer-1을+4에,
ROM3A11C[index] selector를+8에 저장하고 fixture global surface 첫byte를58로 바꾼다.
selector값은 native keyboard capacity와 일치하지 않으므로 글자 수/입력 cap으로 채택하지 않는다.

각 함수는 source/current ROM26 descriptors씩 실제 CPU에서 실행했다.
delete52/setup52회 PASS; whole EWRAM 예상 write 비교, high registers/SP/stack canary 확인.
setup의 external clear service0803A3B0만 명시적으로 모사했다. default lookup/raw copier는 native 실행이다.
16 descriptor pointer-1은 첫 저장 record marker와 같고,나머지10개는 별도 cache 앞byte다.
모든 pointer-1을 canonical record marker로 취급하는 정책은 채택하지 않는다.

8MiB 원본의4byte-aligned080526D0 literal 후보5곳을 확인했다:
35D7C(delete),38DE8(reader),3A160(setup),5181C(dialogue provider),1EF968(resident fixed provider).
literal exact-match 후보 목록은 계산 주소/간접 소비자/전체 save graph의 완전성을 뜻하지 않는다.
함수 body/literal/descriptor source-current identity와 Thumb1+BL semantic roundtrip을 검사했다.

create-kr-patch의 writer/초기화/해제 소유권 기준으로 필요한 상태 전환을 추가했다.
미래 별도 format discriminator/선택 pointer/cache는 확인된 삭제·설정 전환도 함께 무효화/재설정해야 한다.
전체 legacy marker writer/persistent save compatibility가 입증되지 않아 자동 판별 및 ROM 설치는 미채택이다.
실제 한글 자판 화면/대사 glyph/save fresh-load, 기존 whole-memory NOT PASS 경계 유지.
원본/current play/glyph-only ROM 및 사용자 save 변경 없음.

descriptor mutator CPU/source 분석과 report/tool binding을 포함해 foundation 재검증 PASS.
새 analyzer/foundation verifier py_compile PASS. 이 결과는 전체 writer/save 호환성이나 ROM 통합 완료가 아니다.

## 현재 후속 결과: 설정 selector 의미 및 재진입 initializer/import 경계 (2026-10-10)

tools/analyze_keyboard_setup_import.py → setup_import_caller.json.
앞 단계의 selector UI 해석 불확실성 중, coherent descriptor2..17 범위의 의미를 해결했다.
0803A1C2..3A1E7은0200F550+8을metadata index로 쓰며0803B0D0+16*index에서
capacity(+2)/heading(+3)를 읽고 pointer0200F550+4를 destination으로 넘긴다.
selector0은 heading을08038DB8 반환값으로 바꾸므로 이 service는 fixture33으로 모사했다.
descriptor16→metadata14→capacity4가 관찰된 기존 weak-subject 입력과 일치한다.
이후 coherent mapping 밖의 selector/모든 유효 setup argument는 여전히 규명하지 않았다.

source/current각16descriptor×legacy/mixed2조건=64호출 PASS.
원작 initializer080355B6 및 importer0803558C는 실제 machine code를 실행하고 clear96 service만 모사했다.
legacy1문자9B→word9B/E5 및 cursor1, mixed 완성형rank229 '곥'→wordE5/cursor0을 각각32건 확인.
이 native caller가 새 레코드를 다시 편집하려 하면 빈 입력으로 가져오는 경계를 직접 재현했다.
원본 record/주변RAM 보존, editor96 whole EWRAM expected writes/stack canary/SP/caller live-ins 확인.

교체 대상 호출부:0803A1DE(initializer BL),0803A1E4(import BL).
새 editor layout initializer와 record→compact importer를 같은 형식 판별에 연결해야 한다.
둘 중 하나만 바꾸면 old pointer layout/byte importer가 남으므로 단독 ROM 설치하지 않는다.
create-kr-patch의 초기/불러온 입력 경로와 canonical identity 일치 기준을 적용했다.
ROM/사용자 save 변경 없음. actual game UI/auto discriminator/전체 저장·fresh-load는 미완료다.

최종 setup/import caller source/report/tool binding 포함 foundation 재검증 PASS.
새 analyzer/foundation verifier py_compile PASS. glyph-only ROM hash도 보존했다.
기존 whole-memory NOT PASS 및 실제 한글 ROM 미통합 경계는 유지한다.

## 현재 후속 결과: 원작 호출부의 새 초기화/가져오기/재확정 연결 (2026-10-10)

tools/hangul_keyboard_import_shim.py 및 tools/bench_keyboard_reentry.py 구현.
analysis/hangul_keyboard_v1/cpu_keyboard_reentry/에 final-placement ISA/BL/해시 보고서를 생성한다.
원작0803A1C2..3A1E7 metadata 조회를 실행하며 두 BL만 Unicorn source clone에서 교체한다.
초기화 shim08301000→helper08F0C000, 가져오기 shim08302000→helper08F05000.
08301000/08302000은 설치 위치나 free ROM이 아니며 실제 product artifact는 변경하지 않는다.
selector0 heading service만33으로 모사했다. native clear service는 새 initializer가 사용하지 않는다.

새 importer adapter는 r0가 새 editor+16 destination과 일치하는지, UI capacity1..10,
bounded EWRAM record 및 editor96 전체와 disjoint인지 먼저 검사한다.
성공 때 compact76(editor+20)을 복원하며 r4..r11/SP를 보존한다.
형식은 caller가 명시적으로 선택해야 한다. marker 자동판별이나 legacy migration은 구현하지 않는다.
adapter own8+nested124=132byte, caller 최대 initializer140byte는 CPU fixture stack 범위다.
실제 IRQ/게임 stack 여유나 editor 수명 소유권을 채택한 것은 아니다.

caller imports11284, 재확정11220, 완성11172종 fullcap4 마지막 칸 재진입 PASS.
한글 rank229의 E5 payload도 정확히 복원되어 원작 importer의 빈 입력 반례를 해소했다.
import→commit 사이 HOST editor/record 쓰기 없이 CPU가 동일 record를 재출력한다.
16 coherent descriptor row의 cap4/6/8, 혼합 native-tag 레코드도 검사했다.
빈/손상 record64건은 initialized-empty editor로 유지하며 반환0; adapter 주소/전체editor 겹침37건은 editor 무변경.
원작 caller는 반환값을 무시하므로 이 동작은 오류/취소 UX로 채택하지 않는다.
whole EWRAM Expected Writes/실제 write interval/r5 및 상위 register/SP/canary를 확인했다.

create-kr-patch의 재진입 canonical identity 및 초기화/consumer 동시 교체 기준을 적용했다.
아직 실제 keypad dispatch/page/cursor/render/선택 갱신/format 상태/모든 저장 consumer 연결이 남는다.
원본·현재 play ROM 및 사용자 save를 변경하지 않았다. 실제 한글 화면/저장·fresh-load 검증은 미완료다.
기존 whole-memory NOT PASS 경계는 그대로 유지한다.

새 reentry report/dependency/tool/bin 및 원작 BL source guard를 포함한 foundation 재검증 PASS.
새 adapter/bench/foundation verifier py_compile PASS; glyph-only ROM SHA256도 기존값과 일치한다.

## 현재 후속 결과: 원작 A/B 호출 ABI 및 자모 선택/삭제/글자 커서 연결 (2026-10-10)

tools/hangul_keyboard_action_shim.py 및 tools/bench_keyboard_actions.py 구현.
cpu_keyboard_actions/report.json과 shim/dispatch/keyedit/rebase/selector binaries 생성.
원작08034F08의BL080353B0와08034F0C의BNE08034F66을 실제 CPU 실행한다.
BL만Unicorn source clone에서08303000 후보 adapter로 교체했고 source/current6byte identity/semantic roundtrip을 검사했다.
실제 ROM 설치 위치/free ROM 채택이 아니다. outer per-frame draw/navigation 전체는 실행하지 않았다.

r5=new editor96, r10 global+4 key-state pointer, key-state+2 pressed uint16을 읽는다.
원작처럼 B를 A보다 우선한다. A/B가 없으면r0=0/Z=1로 원작 다음 navigation instruction08034F0E에 도달한다.
A/B 처리(입력 거부 포함) 때r0=1/Z=0로 BNE가08034F66으로 분기한다.
이 규칙을 유지하지 않으면 거부된 키 뒤에서 자판 선택 커서가 움직이는 부작용이 생길 수 있다.
old word pointer+16/+20/+24나 flatten buffer는 읽지 않는다.

기존 candidate plan first6rows/15columns90칸에서40개 자모를 모두 매핑한다.
105칸 plan의 seventh row15칸은 native6row navigation 밖이며 모두 inactive다.
page0 자모만 지원; 빈칸은 소비하되 compact 무변경. col15 row2/right42,row3/left41 연결.
다른 command/page/Start/shoulder 기능, 확정·취소·쉼표·Latin·page upload·음향·거부 feedback은 미구현이다.
특히 A/B없는 다른 키는0을 반환할 뿐 완전한 원작 handler 호환이 아니다. 실제 UI에 이 일부 handler만 설치하지 않는다.
불러온 canonical B와 새 key-history B는 기존 dispatch가 구분한다.
UI cap/compact cap 일치 및 fixed editor entry를 먼저 검사한다.

52647 CPU호출: accepted50554/rejected-consumed1325/unhandled768.
three empty/history/loaded states ×3pages×96positions 및 pressed10bit domain1024각 검사.
잘못된 row/column/page/cap/compact, fullcap4 마지막 칸11172종 조합과 B를 확인했다.
각 음절의37,506 A키 동작은 실제 grid row/col→selector→dispatcher 경로를 실행한다.
음절 내 CPU key 사이 HOST compact 재기록 없음; UI row/col/mask는 fixture가 설정한다.
whole EWRAM Expected Writes/CPU write intervals/r4..r11/SP/Z/stack208byte canary PASS.
stack208은 adapter12+nested196 fixture 범위이며 실제 IRQ/게임 여유를 뜻하지 않는다.

create-kr-patch의 active/inactive selector enforcement 및 입력 경로 canonical identity 기준을 적용했다.
원본/current ROM·사용자 save 변경 없음. actual emulator Korean keypad/field pixels 및 save/fresh-load 미검증.
기존 whole-memory NOT PASS, 형식/수명/모든 소비자 교체 및 ROM 미통합 경계를 유지한다.

새 A/B report·dependency·tool·final-placement binaries·원작 BL/BNE source guard 포함 foundation 재검증 PASS.
새 shim/bench/foundation verifier py_compile PASS; glyph-only ROM SHA256는 기존값과 동일하다.

## 현재 후속 결과: 페이지/Start/빈 입력 취소 및 요청→예/아니오 연결 (2026-10-10)

tools/analyze_keyboard_control_routes.py → control_routes.json.
원작353B0/35038/35620 machine code를 source/current에서 실행했다.
page upload356D0/sound00534/cursor refresh35086/dialog322CC만 service로 모사한다.
112command/6comparator, page transition60/confirm request24/cancel exit2 PASS.
원작 확인 목록은 source08636C26/current08800355에서E5 한byte(빈 항목)이다.
내용 제한/금칙어 목록으로 추정했던 해석은 기각한다. 입력0은 skip,98/E5는 종료하며
빈 입력→sound69/script11/substate4, nonmatch→sound1D3/script10/substate0을 실제 비교 코드로 확인했다.
Start는 먼저col15,row5를 선택하고 두번째에 요청한다. L/R은page0..2 순환, B우선 경로는 기존대로다.
emptyB 최초에는state14/callerValue+10=0/cancelFlag+14=2; flag2 재호출은r0=2/Z=1이다.
새 raw handler에서 단순 boolean 반환만으로 원작의 전체 flag 동작을 일반화하지 않는다.

tools/hangul_keyboard_control_shim.py 및 tools/bench_keyboard_controls.py 구현.
cpu_keyboard_controls/helper.bin(query dependency 별도) 및 final-placement ISA/report 생성.
r0 logical command0prev/1next/2toggle01/3toggle12/4Start/5emptyCancel, r5neweditor96.
기존 A/B raw adapter는 수정하지 않았으며 새 논리 helper와의 실제 키 연결은 아직 없다.
page service 호출은 CPU 모사만 했으므로 한글/Latin selector·실제 page glyph upload의 증거가 아니다.
Start 요청은 compact를 validate/replay하고 stack24에 dry-run commit한다.
완성 nonempty면 원작script10/state10, empty면script11/state10/substate4,
partial면sound7F를 내고 편집 상태를 유지한다. malformed query는0/무변경이며 오류 UX는 미채택이다.
empty 안내의 별도substate handler34FB5 경로는 이번 연결 검증에 포함하지 않았다.
emptyCancel은validated current count0에서만+10/+14/state를 갱신한다.
own40+commit140=180byte fixture stack; query100은 순차 실행이며 실제 게임/IRQ 여유가 아니다.
초기 conditional branch의Thumb1 도달 범위 문제를 near failure trampoline으로 수정하고 final-placement roundtrip 통과했다.

11452controls/complete requests11176/partial rejects4/empty requests4/cancel exits4/page changes144 PASS.
cap4/6/8/10 empty/partial/complete 및 invalid command/page/compact를 검사했다.
11172완성형 fullcap4 마지막 칸 요청→Yes5586/No5586을 같은 compact로 CPU 실행한다.
요청→응답 사이 HOST editor/record rewrite 없음; 요청시 레코드 보존, Yes에서만 기록, No는state0C 확인.
whole EWRAM Expected Writes/실제 interval/register/SP/Z/180byte stack canary 확인했다.
create-kr-patch의 미완성 확정 금지·원작 확인 분기 보존·persistent record 쓰기 경계 기준을 적용했다.
ROM/user save 변경 없음. raw-key glue, candidate pages, 실제 렌더/형식·수명/소비자/ROM hooks/save fresh-load는 미완료다.
기존 whole-memory NOT PASS 경계 유지.

원작 control routes 재실행 및 새 control report/tool/dependency/binary binding 포함 foundation 재검증 PASS.
analyzer/control helper/bench/foundation verifier py_compile PASS; glyph-only ROM hash도 보존했다.

## 현재 후속 결과: raw 버튼→편집/페이지/Start/취소 연속 연결 (2026-10-10)

tools/hangul_keyboard_raw_router.py 및 tools/bench_keyboard_raw_router.py 구현.
cpu_keyboard_raw_router/helper.bin/report.json 생성. 기존 AB/논리control 코드는 수정하지 않았다.
원작08034F08 BL만Unicorn source clone에서08304000 후보로 변경하고 BNE08034F0C까지 실행한다.
BL Thumb1 range/prefix/final target와 source/current6byte identity를 검사했다.
08304000은 실제 hook 설치/free ROM 위치가 아니다. source clone 외 제품 ROM 변경 없음.

r5=new editor96, r10 global+4 key state pointer, key+2 pressed uint16을 직접 읽는다.
B>A>Start>L>R 우선순위. A/B/Start/L/R 없는 입력은0/Z1로 다음 navigation instruction에 도달한다.
소비한 입력 및 거부는1/Z0로 원작BNE 종료 경로에 도달해 같은 프레임의 grid navigation을 막는다.
B는validated current count0이면 empty cancel, nonempty이면 기존조합-history/canonical delete dispatch다.
col15row0/1은page toggle,2/3은caret,5는confirm request; row4 space mapping은 아직 미구현.
Start는현선택에서end cell로 이동 후 두번째 요청. L/R shoulder는page 전환helper로 연결했다.
반복 empty cancel은 새 후보가1/Z0로 소비하며 원작flag2/Z1 quirks와 의도적으로 다르다.
page0만40자모 입력을 지원하고 다른page의Latin/selector/glyph 공급은 미완료다.
whole-frame draw/refresh 및 실제 page uploader는 실행하지 않았다. 원작 uploader를 새 asset에 그대로 쓰지 않는다.

mask1024×four cells×empty/partial/complete3상태=12288조건, 다른page/손상compact/순차Start와page 검사.
raw calls72235/consumed71851/unhandled384 PASS.
11172완성형 fullcap4 마지막 칸: A입력37506→Start2회→Yes5586/No5586을 연속 CPU 실행한다.
단계 사이 HOST compact/record 재기록 없이 canonically 동일한 조합/저장 및 No record 보존 확인.
initial3완성형/editor/context/key mask/cell좌표는fixture이며 자연스러운 gamepad 플레이 증거가 아니다.
whole EWRAM Expected Writes/write interval/r4..r11/SP/Z/stack220byte canary PASS.
own12+기존 AB208=220, 논리control192/query112는순차이며 실제 게임/IRQ budget은 미채택이다.
sound/page/dialog/busy/choice service는명시적으로모사했다. 실제 픽셀/음향/대화창 handler 또는 save의 증거가 아니다.

create-kr-patch의 selector→partial→완성/확정연결 및 조작 우선순위/거부 시 상태 보존 기준 적용.
다음은 자판 page graphics/selector 공급과 outer frame/edit-field/cursor render 연결이다.
format 상태/모든 consumer 교체/ROM 설치/실제 한글 화면/native save fresh-load 미완료.
ROM/user save 변경 없음. glyph-only hash 보존; 기존 whole-memory NOT PASS 경계 유지.

새 raw router report/tool/dependency/helper 및 source BL/BNE guard 포함 foundation 재검증 PASS.
raw router/bench/foundation verifier py_compile PASS; 원본/current ROM hash도 최종 재확인했다.

## 2026-10-10: 자모 페이지 타일/배치 및 원작 draw/queue CPU 연결

`tools/prepare_keyboard_page_graphics.py` → `page_graphics/report.json`, native3page PNG,
`jamo_page0_tiles.bin`5472bytes/`jamo_page0_map.bin`1200bytes/`jamo_page0_preview.png`.
`tools/bench_keyboard_page_graphics.py` → `cpu_page_graphics/report.json`.

원작 page_draw08035676은 page table080356C0의30x20 LEhalfword BG map을 고른다.
원작 page_transfer080356D0은080356E8의16byte descriptor를 page*16으로 조회한다.
세 uncompressed4bpp tile bank는0863ABF4/0863D174/0863F654, 크기9600/9440/7232bytes.
모두 VRAM06008000이며 map palette9/10bit tile index/flip을 독립 디코드했다.
current playable ROM의 해당 자료는 원본과 동일하다. 전체 ROM reference completeness를 주장하지 않는다.

page0의 왼쪽 grid x16..190/y56..151 원작 background5/9 및 stroke7/8을 분리했다.
blank strip x14/15와 모든 살아있는 background sample이 (x+y)%4==3→5, 그 외9 패턴과 일치한다.
기존 selector plan의40자모 BDF bitmap을 색1→7/2→8로만 변환하며 배경은 유지한다.
50inactive 위치의 일본어는 제거하고, 명령 영역을 포함한 grid 밖 모든 픽셀을 보존한다.
타일 전체 재인덱싱 후 pixel decode roundtrip PASS. 171tiles/5472bytes, VRAM 끝06009560은 editing-field0600B000 이전이다.
이는 정적 크기 적합성만 증명하며 natural residency/IRQ/scanout이나 RAM 채택은 아니다.

source/current/candidate CPU clone3종에서3pages×4vertical offsets(-8/0/8/16)×3queue counts(0/95/96) 실행.
native page_draw/IWRAM map copy03005A94/fill03005B08/08C8 descriptor loader/0850 enqueue/07DC drain은 실제 코드다.
화면 설정0803438A/08034364 및 BIOS CpuFastSet만 모사한다. native instruction scope는 ARMv4T Thumb1 semantic roundtrip 검사.
108draws/72enqueues/36drains/36queue-full rejects PASS.
candidate page0 draw12/실제 queue→BIOS모델 전송4 PASS. queue0에서 draw→enqueue→drain 사이 HOST map/editor/queue/bank 재기록 없음.
whole EWRAM/VRAM Expected Writes/ABI/stack32(draw),40(enqueue),48(drain) canary PASS.
queue95/96은 enqueue 경계만 보며 기존 알 수 없는 항목 drain은 실행하지 않는다.
native map writer가 r1을 시작 행이 아니라 마지막 다음 행으로 남기는 live-out을 검사했다.

원작 cursor080352E6은 rawcol*11에 group 간격6/6 및 command 간격4를 더한다.
6rows×16cols×4blink states×3variants=1152cursor calls PASS.
40자모×4blink×3variants=480조건에서 glyph x=cursor x+1/y=cursor y+8 정렬을 확인했다.
스프라이트 제출08029538은 모사했으므로 실제 스프라이트 픽셀 또는 게임패드 선택 runtime 증거는 아니다.

CPU clone에서만 page0 map pointer/transfer source+length를09002000/09000000 fixture asset으로 바꿨다.
expected source/final bytes를 report에 기록하며 이 주소는 설치 위치 또는 채택된 free ROM이 아니다.
제품 ROM/사용자 save 변경 없음. 페이지1/2·명령 라벨은 원작 일본어이고 입력 지원도 미완료다.
PNG는 기존 원작 관찰 palette9로 오프라인 재구성한 자료이며 actual Hangul UI screenshot으로 제시하지 않는다.

create-kr-patch의 storage→lookup→load→consumption 구분, glyph/editor/grid 경로 분리,
소비 위치/전송 길이/보존 픽셀/변경 범위 검증 기준을 적용했다.
다음은 raw 입력 page control→실제 candidate page upload/draw 연속 연결과 outer frame/editor/cursor 갱신이다.
형식 상태·모든 consumer 교체·실제 ROM 설치·명령/Latin/공백 지원·save fresh-load는 아직 미완료다.
이전 whole-memory NOT PASS 경계와 release false는 유지한다.

새 page graphics source/assets/CPU report/palette/native code/table guards를 포함한 foundation 재검증 PASS.
두 새 도구와 foundation verifier py_compile PASS; 원본/current ROM 해시 보존 확인.

## 2026-10-10: raw 페이지 입력→원작 그래픽 경로 연속 연결 및 queue 포화 거부

`tools/bench_keyboard_page_input_pipeline.py` → `cpu_page_input_pipeline/report.json`,
`unguarded_control.bin`(CPU 비교 전용; 제품 코드 아님).
`tools/hangul_keyboard_control_shim.py`의 page branch에 queue admission guard를 추가했다.
native0850이 counter>=96이면 전송등록을 조용히 생략하는데, 기존 logical control은 page index를 먼저 바꿨다.
새 코드는 native queue counter02010724를 읽고 unsigned>=96이면 UI mutation/sound/upload 전에 실패한다.
raw router가 해당 입력을 소비하므로 같은 프레임의 navigation은 진행되지 않는다.
검사 없는 비교 변형도 ARMv4T assembler/semantic roundtrip 후 CPU 실행해 page0 VRAM 상태에서 page1 map/index만 바뀌는 반례1건을 재현했다.
비교 변형은 명시적으로 QUEUE_GUARD만 제거한 코드이며 실제 이전 제품 ROM이나 설치 위치가 아니다.

원작BL08034F08/BNE 호출→raw router→logical controls→native356D0 uploader→08C8/0850 queue 등록 실행.
이어 native35676/IWRAM map clear/copy/352E6 cursor→07DC queue drain→BIOS모델이 동일한 page 자료를 소비한다.
helper0830xxxx/page자료09400000/09402000은 CPU fixture이고 제품 free-space 채택이 아니다.
후속 단계 사이 HOST compact/editor/queue/map/bank 재기록 없음. HOST가 공급하는 것은 초기 상태와 버튼/선택 칸뿐이다.
per-frame caller에서 native draw 함수를 이어 호출하는 CPU harness이며 원작 전체 outer-frame를 실행한 것은 아니다.
각단계 whole EWRAM/VRAM Expected Writes, CPU write interval, r4..r11/SP/stack canary와 raw BNE flags PASS.
queue/source payload 수명 및 page map을 통한 최종 소비 pixel decode까지 검사했다.
stack bound는 raw220/draw32/cursor8/drain48 각각 순차 CPU fixture 한도이고 실제 game/IRQ stack은 미채택이다.

623input calls/477page transitions/865draws/725drains/50jamo actions/41backspaces PASS.
empty/partial/complete×3pages×3cells×6mask 우선순위와40자모 입력→R3/L3 왕복→B를 검사한다.
6pending uploads 및 실제 CPU 버튼으로96pending uploads를 채운 뒤97번째 요청을 거부했다.
full queue에서도 ㅏ 입력/삭제를 실행한 뒤, 실제96known entries를 원작 drain으로 소비했다.
pending transitions102, page queue rejects37(실제 포화1 및 full/corrupt fixture36) PASS.
counter96/97/FFFFFFFF×3pages×4page actions는 CPU fixture 경계 조건이며 unknown 기존 entries를 drain하지 않는다.
queued 전송이 아직 소비되지 않은 동안 scanout의 map/tile 동기화와 VBlank/IRQ 동시성은 이 증거가 확정하지 않는다.

원작 page uploader/queue/map writer는 더 이상 이 bench에서 모사하지 않는다.
BIOS CpuFastSet, sound, display config, sprite submit은 여전히 모사한다.
queue reservation/IRQ concurrency, full-queue feedback/retry UX는 미채택이다.
페이지1/2 letters 및 명령 라벨·Latin/공백은 미완료이고 actual game/editor redraw/ROM install/save/reload 증거가 아니다.

create-kr-patch의 소비까지 연결되는 asset 경로 및 페이지 변화에서 입력/표시 상태를 보존하는 기준을 적용했다.
기존 controls bench와 raw router bench는 명시적으로 초기 queue0을 공급하도록 수정해 새 guard 전제와 일치시켰다.
원본/playable ROM과 사용자 저장 파일은 변경하지 않았으며 release false/whole-memory NOT PASS 경계를 유지한다.

새 guard 적용 후 logical controls11452조건/11172request→Yes/No 및 raw calls72235/11172조합→Start→Yes/No 재실행 PASS.
새 pipeline 및 변경 helper/report/tool/의존 해시를 포함한 누적 foundation 재검증 PASS.
변경5개 도구 py_compile PASS; source/playable/glyph-only ROM의 기존 SHA256을 모두 재확인했다.
다음 연결 대상은 raw 조합 입력→편집창 cache/한글 glyph 공급과 페이지 그래픽의 함께 갱신되는 경로다.

## 후속: raw 입력→입력창 한글 픽셀 연속 CPU 연결 (2026-10-10)

`tools/hangul_keyboard_refresh.py`와 기존 page input bench의 `--editfield` 경로를 추가했다.
결과: `analysis/hangul_keyboard_v1/cpu_input_render_pipeline/report.json`.
고정 editor96(0200FC40)에서 compact76→cache41(020155F0)→원작 parser03006824→stage0201E800→원작 queue/drain→VRAM0600B000 순서다.
원작20cell×64byte 픽셀1280byte를 glyph-only ROM의 mono provider/legacy font로 독립 비교했다.
초기 fixture 설정 후 HOST가 editor/cache/stage/queue/map/bank를 단계 사이 재기록하지 않는다.
페이지 draw와 입력창 전송은 같은 큐를 사용한다. BIOS/음향/화면 설정/스프라이트 제출만 모사한다.

666버튼/482페이지 전환/918배치/781소비, 자모66/삭제57/커서6조건 PASS.
refresh920호출: 등록781/보류139/소비 후 최신 상태 재표시2경로 PASS.
fullcap4 마지막 슬롯의 `ㄱㅜㄱㅇㅓ`, `ㄷㅏㄹㄱㅏ`, `ㄲㅗㅏㅣㄹㄱ` 조합·페이지 왕복·커서 이동·키별 삭제도 연속 검사했다.
guard는 counter>=96을 거부하고 기존 queue의 source interval이 stage1280byte에 겹치면 cache/stage를 쓰지 않는다.
95개 occupied 위치×12범위/0길이/overflow 경계=1140조건과 잘못된 editor7조건의 원자적 무변경 거부 PASS.
원작 parser가 r8/r9를 바꾸는 것을 확인해 wrapper가 r8/r9/r10을 복원하도록 수정했다.
wrapper own32+cache112=144byte stack, parser/queue56은 별도 순차 호출이다. guard own12.
모든 호출의 r4..r11/SP/flags 및 전체 EWRAM/VRAM 변경 범위/stack canary를 검사했다.

create-kr-patch의 입력 상태와 전송 버퍼 수명 보존 기준을 적용했다.
helper08F12000/guard08F13000 및 cache/context/stage는 CPU fixture이며 실제 free ROM/RAM 채택 증거가 아니다.
보류 후 재시도는 queue drain 다음 CPU harness가 호출하는 방식이고 실제 outer frame/VBlank/IRQ 동기화나 UX 채택은 아니다.
원작 전체 frame·한글 glyph tilemap의 실제 입력창 배치·자연 입력·스크린샷·저장/재실행은 미검증이다.
나머지 페이지 문자/명령 라벨/Latin/공백, 새 editor 초기화·format/모든 reader/writer 교체도 남았다.
기존 whole-memory NOT PASS/release false 경계를 유지한다. 한글 자판 ROM hook은 설치하지 않았다.

default page-only bench와 새 editfield bench를 포함한 누적 foundation 재실행 PASS; 변경3도구 py_compile PASS.
원본/playable/glyph-only ROM SHA256 불변 확인. 사용자 저장 파일은 변경하지 않았다.
다음 연결 대상은 실제 outer-frame의 입력창 갱신/보류 재시도 지점과 초기화·종료까지의 RAM/queue 수명 검증이다.

## 후속: 원작 입력 상태 프레임과 자연 방향키 선택 CPU 연결 (2026-10-10)

`tools/hangul_keyboard_frame_adapters.py` 및 기존 pipeline의 `--editfield --frame`을 추가했다.
결과: `analysis/hangul_keyboard_v1/cpu_keyboard_frame/report.json`; 누적 foundation에도 연결했다.
원작034E34 dispatcher/body와 상태12의034EFE 입력 handler를 끝까지 CPU 실행한다.
추가 BL5곳: 034E48/034E4C의 구 padding/flatten→공용 no-op,
034E50의 입력창 render→08305000 far veneer→08F12000 refresh,
035350의 구 pointer caret count→08305200 validated compact caret adapter,
034F5C의 일본어 이동 보정→08305300 한글 두 칸 보정 adapter다.
원래 raw input BL034F08과 page0자료 pointer 교체는 앞선 CPU fixture를 유지한다.
각 source body instruction/BL은 ARM7TDMI Thumb1 assembly/disassembly roundtrip 및 immutable source bytes를 확인했다.
helper08305xxx/08Fxxxxx와 cache/context/stage는 실제 free ROM/RAM 채택이 아니다.

### 반례와 수정

원작 page0/1 이동 table은 (6,2),(8,2)를 빈 칸으로 취급해 모든 방향에서 이웃으로 보낸다.
원작 방향키 graph에서 reachable grid87칸이며 새 active40자모 중 selector25=`ㅕ`,27=`ㅗ`는 접근 불가능했다.
보정 전 연속 버튼 검사는 `ㅕ` 접근 실패로 중단됐으며 통과로 기록하지 않았다.
한글 page0의 이 두 위치만 retain하고 나머지는 원작035086으로 tail-call한다.
페이지1/2와 다른 특수 칸/명령 칸의 원작 이동 규칙을 유지한다.
앞선 대화의 `ㅛ` 표기는 잘못이며 실제 두 번째 글자는 `ㅗ`임을 명시적으로 정정했다.

### 검증 결과

2213 native input-state frames/input calls,482페이지 전환,2469배치,2330원작 queue 소비 PASS.
3페이지×6행×16열×5direction/repeat masks=1440조건에 연속 버튼 이동46조건을 더해 navigation1486조건 PASS.
한 세션에서 초기 `가` 편집 상태 이후 HOST grid/caret/editor 위치를 다시 쓰지 않고,
46방향키 이동으로40자모 각각에 도달해 A를 누르고 허용된 입력만 B로 되돌렸다.
거부된 조합은 B로 되돌릴 입력이 아니므로 무조건 B를 누르지 않는다. 이 검사는 상태12를 벗어나는 빈B 취소 경로를 주장하지 않는다.
자모106/삭제76/명시적 caret6; native editing caret sprite1030조건의 x좌표를 replay의 입력 전 logical caret와 독립 비교했다.
원작 cursor는 입력 처리 전에 그려지는 순서를 유지하므로 같은 프레임 입력 후 caret 위치라고 주장하지 않는다.
원작 blink BLE는 signed 비교이므로 low nibble1..7만 표시한다. unsigned 비교를 쓰던 검사 기대값을 수정했다.
원작 page map fill/draw 뒤03564E/034C54 계열이 배치하는 두 ten-column strips의40tile entries를 독립 table 해석과 whole EWRAM Expected Writes로 검사했다.
그래픽 transfer source/VRAM1280byte는 고정 glyph-only ROM의 provider 출력과 비교했다.
refresh2469호출 중 queued2330/deferred139, drain 뒤 무입력 native frame 재시도2조건 PASS.
retry 때 HOST가 grid/editor 위치를 다시 쓰지 않는다. 실제 VBlank/IRQ scheduling을 채택한 것은 아니다.
stage guard1140범위 조건과 malformed editor7조건, full queue97번째 page request의 원자적 거부와 unguarded mismatch 반례도 유지했다.

중첩 stack 상한은 원작 outer frame20+native input8+raw220=248byte CPU fixture다.
refresh144와 caret adapter108은 순차 다른 경로이고 game/IRQ stack budget 채택은 아니다.
r4..r11/SP/flags/stack canary 및 단계별 whole EWRAM/VRAM/CPU write interval 검사 PASS.
전체 frame 실행 후 bounded034F08..034F66 재사용 시 CPU 검사기가 정지 지점을 넘어 POP을 실행해 SP+8/PC0으로 실패하는 것을 확인했다.
CODE hook에서 요청된 정지 지점 BEFORE instruction에 명시적으로 정지하도록 보강했으며 원작 게임 코드는 이 문제 때문에 수정하지 않았다.
보강 후 기존 page-only623조건, editfield666조건 및 새 frame 경로와 누적 foundation 재실행 PASS.
변경3도구 py_compile PASS. 원본/playable/glyph-only ROM SHA256 불변; 사용자 저장 파일 미변경.

### 남은 완료 조건

create-kr-patch의 선택→편집→glyph 소비 연결 기준으로 접근 불가능 active자모를 발견하고 제거했다.
CPU source clone의 상태12만 검증했다. initialization/import/animation/confirmation/exit의 전체 frame 및 natural emulator entry는 미검증이다.
BIOS/음향/화면 설정/스프라이트 제출은 모사하며 실제 scanout/한글 screenshot/사람의 가독성 승인은 없다.
Latin/공백/다른 페이지 문자/명령 라벨, 실제 RAM/cache/stage/queue의 writer·IRQ 소유권 및 ROM hook 설치는 남았다.
모든 committed record consumer/format discrimination, cap10 저장 extent, native save/reset/fresh-load도 아직 미완료다.
기존 whole-memory NOT PASS/release false 경계를 유지한다.
다음 단계는 초기화·확인·종료의 coordinated replacement 및 working RAM/stack 수명을 검증하고,
입력창 국소 성공과 별개로 cap10 레코드 저장/후속 redisplay의 용량·소유권 문제를 해결하는 것이다.

## 2026-10-10 후속: 초기화·확인·종료 상태 전이 CPU 연결

`tools/bench_keyboard_lifecycle.py` 및 `cpu_keyboard_lifecycle/report.json`을 추가했다.
새 initializer08301000→08F0C000과 confirm08F08000/commit08F06000을 검증된 이전 helper에서 읽는다.
원작034E34가 실제 state dispatch table을 읽고 state0/4/8,16,20을 실행한다.
확인 테이블034F7C의 원작08034F85만 CPU clone에서08F08001로 바꾼다. ROM 파일은 변경하지 않는다.
원작 instruction range를 literal/table과 분리해 Thumb1 disassemble→assemble 일치와 source/current identity를 검사했다.

용량1~10×heading bit0/128×callerValue0/1/2=60조건을 진행했다.
초기화120, 프레임4620(진입2160/종료1920), 확인60, No120, busy120, 미완성 자음 거부60,
재진입60, 취소 종료60, byte15 카운터255→0 wrap60조건 PASS.
busy→No1→No2→Yes 사이 HOST compact/결과 버퍼 재기록 없이 동일 편집값으로 확인한다.
state16 substate4의 busy 유지/원작 입력 복귀도 검사했다.
진입은 callerValue2일 때만 offset을 음수로, 종료는 callerValue!=0이면 음수로 만드는 원작 차이를 보존했다.
종료 byte13은 확인1/취소2로 구분하고 최종 r0/Z liveout과 대응한다.
재진입 initializer가96byte 편집 상태를 초기화해도 분리된 committed buffer는 유지된다.
각 호출의 whole EWRAM Expected Writes/CPU write interval/r4..r11/SP/stack canary를 검사했다.
init140byte, state16 outer20+dispatch4+confirm148=172byte는 CPU fixture 한도다.

### 증거 한계 및 다음 작업

이 검사는 preload/page-upload/palette-heading-upload, main의 legacy pad/flatten/refresh/page-map/field-map,
state12 입력을 명시적으로 모사한다. 이전 state12 CPU 픽셀 경로를 전체 lifecycle에 합친 검사가 아니다.
full/partial compact, state16 dialog 진입 및 취소 시작은 HOST fixture다. 자연스러운 게임 진입/Start/빈B 경로를 주장하지 않는다.
test-owned02001000 결과 버퍼는 cap10의22byte 저장을 허용하지만 실제 게임 저장 extent를 증명하지 않는다.
종료 완료값 확인은 graphics queue 해제/IRQ 소유권 증명이 아니다. 실제 code/RAM/stack 소유권 채택도 없다.
cap10 실제 저장 공간·레코드 판별·모든 redisplay provider·native save/reset/fresh-load가 가장 중요한 미완료 조건이다.
누적 foundation에 별도 범위로 연결했다. 실제 ROM hook/한글 screenshot/release 및 whole-memory NOT PASS는 여전히 미완료다.

누적 `verify_hangul_keyboard_foundation.py` 전체 실행 및 변경 도구 py_compile PASS.
원본/playable/glyph-only SHA256은 기존값과 같고 세이브 파일에 쓰지 않았다.

추가 source inspection에서 calendar caller08031030은 main034E34 반환 Z/r0를 실제로 소비한다.
성공 r0=1일 때08031040..3104E가 caller r5+0x32의 slot index를7bit shift하고,
02026281(02026280 staging의 marker 다음)→02026080+index*128로 rawE5 copier08032AC6을 호출한다.
이어서 caller state=0x24로 진행한다. 취소는 state=0x3C로 갈라진다.
source body031030..031060 SHA256 `893409c7c41b88f980548c3f2d30fd7c47ced16ebdff3a9e59e56937d6383468`.
이는 bounded static 전송 경로이며 저장 슬롯의 전체 소유권/폭/개수나 native save 경계를 증명하지 않는다.
새 packed word 레코드를 rawE5 copier에 그대로 넘길 수 없으므로, 다음 조사 대상은 이 성공 경로의
바이너리 레코드→calendar 저장/표시 consumer 변환과02026080 pool의 writer/reader/save 수명이다.

## 2026-10-10 후속: cap10 달력 성공 호출부의 레코드 전송/실패 분기

`tools/hangul_calendar_record_transfer.py`, `tools/bench_calendar_record_transfer.py` 및
`cpu_calendar_record_transfer/{helper.bin,finalizer.bin,report.json}`를 추가했다.
원작 calendar success caller08031040..3105E의 BL3104E만 CPU clone에서08306000으로 바꾼다.
caller suffix31052..3105E도 함께 finalizer08306100 호출로 교체한다. global rawE5 copier는 건드리지 않는다.

### 결함과 처리

원작은 marker 다음02026281부터 pool02026080+index*128로 바이트 단위 E5 복사한다.
새 cap10 record22byte의 count/format marker를 잃는11172조건 및 마지막 음절 low byteE5로
20byte word payload 중간에서 멈추는43조건을 실제 원작 CPU 실행으로 재현했다.
43조건은 rank229+256*k(k=0..42), 즉 전체11172 finished Hangul의 특정 하위 바이트 문제다.
이전 F9FC 문자열 copier의87음절 반례와 분모/표현이 다르므로 동일 수치로 합치지 않는다.

새 transfer는 native source02026281을 확인하고 marker 위치02026280으로 되돌린다.
새 형식을 명시적으로 선택한 조건에서 기존 cap10 record importer08F05000으로
22byte marker/count/words/padding/final terminator를 모두 검증한 뒤 전체22byte를 복사한다.
검증용 compact76은 stack에만 작성하며 persistent scratch RAM을 추가하지 않는다.
destination은 bounded pool slot0/1/2의 시작 주소만 허용하고 나머지는 무수정 거부한다.
이는 전체 pool allocator의 slot 수/수명/소유권 채택이 아니다.

원작 success-only suffix를 유지한 비교 코드는 helper가 실패해도 state24로 진행하는 반례1건을 재현했다.
coordinated finalizer는 성공이면 기존 state24/flag0, 실패면 기존 취소 state3C/flag1로 돌리고 substate를0으로 한다.
실패 후 stale pool 데이터를 확인 화면으로 넘기지 않는다. 별도 오류 설명 dialog는 추가하지 않았으며
실제 자연 입력/시각적 rejection UX를 검증한 것은 아니다.

### 검증 범위

전체11172 finished Hangul을 cap10 마지막 자리에서 검증하고 pool3슬롯으로 분산해 원작/새 caller를 비교했다.
길이1..10×3슬롯×4완성/native identity, record22byte 각각의 변조, 잘못된 slot/source/destination도 검사했다.
accepted11302/rejected27, whole EWRAM/source/staging/adjacent slot 보존22501조건 PASS.
17개의 실패 caller가 취소 분기로 진행하고, unguarded 실패 진행 반례1건을 유지했다.
각 호출은 r4..r11/SP/stack canary/CPU write intervals를 검사하며 ISA는 ARMv4T Thumb1의 verified assembler/disassembler다.
own96+import124=220byte는 helper fixture 한도이고 original caller PUSH4를 더한224byte가
이 success-window의 하한이다. game/IRQ 전체 budget 채택이 아니다.
코드 위치08306000/08306100은 source clone fixture이며 free ROM 증거가 없다.

### 저장·소비자 연결의 미완료 조건

이전 실제 preset 저장/재시작 관찰에서 calendar32byte record의 name offset10/field22가 확인됐다.
이번 candidate record22는 크기상 맞지만, 해당 필드에 새 형식을 저장하거나 실제 새 이름을 재로드한 증거는 아니다.
calendar success pool은 **문자열**이었으므로 새 binary record를 넣은 상태로 원작 소비자를 계속 사용할 수 없다.
정적 bounded source ranges에서 다음 작업 대상을 좁혔다:

- 08033334..33372: native record getter373A2의 record+10을 pool slot0/1/2로 rawE5 복사한다.
- 08033374..3338C 및08033864..33880: script 기반 기본 문자열을 pool에 쓴다. 새 레코드를 덮어쓸 수 있는 writer다.
- 08032F7C: pool0의 logical count/확인창 위치 계산. 현재 F9FC counter hook은 raw 문자열용으로 binary format용이 아니다.
- 08033C94..33CB6: record body를 pool0에 rawE5 복사하고 heading script48로 표시한다.
- 080373A2..373F8: flags/date/index로32byte-stride native record를 선택한다. 문자열 형식 판별은 없다.

이 범위는 선택된 consumer/writer의 관찰이며 전체 calendar/save census가 아니다.
32F7C counter는 기존 F9FC hook 때문에 원작/현재가 동일한 코드라고 취급하지 않는다.
나머지 위의 bounded native 범위는 이번 bench에서 source/current 동일성과 ISA roundtrip을 확인했다.
명시적 새 형식 선택/legacy migration, default/import/confirm/display/storage reader의 coordinated 처리,
풀/실제 저장 필드/IRQ 소유권, native save/reset/fresh-load, 한글 screenshot과 실제 ROM hook은 남았다.
release false 및 whole-memory NOT PASS를 유지하며 원본/playable/glyph-only ROM과 사용자 세이브를 보존한다.

이번 변경을 누적 foundation의 별도 calendar transfer CPU 증거로 연결했고 전체 재실행 PASS.
변경3도구 py_compile PASS. 원본/playable/glyph-only ROM의 SHA256은 기존값과 같으며 사용자 세이브에 쓰지 않았다.

## 2026-10-10 후속: 달력 이름 재표시·확인 count·픽셀 소비 CPU 연결

`hangul_calendar_display_shim.py`, `bench_calendar_record_display.py` 및
`cpu_calendar_record_display/{shim.bin,report.json}`를 추가했다.
기존 검증된 record→display decoder08F09000을 재사용한다. 별도의 레코드 decoder를 만들지 않았다.
glyph-only ROM의 원작 name renderer08033C94..33CB6에서 BL33C9A만 CPU clone의08307000 adapter로 바꾼다.
원작 상위08033C58..33C88은 record+10/row를 넘기는 별도 경로이며 이번 CPU 실행 범위 밖이다.
소스 field는 이전 관찰의0200131A를 fixture로 사용하며 source/current ROM/file hashes를 확인했다.

명시적으로 새 형식을 선택한 상태에서 record22를 검증하고 pool02026080에 최대41byte F9FC/native 문자열을 만든다.
성공하면 원작33C9E로 돌아가 script48/mono font08619EF8/row별stage0201C800+row*1024/
VRAM0600A000+row*1024를 요청한다. 이 heading/TPL-string-buffer 서비스는 모사하며 자동 lookup 증거가 아니다.
실패하면 original33CB6 POP으로 분기해 heading 자체를 호출하지 않고 이전 pool/saved-record/인접필드를 보존한다.
global rawE5 copier나 legacy format handler는 변경하지 않았다.

### 확인창 및 픽셀 연결

같은 CPU-produced pool을 HOST가 다시 쓰지 않은 상태에서 현재 ROM의 native32F7C logical counter를 실행했다.
기존 F9FC-aware counter hook이 음절 내부E5를 terminator로 오인하지 않으며 logical length와
sprite x=130-4*count/y20, descriptor count/고정 속성을 확인했다. sprite 제출 서비스는 모사다.
전체11172음절을 cap10 마지막 자리에서 처리했고 row0/1에 분산했다.
길이1..10×2행×4native/완성 identity,22byte 변조,empty/malformed 및 형식 충돌 반례를 포함해
detail_calls11277/accepted11263/rejected14/count11263/wholeEWRAM22624조건 PASS.
`detail_calls`는 report key 명칭이며 이 함수는 달력 이름을 출력하는 row helper다. 실제 상세화면 전체를 검증한 뜻이 아니다.

대표84조건에서는 heading 모사 후 원작 IWRAM fixed-cell parser03006824를 **별도로** 호출했다.
그 입력은 앞 단계 CPU가 만든 동일 pool 문자열이며 HOST 문자열 재기록이 없다.
실제 heading의 mono font/stage/target 인수를 사용해64byte×10cell=640byte를 생성하고
glyph-only ROM의 Hangul/native/blank glyph 바이트와 whole EWRAM(Expected Writes)로 비교했다.
08000850 transfer는 가로채며 queue/VRAM/scanout까지 이어지는 증거는 아니다.
따라서 heading 전체 실행/printStringBuffer provider lookup이나 actual screenshot을 주장하지 않는다.
source record22/header10/이웃field, buffer 이후 canary, callee registers/SP/stack 및 write interval도 검사했다.
native name caller20+adapter8+decoder80=108byte, counter36byte, 별도 parser40byte는 fixture 한도다.
actual game/IRQ budget이나 pool writer lifetime 채택이 아니다.

### 형식 선택과 다음 완료 조건

cap10 record `81 E5 00 FF ... FF E5`는 새 형식의 count1/rank229 record로 구조상 유효하다.
동시에 첫2byte `81 E5`는 원래 single-byte 일본어 문자열로 소비 가능한 prefix다.
선택된 새 decoder는 F9FC/rank229를 출력하지만 원래 raw string reader는81 한 글자로 읽는다.
이것은 crafted field fixture의 두 해석 반례이며 기존 실제 save에서 발견됐다는 주장은 아니다.
marker/전체 레코드의 구조 검증만으로도 자동 형식 소유권을 확정할 수 없으므로 새/legacy dispatch는 명시적으로 남겨 두었다.

이전 keyboard→pool transfer는 binary record를 썼지만, 이번 표시 helper는 **저장 field의 새 record를 별도로 읽어**
pool에 표시 문자열을 만든다. 둘을 연결된 자연스러운 저장/표시 세션이나 완성된 pool 아키텍처로 취급하지 않는다.
명시적 형식 선택 정보, canonical record와 display cache의 구분 및 pool/default/record writer 수명을
동시에 정리해야 calendar 확인/등록/재입력/목록/저장/재로드를 안전하게 연결할 수 있다.
actual record writer와 native save/reset/fresh-load, old-save migration, IRQ/queue/ROM placement,
자연 한글 입력과 실제 화면, release/whole-memory NOT PASS는 계속 미완료다.
실패 시 heading을 건너뛰는 처리는 pool을 잘못 읽지 않는다는 CPU 증거만 제공한다.
기존 화면 row의 clearing/오류 feedback은 미검증이므로 이를 완성된 invalid-record UX로 취급하지 않는다.

누적 foundation에 별도 calendar record display CPU 증거로 연결했으며 전체 재실행 PASS.
변경3도구 py_compile PASS. 원본/playable/glyph-only ROM SHA256은 기존값과 같고 사용자 세이브에는 쓰지 않았다.

## 2026-10-10 실제 달력 등록 writer의 위험 경로 재현

`tools/bench_calendar_native_registration.py` 및
`analysis/hangul_keyboard_v1/cpu_calendar_native_registration/report.json`.
기존 preset observer의37366은 이름 복사 함수가 아니라 record 등록 메타데이터 함수였다.
실제 이름 writer는32EFE..32F24 안의32F06→32AC6이며, source는pool02026080,
destination은context02014DD0+2C가 가리키는record+10이다. copier는첫E5 포함까지 복사하며
22byte 이름 필드/32byte record 경계나 F9FC token을 검사하지 않는다.
37366은record[0]=3,record[1]=metadata02000950[4] 후 counter를 증가시킨다.
등록 여부의 전역 flag/번호를 새 이름 형식 discriminator로 재사용하지 않는다.

원본 및 current ROM에서 해당 code3범위와literal3개가 같고 Thumb1 assemble/disassemble roundtrip을 검사했다.
원작 copy,metadata,state16까지 CPU 실행했으며 sound0534만모사했다.
모든11172음절을 cap10 repeated-rank 새binary22byte 및 F9FC display41byte로 각각 투입했다.
binary43음절은 lowbyteE5에서 잘림; display43도 동일한 조기 종료를 보였다.
display11129조건은 field22를 넘어 다음record19byte를 침범한다.
깨진 두 경우에도 원작은flag3/counter증가/state16/success sound128로 진행한다.
legacy3문자열×counter0/254/255의9대조군 및 wrap3도 검사했다.
22353CPU등록/whole EWRAM 비교 PASS; 이 PASS는 unsafe integration 반례 재현만 뜻한다.
모든neighbor변조는격리된CPU RAM이며 실제ROM/사용자save에는 쓰지 않았다.

따라서binarypool와displaypool을 같은무형식canonical로 연결하지 않는다.
이전transfer/display를 이어 붙이거나 F9FC41byte를 기존field22에 그대로 저장하는 방안은 거부한다.
표시cache와 구분되는 canonical수명, legacy/new 명시적선택, 원자적인 boundedcommit,
default/import/query/재입력 reader 연결을 다음 설계의 필수조건으로 유지한다.
새저장형식/공간채택/ROM설치/자연한글화면/save/reset/freshload는 미완료이며 release false.
foundation에 negative registration 별도항목을 추가했다. 변경2도구 py_compile PASS.

후속 정적 확인에서3355A도stage02026280+1→record+10 rawcopy 후3737A/37386 metadata를 사용한다.
이는 별도 writer이며 위22353조건의 실행 범위에 포함되지 않는다.
stage를 유일 canonical로 유지하는 대안도 이 다른 caller의 수명/형식 전환을 함께 조사해야 한다.
누적 foundation 전체 재실행 PASS. 원본/playable/glyph-only ROM 해시는 기존값과 일치한다.

## 2026-10-10 별도 canonical 이름으로 두 등록 경로를 bounded 연결

`tools/hangul_calendar_bounded_commit.py`, `tools/bench_calendar_bounded_commit.py`,
`analysis/hangul_keyboard_v1/cpu_calendar_bounded_commit/{copier.bin,pool_adapter.bin,direct_adapter.bin,report.json}`.
**선택된 NEW cap10 CPU session에만** stage02026280를22byte canonical로 취급한다.
decoder08F09000가 stage→pool02026080의별도41byte 표시문자열을 생성하고,
HOST원본/cache 재기록 없이 등록 adapter가 다시stage 원본에서 저장한다.
이 역할은 새로운 lifetime/legacy-dispatch 설계 후보이지 모든 real caller용 채택사항이 아니다.

공통copier08308000은context02014DD0+2C의record pointer와 field=record+10을 비교한다.
원작literal373FC의recordbase020011F0부터255stride32 범위/정렬도 검사한다.
importer08F05000으로전체22byte cap10 구조를 stack에서검증하고 성공한 경우22byte만복사한다.
marker/LEword payload의embeddedE5를 terminator로 해석하지 않는다.
own96+import124=220; adapter8포함228, native outer push4별도232 lower-bound fixture.

32F06은08308100 adapter로만 교체해 기존pool→rawcopy를canonicalcopy로 대체한다.
3354A..3355E는08308200 BL+NOP로 함께 교체한다. 원작의 복사 전success sound를
검증/복사 성공 후에 실행하며 original3355E metadata selection으로 복귀한다.
실패는r5 UIcontext의choice8=2/flag6=1 후 original32F1A 또는3359E reject path로 분기한다.
UI r5=0200F550와record-pointer context02014DD0는별도 fixture로 유지한다.
따라서 실패 시 metadata등록/counter증가 및success sound를 건너뛴다.
원작instruction 이동 없이 의미를 다시 생성했으며 source3범위/placedBL/전체generatedcode의Thumb1roundtrip을 검사했다.
CPU clone주소08308000..08308200은freeROM증거가 아니며 실제ROM에쓰지 않았다.

전체11172음절 cap10×pool/direct 경로22344,255arena슬롯,길이1~10/nativeE4payloadE5/변조/
잘못된pointer·정렬·범위/field/counterwrap를 포함한22745등록 조건,
display decode22703및wholeEWRAM45448검사PASS. 성공22703/실패42.
등록의37366/3737A/37386은원작실행, sound/selector/37440의등록후번호정리는모사다.
direct selector1/2만 실행하며selector0의RTC/config route는이검사의범위밖이다.
모든원본/cache/neighbor/header(non-target bytes) 보존을검사했다.

남은completion-critical조건: stage의real session수명/다른writer, 기본이름/import/query/재입력연결,
persisted legacy/new 구분정보,save/load소비자,직접selector0 및등록후번호정리,
IRQ/전송/ROMplacement와실제화면. 이검사는safe selected copy의CPU증거이지saveABI/전체자판완성이아니다.
원본/playable/save는미변경이며release false/whole-memory NOT PASS를 유지한다.
누적 foundation 전체 재실행 및 변경3도구 py_compile PASS. 원본/playable/glyph-only SHA256은 기존값과 일치한다.

## 2026-10-10 current ROM에서 실제 canonical 수명/변환 경계 관찰

`tools/capture_calendar_name_lifetime.py`, `tools/report_calendar_name_lifetime.py`,
`analysis/hangul_keyboard_v1/calendar_name_lifetime.json`.
current playable SHA5e7bee… 고정, `input-heading-v1-select-gutsman`의동일ROM checkpoint에서
normal controller로menu/time/meal/friend/editor/typed/friend-register/reenter8경로를실행했다.
경로별snapshot/screenshot/trace/observer환경 receipt와same-ROM ancestry12노드의artifact해시를검증했다.
ROM·RAM·script·progress·save주입이없으며원작키보드그대로관찰했다.
이는미설치Hangul CPU후보의runtime증거가아니다.

### 새로운 판별 증거

- menu/time/friend/editor에서stage02026280의22byte는이전비문자열자료그대로다.
  meal기본값‘식사’는ROM→pool02026080→record02001310+10이며stage read/write모두0이다.
  실제37366입구와등록후RAM field에서F9FC‘식사’+E5/zero padding을확인했다.
- 친구이름입력은30EAA caller의355B6호출r0=6,r1=0x26,r2=02026280,r3=1이다.
  cap10으로일반화하지않는다. originalstagewriter3500C/3501E/35026의write3개를실제로관찰했으므로
  observer가stage접근을잡는positive calibration이있다.
- 한문자를입력한stage는`01 9B E5 …`이며미사용후방bytes는그대로다.
  원작30EF4는stage+1→pool을복사하고,확인화면은archive6368E8 **script0x45(십진69)**의
  `AE E4 63 E4 69 E5`를pool+1에추가한다. 최종pool은`9B AE E4 63 E4 69 E5`.
  script0x44는십진68이다. 이전문서의‘script45/44’주소식표기는십육진으로읽어야하며
  Pythonscript_spans의십진45/44와혼동하면다른문구를선택한다.
- 실제32F06→32AC6→37366은suffix포함최종일정이름을저장한다. stage는사람이름만유지한다.
  ‘아니오’후재입력은355B6 r3=2및3558C(stage)로suffix없는사람이름을불러온다.
  사람입력canonical과최종일정canonical은서로다른의미이며같은내용으로취급할수없다.

### CPU 후보 적용 범위와 다음 구현 경계

이전boundedcommit의명시적NEW cap10 CPU계약은유효하지만이actual route에그대로설치할수없다.
default는stage초기화를건너뛰므로거부되거나stale자료를읽게되고,
cap6의새편집record는14byte이므로22byte로명시적정규화가필요하며,
stage에서prefix만저장하면기존의activity suffix와일정의의미가소실된다.
fulltitle로stage를덮으면No→재입력시사람이름baseline도망가진다.

다음설계는personstage를재입력원본으로보존하며,기본이름과person+activity를별도경계에서
finalcalendarrecord22로만들어야한다. stack상의검증된최종record에서boundedcommit하는대안도
비교한다(추가globalRAM을채택했다는뜻아님). default/script/sourcecap/recipe선택과
기존persistedlegacy/new구분은별개문제이므로record[9]의일정종류를새encodingversion으로오용하지않는다.
anniversary/direct3355A·다른default·등록후index정리/selector0·IRQ·save/load·formatversion은미완료다.

관찰/보고2도구py_compile와report실행PASS. 이번에는기존CPU코드를바꾸지않았으므로
foundation전체를재실행하지않고이runtime증거를별도책임으로유지했다.
실제한글자판screen/save/reset/freshload및release/whole-memory NOT PASS는계속미완료다.

## 최종 제목을 저장 경계에서 변환하는 CPU 후보 (2026-10-10)

추가 도구:

- `tools/hangul_calendar_title_record.py`
- `tools/bench_calendar_title_record.py`
- `analysis/hangul_keyboard_v1/cpu_calendar_title_record/report.json`

32F06의 기존 pool 문자열 복사 대신, 실제 최종 title을 명시적으로 NEW cap10 기록으로 변환한다.
기본 이름은 keyboard stage를 거치지 않아도 처리되며, 사람 이름+활동 문구는 전체 제목을 저장한다.
재입력용 person stage는 읽거나 덮어쓰지 않는다. 이 후보는 이전 stage-only 후보의 적용 범위 문제를
해결하기 위한 별도 대안이며, 직접3355A 경로나 기존 저장 형식 자동 판별에 적용한 것이 아니다.

converter ABI: r0=stream, r1=record, r2=inputAvailable(low16)|outputAvailable(high16), r3=cap1..10.
입력은1..41바이트, 출력은2*cap+2바이트, 선언된 양쪽 영역은 겹치면 거부한다.
00..E3→8000..80E3, E4+payload→8100..81FF, F9FC+LErank→0..11171만 허용한다.
E5는 토큰 경계에서만 종료하며 E4 payload나 Hangul rank의 E5는 문자 데이터로 보존한다.
빈 값/부분 자모/알 수 없는 command/초과 길이/잘린 토큰/주소 wrap은 외부 쓰기 전에 실패한다.
private stack44에서 완성 기록을 만들고, 성공할 때만 전체 fixed record를 복사한다.

commit은 실제 context02014DD0+2C와255개 stride32 arena, record+10 출력주소,
입력 pool02026080을 검사한다. converter 포함 stack60, adapter 포함68, 원작 caller push4 별도다.
성공하면 native32F0A→37366 등록 metadata를 실행한다. 실패는 기존 adapter를 통해
UI0200F550의 취소 상태를 설정하고 reject sound/종료로 분기해 성공 등록을 건너뛴다.
메타데이터와 UI를 같은 주소로 가정하지 않는다. sound만 모사했고 native 등록 코드는 실제 실행한다.

검증은 완성 title을 fixture로 공급한다. CPU가 기록한 bytes를 HOST가 다시 쓰지 않고
기존08F09000 CPU decoder로 읽어 원래 token stream과 비교한다. 전체 EWRAM 비교 및 쓰기 추적으로
person stage/pool/cache/이웃 record의 보존을 검사한다. actual lifetime 보고서의 ‘식사’/친구 title도 포함한다.

설치 전에 반드시 남은 연결:

- 원작3302C..33034의 raw E5 scanner와32AA8 suffix 복사. F9FC rank에 E5가 있으면 현재 scanner는
  토큰 중간을 suffix 위치로 오인한다. 이 후보는 **완성된 title 이후만** 검증하므로 append 안전성을 주장하지 않는다.
- 저장형식 version/명시적 dispatch와 기존 record 지원, 모든 default/anniversary/direct3355A/readers.
- 코드 공간 및 runtime/IRQ 소유권 채택, 실제 자판 화면·저장·reset·fresh-process reload.

원본/현재 playable ROM 및 사용자 세이브는 변경하지 않았다. 새 CPU 단계는 별도 실행했으며
기존 foundation 전체를 다시 실행하거나 이 결과를 자연 UI/저장 지원으로 승격하지 않았다.

이 단계 실행 PASS: converter334회 + 원작 등록22877회 =23211조건,
허용23107/거부104, 전체음절 제목22344, E4 payload256, CPU 재표시23107,
whole EWRAM 비교46318회. 변경2도구 py_compile PASS.

## 친구 이름+활동 문구와 확인창 호출부 연결 (2026-10-10)

도구 `hangul_calendar_activity.py`, `bench_calendar_activity.py`와
`cpu_calendar_activity/report.json`을 추가했다. 실제 current ROM의32AD8 archive literal과
halfword table[script0x45=69]에서 suffix 주소를 계산해 원문6바이트와 대조한다.
원문 문구의 번역/의미 변경은 하지 않았다. suffix 주소는 stale original archive에서 얻지 않는다.

대상 helper는 pool02026080만 받는다. cap6 person stream을 기존 converter로 검증하고
CPU decoder로 private stack stream을 만든다. 끝 위치는 raw E5 검색이 아닌 decoder의 반환 길이에서 얻는다.
suffix는 선언된 ROM extent만 임시 stream에 추가한다. 전체 title을 cap10 기록으로 변환한 뒤
다시 decoder로 읽고 반환 길이와 합친 길이의 일치를 요구한다. suffix 내부 E5 payload는 보존하며
조기 종료+trailing garbage, 잘린 토큰, unsupported rank, 총10글자 초과는 외부 쓰기 전에 거부한다.
허용할 때만 전체 title을 pool에 복사한다. person stage는 쓰지 않고 global RAM도 추가하지 않는다.
helper 자체88 + decoder80 =168 stack, 원작33014+adapter 포함196이다.

fixture의 coordinated writes:

- 3302A..3303C raw scanner+32AA8 복사 → bounded activity adapter.
- 33050..33054 → 명시적 성공값1+원작 frame pop. 원래pop와 alignment0000을 정확히 검사하며
  PC-relative literal은33054부터 그대로다. 이 padding 사용은 CPU fixture이며 실제 공간 채택이 아니다.
- 별도 failure tail은33014 저장 frame을 복원하고0을 반환한다.
- 32E22 호출부 → 결과를 검사하는 wrapper. 성공은32E26의 원작 확인창 초기화를 유지한다.
  실패는 UI의 error6/8을 유지하고 state word16을 설정한 뒤32E36 원작 caller pop으로 돌아간다.
  확인창32E60이나state4 설정으로 진행하지 않는다. caller+frame 전체stack208을 검사했다.
- 32F06은 직전 final-title bounded commit 후보를 사용한다.

caller CPU는32E22부터 시작하며 이전 system/config 단계32E10..20은 실행 범위가 아니다.
sprite29164/heading554A4/confirmation32E60/sound는 모사한다. 정상 흐름은
caller→suffix 추가→pool→native32EFE/37366→기록→CPU decoder까지 실행하며 중간에 HOST가
pool이나기록을 다시 쓰지 않는다. 전체 EWRAM 비교 및 쓰기 추적은 stage/cache/이웃 record를 보호한다.
다른 일정 종류0/2/3은 suffix를 추가하지 않는 원작 branch를 실행했다.
통제된 read-only ROM suffix fixture는 E4 payloadE5, Hangul rankE5, trailing bytes,
잘린 토큰/command/총글자 overflow의 허용·거부를 구별한다.

미완료: exit16 continuation의 실제 메뉴 복귀 및 정상 controller 경로, 모든 recipe/문구 번역,
직접3355A/anniversary/default/readers, persistent legacy/new version과 save/load,
code/RAM/IRQ 채택 및 실제 한글 자판 screenshot. 전체 foundation은 이번에 재실행하지 않았다.
ROM 적용·release·whole-memory PASS는 아니다. 원본/현재 playable/사용자 save는 미변경이다.

별도 CPU 실행 PASS:11454조건, 허용11440/거부14, 전체음절11172(embedded E5 ranks43),
원작 heading 경계11438, 실제 등록/CPU 재표시11440, whole EWRAM 비교34334, 다른 종류branch3.
변경2도구 py_compile PASS. ROM3종 SHA256은 기존 값과 일치한다.

## 실패 후 원작 종료·상위 메뉴 복귀 CPU 연결 (2026-10-10)

`bench_calendar_activity.py`를 확장했다. 제목 거부 후 원작 dispatcher32DD6가
UI0200F550의 state16을 읽어32F2C를 호출한다. 24프레임 종료 애니메이션 후 state20이 되고,
다음 프레임32F74가 UI[8]=2를[7]로 옮겨 native dispatcher가 취소2를 반환한다.
확인창을 초기화하지 않은 실패 entry의 UI[4]/[5]=0도 원작 속도 증가가 있으므로 정지하지 않는다.
이를 다른 종료 초기화로 대체하지 않고 원작 코드를 그대로 실행했다.

상위 caller30E82는32DD6 반환의 실제 TST/BEQ flags를 소비한다. 취소2이면 원작35C84가
selector8을 읽는다. 이 getter도 모사하지 않고 literal35CA0가 가리키는 RAM을 읽게 했다.
selector가 nonzero인 친구 입력은 parent context02014DD0의 subtype[1]=28, reentry[10]=1,
진행[2..3]=0으로 돌아간다. selector0 대조 경로는 subtype20으로 돌아간다.
UI와 parent context를 서로 다른 주소로 유지하며 record pointer+44는 보존한다.
따라서 성공 등록이나 확인창 진행이 아니라 실제 상위 edit/selection 분기까지 CPU 증거가 이어진다.
기존 actual lifetime 관찰의 No→cap6 재입력 경로와 일치하지만 새 한글 화면의 자연 실행 증거는 아니다.

caller→거부→상위 frame 반복 사이에 HOST가 UI/pool/stage를 다시 쓰지 않는다.
매 프레임 전체 EWRAM을 비교하여 parent/UI의 선언된 변화 이외에는 기록·입력 원본·pool·이웃을 보존한다.
close-script9의 선택과 native dispatch table/ROM pointers를 확인한다. 스크립트 실행4F7B6과
그리기32FD4는 모사하므로 실제 창 닫힘/픽셀/IRQ/최상위 메뉴 제어의 증거로 확장하지 않는다.

state table pointer32DF0는table32DF4를 가리킨다. state16/20은 각각32E04/32E08의32F2D/32F75다.
close-script literal32338은 원본 archive6368E8에서 현재 archive로 의도적으로 relocation된 값이다.
원본 동일성 요구 대신32AD8의 activity archive와 source/current 양쪽에서 일치하는지 검사한다.
이 literal 차이는 defect나 새 save version이 아니다.

저장 형식 미해결 경계: 새 내부 marker81..8A는 유효한 옛 단일 글자 범위와 겹친다.
81 E5 prefix 반례는 그대로이며, 일정 종류record[9]나 임시 selector8도 encoding version이 아니다.
다음 단계는 모든 name writer/readers를 포함한 명시적 저장 version/변환 정책을 확정하고 연결하는 것이다.
이 CPU 결과 때문에 옛 저장을 자동 이진 decode하거나 save 영역에 추정 version을 기록하지 않는다.
ROM/세이브는 미변경이며 누적 foundation 전체는 이번에 재실행하지 않았다.

현재 별도 실행 PASS: 전체11455조건(허용11440/거부15), 전체11172음절,
등록/CPU재표시11440, whole EWRAM34560회, 취소frame225/return9,
상위 재입력8/선택1. 변경1도구 py_compile 및 보고서/tool/artifact/dependency hash 확인 PASS.

## 조건부 저장 version 경계 CPU 후보 (2026-10-10)

`tools/hangul_calendar_versioned_record.py`, `tools/bench_calendar_versioned_record.py`,
`analysis/hangul_keyboard_v1/cpu_calendar_versioned_record/report.json`을 추가했다.
이 후보는 내부 편집/confirmed record의 count marker를 변경하지 않는다.
별도 저장 경계에서 F8(version byte)+10 LE identity words+E5로22바이트를 만든다.
occupied words는0..11171/8000..80E3/8100..81FF, 나머지FFFF이며 count는 첫FFFF 이전의 연속 길이로 얻는다.
기존 strict record decoder가 값·padding·terminator를 검증하므로 빈/부분 자모/빈칸 뒤 nonempty는 거부한다.
10글자와22바이트 필드/record header10은 유지하며 record[9]나 임시 selector를 version으로 쓰지 않는다.

조건부 legacy grammar는 field22 안의 nonempty 최대10 logical cells:
00..E3 단일 글자, E4+임의 payload, F9FC+complete Hangul rank, 토큰 경계E5 끝이다.
이 domain의 첫 바이트는 F8일 수 없으므로 표식과 분리된다. 하지만 모든 실제 native/default/import writer가
이 domain을 지킨다는 전체 증거는 아직 없다. 따라서 **조건부 primitive 후보**이며 저장 ABI 채택/전체 옛 세이브 호환성 PASS가 아니다.
첫F8이 구조적으로 잘못되면 legacy fallback을 하지 않는다. 다른 첫 바이트는 legacy grammar로만 읽으며,
이전 내부81 E5... binary candidate를 persisted NEW로 오인하지 않는다.

writer ABI: r0=stream, r1=record, r2=inputAvailable(low16)|outputAvailable(high16), r3=10.
1..41 입력/22 출력, 영역 overlap/wrap/작은 출력은 외부 쓰기 전에 거부한다.
private24에 기존 converter가 완성 기록을 만들고, 성공한 결과만 표식을 바꿔22바이트 복사한다.
stack44+converter44=88이다.
reader ABI는 같으며 source22를 소비한다. old stream은 private record로 변환하고,
F8 record는 private 복사 후 count를 복원한다. 두 경로 모두 strict CPU decoder를 거쳐 외부 display stream으로 나간다.
reader stack44+decoder80=124이다. 전체 source/output disjoint 검사와 no-write failure를 확인한다.

CPU writer→reader 사이 HOST가 기록을 다시 쓰지 않고 전체11172음절의10글자 기록을 왕복한다.
16bit identity65536값 전부, native 한 글자228/E4 payload256, legacy F9FC11172,
count1..10의81..8A+E5 collision pair, marker/word/padding/terminator 변형 및 영역 오류를 검사한다.
실제 이전 runtime의 ‘식사’/친구 제목 field22도 legacy로 읽고 source를 보존한다.

새로 확인한 설치 위험: TextPet plugin의 F8 00..03은 storeTimer/storeGlobal8/16/32 명령이다.
F8은 게임 전체에서 unused byte가 아니다. 이 후보는 raw title의 제한된 domain에서만 구분하며,
원작 script/display 소비자에 새 저장 bytes를 직접 넘겨도 안전하다는 뜻이 아니다.
모든 reader/provider에서 반드시 version-aware 변환을 거쳐야 하고, 기존 raw copy/normalize의 전역 치환은 하지 않는다.
6368E8 script61/64..67은 printStringBuffer 명령을 포함한 표시 template이므로 raw committed name으로 혼동하지 않는다.
script69의 원문은 `と約束`이다. 이번 작업은 이 suffix의 번역/의미 변경이 아니며 현재 후보는 같은 bytes를 보존한다.

남은 완료 조건: 전체 실제 writer/default/import grammar와 F8 reservation 검증,
native versioned commit/조회/list/provider 연결, 다른 입력 필드의 cap/width 정책,
code/IRQ/RAM 채택, 실제 자판 화면 및 save/reset/freshload. current ROM/원본/사용자 세이브는 미변경이다.
새 helper 단계만 별도 검증했으며 누적 foundation 전체는 이번에 재실행하지 않았다.

별도 CPU 실행 PASS: writer11172, reader88476(허용34509/거부53967),
65536 identity domain, 전체음절11172왕복, E4 payload256, collision pair10,
whole EWRAM99656회 및 별도 bounds reject8. 변경2도구 py_compile,
report/tool/artifact/dependency hash 확인 PASS. ROM3종 SHA256 불변.

## 2026-10-11: 조건부 version 저장의 native 등록·상세 연결 (CPU 전용)

`tools/bench_calendar_versioned_native.py`와 `cpu_calendar_versioned_native/report.json`을 추가했다.
이 절은 앞 절의 native versioned commit/상세 연결 미완료 상태를 해당 두 경로에 한해 갱신한다.
원작32F06의 raw copy를 CPU clone에서만 adapter08308100→commit08308000→writer0830D000으로 대체한다.
32EFE 및37366이 실제22바이트 F8 필드와 등록 metadata를 작성한 뒤,
같은 record+10을33C94→shim08307000→reader0830D200에 전달한다.
성공 출력 pool을 HOST가 다시 쓰지 않고 현재 원작F9FC counter32F7C가 읽는다.
기존 converter309000과 decoderF09000을 사용하며, 재입력 person stage와 주변 RAM을 보존한다.

등록11695조건: 성공11685/거부10. 상세11693회: 거부3, 글자 수11690회.
전체음절11172, E4 payload256, arena255주소, 기본식사/친구제목을 포함한다.
기존 문자열4개는 별도 상세 경로 대조이며81 E5는 legacy 글자81로 읽힌다.
F8 malformed3개는 heading을 호출하지 않는다. 변형 중 추가 occupied word가 있는1개는 정상 구조로 허용한다.
whole EWRAM35078회 비교, register/detail/count의 callee-saved 및 SP/stack guard PASS.
최대 stack: 등록112바이트(+원작 caller LR4), 상세152, counter36.
생성3범위의 assemble_verified 결과와 원작3범위 ISA roundtrip, 두 BL expected bytes/final placement를 기록한다.
변경1도구 py_compile PASS, 원본/플레이용/글리프 ROM SHA256 모두 불변.

한계: sound/heading/sprite는 모사다. 이번에는 pixels/VRAM/스크린샷을 실행하지 않았다.
제목은 fixture 공급이며 activity append/input과 한 경로로 연결하지 않았다.
다른 direct/default/import writer, prefill/list/provider와 전체 F8 reservation은 계속 미완료다.
F8 format 및 ROM hook은 미채택이며 사용자 세이브는 수정하지 않았다.
`create-kr-patch`의 소비자 연결·실패 원자성 기준으로 CPU 검증과 실제 ROM/save 검증을 구분했다.
누적 foundation은 재실행하지 않았으며 whole-memory/release NOT PASS를 유지한다.
다음: activity→version writer→native 상세를 연결하고 prefill/list readers를 추적한 뒤 설치 가능성을 판단한다.

### 2026-10-11 추가: activity→version 등록→native 상세/글자 수 연결

같은 `bench_calendar_versioned_native.py`를 확장하고 동일 보고서를 재생성했다. 위 직전 수치는 이전 실행의 기록이다.
`cpu_calendar_activity`의 해시 검증된 code/fixture write specification을 사용하며 이전32F06 writer만 versioned writer로 대체한다.
활동 hook의 expected source 및 기존 hook과의 겹침을 검사하고, 원작32E22/33014가 suffix를 조합한다.
이때 작성된 pool과 record를 HOST가 다시 쓰지 않고32EFE/37366→33C94→32F7C로 전달한다.
초기 완성 person pool 및 별도 재입력 stage는 HOST fixture이며 실제 키 입력이 아니다. stage의 보존만 입증한다.
활동11441조건(성공11435/거부6): 전체11172음절6글자 이름, 길이1..6, E4 payload256, native9B,
빈 값/잘린E4/F9/지원밖rank/7글자/command 거부를 포함한다. 실패시 확인창 heading과 initializer를 호출하지 않는다.
기존 등록/legacy/잘못된기록 대조도 재실행했다. 등록23130회(성공23120/거부10), 상세23128회(거부3), 글자 수23125회.
whole EWRAM80824회 비교 PASS; activity caller208·등록112(+outer4)·상세152·counter36 stack guard 및 ABI PASS.
변경1도구 py_compile PASS. source/playable/glyph ROM3종 SHA256 불변. 사용자 세이브는 미변경이다.
누적 foundation 전체 재실행 및 pixels/VRAM/화면/save/reset/freshload는 이번 범위가 아니다.
`create-kr-patch`의 경로 연결/실패 원자성 기준을 적용했으며 F8 및 code/RAM/IRQ 배치는 여전히 미채택이다.

다음 읽기 경계의 정적 조사:33334는 getter로 첫 기록을 받아 pool slot0에 복사하고33374를 호출한다.
33374는 script44(hex68)를 slot1/2에 기본 문구로 넣는다. 이후3334C/3335E getter가 있으면 각 slot1/2를 기록으로 대체한다.
따라서33374가 첫 기록 slot0을 덮는 것은 아니다. 세 raw copy BL33344/3335A/3336E 및 getter NULL flag/기본 슬롯을 함께 보존해야 한다.
이는 디스어셈블 조사이며 prefill/list의 CPU 연결·전체 reader population 입증은 아직 아니다.
다음: 이 prefill 경계를 version-aware reader와 연결하고 실제 입력부터의 경로·전체 저장 소비자를 검증한다.

## 2026-10-12: 남은 히라가나·가타카나 배열의 한글 자판 대체 후보

사용자 요청: 일본어 자판 배열도 작업. 기존 사용자 선택인 자동 한글 조합을 유지한다.
`tools/prepare_keyboard_kana_replacement.py`가 `6368E8:2:0` 및 `6368E8:3:0`을
일반 문구가 아닌 구조 대상에 연결한다. 원본 ROM revision, catalog의 source 문자열/TPL SHA256,
기존40자모 좌표/폰트·페이지 graphics 보고서의 도구와 모든 자산을 검증한다.
원본 배열은 각각85문자이며90칸 selector와 동일한 인덱스표라고 취급하지 않는다.
두 kana 페이지를 같은 기존40자모/50비활성 layout에 연결하는 **개발 후보**다.
최종 배열 승인, 두벌식 PC 자판 배치 승인, 일본어 입력 지원 삭제 승인은 주장하지 않는다.
Latin/symbol page2는 유지할 대상이며 현재 입력 연결은 아직 미구현이다.

권위 후보: `hangul_keyboard_v1/kana_replacement/report.json` 및 같은 폴더의
`selectors.bin`, `shim.bin`, `page0_tiles.bin/map.bin`, `page1_tiles.bin/map.bin`.
각 페이지 grid 영역 x16..190/y56..151만 교체했고, 바깥21,600pixel은 해당 원본 페이지와 동일하다.
각 bank5,472bytes, map1,200bytes이며 palette9/32byte CpuFastSet 정렬/VRAM B000 이전 범위,
원본·후보 pixel roundtrip을 검사했다. preview는 과거 관찰 palette를 이용한 offline 복원이다.
오른쪽 일본어 command/tab labels는 보호하여 아직 미번역으로 남는다. 실제 게임 화면은 아니다.

`tools/bench_keyboard_kana_replacement.py`는 기존 action shim을 변경하지 않고 별도 후보를
조립한다. 페이지0뿐 아니라1에서 자모 selector를 처리하고, page2 및 잘못된 page는 자모로
해석하지 않는다. 원작034F08 BL/BNE와 emitted dispatch/keyedit/rebase를 CPU 실행한다.
초기 editor/UI와 page/row/column/key-state는 HOST fixture다. 음절의 키 입력 사이에는
compact 조합 상태를 HOST에서 재작성하지 않는다. 실제 page toggle/controller는 이 검사에 포함하지 않는다.

첫 실행 PASS: 232,071호출 / accepted228,782 / rejected-consumed1,753 / unhandled1,536.
각 페이지에서11,172음절(합22,344경로), 두 페이지를 오가며11,172음절을 만들고,
각 경로를 A+B로 key-history 역순 삭제하여 빈 상태로 복귀했다.
모든3페이지×16column×6row를 빈/부분조합/기존mixed기록 상태에서 검사했다.
두 한글 페이지 각각의1,024key-mask, invalid coordinate/page와 UI cap mismatch27조건도 포함한다.
전체 EWRAM Expected Writes 및 r4..r11/SP/208byte stack guard와 native handled branch를 대조했다.
최종 source/catalog 보호 검사 강화 이후 재실행 결과와 해시 검증은 아래 추가 기록으로 결속한다.

기존 후보/파이프라인의 도구와 reports는 변경하지 않았다. 누적 foundation 및 전체465번역 tests는
이번 범위에서 재실행하지 않았다. 새 py_compile과 후보 재생성/CPU검사가 이번 증거다.
번역 draft coverage는27,450과 구조 미해결2를 유지한다. 새 결과를 근거로 미해결을0으로 내리지 않는다.

다음 통합 조건: page1에도 native navigation skip-table6/8(row2) 처리가 필요하다.
기존 `hangul_keyboard_frame_adapters.py`는 page0에만 이 우회를 적용한다.
또한 두 페이지 graphics lookup/upload/draw/refresh 경로, command labels와 Latin/symbol 입력,
완성 레코드의 전체 prefill/list/provider/save/reset/fresh-load·legacy 호환을 연결해야 한다.
fixture code/RAM/table 주소는 채택된 빈 공간이 아니며 IRQ·stack·lifetime 승인도 없다.
이 조건 때문에 원본/기존 개발 ROM 및 사용자 save는 변경하지 않았다.
`create-kr-patch`의 active/inactive selector, protected pixels, 입력→저장 전체 경로와
CPU/실제 화면 증거 구분 원칙을 적용했다.

최종 검증: source/catalog 보호 검사를 강화한 최종 코드에서도232,071호출과 위 모든 경로/수치 PASS.
새2도구 py_compile PASS, 현재 tools/artifacts/CPU dependencies SHA256 일치 PASS.
후보 재생성의 report/bin/png 전체 byte identity PASS. 원본 및 기존 개발ROM4종 SHA256 불변 PASS.
후보 report SHA256: `efd4f4e2ad4067b3c9c5e1cca21d04042f01e5c0ba6950ff9509741cfd67e15b`.
CPU report SHA256: `ccd08e780c6b75df277924731c48405752e27d8a22cec72669efba4b35db9bba`.
translation-first coverage 재생성 PASS: catalog31,907 / authored27,450 / structural pending2 /
draft_complete=false / rom_integration_started=false. 과거 remaining515 reconciliation은 당시 snapshot으로 유지한다.

## 2026-10-12 후속: 두 페이지 native 커서·입력·그림 전송 경로

`tools/hangul_keyboard_kana_frame.py`가 기존 frame/caret adapters를 재사용하고
navigation adapter만 두 한글 페이지(0/1)에 적용한다. page2는 native navigation을 유지한다.
`tools/bench_keyboard_page_input_pipeline.py --editfield --frame --kana`를 추가했다.
기존 세 mode는 유지하고 새 mode의 권위 결과는 `hangul_keyboard_v1/cpu_kana_frame/report.json`이다.
원본/기존 glyph ROM의 명령 영역을 hash/Thumb-1 roundtrip 검증하고 fixture clone에만
10곳의 expected/final bytes를 결속했다. page0 후보는 기존 페이지0 bank/map과 byte 동일,
page1은 별도 bank/map과 native lookup/transfer descriptor로 공급한다.

CPU 원작034E34 state12 frame→raw control/action→페이지 upload/draw→editing refresh→
queue drain→VRAM 소비까지 연결했다. 최초 editor/UI와 key pressed/repeat는 fixture다.
선택 루트에서는 이후 HOST가 cursor/compact/queue/map/bank를 재작성하지 않는다.
원작 skip table은 ㅕ/ㅗ를 제외하는 반례를 유지했고 새 adapter로 양쪽 페이지에서 도달 가능해졌다.
page0의40칸 선택 후 R로 page1에 넘어가40칸을 방향키와 A/B로 검사했다.
별도 경로는 ㄱ→ㅗ→ㅏ→ㄹ→ㄱ 입력마다 R/L로 페이지를 오가며 복합 모음/받침을 조합하고
5회의 B로 원래 complete 상태에 복귀했다. 매 단계의 canonical 상태와 glyph pixels를 대조했다.

새 mode PASS: input/native frames2,367, page transitions488, navigation cases1,565,
physical selector paths80, physical navigation moves125, cross-page jamo keys5.
draw/refresh2,624, drains2,485, queued refresh2,485/deferred139/latest-after-drain2.
queue rejection37, pending transitions101, unguarded full-queue mismatch 반례1 재현.
95 queue 슬롯×12 interval edge 조건1,140 및 malformed editor refresh7조건 거부도 유지했다.
whole EWRAM Expected Writes·VRAM 소비·r4..r11/SP 및 frame248byte guard PASS.
BIOS transfer/sprite/sound/config는 모사한다. scanout/VBlank/IRQ/실제 화면 검증이 아니다.

새 연속 삭제 경로의 첫 두 검사는 40,000 instruction cap에서 native tile draw034CB0에
멈춰 ABI/stack 검사 전 실패했다. 이를 실제 게임 코드 결함으로 분류하지 않았다.
도구는 return 미도달과 ABI/stack 실패를 구분하도록 수정하고 instruction 수를 기록한다.
100,000 cap에서 최종복귀/전체 Expected Writes/guard를 확인했고 state12 frame 최대40,679명령이었다.
이 수치는 이번 fixture population의 CPU 명령 수이며 hardware cycles, BIOS 비용 또는
실게임 worst-case frame/audio/IRQ 성능 증거가 아니다. 게임용 helper 명령은 이 사유로 바꾸지 않았다.

기존 page-only·editing render·single-page frame mode도 최종 도구로 재검사한다.
누적 foundation 및 전체 번역 tests는 이번 범위가 아니며 과거 결과를 현재 통합 증거로 승격하지 않는다.
원본/기존 개발 ROM 및 사용자 save는 미변경이다. 일반 초안27,450/구조 미해결2도 유지한다.
남은 조건: 일본어 command labels, page2 Latin/symbol 실제 입력, state12 밖의 init/confirm/exit/reentry,
전체 기록 reader/prefill/list/providers·save/reset/fresh-load/legacy 호환, 실제 code/RAM/IRQ 배치와 화면 검증.
`create-kr-patch`의 runtime asset 연결·입력 상태·실제 ROM/CPU fixture 증거 구분 원칙을 적용했다.

최종 검증: 기존 세 mode623/666/2,213 input calls와 새 두-page frame2,367 calls 모두 PASS.
최종 도구·자산·dependency 해시4개 report 일치, source/개발ROM4종 SHA256 불변 PASS.
새 frame report SHA256: `27f10445a5a6eb0416ca122fc092c4a68e934c25462106b92a70f43c707b9ed2`.
기존 single-page frame report SHA256: `93a8deacc574016917aeaa3d77a72a780a2ecff1fa9ad795a8ab0ead973c98bf`.
translation-first coverage 재생성 PASS: authored27,450 / 미선택 일본어2 / ROM integration=false.

## 2026-10-12 후속: 기능 버튼18개 한글화·공백 입력 연결

`tools/prepare_keyboard_labels.py`가 별도 `hangul_keyboard_v1/keyboard_labels` 후보를 만든다.
기존 kana 후보/원본 page2를 hash 검증하고 동일 BDF Galmuri11-Condensed v2.40.4의 원본·license
SHA256을 검증한 뒤 unscaled8x16 glyph를 사용한다. 새 글자 획이나 fallback을 만들지 않는다.
세 페이지의6개 버튼, 총18개 표시 variant는 한글1/한글2·영숫자·오른쪽·왼쪽·공백·확인이다.
첫 두 버튼은 실제 toggle01/toggle12 목적 페이지에 맞춰 page별로 다른 표기를 사용한다.
현재 두 한글 페이지의 동일 자모 배치는 개발 후보이며 최종 배열/label wording 승인으로 간주하지 않는다.

편집 범위 x196..223/y56..151(28×96)을 각 페이지에서 사전 선언했다.
원본 영역은 ink11/shadow8/background5/9이며 모든 background 좌표의 주기 패턴을 검사했다.
원문 stroke를 배경으로 되돌리고 ink11/shadow8로 한글을 재현한다. 나머지35,712pixel은
각 guarded 입력 페이지와 동일하다. 기존 자모/Latin/symbol 글자판과 경계 장식 AA/FF/CC/0도 보존한다.
각 bank5,312/5,280/6,976bytes, map1,200bytes; byte32 정렬·fixture tile/map 비겹침·VRAM B000 이전 범위,
원본/후보 decoded pixel roundtrip PASS. 후보 preview는 관찰 palette로 offline 생성한 것이며 실제 화면이 아니다.

원본 TextPet table의00=space 및 native big-font glyph0의 blank0x11×64를 검증했다.
별도 emitted action shim에서 col15/row4 A를 native canonical identity8000으로 연결했다.
이 값은 jamo selector0(ㄱ)와 다르다. 기존 dispatch/rebase가 native00 overwrite/append를 수행한다.
page0/1/2 모두 space 버튼은 활성이고 page2의 Latin/symbol grid selection은 여전히 미구현이다.
미완성 초성을 공백으로 조용히 버리거나 완성 음절로 바꾸지 않는다.

실행: `python -X utf8 tools/bench_keyboard_page_input_pipeline.py --editfield --frame --kana --labels`.
새 권위 결과 `hangul_keyboard_v1/cpu_keyboard_labels/report.json`.
CPU native state12 frame/control/action→새 3페이지 lookup/upload/draw→edit-field refresh/drain→VRAM을 실행했다.
input/native frames3,231, page transitions488, physical selector paths80, direction moves125,
cross-page composite jamo keys5. draw/refresh4,352, drains/queued4,213, deferred139/latest-after-drain2.
space boundary855조건: cap1..10, length0..cap, cursor0..length ×3pages의 모든 append/overwrite/full-end rejection.
조합 상태9조건: ㄱ/ㄱㅏ/ㄱㅗㅏㄹㄱ ×3pages에서 공백 뒤 compact 상태가 reference와 동일하다.
space actions864. sealed partial 초성의 reference candidate() 거부도 확인했다.
이 마지막 검사는 HOST reference 확정 가능성 검사이며 실제 native confirmation/save 경로 실행은 아니다.
whole EWRAM Expected Writes·VRAM pixels·r4..r11/SP/frame248byte guard PASS.
queue overflow/interval guard와 unguarded mismatch 반례도 유지했다. BIOS/sound/sprite/config는 모사한다.

기존4개 mode도 최종 도구로 다시 실행했다: page-only623/editfield666/single-page frame2,213/two-page frame2,367 calls PASS.
누적 foundation/전체465번역 tests는 이번 범위에서 재실행하지 않았다.
release/ROM-integration=false; 원본/개발 ROM/사용자 save는 미변경이다.
일반 초안27,450/구조 미해결2의 상태는 유지한다. 표기와 실제 버튼 기능을 함께 묶되
실제 확인창·저장·fresh-load를 미검증 상태로 유지하는 `create-kr-patch` 원칙을 적용했다.

다음: page2 native Latin/symbol/빈칸 selector 연결, 실제 confirm/exit/reentry lifecycle,
prefill/list/전체 saved-record providers와 F8 legacy 구별 및 save/reset/fresh-load,
채택된 code/RAM/IRQ placement 이후 누적 ROM과 실제 화면·사람의 가독성 검토.

최종 감사: 새2도구 py_compile PASS. label 후보 report/bin/png 전체 재생성 byte identity PASS.
builder 및5개 CPU mode의 현재 tools/artifacts/dependencies 해시 일치 PASS.
원본/개발 ROM4종 SHA256 불변 PASS, translation-first coverage 재생성 PASS(27,450초안/구조미해결2).
labels report SHA256: `a39ae9616b9e38702b70b06a2b4e6b2daffcd4b74bcf80f173aa72d740b33efe`.
CPU labels report SHA256: `cd0005fa00e51c386c31c72415c23030280dc9cbc999bb2bd43f225d04ca1404`.
state12 최대40,679 CPU 명령은 검사 fixture 내 수치이며 실게임 frame/cycle/IRQ 성능 보장이 아니다.

## 2026-10-12 후속: 영문·숫자·기호 실제 선택 경로 CPU 연결

`tools/prepare_keyboard_latin_input.py`가 `hangul_keyboard_v1/latin_input` 후보를 만든다.
immutable 원본의 selector literal35748/table6368E8/script4를 직접 읽고 기존75token/region hash와
대조한다. native354A0..354C8의 row×15+column 및 E4 가변 폭 seek 코드를75개 좌표에서 실행해
각 token 시작 주소와 EWRAM 무변경을 검증했다. 페이지6×15칸과 원본75token은 다른 분모다.
원본00 placeholder19개 및 표 밖 row5의15개를 합쳐34칸은 FFFF inactive로 명시했다.
나머지56칸은 대문자26/숫자10/원본기호20이다. 두 byte 기호 ♯/$/¥의 실제 token은 각각
E457/E459/E45F이며 중점은 원본・를 보존한다. 소문자 확대나 기호 치환은 하지 않았다.
native page2 skip data3514C의 독립 graph는 active56칸 모두 도달하고 inactive34칸은 도달하지 않는다.

별도 emitted action shim은 page2에 한해 bounded90×u16 selector09301100을 읽는다.
단일 byte는 canonical8000+value, E4 payload는8100+payload로 기존 native rebase에 전달한다.
기존 자모 page0/1, B 우선순위, caret/공백 command는 보존한다.
표 밖·blank는 consumed/no-edit이며 dedicated 공백 버튼은 모든 페이지에서 사용 가능하다.
ISA ARMv4T Thumb1 최종 배치 assemble/disassemble roundtrip PASS. candidate shim/code160bytes,
literal pool24bytes, selector180bytes는 fixture 주소이며 실제 ROM free space 채택이 아니다.

실행: `python -X utf8 tools/bench_keyboard_page_input_pipeline.py --editfield --frame --kana --labels --latin`.
새 `cpu_latin_input/report.json`은 native state12 frame/input→새 selector→mixed edit→native glyph/map
refresh→queue/drain→VRAM의5,389 input/frame 호출을 검증했다. initial UI/keys/queue drain은 fixture다.
모든90칸×empty/overwrite/full-end/complete-Hangul의360조건, single-letter5E/digit02/two-byteE457에
cap1..10×length0..cap×cursor0..length의855조건, active56×초성ㄱ/복합ㄱㅗㅏㄹㄱ의112조건 PASS.
56칸 모두 한 연속 방향키/A/B 경로로 선택하고 canonical B 및 한글 page왕복을 검증했다.
이 경로는 HOST editor/grid 재작성 없이 native keys로495번 이동한다. 기존 자모80칸 경로도 유지한다.
native 입력은 undo history를 rebase하므로 canonical B를 reference와 비교했으며 이전 조합 history
전체 복원이라고 주장하지 않는다. 초성의 candidate() 확정 거부는 HOST model 검사이지 native확인창
실행 증거가 아니다. 첫 확인·전체 commit/display·save/fresh-load는 여전히 별도 통합 조건이다.

input5,389 / transitions600 / draws·refresh7,838 / drains·queued7,699 / deferred139 / latest-after-drain2.
Latin actions1,256, space actions864, jamo216, B212, queue rejection37, unguarded mismatch1.
whole EWRAM Expected Writes·VRAM pixels·register/SP/frame248byte guard PASS.
기존5개 mode623/666/2,213/2,367/3,231 호출도 최종 도구로 재실행 PASS.
Latin 후보 report/shim/selectors 재생성 byte identity 및 두 도구 py_compile PASS.
누적 foundation/전체465번역 tests는 이번 범위에서 재실행하지 않았다.

원본 및 개발ROM3종 SHA256 불변, 사용자 save 미변경. 일반 초안27,450/구조 미해결2 유지.
`create-kr-patch`의 selector·표시·입력 identity 연결과 CPU/ROM/runtime/persistence 구분 원칙을 적용했다.
다음 어려운 완료 조건은 새 keyboard와 기존 versioned-record 후보를 잇는 실제 확정/초기값·prefill/list/
전체 저장 소비자·legacy 호환 및 save/reset/fresh-load이다. init/confirm/exit/reentry와 code/RAM/IRQ
배치가 함께 성립한 후 cumulative ROM을 생성하고 실제 화면/사용자 가독성 검토를 진행한다.

최종 감사: builder2종 및 CPU6mode의 현재 tools/artifacts/dependencies 해시 일치 PASS.
translation-first coverage 재생성 PASS(27,450초안/구조미해결2/ROM integration=false).
Latin selector 후보 SHA256: `234b7aaba0c6926eff530f2fc8c8358ff0c9dd71a8a7dff7369a74635468ebc5`.
CPU Latin report SHA256: `1b5b7dc2aeeef4f8f1ec92c06cdb95b473a5cf3c46fd7c0cd909866ee4ad6b2e`.
최대40,679명령은 fixture 내부의 실행 한도 관찰이며 실제 hardware frame/cycle/IRQ 성능 증거가 아니다.

## 2026-10-12 ROM 적용 요청의 통합 사전 검사

전체 사전 검사와 실제 기존 기준 ROM coldboot 결과는
`TRANSLATION_FIRST_HANDOFF.md`의 전체 ROM 통합 사전 검사 절을 따른다.
원본 writer 직접 F9FC 저장 반례 재실행 PASS(87음절 잘림/네 글자8byte 초과).
조건부 versioned-record 후보는 아직 전체 소비자에 채택되지 않았다.
새 자동 조합 자판 ROM은 생성/적용하지 않았으며 기존 기준 ROM 메뉴 테스트를
자판 화면·확정·저장 테스트로 간주하지 않는다. 전체 저장 지원 통합과 저장을 막은
입력 시험 전용 ROM은 서로 다른 범위이며 후자는 사용자 선택 전 만들지 않는다.

## 2026-10-12: 저장 지원 통합 선택 / native prefill CPU 연결

사용자의 ‘계속 보완해줘’는 앞선 선택 질문의 저장 지원 통합 보완을 선택한 것으로
진행한다. 저장 차단 시험 ROM으로 범위를 줄이지 않는다. 이는 완료 승인이나
저장 형식/메모리 배치의 기술적 채택이 아니다.

`hangul_calendar_prefill.py`에 세 native copy BL33344/3335A/3336E용 조건부 adapter를
추가했다. 255개32byte 기록 arena의 정렬된 body+10 및 pool 세128byte 슬롯만 허용하며
기존 version-aware reader로22byte 기록을 검증해<=41byte F9FC/native stream으로 복원한다.
실패 시 malformed bytes를 복사하지 않고 native33372 POP으로 남은 읽기를 종료한다.
앞서 정상적으로 쓴 슬롯/기본 문구는 롤백하지 않는다. 오류 표시나 편집 진입 차단은
아직 없으므로 이 실패 경로를 사용자 기능 완료로 보지 않는다. code/RAM/IRQ는 CPU fixture 위치다.

`bench_calendar_versioned_prefill.py`는 native33334/33374,3739A/373A2 getter,
32AA8 script lookup 및32AC6 기본 문구 복사를 실제 CPU에서 실행한다. 서비스 stub 없음.
`cpu_calendar_versioned_prefill/report.json`:11,680경로,35,005슬롯 decode,
45,196 whole-EWRAM Expected Writes 검사 PASS. 모든11,172음절을10글자 최대로
세 슬롯에 emitted writer33,516회로 쓰고 **HOST 기록/pool 재작성 없이** prefill로 읽었다.
원본 raw copier의 F8/내부E5 잘못 복사 반례1개도 재현했다.
기존 single-byte228종/E4payload256종=484,0..3기록,arena0/127/254,
손상된 기록9경로/NULL 첫 기록1경로/삭제·비활성·날짜 필터9경로를 검사했다.
callee-saved regs/SP,writer88byte 및prefill136byte 스택 경계와 기록/pool 쓰기 경계 PASS.

원본/기준 input-heading ROM 불변; 새 ROM/사용자save 미변경.
조건부 F8는 전체 원본 title grammar와 저장 소비자가 확정되기 전에는 미채택이다.
HOST 입력 stream/날짜/flags/index fixtures를 사용했다. 자판 출력이나 실제 세이브에서
로드한 값이 아니며 pixels/VRAM/runtime/save/reset/fresh-load 증거도 아니다.
최종 두 도구 py_compile 및CPU 검사 재실행 PASS. 누적465번역tests/전체foundation은 미실행.
전체 ROM 사전 검사 도구에도 새 prefill 보고서의 도구/산출물/의존성 해시 검사를 연결했다.

다음 완료 경계: malformed/NULL prefill 결과를 편집 진입/오류 UI에 전파하여 stale 값을
정상 기록처럼 사용하지 않게 할 것; 나머지 default/direct/import writers 및 list/표시 소비자와
F8 legacy 판별을 연결할 것; 자판 확정→기록→편집/상세→실제 저장의 누적 경로와
ROM/RAM/IRQ 배치를 채택한 뒤 실제 ROM으로 save/reset/fresh-load를 검증할 것.
33864 정적 확인은 selected pool 및stage의 script 초기값 writer(32AA8 두 호출)이며
저장 기록 reader로 간주하지 않는다. 전체 reader population은 여전히 미확정이다.

## 2026-10-12: prefill 실패를 native 목록 초기화 호출부에 전달

호출부 추가 조사로33334는 직접 편집 진입 함수가 아니라33100 일정 목록 초기화에서
먼저 호출됨을 확인했다. 앞선 ‘재편집 읽기’ 표현은 전체 편집 경로 입증을 뜻하지 않는다.
source image 전체 aligned Thumb-BL 후보 검사에서33114→33334 후보1개를 찾았다.
이는 ARM/간접/오버레이 caller completeness 증거가 아니다. 이번에는 native330C6
목록 dispatcher 및33100 초기화의 실제 CPU 경로를 연결했다.

`hangul_calendar_prefill_guard.py`: 기존 prefill adapter의 실패 경계에만 R12=0을
추가한 파생 후보와33114 caller guard. R12=1을 초기화한 뒤 native prefill을 호출하여
성공 경로는 그대로 진행한다. getter/default/reader/converter/decoder의 검증된 명령이
R12를 사용하지 않음을 확인했다. 저장 RAM의 새 상태 플래그는 만들지 않는다.
IRQ 및 전체 실제 호출 경계에 대한 R12 보존은 아직 미채택이다.

실패 시 세 pool 표시 stream을 E5+zero40으로 비워 이전 정상/기본 문구도 소비되지 않게
하고, native initializer의 count/heading/selection 설정을 건너뛴다. UI state20 및
기존 취소 반환2(완료 flag7=2), sound127 요청, 안전한 offset/selection 값으로 반환한다.
native330C6가 뒤이어 실행하는 장식 draw는 유지하되 문자열 heading은 실행하지 않는다.
원본 저장 기록 및 pool 인접stage는 변경하지 않는다. 한글 오류 대화상자는 아직 없다.
빈 첫 기록을 거부하는 경로의 자연스러운 발생 조건/부모 취소 소비도 미확정이므로
빈 목록 UX의 완료 또는 채택을 뜻하지 않는다.

`cpu_calendar_prefill_guard/report.json`: native dispatcher/initializer/prefill/getter/count,
정상 heading 호출 및 오류 반환을181경로에서 CPU 실행 PASS.
초기화 계속155경로(정상154 및 보호 없는 실패 전진 반례1)/26 보호된 거부 경로,
181 whole-EWRAM Expected Writes, callee-saved/SP 및160byte stack guard PASS.
6음절 rank경계×1..10글자×두 mode, 기존 E4 payload 경계4종,0..3기록,
arena0/127/254,손상 field4종×세 슬롯×두 mode,삭제/비활성/날짜 필터를 검사했다.
핵심 reader 전체11,172음절 증거는 변경하지 않은 기존 prefill dependency 보고서를 따른다.
보호를 제거하면 손상된 slot1에서도 count/heading 후 state4로 진입하는 반례를 재현했다.
보호 후 실패는 heading0/sound127 요청/return2/Z=0 및 세 pool empty로 귀결됐다.

후속으로native30F0C 상위 함수를 연결했다. parent substate+2=4의 이미 초기화된 호출
fixture에서181경로를 재실행했다. 실패 return2/Z=0을 native30F44이 소비하여
parent substate+1=4/초기화word+2=0/import flag+10=1로 바꾸고 flag14:79/80 정리를
요청했다. 성공 return0/Z=1에서는 부모 상태가 유지됐다. parent 경로를 포함한 최종
스택 한계는160byte다. 처음 진입30F14..3E의 초기화와 오류 후 재진입은 아직 미검증이다.
graphics/audio/flag cleanup 서비스는 modeled이며 실제 pixels/VRAM/소리/플래그 정리
효과 증거는 아니다. 위 native parent 상태 소비만 CPU에서 확인했다.
입력 기록/날짜/flags는 HOST fixtures다. 새 ROM/사용자save는 변경하지 않았다.
조건부 F8,다른 writer/list/provider population,자판 확정,실제 code/RAM/IRQ,
save/reset/fresh-load는 여전히 미완료다. 전체 ROM 사전 검사에 새 보고서 해시 검사를 연결했다.
다음: 부모 처음 진입과 오류 후 재진입을 연결하고, 나머지 record 소비자/
writer의 형식 판별 및 자판→실제 저장 경로를 누적 통합할 것.

## 2026-10-12: 첫 진입·오류 후 재호출 및 저장 writer를 통한 복원

`bench_calendar_prefill_guard.py --reentry`에 처음 진입과 연속 단계 검증을 추가했다.
기존181경로 모드도 현재 도구로 재실행 PASS. 새 코드 hook은 추가하지 않았으며
같은 guard/adapter 후보를 누적된 호출 상태에 적용했다.
`cpu_calendar_prefill_reentry/report.json`:245경로/263 whole-EWRAM 검사 PASS,
first-entry64/empty-default4/UI reset 요청60/reentry cycle18/writer repair18.
초기화 계속183경로는 정상182 및 보호 없는 실패 전진 반례1을 포함한다.
보호된 거부62경로. register/SP 및160byte stack guard,writer88byte guard PASS.

native30F0C의 substate0 첫 진입에서는 실제37404 count를 수행한다.
기록이 있으면3A3B0→090C→CpuSet 요청(16byte UI clear)→330C0 mode설정→목록 초기화로
연결했다. 원본 지시문과3A418 UI주소/090C control literal/EC144 SWI11 boundary 확인.
BIOS 서비스는 source stack word0/destinationUI/control05000004만 허용하여 모델링했다.
이는 실제 BIOS/IRQ/runtime의 효과 입증이 아니라 명시된 CPU fixture 서비스다.
메타 count 및 기본 문구 lookup/copier 등 나머지 해당 native 경로는 실제 실행했다.

세 slot×rank0/229/11171×처음mode0/1=18연속 경로:
손상된 첫 진입→같은 기록을 재호출해 다시 거부→emitted versioned writer로 해당
record body22만 수정→HOST 기록/pool/UI/parent/meta 재작성 없이 성공적으로 재호출.
writer 입력 stream은 HOST가 별도stage에 공급했고 호출 register/SP는 fixture가 설정한다.
실패 상태의 UI state20/flag7=2가 native 초기화 요청으로 제거되어 정상 state4/
flag7=0 및 복원된 세 문구로 진행하는 것을 확인했다. 성공 후 자연스러운 사용자 입력/
부모 dispatcher에서 다시 메뉴를 선택하는 전체 traversal은 미검증이다.
재진입은 확인된30F0C routine 경계에서 재호출한 것이며 메뉴 조작 증거로 보지 않는다.

원본의 빈 목록 경로를 확인했다: count0이면 UI/guard를 열지 않고33374 기본 문구를
slot1/2에 공급,selected slot0 및 부모substate3C로 이동한다. 처음0기록 및 전부 삭제
표시된3기록(각mode0/1)에서도 오류음 요청 없이 이 경로 유지 PASS.
따라서 기존보고서의 NULL 최초prefill 거부는 이미 목록에 진입한 불일치 상태의 조건이며
정상적인 처음 빈 목록이 새 guard에 의해 오류로 바뀌는 증거는 아니다.
다만 이 빈 목록 경로는 원래pool slot0/이전 UI를 지우지 않는다. 다음 default/edit 소비자와
입력 stage 초기화에서 stale 값이 사용되지 않는지 별도로 연결해야 한다.

py_compile 및default/reentry CPU2mode PASS. 새 보고서와 원본·기준ROM 및 도구/산출물/
의존성 해시는 전체 ROM 사전 검사에서 확인한다. 새 ROM/사용자save는 변경하지 않았다.
graphics/audio/flag cleanup 및BIOS modeled,실제 pixels/소리/화면/저장 증거 아님.
조건부 F8 전체 writer/reader population·한글 자판 확정·ROM/RAM/IRQ 배치·save/reset/
fresh-load는 미완료다. 다음은 빈 목록→기본/편집 소비자 및 실제 자판 초기값 연결과
나머지 저장 형식 소비 경계다. release나 전체 한글 자판 완료로 판정하지 않는다.
