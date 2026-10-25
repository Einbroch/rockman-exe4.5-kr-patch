# 023: B0 진행 힌트500개 ROM 반영·독립 재빌드·정상 경로 검증

## 최종 현재 상태 (2026-10-15, 아래 진행 기록보다 우선)

최신 검증 개발 ROM을 `poc/output/pending500_023_v1.gba`로 갱신한다. SHA256 `6e6d9104db33fd927714b4a06cd6a1093fd4b6ef6d4f77c6ecd206daa44a39ec`, 12,156,368bytes. 원본·고정022 argv·023 source-bound 입력에서 빌드했고, 별도 작업 폴더/전체 재컴파일의 `_repro.gba`와 전체 바이트 동일하다. 실제 신규500-ID delta/기존 누락0, 누적12,622개, primary405/source payload 물리적 미변경327catalogued archive다. B0의21개 source는 별도 보충 추출/clone으로 관리하며327을 미번역 잔여 수로 확대하지 않는다.

현재 기계 판독 권위는 `analysis/pending500_023_v1/batch_status.json`이다. 이전 source-only checkpoint는 역사적 단계 기록이다. 아래8개 보고서를 해시로 묶으며 needs_review/NON-DISTRIBUTION, release_eligible=false, complete_integrated_request=false를 유지한다.

- `integration.json`: 실제500-ID/총12,622·이전435 clone 바이트/문구/소비 계약·이전 입력lineage·전 source/header/ExpectedWrites/전체diff/독립재빌드 PASS. 이전 reader stub12byte를 제외한 ROM prefix0..12,058,156byte가022와 동일하다. 신규 B0 사본/clone/descriptor는 그 뒤의 단일 append 계획으로 배치하고 원래 B0 압축 저장소/23slot/loader는 보존했다. 최종 전체 composed selector를 재생성해 코드/분기/리터럴 배치를 확인했다. 기존 모든 폰트/코드/그래픽/원본 포인터의 불변성은 prefix 비교로 연결했다.
- `b0_cpu.json`: 실제 최종 B0 reader CPU6,341조건. `a3_cpu.json`: 실제 ROM의 기존A3 reader5,652조건. 전체255 script/Navi·바이트 불일치·잘못된scene/caller/root/index 및 이전 reader 조합/ABI/native RAM 보존 PASS. 합성CPU는 GBA 영상/음향 증거가 아니며 원래216byte clear helper를 제한된 계약으로 대체했다.
- `integrity.json`: 유효 제품 수용과 손상 거부15fixture PASS. 원본 저장소/포인터/loader, native 사본/길이, 번역clone/레이아웃/입력identity, descriptor, 새wrapper/단일installer 손상을 확인했다.
- `natural_b0_runtime.json`: 새023 own cold boot→Monday field→일반 L 입력2회. 원래 script0/진행 분기/default10이 자연스럽게 실행돼 `인터넷을 좀 더\n탐색해 보자!`를 표시했다. **loader/scene/script-table/progress/RAM alias 없음**. 두 번의 정확한 Hangul stream/font CPU reads/OBJ VRAM→화면pixels/52,110 원점/keyWait/빈 영역 잔상/원문RAM·재진입 PASS. Mesen wrapper 표본은 각58,236cycles이며 실기·음향/모든 내비 timing 승인으로 확대하지 않는다.
- `exit_runtime.json`: 두 종료의 context 비활성/E5 end 위치/모든128개 OAM 검사에서 대사·커서 palette14 OBJ0개 확인. source RAM은 두 reader 진입 전·대기·닫기 뒤 전체 바이트 보존이다.
- `normal_runtime.json`: 같은023의 정상 부팅/기존 자판3페이지 VRAM·map/네 선택 가능 내비 OAM/첫 I.P.C. 메일23쪽 순서·keyWait·native load·목록 복귀·재열기 PASS. 이 보고서의 전체 cumulative startup/ancestry/source/font/graphics audit도 통과했다. 자판은 기존 일본어 입력이며 자동 한글 입력을 검증한 것이 아니다.
- `visual_review.json`: 직접 본 초기설정19화면/첫메일23쪽/기본힌트2회·종료2회 기록. 힌트 한글은 잘림/겹침 없이 보이고 종료 뒤 필드로 복귀한다. 구매 안내의 빽빽한 행간은022와 text crop RGB hash 동일한 OPEN_INHERITED, 필드 날짜HUD 일본어/기존 kana 자판·호칭/자동 한글 입력 저장은 OPEN이다. 전체500개 의미·표현의 사람 승인이 아니다.

새 BPS/xdelta/ZIP을 만들지 않았으며 source/022/기존ZIP 해시를 최종 상태에서 다시 확인했다. 사용자 세이브·이전ROM·실패 조사 폴더를 편집/삭제하지 않았다. GUI 테스트는 새 ROM의 새 게임/own checkpoint와 분리된 testRunner를 사용했다.

### 다음 작업

1. 새 모집단은 실제023의 ID 집합에서 산출한다. 이 B021개에서 아직 일본어인 literal ID 목록은 `batch_status.json`의 `remaining_Japanese_units_in_this_B0_table`에 있다. 후보529/선정500/원문574를 전체 게임 잔여 수로 쓰지 않는다. script27은 A3와 전체문맥이 달라 재사용에서 제외했으므로 원문과 실제B0맥락을 보고 번역/보완한다.
2. 다른 진행 플래그 분기/21개 내비 provider, 닉네임99px·칩104이름88px 삽입 페이지의 실제 경계 표본과 기존 A3 자연 이벤트를 보완한다. 현재500개는 source-bound 합성 길이가 통과했지만 기본 힌트 외 모든 페이지의 실행·사람 승인까지 끝난 것은 아니다. B0 printChip104는 이전 Roll/Guts의 두 exact-stream 한글 이름 selector에 해당하지 않아 native 이름이 남으며, 최종 clone 영역과 기존 gate 두 주소의 비중복을 검사했다.
3. 사용자의 자동 한글 조합→확정→저장→불러오기/재표시, 구매안내 행간, 날짜HUD/다른UI·이미지 미번역 등은 남았다. 현재 검증 ROM을 유지하며 다음500개 또는 별도 경계 작업으로 이어간다. 새 패키지는 사용자 재요청 전 만들지 않는다.

### 조사/검증 도구의 실패와 교정 (게임 실패와 구분)

처음 native guard CPU fixture는 BIOS SWI 구현 없이 실행해 멈췄다. source의 실제 clear 호출/리터럴을 확인하고 두 원래EWRAM 버퍼0x02012F50/0x02013E50의0xF00 zero-fill만 대체했다. 변수 경로의 무조건 원본 바이트 불변 가정은 기존0x5162C 칩이름 hook 때문에 거부됐고, 기존 exact-stream selector 전체 재생성/기본 fallback/원래 이름·width 공급을 연결해 처리했다. 종료 검증의 첫 E5/F1 혼동은 고정TextPet에서 end=E5/clearMsg=F1을 대조해 검사 도구만 바로잡았다. 이 교정 때문에 ROM을 임시변경하거나 runtime을 조작하지 않았다. 기존 compile v1/v2 경로/파일명 실패 폴더도 보존한다.

## 이하: 후속 통합 빌드 진행 기록 (완료 전 기록, 현재 상태 아님)

분기/합성 길이 미해결을 보완했다. `pending_insertion_500_023_guard_v1/native_guard_cpu.json`의 native 분기/provider 실행3,000조건 PASS(원래 clear 호출까지 실행, BIOS CpuFastSet만 두 원래EWRAM0xF00 clear 계약으로 대체). `pending_insertion_500_023_capacity_v2/survey.json`은500개 전부 합성 길이 후보 PASS(닉네임99px/원래칩104이름88px), `field_hint_capacity.py` 신규 fixture22개와 기존 full-box/줄배치16개 PASS다. 이전 65/75개 미해결 분류는 당시 단계 기록이며, 현재 용량 모델에서는500개 모두 통과했다. 기본창 검사를 전역 완화하지 않고 B0 source/scene/table/명령 계약을 별도 바인딩했다.

`pending_insertion_500_023_reader_v1/cpu.json`: B0 reader→기존A3/이전 reader 조합의 CPU-memory fixture6,269조건 PASS. 제품 ROM이나 GBA 화면 증거는 아니다. `pending_insertion_500_023_product_preflight_v2/preflight.json`: primary `compile_archive`로500개 전체 source/줄배치/합성/보호 제어/원문·번역 바이트 왕복/비선정script 보존 PASS. v1·capacity v1/v2 등 과거 보고서는 당시 코드 해시의 역사적 증거이며 현재 primary 검증은 새 source-bound gate를 다시 실행한다.

primary `build_development_patch.py --field-b0-hints-023`에21개 B0 clone/전체native비교 사본/23슬롯 descriptor/단일 composed reader 설치를 등록했다. 기존 압축 데이터/loader/포인터는 유지한다. `build_field_b0_023.py`와 `--repro`가 원본과 고정022 argv에서 별도 전체 빌드를 실행 중이다. 예정 산출물은 `poc/output/pending500_023_v1.gba` 및 `_repro.gba`, 작업 폴더는 `poc/work/pending500_023_v1` 및 `_repro`다. **이 진행 중 기록 작성 시 새 ROM 완성/검증을 아직 주장하지 않으며 최신 검증 ROM은022/12,122개다.**

빌드 완료 후 순서: `verify_field_b0_product_023.py --repro poc/output/pending500_023_v1_repro.gba` → `bench_hint_rom_reader.py --rom ... --field-b0 --out analysis/pending500_023_v1/b0_cpu.json` 및 옵션 없는 A3검사 → `verify_field_b0_integrity_023.py` → `run_field_b0_runtime_023.py` → `verify_field_b0_runtime_023.py`와 `verify_first_mail_runtime.py --rom ... --prefix pending500-023-v1 --out analysis/pending500_023_v1/normal_runtime.json` → 화면 직접검토/권위 상태 갱신. 새 B0 화면 검사는 정상 초기 Monday field/L 입력의 observer-only이며 loader/scene/table/flag alias가 없다. 다른 내비/진행 분기/변수 페이지 전수나 자동 한글 저장 완료로 확대하지 않는다. 배포 패키지는 만들지 않는다.

## 이전 source-only 상태 (2026-10-15, 현재 상태 아님)

이번023은 **원문 추출/번역 연결/기계 컴파일 단계**다. 새 ROM을 만들거나500개를 추가 반영한 상태가 아니다. 검증된 최신 개발 ROM은 `poc/output/pending500_022_v2.gba`, SHA256 `7363567b1263dac0700e2430da1046e47aa9ba65c8d9c2125b1ab9b3bd2928a1`, 누적12,122개 그대로다. 사용자 지시에 따라 새 BPS/xdelta/ZIP은 만들지 않았다. 원본·020/021/022·기존ZIP 해시 보존은 `pending_insertion_500_023_b0_reuse_v1/checkpoint.json`에 기록했다. 사용자 세이브는 편집하지 않았다.

현재023 기계 판독 권위는 위 `checkpoint.json`이며, 500개 컴파일 보고서와 작성 도구들의 해시를 묶는다. source-only/mechanical PASS를 ROM 반영/실행/배포 PASS로 확대하지 않는다. needs_review/NON-DISTRIBUTION, insertion_ready=false, release_eligible=false다.

## 추출 모집단과 문구 출처

022 실제 ID 집합을 기준으로 기존 고정 draft를 다시 조사했다. 엄격한132px/raw 계약 후보는1개로 exact500을 만들 수 없었다 (`pending_insertion_500_023_survey_v1/survey.json`). 이는 게임 전체 잔여 미번역 수가 아니다.

022의 정상 초기 필드(B0/Navi0)에서 읽는0x78BF28 힌트는 기존 TPI에 정확한 항목이 없었다. 원본 loader/scene selector와 B0/B1 테이블 경계를 확인했다. scene-root0x53FA0의 B0 슬롯0x54060→0x08054238, 다음B1 슬롯0x54064→0x08054294 사이에는23개의u32LE 내비 슬롯이 있다. null13/14를 제외한21개 archive에서574개 literal 단위를 추출했다. 전부 첫 offset510/255-script 표이며 원문 binary→TPL→binary 전체 바이트 동일 PASS, 원본 압축 범위/기존022의 원본 저장소도 보존 PASS다. 새 공급원은 별도 추출 증거로 보관하며 제3자 TPI를 수정하지 않았다.

`field_b0_hints_v1/extraction.json`은 이23슬롯 모집단에만 완전하다. Navi0는 기존022 정상 runtime 표본에 연결되지만 나머지20개는 동일한 정적 loader/index 규칙을 따르는 것으로만 확인했으며 개별 실행 검증은 아니다. 또 다른 관측 source0x7B65EC는 decoded510bytes가 catalog0x7A6B84와 동일한 alias였고 신규 번역 수에 넣지 않았다.

같은 내비의 A3 테이블0x54180 donor와 대조했다. 같은 script/literal 역할뿐 아니라 **해당 script 전체 제어/인자/초상화와 모든 literal의 순서·언어·원문**이 동일할 때만 고정 기존 번역 문구를 연결했다. source-only/fuzzy matching은 쓰지 않았다. script27은 전체 문맥이 달라21개 모두 제외했다. 일본어가 있는 문구529개가 연결 후보이며 그중 complete-script 그룹으로 exact500개를 선택했다. 전부 실제022 적용ID와 중복0이다.

`pending_insertion_500_023_b0_reuse_v1/selection.json`은 권위 문구의 경로/해시/기존unit ID를 가진다. `pending_insertion_500_023_b0_inputs_v1/*_draft_ko.json`은 읽기 전용 파생 투영이다. 새 번역으로 중복 작성하거나 승인 승격하지 않았고 기존 needs_review 문구·줄바꿈을 그대로 유지했다. 수정 시 donor의 권위 문구를 기준으로 새 버전의 입력/검증을 생성한다.

## exact500 기계 검증과 아직 열린 경계

`pending_insertion_500_023_b0_compile_v3/verification.json`:

- 21개 archive/500개 원문 ID, source/parent/selection 해시 고정.
- 번역 TPL→binary→TPL→binary 전체 바이트 동일. 재추출된 전체 literal stream/언어/ID/문구와 모든 보호 제어 일치.
- 비선정 script의 바이트 전체 보존. 기존 원본 압축 데이터는 변경하지 않음.
- 사용 한글/확장 문자250종에 대해 실제022 normal-font의96byte glyph와12px advance가 고정 BDF/encoding 공급과 일치.
- 원문보다 커진 새 binary는 조사 산출물일 뿐 native RAM에 덮어쓰거나 clone reader에 등록하지 않음.

선정500개의 기술 분류는360개가 현재 full-box 배치 후보 검사를 통과했고,65개는 분기/entry 계약이 미해결이며,75개는 이름/칩 이름 print와의 합성 길이 모델이 더 필요하다. 분류는 우선순위가 있어 entry 조건도 겹치는 print 문구가 있을 수 있다. 360개도 후보 줄 배치를 실제 컴파일에 적용하거나 최종 ROM/화면을 검증한 것이 아니다. 현재500 기계 컴파일은 권위 문구의 기존 LF 그대로다.

주요 entry 미해결 명령은 `checkTournament`, `checkNetDateWeekday`다. TextPet가 해석하고 source script가 보존된다는 이유만으로 full-box 허용 목록을 넓히지 않았다. 분기 대상에서 필요한 창/렌더 상태, 변수 삽입의 prefix·이름·suffix 전체 행 폭, 원문 RAM 수명과 새 reader 선택 경계를 확인해야 한다.

컴파일 검증 도구의 v1은 경로 구분자 표기 비교, v2는 TextPet output basename에서 archive 이름을 만들면서 생긴 `translated` ID 때문에 중단됐다. v3에서 정규화된 경로 비교/원 archive명 binary basename으로 수정해 모두 통과했다. 두 실패 폴더를 보존했으며 어느 단계에서도 ROM은 쓰지 않았다.

## 다음 실행 순서

1. B0 정상 loader/23slot/Navi/source 전체바이트 계약에서 새 ROM clone 소비를 등록할 방법을 검증한다. 기존 A3 selector/carry/원본 fallback과 조합되는지, native RAM extent와 소비 수명이 유지되는지 확인한다. 미확정 pointer를 직접 덮어쓰지 않는다.
2. 위 분기 guard와 변수 print 페이지를 정확한 source ID별 계약으로 검증하고 exact500 전체 capacity를 통과시킨다. 기존 parser 검사 완화나 문구 자동 축약으로500개 수를 맞추지 않는다. 필요 시 별도 version 선택안을 만들어 이전 증거를 보존한다.
3. immutable 원본에서 새 개발 ROM을 만들고 이전12,122개 보존/실제신규500-ID/ExpectedWrites/전체diff/ISA/ancestry/source integrity/독립 재빌드를 확인한다. 그 전에는 적용 누적 수를 늘리지 않는다.
4. 새 ROM의 own cold boot와 정상 초기B0 경로로 script0→10 분기/힌트 표시/폰트CPU→OBJ→pixels/keyWait/닫기·재진입/원본RAM 보존을 확인한다. 이전022 진단 alias나 state를 자연 실행 증거로 사용하지 않는다.
5. 자동 한글 조합→확정→저장→불러오기/재표시, 기존 구매안내 행간, 일본어 자판/닉네임 suffix, 필드 날짜HUD는 기존 미완료 항목이다. 이번 source 조사로 해결했다고 보고하지 않는다. 새 패키지는 사용자 재요청 전 만들지 않는다.
