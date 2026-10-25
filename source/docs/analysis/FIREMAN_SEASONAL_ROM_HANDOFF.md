# 파이어맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

최신 누적 ROM: `poc/output/exe45_ko_development_fireman_seasonal_v1.gba`.
SHA256 `45086b944e2919f245ed8f63b80dde7cc2a3f22fb3209a012e5d6770cfe726c8`.
서치맨 누적판의32개 선택 archive payload와 선택 번역·이미지 자산 해시를 유지하고 파이어맨67AE2C를 추가했다.
신규47 literal=44개 번역 문구+3개 유지 인용부호/느낌표. 누적1,594선택 literal/33선택·699원본 유지 archive.
새해/절분/발렌타인 성별 분기/히나마쓰리/5월5일/칠석/성탄절/연말/생일/창립 기념일/동적 이벤트 안내를 포함한다.

## 원본과 경계 보호

source67AE2C:1444bytes/21slots/root0381F8. Payload SHA `fafc655f894bd17db372edc40aac995818f27cc1efcb785612f123bb2270397e`; TPL SHA `f070365660835b10eb2705529fd965061ffac7d847c3a36099a5218006d16ef7`.
intro676AE4 원문이 파이어맨을 명시한다. native60byte Navi group에서 intro pointer+52가 seasonal pointer이다.
source/IDs/21slots/줄 수 및 선행·후행 newline/명령/global22 성별 분기/날짜/이벤트 이름 buffer·loop를 보존했다. 빈0/13/14/15와 없는16/20도 유지됐다.
생일script11은 이름을 두 번 출력한다. literal11:3의 leading newline,11:4의 trailing newline,11:5의 단일 ‘!’를 유지했다. nickname_suffix_profiles로 empty 첫 줄과 단일 느낌표를 source/target 정확히 고정했다. 이 경계 검사는 한글 이름 입력·저장 지원 또는 생일 이름 표시의 실제 실행 증거가 아니다.
report_roll_pet.static은 11:5의 중복 느낌표를 임의의 첫 일치로 선택하지 않는다. source/compiled script11의 F9 0C 01(printPlayerNickname)+‘!’+E6 00 F1(keyWait/clearMsg) anchor가 각각 정확히1회인지 확인하고 scalar glyph stream을 연결한다. 다른 문구나 전역 literal 규칙을 느슨하게 하지 않았다.
이름 입력·저장 형식·RTC·게임 진행 코드를 바꾸지 않았다. 기존 넘버맨4649 승인 표현도 그대로 유지했다.
불꽃/꼬리/초콜릿 농담, 파이어/버닝 외침과 거친 말투는 문맥 초안이다. 등롱/히나 인형/전뇌 아마자케/일본 명절 날짜를 다른 한국 명절로 대체하지 않았다. おだいりさま의 ‘임금님 인형’, 직녀/견우 이야기와 문화/말투는 인간 검토 대기다.

## 빌드와 검사

자산 `translations/fireman_seasonal_ko.json`; source identity 기반 수동 초안 직렬화 `tools/draft_fireman_seasonal.py`.
이전 `analysis/SEARCHMAN_SEASONAL_ROM_HANDOFF.md`의 모든 누적 flags에 `--fireman-seasonal`을 추가하고 `tools/build_roll_pet.py --work FRESH --out FRESH.gba`로 immutable source에서 재생성한다. 이전 patched ROM을 입력으로 쓰지 않는다.
전체47 literal source/controls/numerals/glyph/3줄132px 채택 범위/native·semantic·binary roundtrip 통과. 최대132px.
관련103tests 통과. 생일 leading/trailing newline 뒤집기와 느낌표 증가를 거부하는 테스트를 포함한다.
main·`_repro`·`_current_repro` 3독립 빌드 동일 SHA, 원본 SHA 보존, 현재498Python 도구 drift=[]: `analysis/fireman_seasonal_v1/final_identity_audit.json`.
최종 도구 identity는 `_current_repro` manifest 기준이다. 원본/이전 후보/실험/isolated test save는 보존했다. 배포용 패치 또는 release 판정은 만들지 않았다.
기존32 payload는 실제 ROM bytes까지 동일하다. 선택 자산 해시도 유지됐다.
기존 그래픽15라벨/5블록(calendar frequency5/PET menu7/attack caption1/save title1/equipment title1)의 위치·길이·SHA와 실제 ROM bytes가 이전 누적판과 동일하다. ‘통신’의 기존 glyph override도 유지된다. 전체 이미지 미번역 해소나 모든 이미지의 신규 runtime QA 주장은 아니다.

## 실행 검증과 진단 구분

`run_numberman_seasonal_normal.py --stem exe45_ko_development_fireman_seasonal_v1 --prefix fireman-seasonal-v1-`로 자체 cold 시작→넘버맨 첫 선택→정상 게임 저장→checkpoint 없는 cold 이어하기→내비 재선택을 일반 controller 입력으로 실행했다.
64KiB native save가 FF 초기 상태에서 SHA `5bc0c601068efe7ef6aabf0f20f6b99e11e4bce8c6e9cb9cbfd00bc50f70e618`로 바뀌었다. save-success58 및 저장 직후 snapshot/현재 디스크 동일성을 확인했고 다른 테스트 saves는 보존했다. 한글 이름 persistence 또는 기존save 호환 증거가 아니다.
같은 누적 ROM 정상 넘버맨 새해3페이지 회귀 통과. 다른 후보 checkpoint/save를 가져오지 않았다.

파이어맨 정상 해금 경로는 미확인이다. 신규 화면은 **격리된 렌더링 진단**이다.
자체 normal-reload-select는 대사 load 이전 checkpoint이다. capture_seasonal_lookup.py로 실제 넘버맨 seasonal root0382AC read를 먼저 관찰하고 exact ROM/receipt를 확인했다: PC08037F20,R0=08038278,R1=1,R3=52.
capture_fireman_seasonal_diagnostic.py는 같은 pre-load parent에서 해당 root read1회만 파이어맨 pool로 alias한다. script1과 normal window/consumer, 넘버맨 caller·초상은 그대로다. source native caller/initializer bytes가 같아야 실행한다. ROM/RAM 직접 쓰기·날짜 변경 없이 실행했으며 alias는 제품 ROM에 포함되지 않는다.
진단 새해3페이지(steps3..5)의 font CPU read→ROM glyph→OBJ VRAM→화면 픽셀, 페이지 순서/빈 영역 clearing/종료 검사가 통과했다.
diagnostic_checkpoint.mss로 격리하고 normal_play_checkpoint_eligible=false를 기록했다. 정상 플레이 후속 state로 사용하지 않는다.
정상 파이어맨 해금·초상·날짜별 이벤트 진입을 검증한 것으로 해석하지 않는다. 다른41문구(생일 nickname·성별 포함), 동적 이벤트 이름과 다른 날짜 분기는 static-only/미검증이다.
검사 `tools/report_fireman_seasonal.py`, 결과 `analysis/fireman_seasonal_v1/runtime.json`, 화면 `analysis/fireman_seasonal_v1/diagnostic_new_year_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_fireman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,594, 미선택 일본어 포함28,405개/기타1,908개. 범위 기반 분류는 완역 분모나 완료율이 아니다. 사용자 전체 요청은 아직 완료되지 않았다.
다음 기념일 대사는 썬더맨680454이며 source intro67C4CC의 화자와 native group 연결부터 확인한다.
가장 어려운 완료 조건: 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환. 전체 graphics/inline/fixed-string population과 이전 native wait-arrow53pixel 차이도 미해결이다.
