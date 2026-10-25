# 007: 기존 부분 적용 아카이브 신규500개 실제 누적 반영

이 문서는007 단계의 이전 상태 기록이다. 이후008에서 다음500개를 추가 반영하고 검증했다. 현재 ROM/재개점 authority는 `analysis/PENDING_INSERTION_500_008_HANDOFF.md`; 아래 현재/다음 서술은007 당시 기준이다.

현재 ROM `poc/output/exe45_ko_development_pending500_007_v1.gba`, SHA256 `c5078d66ffe11d4cc80960edb5484bf9bf3f8b4d533c28d178581345a4367656`. 독립 `_repro.gba` 전체 바이트 동일. 누적6,337개/주270아카이브/원본 미변경462아카이브, 신규500개·이전ID 누락0. 정책 `development-draft; NON-DISTRIBUTION`, 새 BPS/xdelta/ZIP 없음.

## 실제 적용과 병합 계약

기존 source-only selection `pending_insertion_500_007_partial_selection_v1/selection.json`과 `pending_insertion_500_007_partial_preflight_v1/preflight.json`의 신규500개를 사용했다. 기존 초안 재사용이며 신규 문구 생성0개다. source-only payload를 그대로 ROM에 넣지 않았다.

13아카이브:6CDCD0 신규33,71551C89,7A152C14,6A3DD049,6DA21C129,71A66C5,71BE985,7A560413,7AF6D05,716DE436,76C94480,688A1018,69F22024. 모두 기존 부분 적용 아카이브라 주 아카이브 수는 그대로다.

채택 adapter `tools/cumulative_batch500.py`, 병합 사전 검사 `tools/prepare_cumulative500_007.py`, 권위 입력 `analysis/pending_insertion_500_007_cumulative_v2/preflight.json`. 해당 보고서의 source/parent asset hash, source-only preflight hash, old scope와 신규 scripts disjoint, literal-level consumer 설정, 최종 merged asset/compiled hash를 제품 빌드에서 다시 확인한다.

기존 13개 실제 ROM payload를 기존 asset/scope로 재컴파일해 바이트 동일을 먼저 증명했다. 기존 script별 데이터는 모두 보존하며 새 script만 바뀐다. 6DA21C 기존 fixed-big 저장 라벨과 choice geometry,76C944 기존 fixed-mono 질문 및 별도144/168px normal profile도 그대로다. 신규 scripts에만 normal/mmbn45/3행132px profile을 추가한다. schema2 부모의 wording links는 hash-bound 원본에 보존하고 schema1 병합 입력에는 명시적 `resolve_units` 변환 결과를 넣었다. 원문·문구·state identity를 유지한다.

초기 cumulative_v1은 schema2 resolved unit과 신규 schema1 unit을 혼합해 resolve 단계에서 거부됐다. 그 파생 입력은 보존하고 v2의 명시적 변환으로 수정했다. v1에서 제품 ROM을 생성하지 않았다. 기존 untouched-only 제안 adapter `batch500_007_rom.py`는 미채택이며 주 빌드에 연결되지 않았다.

`build_keyitem_full_rom.py`→`build_roll_pet.py`→`build_development_patch.py`의 `--pending-batch500-007`가 이전13개의 translation path/registry/tuple writer를 병합 writer 하나로 바꾼다. immutable 원본에서 Expected Writes를 합성하며 이전 ROM 위에 순차 패치하지 않는다.

## 검증과 관찰 범위

- `analysis/pending500_007_v1/integration_v2.json`: 실제 신규500-ID/기존누락0/6,337개, 이전 비중첩 페이로드 전체 동일, 중첩13개 모든 비신규 script 바이트·기존 layout metrics 동일, 포인터/source/단일 write/ISA 배치 감사, 독립 재빌드 동일 PASS. `integration.json`은 audit의 carry 표현을 보완하기 전 보고서이며 v2가 현재 권위다.
- `selector_cpu.json`: 기존 메일/keyitem/장비 선택기3,195조건 PASS, 합성 CPU.
- `rejection_controls.json`: 유효 current artifact accept와 declared count누락/기존ID누락/기존metrics변조/retained script변조4조건 reject PASS. 모두 메모리 내 negative control; 원본/ROM/asset 파일 변경 없음. 일반 gameplay 시험이 아니다.
- `python -X utf8 -m unittest tools.test_korean_codec`:6tests PASS. 직접 파일 실행은 import 경로가 맞지 않아2오류였고 모듈 entry point로 정상 실행했다.
- `normal_runtime.json`: 같은 ROM의 정상 cold boot→초기 설정·기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23쪽/목록 복귀/재열기 PASS. `first_mail_pages_v1.png`23쪽 직접 시각 검사.
- `display_runtime.json`: 새71551C:17:0..3(프로그램군4쪽),6CDCD0:7:0..2(가족 질문3쪽), 총7리터럴의 실제 normal glyph CPU reads→OBJ VRAM/스크린 픽셀, exact native root/keyWait와 origin PASS. `changed_pages.png`7쪽 직접 시각 검사. 문자 잘림/겹침이 보이지 않았다.

표시 진단은 같은 ROM에서 정상 록맨0/넘버맨8 상태를 만든 뒤 native PET pointer/table read만 alias했다. ROM/RAM 직접 쓰기 없음, native msgOpen/mugshot/position 설정 실행, 진단 checkpoint 격리. 프로그램군은 MrProgGreen native portrait를 사용하며 가족 질문은 진단 시작 NumberMan 문맥이다. 이 화면은 자연 내비별 이벤트 선택/원래 대사 화자/진행/선택 확정/보상/저장 증거가 아니다. alias는 ROM 패치에 포함되지 않았고 원래 내비 lookup이 그대로다.

## 재현

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_007_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005 --pending-batch500-006 --pending-batch500-007
```

## 다음 작업과 미완료 조건

다음500개 선정의 baseline을 현재007 ROM/hash/metadata로 옮긴다. 부분 적용 아카이브는 이번과 같이 누적 scope/asset 병합을 필수로 하고 이미 적용한 ID/script를 재계산한다. 기존 `prepare_pending500_007_partial.py`는 middle-dot 단계 source-only 계획이므로 현재 ROM에 그대로 재사용해 같은500개를 세지 않는다. 현재 단계에서 전체 미번역 잔여 수는 확정하지 않았다.

모든500개 자연 scene/선택 결과/보상/저장 검증과 번역 의미·말투 검수, 기존 보류19개 가운데점 문구 실제 삽입, 이전 별도 미해결4개(dynamic nickname), gear 일부 실화면, 한글 자동 조합·commit/save/redisplay ABI 통합이 남았다. 현 ROM의 자판은 기존 일본어 배열+한글 동작 라벨이며 완성 한글 자판이 아니다. 글꼴 공급·표시 샘플을 자동 조합/저장 완료로 확대하지 않는다.

immutable 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 이전 middle-dot ROM SHA256 `bd16c794be18178e84e0d473c0faff43c78eb1d492f8c7b9137265ff5aef3f0c`, 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`과 모든 이전 산출물/증거는 보존했다. 사용자가 요청하기 전에는 새 배포 패치를 만들지 않는다.
