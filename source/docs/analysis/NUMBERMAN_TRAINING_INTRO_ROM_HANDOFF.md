# 넘버맨 특훈 권유 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 결과와 범위

실험용 ROM은 `poc/output/exe45_ko_development_numberman_training_intro_v1.gba`.
SHA256 `be556380b60b431af4c38b0beb7b5e22b3113ed167e2b6cd6437d358134effdb`.
추가16개, 누적1,212선택 텍스트 /15기존 그래픽 /24선택·708미선택 archive. 전체 완역률이 아니다.

687910 script10 일반 특훈 권유6단위,11 거절2단위,20 플러그인 전 특훈 권유7단위,21 거절 경고1단위다.
넷 배틀 계산 강조와 특훈 제안, 준비 부족에 대한 불안, 거절 경고를 정중한 넘버맨 말투로 작성했다.
source 선택지 うん/やだ/やだな는 오퍼레이터의 가벼운 응답이므로 ‘응/싫어!/싫은데’로 구분한다.
동일 ‘응’은 공유 wording identity를 참조한다. 신규 말투·의미·용어·표현은 독립 검토/인간 승인 대기 초안이다.
result/reward/debug text와61개 미선택 slots는 원문 그대로 유지한다. 닉네임이나 보상 삽입은 이번 선택 범위에 없다.

## source와 cumulative build

source687910:1323bytes/65slots, root038284(32-bit GBA ROM pointer).
source block SHA256 `d49e5b79fc689200d0c605df1503dea33a0c52aaa35105f56b8e14b268da11ac`.
TPI와 literal baseline의 범위를 primary spec에 등록한다. 정확한16IDs/4scripts를 source ROM에서 재추출해 확인한다.
normal consumer92,110, adopted132px/3rows; 최종 최대 literal 폭125px.
standalone 선택지는 script10의literal4/5, script20의literal5/6이며 prefix24px, 원래 yes뒤2공백/space/option row 구조를 primary build에서 검사한다.
현재 compiled1675bytes, offset0x80778C/root0x0880778C. 모든 기존 commands/args/flags/keyWait/clearMsg/waitHold와 페이지/줄 수, 선택 branch/default, delay 및 미니게임 실행 플래그 불변.
source archive storage와61미선택 script bytes 불변, binary/semantic roundtrip과 전체16normal font coverage 검증.
직전 PET-v1 ROM의23archive payload hashes/bytes와 저장 제목6333A4의256bytes 동일. 이동 위치는 current placement에서 산출한다.
새 code hook/저장 형식/이름 입력 지원 변경은 없다.

builder 기존 누적 flags에 `--numberman-training-intro`를 추가하며 기존 `--numberman-pet` 범위 누락을 거부한다.
immutable source에서 각각 fresh work/out으로 재빌드한다. 이전 후보/원본/모든 캡처·testsave/관측 실패 기록을 보존한다.
최종 재현과 도구 audit은 `analysis/numberman_training_intro_v1/final_identity_audit.json`을 참조한다.

## 실행 경로와 증거

먼저 고정된 PET-v1 ROM에서 `numberman-training-source-survey-v1` 정상 입력으로 PET Jack-In ‘예’→687910 script20을 관측했다.
이는 원본 저장 문구를 포함한 이전 development ROM의 경로 조사이며, 새 ROM runtime으로 전용하지 않는다.

새 ROM prefix `poc/runtime/numberman-training-intro-v1-`:
own cold-part1(state_origin=null)→date→profile→navi-menu→select-numberman(right3회)→intro→entry.
모든 checkpoint parent/receipt/artifacts/ROM/emulator SHA가 같은 새 ROM으로 연결된다. 타 ROM state/RAM/save import나 수정 없음.
entry 관측은 특훈 archive load 전 자체 intro checkpoint에서 시작한다.
step5..9의5권유 페이지, step10의선택지2단위, decline-full step13 경고21의1단위에 실제 소비 증거가 있다.
총8선택 단위/8증거 화면에서 ROM stream→normal glyph→CPU font reads→OBJ VRAM/OAM→화면12,852pixel을 검사한다.
current root/script/parser cursor로 페이지를 구분하고 이전 glyph trace를 다음 페이지 증거로 합산하지 않는다.
현재 glyph rectangle 밖 빈 text영역은 wait arrow와 native choice cursor 영역을 제외하고 배경색과 대조해 page/choice 잔상을 검사한다.
번역 ink/shadow를 cursor가 가리면 실패한다. ‘응’ 기본 cursor(108,108)→‘싫은데’(144,108)의 위치와 두 상태 글꼴을 확인했다.
8화면 묶음과 수락 후 미니게임 화면을 직접 검토했다.

초기 decline은 entry의선택지 checkpoint에서 관측을 시작해서 step1의새glyph draws/font reads가0이었다.
완전한 생산 기록을 요구하는 report가 거부했다. late-observation skill case를 참고하되 이 게임의 기록으로 원인을 확인했다.
ROM은 바꾸지 않고 같은 자체 intro(load 이전)에서 전체15개 정상입력을 새 `decline-full` 경로로 재실행했다.
기존 늦은 캡처를 부모 font 증거로 몰래 대체하거나 missing trace를 면제하지 않았다.

decline-full step12/13은 경고21, step14/15는 기존687E3C script1의 플러그인 구호다.
이는 ‘특훈’ 거절이고 플러그인 자체 취소가 아니다. 초기에 PET 복귀라고 설명했던 추정은 runtime root 관측으로 폐기/정정했다.
플러그인 구호는 현재 source Japanese 그대로이며 번역/표시 검증 대상으로 남는다.
entry checkpoint의‘응’ 수락 side route는 step2/3에서 기존 미니게임 root0x08715064를 선택한다.
미니게임 진입 증거일 뿐 설명 이미지/선택·게임 완료/결과·보상/재진입 검증이 아니다.

현재 ROM 자체 intro의 PET script1/2 glyph/OAM/VRAM/pixel 회귀 검사도 통과했다.
옛 PET의 모든 menu/runtime 판정을 byte identity만으로 새 ROM에 전용하지 않는다.
현재 ROM의 native save 실행은 이번 scope에서 재수행하지 않았다. 이전 ROM의 save 완료는 이전 artifact의 증거로 남긴다.

## 검증과 미완료

`runtime.json`은 scripts20/21의8unit runtime-observed와 scripts10/11의8unit runtime-open을 구분한다.
`training_pages.png`는 실제 실행8화면 묶음이다. 관련68unittest 통과(5.229초); historical fixture는 새 ROM runtime 증거와 구분한다.
첫 _current_repro는 동일 ROM이지만 report의 관측 경로/거절 후 이동 정정 전 tool manifest라 보존만 한다. 최종 audit은 fresh _current_repro_r2를 사용한다.
원본 SHA588a77... 보존과 main/_repro/_current_repro_r2 동일 여부 및 current tools drift는 final_identity_audit.json으로 판정한다.

넘버맨 일반 특훈10/11 runtime, 첫 만남 재선택 숫자 말장난, 플러그인 구호, 미니게임 설명/결과/보상 및 남은 다른 Navi/전체게임 미번역은 미완료다.
최대 완료 위험은 한글 이름 입력/편집/committed record/전체 재표시 소비자와 영구 저장·재로드·기존 save 호환성이다.
RTC/alarm·오디오·실기·독립 의미 검토/인간 승인·배포 미완료. 완역/출시후보로 승격하지 않는다.
