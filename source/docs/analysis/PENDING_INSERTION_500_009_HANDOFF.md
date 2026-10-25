# 009: 다음500개 누적 병합·ROM 실제 반영

이 문서는009 단계의 이전 상태 기록이다. 이후010에서 신규500개를 추가 반영했다. 현재 ROM/재개점 authority는 `analysis/PENDING_INSERTION_500_010_HANDOFF.md`; 아래 현재/다음 서술은009 당시 기준이다.

현재 ROM `poc/output/exe45_ko_development_pending500_009_v1.gba`, SHA256 `0b623c19d8cbc944b555b26c2571c52d110e076af5fdb5aa0bedf52c0ac54096`. 독립 `_repro.gba` 전체 바이트 동일. 누적7,337개/주270아카이브/원본 미변경462아카이브, 신규500개·이전ID 누락0. 개발용 `NON-DISTRIBUTION`; 새 BPS/xdelta/ZIP 없음.

## 실제 반영과 입력

008 actual ROM/hash/metadata를 baseline으로 기존 초안500개를 추가했다. 신규 문구 생성0개이며 기존 문구·숫자·명령·줄 수를 임의 변경하지 않았다. 선정된64개 모두 기존 부분 적용 아카이브다. 주 아카이브 수가 늘어난 것은 아니다.

source-only selection `analysis/pending_insertion_500_009_partial_selection_v1/selection.json`, source-only preflight `analysis/pending_insertion_500_009_partial_preflight_v1/preflight.json`. 해당 raw payload는 기존 번역을 담지 않아 직접 삽입하지 않았다.64개 각 archive/script/source-ID/초안 hash와 개수는 이 machine-readable 기록이 권위다.

008 시점의 legacy reason 표현을 후속 generation에서 수정했다.009은 `existing partial archives require cumulative merge`를 명시하며 기존007·008 frozen 기록은 변경하지 않았다.

채택 `tools/cumulative_batch500.py`의 PROFILE009는 base008/hash, source preflight,64아카이브, prior PROFILE007/008을 명시한다. 권위 cumulative input `analysis/pending_insertion_500_009_cumulative_v1/preflight.json`; adapter `tools/cumulative_batch500_009.py`.64개 각각에서 parent asset/scope 재컴파일이 actual008 payload와 일치하고 병합 후 모든 비신규 script 바이트가 동일함을 확인했다. 이전 literal별 normal/big/mono profile·선택지 모델·review state를 보존하고 신규 scripts에만 normal/mmbn45/3행132px profile을 추가했다.

`manifest_lineage`를 명시적 profile 선택과 재귀 ancestry 검증으로 확장했다.009→actual008→actual007→middle-dot 각 링크는 해당 ROM/hash/metadata로 따로 검증한다. 현재 ROM에 이전 relocation offset을 적용하지 않는다. 변경되지 않은 clone도 payload뿐 아니라 layout/translated_units/source_sha256/protected_controls metadata identity를 검사한다.008 ancestry audit가 보완 후에도 통과했고,009 negative controls에서 이 거부 경계도 확인했다.

주 제품 경로 `build_keyitem_full_rom.py`→`build_roll_pet.py`→`build_development_patch.py`의 `--pending-batch500-009`는008 prerequisite를 요구한다. 기존 writer를64개 merged writer로 합성한 뒤 immutable 원본에서 Expected Writes를 계산한다. 이전 ROM 위에 순차 패치하지 않는다.

## 검증과 관찰

- `analysis/pending500_009_v1/integration.json`: actual 신규500-ID/기존누락0/7,337개, 변경64개 모든 비신규 script 바이트·기존 metrics 동일, 이전 비중첩217페이로드 및 소비 metadata 동일, final merged payload/hash와 known pointer relocation, 원본/헤더/전체 write/ISA 배치 감사, 독립 재빌드 동일 PASS.
- `selector_cpu.json`: composed mail/keyitem/gear 선택기3,195조건 PASS, 합성 CPU.
- `rejection_controls.json`: 유효 artifact accept 및 count누락/기존ID누락/기존metrics변조/retained script변조4조건 reject PASS. 메모리 내 negative controls만 사용했고 파일은 수정하지 않았다.
- `python -X utf8 -m unittest tools.test_korean_codec`:6tests PASS. frozen009 input64개/신규500개 binding 및 관련 Python syntax 검사 PASS.
- `normal_runtime.json`: 같은009 ROM cold boot→초기 설정·기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23쪽/복귀/재열기 PASS. `first_mail_pages_v1.png`23쪽 직접 시각 검사.
- `display_runtime.json`: 새71551C:37:0..1 프로그램군2쪽,68BAAC:3:0..1 넘버맨 아이템 알림2쪽. actual normal glyph CPU reads→OBJ VRAM/화면 픽셀, native root/origin/keyWait, 두 경로 페이지 지움 PASS. `changed_pages.png`4쪽 직접 시각 검사.

표시 진단은 같은 ROM의 정상 Rockman0/NumberMan8 상태를 정상 입력으로 만든 뒤 native PET pointer/table read만 alias한다. ROM/RAM 직접 쓰기 없음, 원래 msgOpen/mugshot/position/keyWait 명령 실행, diagnostic checkpoint 격리. 프로그램군은 native MrProgGreen,아이템 알림은 정상 NumberMan 문맥이다. 프로그램군37은 entry에 flag 분기가 없는 source-pinned direct display를 택했다. 자연 비행 결과/프로그램군 이벤트/아이템 획득·실제 알림 발생/보상/저장 증거가 아니다. alias는 ROM에 포함되지 않으며 원래 내비 lookup과 대사 연결은 유지된다.

## 재현

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_009_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005 --pending-batch500-006 --pending-batch500-007 --pending-batch500-008 --pending-batch500-009
```

## 다음 작업과 미완료

다음500개는 현재009 ROM/hash/metadata로 적용ID를 재계산해 선정한다.009 selector의 당시 허용 범위는1,769literal units 중500개를 고른 것이다. 전체 게임의 미번역 잔여 수가 아니며 current remaining count도 아니다.009 source-only 계획을 재사용해 동일500개를 다시 세지 않는다. 부분 적용 archive는 explicit cumulative merge와 single writer를 계속 요구한다.

전체500개 자연 scene/선택 결과/보상/저장 및 번역 의미·말투 검수, 가운데점 보류19문구 실제 삽입, 이전 별도 미해결4개(dynamic nickname), gear 일부 실화면, 한글 자동 조합·commit/save/redisplay ABI 통합은 남았다. 현 자판은 기존 일본어 배열+한글 동작 라벨이며 완성 한글 자판이 아니다. glyph 공급·표시 진단을 자동 입력/저장 완료로 확대하지 않는다.

원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 이전008 SHA256 `be95c71b2cabc2ca2bb7587b34bc38aa1d528868704d7f97a73efd3c63986e76`, 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 및 모든 기존 ROM/증거/패키지 보존. 사용자가 다시 요청하기 전까지 배포 패치를 만들지 않는다.
