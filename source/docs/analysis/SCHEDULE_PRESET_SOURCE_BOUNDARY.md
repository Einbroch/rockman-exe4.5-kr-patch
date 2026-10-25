# 기본 일정명 조사 — 원본 유지 결정

이 문서는 2026-10-04의 고정baseline 결정 기록이다.
2026-10-05 `CALENDAR_PRESETS_POC_HANDOFF.md`에서 후속 기본명2개 실험을 수행했다.
확인·등록·같은세션 조회는 검증했으나 키보드/편집/저장·재로드/모든 소비자 경계는 여전히 미완료다.
이전 source 증거/ROM은 보존하며, 새 실험을 이름 입력 기능 완성으로 취급하지 않는다.

2026-10-04. development-draft; NON-DISTRIBUTION; release_eligible=false.

고정 증거 ROM: `poc/output/exe45_ko_development_roll_schedule_time_v1.gba`
SHA256 `35d20055bbb740d8b4468ea399b998d843827fca66e0d66c7825af10436277c6`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.

## 확정한 연결

- `6368E8` 원본 raw archive: 2,337바이트, 255슬롯. 전체 TPL을 확인했다.
- script60은 메뉴 이름을 이어 붙인 `TVばんぐみともだちと約束ごはんじゅくそのた?????`이다. 임의 길이 변경은 고정 오프셋 메뉴 선택을 깨뜨릴 수 있으므로 변경하지 않았다.
- script62=`CF B4 CA E5` (`ごはん`), script63=`D1 E4 07 A2 E5` (`じゅく`).
- 같은 `CF B4 CA E5`의 두 번째 출현은 script146의 `!すきなごはん` 끝부분이다. 두 번째 기본 일정명 저장소로 잘못 취급하지 않았다.
- `schedule-preset-source-v1-register`는 동일 ROM의 정상 calendar/time 체크포인트에서 컨트롤러로 식사 등록을 계속한 경로다. read-only observer가 frame203에 ROM `08636DA1..08636DA4`의 4바이트 읽기를 관찰했다. CPU PC=`08032ACC`, 목적지 r1=`02026080`.
- 소스 `08032AC6..08032AD6` 루프는 한 바이트씩 복사하고 `E5`를 만나 종료한다. 이 함수에는 별도 길이 상한 검사가 없다. 한글 코드 내부에 종료 바이트가 들어가는지, 실제 목적지/레코드 용량 및 편집 동작을 독립 검증해야 한다.
- `schedule-preset-source-v1-lookup`는 위 정상 등록의 own-ROM 체크포인트에서 PET L 조회를 계속했다. frame408, PC=`08000954`에서 목적지 `02010C40..02010C5F`로 32개 바이트 쓰기 콜백을 관찰했다. 이것은 조회용 임시 이름 버퍼로의 전송 증거이며 영구 저장 증거가 아니다.
- 이전 `roll-schedule-time-v1-list` RAM/폰트/픽셀 보고서는 위 버퍼의 `ごはん` 표시를 증명한다. 입력·편집·저장·재로드 또는 모든 고정 셀 소비자가 한글을 처리한다는 증거로 확장하지 않는다.

## 증거 파일

`poc/runtime/schedule-preset-source-v1-register/`, `...-lookup/`의 result.json,
각 step의 `_preset_source.json`, `_schedule_ram.json`, RAM dump, screenshots,
`preset_source_environment.json`에 도구/관찰기 해시를 보관했다.
`tools/capture_schedule_preset_source.py`는 읽기/쓰기 **관찰만** 하며 ROM/RAM/레지스터 값을 바꾸거나 read alias를 사용하지 않는다.

## 남은 가장 중요한 경계

기본 이름을 실제 등록 자료에서 한글로 바꾸려면 등록 원본→편집 버퍼→확정 레코드→여러 표시 소비자→저장/로드까지 하나의 경로를 검증해야 한다.
메뉴 script60, fixed-cell 메뉴/확인 화면, 일반 대사 임시 버퍼, 입력 키보드 script2/3/4를 분리해서 다룬다.
현재는 이름·입력 자료를 변경하지 않았다. 미번역 `ごはん`/`じゅく`이 남아 있다는 제한을 유지한다.

이번 다음 빌드는 이름 버퍼를 건드리지 않는 `660D90` PET 알림의 독립 고정 문장3/4/6만 추가한다.
식사/학원 알림의 대사 번역은 기본 이름 한글화나 자연 RTC 알림 발생 검증을 대신하지 않는다.

## 후속: 종류 선택기60의 표시 경계 확정 (2026-10-04)

`analysis/CALENDAR_TYPES_ROM_HANDOFF.md`에서 script60 목록만 후속 검증했다.
27셀 전체 해독→1728-byte staging/OBJ, native mono font08619EF8, OAM 구간6/7/3/3/3/5이다.
따라서 이 표시 경로에서 고정 source byte offset으로 이름을 나눌 것이라는 가정은 채택하지 않았다.
원래 셀 구간을 유지해 ‘TV 방송/친구와 약속/식사/학원/기타’를 반영했다.
raw 기본 이름62/63과 script61/입력/저장 소비자는 변경하지 않았고, 위 가장 중요한 열린 경계는 계속 미완료다.
