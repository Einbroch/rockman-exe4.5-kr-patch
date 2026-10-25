# 021: 실제020 기준 신규500개 ROM 반영·검증

부모 검증 기준은020 `poc/output/pending500_020_v1.gba`, SHA256 `1e595b2113e446fa74be2c2e0c7737a0bf13bcbd7984114eb1c1df79b4580788`,11,122units/404primary/328untouched다. 021 제품 빌드·독립 재현·아래 한정 범위의 실행 검증을 완료했다. 새BPS/xdelta/ZIP금지,원본/020/이전제품·세이브·증거보존.

## 동결 입력과 검증

`pending_insertion_500_021_survey_v1/survey.json`:actual020/source/TPI/고정draft-first corpus 재대조,고정초안변경0. `fullbox_layout.py`는180/180/168범위에서기존공백↔LF 위치만조정한다. 동일한flat문구·LF수·source leading/trailingLF/padding보존이며prose치환/페이지추가없다. 기존strictfullbox+layout후보390개로500미달. 첫 `...021_fullbox_survey_v1`과selector실패를보존했다.

`fullbox_capacity.py`에 명시적 profile의 `entry_guards`/`portrait_changes`를 추가했다. 기본020 profile은 기존 단일 portrait/즉시 initializer 조건을 그대로 적용한다. 새 profile에서만 source 선행 checkFlag/checkFlagNavi/checkItem/checkGlobal/flagSet/flagClear/flagSetNavi/flagClearNavi/storeGlobal16의 정확한 command 순서와 반복 portrait를 명시한다. 원본 TPL의 mugshotShow→msgOpen을 필수로 유지하며 position/quick/variable/choice/mugshotHide는 금지한다. msgOpen 1개, 페이지당 literal 1개, clear/exactIDs/행 폭 제한도 유지한다. storeGlobal16은 고정 TextPet `mmbn45-jp.ini`의 F802/global8bit/value16bit 정의와 원본 명령을 확인했다. 원본 선행 flag/global 쓰기와 분기를 삭제·수정·미리 주입하지 않는다. 새로운 자연 조건·이벤트/flag 경로의 실행 증거는 별도로 필요하다.

`...021_fullbox_survey_v2/survey.json`667조건후보에서 `...021_selection_v1/selection.json`20archive/109script/정확500개를고정했다. 선행guard48script·portrait변경40script(중복가능),별도새archive0. `translations/pending_insertion_500_021_layout_v1.json`21개동일문구placement가권위다. selector의prose_changed=false와needs_review/NON-DISTRIBUTION유지.500개전부현재020미적용ID다.

`prepare_pending500_021.py`→`...021_preflight_v1/preflight.json`500source-onlycompile/원본·한국어semantic/binaryroundtrip/보호control/unselectedscripts/geometry PASS. `cumulative_batch500_021.py`→`...021_cumulative_v1/preflight.json`20carry/new0에서parent를020소비계약으로재컴파일해actualpayload동일재현,비신규script/oldmetrics/consumer보존 PASS. 기존literal_profiles의max132/180은변경하지않고새script profile만추가했다. 새fullboxprofile은parent재compile시제외한다.

16fixture PASS(기존8+layout8):sameflat/LF/row수/불가wordwrap/guard정확순서/position거부·portrait 변경 명시 필수·페이지 clear 필수. 첫reflowfixture는테스트입력의총길이가두행에들어갈수없는데수용을기대해서실패했다. 세번째단어5→4음절의유효fixture로수정후통과,제품/폭gate는완화하지않았다.

## 빌드/다음 단계

PROFILE021/primaryrecipe/rollbuilder/primarybuilder에021flag와020prerequisite를연결했다. `build_keyitem_full_rom.py --name pending500_021_v1`+기존전체020flags+`--pending-batch500-021` 원본 기반 빌드 완료. 결과 `poc/output/pending500_021_v1.gba`, SHA256 `76d9cf6626436f4c683a49f9389f72c3c85b01b6d6b43461a466e32976ec7ac4`,11,964,256bytes, 누적11,622units/404primary/328untouched다. `analysis/pending500_021_v1/lineage.json` 실제 신규500개/기존 보존 PASS, `selector_cpu.json` 합성CPU3,195조건 PASS. 독립 재현 `pending500_021_v1_repro.gba`와 전체 바이트 동일하다.

다음은 actual021 lineage/delta/proof/argumenthash·독립 재현 순차 빌드·selector CPU·같은 ROM 부팅/native 자판3페이지/profile/네 내비/첫메일23쪽 회귀 검사다. `capture_cumulative500_021_display.py`:guarded7C0F8C:13(원래storeGlobal16/flag2개와portrait변경3쪽),reflow768800:10(6쪽,21placement중하나),break76C944:137(1쪽)을새021completecheckpoint에서읽기alias진단한다. `verify_cumulative500_021_displays.py`는10쪽의actualCPUfont/geometry/ROMglyph/OBJ→pixels/keyWait/잔상검사를예정한다. read-alias state는격리하며자연NPC/전투/획득·flag조건/소울기능실행증거로세지않는다. 다른ROMstate이식금지,이전action문자열만재사용가능.

자동한글조합/commit/save/redisplay,전체원문맥·의미·자연스러움humanreview,500개전체자연route는미완료다. 새source prelude/portrait계약은 아래 제품 실행 표본까지만 검증한 개발 범위이며 release_eligible=false.

## 화면 검사 중간 결과

`analysis/pending500_021_v1/fullbox_runtime.json` 10쪽 PASS. 각 글자의 실제 CPU 문맥 `0x0200FA20`, 스트림/글리프/위치, ROM 글꼴 읽기, OBJ와 화면 픽셀, 원래 E600 keyWait, 다음 페이지의 빈 영역 잔상 제거를 대조했다. `fullbox_pages_v1.png` 10쪽 비교표와 break 원본 화면을 직접 열어 확인했다. 화자 변경 3쪽/소울 설명 6쪽/긴 문장 재배치 1쪽의 읽기 별칭 진단이며 자연 사건·획득·플래그 조건이나 소울 기능의 검증이 아니다. 모두 같은021 정상 초기설정 checkpoint에서 파생했으며 진단 checkpoint는 격리했다.

첫 화면 검사는 검사기의 잘못된 `0x0210FA20` 비교 상수 때문에 실패했다. 모든 관측 draw가 기존 source/context reset과 같은 `0x0200FA20`이고 예상 offset·glyph와 일치함을 확인했다. 020 검사기와 차이를 대조해021 복제 시 상수 오타임을 확인하고 검사기만 수정했다. ROM/캡처/폭 기준은 바꾸지 않았다. 수정 뒤 전체10쪽 검사가 통과했으며 실패를 통과로 은폐하지 않는다.

초기설정/자판3페이지/프로필/네 내비/첫메일/복귀·재열기의 정상 조작5구간 80캡처가 완료됐다. `normal_runtime.json` 정상 경로의 자판3페이지 VRAM/맵·21개 이름 bank 상주/선택 가능한 네 내비 OAM·첫메일23쪽 순서/keyWait/3개 native archive 로드·재열기 PASS. `startup_pages_v1.png`와 `mail_visual_pages_v1.png`를 직접 확인했다. 최종 보고서에 묶인 `first_mail_pages_v1.png`도 직접 열었으며 사전 확인한23쪽(step10..32) 비교표와 파일 바이트까지 동일하다. 기존 일본어 자판/이름 입력 경로의 회귀이며 한글 자동 조합이나 한글 저장 성공 증거가 아니다.

`visual_review.json`에 초기 구매 안내의 좁은 행간/빽빽한 문구를 OPEN_INHERITED로 기록했다. 020과021의 step009 글자 영역[48,52,192,112]은 RGB 픽셀 동일하고, 전체 차이는 애니메이션 화살표[205,118,216,133]뿐이다. welcome 두 payload 해시도 동일하다. 해당 화면 바이트 상주/회귀 통과를 시각적 품질 승인으로 오인하지 않는다. 가독성 재배치는 후속 보완 대상이다.

## 최종 감사와 다음 재개

`integration.json` PASS: 실제500개 delta/기존 ID 누락0·parent 및 비신규 script/consumer/source storage 보존·최종 포인터/Expected Writes/header/ISA·인자 파일 해시와 독립 재빌드 일치를 확인했다. normal/fullbox/CPU 보고서는 모두 같은021 SHA256에 묶였다. 촬영한10쪽의 일본어 원문도 대조했지만 고정 초안의 needs_review 상태와 전체 사람 검수 미완료는 유지한다. 전체 layout-ID 수와 manifest translated_units는 서로 다른 모집단이므로 같은 총수로 주장하지 않는다.

원본/020/기존 ZIP의 SHA256이 각각 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` / `1e595b2113e446fa74be2c2e0c7737a0bf13bcbd7984114eb1c1df79b4580788` / `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6`로 유지됨을 최종 재확인했다. 새 배포 패키지와 삭제 없음.

다음 재개는 실제021 ROM과 `integration.json`을 기준으로 잔여 미적용을 다시 조사한다. 이미 적용한 ID를 중복500개로 세지 않는다. 초기 구매 안내 행간, 자동 한글 조합/commit/save/redisplay, 아직 일본어인 별도 UI·이미지/소비 경로, 자연 사건·분기/획득·전체 의미 검토는 남았다. 새 선행 guard의 자연 조건이나 전체500개 자연 실행을 이번 진단으로 대체하지 않는다. NON-DISTRIBUTION이며 패치 파일은 사용자 재요청 전 만들지 않는다.
