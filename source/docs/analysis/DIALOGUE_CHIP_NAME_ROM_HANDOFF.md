# 롤 대화 속 삽입 칩 이름 ‘빅해머1’ — 별도 소비자 연결

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review,release_eligible=false. 전체 완역·배포 승인 아님.
한글패치 스킬에따라저장/선택/복사/RAM/글꼴/화면 경계를연결하고,
공유이름표변경과제한된hook의영향을비교했다. 기존칩이름문구를재사용한다.

## ROM과 변경 범위

`poc/output/exe45_ko_development_dialogue_chip_name_v1.gba`.
SHA256 `7bfeb8d1642e77dd1fad4674898059dbf5682cf8c5e30d2fcde4675c0a636ba8`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
누적1,051선택텍스트단위/기존9그래픽 유지,전체게임 완료율이아니다.
재사용wording `library.chip.batch04.104`,sourceunit `765190:104:0`.
`translations/library_chip_names_batch08_ko.json`의 needs_review 초안‘빅해머1’을그대로사용.
새문장생성/기존문구변경없고한문구를다른consumer에연결한것이므로수중복가산없음.
기존16선택/716미선택아카이브,원본·이전 ROM/캡처/상태/실패자료보존.

직전chipquest-v1 ROM과공통범위전체를대조: 설치0x5162C..0x51637의12바이트만변경.
모든기존대사/포인터/글꼴/그래픽/나머지코드바이트동일. ROM끝196바이트추가.
공유9개 이름root pair와765190 원본2437바이트풀 그대로.
추가name block offset0xA8D3F8/128바이트,
body14바이트 `f9fc4512f9fc7429f9fc380e02e5`,나머지114바이트E5.
추가hook offset0xA8D478/68바이트(Thumb 코드44+literal24).
metadata `dialogue_chip_name`는name/header/hook/wording identity와모든machine-code record를기록.

## 원본 선택과 복사 경로

읽기전용 `capture_dialogue_chip_lookup.py`로직전ROM의own 정상roll-intro 부모에서
PET0→13 table alias1회진단: `poc/runtime/dialogue-chip-lookup-source-v1`.
frame9/PC0x08051626에서0x08051664 root pair의0x08765190 선택,
PC0x0805162A에서104*2 엔트리0x08765260의offset0x512 읽기,
PC0x0800094E의128바이트복사에서0x087656A2..AA의원문이름9바이트읽기확인.
소스r0=0x087656A2,destination r1=0x02010AC0,native memcpy LR0x08051643.
그후RAM 이름8글자/88px/원문‘ビッグハンマー1’ 소비 관측.
原복사루프는r2를감소하며128바이트전체복사,이름종료E5 이전만글꼴소비.

공유root 하나를clone으로바꾸면같은F9핸들러의다른대화에영향을넓히고,
전체원본이름풀/포인터정합성 정책과충돌한다.이번연결은원본lookup결과는보존하고,
복사직전소스주소r0만특정호출에서교체한다.
채택한 `dialogue_chip_name.py` 조건은세가지모두일치해야한다:
현재ROM Roll13 printChip stream0x08804BCE(r4),normal context0x0200FA20(r5),
원본chip104 name stream0x087656A2(r0+r1).그외원본소스주소 그대로.
stream은현재빌드664E28의script13 offset과보호prefix/F9006801에서계산하며고정상수복사아님.

설치의원본6명령 `40182f1c64373a88d2013049` 및nativebuffer literal0x02010AC0 기대값검사.
원본효과 adds r0,r0,r1; r7=r5+0x64;ldrh buffer index; r2=index<<7;r1=nativebuffer 재현.
임시8바이트stack return frame으로r3와native continuation0x08051639 보관,
pop{r3,pc}로원본SP/LR/high-register 보존. r0만조건일치때의도적으로바뀐다.
마지막원본arith/shift 효과로flags 재현. 원본복사함수/후속카운터/복귀는변경하지않음.
ARM7TDMI ARMv4T Thumb-1 profile,핀된Keystone0.9.2/Capstone5.0.7,
최종배치양방향어셈블/디스어셈블·literal/branch/모든instruction경계검증.
기존Expected Write 단일writer에설치12바이트등록,overlap/범위/원본/최종diff 검증통과.

## CPU와 실제 소비 증거

`bench_dialogue_chip_name.py`: 원본6명령과최종hook bytes를Unicorn2.1.4 TI925T에서대조.
선택/다른stream/다른context/다른name 네경우×buffer0/1/7/255×초기flags두종류=32벡터.
원본과r0..r14/SP/LR 동일(선택r0만clone),CPSR 동일.모든fallback 원본효과보존.
합성CPU검사이며GBA IRQ/오디오/실제타이밍/모든원본caller를플레이한증거가아니다.

새ROM own cold-chain/정상기본대사·인사·PET·장비·메일도착을재생.
`run_dialogue_chip_name.py`는기존source13진단wrapper 재생뒤추가selector observer를별도실행.
핵심캡처 `poc/runtime/dialogue-chip-name-v1-name-script13`은
같은ROM 정상roll-intro 부모에서자연PET0 call에table alias1회만적용.
ROM/RAM/플래그/닉네임/칩소유/날짜observer쓰기없음.진단checkpoint격리.
`capture_dialogue_chip_name.py`가native설치/continuation 레지스터및clone CPU읽기를관찰.

step002/003에서원본lookup결과/native104/command/context와실제continuation r0 clone 확인.
관측된모든레지스터/SP/LR는원본6명령계약과일치,관측buffer index0.
native memcpy가clone128주소를역순으로모두읽고RAM0x02010AC0..0x02010B3F에완전히일치.
RAM의F9FC3한글+native숫자1/E5,3*12+11=47px.
따옴표포함첫줄69px,둘째행79px≤채택132px.보수적인원본삽입모델110px도여전히유효.
원래문장asset의native-name-pending 메모는hook없는기존소비자에대한것이며,
이번구체적인consumer 연결상태는새dialogue_chip_name metadata/보고서가한정해갱신한다.
13글자(칩4+양따옴표2+본문7)/1776픽셀 CPU폰트읽기→ROM BDF폰트→OBJ VRAM→화면일치.
빈본문3784픽셀배경일치,잔상·잘림·번역잉크겹침없음. keyWait/확인뒤풀교체와PET복귀검증.
화면직접검토: `.../name-script13/step_003.png`.

별도7입력단계 `poc/runtime/dialogue-chip-name-v1-reentry` receipt/ROM/부모/artifact 확인.
첫alias1은유지하며frame734의두번째native0 call은alias되지않음.
step007 기본대사‘인터넷을 더 / 탐색해 보자!’와native nickname 정상표시를직접검토,
칩이름/따옴표 잔상없음.재진입은진단조상의한정된route이며정상퀘스트진행증거로승격하지않음.
이추가재진입화면은시각검토/receipt/호출검증이며,모든픽셀자동대조로주장하지않음.

집중6보고서통과: 정상5(기본탐색/인사/PET/롤장비·공격력/메일도착),이름renderer 진단1.
weekday 입력/메일의추가정상구간은새ROM own 부모에서시작,관련receipt 재귀검증.
이전23분기/전체runtime matrix를이번ROM에서완료했다고가산하지않음.
보고 `focused_runtime.json`,`name_runtime.json`,`selector_bench.json`,정상consumer보고서.
관련18자동테스트통과0.563초: test_tpl_literals/test_archive_scripts/test_dialogue_chip_name.
새3은source/stream/wording 거부,기계코드·128블록·무중복count,실행CPSR/fallback 비교.
별도첫3과사전18실행은중복가산없음.이전40전체회귀는이번턴에재실행하지않음.
기존guide verifier 수정의구버전경로는old_guide_checker_regression에서직전ROM으로통과.

## 보고서 수정·재현·미완료

초기보고서가장비guide검증에서‘hook exact final placement’로exit1.
기존checker가guide를ROM끝의마지막append로가정했는데새name블록/hook이뒤에추가되었기때문.
새declared successor를source/asset/현재배치로다시구성하여전체tail/metadata/설치stub를정확히비교하도록수정.
가드/픽셀기준을완화하지않음.기존실패보고/캡처는유지: `report_failure_v1.txt`.
ROM/wording/capture observer는수정하지않고최종tool로새 `_current_repro2` 생성.
본체/`_repro`/`_current_repro2` 동일해시,377 Python tool 드리프트없음.
이전 `_current_repro`도보존,수정전tool metadata이므로최종감사는repro2사용.
기록 `final_identity_audit.json`,`final_test_summary.txt`.

빌드 `tools/build_roll_pet.py` 옵션:
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-chipquest --roll-mail-alert --roll-dialogue-chip-name`.
항상새work/out(.gba).런타임 `tools/run_dialogue_chip_name.py`,보고 `tools/report_dialogue_chip_name.py`.
별도재진입은같은capture_dialogue_chip_name.py에입력
`none:1:7,r:2:180,none:1:180,a:2:180,none:1:180,r:2:180,none:1:180`와own roll-intro 부모.
정상칩획득/퀘스트 entry 도달·보유조건은미검증. 다른대화 printChip 이름은그대로일본어.
다른미번역/다른메일13분기/입력·저장·RTC 지속/실제오디오·하드웨어·전체게임·배포QA 미완료.
