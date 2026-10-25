# 거츠맨 친구·취향 질문 미번역 — 2026-10-09

## 제품과 선택 범위

개발ROM `poc/output/exe45_ko_development_gutsman_questions_v1.gba`.
SHA256 `52bee4df4ceda2147c48ac1e4b0a414c29e63f3088ed0fe73b66f3b5acedd9e7`.
41literal 추가, 누적2,473선택literal /60선택archive·672원본유지archive.
needs_review / NON-DISTRIBUTION / release_eligible=false. 전체 번역 완료가 아니다.

667044의9/11/13/15/17/19/21/23/25 질문39문구와88반응2문구를 추가했다.
친구, 좋아하는 음식, 취미, 장래희망, 좋아하는 여자아이/남자아이, 존경/꺼리는 사람,
좋아하는 TV 프로그램을 묻는 거츠맨 대화다. 반응88은 nickname 뒤의 반함/이해 문장이다.
중단된 원문 이름 fragment`ロー・・・`는`로・・・`로 중단 상태를 유지하며 완성된 인물명으로 확장하지 않는다.
17의 global22==1→19 분기, native flags/input initialization, nickname, keyWait/clearMsg는 보존한다.
가족 유무 질문1..8과 저장된 답변을 printStringBuffer로 보여주는40..63 등은 아직 미선택이다.

`translations/gutsman_profile_questions_ko.json`은 기존40문구를 원문/번역/상태 그대로 이어받는다.
parent SHA256 `b69d6a1f553ce743c04c44c96112f700bd1725fae7240700397a9b51d54458c5`.
primary selected_scope는 부모 해시/metadata/40unit 일치와11/88의 합성 nickname 페이지3행을 검사한다.
nickname suffix는 고정 한국어 조사를 쓰지 않고 동일 폭 쉼표를 사용한다.
11의`그런데、\n`→nickname→음식 질문과88의 첫 문장→nickname→반응은 각각 한 페이지이며,
literal 두 개를 독립 화면처럼 검증하지 않는다. 두 페이지 모두 nickname은 두 번째 행이다.

## 빌드와 검증 책임

`python -X utf8 tools/build_keyitem_full_rom.py --name <새_이름> --gutsman-plugout --gutsman-profile --gutsman-profile-questions`
기존 primary immutable-source 빌드. 이전 patched ROM을 입력으로 쓰지 않는다.
81선택literal/30script, 원본97slot/5225byte/0x38138pointer, 원본과controls/roundtrip,
67미선택script·전체 glyph/advance·최대125px≤132px 정적검사 PASS.
독립`_repro.gba`는 본ROM과 동일 SHA256이다. 두 번째 빌드는 새 합성페이지3행 gate도 실행했다.
첫 빌드 뒤 gate를 보강했지만 선택문구/ROM bytes는 바뀌지 않았으며 재현본과 일치한다.

`run_gutsman_questions.py`: 새ROM cold→프로필→넘버맨 소개→native새저장→checkpoint 없는
cold이어하기→거츠맨 선택→인터넷/정상플러그아웃→기존 질문29/일본어 입력 UI.
기존ROM의 checkpoint/native save를 새ROM으로 가져오거나 이름·답변·진행 RAM을 주입하지 않는다.
그 뒤 동일ROM의 로드 전 자체 정상 checkpoint에서 새10script를 read-alias로 격리 진단한다.
native reader0x0804FB76의 profile29 table read를 딱 한 번 대체한다. ROM/RAM write는 없다.
17진단은 원본 gender dispatch6byte를 건너뛰고 동일 UI header를 선택한다.
실제 나이/성별/질문·답변 선택/입력/저장 조건의 실행 증거가 아니며 진단 checkpoint를 별도 격리한다.
39개의 각 페이지에서 멈추고, 마지막 질문의 keyWait 뒤 입력 초기화는 실행하지 않는다.

`report_gutsman_questions.py`: 신규41literal/39페이지 전부 CPU font reads→OBJ VRAM→최종 픽셀,
줄·폭·native nickname 원본bytes/terminator/첫째·둘째행 geometry·페이지 지움·순서·마지막 keyWait 검사.
기존29의3문구는 정상 진행 회귀로 별도 기록하고 신규41의 정상 질문 선택과 혼동하지 않는다.
결과 소유자`analysis/gutsman_questions_v1/question_runtime.json`, 합성화면`question_pages.png`.
PET/소개/넘버맨 대표 회귀는`pet_regression/runtime.json`, 플러그아웃 회귀는`plugout_regression/plugout_runtime.json`.
CPU624조건은`cpu/report.json`: 실제 상점02031000 실행을 대신하지 않는 합성 CPU 계약 검사다.
최종 감사`audit_gutsman_profile.main(...,questions=True)`는 원본·header·append·쓰기ledger·재현,
모든 입력·기존59archive payload·기존profile87script/40unit·폰트/advance·기존이미지·keyitem39clone·
최종hook·새저장/cold이어하기·CPU/runtime·현행 도구 identity를 검사한다.
실행 중인 기록을 검증 PASS로 간주하지 않는다. 최종 소유자는`final_identity.json`이다.
관련 합성fixture: 거츠맨78 + keyitem20 PASS. 신규 계약fixture10은 부모/원문/닉네임/합성행 위반과 대기 커서 길이를 검사한다.

## 최종 확인 결과

`question_runtime.json`: 신규41literal/39페이지 전부 PASS; 정상 신규문구0, 격리 표시진단41로 구분했다.
`normal_subject_regression/profile_runtime.json`: 기존29의3문구 정상회귀와 원래 일본어키보드전환 PASS.
PET22문구/소개2·넘버맨3, 플러그아웃 No/B/좌우/Yes/귀환과 새native저장/cold이어하기 PASS.
`final_identity.json`: 최종ROM/원본/재현/쓰기ledger/기존입력·payload/폰트/이미지/키아이템/CPU624/실행identity 감사 PASS.
734도구 pins drift=[] /725Python AST PASS. main/repro SHA는 위와 동일하며 원본 SHA는
`588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`로 불변이다.
39페이지 합성화면과 플러그아웃6화면을 직접 확인했다. 음식11/반응88의 두 번째 행 nickname도 겹침 없이 표시된다.
첫 자동대조는11:0 마지막 확장문자의4byte 길이를3byte 이하로 가정해 거절됐다.
화면/ROM을 수정하지 않고 verifier가 실제1byte/4byte glyph 뒤의 정확한 native keyWait 주소를 검사하도록 고쳤다.
원래 실패 캡처를 보존하고 같은 캡처에서 재검사 PASS; 미완성페이지 거절 fixture도 추가했다.

## 남은 경계와 다음 작업

catalog732 /31,907literal: 선택2,473 /미선택일본어27,575 /기타검토1,859 /errors0.
다음 묶음은667044:1..8 가족 유무 질문/선택지/없음 반응이다. sourceの/は/って 등
nickname suffix와2칸 선택 패딩·Yes/No·B 경로를 기존 롤의 동일 소비자 분석과 대조해야 한다.
그 다음40..63 답변 재표시의 printStringBuffer1/2/3와 등록/편집/재질문 경로를 실제입력과 연결한다.
일본어 키보드 자체, 한글 입력/편집/확정/모든 재표시/영구reload/기존save 호환은 미완료다.
상점02031000 정상 경로, 다른 내비·이미지/inline/fixed/날짜요일/RTC, 전체 인간 의미/용어/시각 검토와
배포 검증도 미완료다. 이 진행분은 남은 전체 번역 요청의 완료가 아니다.
