# 롤 메일 도착 알림 — 초안14단위 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review,release_eligible=false. 전체 완역·배포 승인 아님.
한글패치 스킬에 따라 전체 원문 구조를 먼저 확인하고,제어·닉네임 보존과
정상/진단/미검증 증거를 구분했다. 자동 규칙으로 문장 번역하지 않았다.

## ROM과 범위

`poc/output/exe45_ko_development_roll_mail_alert_v1.gba`.
SHA256 `c21f96e1298edca233ed6a88e3f37f51dfaa6a022699743f6e73fc566b0aa564`.
누적1,050선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
16선택/716미선택 아카이브. 원본·과거 ROM·캡처·상태·실패 증거는 보존.
직전 weekday-v1의15개 compiled payload와 PET 그래픽 블록 모두 동일.
게임 기계코드/훅 추가 수정 없음. 제품 ROM에 진단 alias 추가 없음.

새 archive661060은 원본0x661060/1351바이트,255슬롯/28리터럴,
pointer0x380EC 하나,비압축/size-header 없음.
source archive SHA256 `0fb238422445f63e91dce70531a04c3cc7f992791a63dee9ae3420ebd2e80d08`.
선택스크립트1,2,3,4,5,6,7,20,21,22,23,24,25,26 각각literal1만 선택(14단위).
각각literal0의초기 `!!` 14개는 변경하지 않음. 다른241슬롯 바이트 동일.
새 풀1547바이트/root0x08802AB0,
compiled SHA256 `b1ec6d506b27847340082ee62e0a4e8a9e3560c0e64d921dbfffb7cc984d4b23`.
asset `translations/roll_mail_alert_ko.json`,registry `tools/specs/exe45_dialogue_archives_v1.json`.

14본문 모두 수동 초안 ‘메일이 왔어!!’. 닉네임이 있는1/2/3은
`、\n메일이 왔어!!`,나머지는 한 줄.본체90px,닉네임뒤쉼표11px,
채택폭132px/최대3행 이내. 문구의친근한 반말/도착 알림 의미 유지.
nickname_suffix_scripts=[1,2,3],nickname_suffix_literal=1 등록,
첫줄쉼표와 printPlayerNickname 원본 명령 유지,조사 의존·폭 증가 없음.

## 원문과 명령 보존

`analysis/tpl_baseline/661060.tpl` 전체를 읽고28리터럴 분모와 명령 흐름을 확인.
원문 정상 관측은 직전 weekday-v1의같은ROM weekday-select-roll 부모에서
`poc/runtime/roll-mail-alert-source-v1-arrival`로재생. 10단계 캡처/receipt/부모 체인 검증 통과.
step005/006 초기 `!!`,step007/008 일본어 본문,step009/010 PET 대화 복귀 직접 확인.
정상 entry1/frame609/LR0x08037F27,원문root0x08661060.
capture 도구는 읽기 전용이며 ROM/RAM/진행플래그/닉네임/날짜 주입 없음.

전체 skeleton,미선택 리터럴/스크립트,semantic/binary roundtrip,원본 폰트/폭 검증 통과.
flagSet3585,창/대화속도/머그샷,초기 `!!`,soundPlay155→wait96→soundPlay155→wait96,
clearMsg,닉네임,본문,keyWait,clearMsg,waitHold 모두 원본 명령 순서/값 보존.
2의clearFlag680/callTournamentReceiveMail,3의clearFlag681,
4..7의clearFlag623..626,20..26의flagAddMail8912..8918도 보존.
새보고서가script1의본문 앞 전체바이트 접두사도원문과직접대조.
이 보존은 해당 이벤트의실제 취득/발송/플래그 효과를 플레이로완주했다는뜻이아니다.

## 새 ROM 런타임

`tools/run_roll_mail_alert.py`가새ROM 자체의cold-chain과weekday 날짜입력 UI부터재생.
이전 ROM checkpoint를 새 ROM 검증에 재사용하지 않음. weekday-select-roll은
메일 풀/본문 읽기보다 앞의same-ROM 정상부모이다.
추가 arrival는none60,A180 세번,A60,wait90/120/90,A180,wait180;
전10단계 캡처. 읽기 전용 `capture_roll_mail_alert.py`와
공통 폰트/native RAM nickname probe 해시 확인.

새 arrival의정상call entry1/frame609/LR0x08037F27/root0x08802AB0.
step005/006 초기원본 `!!`,step007/008 ‘ああくん、 / 메일이 왔어!!’ 정상표시.
실제RAM닉네임4네이티브글자/E5/44px,뒤쉼표11px,본문90px.
CPU 글꼴읽기와 폰트인덱스/stride96/행·advance,
ROM폰트→OBJ VRAM→화면픽셀,본문 keyWait 경계 검증 통과.
초기알림 빈본문5296픽셀,최종본문3820픽셀 배경일치,잔상/잘림/번역잉크겹침없음.
누적 draw로그의초기 `!!`는 clearMsg이후현재본문 차지영역에서 제외해검사.
step009/010 확인키뒤풀변경과‘뭘 할까?’ PET 화면 복귀 관측.
한글 이름 입력/영구저장/모든 닉네임 지원이라는 증거는 아니다.

집중28보고서 통과: 정상5(기존4+새메일 도착1),진단23(기존PET 분기).
weekday 정상5구간의부모/입력/캡처 receipt는 별도검증이며보고서수에중복가산없음.
진단23은 테이블읽기 alias를 사용한 글꼴/소비 진단이며,제품ROM에alias없음;
격리된 diagnostic_checkpoint는 정상플레이부모사용불가.
과거 full runtime matrix 결과를새ROM의모든컨슈머증거로전용하지 않음.
기록 `analysis/roll_mail_alert_v1/cumulative_runtime.json`,
`mail_arrival_runtime.json`,`weekday_route.json`,기존소비자/개별diagnostic_runtime.json.
대표정상화면 `poc/runtime/roll-mail-alert-v1-arrival/step_008.png`.

## 재현·테스트·남은 범위

원본에서독립 본체/`_repro`/`_current_repro` 빌드가동일해시.
365 Python 도구 해시 드리프트없음: `analysis/roll_mail_alert_v1/final_identity_audit.json`.
기존34자동회귀 통과(240.273초),신규3통과(0.977초),합계37개고유테스트.
기존34는과거고정ROM/캡처의회귀자료 검사이며새ROM의전체게임실행증거가아니다.
신규3은14단위/미선택241슬롯/제어/닉네임가드/첫줄변경거부/정상도착픽셀검증.
기록 `prior_test_summary.txt`,`new_test_summary.txt`;정적2개별도사전실행은중복가산안함.

빌드 `tools/build_roll_pet.py` 옵션:
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-weekday --roll-mail-alert`.
work/out(.gba)는항상새경로. 런타임 `tools/run_roll_mail_alert.py`,보고 `tools/report_roll_mail_alert.py`.
새14중script1:1만정상evententry검증.나머지13단위는원문명령/폰트/폭 정적검증,
개별native분기 런타임 pending이며 `runtime_open_units`에명시.
오디오비활성 캡처이므로실제소리는미검증;명령보존만입증.
기존날짜UI와작은PET헤더의숫자일관성/RTC 지속성미확정은해결했다고주장하지않음.
다음후보는664E28 script13의2리터럴(동적printChip 문맥/삽입값/폰트·폭확인필요)
및다른미번역아카이브. 전체 진행·저장·입력·하드웨어·오디오·배포 QA 미완료.
