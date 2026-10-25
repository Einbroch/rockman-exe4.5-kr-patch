# 임무 메일 헤더 후속 작업 인계

## 현재 결과와 입력

현재 ROM: `poc/output/exe45_ko_development_mission_mail_header_v1.gba`.
SHA256 `21565ad0db0cbdd25be1326cbed047febf25eb50a1873535833928d34326f389`.
독립 재빌드 `_repro.gba` 전체 바이트 동일. 누적2,837개/67아카이브, 미선택665아카이브. 전체 한글화 완료를 뜻하지 않는다.
이전 ROM `exe45_ko_development_full_mail_header_v1_r3.gba`의66개 아카이브 컴파일 내용은 모두 동일하다.

문구 권위는 `translations/batch500_016_mailhead_6DD864_draft_ko.json`이며 SHA256 `2ea08f800bee7708ee3fb591eb9b2ed2a77d577dc723647642f69086dbe43bc4`.
42개 ID의 원문/번역/needs_review 상태를 그대로 사용했다. 새 문구 치환은 없다.
파생 빌드 선택 입력 `analysis/mission_mail_header_v1/6DD864_selected_asset.json`, 구현 `tools/mission_mail_header.py`.
원문44개 중40/64의 `FROM:`은 그대로, 나머지42개는 한국어다. 0..39는20쌍의 발신자·제목이며41/65는 제목 접두어다.
개발 전용 NON-DISTRIBUTION·release_eligible=false 유지.

## 소비 경로와 적용

원본 `0804054A`는 context(r5)+10의 내비 인덱스를 읽고, `08040550`에서 `0804057C + index*4`의 압축 헤더 포인터를 읽는다.
인덱스27의 포인터 파일 위치 `405E8`가 `086DD864`다. `08040554`의 BIOS type10 호출은 `020262F4`에 풀며 기존4096바이트 한도를 유지했다.
원본 raw516/압축183바이트 → 한국어 raw964/저장1092바이트. 고정 셀 한 줄 최대48px/허용88px.
빌드가 신규 압축 아카이브를 꼬리에 배치하고 원본 포인터 한 곳을 선언된 쓰기로 갱신한다. 원래 압축 데이터·로더 명령·임무 본문·진행 제어는 수정하지 않는다.
원문 테이블66슬롯과 미선택 스크립트/영문 접두어 보존. 20쌍은 짝수/홀수별 같은 컴파일 스트림이며41/65도 같은 스트림이다.

주 빌드는 다음과 같다. 도구/선택 입력 해시는 출력 JSON에 기록된다.

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name exe45_ko_development_mission_mail_header_v1 --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining --calendar-date-save --save-initialize --hangul-keyboard-glyphs --native-keyboard-labels --navi-card-graphics --news-mail --mail-rom-reader --full-mail-body --full-mail-header --mission-mail-header --title-menu-graphics --title-weekend-menu --startup-ui
```

기존 출력은 덮어쓰지 않는다. 재빌드는 `--name`만 새로운 이름으로 지정한다.
이 기능은 `--full-mail-header --news-mail` 누적 선택을 요구한다. BPS/xdelta/ZIP 생성 단계는 실행하지 않았다.

## 검증과 증거

- `mission_mail_header_v1/static_scope_verification.json`: 기존66아카이브 유지, 신규42원문/번역·포인터·압축/버퍼·20동일 스트림 쌍·접두어·미선택 스크립트 보존 PASS.
- `mission_mail_header_v1/static_verification.json`: 누적 최종 차이·선언된 쓰기·선택 입력 해시·원본 보호·독립 재빌드 PASS.
- `mission_mail_header_v1/cpu_verification.json`: 합성 CPU 선택기867조건 PASS. 실제 GBA 진행 증거와 구분.
- 기존 메일 자산7/전체 본문4/선택기4 단위 테스트 PASS. 신규 선택 검사는 정상 입력 허용과 문구 변경/누락/원문 변경/상태 변경의 네 결함 거절을 확인.
- `mission_mail_header_v1/runtime_verification.json`: 동일 ROM의 정상 cold boot, 초기 설정, 자판3페이지, 네 내비 카드, 첫 I.P.C. 메일23쪽·목록 복귀·재열기 PASS.
- `mission_mail_header_v1/normal_gallery/index.json`: 정상61개 캡처/7시트 직접 검사. 기존 표시 내용과 진행을 유지하며 새 깨짐/잘림 없음. 일본어 자판의 실제 글자 배열은 아직 남아 있다.
- `mission_mail_header_v1/header_runtime_verification.json`: 실제 신규 압축 아카이브가 RAM에 정확히 풀렸음을8/9/10화면에서 확인. 목록에 `작전 사령부 / 임무 지령`, 상세에 `FROM: 작전 사령부 / 제목: 임무 지령` 표시. NEW 겹침·칸 침범·잘림 없음.

임무 진단은 같은 ROM의 정상 complete 체크포인트에서 `08040550`의 인덱스0 포인터 읽기 한 번만 인덱스27의 새 포인터로 반환한 격리 실험이다.
ROM 파일/게임 RAM/진행 플래그를 직접 쓰지 않았다. BIOS 로더와 헤더 출력기는 실제 게임 경로로 실행했다.
본문은 일부러 록맨 첫 I.P.C. 메일 그대로이므로 임무 본문이 표시·번역됐다는 증거가 아니다.
격리 상태는 `poc/runtime/mission-mail-header-v1-diagnostic/diagnostic_checkpoint.mss`이며 normal_play_checkpoint_eligible=false. 정상 진행에 재사용하지 않는다.

원본 ROM 해시 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`, 기존 뉴스 메일 ZIP 해시 `2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6` 불변.

## 남은 작업과 재개 지점

임무 수신 플래그·실제 내비27의 헤더/본문 연동·임무 진행/저장/재열기는 미검증이다. 격리 표시는 자연 수신을 대신하지 않는다.
다른 내비 전용 헤더 `6DD718/6DD798/6DD804/6DD91C`, 임무 본문 초안, 미선택 일본어·이미지, 한글 자동 조합과 저장/재표시도 남아 있다.
다음은 이들 전용 헤더의 원문 ID·실제 로딩 포인터·표시 폭을 확인해 기존 초안을 선택하거나, 실제 임무 수신의 writer/flag 경로를 추적한다.
사용자 지시: 요청 전까지 패치 패키지는 만들지 않고 통합 ROM 작업만 한다.
