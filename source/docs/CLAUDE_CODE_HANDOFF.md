# Claude Code 인수인계 — 록맨 EXE 4.5 한글화

## 0000000. 최신 상태 (2026-10-25 늦게) — 아래 모든 절보다 우선

최신 ROM은 `poc/output/pending500_070_v1.gba`(30,359 ID, repro 동일, 정상 진행 16구간 완료)다. 상태 권위는 `analysis/pending500_070_v1/batch_status.json`이다.

- 070: 낱자모가 남으면 확정 막기(사용자 결정). 세이브 저장→새 부팅 복원 확인(`poc/runtime/kb070-save-*`). 정상 진행 레시피 2구간은 「가」 입력으로 바뀌어 041 비교는 무의미, 070 자체 실행이 새 기준.

- 067: PET 상단 요일 (日)→(일). 068: 한글 자판 설치. 069: 고정 칸 파서 출력으로 입력창·확인창 한글 표시.
- 한글 자판 실기 확인: `poc/runtime/keyboard069-probe-v1`(「한글」 입력→확정→확인창 「이름: 한글」), RAM 이름 기록 `80 525d 0401 E5`. 남은 것: 세이브 재실행, 낱자음 확정 처리, 달력 일정 이름, 일정 화면 (木).
- 사용자 결정(10/25): 달력 요일 머리줄은 바꾸지 않는다.


- **065** 사용자 스크린샷(`shots/`) 텍스트 수정(batch_label_v4):
  - 별명 호칭 63720C
  - 아이템 778B08 최신 사본 포인터
  - 칩 이름 풀 한글 사본 연결
- **066** 그림 전용 단계(graphics_fix_v1, 6영역):
  - 날짜 입력 하단, PET 버튼, PET 하위 제목 띠
  - 결과 창 RESULT/WINNER/LOSER(타일 재배정, Galmuri11 Condensed)
  - 프로필 주제 말풍선 19개, 필드 시계
  - 빌드에서 겹치는 기존 패치는 그림 영역 안에 완전히 들어갈 때만 뺀다. 065 verify_final에는 그림을 되돌린 뷰를 넘긴다.
- **다음 그림 단계(067)**:
  - PET 상단 요일 `(日)` → graphics_fix_v2에 준비되어 있다.
  - 달력 요일 머리줄: 타일셋 0x63756C에 95타일이 모두 쓰이고 있고, 맵 0x63818C(30폭)에서 타일 8·9가 두 요일에 공유된다. 타일 2개 추가와 로더 크기 변경이 필요하며, 로더는 아직 찾지 못했다.
- **한글 자판**: `analysis/HANGUL_KEYBOARD_HANDOFF.md` 맨 위 절
  - 저장 형식 A안 결정
  - 표시 훅 v1 CPU 검사 통과
  - 다음은 별명 조합·확정 훅

---


## 000000. 최신 상태 (2026-10-24 저녁) — 아래 모든 절보다 우선

063(대사 292)·064(라벨 87)를 추가 적용했다. 최신 ROM은 `poc/output/pending500_064_v1.gba`(30,339 ID, repro 동일), 미반영 207개다. 상태 권위는 `analysis/pending500_064_v1/batch_status.json`이다.

- **문구 다듬기 189건**: `tools/wording_fit_v1.py`가 만든다. 규칙은 변수 출력 뒤 연결어 축약(「말입니다,」→「말이죠,」 등)이고, 수동 수정은 `translations/wording_fit_v1_manual.json`·`wording_fit_labels_v1_manual.json`에 있다. 결과는 `translations/wording_fit_v1_ko.json`이다.
- `prepare(..., fits=...)`는 초안 번역이 수정 전 문구와 같을 때만 수정본을 쓰고, 원래 문구는 `canonical_wording`에 남긴다. 검토표는 `analysis/wording_fit_v1/REVIEW.md`다. 미검토 개발 초안이다.
- **남은 207개**:
  - 전용 코드 라벨 46: 호칭 63720C는 버퍼 증가 위험, 768764는 명령 바이트 해석, 778C6C는 20바이트 고정 복사
  - 장비 라벨 carry 115: 화면은 이미 한글
  - 참조 미해결 대사 23
  - 원문이 같은 쌍둥이 아카이브 10
  - carry 재구성 불가 대사 8
  - 기타 5

---


## 00000. 최신 상태 (2026-10-24 오후) — 아래 모든 절보다 우선

059~062(153개)를 추가 적용했다. 최신 ROM은 `poc/output/pending500_062_v1.gba`(29,960 ID, repro 동일), 미반영 586개다. 상태 권위는 `analysis/pending500_062_v1/batch_status.json`이다.

- **059 라벨 칸 수**: `tools/label_cells_v1.py`가 라벨 렌더러 호출부의 r4(칸)·r5(행)·r1(스크립트 즉치)을 읽는다. 서브칩 설명은 11칸×3행이다. 라벨의 `·`(U+00B7)는 고정 칸 글꼴에 있는 `・`로 표시하고 기록한다.
- **060 대사**: `generic_page_gate059_v1`은 창 종류를 모를 때 원본에서 가장 좁은 글자 시작 x(92)의 한도 140/140/131을 쓴다.
- **061·062 포인터 재지정**: `batch_label_v3`가 778A4C(내비 이름 21개, `printCurrentNavi`용 0x80바이트 복사)와 76C944의 리터럴 포인터를 새 사본으로 돌린다.
  - 061 빌드 생성 시 기본 포인터 패치 생략, 감사 예외, `nolabel` 사본 복원을 앵커 치환으로 넣었다.
  - 다른 내비로 실제 대사 화면을 본 것은 아니다. 포인터와 해독만 확인했다.
- **남은 586개**:
  - 대사 337개: 창 초과 299, 기타 38 — 문구나 페이지 설계가 필요하다.
  - 렌더러 칸 수보다 넓은 라벨 88개
  - 다른 전용 코드가 읽는 라벨 46개: 호칭 63720C는 버퍼 증가 위험, 768764는 명령 바이트로 파싱, 778C6C는 20바이트 고정 복사
  - 장비 라벨 carry 115개: 화면은 이미 한글

---


## 0000. 최신 상태 (2026-10-24 낮) — 아래 모든 절보다 우선

056~058 라벨 묶음(1,482개)을 추가 적용했다. 최신 ROM은 `poc/output/pending500_058_v1.gba`(29,807 ID, repro 동일), 미반영 739개다. 상태 권위는 `analysis/pending500_058_v1/batch_status.json`이다.

- **라벨 방식**: 고정 칸 라벨 렌더러 진입점 `0x080554A4`(호출 98곳)와 `0x080554C8/0x080554D0`의 공통 경로(훅 위치 `0x080554DC`, 인수 pop을 전처리 코드가 복원)에 대사와 같은 루트·바이트 대조 교체를 건다. IWRAM 고정 칸 파서의 F9 처리기에는 이미 F9FC 한글 확장이 있다.
- **v1 → v2**: 056의 묶음별 선형 래퍼는 057에서 라벨 호출 1회에 최대 약 2만 명령이 들어 PET 메뉴 입력이 빠졌다(폐기본은 `analysis/rejected_builds/`). 057부터 `batch_label_v2.FastLabelComponent`를 쓴다.
  - ROM 루트는 정렬 표에서 이진 탐색한다.
  - EWRAM 루트는 표본 8바이트로 대조한다. 표본 위치는 카탈로그의 모든 LZ 원문 변형과 구별되도록 빌드 때 계산한다.
  - 원래 트램펄린으로 바로 돌아가며, 호출당 최대 약 1,100 명령이다.
- **실기 확인**: 서브칩 설명 「HPを50かいふく!」가 「HP50 회복!」으로(057), 필드 지역명 「インターネット1」이 「인터넷1」로(058) 바뀌었다.
- **주의**: 034~036 마무리 검사는 원본 영역 전체를 비교하므로, 생성 빌드가 라벨 스텁 자리를 원본으로 되돌린 `nolabel` 사본을 넘긴다(next_batch_generic_v1.generate). 플러그인 중인 PET 메뉴 마지막 항목은 「저장」이라 메뉴를 끝까지 내리면 저장된다(testRunner라 파일은 안 남음).
- **남은 739개**:
  - 대사 400개: 창 초과 358, 기타 42
  - 원문보다 넓은 라벨 111개
  - 다른 렌더러를 쓰는 라벨 101개: 적·내비 이름, 호칭 63720C(버퍼 증가 위험), 76C944 등
  - 장비 라벨 carry 재구성 불가 115개: 화면은 이미 6E2B9C 사본으로 한글
  - 글꼴에 없는 글자 12개

---


## 000. 최신 상태 (2026-10-24 오전) — 아래 모든 절보다 우선

054·055 두 묶음(995개)을 추가 적용했다. 최신 ROM은 `poc/output/pending500_055_v1.gba`(28,325 ID, SHA `9b0b9f6b…aa8d6`, repro 동일)이고, 상태 권위는 `analysis/pending500_055_v1/batch_status.json`이다.

- **이름 상한 완화(사용자 결정)**: 검사기 `generic_page_gate054_v1.py`는 플레이어 이름·별명, PET 프로필 입력 문자열(음식·취미·소원·우상·과목 등), 상대 이름을 한글 4자(48px)로 가정한다. 원본 최악값은 99px(6글자+접미사)다.
- **위험**: 4자보다 긴 이름·입력이면 054·055의 995줄이 창을 넘을 수 있다. 목록은 `analysis/pending500_055_v1/relaxed_name_bound_risk_v1.json`에 있다.
- **남은 2,221개**:
  - 라벨 1,821개(고정 칸 렌더러)
  - 48px로도 넘치는 대사 358개(숫자 버퍼·아이템 99px이거나 문구 자체가 긴 경우)
  - 기타 42개

---


## 00. 최신 상태 (2026-10-24) — 아래 0절과 1~9절보다 우선

**042~053 범용 묶음 12개(5,708개)를 추가로 ROM에 적용했다.** 상태 권위: `analysis/pending500_053_v1/batch_status.json`.

| 항목 | 값 |
|---|---|
| 최신 ROM | `poc/output/pending500_053_v1.gba` 14,683,876 bytes |
| SHA-256 | `a7eead551c3bfc14129a9071d0f4bfaaa6d9bc987091e7e8da09174b6b66253c` (repro 동일) |
| 누적 적용 | 27,330 ID / 정규 미반영 3,216 |

방식(`tools/batch_generic_v1.py`):
- **prepare**: 미반영 그룹 중 대사(mmbn45)를 범용 페이지 검사기(`generic_page_gate043_v1.py`)로 거른다.
  - 원문과 번역을 같은 규칙으로 페이지·줄 단위로 시뮬레이션한다.
  - 줄 한도는 1·2행 232−L, 3행 A−2−L(L=글자 시작 x, A=화살표 x)이다. 가변 출력 상한은 내비 48, 칩 88, 그 외 99px다.
  - 줄바꿈과 띄어쓰기만 맞바꿔 다시 배치하고, 그래도 넘치면 keyWait+clearMsg로 페이지를 나눈다(유닛 `pages` 필드에 기록).
  - 아카이브의 기존 한글(carry)은 authored 자산을 재컴파일해 현재 제품 바이트와 같은지 확인한 뒤 합친다.
- **Component**: 공통 `0x4FB4C`에 묶음마다 래퍼를 하나씩 쌓는다. 기술자 root=0은 EWRAM 전체를 뜻한다. 직전 제품이 그 아카이브로 넘기는 모든 payload(원본/재배치 LZ RAM, 원본/재배치/소유자 ROM 루트)와 전체 바이트가 일치할 때만 새 합본으로 바꾼다.
- **검사**: 묶음마다 원본부터 primary·repro 빌드 → 바이트 동일, CPU(`bench_generic_v1.py`), 자체 콜드부트 16구간(`run_normal_generic_v1.py`), 041과의 화면 비교(`compare_coldboot_generic_v1.py`; 시계·바닥 팔레트·연출·전투 난수 타이밍 차이만 있음).

남은 3,216개:
1. **라벨 1,821 (mmbn45s)**: 적 이름·크레딧·BBS 머리글·통신 메뉴 등이다. 고정 칸/OBJ 렌더러가 ROM 루트를 직접 읽어서 공통 래퍼로는 화면이 안 바뀐다. 렌더러별 한글 공급 작업이 필요하다. 장비 라벨 18벌(684)은 이미 6E2B9C 사본을 가리켜 한글로 보인다.
2. **대사 1,353**: 원본 최악 이름 폭(별명 6자+접미사=99px) 기준으로, 재배치와 페이지 분할을 해도 창을 넘는다. 정책 결정(이름 상한 완화 또는 문구 수정)이 필요하다.
3. **기타 42**: 참조 미해결 23, 원문이 같은 쌍둥이 아카이브 10, carry 재구성 불가 8, 부분 적용 스크립트 1.

주의:
- `run_normal_generic_v1.py`는 최신 래퍼만 guard로 넘긴다. 전부 넘기면 Windows 명령줄 32,767자를 넘는다.
- 묶음 빌드는 약 20분이고, primary와 repro를 병렬로 돌린다.

---


## 0. 최신 상태 (2026-10-23, Claude Code) — 아래 1~9절보다 우선

**041 전체 500개를 ROM에 적용했다.** 상태 권위: `analysis/pending500_041_v1/batch_status.json`.

| 항목 | 값 |
|---|---|
| 최신 ROM | `poc/output/pending500_041_v1.gba` 13,208,332 bytes |
| SHA-256 | `4782fdaf94f178b64f062b67d39c85d8c46391d183e5da14b2e805d147b55ff2` |
| repro | `poc/output/pending500_041_v1_repro.gba` 바이트 동일 |
| 누적 적용 | 21,622 ID (040 대비 +500) / 정규 미반영 8,924 |
| 빌드 | `python -X utf8 tools/build_layout500_041_v1.py [--repro]` (원본부터 전체 누적, 약 26분) |

설계: 모든 reader(41D84/3EFBF/3C485/40D67/47963/4B5AF/6A507/4F773/213AB/6AB03)가 공통 `0x4FB4C`를 지난다는 것을
역어셈블로 확인했다. 그래서 그 12바이트 stub 하나에 041 래퍼를 합성했다(`tools/typed_rom_product041_v1.py`).
기술자 = (root, match, match_len, script_count, clone). `r0==root`이고 r0의 **전체 바이트**가 040 제품이 그 자리에 넣는
payload(원본 LZ RAM / 재배치된 옛 LZ RAM / 옛·raw ROM 루트)와 같으면 새 합본 clone으로 바꾸고 040 래퍼로 tail-call한다.
선택하지 않은 스크립트는 바이트가 같아서 화면이 바뀌는 건 선택된 500개뿐이다. 서브칩 전용 selector/component(041_v1/v2)는
이 범용 래퍼로 대체됐다(참고용으로만 보존).

검증:
- 빌드 내 감사: 040 투영 정확성(재생성040 SHA 일치), 최종 쓰기 감사, 기존 consumer 레코드 보존, 500/156/53 모집단, 비선택 스크립트 바이트 일치.
- CPU: `tools/bench_typed041_v1.py` → `analysis/pending500_041_v1/selector_cpu_v1.json` 384건 통과.
- 041 자체 콜드부트: 040 입력 레시피 16구간을 재생했다(`pending500-041-normal-v1-*`). 040과 같은 필드에 도달했고, 차이는 RTC 시계 표시뿐이다.
- 화면: `pending500-041-subchip-count-diag-v1`에서 서브칩 사용 메시지 6F9B4C:6이 한글(「지금은 아직 쓰지 말자」)로 나온다(읽기 alias 진단).
  `pending500-041-equipment-error-v1`: 장비 native 경로에서 비선택 70번·선택지가 040과 동일하다.
- 아직 화면으로 못 본 것: 장비71..75, 메일 알림14/77, 대회 main/secondary, BBS, B2, trader/tutorial.

다음: 042 묶음(8,924 backlog에서 500개) — `typed_rom_product042`를 041 위에 같은 패턴으로 만들고
`generate_primary041_v1.py`처럼 041 빌드에서 앵커 치환으로 042 진입점을 생성한다. 배포 패치는 요청 시에만.

---


작성일: 2026-10-23 / 프로젝트: `D:\Games\Kor Patch\CLude\Rockman exe 4.5`

이 문서는 Claude Code 재개용 요약 스냅샷이다. 상태가 바뀌면 아래 JSON을 기준으로 판단한다.

## 1. 먼저 읽을 파일과 현재 결론

1. **현재 상태 권위:** `analysis/pending_insertion_500_041_source_v8/batch_status.json`
2. 상세 근거/미해결점: `analysis/PENDING_INSERTION_500_041_HANDOFF.md`
3. 과거 작업 이력: `HANDOFF.md` — 긴 누적 이력이며, 아래쪽의 실행 중/미완료 문구는 과거 상태다.
4. 원본·도구·폰트·TPI 프로필: `project.json`

**현재 실제 ROM은040이다. 041의 새500개는 아직 ROM 미반영이다.**
서브칩102개용 ROM 선택 코드와 쓰기계획 API를 구현했고 CPU 검증까지 끝났으나,
나머지398개를 합친 전체500개 제품 빌드·재현 빌드·새 ROM 화면 검증은 남아 있다.
지금부터 번역을 처음부터 다시 하거나 준비500개를 다시 선정할 필요는 없다.

## 2. 원본 / 현재 ROM / 숫자의 의미

| 구분 | 현재 상태 |
|---|---|
| 원본 | `Rockman EXE 4.5 Real Operation (J)(Independent).gba`, 8,388,608bytes |
| 원본 SHA-256 | `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` |
| 최신 실제 누적 ROM | `poc/output/pending500_040_v2.gba`, 13,030,312bytes |
| 현재 ROM SHA-256 | `bf97f861fc244861d2728c67eff4adaf84e532bc321665073908b9e621add570` |
| 독립 재현본 | `poc/output/pending500_040_v2_repro.gba` —040과 동일한 결과 |
| 현재 누적 적용 | 메타데이터 기준21,122 ID |
| 정규 draft 미반영 | 9,424 ID — 준비된041의500개를 포함 |
| 준비된041 묶음 | 500 ID /445scripts /53archives, 기존156 ID 보존 포함 |
| 041 실제 신규 적용 | **0** |
| 서브칩 구현 범위 | 위500개 중102 ID /21archives — 나머지398 ID /32archives 통합 전 |

9,424는 정규 draft ID의 미반영 수이지, 이미지·자판·저장 기능까지 포함한 전체게임 잔여량이 아니다.
일부 기존 도구의 unique layout-ID 수20,775와 누적 메타데이터21,122는 다른 분모다.
500개가 실제 빌드/적용/검증되기 전에는 미반영을8,924로 줄여 보고하지 않는다.

## 3. 사용자의 유지 요청 / 하지 말아야 할 일

- 번역한 내용을 **500개씩 묶어 ROM에 적용**하고 테스트한다. 서브칩102개만 단독 ROM으로 내지 않는다.
- 사용자가 다시 요청하기 전에는 BPS/xdelta/ZIP 등 **배포용 패치 파일을 만들지 않는다**.
- 원본 ROM은 덮어쓰지 않는다. 기존040 ROM과 예전 빌드·번역·실패 기록·저장 파일도 보존한다.
- 사용자 mGBA를 조작하거나 사용자 세이브를 바꾸지 않는다. 자체 격리 Mesen으로 검사한다.
- 최종 제품은 **불변 원본부터 전체 누적 빌드 경로로 재생성**한다.040 ROM을 입력으로 삼아 직접 수정하지 않는다.
- 기존 보고서가 SHA로 참조하는 `.py`/번역/근거 파일은 덮어쓰지 말고 새 버전·출력 경로를 사용한다.
- `new-only` 진단 바이너리를 그대로 주입하면 기존 한글이 빠질 수 있다. 기존156개가 합쳐진 authored carry를 사용한다.
- 현재 존재하는040 빌드 명령을 같은 출력 경로로 재실행하면 보존 가드가 거부한다. 기존 파일을 지우고 우회하지 않는다.
- 코드 변경이 없는데 완료한 소스·폰트·native 경로·CPU 검증을 반복해서 진행량으로 계산하지 않는다.
- 줄바꿈 외 문구 축약/치환·음절 단위 강제 줄바꿈을 임의로 하지 않는다. 제어 코드·분기·변수·숫자를 보존한다.
- 한글 자판 목표는 사용자가 선택한 자동 조합 방식과 저장/재표시까지 포함한다. 입력 시험만으로 완성 처리하지 않는다.
- 넘버맨의4649 말장난은 사용자가 자연스러운 **‘잘 부탁드려요’** 번역을 선택했다.

## 4. 이미 끝난041 준비 — 재작업하지 말 것

모든 다음 상대 경로의 기준은 프로젝트 루트다.

- `analysis/pending_insertion_500_041_source_v8/selection.json`: 정확500개. source_v7은 이력이다.
  호출 미확인 `7794EC:247:0`은 전체 잔여 목록에 남기고, 이번 묶음에서는 `6DD0B8:14:0`으로 교체했다.
  미확인 항목을 번역 완료/미사용으로 선언한 것이 아니다.
- `verification_v3.json`: 원문·제어·숫자·인코딩·텍스트/바이너리 왕복 및 현재 ROM 글꼴468개 검사 통과.
- `carry_verification_v2.json`: 새500+기존156, 기존8물리 consumer의 실제 payload를 authored 입력에서 동일하게 재생성.
  현재 미선택 script bytes도 유지한다. `6E2B9C`의 기존37개는 weapons33+labels4의 합집합이다.
- `carry_roundtrip_v2.json`: 기존 번역과 합친8개 바이너리/텍스트/제어 왕복 통과.
- `source_handoff_v3.json`: 1,348개 고유 의존 파일 /3,601참조 대조 완료. 소스 준비 증거이지 ROM 적용 증거가 아니다.
- 현재040의 실제 검증 근거: `analysis/pending500_040_v2/runtime_closure_v1.json`.
  이040 근거는 앞으로 만드는041의 런타임 증거로 자동 이전되지 않는다.

위041 보고서는 모두 `analysis/pending_insertion_500_041_source_v8/`에 있다.
기존671물리 consumer 전체와 기존 메타데이터를 보존해야 한다. owner catalog의25개 set-match 미확인을 삭제 대상으로 보면 안 된다.

## 5. 최신 구현 — 서브칩102개 부분

| 역할 | 현재 사용할 파일 |
|---|---|
| 선택 코드 생성 | `tools/subchip_rom_selector041_v1.py` |
| 원본 기반 쓰기계획 API | `tools/subchip_rom_component041_v2.py` |
| 실제 component 계획을 사용하는 메모리 fixture | `tools/fixture_subchip041_v3.py` |
| CPU 검사 | `tools/bench_subchip_selector041_v3.py` |
| 입력 거부 검사 | `tools/bench_subchip_component041_v1.py` |
| CPU 결과 | `analysis/pending_insertion_500_041_source_v8/subchip_selector_cpu_v3.json` |
| 입력 검사 결과 | `analysis/pending_insertion_500_041_source_v8/subchip_component_inputs_v1.json` |
| 실제 원래 서브칩 경로 결과 | `analysis/pending_insertion_500_041_source_v8/subchip_boundary_v1.json` |

선택 조건은 native root `02026C00`, common LR `0804F7BD`, 저장된 outer LR `08041D8F`,
대사 번호 범위와 archive별 선택 mask, **디코딩된 native 전체 bytes 동일성**이다.
원래23-slot table `41F38`에서13/14는NULL이고, 유효 archive는21개다. NULL은 그대로 둔다.
20byte descriptor는 clone/native-copy/native-length/script-count/selected-mask 순서다.
32byte 작업 스택만 쓰며 persistent RAM은 추가하지 않는다. 기존040 wrapper로 tail-call한다.

검증 완료:

- CPU1,113건: 선택102, 비선택318, 잘못된root126/caller84/outer105,
  비선택·범위 밖 번호252, native 손상126. 원래41D84부터 common4FB90 직전까지 비교했다.
- 레지스터·context·flags, RAM canary, 기존040 fallback의 스택/레지스터 조건 통과.
- 실제 component 계획과 별도로 배치한 메모리 fixture가 bytes까지 동일하고 재생성도 동일하다.
- 잘못된 입력22종을 거부한다. 추가 쓰기 계획은24,264bytes지만 **실제 ROM 파일로 출력하지 않았다**.

CPU 검사는 실제 게임의 전체 UI/글리프 출력/오디오/타이밍까지 증명하지 않는다.
API는 전체500개 등록, authored 입력 재컴파일, lineage/폰트/layout 검사와 최종 write audit를 대신하지 않는다.
이제 이 부분을 다시 만들기보다 남은398개와 같은 빌드 그래프로 연결해야 한다.

## 6. 다음 재개 순서

1. 현재 JSON과 위 최신 보고서·코드를 읽고 기존 완료/미완료를 구분한다.
2. 남은398개/32archives의 소비 경로와 등록 조건을 마무리한다. 아래 표의 ‘확인’은 전부 화면을 봤다는 뜻이 아니다.
3. 기존156 carry와 기존671물리 consumer를 유지하는 **041 전체500개 primary 빌드 진입점**을 작성한다.
   현재041 전체 제품 빌드 진입점은 아직 없다. 서브칩 component만 완성된 상태다.
4. 기존040의 원본 누적 빌드 구조를 참고해, 새 component를 같은 그래프에 합친다.
   공통 trampoline은 최종 단일 writer로 합성하고, append·pointer·header를 포함한 전체 변경을 감사한다.
5. 불변 원본에서 primary/repro를 각각 만들고 bytes/메타데이터/기존 번역 보존/500개 정확성을 확인한다.
6. 새041 ROM 자체를 coldboot하여 새 번역과 관련 메뉴·선택지·복귀를 검증한다.
   040 저장상태를041에 로드해서 검증했다고 하면 안 된다.
7. 실제 통합/검증 결과에 맞춰 상태 JSON을 갱신한다. 배포용 패치는 생성하지 않는다.

기존 구조 참고 파일:

- `tools/build_layout500_040_v2.py`: 기존040 primary/repro 진입점. **참고용이며 기존 출력에 재실행하지 말 것**.
- `tools/build_development_patch_040_v2.py`, `tools/typed_rom_product040_v2.py`
- `tools/specs/primary040_v2_version.json`: 이전 진입점에서의 정확한 버전 생성 규칙.
- `tools/prepare_typed_inputs040_v1.py`, `tools/typed_rom_selector040_v1.py`
- `tools/verify_typed_product040_v1.py`: 기존 최종 감사 구조 참고.

## 7. 남은 묶음별 쟁점

| 계열 | 새 ID 수 | 확인된 부분 / 남은 부분 |
|---|---:|---|
| 장비 경고 |90|원래70번 경고의 RAM `0202BA7C`, common `4F7BD`, outer `3EFBF`, 출력52,110 확인. 선택71..75의 분기·전체 등록 추가 필요|
| 메일 알림 |2|14/77. 실제 본 intro9/outer40D67을 알림 호출 증거로 확대하지 말 것|
| 대회 main |217|기존040 ABI는 `02024000`/LR47963. 새 상단·하단 배치/clear/분기 확인 필요|
| 대회 secondary |4|같은47958 reader 사용.15/60/62 소스 직접 호출 확인,50 선택 및 live loader 확인 미완료|
| BBS |3|기존 reader 규칙을 재사용하되 새 항목·선택/복귀 검증 필요|
| B2 board |11|원본10-subarea lookup 확인, 실제 경로와 소비 검증 미완료|
| B2 cached NPC |62|weekday0..6/RAM02039800/source LR4F773 연결 확인, 실제 경로 미완료|
| raw trader/tutorial |9|trader23: reader6AAF8/LR6AB03/root pointer6AD80. tutorial5의4개:20444→213A2/LR213AB. tutorial14의4개는 원래 호출 미확인|
| 합계 |398|서브칩102개와 합쳐 이번500개|

근거: `native_contracts_v2.json`, `native_callers_v1.json`, `native_observations_v1.json`, `quick_native_v1.json`.
491개의 lookup 참조 확인을491개 전체 ABI/런타임 완료로 바꾸어 말하면 안 된다.
‘같은 실제 소비 규칙’이 입증된 집단은 묶어서 검증하되, 단순 숫자 채우기로 미확인 항목을 통과시키지 않는다.

주의할 기존 해석:

- 장비guide60/메일intro9는 source가 명시적으로 x92로 배치한다. 초기52→표시92는 기본 좌표 오류 증거가 아니다.
- 장비guide hook은 이미 ROM root를 고르는 경우가 있지만, 실제 경고70은 native RAM/outer3EFBF이다. 두 경로를 혼동하지 않는다.
- PET의 root `08803460`/script23은 `65B9E8`이다. trader `6FE8D4`의040 root는 `0888A440`이다.
- 후보 바이트·literal pool을 Thumb 코드로 잘못 해석하면 ARMv7처럼 보이는 가짜 명령이 나온다. 실제 코드 구간만 ARM7TDMI/Thumb-1로 검증한다.

## 8. 에뮬레이터 출발점 / 진단 한계

- 자체 실행 파일: `poc/runtime/isolated-mesen-chip-matrix/Mesen.exe`.
- 정상040 서브칩 직전: `poc/runtime/pending500-040-native041-field-intro-v1/checkpoint.mss`, 같은 폴더 `result.json`.
- 메뉴 실제 진입: `poc/runtime/pending500-040-native041-subchip-v11/`.
- 대표 사용 불가 대사: `poc/runtime/pending500-040-native041-subchip-count-v3/`.
  이는 아이템39의 availability/수량 **읽기만** 각각1회 바꾼 진단이다. 실제 아이템·HP·상태 records는 유지됐지만 자연 획득/사용 성공/저장 증거는 아니다.
- `diagnostic_checkpoint.mss`는 정상 플레이용 부모로 승격하지 않는다.
- 초기 필드 상태에서Start가 안 먹던 문제는 추가 wait/A 뒤 정상 진입했다.
  입력 전달 자체는 확인됐으며, 특정 cutscene이나Select가 필수라고 원인을 확정한 것은 아니다.
- 과거 검사 실패·초기 모델 거부는 보존돼 있다. 버퍼 수명 밖인 필드 복귀 뒤의 RAM 재사용을 번역 손상으로 오인하지 않는다.

## 9. 환경과 시작 명령

Windows PowerShell / Python3.14. 프로젝트 도구는 보통 `python -X utf8 tools/파일.py`로 실행한다.
의존 도구는 `external/`과 `project.json`의 버전/해시를 유지한다. TextPet alpha3, ARM용 keystone/capstone,
Unicorn2.1.4가 기존 코드에 연결돼 있다. 임의 최신 버전으로 교체하지 않는다.

읽기 전용 시작 명령:

```powershell
Set-Location -LiteralPath 'D:\Games\Kor Patch\CLude\Rockman exe 4.5'
Get-Content -LiteralPath 'CLAUDE_CODE_HANDOFF.md'
Get-Content -LiteralPath 'analysis/pending_insertion_500_041_source_v8/batch_status.json'
Get-FileHash -LiteralPath 'poc/output/pending500_040_v2.gba' -Algorithm SHA256
```

검사 코드 참조용 명령은 `python -X utf8 tools/bench_subchip_selector041_v3.py`와
`python -X utf8 tools/bench_subchip_component041_v1.py`다.
이미 결과가 있으므로 기본적으로 다시 실행하지 않는다. 변경이 생기면 새 버전/새 결과 경로를 마련하고 해당 범위만 재검사한다.

인수인계 시 자체 Python/Mesen 실행·미완료 명령은 없다. 사용자 ROM/세이브·배포 패키지는 변경하지 않았다.
일본어 소형 메뉴·이미지·지역명·한글 자판 저장/재표시·전체게임·실기/오디오/멀티 등은 아직 완료 선언할 수 없다.
