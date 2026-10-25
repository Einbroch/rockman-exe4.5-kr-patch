# 롤 PET 사건 후 대화·추가 탐색 권유 — 초안3문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬에 따라 원본/제어 보존, 페이지 전환 검사 및 진단·정상 플레이 증거 분리를 적용한다.

## ROM과 번역 범위

`poc/output/exe45_ko_development_roll_pet_incident_v1.gba`.
SHA256 `6a2d3efb2d7cb14680f95d44fbf87a5a1a8cd50a0618d5adbbf6d2c7f2da2cb1`.
누적1,015선택 텍스트 단위/기존9그래픽 유지. 게임 전체 완료율이 아니다.
15선택/717미선택 아카이브 보존. 원본과 모든 이전 ROM/상태/조사 자료 보존.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
새 게임 실행 코드/훅 변경 없음. 진단용 선택은 ROM에 포함하지 않는다.

원본664E28:2158바이트/255슬롯/31리터럴, catalog pointer0x3810C,
SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
새 선택10/11/12/14/15/17/31의8리터럴. 기존5단위 source/translation/state 정확히 유지.
다른248슬롯(빈 슬롯 포함) 원본 바이트 동일.23리터럴 미번역 유지, 칩 변수13도 보호.
새 풀2443바이트/root0x08804214,
SHA256 `0a11e9bac92bc5b73ac3b96ea56c9342a08169bc3b5d25f09adc180dea11d026`.
asset `translations/roll_pet_incident_ko.json`, scope_variant `license-incident-prompts`.

원문17의2페이지와31의1페이지를 직접 확인하고 원문 순서로3문구를 수동 작성했다.

- 17:0 ‘방금 쓰러뜨린 내비가 / 사건의 범인이었던 / 것 같아・・・’ (124/104/77px)
- 17:1 ‘피곤하지、 / 잠깐 플러그아웃 / 하지 않을래?’ (59/92/79px)
- 31:0 ‘더 많이、 / 인터넷을 / 탐색해 보자!’ (55/48/79px)

`みたいね`의 추측을 ‘것 같아’로 유지했다. 범인임을 확정하거나 특정 내비를 추가하지 않았다.
기존 내비/플러그아웃/인터넷 개발 용어를 재사용하며 인간 승인된 공식 표현이라고 주장하지 않는다.
원본 행 수,17의keyWait→clearMsg→다음 페이지와 최종waitHold, 창/화살표 좌표 및 진행 분기 명령 보존.
132px/3행 채택 범위 내. 원본/의미/바이너리 roundtrip·미선택 보존·폰트/폭 검사 통과.

## 진단 방법과 한계

직전 라이선스 ROM own Roll intro에서 정상 R 입력의 네이티브script0/호출 문맥을 사용한다.
기존 `capture_roll_pet_license.py` 구현은 변경하지 않고17/31만 허용하는
`capture_roll_pet_incident.py` wrapper에서 보호된 테이블 읽기 결과를 해당 entry로 바꾼다.
base observer 및 wrapper 해시를 모두 기록한다. 원본 caller/initializer/창 설정 접두사 가드 유지.
alias는PC0x0804FB76/r0풀/r1=0/r5=0x0200FA20/원래offset510일 때1회만 허용한다.
관측자 ROM/RAM 쓰기 없음. 모든 진단 checkpoint를 별도 이름으로 격리하고 정상 부모로 재사용하지 않는다.
원문 실행: `poc/runtime/roll-pet-incident-source-v1-script17/31`.
17은정상 R 입력 후 첫 페이지 대기, A1회 후 둘째 페이지 대기만 실행한다(총5단계).
31은같은R 입력+대기3단계. 실제 범인 격파/사건 진행/종료 분기 선택을 검증한 것이 아니다.

## 재현 및 검증

독립 `_repro` 및 최종 도구 `_current_repro`는 본 ROM과 바이트 동일.
새 ROM own cold-chain/PET 메뉴/장비/기존 탐색 안내 정상 경로와
라이선스4개 회귀 및 신규17/31 진단 경로를 분리해 집중 검증한다.
다른 아카이브 payload 및 PET 그래픽 블록 동일성도 검사한다.
직전전체15회귀/181전체테스트를 이번 ROM 증거로 전용하지 않는다.
집중 검증10개 통과: 정상4보고서(탐색 안내/인사/PET/롤 장비·공격력)와
진단6보고서(기존11/12/14/15 및 신규17/31). 모두 이번 ROM 해시와 일치한다.
신규17은2단계 첫 페이지,4단계 둘째 페이지,5단계 안정 대기를 검사했다.
31은2·3단계의 한 페이지를 검사했다. CPU 폰트 읽기·행/advance·OBJ VRAM·화면 픽셀 검사 통과.
빈 본문 픽셀 검사17:0은1900개,17:1은2800개로 페이지 전환 후 잔상 없음.
각 원본 keyWait 경계에서 정확히 정지하고 다음 페이지/최종clearMsg/waitHold 바이트 보존.
6진단 receipt 모두 normal_play_checkpoint_eligible=false, 정상 checkpoint로 재사용 안 함.
실제 사건 진행/전투 승리/범인 선택/종료 분기를 확인한 것은 아니다.
다른 아카이브 payload와 PET 그래픽 블록 동일. 정상 탐색 안내 닉네임/쉼표 검증도 유지.
`analysis/roll_pet_incident_v1/incident_diagnostic_pages.png`의 새3페이지를 직접 검토했다.

관련 자동 테스트21개 통과(18.415초, OK, exit0).
범위: test_roll_pet_incident, test_roll_pet_license, test_roll_pet_talk,
test_tpl_literals, test_archive_scripts. 새 원문/기존5단위/제어/미선택 보존과
두 페이지 렌더링·진단 격리, 기존 PET/라이선스 도구 회귀를 확인했다.
전체185테스트를 이번 ROM에서 실행했다고 주장하지 않는다.
기록: `analysis/roll_pet_incident_v1/test_summary.txt`, `cumulative_runtime.json` 및 각 진단 보고서.
최종 원본/3개 빌드/337 Python 도구 해시 검사 통과, 도구 드리프트 없음.
기록: `analysis/roll_pet_incident_v1/final_identity_audit.json`.

## 재실행과 남은 작업

빌드: `tools/build_roll_pet.py` 누적 옵션에 `--roll-pet-incident`, 신규work/out 사용.
런타임: `python -X utf8 tools/run_roll_pet_incident.py` (모든 출력 폴더 신규 필요).
보고: `python -X utf8 tools/report_roll_pet_incident.py`.
나머지23리터럴 등 미번역, 정상 사건/라이선스 진행, 사용자 입력/저장, 전체 게임·하드웨어·오디오·배포 QA 미완료.
