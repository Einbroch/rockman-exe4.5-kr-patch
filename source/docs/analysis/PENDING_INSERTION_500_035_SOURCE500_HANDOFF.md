# 035 다음500개 압축 NPC 대사 소스 검증 / 실제ROM 미반영

## 현재 권위와 정책

- 현재 실제ROM: `poc/output/pending500_034_v1.gba`, SHA256 `4727b8dfcee840b81d45ed156a9e0613f128f4090f8659b58351d6a9c0a17751`.034 상태/실행증거는 기존 `analysis/pending500_034_v1/batch_status.json` 권위 그대로. 이번 신규ROM 반영0개.
- 원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 재확인. 원본/이전ROM/초안/저장/패키지 보존. 새BPS/xdelta/ZIP 없음.
- 사용자 정책: 신규·비중복 정확500개가 준비되면 누적ROM 반영. 이번500은 **소스 검증 후보**이며 저장/제품입력 준비완료500이 아니다. 적용 준비를 건너뛰어 ROM 생성하지 않는다.

## 이번 완료 범위

1. `inspect_remaining_035.py`: actual034 layout ID 제외 후 정규초안 일본어 문자 포함12,424ID(기존RAW4,728/신규RAW534/압축7,137/참조미해결25). 전체게임·이미지 미번역 분모 아님. 원본SHA는 한번 계산하여034의 반복해시 비용 제거. 최초 실행은 옛coverage 의존경로 한곳이034로 잘못 바뀌어 보고서 생성 전 실패,033의 원래 pinned coverage 근거로 수정 후 통과.
2. 기존RAW 엄격모델 신규검사1ID `6FE8D4:23:0` 통과,1,409script 거부. 목록 어댑터의 미지원 selector가 StopIteration을 내는 문제는035 검사전용 guard로 명시적 거부 처리;034 고정도구는 수정하지 않음. 이1개는 아래 압축500에 포함하지 않음.
3. 신규RAW/압축 저장 구간을 **기존 화면모델 그대로** 별도 조사: 압축1,972ID/801script 통과, 신규RAW 통과0. 화면모델 통과는 저장/로딩/제품 소유 승인 아님.
4. 정규초안에서 신규·비중복 정확500ID/160script/9압축아카이브 선택. 462문구·라벨 +38시간차 점 기호이며 독립500문장으로 보고하지 않는다. 캐릭터/시간분기/점 애니메이션의 원문 제어 순서 보존. 기존 번역문 단어·공백은 그대로,4ID의 내부 LF 배치만 변경.
5. `compile_source500_035.py`: 모든 원본압축을 해제한 **전체 아카이브 바이트**와 원문TPL 재컴파일 일치. 번역TPL→binary→TPL→binary의 literal/control/binary 왕복,미선택script 원문바이트 보존,16bit offset,현재034의547개 글꼴 데이터 일치 PASS. 선택 저장본/포인터word는 원본과actual034 동일. 생성 파일은 `analysis/`의 소스 실험자료이며 ROM이 아니다.
6.9개 번역payload의 literal-only LZ10 self+별도decoder 왕복 PASS. 실제BIOS/게임 loader에 새stream을 공급한 검증은 아님. 모두 해제크기가 증가:79D1082020→3929,79D6502127→4291,79DC102006→3946,79E1482693→5633,79E8902198→4301,7A0D181784→3248,7A32A83306→6780,7A43481707→2001,7A4DD42986→6009bytes. 소스압축slot에 덮어쓰기 금지.
7. `inspect_compressed_loader_035.py`: source/actual034 네이티브0804F712 및 조회함수·호출자·literal 동일/Thumb1 재어셈블 일치. sceneA0/sub-area/8way selector→9개 정확pointerword→02039800의 정적 연결 확인. 뒤의 독립loader 목적지는0203C800,0203D800. 첫 목적지와 두번째의 거리12,288bytes보다 최대번역6,780이 작다는 **필요조건만** 확인;중간영역의 다른사용자/수명/실제쓰기/소비/용량 전체 승인이 아님. 8way slot을 실제요일로 단정하지 않음. 코드/조회/literal/pointer10손상거부 PASS.

## 권위 자료

- `analysis/pending_insertion_500_035_inventory_v1/census.json`
- `analysis/pending_insertion_500_035_locked_carry_layout_v1/survey.json`
- `analysis/pending_insertion_500_035_new_storage_layout_v1/survey.json`
- `analysis/pending_insertion_500_035_source500_selection_v1/selection.json`
- `analysis/pending_insertion_500_035_source_compile500_v1/verification.json`
- `analysis/pending_insertion_500_035_loader_analysis_v1/analysis.json`

위 보고서에 고정된 새tools도 수정하지 말고 수리시 새version filename 사용. 복제 도구의 일부 print/error 문구034/033과 source-only survey의 inherited status/limits는 옛문구이며, 각 보고서의 실제baseline034 SHA 및 `product_admitted=False`, `rom_written=False`, `release_eligible=False`가 우선한다. compile의 새status/limits는 압축저장 미승인을 명시한다.

## 실패/정정 해석

- 정적loader 검사의 첫 시도는0x53898..0x53928 전체가 원본과 같아야 한다고 가정해 실패. 실제 차이는 **다른4기존제품의 pointer**0x538C4/0x538E4/0x53904/0x53924였음. 이번9개의 pointer는 모두 원본 유지. 검사 범위를 scene/sub-area 상위조회와 이번9개 참조로 한정하여 기존 제품을 건드리지 않고 통과. 다른4개 pointer가 압축해제 대상인지,이 loader의 같은selector로 실제호출되는지 등은 조사전 단정금지.
- PowerShell quote 및 rg positional wildcard 탐색 오류는 읽기명령 단계뿐이며 파일/ROM 변경 없음.
- 모든 shell 세션 정상종료/진행중세션없음. 새 에뮬레이터는 실행하지 않음.

## 다음 필수 단계

1. 정확034baseline에서 이9개의 native loader/BIOS 변환,실제RAM 범위·다른writer·수명·reader caller를 확인. 필요시 기존ROM/격리런타임으로 관찰하고 출처를 명시. 인접시작 사이의 gap을 무조건 free로 선언하지 않는다.
2. 소스압축·완전부모payload·번역500·기존소비자 소유와 저장policy를 source-bound 제품입력으로 등록. 다른4개 기존table entry/loader 경로와 기존selector chain 보존. 변경범위를 전체쓰기계획으로 선언하고 단일writer/overlap/protected/참조·압축해제payload 검증.
3. immutable source 기반035 누적빌드+독립재빌드,정확500delta/기존모든번역·code/append 보존,실제게임표시·글꼴/선택·자연대사 경로 회귀 검증 후 실제ROM반영 완료 보고. 그 전에는500소스 컴파일을 ROM완료로 세지 않는다.
4. 이500외에 남겨둔 안전1개는 이후 묶음; 중복합산/부분반영 금지. 한글자동조합→확정→저장→재표시/환영그림 줄겹침/일본어자판·로고 등 기존 미완료 유지. NON-DISTRIBUTION 개발용이며 릴리스·전체한글화 완료 아님.
