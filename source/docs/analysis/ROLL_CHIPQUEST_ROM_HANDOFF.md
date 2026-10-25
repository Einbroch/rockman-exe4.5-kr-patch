# 롤 칩 찾기 대사 — 초안1단위 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review,release_eligible=false. 전체 완역·배포 승인 아님.
한글패치 스킬의동적삽입/소비자 경계 기준에따라대사와칩이름을분리검증했다.
동등한기존23분기진단을반복하는대신,원본명령·기존문구바이트동일성 및
새ROM 공통소비자 정상회귀와변경페이지진단을연결하고미검증범위를명시했다.

## 산출물과 범위

`poc/output/exe45_ko_development_roll_chipquest_v1.gba`.
SHA256 `aff27be5b0bb114a6b08f9db9337f38c427c43ae5e719457a93eda35e7449eb9`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
누적1,051선택 텍스트 단위/기존9그래픽 유지. 전체게임 완료율이 아니다.
16선택/716미선택 아카이브,원본·이전 ROM·상태·실패 자료보존.
게임 기계코드/훅 추가수정없음,제품ROM에진단alias없음.

664E28 원본2158바이트/255슬롯/31리터럴/pointer0x3810C,
SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
asset `translations/roll_pet_chipquest_ko.json`,직전weekday29단위 그대로복사하고
13:1만수동작성. 선택25스크립트/30리터럴,다른230슬롯원본바이트동일.
남은13:0은원본여는따옴표「이며미선택그대로보호.삽입칩이름은별도765190 소스이다.
새풀3129바이트/root0x08804820,
compiled SHA256 `5b51be4801ad4ef217e9f942afe06827f1e0d460272f01b6d5b78734e7834ef6`.
직전mail-alert-v1과비교하여13제외254PET 스크립트span 바이트동일,
다른15개 번역payload/PET그래픽블록 동일.재배치offsettable 변화와span본문을구분했다.

## 원문·번역·삽입 모델

13은원본「→printChip buffer0/chip104→‘」 を\nさがしに行こう!’→keyWait/clearMsg/waitHold.
원문한페이지를 `roll-chipquest-source-v1-script13` step002/003에서직접확인했다.
이는직전ROM own 정상roll-intro 부모의PET0 테이블읽기1회만13으로alias한진단이다.
ROM/RAM/칩소유/진행플래그/닉네임/날짜 쓰기없으며정상퀘스트entry 도달증거가아니다.

별도765190 이름아카이브2437바이트/256슬롯의script104 원문은‘ビッグハンマー1’.
보호바이트 `4b593d243a298202e5`와실제RAM0x02010AC0..C8(E5 포함)이동일.
8네이티브글자,각11px/총88px. native RAM glyph 실행과폰트읽기/화면을연결했다.
이름ROM의정확한각CPU읽기주소/복사함수 전체를추적한증거는아니며,
변경하지않은source printChip0/104와RAM/글꼴소비의일치증거이다.

13:1 수동초안 `」\n찾으러 가자!`.
칩명/닫는따옴표뒤줄바꿈,둘째행으로찾기제안을표시하여조사 의존성을피했다.
칩 이름의일본어는의도적으로수정하지않았고미번역으로명시한다.
기존fixed-cell 라이브러리의‘빅해머1’ 번역이있어도이정상대화 RAM삽입소비자에는자동적용되지않는다.
통합이름한글화는이별도소비자의복사/버퍼/인코딩/글꼴경계를검증한후진행해야한다.
줄바꿈만대사리터럴안에서재배치,전체명령골격·인수·따옴표·원본닉네임가드·대기/지우기유지.
원본/의미/바이너리 roundtrip,미선택리터럴·슬롯,모든선택폰트/폭검사통과.

빌드에 `roll_chipquest_model.py`와등록profile `roll-chip104-native-name-v1` 추가.
고정원본이름바이트,원본창/「/F9006801 명령과닫는따옴표,2행구조를확인.
따옴표11+이름88+닫는따옴표11=첫줄110px,한글둘째행79px≤채택132px.
검증layout에삽입폭과 native_name_localization_pending=true 기록.
이름/명령/두행경계/폭모델에맞지않는입력은빌드차단한다.

## 새 ROM 검증

`run_roll_chipquest.py`는새ROM own cold-chain과정상인사/PET/장비,
normal R 기본대사,weekday date/profile/navi-menu/select-roll/intro를재생한다.
새메일도착은같은ROM weekday-select-roll에서초기알림보다앞의경계부터재생.
이후own 정상roll-intro에서13진단실행.과거/진단checkpoint를정상부모로재사용하지않음.
읽기전용glyph/font/RAM observer와별도alias1회guard/원본caller코드해시검증.
진단checkpoint는diagnostic_checkpoint.mss로격리,normal_play_checkpoint_eligible=false.

집중6보고서: 정상5(기본탐색대사/인사/PET/롤장비·공격력/메일도착),칩13진단1.
weekday5정상구간은부모/입력/receipt 검증으로별도기록,보고서수중복가산없음.
13진단nativecaller frame8/LR0x08037F27/native script0,display alias13.
step002/003의실제RAM8글자와원본「,번역닫는따옴표/본문17글자:
CPU폰트읽기→ROM폰트→OBJ VRAM→화면2268픽셀일치.
각글자offset/행/advance/닫는따옴표396바이트offset/keyWait 경계검증.
빈본문3292픽셀배경일치,잔상/잘림/번역잉크겹침없음.화면직접검토.
step004/005 확인키뒤풀변경과PET ‘뭘 할까?’복귀 관측.
정상메일알림·native닉네임·초기!!·확인뒤전환도새ROM에서재검증.
이전23분기진단은이번ROM에재캡처하지않았고과거통과수를현재보고서수에합산하지않음.
원래퀘스트조건/칩보유·획득/분기선택/전체분기를실제플레이로완주한증거가아니다.

기록 `analysis/roll_chipquest_v1/focused_runtime.json`,
`chipquest_diagnostic_runtime.json`,`mail_arrival_runtime.json`,기존정상consumer 보고서.
화면 `poc/runtime/roll-chipquest-v1-script13/step_003.png`.
기존37자동회귀 통과163.963초,신규3통과0.587초(합계40고유테스트).
기존37은과거고정ROM/캡처 회귀자료 검사이며새ROM 전체게임실행증거가아니다.
신규3:기존29단위/30단위분모/보호제어·230슬롯,삽입두행가드거부,
RAM이름/폰트/픽셀/진단격리.정적2사전실행은중복가산안함.
기록 `prior_test_summary.txt`,`new_test_summary.txt`.

## 보고서 오류와 최종 재현

초기보고서에서정상4개검사는통과했으나기존license helper에빈SCRIPTS를전달하여
폭0 contact sheet 저장중Pillow ‘cannot write empty image’/exit1 발생.
ROM/런타임결함이아님.새report wrapper가네정상보고서를직접호출하게만수정.
`report_failure_v1.txt`와부분license_diagnostic_pages.png/캡처보존,가드/픽셀기준완화없음.
수정후보고서6개통과.모든캡처observer와ROM/번역데이터는수정하지않음.
최종tool로새 `_current_repro2` 생성,본체/`_repro`/`_current_repro2` 동일SHA.
이전 `_current_repro`도보존,내용동일하지만최종보고서수정전tool metadata이므로최종감사는repro2사용.
370 Python 도구 해시 드리프트없음: `final_identity_audit.json`.

빌드 `tools/build_roll_pet.py` 옵션:
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-chipquest --roll-mail-alert`.
work/out(.gba)는항상새경로.런타임 `tools/run_roll_chipquest.py`,보고 `tools/report_roll_chipquest.py`.
다음핵심미번역:대화printChip의원본일본어삽입칩이름(라이브러리와다른consumer).
그밖의미번역·다른메일13정상분기·입력/저장/RTC지속·하드웨어·실제오디오·전체게임·배포QA 미완료.
