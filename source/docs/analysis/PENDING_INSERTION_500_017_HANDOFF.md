# 017: 다음 500개 통합 작업

과거 기준 기록이다. 후속018의 미적용500개 ROM 반영 및 제품/화면 검증이 완료됐고 현재 결과/재개 권위는 `PENDING_INSERTION_500_018_HANDOFF.md`다. 아래017 결과는 해당 artifact의 증거로 보존한다.

현재 개발 ROM: `poc/output/exe45_ko_development_pending500_017_v1.gba`, SHA256 `73cb5ec4b297faaeb95f8ccb531096c753f8a5455adfb2c2d8a5cbe9f30f9106`, 11,873,080 bytes. 원본 기반 제품 빌드 및 독립 `_repro.gba` 전체 byte identity PASS. 실제 미적용 500개 추가/기존 누락 0, 누적 소비 단위 9,122→9,622, 주347/미변경385 아카이브. 현재 결과/재개 권위는 이 문서이며 016 결과는 과거 기준으로 보존한다. 사용자 지시대로 새 BPS/xdelta/ZIP은 만들지 않았다. NON-DISTRIBUTION, 전체 한글패치 완료본은 아니다.

## 기준과 고정 입력

기준 016 ROM `poc/output/exe45_ko_development_pending500_016_v1.gba`, SHA256 `d58330fba33d9656e90405309afc39496483aacce2df73908e62b53a4f64bd08`. 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, TPI와 기존 draft-first 입력 해시 모두 대조했다. 변경/누락 고정 초안 0.

`pending_insertion_500_017_survey_v1/survey.json`은 같은 일반대사 필터를 실제 016 적용 ID에 대조한 새 조사다. 후보 160개 script/254개 unit만 남아 정확히 500개를 선택할 수 없었다. 이 수는 전체 게임 잔여수가 아니다. 앞선 016 조사 결과를 현재 잔여수로 재사용하지 않았다.

`pending_insertion_500_017_layout_survey_v1/survey.json`은 다른 거부 조건을 해제하지 않고 `adopted_normal_geometry`만 남은 문구의 줄 위치를 조사했다. 3행 이내, 채택 폭 132px, 줄 수 유지, 기존 공백만 줄바꿈으로 바꿈, 줄바꿈을 공백으로 펼치면 초안과 정확히 동일해야 한다. 단어 내부 분리, 문구 축약, 조사/말투 치환, 새 페이지/대기 명령 추가는 없다. 이렇게 조사한 유한 범위는 452개 script/1,109개 unit이며, 삽입 가능/의미 승인/전체 잔여수는 아니다.

고정 선택 권위 `pending_insertion_500_017_selection_v1/selection.json`. 111개 script/500개 distinct source-ID, 기존 적용 교집합 0. 원래 draft의 문구를 재사용하며 새로 번역한 500개로 보고하지 않는다. 선택은 분석에서만 수행하고 제품 빌드에서는 고정 결과를 검사·소비한다.

- 716DE4: 224개
- 71A66C: 94개
- 76C944: 72개
- 7A152C: 15개
- 7C0F8C: 57개
- 7C7188: 38개

각 script의 일본어 literal 전체가 선택된다. 부분 script 또는 이미 반영한 문구를 중복 집계하지 않는다. `translations/pending_insertion_500_017_layout.json`은 105개 ID의 같은 문구 줄 위치만 소유한다. 원래 초안은 수정하지 않았고, 각 최종 입력의 `source_draft_links`가 원래 path/hash/ID와 고정 selection hash를 연결한다. 자동 레이아웃의 기계적 통과는 사람의 의미/표현/화면 승인과 다르다. needs_review, NON-DISTRIBUTION 유지.

## 제품 경로와 사전 검사

`pending_insertion_500_017_preflight_v1/preflight.json`: 정확히 500개, 후보 layout 0, 실제 원본/source text/payload·native/semantic/binary roundtrip·숫자·제어·LF topology·glyph/encoding 검사 PASS. 아직 ROM을 쓰지 않은 증거다.

`pending_insertion_500_017_cumulative_v1/preflight.json`: 기존 6개 writer에 서로 겹치지 않는 script를 병합한다. 부모를 재컴파일해 실제 016 payload를 먼저 재현하고, 병합 후 비신규 script byte identity와 기존 per-ID consumer/metrics를 보존했다. 76C944의 기존 작은 소비 범위와 신규 normal-dialogue profile을 분리해 기존 제한을 바꾸지 않았다. 병합 payload bytes: 27,988 / 10,979 / 6,523 / 9,330 / 4,959 / 6,220. 새 아카이브/새 hook/새 그림 변경 0.

`--pending-batch500-017`은 원래 3단계 builder에 연결되고 016을 필수로 요구한다. 원본으로 전체 제품을 재생성하며 이전 ROM에 덧쓰지 않는다. PROFILE017의 고정 selection/input/layout 재검사와 ordered ancestry 검사를 유지한다. generic materializer/survey parameter 변경 뒤 016 고정 24개 입력 및 누적 입력이 모두 그대로 재현됨을 확인했다.

codec 6, denominator 3, same-wording line placement fixture 4 tests PASS. 최초 fixture의 단어 자체가 132px를 넘는 잘못된 기대는 실패했고, 단어 분리 금지 계약을 바꾸지 않고 fixture를 바로잡았다. 단어 분리/용량 초과/4행은 여전히 거부한다. 관련 syntax PASS.

## 같은 017 제품의 검증 결과 / 재개

재현 이름은 `exe45_ko_development_pending500_017_v1`과 `_repro`, 전체 016 build flags + `--pending-batch500-017`. 두 독립 실행 빌드 exit0, SHA256 동일. source→고정 input/layout→cumulative single writer→원래 builder 경로로 생성했다.

`pending500_017_v1/integration.json`: actual500-ID delta/기존 누락0, 이전352개 비병합 payload/consumer metadata 동일, 병합6개 비신규 script/기존 metrics 동일. 실제 pointer bytes와 원본 source storage, 최종 신규 ID별 compiled explicit layout, 전체 ExpectedWrites/header/ISA/ancestry 및 독립 ROM byte identity PASS. 사전 검사만으로 ROM 반영을 주장하지 않고 최종 artifact를 다시 검사했다.

`selector_cpu.json`: composed mail/keyitem selector 3,195 합성 CPU vectors PASS, 실제 플레이 증거와 구분한다. `rejection_controls.json`: 기존 population/ID/metrics/retained payload4 결함 거부 PASS. `changed_archive_controls.json`: 이번 병합 payload/new ID/new layout metrics/pointer bytes/native source storage5 결함 거부 PASS. 유효 제품은 수용하고 메모리 내 변조만 검사했으며 실제 ROM은 수정하지 않았다.

`normal_runtime.json`: 같은017의 정상 cold boot/초기 설정/기존 일본어 자판3페이지 VRAM/map/native21-namebank/선택 가능한 내비4개 OAM/첫 I.P.C. 메일23 ordered keyWait/실제3archive RAM load/리스트 복귀·재열기 PASS. `run_first_mail_regression.py --rom poc/output/exe45_ko_development_pending500_017_v1.gba --prefix pending500-017-v1`와 `verify_first_mail_runtime.py`로 재현한다. `first_mail_pages_v1.png`23쪽을 직접 시각 검사했다.

`display_runtime.json`: 6개 아카이브에서 신규14 literal/245 glyph의 CPU→font→OBJ→pixel/keyWait/페이지 지움 PASS. `changed_pages.png`14쪽 직접 시각 검사, 잘림/이전 페이지 잔상은 해당 표본에서 발견하지 않았다. `run_cumulative500_017_displays.py`로 재현한다. 사례는 716DE4:14, 71A66C:3, 76C944:35, 7A152C:21, 7C0F8C:2, 7C7188:6이다. 원본 prefix와 실제 script count를 고정했고 정상 own017 complete checkpoint에서 시작했다.

진단은 own Navi0 PET root/table read alias만 사용하고 native initializer/portrait/msgOpen/commands를 실행했다. 마지막 keyWait 이후 event/end를 진행하지 않고 checkpoint를 격리했다. 이 alias는 제품 ROM에 설치하지 않았고 직접 ROM/RAM 쓰기도 없다. 배경 록맨은 진단의 시작 내비이며 각 화자의 원본 portrait 명령은 별도로 실행된다. 원래 대사나 speaker lookup을 록맨으로 바꾸지 않았다. 14쪽 sample이 500개 전체의 자연 caller/event/save/말투·화면 사람 승인을 뜻하지 않는다. 런타임 증거는 Mesen의 관찰 범위다.

가장 어려운 남은 완료 조건인 실제 자동 한글 조합/commit/save/redisplay ABI는 여전히 미완료다. 선택지/별도 renderer/변수/압축/자연 경로/사람의 전체 의미·화면 검수도 남았다. 이번 500개 입력 검사와 화면 sample이 전체 한글패치 완료를 뜻하지 않는다.

다음 묶음은 실제017 적용 ID 기준으로 다시 조사한다. 고정017 조사1,109개를 다음 잔여수로 재사용하지 않는다. caller/선택지/변수/다른 renderer·storage 조건을 단순히 제거하거나 이미 반영한 문구를 세어 500개를 만들지 않는다. 같은 문구의 줄 위치가 기존3행132px에 들어가지 않는 대상은 표현 변경 없이 그대로 보류한다.

작업 끝 원본/016/기존 ZIP 해시 재확인: 각각 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, `d58330fba33d9656e90405309afc39496483aacce2df73908e62b53a4f64bd08`, `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`, 모두 동일. 이전 ROM·세이브·증거·배포 파일을 삭제하거나 덮어쓰지 않았다.
