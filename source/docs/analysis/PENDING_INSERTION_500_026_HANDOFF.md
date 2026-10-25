# 026 진행 기록 — 실제025 다음 미적용500개

현재 권위는 **`analysis/pending500_026_v1/batch_status.json`**이다.026 ROM 반영·독립 정적 검증·재빌드·자체 정상 경로/선택지 표본 검증까지 완료했다. 현재 `poc/output/pending500_026_v1.gba`는12,200,828bytes, SHA256 `bf66382b7897f1313a9dba55333512e46f46e5e036a6905d049693ac0af80adf`, 실제500개 추가/누적14,122개다. `_repro.gba`와 전체byte 동일하다. `analysis/pending500_026_v1/integration.json`은430개 비변경 소비자+28개 병합·기존ID/신규delta/owner/포인터·source storage/ExpectedWrites·전체diff를 PASS했다. A3 CPU5,652/B0 CPU6,341·16개 손상거부·네이티브 제어코드/테이블/helper byte동일도 PASS다.

`normal_runtime.json`은026자체 coldboot/초기설정/native자판3페이지·선택 가능한 네내비·첫메일23쪽/닫기·복귀·재열기 PASS다. `raw_samples.json`은세로716DE4:8/PET683054:1의font CPU→OBJ→화면pixels/정확한줄좌표·선택지빈배경·두노드방향8개씩·세로B무시/A그만둔다확정·PET B취소→기존script2→각원래PET복귀 PASS다.26개 기계검사 화면은 **신규7개 서로다른literal+기존취소1개**를 포함한다. 신규Yes후속683054:1:4는 실행하지 않았다. `visual_review.json`은22초기설정/23메일/30raw 접촉표를 직접본 관찰과 한계를 기록한다. 모든500개의 실행·문맥 승인이나 자연임무/배틀효과를 검증한 것은 아니다. 사용자가 다시 요청하기 전에는 BPS/xdelta/ZIP을 만들지 않는다.

첫 `finalize_layout500_026.py`는관찰한고유문구8개를전부신규로잘못세는기대값에서거부했다. 실제신규7+기존1을구분한 `finalize_layout500_026_v2.py`로 현재권위를 생성했다. `checkpoint_count_correction.json`과기존체커를보존했다. ROM/실행증거/기술조건을바꾸지않았다.

다음은 **실제026 적용ID/effective owner/cumulative026.scope**로새미적용500개를찾는다. 이번500개를재선정·재적용하지않는다. carry는 earliest parent scope의기존문구→024새문구→025새문구→026새문구를원본에서재구성하고현재026을byte비교oracle로만쓴다. 원본/025·이전ROM/기존ZIP·세이브/실패증거를보존했다. 자동한글저장과기존UI문제는계속열려있다.

## 고정 입력과 준비 결과

- 기준 ROM `poc/output/pending500_025_v2.gba`, SHA256 `ad775421ab5353c1326ab3861cbc22e323ce6885c411273de5e2bdcaebde040e`, 누적13,622개.
- `analysis/pending_insertion_500_026_survey_v1/survey.json`: 기존 좁은 분류에는 후보0개. 게임 전체 미번역0개라는 뜻이 아니다.
- `analysis/pending_insertion_500_026_layout_v5/survey.json`: 현재 분석 후보509개. v1..v4는 중간 분석 이력이다. v5는 새 네이티브 CPU 증거와 보수적 세로선택지 빈 페이지 조건을 고정한다.
- `analysis/pending_insertion_500_026_selection_v1/selection.json`: 실제025와 겹치지 않는500개,75개 완전 스크립트/28개 기존raw아카이브. PET 고정16px 선택지239/일반 가로201/세로44/일반페이지16. 초안 문구는 유지하고18개 literal의 같은 단어 줄 배치만 명시적으로 조정했다. needs_review/NON-DISTRIBUTION.
- `analysis/pending_insertion_500_026_native_controls_v1/cpu.json`: 원본/실제025 F608·EB00/01·F801/02의3,060개 CPU fixture. 네이티브 query/flag/dispatch helper를 대체하지 않았다. 세로 폭1..10, EB00한칸8px/EB01고정16px, 배틀 global8/9의8bit와global10의16bit만 모델링. 배틀 효과/자연caller/저장 지원 증거가 아니다.
- `analysis/pending_insertion_500_026_models_test_v1/result.json`: 정상·거부38개 제어 fixture.
- `analysis/pending_insertion_500_026_compile500_v1/verification.json`:500개 원문 전체 바이트왕복/번역 제어·문자·바이트왕복/비선택script 보존, 실제025의389개 필요glyph 공급 PASS. 이 source-only 전체payload를 ROM에 직접 덮어쓰면 기존번역을 유실하므로 금지.
- `analysis/pending_insertion_500_026_carry_v1/preflight.json`: 기존2,352개+신규500개 source-bound 병합. effective owner와 cumulative024→025 parent scope/신규문구 순서로 이전 내용을 재구성하고 실제025의28개 payload와byte동일 비교. 기존문구/소비계약·비신규script 보존 PASS.
- `analysis/pending_insertion_500_026_input_gate_v1/verification.json`: 실제source/선정문구/기하/현재025carry/명령 CPU 적용성 입력게이트 PASS. 첫시도는 복제 도구의 두 번째 아카이브 기대값이33으로 남아 거부했고, 고정 선정28로 일치시켜 통과했다. 원본이나 ROM의 기술 조건을 완화한 것이 아니다.
- `analysis/pending_insertion_500_026_gate_tests_v1/result.json`: 실제 production500 입력과28개 손상거부 fixture PASS.

## 빌드 경로와 다음 검사

선정500개 원문/번역을100+150+125+125개로 나누어 전부 사전 대조했다. 형제자매 질문, 수련 A/B버튼·3회실패/휠3개, 등록2000제니, 배틀 수락/거절 등 정보는 유지했다. 이는 사람의 전체 문맥/화자 승인이나 자연이벤트 관찰이 아니다. `1인 독학`, 형/오빠·누나/언니의 어투, 말더듬 `나, 남동생`, 넷배틀/넷 배틀 등의 표현과 native호칭+한국어접미어 조합은 후속 의미/어투 검수 대상으로 남긴다. 문구 자동 일괄 수정은 하지 않았다.

F608 네이티브 query는 r0=1로 `020159F0+8`의 **bit0**를 검사한다. 새 CPU fixture도0/1을 넣어 실제 helper를 실행했다. 예전025 표본체커의 `>>1` 표현을 새 런타임 계산에 복사하지 않는다. 기존 결과를 사후 편집하지 않는다.

`tools/build_layout500_026.py` / `--repro`가 원본부터 독립 빌드한다. `tools/specs/primary026_version.json`은 frozen025 primary에 대한 정확한5개 편집만 허용한다. 024→025→026 조합을 할당 전에 적용한다. `layout500_inputs_026.py`와 `layout500_product_026.py`가 입력·보존·단일owner·정확한500 delta를 검사한다. 이전25 도구는 수정하지 않았다.

완료한 빌드는 `poc/work/pending500_026_v1`, `poc/output/pending500_026_v1.gba`, 별도 `_repro` 경로다. 두primary가정상종료했고실제출력해시가같다. 아래는실행한검증절차이며다음배치와혼동하지않는다. 실패 work/args는 보존하고 새 버전을 사용한다.

1. `verify_layout500_product_026.py --out analysis/pending500_026_v1/integration_pre_repro.json` 후 독립 `_repro.gba`와 `--repro` 최종검사.
2. `bench_hint_rom_reader_024.py --rom ...026_v1.gba --out .../a3_cpu.json`, `--field-b0` 별도 b0_cpu, `verify_layout500_integrity_024.py` 새ROM 매개변수 검사.
3. `run_first_mail_regression.py --rom poc/output/pending500_026_v1.gba --prefix pending500-026-v1 --expanded-startup-captures`, `verify_layout500_normal_026.py`를 같은ROM에 실행. 역사적 generic startup count/lineage는 사용하지 않는다.
4. 새 진단 `capture_layout500_display_026.py`의 `vertical-choice`=716DE4:8, `pet-choice`=683054:1. 검증된 PET root/table read-alias와 네이티브 context reset을 재사용했다. 전자는 prompt후A→두 줄 선택지, disableB=true의B무시/상하/확정/네이티브복귀; 후자는 두 페이지후선택지/입력/취소대사·waitHold이후PET복귀를 확인했다. 진단 checkpoint는 정상play 상태로 승격하지 않는다. `verify_layout500_samples_026.py`의26개표본검사 및 `prepare_layout500_visuals_026.py`의접촉표를직접확인했다. provider첫문자오프셋은실측과99px상한으로검사한것이며독립재계산/최대길이/한글이름지원증거로확대하지않는다.

자동한글 조합→확정→저장→재표시, native 일본어 자판/호칭·필드날짜HUD, 기존 welcome bitmap 행간, 전체500개 문맥/자연이벤트·분기·provider최대길이·배틀효과/실기·오디오 검수는 여전히 미완료다. 해시로 고정된 기존·새 빌드 도구는 사후 편집하지 말고 새 버전을 만든다.
