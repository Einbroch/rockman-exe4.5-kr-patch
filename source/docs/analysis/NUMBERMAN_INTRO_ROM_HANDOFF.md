# 넘버맨 첫 만남 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 결과와 범위

`poc/output/exe45_ko_development_numberman_intro_v1.gba`
SHA256 `219e5f7d88841bc19aeab74db7bca9e7aa309bf068e03c045ba2f3769453dceb`.
추가7개, 누적1,152선택 텍스트 /15기존 그래픽 /22선택·710미선택 archive. 전체 완역률이 아니다.
6872B8 script1의7개 literal만 번역한다. 자기소개, 숫자를 좋아하게 만들겠다는 농담, 원주율 계산 제안과 농담 해명, 마무리 인사다.
정중하고 장난스러운 말투 초안이며 이름·의미·표현·시각적 인간 승인/독립 리뷰는 대기 상태다.
script2는 미선택이며 원문을 유지한다. 재선택 조건과 `4649おねがいします` 숫자 말장난의 한국어 처리 방식은 별도 검토가 필요하다.
이 아카이브에는 nickname 삽입이 없으며, 이름 입력을 지원하도록 바꾸지 않았다.

## 소스·빌드 보호

소스313bytes/4slots, root038278(32-bit GBA ROM pointer), source block SHA256 `23b1f0ca50d46b037e10475c4ee7f10e728f3cd59189fd706183afcf48428188`.
`numberman_intro_ko.json`과 primary spec의7literal IDs·단일script1을 사용한다.
원본 archive와 scripts0/2/3, flag3585·window(92,110)·keyWait/clearMsg/waitHold·페이지/줄 수를 보존한다.
adopted normal-font range132px/3행이며 unmapped glyph/overflow/구조 불일치는 primary build가 거부한다. 의미를 자동 줄이거나 페이지를 재설계하지 않는다.
원본에서 기존 누적 flags에 `--numberman-intro`를 추가해 재현한다. 이전 save 범위가 빠지는 사용은 거부한다.
기존21archive payload와6333A4의256-byte 저장 제목이 직전 넘버맨 저장 ROM과 동일하다.
새 코드 hook·저장 포맷 변경이 없다. 모든 원본/이전 후보·캡처·testsave를 보존한다.

## 실제 실행·관측

`numberman-intro-v1-cold-part1 → date → profile → navi-menu → select-numberman → intro → save-enter → save-commit`.
최초 state_origin=null, 동일 새 ROM의 normal right3회 선택이다. 타 ROM state/RAM/save import 없음.
`capture_numberman_intro.py`는 기존 read-only normal renderer observer를6872B8에 한정한다.
최초 select 캡처는 steps2..14였고 마지막7번째 페이지 다음 step15가 누락되어 종료 검사에서 파일 부재로 거부됐다.
같은 ROM의 자체 navi-menu(소개 로드 이전) checkpoint에서 같은16개 정상 입력을 `select-numberman-full`로 다시 실행해 steps1..16을 모두 관측했다.
이 side route도 source navi-menu receipt와 SHA로 검증한다. 기존 state를 수정하거나 post-load state로 이전 로드를 주장하지 않는다.

7개 페이지는 full route steps8..14에 각각 관측했다.
ROM stream→normal BDF glyph→실제 CPU font reads→OBJ VRAM/OAM→화면 역할별 pixel mask를 검사한다.
각 페이지의 current parser cursor를 해당 literal 범위와 대조한다. 이전 페이지의 누적 trace를 다음 페이지의 관측으로 합산하지 않는다.
글자 영역(92..233,110..149)의 현재 glyph rectangle 밖 전체 빈 영역을 검사해 페이지 잔상을 배제한다. 원래 wait arrow 영역은 별도로 제외한다.
페이지 순서와 native script1 entry, 마지막 페이지→step15에서 해당 root를 떠나고 이전 glyph draws/calls가 더 늘지 않는 종료를 확인한다.
`first_meeting.png`의 실제7화면과 저장 완료 step13을 직접 검토했다.
출력된 소개7단위에 대한 증거이며 다른 PET/재선택/모든 Navi/전체게임으로 일반화하지 않는다.

실제 native save: 새 전용64KB allFF SHA71189f... → `7307a117fc08b3b5b6ee1ffe929fe467178eaae37fd57451285cf3d99dc22c17`.
own-save-enter에서 정상 입력으로 callSave를 수행하고 relocated6DA21C script58 완료를 확인했다. 다른 테스트 save 불변.
저장 disk edge/완료 전환이며 영구 재로드·기존save 호환성 증거는 아니다. 덮어쓰기 취소는 이전 ROM에서의 결과와 구분한다.

## 검증 기록과 미완료

`report_numberman_intro.py`의 `runtime.json`과 `first_meeting.png` 참조.
관련64unittest 통과(11.874초). historical fixtures는 새 ROM 실행 증거가 아니다.
main/_repro/최종 _current_repro_r2 동일 SHA,442Python tools drift=[],원본 SHA 보존은 `final_identity_audit.json`으로 검증했다.
_current_repro도 같은 ROM이지만 종료 캡처 경로 수정 이전 tool manifest여서 최종 current audit에서는 _r2를 사용한다. 둘 다 보존한다.
가장 큰 완료 위험은 한글 이름 입력/편집/저장·재표시 소비자 전체와 기존 save 호환성이다.
재선택/남은 PET/다른 Navi 미번역, 전체게임·RTC/alarm·오디오·실기·독립 의미 검토/인간 승인·배포 미완료. 완역/출시후보로 승격하지 않는다.
