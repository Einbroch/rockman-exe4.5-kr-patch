# 2026-10-03 — 추가 칩 이름 98개 도감·폴더 반영

최신 누적 개발 ROM: `poc/output/exe45_ko_development_chip_secondary_names_v1.gba`.
독립 재빌드: `poc/output/exe45_ko_development_chip_secondary_names_v1_repro.gba`.
두 파일 SHA256: `c0080a116f4966edbfa3cb9578526a39f6c25c45eec52e3eef99eb3530e950bf`.
누적 선택 단위 744 = 이전 646 + 추가 이름 98. 서로 다른 번역 문구 수나 전 게임 번역률이 아니다.
번역 초안은 기존 `translations/chip_secondary_names_ko.json`을 사용했으며 이번 단계에서 문구를 임의로 바꾸지 않았다. 모두 needs_review, NON-DISTRIBUTION.

## 반영 경계

- 원본 765B18 이름 풀 1103바이트 및 공유 포인터는 그대로 보존한다.
- 도감·폴더의 확인된 개별 소비자에만 137슬롯 사설 복제본을 배치한다. 98개 선택 이름을 한글화하고, 39개 비선택 슬롯(빈 항목·???? 포함)은 바이트 동일성을 검사한다.
- 원본 primary/secondary 루트, 정규화된 ID 0..136 및 기존 행·소유자·버퍼·팔레트·캐시 가드를 통과할 때만 추가 복제본을 선택한다.
- 기존 primary 이름 249개, 설명 251개, 추가 설명 75개, 기타 71개는 그대로 유지한다. 배틀 이름 선택 범위는 기존 primary 1..194,201..255 그대로다. 추가 칩 배틀 이름·그 밖의 이름 소비자는 아직 원본이다.
- 7개 아카이브 선택, 다른 725개 보존, 원본/헤더 보존 및 최종 변경 영역 감사 통과.

## 검증

`analysis/exe45_secondary_names_library_cpu_v1.json`: 34,054 벡터.
`analysis/exe45_secondary_names_folder_cpu_v1.json`: 34,058 벡터.
각각 24,224개 bounded glyph copy, 레지스터·메모리·타일·캐시·fallback 검사 통과. CPU fixture는 실제 화면/프레임 부하 증거가 아니다.

새 ROM 해시에 묶인 콜드 부팅 13동작 → 초기 대화 40동작 → 폴더 경로를 새로 수행했다. 이전 ROM의 SAV/checkpoint를 가져오지 않았다. 다른 빌드 세이브는 검증한 경로에서 해시 동일하다.

`poc/runtime/chip-secondary-names-v1-folder-samples`: 16동작, 8개 화면. 진단용 descriptor read alias로 secondary 스크립트 0,1,7,16,22,29,88을 선택했다. 우드맨DS·탭맨·버너맨·레이저맨·비디오맨·파이어플러스·드림소드의 7행 이름과 선택 설명을 검사했다. 실제 이름 타일맵/글리프/스크린샷 픽셀, 설명 스트림·stage·VRAM·27 OBJ 셀/픽셀 및 copy/cache/ABI 관측 통과.
ROM/텍스트/진행 플래그/세이브 RAM 변경은 없지만, 이 경로는 정상 플레이로 획득한 칩의 증거가 아니다. 진단 checkpoint는 격리했으며 정상 플레이 이어하기 입력으로 사용할 수 없다. 사진·수치 등 다른 descriptor 필드 일치도 주장하지 않는다.

`poc/runtime/chip-secondary-names-v1-normal-scroll`: 진단 alias 없이 16동작, 4개 화면. 기존 캐논·에어슛·발칸1 이름 스크롤의 픽셀과 copy/cache/ABI 회귀 검사 통과.
통합 근거: `analysis/exe45_secondary_names_runtime_v1.json`.
재검사: `python -X utf8 tools/report_secondary_names_runtime.py`와 `python -X utf8 -m unittest discover -s tools -p 'test_*.py'`.

초기 빌드는 새 spec JSON 첫 줄의 잘못된 + 때문에 중단되었다. 파일을 수정한 뒤 별도 r2 작업 폴더로 빌드했다. 실패 폴더 `poc/build_chip_secondary_names_v1`은 보존하고 통과 근거에 포함하지 않았다.

## 남은 작업

추가 이름 화면은 98개 중 대표 7개만 확인했다. 도감 선택기는 CPU 검사만 통과했고 이번 ROM의 도감 화면·재진입은 남았다. 추가 배틀 이름/다른 소비자는 별도 조사·통합이 필요하다.
미번역 대사·UI·그래픽, 번역 의미/자연스러움과 사용자 검토, timing/lifetime, 저장 commit/reboot, 전체 게임·오디오·실기·배포 QA는 미완료다. 원본 ROM과 이전 개발본/세이브/검증 자료를 보존한다.
