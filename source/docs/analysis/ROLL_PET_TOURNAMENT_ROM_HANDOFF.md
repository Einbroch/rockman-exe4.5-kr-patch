# 롤 PET 오피셜 토너먼트 안내 — 초안3문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 완역 또는 배포 승인이 아니다.
한글패치 스킬에 따라 원문/제어 보존 및 정상·진단 증거 분리를 적용했다.

## 현재 ROM과 번역

`poc/output/exe45_ko_development_roll_pet_tournament_v1.gba`.
SHA256 `57bb69a6d2ca1d2888eb57a808e76bb10d5444459e0ace787f23d312a54a8d1d`.
누적1,021선택 텍스트 단위와 기존9그래픽. 전체 게임 완료율이 아니다.
15선택/717미선택 아카이브 보존. 원본/이전 ROM·상태·증거 보존.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
게임 실행 코드/훅 변경 없음. 진단 alias는 제품 ROM에 포함하지 않는다.

664E28 원본2158바이트/255슬롯/31리터럴, catalog pointer0x3810C.
원본 archive SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
선택10/11/12/14/15/17/23/24/25/30/31/34,14리터럴. 기존11단위 정확히 유지.
다른243슬롯 바이트 동일,17리터럴 미번역. 요일/플래그 분기와 동적 칩13·닉네임33 보호.
새 풀2657바이트/root0x08804214,
SHA256 `7b426fa84d11ae53ad0ccd7416f3a7804e44683535e875989d4b747aadcf3434`.
asset `translations/roll_pet_tournament_ko.json`, scope_variant `license-incident-keyquest-tournament-prompts`.

원문30/34의3페이지를 직접 확인하고 원문 순서로 수동 작성했다.

- 30:0 ‘오피셜 토너먼트 / 왠지 불타오르네!’ (92/103px)
- 34:0 ‘주가 바뀌면、 / 오피셜 / 토너먼트에’ (79/36/60px)
- 34:1 ‘참가 신청하러 가자!’ (123px)

주가 바뀐 뒤라는 시점과 참가 신청 목적 유지. 원문의 토너먼트 열의를 문자 그대로의
화재 상황으로 해석하지 않았다. 오피셜은 개발 제안 음역이며 공식 한글명 승인 주장 없음.
원본 행 수/페이지 수/창·화살표 좌표/keyWait·clearMsg·waitHold 보존.
34 첫 페이지가 ‘토너먼트에’로 끝나는 원본 구조도 유지한다.
selected 전체 최대124px≤채택132px/3행, 원문/의미/바이너리 roundtrip·폰트·미선택 보존 통과.

## 진단 방법과 한계

원문: 직전 키 퀘스트 ROM own Roll intro 정상 부모에서
`poc/runtime/roll-pet-tournament-source-v1-script30/34` 생성, 일본어3페이지 직접 관찰.
번역: 새 ROM own cold-chain과 intro를 새로 생성하며 다른 ROM 상태를 부모로 사용하지 않는다.
`capture_roll_pet_license.py` 변경 없이 `capture_roll_pet_tournament.py`가30/34만 허용한다.
정상R 입력 `none:1:7,r:2:180,none:1:180`,34만 A입력·대기2단계 추가.
PC0x0804FB76/r0풀/r1=0/r5=0x0200FA20/원래offset510 조건에서
script0 테이블 읽기 결과1회 해당 entry로 치환. 관측자 ROM/RAM 쓰기 없음.
원본 caller/initializer/창 접두사 가드와 observer/wrapper 해시 보존·검사.
진단 checkpoint는 별도 diagnostic_checkpoint.mss로 격리, 정상 부모 사용 불가.
달력이나 진행 플래그를 바꾸지 않는다. 이는 표시·페이지 전환 증거이며
정상 요일별 선택/토너먼트 참가·경기·예선/다음 주 진행 증거가 아니다.

## 검증 상태

독립 `_repro`/최종 도구 `_current_repro2` 빌드는 본 ROM과 바이트 동일.
검사기 수정 전 `_current_repro`도 보존하며 동일 제품 해시다.
원본·3빌드·345 Python 도구 해시 검사 통과, 드리프트 없음.
집중15보고서 통과: 정상4(기본 탐색 대화/인사/PET/롤 장비·공격력),진단11
(11/12/14/15/17/23/24/25/30/31/34). 모두 새 ROM 해시에 귀속한다.
신규30은2·3단계,34는2/4/5단계에서 CPU 폰트 읽기/OBJ VRAM/화면 픽셀,
행·advance·keyWait 경계와 빈 본문 잔상을 검증했다.
34 첫 페이지 빈3460픽셀,둘째 페이지4084픽셀 모두 배경으로 정리되어 잔상 없음.
`analysis/roll_pet_tournament_v1/tournament_diagnostic_pages.png`의3화면 직접 검토,잘림 없음.
진단11checkpoint 모두 정상 부모 사용 불가. 실제 요일·대회 진입은 미검증.
관련25자동 테스트 통과(30.232초,OK,exit0): test_roll_pet_tournament,
test_roll_pet_keyquest,test_roll_pet_incident,test_roll_pet_license,test_roll_pet_talk,
test_tpl_literals,test_archive_scripts. 전체 게임 테스트나 과거 전체15행렬 증거를 전용하지 않는다.
기록: `analysis/roll_pet_tournament_v1/cumulative_runtime.json`,개별diagnostic_runtime.json,
`test_summary.txt`,`final_identity_audit.json`.

### 검사기 대기 경계 오류: 재현·원인·수정

첫 보고 실행에서34:0의 대기 경계 검사가 실패했다. 화면은 정상이며 ROM/RAM 쓰기 없음.
기존검사식 max(stream)+1은 glyph시작좌표가 마지막 바이트라는 가정을 포함했다.
34:0 마지막 ‘에’는 stream0x08804C44에서 F9FCD019의4바이트이므로
기대경계0x08804C45가 아니라 실제RAMcursor와 동일한0x08804C48이다.
이후바이트는 원본 keyWait e600f1.30의ASCII마지막은 기존+1로 정상이다.
ROM/캡처를 고정한 채 literal_end가 마지막 문자 인코딩 길이와 실제 ROM바이트를
검증한 뒤 전체폭을 더하도록 수정했다.34는+4/30은+1인 회귀 테스트 추가.
동일캡처로 전15보고서 통과,과거PET/라이선스/사건/키퀘스트 테스트도 통과.
제품 ROM 수정 없이 관측검사 오류만 해결.초기 해시검사 기록은
`pre_checker_fix_identity_audit.json`로 보존하고 수정된 도구의 독립 재빌드2를 최종감사에 사용.

## 다음 작업과 재현

빌드: `tools/build_roll_pet.py` 누적 옵션
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-tournament`.
신규work/out(.gba) 필요.
런타임: `python -X utf8 tools/run_roll_pet_tournament.py` (모든 출력 폴더 신규 필요).
보고: `python -X utf8 tools/report_roll_pet_tournament.py`.
17리터럴 등 미번역, 정상 진행·사용자 입력·저장·전체 게임·하드웨어·오디오·배포 QA 미완료.
다음 후보: 사건 지역16/18/19/20/21/22(플래그 분기),대회26/28/29/32(요일/닉네임),
메일33(닉네임),우라인터넷27(목표 내비 문맥),칩13(변수 출력).각 전제·분기·변수 조건을 먼저 확인.
