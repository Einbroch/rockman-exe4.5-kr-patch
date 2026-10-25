# 거츠맨 저장 답변 재질문 — 2026-10-09

사용자 요청인 전체 미번역 번역·ROM 반영은 미완료다. 이번 제품은 고정 문구40개 추가 진행분이다.
한글 입력/편집/확정/저장/모든 재표시/기존 save 호환은 범위에서 제외하지 않는다.
development-draft; NON-DISTRIBUTION; release_eligible=false.

## 제품과 입력

최초 제품 `poc/output/exe45_ko_development_gutsman_answers_v1.gba`, 독립 `_repro.gba`.
ROM SHA256 `2635bfc8d3636e420ce27a5bb44c80a8fa02931e3264ae864a903d00a6c7894f`.
2,542선택literal /60선택archive /672원본유지archive. 이전 가족29 제품보다40문구 증가했다.
새 입력 `translations/gutsman_profile_answers_ko.json` SHA256
`e04a02a87e2ca4d5d86caa686965df2abde660ff4a14e93cc9e57fc9705a9b1f`.
150unit composite는 기존 checked family110의 원문/번역/상태를 정확히 유지한다.
parent SHA `b721d8274af3d1b7e5afe84ae8cfbd2023998234014d31f5ab68e86c9a8b0eeb`.
신규40은 주 에이전트 수동 초안, needs_review다.

## 고정 문구 범위와 보존 조건

667044:40..63의24script: 형·오빠/남동생/누나·언니/여동생/친구/취미/TV/갖고 싶은 것.
각 triple은 native nickname에 붙는 prefix1개, 추가 등록 질문/있어/없어3개, 없음 응답1개다.
선택prompt의 두 줄바꿈과 세 번째행 choice, 두 칸 padding, default0/No target를 보존했다.
nickname 받침에 의존하지 않는 동일 폭 쉼표를 쓴다. 창 최대132px와 합성 선택행을 검증한다.
97slots/원본5225bytes/루트0x38138, 새62선택script와35미선택script를 구분한다.
printStringBuffer1/2/3, variable5의 분기, flags3585/3735..3749,3605/3606, waitHold와 모든 제어 명령은 보존한다.

## 재현 빌드

`python -X utf8 tools/build_keyitem_full_rom.py --name <새 이름> --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers`
patched ROM을 입력으로 쓰지 않는다. 원본부터 cumulative recipe와 등록 variant로 생성한다.
기존 파일/빌드 폴더가 있으면 거부하며 과거 ROM·저장·캡처를 보존한다.
검증 도구를 추가한 뒤 `_r2`/`_r2_repro`를 별도로 빌드하여 최종 도구 hash를 고정한다.
전체 ROM bytes/hash 동일성이 입증되기 전에는 과거 실행 증거를 이관하지 않는다.

## 실행 증거의 한계

`run_gutsman_answers.py`는 자체 새ROM cold→native save58→checkpoint 없는 cold continue→PET/소개/넘버맨→인터넷/정상 질문29를 실행한다.
profile-seed는 profile pool 로드 전 같은ROM 정상 checkpoint다.
격리 diagnostic은 native reader0804FB76에서29의 table read만 한 번 alias한다. ROM/RAM write 없음.
prefix40/43/46/49/52/55/58/61은 첫 keyWait에서 멈춰 printStringBuffer를 실행하지 않는다.
choice41/44/47/50/53/56/59/62는 직접 diagnostic 진입 후 실제 native cursor/No 분기와 응답을 실행한다.
41의 B→응답42도 따로 실행한다. Yes의 입력 초기화로 진행하지 않는다.
진단 checkpoint는 diagnostic_checkpoint로 격리하여 정상 진행의 부모로 쓰지 않는다.
고정40 fontCPU→OBJVRAM→화면픽셀·nickname·choice 좌우커서/행 간격·페이지 지움·keyWait를 검증한다.
이 진단은 실제 저장 답변 값, 정상 질문 선택, 한글 입력/저장/재표시의 증거가 아니다.

## 답변 버퍼 조사

`inspect_gutsman_answer_buffers.py` / `gutsman_answers_v1/answer_buffer_static.json`.
F9 정상 wrapper는 FC만 확장 처리하고 다른 명령은08051575로 전달한다. 원본 F9 slot 불변이라고 잘못 주장하지 않는다.
0C consumer080517D0, descriptor table080526D0, slots1C/1D/1E의 포인터는02026080/02026100/02026180.
descriptor의 r2 인수는 각각512이다. 겹치는 범위를 독립적인 영구저장 레코드나 한국어 용량으로 해석하지 않는다.
copy destination은02010AC0 + (context+64 halfword <<7), helper0800094C 호출 이후context+2C로 표시한다.
이것은 source-pinned 정적 연결만 입증한다. 실제 writer/필드 identity/입력 확정/저장 reload의 provenance는 미해결이다.
schedule observer도02010AC0을 관찰하지만 같은 transient output 주소가 같은 producer를 뜻하지 않는다.

## 검증 상태

최초 두 빌드 ROM 동일,150literal static/font/control/roundtrip/35미선택script 보존 검사 PASS.
거츠맨90+keyitem20 테스트,732 Python AST PASS. CPU624는 합성 helper 계약이며 상점 정상 경로 증거가 아니다.
정상29의3문구/일본어키보드 crop, PET22/소개2/넘버맨3/새native save/cold continue 대표 회귀 PASS.
신규40/24고유페이지 fontCPU/OBJVRAM/픽셀·native nickname·row2 choice/좌우커서·페이지 지움 PASS.
8개No와41의B→응답42 PASS. prefix는 printStringBuffer 이전, 모든진단은 input-init 이전에 정지했다.
24페이지와플러그아웃6화면을 직접 확인했다. 저장답변 버퍼 값을 채우거나 한글입력을 검증했다고 주장하지 않는다.
`answer_runtime.json`, `answer_pages.png`, `plugout_regression/plugout_runtime.json`이 실행 증거를 소유한다.
최초_v1/_repro와_r2/_r2_repro 전체 ROM bytes/hash 동일. 현행 제품은 `_r2.gba`다.
runtime prefix/native save basename은 최초_v1이다. 최종 감사가runtime_stem을 명시하고 전체 ROM 동등성을 확인했다.
`final_identity.json`: 원본/ledger/append·기존59다른archive payload/73profile scripts/110unit,
폰트/advance/이미지/keyitem39/final machine code·CPU624·자체native save58/coldcontinue·독립재현 보존 PASS.
732 Python build-tool pins drift=[], 전체741도구pin 기록. 원본 SHA 불변.
현행 catalog/input hashes는 `analysis/full_scope_gutsman_answers_v1_r2/`다. 최초_v1 inventory도 역사로 보존한다.

## 다음 작업

catalog732/31,907literal: 선택2,542/미선택일본어27,506/기타검토1,859/errors0.
이 archive의 남은 일본어 literal은script31의3개다. 다음은 이 질문과 입력 전달 경계를 확인한다.
동시에 실제 입력 writer→확정→필드 저장→buffer 준비→정상 재질문→native save/cold reload를 추적한다.
한글 키보드/입력 ABI·편집/확정/모든 재표시/기존save 호환, 다른 내비/이미지·inline/fixed/날짜·RTC,
상점02031000 정상 경로·전체 인간 의미/용어/시각 검토·배포 검증은 미완료다.
