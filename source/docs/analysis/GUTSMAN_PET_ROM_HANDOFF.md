# 거츠맨 PET 메뉴 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_pet_v1.gba`.
SHA256 `e0e24bbb1b6eaa5bdcac2553fa17569654baa9b3dc79bbf47202d86f395c6686`.
신규44 literal=16문구+28예/아니요 라벨. 누적2,188선택 literal/49선택·683원본 유지 archive. 전체 요청 완료 아님.

## 원본·번역·빌드

665F3C:1147bytes/22slots/root038114. Source payload SHA `45aa744818878d7b67797fcbfc1aefcbc741ca240bc16ff529bfbec67713f719`; TPL SHA `7e61d76a8f55d97d703b40e67c3334d2eb4c6b0062358cc22cc31e30d9cccb01`.
전체TPL 원문을 읽었다. 명시된 거츠맨 장비/거츠맨 이야기의 화자와 original root038114=08665F3C/intro038110+4의 native group 관계 확인. 원문의 초기2..8과 재질문10..16,8의 저장 화면 진입과16의 현재 데이터 저장 구분 보존.20은 거츠맨의 이야기가 아직 끝나지 않았다는 원문이며 임의의 훈계나 친밀감을 추가하지 않았다. 이전 거츠·거스 말투 후보 유지, 문구·명칭·말투 인간 검토 대기. 넘버맨4649 승인 전용 없음.
44개 stable ID/원문/숫자/newline 경계·선택지 빈 행/Yes의 뒤2공백/모든 command·옵션·select targets·flag3584/3585/3588/3615·global30=120 보존. 이름 삽입 없음.0/9/17/18/19/21의6 nonliteral slots 보존. source9의16bytes/실행 flags도 동일. 실제 저장 코드·RTC·게임 진행은 변경하지 않았다.
자산 `translations/gutsman_pet_menu_ko.json`; 개별 작성 초안 직렬화 `tools/draft_gutsman_pet.py`. 이전 거츠맨intro 누적 flags+`--gutsman-pet`, immutable original에서 빌드. 이전 patched ROM을 입력으로 쓰지 않았다.
151관련 tests, source/control/numeral/glyph/3줄132px/14option rows/roundtrip 검사 통과. 실제 최대116px는5/13의 데이터 라이브러리와16의 현재 데이터 문구 첫 행이다. 선택지 누적 advance92px는 prefix24+space8+예12+뒤공백16+space8+아니요36이다. font advance/화면 proof는 실제 glyph metadata로 별도 계산한다.
main·`_repro`·`_current_repro` 3독립 동일 SHA.578Python tools drift=[], 원본 SHA 보존: `analysis/gutsman_pet_v1/final_identity_audit.json`.

## 실행 검증 상태

`tools/run_gutsman_pet.py`의 자체 cold→넘버맨 선택→정상 저장→checkpoint 없는 cold 이어하기→내비 선택/넘버맨 새해3페이지 회귀 완료. 같은 후보의 normal-reload-select parent에서 거츠맨을 left/A로 정상 선택했다. 거츠맨 첫 인사2페이지 회귀는 별도 observer로 같은 parent에서 확인했다. 다른 후보 save/state 수입 없음.
`tools/report_gutsman_pet.py` strict 최종 검사 PASS. 실제 거츠맨 대기1/초기 질문2..8의8장면,22 literal(8문구+14선택지)과30완성 화면 proof 확인.29입력 상태의 relocated pool/script/OAM cursor(Yes x108,No x144,idle x220)를 검증해 포커스 이동/No 수락/B 취소/복귀를 확인했다. ROM glyph→OBJ VRAM→화면 픽셀 및 CPU font read/geometry 통과. 본문 빈 영역은 idle행0/질문행0..1 검사, 선택지 글자는 별도 full glyph 검사한다. 원본 animated cursor 사각형 안의 글자 배경만 독립 처리하는 기존 PET checker를 재사용하며 glyph ink/shadow와 ROM→VRAM 검사는 면제하지 않았다. 새 예외나 검사 완화 없음. 최대116px 데이터 라이브러리 질문은 이번 정상 장면에 포함한다.
메인 에이전트8장면 composite와 저장 질문 No 포커스/취소 후 idle 화면을 직접 확인했다. 결과 `analysis/gutsman_pet_v1/runtime.json`; 화면 `analysis/gutsman_pet_v1/normal_pet_prompts.png`. 전환 중 모든 프레임·음성·하드웨어 증거 아님.
기존48선택 archive payload·선택 자산 SHA와 그래픽15라벨/5블록 위치·길이·SHA·실제ROM bytes 전부 동일. ‘통신’ glyph override 유지. 전체 이미지 완역이나 신규 전체 이미지 QA를 뜻하지 않는다. 원본·과거 후보·실험·테스트 saves 보존.
native bindings: 거츠맨intro038110→08807E1C/PET038114→08807EF0, 넘버맨seasonal0382AC→0880D29C, 포르테seasonal03857C→08814E28. 각각 자기 번역 pool 유지. 앞선 초상 진단 alias는ROM에 포함되지 않는다.
fresh FF64KiB에서 native save 성공script58 확인. 저장 SHA `9929f373bb564064efd13b73ae9efe0b10c626d369b94f741bfd532fd01259bb`, 직후snapshot/현재디스크 동일. 과거 일렉맨 후보와 같은 SHA지만 이번 자체FF시작·입력 receipt로 생성 확인, save 수입 없음. 다른 테스트 saves 보존. 저장/cold continue는 넘버맨 회귀 경로이고 거츠맨 저장·한글 이름 persistence/기존save 호환 증거가 아니다.
정상 선택·입력만 사용하고, ROM/RAM 쓰기·read alias·RTC 변경은 하지 않는다. 모든 초기 질문은 No 수락/B 취소로 되돌아온다. ‘예’ 수락 이후 실제 메뉴 진입이나 통신 상대/네트워크 작동을 검증했다고 주장하지 않는다.
10..16 재질문/20중단 경로의22항목은 static-only. 가장 어려운 미해결 조건인 한글 이름 committed record/모든 재표시/영구 재로드/기존save 호환을 이번 PET 검증으로 대체하지 않는다.

## 남은 작업

최신 catalogue `analysis/full_scope_gutsman_pet_v1/inventory.json`, `literal_backlog.json`:732개/31,907canonical literals, 선택2,188/미선택 일본어 포함27,840/기타1,879. Catalogue는 완전한ROM 번역 분모가 아니다.
다음 묶음 후보: 거츠맨 귀환6663B8(2 literal), 접속6664D0(1), 메일 알림666820(28). 세TPL 전체를 읽었다. Original roots038118/038120/038128은 같은 거츠맨 group에서 각각intro+8/+16/+24; 귀환·패배 문맥/명시 ガッツマン.EXE/‘메일’ 알림과 nickname3경계/96frame2회·tournament receive·mail flags 소비 구조 보존 필요. 아직 신규 번역·등록·빌드 입력 미작성. 서로 같은 renderer 결과라도 접속 type3/timed30frames와 메일 동적 이름·실제 이벤트 조건은 별도 검증 범위다.
세원문 source hashes: 귀환TPL `3272f7060b455a882c8c6ab4c1abafe64327765d5c775018683e93934a021359`/payload `7c1410a2b14758a560a3ebc60abdbc7ae8fa99f5b9bfd7e1fe5418ae34f4fe5b`; 접속TPL `4f8d7f78318d00838083600af2eae557948994d1978a9b2942eb137e160632bb`/payload `4e1ba8197589557b1eb2499289f9c3791a765028749f09bdc21cc227f54dbea6`; 메일TPL `b60dd4aec45016515d02053f5cf45e9a83d8c5dd354bcbc9e96b726fc54a7ce5`/payload `d4cf2e86ad87ce890d855bf60b7e9ebf014981eae826dfb810eaac7845561540`. 메일28개는14일본어 문구+14원본‘!!’로 구분한다.
전체 graphics/inline/fixed-string population, 재질문·중단/실제 선택 후 작동, 내비의 미실행 날짜·성별·이벤트, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환과 이전 native wait-arrow53pixel 차이 미해결. 배포·완역 선언 없음.
