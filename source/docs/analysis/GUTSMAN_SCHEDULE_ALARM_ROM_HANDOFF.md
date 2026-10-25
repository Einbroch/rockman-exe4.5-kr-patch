# 거츠맨 PET 일정 알림 — 2026-10-06

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

후보 `poc/output/exe45_ko_development_gutsman_schedule_alarm_v1.gba`, SHA256 `5e3547d5f773decb9bebfe36b86dadc0fd4df73ee7f003c1aa9870f2e49decfd`. 신규3번역 literal, 누적2,244선택 literal/55선택·677원본 유지 archive. 전체 미번역 요청 완료 아님.

## 원본·적용 범위

66651C:771bytes/28slots/root038124. 원본pointer0866651C와 전체TPL21literal, PET0..6/mugshot20..26 consumer 차이를 확인했다. Source payload SHA `16cd2ff2d4af233f94277cb9077169046a4abe04f4789c735e77495697f18852`; TPL SHA `8286cb9ad04ff3ac3ec9f09570327fd24da70450943fd7f4e5209a19d6e1dce1`.

변수 없는 PET4:0/4:1/6:0만 선택했다. ‘학원 갈\n시간이거스!!’, ‘공부、공부!\n힘내는거츠!!’, ‘그리고・・・’로 개별 작성, 기존 거츠/거스 말투 후보 유지/인간 문구 검토 대기. 자산 `translations/gutsman_schedule_alarm_ko.json`, 직렬화 `tools/draft_gutsman_schedule_alarm.py`. 넘버맨4649 승인 재사용 없음.

18미선택literal/26미선택script span 원본bytes, sound155/wait96·flags3585/3658·event buffer·callCheckNowEvent/callFindNowEventType·nickname·keyWait/clear/waitHold·window/arrow 명령 보존. 별도mugshot24/26은PET132px 모델로 번역하지 않았다. 원본 ROM에서 누적 flags+`--gutsman-schedule-alarm`으로 빌드하며 patched ROM은 입력이 아니다.

3문구/30glyph의 source·skeleton·숫자·glyph·geometry·roundtrip 정적검증 PASS, 최대82px≤132px. 관련163tests/598Python AST PASS. main/repro/final current_repro 동일SHA, tool drift=[]/immutable sourceSHA 보존. `analysis/gutsman_schedule_alarm_v1/final_identity_audit.json`.

## 실행·시각 검증

`tools/run_gutsman_schedule_alarm.py`로 이 후보 자체 freshFF저장/cold이어하기/거츠맨선택 정상16구간 후 Mesen 한 프로세스씩 알림4/6 진단. 정상 넘버맨3페이지/거츠맨첫인사2페이지/PET8장면22항목/29focus·No수락·B취소 회귀 PASS. native save58에서 생성된 save SHA `fb82d51b06fadc2d37d3e87990edc0d1104b5abb9ee99df461803769915f65ca`: 자체 FF에서 생성, 직후snapshot/현재disk 일치, 다른saves보존. 이전후보와같은SHA여도 수입save아님. 이는넘버맨 일반저장회귀이지 한글이름persistence/거츠맨저장증거아님.

기존54archive payload·선택자산·그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 수정 유지. 회귀결과 `analysis/gutsman_schedule_alarm_v1/pet_regression/runtime.json`.

격리 observer `tools/capture_gutsman_schedule_alarm.py`: R 입력의 원래거츠맨talk root038148→0866A844 읽기 반환값을 단1회 알림pool로 연결하고, 요청script0 offset을4 또는6 offset으로 단1회 반환. source dispatcher/glyph consumer code guards 원본과동일. ROM/RAM/RTC/save 쓰기없음. root_aliases=entry_aliases=1, 자체정상 select-gutsman parent/exactROM/tool hashes 검사. 진단checkpoint는 `diagnostic_checkpoint.mss`, `normal_play_checkpoint_eligible=false`, 정상chain재사용금지. alias는ROM에없으므로 내비대사를되돌리는ROM수정도필요없다. 실제거츠맨초상유지.

PET4 첫페이지step2/11glyph·두번째step4/13glyph, PET6step2/6glyph: CPU font read/ROM font→actualOBJ VRAM→화면pixels·advance/행좌표·keyWait E600F1·clearing·nativearrow footprint 분리·오른쪽border·페이지순서 PASS. 빈영역4,087/3,775/4,771pixel 검사.6은keyWait에서멈춰 동적이벤트dispatch미실행,4도마지막keyWait까지의두페이지일뿐 후속이벤트/종료검증아님.

결과 `analysis/gutsman_schedule_alarm_v1/runtime.json`, 화면 `diagnostic_alarm_pages.png`. 메인에이전트가3페이지/정상PET8장면composite 직접확인. 이는알림renderer진단이지 실제현재시간알림·등록일정·이벤트도달성증거아님. 정상신규알림runtime units0/진단3페이지분리. 이번후보에서기존오늘일정/대회/접속/귀환/메일/날짜별대사를모두재실행한것도아님.

## 다음·미해결

`analysis/full_scope_gutsman_schedule_alarm_v1/`: 선택2,244/미선택일본어포함27,804/기타1,859. catalogue732archives/31,907canonical literals는전체ROM번역분모아님.
같은archive18미선택literal: PET0‘!!’유지여부/PET1·2·3·5의event/nickname경계·다음페이지문맥·suffix비증가/별도mugshot21..26의consumer·좌표·폰트capacity 확인필요. 정상일정등록·시간알림/반복·flag3658/동적이름population도별도실행대상.
추가66A7A8의5slot/3승패·무승부literal 전체읽음, 아직번역/등록/빌드미작성.666430‘かりです’는개발용임시placeholder로보이며 맥락미확정, 일반문구로추정번역하지않음.
한글이름편집→committed record→모든재표시→영구재로드→기존save호환이가장어려운미해결조건. 전체graphics/inline/fixed population/prior wait-arrow53pixel 차이/전체이벤트·전투·음성·하드웨어/인간검토도남는다. 전체완료·배포선언없음. 원본·이전후보·실험·실패·테스트saves보존.
