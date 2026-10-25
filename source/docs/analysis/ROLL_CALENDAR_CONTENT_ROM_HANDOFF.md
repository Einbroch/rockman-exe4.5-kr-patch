# 일정 내용·약속 상대 안내 2단위 추가

2026-10-04. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

ROM `poc/output/exe45_ko_development_roll_calendar_content_v1.gba`.
SHA256 `1153e424057effbe2b728369c56c73df6270b3ebc03157aa09cdfb3a3ef4dbe9`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
누적 1,086선택 텍스트단위 / 기존9그래픽 /21선택·711미선택 archive. 전체 완역률은 아니다.

## 원문·문맥·변경 경계

65F11C:22:0 `どんな ないようなの?` → `어떤 내용이야?`.
65F11C:23:0 `ダレとの やくそく?` → `누구와 한 약속이야?`.
원본 archive 전체와 직전 ROM의 정상 종류 선택 화면을 읽었다.
`calendar-promise-source-v1`은 직전 ROM의 own-time checkpoint에서 down/A로
‘ともだちと約束’를 선택하고 script23에 도달한 read-only 관찰이다.
이 단계의 상단 `そのた`는 아직 입력 전 native 기본 표시이며 실제 약속명이 아니다.

수동 초안 `translations/roll_calendar_content_ko.json`은 기존9단위의 모든 필드를 보존한다.
등록된 `content-promise-v1` scope variant를 명시적으로 선택하며, 기존 asset/default scope는 보존한다.
일반 대사 글꼴·렌더러를 재사용한다. 새 hook이나 그래픽 수정은 없다.
255슬롯 중 7스크립트·11리터럴 선택, 248미선택 슬롯 원본 바이트 보존.
제어·공백·줄바꿈·옵션 기본값/대상·날짜 삽입·입력/저장 자료는 변경하지 않았다.
정적 글꼴·구조·왕복 검사 통과, 최장 번역 행123px.

## 재현·검증 기록

관련39테스트 통과(8.730초). 역사적 캡처 검사는 해당 과거 ROM의 근거이며 새 ROM 실행으로 합산하지 않는다.
전체 프로젝트 테스트는 재실행하지 않았다.
main / _repro / _current_repro 3독립 빌드 동일, 현재 Python405도구 drift=[], 원본 SHA 불변.
정본 `analysis/roll_calendar_content_v1/final_identity_audit.json`.
누적 옵션 중 `--roll-calendar-dialogue` 대신 `--roll-calendar-content`를 명시한다.
`run_roll_calendar_content.py`는 새 cold/profile/Roll/intro/PET 경로와 calendar/time/meal/list,
같은 ROM의 time→promise 경로를 사용한다. 이전 ROM checkpoint나 read alias는 쓰지 않는다.
런타임 검증 완료: `calendar_dialogue_runtime.json`의7화면·11단위 정상 활성 script/root,
CPU 글꼴 공급→OBJ VRAM→화면 픽셀, 리터럴 내 글자 위치·빈 영역 무잔상 검사 통과.
새22는 time step6, 새23은 promise step3에서 확인했다. 새 두 화면과7화면 모음을 직접 시각 검토했다.
기존20번역 archive payload 동일. 추가 archive의 기존9번역단위 원문/번역/state 전체 필드 동일.
새 대사1 + 달력메뉴1 + 소개/PET/기본대사/장비4 + 등록 일정 시각조회1 = 집중7정상 보고서 통과.
새 alias 진단 없음. 합성 CPU 회귀 검사는 실제 퀘스트 플레이 증거로 합산하지 않는다.
화면 `analysis/roll_calendar_content_v1/calendar_dialogue_pages.png`.

## 열린 완료 조건

이번 변경은 약속명 입력 안내 대사이지 한글 입력 기능 구현이 아니다.
기본 ‘ごはん’/‘じゅく’, 종류·빈도 메뉴와 다른 달력 대사는 미번역이다.
입력 편집→확정 레코드→여러 표시 소비자→저장/재로드 연결이 가장 중요한 열린 경계다.
선택 취소/아니오·한글 이름 확정·영구 저장/재로드·RTC 자연 알림·전체게임·오디오/하드웨어·인간 검토·배포 미검증.
