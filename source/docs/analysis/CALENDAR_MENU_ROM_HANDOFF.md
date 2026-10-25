# 달력 메뉴 한글화·정상 실행 확인

2026-10-04. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

ROM `poc/output/exe45_ko_development_calendar_menu_v1.gba`.
SHA256 `db282269f75b1c2f91d512cf490c25495b58881cbcaf8fbe2419a78a618d1b96`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
직전 개발 ROM `exe45_ko_development_roll_schedule_alarm_v1.gba` SHA6e59764c….
누적1,075선택 텍스트단위 / 기존9그래픽 /20선택·712미선택 archive. 전체 완역률이 아니다.

## 조사에서 확정한 표시 경계

직전 baseline의 own-ROM intro에서 정상 입력으로 달력을 열었다.
`poc/runtime/calendar-fixed-source-v1/`는 read-only fixed-cell 관찰이며 alias/RAM/ROM/register 변경이 없다.
원본6368E8 script0, 스트림08636AE6, native554A4→IWRAM03006824→copier0300689C.
라이브 진입 r4=2/r5=10을 직사각형 문자 수로 해석하지 않았다. 실제 완료값은24개 글꼴 복사/1536바이트이다.
staging0201A800→OBJ VRAM06013800. 메뉴는24셀의8셀3구역이고 첫 작업명·둘째·셋째 구역을 OAM이 별도 좌표에 표시한다.
기존 big fixed-cell F9FC 글꼴 공급을 재사용할 수 있으므로 새 hook은 추가하지 않았다.
나머지 시각/빈도·일정 종류·입력 경로는 같은 파서라고 추정하지 않으며 기본 이름 과제는 계속 열린다.

## 번역·보호 규칙

`translations/calendar_menu_ko.json` 수동 초안:
`とうろく    よていをみる  さくじょ    ` → `등록      일정 보기   삭제      `.
작업명3개지만 원본이 하나의 리터럴이므로 새 텍스트 단위는1개다.
`calendar_menu_model.py`는 정확한 원문/key/언어/state를 확인하고,24셀 및8셀 구역과 오른쪽 공백 패딩을 강제한다.
한글은 F9FC+uint16, 공백은 원래00, 종료는E5이며 새 데이터48바이트+E5.
종전 대사의 ‘끝 공백 수 동일’ 규칙은 이 메뉴의 소비 경계와 다르다. 첫 빌드는 이를 발견하고 중지했다.
기존 대사/선택지 정책은 완화하지 않고 이 정확한 메뉴에만 구역 경계 검사를 적용했다.
실패 작업폴더 `poc/work/calendar_menu_v1`는 보존; 성공은 `..._build2` 사용.

source6368E8 2,337바이트 /255슬롯 /SHA816d719a….
모든15root를 catalog 그대로 새 raw archive로 재배치하고 원본archive는 그대로 보존했다.
254미선택 슬롯은 바이트 동일: keyboard2/3/4, 원본 기본 이름62/63, 유형메뉴60, 입력/날짜/저장 스크립트 포함.
최종 expected-write 계획, source hash, native/binary/semantic round-trip, source/폰트·변경외범위 검사 통과.
동일 아카이브 relocation이 모든 입력/저장 소비자의 실행 완료를 뜻하지 않으므로 배포는 계속 보류한다.

## 새 ROM 정상 검증

`run_calendar_menu.py`의 새 PREFIX로 cold/date/profile/navimenu/Roll선택/intro/장비,
seed/PET prompts/기본talk를 재실행했다. 예전 ROM checkpoint를 새 ROM에 사용하지 않았다.
같은 새 ROM의 normal intro→calendar→time→meal→list로 AM2:00 1회 식사 등록·L조회·목록·복귀.
`normal_regressions.json`의4정상 보고서, `time_runtime.json`의 등록시각1정상 보고서,
`calendar_menu_runtime.json`의 새 메뉴1정상 보고서 = 집중6정상 보고서, 신규 alias 진단 없음.
기존 빅해머1 selector32합성 CPU 벡터도 통과했지만 실제 해당 퀘스트 진행 재검증은 아니다.

calendar step2/3에서 새 스트림의24글리프 identity/provider, source ABI,1536-byte extent,
BDF8x16 글꼴+원본 공백→staging→VRAM exact bytes,8한글셀의 OAM 타일 참조·좌표·팔레트,
원본 화면의 ink/shadow색→새 픽셀·빈 픽셀 무잔상 대조 통과. 두 화면 직접 시각 검토.
사진 `poc/runtime/calendar-menu-v1-calendar/step_002.png`.
새 ROM list step5에도 `2:00 AM부터 / 「ごはん」` 정상 표시. 원본 이름은 의도적으로 아직 일본어다.

`calendar-menu-v1-highlight`는 같은 meal normal checkpoint에서 down/up으로3작업 간 이동하고 left로PET 복귀했다.
step2 ‘일정 보기’, step4 ‘삭제’ 강조 표시, step9PET 복귀 직접 검토; own-ROM parent/artifact hashes 검증 통과.
이동·표시 확인이며 실제 보기/삭제 메뉴 확정 또는 등록 자료 삭제 검증으로 주장하지 않는다.
PET 복귀 step9에 일본어 롤 일반 대사가 남아 있음을 확인했으며 후속 미번역 조사 대상으로 보존한다.

격리 emulator save directory에서 해당 개발 ROM의19-byte `.rtc`만 정상 업데이트됐다.
기존 `.sav` 등 다른 파일 변경 없음. 초기 보고서는 모든 sidecar 차이를 금지해 이를 발견하고 중지했으며,
최종은 정확한 STEM+'.rtc'만 허용·기록한다. 이것은 RTC 일관성·저장/재로드 검증이 아니다.

## 재현·남은 조건

관련34테스트 /11.702초 /OK. 과거 schedule/time 캡처 재검사는 해당 과거 ROM의 검증이고 현재 정상 실행으로 합산하지 않는다.
전체 프로젝트 테스트는 재실행하지 않았다. 이전19번역 archive payload와 PET 그래픽 동일.
main/_repro/_current_repro2 3최종 독립 ROM 동일. 최종398 Python 도구 해시 drift=[].
`_current_repro`는 RTC 보고서 수정 전 보존 빌드; 현재 도구 pin은 `_current_repro2`.

누적 옵션에 `--calendar-menu` 추가:
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout
--roll-subjects --roll-pet-chipquest --roll-mail-alert --roll-dialogue-chip-name
--roll-competition --roll-schedule-time --roll-schedule-alarm --calendar-menu`.
항상 fresh work/out/PREFIX 사용. 원본·기존 ROM·실패 작업·성공/실패 기록 보존.

기본 이름/입력·확정 자료·다른 고정 셀 표시·저장/재로드의 연결이 가장 중요한 열린 조건이다.
달력 안내 대사, 기본ごはん/じゅく, 시각/빈도/유형 메뉴와 다른 소비자도 아직 미번역이다.
자연 RTC 알림·다중 이벤트·한글 입력·실제 오디오/하드웨어·전체게임·인간 문구/시각 승인·배포 검증 미완료.
