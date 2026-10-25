# 일렉맨 기념일·생일 대사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_elecman_seasonal_v1.gba`.
SHA256 `9772ae035ea240f239664c29008ff7d96137250e74001b656adab9a1a8a55f93`.
신규40 literal=38번역 문구+2유지 인용부호. 누적2,064선택 literal/45선택·687원본 유지 archive.

## 원본·번역 경계

source6CB184:1340bytes/21slots/root038504. Payload SHA `8680c27d7155f430cd1e739b0e770ccb72822c744471144008546f423963d257`; TPL SHA `713d09a2ee410de78b1a9406fc617a8c09516c7e37b169eadd7f2766e515ff8b`.
intro6C7084은 エレキマン과 자극적인 일상을 함께 보내자는 절제된 말투를 명시한다. 원본 intro root0384D0=086C7084, native group+52/root038504=086CB184 확인.
IDs/원문/숫자/줄 수·newline 경계/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지. nickname 삽입 없음.
절분은 머리 양쪽이 뾰족해도 도깨비가 아니고 전기를 다뤄도 천둥신은 아니라는 부정 뒤 썬더맨이 더 도깨비 같다고 한다. カミナリ의 신 의미는 [漢字ペディア sense2](https://www.kanjipedia.jp/kotoba/0007025300)에 있다. 이 장면에서 해당 의미를 고른 것은 머리/도깨비/전기 대비 문맥에서의 추론이며 인간 검토 대기다.
의리 초콜릿1개/성별 분기, 히나 등 촛불→전구, 잉어 깃발 조명 제안, 칠석 불을 끄고 은하수 보기,24일 크리스마스 절정/25일 밤 장식 철거/1년 중 가장 쓸쓸함을 유지했다. 전기 안전성은 원문 화자의 주장으로 보존하며 현실 안전 안내가 아니다.
연말 리셋 호언은 싫고 힘들었던 기억을 가리킨다. 실제 게임 저장 삭제 지시로 바꾸지 않았다. 생일에 특별한 선물이 없다는 의미 유지. 명칭·말투·문화 초안 인간 검토 대기, 넘버맨4649 승인 전용 없음.

## 빌드·검사

자산 `translations/elecman_seasonal_ko.json`, 개별 작성 초안 직렬화 `tools/draft_elecman_seasonal.py`.
기존 아이스맨 flags에 `--elecman-seasonal` 추가, immutable source에서 빌드. 이전 patched ROM을 입력으로 사용하지 않는다.
40항목 원문/제어/숫자/glyph/3줄132px/roundtrip와139tests 통과. 최대132px는8:0 단일 행 크리스마스이브 대사다. native·semantic·binary roundtrip 통과.
main·`_repro`·최종`_current_repro_r2` 3독립 빌드 SHA 동일.558Python 도구 drift=[], 원본 SHA 보존: `analysis/elecman_seasonal_v1/final_identity_audit.json`.
132px 대사8:0 발견 후 같은 ROM에서 diagnostic script8을 추가했다. 첫`_current_repro`는 확장 전 도구 metadata를 보존하며 ROM bytes는 동일하다. 최신 도구 identity 증거는`_current_repro_r2`이다. 이전 파일을 삭제하거나 통과 증거로 재명명하지 않았다.
이전 아이스맨판44선택 archive payload와 선택 자산 SHA 보존. 그래픽15라벨/5블록 위치·길이·SHA·실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 신규 전체 이미지 runtime QA를 뜻하지 않는다. 원본·이전후보·실험·테스트 saves 보존.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. controller 입력만 사용, 다른 후보 save/state 미수입. fresh FF64KiB에서 native save 성공script58 확인. 저장 SHA `9929f373bb564064efd13b73ae9efe0b10c626d369b94f741bfd532fd01259bb`, 직후snapshot/현재디스크 동일. 다른 테스트 saves 보존. 한글 이름 persistence/기존save 호환 증거는 아니다.
신규12페이지는 격리 renderer 진단이다. 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰하고 exact-ROM/lookup receipt 검사. 절분/크리스마스/이브 각각 동일 parent에서 시작했다.
`capture_elecman_seasonal_diagnostic.py --elec-script 2/9/8`: PC08037F20,R0=08038278,R1=1,R3=52 root read1회만 일렉맨 pool로 alias. PC0804FB76,R0=pool,R1=2,R5=0200FA20 requested1 offset read를 target2/9/8으로 각각1회 alias. 각 root_aliases=1,entry_aliases=1. 원본 caller/initializer·normal-window prefix 검사. 넘버맨 caller·초상 유지, ROM/RAM 쓰기·날짜 변경 없음. alias는 제품ROM에 포함되지 않는다.
checkpoint는 diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false. 정상 일렉맨 해금/초상/날짜 선택 증거 아님. 다른26문구/성별·이벤트 이름 consumer는 static-only.
입력 사이300frame 대기. 절분6페이지 steps3..8/크리스마스4페이지 steps3..6/이브2페이지 steps3..4의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 모두 첫 촬영 strict 검사 통과.8:0 단일 행132px 경계도 포함한다. 메인 에이전트12페이지 화면 직접 확인. 검사 완화 없음; 전환 전 프레임·하드웨어·음성·실시간RTC 증거 아님.
검사 `tools/report_elecman_seasonal.py`; 결과 `analysis/elecman_seasonal_v1/runtime.json`; 화면 `analysis/elecman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_elecman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택2,064, 미선택 일본어 포함27,960개/기타1,883개. 범위 기반 분류는 완역 분모나 완료율 아님.
다음 플랜트맨6D0ADC; intro6CC808/seasonal TPL 전체를 이번에 읽었다. 이름 뒤1:0/11:0 쉼표 경계, 가가미모치의 다이다이(橙/代々)·대대로 번영 말장난, 볶은 콩/싹,식물·꽃의 비유, 일본 단오/날짜/숫자 보존 필요. 아직 번역·빌드 입력 미작성.
전체 요청 미완료. 정상 일렉맨 해금·날짜·성별·이벤트 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이 미해결.
