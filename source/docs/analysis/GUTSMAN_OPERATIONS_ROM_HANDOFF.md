# 거츠맨 귀환·접속·메일 알림 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_operations_v1.gba`.
SHA256 `5b03c125ab80d1e56efa0ca450fc1eef5eeb7a99b62881abc7a20db326a2abe3`.
신규31 literal=17번역 문구+14원본 유지 `!!`. 누적2,219선택 literal/52선택·680원본 유지 archive. 전체 요청 완료 아님.

## 원본·번역·정적 검증

전체3TPL 원문과 native GutsMan group 관계를 확인했다. 귀환6663B8:120bytes/4slots/root038118(intro+8), 접속6664D0:75bytes/3slots/root038120(intro+16), 메일666820:1337bytes/255slots/root038128(intro+24).
원문TPL SHA와 payload SHA는 각각 다음과 같다.

- 귀환: `3272f7060b455a882c8c6ab4c1abafe64327765d5c775018683e93934a021359` / `7c1410a2b14758a560a3ebc60abdbc7ae8fa99f5b9bfd7e1fe5418ae34f4fe5b`.
- 접속: `4f8d7f78318d00838083600af2eae557948994d1978a9b2942eb137e160632bb` / `4e1ba8197589557b1eb2499289f9c3791a765028749f09bdc21cc227f54dbea6`.
- 메일: `b60dd4aec45016515d02053f5cf45e9a83d8c5dd354bcbc9e96b726fc54a7ce5` / `d4cf2e86ad87ce890d855bf60b7e9ebf014981eae826dfb810eaac7845561540`.

개별 작성 `tools/draft_gutsman_operations.py`; 자산 `translations/gutsman_return_ko.json`, `gutsman_jackin_ko.json`, `gutsman_mail_alert_ko.json`. 기존 거츠/거스 말투 후보 유지, 귀환 성공·패배의 의미 구분, 명시된 거츠맨.EXE, 트랜스미션, 메일 알림 보존. 넘버맨4649 승인 재사용 없음. 모든 문구 인간 검토 대기.
모든 stable ID/원문/숫자/newline·command/slot/native variable 보존. 귀환 type1/keyWait/clear/waitHold, 접속 type3/30frame 대기/flag3603·3651, 메일 sound155/96frame대기2회/이름 삽입3개/flag3585·623..626·680·681·mail8920..8926·tournament receive 보존. 이름 뒤 쉼표 첫 행11px 원문 동일. protected nonliteral slots 각각2/2/241. 최대117/91/82px, Hangul/native punctuation glyph·roundtrip·제어 검사 통과. 실제 게임 진행·RTC·저장 코드 변경 없음.
초기메일 `!!`와 문장끝 `!!`가 같은 script에 두 번 있어 초기 static checker의 단순 문자열 유일성 검사 실패를 발견했다. ROM 변경 없이 source-pinned `f604e18d` 화살표 명령과 `fd009b00ed006000fd009b00ed006000f1` 알림음/대기/clear boundary로 초기 literal만 유일하게 식별했다. 원본·최종 두 위치 및 정확한 command anchor 유일성을 요구한다. 임의 첫 match/픽셀 예외 아님. 관련154 tests 재실행 PASS.
이전 거츠맨 PET flags+`--gutsman-operations`, immutable original에서 빌드했다. 기존 patched ROM을 입력으로 쓰지 않았다. main/repro/current_repro/current_repro_r2/최종current_repro_r3 동일 SHA. 마지막 감사583Python tools drift=[] PASS, immutable original SHA 보존. 결과 `analysis/gutsman_operations_v1/final_identity_audit.json`. 기존 모든 빌드·실패·실험·saves 보존.

## 실행 검증 상태

`tools/run_gutsman_operations.py`의 자체 fresh FF→넘버맨 선택→저장→checkpoint 없는 cold 이어하기→넘버맨3페이지→거츠맨 첫 인사2페이지/PET8장면·22항목/29focus·No수락·B취소·복귀 회귀 PASS. 기존49 archive payload/선택 자산/그래픽15라벨5블록 actual ROM bytes 모두 동일, ‘통신’ glyph 수정 유지. 결과 `analysis/gutsman_operations_v1/pet_regression/runtime.json`, composite `normal_pet_prompts.png`.
fresh FF64KiB 자체 저장 SHA `046446bad3e5069b17009058279c2a291af9a683effb0d9da149c8444e6cc970`, native success script58, 직후snapshot/현재디스크 일치. 과거 우드맨 후보와 같은 SHA지만 이번 자체 FF 시작·입력 receipt로 생성, 다른 후보 save/state 수입 없음. 다른 테스트 saves 보존. 넘버맨 save/cold continue 회귀이며 한글 이름 persistence/거츠맨 저장 증거 아님.
초기 `jackin-prompt`에서 곧바로 down을 눌렀으나 메뉴는 토너먼트에 남았고 script2 질문을 수락했다. `transmission`의 원본666D5C:10 미등록 안내로 이어져 native 접속 lifecycle 검사 FAIL. 이103샘플/결과·체크포인트는 보존하고 접속 통과로 세지 않는다. 같은 ROM·동일 select-gutsman parent에서 선행 선택 입력을 놓는 none60을 별도 단계로 둔 `jackin-prompt-r2`의 실제PET3 질문을 확인한 뒤 일반 A를 수락했다. ROM/RAM 쓰기·read alias·RTC 강제 변경이나 대사 root alias 없음. 미등록 안내는 아래 다음 미번역 대회10항목에 포함했다.
`transmission-r2`103샘플의 native6664D0:1 entry1회/20glyph/30frame 원본 대기 `ed001e00`/종료 후 추가draw없음 검사 PASS. step66..93/frame67..94의 완성28샘플에서 모든 CPU font reads/ROM glyph→OBJ VRAM→화면 픽셀/geometry/blank clearing strict PASS. 최대91px 행 포함, 실제 거츠맨 초상/일반 입력이다. 원본 wait30은 보존하며 frame64 첫 wait cursor→frame95 첫 release의 31프레임 관측 간격(프레임 단위 샘플링)을 기록한다. 마지막 step103은 인터넷의 거츠맨으로 정상 이동했으며 메인 에이전트가 접속 화면·PET composite·이후 인터넷 화면을 직접 확인했다. 결과 `analysis/gutsman_operations_v1/runtime.json`, 화면 `normal_transmission.png`.
전환 중 step63/frame64의 마지막glyph VRAM132pixel/화면20pixel, step64..65/frame65..66의 화면10pixel 차이는 strict FAIL로 보존하고 완성페이지로 세지 않는다. 동일 calls/draws/font_reads trace의 이후 step66 strict PASS와 대조: VRAM 변경은 마지막 느낌표12×11glyph footprint 내부, 화면 변화는 마지막 두 느낌표 footprint 내부에만 존재한다. 이 사실은 기록하되 원인이나 모든 중간 프레임 무결성을 추정하지 않는다. 새 픽셀 면제/renderer code 변경 없음.
실제 ROM native roots: 거츠맨intro038110→08807E1C/PET038114→08807EF0/귀환038118→088085E8/접속038120→088086B8/메일038128→08808720, 넘버맨seasonal0382AC→0880D9D4, 포르테seasonal03857C→08815560. 각각 자기 pool 유지, 이전 넘버맨 초상 진단 alias는 ROM에 포함되지 않아 복원 수정 불필요.
귀환2/메일28항목은 현재 static-only이며 성공·패배·메일 수신 조건/동적 이름 전체 소비 증거 없음. PET 재질문/중단22항목, 실제 통신/거츠맨 저장도 별도 미검증 범위다.

## 남은 작업

현재 catalogue `analysis/full_scope_gutsman_operations_v1/inventory.json`, `literal_backlog.json`:732archives/31,907canonical literals, 선택2,219/미선택 일본어 포함27,823/기타1,865. Catalogue는 전체 ROM 번역 분모가 아니다.
다음 거츠맨 대회666D5C:473bytes/25slots/root03812C=08666D5C, intro+28. 전체TPL 읽음/미선택10항목 확인. TPL SHA `142b517fc402bcb024d5dfd814c78a1e5b070d0ac05520276bf229ebc566e434`; payload SHA `fc320d1c830dfa2984a693787f92e26d3c46421126a9a2f3af3f354ec44a1a7f`. 패배·우승·미등록·우승 목표4슬롯의 문맥과 nickname뒤 `と`/`!`, 원문숫자2, callCancelMenuTransition/flag3603 경계 보존 필요. 번역/등록/신규 빌드 입력 미작성.
전체 graphics/inline/fixed-string population, 미실행 이벤트·날짜·성별·재질문, 한글 이름 입력·편집→committed record→모든 재표시→영구 재로드→기존save 호환, 이전 native wait-arrow53pixel 차이 미해결. 가장 어려운 이름 조건을 이번 접속 검증으로 대체하지 않는다. 배포·완역 선언 없음.
