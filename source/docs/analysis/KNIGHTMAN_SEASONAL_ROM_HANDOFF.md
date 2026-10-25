# 나이트맨 기념일·생일 대사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_knightman_seasonal_v1.gba`.
SHA256 `2c130314fe4af7611df9a9ace9c667a843baa8fdfe636e276f58e04ab244535f`.
신규42 literal=39번역 문구+3유지 문장부호(새해 nickname 쉼표1/인용부호2). 누적1,952선택 literal/42선택·690원본 유지 archive.

## 원본·번역 경계

source6BA3AC:1378bytes/21slots/root038450. Payload SHA `778552959e3b0c761eae033fb9053a0293e1830d628683233712c3ecf3b290a0`; TPL SHA `66f1acd761c8255f8d19c5007b0f63ce5b9cf0a3e7553ed8af9b741f6f6c2c2a`.
intro6B5A70이 ナイトマン과 플레이어에 대한 충성을 명시한다. 원본 intro root03841C=086B5A70, native group+52/root038450=086BA3AC 확인.
IDs/원문/숫자/줄 수·newline 경계/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지.
nickname suffix7곳을 source/target 첫 줄에 bind했다:1:2 scalar comma,3:0/4:0/9:0/11:0 comma,3:1 leading blank/newline 그대로.4:1 sourceから22px는 조사 비의존 comma11px로 줄이고 다음 행에서 ‘그대가 준 초콜릿에’로 FROM-player 의미를 유지했다. ‘께’만 넣어 받는 사람으로 뒤집거나 ‘께서’24px로 원문 suffix보다 늘리지 않았다. 실제 이름 출력/한글 이름 지원 검증은 아니다.
새해1:2 scalar comma는 원본·대상 nickname print F90C01/comma87/keyWait+clearMsg E600F1 경계에 유일하게 연결해 다른 comma와 혼동하지 않는다. 일반 uniqueness 검사를 완화하지 않았다.
기사다운 정중한 말투, 새해 첫 넷배틀/콩 대신 철구 뿌리기 농담/여성을 배려하는 예절/일본5월 갑옷·투구·인형과 실용성·예술성 대비/칠석 기사 소원을 유지했다. 소원 quote와 둘째 행 선행 공백 유지.
섣달그믐 단일 행은 빌드 전에 의미·행 수를 보존한 ‘오늘은 섣달그믐이오!’로 수동 조정했다. 문화/말투/명칭 인간 검토 대기, 넘버맨4649 승인을 전용하지 않는다.

## 빌드·검사

자산 `translations/knightman_seasonal_ko.json`, 수동 작성 초안 직렬화 `tools/draft_knightman_seasonal.py`.
기존 섀도맨 누적 flags에 `--knightman-seasonal`을 추가해 immutable source에서 생성한다. 이전 patched ROM은 입력으로 쓰지 않는다.
42항목 원문/제어/숫자/이름 뒤 경계/glyph/3줄132px 범위/roundtrip 관련130tests 통과. 최대127px. scalar nickname comma의 유일한 명령 경계/7suffix profiles와 native·semantic·binary roundtrip 통과.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일. 현재543Python 도구 drift=[], 원본 SHA 보존: `analysis/knightman_seasonal_v1/final_identity_audit.json`. 원본/이전후보/실험/테스트 saves 보존.
이전 섀도맨판41선택 archive payload와 선택 자산 해시를 실제ROM bytes까지 보존했다. 그래픽15라벨/5블록의 위치·길이·SHA·실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 신규 전체 이미지 runtime QA를 뜻하지 않는다.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. controller 입력만 사용했고 다른 후보 save/state를 가져오지 않았다. native save 성공script58과64KiB 파일 SHA `fb82d51b06fadc2d37d3e87990edc0d1104b5abb9ee99df461803769915f65ca`, 직후snapshot/현재디스크 동일성 확인. 다른 테스트 saves 보존. 한글 이름 persistence/기존save 호환 증거는 아니다.
신규8페이지는 정상 나이트맨 해금 경로가 아닌 격리 renderer 진단이다. 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰하고 exact-ROM/lookup receipt를 검사했다. 절분/갑옷 설명은 같은 parent에서 각각 시작했다.
`capture_knightman_seasonal_diagnostic.py --knight-script 2/6`: PC08037F20,R0=08038278,R1=1,R3=52의 root read1회만 나이트맨 pool로 alias하고, PC0804FB76,R0=pool,R1=2,R5=0200FA20의 requested1 offset read를 target2/6로1회 alias했다. 각 root_aliases=1,entry_aliases=1 확인. 원본 native caller/initializer와 normal-window prefix 검사. 넘버맨 caller·초상 유지, ROM/RAM 쓰기·날짜 변경 없음. alias는 제품ROM에 포함되지 않는다.
각 checkpoint는 diagnostic_checkpoint.mss로 격리하고 normal_play_checkpoint_eligible=false 기록. 정상 나이트맨 해금/초상/날짜 선택 증거는 아니다. 다른31문구와 이름 출력/성별/이벤트 이름 consumer는 static-only/미검증이다.
입력 사이300frame 대기는 기존 캡처 안정화 관찰에 따라 선택했다. 글리프/OBJ VRAM/화면 role colors 및 clearing 검사는 완화하지 않았다. 이번8페이지 모두 첫 촬영에서 엄격 검사 통과. 모든 전환 프레임·하드웨어·음성·실시간RTC 검증을 뜻하지 않는다.
절분3페이지 steps3..5/갑옷 설명5페이지 steps3..7의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 통과. 메인 에이전트가8페이지 화면 직접 확인.
검사 `tools/report_knightman_seasonal.py`; 결과 `analysis/knightman_seasonal_v1/runtime.json`; 화면 `analysis/knightman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_knightman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,952, 미선택 일본어 포함28,066개/기타1,889개. 범위 기반 분류는 완역 분모나 완료율이 아니다.
다음 네이팜맨6C004C; intro6BBAF8 화자/native group 연결부터 확인한다.
전체 요청 미완료. 정상 나이트맨 해금·날짜·성별·이름 출력·이벤트 이름 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이가 남아 있다.
