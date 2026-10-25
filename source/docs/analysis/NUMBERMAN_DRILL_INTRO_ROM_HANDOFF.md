# 넘버맨 계산 훈련 소개·설명 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 반영 범위

ROM `poc/output/exe45_ko_development_numberman_drill_intro_v1.gba`.
SHA256 `e89d3e753a87ae0530ffdbed961124c1c90c301c7df6928aac815719a6f2c028`.
추가20literal: 715064 script0 소개3/선택지2, script1 설명13/선택지2.
누적1,233선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률이 아니다.

카운트봄 제한 시간0/40, 오답이면 같은 문제 재도전, 모든 문제를 못 풀면 넘버맨 자신이 폭발에 휘말린다는 내용을 유지했다.
偏差値는 ‘편차치’로 옮긴 개발 초안이다. 카운트봄·편차치·훈련/특훈 및 화법의 공식 용어·인간 의미 승인을 주장하지 않는다.
원문 source text/stable ID/wording selection은 `translations/numberman_drill_intro_ko.json`에 보존했다.

source1207bytes/16slots, roots0DD394·0DD894(32-bit ROM pointers), blockSHA256 `4297ac7f1252f9f20fa471ea886fa76b2c7b9aed4ab01099f790f1ccc4103f67`.
두 root는 같은 relocated block0x880A738(offset0x80A738, compiled1758bytes)를 가리킨다. primary builder가 placement에서 계산하며 원본 source block을 보존한다.
일반 소개0와 설명1만 선택한다. 학력조사 변형15, 작은 진행 말풍선2..12/14, 레벨 선택13 등 나머지14slots는 byte-identical이다.
flags5505/5506, keyWait/clearMsg, 줄바꿈, positionOptionVertical width11/13, option navigation/default/disableB/targets 및 기타 명령 불변.
설명 끝의 원문 targets는 모두 continue다. 임의로 ‘다시 설명’ 분기를 추가하거나 원래 동작을 추정해 수정하지 않았다.

원문 실제 bottom consumer는 origin52,110, normal glyph12px/row14px이다. 채택176px/3행은 확정된 전체 게임 공통 최대가 아니다. 현재 최대행폭134px.
세로 선택지의 source nominal width11/13과 선행 space를 유지하며 primary build가 label extent/trailing row boundary를 검사한다.
새 code hook·이름 입력·save format 변경 없음. 이전25archive payload bytes/hashes와 저장 제목6333A4의256bytes 동일.
이전 cumulative flags에 `--numberman-drill-intro`를 추가한다. 누락된 기존 Jack-In 범위를 거부하고 불변 source에서 누적 빌드한다.

## 실행 근거

기존 Jack-In-v1 ROM의 own-intro checkpoint에서 read-only source survey `numberman-drill-source-v1`/`numberman-drill-source-v1-options`를 수행했다.
이 조사는 원문 geometry/context 근거이며 새 ROM 화면 검증으로 전용하지 않는다.

새 롬 prefix `poc/runtime/numberman-drill-intro-v1-`.
own-cold→date→profile→navi-menu→select-numberman(right3회)→intro→drill→lecture.
타 ROM state/RAM/save import나 진행 상태 강제 변경 없이 정상 controller 입력으로 접근했다.
훈련 권유20 수락→소개0→아래 ‘설명 듣기’ 선택→설명1의13페이지→마지막2선택지와 포커스 이동을 관측했다.
20개의 완성 screen snapshots(선택지 포커스 비교 포함)에서 신규20literal 전부의 정확한 ROMstream→normal font CPU reads→OAM/OBJ VRAM→화면43,140pixels 및 vacant page clearing 검사가 통과했다.
선택지 커서는 첫 메뉴47,108→47,122, 마지막 메뉴36,108→36,122. 번역 잉크 가림 없음.
같은 새 롬 PET script1/2의 기존 문구·선택창 픽셀 회귀도 통과했다.
한글 전체 glyph supply 및14unselected slots, source/controls/semantic/binary roundtrip/두 root relocation 정적 검증 통과.
화면은 `analysis/numberman_drill_intro_v1/drill_pages.png`, 상세 receipt는 `runtime.json`.

첫 보고서 실행은 ‘script1에 외부 root-entry0804F7B6 call이 있어야 한다’는 검증 가정 때문에 실패했다. 실제 select 내부 jump는 이 외부 함수 호출을 하지 않는다.
전체 신규 glyph/pixel 검사는 이미 통과했고, parent의 source0 선택 상태→같은 root의 child1→신규 glyph stream을 직접 검사하도록 관측 모델을 수정했다.
게임 patch/문구/입력 경로/픽셀 통과 기준은 바꾸지 않았다. 기존 실패와 수정 이유를 보존한다.

관련72tests 통과. main/_repro/_current_repro_r2가 동일 ROM hash이며 final_identity_audit.json은 최종 Python tool inputs와 source identity를 검증한다.
최초 `_current_repro`는 보고서 관측 가정 수정 이전의 tool manifest로 보존했다. ROM bytes는 동일하다.
원본·이전 후보·test saves·state·실패 기록을 삭제하지 않았다. 배포 patch를 생성하지 않았다.

## 남은 작업과 주장 한계

학력조사 소개, 레벨 선택, 작은 진행 말풍선, 결과·보상과 다른 미번역은 남아 있다.
소개 메뉴의 ‘훈련 시작’ 확정, 설명 끝 두 항목의 이후 동작/반복 설명, 완주·실패·보상 및 gameplay persistence는 이번 실행 범위 밖이다.
가장 큰 완료 조건은 한글 사용자 이름 입력/편집→committed record→모든 재표시 consumer와 저장 재로드/기존save 호환성이다. 아직 미해결이며 이번 문구 반영으로 해결되지 않았다.
전체게임/RTC/오디오/실기/인간 의미·표시 승인/배포 준비를 주장하지 않는다.
