# 롤 첫 만남·재회 — 5문구 개발 반영

2026-10-03. development-draft; NON-DISTRIBUTION. 문구·시각 needs_review.
release_eligible=false. 완역/배포/인간 승인/하드웨어/오디오 검증 주장이 아니다.

## 결과 및 보호 범위

`poc/output/exe45_ko_development_roll_intro_v1.gba`
SHA256 `acf1de2629ddfe529d94da519bce3efe34bb126f700f071639266266bd5e746c`.
불변 원본에서 `_repro.gba` 재빌드 일치. `_current_repro.gba`와 해당 메타데이터는
최종 도구로 같은 바이트가 재현되는지 별도로 확인한다.
누적850텍스트 단위(이번5), 그래픽9개 유지. 전체 게임 분모가 아니다.

입력 `translations/roll_intro_ko.json` / source65F9AC170바이트
SHA256 `cf0dc0132e19674a77a4db380bc042e187e4d3925638dd31c3c1a6489668ba47`.
원본표380D4의 롤 인사 풀을 재배치한다. 원본170바이트는 그대로 보존하며,
새 게임 코드 훅/램 버퍼 확대/진행 플래그/세이브 조작은 추가하지 않았다.
4스크립트 중1/2의5문자열을 선택하고 빈0/3을 원형 보존했다.
모든 flag3585·윈도·글자 위치·속도·keyWait·clearMsg·waitHold·줄/페이지 순서 유지.
문자/명령 재추출·의미/바이너리 roundtrip을 제품 빌드에서 검사했다.

| ID | 원문 | 개발 초안 |
|---|---|---|
| 65F9AC:1:0 | ハイ! / はじめまして!! | 안녕! / 처음 만나 반가워!! |
| 65F9AC:1:1 | わたし ロール! / なかよくしてね!! | 난 롤이야! / 친하게 지내자!! |
| 65F9AC:2:0 | もー! | 정말! |
| 65F9AC:2:1 | わたしを ほったらかして / ほかのナビと / なかよくしてたんでしょ! | 날 내버려 두고 / 다른 내비랑 / 친하게 지냈지! |
| 65F9AC:2:2 | まえより だいじに / してくれないと、 / おこっちゃうんだから! | 전보다 더 아껴 / 주지 않으면, / 화낼 거니까! |

`/`는 원래 줄바꿈이다. script2에 원문에 없는 연애 관계나 부재 기간 조건을
추정하지 않았다. 실제 재회 분기 선택 조건/획득/진입은 아직 미검증이며,
말투·표현은 인간 승인을 받지 않은 초안이다.

## 실제 화면 증거

새 ROM의 cold boot→프로필 입력→정상 Navi Select에서 Roll 선택→설치→롤 인사.
이전 ROM 상태를 가져오지 않고 동일 ROM의 자체 체크포인트만 사용했다.
`poc/runtime/roll-intro-v1-roll-select-roll/step_006.png` / `step_007.png`가
첫 만남 두 페이지다. 비교 `analysis/roll_intro_v1/first_meeting.png`.

- 최초 native normal entry에서 새 ROM root/script1이 선택되고 읽힌다.
- 첫 만남2문구 전체 스트림·공급 글꼴·CPU 읽기→OBJ VRAM→화면 픽셀 일치.
  5문구 전체 한글 BDF·native 문자/구두점 글꼴 및 범위는 정적 검증.
  채택한132px/3행 범위에서 실제 최대122px.
- 두 번째 페이지의 줄 끝은 첫 페이지보다 짧다. 빈 본문 영역
  x202..233/y124..135가 창 배경과 같아 이전 글자 잔상이 없다.
  초기 검사에서 x234의 원래 녹색 창 테두리를 배경으로 포함한 오류를
  확인하고 검증 범위만 바로잡았다. ROM을 바꾸거나 글자 잘림을 숨기지 않았다.
- step8은 원래 후속 풀0865FF3C로 넘어가며, 이전 인사 호출/그리기가 추가되지 않는다.
  이 날짜별 후속 대사는 아직 일본어로 남아 있다.
- 같은 ROM의 기존 PET22문구/29선택 단계, 롤/록맨 장비·폴더·무기 이름,
  공격력 이미지의 native BIOS 해제/상주/VRAM/OBJ/픽셀과 숫자 보존,
  PET7이미지(`통신`) 회귀를 각각 검사한다.

보고서 `analysis/roll_intro_v1/runtime.json`, `pet_regression/runtime.json`,
`rockman_regression/runtime.json`, `roll_caption/runtime.json`.
정상 실행 결과는 ROM/에뮬레이터/각 파일/자기 체크포인트 재귀 해시와 묶인다.
첫 만남2개와 재회3개의 정적/실행 범위를 분리한다.
자동 테스트134개를41.059초에 실행해 OK를 확인했다.
현재 도구로 만든 `_current_repro.gba`도 같은 SHA256이며 메타데이터의
모든 도구 파일 해시가 현재 소스와 일치한다. 원본 ROM 해시도 변경되지 않았다.

## 재현

```powershell
python -X utf8 tools/build_roll_pet.py --roll-intro --work NEW_WORK --out NEW_OUTPUT.gba
python -X utf8 tools/run_roll_equipment_guides_matrix.py --stem exe45_ko_development_roll_intro_v1 --prefix NEW_PREFIX-roll- --pet-probe --intro-probe
python -X utf8 tools/report_roll_intro.py
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

work/output/접두사는 새 경로만 쓴다. 기본 report는 현재 확정 접두사를 사용하므로
다른 실행은 main(stem,prefix,outdir)에 그 실행 경로를 넣어야 한다.
PET/장비 회귀는 자기 ROM의 기존 입력 레시피를 다시 실행하며 source ROM으로 재빌드한다.

## 남은 작업

재회3문구 실제 진입/표시, 기존 롤 PET 재진입/저장 질문/말 끊기22문구의 실행,
날짜별 롤 대사·다른 내비/전체 게임 미번역·전체 분모·진행·세이브/통신·
하드웨어/오디오·인간 문구/시각/배포 승인은 열려 있다. 원본/이전 결과는 보존한다.
