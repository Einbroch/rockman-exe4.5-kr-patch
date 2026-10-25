# 롤 플러그아웃 확인·응답 — 4문구 추가

2026-10-03. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 게임 완역/배포 승인이 아니다.
한글패치 스킬의 원본·제어 보존, 범위 고정, 독립 재현, 실제 소비 경로 및
정상·진단 증거 분리 기준을 적용했다.

## 최신 누적 개발 ROM

`poc/output/exe45_ko_development_roll_plugout_v1.gba`
SHA256 `dddc3a3d5c4f6c73f5f1e54be62ace5b919f839528b5caa3408482f9c9a85163`.
불변 원본에서 만든 `_repro.gba`와 `_current_repro.gba`도 바이트 동일.
최종 도구308개 해시를 `_current_repro.json`에 고정하고 드리프트 없음 확인.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 변경 없음.
이전962텍스트 입력 해시 그대로,4개 추가=966선택 단위. 기존9그래픽/‘통신’ 유지.
전체 게임 분모/완료율이 아니다. 이전 ROM/번역/상태/실행 증거 보존.
새 게임 코드/새 실행 훅 변경 없음.

## 원문과 번역 범위

공용 plug-out archive778338:1810,46스크립트, 원본 catalog pointer06A544.
원본 SHA256 `51f4ec75fbfb4a976ac0a117ef41fdfc73d6eabdbdc7d6f622daba0e97be7e83`.
기존 return-v1 정상 경로 step2/3/4의 RAM script6/6/26을 관측해 롤 소비를 확정했다.
새 읽기 전용 survey는 원본 닉네임과 같은 일반 대사창/선택 UI를 기록했다.
기존 initializer0804F7B6 probe는 이 공용 경로의 호출을 기록하지 않았다.
따라서 해당 호출의 부재를 경로 미실행으로 해석하지 않으며,
context0200FA20의 native root/script와 실제 ROM/RAM stream 소비로 연결을 증명한다.

`translations/roll_plugout_ko.json`4개를 주 에이전트가 문맥에서 직접 작성했다.

- 6:0 — 닉네임 뒤 원본 쉼표 / 플러그아웃할까? / 빈 선택 행
- 6:1 — 예, 원본 뒤 공백2개 유지
- 6:2 — 아니요
- 26:0 — 응! 지금 돌아갈게!

다른 내비/공용 오류/dispatch0/1 등44스크립트 바이트 동일.
checkNaviAll, portrait, printPlayerNickname, msgOpen, positionOptionHorizontal width8,
option 좌우/상하, select default1/clear/targets/취소, keyWait/end 인자 모두 동일.
첫 줄 쉼표와 원문 줄 수 보존; 다른 이름 길이나 한국어 조사 의존성을 추가하지 않는다.
닉네임 첫 줄 변경과 선택용 빈 행 제거는 빌드 전 검사에서 거부한다.
최대 리터럴122px, 질문95px, 보수적 선택행104px, adopted132px/3행 이내.
모든 글리프 공급, native/semantic/binary roundtrip 및 원본 풀 보호 통과.
새1857바이트 풀 ROM offset8441976/root0880D078,
SHA256 `39069f6b0b3cc0af15547ff887f869f549c9ec97ac054dd12c69b15dfe1c3709`.

## 새 ROM 정상 컨트롤러 검증

own cold-chain → Roll 인사/PET → 플러그인 → 인터넷을 새 ROM 자체에서 생성.
이전 ROM의 상태는 부모로 쓰지 않았으며 입력 recipe만 참고했다.
`roll-plugout-v1-choices`15단계:

- step2: R 확인창, 기본 아니요
- step3: A로 아니요, 확인창 닫힘/인터넷 복귀
- step4/5: 다시 R, B 취소/인터넷 복귀
- step6/7/8/9: 재진입 후 기본 아니요→왼쪽 예→오른쪽 아니요→왼쪽 예
- step10: A로 예, native script26 한글 응답
- step11/12: 기존 정상 귀환 첫 페이지
- step13: 기존 정상 귀환 닉네임 페이지
- step14/15: 다음 원본 대사로 진행

선택 커서 x121(아니요)/85(예), y136, tile1020/palette14, 실제 이동 일치.
아니요/B 취소에서 응답26 draw가 추가되지 않았다.
질문/예/아니요/응답4문구 모두 실제 ROM stream→CPU 폰트 읽기→OBJ VRAM→화면 검증.
닉네임 RAM9B9BA2CA/E5와 원본 글리프/advance/쉼표 위치를 별도로 확인한 ‘ああくん’이다.
이름은 사용자 데이터로 변경하지 않았다. 다른 이름·최대 길이 실험은 미완료.
빈 본문 영역 검사로 이전 문구 잔상 없음. step3 인터넷 복귀도 화면을 직접 확인했다.

## 검증 좌표와 네이티브 UI 구분

최초 PET 전용 원점92,110을 적용했을 때 VRAM 검사 실패를 기록했다.
원본 조사와 새 스냅샷의 font OBJ x52,84,116,.../y110 및 문자 stream offset을
대조해 일반 msgOpen 원점52,110을 확정했다. ROM은 변경하지 않았다.
검증기에 원점 인자만 추가하고 기존 PET 기본값92,110은 보존했다.

좌표를 고친 후 색상 불일치는 네이티브 선택 화살표의16x16 OBJ 안에서
글리프 배경 role1에만 발생했다. 기본 아니요 화면에서는 해당 배경90픽셀,
예 선택 화면에서는6픽셀이 화살표 영역과 겹친다.
검증은 이 네이티브 UI 사각형의 화면 배경만 구분해 제외한다.
ROM→VRAM 모든 픽셀과 글자 잉크/그림자는 계속 검사하고,
네이티브 cursor가 잉크를 덮으면 실패하도록 유지한다. 기존 PET 검증 기본 정책은 그대로.
빈 영역 검사도 같은 네이티브 UI 사각형만 제외한다. 검증을 위한 ROM/UI 수정은 없다.
단순한 이전 검사 통과로 원점/커서 조건을 일반화하지 않도록 기록했다.

## 누적 회귀와 남은 작업

같은 새 ROM에서 인사2문구, PET22관측/29선택 단계, 정상 운세23문구와 연출점,
Roll/Rockman 장비 안내·폴더·무기·공격력·숫자·기존 그래픽 회귀 통과.
귀환2정상 페이지와 패배2진단 페이지도 새 ROM에서 다시 검사했다.
패배는 단일 table-read alias1→2만으로 확인했으며 실제 전투 패배 증거가 아니다.
diagnostic_checkpoint.mss/normal_play_checkpoint_eligible=false로 격리했다.

`plugout_runtime.json`, 운세 `runtime.json`, `return_regression/return_runtime.json`은
별도 유지한다. 모음 `plugout_pages.png`의6화면은 모두 정상 플레이 캡처다.
전체 자동 테스트166개 통과(188.154초), 종료 코드0.
명령 `python -X utf8 -m unittest discover -s tools -p 'test*.py' --buffer`.
결과는 `analysis/roll_plugout_v1/test_summary.txt` 참조.
다른44스크립트의 실제 내비별 소비, 귀환 후 날짜별 후속 대사, 전체 미번역,
인간 문구/시각 승인, 실기/오디오/배포 QA는 남았다.
