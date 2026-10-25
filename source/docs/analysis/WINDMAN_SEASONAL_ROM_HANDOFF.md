# 윈드맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

최신 누적 ROM: `poc/output/exe45_ko_development_windman_seasonal_v1.gba`.
SHA256 `30db71bf4d47a7acb163044c2ee745210935acd1cb085c5e175007fd52087301`.
거츠맨 누적판의 30개 archive payload와 선택 번역·이미지 자산 해시를 유지하고 윈드맨66F78C를 추가했다.
신규46 literal=44개 번역 문구+2개 원본 유지 인용 부호. 누적1,507선택 literal/31선택·701원본 유지 archive.
새해·절분·발렌타인·3월3일 히나마쓰리·5월5일 단오·칠석·성탄절·연말·생일·창립 기념일·동적 이벤트 안내를 포함한다. 원본 날짜를 다른 한국 명절 날짜로 바꾸지 않았다.

## 원본 보존과 빌드

source66F78C:1292bytes/21slots/root038180, payload SHA `bc18012be15429b1253d6e546b2ab94755537ecbb3b6104881a8f58117d5ba2f`.
source TPL SHA `4fb6eaac8efabe6bf2ae7bf3c5b04050fa93a71883c6ce752f270dc35392819f`.
intro66B8B0의 화자 원문이 윈드맨을 명시한다. 같은60byte native Navi group의 intro pointer+52가 seasonal pointer다.
source/IDs/21slots/모든 숫자/줄 수/명령/anniversary buffer·loop/인용 부호를 보존했다. 빈0/13/14/15와 없는4/16/20 slots도 그대로다. 이름 입력·저장 형식·RTC·게임 진행 코드를 변경하지 않았다.
전체46 literal의 인코딩/glyph 공급/native·semantic·binary roundtrip 통과. 3줄/132px 채택 범위 내, 실제 최대125px.
관련97tests 통과. 원본과 최종488Python 도구 정합 drift=[] 및3독립 빌드 동일 SHA는 `analysis/windman_seasonal_v1/final_identity_audit.json`에 있다.
원본 ROM과 이전 후보/실패 실험/isolated test save는 보존했다. 배포용 패치를 만들거나 배포 가능 판정을 하지 않았다.

자산: `translations/windman_seasonal_ko.json`.
개별 문맥의 수동 초안을 source stable ID에 직렬화하는 도구: `tools/draft_windman_seasonal.py`.
이전 `analysis/GUTSMAN_SEASONAL_ROM_HANDOFF.md`의 누적 flags를 전부 유지하고 `--windman-seasonal`을 추가한다. `build_roll_pet.py --work FRESH --out FRESH.gba`로 immutable source에서 생성한다. 기존 patched ROM을 입력으로 쓰지 않는다.
독립 빌드 suffix: `_repro`, `_current_repro`. 최종 도구 정합은 `_current_repro` manifest 기준이다.

## 실행 검증과 구분

`run_numberman_seasonal_normal.py --stem exe45_ko_development_windman_seasonal_v1 --prefix windman-seasonal-v1-`로 같은 ROM 자체 cold 시작→넘버맨 첫 선택→게임 내 저장→checkpoint 없는 cold 이어하기→내비 재선택을 일반 controller 입력만으로 실행했다.
64KiB native save가 FF 초기 상태에서 SHA `c4837a72f9e88585e6c71ac6cd685ffb0ca0ae9a641091c5879789ca24e7abd9`로 바뀌었으며 source save-success58과 현재 디스크 동일성을 확인했다. 이 결과는 한글 이름 저장·기존 save 호환 검증이 아니다.
같은 ROM 넘버맨 새해3페이지 정상 회귀 검사 통과. 다른 후보 checkpoint/save를 가져오지 않았다.

윈드맨 정상 해금 경로는 아직 확인되지 않았다. 따라서 신규 화면은 **격리된 렌더링 진단**이다.
`capture_seasonal_lookup.py`에서 실제 넘버맨 seasonal root0382AC의 read를 먼저 관찰했다: PC08037F20, R0=08038278, R1=1, R3=52. source native lookup 코드가 그대로인 것도 확인했다.
그 관찰을 검증한 `capture_windman_seasonal_diagnostic.py`는 같은 정상 pre-load checkpoint에서 시작해 해당 포인터 read1회만 윈드맨 pool로 alias한다. script1, 정상 window/consumer 및 넘버맨 caller/초상은 유지된다. ROM/RAM 직접 쓰기나 날짜 변경은 없으며 개입은 제품 ROM에 포함되지 않는다.
diagnostic checkpoint는 이름을 `diagnostic_checkpoint.mss`로 격리하고 `normal_play_checkpoint_eligible=false`로 기록했다. 이후 정상 플레이 근거로 사용하지 않는다.
진단 새해5페이지(steps3..7)의 font CPU read→ROM glyph→OBJ VRAM→화면 픽셀, 페이지 순서/빈 영역 지워짐/종료가 통과했다. 화면의 넘버맨 초상을 윈드맨 정상 초상으로 해석하지 않는다.
관측과 보호/회귀 검사: `tools/report_windman_seasonal.py`, `analysis/windman_seasonal_v1/runtime.json`.
화면: `analysis/windman_seasonal_v1/diagnostic_new_year_pages.png`.
다른39 신규 문구 및 anniversary 동적 이벤트 이름/다른 날짜는 static-only. 윈드맨 정상 해금·초상·날짜별 이벤트 진입은 미검증이다.

## 검토 대기와 다음 작업

차분한 하마/하거라/이로군 말투는 원문에서 도출한 후보이며 인간 승인된 말투는 아니다.
66F78C:3:3의 초콜릿/おかし(이상한·과자) 말장난을 ‘달콤하고도 묘한 풍습’으로 옮긴 표현은 문맥 초안이며 검토 대기다. 사용자가 승인한 넘버맨4649 결정은 이 표현에 적용되지 않는다. 문화 설명과 연말 속담도 needs_review이다.
전체 catalogue 최신 추적: `analysis/full_scope_windman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literal 중 미선택 일본어 포함28,487개, 기타 미선택1,913개. 기호/반복/문맥을 판정한 완역 분모나 완료율이 아니다. 전체 요청은 아직 완료되지 않았다.
다음 대사 묶음은 서치맨675440이며 source intro670DF4와 seasonal group 연결을 확인한 후 번역한다.
가장 어려운 완료 조건인 한글 이름 입력/편집→committed record→모든 재표시→영구 재로드→기존 save 호환, 전체 graphics/inline/fixed-string population, 이전 native 대기 화살표53pixel 차이는 미해결이다.
