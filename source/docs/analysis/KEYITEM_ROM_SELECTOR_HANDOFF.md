# 키 아이템 전체 번역의 용량 우회 조사 — 2026-10-09

이 문서는 통합 전 조사 기록이다. 후속 구현·새 ROM·정상 경로와 renderer 진단의 현행 결과는 `KEYITEM_FULL_ROM_HANDOFF.md`를 따른다. 아래 미통합/추가반영0개는 당시 상태를 보존한 것이다.

## 현재 상태

제품 ROM은 여전히 `poc/output/exe45_ko_development_possessions_statistics_v1.gba`, SHA256 `f932c28e3de1459424eee2407be1a75b5bcb3c4ca2f33fe202c7a2a1f8b1c556`이다. 이번 조사로 추가 반영한 번역은 0개이며 누적 2,350 선택 literal이다. 원본·저장·기존 제품을 변경하지 않았다.

39 literal 키 아이템 초안은 2,477바이트라 원본 해제 영역 1,291바이트보다 크다. 현재 제품은 빈 안내 1개와 원본 중복 저장 공유만 적용해 1,273바이트를 사용한다. 나머지 38개는 미반영이다. 초안은 계속 NOT BUILD INPUT / needs_review이며 완성·배포본이 아니다.

## 조사 결과와 선택한 실험

- UI 로더 `080349DC`는 `02020800`, 다른 로더 `0804C5B4`는 `02031000`에 압축을 해제한다. 후자는 조건에 따라 709408 또는 709704를 선택한다. 따라서 두 버퍼를 무조건 늘리거나 모든 조회를 한국어 데이터로 바꾸는 방식은 채택하지 않았다.
- UI의 `08034A30` 리터럴은 압축 해제 목적지와 대사 조회 루트가 공유한다. 이것만 ROM 주소로 바꾸면 ROM에 압축 해제를 시도한다. `02020800`을 참조하는 다른 리터럴에는 그래픽 맵도 있으므로 전체 치환하지 않는다.
- `0804FB4C` 원본 reader 앞에 guarded selector를 두는 **CPU 실험**을 만들었다. 기존 압축 해제/RAM 크기는 그대로 두고 알려진 네 호출 LR·두 RAM 루트·script 0..48·원본 16바이트 헤더가 모두 맞을 때만 별도 ROM의 raw 한국어 archive를 조회한다. 나머지는 원본 경로를 유지한다. 영구 RAM 상태나 추가 압축 해제는 없다.
- `tools/keyitem_rom_selector_probe.py`는 분석용 기계어 생성기일 뿐 primary builder에 연결하지 않았다. `tools/bench_keyitem_rom_selector.py`도 시뮬레이터 메모리만 변경하며 ROM 파일을 출력하지 않는다.

## CPU와 실제 실행 증거의 구분

`keyitem_rom_selector_probe_v1_r2/report.json`: 624 조건 PASS. 49개 script×4 호출 경로=196, 다른 archive=180, 변경 헤더=192, 범위 밖 script=20, 미확인 호출/루트=36. Native reader의 레지스터·flags·context 및 원래 stack/context 외 쓰기 금지를 비교했다. 공유 offset은 다음 strict-greater 경계로 풀어 모든 49개 실제 소비 script 시작을 검사했다. Thumb-1 최종 바이트와 원본 네 BL 호출도 검증했다. 합성 fixture 테스트 6개 PASS.

단, native bulk-zero helper는 216바이트 초기화 계약으로 대체했다. CPU 벤치의 PASS는 GBA의 BIOS·타이밍·렌더링 성공이 아니다. 실험 중 Unicorn의 변경 코드 캐시를 명시적으로 비운 후 비교했으며 제품 ROM을 고쳐 오류를 숨기지 않았다.

`keyitem_selector_readiness_v1/report.json`: 변경하지 않은 최신 제품을 정상 입력으로 소지품 진입→대기→B→재진입했다. 로더/압축 해제/조회 이벤트 각각 2회, 조회는 실제 `r0=02020800, r1=32, LR=0803497F`였다. 세 시점의 RAM 1,273바이트·헤더·script/context 루트가 제품 payload와 일치했다. 캡처 `poc/runtime/keyitem-residency-v1-ui-positive/step_008.png`를 직접 확인했다. **이는 selector 실행 증거가 아니라 원본 경로의 guard 전제 증거다.** 다른 정상 메뉴 탐색에서는 두 번째 소비자를 아직 만나지 못했다. 미관측을 미사용/죽은 코드로 해석하지 않는다.

## 수량 경계

원본 FC03 table `0805258C`의 0x31 handler `08034850` → `080302F8` → `08030314 ldrb`를 확인했다. 결과는 unsigned byte 0..255이며 비활성 분기는 0, word buffer `0200FA6C`에 저장한다. item 매개변수가 8비트라는 이유로 수량 범위를 추정한 것이 아니다. 해당 소스 바이트를 보고서 생성기가 고정 검사한다.

현재 제품 font advance로 초안 script 6/7/16/17/18의 수량 결합행 각각 256개를 검사했다. 최대 폭은 78/146/158/170/78 px이다. 이는 저장 범위와 정적 advance 합계이며 printBuffer 실제 출력·양 메뉴의 renderer 배치 적합성까지 입증하지 않는다.

## 다음 구현 경계

1. 모든 39문구 의미·용어 및 수량 명령/레이아웃을 검토하고 개발용 채택 입력을 분리한다. 이전 초안·벤치 파일은 보존한다.
2. primary immutable-source builder에만 ROM clone/selector를 통합한다. 쓰기 중복·원본 보호·최종 ISA/분기/포인터를 최종 ROM에서 검사하고 결정적 재빌드한다. 수동 ROM 패치는 금지한다.
3. 새 ROM의 실제 native reader/한국어 renderer/수량 0..255 경계 및 양 소비자/대체 archive 회귀를 검사한다. 현재 CPU 결과를 새 ROM runtime PASS로 옮기지 않는다.
4. 전체 미번역과 한글 입력·편집·확정·모든 재표시·영구 reload·기존 save 호환 조건은 계속 미완료로 추적한다.

재현: `python -X utf8 -m unittest discover -s tools -p test_keyitem_rom_selector_probe.py`; CPU 벤치는 `--out`에 새 증거 폴더를 지정한다. readiness 도구는 기존 증거 폴더 덮어쓰기를 거부한다. 제품 빌드의 기존 695개 도구 pin은 해당 역사적 빌드 검증이며, 이번에 추가한 분석 도구까지 포함하는 현재 도구 감사라고 주장하지 않는다.
