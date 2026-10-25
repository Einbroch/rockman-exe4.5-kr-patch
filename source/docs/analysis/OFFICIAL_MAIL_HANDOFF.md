# 오피셜 메일 본문 3통 적용 (2026-10-13)

## 누적 산출물

ROM `poc/output/exe45_ko_development_official_mail_v1_r2.gba`, 11,229,216바이트.
SHA256 `e4c56544b754c84f464797d20657f88f7562f017c874c74d7f3ca0af2f024fbd`.
독립 `_repro.gba` 전체 바이트 동일. 원본 ROM/사용자 SAV 변경 없음.
누적 선택 번역 2,710개/66아카이브, 미선택 아카이브 666개.
이번 추가는 `6DD9AC` scripts1/2/3의 본문 7+13+12개=32개이며 다른 메일의 전체 한글화가 아니다.
기존 첫 안내 메일/메일함/제목/내비 그래픽/기능 버튼과 앞선 번역을 보존했다.

development-draft; NON-DISTRIBUTION, needs_review. 공개 배포 승인이 아니다.

## 선택과 배치

기존 `translations/story_mail_draft_ko.json`에서 세 통 전체를 읽고 선택했다.
source/draft 해시는 `tools/first_mail.py`에서 고정, 선택 입력은 `analysis/official_mail_v1/*_selected_asset.json`.
빌드 플래그 `--official-mail`은 기존 `--first-mail` 대신 지정하며 이전 누적 빌드의 나머지 플래그는 그대로이다.
scripts0/1/2/3 본문55개와 기존 메일함/제목7개를 함께 선택한다.

예외 입력 `translations/official_mail_layout_v1.json`:

- `6DD9AC:2:1`: 단어·순서 유지, 줄바꿈만 조정. 줄 폭 116/144/60픽셀.
- `6DD9AC:2:3`: 원문 `くわしくはちょうさ中だが、 / ダークロイドのじょうほうが / いっぱんに もれないように`에서 개별 번역 후보를 작성.
  `자세한 건 조사 중이나, / 다크로이드의 정보가 / 외부에 새지 않도록`, 144/116/112픽셀.
  자세한 조사 진행과 정보 유출 방지 의미를 유지하는 후보이며 사람의 문구·표시 승인은 미완료다.
  자동 일괄 축약 규칙은 사용하지 않았다.

본문은 기존 위치70/80, 3줄/152픽셀, 마지막 줄132픽셀 상한을 유지한다.
새 해제 본문5,961바이트 < 원래 RAM 목적지 `0202B2F4`의8,192바이트 한도, 다음 자산 `0202D2F4`를 침범하지 않는다.
원래 type-10 BIOS 디코더와 목적지, 원본 압축 슬롯, 포인터 배열 인구, 플래그 명령, 대기/넘김 순서를 보존했다.
기존 `first_mail_v2`와 비교해 본문의 scripts1/2/3 외 모든 스크립트 바이트가 동일하고 두 메일함/제목 페이로드도 동일하다.
이전 글꼴 은행과 아카이브/예상 원본 쓰기 집합/최종 압축·포인터를 독립 감사했다.

## 실제 검사와 증거 범위

`poc/runtime/official-mail-v1-r2-{boot,pagecycle,complete,read,selection}`:
이번 ROM의 처음부터 경로, 자판 세 페이지, 프로필, 네 내비 이동/확인/취소, 첫 메일23쪽/완료/재열기를 일반 입력으로 회귀 검사했다.
이번 ROM에서 생성된 상태와 해시 고정 격리 Mesen만 사용했다.
기존 첫 메일23쪽과 추가 오피셜32쪽의 화면을 전부 검토했다.

`...-official1/2/3`은 **격리 진단**이다. 게임 진행으로 오피셜 메일을 수신한 것이 아니다.
실제 메일 로더가 현재 확장 ROM에서 원래 RAM으로 해제한 뒤, 원래 초기화 코드의 `0804FB76` 표 읽기 한 번만 script0 상대 오프셋 대신1/2/3 오프셋을 반환했다.
진단 콜백은 RAM/ROM 바이트를 쓰지 않으며 패치·제품 빌드에 들어 있지 않다.
각 스크립트 원래 flagClear623/624/625는 격리 세션에서 그대로 실행된다. 사용자 SAV는 사용/변경하지 않았다.
원래 파일·메모리 로더/대기·페이지 넘김·종료는 실행했지만 수신/획득 조건·호출자 선택·진행 경로·해당 발신자/제목 연결·저장 호환은 증명하지 않는다.
진단 상단 헤더는 첫 I.P.C. 메일 그대로이며 발신자/제목 번역 검증으로 사용하지 않는다.

기존 key-item 전용 가드가 초기화 진입 `4FB4C..58`을 재배치하므로 원본 동일성 가드를 무작정 완화하지 않았다.
`keyitem_rom_data.verify_final`로 기존 selector/stub/기계 코드/최종 배치를 검증한 뒤 원래 재개 구간 `4FB58..84`와 메일 로더를 확인한다.
메일 RAM 루트는 두 key-item 가드 루트와 다르며 native branch를 따른다.
진단 상태는 `diagnostic_checkpoint.mss`로 격리했고 `normal_play_checkpoint_eligible=false`로 표시했다.

기계 검사 `tools/verify_official_mail_runtime.py`:

- scripts1/2/3의 고유 literal/keyWait와 순서32개, 원래 clearMsg 경계/페이지 bookmark 검사.
- 모든 본문 페이지에서 본문/메일함/제목3개 전체 RAM이 현재 ROM 해제 결과와 바이트 동일.
- 대기 opcode 주소와 끝난 후 native inactive/목록 복귀 상태 검사.
- 개입1회, 현재 ROM·상태·에뮬레이터·전체 증거 해시 바인딩.

결과 `analysis/official_mail_v1/runtime_verification.json`.
`official_mail_display_diagnostic_verified=true`, `official_mail_acquisition_verified=false`, `official_mail_header_correspondence_verified=false`.
기존 소비자/원본 가드·선택 인구·배치 거부4개 테스트와 독립 빌드 동일성 PASS.
실패 빌드 `official_mail_v1`은 미등록 scope_variant 거부로 ROM을 만들지 않았고 작업 폴더를 보존했다.
진단의 초기 원본 초기화 가드 거부도 기존 key-item hook에 대한 검사 모델을 수정한 것이며 제품 ROM 변경은 없었다.

## 개인 테스트 패키지

`patches/exe45_ko_development_official_mail_20261013.zip` 및 동명 폴더.
ZIP SHA256 `fec407009e9f2008b9fffe451a6b90488c4becaef2bcfe2196da8e704d4fc21d`.
BPS SHA256 `20c37b771e43da5c89bcb11922570c7c8b4b52e918b4528f19a9a7150ad5e585`.
xdelta SHA256 `77cfac4ff93ac7269d754a841749d1eafa0d6e70f68f2347054bc1fce2a36cbe`.
원본 ROM SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`에 두 형식 중 하나만 적용한다.
패치 ROM에 겹쳐 적용하지 않는다. ROM/SAV/실행 파일은 패키지에 없다.
전체 바이트 동일 재적용/결정적 패치/틀린 원본·손상 패치 거부/적용 스크립트 출력 덮어쓰기 거부 PASS.

## 재개 지점

메일 아카이브 초안120개 중55개 본문 적용, scripts8..14의 뉴스/초대65개는 아직 미적용이다.
다음은 본문 전체 용량·페이지/변수 조합·인명 삽입 폭을 측정해야 한다. 기존 버퍼 한도를 임의로 늘리지 않는다.
오피셜 발신자/제목과 다른 내비 메일함 분기도 남아 있다.
가나 글자판, 한글 자동 조합/이름 저장, 전체 초안 통합, 실제 오피셜 수신/전 게임 플레이/공개 승인도 미완료다.
