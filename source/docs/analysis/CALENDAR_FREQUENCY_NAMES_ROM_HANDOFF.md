# 동적 반복 주기 이름 — 이어받기

2026-10-08. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## ROM과 범위

ROM `poc/output/exe45_ko_development_calendar_frequency_names_v1.gba`.
SHA256 `9a635be2e6f26ff835bdafd742a2042143183c337e04dc1d5d77884a18bae06b`.
원본SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변.
누적2,345선택literal/58선택·674원본유지archive. 직전schedule-delete판보다5문구 추가.

- 6368E8:119..123: `1回のみ/毎日/毎週/毎月/毎年` → `1회만/매일/매주/매월/매년`.
- 기존 빈도선택기 이미지와 별도인 일반 대사 동적이름이다. 메뉴 이미지를 다시 번역한 수가 아니다.
- 같은archive 부모7개 projection을 해시 고정하고12개 단일writer로 통합.243미선택span 불변.
- `calendar_frequency_names_ko.json`, helper/spec mixed normal-dialogue literal profile, build flag `--calendar-frequency-names`.
- 첫ASCII1 native code02 보존, 한글custom4byte, E5 포함각10/9/9/9/9bytes, native32byte copy extent 내.
- source/skeleton/parent drift/capacity/registry/원래숫자 보존 검사 PASS.
- inventory `full_scope_calendar_frequency_names_v1`:732archives/31,907literals/errors0;미선택일본어27,703/기타1,859. 전체ROM 완전성 분모 아님.

## 검증 상태

main/repro/current_repro_r2는 같은SHA. 최종675tools drift=[]/원본불변 감사 PASS (`final_identity_audit.json`). r1 이후 누적삭제검사를 연결한report 변경을 r2에 고정했다. ROM 바이트 변경은 없다.
`tools/run_calendar_frequency_names.py`는 이전 누적정상경로 후 다섯빈도를 각각 정상등록하고 삭제첫페이지50에서 관측한다.
`tools/report_calendar_frequency_names.py`가 lookup→E5 staging→32byte memcpy→RAM→CPU/font/OBJ VRAM/화면pixels를 연결해 검사한다.
자체정상chain 전체완료, `report_calendar_frequency_names.py` PASS. 신규5개 모두normal lookup/copy/font/VRAM/pixels PASS. 원본119..123 주소에서E5까지의read,02014E54 stage32, source/target/LR이정확한32byte전송,02010C40 residency,각native ASCII1 또는custom4byte draw/CPU font reads/OBJ VRAM/실제화면pixels를검사했다. 첫줄끝x는1회만177/나머지166으로창오른쪽234안이다. 정상등록한식사삭제50에서각frequency가실제로선택된것이며강제script/빈도/record쓰기없이확인했다.
기존넘버맨저장/cold이어하기·거츠맨인사/PET/칩/격리알림renderer·달력조회/기념일이름·관리/일정삭제Yes/No/B·레코드유지/clearing 회귀 PASS. 격리알림은실제RTC발생증거가아니다. 이전전체calendar confirmation 보고서의모든증거가자동이전된것도아니다.
새생일/개교기념일확인과동일세션목록조회 PASS.5장합성 `frequency_names.png`를직접검토했고 `1회만/매일/매주/매월/매년`,식사,거츠맨초상/창경계가정상표시된다. 일본어목록제목/요일 등은여전히남는다.
보고서사전실행두번은수집중인script4/weekly-first result.json이아직없어중단됐다. 이를최종PASS로계산하지않았고완료후재실행PASS했다. 도구의초기 `else4` 문법오류는 `else 4`로수정했으며 ROM변경이아니다.
675Python AST 및 관련63tests PASS. 선택tests는 gutsman*,calendar_anniversary_confirmation,calendar_frequency_names,dialogue_chip_name.
재현 명령/flags/hash: `analysis/calendar_frequency_names_v1/rebuild.ps1`와 `build_recipe.json`.

## 남은 과제

665698:10 소지품 안내3문구는 기존 `next_inventory_drafts.json`의 수동초안이며 ROM 미반영이다.
닉네임 앞뒤 aggregate-template44px와 native one-option 경로를 확인해야 하며 suffix 단독non-growth 검사면제로 선택하지 않는다.
일정중복25/날짜삭제51의새5문구는여전히static-only. 휴일正月/다른행사9이름·날짜/요일이미지·전체이미지/inline/fixed population 미완료.
임의한글입력/편집→commit→모든redisplay→영구native fresh reload→기존save호환은 미해결이다.
같은세션이름조회나 넘버맨cold save 회귀로 이 과제를 닫지 않는다.
실제RTC/C40producer·기존wait-arrow53pixels/TVtransition1pixel·인간wording/presentation검토 미완료.
전체미번역번역 요청은 아직 완료되지 않았다.
