# 묶음003 — 실제500개 누적 ROM 반영

정책: development-draft; NON-DISTRIBUTION. 별도 패치 파일 생성은 사용자 재요청 전까지 하지 않는다. 이번 작업은 create-kr-patch의 기존 프로젝트 재삽입/후킹/빌드 검증 경로를 사용했다. 신규 문구 작성이나 gt-text-translate 입력 계약 이주 작업은 아니다.

## 현재 결과

- ROM `poc/output/exe45_ko_development_pending500_003_v2.gba`
- 독립 재빌드 `poc/output/exe45_ko_development_pending500_003_v2_repro.gba`, 전체 바이트 동일
- SHA256 `2cddc59ca723ce789c7e935a09ab1742c5a347df41583224fb07c78394c26f04`
- 누적3,837→4,337개; 주82→125아카이브, catalog 미변경607개
- 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 보존
- 이전002 ROM과 모든 기존 주/별도 컴파일 페이로드 보존
- 기존 배포 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 보존, 새 BPS/xdelta/ZIP 없음

## 실제500개 구성 및 이월 정산

장비 normal39개(거츠맨2/파이어맨5/블루스7 각13), 스타맨 관련6개, 기존 미적용 raw 대사455개다. 원본의 문구 단위 ID를 그대로 추적하며 재삽입됐다. 단어·순서·숫자와 원래 이벤트 명령은 보존했다.

이전 이월160개 중111개는 원래부터 공통 장비 이름 복제본의 한국어를 소비하는 내비별 source-ID 별칭이었다. 원문/번역/소비 대응을 각각 검증했으며 이111개는 신규 적용량에 포함하지 않는다. 따라서160=이미 표시되는111별칭+이번45개+미해결4개다.

미해결4: `6E1554:0:0`, `6E1CC0:0:0`, `6E21B0:0:0`의 소비 경로 미확정; `6A5578:10:0`은 동적 닉네임과 합산 레이아웃 검증이 필요하다. 이4개만 전체 미번역 잔여라고 주장하지 않는다.

선정/별칭 정산 `pending_insertion_500_003_selection_v1/selection.json`; 준비 검사 `pending_insertion_500_003_preflight_v3/preflight.json`. 입력 초안 파일은 변경하지 않았다.

## 장비 소비 계약

3개 원본 압축 장비 pool은 기존 ROM/BIOS→RAM0202BA7C 흐름과 포인터를 보존한다. normal scripts60..62/70..75만 ROM clone으로 읽는다. `equipment_rom_selector.py`가 root0202BA7C, caller0804F7BD, script 범위, Navi index2/5/7, 원본 table의 앞16/뒤16바이트를 모두 검사한다. 실패하면 이전 누적 선택기로 전달한다. RAM 확대나 저장 구조 변경 없음.

장비 buffer1의 실제 생산자는0803EFAA `ldrh r3,[r5,#0x1c]`,0803EFAC `str r3,[r6,#0x4c]`, 원본4바이트 `ab8bf364`다. uint16 값의 최대5자리55px를 사용한다. 설계상 폴더 수30 등을 임의 상한으로 사용하지 않는다.

파이어맨/블루스 `70:1`의 한 줄 suffix를 명시적 LF로 나누었다. 단어/순서/숫자는 동일, 대기/clear 추가0개다. 숫자 포함 둘째 줄 최대79px, 셋째 줄 파이어맨/블루스48px, 거츠맨59px로 허용152/132px 이내다. `translations/pending_insertion_500_003_pages.json` 및 컴파일 기록 `equipment_aggregate_proof` 참조.

## 검증 근거

- `pending_insertion_500_003_rom/integration_v1.json`: 전체 source-ID union에서 정확히500개 추가, 기존 누락0, 이전 모든 페이로드/포인터 계약/독립 재빌드 검증 PASS
- `selector_cpu_v1.json`:3,195조건 PASS, 장비3종×76script×23Navi, table guard 변조/잘못된 root·caller·index/범위와 이전 메일·keyitem 경로. 합성 CPU 벤치이며 실제 플레이로 주장하지 않는다.
- `startup_audit_v1.json`: 최종 누적 변경 범위/기존 초기 설정·자판·타이틀 보존 감사 PASS
- `normal_runtime_v1.json`: 새 ROM 자체 냉부팅→정상 버튼 초기 설정→기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23대기 경계/목록 복귀/재열기 PASS
- `first_mail_pages_v1.png`: 첫23페이지 모음, 실제 화면을 직접 확인
- `guts_runtime_v1.json`, `guts_guides_v1.png`: 같은 ROM의 정상 내비 선택 거츠맨2→장비 guide60/61/62/나가기/재열기. 원래 RAM payload 보존, 실제 native table lookup clone root/offset, caller·return ABI, 한국어 stream/글꼴 CPU 읽기, OBJ VRAM 및 화면 픽셀 대응 PASS. 직접 화면 확인
- `python -X utf8 tools/test_pending500_002_pages.py`: 기존 명시적 페이지 회귀5tests PASS

정상 runtime 증거는 `poc/runtime/pending500-003-v2-*`에 있다. 거츠맨 첫 `guts-equipment` 증거에는 lookup observer가 없으므로 최종 검증은 `guts-equipment-r2`를 사용한다. 첫 실패 build003_v1, 이전 preflight v1/v2 및 모든 옛 증거는 삭제하지 않았다.

## 재현 명령

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_003_v2_repro --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003
python -X utf8 tools/verify_pending500_003_rom.py --rom poc/output/exe45_ko_development_pending500_003_v2.gba --repro poc/output/exe45_ko_development_pending500_003_v2_repro.gba --cpu analysis/pending_insertion_500_003_rom/selector_cpu_v1.json --out analysis/pending_insertion_500_003_rom/integration_fresh.json
```

새 재현에는 새 이름/출력 경로를 사용한다. 기존 ROM 및 증거를 덮어쓰지 않는다. 런타임 재현도 prefix/폴더를 새로 지정해야 한다.

## 다음 작업과 한계

1. 거츠맨 오류70..75와 파이어맨/블루스 장비 normal39개의 남은 실제 화면 경로를 검증한다. CPU 조건 통과만으로 자연 획득/장비 상태를 검증했다고 쓰지 않는다.
2. 다음 미적용500개를 선정할 때 현재125개 주 등록과 모든 별도 clone의 original-ID를 합집합으로 제외한다. 이번111별칭도 중복 신규 번역으로 세지 않는다.
3. 새500개를 원본 기반 누적 ROM에 적용하고 동일 재현/이전 번역 보존/레이아웃/소비경로 검사를 수행한다.
4. 위 미해결4개는 소비 계약과 닉네임 합산 폭을 증명한 뒤 별도 반영한다.

전체500개 자연 진행·임무·보상·저장 QA, 실제 하드웨어/음성 검증, 최종 문구·미감 승인 미완료다. 한글 자동 조합/저장 ABI는 여전히 누적 ROM에 통합되지 않았다. 개발 ROM 생성과 전체 한글화/배포 승인을 혼동하지 않는다.
