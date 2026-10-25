# 거츠맨 일정 중복·삭제 — 이어받기

## 빌드와 범위

- ROM `poc/output/exe45_ko_development_gutsman_calendar_schedule_delete_v1.gba`.
- SHA256 `844e04d52c314de6cbdc58556ee18b22927c587992df12a6aa941da6abd80dcb`.
- 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 원본 불변.
- 누적2,340 selected literals /58선택·674원본유지archive. 직전management판보다9문구 추가.
- 665698 scripts25/50/51만 변경. 부모45문구를 해시 고정으로 보존한54문구 단일writer,227미선택script span 보존.
- 25:0 `、\n같은 시간에 다른 일정이\n있거스!`; 50:5..8 및51:6..9 `」\n삭제하겠거스!`, `괜찮거스?\n\n`, `예  `, `아니오`.
- 닉네임 뒤 첫줄 쉼표와 일정이름 뒤 첫줄 닫는인용부호 불변. 날짜/시간/요일/이름 buffer·선택targets/flags/waits/제어코드 불변.
- asset `translations/gutsman_calendar_schedule_delete_ko.json`, helper `tools/gutsman_calendar_schedule_delete.py`, registry `calendar-schedule-delete-v1`, flag `--gutsman-calendar-schedule-delete` (기존management chain 필수).
- source/부모45 projection·new9 identity·newline·레지스트리·미선택span·포인터/roundtrip/폰트/폭은builder검사로통과.
- inventory `analysis/full_scope_gutsman_calendar_schedule_delete_v1/`:732 parsed archives/31,907literal/parse errors0,미선택일본어27,708/기타검토1,859. 전체ROM 완전성분모아님.

## 현재 실행 상태

자체정상chain `tools/run_gutsman_calendar_schedule_delete.py` 완료. `tools/report_gutsman_calendar_schedule_delete.py` PASS. Prefix `poc/runtime/gutsman-calendar-schedule-delete-v1-`, 격리된테스트save. 동일prefix재실행거부: 기존evidence보존.

- 정상chain에서committed meal→삭제selector→일정목록→script50첫페이지→질문→Yes/No/B 완료. 신규50:5..8의4문구 CPU/font/OBJ VRAM/pixels·choice·clearing PASS. 25:0와51:6..9의5문구는static-only. 9개전체runtime완료아님.
- 동적식사name 실제RAM02010CC0/02010CC4→CPU font reads→OBJ VRAM/화면288pixels PASS. 이전birthday삭제의02010BC0과같은버퍼로가정하지않는다.
- Yes/No는OAM index1,16x16,tile1020,palette14,x85/121,y136. No/B는예상32byte식사record불변, Yes는32bytes전부0삭제 PASS. 목록의식사유지/제거와6장합성 `schedule_delete.png`, 별도B취소화면직접확인.
- parent관리판의birth삭제/등록슬롯질문·달력조회/복귀/기본이름·같은세션조회·넘버맨저장/cold이어하기·귀환3/거츠맨인사2/PET8장면22literal·칩13·격리알림6/식사2샘플·CPU64vectors 회귀 PASS. 격리알림renderer는실제RTC발생증거아님.
- 재현 `analysis/gutsman_calendar_schedule_delete_v1/rebuild.ps1 -BuildName <새이름>`, flags/hash `build_recipe.json`.
- 독립repro/current_repro_r1 완료, 세ROM동일SHA·670tools drift=[]/원본불변 PASS (`final_identity_audit.json`). 62tests/670AST+registry PASS. Static54문구/227미선택span/모든font/최대144px PASS. Runtime 증거 `runtime.json`.

## 다음과 남은 한계

새50첫페이지에서동적빈도 `1回のみ` 미번역을관측했다. 목록의기존빈도그래픽 `1회만`과별도consumer다. source후보6368E8:119..123의5문구와수동초안 `next_frequency_drafts.json`을보존했다. **ROM미반영/누적수미포함**. 다음에는callBufferEventFrequency→source119lookup→copy extent/다중byte decoder→normalfont경로를trace하고,같은archivefixed-cell/record다른consumer를보호해통합할것. 원문일치만으로lookup확정/전체화면번역완료로판정하지않는다.

665698의남은일본어prose는script10소지품안내3문구. `next_inventory_drafts.json`에수동초안준비, 아직ROM미반영/누적수미포함. 소유격의첫줄suffix는1px늘지만prefix는1px줄어총static44px를유지하는aggregate-template후보이다. 기존suffix단독non-growth검사를면제하지말고source-pinned전체template모델과실제native닉네임/one-option경로를검증한뒤선택할것. 구분자/공백/괄호/날짜·시간separator는비일본어원문그대로보호하며미번역prose로계산하지않는다.

휴일正月/다른행사이름·날짜/요일그래픽·전체이미지/inline/fixed population·임의한글이름/모든재표시/영구native save/fresh process reload/기존save호환·실제RTC/C40producer·이전wait-arrow53pixel/TVtransition1pixel·인간 wording/presentation review 미완료. 삭제의단일테스트record검사와영구저장검증을혼동하지않는다.

전체요청미완료. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.
