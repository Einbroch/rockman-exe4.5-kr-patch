# 024 재개 지점 — 미적용500개 ROM 반영·재빌드·표본 검증 완료

2026-10-15. 현재 기계 판독 권위는 `pending500_024_v1/batch_status.json`이다. 최신 개발 ROM은 `poc/output/pending500_024_v1.gba`, SHA256 `206f130070538fe1ca4fb7a7534045afeb210dc4959f290fd631f60429dc048e`,12,176,264bytes / 누적13,122개다. 원본·023·022·기존ZIP 해시 보존 PASS, 사용자 세이브 편집/새 BPS·xdelta·ZIP 생성 없음. needs_review/NON-DISTRIBUTION, release_eligible=false. 이전 checkpoint v1/v2/v3/v4는 준비 단계의 이력이다.

## 최신 진행: 실제500개 누적 ROM·동일 재빌드·CPU/화면 검증 완료

현재 primary 명령은 `python -X utf8 tools/build_layout500_024.py`, 독립재빌드는 `--repro`다. 이전023 인자 파일을 해시 검증해 새 work/out 좌표만 선택하고, `tools/specs/primary024_version.json`의 명시적인8개 primary 연결점과 A3 최종검사 버전 차이를 검증한다. `build_development_patch_024.py`는 `layout500_inputs_024.load_inputs`를 원본 입력 경계에서 호출하고 기존48raw/신규2raw 및19A3를 **최종 할당 전**에 합류시킨다. 기존023 production 모듈과 모든 frozen hash gate는 그대로 보존했다. 원본에서 최종 제품을 조립하며023 ROM을 입력으로 덧패치하지 않는다. 패키지는 생성하지 않는다.

`pending500_024_v1/integration.json`: 실제 신규500-ID delta/기존ID 누락0·389개 무변경 소비 payload 및67개 병합 소비자의 기존 문구·rich metrics·비신규script 보존/입력 소유권·전체 포인터·source storage·Expected Writes·header·증가 tail을 포함한 전체diff PASS. 총13,122/primary407/원문 물리 미변경325archive다. 원본에서 별도 재실행한 `_repro.gba`와 전체byte 동일 PASS. 전체 immutable source가 모든 glyph/코드/그래픽/clone의 입력이며 이전023은 비교 기준만이다. A3가364→521개로 늘어도 native 압축/포인터/비교복사본/native RAM 및255script×19Navi/23descriptor 구성을 보존한다. B0500/21archive와 기타clone 검증을 유지한다.

`a3_cpu.json`5,652조건 / `b0_cpu.json`6,341조건: **실제024 최종 주소의 코드**에서 native ABI/분기/root/scene/Navi/full-native 비교/등록표/모든script offset·fallback·RAM 무변경 검사 PASS. `integrity.json`: 정상제품 수용 후 A3/B0 compiled payload·native 비교복사본·descriptor·원래 pointer·record/layout/asset 손상16fixture를 모두 거부했다. CPU/손상fixture는 자연 게임플레이나 pixels 증거와 구분한다.

`normal_runtime.json`: 같은024에서 정상 부팅/초기설정·기존 일본어 자판3페이지의 VRAM bank/map/동적field·네내비의 native bank/OAM·첫메일23개 순서대로 keyWait/native3archive load/bookmark/목록복귀·재열기 PASS. 이전 startup 감사의023 전용 count/lineage 검사를 우회하는 대신024 독립 product 감사와 현재ROM VRAM/consumer 검사를 사용한다. 해당 기계 보고서의 visual_review_pending은 별도 visual 보고서에서 다루며 자체적으로 인간 승인을 부여하지 않는다.

`raw_displays.json`: WindMan3의2쪽(새 LF 포함), PET65B9E8:94의1쪽(92,110), 신규778CC0:48의1쪽(52,110)을 actual font CPU reads→원래 row offsets→OBJ→pixels/keyWait/빈영역 잔상 및 원래65A608 록맨PET 복귀까지 검증했다. 원래 창·초상 명령을 그대로 실행한 root/table read-alias 진단이며 원래 이벤트/화자 분기가 이 대사를 골랐다는 증거가 아니다. 진단 상태는 quarantine했다.

`a3_runtime.json`: 신규786D38:10/26을 각각2회 표시해 원래 압축 로드→native RAM→전체native guard→ROM clone→font CPU/OBJ/pixels·2/3행·keyWait·지움·종료4회/재진입 PASS. loader/scene/table read-alias를 썼지만 원래 flags/요일 명령은 그대로 실행하고 flag/RAM/ROM은 수동 변경하지 않았다. 첫 capture v1은 시작이 바로mugshot/msgOpen이어야 한다는 기존 표본 가정으로 **에뮬레이터 실행 전에 거부**됐다. 실제script10/26은 원문 조건/요일 검사가 먼저 온다. 실패 도구를 보존한 채 v2에서 원래 guard prefix 전체와 opener가 동일한지 검사해 실제명령을 실행했다. ROM 수정이나 조건삭제로 통과시키지 않았다. `run_layout500_a3_samples_024.py`가 같은024의 기존 weekday-pagecycle 상태에서 이 두 표본만 재개한다.

`natural_b0_runtime.json`/`exit_runtime.json`: 실제 Monday/B0/록맨 상태에서 평상시 L입력으로 기존 B0 script0→default10을2회 실행했다. loader/scene/table/progress aliases 없이 font CPU/OBJ/pixels·native RAM lifetime·keyWait·닫기/재진입 PASS. E5/비활성 context/대사·커서palette14 OBJ 제거도2회 확인했다.

`visual_review_initial.json`과`visual_review_hints.json`: 초기설정/카드22화면·첫메일23쪽·raw/복귀7화면, A3표본4쪽·B0표시2쪽/닫기2화면의 비교표를 직접 검사했다. 신규 표본의 잘림/잔상은 보이지 않았다. 기존 PET 구매안내 이미지의 겹치는 행간과 필드 일본어 날짜HUD·일본어 자판/호칭은 여전히 열린 항목이다. 실제 화면은 각각 startup_contact.png/mail_contact.png/raw_contact.png/a3_pages.png/natural_b0_pages.png에 있다.

**다음 재개는 actual024 적용ID 기준이다.** 이500개를 재선정/재번역/재적용하지 않는다. 향후 병합은 현재 effective owner와`cumulative024.scope`를 소비해야 한다. 기존022까지만 복원하는 registry 함수나023 전용 generic startup/364-A3 verifier를 새제품의 권위로 쓰면 안 된다. 현재 canonical 입력 gate/버전 primary/독립024감사를 유지하며 다음 미번역500개와 실제 소비 경로를 조사한다. 자동한글조합→확정→저장→재표시, fixed flag 사건 효과/자연 A3 provider·분기, 전체500 의미/사람 승인·전체플레이·실기/음향은 미완료다. 새 패치 파일은 사용자 요청 전까지 만들지 않는다.

## 이전 준비: 기존3,191개 보존·새500개 누적 병합 및 입력 gate 완료

`pending_insertion_500_024_carry_v1/preflight.json` SHA256 `0de493ef372fb5a138a018ec44548f6a2a49131b5824b81566364fb4742bf9e5`: 69archive 모두 원본 및 고정 asset/scope에서 기존023 payload를 복원해 실제023과 전체byte 동일함을 확인했다. 이 기존3,191개와 새500개를 병합해 컴파일/역변환/바이트 재조립, 비신규script bytes, 기존 literal의 소비 계약과 폭 보존 PASS. 48개 기존 primary raw/2개 신규 raw(693590·778CC0)/19개 A3 clone이다. 023은 비교 기준으로만 읽었고 새 payload의 원본 입력으로 사용하지 않았다. 기존 production 코드와 고정 preflight는 변경하지 않았다.

`tools/layout500_inputs_024.py`의 `load_inputs(source)`는 할당 전에 호출할 수 있는 별도 누적 입력 gate다. 고정 carry manifest/모든 연결 파일 해시, 원본 TPI row·payload, 실제023 parent bytes·carry asset/ID/소비 계약, 일본어-bearing literal의 완전 script group, 원문 명령 및 단어 불변, 새500개와 기존 적용ID 교집합0, 다섯 창 profile의 현재 aggregate page geometry와 비신규script bytes를 다시 검사한다. `pending_insertion_500_024_input_gate_v1/verification.json` PASS. 이 gate는 **아직 primary build에서 호출되지 않으며 ROM 적용 승인/할당/실행 증거가 아니다.**

새 거부 테스트12개(잘못된 원본·ID 중복/누락·script·문구·검수상태·prose 변경·target·소비 profile·고정 geometry·기존script bytes 손상)와 기존 공간 검사28개, 총40개 PASS. gate 구현 초기에 기존 carry의 검수상태/일본어가 아닌 구두점과 ShadowMan의 이미 채택된 A3 줄배치를 잘못 가정한 검사가 거부됐다. 원문·문구·기존 gate를 완화하지 않고 기존 input 단계의 effective asset/translation policy를 재사용하도록 정정했으며 checkpointv4에 기록했다.

**다음은 선정·번역·carry 컴파일 반복이 아니라 primary 통합이다.** 기존023의 frozen tool hash를 깨지 않는 명시적인 versioned primary entry에서 `load_inputs`를 호출하고 raw48+2 및 A3 19 병합본을 할당 전에 연결한다. A3의 기존364→누적521개 검증은 versioned verifier로 전체 유지하고 기존 B0500/기타clone/reader 조건을 보존한다. 변경 입력의 소유권·metadata·포인터·Expected Writes·exact500 delta/누적 lineage 검사를 등록하고 원본에서 독립 product/repro를 만든 뒤 같은 새ROM으로 CPU/GBA font→OBJ→pixels·clear·exit/reentry를 검증한다. 자동 한글 확정/저장/재표시·실제 조건/flag 분기·전체 인간 검수는 여전히 미완료다.

## 이전 진행: exact500 선정·source-only 컴파일 및023 공유 renderer 표본

`pending_insertion_500_024_selection_v1/selection.json`은275개 완전 script group/69archive의 실제 미적용500개를 고정한다. 구성은 기존 큰 창187/PET85 + 추가 normal186/고정flag PET40 + 윈드맨 성공 대사2개다. raw343/A3 clone 합류157이며 B1 복제 문구나 기존 적용 문장은 집계하지 않았다. 문구는 전부 기존 고정 초안을 연결했다. 마지막`7C802C:3:1`의「그럼, 앞으로 나아가겠네...」는 단어를 바꾸지 않고 같은 waited page 안에서 LF1개를 추가했다. source literal/조건 분기/flag/기다림/페이지/초상 명령의 순서·인수는 보존한다. 새 조건부 진입/flag 모델은 공간 검사이며 실제 분기 효과·도달의 승인이나 생산 gate가 아니다.

`pending_insertion_500_024_compile500_v1/verification.json`: exact500/69archive의 원문 전체byte왕복, target→binary→TPL literal/명령 동일, 재조립 binary 동일, 비선택 script bytes 보존 PASS. 실제023 font의 확장glyph496개 대조 PASS. LF 수가 달라지는 literal은69개이며 모두 문구 불변·기존 페이지 내부 배치 제안이다. 기존272개 자료를 버리거나 재번역하지 않았다. 새로운 후보 코드의 검사14개와 기존PET 검사14개 PASS.

`pending_insertion_500_024_shared_runtime_v1/verification.json`: **이미023에 적용돼 있던**71551C script17을 같은023의 정상 초기 PET caller에서1회 root/table read alias로 표시했다. msgOpen→mugshotShow 순서/52,110 원점/1→3→1→2행4page의glyph CPU reads·native offset·OBJ→pixels·keyWait·빈 영역 잔상 검사 PASS. source의연속E5 E5 중 첫E5에서 context 비활성을 실제exec callback으로 관측했고, 두 번째E5는실행하지 않고 원래 록맨65A608 PET의EDFF 대기로 복귀했다.4page+복귀 화면을 직접 확인했으며 표본 기하/잔상 문제는 보이지 않았다. 계정/의미/인간 승인이나 새024500개 실행 증거는 아니다. aliases/checkpoint는 격리했고 ROM/RAM/진행/세이브 쓰기 없음.

최초 runtime v1의4page 검사는 통과했으나 step11에서 context가 계속 비활성이어야 한다는 verifier 가정은 실패했다. 실제로는 새 정상 PET 안내창이 즉시 열린 것이었다. v1 자료를 보존한 채 v2 관측에 종료handler 진입/비활성 전환callback만 추가해 원인을 구분했다. 정상 PET text OBJ가 남아 있는 것을 NPC 대사 잔상으로 처리하거나 검사를 임의 완화하지 않았다.5화면 비교표는 위 shared-runtime 폴더의`normal_order_pages.png`다. source-only500과 이023 공유 소비 경로 표본을 구분한다.

v3 당시의 carry 합류 과제는 위 v4에서 완료했다. 원문만 포함한 source-only complete binary를 기존ROM payload 위에 덮어쓰는 방식은 여전히 금지다. 입력 gate가 새ROM 통합/전체 사건 검증을 대신하지 않는다.

## 이전 진행:272개 source-only 컴파일 및 native 명령 CPU 확인

`pending_insertion_500_024_compile_v2/verification.json`: 후보272개/58archive를 실제 메시지 binary로 컴파일했다. 모든 archive의 원문 TPL→binary가 원본 payload와 전체 바이트 동일, 번역 target→binary→TPL literal/명령 구조 동일, 재조립 binary 동일, 비선택 script bytes 동일 PASS.023의 기존 적용ID와272개 교집합0이다. 선택 문자에 필요한 확장glyph376개를 실제023 font bytes와 대조했다. **source-only payload에는 나머지 원문이 들어 있으므로023 ROM의 기존 한글 payload에 직접 덮어쓰면 안 된다.** 적용/생산 gate/기존 번역 합류/실행 PASS가 아니다.

PET85개 중58개 literal은 문구·단어 공백·기존 기다림/페이지를 유지하면서 LF 수를 늘리는 제안이다. 이 제안의 native 명령 전제는 `pending_insertion_500_024_native_controls_v2/cpu.json`에서 원본과023의 같은 명령을 실행해72조건으로 확인했다. 정상 E8 draw handler08050380의 행 offset은0/10752/21504이며 세 번째 LF(네 번째 행)는context+8C=1로 초과 상태가 된다. width용 E8 handler080503B0은 폭 누적을0으로 초기화한다. F1 clear080510BC→0805543C는context의 행/폭/render offset을0으로 만들고EWRAM02012F50와02013E50의연속 두3840byte staging 버퍼를 모두 지운다. EDFF waitHold는stream을 진행시키지 않고 대기 플래그를 설정한다.

CPU 검사는 TI925T/Unicorn의 고정 입력이며080EC140의SWI0C CpuFastSet만 정확한zero-fill 목적지/개수 계약으로 대체했다. 실제 BIOS/VRAM 전송·glyph pixels·음향·자연 PET 이벤트·새024 ROM 실행 증거가 아니다. v2는v1과72case 효과가 전부 같고, 전역 플래그/두 번째 버퍼를 가리키는literal까지 source applicability 범위에 명시했다. v1은 이력이다.

첫 source-only compile v1은661858 원문 TPL의script29에서 nickname 뒤 선행LF(E8)1byte가 사라져5121→5120byte가 되므로 중단했다. 실패 폴더를 보존했다. 원본/고정 TPL/문구는 변경하지 않았다. v2의 임시 TPL에서 모든 literal을 기존`tpl_literals.serialize`로 표기해 선행LF를명시적escaped형식으로 바꿨고, literal 값/명령 구조 동일과 원본 전체byte왕복을 통과했다. 같은 문제를 번역 수정이나 원본 byte 허용 오차로 처리하지 않았다. CPU 조사 초기에 대상외F9 slot까지 비교한 범위와 두 번째clear destination을VRAM으로 예상한 가정도 실패했으며, 실제 native literal/호출의 EWRAM staging 경로로 정정한 뒤에만 PASS를 기록했다.

이전272개 단계의 다음 과제였던228개 추가 확보는 위 exact500 선정으로 대체됐다. 아래 과거 집계와 조사 순서는 이력이며 현재 재개 지시가 아니다.

## 기준과 실제 결과

- ROM `poc/output/pending500_023_v1.gba`, SHA256 `6e6d9104db33fd927714b4a06cd6a1093fd4b6ef6d4f77c6ecd206daa44a39ec`.
- 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
- 이전 적용/CPU/정상 실행/화면 결과는 `PENDING_INSERTION_500_023_HANDOFF.md`와 `pending500_023_v1/batch_status.json`에 보존한다. 이번 분석을 새 ROM의 실행 검증으로 표시하지 않는다.
- 고정 초안 coverage SHA256 `d6f187e8068458394506e9652f4d5d911b33bc728ec3ab90a434dc2afd2d6b65`. 기존 번역 문구와 고정 초안을 수정하지 않았다.

`pending_insertion_500_024_survey_v1/survey.json`: 기존 엄격한 raw/132px/동일 줄 수 계약은1개 후보뿐이고 exact500을 만들 수 없다. 제외 이유는 겹치는 집계이며 전체 게임의 미번역 잔여 수가 아니다.

`pending_insertion_500_024_fullbox_v1/survey.json`: 큰 창/이름·칩 삽입의 기존 기하 모델에 맞는 **187개**(변수93/일반94, raw53/A3 clone 합류134)를 분리했다. 이는 B0용 source-bound 생산 gate를 다른 archive에 적용한 것이 아니다. 새 source-bound gate와 기존 번역 합류/소비 경로 검증 전까지 product_admitted=false다.

`pending_insertion_500_024_quick_reflow_v2/survey.json`: 정확한 PET 명령 prefix와132px×최대3행, 원래 keyWait/clearMsg 순서, waited→cleared→terminal waitHold 형태에 맞는 **85개**를 분리했다. 원래 단어·공백과 페이지 수를 유지하고 기존 페이지 안에서 LF를 추가하는 **분석용 제안**이다. 기존 `tpl_literals.replace_literals`의 동일 LF 수 정책을 변경하거나 우회해 제품을 빌드하지 않았다. 본문/폰트/코드/창 위치 변경 없음.

두 후보 집합의 ID 교집합0, 합계272개다. 아직500개를 구성하지 못했으며,272개도 ROM 반영 가능한 최종 승인 집합이 아니다. 원래 동일 줄 수 quick 조사0개와 첫 reflow 조사0개는 `quick_v1`/`quick_reflow_v1`에 실패 증거로 남겼다. 당시 모델은 waited→cleared→waitHold를 처리하지 못했다. v2는 이 종료 형태를 분석 모델에만 추가했다. 과거 보고서는 현재 모델의 재실행 결과가 아니며, 배포/도입 근거로 쓰지 않는다.

`tools/test_pet_quick_capacity_024.py`:14개 PASS. 합성된 긴 문구/합성 literal 합산 overflow/4행/미지원 명령/clear 전 hold/wait 후 text/구조 변경/미등록 ID/변경된 source/비분할 긴 단어/보호 padding 거부, 문구 동일 LF 확장 검사다. 첫 실행의44px 예상값을80px로 잘못 작성한 테스트1개는 기대값 수정 후 통과했다. 실제 ROM 실행 검사가 아니다.

## B1 힌트 중복 — 신규500개로 세지 않음

원본 root0x53FA0의 B0/B1/B2 슬롯은0x54060/64/68→0x08054238/294/2F0이다. B1은 다음B2 table 시작으로 경계가 고정된23슬롯이며 null13/14를 제외한21개를 원본에서 해제했다. **모든 B1 payload가 같은 Navi의 B0 전체 decoded bytes와 동일**하다. archive별 위치/압축 범위·hash/decoded hash/원본 저장소 불변은 checkpoint에 보존했다. 같은 문구 재등록을 신규500개로 집계하지 않는다.023 reader는 B0 scene만 추가 지원하므로 이 조사만으로 B1 한국어 표시를 주장하지 않는다. B3 root의0x0877994C는 archive 포인터이므로 B2의 다음 Navi-table 경계로 추정하면 안 된다.

## 이미 일부 적용된 script 조사

`script_has_applied_ids` 거부 script 중 아직 적용되지 않은 일본어 정규식 일치 literal이 있는 것은8script/20개였다. 이20개는 timed middle-dot literal이다. 해당 script들의 실제 문장 번역(롤 운세/Guts 일정/록맨·롤 도주)은023 metadata에 이미 등록돼 있다. 고정 draft-first coverage는 모든 과거 번역 자산의 목록이 아니므로, coverage에서 문장이 안 보이는 것을 미번역으로 단정하지 않는다. 기존 문장을 다시 번역하거나 count를 늘리지 않았다.

## 이전 단계의 판별 작업 이력 (현재 재개 순서는 맨 위 참조)

1. PET quick 대표 문장의 LF(E8)→행 위치→최대3행→clear/종료/재진입 lifetime을 실제 소비 코드/023 진단으로 연결한다. 추가 LF는 문구 변경/새 페이지가 아니지만 기존 생산 정책과 달라 명시적 source-bound layout profile이 필요하다. 구조 보존만으로 소비 안전을 주장하지 않는다.
2. `msgOpen` 후 `mugshotShow` 순서의 미적용 문장과 기존 분석의 미지원 명령 집단을 구분해 나머지 후보를 확보한다.500개를 채우려고 미지원 변수를 허용하거나 창 범위를 늘리지 않는다. 긴 문장을 자동 축약하지 않는다.
3. exact500/원본 byte 왕복/포인터·storage·carry 검증/모든 기하 검사 후 별도024 생산 빌드와 독립 재빌드, 최종 Expected Writes·차이, 실제 ROM CPU/관련 실행 및 화면 검증을 진행한다. frozen023 gate dependency나 과거 preflight를 덮어쓰지 않는다.

전체 완성 조건인 자동 한글 조합→확정→저장→재표시, 일본어 자판·호칭·날짜 HUD, 초기 안내 행간과 전체 의미/화면 검수는 여전히 열려 있다. 이번 후보 조사가 이 조건을 완료하거나 사용자 범위를 줄이지 않는다.
