# 거츠맨 전투 결과 대사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

최신 후보: `poc/output/exe45_ko_development_gutsman_battle_results_v1.gba`.
SHA256: `126223bdb1e707b396dbbd1a16788b852bf97ca6ea4aa47f88e68015eedf5e92`.
신규 3번역 literal, 누적 2,247선택 literal / 56선택·676원본 유지 archive. 전체 미번역 요청은 아직 완료되지 않았다.

## 적용 범위와 정적 검증

66A7A8:155bytes / 5slots / 원본 root038130→0866A7A8(intro+32). 전체 source TPL의 3literal은 패배1·승리2·무승부3의 변수 없는 PET 대사이다.
Source payload SHA `753a10f34b5f83d27f12a67eed539c95344366e0caad8dbcd31f1915d846a115`.
TPL SHA `7ec86c57444a12203d07ad7b5ce6ca2e305d7318b83fd810c049316a3af1df0f`.

자산 `translations/gutsman_battle_results_ko.json`, 개별 작성 및 직렬화 `tools/draft_gutsman_battle_results.py`. 패배의 말더듬음·충격, 승리의 자신감·거츠맨 자신의 실력, 무승부와 좋은 승부라는 평가를 보존했다. 기존 거츠/거스 개발 후보 말투를 사용하며 인간 문구 검토 대기 상태이다. 넘버맨4649 승인이나 기존 기술적 통과를 문구 승인으로 전용하지 않았다.

Stable IDs/원문/숫자/newline, positionBox/Text/Arrow, keyWait/clearMsg/waitHold를 보존했다. 빈 slot0/4도 source-identical이다. PET의 채택 범위는92,110에서 3행/132px이며 별도 mugshot renderer로 확대 적용하지 않는다. 전체3literal/48glyph의 source·skeleton·glyph·geometry·roundtrip PASS, 최대103px≤132px.

관련166tests PASS, 전체603Python tools AST PASS. 기존 알림 page helper는 명시 unit_asset 인자를 추가하되 기본 알림 asset을 유지하고 asset/stream ID 전체 집합 일치를 요구한다. 기존 알림 후보의3페이지를 같은 기본 인자로 읽기 재검증하여 기존 strict pixel 결과 유지 확인. 검사 완화나 새 픽셀 예외는 없다.

Immutable original에서 이전 누적 flags + `--gutsman-battle-results`로 빌드했다. main/repro/final current_repro가 동일 SHA,603Python tools drift=[]/원본 SHA 보존. 마지막 감사 `analysis/gutsman_battle_results_v1/final_identity_audit.json`. 기존 patched ROM을 새 빌드 입력으로 사용하지 않았다.

## 실행 증거와 한계

`tools/run_gutsman_battle_results.py`가 이번 ROM의 자체 freshFF 저장·cold 이어하기·거츠맨 선택 정상16구간을 생성했다. 정상 넘버맨3페이지/거츠맨 첫 인사2페이지/PET8장면22항목,29focus·No수락·B취소·복귀 회귀 PASS. Native save58, 생성 save SHA `cf4383ca2c7d85f04ca8d6f67eeaabfb4360f718d1e30dd940161ae6b4216b39`, 직후snapshot/현재disk 일치 및 다른 테스트 saves 보존 확인. 이는 넘버맨 일반 저장 회귀이며 한글 이름 persistence나 거츠맨 저장 검증은 아니다.

기존55archive payload·선택 자산·그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 이미지 수정 유지. 모든 내비 root는 자기 pool 유지. 이번 전투결과 root038130→08809F54도 정적 binding 검사 통과. 결과 `analysis/gutsman_battle_results_v1/pet_regression/runtime.json`.

격리 `tools/capture_gutsman_battle_results.py`는 R 입력의 원래 거츠맨 talk root038148→0866A844 읽기 반환값을 단1회 새 pool로, 요청script0 offset을1/2/3 offset으로 각각 단1회 반환한다. Window prefix/dispatcher·glyph consumer code guard와 source talk root를 검사한다. ROM/RAM/RTC/save 쓰기 없음. 각 root_aliases=entry_aliases=1, 이번 자체 정상 select-gutsman parent, exact ROM/tool hashes 확인. 실제 거츠맨 초상 유지. Alias는ROM에 없으므로 내비 대사를 되돌리는 ROM 수정은 필요 없다. Diagnostic checkpoint는 `diagnostic_checkpoint.mss`, normal_play_checkpoint_eligible=false이며 정상 chain에 재사용하지 않는다.

각 script의 step2에서14/20/14glyph 완성 페이지를 확인했다. CPU font read/ROM font→actual OBJ VRAM→화면 pixels, 문자 advance/행 좌표, keyWait E600F1, 빈 영역3,643/2,815/3,655pixel clearing, native arrow footprint 분리, 오른쪽 border 검사 PASS. 모두 keyWait에서 멈췄으며 후속 exit/reentry나 result-state persistence 증거는 아니다. 실제 전투 승패·무승부와 native caller 선택을 실행한 것으로 세지 않는다. 정상 신규 runtime units0 / 진단 renderer3페이지로 구분한다.

결과 `analysis/gutsman_battle_results_v1/runtime.json`, 화면 `diagnostic_result_pages.png`. 메인 에이전트가 이3페이지와 정상 PET8장면 composite을 직접 확인했다. 원본·이전후보·실험·실패·테스트 saves 보존. 이번 후보에서 이전 일정/대회/접속/귀환/메일/날짜별 대사를 모두 재실행했다는 주장은 하지 않는다.

## 남은 범위와 다음 작업

최신 inventory `analysis/full_scope_gutsman_battle_results_v1/`: 선택2,247 / 미선택 일본어 포함27,801 / 기타1,859. Catalogue732archives/31,907canonical literals는 전체 ROM 번역 분모가 아니다.

다음 거츠맨 R 대화66A844:2191bytes/255slots/root038148의 전체 TPL33literal을 읽었다. 닉네임 삽입2곳(12,31), chip104 삽입1곳(13), license/item/incident/tournament/date/flag 분기와 다중페이지 흐름을 확인했다. 아직 새 번역 입력·등록·빌드는 하지 않았다. 앞뒤 페이지를 끊어 해석하지 않으며 nickname suffix/칩 이름 consumer/숫자/flag·요일 분기 보존을 별도 검사해야 한다. 이후 이 source talk archive를 옮길 때는 현재 진단 observer의 source-only root guard도 적용 범위 재검토 대상이다.

일정 알림66651C의18미선택literal, 동적event/nickname 및 별도mugshot consumer와 실제 시간 알림은 여전히 남는다. 666430의‘かりです’는 임시placeholder로 보이나 맥락 미확정이라 추정 번역하지 않았다.

한글 이름 편집→committed record→모든 재표시→영구 재로드→기존save 호환이 가장 어려운 미해결 조건이다. 전체 graphics/inline/fixed population, prior native wait-arrow53pixel 차이, 전체 이벤트·전투·음성·하드웨어·인간 문구 검토도 남는다. 전체 완료·배포 선언 없음.
