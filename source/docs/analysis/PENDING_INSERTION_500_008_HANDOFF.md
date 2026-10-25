# 008: 다음500개 누적 병합·ROM 실제 반영

이 문서는008 단계의 이전 상태 기록이다. 이후009에서 신규500개를 추가 반영하고 검증했다. 현재 ROM/재개점 authority는 `analysis/PENDING_INSERTION_500_009_HANDOFF.md`; 아래 현재/다음 서술은008 당시 기준이다.

현재 ROM `poc/output/exe45_ko_development_pending500_008_v1.gba`, SHA256 `be95c71b2cabc2ca2bb7587b34bc38aa1d528868704d7f97a73efd3c63986e76`. 독립 `_repro.gba` 전체 바이트 동일. 누적6,837개/주270아카이브/원본 미변경462아카이브, 신규500개·이전ID 누락0. 개발용 `NON-DISTRIBUTION`; 새 BPS/xdelta/ZIP 없음.

## 적용 입력과 누적 계약

기존 초안 중007 실제 적용ID와 중복되지 않는500개를 선택해 반영했다. 신규 문구 생성0개이며 원문/기존 번역/숫자/명령/줄 수를 임의 변경하지 않았다. `tools/prepare_pending500_008_partial.py`의 baseline은007 ROM/hash/metadata다.

source-only 계획 `pending_insertion_500_008_partial_selection_v1/selection.json`, source-only 검사 `pending_insertion_500_008_partial_preflight_v1/preflight.json`. 이 raw payload는 기존 번역을 담지 않아 제품에 직접 삽입하지 않았다. selection의 legacy reason에 compiled consumers excluded라는 표현이 있지만, 권위 필드 `prior_partial_archives_included=true`/`requires_cumulative_merge`는23개 모두 기존 부분 적용임을 명시한다. 소비 경계가 검증됐다는 뜻도 아니다.

신규 개수:6A3DD0 6,6A5814 39,6AA214 3,6AB70C 45,6B6CA4 30,6BCFBC 33,6C1BFC 3,6C84C8 24,6CDCD0 33,6DA21C 102,71551C 21,716DE4 30,71A37C 3,71A66C 21,766134 3,76C944 18,776650 48,778338 3,7A152C 12,7A5604 15,7A8EC0 3,7A9EE4 3,683054 2. 합계500, 모두 기존 아카이브라 주 아카이브 수는 증가하지 않는다.

채택된 `tools/cumulative_batch500.py`를 명시적 PROFILE007/PROFILE008 인자로 확장했다. 이전 profile의 globals를 덮어쓰지 않는다.008은002..006 및007 merged scope를 복원하고 실제007 parent asset/hash/payload에 바인딩한다. literal-level normal/big/mono 표시 설정과 이전 선택지 모델을 보존하고 신규 scripts에만 normal/mmbn45/3행132px profile을 추가한다. schema2 링크는 pinned parent에 남기고 병합 asset에는 명시적 resolve 결과를 사용한다.

008 adapter `tools/cumulative_batch500_008.py`; 권위 cumulative input `analysis/pending_insertion_500_008_cumulative_v1/preflight.json`.23개 각각에서 기존 asset/scope 재컴파일이 actual007 payload와 일치하고 병합 후 비신규 script 바이트가 동일함을 확인했다.007 frozen entry13개와007 cumulative audit도 보완된 도구에서 통과했다.

주 제품 경로 `build_keyitem_full_rom.py`→`build_roll_pet.py`→`build_development_patch.py`의 `--pending-batch500-008`는007 prerequisite를 요구한다. 이전 writer를008 writer 하나로 합성한 뒤 immutable 원본에서 Expected Writes를 계산한다. 이전 ROM을 다음 패치 입력으로 사용하지 않는다.

`manifest_lineage`는 현재008→actual007 검증과 exact007→middle-dot 검증을 각각 수행한 뒤 selected asset ancestry를 정규화한다.008 ROM에007의 옛 relocation offset을 적용하거나 모든 중첩 아카이브를 광범위한 예외로 빼지 않는다.

## 검증

- `analysis/pending500_008_v1/integration.json`: actual 신규500-ID/기존누락0/6,837개, 변경23개 모든 비신규 script·기존 metrics 동일, 비중첩 이전258페이로드 전체 동일, merged final payload/hash 및 known pointer relocation, 원본/헤더/전체 write/ISA 배치 감사, 독립 재빌드 동일 PASS.
- `selector_cpu.json`: composed mail/keyitem/gear 선택기3,195조건 PASS, 합성 CPU.
- `rejection_controls.json`: 유효 artifact accept 및 count누락/기존ID누락/기존metrics변조/retained script변조4조건 reject PASS. 메모리 내 negative control만 사용, 파일 변경 없음.
- `python -X utf8 -m unittest tools.test_korean_codec`:6tests PASS.
- `normal_runtime.json`: 같은008 ROM cold boot→초기 설정·기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23쪽/복귀/재열기 PASS. `first_mail_pages_v1.png`23쪽 직접 시각 검사.
- `display_runtime.json`: 신규71551C:11:0..2 프로그램군3쪽,776650:24:0..2 썬더맨 통신 선택지3리터럴. 실제 normal glyph CPU reads→OBJ VRAM/화면 픽셀, native root/origin/keyWait/select, 커서 위/아래/위 이동, 프로그램군 페이지 지움 PASS. `changed_pages.png`6화면 직접 시각 검사, 글자 잘림/겹침이 보이지 않았다.

표시 진단은 같은 ROM의 정상 Rockman0 PET 상태에서 native pointer/table read만 alias한다. ROM/RAM 직접 쓰기 없음, 원래 msgOpen/mugshot/flag/position 명령 실행, diagnostic checkpoint 격리. 프로그램군은 native MrProgGreen,통신 대사는 native ThunderMan portrait다. 자연 이벤트/썬더맨 선택/통신 오류 발생/선택 확정·배틀 결과/보상/저장 증거가 아니다. alias는 ROM에 들어가지 않는다.

초기 통신 검사기는 기존 Rockman0의 select targets1/2(`EC06800102FF`)를 재사용해 거부했다. immutable 원본776650 script24와 실제008 화면의 세 선택 대기 모두 ThunderMan targets25/26(`EC0680191AFF`)임을 확인했다. 검사기를 해당 source-pinned contract로 수정했으며 ROM·runtime receipt는 그대로 유지했다. 거부를 게임 결함으로 처리하거나 임의 select bytes를 허용하지 않았다.

## 재현

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_008_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005 --pending-batch500-006 --pending-batch500-007 --pending-batch500-008
```

## 다음 작업과 미완료

다음500개는 현재008 ROM/hash/metadata를 baseline으로 선정한다.008 selector의 당시 허용 범위는1,677script groups/2,269literal units 중500개를 고른 것이다. 이 숫자는 전체 게임의 미번역 잔여 수가 아니다. 현재 적용ID를 재계산하고 raw/no-print/geometry/source-bound 부분 적용 아카이브는 동일한 cumulative merge 계약을 사용한다.008 source-only 계획을 재사용해 같은500개를 다시 세지 않는다.

모든500개 자연 scene/선택 결과/보상/저장 검증, 번역 의미·말투 검수, 가운데점 보류19문구 실제 삽입, 이전 별도 미해결4개(dynamic nickname), gear 일부 실화면, 한글 자동 조합·commit/save/redisplay ABI 통합은 남았다. 현 자판은 일본어 배열+한글 동작 라벨이며 완성 한글 자판이 아니다. glyph 공급·표시 진단을 자동 입력/저장 완료로 확대하지 않는다.

원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 이전007 SHA256 `c5078d66ffe11d4cc80960edb5484bf9bf3f8b4d533c28d178581345a4367656`, 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 및 모든 기존 ROM/증거/패키지 보존. 사용자가 다시 요청하기 전까지 배포 패치를 만들지 않는다.
