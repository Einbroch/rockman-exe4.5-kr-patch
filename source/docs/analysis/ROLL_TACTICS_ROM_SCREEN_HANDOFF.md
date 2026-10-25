# 2026-10-03 — 롤 전술 질문 2개 ROM 반영 및 화면 검증

최신 누적 개발 ROM: `poc/output/exe45_ko_development_roll_tactics_v1.gba`.
독립 재빌드: `poc/output/exe45_ko_development_roll_tactics_v1_repro.gba`.
동일 SHA256: `1ca65635bcfb92ff3845bf7b75cf6491a045f32cceda5ec16eca977d7d45f31f`.
누적 선택 단위758 = 이전756 + 롤 전술 질문2. 새 문장2종이나 전체 게임 번역률을 뜻하지 않는다. 원본 ROM·이전 ROM·세이브·증거 보존. NON-DISTRIBUTION, 모든 신규 선택 문구 needs_review, 인간 의미/표현 승인은 미완료다.

## 번역 및 보호

76C944:6:0 「どのてきを/ねらうの?」 → ‘어느 적을/노릴까?’ (`tactics.target`).
76C944:7:0 「あいてとの/まあいは?」 → ‘적과의/거리는?’ (`tactics.distance`). /는 기존 줄바꿈이다.
적 목표와 전투 중 상대와의 거리라는 같은 기능, 부드러운 반말 질문의 개발 판단에 따라 기존 문구를 그대로 연결했다. 인간 목소리/의미 승인은 아직 아니다.

`translations/roll_tactics_wording_links.json`은 새 source unit과 기존 wording ID의 명시적 관계/근거만 저장한다. `prepare_roll_tactics.py`가 원본 ROM·4473바이트 풀·각 script raw bytes·TPL·이전14개 번역·기존 문구 asset·selection·tool 해시를 연결해 schema2 `translations/rockman_roll_tactics_escape_ko.json`을 직렬화한다. 기존14개 resolved unit은 그대로이며 새 asset은16units/14wordings다. 검토 자료 `translations/ROLL_TACTICS_REVIEW.md`.

Native group6 helper212C8, Roll portrait8..11 앞의 mono6/7 및20B48의5x2 consumer가 기능/화자 범위 근거다. 두 행/명령/패딩 정책은 유지한다. 폭은40/32px와24/32px로 각각5칸/행에 들어간다. 새 registry variant는 mono0/1/6/7과 일반 대사2..5/8..11의 소비자를 분리한다. 기존 일반 대사 설계144px, Roll8만168px도 그대로다.
다른132스크립트와 비선택 dots12개 보존. 7개 선택 아카이브/다른725개, 원본 헤더/원본 풀, 무변경 원본 왕복·번역 제어 구조·바이너리 왕복·최종 변경 영역 감사 통과.

## 새 ROM의 실제 실행

`run_roll_tactics_matrix.py`: 새 ROM cold13 → 초기40 → network43 → battle104동작의 정상 checkpoint chain을 다시 생성했다. 이전 receipt의 controller action 문자열만 참고했으며 이전 SAV/checkpoint는 가져오지 않았다. 해시로 고정된 격리 Mesen/BIOS, 음소거 실행. 오디오 검증은 아니다. 관측 route의 자기 ROM stem SAV/RTC native 갱신 외 다른 save 파일 해시는 보존됐다.

### 새 롤 질문 — 진단용

`roll-tactics-v1-roll-tactics-sample`: 정상 battle checkpoint에서7동작,4개 held 화면. native554A8 table-offset 읽기에서 PC/r0/LR20B5F/index0·2를 정확히 제한해 실제 컴파일된6/7 오프셋을 반환했다. native 질문1→표시7(offset636,frame83), native0→표시6(offset604,frame236)의 두 read alias 기록. 원본 관련 code bytes를 비교했고 ROM·텍스트·진행 플래그·save RAM은 쓰지 않았다.
**록맨 초상과 플레이어는 그대로다. 롤을 실제 선택한 플레이/롤 초상 화면으로 주장하지 않는다.** checkpoint는 diagnostic_checkpoint.mss로 격리한다. 별도 개입 경계 문서 `analysis/ROLL_TACTICS_LOOKUP_SAMPLE_SCOPE.md`.

각 질문2개 화면에서 정확한6/7 source stream, F9FC glyph/provider index, ROM/BDF font, 10셀/640바이트 stage, VRAM06008A20 upload, BG3의 tile/palette 좌표와40x32 실제 화면 픽셀을 검사했다. 대상 질문에서 거리 질문으로 바뀔 때 빈칸도 전체10셀 기준으로 검사해 이전 글자 잔상이 없는 것을 확인했다. 같은 문구인 정상0/1과 모양이 같아도 offset/stream/units ID로 구분한다.
근거 `exe45_roll_tactics758_sample_target_v1.json`, `exe45_roll_tactics758_sample_distance_v1.json`.

### 기존 소비자 회귀

- 록맨0/1 정상 전술 재열기7동작/4화면: stage/upload/BG3/10셀/픽셀. `exe45_roll_tactics758_target_v1.json`, `exe45_roll_tactics758_distance_v1.json`.
- 기존 도주 대사22 held 화면: 실제 일반 renderer source/glyph/좌표/font reads 및 글리프 픽셀. 정상 도주 불가5와 진단용 록맨2/3/4·롤8..11을 구분했다. 롤의 실제 도주 결과는 아직 아니다.
- 닫힘/복귀16화면: normal dialogue inactive, native target 선택, 이 ROM에서 별도 픽셀 검증한 target VRAM640바이트/visible40x32 일치. cached prompt 재사용을 새 parser call 부재로 오판하지 않는다.
- 정상 폴더16동작/4화면: 캐논·에어슛·발칸1 이름/설명의 actual copy/cache/ABI, stage/VRAM/OBJ/픽셀.

통합 근거 `analysis/exe45_roll_tactics758_runtime_v1.json`. 자동 테스트96개 통과. 독립 재빌드와 원본 SHA도 재확인했다.

## 구분한 관측 차이

이번 ROM은 록맨과 롤 확인창 닫힘 step8 모두 배경색 마스크가 baseline69→199로 변했다. 이전756에서 확인한 한 route만 허용하던 비교는 새 native 록맨 확인창 step8에서 실패했고 PASS를 저장하지 않았다.
같은 새 ROM의 각 화면에서 추가130픽셀은 native 앞쪽 비투명 Metool OBJ14의125픽셀+OBJ16의5픽셀, palette1/raw67FF에 정확히 대응했다. 대사 ROI 위쪽65픽셀로 동일 RGB를 교차 확인했고, 원래 HP-label69픽셀과 sprite mask 밖 배경은 그대로다. `verify_roll_tactics_dialogue_clear.py`가 두 실제 관측 화면을 각각 검증한다. report는 전체 마스크 일치=false와 각 delta를 보존한다. 텍스트 오류를 숨기거나 전체 애니메이션 화면의 동일성을 주장하지 않는다.
Native choice cursor OAM/focus는 확인했으나 기존 snapshot tile/scanout 불일치에 대한 정밀 cursor bitmap PASS는 여전히 없다. 문자 ink/shadow는 모두 검사하고 source space padding에 덮인 cursor 영역만 구분했다.

## 재현

이미 있는 work/output/route/report는 덮어쓰지 않는다. 새 이름을 지정해 같은 source와 입력으로 빌드한다.

```powershell
python -X utf8 tools/build_development_patch.py --translations translations/megaman_intro_ko.json --translations translations/megaman_pet_menu_ko.json --translations translations/megaman_save_ko.json --translations translations/library_headers_ko.json --translations translations/chip_descriptions_batch09_ko.json --translations translations/chip_secondary_descriptions_ko.json --translations translations/rockman_roll_tactics_escape_ko.json --chip-library --chip-word-copy --chip-cache --chip-burst-copy --chip-library-late-wait --chip-folder --chip-folder-owner-guard --mono-font-poc --chip-battle-names --chip-name-translations translations/library_chip_names_batch08_ko.json --chip-secondary-name-translations translations/chip_secondary_names_ko.json --work poc/build_roll_tactics_next --out poc/output/exe45_ko_development_roll_tactics_next.gba
python -X utf8 tools/report_roll_tactics758_runtime.py
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

## 남은 범위

다른 내비의 질문/도주 대사, 나머지 UI/대사/그래픽 미번역. 실제 롤 선택과 도주 가능 전투의 확인/성공/실패/예·B 취소/확률/후속 진행은 미검증이다. 새 ROM의 추가 칩·도감·배틀 이름·save commit/reboot/lifetime/timing 결과는 이전 ROM에서 자동 상속하지 않는다. 인간 의미/표현 검토, cursor bitmap scanout, 전체 플레이·오디오·실기·배포 QA도 미완료다.
