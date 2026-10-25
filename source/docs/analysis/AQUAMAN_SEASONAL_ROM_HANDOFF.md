# 아쿠아맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_aquaman_seasonal_v1.gba`.
SHA256 `05d164a5eae6cc931b24f7326d8024241e7b4f36a85fa1a1ea9a48762f402eb0`.
신규43 literal=41개 번역 문구+2개 유지 인용부호. 누적1,780선택 literal/38선택·694원본 유지 archive.

## 원본·번역 경계

source69C9F4:1358bytes/21slots/root038360. Payload SHA `a3964058397d628e176eb99f399848b03d089b3dd05e2dd5eee750cccadc77a8`; TPL SHA `d36bb7fb947c1d38c9beb90878815fc7efbd053c12f6ef94fe065f476c254811`.
intro698424의 アクアマン과 ぴゅ 말끝을 확인했다. 원본 intro root03832C=08698424, native group+52/root038360=0869C9F4 확인.
IDs/원문/숫자/줄 수와 newline 경계/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지.
nickname 출력 뒤2:5 첫 줄 も,4:1 첫 줄 は는 동일11px의 조사 비의존 쉼표 ‘、’로 번역하고 다음 행에 초대/질문을 배치했다. 실제 nickname 출력 또는 한글 이름 지원 검증은 아니다.
‘퓨’는 원문 말끝을 옮긴 초안이다. 물·촉촉한 새해/은하수 수영/분수 눈과 화이트 크리스마스/PET 대청소 문맥을 유지했다. 일본 명절 날짜와 두 달 간격을 한국 명절로 바꾸지 않았다. 말투·문화·용어는 인간 검토 대기이며 기존 넘버맨4649 승인을 전용하지 않는다.

## 빌드·검사

자산 `translations/aquaman_seasonal_ko.json`, 개별 수동 초안 직렬화 `tools/draft_aquaman_seasonal.py`.
이전 정크맨 누적 flags에 `--aquaman-seasonal`을 추가하여 immutable source에서 생성한다. 이전 patched ROM은 입력으로 쓰지 않는다.
43항목 원문/제어/숫자/조사 경계/glyph/3줄132px 범위/roundtrip 검사 통과. 최대131px. 관련118tests 통과.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일. 현재523Python 도구 drift=[], 원본 SHA 보존: `analysis/aquaman_seasonal_v1/final_identity_audit.json`.
이전 정크맨판37선택 archive payload와 선택 자산 해시를 실제ROM bytes까지 보존했다. 기존 그래픽15라벨/5블록의 위치·길이·SHA·실제ROM bytes 동일하며 ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 신규 전체 이미지 runtime QA를 뜻하지 않는다.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→새해3페이지 회귀를 controller 입력만으로 실행했다. 다른 후보 save/state를 가져오지 않았다. native save 성공script58과64KiB 저장 파일 SHA `6883a8a6ed4f62f1feb3b656d2ca0d976b52c4e0c16da349696e08fea0bf32f4`, 직후snapshot/현재디스크 동일성 확인. 다른 테스트 saves 보존. 한글 이름 persistence나 기존save 호환 증거는 아니다.
아쿠아맨 정상 해금 경로는 미확인이다. 신규6페이지는 격리된 renderer 진단이다. 같은 ROM 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰했고, 새해/칠석은 이 parent에서 각각 시작했다.
`capture_aquaman_seasonal_diagnostic.py --aqua-script 1/7`: PC08037F20,R0=08038278,R1=1,R3=52의 root read1회만 아쿠아맨 pool로 alias한다.7만 PC0804FB76,R0=pool,R1=2,R5=0200FA20의 requested1 offset read를 target7로1회 alias한다.1의 entry_aliases=0,7의 entry_aliases=1 확인. 원본 native caller/initializer와 normal-window prefix를 검사했다.
ROM/RAM 쓰기·날짜 변경 없고 alias는 제품ROM에 포함되지 않는다. 넘버맨 caller·초상이 유지되므로 정상 아쿠아맨 해금/초상/날짜 선택 증거는 아니다. 두 checkpoint는 diagnostic_checkpoint.mss로 격리하고 normal_play_checkpoint_eligible=false 기록.
새해3페이지와 칠석3페이지(각steps3..5)의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 검사 통과. 메인 에이전트가6페이지 화면을 직접 확인했다. 다른35문구(이름/성별 포함)와 동적 이벤트 이름 consumer는 static-only/미검증이다.
검사 `tools/report_aquaman_seasonal.py`; 결과 `analysis/aquaman_seasonal_v1/runtime.json`; 화면 `analysis/aquaman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_aquaman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,780, 미선택 일본어 포함28,229개/기타1,898개. 범위 기반 분류는 완역 분모나 완료율이 아니다.
다음 우드맨6A2184; intro69E088 화자와 native group 연결부터 확인한다.
전체 요청 미완료. 정상 아쿠아맨 해금·날짜·성별·이름 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이가 남아 있다.
