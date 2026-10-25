# 압축 진행 힌트: RAM 비확장 ROM reader CPU PoC

후속 제품 상태(2026-10-15): 이 문서는 아래 CPU-only 당시의 설계·실험 기록이다. reader를 `hint_rom_selector.py`로 승격하고022 제품 builder에 합성했으며 `pending500_022_v2.gba`의 신규500개/누적12,122개·독립 재빌드·실제 배치 CPU 및 대표 loader/reader/font/OBJ/화면·닫기/재진입 검증을 마쳤다. 현재 권위는 `PENDING_INSERTION_500_022_HANDOFF.md` 최상단과 `pending500_022_v2/batch_status.json`이다. 아래021/미반영/아직 미통합 문구는 과거 단계이며 새 결과를 무효화하거나 CPU-only 증거를 소급해서 runtime 통과로 바꾸지 않는다. 소스/기계어 proof 안에 보존한 analysis_only/runtime_tested 표시는 그 component proof의 범위이며, 제품 설치·런타임 결과는 별도의 해시 고정022 보고서로 판단한다. NON-DISTRIBUTION, 자연 A3 이벤트·모든 내비/분기·한글 자동 조합/저장·전체 UI/사람 검수와 배포 승인은 여전히 미완료다.

## 현재 상태와 기준

제품 ROM은 여전히021, `poc/output/pending500_021_v1.gba`, SHA256 `76d9cf6626436f4c683a49f9389f72c3c85b01b6d6b43461a466e32976ec7ac4`, 누적11,622개다. 022의500개는 소스 전용 검증 상태이며 아직 ROM 반영0개다. 이번에는 RAM 비확장 reader의 분석용 구현과 CPU 실험을 완료했다. GBA/ROM 통합/화면·성능 검증이나 패치 파일을 만들지 않았다.

선행 자료는 `PENDING_INSERTION_500_022_HANDOFF.md` 및 `pending_insertion_500_022_storage_v1/storage.json`이다. 압축19개/364개의 후보가 decoded2574~2823bytes로 증가하지만 RAM0x0203D800의 소유 범위·수명은 미확정이다. raw136개만 따로 반영하고500개 완료로 세지 않는다.

## 선택지와 사전 기준

- 단순 RAM 확장: buffer 끝/동시 사용자의 증거가 없어 채택하지 않는다.
- 문구 축약: RAM 바이트 예산을 맞추기 위한 의미·문체 손실이나 임의 자동 축약을 하지 않는다.
- 개발 후보: 원래 압축 데이터·로더·RAM extent는 그대로 두고, 정확한 원본이 상주한 경우에만 번역 ROM clone을 선택한다. 추가 persistent RAM은 없으나 코드·32byte stack·소비 경로·실행 시간의 검증이 필요하다.

CPU 실험의 사전 통과 조건은 원래 caller/root/scene/Navi/script 및 전체 원본 바이트가 일치할 때만 clone을 선택하고, 나머지는 기존021 selector chain의 레지스터·문맥·최종 flags와 같아야 한다는 것이다. 데이터·문맥 바깥 쓰기 또는 기존 mail/keyitem 변화는 실패다. CPU 통과는 후속 원본 기반 PoC/제품 빌드와 GBA 소비 검증을 허용하는 근거일 뿐 런타임 통과나 배포 승인이 아니다.

## 구현과 확인한 사실

`tools/hint_rom_selector_poc.py`의 wrapper는 기존0x0804FB4C install stub의 saved r3 계약을 받아 원상 복원하고, 기존 selector entry로 다시 전달한다. 기존 기계어 재생·native 초기화는 바꾸지 않는다.

- source0x0804F802의 BL은0x0804FB4C를 호출하며 실제 caller LR은 **0x0804F807**이다. 함수 시작0x0804F7FC와 LR을 혼동하지 않는다. 원본 명령을 독립 disassembly로 검사했다.
- native Navi getter0x08000CEC의 source bytes를 확인했다. r10+0x40 context의+1이 Navi ID이고, 같은 context의+4 scene major가0xA3인 경우만 후보로 처리한다.
- root0x0203D800, script0..254, Navi0..22를 검사하고 고정23slot descriptor를 조회한다. 미선정 slot은0이며 기존 처리로 돌아간다. 선정19개는 source pointer slot0x54180 기준 인덱스와 원본 payload에 묶었다.
- 첫16byte는19개 원본에서 모두 같아 식별자로 사용할 수 없다. 32byte prefix로도 결론 내리지 않고, 해당 Navi의 **원본 payload 전체 바이트**를 RAM과 직접 비교한다. 일치하면 번역 clone root만 바꾼다. 원본 압축 데이터/테이블/압축 해제 크기/내용은 그대로 유지하는 설계다.
- r0..r7을32byte stack에 보존한다. 일치 시 saved r0만 clone으로 바꾸고 모든 레지스터를 복원한다. LR/r10/고위 레지스터는 변경하지 않는다. native continuation 이후의 flags·문맥을 조합 실험으로 대조했다. stack32byte는 persistent RAM0byte와 별도다.
- `assemble_verified`의 기존 ARM7TDMI ARMv4T Thumb-1 경로로 생성·역어셈블·재어셈블 및 분기/리터럴 최종 위치를 검사했다. 실험 배치는0x09000000 영역의 CPU 메모리이며 제품 ROM 주소나 신규 Expected Write로 채택하지 않았다.

## CPU 결과

`tools/bench_hint_rom_selector_poc.py` → `analysis/pending_insertion_500_022_selector_poc_v1/cpu.json` PASS, 총5,652조건:

- 선정19개 × script0..254 =4,845개 선택 조건
- 각 원본의 시작/헤더 중간/본문 중간/마지막 바이트 변경 시 거부133개
- 잘못된 scene114개, 다른 Navi418개, 범위 밖 script57개, 잘못된 caller57개, 다른 root19개
- 기존 keyitem 두 root 및 mail root의 대표 처리9개 유지

각 조건에서 기존021 실행과 wrapper 조합 실행을 실제 Unicorn CPU로 대조했다. clone 선택 시 table offset 및 context root/stream/bookmark만 예상 값으로 달라지고, 다른 레지스터/최종 flags/문맥은 같다. 쓰기는 기존 native216byte 문맥 및 stack 범위만 허용했고, 원본 text RAM과 실험 ROM 데이터가 바뀌지 않았음을 확인했다. native216byte zero helper는 실험에서 동등 쓰기로 대체했다. 바이트 변이 검사는 위7위치/19개이며 모든 possible mutation 전수 검사라고 주장하지 않는다.

이 결과는 **CPU-only**다. 실제 GBA fetch/캐시·ROM metadata/압축 load·글꼴/픽셀·입력/오디오·실제 실행 시간·자연 이벤트·save 검증이 아니다.19개 clone/whole-byte guard의 생성·해시/바인딩과 원래 압축 데이터 보존은 실제 제품 빌드 책임으로 아직 통합하지 않았다. 기존 메일 방식의 성공을 힌트 소비 경로에 자동 전이하지 않는다.

## 다음 단계

### 정상 hint 소비 경로 추가 확인

`poc/runtime/pending500-022-hint-consumer-route-v1`은 기존021의 `pending500-022-weekday-field-v1` checkpoint에서6번 A로 대화를 진행한 후 L을 눌렀다. frame1092에 native0x0804F7FC/0x0804F802를 각1회 관측했고, call 직전 r0=0x0203D800/r1=0이었다. `step_007.png`의 원래 일본어 힌트 화면을 직접 확인했다. RAM/flag/내비·scene 강제 변경이나 새 wrapper 설치 없이 도달했다.

`tools/verify_hint_consumer_route.py` → `pending_insertion_500_022_selector_poc_v1/native_consumer.json`에 같은021·입력·시작 checkpoint·캡처 해시와 native call 관측을 묶었다. LR0x0804F807은 관측한 BL 위치와 원본 명령에서 도출한 값이며 별도 LR 런타임 샘플이라고 주장하지 않는다. 기존022 저장 조사에서 미관측이었던 native hint consumer 진입 경로는 이제 확인했다. 단, 이번 선정19개 원본이나 번역 clone을 실제로 소비한 증거는 아직 아니다.

1. 원본에서 재생성하는 별도 PoC 선택 또는022 primary flag를 설계해 clone/원본 비교본/descriptor/wrapper를 하나의 append writer와 하나의 composed install writer로 등록한다. 기존 selector를 별도 patch 후 덮어쓰지 않는다. source/TPI/사전컴파일/내비 index·descriptor bounds·source bytes/포인터를 제품 빌드가 검사해야 한다.
2. 원래 compressed hint table/로더/압축 데이터는 그대로 두고 ROM clone만 추가한다. raw136개의 carry 병합은 기존 계약으로 별도 검증하되 최종500-ID delta와 소비단위 분모를 명확히 유지한다. 기존 reader entry/모든 clone 위치를 최종 배치에서 산출하고 ISA를 다시 검사한다.
3. 위에서 확인한 native field hint 경로를 새 ROM에서 load 이전부터 다시 실행해 선택/ROM glyph/화면·대기/재진입·처리시간과 원래 RAM 보존을 검사한다. 필요시 read-alias 진단은 자연 사건과 분리하고 checkpoint를 격리한다. 월요일의 초기 Internet snapshot은 아직 별도 source0x78BF28을 로드한 증거여서 선정19개 자연 실행 증거로 전이하지 않는다.
4. 정확500개 통합 ROM과 독립 재빌드가 일치하고 해당 소비 경로 및 기존 정상 회귀가 통과한 뒤에만 반영 완료로 갱신한다. 사람이 검수하지 않은 번역의 needs_review/NON-DISTRIBUTION도 유지한다.

자동 한글 조합/commit/save/redisplay, 초기 구매 안내 행간, 별도 UI·이미지·전체 자연 분기/번역 검수는 여전히 미완료다. 새 배포 패키지는 사용자 재요청 전 만들지 않는다.
