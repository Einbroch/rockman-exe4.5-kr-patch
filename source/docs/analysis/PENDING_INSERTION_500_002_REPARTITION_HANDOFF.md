# 미적용500개 묶음002 — 실제 ROM 반영

사용자는500개씩 ROM에 적용하면서 작업하도록 재지시했다. 이전 계획의 별도 장비 소비 연결만 기다리며 준비 검사를 반복하지 않도록, 그160개를 보존·이월하고 다른 source-bound raw 대사160개로 재구성했다. 앞으로도 적용 완료는 실제 누적 ROM/원문 ID 대조를 기준으로 기록한다.

## 현재 결과

- ROM: `poc/output/exe45_ko_development_pending500_002_v1.gba`
- SHA256: `25c04c4e04dd92c1a1a8d9a6f977ee6631c9a8ec16eed468381f2ecfac3cf6a4`
- 재빌드: `_repro.gba`, 전체 바이트 동일.
- 이번 묶음: **500/500 ROM 반영**, 기존 초안 재사용/새 문구 작성0개.
- 누적:3,837개,주82아카이브,guarded 메일 본문5개,원래 포인터 아카이브650개 유지.
- 원본/이전3,337개 ROM/이전 패키지 보존. 새 패치 패키지0개.
- 개발용/NON-DISTRIBUTION/release_eligible=false. 전체500개 자연 진행 QA 완료를 뜻하지 않는다.

## 재구성 범위와 이월

기존 준비 계획은 `PENDING_INSERTION_500_002_HANDOFF.md`와 r4에 보존한다. 이를 삭제하거나 적용 완료로 승격하지 않는다.

|아카이브|신규 단위|반영 방식|
|---|---:|---|
|6E01AC|105|이전26개를 합친131개/8,798바이트 raw clone|
|6DED88|220|66슬롯/14,957바이트 raw clone,3개 명시적 줄·페이지 배치|
|6DE2C8|15|34슬롯/1,041바이트 raw clone|
|6A3DD0|30|원래 raw 포인터 재배치|
|71BE98|28|동일|
|716DE4|32|동일|
|71A66C|16|동일|
|7A5604|8|동일|
|6AB70C|7|동일|
|71551C|7|동일|
|7A152C|7|동일|
|7AF6D0|7|동일|
|6B6CA4|12|동일|
|6CDCD0|6|동일|

합계340메일+160raw=500개 고유 원본 ID. 완결 script의 일본어 리터럴을 선택했고,새 raw160개는 선택 script에 동적 print* 삽입이 없는132px 이내 기존 초안을 사용했다. 실제 NPC/진행 경로는 후속 QA다. 메일의 동적 변수는 기존 명령 그대로이며 전체 조합 폭은 아직 미완료다.

장비6E1554/6E1CC0/6E21B0 각각51개와6A5578의7개는 **160개 다음 묶음 대기**다. 초안은 수정/삭제하지 않았다. 공통 fixed-name ROM root와 내비별 안내/폴더 오류 RAM 경로를 함께 연결하는 작업이 필요하며,압축 포인터만 바꿔서 적용됐다고 세지 않는다.

## 빌드 및 입력 권위

`tools/prepare_repartition500.py`의 `selection.json`은 source/draft/TPL와 전체 source ID에 바인딩한 재구성 기록이다. 단어/표현을 자동 번역하지 않는다. source-bound 기존 초안이 문구 권위이며 selected_asset/compiled는 생성물이다.

`prepare_repartition500_preflight.py`:500개 native/semantic/binary 왕복,미선택 script 보존,숫자/LF/명령/글꼴 매핑과 모든 페이지 폭 검사 PASS. 현재 결과는 `analysis/pending_insertion_500_002_repartition_preflight_v1/preflight.json`.

`batch500_002_rom.py`는 모든 입력 해시/선택 ID/500+26carry를 재검사하고,기존001의 파괴26개 선택을131개 누적 선택으로 대체한다. 주 빌드는 old001+002를 함께 원본에서 만든다. 11개 새 raw는 native pointer 재배치,메일 본문은 source압축 RAM을 유지한 guarded clone이며 겹쳐 쓰지 않는다.

`pending500_002_pages.py`는41:1의3행,49:1과55:2의2페이지를 각각 명시적으로 처리한다. 글자·단어·숫자·순서와 기존 임무/변수/보상/분기 명령을 보존한다. 두 native keyWait(any=false)+clearMsg 쌍만 추가한다. 추가 fragment를 원본 ID에 연결해500개가502개로 부풀지 않는다.5개 페이지 구조 시험 PASS.

재현 명령은 `build_keyitem_full_rom.py --name <새이름>`에 이전 누적 flags 및 `--pending-batch500 --pending-batch500-002`를 함께 지정한다. 이전 README의 누적 기능 flags를 빼면 기존 기능이 빠질 수 있으므로 현재 `_repro.json`의 전체 선택 assets 및 빌드 wrapper를 따른다. 기존 output/work는 덮어쓰지 않는다.

## 검증

`analysis/pending_insertion_500_002_repartition_rom/integration_v2.json`: 독립 재빌드 동일,기존71개 주 payload와 별도 clone3개 동일,두 기존 임무 본문 동일,파괴38/39/40 script 바이트 동일,전체 compiled-record 원본 ID 집합에서 신규500/누락0,14개 새/누적 선택의 원문/compiled 해시 및 final pointer 대조 PASS. 원래 메일 BIOS 로더/본문 테이블 포인터는 그대로다.

`selector_cpu_v1.json`: **1,072조건 PASS**. 기존 key-item/common-mail와5개 alternate/body,헤더16바이트 각각의 변형,잘못된 caller/root,경계 script를 포함한다. native216-byte zero helper만 bounded contract 대체한 합성 CPU 검사이며 GBA 장면/진행 증거와 구분한다.

`normal_runtime_v1.json`: 정확히 같은 ROM 해시에서 cold boot/초기 설정,기존 자판3페이지 VRAM/맵,내비 bank/OAM,첫 메일23개 대기 포인터·bookmark·복귀·재열기 PASS. 한글 조합/저장 통합 증거는 아니다.

`body_runtime_v1.json` 및 `.png`:5개 격리 native loader/table-read alias 진단에서7개 정확한 리터럴/페이지 대기 포인터,source 압축 RAM 본문 전체 일치,새 ROM root 및 원래 위치 설정을 확인했다. 섀도맨41/49/55는source script0 setup을 실행한 뒤 jump32 테이블 읽기만 별칭 처리했다.등록33/파괴36은 자체 setup을 따른다. 비교표를 에이전트가 시각 확인했으며,7곳 모두 패널 안에 읽을 수 있게 표시되고 화살표를 침범하지 않는다.49/55의추가 페이지 전환은 실제 native waits에서 확인됐다.

진단 state는 diagnostic_checkpoint로 격리했으며 정상 플레이/획득/보상/저장 증거로 사용하지 않는다. 초기 화면의 메일 발신자는 원본 관련 헤더에서 오는 것이며 임의 내비 대사로 갈아끼운 배포 ROM이 아니다. 진단 별칭은 ROM에 쓰지 않았다.

최초 display verifier는 last script33 뒤에34번 table entry가 있다고 가정해 검사를 거절했다. 실제34슬롯의 마지막 script 끝은 payload 끝이므로 경계를 수정했고 재실행 PASS. ROM 내용 오류나 silent 원문 복귀로 처리하지 않았다.

## 다음 작업

다음500개에는 이월160개를 우선 넣고,장비 공통명/내비별 안내·오류 소비를 연결한다. 이번raw160개의 실제 이벤트·선택 경로와 전체 임무 자연 수신/진행/보상/저장은 별도 QA 대기다. 추가 페이지가 timed mission의 읽기 시간/시한에 미치는 영향도 자연 진행에서 확인한다. 말뜻/용어 승인 및 전체 한글 조합/저장 ABI 통합은 미완료다. 새패키지는 사용자의 재요청 전까지 만들지 않는다.
