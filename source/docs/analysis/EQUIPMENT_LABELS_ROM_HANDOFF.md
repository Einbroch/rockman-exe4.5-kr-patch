# 장비 선택 항목 추가 한글화

현재 결과는 development-draft; NON-DISTRIBUTION이다. 이번 추가 범위는 장비
화면의 고정 선택 항목 3개이며, 의미/미감 검토 상태는 needs_review다.

| 원문 | 개발 번역 |
|---|---|
| チップフォルダ (선택 항목의 원본 앞뒤 공백 보존) | 칩 폴더 |
| ロックバスター | 록 버스터 |
| シールド | 실드 |

이전 폴더 제목의 `칩 폴더`와 상단 이미지 `장비`, PET `통신` 교정 및 기존 번역을
그대로 유지했다. 누적 텍스트 단위는 759→762다. 전체 번역 완료 수치가 아니다.

## 현재 ROM 및 증거

- `poc/output/exe45_ko_development_equipment_labels_v2.gba`
- SHA256 `2c25fa199817caa94765e7f5c5d94370cd54f477f72dbf6d5fbb46a534faa0ea`
- 독립 재빌드 `poc/output/exe45_ko_development_equipment_labels_v2_repro.gba`와 동일.
- 최종 검증 코드의 추가 독립 재빌드
  `poc/output/exe45_ko_development_equipment_labels_v2_current_repro.gba`도 바이트 동일.
- 전체 자동 테스트108개 통과 (108 tests, 29.965s, OK).
- `analysis/equipment_labels_v2/runtime.json`: exact-ROM 검증 결과.
- `analysis/equipment_labels_v2/before_after.png`: 왼쪽 이전, 오른쪽 수정본.
- `poc/runtime/equipment-labels-v2-equipment/step_007.png`, 009/011: 3개 선택 상태.
- 같은 루트 step012 나가기, step015 재진입. 처음부터 부팅한 동일 ROM
  cold-part1→cold-part2 상태만 사용했으며 다른 ROM 상태를 옮기지 않았다.

## 데이터 및 소비 경로

원본 23개 Navi 압축 풀에서 첫60 스크립트가 바이트 동일하다. 공통 무기 선택
테이블 23레코드(각4바이트)의 모든 인덱스도 이 공통 범위다. ROM 0x6E2B9C의
76스크립트 복제 중 script1 기존 제목 + script2/3/4만 번역했다. 72개 미선택
스크립트와 모든 원본 압축 풀/Navi 포인터/공유 RAM은 보존한다.

독립 고정문구 함수 0x080D37D4, 무기이름 함수 0x080D3834/383E의 루트 리터럴
0xD37FC/0xD387C만 기존 비압축 ROM 복제로 연결했다. 각 리터럴의 주변 Thumb
LDR 참조는 0xD37D8/0xD385E 한 곳씩이며 명령 바이트는 그대로다.
script38/39의 R/L, script63 숫자, 무기 선택 테이블도 원본이다. 내비별 대사
루트 0x3C488/0x3EFC0 및 원본 해제 RAM 0x0202BA7C는 변경하지 않았다.

네이티브 실행은 lr=0x080D37F9/0x080D387B, root=새 ROM 복제, big-font 공급과
script2/3/4/38/39를 확인했다. 숫자 script63은 기존 RAM 루트를 계속 사용한다.
모든 한글·공백·지우기 글리프의 ROM→stage→VRAM 연결과 8x16 OBJ 좌표/팔레트,
3가지 선택 및 재진입 화면의 ink/shadow 전 픽셀을 검증했다.

## 첫 후보에서 찾은 지우기 문제와 수정

첫 후보 `exe45_ko_development_equipment_labels_v1.gba`는 제목 오른쪽에 숫자
잔상이 나타났다. SHA256 `aa4cc6bf6b2572ba88752af629f2ea6beadf541851217956c9eb626a3d255a4f`.
이 ROM과 실행 기록은 보존했으며 현재 사용본이 아니다.

원본 제목 문구는 12셀이고 실제 제목 OBJ도 12개지만, 선언된 width는 10이었다.
원본 일본어는 길이12로 실제 768바이트를 덮어썼다. 짧아진 한글은 width10의
640바이트만 덮어써 마지막2개 OBJ 타일에 초기화 데이터의 숫자가 남았다.
v2는 데이터 테이블 0xD382C의 제목 width 한 바이트만 10→12로 바꿨다.
v1/v2의 나머지 ROM 바이트는 동일하며 명령/무기행 폭3/3/좌표는 그대로다.

이제 네이티브 clear/upload가 12셀/768바이트이며, 마지막2셀의 글리프 데이터는
모두0이다. 네 화면에서 오른쪽 잔상 영역이 왼쪽 공백과 같은 단색 배경이고,
글자/그림자 색이 없음을 검사했다. 선택 강조 팔레트의 시간별 밝기 변화 때문에
서로 다른 실행의 전체 RGB 동일성을 요구하지 않고 동일 화면 배경을 대조한다.

## 회귀 및 남은 작업

기존 폴더 입력/스크롤 4캡처, 캐시 checks13107/hits13090/reset1,
실제 word copy17 및 ABI 검사, 한글 제목 BG 타일맵/픽셀을 통과했다.
PET 선택7개 전체 글자 마스크도 통과했고 `통신`은 유지된다.
통신 연결/실제 저장은 하지 않았다. 원본 ROM과 이전 개발본은 변경하지 않았다.

아직 장비 아래 안내문(현재 Navi Rockman의 원본 풀0x6E1068 script60..62),
`バスター攻撃力` OBJ 표기와 다른 무기 이름에 일본어가 남는다.
안내문은 23개 Navi별 문구가 다른 경로라 공통 이름 복제를 대사에 연결하면 안 된다.
공격력 OBJ는 현재 VRAM0x06013C00..0x06013F00(768바이트)에서 관찰했지만
원본 ROM의 같은 크기 raw 연속 블록으로 발견되지 않았다. 원본 공급/변환 경로
조사부터 이어가야 한다. 이 범위를 완료 또는 제외로 간주하지 않는다.
전체 플레이/다른 Navi 선택/기기/오디오/문구 승인/배포 QA도 미완료다.

재현: 이전 폴더 빌드 인자에 `--equipment-labels` 추가, 새 work/out 사용.
`tools/run_equipment_labels_matrix.py`는 새 출력 경로만 허용한다.
`python -X utf8 tools/report_equipment_labels_runtime.py`로 증거를 다시 검사한다.
`python -X utf8 -m unittest discover -s tools -p 'test_*.py'`로 자동 검사를 실행한다.
