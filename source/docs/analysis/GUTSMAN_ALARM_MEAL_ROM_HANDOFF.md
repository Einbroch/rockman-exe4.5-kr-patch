# 거츠맨 식사 알림·이름 결합 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_alarm_meal_v1.gba`,SHA `d55433eb563313f4e2fe80ade4ba452ebd9f97345c27f997488f929ee6ccac25`. 신규1literal,누적2,283선택literal/57선택·675원본유지archive. 전체미번역완료 아님.

## 반영 범위·권한

`66651C:3:0` 원문 `、\nゴハンの じかんでガス!` → `、\n밥 먹을 시간이거스!`. 원본 닉네임 출력 뒤 쉼표11px/줄바꿈 그대로,본문123px≤132px. 가변 닉네임 뒤 받침-dependent 조사 없이 직접 식사 시간을 알린다. 기존 거츠/거스 초안 말투·needs_review,NumberMan4649 인간승인 전용없음.

원본66651C:771bytes/28slots/root038124,payload SHA `16cd2ff2d4af233f94277cb9077169046a4abe04f4789c735e77495697f18852`;TPL SHA `8286cb9ad04ff3ac3ec9f09570327fd24da70450943fd7f4e5209a19d6e1dce1`. Native nickname F90C01/쉼표/줄바꿈·position/window/arrow/keyWait/clearMsg·event checks/flags/dispatch·sound/waits·RTC/save 원본보존. 정상시간/등록일정/후속event dispatch·한글이름persistence 검증으로세지 않는다.

기존5unit authority `translations/gutsman_alarm_followup_ko.json`,SHA `2885f95849e7a343476c5f2c97bad0418ae9de91a9efe45e0b70f7849f3b6bdb` 불변. 이전3unitauthority/hash도불변. `tools/gutsman_alarm_meal.py`가 읽기전용5projection+신규1문구를 새 `translations/gutsman_alarm_meal_ko.json`에 직렬화한다. 제품빌드 `--gutsman-alarm-meal`/registered `alarm-meal-v1`은 단일6unitwriter 선택,5/3dependency는각각명시role/path/hash/전체unit일치검사후 input해시로만기록하고 selected 중복집계하지 않는다. 닉네임suffix validator는첫줄쉼표source-identical/non-growing과동일줄바꿈을 강제한다.

## 선행 관측·이벤트 이름 경로 보류

직전 exactROM `exe45_ko_development_gutsman_alarm_followup_v1`/SHA510b75b...의자체정상select-gutsman parent로 `capture_gutsman_alarm_names.py`를 실행했다. script1/3read-alias 각1회,ROM/RAM/RTC/save/flags수정 없음. 소스parser0804F88A의 `ldrb r1,[r4]`/bytes2178 원본동일 guard 뒤 RAM token reads와실제glyphs를 기록한다. 미출력을추정빈버퍼로취급하지 않는다.

- `poc/runtime/gutsman-alarm-names-baseline-v1-script3`: nativeRAM02010AC0..C3/9b9ba5b9,E5 atC4,4glyph/44px,원본「ああさま」 정상소비.
- `poc/runtime/gutsman-alarm-names-baseline-v1-script1`: 같은RAM에 `a0e30420`×8/32bytes,E5 at02010AE0.32glyph는native11px각/352px. 정상등록TV이름 샘플이 아니며 source event-name first-page footprint가PET132px범위를 넘는다. 첫페이지 PASS로채택하지 않음.

확정관측은바이트/폭/종료/실제glyph읽기뿐이다. `callBufferReminders`·이벤트선택초기화를건너뛴 alias가입력전제조건을충족하지않았을 가능성이현재가설이며 정상게임의버퍼bug/번역fontbug로확정하지 않는다. 동일baseline에서닉네임은정상으로분리됐으므로이벤트불확실성을meal로확장하지 않았다. 새모델로가짜event를채워통과시키지 않고 TV/약속/기타이벤트이름앞뒤문구는원본보존한다. 이전 ‘event buffer가비어있을수있음’은추정가능성일뿐;이번직접관측은비어있지않았다. 선행TV/약속두번째페이지clear후검증의범위를첫페이지/정상등록값으로확대하지 않는다.

skill debugging/tips검색에서late observation/init prerequisite의비교경계를확인했다. 사례는GBA의원인증거가아니다. 다음구별관측은정상일정등록→실제reminder초기화→eventbuffer생성→이름소비를연결하는경로이며 현재미해결. 깨진alias첫페이지를현재ROM의정상게임실패로단정하거나release제한승인으로닫지 않는다.

## 현재 검증 상태

제품빌드main/repro/final current_repro 동일 SHA,원본 보존/627 tools drift=[]; audit PASS. 자체 freshFF저장/cold이어하기/정상PET16구간 및 기존알림1/2의두번째페이지·4/6·chip13회귀와신규meal3의격리render검증 PASS. 모든진단checkpoint는정상chain재사용금지. `analysis/gutsman_alarm_meal_v1/runtime.json` passed=true/release_eligible=false.

meal step2/3 두 완성 샘플은 실제 native nickname「ああさま」/9b9ba5b9e5/44px,쉼표 포함 첫줄55px/본문123px,16glyph/2,136검사pixels/3,463빈pixels clearing PASS. parser RAM 주소·각byte·E5종료와실제glyph→font→OBJ VRAM→화면일치,화살표/경계·ink 비가림 검사 PASS. `alarm_pages.png`,식사 `step_002.png`,정상 `pet_regression/normal_pet_prompts.png` 직접시각확인 완료. 진단 식사 화면 검증이며 실제시간에 따른 식사 알림 발생은 미검증.

넘버맨 새저장 script58/64KiB save SHA `91cad204d7b86d47763d195190ec94157dbc7739a288b8615f1ed0326b79a56e`,checkpoint 없는 cold이어하기/3대사 PASS. 거츠맨첫인사2/PET8장면22literal 회귀 PASS. 기존56archive/66651C다른27script/기존5문구·그래픽15라벨5블록 bytes 불변,‘통신’ 유지. 거츠맨chip13 두 화면 native128copy/ABI/이름/본문 PASS,롤은 새ROM 합성selector64vectors 검사만. 기존후속알림 보고서도 이전exactROM으로 재검증 PASS.

관련39tests(거츠맨36/이름selector3),627Python AST PASS. parent변경/없는childwriter/잘못된carry count/닉네임suffix확장·source/control skeleton·줄수·폭fixture 검사 PASS. Inventory `analysis/full_scope_gutsman_alarm_meal_v1/`:선택2,283/미선택일본어포함27,765/기타1,859,catalogue732/31,907canonical/parse errors0/manifest2283일치. 이catalogue는전체ROM번역분모가 아니다.

## 남은 범위

66651C의15미선택literal: 이벤트이름first pages와기타알림·별도mugshot21..26·source!! 등. 실제등록/시간/반복알림과임의nickname/population,한글이름편집→committed record→모든재표시→영구재로드→기존save호환(가장어려운조건),전체이미지/inline/fixed population/prior wait-arrow53pixel차이·인간검토도남음. 원본·선행후보·실패/진단·save 보존,배포/전체완료선언없음.
