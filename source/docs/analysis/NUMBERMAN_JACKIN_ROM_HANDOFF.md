# 넘버맨 플러그인 구호 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 결과와 범위

ROM `poc/output/exe45_ko_development_numberman_jackin_v1.gba`.
SHA256 `0300bee602e8c841360e661703870bf5dd25c660b444decbd4a43db1c1f74135`.
추가1literal/3행 구호, 누적1,213선택 텍스트 /15기존 그래픽 /25선택·707미선택 archive. 전체 완역률이 아니다.
687E3C script1 ‘플러그인! / 넘버맨.EXE、 / 트랜스미션!!’를 추가했다.
플러그인·넘버맨·트랜스미션은 기존 Roll Jack-In/넘버맨 소개와 일치하는 개발용 용어 초안이다. 공식·인간 승인이나 독립 의미 검토 완료를 주장하지 않는다.

source76bytes/3slots, root038288(32-bit GBA ROM pointer), block SHA256 `ddf78003099397cf5e8fe4f12ed2a6414df9718d2759caa7ca4167c7b001ef6a`.
TPI/source literal baseline의 전체1literal을 primary spec complete_literal_scope=true로 선택한다. 0/2 두 nonliteral slots는 불변이다.
normal consumer92,110/window type3, adopted132px/3행; 현재 최대행폭91px. compiled104bytes, offset0x807E18/root0x08807E18.
모든 source commands/args/EXE suffix/3행/flags3603·3651/wait30/flagClear/waitHold 불변이다. 새 code hook·save format·이름 입력 변경 없음.
직전 training-intro-v1의24archive payload hashes/bytes와 저장 제목6333A4의256bytes 동일. placement에 따른 offset은 현재 build에서 계산한다.
기존 누적 flags에 `--numberman-jackin`을 추가하며 이전 training/PET 범위 누락을 거부한다.
원본·이전후보·모든 state/capture/testsave/미통과 기록을 보존한다. 배포패치를 만들지 않았다.

## 실제 실행과 관측

prefix `poc/runtime/numberman-jackin-v1-`.
own cold-part1(state_origin=null)→date→profile→navi-menu→select-numberman(right3회)→intro→warning→transmission.
모든 부모 checkpoint/receipt/artifact hash가 동일 새 ROM에 연결된다. 타 ROM state/RAM/save import나 진행 상태 수정 없음.
warning은 정상 PET 플러그인 ‘예’→특훈 권유20→‘싫은데’→경고21까지 진행한다. 경고의 current-ROM stream/font/OBJ/pixel 회귀도 통과했다.
transmission은 자체 경고21의 checkpoint에서 구호 load 전에 read-only observer를 시작한다.
1회 정상 A 입력과 no-input frame sampling으로103steps를 캡처했다. 게임 속도나 대기 명령을 늘리거나 구호를 강제 호출하지 않았다.

완성 구호는 steps66..93의28연속프레임에서 관측했다. 실제20glyph의 ROMstream→normal font CPU read→OBJ OAM/VRAM→화면 2,784pixel/프레임과 빈영역 clearing을 검증했다.
native entry는 단일 relocated root/script1 호출이며 구호 뒤 해당 stream의 glyph draws가 추가되지 않는 것을 확인한다.
원본 wait30 argument ED001E00을 검사했고 parser cursor의 wait/end 전환을 프레임별로 기록했다.
wait cursor는 sample frames64..94, 다음 cursor는95부터다. 관측 경계 차이는31frames이며 source30명령과 parser/frame callback 경계의 결과로 기록한다. 정확한 실기 timing 인증으로 일반화하지 않는다.
마지막 step103은 실제 네트워크 진입 화면이다. 네트워크 이동/전투/재진입/귀환의 전체 검증은 아니다.

## 미통과 초기 캡처와 판정

첫 통합 report는 step63의 ROM glyph→VRAM 불일치를 거부했다. ROM은 바꾸지 않고 같은103캡처의 경계를 조사했다.
step63은 최종 ‘!’의 VRAM132pixel과 screen20pixel이 변했고, step64/65는 VRAM은 같으나 screen10pixel씩 변했다.
각 미통과 snapshot과 뒤의 엄격 통과 step66은 관측 call/draw/font-read 기록이 동일하다.
VRAM 변화는 마지막 ‘!’ rectangle에만, 화면 변화는 source-preserved 끝 ‘!!’ 두 rectangle에만 한정됨을 확인했다. 그 밖의 문구/빈영역은 변하지 않았다.
두 terminal glyph draw frames는60/63, 완성 strict-pass capture frame은67이다. 늦게 표시되는 이전 glyph와 아직 전달 중인 최종 glyph를 완성 화면으로 취급하지 않는다.
미통과3snapshot은 credited=false로 보존한다. settled28frames에는 기존 strict glyph/VRAM/screen validator를 그대로 적용했다. mapping/폭/실행 대기를 수정하거나 오류를 전역 면제하지 않았다.
특훈 경고→완성 구호→네트워크 진입 묶음과 완성 구호를 직접 검토했다.

## 증거와 미완료

`analysis/numberman_jackin_v1/runtime.json`, `jackin_pages.png`, `transmission.png`, `final_identity_audit.json` 참조.
관련70unittest는 historical fixture와 새 asset/구조 검사이며 실제 실행 증거와 구분한다.
main/_repro/최종 _current_repro_r2를 원본에서 독립 재생성했다. 초기 _current_repro는 같은 ROM이나 관측 report 수정 전 tool manifest여서 보존만 한다.
최종 source SHA/main·repro·current_r2 동일 SHA/current tool drift는 final_identity_audit.json이 판정한다.
이번 ROM에서는 native save를 재실행하지 않았다. 이전 ROM의 저장 검증을 현재 save 실행 증거로 전용하지 않는다.

미니게임 설명·결과·보상과 남은 다른 Navi 대사, 특훈10/11 runtime 및 재선택 숫자 말장난은 미완료다.
네트워크 화면의 일본어 닉네임은 원본 입력 consumer의 테스트 사용자 이름이며 한글 이름 입력 지원을 뜻하지 않는다.
최대 완료 위험은 한글 이름 입력/편집/committed record/모든 재표시와 저장/영구 재로드·기존 save 호환성이다.
전체게임/RTC/alarm/오디오/실기/독립 의미·인간 승인/배포 미완료. 완역·출시후보로 승격하지 않는다.
