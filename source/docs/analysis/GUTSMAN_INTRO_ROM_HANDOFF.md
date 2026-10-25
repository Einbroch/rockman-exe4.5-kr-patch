# 거츠맨 첫 인사·재선택 인사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_intro_v1.gba`.
SHA256 `04dc41d321ef81bbd8a1266204ecbca97bda39fa179a0d3569e474431170afdc`.
신규4번역 literal. 누적2,144선택 literal/48선택·684원본 유지 archive. 전체 요청 완료 아님.

## 원문·번역·빌드 경계

665EB8:129bytes/4slots/root038110. Source payload SHA `ba5d7653dfd99d0c80bc1a5b2eeae3ca2ecbceb03809d30d2bfaa10112ef31b8`; TPL SHA `554c04d09092b0c9f5384a606a7e257a80dc8d1f6e1cb2ddcf1aa996b34805d0`.
원문 전체를 읽고 ガッツマン 화자 명시, original root038110=08665EB8/같은 native group의 +52 seasonal root038144=0866A234를 확인했다. script1 첫 인사2문구와 script2 오랜만의 인사2문구를 구분했다. 이전 거츠맨 seasonal/save 개발 초안의 거츠·거스 말투를 후보로 유지했다. 말투·명칭·문구 인간 검토 대기. 넘버맨4649 승인 전용 없음.
4개 stable ID/원문/숫자/newline 경계/flag3585/keyWait/clearMsg/waitHold와 원본 빈slot0/3 보존. 실제 이름 삽입 없음. 날짜·이름·저장·게임 진행 코드는 변경하지 않았다.
자산 `translations/gutsman_intro_ko.json`; 수동 문구/원본 identity 검증 직렬화 `tools/draft_gutsman_intro.py`. 기존 포르테 누적 flags에 `--gutsman-intro` 추가. 이전 patched ROM을 입력으로 쓰지 않고 immutable original에서 재생성했다.
148관련 tests 통과. source/제어/숫자/glyph/3줄132px/roundtrip와 빈slot0/3 검사 통과. 실제 최대102px는1:1 첫 행 ‘처음 뵙겠거스!!’이다.
main·`_repro`·`_current_repro` 3독립 빌드 SHA 동일.573Python 도구 drift=[], 원본 SHA 보존: `analysis/gutsman_intro_v1/final_identity_audit.json`.

## 실행 검증 상태

`tools/run_gutsman_intro.py`는 자체 fresh cold→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→내비 선택/넘버맨 새해3페이지 회귀를 수행했다. 다른 후보 save/state를 가져오지 않았다. 별도 거츠맨 선택은 같은 후보의 정상 normal-reload-select 부모에서 left/A 입력만 사용한다. ROM/RAM 쓰기·날짜 변경·read alias 없음. 진단 state를 정상 부모로 재사용하지 않았다.
`tools/report_gutsman_intro.py` 최종 strict 검사 PASS. 첫 인사 script1의2페이지는 실제 거츠맨을 정상 선택한 화면이며 steps5/6, 다음step7 종료까지 확인했다. 최대102px 행 포함. CPU font read→ROM glyph→OBJ VRAM→화면 픽셀, 빈 영역 clearing/가림 없음/페이지 순서/종료 검사 통과. 메인 에이전트2페이지 직접 확인. 화면 `analysis/gutsman_intro_v1/normal_intro_pages.png`, 결과 `analysis/gutsman_intro_v1/runtime.json`. 전환 중 모든 프레임·음성·하드웨어 검증은 아니다.
이전 포르테판47개 선택 archive payload와 선택 자산 SHA 전부 동일, 그래픽15라벨/5블록 위치·길이·SHA·실제ROM bytes 보존. ‘통신’ glyph override 유지. 신규 전체 이미지 QA/완역 의미 아님.
native bindings: 거츠맨intro038110→08807E1C, 거츠맨seasonal038144→08807EF0, 넘버맨seasonal0382AC→0880CBA4, 포르테seasonal03857C→08814730. 각각 자신의 번역 pool. 앞선 넘버맨 초상 진단 alias는 이 ROM에도 포함되지 않았다.
fresh FF64KiB에서 native save 성공script58 확인. 자체 저장 SHA `5decd6c04414c022c20702a8d9ad76763cd877cc90ebadf437f1ae6778bf6461`, 직후snapshot/현재디스크 동일. 과거 후보와 같은 save SHA이지만 이번 자체 FF시작·입력 receipt로 생성 확인, 가져온 save가 아니다. 다른 테스트 saves 보존. 이번 저장·cold 재로드는 넘버맨 경로이고, 거츠맨 저장이나 한글 이름 저장/기존save 호환 증거가 아니다.
script2 재선택 인사2문구는 static-only. 원본 caller/flag 조건을 우회해 정상 실행으로 가장하지 않는다.

## 남은 작업

최신 catalogue `analysis/full_scope_gutsman_intro_v1/inventory.json`, `literal_backlog.json`:732개/31,907canonical literals, 선택2,144/미선택 일본어 포함27,884/기타1,879. Catalogue가 전체ROM 번역 분모라는 뜻은 아니다.
다음 거츠맨 PET665F3C는 최신backlog44항목 모두 unselected_japanese. 전체TPL 읽음, original root038114=08665F3C/앞intro038110의+4 관계 확인. Source1147bytes/22slots; TPL SHA `7e61d76a8f55d97d703b40e67c3334d2eb4c6b0062358cc22cc31e30d9cccb01`; payload SHA `45aa744818878d7b67797fcbfc1aefcbc741ca240bc16ff529bfbec67713f719`.
선택지padding·옵션 cursor·callCheckMenuSelection/초기2..8 vs 확인10..16의 branch/flag/global30=120 유지가 필요하다. 아직 신규 번역·등록·빌드 입력 미작성.
가장 어려운 미해결 조건은 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환이다. 전체 graphics/inline/fixed-string population과 이전 native wait-arrow53pixel 차이, 각 내비의 미실행 날짜·성별·이벤트 경로도 남아 있다. 배포·완역 선언 없음.
