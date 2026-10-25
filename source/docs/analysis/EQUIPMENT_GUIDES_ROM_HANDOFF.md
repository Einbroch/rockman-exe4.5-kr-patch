# 장비 안내문 3개 추가 한글화

development-draft; NON-DISTRIBUTION. 문구 상태는 needs_review이며 배포 승인 아님.

이번 문구는 칩 폴더 편집 안내 `칩 폴더를\n편집할게!`, R/L 버튼 지정 안내
`R 버튼에 지정할\n무기를 골라 줘!`, `L 버튼에 지정할\n무기를 골라 줘!`다.
기존762텍스트 단위에서765로 증가했으며 게임 전체 완료 분모가 아니다.

## ROM과 증거

- `poc/output/exe45_ko_development_equipment_guides_v1.gba`
- SHA256 `79ed6e9022dbece072a015d93a296a82254159f486f4c0af7db59a587b8e68b6`
- 독립 재빌드 `poc/output/exe45_ko_development_equipment_guides_v1_repro.gba` 바이트 동일.
- 전체 자동 테스트112개 통과 (112 tests, 31.188s, OK).
- `analysis/equipment_guides_v1/runtime.json`: 실제 ROM 글자 픽셀과 ABI 검사.
- `analysis/equipment_guides_v1/three_guides.png`: 실제 선택3개 화면.
- `analysis/equipment_guides_v1/labels_regression/runtime.json`: 기존 폴더/장비/PET 회귀.
- `analysis/equipment_guides_v1/bench.json`: 최종 Thumb 바이트 합성 CPU72사례.
- 런타임 `poc/runtime/equipment-guides-v1-` cold-part1/cold-part2/folder-regression/equipment/focus.

이 ROM을 처음부터 부팅한 cold-chain만 사용했다. 이전 ROM에서는 입력 목록만
참고했으며 저장 상태는 옮기지 않았다. equipment step007/009/011의 선택3개,
step012의 PET 복귀, step015의 재진입을 확인했다. 나가기 후에는 장비 안내 대신
PET script1의 “자, 뭘 할까?”가 활성화되므로 일반 대사 활성 플래그0을 요구하면
오탐이다. 원본 초기화 명령을 확인하고 대사 root/script/시작 및 현재 포인터가
PET 65A608 script1로 교체됐으며 장비 호출/그리기가 추가되지 않았음을 검사했다.

## 원본 보호 및 소비 경로

원본6E1068 압축625바이트, 해제840바이트/76스크립트를 대조했다.
원본 SHA256 `4c347fde56d3827a7bbcdf5631acb2ceae79d09714f32239f4765928fc55602c`.
별도 비압축 ROM 복제의 script60/61/62만 번역했고73개 나머지 스크립트를 보존했다.
좌표/속도/waitHold/2줄 등 제어 명령·인자도 유지했다. 원본 압축 풀/23Navi 로더
포인터/공유 RAM은 그대로다. 복제를 RAM에 추가 해제하지 않는다.

장비 안내 helper0803C478의 첫12바이트에 Thumb-1 분기를 설치했다.
원래 push{lr}/r1=selection+60 및 정상 대사 진입0804F7B6,
원래 반환0803C484와 root 리터럴3C488은 유지한다. r3 분기 스크래치를 복원하고
r2..r11/SP/caller LR을 보존한다. 원본 Navi 쿼리08000CEC와 테이블을 대조해
Navi0/13/14만 새 복제로, 나머지는 원래0202BA7C RAM 대사로 연결한다.
동일 ROM 실측4호출에서 native call의 r2..r11/stack, 정상 반환 r4..r11/stack을
확인했다. 23Navi+255 ×3선택72 CPU 사례는 스택 복원/분기/레지스터 검사이며,
일반 대사 함수를 실행하지 않는 합성 시험이다. GBA 플레이/타이밍 증거와 구분한다.

한글은 기존 정상 대사12x12 BDF 글리프를 사용하고, R/L/공백/문장부호의 원본
폰트 레코드는 유지한다. 폭 최대99픽셀로 허용132픽셀 이내다.
실제 glyph stream/인덱스/폰트 읽기와 OBJ 좌표, 원본 팔레트 역할1/2/3,
각 글자의 전 픽셀 ROM→VRAM→스크린샷 일치를 검사했다.

## 회귀와 남은 범위

칩 폴더 입력/스크롤4캡처와 캐시/word copy/ABI, 장비3선택 및 재진입의
제목 잔상 제거/무기 이름, PET 선택7개의 `통신` 포함 마스크를 모두 확인했다.
통신 연결이나 실제 저장은 수행하지 않았다. 원본 및 이전 ROM/검증 기록은 보존한다.

`バスター攻撃力` OBJ 표기, 다른 무기 이름, 나머지 Navi별 대사에는 일본어가 남는다.
공격력 표기는 VRAM06013C00..06013F00에서 관찰했지만 원본 raw 연속 블록과
일치하지 않아 원본 공급/변환 경로부터 조사해야 한다.
Navi13/14는 동일 원문 풀과 합성 CPU 선택까지만 확인됐고 실제 플레이 미검증이다.
전체 플레이/기기/오디오/문구·미감 승인/배포 QA는 미완료다.

재현: 이전 장비 빌드 인자에 `--equipment-guides` 추가, 새 work/out 사용.
새 런타임 루트가 필요하며 기존 route를 덮어쓰지 않는다.
`python -X utf8 tools/report_equipment_guides_runtime.py`로 기록을 재검사한다.
`python -X utf8 -m unittest discover -s tools -p 'test_*.py'`로 자동 검사를 실행한다.
