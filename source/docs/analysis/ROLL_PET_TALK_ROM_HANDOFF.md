# 롤 PET 인터넷 탐색 안내 — 1문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역 또는 배포 승인이 아니다.

## 개발 ROM과 범위

권장 후보: `poc/output/exe45_ko_development_roll_pet_talk_v2.gba`.
SHA256 `35d871005b0a50b9f8398d5b3dda95e0ee413728b31eac6b8bfb8504c3e4b7a1`.
누적1,008선택 텍스트 단위, 기존9그래픽 유지. 게임 전체 완료율이 아니다.
15선택 아카이브/717미선택 아카이브 보존. 기존 번역 입력 해시 동일.
원본과 모든 이전 ROM/상태/조사 기록 보존. 새 게임 실행 코드/훅 변경 없음.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.

원본664E28는2158바이트/255스크립트 슬롯/31리터럴, catalog pointer0x3810C.
원본 풀 SHA256 `b788cd856ad90150aa1ba360d3a97294138ba98d24cfd8af33b1631271853dee`.
선택은10:0의1리터럴만. 다른254슬롯(빈 슬롯 포함) 바이트 동일,30리터럴 미번역 유지.
새 풀2179바이트/root0x08804214,
SHA256 `180ef74ebd669438ad0ab4e6737c05cc3f50b407f1bc3ad8b7cdf7b3522e9ae1`.

번역: `、 / 인터넷을 더 / 탐색해 보자!`.
원문 `、 / もっとインターネットを / たんさくしてみよう!`를 직접 확인했다.
초기 화면 판독의 토너먼트 추정은 원문과 달라 채택하지 않았다.
네이티브 닉네임 뒤 쉼표/두 줄바꿈은 원본 그대로, 본문68/79px(132px/3행 제한 이내).
분기 플래그/아이템/날짜/토너먼트 검사와 keyWait/clearMsg/waitHold 보존.
원본/바이너리/의미 roundtrip, 폰트 공급, 미선택 바이트 보존 통과.

## 정상 경로 조사

직전 과목 ROM의 own Roll intro 상태에서 `none:1:7,r:2:180,none:1:180`.
`poc/runtime/roll-pet-talk-source-v1`는 읽기 전용 신규 아카이브 observer 사용.
네이티브 호출script0/frame8/LR0x08037F27, 원본 root0x08664E28.
script0의 보호된 jump10 이후 RAM 활성script10과 원문 화면을 확인했다.
ROM/RAM/스크립트 번호 강제 변경 없이 정상 R 버튼 입력만 사용했다.
R 버튼의 PET 대화 조작 참고: Nintendo 일본어 매뉴얼
<https://www.nintendo.co.jp/data/software/manual/manual_pc5j_00.pdf>.
인터넷 안내의 실제 선택 근거는 매뉴얼이 아닌 원문 TPL/네이티브 관측이다.

취미13/장래희망15 조사에서는 정상 진입을 확인하지 못했다.
`analysis/roll_preferences_survey/roll-preferences-survey-v1.json`의6타이밍은
3/3/29/11/7/1 기존 주제만 선택했다. PET 장시간 대기도 새 주제를 입증하지 못했다.
이 조사 결과를 전체 주제 도달 가능성 증명으로 확대하지 않는다.

## 재현 및 검증 상태

독립 `_repro`와 최종 도구 `_current_repro2`는 권장 ROM 바이트와 동일.
`analysis/roll_pet_talk_v1/final_identity_audit.json`:329 Python 도구 해시 드리프트 없음.
첫 v1 빌드 도중 asset evidence 표기 수정이 발생하여 그 영수증은 현재 asset와 불일치한다.
v1 파일은 삭제/덮어쓰기하지 않고 보존, 검증 후보는 수정 이후 새로 빌드한 v2만 사용한다.
새 ROM own cold-chain 및 기존 회귀, PET 대화 화면 검증15개 모두 통과.
`analysis/roll_pet_talk_v1/cumulative_runtime.json`은 전 보고서 동일 ROM 해시를 확인한다.
인사/PET/운세/플러그아웃/귀환/장비/폴더/무기/공격력·숫자/통신 그래픽,
형제자매4질문의 예/아니요 분기, 음식/과목 질문 화면 회귀를 포함한다.
귀환 패배 문구는 진단 실행만 포함하며 실제 패배 플레이가 아니다.

신규 경로는 `poc/runtime/roll-pet-talk-v1-talk`, 부모는 같은 v2 ROM own Roll intro.
네이티브 호출script0/frame8/LR0x08037F27/root0x08804214 후 보호된 jump10.
2·3단계에서 닉네임을 포함18글리프/2424픽셀씩 폰트→OBJ VRAM→화면 검사 통과.
본문 CPU 폰트 읽기, 정확한 행/advance 및 원본 닉네임 폰트·advance 보존 확인.
원본 닉네임 RAM `ああくん`은 사용자의 입력 데이터이며 미번역 대사가 아니다.
닉네임44px+원문 쉼표11px, 한국어 본문68/79px. 최종 screenshot `step_003.png` 직접 검토.
질문 대기 cursor0x08804500, 원본의 `e600f1edff`(keyWait/clearMsg/waitHold) 정확히 보존.
초기 검증 코드가 waitHold를 다른 바이트로 예상해 검사 실패했다.
preflight 실행 자료는 `poc/runtime/roll-pet-talk-preflight-v1-talk`에 보존하고 수정 이력은 이 문서에 기록한다.
ROM 문제가 아닌 검증 예상값 문제였고 원본 TPL/실제 바이트에 맞춰 수정 후 재검사 통과.
`_current_repro`는 그 수정 전 도구 스냅샷이므로 최종 도구 증거로 사용하지 않는다.
전체 자동 테스트181개 통과(591.758초, OK, exit0).
기록: `analysis/roll_pet_talk_v1/test_summary.txt`.
신규2테스트는 원문/범위/닉네임 접미사 변조 차단/이전 asset 유지 및
정상 PET 대화·15개 동일 ROM 보고서 검증을 포함한다.
빌드 도구는 최종 재빌드 이후 변경하지 않았다.

## 재실행

빌드: `tools/build_roll_pet.py`에 `--roll-intro --roll-fortune-complete --roll-jackin
--roll-return --roll-plugout --roll-subjects --roll-pet-talk`와 신규 `--work`/`--out` 지정.
런타임: `python -X utf8 tools/run_roll_pet_talk.py` (모든 output 디렉터리는 신규여야 함).
보고: `python -X utf8 tools/report_roll_pet_talk.py`.
테스트: `python -X utf8 -m unittest discover -s tools -p 'test*.py' --buffer`.

진행 분기11..34는 미번역/정상 경로 미검증. 닉네임 직접 입력/저장 미검증.
진단용 패배는 실제 패배 플레이 검증이 아니다. 하드웨어/오디오/전체 게임/배포 QA 미완료.
