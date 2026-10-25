# 일정 종류 목록 5항목 번역

2026-10-04. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

최종 ROM `poc/output/exe45_ko_development_calendar_types_v2.gba`.
SHA256 `903858514f23de53ce5ce5def2c07527ff3461d216e3fa6a06d47ef92eb6e883`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
누적1,087선택 텍스트단위 / 기존9그래픽 /21선택·711미선택 archive. 전체 완역률이 아니다.

## 관찰·채택한 경계

기존 `SCHEDULE_PRESET_SOURCE_BOUNDARY.md`의 ‘script60 고정 byte offset 가능성’은 미확정 위험이었다.
직전 content-v1 정상 time step6에서 실제 parser가 script60 처음부터27글리프를 읽어
1728바이트 staging→OBJ VRAM06014000으로 공급하는 경계를 관찰했다.
native caller080554BA, copier/parser source 바이트는 변경하지 않는다.
type source `calendar-types-source-v1`는 동일 ROM의 time checkpoint에서 정상 down4회 이동 관찰이다.
각 메뉴의 OAM 타일 참조는 셀 구간0..5 /6..12 /13..15 /16..18 /19..21에 대응한다.
4번째 down 뒤 스크롤된 다섯째 ‘そのた’의 셀19..21도 확인했다.
27셀을 처음부터 해독하므로 source 내부 byte offset에 임의로 번역을 끼우는 정책을 쓰지 않는다.
이 근거는 표시 목록에 한정하며 기본 이름 복사/입력/레코드 소비자의 한글 지원을 증명하지 않는다.

## 번역·빌드 검사

`translations/calendar_types_ko.json`은 기존 메뉴0 초안을 그대로 유지한다.
60의 하나의 리터럴을 수동 번역: `TV 방송 / 친구와 약속 / 식사 / 학원 / 기타`.
source 6/7/3/3/3/5 셀 구간, 전체27셀을 오른쪽 공백 패딩으로 유지한다.
여섯째 `?????`는 원문 보존하며 현재 정상 경로에서 선택/표시됐다고 주장하지 않는다.
새 단위는 하나이고 작업명은5개다. 새 hook이나 그래픽 수정은 없다.

등록된 `type-labels-v1` variant, 정확한 source/key/language/state와 구간 경계만 허용한다.
calendar_types_model의 별도 패딩 정책이며 다른 대사/선택지 끝 공백 정책은 완화하지 않는다.
source2337바이트·255슬롯·15root 검증, 메뉴0/60 제외253슬롯 및 keyboard2/3/4,
기본이름62/63, dynamic confirmation61, 입력/저장 소비자는 원본 바이트 보존한다.
원본 archive를 보호한 전체 relocation, expected-write·구조·binary/semantic round-trip 검사 통과.
첫 work/calendar_types_v1 빌드는 기존1단위 early validator가 확장을 거부해 중지했다.
등록 variant만 별도 검사로 분기한 뒤 fresh work/calendar_types_v1_build2로 성공; 실패 작업은 보존한다.

## 검증·재현

관련41테스트 /15.163초 /OK. 역사적 schedule 캡처 재검사는 해당 과거 ROM 근거로만 취급한다.
전체 프로젝트 테스트는 재실행하지 않았다.
main / _repro / _current_repro 3독립 ROM 동일, 현재Python409도구 drift=[], 원본 SHA 불변 확인.
정본 `analysis/calendar_types_v1/final_identity_audit.json`.
누적 `--calendar-menu` 대신 `--calendar-types`, `--roll-calendar-content`는 유지한다.
새 ROM own-cold/profile/Roll/intro/PET→calendar/time/meal/list/promise 및 types-scroll 정상 경로 완료.
최종42테스트 /18.121초 /OK. native mono literal profile 분리 검사1개를 추가했다.
최종v2 main/_repro/_current_repro 3독립 ROM 동일, 현재409도구 drift=[], 원본 보존 audit 통과.

## 런타임 검증·조사 중 거부된 가정

초기 보고서는 Windows manifest 역슬래시 경로를 다른 asset으로 거부했다.
정확한 resolve 경로 동일성을 사용하고 해시 검사는 유지했다.
다음에는 작업 메뉴의 big provider08601738 및 big Hangul bank 가정을 거부했다.
실제 source와 current calls는 font08619EF8이고, F9FC가 기존 mono bank로 공급한다.
source mono spec 전체·원본 font hash·roles1/3/4·BDF raster·실제27glyph provider를 연결했다.
명세의 literal profile도 script60은 fixed-cell-mono, script0은 fixed-cell-big로 분리했다.
이 정정은 코드/글꼴/문구를 변경하지 않는다. 그전v1 빌드·실패 보고 시도·캡처는 보존한다.

정정된v2와 정상 실행에 쓴v1은 전체ROM 바이트 동일성을 검사했다.
캡처 `calendar-types-v1-*`의 exactSHA/own-parent/probe/isolated-save 증거를 그 동일한 최종 바이트에만 귀속한다.
새 ROM에 과거 다른 SHA의 checkpoint를 가져온 것이 아니며 CPU/RAM/ROM/register/read alias 수정도 없다.

`types_runtime.json`에서27셀 원문 경계·provider·BDF/source glyph→1728-byte staging→전체VRAM 대조 통과.
time step6 및 정상 down4회의 step2/4/6/8에서 기존 OAM 셀 좌표·순서·palette를 그대로 유지했다.
표시되는0..21셀,5항목의 한글·공백·잔상 픽셀 검증 통과. 여섯째????? 공급은 정적으로/VRAM 검증하되 표시 완료로 합산하지 않는다.
목록 첫4항목/스크롤된기타 화면과 기존 확인/약속 안내를 직접 시각 검토했다.

스크롤 위쪽 native sprite0=(0x0011,0x0038,0xC6D1)가 셀10 첫 줄 일부를 덮는다.
해당 화살표는 OAM/VRAM/palette 원본 동일성과 현재 opaque shape/color consistency를 검증했다.
source/current screenshot의 화살표 RGB가 같지는 않아 그 색의 프레임 동일성은 주장하지 않는다.
가려진 글자도 전체VRAM exact proof에 포함하지만 화면의 가려진 픽셀을 글자 검증으로 집계하지 않는다.
RGB 차이의 정확한 원인/프레임 동등성은 미확정이며 임의 palette/문구 수정으로 숨기지 않았다.

이전20개 다른 번역 archive payload와 이 archive의 기존254개 script(60 제외) 동일.
253개 원본미선택 슬롯,15root,기존9그래픽 보존 확인.
종류목록1 + 등록안내1 + 달력작업메뉴1 + 소개/PET/기본대사/장비4 + 등록시각조회1 = 집중8정상보고서 통과.
새 alias 진단 없음. 합성 CPU 검사는 실제퀘스트 실행으로 합산하지 않는다.
화면 `analysis/calendar_types_v1/types_pages.png`.

## 가장 중요한 열린 경계

종류 선택기의 ‘식사/학원’과 실제 등록 자료/확인/조회 이름은 별도 소비자다.
기본 ‘ごはん’/‘じゅく’의 raw 이름, 한글 입력·편집·확정 레코드·재표시·저장/재로드는 아직 미완료다.
빈도 메뉴·다른 달력 대사도 미번역. 자연 RTC 알림·다중 이벤트·전체게임·오디오/하드웨어·인간 승인·배포 검증 미완료.
