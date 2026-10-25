# 거츠맨 칩 탐색 대사·칩 이름 통합 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_chipquest_v1.gba`.
SHA256 `bc3b668de37dbbe73eecec00c0d04315b4e14adce7c16fdadd0039e42103283a`.
신규2번역 literal, 기존 빅해머1 wording 재사용/신규 이름 wording0. 누적2,280선택 literal /57선택·675원본 유지 archive. 거츠맨 R66A844의33literal을 모두 초안으로 선택했으며 전체 ROM 번역 완료는 아니다.

## 입력·의미·구조

`66A844:13:0` 원문 `ガッツガッツ!!\n「` → `거츠、거츠!!\n「`.
`66A844:13:1` 원문 `」 を\nゲットするでガス!` → `」를\n얻겠거스!`.
가변 이름을 사이에 삽입하는 한 페이지의3행이다. printChip buffer0/chip104·keyWait/clearMsg/waitHold·source nickname/numeral/flag/item/tournament/weekday commands를 변경하지 않았다. 칩 획득이 완료되었다고 번역하지 않았다. 기존 거츠/거스 초안 말투를 유지하고 인간 문구 검토를 기다린다. 넘버맨4649 승인을 전용하지 않았다.

원본66A844:2191bytes/255slots/root038148, payload SHA `ab59357517b022252695e2b9785bf85a45fbab48e3444c5964d75e9c0d930795`, TPL SHA `4793441d1f3ead084ccfa048476540e9ea24b0e31127d0615a59ad58ab0dbd67`.
기존31문구의 editable authority는 `translations/gutsman_pet_talk_ko.json`, SHA `f742943f19f7feda1eea55531b76b8f2dd862fb7acb6f301edbb7031a86c373a` 그대로다. `tools/draft_gutsman_chipquest.py`가 prior31의 읽기 전용 projection+별도로 작성한2문구를 `translations/gutsman_pet_chipquest_ko.json`에 직렬화하며 빌드에서 parent hash/전체31units 일치를 검사한다. 변경은 신규2문구에서만 작성한다. 기본31scope는 유지하고 `gutsman-chipquest-v1` variant에33literal/25scripts를 명시했다.

`tools/gutsman_chipquest_model.py`는 source13 전체50bytes 및 original chip104 name9bytes를 고정하고 원문/번역/행 anchor·원본 이름88px/한국어47px와 결합 폭을 검사한다. 원본 이름으로 fallback해도 둘째행122px, 한국어일 때81px≤132px. 첫행81px/셋째행59px. Native 원문 이름 pool765190/2437bytes 및 다른 내비/칩 이름 전체 population을 번역한 것으로 세지 않는다. 전체33literal의 source/control/glyph/geometry/semantic·binary roundtrip,230미선택 spans source-identical PASS. 이전 후보와 비교해 변경된 script는13뿐이고 다른254script spans 동일. 기존31literal bytes/표현 불변.

## 이름 선택과 이전 경로 보존

기존 롤 exact stream/context/native-name guard를 유지하고 새 거츠맨 compiled13의 보호된 printChip anchor를 파생하여 별도 stream guard를 추가했다. 거츠맨 stream0880A428. 두 경우만 기존 `library.chip.batch04.104` 초안 `빅해머1`의 같은14bytes/E5 terminator/128bytes E5 패딩 ROM block을 선택한다. 다른 stream/context/name은 원본 처리한다.

Single composed writer install5162C/12bytes, expected source `40182f1c64373a88d2013049`, native continuation08051638. 기존6instruction 효과를 재구성하며 r3/높은 register/LR/SP 보존. 기존 ARM7TDMI ARMv4T Thumb-1/Keystone0.9.2/Capstone5.0.7 final placement assemble/disassemble roundtrip gate 사용. Original source name roots를 한국어 clone으로 전역 변경하지 않았다. ABI·native128copy·RAM residency·font/VRAM/screen의 실제 소비는 아래 실행 검증으로 별도 판단한다.

Synthetic Unicorn2.1.4 CPU64vectors: Roll/Guts selected,wrong stream/context/name 각각buffer0/1/7/255·CPSR0/F0000000. 원본 명령과 모든register/SP/LR/CPSR 비교 PASS, Korean source r0만 selected에 변경. `analysis/gutsman_chipquest_v1/selector_bench.json`. 이는 전체 게임caller/타이밍/음성/실기 증거가 아니다.

## 실행 상태와 선행 관측

선행 후보 `exe45_ko_development_gutsman_pet_talk_v1`/SHA75c2355...의 자체 select-gutsman parent에서 read-only script0 offset13 alias로 original Guts13을 관측했다. `poc/runtime/gutsman-chipquest-baseline-v1-script13`: native command0880A41D,원본 source087656A2→02010AC0 copy128, RAM `4b593d243a298202e5`,8one-byte name glyph/88px, 실제 거츠맨 초상. Source「」/printChip/keyWait 보존. 다른 ROM state를 새 후보에 가져오지 않는다.

새 후보 `tools/run_gutsman_chipquest.py`의 자체 freshFF저장/cold이어하기/거츠맨 intro·PET 정상16구간, 정상R, 격리 Guts13/종료·native R재진입, 자체 정상 롤 선택/격리 Roll13 검증 완료. `tools/report_gutsman_chipquest.py` PASS; `analysis/gutsman_chipquest_v1/runtime.json` 및 메인 직접 확인 화면 `chip_pages.png`, `pet_regression/normal_pet_prompts.png`.

Guts13 step2/3 각각19glyph/2,652 font→OBJ VRAM→screen pixels,빈영역2,947pixels clearing PASS. 롤13 step2/3 각각13glyph/1,776pixels,빈영역3,823pixels PASS. 두 caller의 실제 entry→continuation15register/SP/LR·정확한 stream/context/native-name guard·native128byte copy→RAM·E5 terminator·한글3glyph+원본숫자1·폭47px·row geometry·CPU glyph읽기·본문/화살표 분리·오른쪽border·종료 PASS. Guts 이름 결합행81px,Roll69px. 각각 자기 거츠맨/롤 초상·pool 유지. 정상 Guts R10은24glyph/3,324pixels와 A후PET1복귀 PASS; 진단 one-shot alias 소비 후 step6의 native R10재진입도 PASS. 모든 진단 checkpoint는 격리하고 정상 chain에 재사용하지 않는다. 진단으로 실제 chip quest/아이템 획득/진행 flag를 증명하지 않는다.

자체 정상 넘버맨 저장success58/새64KiB save SHA `c0c219a4e14084a232fc4046e686ae44221b1073a683e9e693f084843207e8aa`,checkpoint 없는cold이어하기3페이지·거츠맨인사2페이지/PET8장면22literal·29focus/No수락/B취소 PASS. 기존56archive payloads 및66A844의다른254scripts·prior31문구/hash·그래픽15라벨5블록 actualROM bytes 불변, ‘통신’ 수정 유지. Native 이름pool2437bytes·공유root9쌍 source-identical. 임의이름/모든caller/Yes후실제통신/한글이름 저장 검증으로 확대하지 않는다.

## 기술 검사·이중 집계 오류

최초 롤 경로의13회 A 한계에서 `Roll native idle not reached` FAIL. 실제 롤 선택/첫인사는 정상이고 final은 롤의 필수 숫자 운세 설명script20/65FF3C이었다. 이전 검증된 cold Roll recipe는 selection12A+intro8A=20A 뒤 PET1에 도달한다. 이번 initial1A+advance13A=14A는 아직 소개가 끝나지 않았다. 잘못된 캐릭터/텍스트/hook을 원인으로 보지 않고 모든14정상segment를 보존했다. `--resume-roll-selection`은 동일ROM·부모chain·normal checkpoint를 검사하고 이 경로에서 남은 A 진행을 이어간다. 미래 fresh run의 관측 한계를25회로 확장하고 목적 PET1/root 도달 시 즉시 멈춘다. Save/flag/ROM/state write나 이전ROM checkpoint 사용 없음. 후속 결과는 아래에 기록한다.

첫 Guts chip ABI 검사 FAIL: completed-page RAM FA84=1을 entry live-in buffer index로 간주해 r2=128을 예상했다. 기록된 entry→continuation의 r2는0이며 원본 baseline도0, native copy128의source/destination/remaining도 정확히일치한다. 원본 printChip buffer0/chip104 command가 native buffer index0을 설정하고 출력 이후1로 증가하므로 마지막 snapshot은 ABI 시점의 상태가 아니다. ROM/캡처를 그대로 유지하고 보호된 f9006801 invocation bytes를 검사한 뒤 원본6instruction의 buffer0 contract(r2=0)을 비교하도록 바로잡았다. 다른register15개/LR/SP·name source는 예상과 이미 일치했다. 최초 FAIL을 통과로 바꾸지 않고 별도 기록하며 동일 캡처의 수정된 strict 검사 결과를 아래에 남긴다.

현재 관련35tests(거츠맨32/이름selector3) PASS,617Python tools AST PASS. 기존 PET 회귀 helper 기본 동작도 이전 exact ROM/captures를 새 `backward_pet_helper` 출력에 읽기 재검증하여 PASS. 신규 changed_archives는66A844/13만 허용하고 다른254spans 불변·prior31→33 범위를 검사한다.

롤 정상 경로는 initial1A+advance16A=17A에서 PET1/root65FA58에 도달했다. 앞선20A cold recipe는 다른 경로의 선행 증거일 뿐 이번 입력 횟수로 세지 않는다. `roll_selection_chain.json`의17segments 모두 동일ROM/정상부모·무개입 검증 PASS. 최초13회 제한 실패 자료와 후속14..16을 보존했다.

최종 aggregate 최초 `prior selected asset drift` FAIL은 동일parent의 Windows경로 `translations\\gutsman_pet_talk_ko.json`와 manifest dependency의 `/` 표기 비교 차이였다. 실제 파일 SHA와31units는 일치했다. `Path` 경로 동등 비교와 기존 SHA 동등 조건을 함께 사용하여 엄격 검사 유지; 동일ROM/캡처 재검사 PASS. ROM/번역/hash를 바꾸거나 prior asset 검사를 생략하지 않았다.

최초 inventory는 manifest의 읽기 전용 parent dependency31units를 두 번째 selected writer로 오인하여 `duplicate selected unit` FAIL. ROM/번역을 바꾸지 않고 명시 inherited31 role/path/hash/단일child writer/전체31units 일치 검증 후 dependency는 input hash로 남기되 selected literal로 중복 계산하지 않도록 수정했다. 임의 중복 unit을 허용하거나 텍스트 일치로 dedup하지 않는다. 정상/불량role/count/child 부재 fixtures 테스트 PASS. 재실행 catalogue732/31,907literal/parse errors0;selected2280==manifest2280 PASS.

Immutable original 빌드 main/repro/final current_repro_r3 동일 SHA,617Python tools drift=[]/원본 SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 보존 PASS. 최종 tool 수정 후 current_repro_r3를 다시 빌드하고 감사 `analysis/gutsman_chipquest_v1/final_identity_audit.json` PASS 확인. Manual ROM writes/기존patchedROM input 없음. 이전 후보·실패·캡처·saves 보존.

## 남은 조건

Latest inventory `analysis/full_scope_gutsman_chipquest_v1/`: selected2,280/미선택 일본어 포함27,768/기타1,859. Catalogue732/31,907은 전체ROM 번역 분모가 아니다.
한글 이름 편집→committed record→모든 재표시→영구 재로드→기존save 호환이 가장 어려운 미해결 조건이다. 일정 알림66651C의18미선택literal/동적event·nickname/별도mugshot/실제 시간 알림, 전체graphics/inline/fixed population, prior native wait-arrow53pixel 차이, 인간 문구 검토도 남는다. 전체 번역/전체 게임caller/실기/배포 완료 선언 없음.
