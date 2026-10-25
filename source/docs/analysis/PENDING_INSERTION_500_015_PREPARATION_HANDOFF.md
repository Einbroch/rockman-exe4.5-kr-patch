# 015 준비: 미적용6개 source-only 사전 검사 완료, ROM 미반영

이 문서는 준비 당시 기록이다. 이후6개를015제품ROM에누적병합하고정적/런타임검증했다. 현재권위는 `PENDING_INSERTION_500_015_HANDOFF.md`이며 아래ROM미반영/제품flag없음/미검증서술은 당시 상태를 보존한다.

현재 실행/검증 완료 ROM은014다: `poc/output/exe45_ko_development_pending500_014_v1.gba`, SHA256 `6cdcae37d8682c03a909b08d3ddefea02ad825c6a272899c38bcc5f316be9245`.015 제품 ROM·제품 flag·누적 preflight는 아직 없다. source-only 결과를 실제 ROM 적용 또는 화면 검증으로 세지 않는다. 신규 배포 패키지 없음, 원본·014·기존 ZIP hash 보존. 정책 NON-DISTRIBUTION; 표현 approved=False/needs_review.

## 이번 결과 및 권위

남은 historic9개를 원본TPI payload/TPL/실제014 적용ID와 대조했다. `pending_insertion_500_015_partial_preflight_v1/backlog_consumers.json`이 이번 소비 분류 근거다. 일반 대사4개, 선택지 포함3개, 작은 메뉴 renderer2개이며 모두 아직014에 미적용이다. 132px 측정은 기존 normal용 채택 범위이지 작은 메뉴/선택지의 확인된 최대 용량이 아니다. historic9는 전체 게임 미번역 수가 아니다.

처음7C9C44 script0의2개를 준비한 source-only v1을 보존했고, 이후768800 script2의4개를 더한 v2가 최신 **삽입 준비** 권위다:

- `pending_insertion_500_015_partial_selection_v2/selection.json`
- `pending_insertion_500_015_partial_preflight_v2/preflight.json`
- `translations/batch500_000_insertion015_7C9C44_draft_ko.json`
- `translations/batch500_000_insertion015_768800_draft_ko.json`

실제6 source-ID·기존 적용 교집합0·geometry candidate0. 원본 native roundtrip/보호 제어/semantic roundtrip/binary roundtrip PASS. native/compiled:768800 976/1231bytes(script table13),7C9C44 2094/2186bytes(script table23). source-only payload는 원래 다른 스크립트의 일본어를 보존하며 이미 적용된 번역을 담지 않는다. 특히768800의 기존4개(1:0,4:0,7:0,8:0)를 지울 수 있으므로 직접 ROM 삽입 금지.

이번 신규 원문 번역0개, 직접 작성한 대안4개, 기존 표현 그대로 재사용2개다. compiler의 draft reuse/newly_translated 표시는 선택한 입력 asset에 대한 기록이며 이번 authored wording 대안 수와 다르다. 규칙 기반 축약/치환은 없고 원래 초안과 source/TPL/control/줄 수는 유지했다.

## 표현과 맥락

`pending_insertion_015_wording_proposals.json`:

- 7C9C44:0:0: `여긴 영원한 증오가\n휘몰아치는 세계···`.
- 7C9C44:0:1: `밉다···밉다···\n온 세상이···`.

원문의 여기/영원한 증오/격렬한 소용돌이와 반복되는 증오/온 세계/미완의 말끝을 보존하는 개발용 표현 후보다. source script0에는msgOpen은 있지만mugshotShow는 없다. 인접script1에LaserMan이 등장한다는 이유로script0의 화자를 레이저맨으로 확정하지 않았다. 최종 runtime에서도 portrait를 추가하거나 메뉴창 origin을 임의로 가정하지 않는다.

`pending_insertion_015_tutorial_wording_proposals.json`:

- 768800:2:0: `그렇다, 지금 록맨이\n유니존 가능한 소울은\n거츠 소울이지`.
- 768800:2:2: `즉 「크랙아웃」 등\n지형 파괴 칩을 바쳐\n유니존할 수 있다`.

나머지2:1/2:3은 초안 그대로다. 거츠맨의 주먹/패널 파괴, 지형 파괴 칩을 바치는 조건, 크랙아웃 예시, 가능성·설명 순서를 유지했다. 원문3행 그대로. 실제 현재 normal 채택 범위를 넘던2:0/2:2를 함께 다루어 complete script4쪽을 선택했다. 원본에MrProgGreen portrait가 명시된다. 이는 legacy 소울 유니존 설명이며 ROM 내 존재만으로EXE4.5 실제 플레이의 기능 지원/자연 진입을 주장하지 않는다.

두 producer는 원래 초안 고정SHA/TPL/source profile을 검사하고, proposal ID→source-ID→원래 parent path/hash 관계를 생성 asset에 보존한다. 원래 초안은 수정하지 않는다. 관련 syntax PASS. 제안의 독립/사람 의미 검수와 presentation approval은 미완료다.

## 다음 작업

1.014 exact artifact/hash를 parent로 삼는 누적015 preflight를 준비한다.768800 parent scope는012에서normal3행132px, literal_scripts=[1,4,7,8],4개다. 신규script2와 기존4개를 단일 writer로 병합하고 기존 다른script/metrics/profiles/실제parentpayload identity를 검사한다.7C9C44는새 raw아카이브로23script/known pointer/source bytes를 원본TPI에서 고정한다.
2.누적asset에도 두 manual_wording_proposals 링크를 보존하고,015 product flag를 원래3단계 builder 및 ExpectedWrites/lineage에 연결한다. source-only v2로부터 ROM을 직접 고치지 않는다.
3.원본 기반 새ROM/독립재빌드·실제6-ID delta·기존330+014신규3개 페이로드 보존·known pointer/전체write/ISA 감사를 한다.
4.같은 새ROM의 정상 초기 설정/첫메일 회귀와 변경6쪽을 검증한다.7C9C44는무초상화 msgOpen의 실제origin/clearing을 확인한다. 표시 진단은 자연 진입/화자 확정/유니존 기능/배틀/저장 증거가 아니다.

historic9의 나머지5개는7688002개/7C9C442개가 실제 적용되기 전까지 사라지지 않는다. 이번6개 중 historic 보류에 속한 것은4개다. 지금은historic 적용10/미적용9 그대로다. 이후6개 적용 성공 시 historic 적용14/미적용5로 대조할 수 있으나 아직 그 상태가 아니다.

나머지7B4184script0/4의 선택지는source positionOptionHorizontal width13/11, padding/space, targets(jump3/continue/cancel)을 가진다. 전체script0의4개 및script4의6개를 함께 검사해야 한다. 현재 초안0:3과4:1의normal 측정은172/192px로 채택 범위를 넘는다. 선택지 label만 표시한 성공을 전체 분기/결과 성공으로 세지 않는다.

7CC6A0:76:0/78:0의source language는mmbn45s이고순수 label+end다. normal font hook을 통한 일반 대사 삽입은 맞는 소비 경로가 아니다. 작은 renderer encoding/글꼴·profile menu 호출/선택/재표시를 검증해야 한다. 실제 자동 한글 자판·commit/save/redisplay ABI도 별도 미완료다.

재현(기존 생성 폴더를 덮어쓰지 않음): `python -X utf8 tools/prepare_middle_dot015_inputs.py`, `python -X utf8 tools/prepare_middle_dot015_tutorial_inputs.py`; v2 selector/compiler는 `python -X utf8 tools/prepare_pending500_015_partial_v2.py`. source-only 컴파일 및 분류 외015 제품/런타임 검증은 미실행이다.
