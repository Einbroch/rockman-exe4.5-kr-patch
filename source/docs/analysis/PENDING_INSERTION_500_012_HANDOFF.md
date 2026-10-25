# 이전 기록012: 현재 권위는 PENDING_INSERTION_500_013_HANDOFF.md

아래012 artifact/검증은 보존된 이전 기록이다. 최신 ROM과 다음 재개점은 `analysis/PENDING_INSERTION_500_013_HANDOFF.md`를 사용한다.

## 012: 일반 raw 잔여268개 실제 반영

현재 ROM `poc/output/exe45_ko_development_pending500_012_v1.gba`, SHA256 `c64f3f8d00079a6f77c87b0fd97035ab018959fcc7412c785dcc563e5e97dc90`. 독립 `_repro.gba` 전체 바이트 동일. 빌드의 누적 소비 단위8,605개/주319아카이브/원본 미변경413아카이브. actual 신규268 source-ID·기존ID 누락0. 개발용 `NON-DISTRIBUTION`; 새 배포 패치 없음.

## 입력·분모·누적 경로

사용자500개 묶음 지시의 후속 잔여 작업이다.011 ROM/hash/metadata로 적용ID를 다시 계산한 결과, 기존 raw/no-print/encoding/3행132px 조건과 명시적 제외 목록의 전체 잔여는268개였다. 검증되지 않은 소비 경로를 섞어500개를 만들지 않고268개 잔여 묶음으로 작업한다고 commentary에 알렸다. 새 문구 작성0개이며 기존 source-bound `needs_review` 번역 초안을 반영했다. 원문·숫자·제어 명령·줄 수·기존 문구와 review state를 보존했다.

권위 source-only input: `analysis/pending_insertion_500_012_partial_selection_v1/selection.json`, `analysis/pending_insertion_500_012_partial_preflight_v1/preflight.json`. 총268개·unique268·기존 적용ID 교집합0·geometry candidate0. selection의 legacy `reason` 문장에는500이라는 이전 고정 라벨이 남았지만, 실제 selection의 replacement/total 숫자와268-ID 집합·preflight가 분모다. 이 라벨 수정 시도는 frozen hash 차이가 확인되어 원래 바이트로 복원했다. 기존 선택 입력과 preflight hash는 일치한다. 생산자의 reason은 TARGET 기반으로 수정해 다음 생성부터 정확하게 기록한다. 이 source-only payload는 기존 번역을 담지 않아 직접 삽입하지 않는다.

권위 누적 input: `analysis/pending_insertion_500_012_cumulative_v1/preflight.json`. 기존40개 parent를 원래 소비 scope로 다시 컴파일해 actual011 바이트와 같음을 확인한 다음 신규 script를 합쳤다. 새8개는 registry/기존 primary·supplemental 적용에서 absent인 source-only input으로 등록했다. 새8개:768800,768BD0,7B67C8,7C0970,7C0F8C,7C5CE0,7C714C,7CC6A0. 기존 normal/big/mono literal profile, 동적 모델·metrics·선택지 제어를 덮어쓰지 않았다.

`cumulative_batch500.py` PROFILE012는 exact011 base/hash,source preflight,48개·명시적8개 new inventory,prior007..011 및 **units=268**을 고정한다. 일반 함수의 unit_count는 명시적1..500 정수만 허용하고, 이전 profile은 기본500 그대로다. source preflight·누적 preflight·최종 delta·manifest 증가 모두 같은 profile 분모와 비교한다. 기본500 검사를 제거하거나 임의 actual count에 맞추지 않았다. 고정 fixture3tests(legacy default,explicit boundaries,invalid types/ranges) PASS.

주 제품 경로 `build_keyitem_full_rom.py`→`build_roll_pet.py`→`build_development_patch.py`에 `--pending-batch500-012`를 추가했고011 prerequisite를 요구한다. carry40 writer 교체와 new8 writer 추가 후 원본에서 Expected Writes를 계산한다. first-mail Expected Write 목록에8개 신규 source pointer write도 추가했다. 이전 ROM을 입력으로 순차 패치하지 않는다. standalone BPS/xdelta/ZIP 생성 없음.

## 같은012 ROM 검증

- `analysis/pending500_012_v1/integration.json`: actual268-ID delta/기존누락0, carry40의 모든 비신규 script·기존 metrics 보존, 비중첩 이전282페이로드 및 소비 metadata 동일, new8의 native 저장 영역·미선택 source scripts·payload hash·actual pointer bytes PASS. 원본/헤더/전체 write/ISA 배치 감사, exact artifact별 ancestry, 독립 재빌드 전체 바이트 동일 PASS.
- `selector_cpu.json`: composed mail/keyitem/gear 선택기 합성CPU3,195조건 PASS. 실제 플레이 증거는 아니다.
- `rejection_controls.json`: 유효 artifact accept와 declared count/기존ID/기존metrics/retained script 결함4조건 reject PASS.
- `new_archive_controls.json`: 새 payload/ID/pointer metadata/actual pointer bytes/native source storage 결함5조건 reject PASS.9조건 모두 메모리 내 변조이며 디스크 파일은 변경하지 않았다.
- codec6tests, denominator3tests, 관련 Python syntax PASS.
- `normal_runtime.json`: same012 cold boot·초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 I.P.C. 메일23 ordered keyWait/native RAM load·list return·reentry PASS. `first_mail_pages_v1.png`23쪽 직접 시각 검사.
- `display_runtime.json`: new7B67C8:17:0 설정 안내, new7C714C:0:0 섀도맨 실패 문구, carry776198:17:0 나이트맨 HP 문구,3리터럴. 실제 glyph CPU reads→OBJ VRAM/화면 픽셀·native root/origin/keyWait·빈 영역 검사 PASS. `changed_pages.png`3화면 직접 시각 검사.

표시 진단은 own-ROM 정상 Rockman0 checkpoint에서 native PET pointer/table read만 alias한다. default initializer의 context reset·source mugshot/msgOpen 경로를 그대로 실행하며 직접 ROM/RAM 쓰기 없음. 별도 diagnostic checkpoint로 격리한다. 이는 원래 화자의 자연 이벤트 연결, 설정 편집 시작, 실제 의뢰 실패, 최대HP 보상·저장 증거가 아니다. knight의 native flagSet은 명령대로 실행되지만 보상 결과를 주장하지 않는다. aliases는 ROM에 설치되지 않아 원래 내비 lookup/대사 연결이 유지된다. Mesen의 관찰이며 실기/다른 에뮬레이터 전체 호환성 주장은 아니다.

## 남은 목록 재대조와 잘못된 분모의 거부

`analysis/pending_insertion_after012_raw_probe_v1/selection_failure.json`: exact012 기준에서 같은 좁은 selector·제외 목록으로1개조차 선택 가능한지 조사한 결과 eligible0이다. 이는 해당 삽입 조건 소진이며 전체 일본어0이나 번역 완료가 아니다. 필터·원문·ROM을 바꾸지 않았다.

오래된 `inventory_full_scope.py`는 authored graphics가 포함된 현재 manifest에서 schema KeyError로 중단했다. 오류를 무시하거나 임의 schema를 삽입하지 않았고 완료 보고를 만들지 않았다. 후속 read-only `inventory_compiled_catalog.py`는 authored graphics를 dialogue asset으로 파싱하지 않고 compiled metadata와 채택된732 archive 추출을 대조한다.

처음 대조에서 `manifest translated_units == distinct placed-clone IDs`라는 가정이 거부됐다. 빌드 코드의 누적 수는 chip-name 재사용·별도 provider·header 등 소비 단위도 더하므로 단일 source-ID 분모가 아니다. 이 survey 가정을 고쳤으며 ROM/제품 빌드/기존 검증은 변경하지 않았다. `catalog_reconciliation.json`은 원본/catalog/TPL/native payload hashes와31,907개 canonical literal identity·현재 compiled payload hash를 검사한다.8,177개는 직접 rom_offset을 갖는 clone source IDs,81개는 별도 placement record를 가진 compiled IDs로 총8,258개 distinct compiled-record IDs다. 빌드의8,605 소비 단위와 분모가 다르다.

21,790개 Japanese IDs가 이 compiled-record 집합에 없지만 **실제 미번역 수로 사용하지 않는다**. chip-name 등 다른 provider의 자체 metadata adapter, shared/dormant/debug/미확정 문맥과 그래픽·inline text·입력 경로가 남아 있다.1,859개 non-Japanese도 임의 제외하지 않았다. 다음 목록 정리는 이 경계와 실제 소비 경로를 대조해야 하며, 단순 부재를 미번역·미적용·비텍스트로 확정하지 않는다. 조사 도구는 주 제품 빌드에 넣지 않았다.

## 재현

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_012_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005 --pending-batch500-006 --pending-batch500-007 --pending-batch500-008 --pending-batch500-009 --pending-batch500-010 --pending-batch500-011 --pending-batch500-012
```

## 다음 재개 / 미완료

다음 실제 적용 기준은012 ROM/hash/metadata다. 같은 raw/no-print 조건으로500개가 있다고 가정하지 않는다. 별도 startup70904C:10:0, compressed/fixed/UI/print·dynamic insertion 소비 경로, 이미 일부 번역된 script의 잔여 literal 등은 조건별 검증 후 범위를 정해야 한다. 자연 문맥·뜻·말투 검수와전체 진행/선택 결과/보상/저장은 여전히 미완료다.

010의6989B0 script2 keyWait 없는 waitHold 표시 진단도 미검증 그대로다. proper native battle caller에서 검증해야 한다. 가운데점 보류19문구, 별도 dynamic nickname4개, gear 일부 실화면, **한글 자동 조합·commit/save/redisplay ABI 통합**도 남았다. 현재 자판은 일본어 배열+한글 동작 라벨이며 완성 한글 입력 자판이 아니다. glyph 공급·표시 진단을 입력/저장/전체 QA 완료로 확대하지 않는다.

원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 이전011 SHA256 `c9a23d3cf303921cfaf33b8f053621c6a16cbe180e3723076a87a5721d084f86`, 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`. 원본·기존 ROM/증거/패키지 보존. 사용자 요청 전 배포 패치를 만들지 않는다.
