# 거츠맨 일정 알림 후속 페이지 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_alarm_followup_v1.gba`, SHA256 `510b75b9c9931af339f7df2b8c5b55789667badf392ebece5f5ca998cd8d5dc3`. 신규2literal,누적2,282선택 literal/57선택·675원본 유지 archive. 전체 번역 완료 아님.

## 번역·현재 선택 범위

원본66651C:771bytes/28slots/root038124, payload SHA `16cd2ff2d4af233f94277cb9077169046a4abe04f4789c735e77495697f18852`; TPL SHA `8286cb9ad04ff3ac3ec9f09570327fd24da70450943fd7f4e5209a19d6e1dce1`.

- `66651C:1:1`: `はやくしないと、\nオープニングを\n見のがすでガッツ!!` → `서두르지 않으면、\n오프닝을\n놓치겠거스!!`.
- `66651C:2:1`: `ガッツマンも\nたのしみでガッツ!!` → `거츠맨도\n기대되거츠!!`.

TV 시작 알림/약속 알림의 두 번째 페이지다. 해당 첫 페이지의 가변 이벤트 이름 출력과 원본 suffix,닉네임/식사/기타알림/별도mugshot21..26/등록·시간도달성은 이번 번역 범위에 넣지 않았다. 가변 이름 뒤 한국어 조사를 추정 고정하지 않았고 caller·window·keyWait/clearMsg·sound/wait96·flags3585/3658·callBufferEventName/printScheduleBuffer/callCheckNowEvent/callFindNowEventType·waitHold는 보존한다. 기존 거츠/거스 초안 말투를 사용하고 인간 검토를 기다린다. NumberMan4649 승인은 이 문구 승인으로 전용하지 않는다.

기존3문구 editable authority `translations/gutsman_schedule_alarm_ko.json`/SHA `36eeaab87a9091d0c59e1df75d4d4bf1ab953a378f3b69b95fbe7c39f117b9a0` 불변. `tools/gutsman_alarm_followup.py`는 읽기 전용3projection+개별 작성한2문구를 새 `translations/gutsman_alarm_followup_ko.json`에 직렬화하고 parent 전체3unit/hash를 검사한다. 제품 빌드는 `--gutsman-alarm-followup`/registered `alarm-followup-v1`의 단일5unit writer를 선택하며 dependency는 input hash로만 기록해 이중 집계하지 않는다. 기존 기본3scope 및 prior candidate 보존.

## 검증 상태

자체 freshFF저장/cold이어하기/정상PET16구간과 격리 알림1/2/4/6,주소 이동 영향의Guts chip13 회귀 완료. `analysis/gutsman_alarm_followup_v1/runtime.json` PASS. 메인이 `alarm_pages.png` 5페이지/PET8장면composite와chip13실제화면 직접확인. 기존 source-only alarm observer의 기본 계약은 보존하고 새 opt-in wrapper만 relocated66A844/root038148을 manifest로 파생하여 검사한다. root/entry를 read-only 한 번씩 별도 반환하는 진단이며 ROM/RAM/RTC/save/진행flag 쓰기나 다른 후보checkpoint 수입 없음. Wrapper/base/probe hashes·원본consumer code guards·각한 번 alias·자체 exactROM/정상parent 검증 PASS. 진단checkpoint 정상chain재사용금지; 실제시간알림/등록이벤트/퀘스트 획득 증거로 세지 않는다.

TV1:1(step4)20glyph/2,796font→OBJ VRAM→screen pixels·빈영역2,803pixels;약속2:1(step4)11glyph/1,560pixels·빈영역4,039pixels PASS. 기존학원4:0(step2)11glyph/1,512pixels/빈영역4,087와4:1(step4)13glyph/1,824pixels/3,775,추가알림6:0(step2)6glyph/828pixels/4,771 PASS. 실제clearMsg로일본어첫페이지에서한국어두번째페이지로 넘어간 뒤 잔상·line geometry·CPUglyph reads·keyWait/clear boundary·nativearrow footprint분리·오른쪽border·page순서검사 PASS. 마지막keyWait에서멈춰 callCheckNowEvent/추가dispatch 및실제등록시간/반복알림을 증명하지 않았다.

Guts chip13 새주소에서2완성샘플 actual15register/SP/LR·native128copy→RAM·E5·47px이름/결합행81px·font/OBJ VRAM/화면·clearing·종료 PASS. Roll은 이번ROM에서합성CPU guard 회귀만 실행했고 이전ROM의화면증거를 이번ROM의새실행으로세지 않는다.

정상넘버맨 새64KiB저장success58/save SHA `7a3b38f27ece391dd15b8609b74e60025ba66aa514f32ef1d447653095e9bfaa`·직후snapshot/현재disk일치·다른save불변·checkpoint없는cold이어하기3페이지 PASS. 거츠맨인사2페이지/PET8장면22literal/29focus·No수락·B취소 PASS. 기존56archive payloads·66651C의다른26scripts와prior3문구/hash·그래픽15라벨5블록actualROMbytes 불변, ‘통신’ 유지. 한글이름입력/거츠맨저장/Yes후통신 자체 검증 아님.

관련37tests(거츠맨34/이름selector3) PASS.622Python tools AST PASS. 신규test는 parent 변경/자식writer 부재/잘못된carry count를 거부하고5unit source/control skeleton·행 수·132px 범위를 검사한다. 전체5문구 최대103px≤132px; 새TV3행103/48/82px와약속2행48/82px.24미선택script spans source-identical 및1/2첫페이지의이벤트commands·원문 literal·keyWait/clearMsg까지prefix bytes 원본동일 PASS. 합성selector64CPUvectors PASS(실제runtime 아님). main/repro/finalcurrent_repro 동일SHA/622tools drift=[]/원본 보존 감사 PASS `analysis/gutsman_alarm_followup_v1/final_identity_audit.json`. PEThelper의 선행 chipquest 후보/기존66A844변경계약도 별도출력 `backward_pet_helper`에서 읽기재검증 PASS.

`analysis/full_scope_gutsman_alarm_followup_v1/`: 선택2,282/미선택일본어포함27,766/기타1,859; catalogue732/31,907canonical literals/parse errors0. dependency3은 selected literal로 중복 계산하지 않으며 manifest2282와 일치한다. 이 catalogue는 전체ROM 번역 완료 분모가 아니다.

## 다음·미해결

66651C의16미선택literal: 동적 이벤트/닉네임 suffix와 별도mugshot renderer/capacity/등록·실제시간·반복알림. 현재 읽기 전용 진단에서첫페이지 event buffer가 비어있을 수 있으므로 실제등록값을 출력했다고 주장하지 않는다. 이후 전체텍스트/이미지/inline/fixed population,한글이름편집→committed record→모든재표시→영구재로드→기존save호환,prior wait-arrow53pixel 차이,인간 문구 검토가 남는다. 가장 어려운 한글이름persistence 조건은 해결되지 않았다. 배포·전체완료 선언 없음.
