# 거츠맨 일정 내용·약속 상대 — 2026-10-07

후속 최신 후보는 `analysis/GUTSMAN_CALENDAR_HOME_ROM_HANDOFF.md`의 확인창·달력 홈 ROM이다. 이 문서는 이전 내용/상대 질문 단계의 증거로 보존한다.

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false. 전체 미번역 완료 아님.

현재 검증된 개발후보 `poc/output/exe45_ko_development_gutsman_calendar_content_v1.gba`, SHA256 `e8ab0e4a8381d904d92e155a6852369c70532449f6fd74386831607fd4f0e4d7`. 신규2/누적2,287선택literal·58선택/674원본유지archive. 정상4질문 runtime와최종 current_repro_r3/audit PASS,main/repro/r3 동일SHA/636tools drift=[]/원본SHA588a77da...보존. 단초기TV모서리1pixel전이차이는미해결범위로남고전체시각QA·배포완료가아니다.

## 반영 범위와 입력 보존

665698:22:0「どんな ないようでガス?」→「어떤 내용이거스?」103px, 665698:23:0「ダレとの やくそくでガス?」→「누구와 약속이거스?」115px. 각 문구 개별 수동 작성, 기존 거스 말투 유지, 인간 wording review는 미완료. NumberMan4649 승인 전용 없음.

`translations/gutsman_calendar_content_ko.json`만665698의writer로선택. 이전 `gutsman_calendar_prompts_ko.json` SHA `58ccc8ac8c45883f13c47ee7dd389df8c05568a7c3bcad202ea452daa537b5ec`/2units는읽기전용projection·해시검사dependency이며두번집계하지않는다. source2,077bytes/255slots/root0322E4, payloadSHA `f8592c08c3a5c763052780ccaa48cbd74a1568898eec37425da47530304356ca`, TPLSHA `17f59df298ea973d4da8e1958eb42aa552104717c8922990c56dfd3621203a2e`. 신규 flag `--gutsman-calendar-content`는이전 prompts scope를요구하고단일child만선택한다. 원본 callSkipMugshotFadeIn/msgOpenQuick/GutsMan/textSpeed0/waitHold 및선택·등록·RTC·save controls 보존.

이전58archive중다른57payload동일, 같은archive는22/23두script만변경/나머지253span 동일. 원본기준선택20..23/4literal, 나머지67literal/251scriptspan 원문유지. 기존선택자산SHA/그래픽15라벨5블록·‘통신’bytes불변. 원본 ROM/선행ROM/save/실패캡처 삭제·덮어쓰기 없음.

## 정상 실행과 검사 범위

`analysis/gutsman_calendar_content_v1/runtime.json` PASS. 자체freshFF저장→native NumberMan script58→checkpoint없는cold이어하기→NumberMan귀환3/거츠맨인사2/PET8장면22literal·No/B취소회귀 후, 자기 normal calendar→time→time-stable→person-stable→person-input chain. 다른ROMcheckpoint/진단alias state를정상parent로가져오지않는다. 정상record/name/flags/RTC 주입없음.

실제검사대상: calendar6/script20 12glyph/1,620pixels/빈5,540pixels; time5/script21 8glyph/1,092pixels/빈6,068pixels; time-stable6/script22 9glyph/1,236pixels/빈5,924pixels; person-input2/script23 10glyph/1,380pixels/빈5,780pixels. CPU glyph·font공급/행offset/OBJ VRAM/화면·전체stream·clearing·183pxcapacity 및거츠맨초상/세경계ROI PASS. 4화면합성 `calendar_prompts.png`과 새칩13/식사2/넘버맨귀환5를직접확인.

time5의script21 실제배경은`1회만`주기선택이며, 다음A time6의TV/친구/식사/학원목록은script22. 친구focus만으로23이되지않고, A확정후script23/‘그외’상대선택목록으로진입한다. 이전‘focus=23’예상은기각/정정했다. 한글이름입력이나일정commit을증명하지않는다.

같은64KiB 새save SHA `e0229527c78342653dbeed1d13666f3559894a7b9340ac82ed4c11799fc9a865`. 저장·이어하기는NumberMan회귀이며GutsMan/Hangul이름영구호환증거아님. 알림6페이지/식사native닉네임2샘플·칩13이름/ABI/128copy회귀와합성selector64vectors PASS. 알림·칩alias진단은실제RTC発火/퀘스트進行증거로세지않고정상chain재사용금지. Roll새화면은미실행/합성guard만.

## 실패 증거와 초상 비교 조건

`baseline_route_investigation.md`, `failed_portrait_phase_comparison.md`에예상/관측/기각/다음검사를분리해보존했다. 최초report는calendar눈부근22pixel·TV모서리(1,105)1pixel차이로전체PASS거부. 다음report는friendfocus22를23으로기대한것을실제RAM/전체glyph검사로거부. ROM/flags/font/색상/BlendFrames/ROI/픽셀허용오차 변경없음.

기존고정ROM SHA `68a8d4d0c13d39cc6e80c0bbd3e367d6469062e042363dad2b59461573a56cee` 자신의 calendar/time checkpoint에서각90 native animation phase를read-only로캡처. calendar의세ROI전체가기존native phase33과RGB0오차일치. 새TV는동일normal버튼경로에서마지막A후90frame추가대기한time-stable6의세ROI가기존native TV phase1과RGB0오차일치한다. friend선택후23은기존ROM 자신의person-input2와세ROI0차이. 각reference route/artifact/ROM/tool해시와실제RAMroot/script를검사하고해당화면해시를runtime receipt에보존한다.

최초TV capture의모서리1pixel차이원인은여전히transition-scope 미해결. 안정후4질문표시PASS를초기전이완전동일/버그수정/전체시각QA완료로확대하지않는다. 기존 wait-arrow53pixel문제도별도미해결.

## 다음 번역과 완료 조건

새ROM 자신의time checkpoint에서식사선택→normal confirmation24를확보: `poc/runtime/gutsman-calendar-confirmation-baseline-v1-meal/step_005.png`, 실제RAMscript24/원문「いじょうで いいでガス?」/はい・いいえ. `translations/gutsman_calendar_confirmation_ko.json`에다음3초안(이렇게 하면 되거스? / 예 / 아니오)을준비했다. 4parentunit의SHA/projection·원문·제어skeleton·두newline/선택지두trailing spaces 검사PASS. **현재ROM에는미반영**이며variant의도적미등록으로build선택거부를확인했다. 다음단계: 정확한choice cursor/글자배치/Yes·No·B/확정·취소·등록record검사계약을등록한뒤단일7unit writer로빌드/자체normalchain검증. 이를현재2,287선택count에더하지않는다.

최신inventory `analysis/full_scope_gutsman_calendar_content_v1/`:732catalogue/31,907canonical/parse errors0, 선택2,287/미선택일본어포함27,761/기타review1,859. Catalogue는전체ROM완전성분모아님. 665698다른67literal/66651C15literal, 이미지/inline/fixed populations, eventname C40producer→reminder초기화→alarm소비·실제RTC, 한글이름편집→committed record→모든재표시→영구재로드→기존save호환이남음. 기준식사ROM의같은세션등록조회증거는이번ROM의영구이름호환·TV/약속alarm검증으로전용하지않는다.

관련41tests(거츠맨38+칩이름selector3)/636Python AST PASS. main/repro/current_repro/current_repro_r2 ROMsha동일이나후자의tool receipt는검사정정전자료로보존하며최종은current_repro_r3에결합한다. 최종audit 결과는이문서첫단락에반영한다.
