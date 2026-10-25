# 현재 작업: 미적용500개 묶음001

다음 500개 묶음002의 선정/컴파일 사전 검사 기록은 `PENDING_INSERTION_500_002_HANDOFF.md`에 분리했다. 묶음002는 아직 ROM 적용0개이며 이 묶음001의 적용/QA 기록을 대체하지 않는다.

사용자 지시: 이후 번역·적용 작업은500개 단위로 묶는다. 마지막 잔여 묶음은500개 미만 가능. 사용자가 다시 요청하기 전에는 패치 패키지를 만들지 않는다.

## 완료 조건과 현재 상태

이 묶음의 완료 조건은 원문 기반 번역 선택, 보호 정보/글꼴/실제 표시·변수 폭 검증, 원본에서 재현 가능한 누적 ROM 적용, 소비 경로별 에뮬레이터 검증이다.
현재는 **ROM 반영500/500, 전체 소비 경로의 표시·변수·자연 진행 QA 미완료**다. 기존 초안을 재사용한 것이므로 새 번역500개 작성으로 세지 않는다.
현재 누적 ROM은 `poc/output/exe45_ko_development_pending500_arrow_v2.gba`, SHA256 `da920efbbd2b965a5e7bbab75ee88242735a8613777f96fb483daf5bad0bd068`, 누적3,337개다. 독립 재빌드 전체 바이트 동일. 이전500개 반영본은 보존했다.
개발 ROM만 생성했고 신규 패치 패키지는 만들지 않았다. 원본과 이전 ROM은 보존했다.

### 후속 보완: 임무 마지막 줄8곳

기존152px 리터럴 검사만으로는 마지막 줄의 화살표 여유132px를 보장하지 못했다.6DE3E0:61:1/63:1,6DF988:34:2/35:1/37:1/38:6/42:5/51:4의 마지막 줄136~148px 수요를 발견했다. 이전 ROM의63번/34번 대표 화면을 `poc/runtime/pending500-arrow-before-*`에 보존했다.
개별 배치 권위는 `translations/pending_insertion_500_arrow_layout.json`이다.8개를 줄만 재배치하고 모든 문자의 순서·숫자·뜻과 LF2개를 유지했다.61:1은 WWW 바로 뒤 괄호 앞에서 줄을 나눈다. 대량 문구 변환이나 단축은 하지 않았다.
`tools/prepare_pending_batch500.py`의 r4 준비 검사에서500개 왕복·미선택 보존·문자 매핑과 마지막 줄132px 검사 PASS.6DE3E0은14,633바이트(+1),군사10,636/파괴4,931바이트는 이전과 같은 크기다. 주 빌드가 세 본문 모두 마지막 줄132px 위반을 거절한다.
`tools/mission_reward_model.py`는 원본5그룹·64레코드·32고유 임무의 보상 테이블을 검사한다. 제니1000/1500/2000/2500/3000/3500/4000/4500,버그 조각3~10,HP메모리 이미 소지 시 제니1000 대체다. 제니 삽입 둘째 줄 최대90px/152px,버그 조각 삽입 셋째 줄108px/132px PASS. 다른 버퍼나 소지 한도를 상한으로 쓰지 않았다.
`arrow_reward_cpu_v1.json`: 원본 EE38/684B0 처리256조건 PASS. 소지 여부 검사와 jump helper는 대체한 합성 CPU 검사로, 실제 획득·보상 수령·화면·저장 증거가 아니다.
처음 모델에서 HP 소지 대체량을2000으로 잘못 기입했으나 CPU 실행의 실제1000과 불일치해 거절했다. 모델을1000으로 고쳐 v2 메타데이터를 재빌드했다. v1/v2 ROM 바이트는 동일하지만 현재 문서·메타데이터 권위는 v2다. v1과 v2 전체 바이트 동일성을 통해 v1 런타임 자료를 v2에 연결했다.
`arrow_integration_v2.json`: 원본과 기존67개 컴파일 페이로드 보존,500개 선택/컴파일 바인딩, 재빌드 동일 PASS. `arrow_selector_cpu_v1.json`:990조건 PASS.
`arrow_normal_runtime_v2.json`: 같은 ROM 해시의 `pending500-arrow-v1-*` 정상 입력 경로에서 초기 설정·기존 자판3페이지·네 내비 OAM·첫 메일23쪽·목록 복귀·재열기 PASS. 새 조합 자판/저장 지원 증거가 아니다.
수정8곳 전체의 격리 native-loader/table alias 실행은 `poc/runtime/pending500-arrow-after-*`, 정확한 번역/대기 포인터/줄 폭 검사는 `arrow_runtime_v3.json`에 기록한다.8곳 모두 v3 비교표에서 본문 패널과 화살표 여유를 시각 확인했다. 자연 임무 수신·진행 QA와 구분한다.
v2 화면 검증은 오피셜 두 본문의 진입 setup 누락 때문에 거절했다.61/63번은 자체 위치 명령이 없으므로 원본 script0의 positionText/positionArrow/positionMugshot/mugshotShow를 실행한 뒤 jump32의 원본 테이블 읽기0804FD20에서만 대상 스크립트로 별칭 처리했다. `pending500-arrow-after-setup-25-61/63`에서 원본 위치·SciLabMan 초상화가 복원됐으며 native wait 포인터까지 재검사했다. 다른 여섯 군사 본문은 자체 setup이 있어 기존 진단을 유지했다. 과거 오피셜 직접 진입 스크린샷과 before25-63은 표시 위치의 근거로 사용하지 않는다. before27-34는 자체 setup을 거쳐 이전 마지막 줄의 대표 비교로 유효하다.
다음 주요 재개 지점은 등록 제목의 printMailBuffer, 보상 페이지의 printCurrentNavi/printItem 소비와 전체 자연 진행이다. 새 패치 패키지는 요청 전까지 만들지 않는다.

### ROM 통합 증거

`pending_insertion_500_rom/integration_v2.json`: 기존67개 페이로드 동일, 기본71개 아카이브, 추가 본문 clone3개,500개 선택 ID/컴파일 해시 일치, 원본 본문 로더/포인터 보존, 재빌드 동일 PASS.
`pending_insertion_500_rom/selector_cpu_v2.json`:990조건 PASS. 원래 공통 메일/키 아이템 및 미선택 내비 경로 유지, 선택 임무 전체 스크립트, 각 헤더16바이트 변형, 범위 밖 번호, 잘못된 호출자 검사 포함.
스크립트 분모는 원본 TPL을 따른다:6DE3E0=66,6DF988=52,6E01AC=47. 군사/파괴 임무도66개라고 가정한 첫 빌드는 placement 검증에서 거절됐으며 ROM을 생성하지 않았다. 실패 작업 폴더는 보존했다.
실제 화면/입력 증거는 `poc/runtime/pending500-v2-*`에 기록한다. 격리 진단의 loader/table read alias는 자연 수신·퀘스트·보상·저장 QA가 아니며 진단 state는 정상 플레이에 사용하지 않는다.

## 고정 묶음과 문구 권위

| 아카이브 | 기존 초안 | 묶음 단위 | 컴파일 크기 |
|---|---|---:|---:|
|6DD718|batch500_045_navi_mail_npcs_6DD718_draft_ko.json|16|412|
|6DD798|batch500_045_navi_mail_npcs_6DD798_draft_ko.json|10|323|
|6DD804|batch500_045_navi_mail_npcs_6DD804_draft_ko.json|10|263|
|6DD91C|batch500_045_navi_mail_npcs_6DD91C_draft_ko.json|32|704|
|6DE3E0|protoman_missions_draft_ko.json|253|14,632|
|6DF988|batch500_016_military_6DF988_draft_ko.json|153|10,636|
|6E01AC|batch500_016_destruction_6E01AC_draft_ko.json의38/39/40스크립트|26|4,931|

합계500개 고유 ID,7아카이브. 전용 헤더68+오피셜 임무253+군사 임무153+파괴 의뢰26.
선택 스크립트의 일본어 리터럴은 완결 단위로 선택했고, 파괴 의뢰 나머지105개는 원문을 유지했다. 숫자/원문/명령/기존 문구를 일괄 변환하지 않았다.
문구 권위는 `translations/`의 기존 초안이다. 생성물에 중복된 권위를 만들지 않고 입력 경로·해시·ID를 기록했다. needs_review/NON-DISTRIBUTION/release_eligible=false 유지.

`translations/pending_insertion_500_001_layout.json`은 `6DF988:42:4` 한 항목의 개별 줄 배치다.
기존 `그런데 / 방금 들어온 정보에 따르면 / 과격파 내비가`를 `그런데 방금 들어온 / 정보에 따르면 / 과격파 내비가`로 배치했다.
단어·뜻·순서와 줄바꿈2개는 동일하다. 둘째 줄156px 수요를 보완해 각 줄이 기존152px 비교 범위 안에 든다. 기존 초안 파일 자체는 바꾸지 않았다.

## 검증과 실패 이력

도구: `tools/prepare_pending_batch500.py`. 재실행은 `python -X utf8 tools/prepare_pending_batch500.py --out analysis/<새 이름>`이며 기존 결과를 덮어쓰지 않는다.
현재 증거: `pending_insertion_500_001_r3/preflight.json`, `pending_insertion_500_001_r3/loader_capacity_analysis.json`.
500개 ID·원본 ROM/TPL/아카이브 페이로드 해시·숫자·LF/공백·제어 명령 보존, native/semantic/binary roundtrip, 미선택 스크립트 보존 PASS.
선택 문자 매핑과 일반 폰트의383개 한글 음절 패킹 PASS. 리터럴 자체의 폭 비교 후보는 개별 배치 보완 후0개다.
이는 동적 변수 삽입의 누적 폭이나 화면 검증 PASS를 뜻하지 않는다. 고정 셀 실제 소비 경로는 기존 공급을 이어서 검증해야 한다.
생성한 원문/메시지 바이너리/플러그인 파생물은 `.gitignore`에서 제외하며 새 배포 입력으로 사용하지 않는다.

첫 시도 `pending_insertion_500_001`은 출력 파일명 compiled.msg 때문에 TextPet 역변환 archive ID가 compiled가 되어 거절됐다. ROM은 쓰지 않았다.
아카이브 ID와 같은 파일명을 쓰도록 수정했고 r2에서500개 왕복이 통과했다. r2에는156px 폭 후보가1개 있었다. r3는 개별 배치를 반영해 폭 비교 후보가0개다.
실패/이전 시도는 비교용으로 보존하며 r3만 현재 준비 검사 증거로 사용한다.

## 로더 용량과 이번 반영 방식

네이티브 로더 `0804055E`는 body table `080405F8 + index*4`를 읽고 `08040562`에서 BIOS 압축 해제로 `0202B2F4`에 풀어 준다.
다음 메일 자산 버퍼 `0202D2F4`까지의 간격은8,192바이트다. 인덱스25(6DE3E0),27(6DF988),28(6E01AC)의 포인터는4065C/40664/40668이다.
원본 본문은 모두 이 범위 안에 있으나 한국어 본문14,632/10,636바이트는 넘는다. 큰 압축본을 그 버퍼에 그대로 넣으면 안 된다.

공통120개 메일의 `tools/keyitem_rom_selector.py` guarded ROM reader에 전용 래퍼를 추가했다.
원본 압축 RAM 사본을 유지하고, 각 원본16바이트 테이블 헤더·호출자0804F7BD·루트0202B2F4·스크립트66/52/47슬롯 범위를 가드로 삼아 해당 본문만 ROM clone에서 읽는다. 비대상은 기존 선택기로 복귀한다.
세 본문의 헤더 변형/비대상·호출자·경계 CPU 검증은990조건에 포함됐다. 새 ROM에서 실제 BIOS 원본 압축 해제와 RAM 사본 일치, 확대 한글 ROM root 선택을 세 대표 본문에서 확인했다.

### 새 ROM 화면 시험 결과

`pending_insertion_500_rom/normal_runtime_v2.json`: cold boot, 초기 설정, 기존 자판3페이지의 VRAM/타일맵, 네 선택 내비 OAM, 첫 메일23쪽 순서/대기 포인터/북마크, 복귀·재열기 PASS. `poc/runtime/pending500-v2-{boot,pagecycle,complete,read,selection}`의 정상 버튼 입력 증거에 바인딩돼 있다.
첫 메일 전체23쪽 및 재열기는 `pending_insertion_500_rom/first_mail_sheet_1.png`와 `first_mail_sheet_2.png`에서 시각 확인했다. 원본 일본어 자판 문자 자체와 자동 한글 조합·저장 미통합은 그대로다.
격리 표시 진단: `poc/runtime/pending500-v2-protoman`은25번 내비의33번 본문 첫 쪽, `pending500-v2-military`는27번의33번 본문 첫 쪽, `pending500-v2-destruction`은28번의38번 본문 첫3쪽을 검사했다. `오피셜 보스/오피셜 지령`, `작전 사령부/임무 지령`, `다크 길드/파괴 의뢰`와 한글 본문 표시를 확인했다. 세 진단의 원본 RAM 본문 전체 일치 및 ROM clone 선택 receipt PASS. 실제 획득·진행·보상·저장 증거가 아니다.
신규500개 모든 화면·분기 검증 완료라고 세지 않는다. 특히6DD718/6DD804의 전체 실제 표시, 등록 변수, 보상 분기·동적 이름·다른 임무 본문 전체 페이지는 후속 QA 대상이다.

추가 필수 확인: 6DD718의 printMailBuffer+등록 제목 누적 폭, 오피셜 임무 보상의 printItem/printBuffer 누적 폭, 내비별 헤더·본문 연동, 임무 제어 명령 보존과 진단 격리, 확장 훅의 실제 에뮬레이터 소비.
명령 보존과 대표 소비는 위 증거로 확인했고, 전체 자연 흐름과 동적 변수 폭은 미완료다. EE38 보상 handler08050ED4는080684B0에서 상태 byte+7와 halfword+12를 가져오고 context+54에 버퍼한다. EE0E/EE12는 요청량을 버퍼에 보존한 다음 재화 추가 함수를 부른다. 따라서 소지 한도999999/9999를 printBuffer 숫자 상한으로 가정하지 않는다. 실제 생성 테이블과 보상 종류별 도달 가능한 값의 검증이 필요하다.
이상은 기술 작업의 재개 지점이며, 사용자의 추가 승인 없이 현재 요청 범위에서 진행할 수 있다. 새 패치 패키지는 요청 전까지 생성하지 않는다.
