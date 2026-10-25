# 014: 가운데점 보류 문구 포함10개, 새 raw3아카이브 실제 ROM 반영

이 문서는014 당시 기록이다. 최신 제품/재개 권위는 `PENDING_INSERTION_500_015_HANDOFF.md`이며015에서6개를 추가했다. 아래 보류9개 등의 수치는014 당시 기준이다.

개발본 `poc/output/exe45_ko_development_pending500_014_v1.gba`, SHA256 `6cdcae37d8682c03a909b08d3ddefea02ad825c6a272899c38bcc5f316be9245`. 독립 `_repro.gba` 전체 바이트 동일. 실제 신규 source-ID10개, 기존 누락0, 누적 소비 단위8,606→8,616, 주322/미변경410아카이브. 소비 단위는 전체 일본어/고유 번역 문구 수나 완료율이 아니다. 정책 `development-draft; NON-DISTRIBUTION`, release_eligible=False. 원본/이전 ROM/세이브/증거/기존 패키지 보존, 새 BPS/xdelta/ZIP 생성 없음.

## 선택 및 문구 출처

신규 raw 아카이브7BDC90(script0,5개),7B4184(script1/2/3,4개),7B3C30(script0,1개). 스테레오 프로그램·섀도맨·폐점 상점 안내다. 500개 legacy 도구명과 이번10개 실제 분모를 구분한다. 좁은 일반 raw 범위가 소진된 뒤, 폭 때문에 남았던 유한 범위를 별도로 검증했다. 선택지/동적 삽입/같은 script 부분 미적용은 무작정 포함하지 않았다.

`translations/pending_insertion_014_wording_proposals.json`의5개는 직접 작성한 기술검토용 대안이다. 규칙 기반 치환/자동 축약은 없고, 원문과 기존 초안은 그대로 보존했다. review=needs_review, approved=False, 원래 표현·변경 이유·source-ID·parent path/hash를 기록했다. 나머지5개는 초안을 그대로 사용했다.

- 7B3C30:0:0: `망해 버린 모양이군`→`망한 모양이군`.
- 7BDC90:0:1: `나·는·말·이·야아아!!`→`난·말·이·야아!!`; 음악적인 분절/늘임과 자기소개 유지.
- 7B4184:1:0: `이 빚은···반드시 갚겠다`→`빚은···꼭 갚겠다`; 말더듬·위협·확실한 보복 유지.
- 7B4184:2:0: `너 따위는 마무리할 / 가치도 없다···사라져라`→`넌 끝장낼 가치도 / 없다···사라져라`.
- 7B4184:3:1: `정정당당하게`→`정정당당히`.

줄 수·제어 명령·숫자는 원문 조건을 지키며, 표현에 대한 독립/사람 검수 완료를 주장하지 않는다. `prepare_middle_dot014_inputs.py`는 원래 세 초안의 고정hash와5개 제안으로 선택 입력을 재현한다. `batch500_000_insertion014_*_draft_ko.json`은 출처 링크를 가진 고정된 생성 입력이다. 누적 derive에서 이 입력을 다시 확인하고 manual_wording_proposals를 최종 선택 asset에도 보존한다.

source-only authority: `pending_insertion_500_014_partial_selection_v1/selection.json`, `pending_insertion_500_014_partial_preflight_v1/preflight.json`. 기존 교집합0·candidate0·native/semantic/binary roundtrip PASS. source-only payload를 직접 삽입하지 않았다. 누적 authority: `pending_insertion_500_014_cumulative_v1/preflight.json`, exact013 baseline/hash, 신규10개/3개 parent=None, normal3행132px, source storage·known pointers·255script table을 고정했다. 미선택254/252/254script 슬롯 byte identity PASS(빈 슬롯 포함).

## 제품 경로와 같은 ROM 검증

PROFILE014 및 `--pending-batch500-014`는013을 prerequisite로 요구한다. 원래 제품 builder3단계에서 새로운3개 단일 writer를 추가하고 immutable 원본부터 다시 빌드한다. manifest ancestry는014를 가장 먼저 선택하며, 원래 입력/과거 artifact 각각을 검증한다. first_mail ExpectedWrites는 새3개 known pointer 쓰기를 명시적으로 등록한다. 기존 consumer contract를 임의로 바꾸거나 검사 범위를 제외하지 않는다.

- `pending500_014_v1/integration.json`: 실제10-ID delta/기존 누락0, 기존330페이로드 및 소비metadata 동일, 신규3개 미선택script/source storage·actual pointers·전체write/header/ISA·exact ancestry 감사·독립 재빌드 byte identity PASS.
- `selector_cpu.json`: composed mail/keyitem/gear 선택기3,195 합성CPU조건 PASS; 실제 플레이 증거 아님.
- `rejection_controls.json`, `new_archive_controls.json`: 유효 artifact accept, 기존 unit/ID/metrics/script4조건 및 새 payload/ID/pointer metadata/pointer bytes/source storage5조건 reject PASS. 모두 메모리 내 변조, 디스크 수정 없음.
- codec6tests, denominator3tests, 관련 syntax PASS.
- `display_runtime.json`: 신규10개 모두 glyph CPU reads→OBJ VRAM→화면 pixels, root/origin/native keyWait, 빈 영역 지움 PASS. 실제154glyph. `changed_pages.png`10쪽 직접 시각 검사. 비교표의 높이는10쪽 전부가 들어가도록 계산하며 예전8쪽 이하 결과는 유지한다.
- `normal_runtime.json`: same014 정상cold boot·초기 설정·기존 일본어 자판3페이지 VRAM/map·native21-name bank와 네 내비 OAM·첫 메일23 ordered keyWait/native3archive RAM load/list 복귀/재열기 PASS. `first_mail_pages_v1.png`23쪽 직접 시각 검사.

격리 표시 진단은 same014 정상 Rockman0 상태에서 native PET pointer/table read만 alias한다. native context reset/원본 mugshot/msgOpen 그대로 실행, 직접 ROM/RAM 쓰기 없음. 원본 portrait prefixes를 실제 읽어 고정: MrProg1F,HeelNaviPurple24,ShadowMan32. 선택 내비0과 portrait namespace를 혼동하지 않는다. diagnostic checkpoints는 격리했고 alias는 ROM에 설치되지 않는다.

섀도맨script3의 마지막 keyWait 뒤 global/flag 변경은 실행하지 않았다. 실제 배틀 결과/보상/자연 이벤트 진입/선택 결과/저장 성공을 주장하지 않는다. Mesen에 한정한 표시 증거이며 실기/다른 에뮬레이터 전체 지원 검증이 아니다.

## 보류 목록 재대조 및 다음 재개

`middle_dot_reconciliation.json`은006-v2의 historic19 source-ID를013/014 실제layout과 대조했다.013까지3개 적용/16개 미적용, 이번7개 추가로10개 적용/9개 미적용이다. 앞서 수작업으로4/15라고 센 진행 안내는 잘못이었다. 구 handoff의19개 전부 보류라는 문장도 최신 상태가 아니다. 이는 유한 인코딩 보류 목록이지 전체 게임 미번역 수가 아니다. 표현 검수 상태는 별도다.

남은9개:768800:2:1/2:3,7B4184:0:0/0:3/4:0,7C9C44:0:0/0:1,7CC6A0:76:0/78:0. 선택지 geometry·부분script carry·서로 다른 소비 경로를 먼저 확인한다.010 waitHold의 실제 battle caller, dynamic nickname4개, 기타compressed/fixed/UI 및 자연 경로가 남았다. 실제 자동 한글 조합·commit/save/redisplay ABI도 미완료다. 일본어3페이지 자판과 한글 동작 라벨/CPU 후보를 한글 입력·저장 완료로 세지 않는다.

재현: `cumulative_batch500_014.py` 사전 검사 후013 handoff의 원본 기반 전체 build 명령에 `--pending-batch500-014`를 추가하고 출력명을 새014 이름으로 지정한다. 기존 결과에는 덮어쓰지 않는다. `verify_cumulative500_014.py`, `run_first_mail_regression.py`, `verify_first_mail_runtime.py`, `run_cumulative500_014_displays.py` 및014 결함 검사wrapper로 동일 조건을 반복한다.

보존 해시: 원본 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`,013 `00093bd660f08930abf2db43cd98f5ce93f64c563c9313496051f4472d86b20c`, 기존 ZIP `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`; 작업 끝 read-only 재확인으로 동일.
