# 롤 PET 예선·새 메일 안내 — 초안2문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review,release_eligible=false. 전체 완역/배포 승인이 아니다.
한글패치 스킬에 따라 원본·제어 보존과 정상·진단 증거를 분리한다.
닉네임 재표시는 별도 검사하며 한글 이름 입력·저장 지원 완료를 주장하지 않는다.

## ROM과 번역 범위

`poc/output/exe45_ko_development_roll_pet_mail_v1.gba`.
SHA256 `6146c179e0d5660b4248f2816544d78d169d33e733346b164ced39769af23a5e`.
누적1,029선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율 아님.
15선택/717미선택 아카이브 보존,원본/이전 ROM·상태·증거 유지.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
게임 코드·훅 수정 없음. 진단 alias는 제품 ROM 미포함.

664E28 원본2158바이트/255슬롯/31리터럴,pointer0x3810C,
archive SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
선택10/11/12/14/15/16/17/18/19/20/21/22/23/24/25/30/31/32/33/34,22리터럴.
기존20단위 정확히 유지,다른235슬롯 바이트 동일.9리터럴 미번역.
새 풀2959바이트/root0x08804214,
SHA256 `0dfb61a46d0f03f25751a2579182de29f6269d5656019f27d688e6de1ec756da`.
asset `translations/roll_pet_mail_ko.json`,scope_variant `license-incident-keyquest-tournament-events-mail-prompts`.

원문32/33의2화면을 직접 확인하고 수동 작성했다.

- 32:0 ‘오피셜 / 토너먼트 예선에 / 참가하러 가자!’ (36/92/91px)
- 33:0 ‘、 / 아까 온 메일을 / 읽어 보자!’ (11/88/67px,첫 줄 앞에 네이티브 닉네임)

예선 참가와 최근 도착한 메일을 읽자는 목적 유지,메일 내용/발신자/예선 완료를 추가하지 않았다.
기존 개발 용어 오피셜/토너먼트 재사용,인간 승인된 공식 용어라는 주장은 아니다.
source33 printPlayerNickname(F90C01)과 첫 줄 쉼표를 그대로 유지해 폭 증가·조사 의존 없음.
nickname_suffix_scripts=[10,33]를 빌드 검증에 등록한다.닉네임 수정/키보드·저장 변경 없음.
원본3행/창·화살표/대기·clearMsg·waitHold와 제어 골격 유지.
원본/의미/바이너리 roundtrip,폰트/폭/미선택 보존 검사 통과,선택 최대124px≤채택132px.

## 진단 전제와 한계

원문은 직전 사건 지역 ROM own Roll intro에서
`poc/runtime/roll-pet-mail-source-v1-script32/33` 생성,두 일본어화면 직접 관측.
번역은 새 ROM own cold-chain에서 새 intro 정상 부모를 생성,교차ROM 상태 사용 없음.
`capture_roll_pet_mail.py`는 원본/출력의 창·명령 접두사부터 검사한다.
32는 checkFlag9430 true→33/false→continue(EE00D62421FF),33은닉네임 명령 보존.
PC0x0804FB76/r0풀/r1=0/r5=0x0200FA20/원래offset510 조건에서
script0 table읽기 결과1회만 entry32/33의offset으로 치환,ROM/RAM/플래그/닉네임 쓰기 없음.
정상R 입력 `none:1:7,r:2:180,none:1:180`.
원본 caller/initializer 코드 가드 및 entry/font observer 해시 검사 유지.
진단 checkpoint는 diagnostic_checkpoint.mss로 격리,정상 부모 사용 불가.
닉네임은 실제 RAM의 바이트/종료자/네이티브 글꼴·advance·좌표를 검사하고
한국어 리터럴과 함께 OBJ VRAM→화면 픽셀 및 빈 본문 잔상 검사에 포함한다.
이는 관측된 닉네임 재표시·문구 표시 증거이지 이름 입력/전체 이름/저장·재로드 지원 증거가 아니다.
예선 정상 참가,새 메일 실제 수신/열람,플래그true→33 및 정상entry 선택은 미검증.

## 검증 상태

독립 `_repro`/최종 도구 `_current_repro`는 본 ROM과 바이트 동일.
원본·3빌드·353 Python 도구 해시 검사 통과,드리프트 없음.
집중23보고서 통과: 정상4(기본 탐색 안내/인사/PET/롤 장비·공격력),진단19
(기존17 및 신규32/33).모두 새 ROM 해시에 귀속,과거 전체행렬 증거 전용 없음.
신규32/33 각2·3단계의CPU 폰트 읽기→OBJ VRAM→화면 픽셀/행·advance/대기/잔상 검사 통과.
33의 실제 RAM닉네임은 ああくん,4개 네이티브 글자/종료E5/44px 폭,
그 뒤 원본 쉼표11px.네이티브 글꼴/폭/좌표와 리터럴한글 픽셀이 함께 일치한다.
33의 빈 본문3040픽셀 배경 복원,겹침·잔상 없음.새2화면 직접 검토,잘림 없음.
19진단 checkpoint 정상 부모 사용 불가.진행/메일 수신·열람/이름 입력·저장 미검증.
다른 아카이브 payload와 PET그래픽 블록 동일,정상 기본 대화 닉네임도 유지.
화면: `analysis/roll_pet_mail_v1/mail_diagnostic_pages.png`.
기록: `analysis/roll_pet_mail_v1/cumulative_runtime.json`,개별diagnostic_runtime.json,
`final_identity_audit.json`.
관련 자동 테스트29개 통과(189.492초,OK,exit0).
범위: test_roll_pet_mail,test_roll_pet_events,test_roll_pet_tournament,test_roll_pet_keyquest,
test_roll_pet_incident,test_roll_pet_license,test_roll_pet_talk,test_tpl_literals,test_archive_scripts.
기존20단위/제어/닉네임 첫 줄 보존,첫 줄 변경 거부,새2표시와 닉네임 픽셀·격리 회귀 포함.
기록: `analysis/roll_pet_mail_v1/test_summary.txt`.전체 게임 테스트 완료라는 주장은 아니다.

## 재현과 다음 작업

빌드: `tools/build_roll_pet.py` 누적 옵션
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-mail`.
신규work/out(.gba) 필요.런타임: `python -X utf8 tools/run_roll_pet_mail.py` (출력 폴더 신규 필요).
보고: `python -X utf8 tools/report_roll_pet_mail.py`.
664E28 남은9리터럴: 칩13의2개,대회26/28각2개,우라인터넷27의2개,주말대회29.
변수/요일/목표 내비 문맥 확인 필요.다른 미번역 및 정상 진행·사용자 입력·저장·
전체 게임·하드웨어·오디오·배포 QA 미완료.
