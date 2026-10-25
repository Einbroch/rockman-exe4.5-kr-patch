# 022: 미적용500개 ROM 반영·독립 재빌드·대표 소비 검증 완료 (개발본)

## 최종 현재 상태 (2026-10-15, 아래 진행 기록보다 우선)

`poc/output/pending500_022_v2.gba`: SHA256 `7363567b1263dac0700e2430da1046e47aa9ba65c8d9c2125b1ab9b3bd2928a1`, 12,059,324bytes. raw136+압축 진행 힌트364의 실제 신규500-ID delta로 누적12,122개/primary405/source payload 물리적 미변경327archive다. `pending500_022_v2_repro.gba`는 원본·고정 입력에서 다시 전체 컴파일한 별도 ROM으로 전체 바이트 동일하다. 검증된 최신 개발본을022로 갱신한다. 전체 게임/자연 경로/자동 한글 입력 완료나 배포 승인은 아니다.

현재 기계 판독 권위는 `analysis/pending500_022_v2/batch_status.json`이며 모든 하위 보고서 해시를 묶는다. `integration.json`에서 source/header/Expected Writes·전체 final diff·모든 포인터·ISA·이전 배치 ancestry·실제500-ID/기존 누락0·이전 payload/비신규script/소비계약·선정asset lineage·독립 재빌드 전체 byte identity PASS. `hint_cpu.json`은 실제 최종 배치5,652조건, `selector_cpu.json`은 기존 reader3,195조건, `hint_integrity.json`은 손상 거부11fixture PASS. 큰 창 용량·문구 불변 줄 배치 계약 테스트16개도 통과했다.

`normal_runtime.json`: 새022 cold boot와 그 ROM의 own checkpoint만으로 초기설정/기존 일본어자판3페이지/선택 가능한 네 내비/첫메일23쪽·메일 목록 복귀·재열기 검증 PASS. `display_runtime.json`: 힌트 script11(2행)/15(3행)을 각2회 표시하고 닫기·재진입, raw7CB850/script0의3쪽과 carry7CAF40/script5의2쪽, 총9쪽의 정확한 glyph stream/CPU font reads/OBJ VRAM·화면pixels/keyWait/잔상 제거 PASS. 힌트 원본 RAM은 load 뒤·두 번의 reader 선택 전·대기 및 exit 동안 전체 바이트 동일했고, 정상 B0 native hint는 root0x0203D800을 유지하는 fallback PASS였다. Mesen 표본 wrapper CPU cycle은59,490~59,492다. 원래 compressed payload/모든 포인터와 loader는 제품에서 변경하지 않는다.

`hint_dispatch.json`은 추가적인 원래 dispatcher 진단이다. 같은-ROM preload에서 loader와 scene read만 별칭 처리하고 script0 table 값은 그대로 반환했다. 원래 script0 jump 및 script10 flag 검사/default 일본어 본문이 ROM clone에서 실행되고 대기·닫기·재진입하는 것을 확인했다. 원본 script0/10 바이트 동일, world ctx는 여전히 B0/Navi0, native RAM 전체 보존이다. script10은 아직 미번역이며 이 검사로 추가 번역을 세지 않았다. 이 실험도 자연 A3 진행/분기 전수 검증은 아니다.

직접 본 비교표는 `display_runtime.png`, `hint_exits_v1.png`, `startup_pages_v1.png`, `mail_visual_pages_v1.png`다. `visual_review.json`은9표시/7고유원문 표본 대조를 기록하며 전체500개 사람 승인이나 모든 내비 provider 검증으로 확대하지 않는다. 원래 mugshot/msgOpen 제어는 보존했다. 초기 구매 안내의 빽빽한 행간은021과 텍스트 crop RGB/두 welcome payload 해시가 같으며 OPEN_INHERITED다. 필드 상단 `1月3日(月)`은 별도 미번역 HUD로 관측·기록했다.

원본/020/021/기존 ZIP 해시 보존 PASS는 `protected_artifacts.json`에 있다. 새 BPS/xdelta/ZIP을 만들지 않았고 이전 ROM/사용자 세이브/증거를 보존했다. needs_review/NON-DISTRIBUTION, release_eligible=false, complete_integrated_request=false를 유지한다. 최초 v1 실패 작업 폴더도 삭제하지 않았다.

### 다음 작업과 열린 완료 조건

1. 다음 미적용 모집단은 이022의 실제 ID 집합에서 다시 산출한다. source-only 후보531/남은31 등을 게임 전체 미번역 수로 확대하거나 기존500개를 다시 세지 않는다. 기본 진행 힌트 script10·별도 B0 source0x78BF28/7B65EC(정확 TPI row 미확정), 동적 변수/작은 창/다른 renderer·UI 등은 별도 분석이 필요하다.
2. 새 hint link의 자연 A3 scene/Navi/provider·progress flag/branch/acquisition 경로, 다른 내비 경계·실기·오디오와 전체500개 의미/화면 검수를 보완한다. loader/scene/table read-alias checkpoint는 diagnostic_checkpoint.mss로 격리했고 일반 플레이 상태로 사용하지 않는다. 기존021 state를 새 ROM에 이식하지 않았다.
3. 사용자가 요청한 자동 한글 조합→확정→저장→불러오기/재표시는 아직 미완료이며, 일본어 자판/닉네임 suffix와 기존 구매 안내 행간·필드 날짜 HUD도 남았다. 전체 통합 완료로 보고하지 않는다. 새 배포 패키지는 사용자가 다시 요청하기 전 만들지 않는다.

## 이하: 이번 턴의 진행/실패 기록 (최종 상태를 소급 변경하지 않음)

## 현재 후보 ROM (후속 검증 진행 중)

`poc/output/pending500_022_v2.gba` 빌드 성공: SHA256 `7363567b1263dac0700e2430da1046e47aa9ba65c8d9c2125b1ab9b3bd2928a1`, 12,059,324bytes, 누적12,122개, primary405/source payload 물리적 미변경327archive. `analysis/pending500_022_v2/delta.json`의 실제 신규500-ID delta/기존 ID누락0/이전 payload·병합 비신규script·소비계약·선정asset lineage PASS. `hint_cpu.json` 실제 최종 배치5,652조건, `selector_cpu.json` 기존 reader3,195조건, `hint_integrity.json` 손상 거부11fixture PASS.

현재 독립 `pending500_022_v2_repro` 빌드와 `pending500-022-v2` fresh same-ROM 정상 회귀/힌트 진단을 실행 중이다. 독립 byte identity/전체 Expected Writes·ancestry 감사/실제 글꼴·페이지 검증이 끝나기 전에는 기존021 수준의 검증 완료라고 세지 않는다. 이 후보는 needs_review/NON-DISTRIBUTION이며 새 BPS/xdelta/ZIP 없음. 아래 '빌드 중/미반영' 설명은 당시 단계 기록이다.

## 2026-10-15 제품 연결 작업 (아래 과거 상태보다 우선)

`PROFILE022`와 세 제품 builder의 `--pending-batch500-022`를 등록했다. 원래 500개 소스 preflight를 보존하고 raw136개만 투영한 독립 preflight/실제021 carry 병합 검사를 통과했다. 7C9C44·7CA474·7CAF40은 기존 archive이며 7CB850만 새 primary archive다. 첫 raw 병합 시 7CAF40도 새 archive로 잘못 분류한 검사가 실패했고, 실제021 metadata에 따라 분류를 바로잡았다. 최종 원문/소비 계약을 완화하지 않았다.

`hint_rom_selector.py`/`hint_rom_data.py`가 압축 힌트19archive/364개를 공통 keyitem/mail selector append writer 안에 합성한다. 원본 압축 데이터/포인터/기존 native RAM 해제 크기는 유지하고 전체 native payload 바이트가 같은 sceneA3/정확한 caller/root/Navi/script에서만 ROM clone을 선택한다. 새 persistent RAM은 없고 일시 stack32bytes다. `translations/pending_insertion_500_022_build_v1.json`이 고정500개 preflight를 참조한다. 모든 선택은 needs_review/NON-DISTRIBUTION이다.

첫 `pending500_022_v1` 제품 빌드는 새 `hint_rom_clones` 상위 폴더 생성 누락으로 ROM 저장 전에 실패했다. 실패 작업 폴더를 보존하고 `compile_inputs()`에서 해당 폴더를 먼저 만들도록 수정했다. `analysis/pending_insertion_500_022_hint_component_v1`에서 제품 compiler의 힌트19개/364개·사전컴파일 해시·전체 guard 배치·기존 selector 합성/Thumb-1 검사를 통과했다. 이는 RAM/화면 검증이나 ROM 결과물이 아니다.

`pending500_022_v2`를 원본에서 다시 빌드 중이다. `build_from_frozen_arguments.py`는 첫 wrapper가 확정한 해시 고정 JSON 인자에서 work/out 두 경로만 변경하고 lineage를 남긴다. 기존 컴파일 산출물을 재사용하지 않고 제품 입력/전체 컴파일/최종 검사도 생략하지 않는다. 아직 최종 해시/500-ID delta/독립 재빌드/실제 reader·glyph·페이지 검증 전이므로 **검증된 최신 ROM과 반영 누적은021/11,622개 그대로**다. 압축19개 CPU-only5,652조건 결과를 새 제품 runtime 증거로 전이하지 않는다. 실제 배치 CPU 검사·결함 거부 fixture·fresh same-ROM 정상 회귀 및 진단 도구를 준비했다. 기존021 state는 새 ROM에 이식하지 않는다.

초기 Monday field의 scene값은 이전 스냅샷 global0x0200F2C0→ctx0x02004AD0/+4에서 **B0**였다. A4라는 가정은 채택하지 않았다. 자연 경로는 기존78BF28/native root를 그대로 쓰는 거부 경로이며, 선정A3 힌트의 표시 표본은 loader/scene/table read-alias 진단으로 구분해야 한다. 한글 자동 조합/commit/save/redisplay 및 모든 자연 이벤트/사람 승인은 여전히 미완료다. 새 패치 패키지를 만들지 않았다.

## 이전 소스/CPU 전용 조사 기록

## 현재 권위와 반영 상태

후속 현재 상태: RAM을 늘리지 않는 ROM reader 개발 후보를 구현하고 CPU5,652조건을 통과했다. 제품 통합/실제 GBA 검증은 아직이다. 설계·증거·다음 단계 권위는 `HINT_ROM_SELECTOR_POC_HANDOFF.md`, 결과는 `pending_insertion_500_022_selector_poc_v1/cpu.json`이다. 아래 저장 조사와 소스 전용500개 결과는 그대로 유효하며 ROM 반영 수는 증가하지 않았다.

native 소비 경로도 후속 확인했다. 같은021 월요일 필드 상태에서 A6회→L로0x0804F7FC/0x0804F802 진입과 root0x0203D800/script0을 관측했다. `pending_insertion_500_022_selector_poc_v1/native_consumer.json` 참조. 새 reader/선정19개 번역의 실제 표시 증거는 아니다.

실제 최신 ROM은 여전히 `poc/output/pending500_021_v1.gba`, SHA256 `76d9cf6626436f4c683a49f9389f72c3c85b01b6d6b43461a466e32976ec7ac4`, 누적11,622개다. 이번500개는 소스 전용 컴파일까지 완료했으며 ROM에 반영하지 않았다. 12,122개 반영이나022 통합 완료로 세지 않는다. PROFILE022/제품 빌드 flag/registry 등록도 아직 없다. 새 BPS/xdelta/ZIP 없음. 원본/021/이전 ROM/사용자 세이브/기존 증거 보존.

## 조사와 선택

`analysis/pending_insertion_500_022_survey_v1/survey.json`은 실제021·통합 검사 보고서·원본·TPI·고정 초안을 재대조했다. 고정 초안 변경0. 이전 좁은132px 규칙 후보는1개이며 전체 게임의 미번역 잔여 수가 아니다.

`...022_fullbox_survey_v1/survey.json`은 기존 raw 큰 창 계약으로167개만 남아 정확500개 선택에 실패했다. 실패 조사 결과를 보존했다. 창·변수·선택지 규칙을 수량에 맞춰 완화하지 않았다. 이미 일부 적용된 raw script의 나머지 ID를 같은 제한으로 재조사했지만 새 후보는 없었다.

다른 저장 어댑터 후보를 분류한 뒤, 이미 검증한 큰 창 계약을 만족하는 압축 진행 힌트에 한정했다. 소스 TPI compressed=true/size_header=false, 단일 포인터가 `0x54180..0x541D0`의4바이트 정렬 slot인 범위만 조사 후보로 취급했다. 새 RAM 용량이나 제품 삽입 규칙으로 채택한 것이 아니다. `...022_fullbox_survey_v2/survey.json`의531개 조건 후보에서 `...022_selection_v1/selection.json` 정확500개를 고정했다.

선정 결과23archive/377script, 압축 진행 힌트19archive/364개 + raw4archive/136개. raw은7C9C44(2),7CA474(7),7CAF40(30),7CB850(97)다. source-only 선택에는 이미 적용된 ID가 없다. 기존 초안의 문구·needs_review 상태를 유지하고 `translations/pending_insertion_500_022_layout_v1.json`의5개 줄 배치만 조정했다. 공백과 LF의 위치만 이동하며 문구·LF 수·원본 edge LF/padding을 보존한다. 원본 선행 분기/flag/global 쓰기·화자·대기·페이지 전환은 수정하지 않는다.

## 컴파일과 용량 측정

`tools/prepare_pending500_022.py` → `analysis/pending_insertion_500_022_preflight_v1/preflight.json`의500개 원문/한국어 semantic·binary roundtrip, 원문 무변경 재구축, 제어 코드·비선택 script 보존, 인코딩·3행/180·180·168px 배치 검사 PASS. 이 검사는 원본에서 만든 독립 소스 전용 결과이며 실제021 carry 병합·최종 저장 형식·ROM 포인터·전체 write graph·배포/화면 검증을 대신하지 않는다.

`tools/analyze_pending500_022_storage.py` → `...022_storage_v1/storage.json`: 압축19개는 기존 decoded1789~1954bytes에서 후보2574~2823bytes로 증가한다. raw 후보는2220/3007/3368/7162bytes이며 실제 carry 병합 이후 크기는 별도다. 원래 compressed payload를 단순 교체해도 안전하다고 판단하지 않는다.

원본 코드 `0x0804F712`의 세 번째 field-message load는 `0x08053FA0`의 scene table → Navi index → 압축 원본을 선택하고 `0x0804F744`에서 `0x0203D800`으로 압축 해제한다. 고정 source instruction bytes와 literal을 검증했다. `0x0804F7FC`는 해당 RAM root를 대사 엔진에 넘기는 경로다. 목적지는 확인했지만 끝 경계/수명/다른 scene의 공유 writer는 미확정이다. EWRAM 끝이나 근처의 절대주소 literal을 용량의 증거로 간주하지 않았다.

## 021에서 수행한 정상 경로 조사

기존 초기 날짜2000/1/1(토)은 PET 첫 메뉴가 토너먼트다. `pending500-022-storage-route-v1/v2`의 버튼 입력은 이 상태의 PET 대화/토너먼트 질문을 지나며 field loader PC는0회였다. 이는 로더가 미사용이라는 증거가 아니다.

새021 콜드 부팅에서 날짜 UI만 정상 입력으로2000/1/3(월)로 바꿨다. `poc/runtime/pending500-022-weekday-boot/step_010.png` 월요일 확인 화면을 직접 봤다. 같은 ROM에서 생성한 boot→pagecycle→complete 상태를 사용했고, 기존 자료에서는 action 문자열만 재사용했다. RAM·flag·PC·진행 상태의 강제 주입 없음. 사용자의 기존 저장 데이터는 사용/수정하지 않았다.

`pending500-022-weekday-complete/step_034.png` 인터넷 필드 진입 화면을 직접 확인했다. 같은 weekday-pagecycle checkpoint와 complete action으로 반복한 `pending500-022-weekday-complete-trace`에서 loader진입과3개 압축 호출을 각각1회 관측했다. `tools/verify_pending500_022_loader_observations.py` → `...022_storage_v1/native_loader.json`에 exact021/에뮬레이터/영수증·캡처 해시를 묶었다.

- source0x7B65EC → RAM0x02039800, decoded510bytes
- source0x79C2B4 → RAM0x0203C800, decoded40bytes
- source0x78BF28 → RAM0x0203D800, decoded1759bytes

세 payload 모두 별도 snapshot 실행의 해당 RAM과 전체 바이트 동일했다. 호출 trace와 RAM snapshot은 같은021/동일 시작 상태·입력의 별도 실행이라는 점을 구분한다. 이번 선정 압축19개의 직접 실행/커진 한국어 데이터 로드나 RAM 용량 검증은 아니다. 첫 필드 대화 중 `0x0804F7FC` 소비 경로는 관측되지 않았다. 관련 field/일본어 대화 화면도 직접 확인했으며 신규500개 표시로 세지 않는다.

0x7B65EC와0x78BF28은 이번 TPI에서 정확한 source offset row가 없었다. 실제 load 경계·바이트는 관측했지만 텍스트 소비/추출 모집단과의 관계는 미확정인 후보로 남긴다. 732 TPI 왕복 성공을 게임 전체 추출 완료로 확대하지 않는다. 소스 포인터의 공유/내부 entry/목록 밖 block 여부를 추가로 조사해야 한다.

## 다음 구분 실험과 남은 조건

1. 실제 field hint consumer를 원래 초기 대화 이후 관측하고 scene/Navi별 lookup 및 RAM 수명을 조사한다. snapshot은 load 이전부터 시작한 실행이어야 한다. 용량을 확정하지 못하면 원래 RAM 해제 크기를 유지하는 ROM 직접 읽기 방식의 적용 가능성/비용/ABI를 비교한다. 기존 mail ROM reader의 성공을 다른 root/caller에 자동 전이하지 않는다.
2. 정책을 확정한 뒤에만 압축19개 저장 계약을 제품 빌드에 등록한다. 원본 bytes/모든 포인터·캐리 문구/소비 계약·최종 write set/실제500-ID delta를 증명하고 원본에서 ROM을 빌드한다. raw136개만 반영하고500개 완료로 세지 않는다.
3. 독립 재빌드·해당 압축 loader/consumer의 load·residency·glyph/페이지/재진입과 기존 정상 경로를 최종 ROM에서 검증한다. 소스 전용500개 결과에는 runtime_tested=false와 release_eligible=false를 유지한다.

초기 구매 안내 행간은 기존 구현의 폰트 파생 tile 배치(4행,13px 간격)를 확인했을 뿐 수정·원인 확정·해결하지 않았다. 한글 자동 조합/commit/save/redisplay, 이미지/별도 UI·소비 경로, 전체 자연 분기/사람 검수 역시 미완료다. 사용자가 패치 생성을 다시 요청하기 전에는 새 배포 패키지를 만들지 않는다.
