# 거츠맨 소지품 안내 — 이어받기

2026-10-09. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 선택 범위

6368E8 반복주기5개의직전판을그대로보존하며665698:10의3문구만추가했다.
`これが`→`이건 `,`の\nしょじひんでガス!\n`→`의\n소지품이거스!\n`,`キーアイテムのかくにん`→`키 아이템 확인`.
단일child `translations/gutsman_calendar_inventory_ko.json`,부모54문구 SHA `b1de499497e670a1862ef8d47c40c7a75e0e27f057c8763ede8555c8860bbb7d` 불변。
누적2,348선택literal/58선택·674원본유지archive,같은archive57문구/226미선택span。
원본SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변。
새ROM `poc/output/exe45_ko_development_gutsman_calendar_inventory_v1.gba`。
SHA256 `2adcc7111363c377628071f9b3ac313ead4615c157a7478f842c316a410a80d1`。
source665698:2077bytes→선택payload2959bytes,relocated root08807E54。기존57archive payload/이미지/‘통신’보존。

## 닉네임 template와 진입 근거

source-pinned literal0→printPlayerNickname(capitalizeFirst=false,capitalizeAll=false,printN=false)→literal1。
원문prefix33+suffix11=44px,번역prefix32+suffix12=44px。suffix만1px늘어나는것을면제하지않고
새 `nickname_aggregate_profiles`로전체template/명령/정확원문·번역·합산44를primary builder에서검사한다。
기존nickname_suffix_scripts=[25] 검사는그대로다。prefix의공백은이exacttemplate만helper가serialize하며
일반literal/choice trailing-space 보호규칙은완화하지않는다。첫행총폭은기존닉네임폭만큼더한동일폭이다。
임의한글입력/이름길이전범위/모든재표시/영구저장/기존save호환을해결했다는뜻이아니다。

source baseline `calendar-frequency-names-v1-inventory-side-probe`의정상select-gutsman→left가진짜소지품10을호출。
actual root08807E54, LR080322BD, native닉네임02010AC0의 `9b9ba5b9e5`/4glyph/44px를관측。
초기원문nickname glyph offsets132,176,220,264,source suffix offset308,첫행총88px。
한개option의nativecursor는OAM1,x44,y136,tile1020,palette14,문자시작x60。
A→빈key-item목록32, B→PET본화면1,재진입10의원경로검증 PASS。채워진key-item/획득경로는미검증。

## 보존된 실패와 검증 상태

`inventory-source-r1`은down2로장비4에진입했으며소지품증거아님。
`inventory-source-r2`는down5로통신7에진입했으며소지품증거아님。둘다정상게임상태그대로보존。
side-probe에서left진입10을확정했고추가left입력은그화면을유지했다。
소지품앞공백을일반replace_literals로넣은초기unit test는보호규칙에의해거부됐다。
exactsource-pinnedtemplate 전용replace를추가했고제어코드/원문·부모drift거부와공백범위검사통과。
관련67tests/679Python AST PASS。자체정상cold→넘버맨저장/이어하기→거츠맨intro/PET→소지품/달력경로완료。
`report_gutsman_calendar_inventory.py` PASS。신규3문구19glyph/2580pixels와native nickname4glyph/528pixels를
입장/재진입양쪽에서CPU/font/OBJ VRAM/실제화면검사했다。prefix32/name44/suffix12=88px,원문과동일。
한개option의실제좌표/커서·A/B분기·닉네임bytes·일정record불변과A뒤원문빈목록화면동일성 PASS。
기존거츠맨intro2/PET8장면22문구/넘버맨귀환3·저장/cold이어하기 회귀 PASS。
같은새ROM에서달력날짜1/종류2/확인24/삭제50 페이지와동적 `1회만`의RAM/CPU/font/VRAM/420pixels 회귀 PASS。
기존전체관리/반복주기5개/격리알림전체runtime를재수행한것은아니다。현재artifact에서확인한범위만계산한다。
첫report는native OAM1커서가있는소지품화면에서nickname검사의cursor_indices를빈집합으로둬거부됐다。
동일화면의body검사와원문OAM이미x44/y136/tile1020/palette14인index1을확인했으므로nickname검사에도1을등록했다。
커서와닉네임행은겹치지않고ink/VRAM/pixel검사나허용오차는완화하지않았다。수정후report PASS,ROM변경없음。
main/repro/current_repro_r3 동일SHA·679tools drift=[]·원본불변 감사 PASS (`final_identity_audit.json`)。
report의native OAM1등록수정을포함한최종tools를r3에서고정했으며ROM은r1/r2와도동일하다。
4장합성 `inventory.png`를직접확인했다。앞뒤거츠맨초상/창과일본어닉네임그대로、선택/취소/재진입정상。
catalog732추출/parse errors0,선택2,348/미선택일본어27,700/기타1,859。665698의미선택일본어literal은0이며,이는해당archive문장만의결과이고전ROM완료분모가아니다。
직후빈key-item의일본어는압축archive709408:32:0,실제root02020800/script32임을확인。
`next_keyitem_empty_draft.json`은source/newline/숫자1/ellipsis를유지한수동초안으로ROM미반영/누적수미포함。
무초상공유메시지이므로거츠맨어미를추가하지않는다。소지품통계title6368E8:80의4고정label과는별도consumer다。
통계label80의별도source관측: fixed call stream088005D6/font08601738/tint4/LR080554BA,
stage0201B800→BG VRAM0600A000,64glyph/4096bytes,observer width16/height16。
prefix64bytes는16cell씩4행이며다음81/82호출은별도mono/숫자폰트다。
이관측만으로height16의전환계산/label별보이는영역/모든consumer를확정하지않으며,다음fixed표시작업에서분리검증할것。
709408 후속source경계: catalog line459/sourceoffset709408,compressed763bytes,size_header=false,
동일압축root034A2C/04C5E8 둘다08709408。decoded1291bytes SHA
`15bbcb0dc3e2fa083d55b00fb4180312836bef14fbd2d9f63e2d82f05760d793`。
source-accept의RAM02020800부터1291bytes전체가decoded source와일치한다。
script32는offset928/27bytes `fc06e702f0000011820b0c1d2bcbe802acbdaf9c8a8a8aedff0000`。
압축품의전체residency를확인했지만길이증가후의destination capacity와두root의consumer범위는아직확정하지않았다。
04C5E8은native Thumb0804C5B4..5E0의또다른decompression 경로에서읽는literal root다。
0804C5D8 r0=r7,0804C5DA destination literal04C5F0=02031000,0804C5DC→080EC158(SWI11/LZ77)이다。
조건에따라04C5EC=08709704의다른archive를선택하므로02020800 UI consumer와같다고가정하면안된다。
034A2C 부근은pointer/data table이며해당bytes를Thumb명령으로직독한값은증거로채택하지않는다。
다음은034A2C table을읽는실제loader/caller와두destination의extent를연결하고,한쪽만검증한상태로두root를이동시키지말것。

## 남은 과제

휴일正月/다른행사이름·날짜/요일이미지·전체이미지/inline/fixed population 미완료。
일정중복25/날짜삭제51 및미관측달력관리branch는static-only。
이전ROM의전체달력/반복주기/격리알림runtime가새ROM에자동이전된것은아니다。
닉네임한글입력·편집→commit→모든redisplay→영구nativefresh reload→기존save호환이계속미해결。
실제RTC/C40producer,기존wait-arrow53pixels/TVtransition1pixel,인간wording/presentation검토도미완료。
전체미번역번역요청은아직완료되지않았다。
