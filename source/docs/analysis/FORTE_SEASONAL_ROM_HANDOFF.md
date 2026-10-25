# 포르테 기념일·생일 대사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_forte_seasonal_v1.gba`.
SHA256 `692566c04c780b29131154a7d015e22192c88f3e7858c2858b972977d0fc60d0`.
신규33 literal=30번역 문구+2유지 인용부호+1유지 여섯 점 침묵. 누적2,140선택 literal/47선택·685원본 유지 archive.

## 원본·번역 경계

source6D5A9C:1042bytes/21slots/root03857C. Payload SHA `56a0883fa115c2101bcd78178458caae82213a8ca43889afbc76199e7f933e2a`; TPL SHA `05c158cc9a64bd38ace280249110baa33835fadc88d3a4f864c8a31ed97df6c6`.
intro6D2180/root038548, jack-in6D27A0/root038558, seasonal6D5A9C/root03857C의 같은 native60byte group 관계와 jack-in의 フォルテ.EXE 명시로 화자를 확인했다. 세 TPL 전체를 읽었다.
IDs/원문/숫자/줄 수·newline 경계/명령/global22 성별 분기/이벤트 이름 buffer·loop 보존. 이름 삽입 없음.0/13/14/15 명령 전용과 없는16/20 보존.
새해는 새로운 전투의 시작, 발렌타인은 초콜릿을 빼앗거나 힘으로라도 건네라는 거친 캐릭터 발언, 갑옷은 싸움의 날로 오해, 칠석은 소원을 빌지 않고 자기 힘으로 이룬다는 원문을 유지했다. 생일은 날짜를 기억할 뿐 축하나 친밀감을 추가하지 않았다. 별도 침묵1:2의 native 여섯 점을 그대로 유지했다. 문화·용어·말투 초안 인간 검토 대기. 넘버맨4649 승인은 다른 문구에 전용하지 않았다.

## 빌드·검사

자산 `translations/forte_seasonal_ko.json`, 개별 작성 초안 직렬화 `tools/draft_forte_seasonal.py`. 기존 플랜트맨 flags에 `--forte-seasonal` 추가, immutable original에서 빌드. 이전 patched ROM을 입력으로 쓰지 않았다.
33항목 원문/제어/숫자/glyph/3줄132px/roundtrip와145관련 tests 통과. 실제 최대129px는8:0 크리스마스이브 한 줄이며 이번 진단에 포함했다. native·semantic·binary roundtrip 통과.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일.568Python 도구 drift=[], 원본 SHA 보존: `analysis/forte_seasonal_v1/final_identity_audit.json`.
이전 플랜트맨46선택 archive payload와 선택 자산 SHA 보존. 그래픽15라벨/5블록 위치·길이·SHA·실제 ROM bytes 동일. ‘통신’ glyph override 유지. 신규 전체 이미지 검증이나 전체 이미지 완역을 뜻하지 않는다. 원본·이전 후보·실험·테스트 saves 보존.

## 넘버맨 화면과 실제 ROM 대사 연결

사용자 질문: 진단 스크린샷의 캐릭터가 넘버맨이면 확인 후 넘버맨 대사로 되돌리는가?
되돌리는 ROM 수정은 필요 없다. 진단 Lua가 실행 중 특정 ROM 읽기의 반환값만 임시로 바꾼다. ROM/RAM 쓰기나 날짜 변경이 없으며, 이 진단 연결은 ROM 파일에 포함되지 않는다. 진단 state는 `diagnostic_checkpoint.mss`로 격리하고 normal_play_checkpoint_eligible=false로 표시해 정상 플레이 경로에 재사용하지 않았다.
실제 후보 ROM에서 native root0382AC→0880CAD0은 넘버맨68BBB4 자신의 pool, root03857C→0881465C는 포르테6D5A9C 자신의 pool임을 별도 assertion으로 확인했다. `runtime.json`의 native_navi_bindings와 diagnostic_aliases_embedded_in_rom=false 참조.
이 후보 자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. 정상 실행 Lua는 controller 입력만 사용하며 read alias/ROM·RAM 쓰기 없음. 첫 정상 대사 화면 `poc/runtime/forte-seasonal-v1-normal-return/step_003.png`는 ‘새해 복 많이 받으세요’이다.
fresh FF64KiB에서 native save 성공script58 확인. 저장 SHA `5decd6c04414c022c20702a8d9ad76763cd877cc90ebadf437f1ae6778bf6461`, 직후snapshot/현재디스크 동일. 이전 후보와 같은 save SHA이나 자체 fresh 시작·입력 receipt로 생성 경로 확인, 다른 후보 save/state를 가져오지 않았다. 다른 테스트 saves 보존. 한글 이름 persistence/기존save 호환 검증은 아니다.

## 포르테 화면 검증 범위

자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root 읽기를 관찰하고 exact-ROM/lookup receipt 검사. 새해/칠석/크리스마스이브 각각 같은 정상 parent에서 별도 시작했다.
`capture_forte_seasonal_diagnostic.py --forte-script 1/7/8`: PC08037F20,R0=08038278,R1=1,R3=52 root read1회만 포르테 pool로 alias.7/8은 PC0804FB76,R0=pool,R1=2,R5=0200FA20 requested1 offset read를 target7/8로1회 alias;1은 entry alias0회. 원본 caller/initializer·normal-window prefix 검사. 넘버맨 caller·초상이 유지되는 격리 renderer 진단이다. 정상 포르테 해금/초상/날짜/성별/이벤트 선택 증거가 아니다.
입력 사이300frame 대기. 새해3페이지(번역2+침묵1), 칠석4페이지, 이브1페이지 총8페이지의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 strict 검사 통과. 메인 에이전트8페이지와 정상 넘버맨 화면 직접 확인. 검사 완화 없음. 전환 전 모든 프레임·하드웨어·음성·실시간RTC 증거 아님. 다른23번역 문구는 static-only.
검사 `tools/report_forte_seasonal.py`; 결과 `analysis/forte_seasonal_v1/runtime.json`; 화면 `analysis/forte_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_forte_v1/inventory.json`, `literal_backlog.json`.732개/31,907 canonical literals 중 선택2,140, 미선택 일본어 포함27,888개/기타1,879개. 일본어 분류 감소31은 번역30개 외에 원본 여섯 점 침묵의 U+30FB도 분류되기 때문이며,31개 새 번역이라는 뜻이 아니다. catalogue는 완전한 ROM 번역 분모가 아니다.
다음 거츠맨 intro665EB8의 첫 인사/재선택 인사4문구는 최신 backlog에서 전부 unselected_japanese. TPL 전체를 읽었고 ガッツマン 이름 명시와 original root038110=08665EB8/038144=0866A234의 intro/+52 seasonal 관계를 확인했다. TPL SHA `554c04d09092b0c9f5384a606a7e257a80dc8d1f6e1cb2ddcf1aa996b34805d0`; payload SHA `ba5d7653dfd99d0c80bc1a5b2eeae3ca2ecbceb03809d30d2bfaa10112ef31b8`. 아직 새 번역·등록·빌드 입력 미작성. 이전 거츠맨 번역 말투와 native 초기 선택/재선택 경로를 이어 확인할 것.
전체 요청 미완료. 정상 포르테 해금·날짜·성별·이벤트 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이 미해결.
