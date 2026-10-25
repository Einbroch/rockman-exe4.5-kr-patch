# 넘버맨 계산 훈련 결과·보상 안내 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 롬 반영

ROM `poc/output/exe45_ko_development_numberman_training_results_v1.gba`.
SHA256 `562bb6ba061bc6eb4d6e3c033b148a84a44095a97db2b749aac197ff99a4da9b`.
실패/칭찬/보상/기록 반응의17literal을 추가했다. 누적1,262선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률이 아니다.

`translations/numberman_training_results_ko.json`은 schema2 / scope_variant `numberman-training-results-prose-v1`이며 기존 권유16units/15wordings를 그대로 유지한다. 새17units/9wordings를 합쳐33units/24wordings이다. 동일 문구는 공유 wording ID를 사용하되 각 원문 위치의 고유 ID를 유지한다.
선택 script10/11/13/14/15/17/20/21/50/51/52/53. 새 flag `--numberman-training-results`는 기존 누적 drill-bubbles 범위가 없으면 거부된다.

원문687910:1323bytes/65slots, source SHA256 `d49e5b79fc689200d0c605df1503dea33a0c52aaa35105f56b8e14b268da11ac`.
Compiled2134bytes, primary offset0x80778C, root038284의 새 pool0x0880778C. Compiled SHA256 `9565aa34ed929c3d0b8dbf46640ff39d98c2330c6da1fe1ce08e01d7ee27f7cf`.
주소·크기는 primary build manifest에서 계산한다.

한글패치 스킬의 원문 보호·재삽입·실행 근거 분리 기준에 따라 commands/args/줄바꿈과 부분선택 외 source 문자열을 그대로 유지했다. normal-dialogue132px/3행 제약 및 전체33units 최대행폭125px 검사 통과.
53개 미선택 script slots는 byte-identical이며 선택된52/53의 금액 접미사도 원문 유지한다.
13:0의 첫 comma는 native nickname 뒤에 이어지는 원문 bytes 그대로다. 이름 입력이나 호칭 변환을 새로 구현하지 않았다.
itemGive33의5/1 수량, checkGiveZenny/checkGiveBugFrags의4294967295와 buffer3 명령을 보존했다. 명령 보존은 실제 보상 지급 검증을 의미하지 않는다.
기존25다른 archive payload hashes/bytes, 저장 제목6333A4의256bytes와 권유10/11/20/21의 compiled script bytes가 이전 후보와 동일하다. 새 code hook/save format 변경 없음.

## 실행 검증

이전 bubbles-v1 롬의 정상 시간 종료 경로를 `poc/runtime/numberman-training-results-source-v1`에 조사·보존했다. 이 state를 새 롬으로 가져오지 않았다.
새 롬 own-cold→date→profile→navi-menu→select-numberman(right3)→intro→drill→game→results. Prefix `poc/runtime/numberman-training-results-v1-`.
모든 checkpoint는 같은 ROM의 직전 receipt에서 생성했다. 정상 controller 입력과 read-only observer만 사용했다. RAM/save 편집이나 타 ROM 상태 import 없음.

실제 source dispatcher12→실패13→PET script1 복귀를 확인했다.
신규13:0 ‘이런 계산도 / 못하시다니・・・’,13:1 ‘앞날이 걱정이에요’의 ROM stream→CPU font reads→OBJ OAM/VRAM→화면 픽셀 및 빈 영역 clearing 검사 통과.
관측된 native Japanese 이름 ‘ああさま’ 영역은 이전 원문 조사 장면과 픽셀이 동일하다. 이 한 이름만의 비교이며 임의 이름/한글 이름 지원을 뜻하지 않는다.
새 롬에서 기존 권유20의5페이지와 선택지2literal도 회귀 검증했다. PET 복귀는 root/script 관측이며 전체 PET 회귀를 다시 수행한 것은 아니다.
화면 `analysis/numberman_training_results_v1/results_pages.png`; 기계 검증 `runtime.json`.

## 재현과 미완료

관련76tests 통과. main/_repro/_current_repro 모두 위 ROM SHA256과 동일하다. 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 유지, 현재458Python 도구 drift=[]; 근거 `final_identity_audit.json`.
원본/이전 후보/실패 work/캡처/test saves를 삭제하지 않았고 배포 patch를 생성하지 않았다.

새17개 중2개 runtime verified, 나머지15개 칭찬·보상·기록 반응은 static-only. 성공 판정, 보상 수량·인벤토리 증감은 미검증이다.
16:0ゼニーゲット!,18:0/1バグのかけら/こゲット!,52:2ゼニーです!,53:2/3バグのかけら/コです!와 debug0/dispatcher12 error는 원문 유지한다.
기존 작은 말풍선5개 open paths/폭발 효과 중 가독성, 학력조사/레벨 선택과 다른 미번역이 남는다. 기존 bubbles/lecture의 전체 runtime proof를 이번 롬에 그대로 귀속하지 않는다.
가장 큰 완료 조건은 한글 사용자 이름 입력/편집→committed record→모든 재표시 consumer→영구 재로드/기존save호환이며 미해결이다.
공식 용어·인간 의미/표시 승인, 전체게임/RTC/오디오/실기/배포 준비를 주장하지 않는다.
