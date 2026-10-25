# 거츠맨 프로필 질문·반응 미번역 — 2026-10-09

## 제품과 범위

개발 ROM `poc/output/exe45_ko_development_gutsman_profile_v1.gba`.
SHA256 `256e901d04386db75b8e770c049483db21bac022c1b0ba32cd76b2d91ad22470`.
40literal 추가, 누적2,432선택literal / 60선택archive·672원본유지archive.
needs_review, NON-DISTRIBUTION, release_eligible=false. 전체 번역 완료가 아니다.

`translations/gutsman_profile_ko.json`은667044의97script 중20script/40literal만 선택한다.
27/29의 잘하는·어려운 과목 질문,32/33/34의 유치원·학교·회사 질문,
80..87/89..95의 변수 없는 답변 반응을 번역했다.88의 nickname 관계형 반응은 미선택이다.
입력 초기화·나이 checkGlobal·flags·페이지 구분·대기·native nickname과 다른77script는 보존한다.
기존 내비의 실제 대사를 바꾸지 않으며, 거츠맨667044만 추가한다.
호칭 뒤에는 기존 별명을 그대로 출력한 뒤 받침에 의존하지 않는 쉼표를 사용한다.

원본 어려운 과목 흐름은`gutsman-subjects-source-v1-weak`에서 확인했다.
첫 문장→두 번째 문장→nickname+과목 질문→원래 일본어 입력 화면으로 이어진다.
키보드 일본어·한글 입력/확정/재표시/영구 저장은 이번 번역 범위가 아니다.

## 재현과 증거 소유

`python -X utf8 tools/build_keyitem_full_rom.py --name <새_이름> --gutsman-plugout --gutsman-profile`
기존 primary immutable-source 빌드에40문구를 추가한다. 이전 patched ROM은 입력하지 않는다.
`--gutsman-profile`은`--gutsman-plugout`을 요구한다. 원본 및 과거 산출물/저장/증거를 보존한다.
독립 재현본`_repro.gba`와 동일 SHA256. 정적검사:97script·원본5225byte·pointer0x38138,
선택40literal·보존77script·control skeleton·binary/semantic roundtrip·전 글자 glyph/advance,
최대 literal 폭115px≤132px PASS.

`run_gutsman_profile.py`: 새 ROM cold→프로필→넘버맨→새 native 저장→checkpoint 없는
cold 이어하기→거츠맨 선택→인터넷→정상 플러그아웃→어려운 과목29의 실제 호출과 입력 UI.
`run_gutsman_profile_diagnostics.py`: 같은 ROM의 정상 호출을 먼저 검증한 뒤
로드 전 자체 checkpoint에서 나머지19script의 표시를 격리 진단한다.
원본 실행 reader0x0804FB76의 profile29 table read 하나만 alias하며 ROM/RAM write는 하지 않는다.
32는 원본 나이 dispatch를 변경하지 않고 UI header 이후를 선택하므로 나이 분기 실행 증거가 아니다.
진단 checkpoint는 별도 이름으로 격리하고 normal-play eligible=false로 기록한다.
이는 실제 응답·나이 조건 충족이나 한글 입력·저장 성공을 대신하지 않는다.

`report_gutsman_profile.py`:40문구의 font CPU reads→OBJ VRAM→최종 screenshot 픽셀,
nickname 원본 bytes/종결/폭·줄바꿈/문자좌표·페이지 지움 검사.
정상29의3문구와 별도 renderer 진단37문구를 분리해 기록한다.
`report_roll_plugout.main(...,navi='GutsMan')`: 새 ROM의 No/B/좌우/Yes/귀환 대표 회귀.
`audit_gutsman_profile.py`: 원본·header·append·쓰기ledger·재현·모든 선택입력,
기존59archive payload·glyph/advance·기존 이미지·keyitem39clone·최종hook·runtime·도구 identity.
기존 폰트·클론의 새 주소는 입력 크기에서 파생되며, 이전 절대주소와 같아야 한다고 요구하지 않는다.

최종 결과의 소유자는`analysis/gutsman_profile_v1/profile_runtime.json`,
`plugout_regression/plugout_runtime.json`, `cpu/report.json`, `final_identity.json`이다.
검증 실행 중인 기록을 PASS로 간주하지 않는다. 화면 합성은`profile_pages.png`.
새 주소의 keyitem selector CPU624조건 PASS. 이 CPU 결과는 bulk-zero helper 계약 기반이며
실제 GBA 상점 소비자02031000 실행 증거는 아니다.
합성fixture: profile5 + 기존 plugout4 + keyitem20 PASS.

추가 대표 회귀`pet_regression/runtime.json`: 새 ROM의 거츠맨 PET8scene/22literal,
소개2페이지·넘버맨계절인사3페이지, 선택 cursor/No/B/복귀·glyph/OBJ/pixel PASS.
질문29 종료 시 root가 유지되는 것은 원래 동작이다. 마지막 keyWait→3605/3606 flags→waitHold의
cursor11byte 진행과 profile 글자 추가 출력 없음, 입력 화면의(8,23)-(232,154)29,344pixel이
이전 원문 질문의 실제 입력 화면과 전부 동일함을 확인한다. root 변경을 전환 조건으로 쓰지 않는다.
진단 초기 실행의 질문27/32..34에는 마지막 질문 뒤 A가 한 번 더 포함되어 입력 화면에 도달할 수 있다.
이는 정상 입력/응답 증거로 사용하지 않는다. 현행 실행 도구는 마지막 대사 페이지에서 멈추도록 개선했으며,
기존 실행의 실제 actions는 각`result.json`에 보존한다. 원본 나이 분기/입력 저장을 변조하지 않는다.

최종 결과:40문구 font/OBJ/pixel/닉네임/지움 PASS(정상3 / 격리진단37).
플러그아웃7화면의4문구·defaultNo/No/B/좌우/Yes/거츠맨귀환 대표 회귀 PASS.
전체40문구와 회귀 합성화면을 직접 확인했다. 원본·header·append·쓰기ledger·독립재현·
모든입력·기존59archive payload·폰트/advance·기존이미지·keyitem39clone·최종hook·
자체새저장/cold이어하기·CPU624·runtime identity 최종 감사 PASS.
`final_identity.json`은 현행 도구 snapshot을 포함한다. 옛 제품 tool pins를 현행 감사로 대체하지 않는다.

## 다음 작업과 남은 경계

catalog732/31,907literal 재집계: 선택2,432 / 미선택일본어27,616 / 기타검토1,859 / errors0.
현재 질문·반응 외에도667044의1..26/30 등 가족·취향·동경하는 인물 질문과
그 답변의40..63 재표시 문장이 미선택이다. nickname·printStringBuffer·선택지 관계를
원문과 실제 흐름으로 연결한 뒤 다음 묶음을 선택해야 한다.
일본어 입력 화면에 실제로 진입한 정상 증거는`gutsman-profile-v1-weak/step_003.png`에 남긴다.
입력/저장 호환 검증을 단순 대사 표시 검증과 합치지 않는다.
상점02031000의 정상 경로, 다른 내비, 전체 이미지/inline/fixed/날짜요일/RTC,
한글입력·편집·확정·모든재표시·fresh영구reload·기존save호환,
인간 의미/용어/시각 검토·전체 배포 검증은 계속 미완료다.
