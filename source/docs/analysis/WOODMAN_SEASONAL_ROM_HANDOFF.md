# 우드맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

누적 ROM `poc/output/exe45_ko_development_woodman_seasonal_v1.gba`.
SHA256 `fcca6e0666a071959b01f7ff0af11fa381e703a2f07fd02eb2579937ed38a9f6`.
신규41 literal=39번역 문구+2유지 인용부호. 누적1,821선택 literal/39선택·693원본 유지 archive.

## 원본·번역 경계

source6A2184:1348bytes/21slots/root03839C. Payload SHA `5d66c25b2ab48c88810e7dbfdd89b5f01b9c916d322925548a5d09aaa3c470ac`; TPL SHA `a3908de7e31d2ee1a7936c06be3bfd643fadadaecb7f843a9d145ca77af52faa`.
intro69E088이 ウッドマン과 대지의 은혜를 명시한다. 원본 intro root038368=0869E088, native group+52/root03839C=086A2184 확인.
IDs/원문/숫자/줄 수·newline 경계/명령/global22/이벤트 이름 buffer·loop 보존. 빈0/13/14/15와 없는16/20 유지.
새해1:4 printPlayerNickname 뒤 첫 줄 ‘、’11px 원문 그대로 유지했다. 실제 nickname 출력이나 한글 이름 지원 증거는 아니다.
차분한 말투와 계절·대지의 은혜·감사, 크리스마스트리 거절/살 빠지길 바라는 소원/생일을 잊었다는 의심에 대한 부정을 옮겼다. 새해 손뼉 소리는 ‘짝짝!’이다.
3월3일 복숭아꽃 명절,5월5일 일본 단오·창포물 목욕은 원래 날짜와 문화 맥락을 유지했다. 목욕 효능은 원작 캐릭터 대사 번역이며 검증된 의료 안내가 아니다. 말투/문화/명칭은 인간 검토 대기. 기존 넘버맨4649 승인을 전용하지 않는다.

## 빌드·검사

자산 `translations/woodman_seasonal_ko.json`, 수동 작성 초안 직렬화 `tools/draft_woodman_seasonal.py`.
기존 아쿠아맨 누적 flags에 `--woodman-seasonal`을 추가해 immutable source에서 생성한다. 이전 patched ROM은 입력으로 쓰지 않는다.
41항목 원문/제어/숫자/이름 뒤 쉼표/glyph/3줄132px 범위/roundtrip 관련121tests 통과. 최대125px.
새해1:1/1:3의 동일 ‘짝짝!’ 때문에 기존 literal byte uniqueness 검사가 중단됐다. 번역을 달리하거나 첫 검색 결과를 임의 채택하지 않았다. 첫 손뼉은 다음 대지 기도 literal+keyWait/clearMsg, 두 번째는 nickname print+comma+newline으로 원본·대상 양쪽에 유일하게 연결했다. 원본 두 occurrence/각 command anchor1회, 대상 anchor1회, 서로 겹치지 않는 stream 주소를 검사했다. 모든 기존 uniqueness 검사와 source-preservation 경계 유지.
main·`_repro`·최종 `_current_repro_r3` 3독립 빌드 SHA 동일. 현재528Python 도구 drift=[], 원본 SHA 보존: `analysis/woodman_seasonal_v1/final_identity_audit.json`. 먼저 생성한 `_current_repro`/`_current_repro_r2`도 같은 ROM이지만 도구 보강 전 manifest이므로 최종 tool identity 근거로 쓰지 않는다. 원본/이전후보/실험/테스트 saves 모두 보존.
이전 아쿠아맨판38선택 archive payload와 선택 자산 해시를 실제ROM bytes까지 보존했다. 그래픽15라벨/5블록의 위치·길이·SHA·실제ROM bytes 동일. ‘통신’ glyph override 유지. 전체 이미지 미번역 해소나 신규 전체 이미지 runtime QA를 뜻하지 않는다.

## 검증 상태

자체 cold 시작→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→재선택→정상 넘버맨 새해3페이지 회귀 통과. controller 입력만 사용했고 다른 후보 save/state를 가져오지 않았다. native save 성공script58과64KiB 파일 SHA `046446bad3e5069b17009058279c2a291af9a683effb0d9da149c8444e6cc970`, 직후snapshot/현재디스크 동일성 확인. 다른 테스트 saves 보존. 한글 이름 persistence/기존save 호환 증거는 아니다.
신규7페이지는 우드맨 정상 해금 경로가 아닌 격리 renderer 진단이다. 자체 normal-reload-select 대사load 이전 parent에서 실제 넘버맨 seasonal root0382AC read를 관찰하고 exact-ROM/lookup receipt를 검사했다. 절분/칠석은 같은 parent에서 각각 시작했다.
`capture_woodman_seasonal_diagnostic.py --wood-script 2/7`: PC08037F20,R0=08038278,R1=1,R3=52의 root read1회만 우드맨 pool로 alias하고, PC0804FB76,R0=pool,R1=2,R5=0200FA20의 requested1 offset read를 target2/7로1회 alias했다. 각 root_aliases=1/entry_aliases=1 확인. 원본 native caller/initializer와 normal-window prefix 검사. 넘버맨 caller·초상 유지, ROM/RAM 쓰기·날짜 변경 없음. alias는 제품ROM에 포함되지 않는다.
각 checkpoint는 diagnostic_checkpoint.mss로 격리하고 normal_play_checkpoint_eligible=false 기록. 정상 우드맨 해금/초상/날짜 선택 증거는 아니다. 다른32문구(새해 이름/성별 포함)와 동적 이벤트 이름 consumer는 static-only/미검증이다.
초기180frame 대기 진단의 칠석step003은 마지막 ‘・’의4픽셀(178..179,129..130)에서 role3 화면색134/126/114가 관찰돼 엄격 화면 검사 실패. ROM glyph→OBJ VRAM은 일치했으나 화면색은 ink20/16/17와 배경248/236/212의 정확한 중간값이다. emulator GBA BlendFrames=true 확인. 마지막 draw frame422/캡처425였다. 이 실패를 PASS로 바꾸거나 픽셀 예외를 추가하지 않았다.
동일ROM/동일정상parent/동일관찰도구에서 입력 사이 대기만180→300으로 늘린 `lookup-r2`/`diagnostic-setsubun-r2`/`diagnostic-tanabata-r2`를 새로 실행했다. 칠석 첫 페이지 마지막 draw542/캡처665, 모든7페이지 원래 strict role-color 검사 통과. 이는 안정된 대기 화면 검증이며 최초 캡처의 일시적 blending timing과 일치한다. 정확한 최종VRAM writer/scanout timing은 별도 추적하지 않았으므로 renderer 코드 결함 수정/모든 전환 프레임 검증 주장은 하지 않는다. 초기 캡처/실패를 보존했다.
최종 절분4페이지 steps3..6/칠석3페이지 steps3..5의 CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/순서/종료 통과. 메인 에이전트가7페이지 화면 직접 확인.
검사 `tools/report_woodman_seasonal.py`; 결과 `analysis/woodman_seasonal_v1/runtime.json`; 화면 `analysis/woodman_seasonal_v1/diagnostic_seasonal_pages.png`.

## 남은 작업

최신 catalogue `analysis/full_scope_woodman_v1/inventory.json`, `literal_backlog.json`.
732개/31,907 canonical literals 중 선택1,821, 미선택 일본어 포함28,190개/기타1,896개. 범위 기반 분류는 완역 분모나 완료율이 아니다.
다음 스타맨6A8ADC; intro6A383C 화자/native group 연결부터 확인한다.
전체 요청 미완료. 정상 우드맨 해금·날짜·성별·이름 출력, 전체 graphics/inline/fixed-string population, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이가 남아 있다.
