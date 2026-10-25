# 거츠맨 플러그아웃 미번역 — 2026-10-09

## 현행 제품과 범위

`poc/output/exe45_ko_development_gutsman_plugout_v1.gba`
SHA256 `b69f585644084b5cfb090e4fafc7b0f3b41ea04315b204d1da4bd08600f67df1`.
미번역 4literal 추가, 누적2,392선택literal / 59선택archive·673원본유지archive.
전체 번역 완료/배포본이 아니다. needs_review, NON-DISTRIBUTION, release_eligible=false.

778338:7의 거츠맨 플러그아웃 질문/예/아니요, 778338:27의 귀환 응답을 번역했다.
`roll_gutsman_plugout_ko.json`은 기존 롤4문구를 그대로 이어받는 명시적 개발 입력이다.
원본 nickname/첫줄 쉼표/선택 여백/default No/Navi dispatch/초상/대사 대상/wait/분기는 보존한다.
다른42script는 원본 payload 보존. 넘버맨이나 다른 내비의 대사를 거츠맨 대사로 교체하지 않는다.

## 빌드와 검증 책임

`python -X utf8 tools/build_keyitem_full_rom.py --name <새_이름> --gutsman-plugout`
→ 기존 primary immutable-source 빌더. 이전 patched ROM을 입력으로 쓰지 않는다.
일반 롤 입력과 새 variant는 명시 플래그로 구분한다. 빌더가 롤 부모 입력의 고정 identity와
4개 문구/source/state의 정확한 상속을 검사한다. 일반 재현 결과는 `_repro.gba`와 동일하다.

`tools/run_gutsman_plugout.py`: 동일ROM cold→날짜/프로필→넘버맨→새 native 저장→
checkpoint 없는 cold 이어하기→거츠맨 선택→정상 플러그인→인터넷→R 플러그아웃.
`poc/runtime/gutsman-plugout-v1-*`에 입력/자체 save/화면/메모리/읽기 전용 관찰을 보존한다.
기존ROM의 checkpoint를 새ROM에 가져오거나 nickname/아이템/진행 RAM을 주입하지 않는다.

`report_roll_plugout.main(..., navi='GutsMan')`은 같은 네이티브 UI의 거츠맨7/27 경로를 검사한다.
default No, No 확정, B취소, 재진입, 좌우 Yes/No 전환, Yes 응답, 거츠맨 귀환6663B8:1을
원본 동작과 대조한다. font CPU reads→OBJ VRAM→최종화면, nickname과 텍스트 지움도 확인한다.
최종 결과는 `analysis/gutsman_plugout_v1/plugout_runtime.json`, 합성화면 `plugout_pages.png`가 소유한다.

최종 코드/클론 위치가 이동하므로, 키 아이템 selector를 새 ROM 주소로 CPU624조건 실행했다.
`cpu/report.json`은 bulk-zero helper를 계약으로 대체한 합성 CPU 검사이며 GBA 상점 실행 증거가 아니다.
`audit_gutsman_plugout.py`는 원본·header·append·쓰기 ledger·재현·모든선택입력·기존58archive payload·
롤4문구·한글 glyph/advance table·기존 이미지·전체39 keyitem clone·최종 hook·runtime identity를 검사한다.
폰트/클론의 새 배치는 입력 크기로부터 파생하며, 이전 절대주소와 같아야 한다고 요구하지 않는다.
최종 감사와 현행 도구 snapshot은 `final_identity.json`을 참조한다. 옛 제품의 tool pins를 현행 감사로 쓰지 않는다.
상속/별명/원문/선택패딩·비어 있어야 할 선택행의 합성fixture4개, 기존 keyitem fixture20개를 실행했다.

최종 결과: 위 정상경로/7개선택·응답화면의4문구·CPU font/OBJ VRAM/화면픽셀·지움 PASS.
귀환 응답은 실사용 script27, 귀환은6663B8:1이다. native nickname `ああさま`의 bytes/offset도 보존했다.
`plugout_pages.png`를 직접 확인했다. 감사 PASS, 현행 도구724개 pin. source 원본과 재현본 해시는 각각 위 고정값과 일치한다.

## 이번 정상 경로 조사와 다음 진입점

고정 이전ROM에서도 정상 인터넷 진입을 확인했다:
`keyitem-full-rom-v1-shop-route-prompt`→`shop-route-jackin`→`shop-route-movement`/`shop-route-explore1`.
이는 **상점 입장 증거가 아니다**. 실행 중 R 플러그아웃 거츠맨 원문을 발견해 이번4문구를 처리했다.
source 화면: `keyitem-full-rom-v1-gutsman-plugout-source/step_003.png`.

**다음 즉시 작업점:** 새ROM `gutsman-plugout-v1-choices/checkpoint.mss`는 귀환 후 별도 대화
archive667044/script29의 첫 페이지에 있다. `step_015.png`에서 이를 직접 확인했고 context root=08667044,
script=29를 RAM으로 대조했다. source `667044.tpl`의 literal29:0/1/2는 인터넷/넷배틀과 별개로
플레이어가 어려워하는 교과목을 묻는 거츠맨 문장이다. 다음 페이지와 선택지를 정상 A 입력으로 확인한 뒤
이 관계·nickname·질문응답 흐름에 맞춰 번역한다. 이번 플러그아웃4문구와는 별도 범위이며 미번역으로 남아 있다.

02031000의 다른 공유 메시지 소비자는 정적 코드상 상점이다:
전역 job table 080002E0 +2C →0804C0E1, context0200FCD0;
초기화0804C134→0804C5B4, 원본vendor archive706498 참조와 실제 상품 설명 reader0804CBF8의
LR0804CC31/3F/5D를 연결했다. 정상 인터넷 진입 checkpoint에서 NPC 상점 경로를 계속 찾아야 한다.
709408과709704는 선택 조건이 다르다. 후자는 HP/확장/레귤러UP/서브칩 **이름**을 갖고 있어
같은 script번호라는 이유로709408의 **설명**을 복제하면 안 된다.

catalog732의 현재 미선택일본어27,656 / 기타검토1,859 / parse errors0.
정상 아이템 획득·상점02031000·대체709704, 다른 내비 플러그아웃,
전체 이미지/inline/fixed/휴일·요일/RTC, 한글입력·편집·확정·모든재표시·fresh영구reload·기존save호환,
인간 의미/용어/시각검토는 계속 미완료다. 이번 저장 검증은 일반 native 저장/이어하기에 한정된다.
