# 033 준비 — 253개 소스 컴파일·기존 번역 병합 검증, ROM 신규 적용 0개

## 최신272개 준비 상태로 이관

2026-10-17 현재 준비 권위는 `analysis/pending_insertion_500_033_preflight272_v2/status.json`, 상세 `analysis/PENDING_INSERTION_500_033_SUPPLEMENT19_HANDOFF.md`다.기존253개에일정13/일반6을추가해272개/기존3,035개보존 검증,228개추가필요.사용자는정확500개준비후적용을선택했으며부분253/272ROM은생성하지않는다.실제032ROM/17,122개와패키지금지유지.아래253개기록은이전준비스냅샷으로보존한다.

## 2026-10-17 현재 권위

- 실제 완료 ROM은 **`poc/output/pending500_032_v1.gba`** 그대로다. SHA256 `cc2d02d3fda6ab27601d1735015b24b11d869308dff3e08f0fd4f06f31518f64`, 12,418,796바이트, 누적 **17,122개**. 완료 권위는 `analysis/pending500_032_v1/batch_status.json`이다.
- 이번 준비 권위는 **`analysis/pending_insertion_500_033_preflight_v1/status.json`**. 신규 적용 **0개**이며 033 ROM, BPS, xdelta, ZIP은 만들지 않았다. 500개 단위 ROM 적용과 별도 요청 전 패키지 생성 금지 정책을 유지한다.
- 원본, 032와 독립 재빌드, 이전 보호 파일, 032 메타데이터에 고정된 도구 해시가 그대로임을 최종 검사했다. 모든 실행 세션 종료. 목표·자동화·서브에이전트 없음.

## 진행한 내용

1. 기존 `survey_batch500_016.py`의 CLI에 실제032 ROM/통합 검증 보고서를 명시해 새 `analysis/pending_insertion_500_033_survey_v1/survey.json`을 생성했다. 예전030 기준 조사 결과를 새 기준으로 오인하지 않는다. 이 단순 조건의 후보는 0개이며, 압축 저장·다른 렌더러·동적 삽입 등 제외 조건을 해제하지 않았다. 조사 결과의 원인별 수는 겹치는 스크립트 수이지 잔여 미번역 수가 아니다.
2. **`tools/survey_aggregate_pet_033.py`**로 원본에 정확한 PET 초기화(92,110/132픽셀)를 가진 미적용 RAW 전체 스크립트만 조사했다. 기존 단일 문구 폭이 아니라 닉네임·프로필·칩 이름 등 조건부 삽입 폭까지 합쳐 LF 위치를 탐색했다. 번역의 단어·단어 사이 공백·보호되는 선후행 LF/패딩·제어 코드·페이지 대기/지움 명령은 변경하지 않았다. 기존 엄격한 소비 검증기가 최종 배치를 별도로 재검사한다. 이 탐색은 제품 빌드에 들어가지 않는 분석 절차다.
3. `analysis/pending_insertion_500_033_aggregate_v1/survey.json`: **253개/97스크립트/31아카이브**, 명시적인 LF 배치 변경 **103개**. 소비 유형은 `pet-flags=23`, `pet-native-nickname=8`, `pet-direct-profile=122`, `pet-native-chip-profile=32`, `pet-array-conditional=66`, `pet-extended-native=2`이다. 500개 조합은 아직 없다.
4. **`tools/test_aggregate_pet_033.py`**: 독립된 짧은 합성 예제로 정상 7건, 거부 7건 통과. 변수 앞뒤 합산, 단어를 자르지 않는 배치, 공백/빈 행 보존, 미등록 변수·인자·좌표·제어 변경·닫히지 않은 페이지·표현 불가 이스케이프를 검사한다. 실제 게임 실행이나 의미 검수 결과가 아니다.
5. **`tools/prepare_aggregate_pet_033.py`** → `analysis/pending_insertion_500_033_aggregate_selection_v1/selection.json`: 253개의 고유 ID, 실제032 적용 ID와 비중복, 고정된 초안/원문/배치/기존 소비 검증 결과를 재확인했다. 기존 canonical `needs_review` 문장은 그대로이며 새 번역 작성 수로 세지 않는다.
6. **`tools/compile_aggregate_pet_033.py`** → `analysis/pending_insertion_500_033_compile253_v1/verification.json`: 31개 전체 아카이브 원문 바이너리 왕복 일치, 번역 의미/제어/바이너리 왕복 일치, 미선택 원문 스크립트 바이트 보존, 16비트 오프셋 범위, 실제032 ROM 내 **390개 사용 글꼴**과 고정 BDF 일치 통과. **소스 전용 전체 아카이브는 미선택 일본어를 유지하므로 누적 ROM에 그대로 덮어쓰면 안 된다.**
7. **`tools/merge_aggregate_pet_carry_033.py`** → `analysis/pending_insertion_500_033_carry253_v1/preflight.json`: 원본과 고정된 입력/소비 범위에서 실제032의 기존 **2,750개**를 재구성했다. 032는 바이트 비교 기준일 뿐 빌드 입력이 아니다. 기존 번역·풍부한 배치 메타데이터·소비 계약 및 신규 스크립트 외 바이트를 보존하며 253개를 병합했다. 31개 병합 데이터의 왕복 검증 통과. **아직 ROM에 등록·배치하지 않은 사전 검사다.**
8. **`tools/finalize_aggregate_preflight_033.py`**가 신규 ID·컴파일·병합 일치, 실제032 부모 바이트와 기존 배치 메타데이터, 미선택 스크립트, 이전 보호 파일/도구 해시, 033 ROM 부재를 다시 확인해 현재 준비 상태를 기록했다.

## 다음 작업

- 다음 실제 적용은 **500개 묶음**으로 한다. 현재 준비253개에 **안전한 247개가 추가로 필요**하다. 247개는 전체 게임 잔여 수가 아니다. 기존 일정21루트의 일본어13개도 별도 후보 범위일 뿐 적용 준비가 끝난 것으로 세지 않는다. AquaMan 추가 `soundDisableChoiceSFX` 배치/제어 계약과 남은 캡션의 원본 범위를 확인해야 한다.
- 이번31개 중 **20개는 027/028/030에서 새 RAW로 추가했던 아카이브**다. 목록은 현재 `status.json`의 `affected_prior_appended_archives`에 있다. 다음033 주 빌드는 이20개를 **각각 단 한 번 배치하기 전에** 신규 입력까지 명시적으로 합성해야 한다. 032의 `guard_unaffected_appended`를 끄거나 검사 범위를 넓혀서 통과시키면 안 된다.
- 전체500개가 준비되면 고정 입력·기존 소비/변수 조건·명시 LF 배치 검사를 주 빌드에 등록하고, 원본 기반 누적033 ROM → 독립 재빌드/전체 Expected Writes 및 꼬리 크기 → 실제 새 ROM의 CPU/렌더·글꼴·OBJ·픽셀·지움/복귀/재진입을 확인한다.
- 253개에는 정상 원본 입력 기록·캐시 준비/수명 등 기존 조건부 변수 전제가 남아 있다. 합산 폭/컴파일 성공만으로 모든 입력 작성자·캐시 상태·자연 진입 경로가 검증됐다고 주장하지 않는다.
- 한글 자동 조합→확정→저장→재부팅 후 재표시, 환영문구 겹침, 이미지/공유 요일 등 일본어, 전체 게임 및 의미·말투 검수는 여전히 미완료다. 이번에는 새 ROM 화면 테스트를 수행하지 않았다.

## 보존 및 실행 주의

이번 도구도 보고서의 입력 해시에 고정됐다. 후속 변경에는 새 버전 이름을 사용한다. 이미 사용한 출력 경로에 선정/컴파일/병합/최종화 도구를 재실행해 덮어쓰지 않는다. 원본·기존 ROM·저장 파일·초안·이전 패키지·증거를 보존한다. 패키지는 사용자가 다시 요청할 때만 생성한다.

완료 명령: `python tools/test_aggregate_pet_033.py`, `python tools/prepare_aggregate_pet_033.py`, `python tools/compile_aggregate_pet_033.py`, `python tools/merge_aggregate_pet_carry_033.py`, `python tools/finalize_aggregate_preflight_033.py`. 모두 해당 고유 출력 경로에서 한 번 실행 완료했다.
