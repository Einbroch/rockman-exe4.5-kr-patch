# 롤 플러그인 직전 대사 — 5문구 추가 반영

2026-10-03. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬의 원본 보존/제어 처리 보존/독립 재현 빌드/정상과 진단 증거 분리 및
실제 ROM 폰트→OBJ VRAM→화면 픽셀 검증을 적용했다.

## 최신 누적 개발 ROM

`poc/output/exe45_ko_development_roll_jackin_v1.gba`
SHA256 `53817f7969f64c2391173782e7fe1dd1280d3e904c31d2e609bef0bafca46363`.
불변 원본에서 독립 생성한 `_repro.gba`와 최종 도구 `_current_repro_r2.gba`도 바이트 동일.
최종 도구 해시는 `_current_repro_r2.json`의 build_tools_sha256에 고정한다.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 변경 없음.
이전 입력/ROM/세이브/실행 증거 보존. 이전102/103운세 초안도 그대로다.
누적958텍스트 단위와 기존9그래픽은 전체 게임 분모/완료율이 아니다.
PET ‘통신’, 장비 제목/폴더 제목/버스터 공격력 등 기존 그래픽 유지.

## 원문·번역 범위

원본 catalog `660CA8:231=380E4`, script_count5.
`translations/roll_jackin_ko.json`의5리터럴(1:0,2:0,2:1,3:0,3:1) 전부 선택.
원본 풀 SHA256 `651621ec0242ed05ace62459bbd62e30e9b2712944c358c9f125967f120c2ff3` 고정.
정상 대사창92,110에 표시되는 롤의 전송 구호/내키지 않는 반응/기대하는 반응이다.
기분 분기 조건은 문구만으로 추측하지 않는다.

대표 초안:

- 플러그인! / 롤.EXE、 / 트랜스미션!!
- 오늘은 플러그인을 / 그만두면 안 될까? / 별로 내키지 않아
- ・・・・・・라고 / 말해도 플러그인할 / 거잖아・・・
- 왠지 오늘은, / 좋은 일이 생기겠어!
- 후후, 신이 나네!

주 에이전트가 원문 문맥에서 직접 작성. 기존 플러그인/롤 표기 일관성 유지.
‘트랜스미션’은 음역 개발 후보이며 공식 한국어 승인으로 주장하지 않는다.
EXE 접미사, 원문 줄 수, flags3603/3651, wait30, clearMsg/keyWait/waitHold,
창/화살표/분기 등 모든 제어 명령/인자 그대로.0/4슬롯 바이트 동일.
최대123px/3행, adopted132px/3행 안. 원문/바이너리/의미 roundtrip 및 폰트 공급 통과.
새 실행 코드/새 게임 훅/게임 데이터 안의 진단 개입은 없다.
새 풀404바이트 SHA256 `460447b6ff32edcf132500007d6cb47c2f7aa942a51d0053afcd6c5c9a33bcde`,
ROM offset8398928/root08802850. 최종 현재 도구301개 해시 확인.

## 경로 조사와 정상 실행

고정된 이전 location-v3 ROM에서 정상 컨트롤러 경로를 먼저 조사했다.
`roll-jackin-survey-v1`은 저장 질문, v2는 토너먼트 질문으로 이동한 조사 기록이며
목표 텍스트 미관측을 패치 실패로 판단하지 않았다. 저장 예를 확정하지 않았다.
v3에서 로드 직후60프레임 대기, 아래 이동, 플러그인 확인 예로 원문 script2 진입 확인.
v4에서 다음 페이지 이후 script1이 이어지는 것을 확인했다.
이전 상태는 입력 recipe만 참고하고 새 ROM의 정상 cold-chain 상태를 별도로 생성했다.

새 `roll-jackin-v1-normal` 경로:
own cold-chain → Roll 인사/운세 → PET 플러그인 확인 예 → script2의2페이지 →
script1 전송 구호 → 인터넷 화면.
네이티브 호출08037F22→0804F7B6, LR08037F27, 순서2(frame238)→1(frame693).
전체3문구의 ROM 코드/폰트 CPU 읽기/OBJ VRAM/화면 픽셀 일치,
빈 글자 영역까지 검사해 앞 페이지 잔상 없음. 인터넷 진입 이후 이 풀의 글자 trace 중단.
인터넷 화면 진입을 검증한 것이며, 배틀/실제 보상/임의 지역 탐색 완료를 뜻하지 않는다.

## 중간 캡처의 판정

구호 마지막 글리프는 frame746에 그려졌다. step13/frame749에서는 글리프/VRAM은
완료됐지만 화면 마지막 느낌표의10픽셀이 이후 화면과 달랐다.
step14/frame760은 같은 cursor와 같은 전체 draw trace를 유지한 채 엄격 픽셀 검사 통과.
변화한10픽셀은 마지막 느낌표 안의 x167,y138..148에만 있었다.
ROM은 변경하지 않았다. step13을 완성 화면으로 인정하지 않고
`in_flight_snapshots_not_credited`에 실패·위치·프레임·후속 통과를 기록했다.
검사기의 기대를 낮추거나 해당 픽셀을 가리는 수정은 하지 않았다.
완성 구호 증거는 step14/15. wait30의 컴파일 인자ED001E00 보존,
대기 cursor 관측과 이후 flagClear/waitHold 이동을 따로 기록했다.
샘플 사이의 정확한 호출 프레임/실기 타이밍을 측정한 것은 아니다.

## 밝은 기분 2문구 진단

`roll-jackin-v1-upbeat-diagnostic`: 같은 새 ROM 정상 Roll/PET 확인 경로에서 시작.
네이티브 초기화의 script2 offset 읽기 한 번을 script3 offset으로 반환한다.
PC0804FB76, pool/주소, offset값, r1=4, context0200FA20을 모두 가드한다.
caller/initializer 원본 코드3범위를 고정하고 원본/새 ROM 바이트 동일 확인.
observer ROM/RAM 쓰기나 함수 직접 호출 없음. 원래 글자·대기·페이지 소비를 사용한다.
context의 native script ID는2이며 displayed entry는3이다. 혼동하지 않는다.
2문구 전체 폰트/VRAM/화면/빈 영역 통과.
밝은 기분의 실제 조건이나 일반 플레이에서의 분기 선택을 증명한 것은 아니다.
diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false.
패치 내용과 정상 실행 부모 상태에는 이 개입을 넣지 않는다.

## 누적 회귀 및 재현

같은 새 ROM에서 인사2문구, PET22관측/29선택 단계, 정상 운세23단위와 연출점 대기,
Roll 장비 안내, Rockman 폴더/장비/무기 전환/공격력·숫자 및 기존 그래픽 회귀 통과.
보상/지역안내 진단의 이전 관측은 이전 ROM 증거이며 이번 ROM으로 자동 이전하지 않는다.
이전 번역 입력은 동일하고 새 누적 ROM에서 폰트/폭/구조 정적 검사가 이루어진다.
이번 플러그인5입력 증거는 정상3/진단2, 정적만인 새 리터럴은0.
일반 플레이의 밝은 기분 분기는 미확인이다.

빌드: `python -X utf8 tools/build_roll_pet.py --roll-intro --roll-fortune-complete --roll-jackin --work FRESH --out FRESH.gba`
probe: `capture_roll_jackin.py`, 별도 진단 `capture_roll_jackin_upbeat.py`.
보고서: `analysis/roll_jackin_v1/jackin_runtime.json`, `jackin_pages.png`.
추가 테스트4개: `tools/test_roll_jackin.py`; 전체158테스트 통과(72.452초).
초기 테스트1개는 검증 보고서 키를 잘못 참조해 실패했으며 테스트 키 수정 후 전체 재실행 통과.
제품 ROM은 바뀌지 않았다. 전체 결과 `test_summary.txt` 참조.

다음 후보는 인접 Roll 귀환 풀65FEC0(일반 귀환/패배 및 닉네임 접미사)이다.
닉네임 뒤 첫 행의 원본 쉼표와 동적 폭을 보존하고, 귀환 호출 경로/상태를 먼저 확인해야 한다.
다른 나비/대사 풀/이미지 전체 조사, 인간 문구/시각 검토, 실기·오디오·전체 게임 QA,
배포 조건 검증도 아직 남아 있다.
