# 블루스 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

최신 누적 ROM `poc/output/exe45_ko_development_blues_seasonal_v1.gba`.
SHA256 `a57a6cd7a68f926b18106ec4afc00371633ca12ce6987977143127dbfa3d7bda`.
신규33 literal=31개 번역 문구+2개 유지 인용부호. 누적1,661선택 literal/35선택·697원본 유지 archive.
이전 썬더맨판34개 선택 archive payload와 선택 번역·이미지 자산을 실제ROM bytes/해시까지 보존했다.

## 원본·번역 경계

source685C68:1201bytes/21slots/root038270. Payload SHA `f0f6a9a5af8202801fb267770735dbbbe490c2abce6e45469059f3d6b15fab76`; TPL SHA `d0c842e509eeb40e58f152cf111834a27675eb315f9843419e3b835276f87659`.
intro681AB8 원문이 ブルース를 명시하며 정중한 오퍼레이터 인사를 사용한다. 원본 intro root03823C=08681AB8, native group+52/root038270=08685C68 확인.
새해/첫 참배/절분/발렌타인 성별 분기/히나마쓰리/5월5일/칠석/성탄절/연말/생일/학교 창립 기념일/동적 이벤트 안내를 번역했다.
source/IDs/21slots/줄 수 및 선행·후행 newline/명령/global22/날짜/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20도 유지됐다.
성탄절9:1의25와3월3일/5월5일/7월7일 숫자를 유지했다. single-line 절분2:0/연말10:0에도 줄을 추가하지 않았다.
Hatsumode는 새해 첫 참배, 히나아라레는 이름 유지, Momo no Sekku는 복숭아꽃 절기로 표현한 초안이다. 일본 단오절은 원본5월5일/어린이날 맥락을 유지했으며 한국 음력 단오를 뜻한다는 주장이 아니다. 문화·용어·정중한 말투는 인간 검토 대기.
원본 산타로 오해받는 색깔 농담과25일의 축제 후 쓸쓸함을 유지했다. 이름 입력·저장 형식·RTC·게임 진행 코드는 바꾸지 않았다. 기존4649 승인 표현도 보존했다.

## 빌드·검사

자산 `translations/blues_seasonal_ko.json`, 개별 수동 초안 직렬화 `tools/draft_blues_seasonal.py`.
이전 `analysis/THUNDERMAN_SEASONAL_ROM_HANDOFF.md`의 모든 누적 flags에 `--blues-seasonal`을 추가해 `tools/build_roll_pet.py --work FRESH --out FRESH.gba`로 immutable source에서 재생성한다. 이전 patched ROM을 입력으로 쓰지 않는다.
33항목 원문/제어/숫자/glyph/3줄132px 채택 범위/native·semantic·binary roundtrip 통과. 최대132px.
관련109tests 통과. 숫자25 제거와 single-line 연말 인사에 줄 추가를 거부하는 테스트 포함.
main·`_repro`·`_current_repro` 3독립 빌드 동일 SHA. 원본 SHA 보존, 현재508Python 도구 drift=[]: `analysis/blues_seasonal_v1/final_identity_audit.json`.
기존 그래픽15라벨/5블록(calendar frequency5/PET menu7/attack caption1/save title1/equipment title1)의 위치·길이·SHA 및 실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 전체 이미지 신규 runtime QA 주장은 아니다.
원본/이전 후보/실험/isolated test saves는 보존했다. 배포용 패치 또는 release 판정 없음.

## 정상 실행과 진단 구분

`run_numberman_seasonal_normal.py --stem exe45_ko_development_blues_seasonal_v1 --prefix blues-seasonal-v1-`로 자체 cold 시작→넘버맨 첫 선택→정상 게임 저장→checkpoint 없는 cold 이어하기→내비 재선택을 controller 입력만으로 수행했다.
64KiB native save가 FF 초기 상태에서 SHA `674e4dc5a74dd9d05419d2d564196363e1c38381bbe08719d111c39fcde056c9`로 바뀌었다. save-success58 및 직후snapshot/현재디스크 동일성 확인. 다른 테스트 saves는 보존했다. 이전 썬더맨판과 저장 결과 SHA는 같지만 해당 save를 가져오지 않았으며 신규 basename의FF 초기화→자체 저장을 확인했다. 한글 이름 persistence나 기존save 호환 증거가 아니다.
같은 ROM 정상 넘버맨 새해3페이지 회귀 통과. 다른 후보 checkpoint/save를 가져오지 않았다.

블루스 정상 해금 경로는 미확인이다. 신규 화면은 격리된 renderer 진단이다.
자체 normal-reload-select 대사 load 이전 checkpoint로 실제 넘버맨 seasonal root0382AC read를 먼저 관찰한 뒤, exact-ROM/lookup receipt를 검사한다.
`capture_blues_seasonal_diagnostic.py`는 같은 pre-load parent에서 PC08037F20,R0=08038278,R1=1,R3=52의 root read1회만 블루스 pool로 alias한다. native caller/initializer 원본 bytes를 검사하며 script1/normal window/consumer, 넘버맨 caller·초상은 유지한다. ROM/RAM 쓰기·날짜 변경 없음; alias는 제품ROM에 포함되지 않는다.
새해4페이지 steps4..7의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 검사 통과.132px 경계 줄을 포함해 메인 에이전트가 화면을 직접 확인했다.
diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false. 정상 플레이 후속 state로 사용하지 않는다.
이는 정상 블루스 해금·초상·날짜 선택 증거가 아니다. 다른27문구(생일/성별 포함)와 동적 이벤트 이름 및 다른 날짜 분기는 static-only/미검증이다.
검사 `tools/report_blues_seasonal.py`; 결과 `analysis/blues_seasonal_v1/runtime.json`; 화면 `analysis/blues_seasonal_v1/diagnostic_new_year_pages.png`.

## 계속할 작업

최신 catalogue `analysis/full_scope_blues_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,661, 미선택 일본어 포함28,342개/기타1,904개. 범위 기반 분류는 완역 분모나 완료율이 아니다. 전체 요청은 아직 완료되지 않았다.
다음 기념일 대사는 메탈맨691A64; intro68D3C8 화자와 native group 연결부터 확인한다.
가장 어려운 완료 조건: 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환. 전체 graphics/inline/fixed-string population과 이전 native wait-arrow53pixel 차이도 미해결.
