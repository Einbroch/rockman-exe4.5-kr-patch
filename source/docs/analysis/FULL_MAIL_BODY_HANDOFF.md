# 메일 본문 잔여43개 ROM 적용 (2026-10-13)

사용자 지시: 한글화는 ROM에 반영한다. 사용자가 다시 요청하기 전에는 BPS/xdelta/ZIP 등 배포 패키지를 만들지 않는다. 이번에는 패키징을 실행하지 않았다. 원본·기존 ROM·사용자 SAV·기존 패키지를 보존했다.

## 최신 통합 ROM

`poc/output/exe45_ko_development_full_mail_body_v1_r2.gba`, 11,239,012바이트.
SHA256 `7eee4265c0c0177d65255ecf7c2af31c1cfc0e2301191551e2ec45f67986617d`.
독립 `_repro.gba` 전체 바이트 동일.
누적2,775개 문구/66아카이브,666아카이브 미선택. 전체 게임 한글화 완료나 공개 릴리스가 아니다.

기존 초안의 뉴스4~6호 및 오피셜 토너먼트 초대 메일43개를 추가했다.
공통 본문 `6DD9AC`의120개 리터럴을 전부 선택했다. 다른 내비의 별도 메일 본문·발신자/제목 전체 적용 완료를 뜻하지 않는다.
기존77개 문구는 그대로다. `translations/full_mail_body_layout_v1.json`의 네 개별 줄 배치만 조정했으며 단어·숫자·구두점은 바꾸지 않았다.
뉴스4/5호 제목은 명시적으로2행→3행, 다른 두 문구는3행 내 재배치다. 페이지/wait/퀘스트/플래그/이름 명령은 그대로다.
입력은 `analysis/full_mail_body_v1/6DD9AC_selected_asset.json`, development-draft; NON-DISTRIBUTION / needs_review / release_eligible=false다. 사람의 문구·표현 승인 대기다.

## 용량 문제 해결과 이름 삽입

전체 본문은8,531바이트로8,192바이트 RAM 한도를339바이트 넘는다. 한도를 늘리지 않았다.
기존 압축 로더·목적지 `0202B2F4`와 bounded77의7,005바이트를 유지한다. 추가 RAM 버퍼·영구 상태·추가 압축 해제는 없다.
raw-ROM clone `08AB5C1C`에 전체120개를 놓고 기존 guarded reader로 읽는다.
clone SHA256 `e27e4ffce557bf832ed0962403ab35dd388270b9b2ee5122e74e507cc3b75c1f`.
guard는 로딩된 bounded77 헤더 `4000ef06c608880c1110111011101110`를 사용하며 전체 clone 헤더와 독립적으로 선언된다.
RAM 루트/호출 LR/16바이트 헤더/unsigned8bit script0..31 조건은 기존 PoC와 같다. 다른 호출·다른 내비의 본문5종·키 아이템 경로는 native fallback을 보존한다.

새43개 중 이름을 삽입하는 페이지는5개다. `printPlayerName`은 F90C1F/descriptor31, 원본 `080527C8`의 포인터 `02000E51`/복사13바이트다. 닉네임·약한 과목 필드와 혼동하지 않았다.
실제 이름 입력 초기화 `08039E34`는 r0=6을 `080355B6`에 전달하고 editor+4에 제한을 저장한다. `08035494`→`08035620`의 현재 글자 수 비교가6글자에서 추가 입력을 거부한다. 2바이트 editor 슬롯을 `0803562C`에서 원래 표현으로 압축한다.
보수적으로6글자×12px=72px로 모델링했다. 새 합산 행의 최대 폭95/95/108/128/84px, 최대3행이며 셋째 행은 진행 화살표를 피해132px 이내다. 해당 producer/descriptor 원본 바이트와 최종 ROM 불변을 빌드에서 검사한다.
이는 원래 이름 표현의 검증이지 자동 한글 조합·한글 이름 저장 ABI 채택이 아니다.

## 실제 검증과 범위

- `analysis/full_mail_body_v1/static_verification_r2.json`: 입력/제어/숫자/글꼴/배치/포인터/최종 쓰기·기존 모든 bounded 아카이브·키 아이템 clone 보존, 전체 바이트 재현 PASS. 원래8MiB의 이전 ROM 대비 차이는 shared reader veneer12바이트뿐이다.
- `analysis/full_mail_body_v1/cpu_verification.json`: 최종 ROM의 합성 CPU867조건 PASS. 메일32, 키 아이템196, 변경 헤더160, 범위 밖15, 미확인 호출18, 미확인 루트1, 다른 키 아이템180, 다른 내비 본문265. native zero helper 계약 대체 벤치이며 실제 플레이 증거와 구분한다.
- `analysis/full_mail_body_v1/runtime_verification_r2.json`: 동일 ROM 새 게임·초기 설정·자판 기능 버튼/3페이지·네 내비 선택·첫 메일23쪽·목록 복귀·재열기 PASS. 자동 한글 입력/저장 완료는 아니다.
- `analysis/full_mail_body_v1/remaining_runtime_verification.json`: 새43개 리터럴의39쪽을 실제 Mesen 원래 출력기에서 모두 확인했다. 이름 삽입5쪽, native RAM 로딩 데이터 일치, ROM wait/base/bookmark, 순서·종료·목록 복귀 PASS. 실제 이름 샘플은 원래 한 글자 이름이며 최댓값은 별도 source 모델에서 검증한다.
- `normal_gallery/index.json`, `remaining_gallery/index.json`: 캡처/시트 해시와 원래 화면 경로. 정상61장, 잔여47장(본문39+진입4+복귀4), 전 시트 직접 확인.

잔여39쪽은 격리 진단이다. native script-table의 첫 읽기 한 번만 script0→11/12/13/14로 alias한다. 실제 압축 해제와 guarded reader는 그대로 실행한다. 원래 스토리/플래그 명령은 각 독립 QA 세션에서 실행한다. 진단은 ROM에 들어가지 않으며 state는 diagnostic_checkpoint.mss로 격리한다. 정상 수신 조건·해당 발신자/제목·퀘스트 연속 진행·세이브 호환을 증명하지 않는다.

이전 오피셜/뉴스1~3호54쪽은 이번 ROM에서 재실행하지 않았다. 이전 검증 ROM과 각 script1/2/3/8/9/10의 원래 소비 주소/루트/본문 바이트·bounded 로딩 입력이 모두 동일함을 static_verification_r2의 prior54_page_consumption_equivalence에 기록했다. 현재 ROM의 직접 테스트와 이전 증거의 동등성 검사를 구분한다.
shared selector의 현재 회귀는 CPU867조건+정상 첫 메일23쪽+새39쪽이다. 실제 키 아이템 메뉴 경로는 이번에 다시 실행하지 않았다.

## 재현과 다음 작업

이전 최신 메일 recipe 플래그에 `--full-mail-body`를 추가했다. 원본 immutable-source primary builder가 bounded77과 full120 raw clone을 함께 생성한다. 이전 PoC ROM을 다음 빌드 입력으로 사용하지 않는다.
`full_mail_body.py`가120개 선택/기존77개 불변/네 줄 배치/두 제목의 명시적 행 변경/원래 name producer/합산 폭을 소유한다.
빌드 실패 v1은 제목 행 수 정책을 기존 generic replacer가 거부한 기록이다. 해당 보호 검사를 끄지 않고 오직 두 제목의 명시적 정책을 등록해 r2에서 통과했다. 실패 디렉터리·smoke 기록은 보존했다.
테스트 fixture: 기존 selector7·설치4·mail selector4·mail assets6·full mail4 PASS. 이름 producer 변조/문구·ID·상태 변조/이름 합산·화살표 영역 초과를 거부한다.

다음 완료 조건은 여전히 실제 수신·제목/발신자 연결과 다른 내비 메일 분기, 나머지 미선택 번역·그림, 자동 한글 입력/저장 통합이다. 첫 PET 구매 안내 그래픽의 작은 글꼴/촘촘한 자간도 사람의 표현 검토 대상으로 남긴다(이번 메일 변경 전과 동일). 전체 플레이·공개 배포 승인은 없다.
정상 checkpoint는 `poc/runtime/full-mail-body-v1-complete/checkpoint.mss`와 같은 폴더 result.json에 동일 ROM으로 결속되어 있다. 진단 checkpoint를 정상 진행 증거로 재사용하지 않는다.
