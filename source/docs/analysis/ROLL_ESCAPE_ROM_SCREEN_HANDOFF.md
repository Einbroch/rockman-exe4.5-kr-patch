# 2026-10-03 — 롤 도주 미번역 6개 ROM 반영 및 화면 검증

최신 누적 개발 ROM: `poc/output/exe45_ko_development_roll_escape_v1.gba`.
독립 재빌드: `poc/output/exe45_ko_development_roll_escape_v1_repro.gba`.
동일 SHA256: `9762ba24860844b6bb4e5220a05fb7c0973bf9a4c9cdba456c96e16ea19b4096`.
누적 선택 단위756 = 이전750 + 롤 도주 literal6. 전 게임 번역률/서로 다른 문구 수가 아니다.
원본 ROM·이전 개발 ROM·세이브·이전 증거는 보존했다. NON-DISTRIBUTION, 새 번역 needs_review, 인간 표현 승인은 미완료다.

## 번역·보호·빌드

76C944의 롤 확인 질문/예/아니요/결과/실패/도주 불가 scripts8..11의6개 literal을 직접 번역했다. source9의「にげきれそう」는 ‘도망칠 수 있겠어’로, 이미 도망쳤다는 록맨3의「にげきれた」와 구분했다. seed `translations/roll_escape_draft_seed.json`, 검토 자료 `translations/ROLL_ESCAPE_REVIEW.md`.
`prepare_roll_escape.py`가 원본 해시·4473바이트 풀·TPL·각 script raw bytes·기존8개 문구·seed/tool 해시를 연결해 `translations/rockman_roll_escape_ko.json`을 직렬화한다. 의미를 자동 치환하지 않았다.

새 registry variant는 기존 록맨0/1의 mono5x2와 일반 대사2..5/8..11을 분리한다. 롤6/7 전술 질문은 원문 그대로, 다른134스크립트와 선택 script의 비선택 점12개는 보존했다. 초상·18프레임 대기·줄바꿈·옵션 패딩/선택·취소·분기 제어 구조도 그대로다. 7개 아카이브 선택/다른725개, 원본 헤더/원본 풀, 무변경 원본 왕복·번역 제어 구조·바이너리 왕복·최종 변경 영역 감사 통과.

첫 `poc/build_roll_escape_v1`은 롤 질문156px가 기존144px 개발 범위를 넘어서 실패했다. 출력 ROM은 생성되지 않았고 실패 work/log는 보존했다. 문구를 줄이지 않고 script8만168px 개발 범위로 등록, 나머지 일반 대사는144px 유지했다. r2에서 빌드했고 실제 글리프의 끝/행/창 경계 x52..236를 검사했다. 이는 국소 개발 설계이며 모든 창의 실제 최대폭/인간 표현 승인으로 취급하지 않는다. 새 literal 검사 폭은156,28,36,23/143,43/132,120/47px다.

## 새 ROM의 실행·픽셀·복귀 검증

`tools/run_roll_escape_matrix.py`는 이전 receipt의 controller action 문자열만 재생한다. 새 ROM에서 cold13 → 초기40 → network43 → battle104동작으로 새 정상 checkpoint chain을 생성했다. 이전 ROM의 SAV/checkpoint는 가져오지 않았다. 같은 해시로 고정된 격리 Mesen/BIOS에서 음소거 실행했으며 오디오 검증은 아니다. 모든 관측 route에서 자기 ROM stem의 native SAV/RTC 갱신 외 다른 세이브 파일의 해시는 보존됐다.

- `roll-escape-v1-l-target`/`forbidden-clear`: 정상 입력으로 록맨 도주 불가 script5와 A 닫힘. 롤 플레이 증거로 사용하지 않는다.
- 기존 록맨 `confirm-sample`/`success-sample`/`failure-sample`을 새 ROM에서도 재실행했다.
- 새 `roll-confirm-sample`/`roll-success-sample`/`roll-failure-sample`/`roll-forbidden-sample`: native0804FB76에서 script5 table-offset 읽기 한 번을 새 ROM의 실제8/9/10/11 오프셋으로 반환하는 진단. ROM·텍스트·진행 플래그·save RAM은 쓰지 않았다. 정상 checkpoint는 diagnostic_checkpoint.mss로 격리한다. 실제 롤 선택/도주 성공·실패 판정은 증명하지 않는다.
- 일반 대사22개 held 화면(롤11, 록맨11): 실제 renderer stream/glyph index/좌표·폰트 읽기·ROM/BDF 및 쉼표의 기존 vertical-shift 공급·한글/원본 문장부호 픽셀을 검사했다. 롤 초상, 긴 질문 경계와 결과/불가 대사의 가독성도 실제 스크린샷으로 확인했다.
- 확인창의 좌우 포커스/OAM 위치·형식과 ‘아니요’ 선택 후 닫힘 검사. 기존 native cursor snapshot tile과 scanout의 불일치는 그대로 미검증이다. cursor의 공간 패딩 overlay만 분리하고 모든 문자 ink/shadow를 검사했다. cursor bitmap 정밀검증/예 선택/B 취소 완료를 주장하지 않는다.
- 닫힘·복귀16화면: normal dialogue context 비활성, native target 선택, 해당 ROM에서 픽셀 검증한 target의 VRAM640바이트 및 visible40x32 동일성. 일부 복귀는 cached prompt를 재사용하므로 새 parser call을 강요하지 않고 현재 resident bytes/픽셀을 확인했다.
- `folder-regression`: 정상16동작/4화면의 캐논·에어슛·발칸1 이름/설명, actual copy/cache/ABI·stage·VRAM·OBJ·픽셀 검사.
- `tactics-regression-r2`: 정상7동작/4화면, 록맨 두 질문 mono5x2/640바이트·upload·BG3/10셀/픽셀 검사. `exe45_roll_tactics_target_v1.json`, `exe45_roll_tactics_distance_v1.json`.

통합 근거 `analysis/exe45_roll_escape_runtime_v1.json`. 자동 테스트94개 통과. 독립 재빌드의 ROM 바이트 해시도 동일하다.

## 실패한 비교와 구분한 한계

최초 새 verifier는 기존 전체 배경색 마스크 비교에서 롤 확인창 닫힘 step8을 실패시켰다. step7은 baseline69픽셀과 정확히 같고, step8은199픽셀이었다. 차이130은 x159..189/y110..118에만 있었다.
원래69픽셀은 메톨에 붙은 HP 라벨 OBJ7/palette14였다. 추가130은 실제 앞쪽 비투명 메톨 OBJ14의125픽셀+OBJ16의5픽셀, palette1/raw67FF 타일 마스크에 모두 대응한다. 같은 화면에서 대사 ROI 위쪽 y95..109의 별도65 native body 픽셀로 RGB를 교차 확인했다. 본문 글자를 제외하지 않았으며 sprite mask 밖의 배경 마스크는 baseline과 같다. `verify_roll_dialogue_clear.py`가 이 한 화면의 차이를 분류하고, report는 전체 마스크 일치=false 및 delta를 명시한다. 전체 움직이는 전투 화면의 동일성이나 독립적인 LCD 색 변환 검증은 아니다.
검사 준비 중 기존 verifier의 쉼표가 native1-byte라고 가정한 KeyError도 발생했다. 기존 확장 쉼표 인덱스/shift를 읽도록 새 bound verifier를 수정했으며 ROM이나 번역을 바꾸지 않았다. 검사 실패를 PASS로 저장하지 않았다.

## 재현

이미 있는 work/output/route/report를 덮어쓰지 않는다. 재실행은 새 이름으로 같은 입력/옵션을 지정한다.

```powershell
python -X utf8 tools/build_development_patch.py --translations translations/megaman_intro_ko.json --translations translations/megaman_pet_menu_ko.json --translations translations/megaman_save_ko.json --translations translations/library_headers_ko.json --translations translations/chip_descriptions_batch09_ko.json --translations translations/chip_secondary_descriptions_ko.json --translations translations/rockman_roll_escape_ko.json --chip-library --chip-word-copy --chip-cache --chip-burst-copy --chip-library-late-wait --chip-folder --chip-folder-owner-guard --mono-font-poc --chip-battle-names --chip-name-translations translations/library_chip_names_batch08_ko.json --chip-secondary-name-translations translations/chip_secondary_names_ko.json --work poc/build_roll_escape_next --out poc/output/exe45_ko_development_roll_escape_next.gba
python -X utf8 tools/report_roll_escape_runtime.py
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

## 다음 남은 작업

롤의 mono 전술 질문6/7, 다른 내비 대사와 나머지 UI/대사/그래픽 미번역이 남는다. 실제 롤 선택 및 도주 가능 전투의 확인/성공/실패 경로, 예/B 취소, 재진입/확률/후속 진행은 미검증이다. 새 ROM의 추가 칩·도감·배틀 이름·save commit/reboot/lifetime/timing 결과는 이전 ROM에서 자동 상속하지 않는다. 인간 의미/표현 검토, cursor bitmap scanout, 전체 플레이·오디오·실기·배포 QA도 미완료다.
