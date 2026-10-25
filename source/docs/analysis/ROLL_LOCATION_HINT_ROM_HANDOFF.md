# 롤 운세 지역 안내 — 마지막 미번역 1문구 반영

2026-10-03. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역이나 배포 승인이 아니다.
한글패치 스킬의 원본 보존, 재현 빌드, 원래 제어 처리 보존,
실행 픽셀 검증 및 정상 플레이/개입 진단 분리를 적용했다.

## 최신 누적 개발 ROM

`poc/output/exe45_ko_development_roll_location_v3.gba`
SHA256 `e56d4915752c025ba8b9c91705c83452ed02386a4fc5697298fc499c611be3d0`.
원본에서 독립 생성한 `_repro.gba`, 최종 도구의 `_current_repro.gba` 모두 바이트 동일.
`_current_repro.json`의 build_tools_sha256은 최종 tools/*.py 해시와 일치한다.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 변경 없음.
이전 입력/ROM/세이브 상태/실행 증거는 보존했다.
누적953텍스트 단위와 기존 그래픽9개는 전체 게임 분모나 완료율이 아니다.
PET ‘통신’, 장비/폴더/버스터 공격력 그래픽을 포함한 기존 그래픽 작업도 유지한다.

## 이번 추가 번역 및 보호

`translations/roll_fortune_complete_ko.json`, registry variant
`fortune-and-minigame-complete-v3`, builder 선택 `--roll-fortune-complete`.
이전102개 ID/원문/번역/상태 그대로 보존. 추가 ID `65FF3C:23:0`:

원문: こわーい ふんいきの / エリアにありそうな / よかんがするよ!

초안: 무서운 분위기의 / 에리어에 있을 것 같은 / 예감이 들어!

주 에이전트가 원문에서 직접 작성한 초안이다. 원문에 없는 지명을 넣지 않았다.
원문의3줄 유지, 실제 가로 폭92/132/79px, 채택한132px/3행 범위 내.
원문에 없는 leading clearMsg를 추가하지 않았다.
65FF3C 풀109리터럴은 이제103한국어 초안 + 원문 연출점6개다.
이 풀의 일본어 산문을 처리한 것이며, 다른 대사 풀/전체 게임 완역을 뜻하지 않는다.
미선택35스크립트 바이트 동일. 제어 명령/인자/난수/플래그/대기/아이템 지급
및 숫자 삽입 처리 그대로. 바이너리/의미 roundtrip 통과.
새 풀6363바이트 SHA256
`c7a189732ceef6b3a7777a87e6441a5f1291228d54fa38618346a8a92e0d2628`,
ROM offset8392564/root08800F74. 원본 풀 저장 범위와 네이티브 처리 코드 보존.

## 페이지 전환의 근거와 개입 범위

네이티브 EE33 처리08050E38에서 행운 아이템 위치를 조회한 후,
08050E40의 target byte 읽기 → 0804FD18의 점프 → 0805543C의 clear.
clear는 x/context+70, row/context+0F를0으로 만들고,
02012F50 및02013E50에서 각각F00바이트를0800092C로 지운다.
해당 원본 코드4범위를 SHA로 고정하고 새 ROM에서도 동일함을 확인했다.

새 ROM 자체의 정상 cold-chain → Roll 나비 메뉴 → 결과 직전 상태에서 시작했다.
일반 버튼 delay98frames로 레드 하트 결과 및 마지막 ‘오늘의 / 행운의 아이템은・・・’
페이지를 그대로 거친다. 진단 observer는 PC08050E40, 활성 풀/문맥,
EE33 opcode 및 읽기값20을 모두 확인한 한 번의 byte 읽기에만23을 반환한다.
observer의 ROM/RAM 쓰기, 직접 함수 호출, 스크립트 초기화 우회는 없다.
이후 점프/clear/3줄 출력은 게임 원래 코드다.

실행 관측: target alias1회, hint23 jump1회, clear1회.
그 clear 직후 7,680바이트가 모두0, x=0/row=0.
앞 페이지와 새 안내 모두 ROM 폰트→OBJ VRAM→화면 픽셀 일치.
전체 글자 영역의 빈 곳도 검사해 이전 글자 잔상 없음.
`analysis/roll_location_v3/hint_transition.png`, `hint_runtime.json` 참조.
진단 checkpoint는 `diagnostic_checkpoint.mss`로 격리,
normal_play_checkpoint_eligible=false. 일반 실행의 부모로 쓰지 않는다.
실제 일반 플레이에서23번 지역이 선택되거나 아이템을 획득한 증거는 아니다.

## 누적 회귀 검증

모든 경로는 새 ROM 해시와 자체 cold-chain 세이브를 사용했다.
정상 운세23단위: introduction/blue/red/viridian/orange 및 번호 안내20.
6개 연출점의 원문/대기 프레임 유지, glyph read/VRAM/화면 및 빈 영역 검사 통과.
보상4진단 경로52/53/62/63에서14단위와800제니/5버그 조각의
네이티브 숫자 합성/폭/VRAM/픽셀을 다시 확인. 미니게임 실제 승리·기록·지급 증거 아님.
이103입력의 증거 분모: 정상23 / 보상진단14+지역안내진단1 / 정적검사65.
반복일 인사/다른 하트/미니게임 실패·성공 등 정적만 남은 문구의 정상 실행 확인은 미완료.
이전 ROM의 진단 관측을 새 ROM 정상 실행 증거로 이전하지 않았다.
인사, PET29선택/22실행문구, Roll 장비 안내, Rockman 폴더/장비/무기 전환/공격력
회귀 보고서가 동일 새 ROM 해시로 통과한다.

## 재현 및 다음 작업

빌드: `python -X utf8 tools/build_roll_pet.py --roll-intro --roll-fortune-complete --work FRESH --out FRESH.gba`
실행 recipe: `run_roll_fortune_matrix`/`run_roll_fortune_samples`의 STEM/PREFIX를
새 ROM/새 경로로 지정. 기존 상태는 입력 recipe만 참고한다.
진단: `capture_roll_location_hint.py`, 검증: `report_roll_location_hint.py`.
추가 회귀 테스트: `tools/test_roll_location_hint.py`의4개 검사.
전체 테스트 결과는 `analysis/roll_location_v3/test_summary.txt` 참조.

다음은 다른 나비/다른 대사 풀의 미번역 목록을 재조사하고, 원문·호출 문맥을 확정해
다음 소규모 번역 입력을 분리해야 한다. 새 번역마다 불변 원본 빌드와
해당 ROM 자체의 cold-chain 검증을 반복한다.
미관측65문구의 정상 플레이, 실제 미니게임 성공/보상, 다른 이미지의 전체 인벤토리,
인간 문구/시각 검토, 실기·오디오·전체 게임 및 배포 QA는 아직 남아 있다.
