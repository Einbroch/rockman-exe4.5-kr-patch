# 025 재개 기록 — 500개 누적 반영·재빌드·선택지/이름 표본 검증

현재 권위는 **`analysis/pending500_025_v2/batch_status.json`**이다. 최신 개발 ROM은 `poc/output/pending500_025_v2.gba`,12,188,612bytes, SHA256 `ad775421ab5353c1326ab3861cbc22e323ce6885c411273de5e2bdcaebde040e`이며 독립 `_repro.gba`와 전체byte 동일하다. 이전02413,122개에 실제 미적용500개를 더해 **총13,622개**다. 원본·024/이전ROM·기존ZIP/세이브/증거를 보존했고 새 배포패키지는 없다. 아래 준비/실패 이력을 새 번역 수로 중복 계산하지 않는다.

## 현재 통합·런타임 결과

`analysis/pending500_025_v2/integration.json`: 실제500-ID delta/기존누락0,425개 실제 compiled consumer payload 보존+33개 병합, 포인터/source storage/유효owner/전체ExpectedWrites·diff·append/재빌드 PASS. primary407/catalog미변경325다. 일반 메타데이터 순회460개와 ROM offset을 가진 독립검사458개는 다른 분모이므로 합치지 않는다.325는 잔여 미번역 개수가 아니다.

같은025의 `a3_cpu.json`5,652조건/`b0_cpu.json`6,341조건/`integrity.json`16손상거부 PASS. `normal_runtime.json`은 자체coldboot/초기설정/native자판3페이지/선택가능 네내비/첫메일23쪽·복귀·재열기 PASS. `raw_samples_v3.json`은 신규766134:4선택지의 두노드 모든 상하좌우8이동, A예0/A아니요1/B취소1의native계속실행·원래PET복귀,67D44C:2이름대사2쪽의 fontCPU→OBJ→pixels/행오프셋/정지/빈배경 PASS다. 기본선택지확정·취소 뒤 잔상은 직접비교화면에서 보이지 않았다. `visual_review.json`에22초기화면/23메일쪽/15raw캡처와추가Yes접촉표를 직접본 관찰 및 한계를 기록했다. 이것은500개 인간 승인이나 글로벌표현 승인과 다르다.

표본은격리 PET root/table read-alias로 실제native초기화/선택지입력/핸들러/계속실행을 관찰한 것이다. 자연배틀caller의 결과효과·화자선정·획득·진행/flag/provider최대길이·저장 검증으로 확대하지 않는다. 통신화면/실제넷배틀을 실행한 것이 아니다. 진단은 제품 ROM에 들어가지 않았다.

다음 작업은 **실제025의 적용ID·effective owner·cumulative025.scope를 기준으로** 남은500개 후보를 찾는 것이다. 이500개를 재선정/재번역/재적용하지 않는다.022registry만 재생하면024/025가 빠진다.025새scope의carry는024parent_scope복원→024신규units→025신규units 순서와현재owner자산으로 source재구성하여현재025바이트와 비교해야 한다. 자동한글 저장/재표시와아래기존UI문제는 계속열어둔다.

## 고정된 다음500개

`analysis/pending_insertion_500_025_selection_v1/selection.json`: 실제024의 적용 ID와 겹치지 않는500개,118개 완전 script group/33개 기존 raw archive. 선택지371/PET 고정flag109/PET native이름18/일반2. 기존 canonical needs_review 초안 문구를 유지하고15개 literal의 단어 경계 줄 위치만 명시적으로 조정했다. 새로운 prose 대량 치환은 없다.

- `pending_insertion_500_025_layout_v7/survey.json`: 현재 선택 조사. v6 이전은 이력이다.
- `pending_insertion_500_025_native_controls_v1/cpu.json`: 원본/실제024 F607 폭1..11/F0001,040fixture. native query/flag helper를 대체하지 않았다. 새025 GBA나 선택 결과 검증은 아니다.
- `pending_insertion_500_025_models_test_v1/result.json`: 정상/거부28개. PET flag projection이 print provider 뒤를 빈 페이지로 취급하던 분석 도구의 오류는 `pet_nickname_flags_capacity_025_v2.py`에서 고쳤다. 조사 v7에서도581후보/선택500개는 유지된다.
- `pending_insertion_500_025_compile500_v1/verification.json`: 원본 archive바이트왕복/번역제어·의미·바이트왕복/비선택 script 보존/실제024419glyph PASS. 이 전체 source-only payload를024 위에 덮어쓰면 기존 번역이 유실되므로 직접 삽입 금지.
- `pending_insertion_500_025_carry_v1/preflight.json`: 기존1,897개+신규500개를33archive에 source-bound 병합. 기존 유효 owner/scope를 재구성해 실제024payload와 byte동일. 024가 변경한 arc는 `cumulative024.scope` 및 parent_scope→024새문구 순서로 복원해야 한다. 오래된022 registry만 쓰면024번역이 유실된다.
- `pending_insertion_500_025_input_gate_v1/verification.json`: 현재500개 primary 입력 게이트 PASS.
- `pending_insertion_500_025_gate_tests_v1/result.json`: 실제 production입력500개 정상/손상28거부fixture PASS.

## 빌드 실패와 수정

첫 `pending500_025_v1`은 최종 consumer보존 검사에서 ROM 저장 전에 실패했다. `analysis/pending500_025_v1/build_failure.json` 참조. 부모 선택 방향을 잘못 추가한 검사 버그였다. current→prior에는 가장 큰 subset을, 독립 prior→current에는 가장 작은 superset을 골라야 한다. 최소subset을 고르면 짧은/전체본문이 같은 archive709408/6DD9AC의 전체본문2개가 매칭되지 않는다.

`pending_insertion_500_025_consumer_identity_v1/result.json`: 실제024 self-match에서 오류기준458/460, 수정기준460/460 재현. 동점 모호성은 여전히 거부한다. `layout500_product_025.py`만 수정했으며 기존024/legacy빌드/해시 게이트는 변경하지 않았다. v1실패 work/args와 중단한 자체 repro work는 보존했다. 사용자 프로세스/세이브/원본/기존ROM/ZIP은 삭제하지 않았다.

수정 후 현재 primary는 `tools/build_layout500_025.py`이며 원본→024조합→025조합→할당/ExpectedWrites→025전체보존검사 순서다. `tools/specs/primary025_version.json`으로024 base에 대한 정확한5개 변경만 허용한다.024 A3 verifier는 그대로 유지한다. `025_v2` 및 `_repro`의 별도 원본 빌드는 성공했고 byte동일하다. 기존 실패 폴더를 지우거나 덮어쓰지 않는다.

## 실행한 검증 순서 — 다음 배치 작업과 혼동 금지

1. 새 ROM이 실제 작성됐는지와 primary 종료 결과부터 확인. 아직 작성되지 않은 ROM의 ID증가/화면/재빌드 성공을 주장하지 않는다.
2. `verify_layout500_product_025.py --out analysis/pending500_025_v2/integration_pre_repro.json`, 이후 `--repro poc/output/pending500_025_v2_repro.gba`로 최종 integration 생성.
3. `bench_hint_rom_reader_024.py`를 새 ROM의 실제 배치에 실행해 A3/B0두 CPU보고서 생성. `verify_layout500_integrity_024.py --rom ...025_v2.gba --out analysis/pending500_025_v2/integrity.json`으로16손상거부 검사. 이름024인 도구지만 이 CLI는 새 ROM/024 A3유효 manifest를 매개변수로 받는다.
4. `run_layout500_runtime_025.py`는025자체 coldboot/자판/네내비/메일과 choice-confirm/choice-cancel/nickname별 자체 진단을 실행한다. `verify_layout500_normal_025.py`, `verify_layout500_samples_025.py`로 판정한다. 스크린샷 직접 확인은 별도다. 프로토콜/기대값 오류면 실패를 보존한 새 버전 도구로 진단한다. 빌드 메타데이터가 해시로 고정한 도구는 사후 편집 금지.
5. `prepare_layout500_visuals_025.py`로 contact sheets생성/직접 확인, `visual_review.json`에 실제 관찰과 한계 기록. 최종 권위는 추가Yes검증의 `raw_samples_v3.json`을 묶는 **`finalize_layout500_025_v2.py`**로 생성했다. 현재모든하위보고서는 위025 SHA에 묶여있다.

초기 `verify_layout500_samples_025.py`는 B취소결과를2로 가정해 실패했다. 실제source `EC0680FFFFFF`, `BSeparate=false`에서native50662→50732는 마지막옵션1을 선택한다. trace에서5070A취소경로와506A4/506F8의결과1을 확인했다. ROM변경 없이새 `verify_layout500_samples_025_v2.py`가이를검증했고, `v3.py`는추가Yes0/전체8방향이동까지검증했다. `sample_checker_correction.json` 참조. 원본세번째target은보존하지만이설정의B는별도세번째결과를사용하지않는다. 빌드메타데이터가해시로핀한실패체커도수정하지않고보존했다.

## 문구 사전 대조와 미완료

선택된500개 source/translation을100개씩5회 읽어 사전 대조했다. 조사766134:0:0의 ‘넷토’는 원문 `熱斗くん`에 실제로 있으므로 화자/호칭을 추측해 바꾸지 않았다. 반복 선택지의 ‘예/아니요’, ‘좋아/싫어’, ‘응/그만둘래’와 시험30초·재시험100z·1/2차 등 핵심정보는 유지된다. 전체 문구 인간 승인이나 자연 이벤트 문맥 검증은 아니다. 어투/띄어쓰기(예:나1명), 기사/나이트 표현, native이름의 일본어 호칭과 한국어 뒤붙임은 추가 검수 항목이며 frozen wording을 자동으로 고치지 않았다.

자동한글조합→확정→저장→재표시, native kana자판/일본어 호칭/필드 날짜HUD, 기존 구매안내 이미지의 빽빽한 행간, 전체 의미·화자·분기·flag/provider 최대폭·자연이벤트·실기·음향은 미완료다. 이번 표본은 PET root/table read-alias의 격리 진단이며 실제 배틀결정/캐릭터caller/획득·저장 증거로 확대하지 않는다. NON-DISTRIBUTION/needs_review. 사용자가 다시 패키지를 요청할 때까지 새 BPS/xdelta/ZIP은 만들지 않는다.
