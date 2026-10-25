# 롤 PET 평일 대회 안내 — 초안5문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review,release_eligible=false. 전체 완역·배포 승인 아님.
한글패치 스킬에 따라 원본·요일/닉네임 제어 보존과 정상·진단 증거를 분리한다.

## ROM과 번역 범위

`poc/output/exe45_ko_development_roll_pet_weekday_v1.gba`.
SHA256 `bdd871b59d679c636fc1faa75bc1ae4ca9caffbb087cbdef8336052714f16868`.
누적1,036선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율 아님.
15선택/717미선택 아카이브 보존,원본/이전 ROM·상태·실패 증거 유지.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
게임 코드·훅 추가 수정 없음. 진단 alias는 제품 ROM 미포함.

664E28 원본2158바이트/255슬롯/31리터럴,pointer0x3810C,
archive SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
선택10..34중13제외24개스크립트,29리터럴.기존24단위 정확히 유지,
다른231슬롯 바이트 동일.남은2리터럴은 동적 칩13이며 원문 보존.
새 풀3118바이트/root0x08804214,
SHA256 `415bfb1f7c34f2d15a416a2eac8029b536b9f77b48080804193426e7745108e6`.
asset `translations/roll_pet_weekday_ko.json`,scope_variant
`license-incident-keyquest-tournament-events-mail-undernet-weekday-prompts`.

원문26/28/29의5페이지를 직접 확인하고 수동 작성했다.

- 26:0 ‘오피셜 / 토너먼트의’ (36/60px)
- 26:1 ‘참가 신청 장소에 / 가 보자!’ (100/55px)
- 28:0 ‘、 / 오피셜 / 토너먼트에’ (11/36/60px,첫 줄 앞 네이티브 닉네임)
- 28:1 ‘참가 신청하러 가자!’ (123px)
- 29:0 ‘주말엔 오피셜 / 토너먼트네! / 신나게 해 보자!!’ (80/71/110px)

참가 신청 장소,참가 제안,다가오는 주말 대회를 기대하는 의미 유지.
기존 오피셜/토너먼트/참가 신청 개발 용어 재사용,인간 승인된 공식 용어라는 주장은 아니다.
원본2·3·1행,창·화살표·keyWait·clearMsg·waitHold와 제어 골격 유지.
26/28의일요일0·토요일6→34,29의같은요일→30/그외continue 두 검사 모두 보존.
28 printPlayerNickname(F90C01)과 첫 줄 원본 쉼표 그대로,조사 의존·폭 증가 없음.
nickname_suffix_scripts=[10,28,33] 등록,닉네임/키보드·저장 변경 없음.
원본/의미/바이너리 roundtrip,폰트/폭/미선택 보존 검사 통과,선택 최대124px≤채택132px.

## 정상 날짜 입력과 진단 전제

원문은 직전 우라인터넷 ROM의 own cold-part1에서 정상 날짜 입력으로 관측.
`roll-pet-weekday-source-v1-date` step007은 날짜 입력 UI의2000/1/3(月)를 직접 보여준다.
입력은 A3회→위2회(각release)→A7회,원래 날짜 UI의일 선택에만 적용.
RTC/RAM/플래그/진행 주입 없음.이후 화면에서월요일 표시와 원래요일 검사를 거친
26/28/29의원문 소비를 관측.날짜 저장·재로드/RTC 시간 일관성 검증은 아니다.
작은PET헤더의날짜 숫자는 설정 UI와 일관성이 미확정이므로 날짜 지속 지원을 주장하지 않는다.

첫 원문 진단 `roll-pet-weekday-source-v1-script26/28/29`은 aliases0으로 실패.
주말 인사 입력9단계를 평일에 재사용하자intro9에서플러그인 대화가 남아
PET script0 caller에 진입하지 못함.source-v1-ready도다음대화이며
source-v2-script26/28/29 aliases0실패를보존.ready2에서인터넷 진입 화면을 관측.
관측된step2/4/6/8/9를비교하고 같은select-roll부모에서intro입력7단계만 새로재생.
`roll-pet-weekday-source-v3-intro` step007은PET 기본대화이며R입력시원래caller진입.
source-v3-script26/28/29 aliases1,5원문페이지 직접 확인.관찰기 가드를 완화하지 않았다.

번역 검증도새ROM own cold-chain에서초기상태를새로생성,교차ROM 상태 사용 금지.
`run_roll_pet_weekday.py`는기존주말회귀를재생한뒤같은ROM cold-part1에서평일분기를새로시작.
평일5정상구간 date/profile/navi-menu/select-roll/intro,마지막intro는7단계에서정지.
`capture_roll_pet_weekday.py`는원본/출력의요일 명령접두사와창·닉네임을검사.
PC0x0804FB76/r0풀/r1=0/r5=0x0200FA20/원래offset510조건에서
script0 table읽기결과1회만entry26/28/29 offset으로치환.요일검사는실제실행,건너뛰지않는다.
ROM/RAM/날짜/플래그/닉네임쓰기없음.caller/initializer코드및observer해시유지.
진단checkpoint는diagnostic_checkpoint.mss로격리,정상부모사용불가.
이는문구/페이지/요일continue소비진단이며정상대회진행·참가접수·자연스러운entry선택은미검증.

## 검증 상태

독립 `_repro`/최종 도구 `_current_repro`는 본 ROM과 바이트 동일.
원본·3빌드·361 Python 도구 해시 검사 통과,드리프트 없음.
기록: `analysis/roll_pet_weekday_v1/final_identity_audit.json`.
평일 정상5구간의same-ROM 부모/입력/캡처/artifact해시 검사 통과:
`analysis/roll_pet_weekday_v1/weekday_route.json`.날짜UI의월요일 설정을 직접 검토.
집중27보고서 통과: 정상4(기본 탐색 안내/인사/PET/롤 장비·공격력),진단23
(기존20 및 신규26/28/29).모두 새ROM해시에 귀속,과거 전체행렬 증거 전용 없음.
신규5페이지의CPU폰트읽기→OBJ VRAM→화면픽셀/행·advance/대기 지점 검사 통과.
26둘째페이지 빈본문3700픽셀,28둘째페이지4084픽셀 배경 복원,잔상 없음.
28첫페이지의실제RAM닉네임 ああくん(4네이티브글자/E5/44px)과쉼표11px 보존.
닉네임로그는누적이지만clearMsg이후페이지의차지영역으로취급하지 않는다.
다음페이지에서닉네임영역을포함한본문배경·새글꼴픽셀을검사해잔상·겹침없음.
한글 이름 입력/저장·모든 이름 지원 증거는 아니다.새5화면 직접 검토,잘림 없음.
23진단checkpoint 정상부모사용불가.정상대회참가·접수·진행조건/entry선택은미검증.
다른아카이브payload와PET그래픽블록동일,정상기본대화·메일닉네임도유지.
화면: `analysis/roll_pet_weekday_v1/weekday_diagnostic_pages.png`.
기록: `analysis/roll_pet_weekday_v1/cumulative_runtime.json`,개별diagnostic_runtime.json.
관련 자동 테스트34개 통과(215.204초,OK,exit0).
범위: test_roll_pet_weekday,test_roll_pet_undernet,test_roll_pet_mail,test_roll_pet_events,
test_roll_pet_tournament,test_roll_pet_keyquest,test_roll_pet_incident,test_roll_pet_license,
test_roll_pet_talk,test_tpl_literals,test_archive_scripts.기존24단위/요일·제어·닉네임 보존,
28첫줄변경거부fixture와5페이지·닉네임지우기 회귀 포함.
기록: `analysis/roll_pet_weekday_v1/test_summary.txt`.전체 게임 테스트 완료라는 주장은 아니다.

## 재현과 다음 작업

빌드: `tools/build_roll_pet.py` 누적 옵션
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-weekday`.
신규work/out(.gba) 필요.런타임: `python -X utf8 tools/run_roll_pet_weekday.py` (출력 폴더 신규 필요).
보고: `python -X utf8 tools/report_roll_pet_weekday.py`.
664E28 남은13의2리터럴은 printChip 삽입값·폭·폰트 소비를 연결한 뒤작업.
평일 초기 인사에서별도미번역661060 script1메일도착안내를관측:
source-v1-intro step006 RAM root0x08661060/script1,원문「メールがきたよ!!」.
해당아카이브의원문제어/음효과/닉네임문맥과다른단위의전체분모확인후다음번역대상.
다른 미번역 및 정상 진행·사용자 입력·저장·전체 게임·하드웨어·오디오·배포 QA 미완료.
