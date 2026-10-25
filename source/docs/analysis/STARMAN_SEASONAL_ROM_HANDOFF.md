# 스타맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_starman_seasonal_v1.gba`.
SHA256 `54b2e115560d190da157db187fb5cda3bf5e0eebf64c62bf67291cfd2dc06172`.
신규48 literal=46번역 문구+2유지 인용부호. 누적1,869선택 literal/40선택·692원본 유지 archive.

## 원본·번역 경계

source6A8ADC:1439bytes/21slots/root0383D8. Payload SHA `bb9b7965f03aab554b30ef692eac20fa01090bf3881e8ce363efa5d66038f3d1`; TPL SHA `2573ccbd2799ba2ac448b7e37162640884960da843556f5ea8ca7d24b0154081`.
intro6A383C이 スターマン과 반짝임/친근한 인사를 명시한다. 원본 intro root0383A4=086A383C, native group+52/root0383D8=086A8ADC 확인.
IDs/원문/숫자/줄 수·newline 경계/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지. 이 archive에는 nickname 출력이 없다.
새해 첫꿈의1후지산/2매/3가지 순위와3가지 꿈의 길한 의미, 콩 대신 유성우를 내리겠다는 농담/즉시 철회, 별똥별에 비는 소원과 고백 초콜릿 맥락 유지.
어린이날 질문의 ‘재작년’과 뒤따르는 ‘왜 작년이 아닌가’ 농담을 그대로 유지했다. 기둥의 키 표시 맥락도 보존. 일본 명절 날짜/히나 인형/기모노를 한국 명절·옷으로 바꾸지 않는다.
은하수와 하늘의 빛 축제, 겨울철 대삼각형/북두칠성/북극성, 오전0시 연도 전환을 유지했다. 생일 축하의 늘어진 모음은 흥겨운 말투 초안이다. 문화/말투/용어 인간 검토 대기, 넘버맨4649 승인을 전용하지 않는다.

## 빌드·검사

자산 `translations/starman_seasonal_ko.json`, 수동 작성 초안 직렬화 `tools/draft_starman_seasonal.py`.
기존 우드맨 누적 flags에 `--starman-seasonal`을 추가해 immutable source에서 생성한다. 이전 patched ROM은 입력으로 쓰지 않는다.
48항목 원문/제어/숫자/glyph/3줄132px 범위/roundtrip 관련124tests 통과. 최대131px.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일. 현재533Python 도구 drift=[], 원본 SHA 보존: `analysis/starman_seasonal_v1/final_identity_audit.json`. 원본/이전후보/실험/테스트 saves 보존.
이전 우드맨판39선택 archive payload와 선택 자산 해시를 실제ROM bytes까지 보존했다. 그래픽15라벨/5블록의 위치·길이·SHA·실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 신규 전체 이미지 runtime QA를 뜻하지 않는다.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. controller 입력만 사용했고 다른 후보 save/state를 가져오지 않았다. native save 성공script58과64KiB 파일 SHA `6883a8a6ed4f62f1feb3b656d2ca0d976b52c4e0c16da349696e08fea0bf32f4`, 직후snapshot/현재디스크 동일성 확인. 다른 테스트 saves 보존. 이전 아쿠아맨판과 저장 결과 SHA가 같아도 이번 파일은 이 ROM의 자체 신규FF 파일에서 정상 생성했으며 가져온 파일이 아니다. 한글 이름 persistence/기존save 호환 증거는 아니다.
신규9페이지는 정상 스타맨 해금 경로가 아닌 격리 renderer 진단이다. 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰하고 exact-ROM/lookup receipt를 검사했다. 새해/칠석은 같은 parent에서 각각 시작했다.
`capture_starman_seasonal_diagnostic.py --star-script 1/7`: PC08037F20,R0=08038278,R1=1,R3=52의 root read1회만 스타맨 pool로 alias한다.7만 PC0804FB76,R0=pool,R1=2,R5=0200FA20의 requested1 offset read를 target7로1회 alias한다. 각 root_aliases=1,entry_aliases=0/1 확인. 원본 native caller/initializer와 normal-window prefix 검사. 넘버맨 caller·초상 유지, ROM/RAM 쓰기·날짜 변경 없음. alias는 제품ROM에 포함되지 않는다.
각 checkpoint는 diagnostic_checkpoint.mss로 격리하고 normal_play_checkpoint_eligible=false 기록. 정상 스타맨 해금/초상/날짜 선택 증거는 아니다. 다른37문구(성별 포함)와 동적 이벤트 이름 consumer는 static-only/미검증이다.
입력 사이300frame 대기는 앞선 우드맨 캡처 안정화 관찰에 따라 선택했다. 글리프/OBJ VRAM/화면 role colors 및 clearing 검사는 완화하지 않았다. 이번9페이지 모두 첫 촬영에서 엄격 검사 통과. 모든 전환 프레임·하드웨어·실시간RTC 검증을 뜻하지 않는다.
새해4페이지 steps3..6/칠석5페이지 steps3..7의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 통과. 메인 에이전트가9페이지 화면 직접 확인.
검사 `tools/report_starman_seasonal.py`; 결과 `analysis/starman_seasonal_v1/runtime.json`; 화면 `analysis/starman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_starman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,869, 미선택 일본어 포함28,144개/기타1,894개. 범위 기반 분류는 완역 분모나 완료율이 아니다.
다음 섀도맨6AE834; intro6AA1A0 화자/native group 연결부터 확인한다.
전체 요청 미완료. 정상 스타맨 해금·날짜·성별·이벤트 이름 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이가 남아 있다.
