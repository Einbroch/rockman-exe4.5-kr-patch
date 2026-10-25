# 롤 PET 마이너스 키 안내 — 초안3문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 완역 또는 배포 승인이 아니다.
한글패치 스킬의 원본/제어 보존과 정상·진단 증거 분리 원칙을 적용했다.

## 현재 ROM과 범위

`poc/output/exe45_ko_development_roll_pet_keyquest_v1.gba`.
SHA256 `780366ecee25a884e89b7f2ffae5ca208ab163ebb07e703ef9e6a547d0733aa4`.
누적1,018선택 텍스트 단위와 기존9그래픽. 전체 게임 완료율이 아니다.
15선택 아카이브/717미선택 아카이브 보존. 원본 및 이전 ROM·상태·증거 보존.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
새 게임 실행 코드/훅 변경 없음. 진단 alias는 제품 ROM에 포함하지 않는다.

664E28 원본2158바이트/255슬롯/31리터럴, pointer0x3810C.
원본 archive SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
선택10/11/12/14/15/17/23/24/25/31,11리터럴. 기존8단위 정확히 유지.
미선택245슬롯 바이트 동일,20리터럴 미번역. 동적 칩 출력13도 보호.
새 풀2568바이트/root0x08804214,
SHA256 `624b37cbe56b4fd01dd951f32fddbab24c4dafd2413ecdbaab7337b71af4c152`.
asset `translations/roll_pet_keyquest_ko.json`, scope_variant `license-incident-keyquest-prompts`.

원본 진단 화면23/24/25를 직접 검토한 후3문구를 수동 작성했다.

- 23: ‘블랙 워크스에게서 / 「마이너스 키」를 / 되찾자!’ (104/102/47px)
- 24: ‘「마이너스 키」는、 / 다른 내비가 가진 / 것 같아!!’ (113/100/66px)
- 25: ‘「마이너스 키」를 / 들고 인터넷9의 / 내비에게 가자!’ (102/91/91px)

24의추측,25의아이템 소지와인터넷9 목적지 유지. 블랙 워크스/마이너스 키는
제안 음역이며 승인된 공식 용어라는 주장이 아니다. 인간 문구/말투 승인 미완료.
원본3행/창·화살표 좌표/대기·clearMsg·waitHold 명령 유지.
원본/의미/바이너리 roundtrip,폰트/폭/미선택 보존 검사 통과,전체선택 최대124px≤132px.

## 진단과 재현

원문 장면은 직전 사건 ROM의 own Roll intro 정상 부모로부터
`poc/runtime/roll-pet-keyquest-source-v1-script23/24/25`에서 관측했다.
번역 장면은 새 ROM own cold-chain에서 정상 intro 부모를 새로 생성한다.
`capture_roll_pet_license.py` 기존 가드는 수정하지 않고 새 wrapper가23/24/25만 허용한다.
정상R 입력3단계 `none:1:7,r:2:180,none:1:180`.
PC0x0804FB76/r0풀/r1=0/r5=0x0200FA20/원래offset510 조건으로
script0 테이블 읽기 결과만1회 해당 entry로 치환한다. ROM/RAM 쓰기 없음.
원본 caller/initializer/창 접두사 가드 및 observer/wrapper 해시 검사.
진단 checkpoint는 diagnostic_checkpoint.mss로 격리하며 정상 부모로 재사용하지 않는다.
이는 문구 소비·표시 증거만이며 키 획득/사건 진행/인터넷9 이동/정상 분기 선택 증거가 아니다.

빌드3개 독립 실행 결과 동일. 최초 --out에 확장자를 빠뜨려 extensionless 산출물이 생성됐고,
런타임 시작은 .gba 파일 부재로 실패했다(에뮬레이터 시작 전 FileNotFoundError).
산출물과 메타데이터를 보존한 채 검증된 동일 바이트를 신규 .gba 경로로 복사 후 재시작했다.
extensionless 원본도 유지. 재빌드 명령은 .gba 확장자를 명시한다.
실패를 제품 렌더링 결함이나 정상 런타임 통과로 취급하지 않는다.

## 검증 상태

정적 검사/원본·3빌드·341 Python 도구 해시 검사 통과, 도구 드리프트 없음.
집중 검증13보고서 통과: 정상4(기본 탐색 대화/인사/PET/롤 장비·공격력)와
진단9(11/12/14/15/17/23/24/25/31). 모두 새 ROM 해시와 일치한다.
새23/24/25는 각각2·3단계 폰트 CPU 읽기→OBJ VRAM→화면 픽셀,
행/advance/대기 경계/빈 본문 잔상 검사 통과. 새3화면 직접 검토, 글자 잘림 없음.
정상기본 탐색 닉네임/쉼표 및 기존 그래픽 보존 검증도 통과.
9진단 checkpoint 모두 정상 부모 사용 불가. 실제 키 회수/퀘스트 분기 선택은 미검증.
`analysis/roll_pet_keyquest_v1/cumulative_runtime.json` 및 개별 diagnostic_runtime.json 참조.
화면: `analysis/roll_pet_keyquest_v1/keyquest_diagnostic_pages.png`.

관련 자동 테스트23개 통과(23.901초,OK,exit0).
test_roll_pet_keyquest/test_roll_pet_incident/test_roll_pet_license/test_roll_pet_talk/
test_tpl_literals/test_archive_scripts. 기존8단위/제어/미선택 보존, 진단 격리와 회귀 포함.
전체 게임 테스트 또는 직전15전체 회귀를 이번 ROM에서 수행했다는 주장은 아니다.
`analysis/roll_pet_keyquest_v1/test_summary.txt`, `final_identity_audit.json` 참조.

## 다음 작업

빌드: `tools/build_roll_pet.py`에 누적 옵션
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout --roll-subjects --roll-pet-keyquest`.
신규work와 `.gba` 확장자의 신규out 필요.
런타임: `python -X utf8 tools/run_roll_pet_keyquest.py` (출력 폴더 신규 필요).
보고: `python -X utf8 tools/report_roll_pet_keyquest.py`.
20리터럴 등 미번역, 정상 퀘스트 진행·사용자 입력·저장·전체 게임·하드웨어·오디오·배포 QA 미완료.
