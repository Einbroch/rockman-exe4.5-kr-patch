# 2026-10-03 — 록맨 도주 미번역 6개 반영 및 화면 검증

최신 누적 개발 ROM: `poc/output/exe45_ko_development_megaman_escape_v1.gba`.
독립 재빌드: `poc/output/exe45_ko_development_megaman_escape_v1_repro.gba`.
두 파일 SHA256: `0edaf04c993efcdeced55e743e9f7a4dbbbdabab53d1ced99e759e8e69c1e97e`.
누적 선택 단위 750 = 이전 744 + 새 도주 literal 6. 전 게임의 번역률이나 서로 다른 문구 수가 아니다.
원본 ROM/기존 개발 ROM/세이브는 보존했다. NON-DISTRIBUTION, 모든 새 문구 needs_review.

## 새 번역과 재삽입

`translations/megaman_escape_draft_seed.json`에 록맨의 확인 질문/예/아니요, 성공, 실패, 도주 불가 6개 초안을 직접 작성했다.
`tools/prepare_megaman_escape.py`는 문구를 자동으로 바꾸지 않고 원본 TPL·4473바이트 풀·원본 스크립트 바이트/해시·seed·기존 전술 질문 번역과 연결해 `translations/megaman_tactics_escape_ko.json`을 직렬화한다.
검토 자료는 `translations/MEGAMAN_ESCAPE_REVIEW.md`다. 의미/말투/최종 화면에 대한 인간 승인은 아직 아니다.

76C944는 서로 다른 소비자를 포함한다. 새 registry variant는 기존 전술 질문0/1의 mmbn45s/5x2 mono와 도주2..5의 mmbn45 일반 대사를 분리한다. 하나의 언어·폭으로 전체 아카이브를 처리하지 않는다.
6개 literal만 추가 선택하고, 기존 질문2개는 같은 문구를 유지한다. 기다림18프레임·점6개·초상·선택 이동/취소/분기·줄바꿈·선택지 패딩은 그대로다. 나머지138스크립트와 비선택 literal을 보존한다. 일반 대사는 보수적인144px 개발 범위에서 최대132px로 검사했으며, 이것을 모든 창의 실제 한계라고 주장하지 않는다.
7개 아카이브 선택/다른725개 보존, 원본 헤더/원본 풀 보존 및 최종 변경 영역 감사, 무변경 원본 왕복/번역 제어 구조/바이너리 왕복 통과.

## 동일 ROM의 실제 실행

새 ROM으로13동작 콜드 부팅 →40동작 초기 대화 →43동작 네트워크 튜토리얼 →104동작 전투 경로를 다시 실행했다. 이전 ROM의 SAV/checkpoint를 가져오지 않았다. 격리된 동일 Mesen/BIOS 환경, 음소거 실행이며 오디오 검증은 아니다. 확인한 경로에서 다른 세이브 파일의 해시는 모두 보존됐다.

도주 호출은 전술 질문 화면에서 L 입력으로 확인했다. 원본080212C8은 Navi style*6+script,0802056A는2/5,08020606은3/4를 선택한다.0804FB76이 실제 스크립트 표 오프셋을 읽는다.

- 정상 입력 `megaman-escape-v1-l-target`: 튜토리얼은 도주 불가 조건이어서 실제 스크립트5를 선택한다. “여긴 도망칠 때가 / 아니야!”의 두 화면을 확인했다. 정상 A 입력 후 닫힘도 `forbidden-clear`에서 확인했다.
- `confirm-sample`, `success-sample`, `failure-sample`: native script5 표 오프셋 읽기 한 번만 실제 컴파일된2/3/4 오프셋으로 돌려주는 진단이다. ROM·텍스트·진행 플래그·save RAM은 쓰지 않는다. checkpoint는 격리했으며 정상 플레이의 실제 성공/실패 판정 증거는 아니다.
- 총11개 held 화면: 실제 normal renderer의 stream/glyph index/좌표, 각 글자의 실제 폰트 읽기, ROM/BDF 글리프와 화면 픽셀을 검사했다. 확인창의 좌/우 커서 위치와 ‘아니요’ 선택 후 복귀도 확인했다.
- 총8개 닫힘 화면: 일반 대사 context 비활성, 원래 배경과 같은색 픽셀 마스크, native target 선택, 새 ROM에서 별도로 픽셀 검증한 target 글리프의 VRAM·화면 동일성 확인. 일부 진단 복귀는 캐시를 재사용하므로 새 parser call이 없는 것을 실패로 취급하지 않고 현재 resident bytes와 화면을 직접 확인했다. 움직이는 전투 배경 전체가 동일하다는 주장은 아니다.
- 원본 cursor의 스냅샷 tile role과 scanout은 불일치했다. 정밀 cursor 비트맵 검증은 통과로 처리하지 않는다. OAM 위치/형식과 inspected cursor 화면만 기록한다. source 공간 패딩에 덮이는 cursor 영역은 글자 마스크에서 제외하되, 모든 문자 ink/shadow는 검사했다. 원본 cursor를 고치거나 번역 글자를 지우지 않았다.

`megaman-escape-v1-folder-regression`: 정상16동작/4화면. 기존 캐논·에어슛·발칸1 이름 및 설명의 실제 copy/cache/ABI, 글리프·stage·OBJ·픽셀 회귀 검사 통과.
`megaman-escape-v1-tactics-regression-r2`: 정상7동작/4화면. 두 질문의5x2/640바이트 stage, upload, BG3/10셀/픽셀 검사 통과. 근거는 `exe45_escape_tactics_target_v1.json`, `exe45_escape_tactics_distance_v1.json`.
통합 근거는 `analysis/exe45_megaman_escape_runtime_v2.json`; 앞선 bounded report v1도 보존했다. 자동 테스트91개 통과.

## 보존한 미통과 조사

menu/controls/custom/select survey는 capture 자체가 끝났어도 도주 대사를 호출하지 못했으므로 도주 검증으로 인정하지 않는다. L은 일반 전투/카드 정보 창이 아니라 해당 전술 선택 화면에서 눌러야 이 경로를 통과했다.
첫 tactics-regression은 A가 대상을 확정해 창을 닫았고 새 prompt call이0개여서 검증 실패로 남겼다. r2에서 실제로 질문을 다시 열어 관측했다.
첫 픽셀 검사에서는 native cursor가 source blank padding에 덮이는 것을 글자 오류로 보았다. OAM 범위와 소유자를 분리하되 cursor scanout 불일치 자체는 미검증으로 남겼다.
닫힘 뒤 배경색이0개라는 초기 가정은 원래 메톨도 같은 RGB69픽셀을 사용해서 틀렸다. 새 ROM의 도주 전 화면 마스크와 비교하도록 수정했다. 단순 색상 개수는 창 존재 여부를 독립적으로 증명하지 않는다.

## 재현

기존 산출물을 덮어쓰지 않으므로 아래 work/out은 새 이름을 지정한다.

```powershell
python -X utf8 tools/build_development_patch.py --translations translations/megaman_intro_ko.json --translations translations/megaman_pet_menu_ko.json --translations translations/megaman_save_ko.json --translations translations/library_headers_ko.json --translations translations/chip_descriptions_batch09_ko.json --translations translations/chip_secondary_descriptions_ko.json --translations translations/megaman_tactics_escape_ko.json --chip-library --chip-word-copy --chip-cache --chip-burst-copy --chip-library-late-wait --chip-folder --chip-folder-owner-guard --mono-font-poc --chip-battle-names --chip-name-translations translations/library_chip_names_batch08_ko.json --chip-secondary-name-translations translations/chip_secondary_names_ko.json --work poc/build_megaman_escape_next --out poc/output/exe45_ko_development_megaman_escape_next.gba
python -X utf8 tools/report_megaman_escape_runtime.py
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

## 남은 범위

실제 도주 가능 전투에서 확인창의 예/아니요/B 취소, 실제 성공/실패 확률·재진입·도주 이후 진행은 미검증이다. 다른 내비 대사, 나머지 대사/UI/그래픽 미번역은 남았다.
새 ROM의 추가 칩 이름·도감·배틀 이름·save commit/reboot/lifetime/timing 검증은 이전 ROM의 결과를 그대로 상속하지 않는다. 원본 cursor bitmap scanout, 인간 의미/표현 검토, 전체 플레이·오디오·실기·배포 QA도 미완료다.
한글패치 스킬에 따라 번역 단위와 표시 소비자를 분리하고, 정상 입력과 진단용 표시 검증을 구분했다.
