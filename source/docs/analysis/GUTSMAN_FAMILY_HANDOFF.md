# 거츠맨 가족 질문·선택지 — 2026-10-09

## 제품과 범위

개발ROM `poc/output/exe45_ko_development_gutsman_family_v1_r2.gba`.
SHA256 `c2cec16370b4ca5fa3b83eb1dab2f66d739145813b5d80be618c56c4790aa45a`.
667044:1..8의29literal 추가, 누적2,502선택literal /60선택·672원본유지archive.
needs_review / NON-DISTRIBUTION / release_eligible=false. 전체 번역 완료가 아니다.

형·오빠/남동생/누나·언니/여동생 유무, 있어/없어 선택지, 이름 질문과 없음 응답이다.
`translations/gutsman_profile_family_checked_ko.json`은 기존81unit의 원문/번역/상태를 그대로 이어받는다.
parent `translations/gutsman_profile_questions_ko.json` SHA256
`18d06a397c5708015b30ddb820a5a4b207d8fca369ddedd1ec3d284f0a6a68bb`.
새29문구는 주 에이전트 수동 초안이며, 플레이어 성별을 추정하지 않도록 older sibling을 두 한국어 호칭으로 표현한다.
native nickname의 뒤에는 받침 의존 조사를 고정하지 않고 기존 패턴의 동일 폭 쉼표를 쓴다.
source line/page controls와 두 칸 choice padding, default0/No→다음 짝수script와 세 번째 select target=continue,
3735..3738 absence flags와3605/3606 input 초기화는 그대로 유지한다.

## 빌드와 검증 책임

`python -X utf8 tools/build_keyitem_full_rom.py --name <새_이름> --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family`
기존 primary immutable-source 빌드. 과거 patched ROM을 입력으로 쓰지 않는다.
110선택literal/38script,97slot/5225byte/0x38138 pointer,59미선택script와 controls/roundtrip,
닉네임 suffix·standalone 선택행 prefix16px/공백/합성폭132px gate를 제품 빌드가 검사한다.
별도 `_repro.gba`로 독립 재현하며 결과가 있기 전에는 재현 PASS로 취급하지 않는다.

`run_gutsman_family.py` 최초실행은_v1 새ROM 자체 cold/profile/넘버맨/native저장/체크포인트없는 cold이어하기,
거츠맨 PET/소개·정상인터넷/귀환/기존29 질문·일본어키보드를 먼저 실행한다.
동일ROM 로드 전 자체 정상 checkpoint에서 native reader0x0804FB76 profile29 table read만 한 번 alias한다.
ROM/RAM write 없이1/3/5/7 entry를 선택한다. 그 뒤 native 선택 handler로 Yes/No 및 script1 B를 실행한다.
정상 sibling 선택 조건이나 가족 이름 입력/영구저장의 증거가 아니다. diagnostic checkpoint는 격리한다.
각 Yes는 이름 질문의 마지막 keyWait에서 멈추고3605/3606 입력 초기화 이후로 진행하지 않는다.
BSeparate=false인 script1의 B는 실제로 No 응답2를 선택했다. 세 번째 target=continue를 B 경로로 해석한 초기 가정은 기각했다.

`report_gutsman_family.py`는29literal 전부 fontCPU→OBJVRAM→화면픽셀과 native nickname/geometry,
choice label 간격·cursor 좌우·페이지 지움·정확한1/4byte 글자 뒤 keyWait를 검사한다.
No는 native2/4/6/8 점프와 응답, Yes는 이름 질문, script1 B는 native 응답2 점프를 구분한다.
기존29 정상3문구 회귀는 신규29의 정상 sibling 선택으로 집계하지 않는다.
결과 `analysis/gutsman_family_v1/family_runtime.json`, 화면 `family_pages.png`.
PET/소개/넘버맨 회귀는`pet_regression/runtime.json`, 플러그아웃은`plugout_regression/plugout_runtime.json`.
CPU624조건은`cpu/report.json`: 실제 상점02031000 경로를 대신하지 않는 합성 CPU 계약 검사다.
최종 원본·ledger·재현·입력·기존59archive/89profile scripts·81unit·폰트/이미지/keyitem 보존 감사는
`audit_gutsman_profile.main(...,family=True)`와 `final_identity.json`이 소유한다.
실행 중인 기록을 PASS로 간주하지 않는다.

## 검증 과정의 정정과 동일 ROM 증거

첫 `_v1` 제품·입력·캡처를 보존한다. 원래 draft `gutsman_profile_family_ko.json`의
context에 있던 B→continue 가정은 실제 native 응답2 관측으로 기각했다. 현재 checked 입력과 registry를 정정했다.
한국어 문구/배치/controls는 바뀌지 않았고, `_r2` 제품은 이 정정 입력을 primary빌더로 재생성한다.
`_r2`/`_r2_repro`와 최초 `_v1`의 전체 ROM byte identity가 확인될 때만 같은 hash의 실행 증거를 이관한다.
runtime prefix/native save filename은 최초 `gutsman-family-v1-` / `exe45_ko_development_gutsman_family_v1.sav`를 유지한다.
최종 감사는 runtime_stem을 명시하고 전체 ROM 해시 동일성을 검사한다. 다른ROM의 상태를 주입한 것이 아니다.
기존 일본어키보드 crop29,344pixels는 첫 step3에서커서주변12pixel이 달랐지만,
같은 native waitHold에서 입력 없는 step4 hold는 원래 기록과 전체 crop가 일치했다.
커서/영역 픽셀을 제외하거나 다른 픽셀을 허용하지 않았고, 두 프레임 cursor/root/script 상태를 검사한다.

## 최종 결과

`family_runtime.json`: 신규29literal/25고유페이지, fontCPU/OBJVRAM/화면픽셀·native nickname·choice spacing/커서·지움 PASS.
네 질문 Yes/No 및script1 B→native응답2, Yes마지막keyWait/input-init미실행 PASS. 신규정상선택0/격리진단29를 구분한다.
기존29정상3문구·키보드전환/PET22문구/소개2/넘버맨3/플러그아웃 대표회귀·native저장/cold이어하기 PASS.
_v1/_v1_repro/_r2/_r2_repro 전체 ROM bytes 동일, SHA는 위와 같다. 실행증거 이관의 basename/native save를 final audit에 명시했다.
최종원본/ledger/재현/입력·기존59archive/89scripts/81units/폰트/이미지/keyitem39/CPU624/실행identity 감사 PASS.
관련103fixture(거츠맨83+keyitem20)/728AST/737tool pins drift=[] PASS. 가족25페이지와플러그아웃6화면 직접 확인.
원본SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변.
현재선택asset hashes/catalog는 `analysis/full_scope_gutsman_family_v1_r2/`가 소유한다. 최초_v1 inventory는 역사 기록이다.

## 남은 작업

catalog732 /31,907literal: 선택2,502 /미선택일본어27,546 /기타검토1,859 /errors0.
다음은667044:40..63의 저장답변 printStringBuffer1/2/3, 등록/편집/재질문과 재표시 관계다.
일본어키보드 자체, 한글입력/편집/확정/모든재표시/영구reload/기존save호환은 미완료이며 범위에서 제외하지 않는다.
상점02031000 정상 경로·다른내비·이미지/inline/fixed/날짜요일/RTC·전체 인간 의미/용어/시각 검토와 배포검증도 미완료다.
