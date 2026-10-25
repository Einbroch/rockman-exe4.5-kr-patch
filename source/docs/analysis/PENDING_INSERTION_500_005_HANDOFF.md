# 묶음005 — 미적용500개 실제 누적 ROM 반영

정책 `development-draft; NON-DISTRIBUTION`. create-kr-patch의 immutable source/원본 ID/재삽입/누적 빌드·검증 경로를 사용했다. 기존 초안500개 적용이지 새500개 문구 작성이나 전체 게임 번역 완료가 아니다. 새 BPS/xdelta/ZIP은 사용자 재요청 전까지 생성하지 않는다.

## 현재 결과

- ROM `poc/output/exe45_ko_development_pending500_005_v1.gba`
- 독립 재빌드 `poc/output/exe45_ko_development_pending500_005_v1_repro.gba`, 전체 바이트 동일
- SHA256 `ed3b526e6b5b11e9c68c6d26562784d97aa69f5ee617bb1d83fac8ef3a685bea`
- 누적4,837→5,337개, 주152→183아카이브, catalog 미변경549개
- 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 보존
- 이전004 ROM SHA256 `9492ab8b6ba422ad629784e312a990c0683f43983d6e504f9f3699bdd79ef427` 및 모든 이전 컴파일 페이로드 보존
- 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 보존, 새 배포 파일0개

## 500개 범위와 소비 계약

`pending_insertion_500_005_selection_v1/selection.json`의 정확한500 source-ID를 적용했다. 31 raw 아카이브:6AAB54,6AED8C,6B525C,6B5A70,6B5B1C,6BB2A4,6BBAF8,6BBBBC,6BC344,6BFF50,6C0E38,6C1710,6C2E4C,6C6828,6C7084,6C7128,6CBFC0,6CC8D0,6CD0B4,6CD9E4,6D0A08,6D1984,6D2180,6D2230,6D27EC,6D32EC,6D59B8,6FE8D4,776198,776650,6808C4.

모든 주 및 별도 clone의 기존 적용 ID/아카이브를 제외했다. 선택한 script의 일본어 리터럴 전체를 대상으로 하고 동적 print 포함 script는 제외했다. 새 개별 줄 배치 변경 없음; 번역 단어·순서·숫자·줄 수, option/select/flag/jump/keyWait 등 명령과 값도 보존했다.

원본 raw payload를 확장 ROM에 배치하고 확정 catalog의32비트 포인터를 전부 갱신한다. 압축 pool/RAM 용량/저장 구조 확대나 새 후킹 없음. 기존 선택기·코드·font의 재배치 종속 주소는 누적 원본 기반 빌드에서 다시 계산하고 Expected Write/ISA 검사를 유지한다.

`pending_insertion_500_005_preflight_v1/preflight.json`: 원본 native 바이트 왕복, 의미/바이너리 왕복, command skeleton, unselected scripts exact bytes, font/mapping, 16bit table extent, 최대3행/보수적132px 검사 PASS. 원래 번역 초안 파일 불변.

## 검증

- `pending_insertion_500_005_rom/integration_v1.json`: 실제500-ID 추가/기존 누락0, 이전152개 주 및 모든 별도 컴파일 payload 보존, 신규31개 hash/포인터/ID 계약 및 독립 재빌드 PASS
- `selector_cpu_v1.json`: 메일/keyitem/3장비 선택기3,195조건 PASS, 합성 CPU 벤치이며 실제 플레이 조건 아님
- `startup_audit_v1.json`: 최종 누적 변경·선택 자산·포인터 및 이전 부팅/자판/타이틀 소비 경계 감사 PASS
- `normal_runtime_v1.json`: 해당 ROM 소유 cold boot→날짜/이름/초기 설정→기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23쪽/목록 복귀/재열기 PASS
- `first_mail_pages_v1.png`: 첫23쪽 직접 시각 검사
- `display_runtime_v1.json`, `display_pages_v1.png`: 신규 통신 오류 선택지 `776650:0:0..2` 및 아쿠아맨 `776198:6:0..2` 표시 진단. 각 글자의 ROM stream/실제 font CPU reads/font 공급/OBJ VRAM와 화면 픽셀 대응 PASS. 통신 선택 `EC06800102FF` 정확한 select 경계 및 native cursor44,122→44,136→44,122 확인. 아쿠아맨3쪽의 정확한 E600 대기 경계와 빈 영역 지움 PASS. 실제 초상/화살표/커서/문구 직접 시각 검사
- 기존 명시적 페이지 회귀5tests PASS

## 표시 진단의 범위와 격리

정상 신규 ROM checkpoint `poc/runtime/pending500-005-v1-complete`의 Rockman 상태에서 R 대화 진입을 사용한다. native PET root pointer080380D0의 read를 대상 raw clone으로 한 번 alias하고, initializer0804FB76의 script0 table read를 지정 script offset으로 한 번 alias한다. 확인한 native caller08037F20/r1=0, normal context0200FA20, Navi0과 exact original bytes를 유지한다.

generic initializer0804FB58..70은4개 buffer를 저장하고 contextD8을 zero-fill한 후 복구한다. exact source bytes `ae6d0fb45046c06ad821b0f7d3fe0fbcea642b656c65ae65`; 표시는 이전 PET position을 승계하지 않는다. target script의 원래 mugshotShow/msgOpen `F40017E700`(Rockman 통신 오류), `F40028E700`(AquaMan 대사)를 실행한다. 실제 context+18/+19 origin52/110과 화면 타일을 검사했다.

통신 오류 script의 원래 flagClear7730/7731는 게임 자체가 실행한다. observer가 ROM/RAM/flag를 직접 쓰지는 않는다. 위/아래 이동만 수행하며 선택 확정은 하지 않는다. 아쿠아맨은3번째 keyWait에서 멈추므로 뒤의 jump7 및 HP 보상 경로는 시험하지 않는다. Rockman PET 배경에 AquaMan mugshot이 나타나는 것은 원본 AquaMan script 렌더링 격리 진단이며 native acquisition 또는 원래 게임의 Navi 변경 증거가 아니다. ROM 자체의 대사/내비 mapping을 다른 인물로 바꾸지 않았다.

증거 `poc/runtime/pending500-005-v1-display-communication/aqua`; `normal_play_checkpoint_eligible=false`, checkpoint는 `diagnostic_checkpoint.mss`로 격리한다. 실제 배틀 통신 실패·후속 선택 결과·칩 장착·보상·저장을 검증했다고 쓰지 않는다. 신규6리터럴만 직접 runtime 관찰했으며500개 전체 자연 scene QA로 확대하지 않는다.

## 재현과 재개

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_005_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005
```

다음 선정은 현재183개 주/별도 clone의 original-ID 합집합을 제외하고 진행한다. 111개 공통 장비 이름 별칭은 신규 적용으로 다시 세지 않는다. 기존 결과/증거를 덮어쓰지 않도록 새 출력 이름·runtime prefix를 사용한다.

남은 것: 다음500개 실제 삽입, 전체 자연 진행·선택 확정·임무·보상·저장 QA, 이전 장비 오류70..75/파이어맨·블루스 실화면,4미해결 `6E1554:0:0`,`6E1CC0:0:0`,`6E21B0:0:0`,`6A5578:10:0`의 소비/닉네임 합산 모델, 실제 한글 자동 조합·저장·재표시 ABI. native 일본어 자판 회귀 통과를 실제 한글 자판 완료로 쓰지 않는다. 모든 이전 runtime 근거는 원래 ROM 해시에 귀속한다.

음성·실기·전체 gameplay·최종 문구/미감 승인 미완료. 전체 미번역 잔여 수 및 전체 한글화 완료를 이번500개 선정 결과로 단정하지 않는다. 검증 당시 재빌드가 아직 실행 중인 첫 startup-audit 호출은 산출물이 없다는 조건으로 거부됐고, 재빌드 완료 후 같은 ROM 감사와 정상 검증은 PASS했다.
