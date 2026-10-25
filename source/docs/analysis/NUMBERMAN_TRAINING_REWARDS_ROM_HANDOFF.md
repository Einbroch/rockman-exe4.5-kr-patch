# 넘버맨 금액·개수 보상 표시6단위 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 최종 롬과 선택 범위

ROM `poc/output/exe45_ko_development_numberman_training_rewards_v2.gba`.
SHA256 `bdabafd336f398e19776df64f778950f8f9517b07e40333ddc4dc05002543e35`.
신규6literal:687910:16:0 /18:0,1 /52:2 /53:2,3. 기존33units/24wordings를 유지하고39units/29wordings로 확대했다. 동일 ‘버그 조각’ prefix wording은 공유한다.
초안은 ‘제니 획득!’, ‘버그 조각’+숫자+‘개 획득!’, ‘제니예요!’, ‘버그 조각’+숫자+‘개예요!’이다. 현 프로젝트의 제니/버그 조각 후보 용어를 재사용하며 공식 용어·인간 승인을 뜻하지 않는다.
source/control/flags/숫자buffer formatting/jumps/keyWait/clearMsg/waitHold·원문 줄 수를 보존한다. 값의 받침에 따라 바뀌는 조사를 사용하지 않는다.

`translations/numberman_training_rewards_ko.json`, scope_variant `numberman-training-rewards-v1`.
primary flag `--numberman-training-rewards`는 기존 results/bubbles 누적 선택을 요구한다.
누적1,268선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률이 아니다.
687910 source1323bytes/65slots/sourceSHA `d49e5b79fc689200d0c605df1503dea33a0c52aaa35105f56b8e14b268da11ac` 불변.
compiled2196bytes /offset0x80778C /pool0x0880778C /root038284.
compiledSHA `dbd237cdbdebcbb519ea52ad15ccb67f9c35557e4ea945a34f57994b8deedbab`.
51미선택 script slots byte-identical. debug0/dispatcher12 error는 일본어 원문 유지. 새 게임 코드 훅·save format·이름 입력 변경 없음.
기존25다른 archive payload hashes/bytes, 저장 제목6333A4의256bytes, 권유10/11/20/21 script bytes 동일.

## 숫자 합성 모델과 빌드 보호

기존 롤 FC032E 기록 결과 모델의 적용 가능성을 타이틀 원본에서 다시 확인했다.
FC030F dispatch 저장0x525C8→0x080363C3(Thumb0x080363C2).
Capstone 원본 disassembly:363C2 result byte read→buffer0;363D0 check;363D6 RNG→363EA halfword table lookup→363EE buffer pointer load→363F0 type write→363F2 amount at+8 write.
363D6..363F4는 기존 FC032E의 동일 shared tail이다. 테이블 포인터363F8의0200FA6C/080362C4/080362D4와 숫자 폰트 폭은 기존 모델에서 해시/값으로 고정한다.
ordinary handler source bytes363C2..363F6 SHA `9debffde3fe946ec3bcb123f3cb24d81d2e6c3c74fa8824bd8a610c407a777bf` 추가 보호.
네이티브 table-generated bonus 값만 제니300/500/400/500/300/200/500/800, 버그 조각3/5/2/1/3/4/4/5이며 숫자당11px다. 모든 임의 printBuffer 사용자의 일반 모델이 아니다.
`tools/numberman_reward_model.py`가 원본 전체 SHA/dispatch/코드/table guards 및4합성 줄 폭을 주 빌드에서 fail-closed 검사한다.

| script | 최대 숫자 | 숫자+번역 줄 폭 |
|---|---:|---:|
|16|800|100px|
|18|5|122px|
|52|800|92px|
|53|5|114px|

normal-dialogue adopted132px/3행 이내. 원문 최대 사용량을 엔진의 보편적 용량으로 일반화하지 않는다.
초안 prefix 끝 공백은 원문 trailing-padding 보호 검사에서 거부됐다. 이를 제거한 별도 초안으로 수정하고 최초 실패 work를 보존했다. 실패 빌드는 롬을 생성하지 않았다.

## 실행 근거와 격리

자체 cold→date→profile→navi-menu→select-numberman(right3)→intro→drill→game→results. Prefix `poc/runtime/numberman-training-rewards-v1-`.
정상 결과는 시간 종료→dispatcher12→실패13 두 문구→PET script1 복귀. 두 실패 문구의 ROM stream/font CPU reads/OBJ OAM·VRAM/화면/빈 영역 clearing 및 관측 native 일본어 이름 prefix 동일 픽셀 검사 통과.
기존 권유20의5페이지와 선택지2literal을 같은 롬에서 회귀 검증했다. 작은 말풍선/lecture 전체의 기존 runtime proof를 이번 롬에 무조건 옮기지 않는다.

4진단 `diagnostic-r2-16/18/52/53`은 같은 롬 own-game checkpoint(결과 root가 새로 로드되기 전)에서 시작한다.
native init0804FB76의 script12 halfword read 위치pool+24만12/50 offset으로 반환한다. global5의080509DA 읽기만2/3, 해당 pool/문맥의 지급·decimal buffer3 읽기만 네이티브 최대800/5로 반환한다.
원본 초기화/분기/지급/숫자 소비 함수 바이트 보호 확인. observer ROM/RAM 직접 write 없음. 단, 원래 지급 명령이 진단 인벤토리를 바꿀 수 있으므로 실제 획득·수량·잔액 검증으로 인정하지 않는다.
모든 진단 checkpoint를 `diagnostic_checkpoint.mss`로 격리하고 `normal_play_checkpoint_eligible=false`를 기록한다. 일반 플레이의 부모로 사용하지 않았다.
첫 diagnostic-16은 initializer가 R1을 script index*2로 바꾸는 것을 관찰 조건에서 누락하여 read counts0/0/0로 실패했다. 원본4FB74 LSL→4FB76 LDRH를 확인하고 R1==24로 관찰 조건만 수정했다. ROM 변경 없이 fresh r2 진단4개가 통과했다. 실패 진단은 보존한다.

신규6개 모두 진단 renderer verified. 기록52/53의 기존 prose4개도 진단에서 확인했다. 정상2와 진단10 고유 units를 구분한다.
formatter value/flags/buffer, RAM digit+1 코드/E5 terminator, 숫자/한글 advance, font CPU reads→OBJ VRAM→화면 픽셀, clipping·빈 영역 잔상 검사 통과. 12개의 채택 snapshot 수는 고유 번역 수가 아니다.
그림 `analysis/numberman_training_rewards_v1/diagnostic_reward_pages.png`는 실제 해당 롬 에뮬레이터 캡처다. 정상 `results_pages.png`, 근거 `runtime.json`/`reward_runtime.json`.

## 재현과 한계

메타데이터 voice를 최신6개 금액 초안까지 명확히 하면서 v1 입력 hash와 불일치가 발견됐다. v1과 기존 manifest를 덮어쓰지 않고 현재 입력으로 v2를 빌드했다. v1/v2 ROM SHA 및 전체bytes 동일을 확인했으므로 위 실행 증거는 동일 product bytes에 해당한다. 파일명의 v1만으로 다른 롬의 증거를 이전한 것이 아니다.
v2 main/_repro/_current_repro_r2 동일 SHA; 마지막 suffix는 진단 관찰 조건 수정 뒤 최종463Python tools를 반영한다. tool drift=[] /관련79tests 통과. `final_identity_audit.json` 확인.
원본8MiB SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변. 원본/이전 후보/실패 work/상태/캡처/test saves 삭제 없음, 배포 patch 생성 없음.

이번6개는 정상 승리·기록 달성·보상 지급 경로 검증이 아니다. 이전 결과17개 중 실패2와 기록 보상 prose4 외 나머지11개는 이번 실행의 결과문구 proof에서 미검증이다.
학력조사/레벨 선택, 기존 작은 말풍선5개 open paths/폭발 중 가독성 및 다른 미번역이 남는다.
가장 큰 완료 조건인 한글 사용자 이름 입력/편집→committed record→모든 재표시 consumer→영구 재로드/기존save호환은 미해결이다.
인간 의미·시각 승인/공식 용어/전체게임/RTC/오디오/실기/배포 준비를 주장하지 않는다.
한글패치 스킬의 원문 보호·숫자 합성 검사·정상과 개입 진단 증거 분리 기준을 적용했다.
