# 롤 등록 일정 시각 접미사 ‘부터’ / 정상 일정 등록 경로

2026-10-04. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 전체 완역·배포 승인 아님.
한글패치 스킬에 따라 미확인 동적 삽입 경계를 정상 일정 등록·조회 경로에서 조사했다.
PDF 읽기 스킬은 공식 설명서의 달력 조작 페이지를 확인하는 데 사용했다.

## ROM / 번역

`poc/output/exe45_ko_development_roll_schedule_time_v1.gba`.
SHA256 `35d20055bbb740d8b4468ea399b998d843827fca66e0d66c7825af10436277c6`.
원본 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 변경 없음.
누적1,071선택단위 / 기존9그래픽, 18선택 /714미선택 archive.
전체 게임의 미번역 분모나 완료율이 아니다.
661754:11:2의 원문 ` から\n`를 `부터\n`로 직접 수동 초안 작성했다.
새 고유명사·선택지·변수 내용 변경 없음. 이전5문구는 정확히 동일한 초안 유지.
선택 scope는6리터럴 /5스크립트, 나머지9슬롯·6리터럴 보존.
hour/minute/AMPM/event-name 삽입과 조회 루프·모든 제어 명령·따옴표를 보존했다.
source260바이트 /14슬롯 /pointer0x380F8,
SHA `5bafb1c9666c968c595f3f41f48cc5787afced8ea224335658fe97dd6318f33c`.
compiled358바이트 /offset0x803358,
SHA `eaf770e0db150ac73c42ba435b0204ff44d4d6314ab6752525482c238b8429af`.
native/semantic/binary round-trip, 보호 제어, BDF 글꼴 공급·폭 검사 통과.
별도 모델이 줄바꿈 위치와 source 접미사30px→target24px의 비증가를 검사한다.
시각 삽입 앞부분의 인수·구두점이 그대로이며 이름은 다음 행이므로, 시간/이름 집합을 모르는 상태에서 레이아웃 전체 검증을 주장하지 않는다.
이전17개 별도 archive payload는 전체 실제 바이트 대조한다.
‘빅해머1’ hook은 새 명령 주소로 재구성하며 공유 원본 이름풀은 변경하지 않는다.

## 원문 경로 조사

조사 baseline은 직전 c1838a5e… ROM의 own 정상 roll-intro 상태다.
start/select/L 버튼 후보 `roll-calendar-survey-v1-{start,select,l}`를 각각 격리된 정상 자식으로 관찰.
L 버튼이 정상 script10 오늘 일정 조회를 호출하는 것을 확인했다.
공식 설명서 https://www.nintendo.co.jp/data/software/manual/manual_pc5j_00.pdf
PDF SHA `fca39090a0e8ec86fbd09ce37844d294d315fb730d23b86ab9ee83065b30d601`.
읽기 전용 자료는 `analysis/schedule_native_v1/manual/`에 보존했다.
PDF13번째 펼침면(인쇄22/23쪽)의 달력/일정 설명 전체를 시각 검토했다.
우측 방향키→달력, 등록→날짜→일정→시각→빈도→기본 일정 선택 경로를 제안했고 실제 ROM에서 확인했다.
설명서는 조작 후보와 맥락이며 타깃 동작 증거를 대신하지 않는다.

source `roll-calendar-survey-v1-right`에서달력/오늘날짜/일정/시각 선택,
`...-time`에서 AM2:00/1회만/유형 선택,
`...-meal`에서 기본 ごはん 선택·확인 후 달력 복귀.
최초 `...-list`는 달력에서 불필요한 A/B 입력으로 등록 화면에 다시 들어간 조사 경로다.
예상 목록 화면에 도달하지 않았으며 성공 목록 증거로 사용하지 않는다. 자료 그대로 보존.
`...-list2`는 달력에서 left→PET→L→오늘소개→A→등록일정→A→목록마무리→A→PET.
step5에 원문 `2:00 AM から / 「ごはん」`를 정상 조회로 관측했다.
source meal 경로의 중간취소는 새 경로에서 제거하고 기본선택→확인을 정상 입력으로 재현한다.
이번 일정은 테스트 인스턴스의 임시 세션에서만 등록한다. 실제 사용자의 저장 데이터 변경·호환성을 주장하지 않는다.

## RAM / 글꼴 경계

`capture_roll_schedule_native.py`는 read-only observer이며 read-alias/RAM/ROM/register 직접 쓰기 없음.
glyph draw 시 원본 RAM byte도 기록하여 각 삽입 문자열을 소비 시점에 식별한다.
02:00 AM meal의 소비 버퍼:
hour02010AC0=`00 03 E5`(공백+2), minute02010B40=`01 01 E5`,
AM02010BC0=`5E 6A E5`, name02010C40=`CF B4 CA E5`(ごはん).
원본 AMPM/이름 작성 명령 FC032B00/FC032D00 및 F90C43 해석을 실제 RAM/소비에 연결했다.
다른 작성자·프로필 문자열·전체 입력/시각·이름 집합에 일반화하지 않는다.
native 앞부분 폭82px, target부터24px →첫 행106px; 이름+따옴표는55px.
일정명 ごはん은 일본어 그대로다. 기본 이름표 한글화/사용자 일정명 입력은 아직 미번역·미검증.

## 새 ROM 검증 및 보존

새 ROM own cold/date/profile/navi/selection/intro/equipment와 PET/menu/talk 체인을 먼저 생성한다.
`roll-schedule-time-v1-calendar/time/meal/list`는 같은 ROM의 정상 부모들에서 이어지는 정상 입력 경로다.
기존 단순 일정 안내 1/3/10/12 read-alias 캡처는 별도 `script{n}` 경로이며 정상 등록의 부모로 쓰지 않는다.
새 시각/목록 정상 검증 보고서는 `analysis/roll_schedule_time_v1/time_runtime.json`에 결합한다.
보고서 통과: 새 ROM list step5/6의 native10→조회branch11, 네 종류 RAM버퍼/E5,
원본 글꼴·폭·위치, 한글부터의82px 직후 배치, CPU읽기→OBJ VRAM→화면 픽셀,
빈 본문 무잔상·keyWait/clearMsg, step3소개·step7마무리와step9정상복귀 검증.
step5/6 화면을 직접 검토, 일본어 から 잔존 없음. 이벤트명 ごはん은 원문 유지.
실제 normal runtime units는 661754:10:0 /11:2 /12:0이다.
기존 안내1/3/10없음/12의 보조4alias 경로는 캡처만 실행했으며 formal pixel 보고서나 정상 등록 증거로 합산하지 않는다.
새 ROM greeting/PET/menu/talk/장비4보고서+등록시각1보고서의 정상5보고서를 `focused_runtime.json`에 결합.
기존18관련+신규2테스트=20 /5.550초 /OK exit0, `final_test_summary.txt`.
예비19테스트는 중복 실행으로 합산하지 않는다. 이전207전체 테스트는 이번 턴에 재실행하지 않았다.
새 ROM ‘빅해머1’ selector의32합성 CPU벡터 통과, 실제 칩퀘스트 진행을 재검증한 것은 아니다.
정상 introduction/list-ending 소비도 별도 페이지로 검증한다.
한글 입력·저장/재시작·RTC 지속성·실제 오디오·하드웨어·복수 이벤트/다른 이름/시각/AMPM·전체 게임·배포 승인 미완료.

main/_repro/_current_repro 3독립빌드 동일, Python389도구 drift=[] 통과.
원본·이전·조사 실패/성공 캡처·상태·자료 모두 보존했다.
빌드 선택은 이전 옵션에서 `--roll-schedule` 대신 `--roll-schedule-time`:
`--roll-intro --roll-fortune-complete --roll-jackin --roll-return --roll-plugout
--roll-subjects --roll-pet-chipquest --roll-mail-alert --roll-dialogue-chip-name
--roll-competition --roll-schedule-time`.
fresh work/out/PREFIX 필수. 과거 SHA의 런타임은 새 ROM에 전이하지 않는다.
