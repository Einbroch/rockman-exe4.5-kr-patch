# 아이스맨 기념일·생일 대사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_iceman_seasonal_v1.gba`.
SHA256 `e0d5c1995e12ddbd30755875d37bbe513a4d15fa28dbcc9caa96c61b0d05a4f6`.
신규34 literal=32번역 문구+2유지 인용부호. 누적2,024선택 literal/44선택·688원본 유지 archive.

## 원본·번역 경계

source6C5A88:1182bytes/21slots/root0384C8. Payload SHA `16cd9b1e7ce2355d2b3dc5f91659ea0c92edbad47dfe4b569d196e22a1e7fc63`; TPL SHA `a3aa5fc7530aa4c65550de1072cf22f09ba408b216f7039942114da0f330aaae`.
intro6C167C은 アイスマン과 부드러운 존댓말을 명시한다. 원본 intro root038494=086C167C, native group+52/root0384C8=086C5A88 확인.
IDs/원문/숫자/줄 수·newline 경계/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지.
nickname3:1/11:0 source·target 첫 행 comma11px 그대로. 이름 뒤 신규 조사나 글자를 붙이지 않는다. 경계 검사는 실제 이름 출력/한글 이름 지원 검증이 아니다.
크리스마스8:1은 일본어 イブ(B)/イヴ(V) 차이를 ‘B 소리 말고,/V 소리예요!’로 설명하는 개별 초안이다. 한국어 ‘이브’를 두 번 반복하여 차이가 사라지지 않게 했다. 명칭·말투·표기 농담은 인간 검토 대기, 넘버맨4649 승인을 전용하지 않는다.
일본3월3일 복숭아 절기/히나마쓰리, 인형을 늦게 치우면 시집이 늦는다고 한다는 원문 전승,5월5일 남자아이 날 대비 유지. 칠석 대나무 잎 사각사각/은하수·다이아몬드더스트 비교, 해넘이 소바로 냉중화면을 좋아하는 농담 보존. 뜨거운 소바나 한국 냉면으로 바꾸지 않았다. 모든 원문 날짜·숫자 유지.

## 빌드·검사

자산 `translations/iceman_seasonal_ko.json`, 개별 작성 초안 직렬화 `tools/draft_iceman_seasonal.py`.
기존 네이팜맨 flags에 `--iceman-seasonal` 추가, immutable source에서 빌드. 이전 patched ROM을 입력으로 사용하지 않는다.
34항목 원문/제어/숫자/이름 뒤2suffix/glyph/3줄132px/roundtrip와136tests 통과. 최대127px, native·semantic·binary roundtrip 통과.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일.553Python 도구 drift=[], 원본 SHA 보존: `analysis/iceman_seasonal_v1/final_identity_audit.json`.
이전 네이팜맨판43선택 archive payload 및 선택 자산 SHA 보존. 그래픽15라벨/5블록 위치·길이·SHA·실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 신규 전체 이미지 runtime QA를 뜻하지 않는다. 원본·이전후보·실험·테스트 saves 보존.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. controller 입력만 사용, 다른 후보 save/state 미수입. fresh FF64KiB에서 native save 성공script58 확인. 저장 SHA `5decd6c04414c022c20702a8d9ad76763cd877cc90ebadf437f1ae6778bf6461`, 직후snapshot/현재디스크 동일. 다른 테스트 saves 보존. 한글 이름 persistence/기존save 호환 증거는 아니다.
신규7페이지는 격리 renderer 진단이다. 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰하고 exact-ROM/lookup receipt 검사. 크리스마스이브/섣달그믐 각각 동일 parent에서 시작했다.
`capture_iceman_seasonal_diagnostic.py --ice-script 8/10`: PC08037F20,R0=08038278,R1=1,R3=52 root read1회만 아이스맨 pool로 alias. PC0804FB76,R0=pool,R1=2,R5=0200FA20 requested1 offset read를 target8/10으로 각각1회 alias. 각 root_aliases=1,entry_aliases=1. 원본 caller/initializer·normal-window prefix 검사. 넘버맨 caller·초상 유지, ROM/RAM 쓰기·날짜 변경 없음. alias는 제품ROM에 포함되지 않는다.
checkpoint는 diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false. 정상 아이스맨 해금/초상/날짜 선택 증거 아님. 다른25문구/이름·성별·이벤트 이름 consumer는 static-only.
입력 사이300frame 대기. 크리스마스이브3페이지 steps3..5/섣달그믐4페이지 steps3..6의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 모두 첫 촬영 strict 검사 통과. 메인 에이전트7페이지 화면 직접 확인. 검사 완화 없음; 전환 전 프레임·하드웨어·음성·실시간RTC 증거 아님.
검사 `tools/report_iceman_seasonal.py`; 결과 `analysis/iceman_seasonal_v1/runtime.json`; 화면 `analysis/iceman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_iceman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택2,024, 미선택 일본어 포함27,998개/기타1,885개. 범위 기반 분류는 완역 분모나 완료율 아님.
다음 일렉맨6CB184; intro6C7084/seasonal TPL 전체를 이번에 읽었다. 전기·뿔·도깨비/썬더맨 대비, 조명·잉어 깃발·칠석/크리스마스, 리셋 과장 대사, 날짜·숫자·성별 분기 보존 필요. 아직 번역·빌드 입력 미작성.
전체 요청 미완료. 정상 아이스맨 해금·날짜·이름·성별·이벤트 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이 미해결.
