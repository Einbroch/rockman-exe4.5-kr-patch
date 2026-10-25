# 롤 귀환 후 형·오빠/남동생 질문 — 16문구 추가

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬에 따라 원본/제어 보존, 정상 진입 조사, 동일 새 ROM 검증과 독립 빌드를 적용한다.

## 새 개발 빌드

`poc/output/exe45_ko_development_roll_family_siblings_v1.gba`
SHA256 `47f8e3ec2097f9b72a14ce7edf116d06d8efa8e31b82f14893b81e0d5ddfeec3`.
불변 원본에서 생성한 독립 `_repro.gba`, 최종 `_current_repro.gba` 모두 바이트 동일.
최종 도구318개 해시가 `_current_repro.json`과 일치하며 드리프트 없음.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 유지.
누적998선택 텍스트 단위/기존9그래픽. 전체 게임 분모나 완료율이 아니다.
14선택 아카이브/718미선택 아카이브 보존, 이전 ROM/상태/번역/조사 기록 보존.
새 게임 실행 코드 또는 새 훅 변경 없음.

원본661858:5121바이트/97슬롯/catalog pointer0x380FC.
풀 SHA256 `2e11a21803e3b5eef47aae6e1e9d2868d822194664b17fcff9771f22c3fcf614`.
새 풀5719바이트, offset8399536/root0x08802AB0,
SHA256 `3948d5290c1ad114ca9ee717c12502de3c74c8d9d7126cbac30c294fbbc0137f`.
원본/바이너리/의미 roundtrip, 모든 명령·인자 보존 통과.
이번 추가는 scripts1/2/3/4의16문구. 기존5/6/7/8의16문구는 source/translation/state 그대로.
`translations/roll_family_siblings_ko.json`이 새 누적 선택 asset이며 이전 자매 asset은 보존한다.
다른 기존 번역 입력 해시 동일. 등록된 `all-siblings` 범위만1..8을 선택한다.
기본 여동생 범위와 이전 자매 범위는 변경하지 않았다.
나머지89스크립트 원본 바이트 동일. 이전 미선택29 선행 줄바꿈 보존 포함.

## 정상 진입 조사

기준 ROM은 기존 sisters-v1 SHA `b7227159ae498da3ac3da7e6620d1582170086c20d7e76d778aa7efd8353bb67`.
그 ROM의 own jackin checkpoint에서 조사했고 이전 plugout 조사 receipt는 입력 recipe만 사용했다.
ROM/RAM/대사 번호 강제 변경 없음. 도구 `tools/survey_roll_family_brothers.py`.
첫 조사v1의6시점은5/11/27/29 등을 선택해 형제 진입을 증명하지 못했다.
v1의 긴 입력으로 다른 대사가 진행된 상태는 새 정상 부모로 사용하지 않는다.
다음v2/v3은 첫 대사 페이지만 관측하는10단계로 제한했다.
v2 delay10에서는 native1(frame1165), v3 delay18에서는 native3(frame1173)을 관측했다.
둘 다 root0x08802AB0, LR0x08037F27. 같은 조사에서1/3 이외 주제도 관측했다.
입력 시점과 선택 결과의 상관을 관측했을 뿐 전체 선택 조건/난수/날짜/성별을 증명한 것은 아니다.
조사30경로(v1 6+v2 12+v3 12)와 각각의 입력·상태·화면·영수증을 보존한다.
native호출 후보/소스 Thumb 디스어셈블은 조사 참고일 뿐 호출 강제나 실행 코드 변경에 사용하지 않았다.

## 수동 번역과 보호

원문 `おにいちゃん いるの?`는 손위 남자 형제를 묻는다.
플레이어 성별을 가정하지 않도록 ‘형이나 오빠 있어?’로 작성했다.
`おとうといるの?`는 ‘남동생 있어?’로 구분했다. 인간 문구/말투 승인은 미완료다.
각 분기의 인터넷 이야기3페이지, 닉네임 질문, 있어/없어, 이름 질문, No 응답을 수동 작성했다.
source1人じめ의 단독 독차지 의미는‘혼자만 독차지하면’으로 보존한다.
기존16자매 단위의 자동 문장 변환 없음. 새 source 값은 기존 불변 추출에서 복사하고 빌드에서 재추출 대조한다.

네 닉네임 접미사 모두 source‘は、’→target‘、’,22px→11px.
고정 한국어 은/는 조사나 사용자 이름 변경 없이 네이티브 쉼표로 연결한다.
원본 이름 글리프/advance 공급 및 실제 닉네임 위치는 런타임에서 별도로 검사한다.
최대123px/3행, adopted132px/3행 이내. 형·오빠 질문111px, 남동생 질문79px.
네 선택행 각각96px: spacePx16+space1+있어40px+space1+없어24px.
원문 질문 페이지와 선택 페이지를 합치지 않는다. defaultYes/No target2·4·6·8/취소/뒤 공백2개 보존.
flags3585/3735/3736/3737/3738/3605/3606, keyWait/clear/waitHold/name-entry 명령 그대로.
새 테스트는 네 접미사의 조사 변경과 네 선택행 overflow를 거부하며 이전16단위 일치도 확인한다.

## 새 ROM 런타임/테스트

정상 네 분기32문구의 ROM stream→CPU 폰트 읽기→OBJ VRAM→화면 픽셀 검사 통과.
각 질문·선택·응답의 빈 본문까지 검사해 잔상 없음. 닉네임RAM9B9BA2CA/E5를
‘ああくん’으로 독립 디코딩하고 원본 글리프/advance/쉼표 위치 확인.
각 선택 기본‘있어’ x100/y108, 오른쪽‘없어’ x148→왼쪽100→오른쪽148 및 No 응답 검증.
source nickname 데이터는 변경하지 않았다.
새 형·오빠1 진입frame1165, 남동생3 진입frame1173. 기존 자매5/7 진입frame1154/2006.
모두 네이티브 LR0x08037F27/root0x08802AB0.
네 Yes 이름 질문 cursor(1/3/5/7):0x08802C9B/0x08802E01/0x08802F70/0x088030D6.
원본 후속E600/F1/flags3605·3606 바이트를 검사해 입력 초기화 전 대기임을 검증했다.
각 `older-brother/younger-brother/older/younger/family_pages.png`의8화면은 정상 경로,
9번째 칸은 빈칸이다. 모음 위치: `analysis/roll_family_siblings_v1/`.
`tools/run_roll_family_siblings.py`는 새 own cold-chain과 jackin 상태를 만든다.
이전 상태/조사 상태는 새 ROM의 부모가 아니라 입력 recipe만 참고한다.
형·오빠/남동생 entry는 조사10단계+원문 다음4페이지 확인+선택 페이지 대기15단계.
각 Yes는 이름 질문 keyWait까지만 관측하며 실제 이름 입력·확정·저장까지 검증하지 않는다.
No는 native2/4 응답 경로를 소비한다. 실제 가족 정보가 입력됐다는 뜻이 아니다.
모든 런타임 상태는 격리된 개발 폴더의 임시 데이터다.

동일 SHA의11보고서 모두 passed=true/release_eligible=false:
네 family_runtime, plugout/return regression, greeting/PET regression,
fortune runtime, Rockman regression, Roll caption.
플러그아웃 No/B/좌우/Yes/응답, 귀환2정상 페이지, 패배2진단 페이지,
인사2문구, PET22관측/29선택, 운세23정상 문구·연출점, Roll/Rockman 장비·폴더·무기·
공격력·숫자 및 기존‘통신’ 그래픽 회귀 통과.
패배는 단일 table-read alias1→2 진단일 뿐 실제 패배 아님. 진단 상태 격리,
normal_play_checkpoint_eligible=false, 정상 진행 부모로 사용하지 않았다.
전체 자동 테스트175개 통과(104.117초, exit0).
명령: `python -X utf8 -m unittest discover -s tools -p 'test*.py' --buffer`.
상세 기록: `analysis/roll_family_siblings_v1/test_summary.txt`.

## 미완료

같은 풀의 선호/친구/동적 이름 재사용 등89미선택스크립트는 보존하며 번역되지 않았다.
실제 이름 입력·확정·재표시·저장 지속성, 다른 닉네임, 인간 문구·시각 승인,
전체 게임/실기/오디오/배포 QA는 남았다. 형제자매4주제 번역이 풀 전체 완료는 아니다.
