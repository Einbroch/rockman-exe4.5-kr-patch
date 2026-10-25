# 메탈맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

최신 누적 ROM `poc/output/exe45_ko_development_metalman_seasonal_v1.gba`.
SHA256 `74558c971f1761de0f0b12fb7cb7b62c54a8e9c64420fe4921d5521b5f8c9820`.
신규39 literal=37개 번역 문구+2개 유지 인용부호. 누적1,700선택 literal/36선택·696원본 유지 archive.
이전 블루스판35개 선택 archive payload와 선택 번역·이미지 자산을 실제ROM bytes/해시까지 보존했다.

## 원본·번역 경계

source691A64:1307bytes/21slots/root0382E8. Payload SHA `e06df11b3698486af660647df841f64e865c0bc915c899e0ee93bf07b18c0afd`; TPL SHA `039711e89b466224d4a84a9c52891b90aa4a4c0bc797842cb15ef3644bbcef8d`.
intro68D3C8 원문이 メタルマン을 명시하며 주먹을 갈고닦는 주제를 제시한다. 원본 intro root0382B4=0868D3C8, native group+52/root0382E8=08691A64 확인.
새해/절분/발렌타인 성별 분기/히나마쓰리/5월5일/칠석/성탄절/연말/생일/학교 창립 기념일/동적 이벤트 안내를 번역했다.
source/IDs/21slots/줄 수 및 선행·후행 newline/명령/global22/날짜/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20도 유지됐다.
새해1:0/생일11:0은 native printPlayerNickname 뒤의 첫 줄 ‘、’를 source/target 모두11px로 유지했다. nickname_suffix_profiles로 경계를 고정했다. 이름을 넣는 실제 페이지나 한글 이름 지원이 검증됐다는 뜻은 아니다.
5월5일과12월24일/25일/31일 숫자를 유지했다. single-line 절분/히나마쓰리/칠석/질문/학교 휴일 문구의 줄 수도 보존했다.
오미소카/미소카의 일본어 설명에는 해당 용어와 섣달그믐을 함께 제시했다. 한국어 ‘섣달그믐’의 어원처럼 바꾸지 않았으며 문화·표현·단단한 비존대 말투는 인간 검토 대기 초안이다.
일본 명절 맥락/직녀·견우 이야기, 의리 초콜릿 경고 및 산타 침입·도주 농담을 유지했다. 이름 입력·저장 형식·RTC·게임 진행 코드 변경 없음. 기존4649 승인 표현도 유지했다.

## 빌드·검사

자산 `translations/metalman_seasonal_ko.json`, 개별 수동 초안 직렬화 `tools/draft_metalman_seasonal.py`.
이전 `analysis/BLUES_SEASONAL_ROM_HANDOFF.md`의 모든 누적 flags에 `--metalman-seasonal`을 추가해 `tools/build_roll_pet.py --work FRESH --out FRESH.gba`로 immutable source에서 재생성한다. 이전 patched ROM을 입력으로 쓰지 않는다.
39항목 원문/제어/숫자/glyph/3줄132px 채택 범위/native·semantic·binary roundtrip 통과. 최대124px.
관련112tests 통과. 두 nickname 첫 줄의 쉼표를 한국어 호격으로 늘리거나12월24일을25일로 바꾸는 입력을 거부하는 테스트 포함.
main·`_repro`·`_current_repro` 3독립 빌드 동일 SHA. 원본 SHA 보존, 현재513Python 도구 drift=[]: `analysis/metalman_seasonal_v1/final_identity_audit.json`.
최종 tool identity는 `_current_repro` manifest 기준이다. 첫 빌드 도중 새 report의 환경 파일명 연결을 정정했으며 ROM 생성 내용은 바뀌지 않았다. 이후 재빌드와 최종 정합성 검사를 통과했다.
기존 그래픽15라벨/5블록(calendar frequency5/PET menu7/attack caption1/save title1/equipment title1)의 위치·길이·SHA 및 실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 전체 이미지 신규 runtime QA 주장은 아니다.
원본/이전 후보/실험/isolated test saves 보존. 배포용 패치 또는 release 판정 없음.

## 정상 실행과 진단 구분

`run_numberman_seasonal_normal.py --stem exe45_ko_development_metalman_seasonal_v1 --prefix metalman-seasonal-v1-`로 자체 cold 시작→넘버맨 첫 선택→정상 게임 저장→checkpoint 없는 cold 이어하기→내비 재선택을 controller 입력만으로 수행했다.
64KiB native save가 FF 초기 상태에서 SHA `79c80cd93ae6753625191cffa63d0c12356bc3106c9fd4d55e0fcd79c66d124a`로 바뀌었다. save-success58 및 직후snapshot/현재디스크 동일성 확인. 다른 테스트 saves 보존. 한글 이름 persistence나 기존save 호환 증거가 아니다.
같은 ROM 정상 넘버맨 새해3페이지 회귀 통과. 다른 후보 checkpoint/save를 가져오지 않았다.

메탈맨 정상 해금 경로는 미확인이다. 신규 화면은 격리된 renderer 진단이다. 이름 출력 페이지를 임의로 제외해 새해 전체 검증으로 처리하지 않고, 이름 출력이 없는 절분script2를 별도 검증 대상으로 택했다.
자체 normal-reload-select 대사 load 이전 checkpoint로 실제 넘버맨 seasonal root0382AC read를 먼저 관찰한 뒤 exact-ROM/lookup receipt를 검사한다.
`capture_metalman_seasonal_diagnostic.py --metal-script 2`는 같은 pre-load parent에서 PC08037F20,R0=08038278,R1=1,R3=52의 root read1회만 메탈맨 pool로 alias한다. 이어 PC0804FB76,R0=pool,R1=2,R5=0200FA20의 pool+2 offset read1회만 요청script1에서 targetscript2 offset으로 alias한다. 두 alias 모두1회임을 확인했다.
native caller/initializer 원본 bytes와 script2 normal-window prefix를 검사한다. FA21 requested1/넘버맨 caller·초상은 유지되고 메탈맨script2가 native window/consumer에서 실행된다. ROM/RAM 쓰기·날짜 변경 없음; alias는 제품ROM에 포함되지 않는다.
절분3페이지 steps3..5의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 검사 통과. 메인 에이전트가 화면도 직접 확인했다.
diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false. 정상 플레이 후속 state로 사용하지 않는다.
이는 정상 메탈맨 해금·초상·날짜 선택 증거가 아니다. 다른34문구(새해/생일 이름·성별 포함)와 동적 이벤트 이름 및 다른 날짜 분기는 static-only/미검증이다.
검사 `tools/report_metalman_seasonal.py`; 결과 `analysis/metalman_seasonal_v1/runtime.json`; 화면 `analysis/metalman_seasonal_v1/diagnostic_setsubun_pages.png`.

## 계속할 작업

최신 catalogue `analysis/full_scope_metalman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,700, 미선택 일본어 포함28,305개/기타1,902개. 범위 기반 분류는 완역 분모나 완료율이 아니다. 전체 요청은 아직 완료되지 않았다.
다음 기념일 대사는 정크맨696DD8; intro69303C 화자와 native group 연결부터 확인한다.
가장 어려운 완료 조건: 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환. 전체 graphics/inline/fixed-string population과 이전 native wait-arrow53pixel 차이도 미해결.
