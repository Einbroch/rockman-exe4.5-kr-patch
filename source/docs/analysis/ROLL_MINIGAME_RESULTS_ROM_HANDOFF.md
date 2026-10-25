# 롤 미니게임 결과 — 8문구 추가

2026-10-03. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 완역·배포·실기·오디오 검증이 아니다.
한글패치 스킬의 원본 보존, 재현 빌드 및 정상 실행/진단 증거 분리 기준을 적용했다.

## 누적 개발 ROM

`poc/output/exe45_ko_development_roll_minigame_v1.gba`
SHA256 `2da26c3add35aa3a4bcb59094c58c69ed11febe28646e90036df47bbb97d708b`.
원본에서 독립 빌드한 `_repro.gba`, 최종 도구의 `_current_repro.gba` 모두 바이트 동일.
`_current_repro.json`의 build_tools_sha256은 현재 모든 tools/*.py와 일치한다.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 변경 없음.
원본/이전 ROM/실패 진단/기존 번역 입력을 보존했다. 누적938텍스트 단위와 기존9그래픽은
전체 게임 분모나 완료율이 아니다.

## 번역과 보호

`translations/roll_minigame_results_ko.json`은 이전 운세80개 ID/원문/문구/상태를 유지하고
미니게임50:0,51:0/1,60:0/1/2,61:0/1의8문구만 추가한88개 입력이다.
registry variant `fortune-and-minigame-static-results-v1`, 별도 builder 옵션
`--roll-minigame-results`로만 선택한다. 이전 옵션/기본 입력은 바꾸지 않았다.
주 에이전트가 원문 문맥에 따라 직접 작성한 needs_review 초안이며,
계산 실력·얼음에 방심·재도전·성장 표현을 보존했다. 새 보상 약속을 추가하지 않았다.

65FF3C의 전체109리터럴은 선택88개 + 원문 유지 연출 점6개 + 미번역15개로 나뉜다.
15개는 합성 페이지 행동을 더 확인해야 하는23:0 및 숫자/보상 변수가 섞이는
52/53/62/63의14문구다. 이 분모는 해당 대사 풀만 해당한다.
모든 명령/인자, minigame0/1 기록 호출, global5 결과 분기, item33 지급,
flag3585, keyWait/clearMsg/waitHold와 원문 줄 수를 유지한다.
미선택40스크립트는 바이트 동일하고, 이전 소개의 점6개/대기 연출도 보존한다.
88개 전체 글리프·인코딩·폭·행·구조·의미/바이너리 roundtrip 검사 통과.
최대132px/3행, 새8개 최대127px이며 자동 생략/허용 폭 증가를 하지 않았다.
재배치 풀5935바이트 SHA256
`61be5c4be86fa1f6dadba33a347457cbf225b3636827b0ef4e67dd82265d3343`.
원본 대사 저장 범위 보존,380E0 포인터로 새 풀 선택. 새 게임 코드 훅은 없다.

## 정상 실행과 진단을 분리한 검증

새 ROM의 자체 cold boot→날짜/프로필→롤 설치→인사→운세→PET/장비 경로 및
록맨 자체 cold boot→폴더→장비/가이드→무기 전환을 실행했다.
이전 ROM의 버튼 레시피만 재사용했으며, 정상 경로의 상태 파일은 모두 새 ROM에서 생성했다.
정상 운세23개(소개5, 블루4, 레드5, 오렌지4, 비리디언4, 숫자 힌트1)의
전체 스트림·폰트 CPU 읽기→ROM 글리프→OBJ VRAM→스크린샷 픽셀과 잔상 제거를 확인했다.
정상 운세 보고서의 미관측 집합65개에는 아래 진단4개도 포함된다.
정상 플레이를 통해 미니게임 결과에 도달한 것으로 계산하지 않는다.

새8개 중 실패50:0 및60:0/1/2의4개는 별도 격리 진단에서 실제 에뮬레이터 출력 검증 통과.
기존 네이티브 초기화0804F7B6/0804FB4C..4FC20 바이트를 원본과 비교하고,
0804FB76의 스크립트0 테이블 오프셋 읽기만 최초1회50/60 오프셋으로 반환했다.
네이티브 호출 문맥0200FA20에서 기존 엔진의 결과 기록/분기 및 그리기를 사용한다.
관찰 도구가 ROM/게임RAM을 직접 쓰지 않지만, 게임의 원래 명령에 따른 상태 변경은 발생할 수 있다.
미니게임을 실제 수행하거나 승패·보상을 검증한 것이 아니다.
진단 checkpoint는 `diagnostic_checkpoint.mss`로 격리하고
normal_play_checkpoint_eligible=false로 기록해 정상 진행 부모로 쓰지 않는다.

첫 진단은 도구가 문맥 주소를0202FA20으로 잘못 가정해 실패 처리했다.
실제 draw/context 및 테이블 읽기가0200FA20임을 확인한 뒤 도구를 수정했다.
실패 영수증/상태는 고치지 않고 보존했으며, 새 diagnostic-v2-50/60 경로에서 재검증했다.
진단 화면4개 모두 전 글리프/폰트 읽기/VRAM/스크린샷 픽셀 일치 및 빈 영역 잔상 검사 통과.
새 성공 결과51/61의4개는 정적 검증만 완료했다.

88개 집합은 정상 관측23 + 진단 렌더 관측4 + 정적 전용61로 구분한다.
세 집합은 서로 겹치지 않는다. 진단 관측을 정상 플레이 완료 범위로 합치지 않는다.
`analysis/roll_minigame_v1/runtime.json`과 `minigame_runtime.json`은 동일 ROM SHA에 묶인다.
화면: `fortune_pages.png`, `diagnostic_minigame_pages.png`.
스크린샷 모음은 해당 ROM의 실제 실행 캡처이며 합성 글꼴 예시가 아니다.
기존 인사/PET/롤 장비 회귀 보고서는 같은 폴더의 greeting_regression,pet_regression,
roll_caption에 저장했다. ‘통신’ 이미지 및 기존 그래픽9개는 유지한다.
록맨 최종 회귀도 통과했으며 rockman_regression에 기록했다.
전체 단위 테스트146개를199.229초에 실행해 OK를 확인했다.
추가3테스트는88선택/이전80개 불변/미선택40개/보호 명령 및 원문,
진단 격리와23+4+61분할, 동일 ROM 인사/PET/폴더/무기/장비 회귀를 검사한다.

## 재현 및 다음 미번역

```powershell
python -X utf8 tools/build_roll_pet.py --roll-intro --roll-minigame-results --work NEW_WORK --out NEW_OUTPUT.gba
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

정상 매트릭스/샘플 도구의 STEM/PREFIX를 새 ROM/새 경로로 지정한다.
run_roll_fortune_samples.main(outdir)도 새 증거 폴더를 지정해 이전 보고서를 덮어쓰지 않는다.
diagnostic 캡처 도구와 보고서의 선택/분모는 위 파일들에 명시했다.
다음 우선순위: printBuffer3의 실제 숫자 폭·보상 상한·합성 행을 조사한 뒤
52/53/62/63의14개 번역, hint23의 clear/합성 행동 확인, 실제 미니게임 경로 확보.
성공/실패 정상 획득·보상·저장·통신 실사용, 인간 의미/시각 승인,
전체 게임/이미지 인벤토리 및 실기·오디오·배포 검증은 계속 미완료다.
