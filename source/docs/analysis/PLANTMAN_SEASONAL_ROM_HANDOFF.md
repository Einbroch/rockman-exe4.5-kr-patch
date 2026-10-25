# 플랜트맨 기념일·생일 대사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_plantman_seasonal_v1.gba`.
SHA256 `c7553dffa4d3cf32c935c41fd5e154ae91cee76885eeffdfffec6ab1138f9c93`.
신규43 literal=41번역 문구+2유지 인용부호. 누적2,107선택 literal/46선택·686원본 유지 archive.

## 원본·번역 경계

source6D0ADC:1420bytes/21slots/root038540. Payload SHA `b91a0175b8ad929c797e62ab9c93d8fe20aacbb9a606daeaea94cf9ec9809e62`; TPL SHA `effe34f68a756bb7396c8bc04275c8f5936776ab75ba8cf51ea6c4a8727db520`.
intro6CC808은 プラントマン과 인생을 아름다운 꽃에 비유하는 말투를 명시한다. 원본 intro root03850C=086CC808, native group+52/root038540=086D0ADC 확인.
IDs/원문/숫자/줄 수·newline 경계/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지.
nickname1:0/11:0 source·target 첫 행 comma11px 그대로. 이름 뒤 신규 조사나 글자를 붙이지 않는다. 경계 검사는 실제 이름 출력/한글 이름 지원 검증이 아니다.
가가미모치 위 과일은 귤이 아닌 ‘다이다이라는 등자’이며, 집안이 먼 훗날까지 대대로 오래 번영하기를 바라는 기도와 길한 물건이라는 연결을 유지했다. 일본어 과일 이름 다이다이와 ‘대대로’의 의미를 보존했지만 한국어에서 일본어 동음 말장난은 재현하지 못했다. 명칭·말투·문화 표현 초안 인간 검토 대기, 넘버맨4649 승인 전용 없음.
절분에는 대두를 볶고 생콩을 쓰지 말라는 원문과, 뿌린 생콩에서 시간이 지나면 싹이 난다는 식물 관점의 이유 유지. 카카오 나무 열매, 사랑의 꽃, 일본다운 복숭아꽃의 그윽함, 양력5월5일 일본 단오/어린이날과 옛 중국에서 전해졌다고 한다는 전달·추정 문맥 유지. 한국 음력 명절로 날짜를 바꾸지 않았다.
은하수는 꽃다발로도 견줄 수 없는 아름다움, 크리스마스 거리=꽃밭, 연말 애틋함, 생일 나이테1개와 크고 아름답고 씩씩하게 성장하라는 비유 유지.

## 빌드·검사

자산 `translations/plantman_seasonal_ko.json`, 개별 작성 초안 직렬화 `tools/draft_plantman_seasonal.py`.
기존 일렉맨 flags에 `--plantman-seasonal` 추가, immutable source에서 빌드. 이전 patched ROM을 입력으로 사용하지 않는다.
43항목 원문/제어/숫자/이름 뒤2suffix/glyph/3줄132px/roundtrip와142tests 통과. 최대132px는10:0 둘째 행 섣달그믐 대사다. native·semantic·binary roundtrip 통과.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일.563Python 도구 drift=[], 원본 SHA 보존: `analysis/plantman_seasonal_v1/final_identity_audit.json`.
이전 일렉맨판45선택 archive payload와 선택 자산 SHA 보존. 그래픽15라벨/5블록 위치·길이·SHA·실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 신규 전체 이미지 runtime QA를 뜻하지 않는다. 원본·이전후보·실험·테스트 saves 보존.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. controller 입력만 사용, 다른 후보 save/state 미수입. fresh FF64KiB에서 native save 성공script58 확인. 저장 SHA `5decd6c04414c022c20702a8d9ad76763cd877cc90ebadf437f1ae6778bf6461`, 직후snapshot/현재디스크 동일. 과거 아이스맨 후보와 같은 save SHA이지만 이번 자체 FF시작·입력에서 생성했음을 receipt로 확인했다. 다른 테스트 saves 보존. 한글 이름 persistence/기존save 호환 증거는 아니다.
신규12페이지는 격리 renderer 진단이다. 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰하고 exact-ROM/lookup receipt 검사. 절분/칠석/섣달그믐 각각 동일 parent에서 시작했다.
`capture_plantman_seasonal_diagnostic.py --plant-script 2/7/10`: PC08037F20,R0=08038278,R1=1,R3=52 root read1회만 플랜트맨 pool로 alias. PC0804FB76,R0=pool,R1=2,R5=0200FA20 requested1 offset read를 target2/7/10으로 각각1회 alias. 각 root_aliases=1,entry_aliases=1. 원본 caller/initializer·normal-window prefix 검사. 넘버맨 caller·초상 유지, ROM/RAM 쓰기·날짜 변경 없음. alias는 제품ROM에 포함되지 않는다.
checkpoint는 diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false. 정상 플랜트맨 해금/초상/날짜 선택 증거 아님. 다른29문구/이름·성별·이벤트 이름 consumer는 static-only.
입력 사이300frame 대기. 절분5페이지 steps3..7/칠석4페이지 steps3..6/섣달그믐3페이지 steps3..5의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 모두 첫 촬영 strict 검사 통과.10:0 둘째 행132px 경계도 포함한다. 메인 에이전트12페이지 화면 직접 확인. 검사 완화 없음; 전환 전 프레임·하드웨어·음성·실시간RTC 증거 아님.
검사 `tools/report_plantman_seasonal.py`; 결과 `analysis/plantman_seasonal_v1/runtime.json`; 화면 `analysis/plantman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_plantman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택2,107, 미선택 일본어 포함27,919개/기타1,881개. 범위 기반 분류는 완역 분모나 완료율 아님.
다음 포르테6D5A9C: intro6D2180은 이름을 명시하지 않지만 jack-in6D27A0이 フォルテ.EXE를 명시한다. 세 TPL 전체를 이번에 읽고 원본 root038548=086D2180/038558=086D27A0/03857C=086D5A9C를 확인해 동일 native group intro/+16 jack-in/+52 seasonal 관계로 화자를 식별했다. 거친 힘·전투 말투/침묵/날짜·성별 분기를 보존해야 한다. 아직 번역·빌드 입력 미작성.
전체 요청 미완료. 정상 플랜트맨 해금·날짜·이름·성별·이벤트 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이 미해결.
