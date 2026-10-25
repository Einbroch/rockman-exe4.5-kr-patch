# 섀도맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_shadowman_seasonal_v1.gba`.
SHA256 `480dae114a8b4d0295cd25c7cfaf89a11def7373b6922d35892fc326559893d5`.
신규41 literal=39번역 문구+2유지 인용부호. 누적1,910선택 literal/41선택·691원본 유지 archive.

## 원본·번역 경계

source6AE834:1367bytes/21slots/root038414. Payload SHA `a6f7058c085d4c5e3a4f482f3c113af6c32b070862d7af76eaa899887e00b464`; TPL SHA `30564b461e20e340bf825d3065121d3cbb2a956f8a91d568cb3e2479672ecdfc`.
intro6AA1A0이 シャドーマン과 せっしゃ/そうろう 고풍스러운 말투를 명시한다. 원본 intro root0383E0=086AA1A0, native group+52/root038414=086AE834 확인.
IDs/원문/숫자/줄 수·newline 경계/명령/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 외에 script4의 원본 jump3도 bytes 그대로 유지. 이 archive에는 nickname 출력이나 global22 비교가 없다.
‘소인/그대/일세/구먼’은 원문 말투 기반 초안이다. バテレン은 기독교 신부 의미를 잃지 않게 ‘서양 신부들’로 옮겼다. 일본 옛 풍습과 마음, 산타를 서양 닌자로 여기는 농담/기척을 느끼지 못했다는 놀라움을 유지했다.
3월3일 복숭아꽃 명절/5월5일 일본 단오와 잉어 깃발의 폭포→용 전설→아들의 출세→부모의 소망 연결을 원래6페이지 흐름에 맞춰 번역했다. 생일마다 커지는 책임과 들뜨기만 할 수 없다는 경고도 유지했다.
대사창 폭에 맞춰5:0의 명절 서술,9:2의 기척을 못 느낀 놀라움,11:2의 나이 표현을 빌드 전에 수동으로 다듬었다. 원문/숫자/줄 수를 바꾸지 않았다. 문화/말투/명칭 인간 검토 대기, 넘버맨4649 승인을 전용하지 않는다.

## 빌드·검사

자산 `translations/shadowman_seasonal_ko.json`, 수동 작성 초안 직렬화 `tools/draft_shadowman_seasonal.py`.
기존 스타맨 누적 flags에 `--shadowman-seasonal`을 추가해 immutable source에서 생성한다. 이전 patched ROM은 입력으로 쓰지 않는다.
41항목 원문/제어/숫자/glyph/3줄132px 범위/roundtrip 관련127tests 통과. 최대129px.
static 검사는 원본과 대상 script4의23bytes가 동일함을 확인했다(SHA `24fa89146df5d3bb7f23fc0a181b0c648947ace5b2b7cd744f3121bbc36ab5d1`). 발렌타인 실제 호출/분기 runtime 증거로 확대하지 않는다.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일. 현재538Python 도구 drift=[], 원본 SHA 보존: `analysis/shadowman_seasonal_v1/final_identity_audit.json`. 원본/이전후보/실험/테스트 saves 보존.
이전 스타맨판40선택 archive payload와 선택 자산 해시를 실제ROM bytes까지 보존했다. 그래픽15라벨/5블록의 위치·길이·SHA·실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 신규 전체 이미지 runtime QA를 뜻하지 않는다.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. controller 입력만 사용했고 다른 후보 save/state를 가져오지 않았다. native save 성공script58과64KiB 파일 SHA `6883a8a6ed4f62f1feb3b656d2ca0d976b52c4e0c16da349696e08fea0bf32f4`, 직후snapshot/현재디스크 동일성 확인. 다른 테스트 saves 보존. 이전 후보와 저장 결과SHA가 같아도 이 ROM 자체 신규FF 파일에서 정상 생성했으며 파일을 가져오지 않았다. 한글 이름 persistence/기존save 호환 증거는 아니다.
신규9페이지는 정상 섀도맨 해금 경로가 아닌 격리 renderer 진단이다. 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰하고 exact-ROM/lookup receipt를 검사했다. 새해/잉어 깃발 설명은 같은 parent에서 각각 시작했다.
`capture_shadowman_seasonal_diagnostic.py --shadow-script 1/6`: PC08037F20,R0=08038278,R1=1,R3=52의 root read1회만 섀도맨 pool로 alias한다.6만 PC0804FB76,R0=pool,R1=2,R5=0200FA20의 requested1 offset read를 target6로1회 alias한다. 각 root_aliases=1,entry_aliases=0/1 확인. 원본 native caller/initializer와 normal-window prefix 검사. 넘버맨 caller·초상 유지, ROM/RAM 쓰기·날짜 변경 없음. alias는 제품ROM에 포함되지 않는다.
각 checkpoint는 diagnostic_checkpoint.mss로 격리하고 normal_play_checkpoint_eligible=false 기록. 정상 섀도맨 해금/초상/날짜 선택 증거는 아니다. 다른30문구와 발렌타인4→3 실제 호출/이벤트 이름 consumer는 static-only/미검증이다.
입력 사이300frame 대기는 기존 캡처 안정화 관찰에 따라 선택했다. 글리프/OBJ VRAM/화면 role colors 및 clearing 검사는 완화하지 않았다. 이번9페이지 모두 첫 촬영에서 엄격 검사 통과. 모든 전환 프레임·하드웨어·음성·실시간RTC 검증을 뜻하지 않는다.
새해3페이지 steps3..5/잉어 깃발6페이지 steps3..8의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 통과. 메인 에이전트가9페이지 화면 직접 확인.
검사 `tools/report_shadowman_seasonal.py`; 결과 `analysis/shadowman_seasonal_v1/runtime.json`; 화면 `analysis/shadowman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_shadowman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,910, 미선택 일본어 포함28,105개/기타1,892개. 범위 기반 분류는 완역 분모나 완료율이 아니다.
다음 나이트맨6BA3AC; intro6B5A70 화자/native group 연결부터 확인한다.
전체 요청 미완료. 정상 섀도맨 해금·날짜·발렌타인4→3 분기·이벤트 이름 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이가 남아 있다.
