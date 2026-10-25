# 거츠맨 달력 관리 — 이어받기

## 빌드와 범위

- ROM `poc/output/exe45_ko_development_gutsman_calendar_management_v1.gba`
- SHA256 `d6aac577eedccd8b07c69576ebd33c20fdd02a1b7eb23c55142d52580dd946b9`.
- 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 원본 불변.
- 누적 2,331 selected literal / 58 선택 archive / 674 원본 유지 archive. 직전 navigation판보다 23문구 추가.
- 665698 scripts3/4/5/8/30/32/40..45/52만 변경. 부모22문구를 해시 고정으로 유지한45문구 단일 writer.
- 오류·삭제메뉴·덮어쓰기·장소질문·PET도움말19초안과 삭제확인52의4문구를 통합했다. 이전 `next_calendar_drafts.json`은 미반영 시점의 불변 기록이며, 그19문구를 새 child에서 명시적으로 선택했다.
- `translations/gutsman_calendar_management_ko.json`, helper `tools/gutsman_calendar_management.py`, build flag `--gutsman-calendar-management`, registry `calendar-management-v1`.
- source/부모22 projection·19초안 identity·source controls·인코딩/폰트·문장폭·레지스트리·포인터·roundtrip·230미선택 script span 검사 PASS. main/repro 동일 SHA.
- `analysis/full_scope_gutsman_calendar_management_v1/`: 732 parsed archives,31,907 literal, parse errors0; 미선택 일본어27,717/기타 검토1,859. 전체ROM 완전성 분모 아님.
- 52개 거츠맨 테스트+2개 기념일 확인+5개 chip-name=59 PASS; 666 Python AST/registry PASS.

## 실행 검증 상태

자체 정상경로 실행 완료, `tools/report_gutsman_calendar_management.py` PASS. 동일 prefix 재실행은 기존 evidence 보호를 위해 거부한다.

- runtime prefix `poc/runtime/gutsman-calendar-management-v1-`; 사용자 save와 분리한 테스트 영역.
- `tools/capture_gutsman_calendar_management.py`는 관찰 범위에 EWRAM을 추가한다. RAM 동적 이름의 실제 CPU glyph draw를 기록하며 RAM/ROM/state를 쓰거나 synthetic glyph event를 만들지 않는다.
- 삭제52는 첫 페이지의 월일/생일/닫는 인용부호 뒤 `삭제하겠거스!`, 다음 페이지 `괜찮거스?` 및 예/아니오. 첫 줄 인용부호를 그대로 두어 동적 이름에 새 조사를 연결하지 않는다.
- report `tools/report_gutsman_calendar_management.py`: 자체 baseline 회귀, 정상 삭제메뉴5·삭제확인52의7문구 및 등록위치32의1문구, 총 신규8문구 CPU/font/VRAM/pixels PASS. 23문구 전체 runtime 완료가 아님. 6장 합성 `calendar_management.png` 및 별도32 화면 직접 확인.
- 동적 이름 생일의 실제 RAM stream02010BC0/02010BC4→CPU font reads→OBJ VRAM/화면288pixels PASS. 인용부호 첫줄 유지, 다음확인창의 이전이름행 clearing PASS.
- Yes/No cursor는 OAM index1/tile1020/palette14/16x16, x85/121,y136. No와B는32byte생일record 불변, Yes는해당32byte record를 전부0으로 지움. 삭제후목록에서생일없음, No/B목록에서는생일유지 직접확인. 한 테스트 날짜/이벤트만 확인.
- 첫report는cursor를index2로가정해실패. 실제native index1 및두좌표를고정하여검사모델수정; ROM/문구/허용오차변경없음. `initial_cursor_check_failure.json`과모든원래evidence 보존.
- 정상 저장/cold이어하기·넘버맨귀환3·거츠맨인사2/PET8장면22literal·기존달력6/7/확인33/기본이름/동일세션조회·격리알림renderer6·식사2샘플·칩13·합성CPU64vectors 회귀 PASS. 격리renderer는실제RTC알림발생증거아님.
- `overwrite-candidate`라는 시도이름과달리 실제로는32등록슬롯질문→31입력에진입했으며30덮어쓰기증거아님. `help-navigation`도40..45에진입하지않았으므로도움말runtime증거아님. staleRAM script만으로화면/consumer를승격하지않음.
- 재현 `analysis/gutsman_calendar_management_v1/rebuild.ps1 -BuildName <새이름>`; flags와 해시 `build_recipe.json`. cursor검사모델수정후최종current_repro_r2 재빌드/감사 PASS: main/repro/current_r2 동일SHA,666tools drift=[],원본불변 (`final_identity_audit.json`). r1과초기실패도보존.

## 남은 한계

정상 도달하지 못한 scripts3/4/8/30/40..45의15문구는 정적 검증만으로 분리한다. 삭제도 한 날짜의 격리된 테스트 생일에 대한 검사이며 영구 native save/coldreload 검증과 혼동하지 않는다.

휴일正月(6368E8:130:0)·다른행사이름·날짜/요일 그래픽·전체이미지/inline/fixed population 미완료. 임의한글이름 입력/편집→committed record→모든재표시→영구save/fresh process reload→기존save호환, 실제RTC/C40producer, 이전wait-arrow53pixel/TVtransition1pixel·인간 wording/presentation review 미해결.

전체 요청 미완료. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.
