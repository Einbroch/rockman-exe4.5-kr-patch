# 거츠맨 R 대화 부분 통합 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_pet_talk_v1.gba`.
SHA256 `75c2355fd206156a4a5cde9dcae54a288b6e85fe71183195fccfadf841b8e309`.
신규31번역 literal, 누적2,278선택 literal /57선택·675원본 유지 archive. 전체 요청은 아직 완료되지 않았다.

## 원문·적용 범위

66A844:2191bytes/255slots/root038148. 전체33literal 중 script13의 칩 삽입 앞뒤2literal을 제외한31literal/24scripts를 개별 작성했다. 인터넷 탐색·견습 라이선스·사건·마이너스 키·오피셜 토너먼트·메일 안내이며, 거츠/거스 말투는 기존 개발 후보와 일치하는 검토 대기 초안이다. 넘버맨4649 승인을 이 문구들의 승인으로 사용하지 않았다.

Source payload SHA `ab59357517b022252695e2b9785bf85a45fbab48e3444c5964d75e9c0d930795`.
TPL SHA `4793441d1f3ead084ccfa048476540e9ea24b0e31127d0615a59ad58ab0dbd67`.
입력 `translations/gutsman_pet_talk_ko.json`, 개별 작성/직렬화 `tools/draft_gutsman_pet_talk.py`, 등록 `tools/specs/exe45_dialogue_archives_v1.json`, 빌드 flag `--gutsman-pet-talk`.

Stable ID/원문/숫자/newline·행/페이지·keyWait/clearMsg/waitHold·flag/item/요일 분기, 닉네임 삽입2곳의 첫 행 쉼표를 보존했다. 닉네임 삽입 명령 자체는 변경하지 않았다. 231미선택 script spans source-identical, script13의50bytes도 원본 그대로다. source/control/glyph/geometry/semantic·binary roundtrip PASS; literal570glyph, 최대125px≤PET132px/3행. 별도 mugshot renderer 용량으로 확대 적용하지 않는다.

관련169tests PASS, 최종611Python tools AST PASS. 공용 알림 page helper는 명시적인 only_keys 부분집합을 허용하되 기본 전체 asset/stream 검사와 strict pixel 검사 유지. 기존 알림 후보3페이지 기본 검사와 명시1페이지 검사를 읽기 재검증해 통과했다. 새 픽셀 예외나 검사 완화 없음.

Immutable original에서 이전 누적 flags+신규 flag로 빌드. main/repro/초기 current_repro 동일 SHA. 검사 분기 수정/별도 nickname 진단 wrapper 추가 후 final current_repro_r2도 동일 SHA, 최종611Python tools drift=[],원본 SHA 보존 PASS. 최종 감사 `analysis/gutsman_pet_talk_v1/final_identity_audit.json`. 기존 patched ROM은 빌드 입력으로 사용하지 않는다.

## 실행 검증 상태

첫 검사 FAIL: 정상 R에서 script31 닉네임2페이지가 나올 것이라는 미검증 예상으로 name_page(step2,requested31)를 호출해 `active nickname page`에서 실패했다. 동일 ROM/자체 select-gutsman parent/none→R 입력의 RAM은 step2/3 script10, pool0880A040, cursor0880A34E이다. native caller script0/LR08037F27, 전체24literal draw와 화면은 실제 인터넷 탐색10:0에 일치한다. 첫 A 이후 step4/5는 PET1/pool08807EF0이며 추가 talk draw 없음. 두 번째 A의 step6/7은 PET2로, 둘째 talk 페이지가 아니다. 실패한31 예상은 정상 통과로 세지 않는다. ROM/flag/save는 수정하지 않고 정상 검사를10/복귀4로 고쳤으며,31은 별도 격리 renderer 진단으로 추가한다. 기존 캡처 전부 보존.

`tools/run_gutsman_pet_talk.py`의 자체 freshFF저장/cold이어하기·거츠맨 선택 정상16구간과 정상R/기존7대표분기 캡처 완료. 별도 `tools/capture_gutsman_pet_talk_nickname_diagnostic.py --talk-script31`을 같은 정상 parent/exact ROM에서 실행했다. `tools/report_gutsman_pet_talk.py` PASS 및 메인 에이전트가 `analysis/gutsman_pet_talk_v1/talk_pages.png`의14페이지와 `pet_regression/normal_pet_prompts.png`의8장면을 직접 확인했다.

정상 R script0→10:0 step2의24glyph/3,324font·VRAM·screen pixels,2,275vacant pixels clearing,CPU font read/advance/행 좌표/keyWait/native arrow 분리/우측 border PASS. 첫 A 이후step4 PET1로 복귀·추가talk draw없음 PASS. step6/7은 PET2 질문이므로 정상 talk2페이지로 세지 않는다.

격리11/12/17/25/27/33/34/31 총13페이지 strict CPU/font→actual OBJ VRAM→화면·geometry·clearing·page순서·keyWait·nativearrow분리·border PASS. 닉네임12:0/31:0은 captured RAM 원본「ああさま」44px, 원본 one-byte code/legacy font/advance/terminator를 decode하여 한글 literal과 합친 실제 페이지 픽셀을 검사했다. 다른 이름이나 한글 이름 population·영구 저장을 증명하지 않는다. 실제 flag10→31 선택은 미검증이다. 나머지17선택literal은 static-only이다.

정상 넘버맨3페이지·거츠맨 첫인사2페이지/PET8장면22항목,29focus·No수락·B취소·복귀 회귀 PASS. native NumberMan save58 및 자체 save SHA `674e4dc5a74dd9d05419d2d564196363e1c38381bbe08719d111c39fcde056c9`, 직후snapshot/현재disk 일치·다른 테스트 saves 보존 확인. 한글 이름 또는 거츠맨 저장의 영구 호환 증거는 아니다.

기존56archive payload·선택 자산·그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 수정 유지. 모든 내비 root는 자기 pool이며 거츠맨R038148→0880A040 binding도 확인. 결과 `analysis/gutsman_pet_talk_v1/runtime.json`, 회귀 `pet_regression/runtime.json`.

이번 정상 observer는 relocated66A844 자기 pool을 관찰하며 쓰기/alias 없이 R 경로를 캡처한다. 대표 분기11/12/17/25/27/33/34/31은 동일 정상 parent에서 table script0 offset을 단1회 읽기 alias하는 별도 진단이다. 각각 entry_aliases=1; native root·초상은 유지하며 ROM/RAM/RTC/save 쓰기는 하지 않는다. Native consumer code guards와 exact observer/tool hashes 확인. 진단 checkpoint 격리/정상 chain 재사용 금지. 실제 아이템·라이선스·사건·대회·요일 분기의 정상 도달이나 완료로 세지 않는다. Alias는ROM에 없으므로 넘버맨으로 되돌리는 ROM 수정도 필요 없다.

## 남은 범위와 다음 검증

칩104 삽입 script13의2literal과 원본 칩 이름은 미번역이다. 기존 한국어 빅해머1 이름 selector는 롤664E28의 특정 printChip stream에만 적용되므로 거츠맨에 임의 재사용하지 않았다. 다음 검증은 거츠맨 printChip caller/stream/동적 이름 glyph·advance·종료·행 경계를 추적해 native fallback과 롤 회귀를 함께 증명하는 것이다.

최신 inventory `analysis/full_scope_gutsman_pet_talk_v1/`: 선택2,278/미선택 일본어 포함27,770/기타1,859. Catalogue732archives/31,907canonical literals는 전체 ROM 번역 분모가 아니다.

일정 알림66651C의18미선택literal·동적event/nickname·별도mugshot·실제 시간 알림, 맥락 미확정666430의‘かりです’도 남는다. 한글 이름 편집→committed record→모든 재표시→영구 재로드→기존save 호환이 가장 어려운 미해결 조건이다. 전체 graphics/inline/fixed population, prior native wait-arrow53pixel 차이와 인간 문구 검토 등도 미해결이다. 전체 완료/배포 선언 없음.

이전 알림/전투결과 진단 observer는 source talk root038148→0866A844를 요구하므로 relocated66A844 후보에서 그대로 재사용할 수 없다. 이전 후보의 증거는 보존하며 새 후보에서 재실행했다고 주장하지 않는다.
