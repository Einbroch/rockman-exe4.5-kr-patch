# 이전 기록010: 현재 권위는 PENDING_INSERTION_500_011_HANDOFF.md

아래010 artifact/검증은 보존된 이전 기록이다. 최신 ROM 및 다음 재개점은 `analysis/PENDING_INSERTION_500_011_HANDOFF.md`를 사용한다.

## 010: 다음500개 실제 반영 —49 carry·20 new archives

현재 ROM `poc/output/exe45_ko_development_pending500_010_v1.gba`, SHA256 `8f05118a2dd8a7e452e81f81413b1c580fe9883493aae1e0d85c3d496075663a`. 독립 `_repro.gba` 전체 바이트 동일. 누적7,837개/주290아카이브/원본 미변경442아카이브, 신규500개·기존ID 누락0. 개발용 `NON-DISTRIBUTION`; 새 BPS/xdelta/ZIP 없음.

## 실제 적용과 입력

009 actual ROM/hash/metadata로 적용ID를 재계산해 기존 초안500개를 추가했다. 신규 문구 생성0개, 원문·기존 문구·숫자·명령·줄 수를 임의 변경하지 않았다. source-only selection `analysis/pending_insertion_500_010_partial_selection_v1/selection.json`, source-only preflight `analysis/pending_insertion_500_010_partial_preflight_v1/preflight.json`이69개 archive/script/source-ID·초안 hash·개수의 권위다. source-only payload는 기존 번역을 담지 않아 직접 삽입하지 않았다.

기존 부분 적용49개는 누적 병합했고 새20개는 parent=null인 source-only input으로 등록했다. 새20개는693778,693AA4,6989B0,698CB0,699194,69E5A8,69E61C,69E6BC,69EA0C,6A504C,6AA1A0,6AA730,6AAB08,6AAEB0,6AB600,6AE758,6B6050,6B60F0,6B6474,6B69A0이다. 모두 기존 registry와 primary/supplemental 적용 아카이브에서 absent임을 검사했다.

채택 `tools/cumulative_batch500.py` PROFILE010은 base009/hash,source preflight,69개 및 명시적20개 new inventory,prior PROFILE007/008/009를 고정한다. adapter `tools/cumulative_batch500_010.py`; 권위 cumulative input `analysis/pending_insertion_500_010_cumulative_v1/preflight.json`.

49개는 parent asset/scope를 재컴파일해 actual009 payload와 동일한지 검사한다. 기존 per-literal normal/big/mono profile·선택지 모델·review state를 보존한다. 새20개는 immutable 원본 payload를 기준으로 raw/no-header/known-pointer contract와 native·semantic·binary roundtrip,unselected source-script identity를 검사한다. 신규 scripts에만 normal/mmbn45/3행132px profile을 적용한다. 기존007..009 frozen assets와 preflight는 그대로다.

주 제품 경로 `build_keyitem_full_rom.py`→`build_roll_pet.py`→`build_development_patch.py`의 `--pending-batch500-010`는009 prerequisite를 요구한다.49개 writer를 병합 writer로 교체하고 새20개 writer/path를 추가한 뒤 immutable 원본에서 Expected Writes를 계산한다. 기존 ROM 위에 순차 패치하지 않는다. new/carry metadata 차이와 actual500-ID 증가를 따로 검사하며 ancestry는 exact artifact별로 재검증한다.

startup 감사의 아카이브 분모와 first-mail 감사의 Expected Write inventory에도 새20개 source pointer write를 명시적으로 포함했다. 변경 범위를 통째로 허용하거나 기존 검사기를 비활성화하지 않았다.009 ancestry audit가 보완 후에도 통과했다.

## 검증

- `analysis/pending500_010_v1/integration.json`: actual 신규500-ID/기존누락0/7,837개, 기존49개 모든 비신규 script 바이트·metrics 보존, 비중첩 이전232페이로드/metadata 동일, 새20개의 unselected source scripts/native 저장 영역·payload hash·known pointers, 원본/헤더/전체 write/ISA 배치 감사, 독립 재빌드 동일 PASS.
- `selector_cpu.json`: composed mail/keyitem/gear 선택기3,195조건 PASS, 합성 CPU.
- `rejection_controls.json`: 유효 artifact accept 및 count누락/기존ID누락/기존metrics변조/retained script변조4조건 reject PASS.
- `new_archive_controls.json`: 유효 artifact accept 및 new payload변조/new ID누락/new pointer metadata변조/실제 pointer bytes변조/native source storage변조5조건 reject PASS. 위9조건은 메모리 내 negative controls이며 파일 수정 없음.
- codec6tests, 관련 Python syntax 검사와 frozen input69개/신규500개/새20개 binding PASS.
- `normal_runtime.json`: 같은010 ROM cold boot→초기 설정·기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23쪽/복귀/재열기 PASS. `first_mail_pages_v1.png`23쪽 직접 시각 검사.
- `display_runtime.json`: 새6989B0:1:0 승리 대사와 기존6886F0:20:0 토너먼트 안내, 총2리터럴. actual glyph CPU reads→OBJ VRAM/화면 픽셀, native root/origin/keyWait 및 빈 영역 검사 PASS. `changed_pages.png`2화면 직접 시각 검사.

표시 진단은 같은 ROM에서 정상 입력으로 NumberMan8 상태를 만든 뒤 native PET pointer/table read만 alias한다. ROM/RAM 직접 쓰기 없음, native position/msgOpen/keyWait 실행, diagnostic checkpoint 격리. 이 화면의 NumberMan portrait는 진단 시작 문맥이며6989B0 원래 화자/내비 선택·배틀 승리 결과를 증명하지 않는다. alias는 ROM에 설치하지 않아 원래 내비 lookup/대사 연결은 유지된다.

## 통과하지 않은 waitHold 표시 진단

`poc/runtime/pending500-010-v1-display-new-loss`는 aliases1/1이지만 snapshots2/3의 native root가 target6989B0 pool이 아닌 기본 PET 메뉴 pool이어서 검사에서 거부됐다. 화면도 기본 메뉴로 복귀했다. 원본 source6989B0 script2는 keyWait 없이 waitHold로 끝난다. 전용 배틀 결과 caller/context를 보존하지 않는 PET 진단으로 stable loss display를 증명할 수 없다.

이 관찰을 patch gameplay defect로 확정하지 않았고 waitHold를 keyWait로 바꾸거나 ROM을 재빌드하지 않았다. `wait_hold_probe_unverified.json`에 source contract/actual roots·pointers/screenshot hashes/거부 범위를 기록했다. 새-loss receipt·snapshots·diagnostic state는 보존했다.2개 keyWait 샘플만 PASS 보고서에 포함한다. Source waitHold의 실제 배틀 결과·지속 표시·진행 검증은 미완료이며 다음 작업에 남긴다.

## 재현

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_010_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005 --pending-batch500-006 --pending-batch500-007 --pending-batch500-008 --pending-batch500-009 --pending-batch500-010
```

## 다음 작업·미완료

다음500개는010 ROM/hash/metadata로 적용ID를 재계산해 선정한다.010 selector의 당시 허용 범위는1,269literal units 중500개를 고른 것이다. 전체 미번역 잔여 수나 current remaining count가 아니다.49 carry/20 new를 재사용해 동일500개를 또 세지 않는다. 이후 mixed cohorts에서도 single writer·누적 input·새 pointer write inventory를 유지한다.

waitHold 대사의 verified native battle caller 검증, 전체500개 자연 scene/선택 결과/보상/저장 및 번역 의미·말투 검수, 가운데점 보류19문구 실제 삽입, 이전 별도 미해결4개(dynamic nickname), gear 일부 실화면, 한글 자동 조합·commit/save/redisplay ABI 통합은 남았다. 현 자판은 기존 일본어 배열+한글 동작 라벨이며 완성 한글 자판이 아니다. glyph 공급·부분 표시 진단을 자동 입력/저장 또는 전체 QA 완료로 확대하지 않는다.

원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 이전009 SHA256 `0b623c19d8cbc944b555b26c2571c52d110e076af5fdb5aa0bedf52c0ac54096`, 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 및 모든 기존 ROM/증거/패키지 보존. 사용자가 요청하기 전까지 배포 패치를 만들지 않는다.
