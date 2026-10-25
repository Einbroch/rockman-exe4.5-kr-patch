# 넘버맨 재선택 인사5단위 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 후보 롬과 번역

ROM `poc/output/exe45_ko_development_numberman_return_v1.gba`.
SHA256 `f0c33a99ada35c0575a40a72727bbd894633c2b59b21ae67fb6156d16caa152e`.
신규6872B8:2:0..4, 기존 첫 만남7units 그대로 유지. 총12units.
초안: ‘어라라라~!!’, ‘또 제 차례가/돌아왔군요!?’, ‘울먹울먹~!!/외로웠어요!!’, ‘1명뿐이라 외로워서/계속 수를/세고 있었어요~’, ‘다시 한번/잘 부탁드려요’.
원문source/IDs/flag3585/window92,110/arrow225,141/keyWait/clearMsg/waitHold/줄 수 보존. 2:3의1명 숫자 보존을 빌드에서 검사한다.

4649는 마지막 인사의 숫자 말장난이다. 사용자에게 ‘자연스러운 한국어 인사’와 ‘숫자+뜻 유지’를 제시했다. 사용자가 “‘잘 부탁드려요’로 자연스럽게 번역”을 선택했다.
decision `numberman-return-4649-natural-ko-20261005`는2:4의 의미상 인사 적응만 승인한다. source에는4649를 그대로 보존하고 target에서만 ‘잘 부탁드려요’로 선택했다. 실제 게임 숫자/보상/명령 변경이 아니다.
다른 문구의 인간 의미·시각 승인, 전체 배포 승인을 뜻하지 않는다. primary build는 이 좁은 decision/approved/scope/선택 wording이 없거나 바뀌면 거부한다.

자산 `translations/numberman_return_ko.json`, variant `numberman-return-prose-v1`, flag `--numberman-return`(기존 `--numberman-intro` 필요).
누적1,283선택 텍스트/15기존 그래픽/26선택·706미선택 archive. 전체 완역률 아님.
6872B8 source313bytes/4slots SHA `23b1f0ca50d46b037e10475c4ee7f10e728f3cd59189fd706183afcf48428188` 유지.
compiled680bytes, offset0x806E38/pool0x08806E38/root038278.
compiledSHA `058adb64012c0ee065c6908e655abb56fc363f42957fa2f6382d93d811abe61f`.
첫 만남 script1 전체 compiled bytes와 다른25archive payload hash/bytes, 저장 제목6333A4의256bytes 동일.
빈 script0/3 유지. 새로운 게임 코드 훅·이름 입력·save format 변경 없음.

## 일반 실행과 진단의 구분

자체 cold→date→profile→navi-menu→select-numberman→intro.
Prefix `poc/runtime/numberman-return-v1-`.
별도 normal-full은 자체 navi-menu checkpoint에서 일반 controller input만 사용했다.
기존 첫 만남7페이지(steps8..14)의 current stream/font CPU reads/ROM glyph→OBJ VRAM→screen pixels/빈 영역 clearing/step15 종료 검증 통과.

신규 return5는 같은 자체 navi-menu, 아직6872B8 init 전에 시작한 diagnostic-return에서 확인했다.
native0804FB76의 pool+2 halfword read가 실제 script1(R1==2)/R0pool/R5==0200FA20 문맥일 때만 script2 offset을 한 번 반환한다.
source init4FB4C..4FC20 bytes 동일 및 원본 전체 SHA 확인. observer ROM/RAM 직접 write 없음. 요청 script1 label은 그대로 남는다.
정확한 target2 current stream/CPU font reads/OBJ residency/VRAM/screen 및 페이지 순서8..12, step13 종료를 각각 검증했다. 모든5개 진단 renderer verified, 정상 신규 verified 수0.
진단 checkpoint는 `diagnostic_checkpoint.mss`, `normal_play_checkpoint_eligible=false`; 일반 경로 부모로 사용하지 않았다.
화면 `analysis/numberman_return_v1/return_pages.png`, 근거 `runtime.json`.

첫 clearing 검사 실패는 blank range를236까지 확장하면서 원래 box 오른쪽 border234/235를 텍스트 잔상으로 센 것이었다.
정확한 실패 좌표234,110..115/color66,113,86를 확인했다. 기존 인증된 같은 native window capture와 columns234/235,y110..139 픽셀 동일을 요구하고, 기존 확인된 inner blank range92..233으로 검사했다.
font ink/VRAM 검사 자체는 완화하지 않았다. 동일 border 및 모든 페이지 vacant pixels 검사가 통과했다.
native arrow225,141 영역과 glyph footprint 비겹침 확인; 해당 화살표만 blank 검사에서 제외한다.
이전 레벨/학력 조사 화살표의53screen pixels 차이는 여전히 미해결이다. 이번 검사는 화살표 그래픽 QA 완료가 아니다.

## 정상 저장·재부팅 경로 시도

저장 후 이어하기의 내비 재선택 후보는 웹 검색 및 기존 정상 저장 레시피로 좁혔다. [게임 소개 후보](https://w.atwiki.jp/gcmatome/pages/6212.html)는 진입 가설일 뿐 ROM 실행 증거를 대신하지 않는다. Nintendo 설명서 PDF 직접 fetch는 timeout으로 내용을 확인하지 못했다.

같은 ROM own-intro→save-enter→save-commit, observer-only/current native commands 사용.
격리 폴더 `poc/runtime/chip-matrix-saves`의 이 후보 전용65536bytes sav만 새 게임 FF 상태에서 정상 저장했다.
beforeSHA `71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063`.
afterSHA `1ae6ce9b872417f7ba3db659d4a0ab5a65bda421525a5d0615df47a6bee97708`.
step13 native save success58/root현재6DA21C 및 디스크 snapshot hash 확인.

normal-reload-menu는 checkpoint 없이 cold boot. 이후 normal-reload-navi→normal-reload-select→normal-return은 해당 cold 부모만 사용했다.
각 단계의 saved-file before/after hash는 위 정상 commit과 동일하고 다른 테스트 sav 변화 없음. RTC만 허용 목록으로 구분했다.
초기 START 입력은 title 준비 전에 들어가 메뉴에 진입하지 않았다. title 준비를 실제 capture로 확인한 후 START→이어하기를 눌렀다. 이전 survey도 보존한다.
내비 재선택 화면에서 이전 넘버맨 포커스와 선택 확인을 실제로 관측했다.
이어 native68BBB4/script1 새해 인사3페이지가 보였고 PET로 복귀했다. 대상6872B8/script2 완성 페이지는 이 정상 시도에서 관측되지 않았다.
새해 이벤트가 실제 return2 호출을 막았다고 인과적으로 확정하지 않는다. 같은 내비/다른 내비 변경·이벤트 우선순위 등은 미확인이다. 이 코드를 unreachable로 판단하지 않는다.
정상 native 저장·cold 이어하기의 파일 동일성만 확인한 것이며 한글 이름/기존save 호환/모든 소비자 persistence 검증이 아니다.

## 재현과 남은 조건

관련88tests 통과. source/control/기존7unit lineage,1명 numeral 변경 거부, wordplay 승인 누락 거부 검사 포함.
마지막 보고서 수정 직전 current_repro_r2는 report_numberman_return.py 한 파일 tool drift로 최종 audit 실패했다. 이전 ROM bytes는 동일하지만 그 audit 실패를 통과로 바꾸지 않았다.
현재 코드 고정 뒤 fresh current_repro_r3를 빌드했다. 최종 main/_repro/_current_repro_r3 동일 hash/470Python tools drift=[]/원본 불변 검증이 통과했다. `analysis/numberman_return_v1/final_identity_audit.json`에 passed 결과를 기록했다.
이전 handoff 전체 누적 build flags에 `--numberman-return`만 추가하고 immutable 원본에서 fresh work/out으로 빌드한다.
원본8MiB SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변. 원본/이전 후보/실패 상태/캡처/test saves 삭제 없음, 배포 patch 없음.

새해 인사/메뉴 일부/다른 미번역, 기존 작은 말풍선5개 open paths·효과 중 가독성, 미방문 결과 및 실제 보상 경로가 남는다.
한글 사용자 이름 입력/편집→committed record→모든 재표시 consumer→영구 재로드/기존save 호환은 가장 큰 미해결 완료 조건이다.
RTC 날짜 정확성/오디오/실기/전체게임/인간 승인/배포 준비를 주장하지 않는다.
한글패치 스킬의 원문/숫자 보호·사용자 의미 선택 기록·물리적 글자/빈 영역 검사와 정상/진단 증거 분리 기준을 적용했다.
