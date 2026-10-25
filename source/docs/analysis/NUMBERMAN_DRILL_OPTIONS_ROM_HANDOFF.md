# 넘버맨 레벨 선택·학력 조사 안내10단위 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 롬과 번역 범위

ROM: `poc/output/exe45_ko_development_numberman_drill_options_v3.gba`.
SHA256: `1077e4faf91eb46568a279692c3fbbedc898f594074f5b921dd2f85cae0b5468`.
715064:13:0..4(레벨 안내·레벨1~4),15:0..4(학력 조사 소개3페이지·훈련 시작/설명 듣기) 신규10literal.
‘원하는 레벨을 고르세요’, ‘카운트봄이 내장된 학력 조사 훈련’, ‘편차치가 드러나요’ 등 초안이다. 기존 ‘후후후/가동했군요’와 ‘설명 듣기’를 공유한다. 인간 의미·시각 승인 및 공식 용어 승인은 아니다.

선택 자산 `translations/numberman_drill_options_spaced_ko.json`, scope_variant `numberman-drill-options-spacing-v3`.
715064는42선택 units/40wordings,16script slots 전체 literal 선택. 기존32units/wordings 및 scripts0..12/14 compiled bytes 유지.
누적1,278선택 텍스트/15기존 그래픽/26선택·706미선택 archive. 전체 완역률이 아니다.
715064 source1207bytes SHA `4297ac7f1252f9f20fa471ea886fa76b2c7b9aed4ab01099f790f1ccc4103f67` 유지.
compiled2103bytes, offset0x80A940, pool0x0880A940, roots0DD394/0DD894.
compiledSHA `08e14f6c5764d309281430b7ea83e2e9652c54a5fa3b1d653c3d0c1ec27baf5c`.
이전 rewards-v2의 다른25archive payload hashes/bytes, 저장 제목6333A4의256bytes 동일.
원본의 commands/flags5505·5506/level numbers/option links/default0/disableB/continue targets/keyWait/clearMsg/줄 수 보존. 새 gameplay code hook·이름 입력·save format 변경 없음.

## 커서 겹침과 좁은 여백 예외

v1의 레벨 라벨에서 커서가 한글 ink/shadow를 덮어 strict 검사 실패.
별도 v2 자산은 모든 라벨 앞 literal ASCII 공백1개(8px)를 추가했지만 down-right 포커스 step5에서 왼쪽 ‘레벨3’의 숫자를 여전히 덮었다.
실패 좌표79,126/role3, cursor75,122를 식별했다. 화면의 문자/ROM glyph/OBJ VRAM을 대조한 실패이며 허용 범위를 넓혀 통과시키지 않았다.

v3는 앞 공백1개를 유지하고 왼쪽 열13:1/3 끝에 literal 공백1개를 추가해 열 사이도8px 넓혔다.
빌드 예외는 source-pinned715064:13:1/3 두 ID, 정확히 trailing ASCII1개,16script inventory에만 적용한다. 다른 literal trailing-padding/줄 구조 보호는 계속 엄격하다.
왼쪽 label51px, 오른쪽43px, native space 명령2개 포함 한 줄110px≤176px. 기존 native space 명령과 option cursor 링크는 바뀌지 않는다.
학력 조사 vertical native width9는99px slot, label56+native prefix8px 이내.

TPL leading-space+newline 삼중 따옴표가 canonical dedent에서 여백을 잃는 실패도 발견했다. 명시적 escaped quoted literal로만 직렬화해 leading-space/newline/바이너리 roundtrip을 보존했다.
v1/v2 및 실패 work/상태/캡처는 삭제하거나 덮어쓰지 않았다.

## 실행 증거와 분리

v3 자체 cold→date→profile→navi-menu→select-numberman(right3)→intro→pre→normal.
Prefix `poc/runtime/numberman-drill-options-v3-`.
normal은 일반 controller input만으로 기존 특훈 소개3페이지와 세로 선택지0→1→0을 다시 확인했다. 6채택 pages, 기존5고유 units의 회귀이며 신규10의 정상 진입 증거가 아니다.

신규10은 own-pre(아직687910/script20,715064 init 전)에서 시작한 별도 level/exam 진단으로 확인했다.
native0804FB76가 pool[0]를 읽는 정확한 CPU/register 문맥만13/15 offset으로 한 번 반환한다. 원본 init4FB4C..4FC20 bytes 동일 확인, observer ROM/RAM 직접 write 없음.
init가 먼저 기록한 active requested script0 label을13/15라고 바꾸지 않는다. 실제 target stream/current pointer/font CPU reads/OBJ residency/VRAM/화면을 각각 입증한다.
진단의 `diagnostic_checkpoint.mss`와 `normal_play_checkpoint_eligible=false`를 기록하고 일반 플레이 부모로 사용하지 않는다.

신규10 모두 진단 renderer verified,12채택 pages. 일반 플레이 신규 verified 수0.
레벨 focus:24,108→83,108→83,122→24,122→24,108. 네이티브 애니메이션의 horizontal anchor27/86과0..3px 범위 내이며 캡처별 실제 위치에서 strict ink/shadow 비가림 검사 통과.
학력 조사 focus:58,108→58,122→58,108.
완전한 현재 glyph stream, CPU font24word reads/glyph, ROM glyph→OBJ VRAM→화면 role색, clipped glyph 없음, 번역 영역 vacant-page clearing 통과.
실제 화면 모음 `analysis/numberman_drill_options_v3/diagnostic_options_pages.png`, 근거 `runtime.json`.

### 대기 화살표: 미해결 그래픽 비교

레벨 native OAM205,134; 학력 조사225,141(16px OBJ가 오른쪽 screen edge를 넘어감)은 원문과 같은 배치다.
source-exam3페이지에서 native tile 두 animation phases가 관찰됐다. 후보별 OAM/VRAM1016..1023/palette14를 실제 source phase와 정확히 일치시켰다. 알려지지 않은 tile/palette는 허용하지 않는다.
다만 RAM 일치가 화면 일치와 같지는 않다. 레벨 prompt와 학력 조사1/3페이지의 화살표 영역은 source와53screen pixels 차이, 학력 조사2페이지는0이다. 원인/프레임 시점은 아직 미확인이며 단순 animation으로 결론내리지 않는다.
등록된 화살표 사각형은 glyph footprint와 겹치지 않는 것을 확인한 뒤 텍스트 빈 영역 검사에서만 제외했다. 그 영역을 blank/pixel-identical/그래픽 QA 완료로 인정하지 않는다. 통합 QA·release 완료가 아니다.

## 재현·최종 검증

관련85tests 통과. grid numbers 변경/overwide vertical choice/leading padding 제거/trailing 예외 삭제/다른 literal trailing 공백은 fail-closed 테스트 대상이다.
main/_repro/_current_repro_r3 독립 빌드 동일 SHA 확인 통과. 마지막 suffix는 source-arrow phase 비교 보고서 수정 후 최종466Python tools를 고정한다. tool drift=[]/원본 불변 확인 통과.
`analysis/numberman_drill_options_v3/final_identity_audit.json`의 passed/builds/tool_drift를 최종 근거로 확인한다. 앞선 current_repro/r2도 보존한다.

빌드: `python -X utf8 tools/build_roll_pet.py`에 아래 전체 누적 flags와 fresh `--work`/`--out` 사용.

```text
--roll-intro --roll-fortune-complete --roll-jackin --roll-return
--roll-plugout --roll-subjects --roll-pet-chipquest --roll-mail-alert
--roll-dialogue-chip-name --roll-competition --roll-schedule-time
--roll-schedule-alarm --calendar-types --roll-calendar-date
--calendar-frequency-graphics --calendar-presets-poc --roll-save
--save-labels --save-surface --gutsman-save --numberman-save
--numberman-intro --numberman-pet --numberman-training-intro
--numberman-jackin --numberman-drill-intro --numberman-drill-bubbles
--numberman-training-results --numberman-training-rewards
--numberman-drill-options --numberman-drill-options-padding
--numberman-drill-options-spacing
```

원본8MiB SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변. 이전 후보·실패 자료·test saves 보존. 배포 patch 생성 없음.

## 남은 작업

레벨 실제 호출/학력 조사 flags5505·5506 획득/선택 후 gameplay effect는 미검증. 진단으로 진행 플래그 취득이나 정상 게임 진입을 주장하지 않는다.
기존 작은 말풍선5개 open paths/효과 중 가독성, 미방문 결과·실제 승리/보상 지급 및 다른 미번역이 남는다.
가장 큰 완료 조건인 한글 이름 입력/편집→committed record→모든 재표시 consumer→영구 재로드/기존save호환은 미해결.
전체게임/RTC/오디오/실기/인간 승인/배포 준비를 주장하지 않는다.
한글패치 스킬의 원문 보호, 물리적 커서 점유와 빈 영역 clearing 검사, 정상 실행과 개입 진단 증거 분리 기준을 적용했다.
