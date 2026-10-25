# 묶음004 — 기존 미적용500개 실제 누적 ROM 반영

정책 `development-draft; NON-DISTRIBUTION`. create-kr-patch의 기존 초안 재삽입/원본 보존/누적 빌드·검증 절차로 진행했다. 새로운 번역 문구 작성이나 전체 게임 번역 완료 주장이 아니다. BPS/xdelta/ZIP은 사용자 재요청 전까지 생성하지 않는다.

## 현재 결과

- ROM `poc/output/exe45_ko_development_pending500_004_v1.gba`
- 독립 재빌드 `poc/output/exe45_ko_development_pending500_004_v1_repro.gba` 전체 바이트 동일
- SHA256 `9492ab8b6ba422ad629784e312a990c0683f43983d6e504f9f3699bdd79ef427`
- 누적4,337→4,837개, 주125→152아카이브, catalog 미변경580개
- 모든 빌드는 immutable 원본 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`에서 시작
- 이전003 ROM SHA256 `2cddc59ca723ce789c7e935a09ab1742c5a347df41583224fb07c78394c26f04` 및 모든 이전 payload 보존
- 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 보존, 새 패치 파일 생성0개

## 선정 및 소비 계약

`pending_insertion_500_004_selection_v1/selection.json`의 정확한500 source-ID를 적용했다. 27 raw 아카이브:68BAAC,68CBFC,68D454,68D96C,68E5E0,68E8C4,692874,69303C,6930F8,6942F0,697B70,698508,6999F4,69D020,69D8D4,69E088,69E12C,69E708,69EF48,6A207C,6A2FBC,6A38E8,6A4BF0,6A4CC8,6A9970,6AA214,680370.

기존 주 및 별도 장비·메일·keyitem 등 모든 컴파일 소비자의 ID/아카이브를 제외했다. script 단위 일본어 리터럴 전체를 선정했고 동적 print 명령이 있는 script는 이번 대상에서 제외했다. 원문 단어·명령·번역 단어·숫자·줄 수 변경 없음. 옵션/이벤트/flag/jump/wait 값도 원본대로 유지한다.

raw payload를 확장 ROM에 배치하고 확정 catalog의 모든 해당32비트 포인터를 갱신한다. 압축 pool/RAM 용량 변경이나 새 코드 후킹은 없다. 기존 메일5/장비3 ROM clone 및 선택기는 재배치 주소를 재계산하며 모든 ISA/ABI/Expected Write 검사를 누적 빌드에서 유지한다.

준비 검사 `pending_insertion_500_004_preflight_v1/preflight.json`: source native 바이트 왕복, command skeleton, 의미·바이너리 왕복, unselected scripts byte identity, 모든 glyph/mapping, 16bit table extent, 최대3행/보수적132px 검사 PASS. 기존 초안은 그대로이며 `translations/pending_insertion_500_004_layout.json`은 빈 layout 목록이다.

## 검증 근거

- `pending_insertion_500_004_rom/integration_v1.json`: 모든 원본 ID 합집합에서 정확히500개 추가/기존 누락0; 이전125개 주 및 별도 페이로드 byte identity, 신규27개 payload hash/포인터/source-ID와 독립 재빌드 동일 PASS
- `selector_cpu_v1.json`: 기존 메일/keyitem/3장비 선택기3,195조건 PASS, 합성 CPU 벤치이며 실제 진행 증거 아님
- `startup_audit_v1.json`: 누적 변경 범위·선택 자산·포인터·부팅/자판 보호 영역 및 재현 감사 PASS
- `normal_runtime_v1.json`: 새 ROM 소유 cold boot→날짜/이름/초기 설정→기존 일본어 자판3페이지→네 selectable Navi→Rockman 첫 메일23쪽/목록 복귀/재열기 PASS
- `first_mail_pages_v1.png`: 해당 첫23쪽을 직접 시각 검사
- `alert_runtime_v1.json`, `number_alerts_v1.png`: 아래 격리 진단 신규6리터럴의 실제 keyWait endpoint, ROM stream, 한국어/쉼표 font CPU reads, source font 공급, OBJ VRAM/화면 role pixels 및 각 페이지의 빈 영역 지움 PASS. 실제 넘버맨 초상/글상자/화살표를 직접 시각 검사
- `python -X utf8 tools/test_pending500_002_pages.py`: 기존 명시적 페이지 회귀5tests PASS

정상 체인 증거 `poc/runtime/pending500-004-v1-boot/pagecycle/complete/read/selection` 및 `number-complete`. 정상 NumberMan8을 선택한 뒤 NumberMan talk table080382B0의 native root read를 신규68BAAC로, native script0의 table lookup을 script1 또는2로 한 번만 alias했다. caller08037F20, initializer0804FB76, context0200FA20, Navi8, target source window prefix를 모두 확인했다. ROM/RAM/날짜/flag/진행 정보를 observer가 직접 쓰지 않는다. alias된 호출 이후 게임 자체 원본 명령이 실행한다. 신규6개만 렌더링 진단했으며500개 전체 gameplay로 확대하지 않는다.

진단 증거 `poc/runtime/pending500-004-v1-number-alert1/2`; 체크포인트는 `diagnostic_checkpoint.mss`로 격리하고 `normal_play_checkpoint_eligible=false`다. 정상 날짜/대회 알림 발생·branch selection·진행·저장 검증이 아니다. 게임/원본 데이터의 넘버맨 대사를 다른 내비로 영구 변경하지 않았다.

## 재현

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_004_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004
```

새 출력 이름/새 runtime prefix를 사용해 기존 결과를 보존한다. 재현/QA 도구: `prepare_pending500_004.py`, `batch500_004_rom.py`, `verify_pending500_004_rom.py`, `run_pending500_004_alerts.py`, `capture_pending500_004_alert.py`, `verify_pending500_004_alerts.py`.

## 남은 작업

1. 이번500개와 모든 별도 clone source-ID를 제외해 다음500개를 선정·적용한다. 이미 한국어 공통 이름으로 표시되는111별칭도 새 번역으로 세지 않는다.
2. 신규 대상의 실제 소비 경로별 대표 runtime를 확대한다. 선택지 합산 배치 및 native branching은 이번 alert6개 진단에서 검증하지 않았다.
3. 이전 장비 오류70..75, 파이어맨/블루스 실화면, 자연 진행·보상·저장 QA는 별도 미완료 그대로다. 이전 거츠맨 실화면 증거는003 ROM에 바인딩돼 있으며 새004에서 재실행했다고 주장하지 않는다.
4. 이전4미해결 `6E1554:0:0`,`6E1CC0:0:0`,`6E21B0:0:0`,`6A5578:10:0`는 소비 경로/닉네임 합산 모델을 먼저 증명한다.
5. 한글 자동 조합 및 사용자 문자열 저장/재표시 ABI는 여전히 미통합이다. native 일본어 자판 회귀 통과를 실제 한글 자판 완료로 쓰지 않는다.

전체 자연 진행·전체 선택지/이벤트·저장·음성·실기·최종 문구/미감 승인 미완료. 전체 미번역 잔여 수나 전체 한글화 완료를 이번500개 선정 결과로 단정하지 않는다.
