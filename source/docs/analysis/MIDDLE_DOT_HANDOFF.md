# 가운데점 지원과 다음500개 source-only 준비

이 문서는 가운데점 단계의 이전 상태 기록이다. 여기서 준비한13아카이브 신규500개는 이후007에서 누적 병합·ROM 적용·검증을 완료했고008..016에서 추가 반영했다. 현재 authority는 `analysis/PENDING_INSERTION_500_016_HANDOFF.md`; 아래 미완료 서술은 당시 기준이다. historic19 보류 ID의 마지막 별도 재대조는015에서14적용/5미적용이며 `analysis/pending500_015_v1/middle_dot_reconciliation.json`을 따른다.016의새24아카이브범위에는그5개가포함되지않았다. 전체 게임 미번역 수 또는 의미 검수 완료 수가 아니다.

현재 ROM `poc/output/exe45_ko_development_middle_dot_v1.gba`, SHA256 `bd16c794be18178e84e0d473c0faff43c78eb1d492f8c7b9137265ff5aef3f0c`. 독립 `_repro.gba` 전체 바이트 동일. 누적5,837개/주270아카이브 유지, 신규 번역 적용0개다. 정책 `development-draft; NON-DISTRIBUTION`, 새 배포 파일 없음.

## 채택한 문자 공급

`korean_codec.py`에서 기존 Hangul0..11171/쉼표11172는 그대로 유지하고 `·`을11173(`F9FCA52B`)로 추가했다. 기존 Galmuri11-Condensed-v2.40.4 고정 BDF의 실제 가운데점 glyph를12px advance/vertical shift0으로 공급한다. 새 글자 모양을 임의로 그리거나 기존 문구를 다른 점으로 치환하지 않았다.

자모 glyph mapping은 추가 문자 집합 끝에서 파생되는 JAMO_BASE11174를 사용한다. 이전 자모 glyph의 동일한 bitmap/advance는 유지하며 physical slot만+1 이동했다. mixed display 후보의 Python/Thumb encoder도 상수+1을 제거하고 같은 mapping에서 파생되도록 보완했다. 이전 독립 후보 binary의 old jamo mapping을 새 ROM에 그대로 사용하지 않는다. 후보는 여전히 게임 입력/저장 hook으로 설치되지 않았다.

초기 회귀 감사는 font bank 전체 바이트 동일을 요구해 정상적인 한 슬롯 추가에도 거부했다. `font_extension_lineage.py`로 오직 명시적 `·` 한 슬롯 성장만 허용하고, legacy/Hangul/쉼표 prefix와 모든 기존 자모의 bitmap/advance identity를 검증한다. bank growth96/4/64bytes, jamo mapping+1, 신규 nonempty dot/12px를 모두 확인한다. 임의 font 변경을 허용하는 우회가 아니다.

## 검증

- `middle_dot_v1/integration.json`: 원본 보존/독립 재빌드 일치/모든 기존 주 및 별도 번역 payload 동일, normal 기존 문자 prefix와 자모 identity 보존, 가운데점 BDF record/advance PASS
- `selector_cpu.json`: 기존 메일/keyitem/장비 선택기3,195조건 PASS, 합성 CPU
- `mapping_cpu.json`:19초성×10슬롯×edit/commit-mode380조건, host/Thumb glyph identity·출력 범위·원본 surface·register/SP 보존/partial commit 거부 PASS. 실제 게임 자판/저장 증거 아님
- codec6tests/명시적 페이지5tests PASS
- `normal_runtime.json`: 같은 ROM cold boot→날짜/이름/초기 설정→기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23쪽/복귀/재열기 PASS
- `first_mail_pages_v1.png`: 해당23쪽 직접 시각 검사
- `glyph_runtime.json`: normal renderer의 실제 가운데점 font CPU reads, BDF record→OBJ VRAM/화면 픽셀 및 native wait/root PASS. `poc/runtime/middle-dot-v1-glyph/step_002.png` 직접 시각 검사

격리 진단은 정상 NumberMan8 상태에서 `68C2CC` script3를 table read alias로 표시한 뒤, 원래 쉼표 한 곳의 low-rank byteA4를 normal handler `ldrb r7,[r4,#2]` read에서만A5로 반환한다. final handler 명령과 PC/r4 stream/r5 context0200FA20/source byte를 검사한다. ROM/RAM을 직접 쓰지 않으며 원래 ROM 쉼표4바이트는 그대로다. 해당 font-supply 진단을 실제 번역 적용 또는 자연 배틀/보상/저장 증거로 세지 않는다. diagnostic checkpoint와 receipt는 격리돼 있다.

## 다음500개 준비와 실제 적용 미완료

미등록/raw/no-print/geometry 제한만 적용하면249script/249리터럴만 남아500개 구성이 불가능했다. `pending_insertion_500_007_selection_v1/selection_failure.json`에 범위와 실패를 기록했다. 이는 전체 미번역 잔여249개라는 뜻이 아니다.

기존 부분 적용 아카이브도 조사하되, 이미 적용한 ID가 하나라도 있는 script는 제외해 다음500개를 선정했다. 권위 selection `pending_insertion_500_007_partial_selection_v1/selection.json`; source-only 검사 `pending_insertion_500_007_partial_preflight_v1/preflight.json`. 정확한500개 신규 ID/기존 intersection0, 원본/명령/숫자/줄 수·encoding·font·의미/바이너리 왕복·unselected SOURCE script byte identity PASS.13아카이브 모두 기존 부분 적용 아카이브다.

구성:6CDCD0(33),71551C(89),7A152C(14),6A3DD0(49),6DA21C(129),71A66C(5),71BE98(5),7A5604(13),7AF6D0(5),716DE4(36),76C944(80),688A10(18),69F220(24).

이 사전 검사는 **immutable 일본어 원본 + 새500개만**으로 컴파일한 것이므로 기존 번역을 함께 담지 않았다. product input으로 바로 사용하면 기존 번역이 사라질 수 있다. 따라서 누적 ROM 적용은0개이며 기존 `batch500_007_rom.py`의 일반 raw/batch-id 계약도 이 partial-source-only 보고서를 승인하지 않는다. 현재 빌드 경로에는007 flag를 등록하지 않았다.

### 다음 안전한 작업

1.13개 각각의 현재 ROM asset/registry/consumer profile/특수 renderer·code provider를 복원한다. 특히6DA21C의 기존 save 관련 mixed consumer,71551C 등의 기존 특수 경계를 단순 normal scope로 덮어쓰지 않는다.
2. 기존 ID/문구와 신규 ID500개를 명시적으로 병합하고, 기존 scripts/languages/layout/명령/원래 source를 보존한 **cumulative merged preflight**를 별도 생성한다. literal-level partial carry와 source-ID 원본 추적도 검증한다.
3. 이전 cohort translation path/registry/clone registration과 중복되지 않게 하나의 최종 writer로 합성한다. 기존 ROM을 입력으로 패치하지 않고 immutable 원본 기반 누적 빌드에 등록한다.
4. 실제500-ID 증가와 기존 ID 누락0, 이전 script 및 consumer 보존, 모든 포인터/write-set, 독립 재빌드 및 affected runtime를 확인한다. 이때만 누적6,337개를 주장한다.
5. 보류19개 가운데점 문구는 현재 selection500개에 포함되지 않았다. 지원 인코딩 gap은 보완했지만 실제 삽입/레이아웃·소비 검증은 따로 남는다.

## 현재 ROM 재현

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_middle_dot_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005 --pending-batch500-006
```

기존 원본·006 ROM SHA256 `02d14a3ead55aa2d52f9458b095384c50c7c92683f82ae08a685c794bb8edc69`·기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 및 모든 이전 증거는 보존했다. 새 출력 이름/runtime prefix를 사용한다. 전체 자연 진행/보상/저장/한글 자동 조합·입력·재표시 ABI/실기·음성·문구·미감 승인은 여전히 미완료다. normal 가운데점 소비 증거를 모든 fixed-cell/menu/입력/저장 경로의 완료로 확대하지 않는다.
