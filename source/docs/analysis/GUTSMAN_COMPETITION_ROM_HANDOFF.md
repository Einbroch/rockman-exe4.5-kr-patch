# 거츠맨 대회 대사 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_competition_v1.gba`.
SHA256 `d52e23a57df78ad2ce5c89dfd59bf77f3b6af4d7612c1d73e63138a40c37cc53`.
신규10번역 literal. 누적2,229선택 literal/53선택·679원본 유지 archive. 전체 요청 완료 아님.

## 원본·번역·정적 검증

666D5C:473bytes/25slots/root03812C=intro+28. Source payload SHA `fc320d1c830dfa2984a693787f92e26d3c46421126a9a2f3af3f354ec44a1a7f`; TPL SHA `142b517fc402bcb024d5dfd814c78a1e5b070d0ac05520276bf229ebc566e434`.
전체TPL 원문을 읽었다. 원본 root03812C=08666D5C의 거츠맨 group 관계 및 이전 operations-v1의 실제 거츠맨 미등록 script10 화면으로 화자·소비 문맥 확인.1은 패배와 다음 우승 다짐,2는 우승과 둘이 함께 이룬 영광/거츠 응원,10은 참가 미등록,20..23은 우승 목표의 응원이다. 새로운 적대감·칭찬·관계 의미 추가 없음. 기존 거츠/거스 말투 초안 유지, 인간 문구/말투 검토 대기. 넘버맨4649 승인 재사용 없음.
자산 `translations/gutsman_competition_ko.json`; 개별 작성 초안 직렬화 `tools/draft_gutsman_competition.py`. stable ID/원문/숫자2/newline/원본3줄 구조/모든 command·slot·keyWait·clear·waitHold·callCancelMenuTransition·flag3603 보존. 귀환·대회 승패의 의미 혼동 없음.25slots 중18nonliteral 보존.
우승2:1의 nickname뒤 と11px를 쉼표11px로 대체하고 다음행 ‘2명이 함께 이룬’으로 협력 의미를 명시했다. 이름 값의 받침에 따라 달라지는 한국어 조사 하드코딩 없음.10:0의 이름 뒤 !11px 원문 동일. Source-pinned suffix profiles/숫자2 검사 적용. 이름 전체 population/우승 정상 caller는 별도 미검증이다.
157관련 tests/source·control·numeral·glyph·geometry·roundtrip PASS. 실제 max132px는10:0의 ‘참가 등록이 안 됐거스’ 행이다. Hangul/native punctuation 정상 glyph 공급 검증. 기존 patched ROM을 입력으로 쓰지 않고 immutable original에서 이전 operations 누적 flags+`--gutsman-competition`으로 빌드. main/repro/최종current_repro_r2 3독립 동일 SHA;588Python tools drift=[] 및 immutable original SHA 보존 PASS. 결과 `analysis/gutsman_competition_v1/final_identity_audit.json`. 원본·과거 후보·실험·테스트 saves 보존.

## 실행 검증 상태

`tools/run_gutsman_competition.py`의 자체 fresh FF저장→checkpoint 없는 cold 이어하기→넘버맨3페이지→실제 거츠맨 첫 인사2페이지/PET8장면·22항목·29focus/No수락/B취소·복귀→PET2 토너먼트 질문 Yes→미등록10→A→메뉴 복귀 정상 경로 PASS. `tools/capture_gutsman_competition.py`는 정상 ROM·RAM 읽기 observer만 추가, ROM/RAM 쓰기·root read alias·RTC 변경 없음. 다른 후보의save/state 수입 없음.
`tools/report_gutsman_competition.py`의 strict 검사 PASS. 미등록10:0의 step2/3 두 완성 샘플에서 native entry1회/root08808D20/script10, keyWait cursor08808E99, source-native 이름4glyph44px+literal13glyph/총17glyph 확인. CPU font reads/원본 nickname glyph·advance/ROM→OBJ VRAM→화면 픽셀/geometry/3,316vacant pixels clearing PASS. 132px 둘째 행과 native 이름 뒤 !11px 포함, 글자 가림 없음. step4/5에서 relocatedPET08807EF0/script1로 복귀, 추가 competition calls/draws 없음. 메인 에이전트가 실제 미등록 화면/PET composite/복귀 화면을 직접 확인했다. 결과 `analysis/gutsman_competition_v1/runtime.json`, 화면 `normal_unregistered.png`; regression `pet_regression/runtime.json`, `normal_pet_prompts.png`. 모든 중간 프레임/음성/하드웨어 전체 QA 아님.
최초 checker는 과거 다른 후보의 ああくん/9b9ba2cae5를 고정 기대값으로 사용해 `own native nickname population` FAIL했다. 실제 이번 자체 정상 프로필의 name은 ああさま/9b9ba5b9e5이다. 동일한 이번 ROM의 정상 cold이어하기→넘버맨 대사 step6..8에서도 같은 native 이름 RAM bytes를 독립 확인했다. 이름 생성 규칙/차이의 원인을 성별 등으로 단정하지 않는다. ROM/번역/입력/상태를 바꾸지 않고 observer의 contiguous4glyph+E5terminator를 요구하고, source table의 실제 decode·원본96byteglyph·원본advance·CPU read·geometry·VRAM·화면 검사를 적용했다. 더 이상 다른 후보의 이름 값을 이번 입력 계약으로 간주하지 않는다. 체크 도구 수정 뒤 동일 재현 strict PASS/157tests 재실행 PASS. 초기 실패를 통과로 재표기하지 않는다. 실제 확인한 이름 하나만 증거로 세며 임의 name population이나 한글 이름 입력 proof 아님. 마지막 current_repro_r2 동일 SHA/588Python tools drift=[] 감사 PASS, 최신 receipt는해당 최종suffix를 사용한다. 첫 current_repro도 보존했다.
자체 fresh FF64KiB SHA `71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063`에서 정상 save success58 확인. 생성save SHA `fb82d51b06fadc2d37d3e87990edc0d1104b5abb9ee99df461803769915f65ca`, 직후snapshot/현재디스크 동일, 다른 테스트 saves 보존. 넘버맨 save/cold continue 회귀이며 거츠맨 저장/한글 이름 persistence proof 아님.
기존52선택 archive payload·선택 자산 SHA/actual ROM bytes, 그래픽15라벨5블록 위치·크기·SHA/actual ROM bytes 모두 동일, ‘통신’ 수정 유지. 실제ROM native bindings: 거츠맨intro038110→08807E1C/PET038114→08807EF0/competition03812C→08808D20, 넘버맨seasonal0382AC→0880DCBC, 포르테seasonal03857C→08815848. 각각 자기 pool 유지, 이전 초상 진단 alias는ROM에 포함되지 않는다.
패배/우승/격려의 나머지9항목은 static-only. native 승패·대회 참가·등록·임의 이름 입력/영구 저장 proof를 미등록 안내로 대체하지 않는다. 이전 접속/귀환/메일/기념일의 실행 결과도 이 ROM의 새 실행 증거로 간주하지 않는다.

## 남은 작업

현재 catalogue `analysis/full_scope_gutsman_competition_v1/inventory.json`, `literal_backlog.json`:732archives/31,907canonical literals, 선택2,229/미선택 일본어 포함27,813/기타1,865. Catalogue는 전체ROM 번역 분모가 아니다.
다음 일정 후보666F38:265bytes/14slots/root038134=08666F38, intro+36. TPL SHA `2f11d47888bf9857742cf94aa049c347dea49595302b2ddafed1c8affb9a5c64`, payload SHA `2facebf606327d4cf9df68310b945d90285de9b168999aef17c3697dd5ff4464`. 전체TPL 읽음;12literal 중 새 한국어가 필요한 독립5문구와 동적시간뒤1suffix, 원문 유지 punctuation6개를 구분했다. callBufferReminders/findSoon/findToday/printScheduleBuffer/name·hour·minutes·AMPM 경계, 숫자·시각서식과 동적event name 반복은 그대로 보존 필요. roll661754의 유사 구조는 가설로만 사용하며 대상 source/consumer 확인 후 등록한다. 아직 새 번역 입력·등록·빌드 미작성.66651C의 전체28slotTPL도 읽었으며 PET vs mugshot의 별도 소비 경로와 동적 이름·이벤트 suffix가 있으므로 단일132px 모델로 통합하지 않는다.
한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환은 여전히 가장 어려운 미해결 조건이다. 전체 graphics/inline/fixed-string population, 재질문·중단·미실행 날짜/성별/이벤트, 이전 native wait-arrow53pixel 차이 미해결. 전체 완료·배포 선언 없음.
