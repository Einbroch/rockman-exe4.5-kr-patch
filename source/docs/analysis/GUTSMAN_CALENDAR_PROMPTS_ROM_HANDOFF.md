# 거츠맨 일정 입력 질문 — 2026-10-07

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후속현재후보는 `GUTSMAN_CALENDAR_CONTENT_ROM_HANDOFF.md`의내용·약속상대2문구추가ROM이다. 이문서는이전2질문범위와실패/검증증거의역사기록으로보존한다.

후보 `poc/output/exe45_ko_development_gutsman_calendar_prompts_v1.gba`,SHA `68a8d4d0c13d39cc6e80c0bbd3e367d6469062e042363dad2b59461573a56cee`. 신규2literal,누적2,285선택literal/58선택·674원본유지archive. 전체 미번역 완료 아님. runtime/최종 current_repro_r2/audit PASS,현재 검증된 개발후보.

## 번역·반영

`665698:20:0`「時間は何時からでガス?」→「몇 시부터 시작하거스?」135px,`665698:21:0`「どのタイプでガス?」→「어떤 종류거스?」91px. 원본 일정 시작시각/일정종류 입력 질문,실제 정상 메뉴 화면으로 context 확인. 기존 거츠/거스 말투 초안 사용,별도 인간 wording 승인 없음/NumberMan4649 승인 전용 없음.

원본665698:2,077bytes/255slots/root0322E4,payload SHA `f8592c08c3a5c763052780ccaa48cbd74a1568898eec37425da47530304356ca`,TPL SHA `17f59df298ea973d4da8e1958eb42aa552104717c8922990c56dfd3621203a2e`. 원본 source를보존한 등록 relocation/단일 `translations/gutsman_calendar_prompts_ko.json` writer. 신규 `--gutsman-calendar-prompts`만 추가,기존57선택archive 자산 및 코드기능 보존. standard mugshot52,110/183px범위,원본 callSkipMugshotFadeIn/msgOpenQuick/GutsMan/textSpeed0/waitHold·입력/RTC/save controls 보존. 선택2/미선택69literal·253script spans 원문 유지.

main/repro/final current_repro_r2 동일 SHA,관련39tests(거츠맨36/칩이름selector3)/632Python AST PASS. 최종632tools drift=[]/원본 SHA588a77da... 보존,`final_identity_audit.json` PASS. 최초 current_repro는검사단계정정전report 소스를기록했으므로삭제/최종으로전용하지 않고보존,최종tool identity는r2에결합한다. Inventory `analysis/full_scope_gutsman_calendar_prompts_v1/`:선택2,285/미선택일본어포함27,763/기타1,859,catalogue732/31,907canonical/parse errors0. Catalogue는전체ROM 완전성 분모 아님.

## 고정 baseline 정상 일정 등록·이름 비교

직전 exact식사ROM SHA `d55433eb563313f4e2fe80ade4ba452ebd9f97345c27f997488f929ee6ccac25`을 그대로 유지,자체 정상select-gutsman checkpoint에서 정상 버튼만 사용. `gutsman-event-buffer-native-v1-today/calendar/time/meal-register/meal-query`5구간,ROM/RAM/진행flag/RTC주입·alias 없음. 오늘 일정 없는 정상2페이지 후,right→일정등록→2000/1/1 AM2:00→식사 선택→native commit→PET L 조회.

`analysis/gutsman_event_buffer_native_v1/runtime.json` PASS: 식사 preset 원본ROM의선택된6368E8:62한글payload `f9fcdd16f9fcac14e5`가nativecopy08032AC6으로02026080에203frame,308frame에0200131A로복사. committed32byte record `03000001010602000002f9fcdd16f9fcac14e500000000000000000000000000`. 같은 세션 조회의02010C40/C44두 Hangul glyph·E5 atC48/7parser reads·font/OBJ VRAM/화면pixels 일치. 화면을 직접 확인했다. per-glyph color는이번추적에없어서active0200FABC snapshot을사용한pixelproof로명시;trace값으로꾸미지 않았다.

이번 query의 buffer는hour02010AC0/minutes02010B40/AMPM02010BC0/name02010C40이며,지난 alarm alias의 잘못된32byteAC0소비와 consumer 상태가같다고 단정할수없다. 새 write watch AC0..AE0은hour writer만포착,이름C40producer 추적 아님. C40 생성/선택recordread와정상 reminder/event초기화→alarm 소비는아직연결되지 않았다. 따라서정상식사 query PASS를TV/약속alarm first-page/시간alarm PASS나alias원인확정으로 확대하지 않으며,새ROM의등록commit 증거로도 이전baseline을전용하지 않는다. 앞선32bytes 실패와이후정상query 비교증거 모두보존.

## 새 ROM 실행 검증·미완료

`analysis/gutsman_calendar_prompts_v1/runtime.json` PASS. 정상 calendar6/script20:12glyph/1,620검사pixels/5,540빈pixels clearing, time5/script21:8glyph/1,092검사pixels/6,068빈pixels clearing. 실제 CPU glyph/font→OBJ VRAM→화면일치/행offset·135px/91px/원본거츠맨mugshot·border 불변 PASS. 두 화면 및 새Guts칩13/넘버맨귀환 화면 직접시각확인 완료.

정상 자체FF저장→native script58→checkpoint없는 cold이어하기/넘버맨3·거츠맨인사2/PET8장면22literal·선택No/B취소회귀 PASS. 새64KiB save SHA `7039a1597c646cc9eda4ba307c68b7abfc5dbc411e69c7563f7385156af5479f`. 기존알림6페이지/meal native닉네임결합2샘플·Gutschip13 이름/ABI/128copy 두 화면·합성selector64vectors PASS. 롤 새화면은미실행/합성guard검사만. 기존57archive와자산SHA/그래픽15라벨5블록/‘통신’bytes불변. 모든진단state는정상chain재사용금지,알림실시간등록/dispatch검증으로세지않음.

새ROM 자체freshFF저장/cold이어하기/정상PET16구간·알림6페이지/meal2샘플·칩13 회귀 후정상 calendar6/script20,time5/script21 두질문 검사완료. 최초 time6도21로예상한검사는실패로보존(`analysis/gutsman_calendar_prompts_v1/failed_sample_expectation.md`):native A로22내용입력까지진행했으므로원문그대로이며PASS로세지않음. ROM/state/font/pixel tolerance 변경없이관측단계만정정,asset의time6참조는TV선택후context이고종류질문직접증거는time5다. runtime 결과/스크린샷 및마지막 current_repro_r2/audit를기록하고최신개발후보로승격했다.

가장어려운 한글이름입력→committed record→모든재표시→영구재로드→기존save호환 조건은미해결. 식사일정 preset의같은세션등록조회는임의이름편집/영구호환을증명하지 않는다. 일정입력의다른69literal/알림15literal/전체이미지·inline/fixed population/prior wait-arrow53pixel차이/인간review·실제RTC alarm/TV·promise·other event name 생성경로도남음. 원본/선행ROM/save/실패증거보존,배포/전체완료선언 없음.
