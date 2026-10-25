# 키 아이템 전체39문구 ROM 통합 — 2026-10-09

## 결과와 정확한 범위

개발 ROM: `poc/output/exe45_ko_development_keyitem_full_rom_v1.gba`.
SHA256: `4f780b9c7df2e2133e308cdd59821dbcd840936deff17ec168426df61d5fc133`.
새로 선택한 literal38개, 누적2,388개 / 기존59개 archive·673개 원본유지 archive. 키 아이템39개 중 기존 빈 안내1개는 중복 계산하지 않는다. **전체 게임 번역 완료/배포본이 아니다.**

기존39개 작성 초안을 문구 변경 없이 `translations/keyitem_full_rom_ko.json` 개발용 입력으로 명시 채택했다. 기존 `analysis/keyitem_translation_draft_v1/`는 역사적 초안·벤치 증거로 보존하며 자동 빌드 입력이 아니다. 현재 선택 권한은 새 translation asset에 있다. source text·item ID·수량 삽입·줄바꿈·wait·원본 MegaMan mugshot 등 제어코드와 기존 빈 안내 문구는 보존한다. needs_review / NON-DISTRIBUTION / release_eligible=false.

## 빌드 및 저장 설계

primary `build_development_patch.py`가 immutable 원본부터 기존 누적 입력과 새 raw-ROM clone·selector를 한 번에 만든다. `build_keyitem_full_rom.py`는 기존 pinned recipe의 선택 플래그를 연결하는 실행 진입점이다. 이전 patched ROM을 빌드 입력으로 사용하지 않는다.

기존 두 로더/압축 데이터/RAM 버퍼를 그대로 유지한다. 해제 데이터1,273바이트는 원본1,291바이트 영역 이내다. 별도 ROM의2,477바이트 한국어 archive를 추가하고, 알려진4개 호출 LR·두RAM루트·49 script 범위·원본16바이트 header가 모두 맞을 때만 reader의 루트를 바꾼다. 다른709704·미확인 호출·변경 헤더 등은 native reader로 돌아간다. RAM 증설·영구 상태·추가 압축 해제 없음.

`keyitem_rom_selector.py`는 이전 CPU 실험에서 검증한 emitter를 역할 이름으로 채택한 단일 구현이다. 옛 probe 이름은 분석 벤치의 compatibility import일 뿐 다른 코드 생성기가 아니다. 실제 payload 길이를 배치·겹침 검사에 전달하며 예전2,477바이트 결과를 미래 번역 길이 제한으로 고정하지 않는다.

원본추출→native binary roundtrip→literal/control 보존→번역 compile/reverse/rebuild→finite glyph/행·폭→원본 alias/blank→수량0..255 합계→raw clone/후킹 배치→최종 ISA/분기·기계어/쓰기계획을 빌더가 검사한다. 176px은 이번 개발 UI의 채택 표시 범위이며 모든 game renderer의 최대용량이라는 주장이 아니다. 최종 화면에서 최대 수량행170px까지 검사했다.

이전 최신 제품과 공통 길이에서 달라진 바이트는 reader entry의12바이트뿐이고 나머지는 append다. 기존59개 payload·폰트·이미지·‘통신’과 원본 ROM은 그대로다.

## 정적/CPU 증거

`analysis/keyitem_full_rom_v1/static.json`: 39개 literal의 정확한 최종 바이트·Hangul BDF glyph와 native 기호/숫자 glyph, 원본/헤더/append/쓰기 ledger 및 이전 제품 대비 변화 범위 확인.

`cpu/report.json`: **최종 ROM의 실제 clone/hook 주소와 바이트**로624조건 PASS. 49개 script×4 알려진 호출196, 대체 archive180, 변경 header192, 범위 밖 script20, 미확인 호출/루트36. 단 native216바이트 zero-helper는 계약으로 대체한 CPU 벤치다. BIOS·타이밍·렌더링/GBA 성공으로 해석하지 않는다. 관련 controlled fixture20tests PASS.

## 정상 경로 실행

동일ROM 자체 cold→날짜/프로필→넘버맨→native 새 저장→checkpoint 없는 cold 이어하기→넘버맨 귀환→거츠맨 정상 선택을 실행했다. PET8scene22문구/선택·취소·복귀, 거츠맨 소개2page, 넘버맨 귀환3page를 기존 checker로 검증했다. 다른 캐릭터의 대사로 교체한 검사가 아니다.

정상 소지품 진입→빈 아이템→대기→B→재진입: 원래 로더의압축/RAM gate 후 새 ROM root가 context에 들어간 것을 확인했다. 입장·재입장 각각15glyph/2,016pixel의 native CPU font read→OBJ VRAM→화면, B복귀script10 PASS. 대기는 glyph를 새로 그리지 않는 정상 동작이므로 진입 geometry를 재사용해 held font OBJ/pixels만 확인했다. 전체 VRAM은 native 배경 애니메이션 때문에 동일할 필요가 없다.

기존 소지품 통계4제목도 진입/B복귀 각각64cell decode/4,096byte transfer/40visible cell/5,120pixel 및 별도 숫자 영역 불변 PASS. 정상 경로는 `poc/runtime/keyitem-full-rom-v1-*`의 같은ROM ancestry를 검증했다. 기록 `runtime.json`, `selector_runtime.json`, `statistics_runtime.json`; 화면 `selector_normal.png`, `possessions_statistics.png`, `normal_pet_prompts.png`.

## 분리한 렌더러 진단

`poc/runtime/keyitem-full-rom-v1-matrix-r3`: 정상 소지품 checkpoint에서 시작하되, 정확한 native49-offset read의 script32 entry만 각 설명 offset으로 alias했다. 수량은 native printBuffer1 word read `080516C0`/`0200FA6C`를0/255로 alias했다. ROM/RAM/native save를 쓰지 않았다. 모든 read는 PC·주소·루트·context·명령/매개변수 조건을 검사한다. 이 diagnostic checkpoint는 normal-play 불가로 표시하고 별도 이름으로 보존했다.

39개 문구 전부와 5개 수량형 각각0/255, 총39페이지(34script+수량255추가5)를 native renderer로 실행했다. 각 문구 및 삽입 숫자의 정확한 glyph·CPU font read·offset/접미사 합계·OBJ VRAM·화면 픽셀 PASS. `renderer_matrix.json`/`renderer_matrix.png`에 저장했고 합성화면을 직접 확인했다. 원본 지정 MegaMan 초상은 해당 script에만 나타나며 뜻하지 않은 캐릭터/대사 수정은 없다.

이 검사는 **정상 아이템 획득·선택 조건, native 수량 저장/분기, 다른02031000 메뉴 경로를 입증하지 않는다.** CPU의4caller PASS와 합쳐도 두 번째 실제 GBA 소비자 검증을 완료한 것은 아니다.

## 보존한 실패와 재평가

- 첫 matrix는 EWRAM 전체 read callback으로 느려져 지정된 해당 테스트 프로세스만 종료했다. 2/40부분 캡처를 보존했고 PASS로 쓰지 않는다.
- matrix-r2는 캡처40/40을 마쳤지만 새 게임 count gating이 byte load 이전에0을 반환해, 의도한0/255 대체 조건(count_aliases=10)을 충족하지 못했다. 실패 상태와 캡처를 보존했다. 이를 게임/번역 결함으로 오인하지 않았으며 r3에서 원본 printBuffer handler의 정확한 word-read를 조사해 숫자 표시 검사만 분리했다.
- 정상 hold 보고서의 최초 기준은 새draw/전체VRAM동일을 요구했으나 대기에는 새draw가 없고 native 배경은 움직인다. ROM은 바꾸지 않고 font OBJ residency/pixels라는 실제 영향 범위로 관찰 기준을 바로잡았다.

## 재현과 남은 일

빌드: `python -X utf8 tools/build_keyitem_full_rom.py --name <새로운_이름>`.
정상 실행: `python -X utf8 tools/run_keyitem_full_rom.py` (기존 증거/동명 save가 없는 새 실행 이름 필요).
CPU: `python -X utf8 tools/bench_keyitem_rom_selector.py --stem exe45_ko_development_keyitem_full_rom_v1 --integrated --out <새_증거폴더>`.
검증: `tools/report_keyitem_full_rom.py`, `tools/report_keyitem_rom_matrix.py`, `tools/audit_keyitem_full_rom.py`.
최종 재현/도구 pin/보고서 identity 결과는 `final_identity.json`이 소유한다. 이전 역사적 도구 pin을 현재 도구 집합 감사로 쓰지 않는다.

catalog732 기준 미선택일본어27,660 / 기타검토1,859 / parse errors0. 이는 전체ROM text/graphics 완전성 분모가 아니다. 다음에는 두 번째02031000 실제 경로·대체709704 경로와 정상 아이템 획득/선택을 조사하고, 다른 미번역을 계속 처리한다. 전체 한글 입력·편집·확정·모든재표시·fresh 영구reload·기존save호환, 전체 이미지/inline/fixed/휴일·날짜요일/RTC/인간 의미·용어·시각 검토 조건은 계속 미완료다.
