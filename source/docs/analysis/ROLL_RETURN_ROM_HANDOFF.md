# 롤 귀환·패배 대사 — 4문구 추가 반영

2026-10-03. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬에 따라 원본/제어 처리 보존, 독립 재현 빌드, 정상·진단 증거 분리와
ROM 폰트→OBJ VRAM→화면 픽셀 검증을 적용했다.

## 최신 누적 개발 ROM

`poc/output/exe45_ko_development_roll_return_v1.gba`
SHA256 `04fa8f4ee432880ef52469ae149e42de6d5043e1db8b6699806d5f2c70e21c52`.
불변 원본에서 만든 `_repro.gba`, `_current_repro.gba`, `_current_repro_r2.gba`,
최종 `_current_repro_r3.gba` 모두 바이트 동일.
최종 현재 도구305개의 해시는 `_current_repro_r3.json`에 고정하며 드리프트 없음 확인.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 변경 없음.
이전958텍스트 입력 해시 전부 동일, 새4문구를 합쳐962텍스트 단위.
기존9그래픽/PET ‘통신’ 유지. 이 수치는 전체 게임 분모/완료율이 아니다.
이전 입력/ROM/세이브/실행 증거 보존. 게임 실행 코드/새 게임 훅 변경 없음.

## 선택 범위와 보호

원본 archive65FEC0,123바이트, script_count4, catalog pointer380DC.
원본 풀 SHA256 `ae766f6e7423463ca65f478567c93b3a551fd2e53f7f54820453892bb692b62f`.
새 풀201바이트, ROM offset8392564/root08800F74,
SHA256 `8d4669a486e987481fcb4398accfa6861f2836105aaccd401a75ca32d3c0b8ac`.
`translations/roll_return_ko.json`의4문구를 주 에이전트가 원문 문맥에서 직접 작성했다.

- 1:0 — 휴, 다녀왔어!
- 1:1 — 원본 닉네임 뒤 쉼표 / 수고했어!
- 2:0 — 아야야・・・ / 당해 버렸네
- 2:1 — 다음엔 제대로 / 오퍼레이팅해 줘!

‘오퍼레이팅’은 미승인 음역 개발 후보. 인간 문구/말투 검토는 남았다.
원문 줄 수/창 위치/화살표/printPlayerNickname/clearMsg/keyWait/waitHold 등
모든 명령과 인자 유지. 비리터럴0/3슬롯 바이트 동일, 원본 풀도 그대로.
리터럴 최대103px/2행, adopted132px/3행 이내. 구조/바이너리/의미 roundtrip 및 폰트 공급 통과.
nickname_suffix_literal=1을 추가하되 이전 PET의 기본 리터럴0 검사도 유지.
닉네임 뒤 첫 줄 쉼표는 원본과 정확히 동일; 이름 길이·한국어 조사 의존성을 추가하지 않는다.
변조된 접미사 첫 줄은 빌드 전 검증에서 거부한다.

## 정상 귀환 경로

이전 jackin-v1 ROM에서 먼저 읽기 전용 경로 조사:
survey-v1은 로드 직후 입력, v2의 R 확인창은 기본 ‘아니요’로 취소,
v3의 L은 조언 대사였다. 이 목표 미관측을 패치 실패로 간주하지 않는다.
survey-v4에서 R→왼쪽→A로 ‘예’ 선택, 다음 A로 플러그아웃 후 원문 귀환 확인.
새 ROM에서는 이전 상태를 부모로 사용하지 않고 입력 recipe만 참고했다.

own cold-chain → Roll 선택/인사 → PET 플러그인 → 인터넷 →
R 확인창/‘예’ → 귀환script1 →2페이지 → 다음 원본 대사 풀08661858.
`roll-return-v1-jackin`21단계, `roll-return-v1-normal`9단계가 같은 ROM 해시에 귀속된다.
귀환 네이티브 호출08037F22→0804F7B6, LR08037F27, script1/frame708.
첫 페이지step5/6, 닉네임 페이지step7. 다음 대사로 이동한step9에는
귀환 ROM/닉네임 draw trace가 더 이상 추가되지 않았다.

닉네임 RAM02010AC0의 실제4바이트9B9BA2CA 및 E5종단을 독립 디코딩해
기본 이름 ‘ああくん’을 확인했다. 실제 RAM 바이트/글리프 인덱스/advance/쉼표 위치,
원본 네이티브 폰트와 새 폰트 동일, CPU 폰트 읽기, OBJ VRAM와 화면 픽셀 모두 검증했다.
이름은 사용자 데이터이므로 임의 번역/변경하지 않았다.
다른 이름 입력·최대 길이 실험까지 한 것은 아니며 첫 줄을 늘리지 않는 보호만 적용한다.
두 페이지 모두 빈 글자 영역 검사를 포함해 이전 페이지 잔상이 없다.

## 패배 대사 진단 — 정상 패배 증거 아님

같은 새 ROM 인터넷 부모 상태에서 `roll-return-v1-defeat-diagnostic` 실행.
네이티브 초기화script1 table offset 읽기 한 번만 script2 offset으로 반환했다.
PC0804FB76, 주소/pool/원래offset8/r1=2/context0200FA20 가드,
대상offset82, 별칭1회. caller/initializer3범위 원본 코드 해시/바이트 동일 확인.
observer ROM/RAM 쓰기나 함수 직접 호출 없음. 네이티브 script ID는1,
표시한 entry는2이며 일반 플레이 분기로 주장하지 않는다.
2페이지의 전체 폰트/CPU 읽기/VRAM/화면/빈 영역 검사가 통과했다.
diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false.
실제 전투 패배·부활 조건 및 해당 정상 분기 검증은 미완료다.

## 누적 회귀와 후속 작업

같은 새 ROM에서 인사2문구, PET22관측/29선택 단계, 정상 운세23문구와
연출점 대기, Roll 장비 안내, Rockman 폴더/장비/무기/공격력·숫자·그래픽 회귀 검사.
운세 `runtime.json`과 귀환 `return_runtime.json`을 별도 파일로 유지한다.
전체 자동 테스트162개 통과(284.944초), 종료 코드0.
명령 `python -X utf8 -m unittest discover -s tools -p 'test*.py' --buffer`.
결과는 `analysis/roll_return_v1/test_summary.txt` 참조.
스크린샷 모음 `analysis/roll_return_v1/return_pages.png` 위쪽2개 정상/아래쪽2개 진단.

다음 미번역 후보는 실제로 보인 플러그아웃 확인/응답과 귀환 후 후속 대사다.
확인창 기본 ‘아니요’ 및 닉네임/선택 제어를 유지하며 새 범위를 따로 고정해야 한다.
다른 내비/날짜·기념일 등 전체 미번역, 실제 패배 분기, 인간 문구/시각 승인,
전체 게임/실기/오디오/배포 QA는 남았다. 이전 ROM의 진단 증거는 자동 이전하지 않는다.
