# 거츠맨 기념일 확인·기본 이름 인수인계

날짜: 2026-10-08. 개발 입력; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 현재 산출물

- ROM: `poc/output/exe45_ko_development_gutsman_calendar_anniversary_confirmation_v1.gba`
- SHA256: `23fa4ce6d4e5c51c1bb45a5b64e72b5e6652c8b4a1aace9c764d5a475ee12088`
- 크기: 11,143,312 bytes.
- 원본 SHA256: `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
- 2,304선택literal/58선택archive/674원본유지archive. catalog732/31,907literal, 미선택일본어포함27,744/기타검토1,859/parse errors0. catalog는전체ROM완전성분모가 아니다.

## 이어받은 작업과 신규 번역

이전 register판 `37132321d706f824af0badd922ff356b6c6e22e286ba27fd4b28e55f2bbbc53e`의 날짜1·종류2(4literal), anniversary판 `2536ac0a3c4f237912899e5e74c5577e087e430c556636e38d4cdb54cf3ffd77`의 질문31·세항목73(2literal)을 보존했다. 중단된 anniversary판 검증을 마무리했다.

| ID | 원문 | 신규 번역 |
|---|---|---|
| 665698:33:0 | これでいいでガス? + LF×2 | 이렇게 하면 되거스? + LF×2 |
| 665698:33:1 | はい + 공백×2 | 예 + 공백×2 |
| 665698:33:2 | いいえ | 아니오 |
| 6368E8:74:0 | たんじょう日 | 생일 |
| 6368E8:75:0 | そうりつきねん日 | 개교기념일 |

선택 입력은 `translations/gutsman_calendar_anniversary_confirmation_ko.json`(읽기전용15+신규3), `translations/calendar_anniversary_presets_ko.json`(읽기전용5+신규2)이다. 부모 파일의 해시와 전체projection을 검증하며 archive당writer는 하나다. 후속변경에서 부모를 수정하면현재child는실패하므로 새근거로재정합해야한다.

신규 flag `--gutsman-calendar-anniversary-confirmation`은기존calendar chain과preset counter PoC를필수로요구한다. 재현설정은 `gutsman_calendar_anniversary_confirmation_v1/build_recipe.json`; 새빌드이름으로 `rebuild.ps1 -BuildName <new_name>` 실행. 모든빌드는immutable원본을입력으로사용한다.

## 정적 및 실행 검증

- 직전 anniversary판 대비 달라진 compiled archive는6368E8(5→7),665698(15→18) 두개다. 바뀐script는각각74/75와33뿐이며 다른script bytes는동일하다. header/final diff audit PASS.
- 이름+E5는9/21bytes,22byte name field와10logical-cell confirmation 범위에맞는다. school tail은1byte, birthday tail은13byte zero로commit된다. 원문키보드와다른기본이름은변경하지않았다.
- 정상콜드부팅/넘버맨저장/cold이어하기/거츠맨선택/달력진입부터새ROM자체경로로재생했다. observer만사용했고RAM/flag/read-alias개입없다. capture 및checkpoint ancestry는exactROM SHA에묶인다.
- 질문31/selector73:48decoded cells/3072bytes source→stage→VRAM,3×10visible OBJ cells/3840pixels,blank clearing/원래geometry/palette,3focus/B/세accept PASS. 실제source font619EF8/mono role1,3,4 경로를관측해초기big추정을정정했다. 최초실패를성공으로덮거나ROM기준을완화하지않았다.
- 확인33:3literal의CPU font reads/OBJ VRAM/화면마스크,기본Yes(85,136)·No(121,136),두기본이름의10cell표시/clearing PASS.
- No/B는script31복귀·32byte record불변. Yes는script0복귀·정확한header/name/E5/zero-tail commit.
- 생일 record: `35000001010600000000f9fcdd14f9fc7c1be500000000000000000000000000`.
- 개교기념일 record: `35000001010600000001f9fc1c00f9fc5001f9fc3002f9fc5005f9fc7c1be500`.
- 같은세션목록:script72의buffer1+10공백을각각12/15cells(768/960bytes)로전송. 다음행과1024bytes간격에서256/64bytes여유. BG2/charbase8000/screenF000/palette10,10visible cells/1280pixels,ROM폰트/stage/VRAM/타일맵/화면마스크 PASS. 직접화면확인완료.
- 기존넘버맨새저장/실제cold이어하기·귀환,거츠맨인사/PET8장면/알림6페이지/칩13/일정질문·확인·홈누적회귀 PASS. 기존그래픽payload 및 ‘통신’수정 유지.
- 46거츠맨tests+2신규negative/source-control tests+3chip-name tests=51 PASS;657Python AST 및registry JSON PASS.

## 증거와 최종 감사

`gutsman_calendar_anniversary_confirmation_v1/runtime.json`에전체누적검사,branch record,픽셀증거를저장했다. `anniversary_confirmation.png`는두확인창/No focus/확정뒤home, `anniversary_queries.png`는두등록후재조회, `calendar_anniversary.png`는세selector focus 및분기이다. `poc/runtime/gutsman-calendar-anniversary-confirmation-v1-*`가정상경로원자료다.

main와독립`_repro`,최종`_current_repro_r2`의해시일치및현재도구657개/원본보존감사는 `final_identity_audit.json` 참조. `_current_repro_r1`도같은ROM해시이며후속report보강전도구기록으로보존했다.

## 남은 작업과 재개점

- 확인된다음미번역:기념일B취소후등록선택665698:7:0~2,조회날짜질문665698:6:0,목록正月=6368E8:130:0,날짜/요일그래픽. 개별문구를다른consumer에일괄치환하지말것.
- 기타기념일선택은원문키보드6368E8/script9진입만확인했다. 임의한글이름입력/편집은지원완료가아니다.
- 기념일이름native save→fresh-process reload는이번판미검증이다. 넘버맨저장회귀로이를대체하지않는다. 모든재표시consumer/기존save호환도미해결.
- 실제RTC알림/C40producer,전체이미지·inline/fixed population,기존wait-arrow53pixel/TVtransition1pixel차이,문구·presentation인간review가남아있다. 전체번역/출시완료가아니다.
