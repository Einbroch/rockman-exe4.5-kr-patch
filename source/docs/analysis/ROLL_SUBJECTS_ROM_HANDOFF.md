# 롤 귀환 후 잘하는 과목·어려운 과목 — 5문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬에 따라 원본/제어 보존, 정상 진입 조사, 동일 새 ROM 검증과 독립 빌드를 적용한다.

## 개발 ROM

`poc/output/exe45_ko_development_roll_subjects_v1.gba`
SHA256 `bfc695dfeecc6de17ce82ad2b55c5219bec42e6d7ca8bc2179f12612842e0723`.
불변 원본에서 만든 독립 `_repro.gba`와 최종 도구 `_current_repro.gba` 모두 바이트 동일.
최종 도구325개 해시 일치/드리프트 없음: `roll_subjects_v1/final_identity_audit.json`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 유지.
누적1,007선택 텍스트 단위와 기존9그래픽. 전체 게임 분모/완료율이 아니다.
14선택 아카이브/718미선택 아카이브 보존. 이전 ROM/상태/번역/조사 기록 보존.
이번 작업에서 새 게임 실행 코드 또는 훅 추가 없음.

## 범위와 번역

원본661858:5121바이트/97슬롯/catalog pointer0x380FC.
원본 풀 SHA256 `2e11a21803e3b5eef47aae6e1e9d2868d822194664b17fcff9771f22c3fcf614`.
새 풀5985바이트, offset8399536/root0x08802AB0,
SHA256 `5ba011f9c07679512b669d3ec9a3cf6e96205eece785ca6c74324506bd1a56aa`.
기존 형제자매/음식36단위 source/translation/state 동일, 다른 번역 입력 해시 동일.
새 누적 asset `translations/roll_subjects_ko.json`, 등록 범위 `all-siblings-food-subjects`는
1..8/11/27/29만 선택한다. 나머지86스크립트 원본 바이트 동일.
기본 여동생·자매·형제자매·음식 범위는 유지했다.
원본/바이너리/의미 roundtrip과 모든 제어명령/인자 보존 통과.

script27의2리터럴과29의3리터럴을 정상 원문 화면 확인 후 수동 번역했다.
공통3행: ‘전뇌 세계에선、 / 평소에 쌓은 지식이 / 뜻밖에 도움이 돼’.
`とくいかもく`는 ‘잘하는 과목’, `ニガテかもく`는 ‘어려운 과목’으로 구분했다.
좋아함/싫어함이나 선호 과목으로 의미를 바꾸지 않았다.
전뇌 세계 용어와 전체 문구는 개발 초안이며 인간 승인된 용어/말투라고 주장하지 않는다.

두 질문의 원문 닉네임 접미사 `の`는 첫 행 쉼표 `、`로 연결한다(11px→11px).
두 번째 행은 각각 ‘잘하는 과목은 뭐야?’, ‘어려운 과목은 뭐야?’(123px).
고정 한국어 조사 은/는/의 사용이나 사용자 이름 변경 없이 임의 받침 의존성을 피한다.
29:1은 원본의 선행 줄바꿈을 유지하고 ‘어쩌면、 / 없을 수도 있지만、’로 조건을 보존한다.
이 페이지의 첫 행은 네이티브 닉네임만 표시하고 본문은 두 번째·세 번째 행에 둔다.
원문3행 구조 유지, 새 최대123px/adopted132px/3행 이내.
flags3585/3605/3606, nickname/clear/keyWait/waitHold/name-input 명령 그대로.
새2접미사 가드와 기존 음식/형제자매 가드, 선택행 보호를 함께 유지한다.

## 정상 진입 조사

기준은 직전 음식 ROM SHA `986450bc2c3e6aef7688428863e4a0ca478c2ce9b5b60f6628917caecc283bd9`.
그 ROM의 own jackin 상태에서 두 정상 입력 경로를 조사했다.
옛 b7227159... 조사 receipt는 입력 recipe만 참고하고 새 ROM 부모로 사용하지 않는다.
27은 `roll-family-brothers-survey-v1-7`의 첫10입력만 사용한다.
그 조사 후반의 입력/이름 화면 진입 가능성은 버리고 새 주제는 질문 keyWait까지만 관측한다.
29는 `roll-family-brothers-survey-v2-3`의10입력을 사용한다.
첫 페이지 이후27은A1회+대기(총12단계),29는A2회+대기(총13단계).
읽기 전용 observer 사용, ROM/RAM/대사 번호/호출 강제 변경 없음.
원문27 진입frame1162,29 진입frame1158, 모두native LR0x08037F27/root0x08802AB0.
근거: `roll_subjects_survey_v1/native_scenes.json`과 각 경로의 실제 화면·상태·입력 영수증.
전체 난수/날짜/성별/진입 조건을 증명한 것은 아니다.

## 새 ROM 검증

새 own-ROM cold-chain과 jackin에서 동일 정상 입력으로 재현했다.
새 ROM27 진입frame1162,29 진입frame1158, 모두native LR0x08037F27/root0x08802AB0.
두 대화의5문구, 정상5페이지와 최종 질문 안정 대기까지 ROM stream→CPU 폰트 읽기→
OBJ VRAM→화면 픽셀 검사 통과. 모든 문자 행/advance와 빈 본문 영역을 검사해 잔상 없음.
원본 닉네임RAM을 독립 디코딩한 `ああくん`은 원본 개인 입력 데이터이며 번역 누락 문구가 아니다.
닉네임 원본 폰트/native advance 보존, 첫 행44px와 질문 쉼표11px 위치 확인.
29:1의 닉네임 첫 행/조건문 둘째·셋째 행 구조와 실제 앞 줄바꿈 확인.
후속E600/F1/flags3605·3606 원문 바이트와 질문 cursor를 검증해 입력 초기화 전 대기임을 확인.
질문 cursor27:0x088036A5,29:0x08803783.
실제 과목을 입력하거나 저장한 성공을 뜻하지 않는다.
화면: `roll_subjects_v1/strong/subject_pages.png`, `roll_subjects_v1/weak/subject_pages.png`.
근거: 각 `subject_runtime.json`.
동일 SHA의14보고서 모두 passed=true/release_eligible=false: 두 과목, 음식, 네 형제자매,
plugout/return, greeting/PET/fortune, Rockman/Roll caption. 기존‘통신’ 그래픽 회귀 포함.
집계: `roll_subjects_v1/cumulative_runtime.json`.
기존 음식2테스트와 새 source/guard1테스트 통과(10.350초).
전체 자동 테스트179개 통과(125.255초, exit0).
명령: `python -X utf8 -m unittest discover -s tools -p 'test*.py' --buffer`.
결과: `roll_subjects_v1/test_summary.txt`.
새2테스트는 이전36단위·전체 제어 보존,5원문·leading newline 손실 거부,
두 닉네임 조사 실패 가드·폰트·86미선택 바이트 보존·14동일 ROM 보고서·닉네임 행/폭을 검사한다.

## 남은 범위

이 풀의143리터럴 중41개 선택,102개가 남았다.86미선택스크립트 슬롯은 보존한다.
다음 후보는 취미13/장래 희망15 및 다른 선호·친구 대화이며 정상 진입/변수 보호 조사 필요.
실제 과목 입력·확정·재표시·저장, 음식/가족 이름 입력·저장, 다른 닉네임,
인간 문구/시각 승인, 전체 게임/실기/오디오/배포 QA는 남았다.
패배 회귀는 격리된 단일 table-read alias 진단이며 실제 패배를 증명하지 않는다.
