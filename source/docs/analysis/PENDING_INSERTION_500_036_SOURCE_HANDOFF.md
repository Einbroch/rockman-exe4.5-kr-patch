# 036 다음500개 소스 준비 완료 — ROM 미반영

## 현재 결과와 범위

- 현재 ROM은 여전히 `poc/output/pending500_035_v2.gba`, SHA256 `41fdee5673329c00f80989e5de2d98db6b3b0980c9a30c5e4b8202fd8dd4d95d`, 누적18,622 적용 단위. 이번 신규 ROM 반영0, 신규 배포 패키지0. 원본/035/기존자료 보존.
- 소스 준비 권위: `pending_insertion_500_036_source_only_v1/verification_v2.json`. 기존 canonical 초안에서 **정확500개,162script,20archive**를 준비했다. 새로500문장을 작성했다는 뜻이 아니다. 37개는 기호만 있는 source literal이며, 단위는 문장 수가 아닌 stable literal ID다. 기존 적용 ID/기존 소유 archive와 중복0, 단어·공백 변경0, 기존 검증된 LF 배치만 유지. needs_review/NON-DISTRIBUTION 유지.
- `selection.json`: 기존 canonical ROM미반영 초안11,924ID 중500개 준비/나머지 미선정11,424. 아직500개도 ROM미반영이므로 **ROM미반영 총수는11,924 그대로**다. 전체게임/이미지 잔여량이 아니다. 035 실제 unique literal delta500 확인.
- 원본 전체byte 왕복, 번역 literal/언어/ID/control topology/binary 왕복, 미선택script 원본보존, 보호된 숫자·경계, 16bit script offset 통과. 검증된 profile normal-pages444/normal-horizontal56 재실행, 현재035 ROM의532개 확장 글꼴 byte 대조 PASS.
- `loader_analysis_v1.json`: A0/A1/A3의84개 native source population에서20개 source의 유일 lookup 및 동일 scene 내 full/prefix 비충돌 확인, 원본압축/포인터/loader 동일,9손상거부 PASS. 430개는A0,41개는A1의7AAF94(sub3/slot5),29개는A3의7B469C(sub3/slot5). 모두 native NPC root02039800지만, 현재035 selector는A0만 허용한다. **새 selector가 들어갔다는 뜻이 아니다.**

## 035 정상 접근 조사

- `pending500_035_v2/normal_green_progress_v1.json`: 새14정상 segment artifact/부모state/원문2,127byte 일치 PASS, 실제cached NPC호출0. 누적36개 실행segment는 분기 재시도 포함이며 하나의 연속36segment가 아니다.
- 새 경로 v1~v4는 데이터가 있는 막다른 길, v5~v10/v12는 중앙계단/시험센터 입구로 귀결. v11은홈페이지로가는빨간다리. 같은막힘반복금지. 최신정상 `poc/runtime/pending500-035-fixed-green-route-v14/checkpoint.mss`,동일result.json. 좌표(-176.25,56,0), 안내문 닫힘, HP100. 진단 state 아님.
- **확정한 입구 조건:** 현재 EWRAM0203C800은source799314 전체byte와 같고, 대사context는script8. 원본script0은item0/amount1을검사해부족하면8,성공하면Navi flag1368을설정한다. script8의세페이지는견습시험센터/관리구역/수험표필요를안내한다. 이는이시험센터입구의조건이며, 다른모든NPC접근실패의원인으로일반화하지말것. 수험표/flag를강제로넣지않았다.
- 참고 경로 가설: https://gamefaqs.gamespot.com/gba/921255-rockman-exe-45-real-operation/faqs/34214 검색결과는카운터NPC에서수험표구매를안내한다. 본문fetch는restricted실패하여정확한이동경로/가격은미확인. 외부힌트는실제획득증거가아니다. 원본description709408:0:0도견습시험응시용수험표다.
- 035의격리native caller/표시진단PASS는그대로유효하지만자연NPC선택은미완료. 기존036제품반영게이트를해제하지않았다. 접근조사를반복하는동안독립적인소스준비만진행했으며ROM승격과분리한다.

## 다음 작업

1. 035 정상 NPC 선택은미완료로유지. 시험센터계단의이동미세조정대신수험표획득을정상진행으로확인하거나, 잠기지않은다른NPC경로를원본/가이드에서확정. 기존source-mode격리진단을자연획득으로승격금지.
2. 036은아직source-only. A0/A1/A3 scene별원문신원과원본LR4F773을검증하는새selector/CPU/경계·worst-case emulated timing,기존035/이전consumer보존,소유권·전체쓰기·독립재빌드·실제화면검증필요. native압축/RAM을키우지않는ROM clone설계후보이나제품채택/설치미실행.
3. 새로운도구는아래버전명을보존하고다음버전파일로작성. 원본에서재구축하며patched035는분석/비교baseline일뿐빌드입력이아니다. 새ROM에정확500개가반영되기전누적19,122로집계금지. 사용자요청전BPS/xdelta/ZIP생성금지.

## 도구 및 실패 보존

- `prepare_source500_036_v1.py`: source-only선정PASS,파일hash고정. 최초compile은출력파일명을target.msg로하여TextPet가reverse @archive target을생성했고,ID/topology검사가정상거부했다. `compile/79CF04` 실패자료보존. 실제binary는왕복동일했어도ID검사를완화하지않음.
- `compile_source500_036_v2.py`: archive이름.msg로컴파일,source/역변환텍스트의ID를고치지않고전체20개통과. 출력 `compile_v2/`,권위 `verification_v2.json`.
- `inspect_source500_036_v1.py`: 추가20source/84population lookup/9손상거부PASS.
- `record_green_route_035_v1.py`:14정상segment/시험센터script8확인. 모든shell/에뮬레이터명령종료,사용자mGBA변경없음. ROM SHA재확인.
