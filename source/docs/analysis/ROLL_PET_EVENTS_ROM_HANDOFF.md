# 롤 PET 인터넷 지역 사건 안내 — 초안6문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review,release_eligible=false. 전체 완역/배포 승인 아님.
한글패치 스킬의 원본·제어 보존 및 정상·진단 증거 분리 원칙을 적용했다.

## ROM과 범위

`poc/output/exe45_ko_development_roll_pet_events_v1.gba`.
SHA256 `c2a6806e64e5cd39e5e0bdf1fa7b44d054b81364ddedec27ab475c5ab5c388d2`.
누적1,027선택 텍스트 단위/기존9그래픽 유지,전체 게임 완료율 아님.
15선택/717미선택 아카이브 보존. 원본/이전 ROM·상태·실패·조사 자료 보존.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
게임 실행 코드/훅 변경 없음. 진단 읽기 alias는 제품 ROM 미포함.

664E28 원본2158바이트/255슬롯/31리터럴,catalog pointer0x3810C,
archive SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
선택10/11/12/14/15/16/17/18/19/20/21/22/23/24/25/30/31/34,20리터럴.
기존14단위 source/translation/state 정확히 유지. 다른237슬롯 바이트 동일.
11리터럴 미번역,동적 칩13·닉네임33·요일 분기 보호.
새 풀2891바이트/root0x08804214,
SHA256 `8aa7952fb191733c737397cbd114ac492b171833fbddf32b4aa54a226494ee30`.
asset `translations/roll_pet_events_ko.json`,scope_variant `license-incident-keyquest-tournament-events-prompts`.

일본어6화면을 개별 검토하고 각 문구를 수동 작성했다.

- 16: 인터넷3에서 / 일어난 사건、 / 신경 쓰이네・・・ (71/79/101px)
- 18: 인터넷5에서 / 일어난 사건、 / 신경 쓰이네・・・ (71/79/101px)
- 19: 인터넷7에서 / 일어난 사건、 / 신경 쓰이네・・・ (71/79/101px)
- 20: 인터넷9에서 / 일어난 사건、 / 신경 쓰이네・・・ (71/79/101px)
- 21: 인터넷10에서 / 일어난 사건、 / 신경 쓰이네・・・ (82/79/101px)
- 22: 인터넷12에서 / 일어난 사건、 / 신경 쓰이네・・・ (82/79/101px)

지역 번호 각각 보존,사건에 대한 관심·걱정을 해결 명령/범인 단정/완료 선언으로 바꾸지 않았다.
기존 개발 용어 인터넷 재사용. 인간 문구·말투 승인 미완료.
원본3행/창·화살표 좌표/keyWait→clearMsg→waitHold 및 전체 제어 골격 보존.
신규최대101px,선택전체 최대124px≤채택132px/3행.
원본/의미/바이너리 roundtrip,미선택 보존 및 폰트·폭 검사 통과.

## 진단의 전제와 한계

원문은 직전 토너먼트 ROM own Roll intro에서
`poc/runtime/roll-pet-events-source-v1-script16/18/19/20/21/22`로 관측했다.
번역은 새 ROM own cold-chain에서 새 intro 정상 부모를 생성한다. 교차ROM 상태 사용 없음.
이6개는 기존 직접 창 생성과 달리 앞에 checkFlag가 있으므로 별도
`capture_roll_pet_events.py`가 원본과 출력의 플래그 명령/창 접두사를 먼저 검사한다.
플래그16→9424,18→9425,19→9426,20→9427,21→9428,22→9429;
각 true→33,false→continue. bytes EE00 + little-endian flag +21FF 유지.
진단에서 플래그/요일/명령을 수정하거나 checkFlag를 건너뛰지 않는다.
정상R 입력 `none:1:7,r:2:180,none:1:180`.
PC0x0804FB76/r0풀/r1=0/r5=0x0200FA20/원래offset510 조건일 때
script0 테이블 읽기 결과1회만 해당 원본 entry offset으로 치환. ROM/RAM 쓰기 없음.
원본 caller/initializer 코드 가드,별도 entry observer 및 기존 font observer 해시 기록·검사.
관측된 부모 상태에서 지역 안내가 표시됐다. 정상 진행으로 해당 entry가 선택되거나
플래그true→메일33 분기를 탔다는 증거가 아니다. 해당 진행·획득 조건은 미검증.
진단 checkpoint는 diagnostic_checkpoint.mss로 격리하고 정상 부모로 재사용하지 않는다.

## 검증 상태

독립 `_repro`/최종 도구 `_current_repro` 본 ROM과 바이트 동일.
원본/3빌드/349 Python 도구 해시 검사 통과,드리프트 없음.
새 ROM 집중21보고서 통과: 정상4(기본 탐색 안내/인사/PET/롤 장비·공격력),진단17
(11/12/14/15/17/23/24/25/30/31/34 및 신규16/18/19/20/21/22).
모두 새 ROM 해시에 귀속,과거 전체행렬/전체게임 테스트를 전용하지 않는다.
신규6개는 각2·3단계 CPU 폰트 읽기→OBJ VRAM→화면 픽셀,행·advance,
keyWait 경계와 빈 본문 잔상 검사를 통과했다. 6화면 직접 검토,잘림 없음.
원본/출력의checkFlag 접두사와 observer 해시 검사도 통과,진행 플래그 수정 없음.
17진단 checkpoint 정상 부모 사용 불가. 실제 사건 진행·완료/메일 분기·정상 entry선택은 미검증.
다른 아카이브 payload와 PET그래픽 블록 동일성 및 정상 닉네임/쉼표 검증 유지.
`analysis/roll_pet_events_v1/cumulative_runtime.json`,개별diagnostic_runtime.json 참조.
화면: `analysis/roll_pet_events_v1/events_diagnostic_pages.png`.

관련 자동 테스트27개 통과(38.644초,OK,exit0).
범위: test_roll_pet_events,test_roll_pet_tournament,test_roll_pet_keyquest,
test_roll_pet_incident,test_roll_pet_license,test_roll_pet_talk,test_tpl_literals,test_archive_scripts.
기존14단위/제어/플래그/미선택 보존 및 신규6표시·진단격리 회귀 포함.
기록: `analysis/roll_pet_events_v1/test_summary.txt`,`final_identity_audit.json`.

## 재현과 다음 작업

빌드: `tools/build_roll_pet.py` 누적 옵션
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-events`.
신규work/out(.gba) 필요.런타임: `python -X utf8 tools/run_roll_pet_events.py` (출력 폴더 신규 필요).
보고: `python -X utf8 tools/report_roll_pet_events.py`.
남은664E28의11리터럴: 칩13의2개,대회26/28의각2개,우라인터넷27의2개,
주말대회29,예선32,닉네임 메일33. 변수/요일/목표 내비 문맥을 확인한 뒤 번역.
다른 미번역,정상 진행·사용자 입력·저장·전체 게임·하드웨어·오디오·배포 QA 미완료.
