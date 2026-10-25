# 정크맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_junkman_seasonal_v1.gba`.
SHA256 `59ea4b8d2281d2ee1addd58de2c8b84492c417bfc993f4f53d95f41cf2bf87e7`.
신규37 literal=35개 번역 문구+2개 유지 인용부호. 누적1,737선택 literal/37선택·695원본 유지 archive.
이전 메탈맨판36개 선택 archive payload와 선택 번역·이미지 자산을 실제ROM bytes/해시까지 보존했다.

## 원본·번역 경계

source696DD8:1168bytes/21slots/root038324. Payload SHA `919820b50b476172c3c5b71d386f908e265a53ec42635643eb54aa3447670ba3`; TPL SHA `622cf5381e7d94bb69db90754efce6479b21da01a48558a0327eeb72ae13ad62`.
intro69303C 원문이 ジャンクマン을 명시하며 내비가 된 부끄러움과 버림받을까 하는 걱정을 보여 준다. 원본 intro root0382F0=0869303C, native group+52/root038324=08696DD8 확인.
source/IDs/21slots/줄 수 및 선행·후행 newline/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지.
생일11:0 native printPlayerNickname 뒤 첫 줄 ‘、’를 source/target 모두11px로 유지하고 nickname_suffix_profiles로 고정했다. 실제 이름 출력이나 한글 이름 지원 검증을 뜻하지 않는다.
평소 source-scoped hesitations와 칠석7:3의 일시적으로 또렷한 질문,7:4의 깨달음을 개별 번역했다. 무조건 모든 문구에 더듬거림을 넣는 규칙은 사용하지 않았다.
696DD8:4:2 チョコ/チョコット 말장난은 ‘초콜릿 못 받아/조금 쓸쓸해’로 뜻만 옮긴 초안이며 말장난은 재현되지 않았다. 인간 표현·각색 검토 필요. 넘버맨4649 승인을 전용하지 않았으며 배포 적격으로 승격하지 않는다.
일본 명절/히나 인형/제야의 종 맥락 유지. ‘정크 프레스’는 원문 기반 명칭 초안이고 말투·문화·용어는 인간 검토 대기다. 이름 입력·저장 형식·RTC·게임 진행 코드 변경 없음.

## 빌드·검사

자산 `translations/junkman_seasonal_ko.json`, 개별 수동 초안 직렬화 `tools/draft_junkman_seasonal.py`.
이전 `analysis/METALMAN_SEASONAL_ROM_HANDOFF.md`의 모든 누적 flags에 `--junkman-seasonal`을 추가하고 `tools/build_roll_pet.py --work FRESH --out FRESH.gba`로 immutable source에서 재생성한다. 이전 patched ROM은 입력으로 쓰지 않는다.
37항목 원문/제어/숫자/glyph/3줄132px 채택 범위/native·semantic·binary roundtrip 통과. 최대132px.
초기 초안2:1의144px 문구는 주어가 자연스럽게 생략되는 ‘도깨비가 무서워・・・’로 수동 재작성했다.9:0의134px은 더듬거림과 느낌표를 유지한 ‘메,메리 크리스마스!’ 배치로 수정했다. 원문이나 줄 수 변경 없이 빌드 전에 테스트를 통과했다.
관련115tests 통과. birthday comma 경계, single-line 보존 및 칠석의 fluent voice 초안 고정 검사 포함.
main·`_repro`·`_current_repro` 3독립 빌드 동일 SHA. 원본 SHA 보존, 현재518Python 도구 drift=[]: `analysis/junkman_seasonal_v1/final_identity_audit.json`.
기존 그래픽15라벨/5블록(calendar frequency5/PET menu7/attack caption1/save title1/equipment title1)의 위치·길이·SHA 및 실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 전체 이미지 신규 runtime QA 주장은 아니다.
원본/이전 후보/실험/isolated test saves 보존. 배포용 패치 또는 release 판정 없음.

## 정상 실행과 진단 구분

`run_numberman_seasonal_normal.py --stem exe45_ko_development_junkman_seasonal_v1 --prefix junkman-seasonal-v1-`로 자체 cold 시작→넘버맨 첫 선택→정상 저장→checkpoint 없는 cold 이어하기→내비 재선택을 controller 입력만으로 수행했다.
64KiB native save가 FF 초기 상태에서 SHA `7cf71e6b1961ea7d4e136650401917c5e9a17f9071c780efa18d3a5025b68e02`로 바뀌었다. save-success58 및 직후snapshot/현재디스크 동일성 확인. 다른 테스트 saves 보존. 한글 이름 persistence나 기존save 호환 증거는 아니다.
같은 ROM 정상 넘버맨 새해3페이지 회귀 통과. 다른 후보 checkpoint/save를 가져오지 않았다.

정크맨 정상 해금 경로는 미확인이다. 신규8페이지는 격리된 renderer 진단이다.
자체 normal-reload-select 대사 load 이전 checkpoint에서 실제 넘버맨 seasonal root0382AC read를 먼저 관찰하고 exact-ROM/lookup receipt를 검사한다. 두 진단은 이 같은 정상 parent에서 각각 시작하며 diagnostic child를 정상 후속 state로 쓰지 않는다.
`capture_junkman_seasonal_diagnostic.py --junk-script 1/7`은 PC08037F20,R0=08038278,R1=1,R3=52의 root read1회만 정크맨 pool로 alias한다.7만 추가로 PC0804FB76,R0=pool,R1=2,R5=0200FA20의 pool+2 requested1 offset read를 target7로1회 alias한다.1의 entry_aliases=0,7의 entry_aliases=1 확인.
native caller/initializer 원본 bytes와 대상 normal-window prefix 검사. FA21 requested1/넘버맨 caller·초상 유지; 정크맨script1/7은 native window/consumer에서 실행된다. ROM/RAM 쓰기·날짜 변경 없음; alias는 제품ROM에 포함되지 않는다.
새해3페이지 steps3..5, 칠석5페이지 steps3..7의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 검사 통과.132px 경계와 또렷한 질문 페이지를 포함해 메인 에이전트가 화면을 직접 확인했다.
각 checkpoint는 diagnostic_checkpoint.mss로 격리, normal_play_checkpoint_eligible=false 기록.
이는 정상 정크맨 해금·초상·날짜 선택 증거가 아니다. 다른27문구(생일 이름/성별 포함)와 동적 이벤트 이름 및 다른 날짜 분기는 static-only/미검증이다.
검사 `tools/report_junkman_seasonal.py`; 결과 `analysis/junkman_seasonal_v1/runtime.json`; 화면 `analysis/junkman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 계속할 작업

최신 catalogue `analysis/full_scope_junkman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,737, 미선택 일본어 포함28,270개/기타1,900개. 범위 기반 분류는 완역 분모나 완료율이 아니다. 전체 요청은 아직 완료되지 않았다.
다음 기념일 대사는 아쿠아맨69C9F4; intro698424 화자와 native group 연결부터 확인한다.
가장 어려운 완료 조건: 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환. 전체 graphics/inline/fixed-string population과 이전 native wait-arrow53pixel 차이도 미해결.
