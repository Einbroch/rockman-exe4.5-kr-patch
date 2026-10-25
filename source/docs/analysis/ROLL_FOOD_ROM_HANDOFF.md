# 롤 귀환 후 좋아하는 음식 — 4문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬에 따라 원본/제어 보존, 동일 새 ROM 정상 경로와 독립 빌드를 적용한다.

## 개발 ROM

`poc/output/exe45_ko_development_roll_food_v1.gba`
SHA256 `986450bc2c3e6aef7688428863e4a0ca478c2ce9b5b60f6628917caecc283bd9`.
불변 원본에서 만든 독립 `_repro.gba`와 최종 도구 `_current_repro.gba` 모두 바이트 동일.
최종 도구322개 해시 일치/드리프트 없음: `roll_food_v1/final_identity_audit.json`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 유지.
누적1,002선택 텍스트 단위와 기존9그래픽. 전체 게임 분모/완료율이 아니다.
14선택 아카이브/718미선택 아카이브 보존. 이전 ROM/상태/번역/조사 기록 보존.
이번 작업에서 새 게임 실행 코드 또는 훅 추가 없음.

## 번역과 보호

원본661858:5121바이트/97슬롯/catalog pointer0x380FC.
원본 풀 SHA256 `2e11a21803e3b5eef47aae6e1e9d2868d822194664b17fcff9771f22c3fcf614`.
새 풀5797바이트, offset8399536/root0x08802AB0,
SHA256 `f871b973fc85a01c222a163fce4dd603487ea0a44f8455fae828e2e72d11d3c8`.
기존 형제자매32단위 source/translation/state 동일, 다른 번역 입력 해시 동일.
새 누적 asset `translations/roll_food_ko.json`, 등록 범위 `all-siblings-food`는1..8과11만 선택.
나머지88스크립트 원본 바이트 동일. 미선택29의 선행 줄바꿈도 보존.
원본/바이너리/의미 roundtrip과 모든 제어명령/인자 보존 통과.

script11의4리터럴을 수동 번역했다:

- 인터넷에서 / 뛰어다니면、 / 배가 고파지네!
- 배고프다 하니까、 뒤의 원본 줄바꿈 유지
- 닉네임 뒤의 `は` → `、`
- 어떤 음식을 / 좋아해?

원문과 같은3페이지/3·2·2행 구조. 최대 새 문구103px, adopted132px/3행 이내.
두 번째 페이지는 첫 행 문구와 두 번째 행 동적 닉네임+쉼표를 별도 검증한다.
닉네임 조사를 고정 한국어 은/는으로 처리하지 않으며 사용자 이름 데이터 변경 없음.
새 조사 접미사 프로필은11:2만 정확한 원문 `は` / 번역 `、`를 허용(11px→11px).
기존1/3/5/7 조사/선택행 보호는 유지한다. 다른 접미사, 원문 변경은 테스트에서 거부.
단일 쉼표는 다른 문구 안에도 존재하므로 문자 검색 첫 결과로 위치를 지정하지 않는다.
첫 static 검사는 중복 쉼표의 단순 검색을 거부했다. 명령 경계 고정 후 재검사 통과.
원본/새 바이너리의 `E8 F9 0C 01 + suffix + E6 00 F1` 유일 명령 경계로 고정한다.
flags3585/3605/3606, nickname/clear/keyWait/waitHold/name-input 명령 그대로.

## 정상 경로와 검증

기존 sisters-v1 읽기 전용 조사 `roll-family-brothers-survey-v3-19`의10단계 입력 recipe만 사용한다.
원 조사ROM b7227159...의 첫 대사11/native LR0x08037F27을 검증한다.
그 조사 상태는 새 ROM의 부모로 사용하지 않는다. 새 own-ROM cold-chain/jackin에서 재현한다.
음식 경로는10단계+다음2페이지 A확인+대기 총13단계이며 음식 입력 초기화 전 중단한다.
입력 시점과 native 선택의 상관만 관측; 전체 난수/날짜/성별/진입 조건을 증명하지 않는다.

새 ROM 정상 진입frame1174/root0x08802AB0/script11/LR0x08037F27 확인.
3페이지4문구와 최종 질문 안정 대기까지 ROM stream→CPU 폰트 읽기→OBJ VRAM→화면 픽셀 검증 통과.
모든 문구의 실제 행/advance와 빈 본문 영역까지 검사해 잔상 없음.
닉네임RAM을 독립 디코딩한 `ああくん`은 원본 개인 입력 데이터이며 번역 누락 문구가 아니다.
원본 이름 폰트와 native advance 테이블을 검증하고 두 번째 행44px 다음 쉼표11px 위치 확인.
원문 후속E600/F1/flags3605·3606 바이트와 질문 cursor를 검증해 음식 입력 초기화 전 대기임을 확인.
최종 질문 cursor0x08803239. 실제 음식 입력 또는 저장 성공을 뜻하지 않는다.
화면: `roll_food_v1/food_pages.png`; 근거: `roll_food_v1/food_runtime.json`.
동일 새 ROM의12보고서 passed=true/release_eligible=false: 음식, 네 형제자매, plugout/return,
greeting/PET/fortune, Rockman/Roll caption. 기존‘통신’ 그래픽 회귀 포함.
집계: `roll_food_v1/cumulative_runtime.json`.
전체 자동 테스트177개 통과(117.316초, exit0).
명령: `python -X utf8 -m unittest discover -s tools -p 'test*.py' --buffer`.
결과: `roll_food_v1/test_summary.txt`. 새2테스트는 기존32문구·전체 제어 보존,
4음식 원문·끝 줄바꿈·폰트·닉네임 조사 실패 가드·12동일 ROM 보고서·닉네임 행/폭을 검사한다.

## 남은 범위

다른88미선택스크립트 슬롯은 번역하지 않고 보존했다. 이 풀의143리터럴 중107개가 남았다.
다음 후보는 취미13/장래 희망15/잘하는 과목27/어려운 과목29이며 각각 정상 진입·변수 보호 조사 필요.
실제 음식 입력·확정·재표시·저장, 실제 가족 이름 입력/저장, 다른 닉네임,
인간 문구/시각 승인, 전체 게임/실기/오디오/배포 QA는 남았다.
패배 회귀는 격리된 단일 table-read alias 진단이며 실제 패배를 증명하지 않는다.
