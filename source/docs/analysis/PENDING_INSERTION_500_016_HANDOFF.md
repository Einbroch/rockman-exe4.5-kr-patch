# 016: 정확히500개 추가 ROM 반영

과거 기준 기록이다. 후속017에 미적용500개 추가·제품/화면 검증이 완료됐으며 현재 권위와 재개점은 `PENDING_INSERTION_500_017_HANDOFF.md`다. 아래016 결과는 변경하지 않고 해당 artifact의 증거로 보존한다.

현재 개발본 `poc/output/exe45_ko_development_pending500_016_v1.gba`, SHA256 `d58330fba33d9656e90405309afc39496483aacce2df73908e62b53a4f64bd08`. 독립 `_repro.gba` 전체 바이트 동일. 실제500 source-ID 추가/기존 누락0, 누적 소비 단위8,622→9,122, 주347/미변경385아카이브. 사용자 지시대로500개 묶음으로 ROM 적용했다. 새BPS/xdelta/ZIP은 만들지 않았다. 원본·이전ROM/세이브/증거·기존ZIP 보존. NON-DISTRIBUTION, needs_review/release_eligible=False 유지.

## 좁은 주소 필터 재평가와 실제 선택

기존 일반raw selector는680000..7FFFFF만 보았다. 이 조건의 잔여0을 전체 미적용0으로 취급하지 않았고, 이번에는 원본과 고정된 draft-first corpus를 다시 대조했다. `pending_insertion_500_016_survey_v1/survey.json`은source/verified015/TPI/`translation_first_v1/coverage.json`의고정draft hashes에 연결된다. 변경/누락된 고정입력0, conflicting wording을선택하지 않음. 새로운 문구 작성·자동 prose축약/치환0; 기존 번역을 그대로 재사용한다.

유한 후보538script/754units 중665units는과거 주소 필터보다앞에있었다. 이는즉시 삽입가능 판정이나 전체미번역수가 아니다. 압축/size-header·알수없는references·다른renderer·print변수·선택지·불명확한windowcaller·채택geometry초과·부분적용script 등의별도조건을 분리했다. source language가mmbn45이며msgOpen/msgOpenQuick·3행132px·원문LF유지 조건을만족하는일반대사 후보만선정했다. 작은메뉴/선택지/변수 삽입은normal처럼무조건 넣지않았다.

기존 compiled-record 아카이브와원래 registry가이미소유한 아카이브를전부제외한범위는609units/63archives였다. 이중아카이브별 완전한eligible script 묶음으로정확히500개를선정했다. 최종24archive/378script다. 각script의Japanese literal 전체를선택하고 나머지nativecommands/scripts는보존했다. 같은script의:10/:2를문자열정렬로재배치하지않고 원본TPL순서로asset을생성했다. source/control/order를고치는작업이아니다.

선택 권위 `pending_insertion_500_016_selection_v1/selection.json`. generation은`prepare_batch500_016_inputs.py`가이동결결과만소비하며현재productbuild에서후보scan/knapsack을재실행하지않는다. 최종asset의source_draft_links는500개각각의원래draft path/hash/ID와고정selection hash를보존한다. 원래초안은변경하지않았다. 선택번역에Japanese residue0, 모두needs_review이며 의미/말투/용어의사람승인을뜻하지않는다.

## 사전 검사와 제품 경로

`pending_insertion_500_016_preflight_v1/preflight.json`: 원문/실제nativepayload·knownpointer/TPI·native roundtrip·semantic/binary roundtrip·제어·인코딩·글꼴·채택line/row·500distinct-ID·기존교집합0·geometrycandidate0 PASS. source-only결과는ROM미반영이므로제품검증과구분한다.

`pending_insertion_500_016_cumulative_v1/preflight.json`: exact015 base/hash,source-onlyhash,고정24새rawarchive,각script count·native source/pointers,단일writer/미선택source preservation을묶는다. PROFILE016의prepared_016은고정500input을재현/검사하고최종selectedasset에도source_draft_links를보존한다. 기존productflags모두유지+`--pending-batch500-016`을원래builder3단계에연결했다.015 prerequisite,ExpectedWrites에새knownpointers를등록하고immutable원본부터빌드했다. 이전ROM위에순차patch하지않는다.

선택script의명시적positionText는307곳 모두92/110이었다. sourcepositionBox/msgOpenQuick/arrow명령은그대로이며normal3행132px은채택표시범위다. native source keyWait/waitHold 및event/flag/caller명령도보존했다. keyWait없이waitHold로표시하는경로와실제eventcallee는각각의caller 검증이남으며,source명령을임의로keyWait로바꾸지않는다.

## 같은016 ROM 검증

- `pending500_016_v1/integration.json`: actual500-ID delta/기존누락0, 이전334페이로드/소비metadata 동일. 새24개의미선택script/source storage·compiledpayload·actualknownpointers·전체write/header/ISA·exactancestry감사,독립재빌드byteidentity PASS.
- `selector_cpu.json`: composed mail/keyitem/gear3,195 합성CPU조건 PASS;실제플레이증거아님.
- `rejection_controls.json`: 기존declaredunit/ID/metrics/retainedpayload4결함reject PASS. `new_archive_controls.json`: 새payload/ID/pointermetadata/pointerbytes/source storage5결함reject PASS. validartifactaccept,메모리내변조만수행.
- codec6tests,denominator3tests,관련syntax PASS.
- `normal_runtime.json`: exact016 coldboot·초기설정·기존일본어자판3페이지VRAM/map·native21-namebank/네내비OAM·첫I.P.C.메일23orderedkeyWait/native3archive RAMload/list복귀/재열기 PASS. `first_mail_pages_v1.png`23쪽직접시각검사.
- `display_runtime.json`: 신규문구중11literal/198glyph샘플의actualfontCPUreads→OBJVRAM→화면pixels,root/keyWait/페이지지움 PASS. `changed_pages.png`11쪽직접시각검사.

표시sample:65AFA0:23 록맨식사알림1쪽,67CB70:23 썬더맨식사2쪽(원본portrait17/2F),66CA84:11 음식질문5쪽/677F64:15 꿈질문3쪽(positionBox+msgOpenQuick,원본textorigin92/110). sourceprefix를원본byte에서읽어고정했다. 큰box52/110과작은box92/110을분리검증했고마지막selectedkeyWait뒤event/flag/terminalwaitHold는진행하지않았다.

같은016 정상Rockman0 checkpoint에서PET pointer/table read만alias하여nativecontextreset/원본명령을실행했다. 직접ROM/RAM쓰기없음,checkpoint격리,alias는제품ROM에설치하지않는다. quickprofile샘플의록맨배경이미지는진단시작Navi문맥이며실제윈드맨/파이어맨의자연profile진입이나portrait증거가아니다. 원래화자/내비lookup을ROM에서바꾸지않았다. 11쪽이500개전체자연scene/플레이/말투승인을증명하지않으며Mesen한정관찰이다.

## 재개와 한계

사용자500개단위정책을유지한다. 다음500개는actual016기준으로다시대조하고,부족하면caller-context/기존부분적용/선택지/변수/별도renderer의소비계약을먼저확인한다. survey의754후보/609untouched단위는015기준의유한검사범위이지현재전게임잔여수나준비완료수로재사용하지않는다. 500을맞추기위해중복ID나이미적용한문구를재집계하거나검사를무시하지않는다.

historical가운데점5개(7B4184선택지3,7CC6A0작은메뉴2),010waitHoldactualbattlecaller,dynamicnickname4개,다른compressed/fixed/UI/자연루트·사람검수가남았다. **실제자동한글조합·commit/save/redisplay ABI는미완료**다. 현재일본어자판/한글동작라벨/CPU후보를한글입력저장완료로세지않는다. 개발용ROM이지release완료본이아니다.

재현:015원본기반전체build명령에 `--pending-batch500-016`과새출력명을추가한다(이전모든flags보존). 고정selection/input→`prepare_pending500_016.py`source-only→`cumulative_batch500_016.py`cumulative→제품builder→`verify_cumulative500_016.py`/CPU/정상회귀/`run_cumulative500_016_displays.py`로검증한다. 이전결과에덮어쓰지않는다. 새선택조사는현재artifact를기준으로별도분석에서수행한다.

보존해시작업끝재확인:원본 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`,015 `a6d3b0330566374937857cb49b2f07475a6c590e73ac6873486556585a4f4d81`,기존ZIP `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`,모두동일.
