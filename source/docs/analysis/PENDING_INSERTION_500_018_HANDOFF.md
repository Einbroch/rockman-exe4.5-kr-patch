# 018: 다음 500개 통합 작업

현재 개발 ROM: `poc/output/exe45_ko_development_pending500_018_v1.gba`, SHA256 `a8d39423bbd4792d948af4bea991dd8c56bb6d34dac8c1a7c570f0c3938f3241`, 11,899,160 bytes. 독립 `_repro.gba` 전체 byte identity PASS. 실제500-ID 추가/기존 누락0, 누적 소비 단위9,622→10,122, 주377/미변경355 아카이브. 현재 결과/재개 권위는 이 문서다. 017은 이전 기준으로 보존한다. 사용자 지시대로 새 BPS/xdelta/ZIP은 만들지 않았다. needs_review, NON-DISTRIBUTION, 전체 한글패치 완료본은 아니다.

## 고정 기준과 선택

원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`; 기준017 ROM `poc/output/exe45_ko_development_pending500_017_v1.gba`, SHA256 `73cb5ec4b297faaeb95f8ccb531096c753f8a5455adfb2c2d8a5cbe9f30f9106`. 원본/TPI/고정 draft-first 입력과017의 실제 적용 ID를 다시 대조했다. 변경/누락 고정 초안0.

`pending_insertion_500_018_survey_v1/survey.json`: 기존 일반대사 필터에서143 script/207 unit, 기존 same-row 줄 배치 조사에서341 script/609 unit 후보. 전체 게임 잔여수가 아니며 즉시 적용 준비 완료 판정도 아니다.

첫 선정/컴파일은6BB2A4:32:0의 trailing LF 이동을 차단하고 실패했다. 앞선 배치의 검사를 완화하지 않았다. `pending_insertion_500_018_preflight_v1`은 실패 중간 증거로 남기고 제품에 사용하지 않는다. `layout_survey_v2/survey.json`은 source와 target의 leading LF/trailing LF/trailing spaces를 추가 대조하여9 script/23 unit을 보류했다. 남은332 script/586 unit에서 다시500개를 선정했다. 기존 렌더러/참조/storage/변수/선택지/caller 조건을 제거하지 않았다.

현재 선정 권위 `pending_insertion_500_018_selection_v2/selection.json`; layout `translations/pending_insertion_500_018_layout_v2.json`. 252개 script의 일본어 literal 전체에서500 distinct source-ID, 기존 교집합0. 78개 아카이브(기존48/new30),142개 explicit line layout. 초안 문구를 그대로 재사용하며 새로 번역한500개로 보고하지 않는다. 줄 수/단어/공백으로 펼친 문구/숫자/controls 유지, 단어 내부 분리·축약·새 page/wait 명령 추가0. 원래 초안은 수정하지 않았고 per-unit parent path/hash/ID와 고정 selection hash를 유지했다. needs_review, NON-DISTRIBUTION이다.

## 사전 검사와 단일 writer

`pending_insertion_500_018_preflight_v2/preflight.json`: actual source/payload/TPL/native·semantic·binary roundtrip, 숫자/제어/LF/edge/padding, glyph/encoding/geometry PASS. 총500, unique500, applied-ID 교집합0, layout 후보0. ROM 미작성 증거와 구분한다.

`pending_insertion_500_018_cumulative_v1/preflight.json`: 78개 전부 PASS. 기존 실제 parent48개를 다시 컴파일해017 payload를 재현한 뒤 비신규 script/기존 metrics/consumer를 보존했다. 새30개는 source-known pointers/raw normal-dialogue contract를 고정한다. `--pending-batch500-018`은017 prerequisite와 기존3단계 builder/ExpectedWrites/ancestry에 연결된다.

65B220은 기존 startup followup scope를 실제 제품 builder와 같은 `startup_ui.followup_scopes()`에서 가져온다. 기존1..7 script/7개 suffix, 새20..26 script/7개 mail notification을 분리하고 native cue/sound/wait/flag/nickname/event를 보존한다.

66651C의 초기 누적 검사는 read-only inherited3 기록을 실제 parent로 잘못 선택해 carry source-ID 불일치로 실패했다. 실제017 primary asset은 `gutsman_alarm_meal_ko.json`의6개이며 inherited5/3은 별도 writer가 아니다. 현재018은 명시적인 read-only inherited 메타데이터를 제외한 유일 primary owner만 채택하고 모호하면 실패한다. 실제6개 parent bytes 재현 및 새3개 병합/미선택 보존 PASS. 이전017 고정 입력/누적 입력도 그대로 재현했다.

병합으로 scope_variant가 제거되면 old inherited read-only metadata projections를 새 제품에 중복 writer처럼 추가하지 않는다. 대신 exact old primary asset→parent_asset immutable hash chain에 각 projection의 path/hash가 실제 존재함을 검증한 후 과거 lineage 배열을 정규화한다. 해당 링크가 없거나 순서/다른 항목이 바뀌면 실패한다. 실제 carry ID/metrics/payload/asset hash 검사를 완화하지 않는다. 이전 provenance 파일은 그대로 보존한다.

## 제품 명령 전달 보완과 현재 실행

최초 동시 빌드는 공통 생성 입력 `input_remaining_v1/selected_asset.json`의 write/read 시점이 겹쳐 empty SHA를 읽는 오류로 중단했다. 생성 완료 파일 SHA는 이전 입력과 동일한 `d2aff7aadcd997c2accab52f761bce57ecf47926b9986f93c4bfec710fc58647`다. 해당 입력 의미나 요구 해시를 바꾸지 않고 제품 빌드는 순차 실행한다.

다른 초기 실행은 Windows WinError206으로 긴 command line을 생성하지 못했다. 현재 `build_arguments.py`의 schema1 JSON argv transport로811개 args/377개 translation flags를 순서 그대로 전달한다. 기존 builder entrypoint가 `--argument-file <path> --argument-file-sha256 <hash>`를 독점 호출로 검사/파싱하며 모든 기존 옵션/제품 게이트를 그대로 실행한다. nested manifest/unknown fields/types/NUL/hash 변경/기존 manifest 덮어쓰기를 거부한다. 개별 제품의 `poc/build_arguments/<stem>.json`을 입력으로 고정하고 최종 metadata에 그 path/hash를 남긴다. ROM writer나 게임 명령을 바꾸는 조치가 아니다.

primary 이름 `exe45_ko_development_pending500_018_v1`, independent 재빌드 `_repro`를 primary 완료 뒤 같은 원본/고정 입력/전체017 flags+018로 실행했다. 두 실행 exit0/SHA256 동일. 최초 실패는 work/output을 생성하기 전에 일어났다. 재시도 중간 파일도 보존했다. 공통 생성 입력을 사용하는 두 제품 빌드를 동시에 실행하지 않는다. JSON argv transport 자체가 공통 생성 파일의 동시 쓰기를 해결했다는 주장은 하지 않는다.

tests: codec6/denominator3/line-placement6/argument transport4 PASS, 관련 syntax PASS. trailing LF 이동의 회귀 fixture를 추가했으며 단어 분리/용량 초과/4행 및 source edge/padding 변경은 여전히 거부한다.

## 같은018 제품의 실제 검증 결과

`pending500_018_v1/integration.json`: 실제500-ID delta/기존 누락0, 이전310 비병합 payload/consumer metadata 동일,48 병합 아카이브의 비신규 script/기존 metrics/consumer 보존 PASS. 새30개의 actual known pointers/source storage/미선택 script와 최종 compiled ID별 layout, 전체 ExpectedWrites/header/ISA/정규화된 exact ancestry, hash-bound argument manifest 및 독립 byte identity PASS. 실제 artifact를 다시 검사했고 사전 검사만으로 ROM 반영을 주장하지 않는다.

`selector_cpu.json`: composed mail/keyitem 3,195 합성 CPU vectors PASS; 실제 플레이 증거와 다르다. `rejection_controls.json` 기존4, `changed_archive_controls.json` 실제66651C 병합5, `new_archive_controls.json` 새65E8285 결함 거부 PASS. 유효 artifact 수용 및 메모리 내 변조만 수행했다. 실제 제품 파일을 고치지 않았다.

`normal_runtime.json`: 같은018 정상 cold boot/초기 설정/기존 일본어 자판3페이지 VRAM/map/native21-namebank/선택 가능한 내비4개 OAM/첫메일23 ordered keyWait/실제3archive RAM load/리스트 복귀·재열기 PASS. `run_first_mail_regression.py --rom poc/output/exe45_ko_development_pending500_018_v1.gba --prefix pending500-018-v1`와 `verify_first_mail_runtime.py`로 재현한다. `first_mail_pages_v1.png`23쪽 직접 시각 검사.

`display_runtime.json`: own018 complete checkpoint 이후7개 archive의 신규17 literal/240 glyph sample의 CPU/font reads→OBJ VRAM→pixels/keyWait/페이지 지움 PASS. `changed_pages.png`17쪽 직접 시각 검사, 해당 표본에서 잘림/잔상 발견0. `run_cumulative500_018_displays.py`로 재현한다. 사례는65B220:20,65E828:1,661858:31,66651C:24,66A160:1,698424:2,7C9C44:5이다. full origin52/110과 source-positioned quick92/110을 구분했고 원본prefix/실제script count를 고정했다. 첫 mail notification은 원래nonJapanese cue와96+96frame wait/clear 후의 Japanese literal만 선택했으며 flag/sound/event 명령을 바꾸지 않았다.

display diagnostic은 PET root/table read aliases만 사용해 native initializer/원본 명령을 실행했다. 마지막 keyWait 뒤event/end는 진행하지 않았고 checkpoint를 격리했다. ROM에alias 설치/직접ROM·RAM 쓰기 없음. 배경 록맨은 진단 시작 own Navi0 문맥이며 대사의 원래 portrait/내비 lookup은 변경하지 않았다. 자연 caller/RTC/battle/mail event/save와500개 전체 의미·화면 사람 승인으로 세지 않는다. Mesen의 관찰 범위다.

## 재개와 남은 완료 조건

가장 어려운 자동한글조합·commit/save/redisplay ABI는 미완료다. 압축/변수/선택지/다른renderer/실제caller/자연루트/사람 검수도 남았다. 이 단계가 전체 게임 잔여0이나 release 완료를 뜻하지 않는다. 다음500개는 실제018 기준으로 다시 조사해야 하며 고정586후보를 다음 잔여수로 재사용하지 않는다. 부족하다고 원문LF/padding/변수/선택지 조건을 제거하거나 이미 반영한 ID를 재집계하지 않는다.

작업 끝 보존 해시 확인: 원본 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`,017 `73cb5ec4b297faaeb95f8ccb531096c753f8a5455adfb2c2d8a5cbe9f30f9106`,기존 ZIP `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`, 모두 동일. 원본·기존ROM/세이브/증거/ZIP을 삭제하거나 덮어쓰지 않았다.
