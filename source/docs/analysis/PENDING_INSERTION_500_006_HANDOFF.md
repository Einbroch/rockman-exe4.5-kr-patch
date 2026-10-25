# 묶음006 — 기존 미적용500개 실제 누적 ROM 반영

정책 `development-draft; NON-DISTRIBUTION`. create-kr-patch의 원본 보존/명시적 문자 공급/재삽입/누적 빌드·검증 절차를 적용했다. 신규 번역500문구 작성이 아니라 기존 미적용 초안500개를 실제 ROM에 반영했다. 별도 패치 파일은 사용자 재요청 전까지 생성하지 않는다.

## 현재 결과

- ROM `poc/output/exe45_ko_development_pending500_006_v1.gba`
- 독립 재빌드 `poc/output/exe45_ko_development_pending500_006_v1_repro.gba`, 전체 바이트 동일
- SHA256 `02d14a3ead55aa2d52f9458b095384c50c7c92683f82ae08a685c794bb8edc69`
- 누적5,337→5,837개, 주183→270아카이브, catalog 미변경462개
- immutable 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 보존
- 이전005 ROM SHA256 `ed3b526e6b5b11e9c68c6d26562784d97aa69f5ee617bb1d83fac8ef3a685bea` 및 이전 모든 컴파일 페이로드 보존
- 기존 ZIP SHA256 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 보존, 새 BPS/xdelta/ZIP0개

## 적용 범위

정확한 source-ID500개와87개 raw 아카이브는 `pending_insertion_500_006_selection_v2/selection.json`에서 고정한다. 준비 검사 authority는 `pending_insertion_500_006_preflight_v2/preflight.json`이다. 기존 주 및 모든 별도 clone 소비자 ID/아카이브는 선정에서 제외했다. 이미 공통 장비 이름으로 표시되는111별칭도 새 적용으로 세지 않는다.

선택한 script의 일본어 리터럴 전체를 대상으로 하며 동적 print 포함 script는 제외했다. 원래 번역 초안 파일·단어·순서·숫자·줄 수 및 원본 option/select/flag/jump/keyWait 명령·값은 변경하지 않았다. 개별 추가 줄 배치도0개다.

각 raw payload를 확장 ROM에 배치하고 확정 catalog의 모든 해당32비트 포인터를 갱신했다. 압축 pool/RAM 용량/저장 구조 확대나 새 후킹 없음. 기존 후킹·font·guard clone의 재배치 주소는 동일한 누적 빌드 경로에서 계산한다.

## 가운데점 인코딩 gap

첫 준비v1은 `7A7000:0:1`의 `·`가 문자표에 없으므로 거부됐다. v1 selection/중간 compile 증거는 보존했으며 ROM을 만들지 않았다. 문자 누락/공백 치환/다른 점으로 대체하지 않았다.

분석 선정기가 기존 native table, 전체 Hangul 및 현재 명시적 추가 문자 집합과 비교하도록 보완했다. 미지원 문구19개는 v2 selection의 `deferred_unmapped_literals`에 원래 ID/문자/초안 경로/이유를 기록했다. 이19개는 이번 후보 분석에서 발견한 인코딩 gap이지 전체 미번역 잔여 수가 아니다. 해당 문구를 포함한 script 전체를 제외하고 다른 complete-script 단위로 정확한500개를 다시 구성했다.

`7A7000`은 script2/3/34/52의8개만 이번에 적용했고 미지원 script0을 포함한 비선택 script는 원본 바이트로 보존한다. 다른 `·` 문구도 원본/초안은 불변이며 후속 지원 대상이다. 새 인코딩/글꼴 자리를 추가하려면 `korean_codec.py`, TextPet plugin, 공급 bank/advance, 독립 decoder, normal 소비 및 jamo 표시 경계를 함께 검증해야 한다. 현재 `hangul_editor_display.py`의 JAMO_BASE는 추가 문자 수에서 파생되므로 고정 인덱스를 임의 덮어쓰지 않는다.

## 검증 근거

- `pending_insertion_500_006_rom/integration_v1.json`: 전체 source-ID 합집합에서 정확히500개 추가/기존 누락0; 이전183개 주 및 모든 별도 컴파일 페이로드 byte identity; 신규87개 payload hash/포인터/ID 계약, 독립 재빌드 동일 PASS
- `selector_cpu_v1.json`: 메일/keyitem/3장비 선택기3,195조건 PASS, 합성 CPU 벤치이며 자연 플레이 증거 아님
- `startup_audit_v1.json`: 최종 누적 변경·자산·포인터·부팅/자판/타이틀 보호 영역·재현 감사 PASS
- `normal_runtime_v1.json`: 새 ROM 소유 cold boot→날짜/이름/초기 설정→기존 일본어 자판3페이지→네 내비 선택→첫 I.P.C. 메일23쪽/목록 복귀/재열기 PASS
- `first_mail_pages_v1.png`: 해당23쪽 직접 시각 검사
- `number_runtime_v1.json`, `number_pages_v1.png`: 신규 `68787C:2:0..1` 및 `68C2CC:3:0..1`의 정확한 E600 대기/ROM stream/한글·구두점 font CPU reads·공급 bank/OBJ VRAM 및 화면 픽셀 대응, 매 페이지 빈 영역 지움 PASS. 실제 넘버맨 초상/문구/화살표 직접 시각 검사
- 기존 명시적 페이지 회귀5tests PASS

## 표시 진단 범위

동일 새 ROM의 정상 초기 설정→넘버맨8 선택/소개 완료 checkpoint `poc/runtime/pending500-006-v1-number-complete`를 사용한다. 원래 NumberMan PET table080382B0의 read를 지정 raw clone으로 한 번 alias하고, native initializer0804FB76의 script0 table read를 각각 return2/draw3 offset으로 한 번 alias한다.

caller08037F20/r1=0, normal context0200FA20, native Navi8 및 target 원본 window prefix `F6000A0C01E702F6025C6E03F604E18D`를 검사한다. target의 원래 box/text/arrow 설정을 실행하고 실제 text origin92/110을 검증했다. observer가 ROM/RAM/flag/date/Navi 값을 직접 쓰지 않는다. 원본 게임의 인물·대사 연결을 다른 내비로 영구 변경하지 않았다.

증거 `poc/runtime/pending500-006-v1-number-return/draw`; `normal_play_checkpoint_eligible=false`, checkpoint는 `diagnostic_checkpoint.mss`로 격리한다. 이는 표시 소비 진단이지 실제 jack-out 패배/배틀 무승부/보상/저장 증거가 아니다. 신규4리터럴만 runtime 관찰했으며500개 전체 scene QA로 확대하지 않는다.

## 재현과 다음 작업

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_pending500_006_fresh --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui --pending-batch500 --pending-batch500-002 --pending-batch500-003 --pending-batch500-004 --pending-batch500-005 --pending-batch500-006
```

새 출력 이름과 runtime prefix를 사용해 현재 증거를 보존한다. 다음 선정은 주270개/모든 별도 소비자의 적용 ID를 제외한다. 이미 일부 적용한 아카이브의 미적용 script도 남아 있으므로 아카이브 제외만으로 전체 미번역을 계산하지 않는다. 이들을 추가할 때는 기존 선택 scope와 새 ID를 명시적으로 병합하고 이전 byte/명령 보존을 검증한다.

다음 핵심: 가운데점 지원 및 보류19문구 재검사, 다음500개 실제 삽입, 전체 자연 진행·선택 확정·임무·보상·저장 QA, 이전 장비 오류70..75/파이어맨·블루스 실화면,4미해결 `6E1554:0:0`,`6E1CC0:0:0`,`6E21B0:0:0`,`6A5578:10:0` 소비/닉네임 합산 모델, 실제 한글 자동 조합·저장·재표시 ABI. native 일본어 자판 회귀 통과를 한글 자판 완료로 쓰지 않는다.

실기·음성·전체 플레이·최종 문구/미감 승인 미완료. 이전 runtime 증거는 원래 ROM 해시에 귀속하며 이번 artifact의 전 장면으로 일반화하지 않는다. 전체 한글화/배포 승인을 이번500개 적용 결과로 단정하지 않는다.
