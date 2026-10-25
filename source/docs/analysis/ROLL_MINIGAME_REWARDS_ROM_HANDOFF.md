# 롤 미니게임 보상 — 14문구 추가

2026-10-03. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 완역·배포·실기·오디오 검증이 아니다.
한글패치 스킬 기준에 따라 원본 보존/재현 빌드/숫자 합성 줄 검사 및
정상 실행과 개입 진단의 증거 분리를 적용했다.

## 최신 누적 개발 ROM

`poc/output/exe45_ko_development_roll_rewards_v2.gba`
SHA256 `9b1fd881ab190ef8c396c4733b7e0554c7d0668f3d554d289d0f0961fd198e10`.
불변 원본에서 독립 생성한 `_repro.gba`, 최종 도구의 `_current_repro.gba`도 바이트 동일.
최종 `_current_repro.json`의 build_tools_sha256은 현재 모든 tools/*.py를 포함하며 해시가 일치한다.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 변경 없음.
원본/이전 ROM/이전 번역 입력/이전 실행 증거를 보존했다.
누적952텍스트 단위와 기존 그래픽9개는 전체 게임 분모나 완료율이 아니다.

## 선택 및 보호 범위

`translations/roll_minigame_rewards_ko.json`, registry variant
`fortune-and-minigame-rewards-v2`, builder 선택 `--roll-minigame-rewards`.
이전88개 ID/원문/초안/상태를 그대로 유지하고52/53/62/63의14리터럴을 추가했다.
주 에이전트가 원문 문맥에서 직접 초안을 작성했다. 이전 성공 표현도 동일하게 재사용했다.
드릴은 계산 연습 교재/미니게임의 원어 명칭을 음역한 개발 후보이며,
물리 공구로 확정한 해석이 아니다. 이 명칭/말투 및 전체 초안의 인간 검토는 남아 있다.
숫자 뒤의 ‘제니가’, ‘개’는 숫자 마지막 음절의 받침에 따른 조사 변경을 요구하지 않는다.

65FF3C 전체109리터럴은 선택102 + 원문 유지 점6 + 미번역 지역 안내23:0의1개다.
이 분모는 이 풀만 해당한다. 전체 게임·이미지 번역 완료를 의미하지 않는다.
모든 제어 명령/인자, 난수/플래그, minigame0/1 결과 기록, global5 분기,
item33 지급, EE0E/EE12의FFFFFFFF sentinel, F903의buffer3/minLength0/padZerosfalse 및
각 padLeft 값, keyWait/clearMsg/waitHold, 원문 줄 수를 보존한다.
미선택36스크립트는 바이트 동일하고 기존 점6개/대기 연출도 그대로다.
새 풀6300바이트 SHA256
`c646d4c538026253fc5dd9203ba67404bb70ea3a337cd7b795eef2a8084f555f`.
원본 저장 범위 보존/380E0 포인터 재배치/기존 한글 폰트 경로를 사용했다.
새 게임 코드 훅이나 게임 데이터 내 진단 개입은 없다.

## 숫자 삽입 근거 및 주 빌드 검사

원본의 정상 대사 FC 디스패치08051C54→FC03의08051E5C→
테이블0805258C의slot2E(저장52644)→08036376을 역추적했다.
08036376의 네이티브 보너스 생성 분기는 RNG 결과의 bit1..3으로8개 halfword를 고르고,
bit0 carry로 제니/type2와 버그 조각/type3를 고른다.
363F8의 버퍼 포인터0200FA6C, 테이블 포인터080362C4/080362D4를 확인했다.
원본 함수가 결과 종류를0200FA6C, 수량을+8인0200FA74에 쓴다.

- 제니 테이블:300,500,400,500,300,200,500,800.
- 버그 조각 테이블:3,5,2,1,3,4,4,5.
- TPL buffer3는 문맥0200FA20의+54, 곧0200FA74를 가리킨다.

EE0E/EE12 sentinel 처리08052298/080523A0은 buffer3 값을 읽어 같은 버퍼에 저장하고
네이티브 지급 함수를 호출한다. F903의080516AC는buffer3를 읽고08052150 formatter가
숫자코드digit+1 및E5 종료의 임시 RAM 스트림을 만든다. padLeft/minLength0에 의해
별도 추가 패딩 없이 제니3자리 또는 조각1자리가 한글 리터럴 사이에 표시된다.
숫자0..9의 네이티브 advance는 모두11px다.

`tools/roll_reward_model.py`는 불변 원본 전체 SHA와 이 함수/테이블의 범위 해시 및
포인터/값을 fail-closed로 확인한다. 선언은 조사에서 확인한 고정 카탈로그이며
제품 빌드가 휴리스틱으로 새 주소나 범위를 찾지 않는다.
주 빌드 compile_archive가 이 모델을 소비해 숫자까지 합친 줄 폭을 검사한다.

| 스크립트 | 숫자 폭 | 합성 첫 줄 최대 |
|---|---:|---:|
|52/62 제니|33px|69px|
|53/63 버그 조각|11px|91px|

102개 전체 최대132px/3행, 새14개 정적 리터럴 최대127px.
허용 범위를 늘리거나 자동 줄임/생략하지 않았다. 숫자 합성 폭까지 검사를 통과했다.
이 보상 범위는 네이티브 테이블 생성 경로만 해당하며 모든 printBuffer 사용자나
임의 외부 값, 실제 보상/잔액 정확성에 대한 보장이 아니다.

## 실행 증거

이전 ROM의 입력 레시피만 사용해 새 ROM의 자체 cold boot→날짜/프로필→롤 설치→
인사→운세→PET/장비 및 록맨 자체 cold boot→폴더→장비/가이드→무기 전환을 실행했다.
정상 경로는 새 ROM에서 만든 상태만 부모로 사용하고, 게임RAM/난수/결과를 주입하지 않았다.
정상 운세23개 전체 문자/폰트 읽기/OBJ VRAM/화면 픽셀 및 잔상 제거를 확인했다.
보상14개가 정상 미니게임 완료로 관측됐다는 의미는 아니다.

별도 진단52/53/62/63은 이 새 ROM의 정상 navi-menu 체크포인트에서 시작한다.
검증된 네이티브 초기화의script0 테이블 읽기만50/60 오프셋으로 반환하고,
080509DA의global5 읽기만2/3으로, 지급·출력 함수의buffer3 읽기만 테이블 최대값800/5로
반환한다. PC/문맥/풀 범위를 제한하고 기존 함수 바이트가 원본과 같은지 확인한다.
관찰 도구는 ROM/게임RAM을 직접 쓰지 않으나, 원래 지급 명령이 진단 인벤토리를 변경할 수 있다.
미니게임 플레이·완료·승패 기록·보상 획득 정확성의 증거가 아니다.
진단 상태는 diagnostic_checkpoint.mss로 격리하고 normal_play_checkpoint_eligible=false로 기록한다.

네 경로의14리터럴/12페이지 전부 관측했다. 최대 보상 화면에서formatter의 값/flags/buffer,
RAM 숫자코드와E5 종료, 숫자 CPU 글리프 읽기, 네이티브 숫자/한글 advance,
ROM 글꼴→OBJ VRAM→스크린샷 픽셀 일치와 빈 영역 잔상 제거를 검사했다.
숫자와 분리된 두 리터럴53:2/3 및63:2/3도 실제 동일 페이지로 합성해 검사한다.
화면은 합성 글꼴 프리뷰가 아닌 해당 ROM의 에뮬레이터 캡처다.
`analysis/roll_rewards_v2/diagnostic_reward_pages.png`를 직접 시각 확인했다.

102개는 정상 관측23 + 진단 렌더 관측14 + 정적 전용65로 분리하며 서로 겹치지 않는다.
이전 ROM의 실패 결과 진단을 변경된 ROM의 실제 관측 집합으로 자동 이전하지 않았다.
정상 보고서runtime.json 및 별도reward_runtime.json이 동일 ROM SHA에 묶인다.
정상 화면은fortune_pages.png, 정상 입력 샘플은normal_sample_routes.json에 있다.
기존 인사/PET/‘통신’ 이미지/폴더/록맨·롤 가이드/장비/무기/공격력/숫자 보존 회귀는
greeting_regression,pet_regression,rockman_regression,roll_caption에 기록한다.
전체 자동 테스트150개를175.929초에 실행해 OK를 확인했다.
추가4테스트는102선택/이전88개 불변/원문 점6개 및23보존/36미선택 스크립트,
보상 최대값/숫자 합성 폭/폭 초과 및 원본 불일치 거부,
진단14개 전부의 숫자RAM/폰트/화면 픽셀/격리/23+14+65분할,
동일 ROM의 인사/PET/‘통신’/폴더/장비/무기 회귀를 검사한다.

## 다음 지역 안내 및 미완료 조건

지역 안내23에 clearMsg가 없다는 이유만으로 오류로 확정하지 않았다.
이번 원본 정적 조사에서 EE33 handler08050E38이jump0804FD18로 연결되고,
jump의0804FD4E가0805543C를 호출함을 확인했다.
0805543C는 문맥+70/x,+0F/row를0으로 만들고02012F50의F00바이트와
02013E50의F00바이트를0800092C로0 초기화한다. 즉 네이티브 점프 자체에
대사 스테이징 초기화 경로가 존재한다. 아직23의 해당 실제 화면을 관측한 것은 아니다.
다음에는 행운 아이템 페이지→EE33→23의 실제 호출/초기화/화면을 확인하고 번역한다.

실제 미니게임 정상 완료/보상·기록, 반복 날 운세와 미관측 분기,
전체 게임/이미지 인벤토리, 인간 의미/시각 승인, 실기·오디오·배포 QA는 계속 남아 있다.

## 재현

```powershell
python -X utf8 tools/build_roll_pet.py --roll-intro --roll-minigame-rewards --work NEW_WORK --out NEW_OUTPUT.gba
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

정상 매트릭스와 샘플의 STEM/PREFIX/outdir를 새 ROM/새 경로로 지정한다.
reward 진단은 capture_roll_reward_samples.py --script52/53/62/63으로 실행하고
report_roll_rewards.py로14개 및 숫자/한글 합성 페이지를 검증한다.
기존 builder 선택/번역 입력은 유지하고 새 옵션으로만102개 범위를 선택한다.
