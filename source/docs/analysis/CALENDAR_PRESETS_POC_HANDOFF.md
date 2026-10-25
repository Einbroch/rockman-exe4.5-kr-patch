# 기본 일정명2개 기술 실험

2026-10-05. functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

실험 ROM `poc/output/exe45_ko_development_calendar_presets_poc_v1.gba`.
SHA256 `08d40db5a96aa995eb83ef72db998cbe831a8547c01da35f9d176918b4e07cbf`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
누적1,092선택 텍스트단위 /14그래픽 문구 /21선택·711미선택 archive. 전체 완역률 아님.

## 무엇을 변경했는가

6368E8 raw 기본명62 `ごはん`→`식사`,63 `じゅく`→`학원`.
`calendar_presets_ko.json`은 기존 calendar_types 2개 초안의 필드를 그대로 유지하며 2기본명만 추가한다.
type-presets-poc-v1은0/60/62/63 네 리터럴만 선택하고251다른슬롯·원본 source archive를 보존한다.
이름 값은 기존 F9FC+uint16LE 글꼴 인코딩을 사용하며 각각8byte+E5=9bytes이다.
선택 데이터는 native rawE5 byte-copy를 위해 내부E5를 금지하고22-byte 필드/10-cell 표시 상한을 확인한다.
이 제한을 전체한글 사용자 입력의 안전성으로 확대하지 않는다. E5가 내부에 있는 다른 한글 코드값은 별도 설계가 필요하다.

원본 확인화면32F88..32F9A는E4 일본어확장만2byte/1cell로 세고 나머지는1byte/1cell로 센다.
F9FC를 그대로 넣으면2음절을8cells로 세어 가운데 정렬이 틀어진다.
따라서 이 로컬 길이 루프만 appended Thumb-1 handler로 연결했다.
F9FC는4byte/1cell, E4는원래2byte/1cell, 나머지는원래1byte/1cell이며 E5종료를 유지한다.
32F9A복귀 시 r0=E5,r1=byte length,r2=logical cells,r3=source; 그밖의register/SP/LR와종료CMP flags 보존.
기존32AC6 E5복사함수·37366 등록flag/ID·32-byte 저장표현·키보드2/3/4·확인동적script61은 수정하지 않았다.
생성code의 assembler/disassembler, literal/branch/final-placement 검증과 immutable source Expected Write 검사를 사용한다.

## 연결된 정상 증거

새ROM own-cold/date/profile/Roll/intro/PET/장비부터 달력시간/내용/확정/조회로 정상 패드 이동했다.
다른SHA checkpoint, ROM/RAM/register 수정, read alias를 사용하지 않았다.
own-time에서 식사 down2/학원 down3의 각 독립 정상 등록 경로와 그 own-checkpoint의 PET L조회 경로를 기록했다.
`capture_calendar_presets.py`는 관찰만 하며 source lookup/copy/count/commit PC와 glyph/메모리를 수집한다.

식사/학원 각각 relocated script62/63 source→02026080의9bytes를 확인했다.
로컬 count의 실제출력 byte length8/logical length2를 확인했다.
mono provider BDF 원본glyph→fixed640-byte staging→06014000→2문자+8nativeblank clear→확인화면 픽셀 검증 통과.
canonical02001310의32-byte record에서 앞10byte 날짜/시각/종류header와name+10/9bytes/E5/남은13zero를 확인했다.
그 이후같은세션 L조회에서 동일record→02010C40의한글값→normal font→OBJ VRAM/화면 픽셀을 확인했다.
`preset_pages.png`의 네 화면(두 기본명 확인/조회)을 직접 시각 검토했다.

원본251미선택슬롯, 직전frequency_v1의20다른archive payload, 이전6368E8의253스크립트(62/63외),15relocatedroots,
빈도압축슬롯63673C..6368E8 불변 검사를 통과했다.
이번새 기본명2개 증거는 고정명 같은세션 동작이지 한글입력/편집/영구저장 증거가 아니다.

## 검증과 유지한 실패 기록

실제 emitted counter를 CPU로 실행하여487native 호환vector와11172한글 음절counter vector의 register/SP/LR/flags와name-buffer 불변을 검사했다.
native E5복사는선택2개의9byte와22-byte field의 나머지canary 불변만 별도로 검사했다.
이 CPU bench는 게임플레이/오디오/RTC/저장 검증이 아니다.
관련50unittest 통과. historical capture fixture를 새ROM 실행으로 합산하지 않는다.
새ROM 날짜 안내, 인사, PET 선택, 장비 caption/guide 네집중회귀보고서와새기본명보고서 통과.
장비의 synthetic selector32건/guide72건은 실제퀘스트 플레이가 아니다.

첫 hook source-byte 기대값 검사는 Thumb ADD canonical alias 차이를 거부했고, 실제source exact hex로 고쳤다.
이때 제품파일은 생성되지 않았다.
장비 회귀의 full-tail equality도 새 appended component를 알지 못해 거부했다.
검사를 느슨하게 하지 않고 정확한 preset asset/constructor/metadata/설치바이트를 재구성해 전체tail equality를 유지했다.
실패 실행 로그와 이전capture/build는 보존한다.

main/_repro/_current_repro2의최종 ROM identity/tool audit는 `calendar_presets_poc_v1/final_identity_audit.json`에 기록한다.
3ROM SHA동일,425Python도구 drift=[],원본 SHA보존 검사를 통과했다. 최종50테스트는5.640초에통과했다.
원본과 기존frequency_v1/date_v1 ROM은 덮어쓰지 않는다.

## 다음 가장 중요한 검증

2026-10-05 후속: 이정확한ROM의`학원`기본명1건은native명시적save→새프로세스cold reload→32byte등록값복원→1월1일목록fixed-cell한글표시까지검증했다.
`calendar_presets_poc_v1/persistence_runtime.json`과`ROLL_SAVE_POC_HANDOFF.md`참조. 최초same-session보고서는그원래범위를유지한다.
`식사`의영구재로드,새save문구후속ROM에서의이름저장·재로드는아직검증해야한다.
기존저장값 호환, 키보드/편집/다른 이름·메뉴·복사소비자도 여전히 미완료다.
전체 Hangul 입력 지원범위와 UX의 인간선택·전체게임·RTC/alarm·실기·오디오·인간검토/배포도 미완료다.
본실험은배포/릴리즈후보가 아니며 기존정상baseline을전부대체했다고 주장하지 않는다.

재현: 기존 `build_roll_pet.py` 누적 날짜/빈도 flags에 `--calendar-presets-poc` 추가.
검증: `run_calendar_presets.py`, `bench_calendar_presets.py`, `report_calendar_presets.py`.
증거: `analysis/calendar_presets_poc_v1/preset_runtime.json`, `counter_bench.json`, 각 normal receipt/observer metadata.
