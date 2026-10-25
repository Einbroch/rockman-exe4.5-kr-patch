# 롤 PET 우라인터넷 안내 — 초안2문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review,release_eligible=false. 전체 완역·배포 승인 아님.
한글패치 스킬에 따라 원본·제어 보존과 정상·진단 증거를 분리한다.

## ROM과 번역 범위

`poc/output/exe45_ko_development_roll_pet_undernet_v1.gba`.
SHA256 `3812dae6e9c32830520e72de0c2a1ef98ac5e2994254cd5702af2ea2446524a9`.
누적1,031선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율 아님.
15선택/717미선택 아카이브 보존,원본/이전 ROM·상태·증거 유지.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
게임 코드·훅 추가 수정 없음. 진단 alias는 제품 ROM 미포함.

664E28 원본2158바이트/255슬롯/31리터럴,pointer0x3810C,
archive SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
선택10/11/12/14/15/16/17/18/19/20/21/22/23/24/25/27/30/31/32/33/34,24리터럴.
기존22단위 정확히 유지,다른234슬롯 바이트 동일.7리터럴 미번역.
새 풀3002바이트/root0x08804214,
SHA256 `7eceb50bf0893ab93b0b8ccace2f34549cdac7dfd8bc3637bb5de1c46d1d68f4`.
asset `translations/roll_pet_undernet_ko.json`,scope_variant
`license-incident-keyquest-tournament-events-mail-undernet-prompts`.

원문27의2페이지를 직접 확인하고 수동 작성했다.

- 27:0 ‘우라인터넷으로 / 가자!’ (84/35px)
- 27:1 ‘목표 내비의 / 표식은 / 관이었지!’ (68/36/59px)

이동 제안과 목표 내비의 관 표식 회상을 유지했다. 목표의 이름·소속·조우 결과를 추가하지 않았다.
우라인터넷/관은 개발 초안 용어이며 인간 승인된 공식 용어라는 주장은 아니다.
원본2행/3행,창·화살표·keyWait·clearMsg·waitHold와 제어 골격 유지.
기존nickname_suffix_scripts=[10,33] 보존,닉네임/키보드·저장 변경 없음.
원본/의미/바이너리 roundtrip,폰트/폭/미선택 보존 검사 통과,선택 최대124px≤채택132px.

## 진단 전제와 한계

원문은 직전 예선·메일 ROM의 own Roll intro에서
`poc/runtime/roll-pet-undernet-source-v1-script27` 생성,step003/005 일본어화면 직접 관측.
번역 검증은 새 ROM own cold-chain에서 정상 부모를 새로 생성한다. 교차ROM 상태 사용 금지.
`capture_roll_pet_undernet.py`는 원본/출력의 창 접두사
F6000A0C01E702F6025C6E03F604E18D와 원래 script0 EF000A를 검사한다.
PC0x0804FB76/r0풀/r1=0/r5=0x0200FA20/원래offset510 조건에서
script0 table읽기 결과1회만 entry27 offset으로 치환,ROM/RAM/플래그 쓰기 없음.
R/다음 페이지 입력 `none:1:7,r:2:180,none:1:180,a:2:180,none:1:180`.
원본 caller/initializer 코드 가드 및 entry/font observer·wrapper 해시 검사 유지.
진단 checkpoint는 diagnostic_checkpoint.mss로 격리,정상 부모 사용 불가.
이는 원래 소비자의 문구·페이지 표시 진단이지 우라인터넷 진입·목표 내비 조우·
진행 조건·자연스러운entry 선택의 증거가 아니다.

## 검증 상태

독립 `_repro`/최종 도구 `_current_repro`는 본 ROM과 바이트 동일.
원본·3빌드·357 Python 도구 해시 검사 통과,드리프트 없음.
기록: `analysis/roll_pet_undernet_v1/final_identity_audit.json`.
집중24보고서 통과: 정상4(기본 탐색 안내/인사/PET/롤 장비·공격력),진단20
(기존19 및 신규27).모두 새 ROM 해시에 귀속,과거 전체행렬 증거 전용 없음.
신규27의step2첫 페이지/step4·5둘째 페이지에서 CPU 폰트 읽기→OBJ VRAM→
화면 픽셀/행·advance/대기 지점 검사 통과.둘째 페이지의 빈 본문3604픽셀이 배경으로
복원돼 앞 페이지 잔상 없음.새2화면 직접 검토,잘림·겹침 없음.
20진단 checkpoint 정상 부모 사용 불가.목표 내비 조우/자연스러운 선택·진행은 미검증.
다른 아카이브 payload와 PET그래픽 블록 동일,정상 기본 대화·메일 닉네임도 유지.
화면: `analysis/roll_pet_undernet_v1/undernet_diagnostic_pages.png`.
기록: `analysis/roll_pet_undernet_v1/cumulative_runtime.json`,개별diagnostic_runtime.json.
관련 자동 테스트31개 통과(191.060초,OK,exit0).
범위: test_roll_pet_undernet,test_roll_pet_mail,test_roll_pet_events,test_roll_pet_tournament,
test_roll_pet_keyquest,test_roll_pet_incident,test_roll_pet_license,test_roll_pet_talk,
test_tpl_literals,test_archive_scripts.기존22단위/제어/닉네임 보존,새2페이지와 잔상·격리 회귀 포함.
기록: `analysis/roll_pet_undernet_v1/test_summary.txt`.전체 게임 테스트 완료라는 주장은 아니다.

## 재현과 다음 작업

빌드: `tools/build_roll_pet.py` 누적 옵션
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-undernet`.
신규work/out(.gba) 필요.런타임: `python -X utf8 tools/run_roll_pet_undernet.py` (출력 폴더 신규 필요).
보고: `python -X utf8 tools/report_roll_pet_undernet.py`.
664E28 남은7리터럴: 칩13의2개,대회26/28각2개,주말대회29.
26/28은 일요일0·토요일6이면34,29는 같은 요일이면30으로 이동한다.
현재 초기 날짜1/1토요일에서는 이들 원문 리터럴이 표시되지 않으므로
다음 작업은 정상 날짜 입력 UI로 평일을 설정하고 분기·닉네임 문맥을 관측하는 것.
동적 칩13은 printChip 값·폭·폰트 소비 검증이 필요하며 원문 유지.
다른 미번역 및 정상 진행·사용자 입력·저장·전체 게임·하드웨어·오디오·배포 QA 미완료.
