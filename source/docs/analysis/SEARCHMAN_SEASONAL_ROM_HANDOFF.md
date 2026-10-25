# 서치맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

최신 누적 ROM: `poc/output/exe45_ko_development_searchman_seasonal_v1.gba`.
SHA256 `4a42aa2821057f480a1aacfe4c3c78a2a87e85eeb1d6152bc1a8e7e699cf50b2`.
윈드맨 누적판의31개 선택 archive payload 및 선택 번역·이미지 자산 해시를 유지하고 서치맨675440를 추가했다.
신규40 literal=38개 번역 문구+2개 원본 유지 인용 부호. 누적1,547선택 literal/32선택·700원본 유지 archive.
새해/절분/발렌타인 성별 분기/히나마쓰리/어린이날/칠석/성탄절/연말/생일/창립 기념일/동적 이벤트 안내를 포함한다.

## 원본과 보호 정책

source675440:1273bytes/21slots/root0381BC. Payload SHA `aa4125147506b7467818e08c32c0d5e54597da39ad69ce220ce62ec7224f3973`, TPL SHA `26b77c7badf06979641c3b872f2e2f8d82dd966c435be3e08254c914f93ba90d`.
intro670DF4 원문이 서치맨을 명시하며, native60byte Navi group의 intro pointer+52가 seasonal pointer이다.
source/IDs/21slots/줄 수/명령/global22 성별 분기/날짜/60·55·45% 수치/이벤트 이름 buffer·loop/인용 부호를 보존했다. 빈0/13/14/15와 없는16/20도 그대로다.
675440:3:1은 printPlayerNickname 직후에 나오는 source 첫 줄 ‘の’를 조사 없는 구두점 ‘、’로 옮겼다. 동일11px 폭, 뒤 두 줄은 독립적인 ‘초콜릿 획득/확률은・・・’이다. 한글 이름 뒤 고정 조사 사용이나 첫 줄 폭 증가를 허용하지 않는다. builder의 nickname_suffix_profiles에 exact source/target를 등록했다.
이 suffix 검사는 이름 입력·한글 이름 persistence 지원을 뜻하지 않는다. 해당 성별/닉네임 대사 실행은 아직 static-only다.
문화 표현은 원본 일본 날짜와 맥락을 보존한다. 히나/마트료시카 인형 비교와 일본 갑옷·투구 풍습을 유지했다.
정중한 군인 말투와 ‘미션/목표/록온’, 원문 Weather Search의 ‘기상 탐색!’은 문맥 초안이며 인간 승인된 용어/말투가 아니다. 전체 needs_review.
이름 입력·저장 형식·RTC·게임 진행 코드나 확률 계산은 변경하지 않았다. 기존 넘버맨4649 승인 표현 ‘다시 한번/잘 부탁드려요’는 그대로 유지한다.

## 빌드와 보존 검사

자산 `translations/searchman_seasonal_ko.json`; source 기반 수동 초안 직렬화 `tools/draft_searchman_seasonal.py`.
이전 `analysis/WINDMAN_SEASONAL_ROM_HANDOFF.md`의 모든 누적 flags에 `--searchman-seasonal`을 추가한다. `tools/build_roll_pet.py --work FRESH --out FRESH.gba`로 immutable source에서 재생성하며 기존 patched ROM을 빌드 입력으로 사용하지 않는다.
전체40 literal 인코딩/glyph/native·semantic·binary roundtrip/3줄132px 채택 범위 통과. 최대125px.
관련100tests 통과. source/control/초안 일치, 숫자 변경과 nickname suffix 변경 거부 테스트를 포함한다.
main·`_repro`·`_current_repro_r2`의3독립 빌드 동일 SHA, 원본 SHA 보존, 현재493Python 도구 drift=[]: `analysis/searchman_seasonal_v1/final_identity_audit.json`.
먼저 만든 `_current_repro`는 그래픽 ROM-byte 보존 검사를 보강하기 전 도구 identity로 남겨 두었다. 최종 정합 감사는 `_current_repro_r2`를 사용한다. 이전 후보/원본/실험/isolated test saves를 삭제하지 않았다.
기존31개 선택 archive payload가 실제 ROM bytes까지 동일하다. 선택 자산 해시도 동일하다.
기존 그래픽15라벨의5블록(calendar frequency5/PET menu7/attack caption1/save title1/equipment title1)을 실제 저장 범위로 비교했다. source_offset/bytes/final SHA와 ROM bytes가 이전 누적판과 동일하다. ‘통신’의 기존 glyph override도 유지된다. 이는 전체 이미지 미번역 해소나 모든 이미지의 신규 runtime QA 주장이 아니다.

## 실제 실행과 진단 구분

`run_numberman_seasonal_normal.py --stem exe45_ko_development_searchman_seasonal_v1 --prefix searchman-seasonal-v1-`로 자체 cold 시작→넘버맨 첫 선택→정상 게임 저장→checkpoint 없는 cold 이어하기→내비 재선택을 일반 controller 입력만으로 실행했다.
64KiB save가 FF 초기 상태에서 SHA `be50a69cb0a10ad16e73893b40394250f30e27ab053d6865ddb3f6fcaa5305ae`로 바뀌었다. source save-success58과 현재 디스크/저장 직후 snapshot 동일성을 확인했다. 다른 테스트 저장 파일은 보존됐다. 한글 이름 저장 및 기존save 호환의 증거는 아니다.
같은 누적 ROM 정상 넘버맨 새해3페이지 회귀 통과. 다른 후보 checkpoint/save를 가져오지 않았다.

서치맨 정상 해금 경로는 미확인이다. 신규 화면은 **격리된 렌더링 진단**이다.
자체 normal-reload-select checkpoint는 대사 load 이전이다. `capture_seasonal_lookup.py`로 실제 넘버맨 seasonal root0382AC를 read-only 관찰하고 exact ROM/receipt를 검증했다: PC08037F20,R0=08038278,R1=1,R3=52.
`capture_searchman_seasonal_diagnostic.py`는 같은 pre-load parent에서 root read1회만 서치맨 pool로 alias한다. script7/8은 native initializer PC0804FB76/R0=pool/R1=2/R5=0200FA20의 script1 offset read1회도 해당 target offset으로 alias한다. source native caller/initializer bytes가 동일해야 실행한다.
script1 새해3페이지(steps3..5), script7 칠석/55%4페이지(3..6), script8 이브/45%4페이지(3..6), 합계11페이지가 font CPU read→ROM glyph→OBJ VRAM→화면 픽셀/페이지 순서/빈 영역 clearing/종료 검사를 통과했다.
넘버맨 caller·초상이 남아 있으므로 서치맨 정상 해금/초상/날짜 선택/확률 계산 검증으로 해석하지 않는다. ROM/RAM 직접 쓰기나 날짜 변경 없이 실행했으며 alias는 제품 ROM에 포함되지 않는다.
각 진단 checkpoint는 diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false. 정상 플레이의 후속 state로 사용하지 않는다.
검사 `tools/report_searchman_seasonal.py`, 결과 `analysis/searchman_seasonal_v1/runtime.json`, 화면 `analysis/searchman_seasonal_v1/diagnostic_pages.png`.
다른27문구(성별/닉네임60% 포함), 동적 이벤트 이름 소비 및 정상 서치맨 진입은 미검증/static-only이다.

## 남은 범위와 다음 작업

최신 catalogue `analysis/full_scope_searchman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,547, 미선택 일본어 포함28,449, 기타 미선택1,911. 범위 기반 일본어 분류는 완역 분모나 완료율이 아니다. 전체 사용자 요청은 아직 완료되지 않았다.
다음 기념일 대사: 파이어맨67AE2C, source intro676AE4 화자·native group 연결 확인부터 진행한다.
가장 어려운 제품 완료 조건: 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환. 전체 graphics/inline/fixed-string population과 이전 native wait-arrow53pixel 차이도 미해결이다. 배포용 패치 또는 release 판정을 만들지 않았다.
