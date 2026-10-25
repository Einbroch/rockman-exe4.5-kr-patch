# 롤 귀환 후 누나·언니 질문 — 8문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬에 따라 원본과 제어문자를 보존하고, 기존 여동생 분기를 포함한
동일 ROM의 정상 소비 경로 및 독립 재현 빌드를 검사한다.

## 빌드와 선택 범위

`poc/output/exe45_ko_development_roll_family_sisters_v1.gba`
SHA256 `b7227159ae498da3ac3da7e6620d1582170086c20d7e76d778aa7efd8353bb67`.
불변 원본에서 생성한 `_repro.gba`, 최종 `_current_repro.gba` 모두 바이트 동일.
최종 도구314개 해시는 `_current_repro.json`에 고정했으며 드리프트 없음.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 유지.
14선택 아카이브,718미선택 아카이브 유지. 누적982텍스트 단위/기존9그래픽.
전체 게임 분모나 완료율이 아니다. 이전 ROM/번역/상태/조사 기록 보존.
새 게임 실행 코드 또는 새 훅 변경 없음.

원본661858:5121바이트,97슬롯, catalog pointer0x380FC.
풀 SHA256 `2e11a21803e3b5eef47aae6e1e9d2868d822194664b17fcff9771f22c3fcf614`.
새 풀5420바이트, offset8399536/root0x08802AB0,
SHA256 `73af2f5be93360b5ba8e2e1371155f27d879ced3b6242b8519808856af5f39cd`.
원본/바이너리/의미 roundtrip 및 모든 제어명령·인자 보존 통과.
이번 추가는 scripts5/6의8문구. 기존7/8의8문구는 source/translation/state 그대로 유지.
새 누적 asset `translations/roll_family_sisters_ko.json`이 기존 여동생 asset 대신 선택된다.
이전 asset 자체는 보존하고 다른 기존 번역 입력 해시도 그대로 유지한다.
등록된 `older-younger-sisters` 범위만5/6/7/8을 선택하며 기본7/8 범위는 변경하지 않았다.
나머지93스크립트 원본 바이트 동일. 이전에 수정한 미선택29 선행 줄바꿈 보존 포함.

## 원문 문맥과 번역

읽기 전용 `roll-family-survey-v1`의 정상 입력 경로에서 native script5를 관측했다.
script5의 원문 `おねえちゃん いる?`는 손위 여자 형제를 묻는다.
플레이어 성별을 가정하거나 친족 성별을 바꾸지 않도록 ‘누나나 언니 있어?’로 수동 작성했다.
한국어 자연스러움/말투에 대한 인간 승인은 미완료다.

- 인터넷、 / 재밌었지!!
- 이 즐거움을 / 혼자만 독차지하면 / 안 되잖아
- 누군가에게 / 알려 줘야겠어!
- 닉네임 뒤 쉼표 / 누나나 언니 있어?
- 있어(원본 뒤 공백2개) / 없어
- 있지, 이름이 뭐야?
- 아, 그렇구나・・・

원문1人じめ의 단독 독차지 의미 보존. 새로운8문구는 주 에이전트가 원문 문맥에서 직접 작성했다.
기존 여동생8문구의 자동 문장 변환은 하지 않았다.
최대123px/3행, adopted132px/3행 이내. 누나·언니 질문 둘째 행111px.
원문 topic 접미사‘は、’는 정확한 네이티브 쉼표‘、’로 옮겨22px→11px.
동적 닉네임 자체는 번역하거나 변경하지 않으며 고정 한국어 조사도 붙이지 않는다.
5/7 양쪽 접미사를 검사하고 미등록 조사/소스 불일치/폭 증가는 빌드에서 거부한다.
별도 clear된 선택 페이지: spacePx16+space1+있어40px+space1+없어24px=96px.
5/7 양쪽 선택행 검사, 원본 defaultYes/No targets6·8 및 취소 유지.
flags3585/3737/3738/3605/3606, keyWait/clear/waitHold/name-entry 명령 그대로.

## 새 ROM 런타임 검증

누나·언니 정상8문구의 ROM stream→CPU 폰트 읽기→OBJ VRAM→화면 픽셀 검사 통과.
기본‘있어’ x100/y108, 오른쪽‘없어’ x148→왼쪽100→오른쪽148 및 native6 응답 검증.
닉네임RAM9B9BA2CA/E5를‘ああくん’으로 독립 디코딩하고 원본 글리프/advance/쉼표 위치 확인.
질문·선택·응답 빈 본문의 잔상 검사 통과. 네이티브 script5 진입 frame1154,
LR0x08037F27, root0x08802AB0. Yes는 원본 keyWait와 후속clear/입력 초기화 flags 앞에서 중지.
모음 `analysis/roll_family_sisters_v1/older/family_pages.png`의8화면 모두 정상 경로다.
마지막9번째 칸은 빈칸이다.
동일 새 ROM의 여동생7/8 정상8문구도 같은 검사 통과. 총16문구 정상 관측이며
`analysis/roll_family_sisters_v1/younger/family_pages.png`로 이전8문구 회귀를 확인한다.
두 Yes 질문의 cursor는 각각0x08802E45/0x08802FAB, 후속 원본
E600/F1/flags3605·3606 바이트를 검사해 실제 이름 입력 초기화 전 대기임을 검증했다.
이전 상태는 새 ROM의 부모가 아니라 입력 recipe 참고용이다.
새 own cold-chain을 생성하는 `tools/run_roll_family_sisters.py`로 정상 경로를 재현한다.
누나·언니 entry는 survey-v1의14단계 입력, 여동생 entry는 이전 sister-v1의20단계 입력.
선택 조건을 랜덤/날짜/성별로 단정하지 않는다.
각각 Yes는 이름 질문 keyWait까지만 관측한다. 실제 이름 입력·확정·저장 검증은 하지 않는다.
No는 원문 native6/8 응답 경로다. 실제 가족 정보를 설정했다는 뜻이 아니다.
모든 기록은 격리된 개발 런타임의 임시 상태다.

동일 SHA의9보고서가 모두 passed=true/release_eligible=false:
older/younger family_runtime, plugout/return regression, greeting/PET regression,
fortune runtime, Rockman regression, Roll caption.
플러그아웃 No/B/좌우/Yes/응답, 귀환2정상 페이지, 패배2진단 페이지,
인사2문구, PET22관측/29선택, 운세23정상 문구·연출점, Roll/Rockman 장비·폴더·무기·
공격력·숫자 및 기존‘통신’ 그래픽 회귀 통과.
패배는 단일 table-read alias1→2의 진단일 뿐 실제 패배 아님. 진단 상태 격리,
normal_play_checkpoint_eligible=false, 정상 진행의 부모로 사용하지 않았다.
최종 전체 자동 테스트173개 통과(207.273초, exit0).
명령: `python -X utf8 -m unittest discover -s tools -p 'test*.py' --buffer`.
상세 기록: `analysis/roll_family_sisters_v1/test_summary.txt`.

## 미완료

같은 풀의 형/남동생·선호·재사용 대사, 실제 이름 입력·저장/다른 닉네임,
인간 문구·시각 승인, 전체 게임/실기/오디오/배포 QA는 남았다.
패배 진단은 정상 진행 부모가 아니며 실제 패배 검증을 대체하지 않는다.
