# 넘버맨 계산 훈련 작은 말풍선 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 롬 반영

ROM `poc/output/exe45_ko_development_numberman_drill_bubbles_v1.gba`.
SHA256 `6763f94f40539c1309250416e18f988aeb397788af581cb4862f88a93eced2da`.
추가12literal: 715064 script2..12/14의 작은 진행 말풍선. 기존0/1의20literal을 그대로 유지했다.
누적1,245선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률이 아니다.

원문1207bytes/16slots, 두 root0DD394·0DD894와 source blockSHA256 `4297ac7f1252f9f20fa471ea886fa76b2c7b9aed4ab01099f790f1ccc4103f67` 불변.
새 compiled1919bytes, offset0x80A738, root0x0880A738. 주소·크기는 primary placement에서 계산한다.
`translations/numberman_drill_bubbles_ko.json`은 기존20wordings/units를 그대로 포함한 scope_variant `numberman-drill-bubbles-v1`이며 원문·고유 ID·draft wording을 보존한다.
기존 intro-only variant를 바꾸지 않았다. primary build의 flag `--numberman-drill-bubbles`는 intro/Jack-In/PET 누적 범위 누락을 거부한다.

type2 box0,1 / normal text10,18 / arrow221,141를 그대로 유지한다. 작은 말풍선에만 채택60px/3행을 적용하고 전체 게임의 공통 용량으로 일반화하지 않는다. 현재 최대행폭59px.
모든 commands/args/줄바꿈/빈 마지막 행/waitHold, script2 wait60와11 wait80 보존. 학력조사15와 레벨 선택13은 byte-identical 일본어 원문이다.
첫 빌드는14의 원문3행을2행으로 옮긴 초안을 보호 검사에서 거부했다. ‘이 식으로 / 해도 / 될까요?’3행 초안으로 수정했고 실패 work를 보존했다. 실패 빌드가 ROM을 만들지는 않았다.
새 code hook·save format·이름 입력 변경 없음. 기존25개의 다른 archive payload hashes/bytes 및 저장 제목6333A4의256bytes 동일.
715064의 기존 intro0/lecture1 compiled script bytes도 이전 후보와 동일하다.

## 정상 실행과 검증 범위

직전 intro-v1 롬에서 두 source 조사 실행을 보존했다.
`numberman-drill-level-source-v1`: 짧은 up 입력 뒤에도 아래 선택 포커스가 유지되어 설명1에 들어갔다.
`numberman-drill-level-source-v1-release`: no-input release 뒤10frame up과 확인 입력으로 훈련에 들어갔다.
이는 관측된 입력 차이이며, 짧은 입력 실패 원인이나 모든 입력 장치의 규칙을 확정하지 않는다.
일반 특훈의 ‘훈련 시작’은 테스트 경로에서 source13 레벨 선택 없이 문제에 진입했다.13이 다른 경로에서도 도달 불가능하다는 뜻이 아니다.

새 롬 own-cold→date→profile→navi-menu→select-numberman(right3)→intro→drill→game.
prefix `poc/runtime/numberman-drill-bubbles-v1-`. game-dense/game-early는 같은 새 롬 own-drill에서, game-answer는 같은 새 롬 own-game-early에서 출발한다.
타 ROM checkpoint/RAM/save import나 진행 상태 변경 없음. read-only observer와 정상 controller 입력만 사용했다.
43개의 긴 구간, 마지막100frame, 초기150frame 및9개의 추가 입력 snapshot을 보존했다.

신규12문구 전체의 encoding/font/geometry/controls/roundtrip 정적 검사 통과.
새 롬의 실제 화면 검증을 통과한 신규7문구:2 ‘훈련・・・’,3 ‘쉬워요/정말로’,4 ‘음~’,5 ‘더/힘내요’,8 ‘빠, 빨리/서둘러요!/서둘러요!’,9 ‘시,/시간이/없어요’,12 ‘힘내/주세요!’.
기존 소개0와 선택창 focus도 새 롬에서 회귀 검증했다.126개의 채택된 완성 snapshots에서 ROMstream→font CPU reads→OBJ OAM/VRAM→화면97,380pixels 및 vacant-region clearing 통과.
반복 snapshot 수를 고유 번역 수나 완역률로 사용하지 않는다. 그림 `analysis/numberman_drill_bubbles_v1/bubble_pages.png`; 전체 근거 `runtime.json`.

‘더 힘내요’는 무입력 대기 중에도 정기적으로 표시됐다. 이를 오답 판정 근거로 사용하지 않는다. 추가 A/right 입력으로 선택·문제 표시 변화는 관측했지만 정답/오답 판정·완주·보상은 검증하지 않았다.

## 관측 실패와 보류

완료된 CPU parser stream이 남아 있어도 source2의 timed window는 이미 닫혀 있을 수 있었다. 따라서 작은 text OBJ residency를 별도로 요구한다.
반복 말풍선의 이전 glyph를 현재 instance로 인정하지 않고, 현재 첫 glyph frame 이후의 draw만 완성 후보로 인정한다.
CPU draw+1 및+4 부근에는 전송/화면 반영 중 불일치가 관측됐다. primary ROM과 입력·픽셀 비교 기준은 유지하고, >=6frame가 지난 안정 snapshot만 화면 검증 근거로 채택했다. 이는 실기 latency 상한·원문 대기 연장을 주장하는 규칙이 아니다.
폭발 시 native PPU blendMainControl191/brightness1..16이 실행돼 text 화면과 효과가 섞였다. VRAM 일치나 전체 백색 화면을 읽을 수 있는 한글 표시로 인정하지 않았다.
일반 unflashed PPU mode0 consumer의 proof만 채택하며, 비명10의 효과 중 legibility/원문 비교는 미완료다.175개의 typing/transfer/effect/closed-window snapshots는 PASS로 세지 않았다.
첫 보고서 실패와 보수적 proof scope 변경 이유를 보존한다. 반복 실패를 가리기 위해 게임 문구·대기·코드·상태를 바꾸지 않았다.

화면 검증이 남은 신규5문구는6 다음 문제,7 한 번 더,10 비명,11 칭찬,14 식 확인이다. 이5개는 static-only 개발 입력이며 배포 자격이 없다.
이전 lecture1 전체 traversal은 이번 실행에서 반복하지 않았으며 byte/font/control preservation 정적 검사만 했다.

## 재현과 다음 작업

관련73tests 통과. main/_repro/_current_repro_r3의 동일 ROM hash 및 final tool/source identity는 `final_identity_audit.json`에서 확인한다.
초기 `_current_repro`와 `_current_repro_r2`는 보고서 최종 관측 정책 수정 전 manifest로 보존했다. ROM bytes는 동일하다.
원본·이전 후보·state/capture/test saves와 실패 work를 삭제하지 않았다. 배포 patch를 생성하지 않았다.

다음은 남은5문구의 실제 소비 경로·효과 중 가독성, 학력조사/레벨 선택 및 결과·보상이다.
가장 큰 완료 조건은 한글 사용자 이름 입력/편집→committed record→모든 재표시 consumer와 저장 재로드/기존save호환이며 미해결이다.
공식 용어/인간 의미·표시 승인, 전체게임/RTC/오디오/실기/배포 준비를 주장하지 않는다.
