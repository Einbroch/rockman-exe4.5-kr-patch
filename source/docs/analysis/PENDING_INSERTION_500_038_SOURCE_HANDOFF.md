# 038 정확500 준비 — 소스·전체carry 검증, ROM 미반영

## 현재 권위와 결과

- 권위 `pending_insertion_500_038_source_only_v5/batch_status.json`. 현재 ROM은 계속 `poc/output/pending500_037_v2.gba`, SHA `b98d6f5f7f1cbc9c4c25653edd8207635624e7ece23503d1ebfb9dce6dee51fd`, 누적19,622ID. **이번500 실제ROM 반영0**, 새패키지0/실행중명령없음/사용자mGBA·저장·원본·과거ROM불변.
- 기존 정규초안에서 중복없는500ID/271script/66archive를선정. NPC199+board224+hint77. **새문장500작성 아님**, 문구변경0/제어문자보존, 기계적으로확정된LF배치만사용. 모든needs_review/NON-DISTRIBUTION. 일본어자판/지역명/한글확정저장재표시미완료.
- `verification_v1.json` SHA `ef3ac82c021b1b2e0cb72bb691227b619e1f43db4378c2f75a39095bf81e3ce1`: 원본전체byte왕복, 번역전체semantic/control/binary왕복, 미선택원본script 보존, 실제037글꼴468개일치 PASS. 이것만 ROM등록입력으로사용금지: 기존번역을source로되돌릴수있다.
- `../pending_insertion_500_038_carry_v2/verification_v1.json` SHA `7ffcfcdbcfe1e5d7927e6d9557ee18f2691c4b77eaba66f8853a32422da453ac`: 기존owner24개는실제037전체compiledpayload를왕복검증한뒤새script만교체, **기존496ID/모든미선택script byte동일**. 선택script는source-only compile과byte동일, 전체target다시왕복PASS. 새owner42개도source완전target으로보존. 이파일은analysis용파생물이며,제품빌드는037부모를원본+선언입력에서재생성하여같은경계를증명해야한다. 이전ROM을제품빌드의source로사용금지.
- `preflight_v1.json` SHA `454a4a63b8964ee04d0039015bef986ef3a7389b2e2ad2f1ef02e4e38a831162`: 정확500/disjoint/66source table·TPI참조전체멤버십/원본LZ·pointer유지/nativebuffer한도/currentcarry보존 PASS. A4 `7B5110`/`7B5AA8` 두native동일alias는**전체target도byte동일**; 두owner모두선택/미해결alias0. source reference는자연획득증거아님.

## ROM 적용 전에 남은 경계

1. 새 geometry profile: `normal-store-tail-geometry`92ID는최종keyWait뒤global24/25/26/27/28저장tail만geometry투영에서제외; `normal-navi-tail-geometry`31ID는wait→clear뒤checkNavi/end tail만투영. **실제source/compiled명령은원문그대로**다. 그러나 native저장CPU영향/branch target의초기화·event outcome은아직검증하지않았으므로이투영만으로제품admission금지.
2. 기존037 두caller 외에 hint caller **BL4F802→LR4F807/root0203D800**, navi/scene/source lookup을세번째typed class로등록해야한다. 원본caller/selector에실제명령형상을검증하고 unrelated caller/null-scene를안전하게거부하는순서유지. A4/B1도source indexpath 확인일뿐자연진행승인아님.
3. 완전carry/supersession: 기존소비자578개와그번역을손상시키지않으면서새상위selector가24개기존archive를새완전clone으로소비해야함. 상속496ID를새500에합산금지. 원본에서037prefix/stub를재생성→단일composed write→038append/typeddescriptors,정확delta500,모든쓰기/전체diff/부모preserved controls/oldtranslatedscripts를제품빌드가강제해야한다.
4. actual-caller CPU/거부fixture/독립재빌드/전체image동일성/무결성후038 자체coldboot·세소비자대표표시/interaction. **037 state를038에사용금지**. 미리만든carrymsg만쓰거나부분500적용/패키지생성금지.

## 소스 사실 정정과 실패 자료

- **이전 prose의 ‘A4 NPC table null’은오류**. 원본 `0x53790` word는`0x08053B18`;해당table에sub0→53B20/sub1→53B40가있다. 기존 `037_source_only_v1/loader_classification_v1.json`도 `native_A4_NPC_table_is_null=false`로기록했다. 새500은이를원본에서재확인했으며자연A4도달을추론하지않는다. 과거마크다운의null주장을재사용금지.
- 038v1 필드한정기존모델후보265, v3 확장정적class모델447, v4 NPC/board후보394로500미달. 각`selection_attempt_*.json`보존. 새cleared-page Navi-tail투영/기존hint fullbox를합쳐총502중whole-script정확500선정(v5). 부분적용0/삭제0.
- carryv1은TextPet가`799314_current037.msg`에서archiveheader를같은suffix로유도하여skeletoncheck에서정확히거부했다. 부모payload byte재조립은이미동일했음. v2는`parent/799314.msg`정규basename을사용하며어떤검사도완화하지않았다. 실패폴더보존.
- preflightv1은helper `ref`가lookup loop의dict이름에가려져보고서직렬화직전TypeError. v2는receipthelper이름만변경,체크동일. 최종보고서명preflight_v1.json은도구v2가생성.

## 재개 지점

- 소스선정/컴파일/carry/preflight는완료. 기존nonemptyout에같은명령재실행금지. 이름고정된 `.py`는보고서해시로핀되어있으므로수정시새버전.
- 도구 `prepare_source500_038_v5.py`, `compile_source500_038_v1.py`, `compile_carry038_v2.py`, `verify_source038_v2.py`; 버전생성명세는`tools/specs/*038*`.
- 정상037seed는계속`poc/runtime/pending500-037-normal-v1-16/checkpoint.mss`/동일result.json. qualifiedstate는격리유지.
- 정규ROM미반영은계속**10,924**(이번선정500포함),그외미선정10,424. 전체게임/이미지의총잔여량아님. 20,122적용완료라고보고하지말것. 배포승인없음.
