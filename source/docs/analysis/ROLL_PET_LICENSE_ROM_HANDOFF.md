# 롤 PET 견습 라이선스 안내 — 개발 초안4문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬에 따라 원본 제어/미선택 바이트 보존과 진단·정상 플레이 증거 분리를 적용했다.

## ROM과 범위

`poc/output/exe45_ko_development_roll_pet_license_v1.gba`.
SHA256 `46dcd61b1e9939c24a2325f67c4bdee7e5e9a98e9aab42d712b2d792a1664263`.
누적1,012선택 텍스트 단위/기존9그래픽 유지. 게임 전체 완료율이 아니다.
15선택 아카이브/717미선택 아카이브 보존. 원본 및 이전 ROM/상태/조사 자료 보존.
새 게임 실행 코드/훅 변경 없음. 진단용 대사 선택은 ROM과 빌드 입력에 포함하지 않는다.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.

원본664E28:2158바이트/255스크립트 슬롯/31리터럴, pointer0x3810C.
원본 풀 SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
선택10/11/12/14/15의5리터럴 중10:0는 기존 source/translation/state 정확히 유지.
다른250슬롯(빈 슬롯 포함) 원본 바이트 동일.26리터럴은 미번역 유지.
특히 칩 이름 삽입13은 변수 소비·폭 검증이 필요하므로 이번 범위에서 제외했다.
새 풀2322바이트/root0x08804214,
SHA256 `5be6c85335f23192e18ffae64b7a0f2b31b86e5134d7db967ef564d8d5ca5442`.

asset `translations/roll_pet_license_ko.json`, 등록 scope_variant `license-prompts`.
기존 탐색 안내를 보존하고 다음4문구를 원문 순서로 직접 번역했다.

- 11: 견습 라이선스 시험 / 도전해 보지 않을래? (112/123px)
- 12: 견습 라이선스 시험 / 힘내 보자!! (112/78px)
- 14: 견습 라이선스를 / 받으러 가자! (92/79px)
- 15: 견습 라이선스 시험 / 고생했어! / 잠깐 쉴래? (112/59/67px)

원문의 권유/응원/수령/시험 후 위로를 구분했다. `견습 라이선스`는 개발 용어 후보이며
인간 승인된 공식 한국어 명칭이라고 주장하지 않는다. 자동 규칙으로 번역 문장을 수정하지 않았다.
원본 행 수, position92,110, keyWait/clearMsg/waitHold 및 모든 진행 분기 검사 보존.
132px/3행 채택 범위 내. 원본/바이너리/의미 roundtrip·글리프 공급·폭 검사 통과.

## 정상 진입과 진단 증거의 구분

직전35d871... ROM own Roll intro에서 네이티브 R 대화 호출script0와 소비 문맥을 사용한다.
원래0의 jump10 대신 스크립트 테이블 읽기 결과만11/12/14/15로 바꾸는 진단 observer를 작성했다.
원본 caller/initializer 범위37F0C..37F54,4F7B6..4F7D0,4FB4C..4FC20와
대상4스크립트의 동일 창 설정 접두사 `f6000a0c01e702f6025c6e03f604e18d`를 검증한다.
읽기 alias는 실행PC0x0804FB76/r0풀/r1=0/r5=0x0200FA20/원래offset510 조건에서 단1회만 허용한다.
관측자 ROM/RAM 쓰기 없음. 별도 진단 checkpoint는 `diagnostic_checkpoint.mss`로 격리하고
result의 normal_play_checkpoint_eligible=false. 정상 부모로 재사용하지 않는다.
source 실행: `poc/runtime/roll-pet-license-source-v1-script11/12/14/15`.
원문 화면4개를 직접 확인했다. 라이선스 획득/시험 완료/정상 진행 분기 선택 증거가 아니다.

## 새 ROM 검증

새 ROM own cold-chain/PET 메뉴·장비·기존 탐색 안내 정상 경로와
새4문구 진단 렌더러 경로를 분리한 집중 검증을 진행한다.
이번 변경은 새 아카이브나 훅이 아닌 같은 소비자의4리터럴 확장이다.
변경 아카이브와 공통 폰트 소비 경로 중심으로 회귀를 선택하며,
직전 ROM의15개 보고서를 새 ROM에서 모두 재실행했다고 주장하지 않는다.
기존 다른 아카이브 컴파일 payload와 PET 그래픽 블록 동일성을 별도로 검증한다.

독립 `_repro`와 최종 도구 `_current_repro`는 본 ROM 바이트와 동일.
`analysis/roll_pet_license_v1/final_identity_audit.json`:333 Python 도구 해시 드리프트 없음.
집중 검증8개 통과: 정상4보고서(탐색 안내/인사/PET 메뉴/롤 장비·공격력)와
진단4보고서(11/12/14/15). 모두 이번 ROM 해시와 일치하며 release_eligible=false.
신규4문구는2·3단계의 글리프/행·폭/CPU 폰트 읽기/OBJ VRAM/화면 픽셀 및 빈 영역 잔상 검사를 통과.
각 최종 대기 cursor는 해당 리터럴 뒤 `e600f1edff` 경계에서 정확히 정지한다.
진단4 receipt의 normal_play_checkpoint_eligible=false 및 정상 checkpoint 없음 검사 통과.
이것은 라이선스 진행 조건이나 정상 branch 선택/시험 완료/수령 검증이 아니다.
정상 탐색 안내의 닉네임과 쉼표는 새 ROM에서도 기존 바이트/advance 그대로 검증했다.
다른 선택 아카이브 payload와 기존 PET 그래픽 블록 해시 동일, 통신 표시 유지.
화면 모음 `analysis/roll_pet_license_v1/license_diagnostic_pages.png`를 직접 검토했다.

관련 자동 테스트19개 통과(13.986초, OK, exit0).
범위: `test_roll_pet_license`, `test_roll_pet_talk`, `test_tpl_literals`, `test_archive_scripts`.
원문/기존 단위/제어 보존, 닉네임 접미사 변조 차단, 미선택 스크립트 보존,
집중 런타임 증거와 진단 격리 및 기존 PET 도구 회귀를 확인한다.
기록: `analysis/roll_pet_license_v1/test_summary.txt`, `cumulative_runtime.json`, 각 진단 보고서.
이번 ROM에서 전체183테스트를 실행했다고 주장하지 않는다. 직전181개 전체 테스트는 직전 ROM 증거다.

## 재실행과 남은 작업

빌드: `tools/build_roll_pet.py`의 기존 누적 옵션에 `--roll-pet-license` 지정, 신규work/out 사용.
집중 런타임: `python -X utf8 tools/run_roll_pet_license.py --focused` (출력 폴더 신규 필요).
집중 보고: `python -X utf8 tools/report_roll_pet_license.py`.
진단 렌더러 증거와 정상 대화/메뉴 증거를 혼합해 진입 조건을 확정하지 않는다.
나머지26리터럴, 라이선스 진행/획득 정상 경로, 사용자 입력/저장, 전체 게임/하드웨어/오디오 QA 미완료.
