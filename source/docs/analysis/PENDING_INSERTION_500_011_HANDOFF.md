# 이전 기록011: 현재 권위는 PENDING_INSERTION_500_012_HANDOFF.md

아래011 artifact/검증은 보존된 이전 기록이다. 최신 ROM 및 다음 재개점은 `analysis/PENDING_INSERTION_500_012_HANDOFF.md`를 사용한다.

## 011: 다음500개 실제 반영 —40 carry·21 new archives

현재 ROM `poc/output/exe45_ko_development_pending500_011_v1.gba`, SHA256 `c9a23d3cf303921cfaf33b8f053621c6a16cbe180e3723076a87a5721d084f86`. 독립 `_repro.gba` 전체 바이트 동일. 누적8,337개/주311아카이브/원본 미변경421아카이브, actual 신규500-ID·기존ID 누락0. 개발용 `NON-DISTRIBUTION`; 새 BPS/xdelta/ZIP 없음.

## 입력과 단일 제품 빌드

010 actual ROM/hash/metadata로 primary와 supplemental 적용ID를 재계산했다. 기존 source-bound 번역 초안500개를 추가 반영했으며 새 문구 작성0개다. 원문·기존 번역·숫자·명령·줄 수·review state를 임의 변경하지 않았다. 이번 문구도 `needs_review`이며 인간 승인이나 전체 번역 품질 완료를 뜻하지 않는다.

권위 source-only selection `analysis/pending_insertion_500_011_partial_selection_v2/selection.json`, source-only preflight `analysis/pending_insertion_500_011_partial_preflight_v2/preflight.json`. 이 payload는 기존 번역이 빠져 직접 삽입할 수 없다. 누적 권위 `analysis/pending_insertion_500_011_cumulative_v1/preflight.json`은61개 최종 입력·compiled hash·parent/source ID·표시 scope를 고정한다.

기존40개는010 parent asset/scope를 다시 컴파일해 actual010 payload와 같음을 확인한 다음 신규 scripts를 합쳤다. 기존 per-literal normal/big/mono 소비 경로와 metrics, 선택지·dynamic 모델을 보존했다. 새21개는 parent=null이며 기존 registry/primary/supplemental에서 absent이고 immutable 원본 payload를 기준으로 검증했다. 신규 scripts에만 normal/mmbn45/3행132px profile을 적용했다.

새21개:6BC2F8,6BC74C,6BCCD0,6C1B84,6C231C,6C2660,6C5F28,6C7608,6C79E8,6C7D04,6CB6C0,6CD068,6CD48C,6D1068,6D26A0,6D2700,6D27A0,6D2B34,6D3050,6D5EB0,704368.

`tools/cumulative_batch500.py` PROFILE011은 exact010 base/hash, source preflight v2,61개·명시적21개 new inventory, prior007/008/009/010을 고정한다. `tools/cumulative_batch500_011.py`는 기존 병합 구현 adapter다. `build_keyitem_full_rom.py`→`build_roll_pet.py`→`build_development_patch.py`의 `--pending-batch500-011`은010 prerequisite를 요구한다. 기존40 writer를 누적 writer로 교체하고 새21 writer를 추가한 뒤 원본에서 Expected Writes를 계산한다. 이전 ROM 위에 순차 패치하지 않는다. first-mail Expected Write 목록에도 신규21개의 실제 source pointer write를 포함했다. 검사를 우회하거나 허용 범위를 통째로 넓히지 않았다.

## 보존한 미적용 v1 / 별도 표시 경로

처음 source-only v1 선정은70904C:10:0을 포함했고 자체 preflight는 통과했으나, cumulative derive에서70904C의 별도 startup scope가 일반 registry에 없으므로 KeyError로 중단했다. 이 scope는 별도 proportional UI 경로를 갖는다. generic normal profile을 강제로 추가하거나 기존 startup 표시 경로를 덮어쓰지 않았다. 이 시도에서는 ROM이 생성되지 않았다.

v1 selection/preflight와 관찰은 보존하며 제품 입력이 아니다. selector의 선택적 `EXTRA_EXCLUDE`를 통해 이번 cohort만70904C를 제외하고 v2에서 다른 문구로500개를 채웠다. 기존 호출의 기본 제외 목록은 바뀌지 않는다. 해당1문구는 별도 소비 경로·초기 UI 문맥을 검증한 후 작업할 항목이다.

## 검증 — 같은011 artifact

- `analysis/pending500_011_v1/integration.json`: 신규500-ID/기존누락0/8,337개, 기존40개 모든 비신규 script 바이트·metrics 보존, 비중첩 이전261페이로드/metadata 동일, 새21개의 unselected source scripts·native 저장 영역·payload hash·actual pointer bytes PASS. 원본/헤더/전체 write/ISA 배치 감사와 독립 재빌드 전체 바이트 동일 PASS. 이전 ancestry도 해당 exact artifact별로 검증했다.
- `selector_cpu.json`: composed mail/keyitem/gear 선택기3,195조건 PASS. 합성 CPU 검사이며 실제 플레이 증거가 아니다.
- `rejection_controls.json`: 유효 artifact accept 및 declared count누락/기존ID누락/기존metrics변조/retained script변조4조건 reject PASS.
- `new_archive_controls.json`: 유효 artifact accept 및 새 payload변조/ID누락/pointer metadata변조/actual pointer bytes변조/native source storage변조5조건 reject PASS.9조건 모두 메모리 내 negative controls, 파일 수정 없음.
- codec6tests 및 관련 Python syntax PASS.
- `normal_runtime.json`: same011 cold boot→초기 설정·기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23쪽/native RAM body/list return/reentry PASS. Mesen의 실제 런타임이며 다른 에뮬레이터·실기 전체 호환성 주장이 아니다. `first_mail_pages_v1.png`23쪽 직접 시각 검사.
- `display_runtime.json`: 새6C5F28:1:0 아이스맨 칩 요청, 새6D1068:3:0 플랜트맨 무승부 문구, carry6B69A0:22:0 전투 안내,3리터럴. actual glyph CPU reads→OBJ VRAM/화면 픽셀, native root/origin/keyWait, 빈 영역 검사 PASS. `changed_pages.png`3화면 직접 시각 검사.

표시 진단은 같은 ROM에서 정상 입력으로 NumberMan8 상태를 만든 뒤 PET pointer/table read만 alias한다. ROM/RAM 직접 쓰기 없음, native position/msgOpen/keyWait 실행, diagnostic checkpoint 격리. 화면의 NumberMan portrait는 진단 시작 문맥이며 실제 화자·배틀 결과·자연 이벤트·보상·저장 증거가 아니다. aliases는 ROM에 설치하지 않아 원래 내비 lookup/대사 연결이 유지된다. `run_cumulative500_011_displays.py`는 own-ROM pagecycle checkpoint와 검증된 버튼 입력만 사용한다.

## 재현

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_011_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005 --pending-batch500-006 --pending-batch500-007 --pending-batch500-008 --pending-batch500-009 --pending-batch500-010 --pending-batch500-011
```

## 다음 재개 / 미완료

다음 적용ID 기준은011 ROM/hash/metadata다. v2 selector의 당시 좁은 raw/no-print/encoding/geometry 허용 범위는768개 중500개를 선택했다. 같은 범위의 잔여268개와 별도 보류70904C:10:0은 전체 일본어 잔여 수가 아니다. 이 범위만으로 다음500개가 된다고 가정하지 말고 남은 소비 경로·scope를 조사하거나 남은 크기의 묶음을 명시한다. 기존500개를 다시 세거나 print/동적 삽입 검사를 무시해500개를 채우지 않는다.

010의 keyWait 없는6989B0 script2 waitHold 진단은 미검증 그대로다. 이전 실패 관찰을 pass로 바꾸지 않았으며 source 명령/ROM을 수정하지 않았다. proper native battle-result caller에서 확인해야 한다. 전체500개 자연 scene/선택 결과/보상/저장, 번역 의미·말투 검수, 가운데점 보류19문구, 별도 dynamic nickname4개(6E1554:0:0,6E1CC0:0:0,6E21B0:0:0,6A5578:10:0), gear 일부 실화면, 한글 자동 조합·commit/save/redisplay ABI 통합은 남았다. 현재 자판은 일본어 배열+한글 동작 라벨이며 완성 한글 입력 자판이 아니다.

원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 이전010 SHA256 `8f05118a2dd8a7e452e81f81413b1c580fe9883493aae1e0d85c3d496075663a`, 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`. 원본·기존 ROM/증거/패키지를 보존했고 사용자가 다시 요청하기 전까지 배포 패치를 만들지 않는다.
