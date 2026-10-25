# 롤 장비 안내문 — 개발 ROM / 실제 화면

2026-10-03. development-draft; NON-DISTRIBUTION. 모든 문구·미감 needs_review,
release_eligible=false. 완역·배포판·하드웨어·오디오 검증 주장이 아니다.

## 결과

`poc/output/exe45_ko_development_roll_equipment_guides_v1.gba`
SHA256 `fafc0a85d217fad5b614fa0b5f6155f195cb6406ded300c10952aac8d56cff2d`.
불변 원본에서 독립 `_repro.gba` 재빌드 일치. 최종 도구로 만든
`_current_repro.gba`도 같은 해시일 때만 현재 구현의 재현 근거로 사용한다.
누적801텍스트 단위(이번 추가3개), 그래픽9개 유지. 전체 게임 분모가 아니다.

| 원문 ID | 원문 | 이번 초안 |
|---|---|---|
| 6E12DC:60:0 | チップフォルダを / へんしゅうするよ! | 칩 폴더를 / 편집할게! |
| 6E12DC:61:0 | Rボタンにわりあてる / ブキをえらんでちょうだい | R 버튼에 지정할 / 무기를 골라 줄래? |
| 6E12DC:62:0 | Lボタンにわりあてる / ブキをえらんでちょうだい | L 버튼에 지정할 / 무기를 골라 줄래? |

`/`는 기존 줄바꿈이다. 롤의 부드러운 요청은 초안이지 인간 승인된 말투가 아니다.
기존 버튼/위치/속도/대기 명령과 인수, 두 행을 그대로 유지했다.
채택한 한 행132px 범위 내 실제 최대111px. 76스크립트 중73개는 바이트 보존.
원본631바이트 압축 풀 및23Navi 로더 테이블 변경 없음.

## 화자 및 경로 근거

원본 테이블3C5BC의 entry1→086E12DC. 같은 풀의 script70..75는
`mugshot=Roll`. 정상 Navi Select에서 `ロール`을 선택하고 실제 롤 초상 PET에
진입했다. 아래 루트는 게임 RAM/진행 플래그/호출 강제 변경 없이 정상 입력만 쓴다.
모든 체크포인트는 이번 동일 ROM의 cold boot에서 파생되며 이전 ROM 상태를 가져오지 않았다.

`roll-equipment-v1-rockman-cold-part1` → `roll-equipment-v1-select-survey`
→ `select-survey2` → `select-survey3` → `select-roll` → `roll-intro`
→ `roll-equipment-v1-roll-equipment` (중간 접두사는 모두 roll-equipment-v1-).

선택 증거: `poc/runtime/roll-equipment-v1-select-roll/step_002.png`와
`step_003.png`. 실제 장비: `poc/runtime/roll-equipment-v1-roll-equipment/step_007.png`,
`009.png`, `011.png`, `012.png`, `015.png`.

## 기술 검증

- helper0803C478만 확장: Navi0/13/14는 기존 록맨 복제 풀, Navi1은 별도 롤
  복제 풀, 나머지는 기존 RAM0202BA7C. 숫자·일반 PET/내비 로더 변경 없음.
- Thumb1 코드 생성/재해석, 최종 설치 바이트·배치 일치.
  23Navi+invalid255 ×3선택=72 Unicorn TI925T 합성 CPU 벡터 통과.
  이는 GBA 실행·타이밍 또는 미실행 내비 정상 플레이 증거가 아니다.
- 실제 Navi1의 [60,61,62,60] 네 호출 모두 새 풀0880B5E0을 소비.
  호출 r2..r11, 반환 r4..r11, 원래 LR/스택 보존.
- 각 번역의 전체 문자 스트림/한글 BDF·영문·공백 원본 글꼴 읽기,
  OBJ VRAM·기하·팔레트 역할과 화면 픽셀 일치. 단순 화면 OCR 판정이 아니다.
- PET 복귀는 native Roll root0865FA58/script1/start0865FA84로 전환되고
  이전 장비 대사 호출/글리프가 추가되지 않는다. 재진입 때 폴더 안내 재표시.
  정상 PET 자체 대사가 활성인 상태를 잘못 잔상으로 간주하지 않는다.
- 롤과 록맨 각각 공격력 이미지의 원래 BIOS 해제1156바이트/상주1152바이트,
  768바이트 caption VRAM·OBJ·픽셀, 숫자192바이트와 겹침 보존 통과.
- 같은 누적 ROM의 록맨 정상 경로에서 공통 무기 이름/폴더/장비 제목,
  안내문·PET7 이미지와 `통신` 회귀 통과.

보고서: `analysis/roll_equipment_guides_v1/roll_runtime/runtime.json`,
`roll_caption/runtime.json`, `rockman_regression/runtime.json`.
자동 테스트126개를68.003초에 실행해 OK를 확인했다. 최신 결과는 아래 명령으로 재현한다.

## 재현

기존 공격력 누적 빌드의 모든 선택을 유지하고 `--roll-equipment-guides` 추가.
`--equipment-guides --equipment-labels --equipment-weapons --equipment-attack-caption`
및 기존 PET/폴더/칩/폰트 선택을 모두 포함해야 한다. 출력·work는 새 경로만 쓴다.

```powershell
python -X utf8 tools/run_roll_equipment_guides_matrix.py --prefix NEW_FRESH_PREFIX-
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

위 실행기는 입력 레시피만 재사용하고 자기 실행에서 새 상태를 만든다.
롤 검증은 `report_equipment_guides_runtime.main(...,roll=True)`;
공격력은 `report_attack_caption_runtime.main(...,roll=True)`를 사용한다.
록맨 전체 회귀는 roll=False/default이며 두 결과를 혼동하지 않는다.

## 남은 작업

롤 첫 인사·PET 메뉴 질문(원본65FA58 등)은 아직 일본어이며 정상 선택 루트에서
실제로 확인했다. 이후 번역 시 해당 풀의 변수 이름/선택/대기/분기 소비 조건을
별도로 분석해야 한다. 남은19개 고유 풀의 장비 안내와 전체 게임 미번역,
모든 내비/진행/세이브·통신·하드웨어·오디오 및 인간 문구/시각 승인은 미완료다.
전체 게임 분모와 완역 비율은 주장하지 않는다. 원본·이전·실패 결과 모두 보존.
