# 네이팜맨 기념일·생일 대사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_napalmman_seasonal_v1.gba`.
SHA256 `5a2644e47d768d1afbf5b7becf49053c25e99d84cfa43e36d91a75680fc22406`.
신규38 literal=36번역 문구+2유지 인용부호. 누적1,990선택 literal/43선택·689원본 유지 archive.

## 원본·번역 경계

source6C004C:1199bytes/21slots/root03848C. Payload SHA `6a2c9afa4c376d637ee48ac5f86dd1dd275cbc9c392dff8a61cfe44dacc1e1aa`; TPL SHA `b8fc0f74af82d83016d1c00b711ed5a48ea5ac610f668250ea7a6f1fbb226a8b`.
intro6BBAF8은 ナパームマン과 성급한 파괴·발사 말투를 명시한다. 원본 intro root038458=086BBAF8, native group+52/root03848C=086C004C 확인.
IDs/원문/숫자/줄 수·newline 경계/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지. nickname 삽입 없음.
새해 발사 호언, 절분 콩·도깨비 밖/복 안 구호·폭발음, 발렌타인 표적·초콜릿 바주카, 일본 축제 문맥 유지. 크리스마스8:1의 싫어하는 듯한 전개 뒤8:2에서 좋아한다는 반전 보존. 칠석7월7일과 제야의 종 대신 네이팜탄108발이라는 수량·대상 보존. 생일은 즉시 기념 넷배틀이다.
개별 작성 초안이며 명칭·말투·폭발 의성어 인간 검토 대기. 넘버맨4649 승인을 전용하지 않는다.

## 빌드·검사

자산 `translations/napalmman_seasonal_ko.json`, 개별 작성 초안 직렬화 `tools/draft_napalmman_seasonal.py`.
기존 나이트맨 flags에 `--napalmman-seasonal` 추가, immutable source에서 빌드. 이전 patched ROM을 입력으로 사용하지 않는다.
38항목 원문/제어/숫자/glyph/3줄132px/roundtrip와133tests 통과. 최대127px, native·semantic·binary roundtrip 통과.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일.548Python 도구 drift=[], 원본 SHA 보존: `analysis/napalmman_seasonal_v1/final_identity_audit.json`.
이전 나이트맨판42선택 archive payload와 선택 자산 SHA 보존. 그래픽15라벨/5블록의 위치·길이·SHA·실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소/신규 전체 이미지 runtime QA를 뜻하지 않는다. 원본·이전후보·실험·테스트 saves 보존.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. controller 입력만 사용, 다른 후보 save/state 미수입. fresh FF64KiB에서 native save 성공script58 확인. 저장 SHA `046446bad3e5069b17009058279c2a291af9a683effb0d9da149c8444e6cc970`, 직후snapshot/현재디스크 동일. 과거 후보와 같은 save SHA라도 자체 입력에서 생성됐음을 receipt로 확인했다. 한글 이름 persistence/기존save 호환 증거는 아니다.
신규9페이지는 격리 renderer 진단. 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰하고 exact-ROM/lookup receipt 검사. 새해/절분 각각 동일 parent에서 시작.
`capture_napalmman_seasonal_diagnostic.py --napalm-script 1/2`: PC08037F20,R0=08038278,R1=1,R3=52 root read1회만 네이팜맨 pool로 alias. 절분만 PC0804FB76,R0=pool,R1=2,R5=0200FA20 requested1 offset read를 target2로1회 alias. root_aliases=1,entry_aliases=0/1. 원본 caller/initializer·normal-window prefix 검사. 넘버맨 caller·초상 유지, ROM/RAM 쓰기·날짜 변경 없음. alias는 제품ROM에 포함되지 않는다.
checkpoint는 diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false. 정상 네이팜맨 해금/초상/날짜 선택 증거 아님. 다른27문구/성별·이벤트 이름 consumer는 static-only.
입력 사이300frame 대기. 새해4페이지 steps3..6/절분5페이지 steps3..7의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 모두 첫 촬영 strict 검사 통과. 메인 에이전트9페이지 화면 직접 확인. 검사 완화 없음; 전환 전 프레임·하드웨어·음성·실시간RTC 증거 아님.
검사 `tools/report_napalmman_seasonal.py`; 결과 `analysis/napalmman_seasonal_v1/runtime.json`; 화면 `analysis/napalmman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_napalmman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,990, 미선택 일본어 포함28,030개/기타1,887개. 범위 기반 분류는 완역 분모나 완료율 아님.
다음 아이스맨6C5A88; intro6C167C/seasonal TPL 전체를 이번에 읽었다. 이름 뒤3:1/11:0 comma 경계, 날짜, 일본 이브 표기 농담8:1과 찬 연말국수 농담 의미·문화 검토 필요. 아직 번역·빌드 입력 미작성.
전체 요청 미완료. 정상 네이팜맨 해금·날짜·성별·이벤트 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이 미해결.
