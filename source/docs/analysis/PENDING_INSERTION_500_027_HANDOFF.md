# 027 다음500개: 실제 ROM 반영·독립재빌드·최대 프로필 표본 검증 완료

- 요청: 중단 지점부터500개씩 ROM에 적용. 별도 요청 전 BPS/xdelta/ZIP을 만들지 않는다.
- 실제027 ROM: `poc/output/pending500_027_v1.gba`.
- SHA256: `2353a0077b7655abb0abb3f3ba8ca95d4242112931e3dddaccb16f27527f2a0d`.
- 12,289,028bytes; 실제026의14,122개에 신규500개를 더해14,622개.
- 158개 whole script / 새 RAW archive11개 / 명시적인 줄배치24개. 초안 문구는 바꾸지 않았다.
- primary418 / 원문 catalog 물리적 비변경314. 314는 잔여 미번역 개수가 아니다.
- 이500개는 이미 적용됐다. 다음 선정 시 실제027의 ID와 cumulative027.scope를 사용한다.

## 원본 기반 재생성 경로

`prepare_layout500_027.py` → `compile_layout500_027.py` → `merge_layout500_carry_027_v2.py` → `layout500_inputs_027.py` → `build_layout500_027.py`.

027은 기존 적용 archive의 덮어쓰기가 아니라 새 RAW11개의 등록이다. 이전024/025/026 입력의 합성을 유지하고, 검증한 immutable source/native payload와500개 입력을 기존024 방식의 확장영역에 배치한다. 이전026 ROM은 비교 기준이지 빌드 원본이 아니다. 원본 payload와 비선택 script를 보존하고 catalog의 모든 해당 포인터를 ExpectedWrites로 갱신한다. `tools/specs/primary027_version.json`에 frozen026 대비 정확한5개 코드 변경을 기록했다.

## 현재까지 통과한 검사

- 원본/번역/역추출 바이너리 roundtrip,500개 disjoint ID,478개 실제026 글꼴.
- source-bound 입력 게이트, 직접 프로필 모델29개 fixture, 실제 입력 게이트 손상 거부14개.
- `analysis/pending500_027_v1/integration_pre_repro.json`: 기존 소비자458개 payload/메트릭 유지, 새 RAW11개/500개, source storage/포인터/owner/ExpectedWrites/전체diff.
- 실제027의 프로필 cap-load/input/flatten/commit/F90C CPU: source+027 합계304개. 고정 CpuSet clear와 sound만 모델링하며 native helper는 실행한다.
- 실제027 A3 CPU5,652 / B0 CPU6,341개. native-control byte identity transfer도 통과했다.

독립 재빌드 `_repro.gba`는 첫027 ROM과 전체byte 동일하다. `integration.json`이 실제500 delta/기존458개 소비자/새 RAW11개와 repro를 확인했다. 같은027의 coldboot/초기설정/기존 자판3페이지/네 내비/첫메일23쪽·복귀·재열기도 PASS다. max8 및 max4 프로필을 끼운2쪽의 source/RAM glyph→font CPU→OBJ/pixels·독립 합산 줄좌표/빈배경·keyWait/PET복귀를 검사했다. 신규 고유문구3개가 픽셀 검증된 표본이며500개 전체를 실행한 것은 아니다. 22초기설정/23메일/5raw 화면을 직접 봤다. 현재 기계 판독 권위는 `analysis/pending500_027_v1/batch_status.json`이다. 이 체크포인트는 배포 승인이나 전체 요청 완료가 아니다.

## 진단과 한계

검증한 직접 필드는 학교/좋아하는 음식/꿈/좋아하는 사람/동경하는 사람/라이벌/잘하는 과목/못하는 과목이다. 폭은 native editor의 논리 입력 상한8 또는4와 source441개 metric의 최대11px에서 도출했으며 descriptor의17/9bytes를 글자 수로 간주하지 않았다. 정상 native record에 한정하며 친구/취미/희망 등의 배열 필드와 임의·손상·가져온 세이브의 안전성을 승인하지 않는다.

화면 시험은 격리된 PET root/table read alias와 F90C 직전 임시 최대길이 native record를 사용한다. 실제 입력 가능한 E406(ゃ) 토큰을 복사한 뒤 원래 필드 bytes를 복원한다. 실제 native reader와 글리프 소비를 검증할 수 있지만 자연 획득/모든 writer/default/import, 실제 화자/caller, 저장/재로드 또는 한글 입력 지원의 증거는 아니다.

이전 실패와 수정은 `analysis/pending_insertion_500_027_checkpoint_failures.json`에 기록했으며 기존 도구·실패자료는 남겼다. 자동한글조합→확정→저장→재표시, native kana/일본어 호칭·날짜HUD·타이틀로고, inherited welcome bitmap 행간/겹침, 전체 문맥·자연 이벤트·플레이·하드웨어/음성 검수는 미완료다. `65CC78:43`은 “오늘은 … 과목은”의 겹치는 주제 표현을 추가 문장 검수 대상으로 기록했으며 이 개발본을 문구 승인으로 보지 않는다. NON-DISTRIBUTION/needs_review이며 완성판이 아니다. 원본/이전 ROM/세이브/기존ZIP의 해시7개를 확인했고 새 패키지는 만들지 않았다.

## 다음 재개

실제027의 적용ID를 제외하여 다음500개를 선정한다. 027에서 새로 채택한11개 RAW 영역은 다음 누적 병합에서 effective translation owner와 `cumulative027.scope`를 사용한다. source-bound carry 재구성 순서는024→025→026→027이며, 새 영역을 원문만으로 다시 컴파일해 이미 적용된500개를 지우지 않는다. 이500개를 다시 선정하거나 이전026을 최신으로 잘못 사용하지 않는다. 별도 요청 전에는 ROM 작업만 진행한다.
