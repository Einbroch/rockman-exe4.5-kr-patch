# 015: 미적용6개 실제 ROM 반영·표시 검증

이 문서는015당시기록이다. 이후016에서500개를추가했고최신제품/재개권위는 `PENDING_INSERTION_500_016_HANDOFF.md`다. 아래수치와잔여분석은015기준으로보존한다.

최신 개발본 `poc/output/exe45_ko_development_pending500_015_v1.gba`, SHA256 `a6d3b0330566374937857cb49b2f07475a6c590e73ac6873486556585a4f4d81`. 독립 `_repro.gba` 전체 바이트 동일. 실제 신규6 source-ID/기존 누락0, 누적 소비 단위8,616→8,622, 주323/미변경409아카이브. 이 분모는 전체 미번역 수나 완료율이 아니다. 개발용 NON-DISTRIBUTION/release_eligible=False, 표현 needs_review/approved=False 유지. 원본·이전 ROM/세이브/증거·기존 ZIP 보존, 새BPS/xdelta/ZIP 생성 없음.

## 입력과 단일 writer

준비 기록과 source-only v1/v2를 보존했다. 이번 입력은v2의6개다.768800 script2의4개를 기존 script1/4/7/8의4개에 더한8개 asset,7C9C44 script0의2개를 새 아카이브로 추가했다. source-only payload는 이전 번역을 담지 않아 직접 삽입하지 않았다.

권위 `pending_insertion_500_015_cumulative_v1/preflight.json`: exact014 parent/hash, source-onlyv2/hash, 신규6-ID, carry1/new1, script counts13/23, raw source/known pointers를 고정한다. 원래768800 parent를 재컴파일해actual014 payload와 일치함을 확인했고, 신규script2 외12script byte identity·기존4개 wording/metrics/profile 보존 PASS. 새7C9C44 미선택22script/원본 저장 영역 보존 PASS.

원래 초안과4개 제안의 source-ID/wordingID/parent path/hash 관계를 최종 누적asset의manual_wording_proposals에도 보존했다. 두 producer가 생성 입력을 재검증한다. 신규 원문 번역0개, 이전 턴 직접 작성한 표현 대안4개와 그대로 재사용2개를 실제 적용했다. 기존 초안/줄 수/제어/숫자를 고치지 않았고 규칙 기반 prose 치환·축약은 없다. 사람 의미/말투/presentation 검수는 미완료다.

PROFILE015와제품 `--pending-batch500-015`는014 prerequisite를 요구한다. 원래 builder3단계에서768800 writer를 교체하고7C9C44 writer를 추가하며, immutable 원본부터 ExpectedWrites를 계획/검사해ROM을 생성한다. 새 known pointer1개를first_mail ExpectedWrites에 명시했다. manifest lineage는015를 먼저 판단하고 이전 artifact별 검증을 유지한다.

## 중복 재귀 검사 보완

derive가각이전entries를 재귀적으로 재호출해동일 선행입력 검증을 지수적으로 반복하던 것을 순서대로 검증하는 방식으로 바꿨다. top-level derive가원래 registry를 만들고 선언된prior_cumulative 순서에서각entries의기존 preflight/base/source/asset/scope/parent/new-ID guard를 통과한 범위를 다음링크에deepcopy로 전달한다. 모든 이전 링크를 검사하며 결과/파일해시를 영구cache하지 않는다. 제품/새검증 호출은처음부터 다시 검사한다. 입력·검사 범위를 생략하는 fast-path가 아니다.

007~014 각frozen asset/scope/parent/new-ID 재현 PASS. 개선전 실행으로동결된015 preflight도 개선후entries가같게재현했다(7688008개/신규4/제안링크2,7C9C442개/신규2/제안링크2). 아래exact015 긍정 및11개 결함거부 검사도 개선된 경로로 통과했다. 이 보완은문구/ROM코드/소비방식을 바꾸지 않는다.

## 같은015 ROM 검증

- `pending500_015_v1/integration.json`: actual6-ID delta/기존 누락0, 변경768800의12비신규script·기존4개metrics/profile 동일, 비중첩이전332페이로드/소비metadata 동일, 새7C9C44미선택22script/source storage·actual pointer·전체write/header/ISA·exact ancestry 감사·독립재빌드 byte identity PASS.
- `selector_cpu.json`: composed mail/keyitem/gear 선택기3,195 합성CPU조건 PASS. 실제 게임플레이/저장 증거 아님.
- `rejection_controls.json`: declaredunit누락/기존ID누락/기존metrics변조/retainedscript변조/newscript변조/actualpointerbytes변조6개 reject PASS. `new_archive_controls.json`: 새payload/ID/pointermetadata/pointerbytes/source storage5개 reject PASS. 유효 artifact accept, 디스크 수정 없는 메모리 내 변조.
- codec6tests, denominator3tests, 관련syntax PASS.
- `normal_runtime.json`: exact015 coldboot·초기 설정·기존 일본어 자판3페이지VRAM/map·21-name nativebank와네내비OAM·첫I.P.C.메일23orderedkeyWait/native3archive RAM load/list 복귀/재열기 PASS. `first_mail_pages_v1.png`23쪽 직접 시각 검사.
- `display_runtime.json`: 신규6개/154glyph 모두actual font CPU reads→OBJ VRAM→화면pixels, root/nativekeyWait/페이지지움 PASS. `changed_pages.png`6쪽 직접 시각 검사.
- `portrait_free_region.json`: world두페이지각1,600px의왼쪽빈영역 검사 PASS. 두진단모두nativeorigin52/110을실제로관찰했다.

display는same015 정상Rockman0 checkpoint에서PET pointer/table read만alias해nativecontextreset과원본명령을 실행한다. directROM/RAM 쓰기없음,diagnosticcheckpoint 격리,alias는제품ROM에설치되지 않는다.768800script2의원본MrProg1F portraitprefix=f4001fe700이며7C9C44script0은e700만시작하고mugshot명령없음. 실제후자2화면에초상화가없음을확인했고 임의화자/portrait를추가하지않았다. 주변script1의LaserMan을script0화자로확정하지 않는다.

소울유니존 문구는legacy tutorial이다. 이번표시는설명의자연진입·EXE4.5실제기능지원·배틀결과/보상/저장증거가아니다. world의자연caller와원래화자도미검증이다. Mesen의한정된관찰이며실기/다른에뮬레이터전체지원주장이아니다.

## 보류와 다음 재개

`middle_dot_reconciliation.json`은실제integration.json과ROMhash에연결된다. historic19개중014까지10적용,이번4추가로14적용/5미적용이다. 신규6개중7688002:0/2:2는historic19에없었던동일script의폭보완문구다. 이는전체게임미번역수 또는 의미검수완료수와 다르다.

남은historic5개:7B4184:0:0/0:3/4:0(선택지·전체script geometry/분기 결과),7CC6A0:76:0/78:0(mmbn45s 작은메뉴renderer). 준비기록의전체script0/4와작은메뉴분석을 따른다.010 waitHold의actualbattlecaller, dynamicnickname4개와다른compressed/fixed/UI/자연진행/사람검수도 남았다. **실제 자동한글 조합·commit/save/redisplay ABI는미완료**이며 일본어자판3페이지/한글동작라벨이나CPU후보를한글입력·저장완료로세지않는다.

재현:014handoff의원본기반전체빌드명령에 `--pending-batch500-015`를 추가하고 새출력명을 지정한다(이전모든flags보존). `cumulative_batch500_015.py`의동결된누적preflight와제품input검사를 거친다. static/CPU/정상회귀는015wrapper및기존CLI를 사용한다. 표시capture=`run_cumulative500_015_displays.py`,검증=`verify_cumulative500_015_displays.py`; capture완료만으로pixel검증완료를세지않는다. 생성결과에덮어쓰지않는다.

보존hash작업끝재확인:원본 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`,014 `6cdcae37d8682c03a909b08d3ddefea02ad825c6a272899c38bcc5f316be9245`,기존ZIP `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`,모두동일.
