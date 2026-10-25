# 거츠맨 달력 조회·복귀 메뉴 — 이어받기

## 빌드와 범위

- ROM `poc/output/exe45_ko_development_gutsman_calendar_navigation_v1.gba`
- SHA256 `2f68c4df93067b78957b69c20f20fb55dd2569eeb32e616de094a648b0b02d59`
- 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 원본 불변.
- 누적 2,308 literal / 58 선택 archive / 674 원본 유지 archive.
- 직전 확인판 대비 665698 scripts6/7만 변경. 기존18개 literal을 해시 고정 부모로 유지한22개 단일 writer.
- 새문구: 6:0 `어느 날의 일정을\n볼 거스?`, 7:0 `뭘 등록하거스?\n`, 7:1 `일정\n`, 7:2 `기념일`.
- 복귀 메뉴7은 초기 메뉴2와 다르게 default=1(기념일). 이 차이와 vertical width7/option/BSeparate/targets/waitHold 보호.
- `translations/gutsman_calendar_navigation_ko.json`, helper `tools/gutsman_calendar_navigation.py`, build flag `--gutsman-calendar-navigation`, registry `calendar-navigation-v1`.
- main/repro/current_repro_r1/r2/r3 동일 SHA 확인. focus-only 검사 모델 수정 후 final current 도구 재빌드 r3로 최종감사 PASS: 661 tools, drift=[], 원본불변 (`analysis/gutsman_calendar_navigation_v1/final_identity_audit.json`).

## 현재 확인

- source/부모 projection·source controls·원문 재추출·인코딩/폰트·레지스트리·포인터·roundtrip 검사 PASS.
- `analysis/full_scope_gutsman_calendar_navigation_v1/`: 732 parsed archives,31,907 literal, parse errors0; 미선택 일본어27,740/기타 검토1,859. 전체ROM 완전성 분모 아님.
- 49개 거츠맨 테스트+2개 기념일 확인+3개 chip-name=54 PASS; 661 Python AST/registry PASS.
- 런타임 검증 완료. 실행 `python -X utf8 tools/run_gutsman_calendar_navigation.py`; `tools/report_gutsman_calendar_navigation.py` PASS. 신규4문구·cursor·두accept·두B/record불변, 기존 확인33/생일·개교기념일/같은세션조회 이름/CPU/font/stage/VRAM/pixel PASS. 직접6장 합성화면 확인 `calendar_navigation.png`.
- 정상 저장/cold이어하기/넘버맨 귀환3·거츠맨 인사2/PET8장면22literal, 격리알림renderer6페이지·식사nickname2샘플·칩13·합성CPU64vectors PASS. 알림은 normal RTC 발생 증거가 아니다.
- focus-only 첫 검사는 draw events가 없다는 이유로 실패했다. 원인은 native cursor이동은 glyph재그리기 없이 기존VRAM을유지하는 것. ROM/문구/허용오차 변경 없이 parent13draw/font 공급→child기존glyphVRAM/화면pixels·cursor·root/script로 residency 검사를 정정했다. `initial_focus_check_failure.json`, 원래 evidence 모두 보존.
- 원문 일본어 baseline의 거츠맨 초상/창경계3ROI와 새script7 화면은 exact RGB일치 (`portrait_window_identity.json`, 양쪽normal route/hash검사); redraw/retention 검사와별개.
- runtime prefix `poc/runtime/gutsman-calendar-navigation-v1-`; 모든 evidence/save 격리, 기존 사용자 saves 불변. 동일 prefix 재실행은 거부하므로 실행 중 세션/완료 폴더부터 확인.
- report `python -X utf8 tools/report_gutsman_calendar_navigation.py`; 이 보고서는 새4문구/분기·CPU/font/VRAM/pixel·기존 확인/기본이름 재조회와 PET/save/알림/chip 회귀를 확인한다. 이전 full calendar report 전체를 새ROM의 PASS로 자동 승격하지 않는다.
- 재현 `analysis/gutsman_calendar_navigation_v1/rebuild.ps1 -BuildName <새이름>`; flags와 해시 `build_recipe.json`.

## 다음과 남은 한계

- `analysis/gutsman_calendar_navigation_v1/next_calendar_drafts.json`에 독립 UI 오류·삭제·덮어쓰기·장소질문·PET도움말19개 수동초안. source/newline identity PASS. 한글74glyph의 실제ROM font bytes=BDF, 문장폭최대116px/183px, 3행이하 사전검사 PASS (`next_calendar_drafts_static.json`). 이 값은 메뉴옵션의 배치 및 실제화면을 대신하지 않는다. **ROM 미반영**, 선택불가 policy, 누적2308에 미포함. 다음에는 실제 route/default/cursor/record/renderer를 확인한 뒤 child composite 선택.
- 목록 正月=6368E8:130:0 미번역. 기존 query2행 target0600A400은 mono native619EF8, source RAM020155F0에서389/304 glyph를 읽고 name2+spaces10=12cells/768bytes 전송. 이 경로와 새해 이름의 ROM→원문복사/record capacity를 검증한 뒤 번역할 것. 130..138은별도9개일본행사이름; 일본문화를한국명절로바꾸지않는다.
- 날짜/요일 그래픽, 모든 이미지/inline/fixed population 미완료.
- 임의 한글입력/편집→committed record→모든 재표시→영구 native save/fresh process reload→기존save호환 미해결. 넘버맨 save 회귀는 기념일 영구저장 검증이 아님.
- RTC/C40producer/실제알림, 이전 wait-arrow53pixel/TVtransition1pixel, 인간 wording/presentation review 미해결.
- 다음 삭제메뉴의 정상 접근원문을 추가 확보했다. `next-delete-menu` 첫 시도는 hold4가2회이동을뜻한다는 가정을 기각: 실제query6→list9. 보존했다. `next-delete-menu-r2`는 down2→release→down2→A로script5 진입(step5), 이어A에서빈일정목록으로전환(step6). RAMscript5가잔류해도메뉴표시를뜻하지않음. 이checkpoint에서추가down/A한 `next-delete-anniversary`/`next-delete-anniversary-confirmation`도빈일정목록이었으며기념일목록/삭제확인증거가아니다. B는delete-selector가아닌home0으로복귀했고, 이어r3는등록날짜1/종류2였다. 이실패이름들도보존; 기념일삭제로승격하지않음. 원래정상home에서A를한번덜누른5-action selector checkpoint를다시만들어추적한다. 이normal source 경로는 다음삭제번역문맥 증거이며현재4문구검증에포함하지않음.
- 전체 요청 미완료. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 후속 삭제 경로 확정

`next-delete-selector`는 정상home에서5-action으로script5 selector 자체를 checkpoint화(마지막 불필요한A 제거). `next-delete-anniversary-list`에서 실제기념일목록/생일행 확인; RAMscript5는목록에도잔류하므로화면·상태를함께본다. `next-delete-confirmation-v2`는실제로script52/root08807E40에진입하여 `1/1`, `생일`, 일본어삭제질문의첫페이지를표시한다. Yes/No는원문52의다음페이지에있다. 동적생일name출력정상, 삭제확인은미번역. 다음2번B입력을 `next-delete-cancel`에보존했으며삭제Yes는누르지않았다. 마지막화면은생일이남은기념일목록이며32byte레코드불변 PASS; RAMscript52잔류만으로확인창잔류라고판정하지않는다. 새source52의실제동적이름·월일·인용부호·취소후목록문맥증거로사용; 현재4문구의번역추가나52전체검증완료로계산하지않는다.
