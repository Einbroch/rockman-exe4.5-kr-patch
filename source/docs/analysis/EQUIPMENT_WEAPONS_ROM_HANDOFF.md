# 공통 장비 무기 이름33개 추가

development-draft; NON-DISTRIBUTION. 전체 번역·배포 완료 아님.
문구/고유명사는 needs_review이며 공식 한국어 명칭 승인 주장 없음.

## 결과 및 고정 아티팩트

- 현재 ROM `poc/output/exe45_ko_development_equipment_weapons_v1.gba`
- SHA256 `d0cd5c4f7f65d73a3974deec567a4896edeeed930da3f29300e3eb634e4581c4`
- 독립 재빌드 `poc/output/exe45_ko_development_equipment_weapons_v1_repro.gba` 동일.
- 최종 코드 재빌드 `poc/output/exe45_ko_development_equipment_weapons_v1_current_repro.gba` 동일.
- 누적 텍스트765→798. 추가33개 이름이며 전체 게임 완료 분모 아님.
- 전체 자동 테스트115개 통과 (115 tests, 32.328s, OK).
- `translations/equipment_weapons_ko.json`: 원문/33개 번역/안정 ID/검토 상태.
- `analysis/equipment_weapons_v1/runtime.json`:33개 정적 검증과 실제 무기 변경 증거.
- `analysis/equipment_weapons_v1/weapon_cycle.png`: 실드→차지 샷→재진입 실제 화면.
- `analysis/equipment_weapons_v1/guides_regression/`: 안내문3개, selector ABI72합성사례,
  장비 기본 화면4개·폴더4개·PET `통신` 포함7개 회귀.

이번 범위는 원본6E2B9C의 standalone/end 무기 이름 script5..37이다.
버스터·배리어·롤 애로·거츠머신건·거츠 해머·롱소드·메탈 블레이드 등이다.
기존 칩 이름과 일치하는 용어는 기존 개발 번역을 이어받았고,
킹덤C·로열WB·슈팅B·D오버로드는 원문 약자를 그대로 유지했다.
소스에서 확인하지 않은 약자 확장/공격 효과 설명을 추가하지 않았다.

## 빌드/소비 경로

`--equipment-weapons`는 `--equipment-labels`를 필요로 한다. 기존4개 문구와
추가33개 자산을 메모리에서 병합해 script1..37의 별도 비압축 ROM 복제를 만든다.
원본 압축 풀634바이트 및 포인터/공유 해제 RAM/Navi별 대사는 수정하지 않는다.
script0 및38..75의39개 스크립트, R/L 접두사 및 원본 무기 선택 테이블을 보존한다.

원본23Navi 풀의 첫60개 스크립트가 동일하고,23개 무기 selector 레코드의
모든 추가 이름이 확인됐다. 기존 장비 고정 이름 소비 함수080D3834/383E는
변경하지 않으며, 루트만 새 common clone을 읽는다. 정상 폰트/한글 고정셀 공급,
문자별64바이트 타일 형식도 기존 경로다. 코드 hook을 새로 추가하지 않았다.

전33개 문자열의 원문/종료E5/번역 인코딩을 바이트 대조했다. 모두 한 줄/9셀
(72픽셀) 이내이며, 모든 한글 글리프가 BDF 기반8x16 레코드와 동일하다.
공백과 C/W/B/D 등의 원본 글리프도 보존한다. 미매핑/폭 초과는 빌드에서 실패한다.

## 실제 실행과 검증 범위

`poc/runtime/equipment-weapons-v1-`의 새 cold-part1→cold-part2에서 시작했다.
이전 ROM 저장 상태는 사용하지 않았고 입력 목록만 재사용했다.
folder-regression/equipment/focus의 기본 회귀 이후, 동일 ROM의 equipment
checkpoint에서 weapon-cycle-r3를 정상 컨트롤러 입력으로 실행했다.
RAM/진행도/CPU 조작은 하지 않았다. 저장·통신 연결·오디오 검증은 수행하지 않았다.

Rockman의 R행 무기는 원래 순서가 록 버스터→실드→차지 샷이다.
step3/5/6/7/8/9/10/13/14/15에서 무기 root/script/첫 포인터,
실제 glyph stream/공급 font/인덱스,9셀576바이트 stage→VRAM→9개 OBJ,
글자 ink/shadow 전 픽셀을 대조했다. 단어 뒤 OBJ 타일은 모두0으로 지워진다.
선택한 행은 원래5픽셀 왼쪽으로 이동하고 마지막 clear OBJ에3픽셀 간격이 있다.
짧은 이름의 투명한 공백에는 원래 선택 화살표와 PET 배경이 보이므로 전체 공백
RGB가 단색일 것을 요구하지 않는다. 실제 그리기 타일의0과 글자/그림자를 구분한다.

처음 weapon-cycle 입력은 상태 로드 직후 첫 입력이 안 먹어 목표에 도달하지 못했다.
r2는 R행에서 한 번만 오른쪽을 눌러 실드까지만 관찰했다.
두 기록을 보존하고 최종 검증에는 사용하지 않았다. r3는 시작60프레임 무입력,
R행에서 두 번 오른쪽을 눌러 차지 샷까지 이동한다. ROM 수정 없이 입력만 교정했다.

33개의 이름은 동일 선택/공급 경로라는 정적 증거로 묶여 있지만 이번 새 이름의
실제 플레이 샘플은 차지 샷 하나다. 다른 Navi 선택/길이가 긴 이름의 실제 화면은
아직 미검증이며, 전체 Navi 플레이·모든 무기 동작 검증으로 확대 주장하지 않는다.

## 남은 작업 및 재현

공격력 OBJ `バスター攻撃力`는 아직 일본어다. 원본 공급/변환 경로 조사가 필요하다.
다른 Navi별 장비 안내문과 전체 게임 미번역도 남아 있다.
문구/미감 승인, 전체 플레이, 기기·오디오, 배포 QA 미완료.
원본 및 이전 ROM/실패 입력 캡처는 변경하거나 삭제하지 않았다.

이전 guide ROM 빌드 인자에 `--equipment-weapons`를 더하고 새 work/out을 지정한다.
`python -X utf8 tools/run_equipment_weapons_matrix.py`는 새 런타임 루트가 필요하다.
`python -X utf8 tools/report_equipment_weapons_runtime.py`로 기존 증거를 재검사한다.
`python -X utf8 -m unittest discover -s tools -p 'test_*.py'`로 자동 검사를 실행한다.
