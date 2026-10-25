# 록맨 에그제 4.5 한글패치

대상은 `Rockman EXE 4.5 Real Operation (J)(Independent).gba` 단일 리비전이다.
원본 ROM은 변경하지 않으며, 모든 조사와 빌드는 `project.json`의 해시를 통과해야 한다.

작업 방식(사용자 지시): 후속 작업은 ROM에만 반영한다. 사용자가 패치 파일 생성을 다시 요청하기 전에는 BPS/xdelta/ZIP 등 새 배포 패키지를 만들지 않는다. 기존 패키지는 보존한다.

## 031 진행 중: 추가130개 원본 기반 컴파일·상대 칩 소비 경로 검증 (미반영)

현재 적용 ROM은 아래030/누적16,122개 그대로다. 다음500개를 위한 상대 칩 통계 주변 **130개/46script/18archive**를 동결된 기존 초안에서 준비해 원문·번역·바이너리 왕복/비선택script 보존과268개 기존한글glyph 공급을 검사했다. 원본+030의두 상대칩 기록producer→F90C CPU1,580조건, geometry20fixture/실제130개, 같은030에서두 native 최대8글자칩 이름의RAM/fontCPU/OBJ/pixels·대기·PET복귀 및6개 화면도 확인했다. 이6개는 원래 일본어 대사의 소비경로 시험이며 새130개 한국어화면 검증이 아니다.

검토한 모델의 다음조합은223개로 아직500개가 되지 않는다. 부분번역script 신규20개를 조사했지만 별도 혼합소비계약이 필요하다. **이번 신규 ROM반영0개/새ROM·배포패키지없음**.130개를누적수에더하지않는다. `analysis/pending_insertion_500_031_preflight_v1/status.json`이 준비상태 권위이며 [031 재개 기록](analysis/PENDING_INSERTION_500_031_HANDOFF.md)에 다음분석지점이 있다. 원본/030의모든기존빌드도구/이전보호artifact를해시보존했다. 상대플레이어이름 통신의12byte전달과종단소유권은미확인이므로500개수를채우기위해임의허용하지않았다.

후속 조사 `analysis/pending_insertion_500_031_packet_boundary_v1/verification.json`:source/030 CPU168조건과 일반버튼 경로에서원래자판의2byte문자‘ゃ’6글자입력/7번째거부/확정을확인했다. 통신의12byte복사는최대이름의E5끝표시를포함하지않으며13번째바이트도갱신하지않는다. 실제대전은상대기기준비단계이후로진입하지못했으므로수신초기화의끝표시소유권은아직미확인이다. 원본게임오류확정이나임의종단추가를뜻하지않는다.7개화면직접검토,ROM추가반영0개.500개단위유지가기본이며130개우선반영여부는사용자선택질문만제시했다.

## 최신 개발 ROM: 030 다음500개 누적 반영·재빌드·칩 통계 대사 표본 검증

`poc/output/pending500_030_v1.gba`, SHA256 `203fd306a7c9c713e3c6f4e7af3dd24d5f21eab0c000f210a061295d31083491`,12,400,552bytes. 새500개(183 whole scripts/19 RAW-carry+새 RAW6D44D4)를 적용해 **누적16,122개**다. 원본에서 영향받는 기존1,413개를 재구성·보존하고, 기존 초안 문구를 유지하며26개 LF 줄배치를 명시했다. 칩 통계 주변문구262개/배열형 프로필172개/직접 프로필66개다. 두 원본 기반 전체 빌드는 byte 동일하며, 완료 권위는 `analysis/pending500_030_v1/batch_status.json`이다.

기존459개 소비자 보존+19개 병합/새 RAW1개·전체diff/owner/포인터 PASS. 실제030/source native 칩 lookup→통계writer→F90C CPU3,932개, 배열형34,276개/직접프로필304개/A3 5,652개/B0 6,341개, 손상거부16개를 통과했다. 입력게이트21거부, 실제append source합집합2000개·중복writer거부도 PASS다. primary428/catalog 물리적 비변경304이며304는 잔여 미번역 수가 아니다.

같은030의coldboot/초기설정/기존자판3페이지/네내비/첫메일23쪽·복귀·재열기와 신규4문구·4쪽의glyph→fontCPU→RAM/OBJ/pixels·전체줄폭/잔상제거/순서·keyWait/두PET복귀를 확인했다. 신규표본은 own Rockman host의 격리GutsMan75/89 read-alias로 호출했다. 원본 분류가 맞는 최대8글자 Standard칩9/Giga칩302 통계record를 실제F90C 직전에 잠시 넣고 복원했으며 영구내비변경·자연획득 검증이 아니다. 초기설정22/메일23/raw6의 **51개 캡처를 직접 검토**했다.

**통계에 삽입되는 칩 이름 자체는 아직 일본어다.** 별도 라이브러리/배틀 한글 이름 경로를 이17byte record에 그대로 적용할 수 없다. 자동한글조합→확정→저장/재표시, 환영문bitmap 겹침, 일본어자판·호칭·타이틀·요일·메일머리글과전체500개 문맥/말투검수도 미완료다. NON-DISTRIBUTION/needs_review이며 원본/이전ROM/세이브/기존ZIP 보존, **새 배포패키지없음**. [030 완료·다음 재개 기록](analysis/PENDING_INSERTION_500_030_HANDOFF.md). 다음은실제030 ID/cumulative030.scope 기준으로 진행하며이번500개는다시적용하지않는다.

## 이전 개발 ROM: 029 다음500개 누적 반영·재빌드·배열형 프로필 화면 검증

`poc/output/pending500_029_v1.gba`,SHA256 `a089f2e0abd7fa2fc9af25549dbce6737f37487fc5a304434c5893b05dce4ff5`,12,379,368bytes. 새500개(162 whole scripts/16 RAW-carry 영역)를 적용해 **누적15,622개**다. 원본에서 기존837개+새500개를 재구성했고, 문구는 유지하고14개 줄배치만 명시했다. 독립재빌드 `_repro.gba`와 전체byte 동일하다. 권위는 `analysis/pending500_029_v1/batch_status.json`이다.

독립검사462개 기존소비자 보존+16개 병합/전체diff/owner/포인터, actual029 배열CPU34,276/A3 5,652/B0 6,341/손상거부16개, 입력게이트 거부7개와 실제append 함수의027→028→029 합집합1500개/중복writer거부가 PASS다. 정상 초기화26행과8종cache 유지/record·flag복원을 검증한 뒤, actual029 coldboot/기존자판3페이지/네 내비/첫메일23쪽·복귀·재열기도 통과했다.

새 형제이름 최대6글자/방송이름 최대8글자는 실제초기화 전에 native record를 잠시 넣고 직후복원했다. own Rockman PET host에서 격리된GutsMan5/35 root/table read-alias로 신규4문구·4쪽의glyph→font CPU→OBJ/pixels·줄좌표/배경지움·순서/keyWait·두PET복귀를 검증했다. 53개 화면도 직접 검토했다. 자연 캐릭터/대사 선택, 전체500개 문맥·말투 승인, 한글입력 확정·저장/재표시나 전체게임 완료를 뜻하지 않는다. 환영문 bitmap 줄겹침, 일본어 자판·호칭·타이틀·요일·메일머리글 등은 여전히 미완료다. NON-DISTRIBUTION/needs_review이며 원본/이전ROM/세이브/기존ZIP 보존, **새 배포패키지없음**. [029 완료·다음 재개 기록](analysis/PENDING_INSERTION_500_029_HANDOFF.md).

## 이전 개발 ROM: 028 다음500개 누적 반영·재빌드·6쪽 최대 프로필 표본 검증

`poc/output/pending500_028_v1.gba`, SHA256 `66d93c8f0142f2d5e5a48e112af995af5f40e7d031627b9c362878573a95f3ef`,12,364,916bytes. 실제027과 겹치지 않는500개(142개 whole script/11archive)를 추가해 **누적15,122개**다. 기존2개 영역의41문구를 유지하며23개를 추가하고, 새 RAW9개에477개를 추가했다. 문구는 유지하고28개 줄배치만 명시했다. 027에서 새로 등록한 영역도028을 합친 뒤 한 번만 배치하도록 원본 기반 경로를 연결했으며, 독립 재빌드와 전체byte 동일하다.

현재 권위는 `analysis/pending500_028_v1/batch_status.json`이다. 기존467개 소비자 보존+2개 병합/500-ID delta/새 RAW9개/원문 storage·포인터·owner·ExpectedWrites·전체diff, actual028 profile CPU304(source+028)/A3 CPU5,652/B0 CPU6,341/손상 거부16개가 PASS다. 입력 게이트 손상7개와 실제 append 함수의 격리된source-derived 합집합1000개/중복writer거부 검사도 통과했다. primary427/catalog 물리적 비변경305이며305는 미번역 잔여 수가 아니다.

같은028의coldboot/초기설정/기존 자판3페이지/네 내비/첫메일23쪽·복귀·재열기를 재검증했다. 새 WoodMan/AquaMan 대사는 own Rockman PET host의 격리 root/table read-alias로 호출하고, 좋아하는 사람 최대8글자/못하는 과목 최대4글자 native record를 실제F90C에서 잠시 주입·복원했다. 신규7문구·6쪽의 source/RAM glyph→font CPU→OBJ/pixels·전체 줄좌표/빈배경·순서/keyWait·두PET복귀 PASS이며53개 화면을 직접 봤다. 첫검사의저장script index기대값은 sourceinitializer가r1=0을먼저저장한다는코드/6개정지주소로정정했다. 실패도구와증거를보존했고ROM/캡처는변경하지않았다.

자연 WoodMan/AquaMan caller/화자·획득/default/import/all writers나전체500개 문맥 승인이 아니다. 자동한글조합→확정→저장/재표시, native kana/일본어 호칭·날짜HUD·타이틀로고·메일머리글Eメール, inherited welcome bitmap 행간/겹침과기존문장검수는미완료다. native8/4글자 폭88/44px은한글8/4음절의96/48px로자동승격할수없다. NON-DISTRIBUTION/needs_review, 원본/이전ROM/세이브/기존ZIP 보존, 새패키지없음. [028 완료·다음 재개 기록](analysis/PENDING_INSERTION_500_028_HANDOFF.md). 다음은실제028 ID/cumulative028.scope로진행하며이500개를다시적용하지않는다. 현재direct-profile모델의남은후보전망119개는게임전체잔여수가아니며다음500개에는추가소비경로분석이필요하다.

## 이전 개발 ROM: 027 다음500개 누적 반영·재빌드·최대 프로필 표본 검증

`poc/output/pending500_027_v1.gba`, SHA256 `2353a0077b7655abb0abb3f3ba8ca95d4242112931e3dddaccb16f27527f2a0d`, 12,289,028bytes. 실제026과 겹치지 않는500개(158개 whole script/새 RAW archive11개)를 더해 **누적14,622개**다. 기존 초안 문구를 유지하고24개 줄배치를 명시했다. 원본 기반 독립재빌드 `_repro.gba`와 전체byte 동일하며 기존458개 소비자의 payload/메트릭, 비선택script, 새 RAW 원문 storage/포인터/owner/ExpectedWrites·전체diff를 검증했다. primary418/catalog 물리적 비변경314이며314는 미번역 잔여 수가 아니다.

현재 권위는 `analysis/pending500_027_v1/batch_status.json`이다. 직접 프로필8종의 native 입력 상한·확정·F90C reader에 대해 source+실제027 CPU304개, 모델29개/실제 입력 게이트 손상 거부14개, 실제027 A3 CPU5,652/B0 CPU6,341·손상 거부16개를 통과했다. 같은ROM의coldboot/초기설정/기존 자판3페이지/네 내비/첫메일23쪽·복귀·재열기, native 최대8/4글자 프로필을 끼운2쪽의 font CPU→RAM/OBJ→pixels·독립 줄좌표/빈배경·정지·PET복귀를 확인했다. 초기설정22/메일23/raw5 화면도 직접 검토했다.

신규 고유문구3개가 픽셀 검증된 표본이다. 두 프로필은 격리된 root/table read-alias와 F90C 직전 임시 native record 주입·복원으로 시험했으며 자연 획득/default/import/all writers·다른6종의 GBA 실행·저장 지원이나 전체500개 문맥 승인은 아니다. `65CC78:43`의 “오늘은 … 과목은”은 추가 한국어 문장 검수 대상으로 기록했다. 자동한글조합→확정→저장/재표시, native kana/일본어 호칭·날짜HUD·타이틀로고, inherited welcome bitmap의 겹치는 행간과 전체검수는 미완료다. NON-DISTRIBUTION/needs_review 개발본이며 원본/이전ROM/세이브/기존ZIP을 보존했다. 새패키지는 없다. [027 완료·다음 재개 기록](analysis/PENDING_INSERTION_500_027_HANDOFF.md). 다음은 실제027 ID와 cumulative027.scope를 기준으로 진행하며 이500개를 다시 적용하지 않는다.

## 이전 개발 ROM: 026 다음500개 누적 반영·재빌드·선택지 표본 검증

`poc/output/pending500_026_v1.gba`, SHA256 `bf66382b7897f1313a9dba55333512e46f46e5e036a6905d049693ac0af80adf`,12,200,828bytes. 실제025와 겹치지 않는500개(75script/28기존raw archive)를 더해 **누적14,122개**, 독립repro와 전체byte동일하다. 초안 문구를 유지하고18개 줄배치만 명시했다. 새 명령은 원본/025의3,060 CPU fixture, 모델38개·production손상28개를 통과했다. 기존2,352개 source-bound carry 보존과 최종430개 소비자 비변경+28병합/포인터/owner/ExpectedWrites·전체diff,026의A3 CPU5,652/B0 CPU6,341·16손상거부도 PASS다.

현재 권위는 `analysis/pending500_026_v1/batch_status.json`. 같은ROM의coldboot/초기설정/native자판3페이지·네내비·메일23쪽/닫기·복귀·재열기와 세로/PET선택지26개 화면의font CPU→OBJ→pixels·행좌표/빈배경·방향8개씩/B비활성·확정·취소·원래PET복귀 표본을검증했다.22초기설정/23메일/30raw화면을직접봤다. 표본고유문구는신규7+기존취소1이며신규Yes후속문구는미실행이다. PET root/table read-alias 진단이므로 자연임무/배틀/caller·flag효과/전체500개문맥 승인으로 확대하지 않는다. 첫체크포인트의신규8개기대값오류는기존체커/증거보존후신규7+기존1로정정했으며ROM은바꾸지않았다.

자동한글조합·확정·저장/재표시, 일본어자판/호칭·날짜HUD·타이틀로고, 기존welcome bitmap의겹치는행간과전체검수는미완료다. NON-DISTRIBUTION/needs_review이며완성판·배포승인이아니다. 이전ROM/원본/세이브/기존ZIP보존, 새패키지없음. [026 완료·다음 재개 기록](analysis/PENDING_INSERTION_500_026_HANDOFF.md). 다음은실제026의적용ID와cumulative026.scope로진행하며이번500개는다시적용하지않는다.

## 이전 개발 ROM: 025 미적용500개 누적 반영·재빌드·선택지 표본 검증

현재 개발본은 `poc/output/pending500_025_v2.gba`, SHA256 `ad775421ab5353c1326ab3861cbc22e323ce6885c411273de5e2bdcaebde040e`,12,188,612bytes다. 실제024와 겹치지 않는500개(118script/33기존raw archive)를 추가해 **누적13,622개**다. 기존 초안 문구를 유지하고15개 줄 배치만 조정했으며, 선택지371/PET상태109/native이름18/일반2다. 원본 기반 독립재빌드 `_repro.gba`와 전체byte 동일하다. 기존1,897개 문구/소비 계약과 비신규script를 병합 보존했으며, 독립 검사는 기존425개 payload 보존+33개 병합·ID delta/포인터/전체ExpectedWrites/diff/유효owner를 확인했다. primary407/기존 catalog 미변경325이며325는 잔여 미번역 개수가 아니다.

`analysis/pending500_025_v2/batch_status.json`이 현재 기계 판독 권위다. 실제025 A3 CPU5,652/B0 CPU6,341/손상거부16fixture, 같은ROM 부팅·초기설정·기존 자판3페이지·네내비·첫메일23쪽/복귀/재열기 PASS. 신규 선택지 표본의 두항목 상하좌우8이동/예·아니요확정/B취소/원래PET복귀와 이름 삽입 대사2쪽은 fontCPU→OBJ→pixels/정지·줄 위치·빈 배경/복귀 검사 PASS. 실제 비교 화면을 직접 확인했다. 표본은 격리된 PET root/table read-alias 진단이며 자연 배틀/Navi화자/획득·분기 결과나500개 인간 승인은 아니다.

첫025_v1은 최종검사의 부모 매칭 방향 오류로 ROM 저장 전에 실패했다. 최소subset의458/460누락→최대subset460/460매칭을 재현해 고쳤으며, 실패자료를 보존한 새v2로 재빌드했다. 첫선택지 검사도 B취소를 별도결과2로 가정해 실패했으나, 원본 `BSeparate=false`는 마지막선택지1을 사용함을 native코드/실행trace로 확인했다. ROM을 바꾸지 않고 새검사v2/v3에서 예0/아니요1/B1을 검증했다.

자동한글조합→확정→저장→재표시, native kana자판/일본어 호칭·필드 날짜HUD, 기존 구매안내 bitmap의 겹치는 행간과 전체 의미·자연이벤트 검수는 미완료다. NON-DISTRIBUTION/needs_review 개발본이며 완성판/배포 승인이 아니다. 원본·024/이전ROM·세이브·ZIP/증거 보존, 새 BPS/xdelta/ZIP 없음. [025 완료·다음 재개 기록](analysis/PENDING_INSERTION_500_025_HANDOFF.md). 다음은 실제025 적용ID를 기준으로 진행하며 이500개는 다시 적용하지 않는다.

## 이전 개발 ROM: 024 미적용500개 누적 반영·재빌드·화면 표본 검증

현재 개발본은 `poc/output/pending500_024_v1.gba`, SHA256 `206f130070538fe1ca4fb7a7534045afeb210dc4959f290fd631f60429dc048e`, 12,176,264bytes다. 실제 미적용500개(raw343/A3 clone157)를69archive에 누적 반영해 **총13,122개**다. 원본에서 별도 전체 빌드한 `_repro.gba`와 전체byte 동일하며, 기존389개 소비 payload와 병합67개 소비자의 비신규script/기존 문구·소비 계약을 보존했다. primary407/원문 payload 물리적 미변경325archive이며,325는 미번역 잔여 수가 아니다.

`analysis/pending500_024_v1/batch_status.json`이 현재 기계 판독 권위다. 실제500-ID delta/전체기존ID/포인터/source storage/입력 소유권/Expected Writes·전체diff·독립재빌드 PASS. 실제 ROM의 A3 CPU5,652/B0 CPU6,341조건과 손상거부16fixture PASS. 같은024 정상 부팅·초기설정·기존 자판3페이지·네내비·첫메일23쪽/복귀/재열기 검증 PASS. 신규 raw4쪽과 A3 신규2script 각2회는 font CPU→OBJ→pixels·keyWait·잔상/닫기/복귀·재진입 표본 검증 PASS. 기존B0 정상 L입력2회도native RAM·닫기/재진입·대사/커서OBJ 제거 PASS. 비교 화면을 직접 확인했다.

raw 표본은 PET root/table read-alias, A3 표본은 loader/scene/table read-alias 진단이므로 자연 사건·화자 provider·분기 전수나500개 인간 승인으로 세지 않는다. 실제 조건/요일 명령은 보존·실행했으며 flags를 바꾸지 않았다. 자동한글조합→확정→저장→재표시, 일본어자판/호칭·필드 날짜HUD, 기존 구매안내 이미지의 겹치는 행간과 전체 검수는 미완료다. 원본·023·022·기존 ZIP/세이브/증거 보존, 새 BPS/xdelta/ZIP 없음. NON-DISTRIBUTION 개발본이며 완성판/배포 승인이 아니다. [024 재개 기록](analysis/PENDING_INSERTION_500_024_HANDOFF.md).

## 이전 개발 ROM: 023 B0 진행 힌트500개 추가 반영·검증

현재 개발본은 `poc/output/pending500_023_v1.gba`, SHA256 `6e6d9104db33fd927714b4a06cd6a1093fd4b6ef6d4f77c6ecd206daa44a39ec`, 12,156,368bytes다. B0 진행 힌트21개 archive의 실제 신규500개를 추가해 누적12,622개다. 원본에서 별도 전체 빌드한 `_repro.gba`와 전체 바이트 동일하며, 이전435개 clone의 문구/바이트/소비 계약과 기존 폰트·코드·그래픽·데이터 prefix를 보존했다. 원래 B0 압축 데이터/포인터/loader/native RAM 크기는 바꾸지 않고 전체native 바이트·caller/root/scene/Navi가 맞을 때만 ROM clone을 선택한다.

500개 전체 primary archive source/줄배치/변수합성/제어·바이트왕복 PASS. 실제 ROM B0 reader CPU6,341조건/기존A3 reader5,652조건/손상 거부15fixture PASS. 정상 새 ROM의 초기 Monday B0/Navi0에서 **원래 script0→분기/default10**을 L 버튼으로 두 번 실행했다. loader/scene/table/flag alias 없이 한글 font CPU→OBJ→화면pixels/keyWait/빈 영역 잔상 검사·닫기·재진입·native RAM 보존 PASS. 두 종료에서는 E5 end/비활성 context/대사·커서OBJ 제거를 확인했다. 부팅·기존 자판3페이지·선택 가능한 네 내비·첫메일23쪽/복귀/재열기도 PASS다.

기계 판독 현재 권위는 `analysis/pending500_023_v1/batch_status.json`이며 모든 하위 보고서 해시를 묶는다. [023 작업 기록](analysis/PENDING_INSERTION_500_023_HANDOFF.md)에 적용 방식·재개 순서·열린 조건이 있다. 직접 본 표본은 초기설정19화면/첫메일23쪽/새 기본힌트2회와 종료2회다. 전체500개 사람 승인/다른 내비·진행 분기·이름/칩 삽입 페이지 전수/실기·오디오 검증은 아니다. 초기 구매안내 행간은022와 동일한 기존 문제이며, 필드 날짜HUD·일본어 자판/호칭과 자동 한글 조합→확정→저장→재표시도 미완료다. needs_review/NON-DISTRIBUTION, release_eligible=false. 원본/022/기존ZIP은 해시 보존했고 새 패키지는 만들지 않았다.

## 이전 개발 ROM: 022 미적용 500개 추가 반영

현재 개발본 `poc/output/pending500_022_v2.gba`, SHA256 `7363567b1263dac0700e2430da1046e47aa9ba65c8d9c2125b1ab9b3bd2928a1`, 12,059,324bytes. 실제 미적용500개(raw136 + 압축 힌트364)를 추가해 누적12,122개다. primary405/source payload 물리적 미변경327archive이며, 이327은 미번역 잔여 수가 아니다. 압축 힌트19개는 원래 압축 데이터·포인터·native RAM 해제 크기를 유지하고, 정확한 caller/root/scene/Navi/script와 원본 전체 바이트가 맞는 경우만 ROM clone을 읽는다. persistent RAM 추가0/일시 stack32bytes다.

`analysis/pending500_022_v2/batch_status.json`: 실제500-ID delta/기존누락0·carry 문구/비신규script/소비계약·포인터·Expected Writes/ISA/전체 diff/ancestry/hash-bound arguments·독립 재빌드 전체byte identity PASS. 실제 ROM 힌트 CPU5,652조건 + 기존 reader3,195조건, 손상 거부11fixture PASS. 같은 ROM에서 정상 부팅/초기설정/기존 자판3페이지/선택 가능한 네 내비/첫메일23쪽·복귀·재열기 검증 PASS. 힌트4회 표시와 raw5쪽은 font CPU→OBJ→화면pixels/keyWait/잔상 검사 PASS, 비교 화면을 직접 확인했다. 힌트 닫기·재열기 전후 원본 RAM 유지, 기존 B0 native hint의 정상 fallback도 확인했다.

힌트 표본은 loader/scene/table read-alias 진단이며 자연 A3 이벤트/화자 provider/전체 분기나500개 사람 승인이 아니다. 별도 script0 진단에서는 table 값을 변경하지 않고 원래 jump/flag 검사→기본 script10을 실행해 ROM clone 안의 분기와 재진입을 확인했다. 기본 script10의 일본어는 미번역 그대로이며 추가 번역 수로 세지 않았다. Mesen 표본 reader 측정59,490~59,492cycles는 다른 내비/실기/음향 검증으로 확대하지 않는다.

한글 자동 조합/commit/save/redisplay, 초기 구매 안내의 빽빽한 행간, 필드 날짜 HUD의 `1月3日(月)` 등 다른 UI/이미지·소비 경로와 전체 자연 이벤트/번역 검수는 미완료다. needs_review/NON-DISTRIBUTION 개발본이며 완성판/배포 승인이 아니다. 새 BPS/xdelta/ZIP 없음. 원본·020·021·기존 ZIP 해시 보존 PASS, 이전 ROM/사용자 세이브/증거 보존. 첫 v1 빌드는 도구의 폴더 생성 오류로 ROM 저장 전에 실패했고, 실패 기록을 남긴 채 v2와 독립 재빌드를 원본에서 새로 만들었다. 현재 결과·다음 재개 권위 `analysis/PENDING_INSERTION_500_022_HANDOFF.md`.

## 이전 개발 ROM: 021 미적용 500개 추가 반영

현재 개발본 `poc/output/pending500_021_v1.gba`, SHA256 `76d9cf6626436f4c683a49f9389f72c3c85b01b6d6b43461a466e32976ec7ac4`, 11,964,256bytes. 020에서 미적용이던500개를 기존20archive/109script에 추가해 누적11,622개(주404/미변경328archive)다. 고정 번역 문구를 유지하고21개 줄 배치만 조정했다. 원본 선행 guard/flag/global 명령 및 화자 변경을 보존한 큰 대사창 profile을 명시적으로 추가했으며 작은 창과 이전 소비 계약은 유지했다.

`analysis/pending500_021_v1/integration.json`: 실제500-ID delta/기존누락0·parent payload/비신규script/consumer/source storage/포인터/전체 Expected Writes/header/ISA/hash-bound arguments·독립 재빌드 전체byte identity PASS. 합성CPU3,195조건·계약 테스트16개 PASS. 같은021 정상 초기설정/기존일본어자판3페이지/선택 가능한 네 내비/첫메일23쪽·목록복귀·재열기 검증 PASS. 대표 대사10쪽은 CPU/font/OBJ/pixels/keyWait/잔상 제거 검사와 화면 직접 확인을 마쳤다.

10쪽은 읽기 별칭 진단이며500개 전체 자연 이벤트/분기 조건/획득·소울 기능 검증이나 전체 번역 사람 승인이 아니다. 원문10개 표본 대조도 전체 사람 승인과 구분한다. 초기 구매 안내의 좁은 행간은020과 동일한 기존 시각적 보완 항목으로 `visual_review.json`에 남겼다. 한글 자동 조합/commit/save/redisplay는 미완료다. NON-DISTRIBUTION 개발본이며 새 BPS/xdelta/ZIP 없음. 원본·020·이전 ROM/세이브/증거/ZIP 보존. 현재 결과·재개 권위 `analysis/PENDING_INSERTION_500_021_HANDOFF.md`.

## 이전 개발 ROM: 020 미적용 500개 추가 반영

현재 개발본 `poc/output/pending500_020_v1.gba`, SHA256 `1e595b2113e446fa74be2c2e0c7737a0bf13bcbd7984114eb1c1df79b4580788`,11,945,892bytes. 019에서 미적용이던500개를52archive/194script에 추가해 누적11,122개(주404/미변경328archive)다. 20개 개별 수정문구를 포함한65개 이름 대사 script unit와 문구 불변435개 큰 대사창 unit를 반영했다. 작은 창과 기존 carry 계약은 유지하며, 엄격히 구분한 큰 창에만180/180/168px 개발용 profile을 사용한다.

실제500-ID delta/기존누락0·parent payload/비신규script/consumer/source storage/포인터/전체Expected Writes/header/ISA/hash-bound arguments·독립 재빌드 전체byte identity PASS. 합성CPU3,195조건과 같은020 정상 초기설정/기존일본어자판3페이지/네내비/첫메일23쪽·목록복귀·재열기 회귀 PASS. 긴 창5쪽(180px2행/긴→짧은·짧은→긴page/3행)과 새 이름 소유 표현1쪽(최대native6glyph+호칭99px+의12px=111px)은 CPU/font/OBJ/pixels/keyWait/잔상 검증 PASS, 비교표/화면 직접 검사했다.

이6쪽은 read-alias 진단이며500개 전체 자연이벤트/화자·의미·자연스러움 승인이 아니다. 한글자동조합/commit/save/redisplay와 전체 사람 검수는 미완료다. NON-DISTRIBUTION 개발본, 새 BPS/xdelta/ZIP 없음. 원본·019·이전증거/세이브/ZIP 보존. 결과·다음재개 권위 `analysis/PENDING_INSERTION_500_020_HANDOFF.md`.

## 이전 개발 ROM: 019 미적용 500개 추가 반영

현재 개발본 `poc/output/pending500_019_v1.gba`, SHA256 `38118847f8deeec0586b7c5b400a9dd15ec32a1875c174657fad3ee8029b8042`,11,922,628bytes. 기존018에서 미적용이던500개를 기존112/새21아카이브에 추가해 누적10,622개(주398/미변경334아카이브)다. 신규 이름 대사는 기존 native6glyph 이름/호칭 공급 계약에 묶인221개 script/428unit이며 일반72unit과 함께 반영했다. 기존 초안의 문구는 유지하고44개 줄 배치를 조정했다.

`analysis/pending500_019_v1/integration.json`: 실제500-ID delta/기존누락0·carry/source storage/포인터/Expected Writes/header/ISA/독립 재빌드 byte identity PASS. 합성CPU3,195조건, 같은019의 정상 초기설정/기존일본어자판3페이지/네내비/첫메일23쪽·복귀·재열기 검증 PASS. 첫메일23쪽 비교표를 직접 검사했다. 새 이름 대사2개 quick-box 진단은6글자 native 이름+호칭에 comma111px/‘ 님께’131px 결합, CPU→ROM font→OBJ→화면pixels/keyWait/잔상 검사 PASS. 읽기 별칭으로 고른 진단 페이지이며 자연 사건/화자 일치 증거가 아니다.

후속 full-box2페이지 식사대사 진단도name111px/font/OBJ/pixels/keyWait/잔상제거/마지막A후원래Rockman PET복귀 PASS,3장직접확인·결함거부4fixture PASS. 진단이므로 자연식사알람 사건/해당화자의provider 검증은아니다. 재열기·221개 전체 profile/다른내비 경계, 자동한글조합/commit/save/redisplay, 전체 의미·화면 사람 검수는 미완료다. 개발용 NON-DISTRIBUTION이며 완성판/배포승인이 아니다. 새patch 없음;원본/이전ROM/세이브/ZIP 보존. 재개 권위 `analysis/PENDING_INSERTION_500_019_HANDOFF.md`.

## 이전 ROM: 018 미적용 500개 추가 반영

현재 개발본 `poc/output/exe45_ko_development_pending500_018_v1.gba`, SHA256 `a8d39423bbd4792d948af4bea991dd8c56bb6d34dac8c1a7c570f0c3938f3241`. 미적용 번역500개/252개 script를 기존48개·새30개 아카이브에 반영해 누적10,122개(주377/미변경355 아카이브)다. 문구 변경 없이142개 줄 위치를 조정하고 source edge LF/padding을 보존했다. 실제500-ID delta/기존누락0, 이전310 payload 및 병합 비신규 script/metrics 보존, 전체 write/header/ISA/포인터/source storage/독립 재빌드 byte identity PASS.

합성CPU3,195조건/결함거부14조건·같은018 정상 초기설정/기존일본어자판3페이지/네내비/첫메일23쪽·복귀/재열기 PASS. 신규17쪽 sample은 font CPU→OBJ→화면pixels/keyWait/페이지지움 PASS, 비교표 직접 검사. 자연 caller/event/save 및500개 전체 의미·화면 사람 승인은 아니다. 긴 Windows command line은 해시가 고정된 JSON 인자 파일로 전달하고 제품 빌드는 공통 생성 입력의 동시 write/read를 피하도록 순차 실행했다.

새 패치 파일 없음. 자동한글조합/commit/save/redisplay·다른소비경로/자연루트/사람검수는 남았다. 원본·이전ROM/세이브/증거/ZIP 보존, NON-DISTRIBUTION. 현재 결과/재개 권위 `analysis/PENDING_INSERTION_500_018_HANDOFF.md`.

## 이전 ROM: 017 미적용 500개 추가 반영

현재 개발본 `poc/output/exe45_ko_development_pending500_017_v1.gba`, SHA256 `73cb5ec4b297faaeb95f8ccb531096c753f8a5455adfb2c2d8a5cbe9f30f9106`. 미적용 번역500개/111개 script를 기존6개 아카이브에 추가해 누적9,622개(주347/미변경385 아카이브)다. 문구 변경 없이105개 ID의 줄 위치만 조정했고 기존 script/consumer/metrics를 보존했다. 실제500-ID delta/기존누락0, 이전352 payload 동일, 전체 write/header/ISA/ancestry와 독립 재빌드 byte identity PASS.

합성CPU3,195조건/결함거부9조건·같은017의 정상 초기설정/기존일본어자판3페이지/네내비/첫메일23쪽·복귀/재열기 PASS. 신규14쪽 sample은 font CPU→OBJ→화면pixels/keyWait/페이지지움 PASS, 비교표 직접 검사. 자연 caller/event/save나 500개 전체 의미·화면 사람 승인은 아니다. 원래 portrait/대사/내비 lookup은 변경하지 않았다.

자동한글조합/commit/save/redisplay, 선택지/변수/별도 renderer·storage/자연루트/사람검수는 남았다. 새 패치 파일 없음, 원본·이전ROM/세이브/증거/ZIP 보존, NON-DISTRIBUTION. 현재 결과/재개 권위 `analysis/PENDING_INSERTION_500_017_HANDOFF.md`.

## 이전 ROM:016 미적용500개 추가 반영

현재본 `poc/output/exe45_ko_development_pending500_016_v1.gba`, SHA256 `d58330fba33d9656e90405309afc39496483aacce2df73908e62b53a4f64bd08`. 원본과고정초안을재대조해기존좁은주소필터앞쪽의24raw아카이브/378script에서미적용500개를그대로추가했다. actual500-ID delta/기존누락0, 누적소비단위8,622→9,122, 주347/미변경385아카이브. 기존334페이로드·새아카이브의미선택source/포인터/전체write/ISA보존감사와독립재빌드byteidentity PASS.

합성CPU3,195조건/결함거부9조건·초기설정/기존일본어자판3페이지/네내비/첫메일23쪽·복귀/재열기회귀 PASS. 큰대사창·작은positioned대사창의신규11쪽샘플은glyphCPUreads/OBJVRAM/화면pixels·keyWait/페이지지움 PASS,비교표직접검사. 샘플을500개전체자연플레이·화자/의미승인으로세지않는다.

다음도500개단위로ROM적용하며실제현행ROM기준으로미적용ID와소비경로를확인한다. 자동한글조합/저장·선택지/작은메뉴/변수/자연루트와사람검수는미완료다. 원본·이전ROM/증거/패키지보존,새패치파일없음. NON-DISTRIBUTION;현재권위/재개점 `analysis/PENDING_INSERTION_500_016_HANDOFF.md`.

## 이전 ROM:015 미적용6개 실제 반영·표시 검증

현재본 `poc/output/exe45_ko_development_pending500_015_v1.gba`, SHA256 `a6d3b0330566374937857cb49b2f07475a6c590e73ac6873486556585a4f4d81`.768800에4개,7C9C44에2개를 추가해 누적 소비 단위8,616→8,622, 주323/미변경409아카이브다. actual6-ID delta/기존 누락0, 기존332페이로드 및 병합 아카이브의 비신규12script/기존4개metrics 보존, 새22미선택script/source storage·actual pointer/전체write/ISA 감사·독립재빌드 byte identity PASS.

변경6쪽 glyph CPU reads/OBJ VRAM/화면pixels·keyWait·페이지지움 PASS, 무초상화2화면의빈영역도확인했다. 비교표 직접검사. 초기 설정·기존 일본어자판3페이지·네내비·첫메일23쪽/복귀/재열기 회귀, 합성CPU3,195조건·결함거부11조건 PASS. 앞선 고정입력을 순서대로 검증하도록 중복재귀를 줄였고007~015 입력결과동일 및검사조건보존을확인했다.

historic가운데점19개중14적용/5미적용이며 전체게임미번역수는아니다. legacy소울유니존/자연진입/배틀/저장 성공을주장하지않는다. 표현 needs_review/approved=False, 자동한글조합·저장 및선택지/작은메뉴/사람검수미완료. 새패치파일없음, 개발용NON-DISTRIBUTION. 현재권위/재개점 `analysis/PENDING_INSERTION_500_015_HANDOFF.md`.

## 이전 ROM: 가운데점 보류 포함10개 추가・누적014

현재본 `poc/output/exe45_ko_development_pending500_014_v1.gba`, SHA256 `6cdcae37d8682c03a909b08d3ddefea02ad825c6a272899c38bcc5f316be9245`. 상점 안내1개·스테레오 프로그램5개·섀도맨4개를 추가해 누적 소비 단위8,606→8,616, 주322/미변경410아카이브다. 실제10-ID delta/기존 누락0, 기존330페이로드/소비metadata와 미선택script/source storage·포인터/전체write/ISA 보존 감사, 독립 재빌드 byte identity PASS.

새10쪽 모두 실제 glyph CPU reads/OBJ VRAM/화면 pixels·keyWait·페이지 지움 PASS, 비교 화면 직접 검사. 초기 설정·기존 일본어 자판3페이지·네 내비·첫 메일23쪽/복귀/재열기 회귀 PASS. 합성CPU3,195조건·결함 거부9조건 PASS. 표시 진단은 원본 화자 명령을 유지하는 격리 read alias이며 실제 배틀/자연 이벤트/저장 성공 증거가 아니다.

폭에 맞춰 직접 작성한5개 대안의 출처/이유와 원래 초안을 보존했고 review=needs_review/approved=False다. 과거 가운데점 보류19개 중 이전3+이번7=적용10/미적용9; 전체 게임 미번역 수가 아니다. 자동 한글 조합/저장·선택지 등 다른 소비 경로와 전체 의미/말투 검수는 미완료다. 새 배포 패치 없음, 개발용 NON-DISTRIBUTION. 현재 권위/재개점 `analysis/PENDING_INSERTION_500_014_HANDOFF.md`.

## 이전 ROM: 보류된 록맨 메일 알림1개・startup mixed scope 통합013

현재본 `poc/output/exe45_ko_development_pending500_013_v1.gba`, SHA256 `00093bd660f08930abf2db43cd98f5ce93f64c563c9313496051f4472d86b20c`. 보류70904C:10:0 `넷토, 메일이 도착했어!`를 기존 초안 그대로 추가해 누적 소비 단위8,605→8,606개다. 주319아카이브/미변경413아카이브, actual1-ID delta/기존누락0. 원본 기반 빌드와 독립 `_repro.gba` byte identity PASS.

같은 아카이브의 초기 UI41개와 normal 알림을 별도 literal profiles로 보존했다. 모든 비신규119scripts・기존 metrics・dynamic Navi 확인 설정과 비중첩329페이로드 동일, actual pointers/전체write/ISA 감사・CPU3,195조건・결함 거부6조건 PASS. 초기 설정・기존 일본어 자판3페이지・네 내비 선택・첫 메일23쪽/복귀/재열기 PASS. 알림은 격리 표시 진단에서 실제 글꼴 읽기/OBJ VRAM/화면 pixels・keyWait・빈 영역 PASS, 비교표 직접 시각 검사. source portrait17을 Navi index0과 혼동한 진단 기대값만 고쳤고 ROM은 재수정하지 않았다. 자연 메일 트리거・저장 검증은 아니다.

자동 한글 자판/저장과 다른 미적용 소비 경로・전체 의미/말투/자연 진행 검증은 미완료다. 원본・이전 ROM/증거/패키지 보존, 새 배포 패치 없음. 개발용 `NON-DISTRIBUTION`; 현재 권위/재개점 `analysis/PENDING_INSERTION_500_013_HANDOFF.md`.

## 이전 ROM: 일반 raw 잔여268개 묶음012 실제 반영

현재본 `poc/output/exe45_ko_development_pending500_012_v1.gba`, SHA256 `c64f3f8d00079a6f77c87b0fd97035ab018959fcc7412c785dcc563e5e97dc90`. 기존40아카이브와 새8아카이브에 미적용 번역268개를 반영해 빌드의 누적 소비 단위8,337→8,605개다. 주319아카이브/미변경413아카이브, actual 신규268 source-ID·기존ID 누락0. 원본 기반 빌드와 독립 `_repro.gba` 전체 바이트 동일.

carry40의 비신규 script/metrics/profile과 비중첩282페이로드 보존, 새8개 native 저장 영역·미선택 scripts·actual pointers·전체 write/ISA 감사 PASS. 합성CPU3,195조건·결함 거부9조건 PASS. 같은 ROM 초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 설정 안내·섀도맨·나이트맨3대사는 격리 표시 진단에서 glyph CPU reads/OBJ VRAM/화면 픽셀·keyWait·빈 영역 검사 PASS; 비교표 직접 시각 검사. 실제 설정 편집·의뢰 결과·HP 보상·저장 증거는 아니다.

해당 일반 raw/no-print/geometry 조건의 잔여는0이지만 전체 번역 완료가 아니다. 별도 표시·동적 삽입·자판·저장 등이 남았다.732 archive 재대조는 소비 단위 수와 distinct compiled IDs를 구분하며, 기록에 없는 source ID를 실제 미번역 수로 단정하지 않는다. 원본·이전 ROM/증거/패키지 보존, 새 배포 패치 없음. 개발용 `NON-DISTRIBUTION`; 최신 권위/다음 재개점 `analysis/PENDING_INSERTION_500_012_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음011 누적 병합·실제 반영

현재본 `poc/output/exe45_ko_development_pending500_011_v1.gba`, SHA256 `c9a23d3cf303921cfaf33b8f053621c6a16cbe180e3723076a87a5721d084f86`. 기존 부분 적용40아카이브와 새21아카이브에 미적용 번역500개를 추가해7,837→8,337개다. 주311아카이브/미변경421아카이브, 기존ID 누락0. 원본 기반 빌드와 독립 `_repro.gba` 전체 바이트 동일.

기존40개 비신규 script/metrics/profile과 비중첩261페이로드 보존, 새21개 native 저장 영역·미선택 script 보존, actual pointer·전체 write/ISA 감사·CPU3,195조건 및 결함 거부9조건 PASS. 같은 ROM 초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 새2아카이브와 carry1아카이브의3리터럴은 격리 표시 진단의 glyph CPU reads/OBJ VRAM/화면 픽셀·native keyWait·빈 영역 검사 PASS; 비교표 직접 시각 검사. 자연 배틀 결과/화자/보상/저장 증거는 아니다.

source-only v1에 포함된70904C:10:0은 별도 startup 소비 scope이므로 누적 병합에서 중단됐고 ROM 미적용이다. 이를 일반 scope로 덮어쓰지 않고 보류한 v2로500개를 선정했다. 당시 좁은 selector 범위의 잔여268개는 전체 미번역 수가 아니다. 전체 자연 진행·의미/말투 검수·한글 자동 조합/저장은 미완료, 개발용 `NON-DISTRIBUTION`이다. 원본·이전 ROM/증거/패키지 보존, 새 배포 패치 없음. 최신 권위와 다음 재개점 `analysis/PENDING_INSERTION_500_011_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음010 누적 병합·실제 반영

현재본 `poc/output/exe45_ko_development_pending500_010_v1.gba`, SHA256 `8f05118a2dd8a7e452e81f81413b1c580fe9883493aae1e0d85c3d496075663a`. 신규500개를 기존 부분 적용49아카이브와 새20아카이브에 반영해7,337→7,837개다. 주290아카이브/미변경442아카이브, 기존ID 누락0. 원본 기반 빌드와 독립 `_repro.gba` 전체 바이트 동일.

49개 기존 script/metrics/profile과 비중첩232페이로드 보존, 새20개 native 저장 영역·미선택 script 보존, 실제 포인터·전체 write 감사·선택기 CPU3,195조건 및 결함 거부9조건 PASS. 초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS.

새 아카이브의 승리 대사1쪽과 기존 아카이브에 추가한 토너먼트 안내1쪽은 격리 표시 진단에서 glyph CPU reads/OBJ VRAM/화면 픽셀·native keyWait·빈 영역 검사 PASS. 비교표 직접 시각 검사. 새 패배 대사는 source가 keyWait 없이 waitHold로 끝나 현재 PET 진단에서 기본 메뉴로 돌아갔으므로 표시 미검증이다. ROM·원문 명령을 바꾸지 않았고 실패 관찰을 보존했다. 자연 승패/보상/저장 증거가 아니다.

원본·이전 ROM/패키지 보존, 새 배포 패치 없음. 전체 자연 진행/선택 결과/보상/저장과 한글 자동 조합·저장/재표시 ABI는 미완료다. 개발용 `NON-DISTRIBUTION`; 다음 재개점 `analysis/PENDING_INSERTION_500_010_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음009 누적 병합·실제 반영

현재본 `poc/output/exe45_ko_development_pending500_009_v1.gba`, SHA256 `0b623c19d8cbc944b555b26c2571c52d110e076af5fdb5aa0bedf52c0ac54096`. 기존 부분 적용64아카이브에 신규500개를 누적 반영해6,837→7,337개다. 주270아카이브/미변경462아카이브, 기존ID 누락0. 원본 기반 빌드와 독립 `_repro.gba` 전체 바이트 동일.

변경64개의 모든 비신규 script 바이트·기존 표시 metrics/profile 동일, 비중첩 이전217페이로드 및 소비 metadata 동일, 포인터·전체 write 감사·선택기 CPU3,195조건 및 검사기 결함 거부4조건 PASS. 각 ancestry는 해당 exact artifact에서 재검증한다.

같은 ROM 정상 cold boot·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 새 프로그램군2쪽과 넘버맨 아이템 알림2쪽은 격리 표시 진단에서 실제 글꼴 CPU 읽기·OBJ VRAM/화면 픽셀·keyWait 위치·페이지 지움 PASS. 비교표 두 장 직접 시각 검사. 자연 이벤트/아이템 획득/저장 성공 증거는 아니다.

원본과 이전 ROM/패키지 보존, 새 배포 패치 없음. 전체 자연 진행/선택 결과/보상/저장 및 한글 자동 조합·저장/재표시 ABI는 여전히 미완료다. 개발용 `NON-DISTRIBUTION`; 다음 재개점 `analysis/PENDING_INSERTION_500_009_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음008 누적 병합·실제 반영

현재본 `poc/output/exe45_ko_development_pending500_008_v1.gba`, SHA256 `be95c71b2cabc2ca2bb7587b34bc38aa1d528868704d7f97a73efd3c63986e76`. 기존 부분 적용23아카이브에 신규500개를 누적 반영해6,337→6,837개다. 주270아카이브/미변경462아카이브, 기존ID 누락0. 원본 기반 빌드와 독립 `_repro.gba` 전체 바이트 동일.

변경23개의 모든 비신규 script 바이트·기존 layout/소비 profile 동일, 이전 비중첩258페이로드 동일, 포인터·전체 write 감사·선택기 CPU3,195조건 및 검사기 결함 거부4조건 PASS. 007의 carry 검증도 exact007 artifact에서 다시 확인한 뒤008 ancestry를 연결했다.

같은 ROM 정상 cold boot·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 새 프로그램군3쪽과 썬더맨 통신 선택지3리터럴은 격리 표시 진단에서 실제 글꼴 CPU 읽기·OBJ VRAM/화면 픽셀·keyWait/select 위치·커서 위/아래/위 이동·프로그램군 페이지 지움 PASS. 비교표 두 장 직접 시각 검사. 선택 확정/결과·자연 이벤트·저장 증거는 아니다.

원본과 이전 ROM/패키지 보존, 새 배포 패치 없음. 전체 자연 진행/보상/저장과 한글 자동 조합·저장/재표시 ABI는 여전히 미완료다. 개발용 `NON-DISTRIBUTION`; 다음 재개점 `analysis/PENDING_INSERTION_500_008_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음007 누적 병합·실제 반영

현재본 `poc/output/exe45_ko_development_pending500_007_v1.gba`, SHA256 `c5078d66ffe11d4cc80960edb5484bf9bf3f8b4d533c28d178581345a4367656`. 기존 부분 적용13아카이브에 신규500개를 누적 병합해5,837→6,337개다. 주270아카이브/미변경462아카이브, 기존 번역ID 누락0. 원본 기반 단일 writer 빌드와 독립 `_repro.gba` 전체 바이트 동일.

기존 문구·script 바이트·literal별 normal/big/mono 표시 설정을 보존했다. 특히 저장6DA21C와 전투76C944의 기존 mixed profile을 normal scope로 덮어쓰지 않았다. 그 외 이전 페이로드 전체 동일, 실제500-ID delta/누적 write 감사/선택기 CPU3,195조건 및 검사기 결함 거부4조건 PASS.

같은 ROM에서 정상 cold boot→초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 신규 프로그램군4쪽·가족 질문3쪽은 격리 표시 진단에서 정확한 대기 포인터/normal 글꼴 CPU 읽기/OBJ VRAM/화면 픽셀 PASS; 두 비교표 직접 시각 검사. 진단은 자연 이벤트·선택 확정·저장 검증이 아니다.

새 배포 패치 없음. 모든500개 자연 진행/선택 결과/보상/저장 QA, 한글 자동 조합·저장/재표시 ABI, 가운데점 보류19문구 실제 삽입은 여전히 미완료다. 개발용 `NON-DISTRIBUTION`; 다음 재개점 `analysis/PENDING_INSERTION_500_007_HANDOFF.md`.

## 이전 ROM: 가운데점 글꼴·인코딩 보완

최신본 `poc/output/exe45_ko_development_middle_dot_v1.gba`, SHA256 `bd16c794be18178e84e0d473c0faff43c78eb1d492f8c7b9137265ff5aef3f0c`. 기존5,837개/주270아카이브를 유지하며 신규 번역 적용0개다. 가운데점 `·`의 명시적 F9FC 인코딩·글꼴 공급을 추가했다. 쉼표/기존 한글·모든 번역 페이로드는 그대로 보존했다.

독립 재빌드 일치, normal 글꼴·자모 이동 후 동일 글꼴 보존, 선택기3,195조건/혼합 입력 표시 후보380 CPU조건, 정상 초기 설정·기존 일본어 자판·첫 메일23쪽 PASS. 가운데점은 격리 rank read alias에서 실제 normal 글꼴 읽기·OBJ VRAM/화면 픽셀 PASS. 원래 ROM 문구는 치환하지 않았다.

당시 다음500개는13개 기존 부분 적용 아카이브의 미적용 script를 선정해 source-only 사전 검사만 완료한 상태였다. 이후007에서 기존 번역·소비 scope를 함께 병합하고 실제 ROM에 적용했다. 가운데점 보류19문구는 아직 미적용이다. 당시 기록 `analysis/MIDDLE_DOT_HANDOFF.md`, 현재 재개점은007 handoff다.

## 이전 ROM: 미적용500개 묶음006 실제 반영

최신본은 `poc/output/exe45_ko_development_pending500_006_v1.gba`다. 기존 미적용 초안500개를87개 raw 아카이브에 적용해5,337→5,837개, 주183→270아카이브다. SHA256 `02d14a3ead55aa2d52f9458b095384c50c7c92683f82ae08a685c794bb8edc69`.

실제 source-ID 추가500개/기존 누락0, 이전183개 주 아카이브와 모든 별도 페이로드 보존, 독립 재빌드 전체 바이트 동일, 누적 감사 및 선택기 CPU3,195조건 PASS. 단어·순서·숫자·명령·줄 수 변경 없음.

정상 초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 실제 넘버맨 선택 상태에서 신규 복귀 대사2개 및 무승부 결과 대사2개를 격리 표시 진단했고, 정확한 대기 포인터·글꼴 읽기·OBJ VRAM/화면 픽셀·페이지 지움 PASS. 비교표 `analysis/pending_insertion_500_006_rom/number_pages_v1.png`. 실제 패배/무승부 발생·보상·저장 증거는 아니다.

현재 문자표에 없는 가운데점 `·`을 포함한19문구는 보류 기록에 남기고 임의 치환하지 않았다. 해당 script 전체를 이번 선정에서 제외하고 다른 검증 가능한 문구로500개를 구성했다. 전체 게임의 미번역 잔여 수가19개라는 뜻은 아니다.

전체 자연 진행·선택지·보상·저장 및 한글 자동 조합/저장 ABI는 미완료다. 원본/이전 ROM/기존 패키지 보존, 새 BPS/xdelta/ZIP 없음. 개발용 `NON-DISTRIBUTION`; 기록 `analysis/PENDING_INSERTION_500_006_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음005 실제 반영

최신본은 `poc/output/exe45_ko_development_pending500_005_v1.gba`다. 기존 미적용 초안500개를31개 raw 아카이브에 적용해4,837→5,337개, 주152→183아카이브다. SHA256 `ed3b526e6b5b11e9c68c6d26562784d97aa69f5ee617bb1d83fac8ef3a685bea`.

실제 source-ID 추가500개/기존 누락0개, 이전152개 주 아카이브와 모든 별도 페이로드 보존, 독립 재빌드 전체 바이트 동일, 선택기 CPU3,195조건 및 누적 변경 범위 감사 PASS. 단어·순서·숫자·명령·줄 수 변경 없음.

새 ROM 정상 초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 신규 통신 오류 선택지3리터럴과 아쿠아맨 칩 통합 대사3리터럴은 격리 표시 진단에서 native 대기/선택 위치·글꼴 읽기·OBJ VRAM/화면 픽셀, 선택 커서 위/아래/위 이동 및 아쿠아맨 페이지 지움 PASS. 비교표 `analysis/pending_insertion_500_005_rom/display_pages_v1.png`. 실제 통신 오류 발생/선택 확정 결과/HP 보상 검증은 아니다.

전체500개 자연 진행·전체 선택지·보상·저장 QA 및 한글 자동 조합/저장 ABI는 여전히 미완료다. 원본/이전 ROM/기존 패키지는 보존했으며 새 BPS/xdelta/ZIP 없음. 개발용 `NON-DISTRIBUTION`; 기록 `analysis/PENDING_INSERTION_500_005_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음004 실제 반영

최신본은 `poc/output/exe45_ko_development_pending500_004_v1.gba`다. 기존 미적용 초안500개를27개 raw 대사 아카이브에 적용해4,337→4,837개, 주125→152아카이브다. SHA256 `9492ab8b6ba422ad629784e312a990c0683f43983d6e504f9f3699bdd79ef427`.

단어·순서·명령·숫자·줄 수를 유지했다. 전체 주/별도 ROM 소비자의 기존 ID를 제외했고 실제 source-ID 추가500개/기존 누락0개, 이전125개 주 아카이브와 모든 별도 페이로드 보존, 독립 재빌드 전체 바이트 동일을 검증했다. 선택기 CPU3,195조건/누적 변경 범위 감사 PASS.

새 ROM 정상 초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 정상 선택한 넘버맨 상태에서 신규 알림6개를 native pointer/table read alias로 격리 화면 시험했으며 실제 대기 포인터·글꼴 읽기·OBJ VRAM/화면 픽셀·페이지 지움 PASS. 비교표 `analysis/pending_insertion_500_004_rom/number_alerts_v1.png`. 자연 날짜/대회 조건 발생 증거는 아니다.

전체500개 실제 자연 진행·선택지·보상·저장 QA와 이전 미해결4개, 파이어맨/블루스 장비의 남은 실화면 검증은 계속 대기한다. 한글 조합/저장 ABI도 미통합이며 `NON-DISTRIBUTION`이다. 원본/이전 ROM/기존 패키지 보존, 새 BPS/xdelta/ZIP 없음. 재개 기록: `analysis/PENDING_INSERTION_500_004_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음003 실제 반영

최신본은 `poc/output/exe45_ko_development_pending500_003_v2.gba`다. 기존 미적용 초안500개를 추가로 반영해3,837→4,337개다. 주125아카이브, 기존 guarded 메일5개와 신규 내비별 장비 대사 ROM clone3개다. SHA256 `2cddc59ca723ce789c7e935a09ab1742c5a347df41583224fb07c78394c26f04`.

새 적용500개는 거츠맨·파이어맨·블루스 장비 대사39개, 스타맨 관련6개, 다른 raw 대사455개다. 기존 공통 장비 이름으로 이미 표시되는111개 별칭은 중복 집계하지 않았다. 기존 초안의 단어·순서는 유지했으며 파이어맨/블루스 숫자 경고2곳은 줄바꿈만 보완했다.

독립 재빌드 전체 바이트 동일, source-ID 실제 추가 정확히500개/기존 누락0개, 이전82개 주 아카이브와 모든 별도 페이로드 보존. CPU3,195조건과 누적 빌드 감사 PASS. 정상 초기 설정·기존 일본어 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 정상 거츠맨 장비 안내3종은 실제 ROM 읽기·글꼴 소비·OBJ 타일/화면 픽셀·나가기/재열기 PASS. 화면 `analysis/pending_insertion_500_003_rom/guts_guides_v1.png`.

전체500개 자연 진행·보상·저장, 파이어맨/블루스의 실제 장비 화면과 오류 대사 경로는 미검증이다. 한글 자동 조합/저장 ABI도 미통합이며 배포 완료본이 아니다. 원본/이전 ROM/기존 패키지는 보존했고 새 BPS/xdelta/ZIP은 만들지 않았다. 재개 기록: `analysis/PENDING_INSERTION_500_003_HANDOFF.md`.

## 이전 ROM: 미적용500개 묶음002 실제 반영

최신본은 `poc/output/exe45_ko_development_pending500_002_v1.gba`다. 새500개를 누적 반영해3,337→3,837개이며, 주82아카이브와 guarded 메일 본문5개다. SHA256 `25c04c4e04dd92c1a1a8d9a6f977ee6631c9a8ec16eed468381f2ecfac3cf6a4`.

독립 재빌드 전체 바이트 동일. 이전71개 주 페이로드 및 별도 복제본3개,기존 파괴26개 script 바이트 보존. source-ID 집합에서도 정확히500개 추가/기존 누락0개다. 원본 및 이전 ROM/패키지는 보존했다. 새 BPS/xdelta/ZIP은 만들지 않았다.

파괴 잔여105+섀도맨 임무220+대회 등록 메일15+다른 원본 raw 대사160개다. 기존 계획의 장비153/관련 내비7개는 삭제하지 않고 별도 소비 연결을 위한 다음 묶음 대기 목록에 남겼다. 새 번역500개 작성이 아니라 기존 초안500개를 ROM에 적용한 것이다.

CPU 선택기1,072조건 PASS. 정상 초기 설정/기존 일본어 자판3페이지/내비 선택/첫 메일23쪽·복귀·재열기 PASS. 신규 본문7개 리터럴/페이지의 실제 native 대기 포인터와 화면을 격리 진단에서 확인했다. 비교표 `analysis/pending_insertion_500_002_repartition_rom/body_runtime_v1.png`.

`NON-DISTRIBUTION`,단어/뜻 검수 및 전체 자연 임무 수신·진행·보상·저장 QA는 미완료다. 기존 한글 자동 조합/저장 ABI 미통합도 유지한다. 기록: `analysis/PENDING_INSERTION_500_002_REPARTITION_HANDOFF.md`.

## 이전 ROM: 500개 반영본의 임무 본문 줄 배치8곳 보완

최신본은 `poc/output/exe45_ko_development_pending500_arrow_v2.gba`다. 임무 본문의 마지막 줄8곳을 진행 화살표 앞132px 범위에 맞춰 재배치했다. 단어·뜻·순서와 페이지/명령은 유지했으며 신규 번역0개, 누적3,337개다. 기본71아카이브와 추가 임무 본문 ROM clone3개다.
SHA256 `da920efbbd2b965a5e7bbab75ee88242735a8613777f96fb483daf5bad0bd068`. 독립 재빌드 ROM 전체 바이트 동일, 기존67아카이브 내용 보존, 선택기 CPU990조건·네이티브 보상 처리 CPU256조건 PASS.
헤더68개는 기존 BIOS 로더로, 본문432개는 아카이브 식별·호출자·스크립트 범위 확인 후 ROM에서 읽는다. 원래 압축 본문과 RAM 로딩 포인터는 보존했다.
기존 초안 재사용이며 새 번역500개 작성이 아니다. 개발용/NON-DISTRIBUTION 상태다. 실제 보상 값과 제니/버그 조각 숫자 삽입 줄 폭은 빌드 검사에 등록했다. 동적 이름·아이템·등록 제목의 누적 폭, 전체 임무의 자연 수신·진행·저장은 아직 미검증이다. 한글 자동 조합·저장 ABI도 미통합이다.
별도 패치 파일은 만들지 않았다. 재개 지점 및 화면 시험 기록: `analysis/PENDING_INSERTION_500_HANDOFF.md`.
새 ROM의 정상 초기 설정·기존 자판3페이지·네 내비 선택·첫 메일23쪽/복귀/재열기 PASS. 임무 본문3종은 원본 RAM 보존과 한글 ROM 읽기를 격리 화면 시험에서 확인했다. 모든 신규 문구의 실제 진행 검증을 뜻하지 않는다.
수정8곳은 원본 글상자 진입 설정을 보존한 격리 화면 시험과 정확한 대기 포인터 검사 PASS. 비교표 `analysis/pending_insertion_500_rom/arrow_runtime_v3.png`, 검증 `arrow_runtime_v3.json`.

## 최신 임무 메일 발신자·제목 적용 (2026-10-13)

현재 통합 ROM은 `poc/output/exe45_ko_development_mission_mail_header_v1.gba`다.
별도 임무 헤더 `6DD864`의 기존 초안42개를 문구 변경 없이 적용했다. `작전 사령부 / 임무 지령`, 두 위치의 `제목:`을 포함하며 누적2,837개/67아카이브다.
SHA256 `21565ad0db0cbdd25be1326cbed047febf25eb50a1873535833928d34326f389`. 독립 재빌드 전체 바이트 동일, 기존66개 아카이브 컴파일 내용 동일, 원본 ROM·기존 패키지 보존.
새 ROM에서 정상 초기 설정·자판3페이지·네 내비 선택·첫 메일23쪽·복귀·재열기와 CPU867조건 PASS.
임무 헤더는 원래 BIOS 압축 해제·RAM 표시 경로의 격리 진단에서 목록/상세 화면 PASS. 실제 임무 수신·진행·저장 증거는 아니다.
한글 자동 조합·저장 ABI는 아직 통합되지 않았다. 새 패치 파일은 생성하지 않았다. 현재 기록은 `analysis/MISSION_MAIL_HEADER_HANDOFF.md`.

## 이전 스토리 메일 발신자·제목 적용 (2026-10-13)

`poc/output/exe45_ko_development_full_mail_header_v1_r3.gba`에 록맨 공통 스토리 메일의 발신자·제목22개를 적용했다.
기존2개에서20개가 늘어 누적2,795개/66아카이브이며 SHA256은 `a4724f32d388c38f359a352a963cbc21f4121e62f9f655962affb518c4441ff8`이다.
독립 재빌드 ROM 전체 바이트가 동일하다. 고정 셀 제목 최대 폭은80px/허용88px다.
정상 경로의 첫 `I.P.C. / 고객 여러분께`와 본문23쪽·목록 복귀·재열기 PASS. 나머지 대응10쌍은 격리 목록 렌더링에서 모두 확인했으며 실제 후속 메일 수신 증거는 아니다.
헤더 외65개 아카이브와 전체 메일 본문8,531바이트는 이전과 내용 동일, CPU 선택기867조건 PASS. 새 패치 파일은 생성하지 않았다.
기록 `analysis/FULL_MAIL_HEADER_HANDOFF.md`, 검증 `analysis/full_mail_header_v1_r2/header_runtime_verification_r3.json`.

## 최신 잔여 메일43개 본문 적용 (2026-10-13)

`poc/output/exe45_ko_development_full_mail_body_v1_r2.gba`에 뉴스4~6호와 오피셜 초대 메일43개를 추가했다.
공통 본문120개를 전부 선택했으며 누적2,775개/66아카이브다. 전체 게임/다른 내비 메일 완성은 아니다.
전체8,531바이트는 ROM에서 직접 읽고, 기존 RAM 로딩7,005바이트와8,192바이트 한도는 유지했다.
독립 재빌드 동일·CPU867조건·첫 메일23쪽 정상 읽기/재열기·새39쪽/이름 삽입5쪽 격리 표시/종료 PASS.
이전 오피셜/뉴스54쪽은 byte/address 소비 동등성으로 연결했으며 이번 ROM에서 직접 재실행한 것은 아니다.
새 패치 파일은 생성하지 않았다. 실제 수신·해당 제목/발신자·퀘스트 연속 진행·한글 자동 입력/저장은 아직 미완료다.
기록 `analysis/FULL_MAIL_BODY_HANDOFF.md`, 검증 `analysis/full_mail_body_v1/remaining_runtime_verification.json`.

## 직전 메일 ROM 읽기 경로 시험 (2026-10-13)

`poc/output/exe45_ko_development_mail_rom_reader_v1.gba`에 guarded ROM 직접 읽기 경로를 적용했다.
원본 RAM 버퍼와 기존2,732개 번역은 유지했다. 신규 번역0개이며 남은43개 적용 전의 용량 경로 PoC다.
독립 재빌드 동일·CPU867조건·첫 메일23쪽 정상 읽기/재열기·오피셜32쪽/뉴스22쪽 격리 표시/종료 PASS.
새 패치 파일은 생성하지 않았다. 전체120개 clone과 안전한 RAM 로딩 입력 분리 및 잔여43개의 배치/이름 삽입 검증은 다음 작업이다.
기록 `analysis/MAIL_ROM_READER_HANDOFF.md`, 검증 `analysis/mail_rom_reader_v1/runtime_verification.json`.

## 직전 메일 뉴스1~3호 본문 적용 (2026-10-13)

뉴스1~3호 본문22개 추가, 누적2,732개/66아카이브.
`news_mail_v1` 독립 재빌드 전체 바이트 동일, 기존 본문/목록/그림/글꼴/제어 보존.
초기 설정·기능 버튼·네 내비 선택·첫 메일23쪽은 정상 입력 회귀 PASS.
오피셜32쪽과 뉴스22쪽은 원래 압축 로더/출력기에서 격리 진단 PASS. 실제 수신·해당 발신자/제목·뉴스 퀘스트 진행 증거는 아니다.
개인 테스트 BPS·xdelta ZIP: `patches/exe45_ko_development_news_mail_20261013.zip`.
남은 메일43개를 같은 방식으로 모두 넣으면 예상8,531바이트로8,192바이트 한도를339바이트 넘는다. 다음은 로딩 방식과 변수/호출 경로 보완이다.
전체 번역·한글 자동 입력/저장 완료본이나 공개 릴리스가 아니다.
재개 기록: `analysis/NEWS_MAIL_HANDOFF.md`, 검증: `analysis/news_mail_v1/runtime_verification.json`.

## 직전 오피셜 메일 본문 적용 (2026-10-13)

오피셜 메일3통의 본문32개를 추가 적용했다. 누적 2,710개/66아카이브.
`official_mail_v1_r2` 독립 재빌드 전체 바이트 동일, 기존 첫 메일과 목록·그림·글꼴·제어 보존.
첫 메일/초기 설정/자판 기능 버튼/네 내비 선택은 일반 입력으로 회귀 검사했다.
추가32쪽은 원래 로더와 출력기에서 격리 진단 PASS. 실제 수신 조건·발신자/제목 연결·저장 호환 증거는 아니다.
개인 테스트 BPS·xdelta ZIP: `patches/exe45_ko_development_official_mail_20261013.zip`.
전체 번역·한글 자동 입력/저장 완료본이나 공개 릴리스가 아니다.
재개 기록: `analysis/OFFICIAL_MAIL_HANDOFF.md`, 검증: `analysis/official_mail_v1/runtime_verification.json`.

## 직전 첫 안내 메일 적용 (2026-10-13)

첫 I.P.C. 메일 본문 23쪽과 메일함·제목·록맨 안내 7개를 추가 반영했다. 누적 2,678개/66아카이브.
`first_mail_v2` 독립 재빌드 전체 바이트 동일, 원래 압축 로더/목적지/제어 유지.
마지막 쪽의 진행 화살표 겹침을 줄바꿈만 조정해 수정했다.
실제 본문 23쪽 읽기·목록 복귀·재열기와 자판 페이지/네 내비 선택 회귀 PASS.
개인 테스트 BPS·xdelta ZIP: `patches/exe45_ko_development_first_mail_20261013.zip`.
다른 메일/내비 분기·자동 한글 조합/이름 저장·전체 초안 통합은 미완료, 공개 릴리스가 아니다.
재개 기록: `analysis/FIRST_MAIL_HANDOFF.md`, 검증: `analysis/first_mail_v2/runtime_verification_r3.json`.

## 직전 내비 카드 이름 적용 (2026-10-12)

이름 입력 기능 버튼 패치를 보존하고 내비 카드의 일본어 그림 글자 21개를 추가 한글화했다.
`navi_card_names_v1` 원본 재빌드와 독립 재빌드 동일, 원래 압축 슬롯/팔레트/선택 로직 유지.
현재 선택 가능한 록맨·롤·거츠맨·넘버맨의 이동·확인·취소 및 기존 자판/초기 안내 회귀 PASS.
개인 테스트 BPS·xdelta ZIP: `patches/exe45_ko_development_navi_card_names_20261012.zip`.
잠긴 17개 내비는 그래픽 전체 업로드만 검증했으며 실제 해금·플레이는 미검증이다.
가나 글자판, 한글 자동 조합/이름 저장, 전체 초안 ROM 통합은 여전히 미완료다.
재개 기록: `analysis/NAVI_CARD_NAMES_HANDOFF.md`.

## 직전 이름 입력 기능 버튼 적용 (2026-10-12)

기존 startup_ui_v1_r7에 가나 입력 세 페이지의 기능 버튼 18개를 추가 한글화했다.
`native_keyboard_labels_v1` 독립 재빌드/세 페이지 실제 VRAM·맵/일본어 이름 확정·프로필/록맨 안내 회귀 PASS.
개인 테스트 BPS·xdelta ZIP: `patches/exe45_ko_development_native_keyboard_labels_20261012.zip`.
가나 글자판과 입력·저장 코드는 그대로이며 한글 자동 조합/저장 구현이 아니다. 작은 버튼 글자는 needs_review.
재개 기록: `analysis/NATIVE_KEYBOARD_LABELS_HANDOFF.md`.

## 직전 새 게임 설정 적용 (2026-10-12)

`startup_ui_v1_r7`에 날짜·프로필·내비 확인·초기 메일 52개 및 PET 안내/날짜 버튼 이미지 추가, 누적 2,648개.
실제 일반 입력 새 게임 경로와 원래 로더의 전체 이미지 메모리 동일성, 독립 재빌드 및 BPS/xdelta 재적용 검증 PASS.
개인 테스트용 패치 `patches/exe45_ko_development_startup_ui_20261012.zip`.
남은 일본어: 가나 자판/기능 버튼, 내비 카드 그래픽 등. 한글 자동 입력/저장과 초기 메뉴 전체 완료본은 아니다.
재개 지점과 실패 후보: `analysis/STARTUP_UI_ROM_HANDOFF.md`, 실제 화면 연결: `poc/runtime/startup-ui-v1-r7-verification.json`.

## 미번역 작업 재개 (2026-10-12)

최신 사용자 요청에 따라 **전체 번역 초안부터 작성한 뒤 ROM 적용** 순서로 전환했다. 후속 요청으로 stable literal500개씩 번역한다(유일 문장500개와는 다름).
저장271/토너먼트290/임무253/메일120/스타맨129/골드게시판90/배틀게시판125/광장NPC95/미스터리데이터90/오피셜예선·NPC117/블랙워크스동생구역92/형구역130/오피셜접수124/일반배틀38/언더배틀·상점·접수137/고난도통행시험122/개인정보24/비밀특훈·대회장41/공장·수련·장난감·라디오64/골프장69/자동차·정원64/배경·대회장54/철판주문·배틀·정지프로그램60/네이팜시험·미디어·블랙마켓67/배경·바이러스배틀·오르간·대회장·쓰러진나비·어둠배틀79/웃는프로그램·윈드맨요청·브루스현장118/하트·스타보상·강화·귀환59/버스팅연습·결과·의뢰실패186/셰이드맨관조우102/셰이드맨승리귀환98/레이저맨조우73/레이저맨전후95/포르테조우73/포르테승리132/개인정보관리128/크레딧71/미니게임결과31/일정알림12/메일알림14/대회즉시안내12/일정조회6/프로필질문136/진행힌트31/롤메뉴잔여51/운세점기호6/일정알림잔여11/프로필잔여B102/대회격려5/배틀결과4/거츠일정잔여14/윈드맨메뉴잔여57/메뉴확인B44/바람귀환2/윈드맨구호1/윈드맨알림18/500묶음001장비459·진행31·대회10/500묶음002장비459·진행31·대회10/500묶음003메뉴484·훈련15·구호1/500묶음004메뉴220·진행280/500묶음005진행226·일정190·훈련84/500묶음006일정메뉴488·대회12/500묶음007일정메뉴477·메일14·인사9/500묶음008개인정보·칩401·메뉴67·알림24·짧은대사8/500묶음009개인정보459·메일29·대회11·구호1/500묶음010개인정보410·메일42·일정38·대회10, 500묶음011개인정보438·메일28·임무훈련27·일정6·접속1, 500묶음012개인정보474·메일14·일정6·인사6, 500묶음013개인정보405·메뉴56·훈련28·대회10·접속1, 500묶음014개인정보후속403·힌트8·배틀3·인사6·귀환6·훈련16·접속3·메일14·대회15·일정6·알림20, 500묶음015후속183·의뢰220·알림26·메일28·대회16·일정11·힌트13·배틀3, 500묶음016메일함77·헤더42·군임무153·파괴임무131·장비96·접속1, 500묶음017서치임무·훈련479·내비이름21, 500묶음018윈드의식·비행253·개인정보후속243·짧은안내4, 500묶음019바이러스·내비이름255·별개인정보244·주의안내1, 500묶음020거츠개인정보258·넘버개인정보240·썬더주의2, 500묶음021주먹개인정보238·거친개인정보241·통행21, 500묶음022기사개인정보264·불꽃개인정보225·버그조각11, 500묶음023닌자개인정보225·저격개인정보222·금요일NPC53, 500묶음024나무개인정보219·얼음개인정보215·트레이더보상66, 500묶음025정크말투개인정보213·전기개인정보211·일상NPC49·토요일NPC27, 500묶음026존대개인정보211·물주제개인정보194·인터넷1NPC67·평일NPC28, 500묶음027전기질문135·존대질문132·물주제질문174·언더게시판59, 500묶음028일반상점191·힐상점191·시간대NPC51·잡담게시판65·서치주의2, 500묶음029보라상점191·버그조각교환191·목요일NPC68·잠금문/쓰레기50, 500묶음030네이팜임무218·섀도임무현장212·인터넷7NPC70, 500묶음031나이트배틀172·포르테배틀141·통신오류184·NPC3, 500묶음032골드접수시험325·실버접수134·금요일NPC41, 500묶음033견습/인터넷2 270·인터넷6 84·플러그아웃80·배틀게시판제목30·인터넷2NPC36, 500묶음034통신메뉴462·폴더9·인터넷2NPC29, 500묶음035통신메뉴421·토요일광장NPC79, 500묶음036요일·시간대NPC338·배틀NPC149·학원NPC13, 500묶음037장애물·조사·보상457·대회진행43, 500묶음038내비진행494·주말닌자NPC6, 500묶음039서브칩336·진행81·오피셜NPC6·인터넷4NPC77, 500묶음040배틀306·게시판42·지역45·공격16·아이템33·통행5·NPC53, 500묶음041미니게임81·튜토리얼46·배틀278·대회/NPC95, 500묶음042대회시상·룰렛·포르테전후·인터뷰482·NPC18, 500묶음043잔여인터뷰377·메탈수련27·배틀29·칩강화45·접속5·대회명8·NPC9, 500묶음044내비 인사·귀환·훈련결과·메일·일정·대회500, 500묶음045내비·메일·폴더366·NPC/통행/석상/대회134, 500묶음046잔여500·최종047잔여13, 총27450개 신규 초안을 작성했다(465개 회귀 검사 통과(394.323초)).
초안 미작성 입력키 배열2개(6368E8:2:0/3:0); ROM 미선택 일본어27452개는 그대로이며 이번에 ROM을 빌드하지 않았다.
초안은 needs_review이며 3715개 literal은 보수적 화면 폭 재검토 대상이다. 개인정보 입력 전 라벨의 실제 consumer도 미해결이다. 전체 완료·화면 검증·배포 완료가 아니다.
기록 `analysis/TRANSLATION_FIRST_HANDOFF.md`, 전체 추적 `analysis/translation_first_v1/worklist.json`.

최신 후속: 저장 데이터 초기화 안내9개를 `--save-initialize`로 누적 ROM에 반영했다.
개발 후보 `poc/output/exe45_ko_development_save_initialize_v1.gba`,11157488bytes,
SHA256 `906f374acaabe9a37c70fddcae364f07c55545ae1d81b57953d727bb881415be`.
독립 재빌드 전체byte동일·관련52tests·기존59archive/252공용script/폰트/이미지 보존 감사 PASS.
명시적인 기존QA native SAV 복사본으로 새 ROM을 coldboot했다. 정상96 확인창의한국어/기본‘아니요’와B 타이틀복귀를 직접확인했다.
QA SAV 불변, 다른basename 파일 불변(새 ROM 자체rtc만 변경). 사용자save/원본은 미변경이다.
초기화 실행/실패/완료6문구는 ROM에 반영했지만 실제화면은 미검증이다. 저장초기화는 실행하지 않았다.
catalog732: 선택2596/미선택일본어27452/기타검토1859/errors0. 전체완료·배포용이 아니다.
기록 `analysis/SAVE_INITIALIZE_HANDOFF.md`; 확인창 `poc/runtime/save-initialize-v1-prompt/step_005.png`.

직전 후속: 날짜 변경·저장 안내17개를 `--calendar-date-save`로 ROM에 반영했다.
개발 후보 `poc/output/exe45_ko_development_calendar_date_save_v1_r2.gba`,11157340bytes,
SHA256 `675d6c977a0138fcf47050ca841fef056fd0be384c099e041247ef54528fe833`.
독립 재빌드 전체byte동일, 원본/기존59archive·249공용script/폰트/이미지/keyitem39 보존 감사 PASS.
새 ROM 자체 coldboot→타이틀까지 확인했다. 신규17문구의 실제caller/화면/저장 회귀는 미검증이다.
catalog732 재집계: 선택2587/미선택일본어27461/기타검토1859/errors0. 전체완료·배포용이 아니다.
기존 검증ROM·사용자save를 보존했다. 기록 `analysis/CALENDAR_DATE_SAVE_HANDOFF.md`.

추가: 날짜 변경·저장 안내17개 초안을 `translations/calendar_date_save_draft_ko.json`에 작성했다.
크레딧0/통화[z]·이벤트중단/전원금지/저장실패 경고와분기명령을보존한다. source/control/font/codec/제안배치검사 및8tests PASS.
초안 작성 당시17개는ROM미선택이었다. 위 후속에서 반영했으며 실제날짜변경·저장초기화는실행하지않았다.
보고서 `analysis/calendar_date_save_draft_v1/report.json`; `create-kr-patch`의원문보호·개발초안정책을적용했다.

후속: 해당21개를 기존17개와 함께 명시적 `--input-remaining` 빌드 옵션으로 반영했다.
새 개발 ROM은 `poc/output/exe45_ko_development_input_remaining_v1.gba`, SHA256 `56a26c612a2fbfc08a57fb9ae4c9e3d43dcbaaddccfd9f654b16d64bf3369a15`.
누적2570선택 문구/60archive. 원본Expected Write/append/header·기존59archive와234공용script·폰트/기존이미지/keyitem39 보존 감사 PASS.
새 ROM의 자체 coldboot→타이틀에서 ‘처음부터’ 선택 표시까지 확인했다. 신규21문구의 실제 화면은 아직 미검증이다.
새 자판 저장 후보는 포함하지 않았으며, 기존 검증 ROM은 보존한다. 이 ROM은 화면/저장 회귀 대기 개발 후보이며 배포용이 아니다.
문구 authority는 delta JSON 그대로이고 누적 selected_asset은 빌드가 생성하는 read-only 입력이다. 기록 `analysis/input_remaining_v1/artifact_audit.json`.

공용 입력 제목20개와 오류 안내1개의 한국어 초안을 `translations/input_remaining_draft_ko.json`에 추가했다.
원문/제어 구조/기존 parent17 보존, 한글 BDF 수록 및 제안 배치 검사 PASS (`analysis/input_remaining_draft_v1/report.json`).
위 후속 전에는 ROM 미선택 초안이었다. 이번 반영 이후에도 실제21문구 화면검증은 미완료이며 기존 검증 플레이용 ROM은 보존한다.
스킬 `create-kr-patch`의 source 보호 및 초안/런타임 구분 기준을 적용했다. 후속은 명시적 빌드 등록·재빌드·화면 검증이다.

## 현재 작업: 실제 한글 자판 (2026-10-09)

추가 후속(2026-10-11): 활동 문구 조합→조건부 F8 등록→실제 상세/글자 수 계산을 같은 CPU clone에서 연결했다.
친구용6글자 이름 전체11172음절을 조합해 등록한 뒤, pool/기록을 HOST가 고쳐 쓰지 않고 읽는다.
활동11441조건(성공11435/거부6), 누적 등록23130회·상세23128회·글자 수23125회, whole EWRAM80824회 비교 PASS.
길이1..6, E4 payload256, 잘못된/미완성 토큰 및7글자 이름 거부도 포함한다. 재입력 stage와 이웃 메모리는 보존된다.
현재 보고서는 `cpu_calendar_versioned_native/report.json`이며 아래 직전 수치들을 갱신한다.
완성된 사람 이름과 별도의 재입력 stage는 초기 HOST fixture다. 실제 자판 입력·화면·저장/재로드 및 ROM 반영은 아직 미완료다.
`create-kr-patch`의 경로 연결 기준에 따라 기존 activity 코드를 재사용하고 실패시 확인창 진입을 막는 동작도 검증했다.

후속(2026-10-11): 조건부 F8 저장 writer/reader를 실제 달력 등록32EFE/37366과 상세 표시33C94에 연결한 CPU 후보를 검증했다.
등록된22바이트 기록과 pool을 HOST가 다시 쓰지 않고 상세 표시→기존 F9FC 글자 수 계산까지 실행한다.
전체11172음절, E4 payload256개, 기록 주소255개, 기존 식사/친구/81 E5 문자열 대조를 포함한다.
등록11695조건(성공11685/거부10), 상세11693회, 글자 수11690회, whole EWRAM35078회 비교 PASS.
잘못된 F8 기록3개는 heading에 전달하지 않으며, 정상 F8 변형1개도 함께 확인했다.
`create-kr-patch` 기준에 따라 이 결과는 CPU 소비 경계 검증으로만 기록한다. heading/sound/sprite는 모사이며 화면·저장 재로드를 입증하지 않는다.
당시 append/input 연결은 미완료였다. append의 CPU 연결은 위 추가 후속에서 갱신하며 전체 작성/읽기 경로와 실제 입력 연결은 미완료다. F8 형식 및 ROM hook은 미채택이고 원본/플레이용/글리프 후보 ROM3종 SHA256 불변이다.
증거: `analysis/hangul_keyboard_v1/cpu_calendar_versioned_native/report.json`; 실행: `python -X utf8 tools/bench_calendar_versioned_native.py`.

후속(2026-10-10): 저장 경계 전용 version 표식을 사용하는 조건부 CPU 후보를 구현했다.
내부 count marker81..8A는 그대로 유지하고, 저장 후보는F8+10개 LE identity word+E5로22바이트다.
reader는 F8이면 새 구조 전체를 검증하고, 다른 첫 바이트는 제한된 옛 이름 문자열로 변환한다.
따라서81 E5 충돌 사례는 옛 글자81로, 새 F8 기록은 해당 한글 rank로 읽힌다. 잘못된 새 기록을 옛 형식으로 재해석하지 않는다.
`create-kr-patch` 기준으로 전체 작성 경로의 grammar가 입증되기 전에는 F8을 저장 형식으로 채택하지 않는다.
F8은 원작의 storeTimer/storeGlobal 명령 prefix이기도 하므로 기존 parser에 새 기록을 직접 전달하면 안 된다.
당시 범위는 helper ABI였다. 원작 등록/표시 경로의 CPU 연결은 위2026-10-11 후속에서 확인했다. 실제 ROM/세이브는 미변경이다.
증거: `analysis/hangul_keyboard_v1/cpu_calendar_versioned_record/report.json`.
별도 CPU writer11172/reader88476, 전체65536 identity 및99656 whole EWRAM 비교 PASS. 변경2도구 py_compile PASS.

후속(2026-10-10): 실패 제목의 취소를 원작 상위 메뉴 처리까지 CPU 연결했다.
이전 activity 후보의 exit16에서 HOST가 UI를 다시 초기화하지 않고 원작32DD6의 상태16→20과
30E82 상위 호출부를 실행한다. 실제35C84 getter가 selector8을 읽어 입력 재진입28/선택 메뉴20으로 분기한다.
실패9경로가25프레임씩(총225프레임) 종료되어, 친구8경로는 재입력 상태·선택0 대조1경로는 선택 상태로 돌아간다.
전체 기존 activity 검증도 함께 재실행했다. `create-kr-patch` 기준으로 기록/stage/이웃 보호를 매 프레임 검사한다.
이는 CPU 경로 검증이며 script/render는 모사다. 실제 새 자판 화면/ROM 적용/저장·재로드는 아직 미완료다.
저장 형식 구분은 계속 미채택이다. 현재 count marker는 옛 문자열과 충돌하므로 marker만 보고 판별하지 않는다.
별도 CPU11455조건/34560 whole EWRAM 비교 PASS. 변경1도구 py_compile PASS, ROM3종 SHA256 불변.

후속(2026-10-10): 친구 이름 뒤에 활동 문구를 붙이는 경계를 수정한 CPU 후보를 추가했다.
cap6 사람 이름을 검증하고 private stack에서 suffix를 합친 뒤 cap10 최종 제목 전체를 검증한다.
완성된 제목만 pool에 반영하므로 한글 rank/E4 payload 안의 E5를 종료 문자로 오인하지 않는다.
원작33014의 조건 분기와32E22 호출부도 연결했다. 실패하면 확인창 초기화를 건너뛰고 exit16으로 돌아간다.
`create-kr-patch`의 실패 원자성 기준으로 caller의 무조건 진행도 함께 수정했다.
증거: `analysis/hangul_keyboard_v1/cpu_calendar_activity/report.json`; 원작 sprite/heading/sound는 모사다.
현재 suffix script0x45의 문구는 원문 그대로이며, 이번 단계는 토큰 처리 수정이다. 실제 ROM/세이브는 미변경이다.
다음 미해결 경계는 exit16의 실제 메뉴 복귀, 기존/새 저장형식 선택, 전체 readers 및 실제 한글 자판 화면·저장/재로드다.
별도 CPU11454조건/34334 whole EWRAM 비교 PASS, 전체음절11172 및 embedded E5 43음절 포함. 변경2도구 py_compile PASS.

후속(2026-10-10): 최종 표시 제목 → 새 고정 기록 → 원작 등록 → CPU 재표시 연결을 구현했다.
기본 ‘식사’와 사람 이름+활동 문구를 같은 저장 경계에서 변환하며, 재입력용 stage는 보존한다.
`tools/bench_calendar_title_record.py`가 전체 11172음절의 10글자 제목과 6글자 이름+3글자 suffix,
E4의 모든 payload, 잘못된 토큰/길이/주소 및 255개 기록 주소를 검사한다.
변환 결과는 stack에서 완전히 검증한 뒤 22바이트만 기록한다. 기록을 HOST가 다시 쓰지 않고 CPU decoder로 읽는다.
create-kr-patch의 실제 소비자 경계·실패 원자성 기준으로 이전 stage-only 저장 후보를 보완했다.
이는 ROM 미반영 CPU 후보다. 원작3302C의 byte 단위 suffix 탐색은 여전히 F9FC 안의 E5를 오인한다.
다음은 suffix 추가 경계를 token-aware로 연결하는 작업이며, 기존/새 저장형식 선택과 전체 reader 연결도 필요하다.
새 보고서: `analysis/hangul_keyboard_v1/cpu_calendar_title_record/report.json`. 누적 foundation 전체는 이번에 재실행하지 않았다.
별도 CPU 실행23211조건/46318 whole EWRAM 비교 PASS, 변경2도구 py_compile PASS.

후속(2026-10-10): current ROM의 실제 달력8경로를 normal controller로 실행해 이름 버퍼 수명을 확인했다.
기본‘식사’는stage02026280를 건드리지 않고 pool→저장field로 복사한다. 친구 입력은실제cap6/heading0x26이다.
친구 확인 시pool에activity suffix(script0x45=69)가 붙고 그전체가저장된다. stage는사람이름만 유지한다.
‘아니오’→재입력은suffix없는stage를import한다. 따라서stage를그대로저장하면일정의활동문구를잃는다.
create-kr-patch의실제writer/자료수명 기준으로기존cap10 CPU후보의무조건설치를거부했다.
다음연결은기본이름변환·입력cap별정규화·사람이름→완성일정이름변환을분리해야한다.
관찰/검증2도구py_compile 및새runtime보고서PASS(8경로/동일ROM ancestry12노드). 기존CPU누적PASS는유지하되이번에재실행하지않았다.
원작일본어자판그대로의관찰이며새한글hook/저장형식/화면/저장·재로드완료주장이아니다. ROM은미변경이다.

후속(2026-10-10): 명시적으로 선택된 새 cap10 이름 원본→표시 pool→두 원작 등록 경로를 CPU 연결했다.
저장은 표시 문자열이 아니라22byte 원본을 검증한 뒤 복사하며, 실제255개 record 주소/stride와context pointer를 검사한다.
전체11172음절×두경로 및255주소,22745등록 조건/45448 whole EWRAM 검사 PASS.
실패42조건은 기록·원본·표시cache·등록metadata를 보존하고 성공 등록을 건너뛴다.
직접 입력 경로의 성공음도 검증 후로 옮겼다. create-kr-patch의 자료 분리·경계·실패 원자성 기준을 적용했다.
이는CPU fixture의 구현이며 stage 수명/형식dispatch는 미채택이다. sound/selector/등록 후 번호 갱신은 모사, 직접selector0경로는 미검증이다.
실제ROM hook·기본이름/import/query연결·기존save구분·화면·저장/재로드는 남아 있다.
누적 foundation 전체 재실행 및 변경3도구 py_compile PASS. ROM3종 SHA256 불변, 사용자 세이브 미변경.

후속(2026-10-10): 실제 달력 등록 경로32EFE→32AC6→37366의 복사·등록 메타데이터를 CPU 실행했다.
22353조건 whole EWRAM 검사로 잘못된 연결의 위험을 재현했다. 새 이진 레코드는43음절에서 조기 종료된다.
10글자 F9FC 표시 문자열은11129음절에서22byte 이름 필드를 넘어 다음 레코드19byte를 침범한다.
나머지43음절은 embedded E5에서 잘리지만 두 경우 모두 원작은 등록 성공 상태로 진행한다.
create-kr-patch의 소비자 경계·공유 자료 수명 기준에 따라 pool을 저장 원본과 표시 cache로 겸용하는 연결은 미채택이다.
이 PASS는 위험한 경로를 재현한 반례 검증이지 안전한 저장 완료가 아니다. 실제 ROM/세이브는 변경하지 않았다.
다음 필수 조건은 별도 canonical 이름 수명, 기존/새 형식의 명시적 선택, 경계 검사된 실제 commit 및 모든 reader 연결이다.
누적 foundation 전체 재실행 및 변경2도구 py_compile PASS. ROM3종 SHA256 불변을 다시 확인했다.

후속(2026-10-10): 새 cap10 달력 기록→원작 이름 표시 함수33C94→pool 문자열→확인창 count를 CPU 연결했다.
전체11172음절/확인 count11263조건 및 원작 고정폭 parser의 대표84조건(각640byte 픽셀) PASS.
잘못된 record14조건은 pool/기록/인접 필드를 보존하고 표시 요청을 건너뛴다.
create-kr-patch의 기록·표시 identity/자료 수명 기준을 적용했다. heading·문자열 lookup·sprite·transfer 서비스는 모사다.
81 E5가 기존 일본어 문자열과 새 record 양쪽으로 해석되는 반례도 확인했다. 따라서 자동 형식 판별은 미채택이다.
실제 저장 형식 선택·기본값/기록 writer 연결·화면·저장/재로드와 ROM 설치는 아직 미완료다.
누적 foundation 전체 재실행 및 변경3도구 py_compile PASS. ROM3종 해시 불변, 사용자 세이브 미변경.

후속(2026-10-10): 달력 확인 후 새22byte 레코드를128byte-stride 문자열 pool로 넘기는 처리를 CPU 연결했다.
원작 경로의 marker 소실11172조건과 embedded E5 때문에 마지막 글자가 잘리는43음절을 재현했다.
전체11172음절 및 길이/변조/범위 검사를 포함한22501 whole EWRAM 검사 PASS.
레코드 전체 검증 후22byte만 복사하며, 실패 후 다음 화면으로 진행하던 호출부도 기존 취소 상태로 연결했다.
create-kr-patch의 소비자 경계·실패 원자성 기준을 적용했다. pool3슬롯과 새 형식은 명시적 CPU fixture다.
실제22byte 저장 필드에 크기는 맞지만 기본 이름/확인창/목록/재로드의 형식 처리와 소유권 검증이 남아 ROM에는 미설치다.
누적 foundation 전체 재실행과 변경3도구 py_compile PASS. 원본/playable/glyph-only ROM 해시는 불변이다.

후속(2026-10-10): 새 초기화/확인 처리와 원작 진입·종료 상태 전이를 CPU clone에서 연결했다.
용량1~10/대체 heading bit/호출값0·1·2 조건, 초기화120회·프레임4620회 PASS.
‘아니오’120/대기120/미완성 자음60은 결과 버퍼를 보존하며, 확인60/취소 종료60의 완료값1·2를 구분했다.
확인 후 재진입60회는 편집 상태를 초기화하고 결과 버퍼를 유지한다. 카운터 wrap60조건도 PASS.
이 lifecycle 검사는 그리기·입력 상태12·preload를 모사한다. 이전 입력/픽셀 검사와 합친 전체 화면 경로는 아니다.
create-kr-patch의 상태 초기화·종료/사용자 문자열 보존 기준을 적용했다. 실제 ROM hook/화면/저장·재로드는 미완료다.
가장 중요한 미해결 조건은 cap10 레코드의 실제 저장 공간과 후속 redisplay consumer다. ROM과 세이브는 보존했다.
누적 foundation 및 변경 도구 py_compile PASS. calendar 확인 후 staging→128byte-stride pool의 rawE5 복사 경로를 추가 확인했다.

후속(2026-10-10): 원작034E34의 입력 상태12 프레임에 새 자판/입력창 갱신을 CPU 연결했다.
원작 일본어 이동 보정 때문에 방향키로 선택 불가능했던 `ㅕ`, `ㅗ` 두 칸을 한글 페이지에서만 보정했다.
3페이지×96위치×5방향 mask1440조건 및 HOST 위치 재기록 없는40자모 선택·허용 입력 되돌리기 PASS.
2213프레임/1030입력 커서/2330전송과 무입력 프레임을 통한 보류 갱신 재시도2경로 PASS.
원작 padding/flatten을 함께 대체하고 caret query/먼 거리 render veneer를 추가했으며 stack248byte CPU 한도를 검사했다.
create-kr-patch의 입력·선택·표시 연결 기준으로 두 접근 불가능 자모를 찾아 수정했다. 누적 foundation/py_compile PASS.
실제 ROM에는 미설치다. 초기화·확인·종료 상태, RAM/IRQ 수명, 실제 한글 화면과 저장/재실행은 미검증이며 ROM3종은 보존했다.

후속(2026-10-10): raw 자모/삭제/커서 입력→자동 조합→cache→원작 입력창 픽셀 생성/전송까지 연속 CPU 연결 PASS.
666버튼/781전송, 화면 갱신920호출 중139보류 및 전송 후 최신 입력 재표시2경로를 검증했다.
대기 중 stage 버퍼를 읽는 queue 항목이 있으면 갱신을 미루며1140범위 경계/잘못된 editor7조건을 검사했다.
원작 parser의 r8/r9/r10을 복원하며 중첩 stack144byte. 기존 페이지 경로와 누적 foundation/py_compile PASS.
create-kr-patch의 입력 상태·전송 자료 수명 보존 기준을 적용했다. CPU fixture이며 BIOS 등 일부 서비스는 모사다.
원본/playable/glyph-only ROM 해시 불변. 실제 ROM hook·게임 프레임/IRQ·한글 화면·저장/재실행 검증은 미완료다.

후속(2026-10-10): raw 버튼→페이지 제어→원작 타일 전송/배치/queue 소비 연속 CPU 연결 PASS.
623버튼/477페이지 전환/865배치/725소비 및40자모의 페이지 왕복·삭제를 검증했다.
실제 버튼 처리로 queue96칸을 채웠으며97번째 전환은 페이지/편집/queue/VRAM을 보존하고 거부한다.
큐가 찬 동안 자모 입력·삭제도 유지된다. 검사 없는 비교 코드에서 화면/페이지 불일치 반례1건 재현 후 예방했다.
원작 queue/page uploader는 실제 실행, BIOS/음향/화면 설정/스프라이트 제출은 모사다.
ROM/실제 게임 화면/save 미적용 상태이며 outer frame/입력창 갱신·명령/Latin/공백·IRQ 동시성은 남았다.

후속(2026-10-10): 40자모 page0 타일/배치 자료(5472/1200byte)를 만들고 원작 page draw/upload에 CPU 연결했다.
90칸 중40자모/50빈칸은 기존 selector와 일치하며, grid 밖 배경·명령 영역 픽셀을 보존한다.
원작 IWRAM 배치/클리어 및 ROM queue enqueue/drain 실행:108배치/72전송등록/36소비/36포화거부 PASS.
원작 커서1152조건, 자모 위치 정렬480조건 PASS. BIOS/화면 설정/스프라이트 제출 서비스는 모사했다.
오프라인 타일 미리보기는 기존 관찰 palette9를 사용하며 실제 한글 자판 에뮬레이터 화면은 아니다.
ROM 미설치. 페이지1/2·명령 라벨·Latin/공백·outer frame/편집창 갱신·save/reload는 남았다.

후속(2026-10-10): raw 버튼 입력→자모/커서·페이지/Start/빈B 취소 연결 후보를 구현했다.
원작 BL/BNE CPU 실행에서 B>A>Start>L>R 우선순위,1024버튼 mask×4칸×3편집 상태12288조건 확인.
72235입력 호출 및 한글11172종 A조합→Start2회→예/아니오를 HOST compact/record 재기록 없이 검증 PASS.
실제 ROM에는 미설치이며 outer frame/페이지 그래픽·Latin·공백·음향/대화창 실제 실행·save/reload 검증은 남았다.

후속(2026-10-10): 원작 페이지/Start/빈 입력 취소112조건과 비교 루틴6조건 CPU 검증.
원본·현재 ROM의 확인 목록은 빈 입력 항목 하나이며, 빈 안내(script11)와 일반 확정(script10)을 구분한다.
새 논리 제어 코드에 페이지 전환·2단계 Start·빈 취소·미완성 거부를 구현했다.
11452제어/144페이지 전환 및 한글11172종 요청→예5586/아니오5586 연속 CPU 검증 PASS.
확정 요청은 stack 임시 저장 검사만 하며 실제 레코드는 예에서만 기록한다. raw키 연결/페이지 그래픽·실제 UI·ROM 설치·save/reload는 미완료다.

후속(2026-10-10): 원작353B0 호출부의 BL/BNE에 새 A/B·글자 커서 처리 후보를 CPU 연결했다.
40자모/빈칸 거부, B 우선·조합 이력 되돌리기/불러온 음절 분해·좌우 이동 및 조건 플래그 보존 확인.
52647호출, fullcap4 마지막 칸 한글11172종의 실제 A칸 선택→조합→B 검증 PASS.
페이지0 후보 배치만 사용하며 페이지/확정/취소/음향·거부 표시와 실제 화면·ROM 설치·save/reload는 아직 미완료다.

후속(2026-10-10): 원작 metadata 호출부→새 초기화→혼합 레코드 가져오기→재확정 CPU 연결 PASS.
완성11172종을 fullcap4 마지막 칸에 복원하고, 단계 사이 HOST editor/record 재기록 없이 같은 레코드로 재확정했다.
16개 descriptor row, 잘못된/빈 레코드64건 및 editor96 전체 겹침·잘못된 주소37건 거부를 확인했다.
두 BL은 CPU source clone에만 교체했다. 형식은 명시 선택이며 원작 caller의 실패 처리 UX, 실제 ROM 자판·화면·save/reload는 미완료다.

후속(2026-10-10): 선택 설정→원작 initializer/import 호출부를64회 CPU 실행해 selector가 metadata row index임을 확인했다.
descriptor2..17→metadata0..15에서 원작이 글자수/제목을 조회한다. descriptor16→row14→cap4 연결도 확인했다.
기존 문자32건은 정상 재진입, 새 '곥' packed record32건은 기존 importer에서 빈 입력이 된다.
초기화/가져오기 두 호출부도 함께 교체해야 하며 ROM 설치·실제 화면/save는 아직 미완료다.

후속(2026-10-10): descriptor 삭제/선택 설정 소비자2개를 추가 확인하고 원본·현재 ROM26항목씩 CPU 실행했다.
삭제52회는 pointer-1을0으로 하고 기본값을 덮는다. 설정52회는 pointer-1과 selector를0200F550에 넣는다.
16개는 첫 저장 record marker,10개는 다른 cache 앞 byte를 가리킨다. selector를 자판 글자수로 해석하지 않는다.
별도 형식 정보나 표시 cache를 도입할 때 이 삭제·설정 전환까지 처리해야 한다. ROM hook은 미설치다.

후속(2026-10-10): CPU 자모 입력→자동 조합→고정 레코드 저장→원작 대사 provider 연속 검증 PASS.
37506 key입력, 완성11172종 fullcap4 마지막 슬롯 및 초성 상태 확정 거부11172회 확인.
단계 사이 compact/record/display 문자열 HOST 재기록 없이 최대17byte 문자열을 전달했다.
초기 editor/context/입력키는 fixture이며 실제 자판 조작·형식 자동판별·한글 화면·save/reload 검증은 아니다.

후속(2026-10-10): 원작 printStringBuffer 대사 처리 루틴의 복사 단계에 저장→표시 변환 후보80byte를 연결했다.
descriptor16의 cap4 레코드를 대사 cache에 직접 확장하며 임시 문자열/저장 레코드를 쓰지 않는다.
완성11172종 마지막 슬롯, 변수형 selector8건, legacy144조건의 register/CPSR/memory 대조 PASS.
CPU fixture만 변경했으며 실제 ROM hook은 미설치. format 판별, cache 수명/선택 레코드 연결 및 실제 화면·save가 남았다.

후속(2026-10-10): 원작 일본어 확정·복귀 경로에서26개 metadata 갱신과 저장 레코드 내부 복사를 실제 관찰했다.
임시 문자열02014E74+32의02014E94는 다른 루틴이 읽는4byte 카운터이며, 최대41byte 확장은 이를 침범한다.
8글자 최대33byte 문자열도 카운터 첫 byte를 덮으므로 임시 버퍼를 단순 확장하지 않는다.
관찰된 fixed-cell provider860건은 모두 descriptor0이며 실제 한글 대사 삽입 증거는 아니다.
별도 표시 저장소와 소비 경로 연결이 남았으며 ROM·사용자 save는 변경하지 않았다.

후속(2026-10-10): 혼합 고정 레코드→표시 문자열 Thumb428byte 후보 구현(중첩 stack80byte).
완성11172종 fullcap10 저장→표시 변환 및 occupied-word65536domain 포함82820 CPU호출 PASS.
별도 compact/history/transition table 없이 구조를 검사하고 최대41byte 문자열을 생성한다.
원작 rawE5 복사 코드에서 '곥'/E4-E5 payload가 잘리는 반례2건도 CPU 실행으로 재현했다.
26 metadata 중16개 descriptor는 첫 저장 레코드 내부를 가리키며,26개 모두 최대 한글 표시 복사 한도가 부족하다.
따라서 레코드 직접 덮어쓰기나 descriptor 한도만 늘리는 변경은 미적용. 별도 표시 저장소/reader·provider 연결이 남았다.
ROM설치 및 실제 한글 대사·save/fresh-load 검증은 미완료다.

후속(2026-10-10): 실제 '예/아니오' handler212진입을 관찰하고 새 확정 처리 Thumb152byte 후보 구현.
원작은 commit 반환값을 검사하지 않고 종료하므로 호출 함수만 바꾸면 미완성 확정 거부가 되지 않는다.
새 layout에서는 검증 성공 때만 record를 쓰고 state14로, 실패/취소는 record를 보존하고 state0C로 복귀한다.
12579 CPU호출/성공11703/거부616/대기256/취소4, 원작 대기·취소258조건 대조 PASS.
완성11172종 및 저장대상-editor96 겹침/주소 overflow 거부 포함. dialog/sound 서비스는 CPU에서 모사했다.
ROM hook 미설치. 실제 캡처는 원작 일본어 자판 정상 경로이며 한글 자판 화면·save 검증이 아니다.

후속(2026-10-10): compact 편집 상태→혼합 고정 레코드 확정 연결 후보 Thumb944byte 구현.
4/10글자 full field의 완성11172종 각각, history입력·되돌리기140단계 포함23202 CPU호출 PASS.
미완성·빈 기록·잘못된 compact·짧은 버퍼·겹침467거부 시 원본/저장대상 유지 확인.
원작 기록 선택 루프의26 metadata/57 slot×marker256종14592조건에서는0만 제외했다.
정상 경로9 RAM캡처513기록의 marker는0(511)/1(2)였지만 새 값 예약이나 save 호환성 증명은 아니다.
원작 확정 ABI/형식 선택·모든 writer/consumer 교체·ROM설치 및 fresh-load 검증은 미완료다.

후속(2026-10-10): 한글·native 혼합 고정 레코드 저장408byte/불러오기486byte Thumb 후보 구현.
완성11172종을 가득 찬10글자 마지막 칸에 넣어 CPU 저장→불러오기 연결 PASS(중간 host 재기록 없음).
저장77393호출/불러오기83262호출, 미완성·빈 기록·잘못된 값·짧은 버퍼·겹침 거부 및 쓰기 경계 검사.
원작 importer에서 '곥'의 새 레코드가 빈 문자열로 읽히는 반례도 직접 실행했다.
따라서 marker 자동 판별은 채택하지 않고 caller가 새 형식을 선택하는 후보로만 검증했다.
실제 commit/reader/normalize 교체·save/fresh-load·한글 자판 화면·ROM 반영은 아직 미완료다.

후속(2026-10-10): 실제 입력·삭제·B/No·확정·대화 복귀 경로에서 cache/stage writer 추적 완료.
860회 cache 소비 및 deferred 전송 구간에 관찰된 덮어쓰기0건.
원작 cache byte write27520회/stage word write275200회로 관찰 callback 작동도 확인했다.
512byte cache/1280byte stage/editor96/record10의9캡처×4구간36개는 이전 실행과 일치했다.
전체 메모리 비교45개 중27개는 달랐고 RTC/CPU 상태 차이가 관찰됐다.
따라서 전체 byte-identical 회귀 PASS는 주장하지 않는다. 한글 cache41byte 소유권/ROM설치도 미완료다.

후속(2026-10-10): 원작 표시 provider의 호출 규약을 유지하는 선택적 복사 연결 후보924byte 구현.
입력창 descriptor0/slot0의 확인된 인수·복귀 주소만 compact→41byte 표시로 전환하며,
다른 descriptor/slot95조건은 원래 복사 결과와 일치했다(512byte 공통 버퍼 포함).
새 표시531조건/잘못된 compact76건의 빈 E5 fallback, 직접 복사 ABI/NZCV7조건 PASS.
연결은 CPU fixture의 포인터 한 곳만 바꿔 검사했다. 기존 editor와 혼용할 수 없으므로 ROM미설치.
132byte 중첩 stack/원작 provider 포함176byte는 fixture 결과이며 게임/IRQ 예산은 미확정이다.

후속(2026-10-10): compact 편집→41byte cache→원작20셀 parser/copier→전송 큐 등록·소비 연결 PASS.
639회 렌더링에서 최대10한글/미완성 자음/native token/빈칸/tint를 검사했다.
70번 native 입력과70번 history B를 중간 host 재기록 없이 픽셀 생성까지 연결했다.
원작 전송 큐는 실제 실행했지만 BIOS CpuFastSet은 모사했으며 VBlank/화면 검증은 아니다.
큐 포화96건에서 새 항목이 등록되지 않는 동작도 확인했다.
새 cache의 실제 소유권·hook ABI, 자판 선택 연결·확정·save/fresh-load는 여전히 미완료다.

후속(2026-10-10): 원작 입력창의 실제 전송860회를 에뮬레이터에서 추적했다.
mono8 글꼴/20셀1280byte pixels가 요청 큐에 등록되고 다음 프레임 VRAM에 복사되며,
등록·소비·복사 후 데이터가 모두 일치했다. 일본어 정상 입력 경로의 증거이며 한글 화면은 아니다.
compact76→최대41byte 표시 cache 연결 Thumb804byte를 구현하고852 CPU호출/거부311 PASS.
70키 history, 미완성 자음, native token, 겹침·짧은 버퍼 거부와112byte stack 경계를 검사했다.
기존 descriptor0의32byte 복사 교체와 새 버퍼 수명/전체 writer 검증은 아직 ROM에 설치하지 않았다.

후속(2026-10-10): 새 mixed 표시 CPU출력→원작 fixed-cell parser→글꼴 선택→copier→빈칸 채우기 연결 PASS.
24,584 parser호출에서 완성11172종×big/mono, 미완성 자음, native token, 모든 길이/위치/tint를 검사했다.
최대10글자 F9FC 표시41byte도 소비했다. VRAM 전송 함수는 모사했으며 실제 게임 화면 증거가 아니다.
**이 fixed-cell 입력창 후보 경로는8pixel/cell이며 대사의12pixel advance와 다르다.**
이전의 커서8pixel 대 한글12pixel 충돌 가정은 서로 다른 provider를 섞은 것이므로 채택하지 않는다.
실제 입력창 font selection/descriptor0 cache41byte/커서 연결·확정·저장은 여전히 미완료다.

후속(2026-10-10): compact76의 현재 커서 위치/글자 수를 복원해서 반환하는 native query 후보 추가.
25,180 CPU호출/거부262 PASS. 원작 pointer_count leaf570조건 대조,
완성 한글11172종 native 마지막 자모 편집→query22344회 연결(중간 host 재기록 없음) PASS.
새 반환 ABI는 value/status이며 원작 pointer live-out ABI나 화면 pixel 계산은 아니다.
직접 BL 후보4곳 확인. 실제 화면 커서와 새 logical query의 연결은 아직 미완료다.

후속(2026-10-10): 원작 초기화 register ABI 연결 후보 Thumb60byte 추가.
10,240조건의 r0..r3/NZCV가 원작 body와 일치하고, shim10,479호출/지원외239거부 PASS.
중첩 stack140byte는 CPU fixture 범위이며 게임/IRQ 예산 증명이 아니다.
직접 BL 후보5곳의 명시적 코드창을 확인했다. 간접 호출/전체 caller·writer 검증은 미완료.
호환용 r2=editor+32는 새 배치에서 옛 wordbuffer가 아니다. 구 reader 동시 교체 전 ROM미설치.

사용자가 자동 자모 조합 방식 선택. 기준 자동조합/삭제/불러온 문자열 재편집 구현과 11개 계약 검사 PASS.
현대 한글11172 생성·되돌리기/불러오기·삭제 검사, 독립 Thumb 완성음절 인코더11187 CPU벡터 PASS.
40자모 고정셀/105선택지 후보 생성; 정적 미리보기이며 실제 게임 화면이 아니다.
현행동일ROM 정상입력 trace에서 질문의 4글자·10바이트 레코드 간격과 제자리 reader를 확인했다.
기존 F9FC 표시코드를 기록에 그대로 복사하면 범위를 초과하므로 저장/표시 분리가 필요하다.
**한글 자판 ROM 통합·한글 저장/재표시는 미완료**, 이번 작업에서 ROM/사용자 세이브 변경 없음.
현재 메모리방향: 외부baseline없는 mixed replay76byte HOST 후보,5계약검사 PASS.
기존UI16byte+destination4byte+state76byte=96byte 배치후보이며실제메모리채택은아니다.
588byte delta/native kernel은이전wide reference증거로보존;그크기를게임RAM/stack에할당하지않는다.
현재compact76 native복원/편집/표시후보를검증중이며다음게임연결은기존pointer/표시/확정reader동시교체다.
후속(2026-10-10): compact76→mixed current24 Thumb428byte,627595 독립CPU호출 PASS.
전체packed key replay/불가능전이·overflow거부,68byte stack/전체history scratch0을검증했다.
새surface는count/cap/cursor/activeFF라기존pure-Hangul표시ABI와다르며ROM미설치다.
mixed current24→display Thumb292byte,259347표시CPU검사/전체11172음절 native replay→display연결 PASS.
sealedpartial은어느칸이든편집표시/확정거부,원래native token바이트를보존한다.실제cache/자판화면/저장은미연결이다.
호스트검사보고서의시간정보를identity에서제외해CPU증거의dependency hash가재실행에도유지되도록수정했다.
중단된전체foundation검증 PASS(편집helper추가전68개도구결속).
compact76 자모추가/accepted-key B 후보 구현,26421편집CPU호출 PASS.
전체11172음절 native edit→replay→display연결도PASS;실제게임입력창/저장은미연결이다.
중첩stack196byte의게임예산은미확정이다. canonicalB/move/nativewrite·rebase는아래후속에서CPU후보구현했다.
새편집helper포함foundation전체 PASS,71개도구hash 및원본/현재ROM identity보존확인.
후속:compact76 일반B/커서이동/nativeoverwrite rebase804byte와native명령dispatcher56byte 후보구현.
214664명령CPU검사 PASS:11191완성/부분word×10각칸삭제,65536actiondomain,31460native-capacity/cursor경로.
native dispatcher로5000연속혼합명령실행;sealedpartial보존/원작중간overwrite/무변경거부확인.
실제editor96byte writer교체·초기화/import·표시cache/cursor/dest·stack/IRQ·저장/재실행은미완료다.
rebase/dispatcher포함foundation전체 PASS;74개도구/59개artifact hash와원본/현재ROM identity재확인.
후속:caller가legacy형식을선택한record→compact76 import/init Thumb196byte,stack96byte 후보.
97506불러오기CPU검사/원본importleaf4840대조/실제import출력→자모입력→B복구4840경로 PASS.
빈편집상태초기화·cursor0·nativeescapepayload보존확인. 새저장형식판별/실제game96byte초기화는미연결이다.
importhelper포함foundation전체 PASS;76개도구/61개artifact hash 및원본/현재ROM identity재확인.
후속:editor96 staging초기화 Thumb180byte/stack116byte 후보구현.
원본초기화UI16/목적지와10240조건대조 및새초기화10491CPU호출 PASS(원본clear서비스는모사).
13개boundedconsumer코드영역을해시/ISA검증해교체경계로기록했다. 전체writer감사/원본ABIhook은미완료다.
초기화계약포함foundation전체 PASS;78개도구/63개artifact hash와원본/현재ROM identity재확인.
커서 인식 혼합 상태의 고정폭 host codec 후보588byte 구현: 헤더/10칸28byte +70회 delta560byte.
전체11172음절 왕복·uint16 word전체65536·모든짧은extent588개·70undo 검사 PASS.
이것은실제RAM할당/저장레코드/native CPU 구현이아니며이전64byte overlay에넣을수없다.
현재진행방향은native혼합편집 코드와메모리소유권/수명 검증이며 ROM반영전조건을완화하지않는다.
후속: 혼합 B/undo Thumb508byte,109090 독립CPU호출 PASS(52byte stack/미설치).
유효한canonical상태를caller가보장해야하며전체이력decoder가아니다. 위조전이허용반례를보존했다.
이력검증/native입력·메모리배치·화면/저장 연결은미완료다.
후속: 커서 인식 mixed feed Thumb404byte와기존B 연결,1266270 독립CPU호출 PASS.
11192row×40키/10각칸의전체11172음절입력·undo/연속native220경로를검사했다.
입력/삭제kernel은유효history전제의미설치후보이며nativecursor/초기화와RAM수명·혼합화면/저장은미연결이다.
인계 `analysis/HANGUL_KEYBOARD_HANDOFF.md`, 기반 해시검증 `analysis/hangul_keyboard_v1/foundation.json`.
후속: 저장 표현→표시 Thumb 변환 후보 유효134136/거부291 CPU벡터 및5개 호스트 계약 PASS.
기존 저장 코드의87음절 절단/4글자8byte초과를 독립 CPU로 재현했다. 새marker/저장ABI는미채택.
732sourceTPL의3803 named표시명령 조사: 어려운과목은전용descriptor16(68참조),공용28..30과구분.
자동조합/B삭제 Thumb 후보 추가: feed304/undo344bytes, 독립CPU590868검사 PASS(ROM미설치).
입력 상태 뒤276byteRAM후보는 정상CPU접근17그룹과 겹쳐 배제. 64byte압축 상태 호스트4계약 PASS.
64byte native wrapper604bytes 구현, 독립CPU154592검사 PASS(미설치).
게임RAM 소유권·444byte 임시stack 예산·baseline 수명·자모 화면 연결은 다음 작업이다.
정상입력 observer에서 B/No복귀·입력유지/Yes확정과 descriptor0의32byte 복사를 확인했다.
64byte 상태 후보는 기존 FC60..FC9F와 겹치므로 편집/매프레임 표시/확정의 동시 교체가 필요하다.
편집 상태→표시 Thumb 후보244bytes,201959 CPU검사 및 native조합→표시57경로 PASS.
기존 쉼표 index11172를 보존하는40자모 일반폰트3840byte 후보 생성(현재ROM미공급).
별도 글꼴공급 ROM `poc/output/exe45_ko_development_keyboard_glyphs_v1.gba` 생성:
40자모 normal/big/mono 공급, native copier22718 CPU검사/타이틀까지coldboot 확인.
SHA256 `bc3af1afc5855f8e1161d6a5e5f6cffcfeb66952beb86edcc875107fb9e0d4bd`.
자동조합/선택/표시 연결은 미설치이며 실제 자모 화면 미검증. 현재 플레이 기준으로 승격하지 않았다.
옵션 없는 기존빌드 재생성 SHA256은 기존제품과 일치했다. 근거 `analysis/hangul_keyboard_v1/glyph_supply.json`.
현재 플레이 제품은 아래 입력창 제목 ROM 그대로다. NON-DISTRIBUTION.
후속: 정상 B/No/Yes 경로에서860회 descriptor0→020155F0 cache→동일 호출 parser 소비/slot 초기화 확인.
원본 코드/literal와128byte stride를 결속했다. 실제33byte 한글 출력/자동조합 hook/저장은 아직 미설치다.
현재 근거 `analysis/hangul_keyboard_v1/display_cache.json`, foundation33도구 검증 PASS.
후속: 초기화 진입/용량4·제목33·기록 목적지와 No까지 원래 기록 유지→Yes 갱신을 정상 경로에서 확인.
record→baseline Thumb180bytes 구현,190793 CPU검사/네이티브 조합 연결35경로 PASS(미설치).
기존 일본어 기록은 무변경 별도 분기로 구별한다. nonempty import/실제 stack·IRQ·저장 호환은 미완료.
근거 `analysis/hangul_keyboard_v1/lifecycle.json`, `cpu_baseline_bridge/report.json`.
추가 source caller에서 **기념일 내용 최대10글자**와 flag-driven staging import를 확인했다.
8글자 후보를 전체 상한으로 채택하지 않는다. key-log64/70키 호스트4계약과10글자 backend120468 CPU검사 PASS.
native key-log replay604byte 구현,154574 CPU검사 PASS. baseline24/64byte 상태/최대70키 연결(ROM미설치).
10글자 표시·기록·import bridge와 실제 stack·IRQ는 아직 미연결. 임시 stack472bytes는 게임에서 미승인.
근거 `analysis/hangul_keyboard_v1/extended_scope.json`, `cpu_extended_composer/report.json`.
최신 연결 근거 `analysis/hangul_keyboard_v1/cpu_keylog/report.json`.
10글자 표시 helper228byte/read-only replay→표시 bridge496byte 추가, CPU241025회 PASS.
각10칸×11172음절·rank uint16전체·fresh/loaded keylog와41byte 출력 경계 확인.
읽기 전용 표시 경로 stack408bytes; ROM 화면/커서/cache/저장 연결은 아직 미설치.
근거 `analysis/hangul_keyboard_v1/cpu_ten_cell_display/report.json`.
호출자 선택형10글자 baseline24 helper196byte 추가, CPU207604회 PASS.
marker0/1도 import 요청 시 원문 보존 분기(무변경)를 반환한다. 일본어 재편집/실제 import는 미구현.
후보 한글기록→baseline→native편집/표시 연결 확인; 저장marker/ROM hook은 미채택.
근거 `analysis/hangul_keyboard_v1/cpu_ten_cell_baseline/report.json`.
원본 import/flatten/중간삭제/덮어쓰기10900 CPU호출 확인. 원래 import 커서는 첫칸에 유지된다.
기존 일본어칸은 한글rank와 겹치므로 opaque tag 내부표현 후보484개 왕복/uint16전체 검사 PASS.
현재 tail-only 한글keylog는 원작 중간편집/legacy문자를 보존하지 못해 그대로 설치할 수 없다.
다음은 혼합문자·커서 인식 편집과 실제 nonempty import/stack/저장 검증이다.
근거 `analysis/hangul_keyboard_v1/legacy_edit.json`.
커서 인식 혼합 편집 host 모델 추가:6계약/10칸×11172한글/484문자×10용량 PASS.
불러온 커서0·native중간삭제/덮어쓰기·한글carry/undo·모든위치partial확정거부 확인.
host snapshot 이력은 이전keylog64 ABI가 아니며 native기계어/혼합표시/저장/UI검토는 미완료.
근거 `analysis/hangul_keyboard_v1/mixed_editor_host.json`.

## 현재 플레이 제품: 입력창 제목 (2026-10-09)

6368E8:33:0 `にがてな かもくは?` → `어려운 과목은?` 추가 적용, 누적2549literal.
현행ROM `poc/output/exe45_ko_development_input_heading_v1_r2.gba`, SHA256 `5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4`.
최초_v1/독립_repro/도구고정_r2 동일bytes. 기존16unit/254공용scripts/59다른payload·폰트/주요이미지/keyitem39 보존 PASS.
새ROM 정상29→입력창의mono glyph→stage→VRAM→BG2 1280pixels·No복귀 제목유지·삭제/재입력/예/아니요 PASS. 자체native save58/coldcontinue는 입력전회귀다.
27fixture/748AST·r2의748Python pins drift=[]·big/mono native copier22390 CPU벡터 PASS.
기록 `analysis/INPUT_HEADING_HANDOFF.md`, 검증 `analysis/input_heading_v1/runtime.json`, 화면 `heading_pages.png`, 현행catalog `analysis/full_scope_input_heading_v1_r2/`.
미선택일본어27499/기타1859. 다른입력제목·키보드/한글입력·전체미번역/이미지/상점/RTC/인간검토/배포검증 미완료; NON-DISTRIBUTION.

## 이전 검증 제품: 공용 입력 확인창 (2026-10-09)

6368E8:10:0..2를 `이대로 정할까요? / 예 / 아니요`로 추가 적용, 누적2,548literal/60선택·672원본유지archive.
ROM SHA256 `68260ec96c118939efa66f24f077dd06d375bdebffb8246529bcdfd6c45e87a6`.
최종 도구 고정ROM `poc/output/exe45_ko_development_input_confirmation_v1_r3.gba`, 최종 감사 PASS. 실행은동일byte 최초_v1; _v1/_repro/_r2/_r2_repro/_r3 다섯제품의전체ROM동일.
3문구 정상fontCPU/OBJVRAM/픽셀·Yes/No커서·No/B 키보드복귀/편집값유지·No후재확인창 PASS.
원본/ledger/append·기존13unit/254scripts/59payload·폰트/이미지/keyitem39 보존 PASS.
정상29/키보드·PET22/소개2/넘버맨3/플러그아웃 대표회귀·새native save58/coldcontinue PASS. 새save는입력전 회귀이며 입력값 영구저장증거가아니다.
125fixture/742AST·742Python 도구pin drift=[], CPU624 합성helper계약 PASS. 최종 감사 `analysis/input_confirmation_v1/final_identity.json`.
native확정writer08035000을관찰했다. 첫1은길이가아닌constant marker, editing0200FC80→FC40+1C목적지020010A6에바이트복사/E5또는98종료.
후속 정상 일본어입력은4글자까지, 다섯입력거부/B삭제/재입력/Yes반응93을 확인했다. 실제저장완료28→savestate없는새실행 native continue→거츠맨PET에서 같은record019b9b9b9be500 복원 PASS.
`analysis/input_entry_v1/native_input_persistence.json`/`native_input_pages.png`에 전후SAV백업·sameROM경로·다른basename불변 감사. 이번후속은 신규번역0/ROM변경없음; 위742도구pin은 이전빌드시점, 신규observer는별도hash.
이구조는한글다중바이트 중간절단위험이있다. field ABI/한글편집·모든재표시/한글영구저장/기존save호환은미완료다. 미번역제목6368E8:33의mono native소비자를확인했고 아직원문유지한다.
기록 `analysis/INPUT_CONFIRMATION_HANDOFF.md`, 화면 `analysis/input_confirmation_v1/confirmation_pages.png`, 현행catalog `analysis/full_scope_input_confirmation_v1_r3/`.
미선택일본어27,500/기타1,859/errors0. 전체미번역/이미지·한글입력·상점·인간검토·배포검증 미완료.
needs_review; NON-DISTRIBUTION; release_eligible=false.

## 이전 검증 제품: 거츠맨 희망 물건 질문 (2026-10-09)

개발ROM `poc/output/exe45_ko_development_gutsman_wishlist_v1_r2.gba`, SHA256 `cb0cc5dca0831bdd10adfed3eb4ed940b51f98d2c358fb13a87e56e6ab6a2c7e`.
667044:31:0..2 칩/희망 물건 질문3literal 추가, 누적2,545 /60선택·672원본유지archive.
이 archive의 고정literal153 전체선택을원본집합과검증했다. dynamic입력값/일본어키보드/모든정상분기까지완료했다는뜻은아니다.
신규3페이지는격리read-alias renderer진단이며fontCPU/OBJVRAM/픽셀·nickname·지움/keyWait·input-init바이트보존 PASS,화면직접확인.
원본/ledger·독립4빌드동일·기존150unit/96scripts/59payload·폰트/이미지/keyitem39보존, 정상29/키보드·PET/소개/넘버맨/플러그아웃·native save/coldcontinue대표회귀 PASS.
115fixture/736AST·736Python buildpin drift=[]/745전체도구pin, CPU624합성계약 PASS.
정상29의일본어「あ」입력→決定 focus→확인창→Yes→반응93을추가관찰했다. RAM020010A6..AC 변화는record후보이며writer/ABI/저장증거는아직없다.
새미번역확인창6368E8:10:0..2 및해당record writer/저장·정상재표시가다음작업이다.
기록 `analysis/GUTSMAN_WISHLIST_HANDOFF.md`, 감사 `analysis/gutsman_wishlist_v1/final_identity.json`, 화면 `wishlist_pages.png`, 입력관찰 `native_input_observation.json`.
현행catalog `analysis/full_scope_gutsman_wishlist_v1_r2/`: 미선택일본어27,503/기타1,859/errors0.
전체미번역·이미지·한글입력/편집/확정/모든재표시/영구저장/기존save호환·상점·인간검토는미완료. needs_review; NON-DISTRIBUTION; release_eligible=false.

## 이전 검증 제품: 거츠맨 저장 답변 재질문 고정 문구 (2026-10-09)

개발ROM `poc/output/exe45_ko_development_gutsman_answers_v1_r2.gba`, SHA256 `2635bfc8d3636e420ce27a5bb44c80a8fa02931e3264ae864a903d00a6c7894f`.
667044:40..63 형제·친구·취미·TV·희망 물건 재질문/선택/없음 응답40literal 추가, 누적2,542 /60선택·672원본유지archive.
고정40/24페이지 격리 renderer/분기진단으로fontCPU/OBJVRAM/픽셀·native nickname·선택행/커서·지움 PASS, 화면직접확인.
8개native No와41의B→응답42 PASS. prefix는printStringBuffer전, 모든진단은input-init전에멈췄다.
실제 저장 답변 버퍼나 정상 재질문 선택/한글입력·저장 증거가 아니다. native buffers/controls와 prior110 정확히 보존했다.
정상29/일본어키보드·PET/소개/넘버맨/플러그아웃 대표회귀·새native save/coldcontinue PASS.
원본보존·독립4빌드 동일ROM·기존59payload/73scripts/110units·폰트/이미지/keyitem39 보존 감사 PASS.
110fixture/732AST·732 Python buildpins drift=[] /741전체도구pin, CPU624 합성 계약 PASS.
기록 `analysis/GUTSMAN_ANSWERS_HANDOFF.md`, 감사 `analysis/gutsman_answers_v1/final_identity.json`, 화면 `answer_pages.png`.
현행catalog `analysis/full_scope_gutsman_answers_v1_r2/`: 미선택일본어27,506/기타1,859/errors0.
다음은script31의3문구 및 실제입력 writer/확정/저장/정상재표시 연결이다. 전체미번역·이미지/한글입력·영구저장/기존save호환/상점/인간검토 미완료.
needs_review; NON-DISTRIBUTION; release_eligible=false.

## 이전 검증 제품: 거츠맨 가족 질문·선택지 (2026-10-09)

개발ROM `poc/output/exe45_ko_development_gutsman_family_v1_r2.gba`, SHA256 `c2cec16370b4ca5fa3b83eb1dab2f66d739145813b5d80be618c56c4790aa45a`.
형·오빠/남동생/누나·언니/여동생 유무·있어/없어·이름 질문·없음 응답29literal 추가, 누적2,502선택literal /60선택·672원본유지archive.
기존81문구/89profile scripts와 다른59archive payload·폰트/advance·키아이템39·이미지 보존 감사 PASS.
신규29문구는 정상29의 table read를 한 번 alias한 격리 표시/분기진단으로 확인했다. 정상 sibling 질문 선택이나 가족 이름 저장 증거가 아니다.
fontCPU→OBJVRAM→픽셀·native nickname·choice 간격/커서·지움 PASS, 가족25페이지와플러그아웃6화면 직접 확인.
네 Yes/No와script1 B를 실행했으며 BSeparate=false의 B는 실제로 없음 응답2로 이동했다. 초기 B→continue 가정을 기각하고 checked 입력 설명을 정정했다.
정상 기존29의3문구/일본어키보드 전환·새native저장/cold이어하기·PET/소개/넘버맨/플러그아웃 대표회귀 PASS.
일본어키보드 crop는 입력 없는 다음 hold에서 전체29,344pixels 동일, 픽셀 제외 없음. 한글 입력 검증이 아니다.
최초_v1/재현과 checked입력_r2/재현 전체ROM bytes 동일. 실행 증거는 동일ROM bytes에 한해 명시적으로 이관했다.
CPU624조건·관련103fixture/728AST/737tools drift=[] PASS. 기록 `analysis/GUTSMAN_FAMILY_HANDOFF.md`, 감사 `analysis/gutsman_family_v1/final_identity.json`.
현행catalog `analysis/full_scope_gutsman_family_v1_r2/`: 미선택일본어27,546/기타1,859/errors0. 다음은40..63의저장답변 재표시다.
전체미번역·한글입력/영구저장/기존save호환·상점02031000·인간검토는 미완료. needs_review; NON-DISTRIBUTION; release_eligible=false.

## 이전 검증 제품: 거츠맨 친구·취향 질문 미번역 (2026-10-09)

개발ROM `poc/output/exe45_ko_development_gutsman_questions_v1.gba`, SHA256 `52bee4df4ceda2147c48ac1e4b0a414c29e63f3088ed0fe73b66f3b5acedd9e7`.
친구·음식·취미·장래희망·좋아하는 사람·존경/꺼리는 사람·TV 질문과 반응41literal 추가, 누적2,473선택literal /60선택·672원본유지archive.
기존 프로필40문구와87script, 나머지59archive payload·폰트/advance·키아이템39·이미지 보존 감사 PASS.
신규41문구/39페이지는 격리 read-alias renderer 진단이며 정상 질문 선택/입력/진행 증거가 아니다.
fontCPU→OBJVRAM→화면픽셀·native nickname 첫째/둘째행·페이지 지움·순서·마지막 keyWait PASS, 합성 화면 직접 확인.
기존 질문29의3문구 정상 회귀와 일본어 입력화면 전환, 새native저장/cold이어하기·PET/소개/넘버맨/플러그아웃 대표 회귀 PASS.
독립 재현 동일해시, CPU624조건·관련98fixture·725AST·734도구identity drift=[] PASS. 원본 ROM 불변.
기록 `analysis/GUTSMAN_QUESTIONS_HANDOFF.md`, 검증 `analysis/gutsman_questions_v1/final_identity.json`, 화면 같은 폴더`question_pages.png`.
catalog732 미선택일본어27,575/기타1,859/errors0. 다음은667044:1..8 가족 질문/선택 경로다.
전체미번역·한글입력/영구저장/기존save호환·상점02031000·인간검토는 미완료. needs_review; NON-DISTRIBUTION; release_eligible=false.

## 이전 검증 제품: 거츠맨 프로필 질문·반응 미번역 (2026-10-09)

개발ROM `poc/output/exe45_ko_development_gutsman_profile_v1.gba`, SHA256 `256e901d04386db75b8e770c049483db21bac022c1b0ba32cd76b2d91ad22470`.
과목·유치원·학교·회사 질문과 답변 반응40literal 추가, 누적2,432선택literal / 60선택·672원본유지archive.
원본부터 독립 두번빌드 동일해시. 기존59archive payload·폰트/advance·키아이템39·이미지 보존 감사는`final_identity.json`이 소유한다.
자체 native 새 저장/cold 이어하기→거츠맨→인터넷/귀환→어려운 과목 질문29의3문구 정상 실행.
나머지37문구는 격리 read-alias 표시 진단으로 정상 나이/응답 조건 실행과 구분했다.
40문구 fontCPU/OBJVRAM/화면픽셀/닉네임/지움 PASS, 합성화면 직접 확인.
원래 일본어 입력 화면으로 전환됨을 keyWait/flags/waitHold 및29,344pixel 동일 비교로 확인했다. 한글 입력/저장 검증은 아니다.
거츠맨 PET8scene/22문구·소개2·넘버맨3·플러그아웃 No/B/좌우/Yes/귀환 대표 회귀, CPU624조건·관련29fixture PASS.
기록 `analysis/GUTSMAN_PROFILE_HANDOFF.md`, 검증 `analysis/gutsman_profile_v1/`.
catalog732 미선택일본어27,616/기타1,859/errors0. 전체미번역·한글입력/영구저장/기존save호환·상점02031000·인간검토는 미완료.
needs_review; NON-DISTRIBUTION; release_eligible=false.

## 이전 검증 제품: 거츠맨 플러그아웃 미번역 (2026-10-09)

개발ROM `poc/output/exe45_ko_development_gutsman_plugout_v1.gba`, SHA256 `b69f585644084b5cfb090e4fafc7b0f3b41ea04315b204d1da4bd08600f67df1`.
질문/예/아니요/귀환응답4literal 추가, 누적2,392선택literal. 원본·기존롤4문구·기존58archive payload·키아이템39문구·이미지 보존.
원본부터 두번빌드해 동일해시; 새ROM의 자체저장/체크포인트없는cold이어하기→정상거츠맨선택/인터넷/R플러그아웃을 실행했다.
defaultNo/No확정/B취소/재진입/좌우전환/Yes응답/거츠맨귀환 및 nickname/fontCPU/OBJVRAM/화면픽셀·텍스트지움 PASS. 합성화면직접확인.
새주소의키아이템CPU624조건·합성fixture4+기존20tests·쓰기ledger/재현/724도구identity 감사 PASS.
기록 `analysis/GUTSMAN_PLUGOUT_HANDOFF.md`, 증거 `analysis/gutsman_plugout_v1/`.
catalog732 미선택일본어27,656/기타1,859/errors0. 상점02031000 경로/다른미번역/한글입력·영구reload·기존save호환·인간검토는 계속미완료. NON-DISTRIBUTION; release_eligible=false.

## 이전 검증 제품: 키 아이템 전체39문구 ROM 통합 (2026-10-09)

개발ROM `poc/output/exe45_ko_development_keyitem_full_rom_v1.gba`, SHA256 `4f780b9c7df2e2133e308cdd59821dbcd840936deff17ec168426df61d5fc133`.
기존초안의미반영38literal 추가, 누적2,388선택literal/59기존선택archive·673원본유지archive. 기존빈안내1개중복계산없음.
primary immutable-source builder가2,477byte raw-ROM clone/guarded reader를통합. 기존압축/RAM1,273byte와payload/이미지/‘통신’·원본ROM보존.
최종ROM CPU624조건·관련20fixturetests PASS. 자체새저장/cold이어하기/PET8scene/거츠맨소개·넘버맨귀환 및정상빈안내의CPU/font/VRAM/pixels·hold/B/재진입 PASS.
39문구와5개수량형0/255를게임renderer로진단실행/픽셀검증·합성화면직접확인. 이는guarded read alias 진단이며 정상아이템획득·두번째02031000실제경로의증거는아니다.
소지품통계4제목/숫자영역대표회귀 PASS. 기록 `analysis/KEYITEM_FULL_ROM_HANDOFF.md`, 증거 `analysis/keyitem_full_rom_v1/`; 최종재현/도구감사는해당폴더`final_identity.json`.
catalog732 미선택일본어27,660/기타1,859/errors0. 전체미번역/한글입력·영구reload·기존save호환/인간검토미완료. NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 조사: 키 아이템 전체 번역의 ROM 직접 조회 (2026-10-09)

2,477byte 초안을 RAM 증설 없이 조회하는 guarded selector CPU 실험624조건 및 합성fixture6tests PASS.
변경하지 않은 최신ROM 정상 소지품 진입/대기/B/재진입에서 실제 호출·헤더·1,273byte RAM payload 일치를 확인했다.
원본 수량 handler의 unsigned byte 0..255와 초안 수량행 정적 최대78/146/158/170/78px 확인.
**제품 builder 미통합, 새 ROM/추가 반영0개.** 다른02031000 정상 소비 경로·새 selector GBA 실행·동적 배치는 아직 미검증이다.
기록 `analysis/KEYITEM_ROM_SELECTOR_HANDOFF.md`, CPU `analysis/keyitem_rom_selector_probe_v1_r2/`, 정상 경로/수량 `analysis/keyitem_selector_readiness_v1/`.
최신 플레이용 개발ROM과누적2,350선택literal은 아래 제품과동일하다. 전체 번역 완료가 아니다.

## 이전 검증 제품: 소지품 통계 제목 (2026-10-09)

ROM `poc/output/exe45_ko_development_possessions_statistics_v1.gba`, SHA256 `f932c28e3de1459424eee2407be1a75b5bcb3c4ca2f33fe202c7a2a1f8b1c556`.
`컵 / 크레딧 / 버그 조각 / 대전 전적` 네 제목(6368E8:80:0 literal1개)을 추가해 누적2,350선택literal/59선택·673원본유지archive.
부모12문구/기존58archive·이미지·‘통신’과 원본 ROM 보존. 4×16칸/4096byte stage·숫자/Z 영역 불변.
정상 진입/B복귀 각각40visible cells·5120픽셀, 빈 아이템 LZ/RAM/lookup/font/화면·대기/재진입 PASS.
새 저장/cold 이어하기·거츠맨PET/인사·넘버맨귀환과 달력 등록/확인/삭제/1회만 대표 회귀 PASS. 합성 화면 직접 확인.
관련41tests/695AST PASS, main/repro/current_repro/current_repro_r2 동일SHA·최종tools drift=[]·쓰기/입력/원본 감사 PASS.
초기 원본0x40을 count prefix로 본 기록은 カ 코드로 정정. 정책 metadata만 수정했고 ROM 바이트는 동일하며 최초 manifest도 보존했다.
기록 `analysis/POSSESSIONS_STATISTICS_ROM_HANDOFF.md`, 증거·재현 `analysis/possessions_statistics_v1/`.
catalog732: 미선택일본어27,698/기타1,859/errors0. 키 아이템 초안38개 미반영 및 한글입력/모든재표시/영구reload/기존save호환 등 전체요청 미완료. NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 빈 키 아이템 안내 (2026-10-09)

ROM `poc/output/exe45_ko_development_keyitem_empty_v1.gba`, SHA256 `ab7182e1921f12c58031d2cfce2457587b09d657527c8476e8a9a3388c12f6b6`.
`키 아이템이 / 1개도 없다・・・` 추가, 누적2,349선택literal/59선택·673원본유지archive.
완전히 동일한 원본 설명10/11의 저장만 공유해 해제 크기1,273바이트(원본1,291 이내)를 유지한다. 문구 축약·RAM 증설·새 코드 후킹 없음.
새 ROM 정상 cold/저장·이어하기/PET 회귀와빈 안내의네이티브LZ→RAM→lookup→CPU/font→VRAM/pixels, 대기/B복귀/재진입 PASS.
진입/재진입 각각15글리프·2,016픽셀 확인, 합성화면 직접 검토. main/repro 동일SHA.
달력 날짜/종류/확인/삭제 및 동적1회만 대표 회귀 PASS. 최종current_repro_r2도동일SHA/689tools drift=[]/원본·헤더·계획쓰기·입력 해시 감사 PASS.
기존58archive payload/이미지/‘통신’ 보존. 키 아이템 전체39개 초안 중 나머지38개는 ROM 미반영.
다른02031000 소비자는 원본 해제 범위 이내 정적 검증이며 정상 화면 검증은 미실시.
기록 `analysis/KEYITEM_EMPTY_ROM_HANDOFF.md`, 증거/재현 `analysis/keyitem_empty_v1/`.
catalog732: 미선택일본어27,699/기타1,859/errors0. 전체요청 및 한글입력/모든재표시/영구reload/기존save호환 미완료. NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 소지품 안내 (2026-10-09)

ROM `poc/output/exe45_ko_development_gutsman_calendar_inventory_v1.gba`, SHA256 `2adcc7111363c377628071f9b3ac313ead4615c157a7478f842c316a410a80d1`.
소지품 안내3문구 추가, 누적2,348선택literal/58선택·674원본유지archive. 이전반복주기/57archive·이미지·‘통신’을보존했다.
닉네임앞뒤source-pinned template44px와원문제어코드·선택·공백범위·226미선택span 검증,관련67tests/679AST PASS.
자체정상cold/저장·이어하기/PET 회귀와소지품3문구/native닉네임/one-option/A/B/재진입 CPU/font/VRAM/pixels PASS,4장화면직접확인.
달력등록/확인/삭제 및동적1회만 대표회귀 PASS. 이전전체관리/알림/다섯빈도runtime가자동이전된것은아니다.
기록 `analysis/GUTSMAN_CALENDAR_INVENTORY_ROM_HANDOFF.md`, 화면 `analysis/gutsman_calendar_inventory_v1/inventory.png`, 재현/최종감사같은폴더.
main/repro/current_repro_r3 동일SHA·679tools drift=[]·원본불변 PASS.
catalog732: 미선택일본어27,700/기타1,859/errors0, 전체ROM 완전성분모 아님. 소지품통계제목과공용빈key-item 메시지는여전히미번역.
전체미번역번역요청미완료. NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 동적 반복 주기 이름 (2026-10-08)

ROM `poc/output/exe45_ko_development_calendar_frequency_names_v1.gba`, SHA256 `9a635be2e6f26ff835bdafd742a2042143183c337e04dc1d5d77884a18bae06b`.
일반 대사에 삽입되는 `1회만/매일/매주/매월/매년` 5문구 추가, 누적2,345선택literal/58선택·674원본유지archive.
기존 빈도선택 이미지와 별도consumer이며 이전생일/개교기념일·이미지·‘통신’을 유지했다.6368E8의243미선택span·source/제어코드/32bytecapacity PASS, 관련63tests/675AST PASS.
자체정상runtime chain 및신규5개의lookup→E5stage→native32bytecopy→RAM→CPU/font/VRAM/pixels PASS,5장합성화면직접확인. 기존저장/이어하기·PET/칩·격리알림renderer·달력관리/일정삭제회귀 PASS. main/repro/current_repro_r2 동일SHA/675tools drift=[]/원본불변 PASS. 결과/한계 `analysis/CALENDAR_FREQUENCY_NAMES_ROM_HANDOFF.md`, 화면 `analysis/calendar_frequency_names_v1/frequency_names.png`. 전체번역완료는아니다.
catalog732: 미선택일본어27,703/기타1,859/errors0, 전체ROM 완전성분모 아님. NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 일정 중복·삭제 (2026-10-08)

ROM: `poc/output/exe45_ko_development_gutsman_calendar_schedule_delete_v1.gba`.
SHA256 `844e04d52c314de6cbdc58556ee18b22927c587992df12a6aa941da6abd80dcb`.
일정중복경고25와삭제확인50/51의9문구추가, 누적2,340선택literal/58선택·674원본유지archive. 부모45문구/기존57archive·이미지·‘통신’ 유지. 정적54문구폰트/제어코드/폭(최대144px)·227미선택span 검사,62tests/670AST+registry PASS. main/repro/current_repro_r1 동일 SHA 및670tools drift=[]/원본불변 PASS.
새ROM에서정상저장·이어하기/PET/칩/격리알림·기존달력/기념일삭제 회귀 PASS. 정상일정등록→목록→script50삭제확인4문구/동적식사name CPU/font/VRAM/pixels·직접화면확인 PASS. No/B는32byte식사record유지, Yes는전부0삭제 PASS. 나머지신규5문구는static-only. 첫페이지반복주기1回のみ는별도미번역으로확인/후속5초안은미반영. 기록 `analysis/GUTSMAN_CALENDAR_SCHEDULE_DELETE_ROM_HANDOFF.md`; 화면 `analysis/gutsman_calendar_schedule_delete_v1/schedule_delete.png`; 재현·감사같은폴더.
catalog732집계: 미선택일본어포함27,708/기타1,859/parse errors0. 전체ROM완전성분모아님. 소지품10의3초안은ROM미반영. 휴일·날짜/요일이미지·임의한글이름·영구native reload/기존save호환·실제RTC·전체이미지/inline/fixed·인간검토미완료. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 달력 관리 (2026-10-08)

ROM: `poc/output/exe45_ko_development_gutsman_calendar_management_v1.gba`.
SHA256 `d6aac577eedccd8b07c69576ebd33c20fdd02a1b7eb23c55142d52580dd946b9`.
오류·삭제메뉴·덮어쓰기·장소질문·PET도움말 및 기념일 삭제확인23문구 추가, 누적2,331선택literal/58선택·674원본유지archive. 부모22문구/기존57archive·이미지·‘통신’ 유지. 정적 폰트/폭/제어코드/230미선택span 검사와59tests/666AST+registry PASS. main/repro/최종current_repro_r2 동일 SHA 및 tools drift=[]/원본불변 검사 PASS.
정상 저장·cold이어하기/거츠맨인사/PET/칩/격리알림renderer·기존달력 회귀 PASS. 새 삭제메뉴5/확인52/등록슬롯질문32의8문구 CPU/font/VRAM/pixels·직접화면확인 PASS. No/B는32byte생일record불변, Yes는전부0삭제 PASS. 나머지15문구는 static-only. 첫cursor index가정실패를보존하고native index1/두좌표로검사모델수정; ROM변경없음, 수정후최종tools재감사PASS. 기록 `analysis/GUTSMAN_CALENDAR_MANAGEMENT_ROM_HANDOFF.md`; 화면 `analysis/gutsman_calendar_management_v1/calendar_management.png`; 재현·감사 같은폴더.
catalog732집계: 미선택일본어포함27,717/기타1,859/parse errors0, 전체ROM완전성분모아님. 휴일·날짜/요일이미지·임의한글이름·영구native reload/기존save호환·실제RTC·전체이미지/inline/fixed·인간검토 미해결. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 달력 조회·복귀 메뉴 (2026-10-08)

ROM: `poc/output/exe45_ko_development_gutsman_calendar_navigation_v1.gba`.
SHA256 `2f68c4df93067b78957b69c20f20fb55dd2569eeb32e616de094a648b0b02d59`.
조회날짜 질문6과 기념일 취소 후 등록메뉴7의4문구를 추가해 누적2,308선택literal/58선택·674원본유지archive. 직전판 대비665698 scripts6/7만 변경, 부모18문구/기존57archive payload 및 기존이미지·‘통신’ 유지.
정상 자기ROM에서 신규4문구 CPU/font/VRAM/화면pixels, default기념일→일정cursor, 두선택확정과 B복귀/32byte레코드불변 PASS. focus-only 구간은 문자를 재그리지 않는 native 동작임을 확인하여 parent공급→child VRAM/화면잔존·커서로 검사했다; 초기실패기록 보존. 기존기념일확인33 및 생일/개교기념일의고정폭표시·같은세션재조회, 넘버맨저장/cold이어하기·귀환/거츠맨인사/PET/알림renderer·칩/합성CPU64vectors 회귀 PASS. 알림renderer는실제RTC발생증거가아니다.
관련54tests/661Python AST+registry PASS. 재현명령·해시·최종tools감사 `analysis/gutsman_calendar_navigation_v1/`; 전체기록 `analysis/GUTSMAN_CALENDAR_NAVIGATION_ROM_HANDOFF.md`, 화면 `analysis/gutsman_calendar_navigation_v1/calendar_navigation.png`.
catalog732집계: 미선택일본어포함27,740/기타검토1,859/parse errors0, 전체ROM완전성분모아님. 후속오류·삭제·덮어쓰기·안내19초안은source/newline·74한글glyph/ROMfont·최대116px 사전검사만통과했으며 **ROM미반영/누적수미포함**.
휴일正月·날짜/요일이미지·전체이미지/inline/fixed population, 한글이름입력/모든재표시/영구native재로드/기존save호환, RTC/C40producer, 기존시각차이·인간검토 미해결. 전체요청완료아님. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 기념일 확인·기본 이름 (2026-10-08)

ROM: `poc/output/exe45_ko_development_gutsman_calendar_anniversary_confirmation_v1.gba`.
SHA256 `23fa4ce6d4e5c51c1bb45a5b64e72b5e6652c8b4a1aace9c764d5a475ee12088`.
기념일 확인창 ‘이렇게 하면 되거스?’/‘예’/‘아니오’와 기본 이름 ‘생일’/‘개교기념일’ 5개를 추가했다. 직전 중단 작업의 등록 날짜·종류4개 및 기념일 질문·세 항목2개도 누적 반영되어 있다. 누적2,304선택literal/58선택·674원본유지archive.
기념일판 대비 변경 script는665698:33 및6368E8:74/75뿐이다. 확인창의CPU/font/OBJ VRAM/픽셀·선택 커서, 두 기본 이름의9/21byte 원문복사·10cell 표시/clearing, Yes/No/B,32byte등록레코드, 같은세션BG2목록 재조회까지 검사PASS 및 직접화면확인. No/B는31복귀·레코드불변, Yes는0복귀·예상header/한글/E5/zero-tail commit. 목록12/15cell 전송과10visible cell 픽셀/타일맵도PASS; 다음행1024byte 간격에서각각256/64byte 여유.
넘버맨 새저장/cold이어하기·귀환, 거츠맨 인사/PET/알림/칩/일정 누적회귀PASS. 관련46거츠맨+2신규+3chip-name tests 및657Python AST PASS. 최종 해시 감사는 `analysis/gutsman_calendar_anniversary_confirmation_v1/final_identity_audit.json` 참조.
최신inventory `analysis/full_scope_gutsman_calendar_anniversary_confirmation_v1/`: 미선택일본어포함27,744/기타1,859/parse errors0. 이것은732archive catalog 집계이며 전체ROM 완전성 분모가 아니다. 원본 ROM과 기존 그래픽·‘통신’ 수정은 유지했다.
기록 `analysis/GUTSMAN_CALENDAR_ANNIVERSARY_CONFIRMATION_ROM_HANDOFF.md`; 확인·분기 화면 `analysis/gutsman_calendar_anniversary_confirmation_v1/anniversary_confirmation.png`, 재조회 `anniversary_queries.png`. 재현 명령은 같은 폴더의 `rebuild.ps1`과 `build_recipe.json`에 저장했다.
기념일 취소 후script7, 조회질문6, 목록의正月(6368E8:130:0), 날짜/요일 이미지 등은 여전히미번역이다. 임의한글이름 편집→모든재표시→영구save/reload→기존save호환·실제RTC알림·전체이미지/inline/fixed population·기존시각차이도미해결. 전체요청완료아님. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 일정 확인·달력 홈 (2026-10-07)

ROM: `poc/output/exe45_ko_development_gutsman_calendar_home_v1.gba`.
SHA256 `dba4a8792f15225df552dcd61b9a7fddcb8d1e5c800aae818b93e08390d4dd9a`.
확인창 ‘이렇게 하면 되거스?’/‘예’/‘아니오’ 3문구와 확정 직후 동적 달력 홈 ‘오늘은 [월]월 [일]일이거스 / 뭘 할 거스?’ 3문구를 추가했다. 누적2,293선택literal/58선택·674원본유지archive. 직전 확인판 대비665698 script0만 변경, 그 이전 내용판 대비script24만 변경했다.
자기 정상경로에서 질문20~23, 확인24, 예/아니오 focus, No확정, B취소, Yes확정, 동적1월1일 홈0을 검증했다. No/B는일정레코드불변·script22복귀, Yes는예상32byte식사레코드commit·script0복귀 PASS. CPU/font/OBJ VRAM/화면픽셀·선택커서·잔상·동적buffer·초상/경계 보존과 직접화면확인 PASS.
기존 넘버맨 새저장/cold이어하기·귀환, 거츠맨 인사/PET/알림/칩13 및 질문4화면 누적회귀 PASS. 42거츠맨tests+3chip-name tests/644AST PASS. main/repro/current_repro_r1 세빌드동일SHA, tools drift=[]/원본보존.
최신inventory `analysis/full_scope_gutsman_calendar_home_v1/`: 미선택일본어포함27,755/기타1,859/parse errors0. 다른날짜·내용/상대이름입력·충돌/삭제·영구저장/재로드·기존save호환·실제RTC알림과전체이미지는미검증이며전체완료가아니다.
기록 `analysis/GUTSMAN_CALENDAR_HOME_ROM_HANDOFF.md`; 화면 `analysis/gutsman_calendar_home_v1/calendar_home.png`, 선택분기 `analysis/gutsman_calendar_home_v1/confirmation_choices.png`.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 일정 내용·약속 상대 (2026-10-07)

ROM: `poc/output/exe45_ko_development_gutsman_calendar_content_v1.gba`.
SHA256 `e8ab0e4a8381d904d92e155a6852369c70532449f6fd74386831607fd4f0e4d7`.
‘어떤 내용이거스?’, ‘누구와 약속이거스?’ 신규2문구 반영, 누적2,287선택literal/58선택·674원본유지archive. 자기 정상일정경로20/21/22/23 네질문의CPU/font/OBJ VRAM/화면·clearing·폭135/91/103/115px 검사PASS, 직접화면확인. 친구focus만으로23이아니며A확정후상대질문23이라는잘못된초기예상을정정했다.
거츠맨초상/경계는RGB0오차의기존native animation phase와비교. 초기TV모서리1pixel차이는transition-scope 미해결, 추가90frame대기후안정TV화면은PASS. 초기실패증거삭제·검사허용오차완화없음. 기존57archive/같은archive다른253span/선택자산·그래픽15라벨5블록/‘통신’bytes유지.
자체새저장/cold이어하기·넘버맨귀환3/거츠맨인사2/PET8장면·No/B취소/알림6페이지·식사닉네임2샘플·칩13/합성64vectors 회귀PASS. 관련41tests/636AST/main-repro-final current_repro_r3동일/tools drift=[]/원본보존. 새Roll화면은미실행/합성guard만.
확인24/예/아니오 다음3초안과정상원문확인화면도준비했으나 **현재ROM 미반영**. 선택지/확정·취소·등록검사후반영할계획이며현재count에미포함. 남은입력67literal/알림15literal·미선택일본어포함27,761/기타1,859/전체이미지·이름영구저장/기존save호환 등미완료.
기록 `analysis/GUTSMAN_CALENDAR_CONTENT_ROM_HANDOFF.md`; 검사·화면 `analysis/gutsman_calendar_content_v1/`.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 일정 입력 질문 (2026-10-07)

ROM: `poc/output/exe45_ko_development_gutsman_calendar_prompts_v1.gba`.
SHA256 `68a8d4d0c13d39cc6e80c0bbd3e367d6469062e042363dad2b59461573a56cee`.
‘몇 시부터 시작하거스?’, ‘어떤 종류거스?’ 2문구 추가. 누적2,285선택 literal/58선택·674원본 유지 archive. 정상 일정 입력의 두 화면에서 CPU/font/OBJ VRAM/화면·135px/91px·clearing·거츠맨초상/경계 유지 PASS,직접시각확인 완료. 최초6번째화면도종류질문으로기대한검사는실패로보존;실제로다음내용입력22이며정확한5번째21로정정,ROM/검사허용범위 변경없음.
기존57archive/선택자산/그래픽15라벨5블록·‘통신’bytes유지. 정상넘버맨새저장/cold이어하기·거츠맨인사/PET8장면/알림6페이지·식사닉네임결합·Guts칩13 회귀 PASS. 롤 새화면은미실행/합성64vectors 검사만. 관련39tests/632AST PASS; main/repro/final current_repro_r2 동일/tools drift=[]/원본 보존.
이전식사ROM을유지한정상식사등록→committed record→같은세션조회도추가검증 PASS: ‘식사’가02010C40에서표시됨. 이전alarm alias의반복32byte02010AC0와같은consumer상태로취급하지않음. C40 producer/실제 reminder초기화·TV/약속이름/RTC 알림은미해결.
미선택일본어포함27,763/기타1,859;입력69literal/알림15literal·전체이미지/inline/fixed·한글이름 영구저장/기존save호환 등 남음. 전체완료 아님.
기록 `analysis/GUTSMAN_CALENDAR_PROMPTS_ROM_HANDOFF.md`; 검사·화면 `analysis/gutsman_calendar_prompts_v1/`.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 식사 알림 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_alarm_meal_v1.gba`.
SHA256 `d55433eb563313f4e2fe80ade4ba452ebd9f97345c27f997488f929ee6ccac25`.
식사 알림 ‘밥 먹을 시간이거스!’ 1문구 추가, 누적2,283선택 literal/57선택·675원본 유지 archive. native 닉네임44px/쉼표 포함55px·본문123px의 두 진단 화면: parser RAM/E5·CPU/font/OBJ VRAM/화면·clearing·화살표/경계 검사 및 직접시각확인 PASS. 실제시간 알림 발생 검증은 아님.
기존알림5페이지/거츠맨칩 이름·대사/넘버맨새저장·cold이어하기/거츠맨인사·PET8장면 회귀 PASS. 기존56archive/알림다른27scripts/기존5문구·그래픽15라벨5블록 불변, ‘통신’ 유지. 관련39tests/합성selector64vectors/627Python AST PASS; main/repro/final current_repro 동일/tools drift=[]/원본 보존.
TV 이벤트 이름은 이전ROM의 진단 경로에서 반복32bytes/352px를 관측해 정상샘플로 채택하지 않았다. 정상등록→reminder 초기화 경로 확인 전 이벤트이름 첫페이지 번역은 보류. 미선택 일본어포함27,765/기타1,859; 알림15literal·전체이미지/inline/fixed·한글이름 영구저장/기존save호환 등 남음. 전체완료 아님.
기록 `analysis/GUTSMAN_ALARM_MEAL_ROM_HANDOFF.md`; 검사·화면 `analysis/gutsman_alarm_meal_v1/`.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 일정 알림 후속 페이지 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_alarm_followup_v1.gba`.
SHA256 `510b75b9c9931af339f7df2b8c5b55789667badf392ebece5f5ca998cd8d5dc3`.
TV/약속 알림의두번째페이지2문구를 추가했다. 누적2,282선택 literal/57선택·675원본 유지 archive. 이벤트이름첫페이지/별도얼굴창 등16literal은 이번범위에서 원문보존.
신규2+기존학원/추가알림3=진단5페이지의CPU/font/OBJ VRAM/화면·clearing·줄배치·페이지순서·화살표/경계 검사와직접화면확인 PASS. 진단은 실제등록시간알림·반복·이벤트도달성 검증이아니며진단state는정상chain재사용금지.
주소이동 후 거츠맨 ‘빅해머1’의실제ABI/128copy/RAM/화면 회귀 PASS;롤은새ROM에서합성guard검사만실행. 정상넘버맨새저장/cold이어하기·거츠맨인사/PET8장면22literal/29focus·No·B취소 PASS. 기존56archive/알림다른26scripts/기존3문구·그래픽15라벨5블록 실제bytes 불변, ‘통신’ 유지.
관련37tests/합성selector64vectors PASS. main/repro/final current_repro 동일/622Python tools drift=[]/원본 보존. 기록 `analysis/GUTSMAN_ALARM_FOLLOWUP_ROM_HANDOFF.md`;화면·검사 `analysis/gutsman_alarm_followup_v1/`.
미선택일본어포함27,766/기타1,859. 전체이미지/inline/fixed·한글이름committed record/모든재표시/영구재로드/기존save호환·prior wait-arrow53pixel 차이 등 남음. 전체요청완료아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 칩 탐색 대사·이름 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_chipquest_v1.gba`.
SHA256 `bc3b668de37dbbe73eecec00c0d04315b4e14adce7c16fdadd0039e42103283a`.
신규2literal과 기존 칩 이름 ‘빅해머1’을 반영했다. 누적2,280선택 literal/57선택·675원본 유지 archive; 거츠맨 R66A844의33/33literal 초안 선택, 전체게임 완료 아님.
거츠맨/롤 각2완성 진단 화면의 실제 ABI·native128copy/RAM·font/OBJ VRAM/화면·폭·clearing·화살표/경계·종료 PASS. 각각 자기 초상/대사pool 유지; 다른 stream/context/name은 원본 fallback. 진단은 실제 칩 퀘스트 진행/획득 증거가 아니며 진단state는 정상chain 재사용 금지.
정상 거츠맨 R10/PET복귀, 자체 넘버맨 freshFF저장/cold이어하기·거츠맨인사/PET8장면22literal·29focus/No/B취소 회귀 PASS. 기존56archive와66A844의다른254scripts·31문구·그래픽15라벨5블록 실제bytes 불변, ‘통신’ 유지.
관련35tests/합성CPU64vectors PASS. main/repro/final current_repro_r3 동일SHA,617Python tools drift=[]/원본 보존. 기록 `analysis/GUTSMAN_CHIPQUEST_ROM_HANDOFF.md`; 화면·검사 `analysis/gutsman_chipquest_v1/`.
미선택 일본어 포함27,768/기타1,859개. 일정 알림18literal·전체이미지/inline/fixed·한글이름 committed record/모든재표시/영구재로드/기존save호환·prior wait-arrow53pixel 차이 등 남음.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 R 대화 부분 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_pet_talk_v1.gba`.
SHA256 `75c2355fd206156a4a5cde9dcae54a288b6e85fe71183195fccfadf841b8e309`.
신규31번역 literal(인터넷/라이선스/사건/키/대회/메일), 누적2,278선택 literal/57선택·675원본 유지 archive.
169tests/source·control·숫자·nickname suffix·glyph·geometry·roundtrip PASS. 최대125px≤PET132px. main/repro/final current_repro_r2 동일,611Python tools AST PASS/drift=[]/원본 보존.
실제 거츠맨 R script0→10의 정상1페이지24glyph/화면·clearing·native arrow분리·border·A입력후PET복귀4 PASS. 처음31분기로 예상한 검사는 FAIL로 보존 후 실제10분기로 바로잡았고 ROM/flag/save는 변경하지 않았다.
대표11/12/17/25/27/33/34/31 격리 renderer13페이지 strict CPU/font/OBJ VRAM/화면·clearing·page순서 PASS. 원본 닉네임「ああさま」44px와 본문을 합친12/31 두샘플 포함. 실제 flag/아이템/라이선스/사건/대회/요일 선택이나 한글 이름 persistence 검증은 아님. 다른17선택literal static-only. 진단 alias는ROM에 없고 진단state는 정상chain 재사용 금지.
자체 정상 넘버맨 freshFF저장/cold이어하기3페이지·거츠맨첫인사2페이지/PET8장면22항목/29focus·No·B취소 회귀 PASS. 기존56archive·선택 자산·그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 수정 유지. 실제 거츠맨 초상 및 모든 내비 자기 pool 유지.
기록 `analysis/GUTSMAN_PET_TALK_ROM_HANDOFF.md`; 결과·직접 확인 화면 `analysis/gutsman_pet_talk_v1/`.
미선택 일본어 포함27,770개/기타1,859개. 이번33source literals 중 chip104 script13의2literal/칩 이름은 원문 유지: 기존 롤 전용 selector를 거츠맨에 전용하지 않았고 별도 consumer/layout 검증 필요. 일정 알림18literal/전체이미지·inline/fixed population/한글 이름 committed record·재표시·영구재로드·기존save호환 등 남음. 전체 요청 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 전투 결과 대사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_battle_results_v1.gba`.
SHA256 `126223bdb1e707b396dbbd1a16788b852bf97ca6ea4aa47f88e68015eedf5e92`.
신규3번역 literal(패배·승리·무승부), 누적2,247선택 literal/56선택·676원본 유지 archive.
166tests/source·control·glyph·geometry·roundtrip PASS. 최대103px≤PET132px. main/repro/final current_repro 동일,603Python tools drift=[]/원본 보존.
거츠맨 초상을 유지한 격리 renderer3페이지의 CPU/font/OBJ VRAM/화면·clearing·native arrow분리·border 검사와 직접 화면 확인 PASS. 실제 전투 결과/native caller/종료·재진입 검증은 아님. 진단 alias는ROM에 없고 진단state는 정상chain 재사용 금지.
정상 자체 freshFF저장/cold이어하기·넘버맨3페이지/거츠맨첫인사2페이지/PET8장면22항목/29focus·No·B취소 회귀 PASS. 기존55archive·선택 자산·그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 수정 유지.
기록 `analysis/GUTSMAN_BATTLE_RESULTS_ROM_HANDOFF.md`; 결과·화면 `analysis/gutsman_battle_results_v1/`.
미선택 일본어 포함27,801개/기타1,859개. 다음 R대화66A844의 전체33literal·닉네임2/칩이름1 삽입·flag/요일 분기는 읽었으나 번역 입력 미작성. 일정 알림18미선택literal/전체이미지·inline/fixed population/한글 이름 committed record·재표시·영구재로드·기존save호환 등 남음. 전체 요청 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 PET 일정 알림 부분 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_schedule_alarm_v1.gba`.
SHA256 `5e3547d5f773decb9bebfe36b86dadc0fd4df73ee7f003c1aa9870f2e49decfd`.
신규3번역 literal(PET학원2페이지/추가일정 연결1), 누적2,244선택 literal/55선택·677원본 유지 archive.
163tests/source·control·glyph·geometry·roundtrip PASS. 최대82px≤132px. main/repro/final current_repro 동일,598Python tools drift=[]/원본 보존.
격리 PET renderer3페이지 strict CPU/font/OBJ VRAM/화면·clearing·page 순서·native arrow 분리·border 검사 및 직접 화면 확인 PASS. 실제 시간에 따른 알림 발생/등록일정/후속dispatch 증거는 아님. 진단state 정상chain 재사용 금지, alias는ROM에 없음, 거츠맨 초상 유지.
정상 자체 freshFF저장/cold이어하기·넘버맨3페이지/거츠맨첫인사2페이지/PET8장면22항목/29focus·No·B취소 회귀 PASS. 기존54archive·선택자산·그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 수정 유지.
기록 `analysis/GUTSMAN_SCHEDULE_ALARM_ROM_HANDOFF.md`; 결과·화면 `analysis/gutsman_schedule_alarm_v1/`.
미선택 일본어 포함27,804개/기타1,859개. 알림의 다른18literal(동적event/nickname/PET·mugshot 별도 consumer), 전체이미지/inline/fixed population/한글 이름 committed record·재표시·영구재로드·기존save 호환 등 남음. 전체 요청 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 일정 안내 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_schedule_v1.gba`.
SHA256 `b41a0a423c4fe07f2be59d1b30421fc87a4bff96b1fda3b6f51272601bec04ba`.
신규12항목=6번역 표현+6원문 유지 punctuation. 누적2,241선택 literal/54선택·678원본 유지 archive.
160tests/source·제어·숫자·glyph·geometry·roundtrip PASS. 시각뒤 ‘부터’24px≤원문30px/build-owned non-growth 검사, 원문 clock·AMPM·event buffer/quote·colon·space/loop 보존. main/repro/최종current_repro_r2 동일,593Python tools drift=[],원본 보존.
실제 거츠맨 L 오늘 일정10/no-event2페이지 strict CPU/font/OBJ VRAM/화면·clearing·page 순서·메뉴 복귀 PASS. 다가오는 일정1→2→3와 등록 일정11 시각/이벤트명→12는 static-only; 동적 event name 전체 번역·시각population·등록 이벤트 작동 증거 아님.
자체 넘버맨 freshFF저장/cold 이어하기3페이지·거츠맨 첫인사2페이지/PET8장면22항목/29focus·No수락·B취소 회귀 PASS. 기존53archive·선택 자산·그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 수정 유지. 각 내비 root는 자기 pool, 진단 alias는ROM에 없음.
기록 `analysis/GUTSMAN_SCHEDULE_ROM_HANDOFF.md`; 결과·화면 `analysis/gutsman_schedule_v1/`.
미선택 일본어 포함27,807개/기타1,859개, 전체 이미지·inline/fixed population·한글 이름 committed record/재표시/영구재로드/기존save 호환 등 남음. 전체 완료 아님. 다음 거츠맨 알림66651C: PET/mugshot 별도 renderer와 dynamic name·event 경계 추가 분석, 새 번역 입력 미작성.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 대회 대사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_competition_v1.gba`.
SHA256 `d52e23a57df78ad2ce5c89dfd59bf77f3b6af4d7612c1d73e63138a40c37cc53`.
신규10번역 literal. 누적2,229선택 literal/53선택·679원본 유지 archive.
157관련 tests/source·control·숫자2·nickname suffix·glyph·geometry·roundtrip PASS. main/repro/최종current_repro_r2 동일,588Python tools drift=[],원본 보존.
실제 거츠맨 참가 미등록10:0의 정상2완성샘플: 원본 이름 ああさま44px+느낌표와132px 둘째 행 포함, strict CPU/font/OBJ VRAM/화면 픽셀·clearing PASS. A 입력 후 PET 메뉴 복귀·추가draw없음 확인. 최초 검사에 다른 후보 이름 ああくん를 고정한 오류는 실패로 보존, 이번 원본 name decode/glyph/advance 검사를 적용해 동일 ROM에서 재검증. 우승/패배/격려 나머지9항목은 static-only, 실제 대회 결과·임의 이름·한글 이름 persistence 미검증.
자체 넘버맨 fresh FF저장/cold 이어하기/3페이지·거츠맨 첫인사2페이지/PET8장면22항목/29focus·No수락·B취소·복귀 회귀 PASS. 기존52archive·선택 자산·그래픽15라벨5블록 actualROM bytes 동일, ‘통신’ 수정 유지. 각 내비 root는 자기 pool, 진단 alias는ROM에 없음.
기록 `analysis/GUTSMAN_COMPETITION_ROM_HANDOFF.md`; 결과·화면 `analysis/gutsman_competition_v1/`.
미선택 일본어 포함27,813개/기타1,865개, 전체 이미지·inline/fixed population·한글 이름 committed record/재표시/영구재로드/기존save 호환 등 남음. 전체 완료 아님. 다음 거츠맨 일정666F38의12literal: 고정5번역 문구/시간뒤1suffix/유지punctuation6, 전체TPL·265bytes/root038134 확인, 새 번역 입력 미작성.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 귀환·접속·메일 알림 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_operations_v1.gba`.
SHA256 `5b03c125ab80d1e56efa0ca450fc1eef5eeb7a99b62881abc7a20db326a2abe3`.
신규31항목=17번역 문구+14원본 유지‘!!’. 누적2,219선택 literal/52선택·680원본 유지 archive.
154관련 tests/원문·숫자·제어·이름 뒤 쉼표·glyph·geometry·roundtrip PASS. main/repro/최종current_repro_r3 동일,583Python tools drift=[],원본 보존. 메일 초기‘!!’는 원본 알림음/대기 명령 boundary로 문장끝 느낌표와 구분, 검사 완화·ROM code 변경 없음.
실제 거츠맨 접속1페이지20glyph의 완성28샘플 strict font/VRAM/화면·clearing 검사 통과, 원본wait30 명령 유지/샘플 관측 간격31프레임, 이후 인터넷 화면 진입 확인. 초기 잘못 선택된 토너먼트 경로와 마지막 느낌표 작성 중3미완성샘플 FAIL 증거 보존·통과로 세지 않음. 귀환2/메일28항목의 정상 caller/이름·메일 delivery 이벤트는 static-only.
자체 넘버맨 fresh FF저장/cold 이어하기/넘버맨3페이지·거츠맨 첫인사2페이지·PET8장면22항목/29focus·No수락·B취소·복귀 회귀 PASS. 기존49 archive·선택 자산·그래픽15라벨5블록 actualROM bytes 보존, ‘통신’ 수정 유지. 모든 내비 root는 자기 pool 유지, 진단 alias는ROM에 없음.
기록 `analysis/GUTSMAN_OPERATIONS_ROM_HANDOFF.md`; 결과·화면 `analysis/gutsman_operations_v1/`.
미선택 일본어 포함27,823개/기타1,865개, 전체 이미지·inline/fixed population·한글 이름 committed record/재표시/영구재로드/기존save 호환 등 남음. 인간 검토 대기, 전체 완료 아님. 다음 거츠맨 대회666D5C의10미번역(이번 화면에서 확인한 미등록 안내 포함): 전체TPL/root03812C/473bytes 확인, 신규 번역 입력 미작성.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 PET 메뉴 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_pet_v1.gba`.
SHA256 `e0e24bbb1b6eaa5bdcac2553fa17569654baa9b3dc79bbf47202d86f395c6686`.
거츠맨 PET44항목(16문구+28예/아니요 라벨) 추가. 누적2,188선택 literal/49선택·683원본 유지 archive.
원문/제어/숫자/선택지14행/glyph/geometry/roundtrip와151tests 통과.3독립 동일 빌드,578Python 도구 drift=[], 원본 보존.
실제 거츠맨 idle/초기 질문의8장면·22항목,29focus/No 수락/B 취소/복귀 상태와 font/VRAM/화면 픽셀·본문 clearing 검사 통과. 최대116px 본문 포함. 나머지 재질문10..16/중단20의22항목은 static-only. ‘예’ 수락 이후 실제 메뉴 진입/통신 작동은 이번 검증 범위 아님.
자체 정상 넘버맨 저장/cold 이어하기/넘버맨3페이지·거츠맨 첫 인사2페이지 회귀 및 기존48archive·자산·그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ 수정 유지. 각 내비 대사 root는 자기 pool 유지, 진단 alias는ROM에 포함되지 않는다.
기록 `analysis/GUTSMAN_PET_ROM_HANDOFF.md`; 결과·화면 `analysis/gutsman_pet_v1/`.
미선택 일본어 포함27,840개/기타1,879개와 전체 이미지·한글 이름 입력/저장 호환 등이 남아 있다. 인간 검토 대기, 전체 완료 아님. 다음 거츠맨 귀환6663B8/접속6664D0/메일 알림666820 묶음: 전체 원문과 native roots 확인, 신규 번역 입력 미작성.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 첫 인사·재선택 인사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_gutsman_intro_v1.gba`.
SHA256 `04dc41d321ef81bbd8a1266204ecbca97bda39fa179a0d3569e474431170afdc`.
거츠맨 인사4문구 추가. 누적2,144선택 literal/48선택·684원본 유지 archive.
원문/제어/숫자/glyph/geometry/roundtrip와148tests 통과.3독립 동일 빌드,573Python 도구 drift=[], 원본 보존.
실제 거츠맨 정상 선택으로 첫 인사2페이지 strict font/VRAM/화면 픽셀·clearing·순서·종료 검사 통과. 최대102px 행 포함. 이번 화면은 넘버맨 초상 진단이 아닌 실제 거츠맨이다. 재선택 인사2문구는 ROM 반영·static 검사만 완료, 정상 호출 미검증.
자체 정상 넘버맨 저장/cold 이어하기/넘버맨3페이지 회귀와 기존47archive·선택 자산·그래픽15라벨/5블록 실제ROM bytes 보존 통과. ‘통신’ 수정 유지. 각 내비의 대사 root는 자기 pool 유지, 진단 alias는ROM에 포함되지 않는다.
기록 `analysis/GUTSMAN_INTRO_ROM_HANDOFF.md`; 결과·화면 `analysis/gutsman_intro_v1/`.
미선택 일본어 포함27,884개/기타1,879개와 전체 이미지·한글 이름 입력/저장 호환 검증 등이 남아 있다. 인간 검토 대기, 전체 완료 아님. 다음 거츠맨 PET665F3C의44미번역 항목: 전체 원문과 original root038114 확인, 신규 번역 입력 미작성.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 포르테 기념일·생일 대사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_forte_seasonal_v1.gba`.
SHA256 `692566c04c780b29131154a7d015e22192c88f3e7858c2858b972977d0fc60d0`.
포르테30문구와 유지 인용부호2개·여섯 점 침묵1개 추가. 누적2,140선택 literal/47선택·685원본 유지 archive.
33항목 원문/제어/숫자/glyph/geometry/roundtrip와145tests 통과.3독립 동일 빌드,568Python 도구 drift=[], 원본 보존.
새해3/칠석4/이브1 총8페이지 격리 renderer 진단과 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 최대129px 한 줄 포함, 잘림/가림/잔상 없음. 정상 포르테 해금/초상/날짜 선택 증거 아님. 다른23번역 문구/성별·이벤트 static-only.
진단 스크린샷은 넘버맨 caller·초상을 유지한 임시 read alias이며 ROM에 포함되지 않는다. 실제 ROM에서는 넘버맨 root0382AC와 포르테 root03857C가 각각 자기 pool을 가리킨다. 넘버맨으로 되돌리는 수정 불필요, 진단 state는 정상 경로 재사용 금지.
기존46 archive payload·선택 자산과 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/FORTE_SEASONAL_ROM_HANDOFF.md`; 결과·화면 `analysis/forte_seasonal_v1/`.
미선택 일본어 포함27,888개/기타1,879개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 인간 검토 대기, 전체 완료 아님. 다음 거츠맨 intro665EB8의 미번역4문구, 원문 전체와 original roots038110/038144 관계 확인.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 플랜트맨 기념일·생일 대사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_plantman_seasonal_v1.gba`.
SHA256 `c7553dffa4d3cf32c935c41fd5e154ae91cee76885eeffdfffec6ab1138f9c93`.
플랜트맨41문구와 유지 인용부호2개 추가. 누적2,107선택 literal/46선택·686원본 유지 archive.
43항목 원문/제어/숫자/이름 뒤2suffix/glyph/geometry/roundtrip와142tests 통과. 다이다이·대대로 의미/볶은 콩·싹/꽃·나이테 비유/일본 날짜 보존 초안.3독립 동일 빌드,563Python 도구 drift=[], 원본 보존.
절분5/칠석4/섣달그믐3 총12페이지 격리 renderer 진단과 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과.132px 둘째 행 경계 포함, 잘림/가림/잔상 없음. 넘버맨 caller·초상 유지 진단이며 정상 플랜트맨 해금/초상/날짜 선택 증거 아님. 다른29문구/이름·성별·이벤트 static-only.
기존45 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/PLANTMAN_SEASONAL_ROM_HANDOFF.md`; 결과·화면 `analysis/plantman_seasonal_v1/`.
미선택 일본어 포함27,919개/기타1,881개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 인간 검토 대기, 전체 완료 아님. 다음 포르테6D5A9C: 동일 group jack-in6D27A0의 フォルテ.EXE와 원본 root 관계로 화자 확인.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 일렉맨 기념일·생일 대사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_elecman_seasonal_v1.gba`.
SHA256 `9772ae035ea240f239664c29008ff7d96137250e74001b656adab9a1a8a55f93`.
일렉맨38문구와 유지 인용부호2개 추가. 누적2,064선택 literal/45선택·687원본 유지 archive.
40항목 원문/제어/숫자/glyph/geometry/roundtrip와139tests 통과. 도깨비·천둥신·썬더맨 대비/조명·리셋 호언/날짜 보존 초안. main/repro/최종current_repro_r2 동일,558Python 도구 drift=[], 원본 보존.
절분6/크리스마스4/이브2 총12페이지 격리 renderer 진단과 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과.132px 단일 행 경계 포함, 잘림/가림/잔상 없음. 넘버맨 caller·초상 유지 진단이며 정상 일렉맨 해금/초상/날짜 선택 증거 아님. 다른26문구/성별·이벤트 static-only.
기존44 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/ELECMAN_SEASONAL_ROM_HANDOFF.md`; 결과·화면 `analysis/elecman_seasonal_v1/`.
미선택 일본어 포함27,960개/기타1,883개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 인간 검토 대기, 전체 완료 아님. 다음 플랜트맨6D0ADC.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 아이스맨 기념일·생일 대사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_iceman_seasonal_v1.gba`.
SHA256 `e0d5c1995e12ddbd30755875d37bbe513a4d15fa28dbcc9caa96c61b0d05a4f6`.
아이스맨32문구와 유지 인용부호2개 추가. 누적2,024선택 literal/44선택·688원본 유지 archive.
34항목 원문/제어/숫자/이름 뒤2suffix/glyph/geometry/roundtrip와136tests 통과. B/V 이브 표기 대비·찬 중화면 농담·일본 날짜 보존 초안.3독립 동일 빌드,553Python 도구 drift=[], 원본 보존.
크리스마스이브3/섣달그믐4 총7페이지 격리 renderer 진단과 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 잘림/가림/잔상 없음. 넘버맨 caller·초상 유지 진단이며 정상 아이스맨 해금/초상/날짜 선택 증거 아님. 다른25문구/이름·성별·이벤트 static-only.
기존43 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/ICEMAN_SEASONAL_ROM_HANDOFF.md`; 결과·화면 `analysis/iceman_seasonal_v1/`.
미선택 일본어 포함27,998개/기타1,885개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 인간 검토 대기, 전체 완료 아님. 다음 일렉맨6CB184.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 네이팜맨 기념일·생일 대사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_napalmman_seasonal_v1.gba`.
SHA256 `5a2644e47d768d1afbf5b7becf49053c25e99d84cfa43e36d91a75680fc22406`.
네이팜맨36문구와 유지 인용부호2개 추가. 누적1,990선택 literal/43선택·689원본 유지 archive.
38항목 원문/제어/숫자/glyph/geometry/roundtrip와133tests 통과. 크리스마스 반전과108발 수량 보존.3독립 동일 빌드,548Python 도구 drift=[], 원본 보존.
새해4/절분5 총9페이지 격리 renderer 진단과 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 잘림/가림/잔상 없음. 넘버맨 caller·초상 유지 진단이며 정상 네이팜맨 해금/초상/날짜 선택 증거 아님. 다른27문구/성별·이벤트 static-only.
기존42 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/NAPALMMAN_SEASONAL_ROM_HANDOFF.md`; 결과·화면 `analysis/napalmman_seasonal_v1/`.
미선택 일본어 포함28,030개/기타1,887개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 인간 검토 대기, 전체 완료 아님. 다음 아이스맨6C5A88.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 나이트맨 기념일·생일 대사 통합 (2026-10-06)

ROM: `poc/output/exe45_ko_development_knightman_seasonal_v1.gba`.
SHA256 `2c130314fe4af7611df9a9ace9c667a843baa8fdfe636e276f58e04ab244535f`.
나이트맨39문구와 유지 문장부호3개 추가. 누적1,952선택 literal/42선택·690원본 유지 archive.
42항목 원문/제어/숫자/이름 뒤7suffix 경계/glyph/geometry/roundtrip와130tests 통과.4:1은 주는 방향을 유지하며 source22px suffix를 comma11px로 줄였다. 새해 scalar comma는 원본·대상 명령 경계에 고정.3독립 동일 빌드,543Python 도구 drift=[], 원본 보존.
절분3/갑옷 설명5 총8페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 잘림/가림/잔상 없음. 진단은 넘버맨 caller·초상 유지, 정상 나이트맨 해금/초상/날짜 선택 증거 아님. 다른31문구/이름·성별·이벤트 출력 static-only.
기존41 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/KNIGHTMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/knightman_seasonal_v1/`.
미선택 일본어 포함28,066개/기타1,889개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 문화/말투/명칭 인간 검토 대기, 전체 완료 아님. 다음 네이팜맨6C004C.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 섀도맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_shadowman_seasonal_v1.gba`.
SHA256 `480dae114a8b4d0295cd25c7cfaf89a11def7373b6922d35892fc326559893d5`.
섀도맨39문구와 유지 인용부호2개 추가. 누적1,910선택 literal/41선택·691원본 유지 archive.
41항목 원문/제어/숫자/glyph/geometry/roundtrip와127tests 통과. 원본 script4의 jump3/23bytes 보존.3독립 동일 빌드,538Python 도구 drift=[], 원본 보존.
새해3/잉어 깃발 설명6 총9페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 잘림/가림/잔상 없음. 진단은 넘버맨 caller·초상 유지, 정상 섀도맨 해금/초상/날짜 선택 증거 아님. 다른30문구/발렌타인 실제 분기/이벤트 이름 출력 static-only.
기존40 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/SHADOWMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/shadowman_seasonal_v1/`.
미선택 일본어 포함28,105개/기타1,892개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 문화/말투/명칭 인간 검토 대기, 전체 완료 아님. 다음 나이트맨6BA3AC.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 스타맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_starman_seasonal_v1.gba`.
SHA256 `54b2e115560d190da157db187fb5cda3bf5e0eebf64c62bf67291cfd2dc06172`.
스타맨46문구와 유지 인용부호2개 추가. 누적1,869선택 literal/40선택·692원본 유지 archive.
48항목 원문/제어/숫자/glyph/geometry/roundtrip와124tests 통과.3독립 동일 빌드,533Python 도구 drift=[], 원본 보존.
새해4/칠석5 총9페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 잘림/가림/잔상 없음. 진단은 넘버맨 caller·초상 유지, 정상 스타맨 해금/초상/날짜 선택 증거 아님. 다른37문구/성별/이벤트 이름 출력 static-only.
기존39 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/STARMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/starman_seasonal_v1/`.
미선택 일본어 포함28,144개/기타1,894개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 문화/말투/명칭 인간 검토 대기, 전체 완료 아님. 다음 섀도맨6AE834.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 우드맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_woodman_seasonal_v1.gba`.
SHA256 `fcca6e0666a071959b01f7ff0af11fa381e703a2f07fd02eb2579937ed38a9f6`.
우드맨39문구와 유지 인용부호2개 추가. 누적1,821선택 literal/39선택·693원본 유지 archive.
41항목 원문/제어/숫자/새해 이름 뒤 쉼표/glyph/geometry/roundtrip와121tests 통과. 반복 손뼉2문구는 각각 원본 명령 경계로 구분했다. main/repro/최종current_repro_r3 동일,528Python 도구 drift=[], 원본 보존.
절분4/칠석3 총7페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 칠석 첫 캡처의4픽셀 blending 실패는 보존하고 같은 ROM에서 대기를 늘려 strict pixel 검사를 통과했다. 진단은 넘버맨 caller·초상 유지, 정상 우드맨 해금/초상/날짜 선택 증거 아님. 다른32문구/이름 출력 static-only.
기존38 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/WOODMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/woodman_seasonal_v1/`.
미선택 일본어 포함28,190개/기타1,896개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 문화/말투/명칭 인간 검토 대기, 전체 완료 아님. 다음 스타맨6A8ADC.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 아쿠아맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_aquaman_seasonal_v1.gba`.
SHA256 `05d164a5eae6cc931b24f7326d8024241e7b4f36a85fa1a1ea9a48762f402eb0`.
아쿠아맨41문구와 유지 인용부호2개 추가. 누적1,780선택 literal/38선택·694원본 유지 archive.
43항목 원문/제어/숫자/이름 뒤 쉼표 경계/glyph/geometry/roundtrip와118tests 통과.3독립 동일 빌드,523Python 도구 drift=[], 원본 보존.
새해3/칠석3 총6페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 진단은 넘버맨 caller·초상 유지, 정상 아쿠아맨 해금/초상/날짜 선택 증거 아님. 다른35문구와 실제 이름 출력은 static-only.
기존37 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/AQUAMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/aquaman_seasonal_v1/`.
미선택 일본어 포함28,229개/기타1,898개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. ‘퓨’ 말끝/문화/용어는 인간 검토 대기이며 전체 완료 아님. 다음 우드맨6A2184.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 정크맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_junkman_seasonal_v1.gba`.
SHA256 `59ea4b8d2281d2ee1addd58de2c8b84492c417bfc993f4f53d95f41cf2bf87e7`.
정크맨35문구와 유지 인용부호2개 추가. 누적1,737선택 literal/37선택·695원본 유지 archive.
37항목 원문/제어/줄 구조/생일 이름 뒤 쉼표/glyph/geometry/roundtrip와115tests 통과.3독립 동일 빌드,518Python 도구 drift=[], 원본 보존.
새해3/칠석5 총8페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과.132px 경계 줄 잘림/가림 없음. 진단은 넘버맨 caller·초상 유지, 정상 정크맨 해금/초상/날짜 선택 증거 아님.
기존36 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/JUNKMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/junkman_seasonal_v1/`.
초콜릿 말장난은 뜻만 옮긴 인간 검토 대기 초안. 미선택 일본어 포함28,270개/기타1,900개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 전체 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 메탈맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_metalman_seasonal_v1.gba`.
SHA256 `74558c971f1761de0f0b12fb7cb7b62c54a8e9c64420fe4921d5521b5f8c9820`.
메탈맨37문구와 유지 인용부호2개 추가. 누적1,700선택 literal/36선택·696원본 유지 archive.
39항목 원문/제어/숫자/이름 뒤 쉼표 경계/glyph/geometry/roundtrip와112tests 통과.3독립 동일 빌드,513Python 도구 drift=[], 원본 보존.
절분3페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 진단은 넘버맨 caller·초상 유지 및 root/script-offset alias, 정상 메탈맨 해금/초상/날짜 선택 증거 아님. 새해/생일 이름 출력 페이지는 static-only.
기존35 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/METALMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/metalman_seasonal_v1/`.
미선택 일본어 포함28,305개/기타1,902개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 전체 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 블루스 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_blues_seasonal_v1.gba`.
SHA256 `a57a6cd7a68f926b18106ec4afc00371633ca12ce6987977143127dbfa3d7bda`.
블루스31문구와 유지 인용부호2개 추가. 누적1,661선택 literal/35선택·697원본 유지 archive.
33항목 원문/제어/숫자/줄 구조/glyph/geometry/roundtrip와109tests 통과.3독립 동일 빌드,508Python 도구 drift=[], 원본 보존.
새해4페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과.132px 경계 줄 가림/잘림 없음. 진단은 넘버맨 caller·초상 유지, 정상 블루스 해금/초상/날짜 선택 증거 아님.
기존34 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/BLUES_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/blues_seasonal_v1/`.
미선택 일본어 포함28,342개/기타1,904개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 전체 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 썬더맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_thunderman_seasonal_v1.gba`.
SHA256 `82a8d2cbe6b411cef7d5705c1b22109221b9694bfe61fde3386a50ad0ee5e4c4`.
썬더맨32문구와 유지 인용부호2개 추가. 누적1,628선택 literal/34선택·698원본 유지 archive.
34항목 원문/제어/숫자/줄 구조/glyph/geometry/roundtrip와106tests 통과.3독립 동일 빌드,503Python 도구 drift=[], 원본 보존.
새해2페이지 격리 renderer 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 진단은 넘버맨 caller·초상 유지, 정상 썬더맨 해금/초상/날짜 선택 증거 아님.
기존33 archive payload와 선택 자산, 그래픽15라벨/5블록 실제ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/THUNDERMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/thunderman_seasonal_v1/`.
미선택 일본어 포함28,373개/기타1,906개와 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 전체 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 파이어맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_fireman_seasonal_v1.gba`.
SHA256 `45086b944e2919f245ed8f63b80dde7cc2a3f22fb3209a012e5d6770cfe726c8`.
파이어맨44문구와 유지 인용부호/느낌표3개 추가. 누적1,594선택 literal/33선택·699원본 유지 archive.
전체47항목 원문/제어/숫자/생일 이름 출력 경계/glyph/geometry/roundtrip와103tests 통과.3독립 동일 빌드,498Python 도구 drift=[], 원본 보존.
새해3페이지 격리 렌더링 진단과 같은 ROM 정상 저장/cold 이어하기/넘버맨3페이지 회귀 통과. 진단은 넘버맨 caller·초상 유지, 정상 파이어맨 해금/초상/날짜 선택 증거 아님.
기존32 archive payload와 선택 자산, 그래픽15라벨/5블록 실제 ROM bytes 보존. ‘통신’ glyph 수정 유지.
기록 `analysis/FIREMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/fireman_seasonal_v1/`.
미선택 일본어 포함28,405개/기타1,908개 및 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 전체 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 서치맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_searchman_seasonal_v1.gba`.
SHA256 `4a42aa2821057f480a1aacfe4c3c78a2a87e85eeb1d6152bc1a8e7e699cf50b2`.
서치맨38문구와 유지 인용 부호2개 추가. 누적1,547선택 literal/32선택·700원본 유지 archive.
전체40항목 source/controls/숫자/glyph/geometry/roundtrip,100tests,3독립 동일 빌드/493Python drift=[] 통과.
격리된 렌더링 진단11페이지(새해3/칠석55%4/이브45%4)와 같은 ROM 정상 저장/cold 이어하기/넘버맨 새해3페이지 회귀 통과. 신규 화면의 넘버맨 caller·초상은 유지되므로 서치맨 정상 해금/초상/날짜 선택 증거 아님.
기존31 archive payload와 선택 자산, 그래픽15라벨/5블록의 실제 ROM bytes 보존. ‘통신’ glyph 수정도 유지.
기록 `analysis/SEARCHMAN_SEASONAL_ROM_HANDOFF.md`; 결과와 화면 `analysis/searchman_seasonal_v1/`.
미선택 일본어 포함28,449개/기타1,911개, 전체 이미지·이름/저장 호환 검증 등이 남아 있다. 전체 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 윈드맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_windman_seasonal_v1.gba`.
SHA256 `30db71bf4d47a7acb163044c2ee745210935acd1cb085c5e175007fd52087301`.
윈드맨44문구와 원본 유지 인용 부호2개 추가. 누적1,507선택 literal/31선택·701원본 유지 archive. 이전30 payload와 번역·이미지 자산 유지.
46개 전체 원문/제어/숫자/폰트/geometry/roundtrip,97tests와3독립 동일 빌드 통과. 최종488Python 도구 drift=[], 원본 보존.
윈드맨 새해5페이지는 격리된 renderer 진단으로 검증했다. 넘버맨 caller/초상 유지, 정상 윈드맨 해금·초상·날짜 선택 검증 아님. 같은 ROM 정상 저장/cold 이어하기 및 넘버맨 새해3페이지 회귀 통과.
기록: `analysis/WINDMAN_SEASONAL_ROM_HANDOFF.md`; 화면/검사: `analysis/windman_seasonal_v1/`.
미선택 일본어 포함28,487개/기타1,913개와 전체 이미지·이름 입력/저장 호환 등이 남아 있다. 전체 완료 아님.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 거츠맨 기념일·생일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_gutsman_seasonal_v1.gba`.
SHA256 `6af4aad8403d878fc1a4ebf035cb0e0b665c721e5aacfd1a4a66e3a3c8437b56`.
거츠맨47문구와 원본 유지 인용 부호2개 추가. 누적1,461선택 텍스트/30선택·702원본 유지 archive. 이전 번역·이미지 선택 유지.
49개 전체 원문/제어/숫자/폰트/레이아웃/roundtrip와 관련95tests 통과. 실제 화면·회귀 결과: `analysis/gutsman_seasonal_v1/runtime.json`.
기록: `analysis/GUTSMAN_SEASONAL_ROM_HANDOFF.md`. 미선택 일본어 포함28,531개/그 밖1,915개가 남았으며 전체 번역 완료는 아니다.
한글 이름·저장 호환·전체 이미지/미방문 분기 검증 미완료. functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 작업: 전체 미번역 목록 확정·3내비 기념일 대사 통합 (2026-10-05)

ROM: `poc/output/exe45_ko_development_seasonal_trio_v1.gba`.
SHA256 `59cb097e0a40f26763ff3dbbbe60c533defb72de7617895ab802cd20d45cad89`.
록맨28/롤41/넘버맨60 literal 추가: 새 번역123문구와 원본 유지 인용 부호6개. 누적1,412선택 텍스트/29선택·703미선택 archive. 기존 번역 및 이미지 선택 유지.
732개 archive를 새로 추출하고 엄격히 분석했다. 실제 literal31,907개이며 현재 미선택 일본어 포함28,578개/그 밖1,917개가 남았다. 전체 완역 완료가 아니다.
전체 관련93tests와 129개 static 원문·제어·수치·폰트·레이아웃·roundtrip 검사 통과. 세 내비 정상 경로 새해 인사9페이지 검증은 `analysis/seasonal_trio_v1/runtime.json`, 화면은 `analysis/seasonal_trio_v1/new_year_pages.png` 참조.
최종3독립 빌드 동일 SHA/원본 보존/478Python 도구 drift=[] 확인: `analysis/seasonal_trio_v1/final_identity_audit.json`.
전체 목록과 다음 작업: `analysis/FULL_TRANSLATION_BACKLOG_HANDOFF.md`, `analysis/full_scope_trio_v1/literal_backlog.json`.
한글 이름 입력·committed record·재표시·영구 재로드·기존save 호환 및 전체 이미지/미방문 분기 검증 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 재선택 인사5단위 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_return_v1.gba`.
재선택 인사5literal 추가. 마지막4649 말장난은 사용자가 선택한 자연스러운 ‘다시 한번/잘 부탁드려요’로 번역했다. 원문 source와 제어 코드/1명 숫자/줄 구조 보존.
누적1,283선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률 아님.
신규5개 별도 격리 진단의 font→OBJ VRAM→화면/잔상/종료 검증, 기존 첫 만남7페이지 정상 회귀 및88tests 통과.
같은 롬 정상 저장→cold 이어하기→넘버맨 재선택도 시도했으나 새해 인사 이벤트가 나와 대상script2 정상 진입은 아직 미검증이다. 저장 파일은 reload 전후 동일; 한글 이름 persistence proof 아님.
SHA256 `f0c33a99ada35c0575a40a72727bbd894633c2b59b21ae67fb6156d16caa152e`.
화면: `analysis/numberman_return_v1/return_pages.png`. 기록: `analysis/NUMBERMAN_RETURN_ROM_HANDOFF.md`.
최종 독립3빌드/470Python 도구 audit은 `analysis/numberman_return_v1/final_identity_audit.json` 참조.
다른 미번역/대기 화살표 차이/일부 말풍선·결과 및 한글 이름·재표시·영구 재로드·기존save 호환 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 레벨 선택·학력 조사 안내10단위 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_drill_options_v3.gba`.
레벨 안내·레벨1~4 및 학력 조사 소개/선택지10literal 추가. 누적1,278선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률 아님.
원문 명령·번호·줄 구조 보존. 커서가 왼쪽 숫자를 덮는 실패를 고치기 위해 source-pinned grid 앞/열 사이8px literal 여백 적용.
신규10개는 별도 격리 진단12화면의 font→OBJ VRAM→화면/비가림/잔상 검증 통과. 실제 진입 조건·선택 gameplay effect는 아직 미검증이다.
같은 롬 own-cold의 기존 특훈 안내/선택지6페이지 회귀 검사 통과. 관련85tests 통과. 세 독립 빌드·최종466Python 도구 검증은 final_identity_audit.json 참조.
SHA256 `1077e4faf91eb46568a279692c3fbbedc898f594074f5b921dd2f85cae0b5468`.
화면: `analysis/numberman_drill_options_v3/diagnostic_options_pages.png`. 기록: `analysis/NUMBERMAN_DRILL_OPTIONS_ROM_HANDOFF.md`.
native 대기 화살표는 OAM/VRAM/palette source phase와 같으나 일부 screen53pixels 차이는 원인 미확인. 그래픽/전체 QA 완료로 인정하지 않는다.
다른 미번역/일부 말풍선·결과, 한글 이름 입력/committed record/재표시·영구 재로드/기존save호환 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 금액·개수 표시6단위 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_training_rewards_v2.gba`.
제니/버그 조각 획득·기록 결과의 숫자 접미사6literal 추가. 누적1,268선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률 아님.
숫자·보상 명령과 원문 구조 보존, 최대800/5를 포함한 합성 줄100/122/92/114px 검사 통과.
같은 롬 정상 실패2문구/PET 복귀·권유 회귀, 별도 격리 진단4종의 신규6개 전체 숫자 RAM→font→OBJ VRAM→화면/잔상 검사 통과. 정상 승리·보상 지급 proof가 아니다.
79tests 및 최종3독립 빌드 동일 SHA, 원본 보존·463Python tools drift=[] 통과.
SHA256 `bdabafd336f398e19776df64f778950f8f9517b07e40333ddc4dc05002543e35`.
화면: `analysis/numberman_training_rewards_v1/diagnostic_reward_pages.png`. 기록: `analysis/NUMBERMAN_TRAINING_REWARDS_ROM_HANDOFF.md`.
v1 실행 ROM/v2 최종 ROM 전체bytes 동일 확인. 메타데이터 정합을 위해 v2를 별도 빌드했으며, 실패 빌드/첫 진단·이전 후보를 보존했다.
학력조사/레벨 선택/일부 말풍선·결과/다른 미번역, 한글 이름 입력/committed record/재표시·영구 재로드/기존save호환 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 계산 훈련 결과·보상 안내17단위 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_training_results_v1.gba`.
실패/칭찬/보상/기록 반응17literal을 추가했다. 누적1,262선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률 아님.
기존25다른 archive payload·저장 제목·권유10/11/20/21 bytes와 제어/숫자 명령 유지.
새 롬 own-cold→시간 종료→실패 대사2개→PET 복귀의 font→OBJ VRAM→화면 검증 통과. 나머지15개는 static-only, 성공·보상 지급 미검증.
관련76tests, 세 독립 빌드 동일 해시, 원본 보존·458Python 도구 drift=[] 검사 통과.
SHA256 `562bb6ba061bc6eb4d6e3c033b148a84a44095a97db2b749aac197ff99a4da9b`.
화면: `analysis/numberman_training_results_v1/results_pages.png`. 기록: `analysis/NUMBERMAN_TRAINING_RESULTS_ROM_HANDOFF.md`.
동적 금액 접미사/학력조사/레벨 선택/일부 말풍선·다른 미번역과 한글 이름 입력/committed record/재표시·영구 재로드/기존save호환 미완료. 관측 native 일본어 이름만 원문 픽셀 보존 비교했다.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 계산 훈련 작은 말풍선12단위 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_drill_bubbles_v1.gba`.
작은 진행 말풍선12literal을 추가했다. 누적1,245선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률 아님.
기존25다른 archive payload/저장 제목 및 훈련 소개·설명0/1 bytes 유지. 신규7문구 실제 font→OBJ VRAM→화면 검증, 신규5문구는 static-only이며 화면 검증 미완료.
같은 새 롬 own-cold→훈련, 초기/마지막 프레임 관측.175개의 typing/transfer/효과/닫힌창 snapshot은 완성 화면으로 세지 않았다. 관련73tests 통과.
SHA256 `6763f94f40539c1309250416e18f988aeb397788af581cb4862f88a93eced2da`.
화면: `analysis/numberman_drill_bubbles_v1/bubble_pages.png`. 기록: `analysis/NUMBERMAN_DRILL_BUBBLES_ROM_HANDOFF.md`.
학력조사/레벨 선택/결과·보상·다른 미번역과 한글 이름 입력/committed record/재표시·영구 재로드/기존save호환 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 계산 훈련 소개·설명20단위 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_drill_intro_v1.gba`.
훈련 소개/설명/세로 선택지20literal을 추가했다. 누적1,233선택 텍스트 /15기존 그래픽 /26선택·706미선택 archive. 전체 완역률 아님.
기존25archive payload·저장 제목 유지. 새 롬 own-cold→넘버맨→훈련 소개→설명 전 페이지에서 신규20문구 전부의 font CPU reads→OBJ VRAM→화면43,140pixels, 잔상 제거, 위/아래 포커스 통과.
관련72tests와 동일 해시 재빌드 통과. SHA256 `e89d3e753a87ae0530ffdbed961124c1c90c301c7df6928aac815719a6f2c028`.
화면: `analysis/numberman_drill_intro_v1/drill_pages.png`. 기록: `analysis/NUMBERMAN_DRILL_INTRO_ROM_HANDOFF.md`.
학력조사/레벨 선택/작은 말풍선/결과·보상·다른 미번역, 한글 이름 입력/편집/committed record/재표시·영구 재로드/기존save호환 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 플러그인 구호 번역 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_jackin_v1.gba`.
‘플러그인! / 넘버맨.EXE、 / 트랜스미션!!’ 3행 구호1단위를 추가했다. 누적1,213선택 텍스트 /15기존 그래픽 /25선택·707미선택 archive. 전체 완역률 아님.
기존24archive payload와 저장 제목 유지. 새 롬 own-cold→넘버맨 선택→특훈 거절→구호의 CPU font read→OBJ VRAM→화면 픽셀·빈영역 검증, 원본 wait30 보존과 네트워크 진입 확인.
103프레임 캡처 중 완성된28연속프레임이 통과했다. 마지막 글자 전송/표시 중3캡처는 불일치 범위를 기록했으며 완성 화면으로 인정하지 않았다.
SHA256 `0300bee602e8c841360e661703870bf5dd25c660b444decbd4a43db1c1f74135`.
화면: `analysis/numberman_jackin_v1/jackin_pages.png`. 기록: `analysis/NUMBERMAN_JACKIN_ROM_HANDOFF.md`.
미니게임 설명/결과/보상·다른 남은 미번역·한글 이름 입력/편집·기존save호환·영구 재로드·전체게임/RTC/실기/오디오/인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 특훈 권유16단위 번역 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_training_intro_v1.gba`.
특훈 권유/거절과 플러그인 전 특훈 제안/거절16단위를 번역했다. 누적1,212선택 텍스트 /15기존 그래픽 /24선택·708미선택 archive. 전체 완역률 아님.
기존23archive payload 및 저장 제목 유지. 신규8단위는 실제 CPU font read→OBJ VRAM→화면12,852픽셀, 페이지/선택지 잔상과 응/싫은데 focus 검증 통과.
거절→경고21→기존 플러그인687E3C, 수락→미니게임715064 진입을 관측했다. 거절은 특훈 거절이며 PET로 돌아가는 선택이 아니다.
일반 특훈 권유10/거절11의8단위는 정적 검증만. 플러그인 구호와 미니게임 설명/결과/보상은 아직 일본어다.
관련68테스트 통과. 화면: `analysis/numberman_training_intro_v1/training_pages.png`. 기록: `analysis/NUMBERMAN_TRAINING_INTRO_ROM_HANDOFF.md`.
SHA256 `be556380b60b431af4c38b0beb7b5e22b3113ed167e2b6cd6437d358134effdb`.
한글 이름 입력/편집·기존save호환·영구 재로드·남은미번역/전체게임/RTC/실기/오디오/인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 PET 메뉴44단위 번역 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_pet_v1.gba`.
대기 질문·대회·플러그인·장비·라이브러리·메일·통신·저장 질문 및 선택지, 재진입/대화중단 반응44단위를 번역했다.
추가44개, 누적1,196선택 텍스트 /15기존 그래픽 /23선택·709미선택 archive. 전체 완역률 아님.
기존22archive payload 및 저장 제목 동일. 새 ROM cold→넘버맨 정상 선택→8종 PET 화면,22단위의 CPU font read→OBJ VRAM→화면픽셀·빈영역 clear·29 focus/cancel/return 전환 검증 통과.
저장 화면 ‘예’ 정상 진입→실제64KB native save 갱신·완료58 확인. 관련66테스트 통과, 원본 보존·최종3독립ROM 동일·현재445Python 도구 drift=[].
SHA256 `f590cc6fd38556ba85ca3b92101987019142b091d452b3485862feb79eb464f5`.
화면: `analysis/numberman_pet_v1/pet_prompts.png`. 기록: `analysis/NUMBERMAN_PET_ROM_HANDOFF.md`.
나머지22단위(중복 재진입/즉시저장/대화중단)는 정적 검증만; 한글 이름 입력/편집·기존save호환·영구 재로드·남은미번역/전체게임/RTC/실기/오디오/인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 첫 만남7페이지 번역 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_intro_v1.gba`.
자기소개·숫자/원주율 농담·마무리 인사7단위를 번역했다. 재선택 script2의 숫자 말장난은 원문 유지·별도 검토 대상이다.
추가7개, 누적1,152선택 텍스트 /15기존 그래픽 /22선택·710미선택 archive. 전체 완역률 아님.
기존21archive payload 및 저장 제목 동일. 새 ROM 정상 넘버맨 선택→7페이지의 실제 CPU glyph read→OBJ VRAM→화면 픽셀·빈 영역 clear·순서·종료 검증 통과.
실제64KB native save 갱신·완료58 확인. 관련64테스트 통과, 원본 보존·최종3독립ROM 동일·현재442Python 도구 drift=[].
SHA256 `219e5f7d88841bc19aeab74db7bca9e7aa309bf068e03c045ba2f3769453dceb`.
화면: `analysis/numberman_intro_v1/first_meeting.png`. 기록: `analysis/NUMBERMAN_INTRO_ROM_HANDOFF.md`.
넘버맨 PET 나머지/재선택·다른 Navi 미번역, 한글 이름 입력/편집·기존save호환·영구 재로드·전체게임/RTC/실기/오디오/인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 넘버맨 저장 문구16개 번역 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_numberman_save_poc_v1.gba`.
정중한 넘버맨 저장 확인·덮어쓰기·전원 경고·완료·실패/재시도·잘못 변경된 데이터 경고16단위를 추가했다.
기존 록맨/롤/거츠맨53저장 단위와15그래픽 유지. 누적1,145선택 텍스트 /21선택·711미선택 archive. 전체 완역률 아님.
새 ROM own-cold 넘버맨 선택→정상8단위의 CPU font read→OBJ VRAM→픽셀 검사 통과.
실제64KB native save 갱신·덮어쓰기 ‘아니요’의 disk 불변·PET 복귀 확인. 오류 관련8단위는 정적 검증만 완료했다.
이전115save slots(55..59외)·20다른payload·95미선택source slots 보존. 관련62테스트 통과.
SHA256 `7431216a52a62898fad57984cf17b6bd5566c9eb26282b30e9886f9666100345`.
화면: `analysis/numberman_save_poc_v1/save_pages.png`. 기록: `analysis/NUMBERMAN_SAVE_POC_HANDOFF.md`.
넘버맨 PET 일반 대사·다른 Navi 미번역, 한글 이름 입력/편집·기존save호환·영구 재로드·전체게임/RTC/실기/오디오/인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 거츠맨 저장 문구16개 번역 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_gutsman_save_poc_v1.gba`.
거츠맨의 저장 확인·덮어쓰기·전원 경고·완료·실패/재시도·잘못 변경된 데이터 경고를 번역했다.
기존 록맨/롤 저장37단위와 상단 `저장`·개수 `개`를 보존했다.
추가16개, 누적1,129선택 텍스트 /15그래픽 /21선택·711미선택 archive. 전체 완역률 아님.
새 ROM own-cold 거츠맨 선택→저장 진입에서 정상8단위의 CPU glyph read→OBJ VRAM→화면 픽셀 검증 통과.
실제64KB native save 갱신, 덮어쓰기 ‘아니요’의 파일 불변과 PET 복귀 확인. 오류 관련8단위는 정적 검증만 완료했다.
관련60테스트 통과. 이전115save scripts(25..29외)·20다른payload·100미선택source slots 보존.
SHA256 `35e9c751134d8016f1e81144a996632a060f06cf01dad97211c9b7773161d08b`.
화면: `analysis/gutsman_save_poc_v1/save_pages.png`. 기록: `analysis/GUTSMAN_SAVE_POC_HANDOFF.md`.
거츠맨 `거스/거츠` 말투는 검토 대기 초안이다. PET 일반 대사와 다른 Navi 미번역, 한글 이름 입력·기존save호환·전체게임/RTC/실기/오디오/인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 저장 제목·개수 단위 번역 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_save_surface_poc_v1.gba`.
상단 그래픽 `セーブ→저장`, 컵 개수 접미사 `コ→개`를 반영했다.
추가 텍스트1개·그래픽1문구, 누적1,113선택 텍스트 /15그래픽 /21선택·711미선택 archive. 전체 완역률 아님.
기존 저장36단위와 숫자·컵 아이콘·제어 명령을 유지했다. 제목은 원본256-byte 슬롯과 편집 영역 밖 픽셀을 보존한다.
새 ROM own-cold 정상 저장 진입에서 제목의 CPU 복사→OBJ VRAM/OAM→픽셀, `0개`의 글꼴→BG→픽셀 검증 통과.
실제64KB native save 갱신·완료 분기, 관련58테스트 통과. 다른 컵 수치/모든 Navi/영구 재로드는 이번 실행에서 검증하지 않았다.
SHA256 `303319827a54790b1b81100c37c6f1a8ebe67675dbe781cd51cd94d1033868a6`.
화면: `analysis/save_surface_poc_v1/save_surface.png`. 기록: `analysis/SAVE_SURFACE_POC_HANDOFF.md`.
한글 이름 입력/편집·기존save호환·전체게임·RTC·실기·오디오·인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 저장 항목명4개 번역 (2026-10-05)

실험용 ROM: `poc/output/exe45_ko_development_save_labels_poc_v1.gba`.
`タイム/チップ/カップ/クレジット` → `시간/칩/컵/크레딧`.
실행 조사 결과 이 네 항목은 그래픽 이미지가 아니라 6DA21C scripts10..13의 고정폭 문자열이었다.
기존32저장 단위와 숫자 표시 명령은 유지했다. 추가4개, 누적1,112선택 텍스트 /14기존 그래픽 /21선택·711미선택 archive. 전체 완역률 아님.
새 ROM own-cold→저장 진입에서 네 라벨의 lookup→big Hangul font→6칸 clear/stage→BG0 tilemap/palette→화면 ink/shadow 픽셀 검사 통과.
실제64KB native save 갱신과 완료 분기 확인. 관련54테스트 통과. 이전20payload와116save scripts(10..13외),원본106미선택save slots 보존.
SHA256 `08ead564156407b7d9c17e1579accf60a958b06410213607edfd68d8b038054e`.
화면: `analysis/save_labels_poc_v1/save_labels.png`. 기록: `analysis/SAVE_LABELS_POC_HANDOFF.md`.
이 버전에서 상단 `セーブ` 그래픽 제목과 컵 개수 접미사 `コ`는 미번역이었다. 후속 save_surface_poc_v1에 반영했다. 이름 입력/편집·기존save호환·전체게임·RTC·실기·오디오·인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 롤 저장 문구16개 번역 (2026-10-05)

실험용 개발 ROM: `poc/output/exe45_ko_development_roll_save_poc_v1.gba`.
저장 확인/덮어쓰기 확인/저장 중 전원 경고/완료/실패·재시도/잘못 변경된 데이터 경고를 번역했다.
록맨의 기존16저장 단위는 그대로 유지한다. 추가16개, 누적1,108선택 텍스트단위 /14그래픽 /21선택·711미선택 archive. 전체 완역률 아님.
새 ROM own-cold 정상경로에서 확인·덮어쓰기·저장 중 경고·완료의 실제 글꼴 CPU read→OBJ VRAM→화면 픽셀/범위 검사를 통과했다.
실제64KB 테스트 save 갱신 및 덮어쓰기 ‘아니요’의 파일 불변 확인. 실패/잘못된 데이터 경고는 정적 검증만 완료, 실제 오류를 유발하지 않았다.
이전20다른archive payload와이전115save scripts(20..24외),원본110미선택save slots 보존. 관련52테스트 통과.
SHA256 `7f121d4acb5c3ea2eb5c9379d0b855234f676699e7dd9a5f17ad7862343248c5`.
화면: `analysis/roll_save_poc_v1/save_pages.png`. 기록: `analysis/ROLL_SAVE_POC_HANDOFF.md`.
이 버전에서 저장 제목과 항목명이 원문이었다. 후속 조사에서 네 항목은 고정폭 문자열로 확인되어 save_labels_poc_v1에 번역했다. 상단 제목은 별도 그래픽이다.
한글 이름 입력·편집, 기존save 호환, 전체게임·RTC·오디오·실기·인간검토/배포 미완료.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전 실험: 기본 일정명2개 번역 (2026-10-05)

실험용 개발 ROM: `poc/output/exe45_ko_development_calendar_presets_poc_v1.gba`.
기본명 `ごはん/じゅく`를 `식사/학원`으로 번역했다. 기존 종류/작업메뉴 초안은 그대로 유지한다.
일본어만 세던 확인화면32F88의 문자 수 계산을 F9FC 한글 인식으로 수정했다.
누적1,092선택 텍스트단위 /14그래픽 문구 /21선택·711미선택 archive. 전체 완역률 아님.
실제 ROM lookup→9-byte copy→mono font/640-byte clear→확인 화면→32-byte 등록 레코드→같은 세션 일정 조회/normal font 픽셀 검사 통과.
원본 필드22bytes 안9bytes/E5-safe,251원본슬롯·직전20다른archive payload·기존253스크립트(62/63외) 보존.
487원본문자 호환성과11,172한글 음절의 실제 emitted-counter CPU 검사 통과. CPU bench는 실기 플레이/한글입력 지원 아님.
SHA256 `08d40db5a96aa995eb83ef72db998cbe831a8547c01da35f9d176918b4e07cbf`.
화면: `analysis/calendar_presets_poc_v1/preset_pages.png`.
기록: `analysis/CALENDAR_PRESETS_POC_HANDOFF.md`.
후속 `persistence_runtime.json`: 이 정확한ROM의 `학원` 기본명1건은native save→새프로세스 cold reload→32byte레코드 복원→1월1일 목록 한글 font/staging/VRAM/직접화면 확인까지 통과.
`식사` 영구재로드, 키보드/편집/다른이름소비자는 미완료. 이저장결과를후속ROM의실행증거로합산하지 않는다.
이 실험을 기존 빈도 baseline의 배포 승인이나 완전한 이름 입력 지원으로 승격하지 않는다.
functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전: 달력 빈도 그래픽5문구 번역 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_calendar_frequency_v1.gba`.
`1회만 / 매일 / 매주 / 매월 / 매년`을 기존 한글 픽셀 폰트로 번역했다.
실제 원본 압축블록63673C의 5개32×16 OBJ 문구이며, 문자열119..123 번역으로 대체하지 않았다.
누적1,090선택 텍스트단위 /14그래픽 문구 /21선택·711미선택 archive. 전체 완역률이 아니다.
원본 BIOS 압축해제 결과와 독립 디코더 일치, 새 ROM 정상5선택의 네이티브 압축해제→VRAM→OAM→전체문구 픽셀 검사 통과.
원래428-byte 슬롯 안344-byte 재압축; 직전 날짜 ROM 대비 해당 슬롯 외 모든 바이트 동일.
새 ROM own-cold부터 정상경로 수행, 기존9집중보고서와 새 빈도1보고서 통과. 관련47테스트(13.265초).
3독립 ROM 동일,419Python도구 drift=[],원본 ROM 보존.
SHA256 `43f7305a20ccc4acfff75815e9cde450fb22642a9c2012bd7d08ac97cd7da6ac`.
화면: `analysis/calendar_frequency_v1/selector_contact_sheet.png`.
기록: `analysis/CALENDAR_FREQUENCY_ROM_HANDOFF.md`, `analysis/calendar_frequency_v1/`.
공유4reference 전체의 로더/선택/등록·조회 검증, 기본이름·한글입력/저장/재로드·RTC·전체게임·인간검토·배포 미완료.
development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전: 달력 날짜 안내3리터럴 번역 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_calendar_date_v1.gba`.
‘오늘은 …월…일!! / 무엇을 할까?’를 번역하며 원본 월/일 숫자 삽입·제어 명령은 보존했다.
기존11개calendar 초안은 그대로 유지한다. 누적1,090선택단위 / 기존9그래픽 /21선택·711미선택 archive.
새 정상1월1일2화면의 RAM숫자/한글→CPU글꼴→OBJ픽셀·위치·무잔상 검사와 정상9집중보고서 통과.
247미선택슬롯·직전20다른payload 보존. 관련44테스트(11.910초),최종3독립ROM 동일,414도구 drift=[],원본 보존.
SHA256 `afc8a779872ad6e81db8a6b29f96af9423540ed14062e2940953afebd78bf7c1`.
화면: `poc/runtime/calendar-date-v1-date-font2/step_002.png`.
기록: `analysis/CALENDAR_DATE_ROM_HANDOFF.md`, `analysis/calendar_date_v1/`.
빈도 선택기는source119..123소비경로 미확정으로원문유지; `analysis/CALENDAR_FREQUENCY_SOURCE_BOUNDARY.md` 참조.
원본 기본이름·한글입력/저장/재로드·다른날짜/RTC·전체게임·인간검토·배포 미완료.
development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전: 일정 종류 목록5항목 번역 (2026-10-04)

최종 개발 ROM: `poc/output/exe45_ko_development_calendar_types_v2.gba`.
‘TV 방송 / 친구와 약속 / 식사 / 학원 / 기타’를 번역했다. 새 리터럴1단위, 기존27셀 구간·선택 순서 유지.
누적1,087선택단위 / 기존9그래픽 /21선택·711미선택 archive. 전체 완역률이 아니다.
실제 mono font 공급·1728-byte staging→OBJ VRAM→화면 픽셀, 첫4항목과 스크롤된기타 검증 통과.
화살표에 가려진 글자는 전체VRAM 검증에 포함하되 source/current arrow screenshot RGB 동일성은 주장하지 않는다.
정상8집중보고서 통과. 기존20다른번역 payload/253원본슬롯/15root/그래픽 보존 확인.
최종42테스트(18.121초),v2 3독립 ROM 동일,Python409도구 drift=[],원본 보존.
v2는 명세 font profile 정정본이며, 정상 실행v1과 전체ROM 바이트 동일성을 확인했다.
SHA256 `903858514f23de53ce5ce5def2c07527ff3461d216e3fa6a06d47ef92eb6e883`.
기록: `analysis/CALENDAR_TYPES_ROM_HANDOFF.md`, `analysis/calendar_types_v1/`.
화면: `analysis/calendar_types_v1/types_pages.png`.
기본 일정명·빈도 메뉴·한글 입력/저장/재로드·RTC·전체게임 미완료.
development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전: 일정 내용·약속 상대 안내 2단위 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_calendar_content_v1.gba`.
‘어떤 내용이야?’, ‘누구와 한 약속이야?’ 추가. 직전9개 안내·선택지 초안은 그대로 유지한다.
누적1,086선택단위 / 기존9그래픽 /21선택·711미선택 archive. 전체 완역률이 아니다.
65F11C content-promise-v1 variant 선택, 나머지248슬롯·입력/저장 자료 보존.
새 ROM 정상7집중보고서, 등록/약속 안내7화면·11단위 글꼴→픽셀·위치·무잔상 검사 통과.
관련39테스트(8.730초), 3독립 ROM 동일, Python405도구 drift=[], 원본 보존 확인.
SHA256 `1153e424057effbe2b728369c56c73df6270b3ebc03157aa09cdfb3a3ef4dbe9`.
기록: `analysis/ROLL_CALENDAR_CONTENT_ROM_HANDOFF.md`, `analysis/roll_calendar_content_v1/`.
화면: `analysis/roll_calendar_content_v1/calendar_dialogue_pages.png`.
기본 일정명·종류/빈도 메뉴·한글 입력·저장/재로드·RTC·전체게임 미완료.
development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전: 롤 일정 등록 안내·선택지 9단위 번역 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_calendar_dialogue_v1.gba`.
날짜 선택 질문, 일정/기념일, 시작 시각·종류 질문, 최종 확인·예/아니오를 번역했다.
누적 1,084선택단위 / 기존9그래픽 /21선택·711미선택 archive. 전체 완역률이 아니다.
65F11C의 5스크립트·9리터럴만 변경, 나머지250슬롯·제어·입력/저장 구조 보존.
새 ROM 정상7집중보고서 통과, 새 안내5화면·9단위 CPU 글꼴→화면 픽셀·선택 위치·무잔상 확인.
관련37테스트 최종 통과(15.052초). 재현/원본/도구 정본은 `analysis/roll_calendar_dialogue_v1/final_identity_audit.json`.
SHA256 `36dd3af596c01f5ce251c3527b3e8b475d0445a4c3a87a555d1c282fc61c576a`.
화면: `analysis/roll_calendar_dialogue_v1/calendar_dialogue_pages.png`.
기록: `analysis/ROLL_CALENDAR_DIALOGUE_ROM_HANDOFF.md`.
기본일정명·빈도/종류 메뉴·다른 달력 대사·한글 입력·저장/재로드·RTC·전체게임 검증은 남았다.
development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전: 달력 ‘등록 / 일정 보기 / 삭제’ 메뉴 번역 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_calendar_menu_v1.gba`.
6368E8의 메뉴0 한 리터럴(3개 작업명)을 번역, 8칸씩3구역·총24셀 배치 유지.
누적1,075선택단위 / 기존9그래픽 /20선택·712미선택 archive. 전체 완역률이 아니다.
15root 포인터 검증, 나머지254스크립트·키보드·기본 일정명·저장 대사 원문 보존.
새 ROM 정상6집중보고서: 소개/PET/기본대사/장비/등록일정조회/달력메뉴 통과.
메뉴 원본→한글 디코드→1536바이트 staging→OBJ VRAM→화면 픽셀, 원본 좌표·색·잔상 검사 통과.
정상 메뉴 이동에서 ‘일정 보기’와 ‘삭제’ 강조 표시를 직접 확인; 실제 일정 삭제는 하지 않았다.
관련34테스트 통과(11.702초). main/repro/current_repro2 3독립 빌드 동일, Python398도구 drift 없음.
SHA256 `db282269f75b1c2f91d512cf490c25495b58881cbcaf8fbe2419a78a618d1b96`.
화면: `poc/runtime/calendar-menu-v1-calendar/step_002.png`.
기록: `analysis/CALENDAR_MENU_ROM_HANDOFF.md`, `analysis/calendar_menu_v1/`.
기본 ‘ごはん’/‘じゅく’, 달력 대사·다른 메뉴·한글 입력·저장/재로드·RTC/자연 알림·전체게임 검증 미완료.
development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 이전: 롤 식사·학원 알림 3문장 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_schedule_alarm_v1.gba`.
‘밥 먹을 시간이야!’, 학원 준비·지각 안내, 추가 일정 연결 문구를 번역했다.
누적1,074선택단위 / 기존9그래픽 /19선택·713미선택 archive. 전체 완역률이 아니다.
660D90의3리터럴만 변경, 다른25슬롯·이름/입력 자료·제어 명령 보존.
새 ROM 정상5집중보고서(소개/PET/기본대사/장비/등록일정 조회) 통과.
새 알림3문장은 격리된3렌더러 진단 경로·6페이지에서 글꼴 CPU→OBJ→화면 픽셀·줄 위치·무잔상·keyWait 검증.
자연 RTC 알림 발생·식사/학원 이벤트 진행을 검증한 것은 아니다.
관련26테스트 통과(35.483초); 역사적 캡처 재검사를 새 ROM 실행 증거로 합산하지 않는다.
이전18번역 payload 동일, 3최종 독립 빌드 동일, Python394도구 drift 없음.
SHA256 `6e59764c4fc951eb0b1c3f07c739ed19b6e06fd99d228856f0c213f4ac01f634`.
기록: `analysis/ROLL_SCHEDULE_ALARM_ROM_HANDOFF.md`, `analysis/roll_schedule_alarm_v1/`.
화면: `analysis/roll_schedule_alarm_v1/alarm_pages.png`.
기본 일정명 `ごはん`/`じゅく` 및 메뉴는 아직 미번역. 원본 이름 복사/조회 경계는 `analysis/SCHEDULE_PRESET_SOURCE_BOUNDARY.md`에 기록했다.
development-draft; NON-DISTRIBUTION; 문구/시각 needs_review; release_eligible=false.
한글 입력·저장/재시작·RTC 지속성·실제 오디오·하드웨어·전체게임·배포 검증 미완료.

## 이전: 등록 일정 시각의 ‘부터’ 번역·정상 조회 검증 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_schedule_time_v1.gba`.
시각 뒤 `から`를 `부터`로 한글화, 이전5개 일정 안내 문구 유지.
누적1,071선택단위 / 기존9그래픽 /18선택·714미선택 archive. 전체 완역률이 아니다.
실제 정상 입력으로 달력에서 02:00 AM 1회 일정 등록→PET L조회→목록→복귀를 새 ROM에서 확인했다.
시각·AM·일정명 RAM, 한글/원본 글꼴 CPU→OBJ→화면 픽셀, 106px 첫 행·55px 이름 행, 무잔상·확인키 검증 통과.
정상5집중보고서 /관련20테스트(5.550초) 통과. 별도4alias 캡처를 정상 경로로 합산하지 않는다.
기본 일정명 `ごはん`은 일본어 유지, 다른 시각/AMPM/이름·다중 일정·저장/RTC 지속성은 아직 미검증이다.
이전17개 별도 archive payload 동일. 3독립 빌드 동일, Python389도구 drift 없음.
SHA256 `35d20055bbb740d8b4468ea399b998d843827fca66e0d66c7825af10436277c6`.
기록: `analysis/ROLL_SCHEDULE_TIME_ROM_HANDOFF.md`, `analysis/roll_schedule_time_v1/`.
화면: `poc/runtime/roll-schedule-time-v1-list/step_005.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.
한글 입력·실제 오디오·하드웨어·전체게임·배포 검증 미완료.

## 이전: 롤 일정 안내 5문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_schedule_v1.gba`.
일정 알림 시작·마무리, 오늘 등록된 일정 소개·없음 안내·목록 마무리를 추가했다.
누적 1,070 선택 텍스트 단위 / 기존9그래픽, 18선택 / 714미선택 아카이브.
661754의5리터럴과4스크립트를 번역했고, 동적 일정명·시각을 삽입하는 script2/11은 원문 바이트 그대로 보존했다.
새 ROM 정상4보고서+일정진단1보고서 통과. 격리된4경로·5페이지의 글꼴 CPU읽기→OBJ→화면 픽셀, 확인키, 복귀·무잔상 검증과 직접 시각 검토 완료.
실제 일정 등록·알림 발생·등록된 일정 목록/AMPM의 정상 소비 경로는 아직 미검증이다.
이전17개 번역 payload 동일, 기존 ‘빅해머1’ hook 유지·32합성 CPU 벡터 통과.
관련21자동 테스트 통과(7.051초). 직전207개 전체 테스트를 이번 턴에 재실행한 것은 아니다.
3독립 빌드 동일, Python384도구 해시 drift 없음.
SHA256 `c1838a5e877e6a726733a8e9797cc9487fa065312627b9131650c9df80c112ed`.
기록: `analysis/ROLL_SCHEDULE_ROM_HANDOFF.md`, `analysis/roll_schedule_v1/`.
화면: `analysis/roll_schedule_v1/schedule_pages.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.
전체 완역·한글 입력·저장·RTC·실제 오디오·하드웨어·배포 검증 미완료.

## 이전: 롤 대회 결과·참가 안내 14문구 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_competition_v2.gba`.
패배 후 격려, 우승 축하, 참가 미등록 안내, 대회 직전 응원을 추가했다.
누적 1,065 선택 텍스트 단위 / 기존 9그래픽 유지. 전체 게임 완료율이 아니다.
6615A8의 7스크립트·14리터럴, 나머지 18빈 슬롯과 모든 제어 명령을 보존했다.
이전 16개 번역 payload 동일, ‘빅해머1’ 선택 hook 유지·32합성 CPU 벡터 통과.
새 ROM 정상 롤 선택·소개·PET 메뉴·기본 대사·장비 회귀 검증 통과.
대회 대사는 7개 격리 진단 경로 / 10페이지에서 이름 RAM·글꼴·OBJ·화면 픽셀·무잔상 확인.
실제 대회 참가·승패·플래그 분기의 정상 진행 검증은 아직 남아 있다.
3최종 독립 빌드 동일, 380 Python 도구 해시 드리프트 없음.
프로젝트 자동 회귀 테스트 207개 통과(518.258초). 과거 캡처 재검사는 새 ROM 정상 실행 증거로 전이하지 않는다.
SHA256 `9d99325c9cd23536a8914b63d6a9cf8d1af379c9f3eec1ec9c61114a23814b35`.
기록: `analysis/ROLL_COMPETITION_ROM_HANDOFF.md`, `analysis/roll_competition_v1/`.
화면: `analysis/roll_competition_v1/competition_pages.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.
한글 이름 입력·저장·RTC·실제 오디오·전체 게임·하드웨어·배포 검증 미완료.

## 이전: 롤 대화 삽입 칩 이름 ‘빅해머1’ 한글화 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_dialogue_chip_name_v1.gba`.
롤13의일본어삽입칩이름을기존번역 ‘빅해머1’로연결,‘빅해머1 / 찾으러 가자!’ 화면검증.
기존이름문구재사용이므로누적1,051선택단위/9그래픽 유지,번역수중복가산없음.
공유이름표/9개root pair/원본풀변경없음.호출stream·정상문맥·원본104이름 3중조건의선택hook.
원본128바이트copy/RAM/폰트/화면1776픽셀/행69·79px/빈본문3784픽셀 검증통과.
전체레지스터·SP·LR 실제경계보존,32합성CPU벡터에서원본CPSR/일반호출fallback 동일.
정상5+이름진단1 집중6보고서,관련18자동테스트 통과(0.563초).
별도재진입캡처에서alias1 유지/다음native0 기본대사·닉네임·무잔상 화면직접검토.
진단은정상칩획득/퀘스트진행검증이아님.다른대화칩이름/다른정상분기는미번역·미검증.
직전ROM 공통범위에서설치12바이트만변경,ROM끝196바이트추가,기존대사·폰트·그래픽바이트동일.
원본/이전/실패자료보존,최종3독립빌드 동일,377 Python도구드리프트없음.
SHA256 `7bfeb8d1642e77dd1fad4674898059dbf5682cf8c5e30d2fcde4675c0a636ba8`.
기록: `analysis/DIALOGUE_CHIP_NAME_ROM_HANDOFF.md`, `analysis/dialogue_chip_name_v1/`.
화면: `poc/runtime/dialogue-chip-name-v1-name-script13/step_003.png`.
development-draft; NON-DISTRIBUTION,문구/시각 needs_review,release_eligible=false.
한글이름입력/저장/RTC/실제오디오/전체게임/하드웨어/배포검증미완료.

## 이전: 롤 칩 찾기 대사1문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_chipquest_v1.gba`.
누적1,051선택 텍스트 단위/기존9그래픽 유지.전체 게임 완료율이 아니다.
664E28:13:1을 ‘」 / 찾으러 가자!’로수동번역,첫줄원본 칩이름/따옴표 보존.
printChip buffer0/chip104와원본 이름RAM삽입 유지.본문 한글화이며삽입된일본어칩이름은미번역으로남음.
동적삽입폭 모델 빌드검사: 원본이름88px+따옴표22px=110px,둘째행79px.
새ROM 정상5+칩대사 진단1 집중6보고서 통과.기존23진단은이번ROM에서재캡처하지않음.
칩대사17글자/2268픽셀대조·빈본문3292픽셀·확인키뒤복귀 검증,직접시각검토.
기존37회귀테스트(163.963초)+신규3테스트(0.587초) 통과.
기존29문구/다른254PET 스크립트·다른15번역 payload/PET그래픽 동일.
3최종독립빌드 동일,370 Python 도구 드리프트없음.보고서빈이미지오류/수정증거보존.
SHA256 `aff27be5b0bb114a6b08f9db9337f38c427c43ae5e719457a93eda35e7449eb9`.
기록: `analysis/ROLL_CHIPQUEST_ROM_HANDOFF.md`, `analysis/roll_chipquest_v1/`.
화면: `poc/runtime/roll-chipquest-v1-script13/step_003.png`.
development-draft; NON-DISTRIBUTION,문구/시각 needs_review,release_eligible=false.
정상칩획득·진행/삽입이름한글화/다른메일13분기/저장·RTC·오디오·전체게임·배포검증미완료.

## 이전: 롤 메일 도착 알림14문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_mail_alert_v1.gba`.
누적1,050선택 텍스트 단위/기존9그래픽 유지.전체 게임 완료율이 아니다.
661060의14개 메일 도착 본문을 ‘메일이 왔어!!’로 수동 번역,초기14개 `!!` 보존.
닉네임1/2/3의첫줄 쉼표·알림음155 두 번·96프레임 대기 두 번·메일/플래그 명령 유지.
새ROM 정상script1 도착 경로에서 초기알림→닉네임/본문→확인키/PET 복귀 검증.
폰트 CPU읽기→OBJ VRAM→화면픽셀·행/폭·대기·빈본문/잔상 검사 통과,직접 시각 검토.
정상5+진단23 집중28보고서 통과.기존34회귀 테스트(240.273초)+신규3테스트(0.977초) 통과.
다른13메일 이벤트 entry는 정적 구조/폰트/폭만 검증,개별 정상분기 런타임 미검증.
16선택/716미선택 아카이브,661060의다른241슬롯과 초기14리터럴 보호.
직전15개 번역 payload/PET 그래픽 동일,원본·이전·실패 자료 보존.
3독립 빌드 동일,365 Python 도구 해시 드리프트 없음.
SHA256 `c21f96e1298edca233ed6a88e3f37f51dfaa6a022699743f6e73fc566b0aa564`.
기록: `analysis/ROLL_MAIL_ALERT_ROM_HANDOFF.md`, `analysis/roll_mail_alert_v1/`.
화면: `poc/runtime/roll-mail-alert-v1-arrival/step_008.png`.
development-draft; NON-DISTRIBUTION,문구/시각 needs_review,release_eligible=false.
한글 이름 입력/저장/RTC 지속성·실제 오디오·전체 게임·배포 검증 미완료.

## 이전: 롤 PET 평일 대회 안내5문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_weekday_v1.gba`.
누적1,036선택 텍스트 단위/기존9그래픽 유지.전체 게임 완료율이 아니다.
참가 신청 장소·닉네임 참가 제안·주말 대회 안내5문구 추가,기존24단위 정확히 유지.
게임 날짜 입력 UI로월요일을설정,평일 정상5구간 부모/입력/캡처검증 통과.
정상4+진단23 집중27보고서 및 관련34자동 테스트 통과(215.204초).
새5페이지 폰트/VRAM/화면 픽셀/행·폭/대기/잔상 검사 통과,직접 시각 검토.
28의네이티브닉네임 ああくん(44px)·쉼표11px 보존,다음페이지지우기검증.
원본 일요일/토요일 분기·창·페이지·닉네임 명령 유지,진단alias는 ROM미포함.
정상 대회 참가·접수·해당entry 선택/한글 이름 입력·저장/RTC 날짜 지속성은 미검증.
717미선택 아카이브·다른231슬롯 보존,해당 아카이브의 동적칩13의2리터럴 등 미번역 남음.
별도661060 script1메일도착알림을평일초기화에서관측,다음후보로기록.
원본/이전/실패 자료 보존,3독립 빌드 동일,361 Python 도구 해시 드리프트 없음.
SHA256 `bdd871b59d679c636fc1faa75bc1ae4ca9caffbb087cbdef8336052714f16868`.
기록: `analysis/ROLL_PET_WEEKDAY_ROM_HANDOFF.md`, `analysis/roll_pet_weekday_v1/`.
화면: `analysis/roll_pet_weekday_v1/weekday_diagnostic_pages.png`.
development-draft; NON-DISTRIBUTION,문구/시각 needs_review,release_eligible=false.

## 이전: 롤 PET 우라인터넷 안내2문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_undernet_v1.gba`.
누적1,031선택 텍스트 단위/기존9그래픽 유지.전체 게임 완료율이 아니다.
우라인터넷 이동과 목표 내비의 관 표식 안내2문구 추가,기존22단위 정확히 유지.
정상4+진단20 집중24보고서 및 관련31자동 테스트 통과(191.060초).
새2페이지 폰트/VRAM/화면 픽셀/행·폭/대기/잔상 검사 통과,직접 시각 검토.
원본 창·페이지 전환·대기 명령과 기존 닉네임 유지,진단alias는 ROM미포함.
정상 우라인터넷 진입·목표 내비 조우·진행 조건·해당entry 선택은 미검증.
717미선택 아카이브·다른234슬롯 보존,해당 아카이브7리터럴 등 미번역 남음.
원본/이전 자료 보존,3독립 빌드 동일,357 Python 도구 해시 드리프트 없음.
SHA256 `3812dae6e9c32830520e72de0c2a1ef98ac5e2994254cd5702af2ea2446524a9`.
기록: `analysis/ROLL_PET_UNDERNET_ROM_HANDOFF.md`, `analysis/roll_pet_undernet_v1/`.
화면: `analysis/roll_pet_undernet_v1/undernet_diagnostic_pages.png`.
development-draft; NON-DISTRIBUTION,문구/시각 needs_review,release_eligible=false.

## 이전: 롤 PET 예선·새 메일 안내2문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_mail_v1.gba`.
누적1,029선택 텍스트 단위/기존9그래픽 유지.전체 게임 완료율이 아니다.
오피셜 토너먼트 예선·새 메일 읽기 안내2문구 추가,기존20단위 정확히 유지.
정상4+진단19 집중23보고서 및 관련29자동 테스트 통과(189.492초).
새2화면 폰트/VRAM/화면 픽셀/행·폭/대기/잔상 검사 통과,직접 시각 검토.
네이티브 닉네임 ああくん(44px)과 뒤 쉼표11px 보존·재표시 검증.
원본 플래그9430 분기·닉네임 명령 유지,진단alias는 ROM미포함.
정상 예선 참가·메일 수신/열람·한글 이름 입력/저장 지원은 미검증.
717미선택 아카이브·다른235슬롯 보존,해당 아카이브9리터럴 등 미번역 남음.
원본/이전 자료 보존,3독립 빌드 동일,353 Python 도구 해시 드리프트 없음.
SHA256 `6146c179e0d5660b4248f2816544d78d169d33e733346b164ced39769af23a5e`.
기록: `analysis/ROLL_PET_MAIL_ROM_HANDOFF.md`, `analysis/roll_pet_mail_v1/`.
화면: `analysis/roll_pet_mail_v1/mail_diagnostic_pages.png`.
development-draft; NON-DISTRIBUTION,문구/시각 needs_review,release_eligible=false.

## 이전: 롤 PET 인터넷 지역 사건 안내6문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_events_v1.gba`.
누적1,027선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
인터넷3/5/7/9/10/12 사건 안내6문구 추가,기존14단위 정확히 유지.
정상4+진단17 집중21보고서 및 관련27자동 테스트 통과(38.644초).
새6화면 폰트/VRAM/화면 픽셀/행·폭/대기/잔상 검사 통과,직접 시각 검토.
원본 플래그9424..9429의true→33/false→continue 분기 보존,진행 상태 수정 없음.
진단 alias는 ROM에 미포함.정상 사건 진행/완료·메일 분기·해당entry 선택은 미검증.
717미선택 아카이브·다른237슬롯 보존,해당 아카이브11리터럴 등 미번역 남음.
원본/이전 자료 보존,3독립 빌드 동일,349 Python 도구 해시 드리프트 없음.
SHA256 `c2a6806e64e5cd39e5e0bdf1fa7b44d054b81364ddedec27ab475c5ab5c388d2`.
기록: `analysis/ROLL_PET_EVENTS_ROM_HANDOFF.md`, `analysis/roll_pet_events_v1/`.
화면: `analysis/roll_pet_events_v1/events_diagnostic_pages.png`.
development-draft; NON-DISTRIBUTION,문구/시각 needs_review,release_eligible=false.

## 이전: 롤 PET 오피셜 토너먼트 안내3문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_tournament_v1.gba`.
누적1,021선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
대회 열의·다음 주 참가 신청 권유3문구/3페이지 추가,기존11단위 보존.
정상4+진단11 집중 검증15보고서 및 관련25자동 테스트 통과(30.232초).
새3페이지 폰트/VRAM/화면 픽셀/행·폭/대기/페이지 전환 잔상 검사 통과,직접 시각 검토.
진단 alias는 ROM미포함.정상 요일별 분기·대회 참가·경기는 미검증.
717미선택 아카이브·다른243슬롯 보존.해당 아카이브17리터럴 등 미번역 남음.
원본/이전 자료 보존,독립/최종재빌드2 바이트 동일,345 Python 도구 드리프트 없음.
SHA256 `57bb69a6d2ca1d2888eb57a808e76bb10d5444459e0ace787f23d312a54a8d1d`.
기록: `analysis/ROLL_PET_TOURNAMENT_ROM_HANDOFF.md`, `analysis/roll_pet_tournament_v1/`.
화면: `analysis/roll_pet_tournament_v1/tournament_diagnostic_pages.png`.
검사기 마지막 한글 바이트 경계 오류 수정·회귀 검증,ROM 내용 변경 없음.
development-draft; NON-DISTRIBUTION,문구/시각 needs_review,release_eligible=false.

## 이전: 롤 PET 마이너스 키 안내3문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_keyquest_v1.gba`.
누적1,018선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
키 회수·다른 내비의 소지 추측·인터넷9 이동 안내3문구 추가, 기존8단위 보존.
정상4+진단9 집중 검증13보고서 및 관련 자동 테스트23개 통과(23.901초).
새3화면 폰트/VRAM/화면 픽셀/행·폭/대기/잔상 검사 통과, 직접 시각 검토.
진단 선택은 ROM에 미포함. 정상 퀘스트 선택·획득·실제 이동은 미검증.
717미선택 아카이브·다른245슬롯 보존. 해당 아카이브20리터럴 등 미번역 남음.
원본/이전 자료 보존,3독립 빌드 동일,341 Python 도구 해시 드리프트 없음.
SHA256 `780366ecee25a884e89b7f2ffae5ca208ab163ebb07e703ef9e6a547d0733aa4`.
기록: `analysis/ROLL_PET_KEYQUEST_ROM_HANDOFF.md`, `analysis/roll_pet_keyquest_v1/`.
화면: `analysis/roll_pet_keyquest_v1/keyquest_diagnostic_pages.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 PET 사건 후 대화·탐색 권유3문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_incident_v1.gba`.
누적1,015선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
사건 후 대화2페이지와 추가 탐색 권유1페이지 번역, 기존 라이선스/탐색5단위 보존.
새3페이지 진단 폰트/VRAM/화면 픽셀/행·폭/대기 경계/페이지 전환 잔상 검사 통과.
정상4+진단6 집중 검증10보고서, 관련 자동 테스트21개 통과(18.415초).
진단 선택은 ROM에 미포함. 사건·종료 분기의 정상 진행/전투 승리는 미검증.
717미선택 아카이브·다른248슬롯·기존 그래픽 보존. 해당 아카이브23리터럴 등 미번역 남음.
원본/이전 자료 보존, 독립/최종 도구 재빌드 동일,337도구 해시 드리프트 없음.
SHA256 `6a2d3efb2d7cb14680f95d44fbf87a5a1a8cd50a0618d5adbbf6d2c7f2da2cb1`.
기록: `analysis/ROLL_PET_INCIDENT_ROM_HANDOFF.md`, `analysis/roll_pet_incident_v1/`.
화면: `analysis/roll_pet_incident_v1/incident_diagnostic_pages.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 PET 견습 라이선스 안내4문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_license_v1.gba`.
누적1,012선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
시험 도전·응원·라이선스 수령·시험 후 휴식 안내4문구 추가, 기존 탐색 안내 보존.
4문구는 별도 읽기 alias 진단 화면에서 폰트/VRAM/화면 픽셀/행·폭/잔상 검사 통과.
진단 선택은 ROM에 미포함. 진행 조건별 정상 선택·획득·시험 완료는 미검증.
정상4+진단4 집중 검증8보고서, 관련 자동 테스트19개 통과(13.986초).
직전15전체 회귀/181전체 테스트를 이번 ROM 결과로 전용하지 않는다.
717미선택 아카이브·다른250슬롯·기존 번역과 그래픽 보존.26리터럴 등 미번역 남음.
독립/최종 도구 재빌드 바이트 동일,333도구 해시 드리프트 없음. 원본/이전 자료 보존.
SHA256 `46dcd61b1e9939c24a2325f67c4bdee7e5e9a98e9aab42d712b2d792a1664263`.
기록: `analysis/ROLL_PET_LICENSE_ROM_HANDOFF.md`, `analysis/roll_pet_license_v1/`.
화면: `analysis/roll_pet_license_v1/license_diagnostic_pages.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 PET 인터넷 탐색 안내1문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_pet_talk_v2.gba`.
누적1,008선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
정상 PET R 대화의 ‘인터넷을 더 / 탐색해 보자!’를 번역했고 닉네임·쉼표·줄바꿈 유지.
새664E28의 다른254슬롯(빈 슬롯 포함),717미선택 아카이브와 기존 번역 입력 보존.
새 ROM own cold-chain, 신규 대화 폰트/VRAM/화면 픽셀 및 기존 회귀15보고서 통과.
독립/최종 도구 재빌드 바이트 동일, 원본/이전 작업 보존,329도구 해시 드리프트 없음.
전체 자동 테스트181개 통과(591.758초). 새 아카이브30리터럴, 다른 미번역과 사용자 답변 입력·저장 미검증.
SHA256 `35d871005b0a50b9f8398d5b3dda95e0ee413728b31eac6b8bfb8504c3e4b7a1`.
기록: `analysis/ROLL_PET_TALK_ROM_HANDOFF.md`, `analysis/roll_pet_talk_v1/`.
화면: `poc/runtime/roll-pet-talk-v1-talk/step_003.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 잘하는 과목·어려운 과목 대화5문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_subjects_v1.gba`.
누적1,007선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
기존 형제자매/음식36단위 유지, 과목27/29의5문구 추가. 다른86스크립트 원본 바이트 동일.
새 own-ROM 정상 경로에서5페이지·닉네임·쉼표·선행 줄바꿈·폰트/VRAM/화면·잔상 검사 통과.
실제 과목 답변 입력/확정/저장은 미검증.14동일 ROM 런타임 보고서와 전체 자동 테스트179개 통과(125.255초).
독립/최종 도구 재빌드 바이트 동일, 원본/이전 작업 보존, 도구325해시 드리프트 없음.
SHA256 `bfc695dfeecc6de17ce82ad2b55c5219bec42e6d7ca8bc2179f12612842e0723`.
기록: `analysis/ROLL_SUBJECTS_ROM_HANDOFF.md`, `analysis/roll_subjects_v1/`.
화면: 위 분석 폴더의 `strong/subject_pages.png`, `weak/subject_pages.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 좋아하는 음식 대화4문구 추가 (2026-10-04)

개발 ROM: `poc/output/exe45_ko_development_roll_food_v1.gba`.
누적1,002선택 텍스트 단위/기존9그래픽 유지. 전체 게임 완료율이 아니다.
기존 형제자매32단위 유지, 음식11의4문구 추가. 다른88스크립트 원본 바이트 동일.
새 own-ROM 정상 진입으로 음식3페이지·두 번째 행 닉네임·쉼표·폰트/VRAM/화면·잔상 검사 통과.
음식 답변 입력/확정/저장은 미검증.12동일 ROM 런타임 보고서와 전체 자동 테스트177개 통과(117.316초).
독립/최종 도구 재빌드 바이트 동일, 원본/이전 작업 보존, 도구322해시 드리프트 없음.
SHA256 `986450bc2c3e6aef7688428863e4a0ca478c2ce9b5b60f6628917caecc283bd9`.
기록: `analysis/ROLL_FOOD_ROM_HANDOFF.md`, `analysis/roll_food_v1/`.
화면: `analysis/roll_food_v1/food_pages.png`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 귀환 후 형·오빠/남동생 질문16문구 추가 (2026-10-04)

현재 개발 ROM은 `poc/output/exe45_ko_development_roll_family_siblings_v1.gba`다.
누적998텍스트 단위와 기존9그래픽 유지. 전체 게임 완료율이 아니다.
형·오빠1/2와 남동생3/4의16문구 추가, 기존 자매5/6/7/8의16문구 그대로 유지.
플레이어 성별을 가정하지 않도록 ‘형이나 오빠 있어?’로 번역했다.
읽기 전용 정상 입력 시점 조사에서1/3 진입 확인 후 새 own-ROM cold-chain에서 재현했다.
네 형제자매 분기32문구·닉네임·선택 좌우·두 응답 화면 검증.
동적 이름/제어명령 보존, 다른89스크립트 바이트 동일. 실제 이름 입력·저장은 미검증.
원본/이전 작업 보존, 독립/최종 도구 재빌드 바이트 동일, 도구318해시 드리프트 없음.
인사/PET/운세/플러그아웃/귀환/장비/폴더/무기/‘통신’ 그래픽 동일 ROM 회귀 통과.
SHA256 `47f8e3ec2097f9b72a14ce7edf116d06d8efa8e31b82f14893b81e0d5ddfeec3`.
기록: `analysis/ROLL_FAMILY_SIBLINGS_ROM_HANDOFF.md`, `analysis/roll_family_siblings_v1/`.
화면: `older-brother/family_pages.png`, `younger-brother/family_pages.png`(위 분석 폴더 아래).
자동 테스트175개 통과(104.117초): `analysis/roll_family_siblings_v1/test_summary.txt`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 귀환 후 누나·언니 질문8문구 추가 (2026-10-04)

이전 개발 ROM은 `poc/output/exe45_ko_development_roll_family_sisters_v1.gba`다.
누적982텍스트 단위와 기존9그래픽 유지. 전체 게임 완료율이 아니다.
누나·언니 질문5/6의8문구 추가, 기존 여동생7/8의8문구 source/wording/state 그대로 유지.
새 ROM 정상 경로에서 두 자매 분기의16문구·닉네임·선택 좌우·두 응답 화면 검증.
플레이어 성별을 가정하지 않도록 ‘누나나 언니 있어?’로 번역했다.
동적 이름/제어명령 보존, 다른93스크립트 바이트 동일. 실제 이름 입력·저장은 미검증.
원본/이전 작업 보존, 독립/최종 도구 재빌드 바이트 동일, 도구314해시 드리프트 없음.
인사/PET/운세/플러그아웃/귀환/장비/폴더/무기/‘통신’ 그래픽 동일 ROM 회귀 통과.
SHA256 `b7227159ae498da3ac3da7e6620d1582170086c20d7e76d778aa7efd8353bb67`.
기록: `analysis/ROLL_FAMILY_SISTERS_ROM_HANDOFF.md`, `analysis/roll_family_sisters_v1/older/family_runtime.json`.
화면: `analysis/roll_family_sisters_v1/older/family_pages.png`, `analysis/roll_family_sisters_v1/younger/family_pages.png`.
자동 테스트173개 통과(207.273초): `analysis/roll_family_sisters_v1/test_summary.txt`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 귀환 후 여동생 질문8문구 추가 (2026-10-04)

이전 개발 ROM은 `poc/output/exe45_ko_development_roll_family_sister_v1.gba`다.
누적974텍스트 단위와 기존9그래픽 유지. 전체 게임 완료율이 아니다.
귀환 후 인터넷 이야기/여동생 질문/있어·없어/이름 질문8문구를 추가했다.
새 ROM의 정상 경로에서8문구, 닉네임, 선택 좌우 이동과 두 분기 화면을 검증했다.
‘있어’는 이름 질문의 대기 지점까지만 검사했으며 실제 이름 입력·저장은 하지 않았다.
원문 topic 접미사 ‘は、’는 정확히 쉼표 ‘、’로 번역해 닉네임 행의 폭을 줄였다.
선택 페이지는 질문 페이지와 분리된 원문 구조를 유지했다.
다른95스크립트 원본 바이트 그대로, 선행 줄바꿈29의 조립 손실도 검사기가 감지해 수정했다.
이전966번역 입력/원본/이전 결과 보존, 독립/최종 도구 재빌드 바이트 동일.
기존 인사/PET/운세/플러그아웃/귀환/장비/폴더/무기/‘통신’ 그래픽 회귀 포함.
SHA256 `c15aa3d4c421719e7efb5fa47e73ee8741a797bcc8f5313e477b721699822c14`.
기록: `analysis/ROLL_FAMILY_SISTER_ROM_HANDOFF.md`, `analysis/roll_family_sister_v1/family_runtime.json`.
자동 테스트171개 통과(81.890초): `analysis/roll_family_sister_v1/test_summary.txt`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 플러그아웃 확인·응답4문구 추가 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_roll_plugout_v1.gba`다.
누적966텍스트 단위와 기존9그래픽 유지. 전체 게임 완료율이 아니다.
공용778338 풀에서 롤 확인6/응답26의4문구만 번역, 다른44스크립트 보존.
닉네임/확인창/기본 ‘아니요’/B 취소/좌우 이동/‘예’ 응답과 귀환 연결을
새 ROM의 정상 cold-chain에서 검증했다. 이전 번역962단위 입력 해시 동일.
일반 대사창 시작52,110과 PET창92,110을 구분해 폰트/VRAM/화면을 검사했다.
기존 인사/PET/운세/귀환/장비/폴더/무기/공격력·숫자/‘통신’ 그래픽 회귀 포함.
독립/최종 도구 재빌드 바이트 동일, 원본/이전 작업 보존.
SHA256 `dddc3a3d5c4f6c73f5f1e54be62ace5b919f839528b5caa3408482f9c9a85163`.
기록: `analysis/ROLL_PLUGOUT_ROM_HANDOFF.md`, `analysis/roll_plugout_v1/plugout_runtime.json`.
자동 테스트166개 통과(188.154초): `analysis/roll_plugout_v1/test_summary.txt`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review, release_eligible=false.

## 이전: 롤 귀환·패배 대사4개 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_roll_return_v1.gba`다.
누적962텍스트 단위와 기존9그래픽 유지. 전체 게임 완료율이 아니다.
귀환2페이지는 새 ROM 자체의 정상 cold-chain/플러그아웃 경로에서 검증했다.
닉네임 RAM 문자열→원본 폰트→OBJ VRAM→화면 픽셀까지 일치하고 잔상 없음.
패배2페이지는 격리된 table-read 진단으로만 검증했으며 실제 전투 패배 증거가 아니다.
기존 인사/PET/운세/장비/폴더/무기/공격력·숫자 및 ‘통신’ 그래픽 회귀 포함.
원본과 이전 작업 보존, 독립 및 최종 도구 재빌드 바이트 동일.
SHA256 `04fa8f4ee432880ef52469ae149e42de6d5043e1db8b6699806d5f2c70e21c52`.
기록: `analysis/ROLL_RETURN_ROM_HANDOFF.md`, `analysis/roll_return_v1/return_runtime.json`.
자동 테스트162개 통과(284.944초): `analysis/roll_return_v1/test_summary.txt`.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review 및 release_eligible=false 유지.

## 이전: 롤 플러그인 대사5개 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_roll_jackin_v1.gba`다.
누적958텍스트 단위와 기존9그래픽 유지. 전체 게임 완료율이 아니다.
롤 운세/미니게임 풀의103산문 초안에 이어 플러그인 직전5문구를 추가했다.
정상3문구와 인터넷 진입, 별도 밝은 기분2문구 진단의 폰트/VRAM/화면 검사 통과.
진단은 정상 기분 분기 증거가 아니며 상태 파일을 격리했다.
원본/이전 번역/ROM 보존, 독립/최종 도구 재빌드 바이트 동일.
SHA256 `53817f7969f64c2391173782e7fe1dd1280d3e904c31d2e609bef0bafca46363`.
기록: `analysis/ROLL_JACKIN_ROM_HANDOFF.md`, `analysis/roll_jackin_v1/jackin_runtime.json`.
전체 테스트는 `analysis/roll_jackin_v1/test_summary.txt` 참조.
development-draft; NON-DISTRIBUTION, 문구/시각 needs_review 및 release_eligible=false 유지.

## 이전: 롤 첫 만남·재회 대사5개 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_roll_intro_v1.gba`다.
롤 인사 풀65F9AC의5문구를 번역해 누적850텍스트 단위다. 기존9그래픽 유지.
정상 롤 선택 경로로 첫 만남2문구의 실제 글리프/VRAM/화면 픽셀과
페이지 전환 잔상·후속 대사 전환을 확인했다. 재회3문구는 원문 구조/인코딩/
폰트/폭 검증만 했으며 실제 진입·표시는 아직 열려 있다.
기존 롤 PET22실행 문구/29선택 단계, 롤/록맨 장비·폴더·무기·공격력/숫자·
PET7이미지(`통신` 포함)는 같은 새 ROM에서 회귀 검증한다.
자동 테스트134개 통과(41.059초). 독립/현재 도구 재빌드 동일, 원본 보존.
SHA256: `acf1de2629ddfe529d94da519bce3efe34bb126f700f071639266266bd5e746c`.
기록: `analysis/ROLL_INTRO_ROM_HANDOFF.md`, `analysis/roll_intro_v1/runtime.json`.
첫 인사 다음 날짜별 대사와 다른 내비/전체 미번역, 인간 문구/시각 승인 등은 남았다.
전체 게임 분모/완료율이 아니며 development-draft; NON-DISTRIBUTION 유지.

## 롤 PET 대사44개 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_roll_pet_v2.gba`다.
롤의 대기·7메뉴 확인·재진입·말 끊기 반응44개 문구를 추가했다.
누적845텍스트 단위, 번역 그래픽9개 유지. 전체 게임 완료 수치가 아니다.
실제 정상 롤 경로에서 대기·7확인창22개 단위의 전체 글리프/VRAM/화면 픽셀과
29단계 예/아니요 이동·취소·복귀를 확인했다. 다른22개(재진입·저장 질문·
말 끊기 반응)의 실제 표시 검증은 남아 있고, 원문 명령/분기/폰트는 정적 검증했다.
닉네임 뒤 첫 행은 원본 쉼표 바이트를 유지해 길이나 조사 의존성을 추가하지 않았다.
록맨/롤 장비·공격력 이미지와 숫자, 폴더·무기·PET7 이미지/`통신` 회귀 통과.
자동 테스트130개 통과(38.807초), 독립/현재 도구 재빌드와 일치. 원본 보존.
SHA256: `28f7d52dc6d09a13b6c91e4a29950f6fa443225049328c70bdc4023657cffd24`.
기록: `analysis/ROLL_PET_ROM_HANDOFF.md`, `analysis/roll_pet_v2/runtime.json`.
롤 첫 인사·날짜별 대사 등 미번역과 인간 문구/시각 승인, 전체 게임 검증은 남아 있다.
development-draft; NON-DISTRIBUTION 유지.

## 롤 장비 안내문 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_roll_equipment_guides_v1.gba`다.
롤의 폴더 편집·R/L 무기 선택 안내3개를 추가했다. 누적801텍스트 단위와
기존9그래픽이며 전체 게임 완료 수치가 아니다. 롤은 별도 원본6E12DC 풀을
복제해 사용하고, 록맨과 다른 내비의 원문 풀·로더는 유지한다.
정상 Navi 선택→롤 PET→장비 경로에서3선택·복귀·재진입을 확인했다.
모든 안내 글꼴·VRAM·화면 픽셀, 롤/록맨 공격력 이미지와 숫자 보존,
기존 무기·폴더·PET7개 이미지(`통신` 포함) 회귀를 확인했다.
자동 테스트126개 통과(68.003초). 원본 ROM은 변경하지 않았다.
SHA256: `fafc0a85d217fad5b614fa0b5f6155f195cb6406ded300c10952aac8d56cff2d`.
자세한 범위와 재현 방법: `analysis/ROLL_EQUIPMENT_GUIDES_ROM_HANDOFF.md`.
롤 첫 인사/PET 대사와 다른 내비 안내는 미번역으로 남아 있다.
development-draft; NON-DISTRIBUTION 및 문구/미감 needs_review 유지.

## 장비 공격력 이미지 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_attack_caption_v2.gba`다.
일본어 공격력 이미지를 `버스터 공격력`으로 번역했다. 테두리/배경/숫자 영역과
팔레트/크기/포인터/게임 코드는 유지하고 원래 압축 슬롯 안에서 재압축했다.
798텍스트 단위는 그대로이며 번역 그래픽은 PET7 + 장비 제목1 + 공격력1의9개다.
전체 게임 완료 수치가 아니다. 실제 BIOS 해제1156바이트, RAM/VRAM/OBJ,
3선택·재진입의4화면 픽셀과 숫자 보존, 기존 무기/안내/폴더/`통신` 회귀를 확인했다.
자동 테스트121개 통과. 독립 재빌드 SHA256:
`cc3c18f31e3ce3f6dfadbe7fa75605526cbef67dc75d5ff7fdd03cb76c77294e`.
기록: `analysis/ATTACK_CAPTION_ROM_HANDOFF.md`, `analysis/attack_caption_v2/runtime.json`.
다른 Navi의 안내문과 전체 게임 미번역/실제 플레이 검증은 남아 있다.
development-draft; NON-DISTRIBUTION 및 문구/미감 needs_review 유지.

## 공통 장비 무기 이름33개 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_equipment_weapons_v1.gba`다.
차지 샷·거츠머신건·롱소드 등 공통 무기 이름33개를 추가해 누적798텍스트 단위다.
원문 약자 C/WB/B/D를 유지하고, 기존4개 UI 문구는 그대로 이어받았다.
33개 모두 인코딩/종료/폭/폰트/23Navi 선택 테이블을 대조했다.
실제 플레이 샘플은 Rockman의 록 버스터↔실드↔차지 샷 및 종료·재진입이며,
다른 Navi의 무기 이름 실제 화면까지 검증했다는 의미는 아니다.
기존 안내문/폴더/PET `통신` 회귀와 전체 자동 테스트115개를 통과했다.
독립 재빌드 SHA256: `d0cd5c4f7f65d73a3974deec567a4896edeeed930da3f29300e3eb634e4581c4`.
자세한 기록: `analysis/EQUIPMENT_WEAPONS_ROM_HANDOFF.md`, `analysis/equipment_weapons_v1/runtime.json`.
공격력 OBJ 표기와 다른 Navi 안내문 등은 미번역이다. 문구 needs_review,
development-draft; NON-DISTRIBUTION 유지. 원본/이전 개발 ROM 보존.

## 장비 안내문 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_equipment_guides_v1.gba`다.
칩 폴더 편집과 R/L 버튼 무기 지정 안내문 3개를 추가해 누적765텍스트 단위다.
원본 대사 풀을 유지하고, 동일 원문 풀을 사용하는 Navi0/13/14의 장비 안내만
별도 ROM 복제로 연결했다. 실제 화면 검증은 Navi0의 선택3개·종료·재진입이며,
나머지 Navi 분기는72개 합성 CPU 사례와 원본 풀 대조까지다.
ROM→폰트→VRAM→화면 글자 픽셀, 기존 폴더/장비/PET `통신` 회귀를 통과했다.
독립 재빌드와 동일하며 SHA256은
`79ed6e9022dbece072a015d93a296a82254159f486f4c0af7db59a587b8e68b6`.
세부 기록: `analysis/EQUIPMENT_GUIDES_ROM_HANDOFF.md`, `analysis/equipment_guides_v1/runtime.json`.
공격력 OBJ 표기·다른 무기 이름·다른 Navi 안내문 등은 아직 미번역이다.
전체 번역/배포 완료 아님. development-draft; NON-DISTRIBUTION, 원본/이전본 보존.

## 장비 선택 항목 추가 반영 (2026-10-03)

이전 개발 ROM은 `poc/output/exe45_ko_development_equipment_labels_v2.gba`다.
장비 내부의 `칩 폴더 / 록 버스터 / 실드` 3개 항목을 추가해 누적762텍스트 단위다.
짧아진 제목 뒤에 생긴 숫자 잔상도 원래12개 OBJ의 지우기 폭을 맞춰 수정했다.
새 ROM cold-chain의 3선택·나가기·재진입, ROM→stage→VRAM→OBJ 글자 픽셀,
기존 폴더/PET `통신` 포함 회귀와 독립 재빌드 동일성을 검증했다.
SHA256: `2c25fa199817caa94765e7f5c5d94370cd54f477f72dbf6d5fbb46a534faa0ea`.
세부 기록: `analysis/EQUIPMENT_LABELS_ROM_HANDOFF.md`, `analysis/equipment_labels_v2/runtime.json`.
장비 안내문·공격력 OBJ·다른 무기 이름 등 미번역은 남아 있다.
development-draft; NON-DISTRIBUTION 유지. 첫 잔상 후보/이전 개발본/원본 보존.

## 9번째 장비/칩 폴더 화면 추가 반영 (2026-10-03)

현재 개발 ROM은 `poc/output/exe45_ko_development_folder_labels_v1.gba`다.
상단 일본어 이미지를 `장비`, 목록 제목을 `칩 폴더`로 번역했다.
누적 759텍스트 단위, PET 7그래픽 + 장비 상단 1그래픽이며 전체 완료 수치가 아니다.
새 ROM 자체 cold-chain, 폴더 입력/스크롤 4캡처, ROM→버퍼→VRAM→화면 픽셀,
기존 PET `통신` 포함 7개 선택 화면과 독립 재빌드 동일성을 검증했다.
SHA256: `b4afc0967d53276dd23fb5980014be4ecbc3eafabb79694a20d44b5e782d1360`.
세부 기록은 `analysis/FOLDER_LABELS_ROM_HANDOFF.md`, `analysis/folder_labels_v1/runtime.json`.
development-draft; NON-DISTRIBUTION 유지. 원본/이전 개발본은 보존했다.

## PET 메뉴 이미지 ROM 반영 (2026-10-03)

사용자 승인에 따라 소형 픽셀폰트로 PET 메뉴 7개 라벨을 다시 작성해 새 개발 ROM
`poc/output/exe45_ko_development_pet_graphics_v1.gba`에 반영했다. 통의 초성 구분을 위한
프로젝트 전용 8픽셀 글리프를 적용했다. 원본 아이콘·테두리·팔레트·타일 크기 보존 검사를 통과했다.
기존 758문장 번역 유지 + 그래픽 라벨 7개이며, 전체 게임 이미지 번역 완료 수치가 아니다.
동일 ROM cold-chain, 선택7/확인·취소14 화면의 모든 라벨 픽셀 마스크와 원본 로더 읽기를
검증했다. 재빌드가 동일하며 SHA256은 `2ec5cf763c8cf063cc67e2e02609a3097de2471425792670c5172e523ae69f40`다.
세부 범위는 `analysis/PET_FONT_ROM_SCREEN_HANDOFF.md`와 `analysis/pet_font_v2/runtime.json` 참조.
여전히 development-draft; NON-DISTRIBUTION이다.

## 이전 PET 이미지 미번역 조사 (보존 기록)

PET 메뉴 일본어 라벨 7개를 OBJ 그래픽으로 확인하고, 원본 타일·OAM·수정 영역 및
한글 문구 후보를 `analysis/pet_labels_v1/`에 기록했다. 한글 이미지 생성 시안 1개는
크기/팔레트 검사 실패로 ROM에 넣지 않았다. 현재 ROM은 기존 758문장 개발본 그대로다.
동일 ROM의 검증된 cold-chain에서 메뉴 7항목을 실제 입력으로 순회했으며, 각 선택의
위치/팔레트와 원본 그래픽 블록 일치를 확인했다. 자세한 한계와 이어갈 작업은
`analysis/PET_IMAGE_ROM_HANDOFF.md`를 참조한다. 정식 이미지 단계 및 배포 완료 아님.

## 고정 입력

| 항목 | 값 |
|---|---|
| 크기 | 8,388,608 바이트 |
| SHA-256 | `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` |
| SHA-1 | `f89ef4ca8ec1823eb75fa184f2d0f9e66cc78a59` |
| MD5 | `0f82bb24585c9ec64e99394c9d316315` |
| 헤더 | `ROCKEXE4.5`, 게임 코드 `BR4J`, 버전 0 |

## 현재 확정된 텍스트 경계

공개 영문 패치 소스의 `exe45.tpi`를 후보 카탈로그로 사용하되 대상 ROM과 전수
대조한다. 카탈로그는 732개 아카이브와 961개 포인터를 선언한다. 이 수치는
`tools/verify_tpi_index.py`가 실제 바이트, LZ77 경계, 포인터 값을 모두 통과한 뒤에만
채택한다. 카탈로그 밖의 메뉴·그래픽 텍스트는 아직 전체 분모가 아니다.

EXE3에서 재사용한 원칙은 다음과 같다.

- 제3자 주소표를 사실로 간주하지 않고 대상 ROM에서 전수 검증한다.
- 수정 전 TPL 추출→재삽입의 무변경 왕복을 먼저 통과시킨다.
- 압축 표현이 달라도 게임이 소비하는 해제 페이로드가 같으면 동등으로 본다.
- 폰트·코드페이지·렌더러는 EXE3 주소를 옮겨 쓰지 않고 4.5에서 다시 확정한다.

## 재현

```powershell
python tools/verify_tpi_index.py --rom "Rockman EXE 4.5 Real Operation (J)(Independent).gba" --tpi external/textpet-indexes/exe45.tpi --output analysis/exe45_tpi_verification.json --label exe45-jp-retail
python tools/extract_baseline.py
python tools/text_corpus_stats.py --tpl-dir analysis/tpl_baseline --output analysis/exe45_text_corpus_stats.json
python tools/build_nochange_roundtrip.py
python tools/survey_font_candidates.py
python tools/analyze_codepage.py
python tools/scan_f9fc_collisions.py
python -X utf8 tools/verify_korean_roundtrip.py --extra-characters ',' --work poc/visibility/work-codec-check --report analysis/exe45_korean_codec_check.json
python -X utf8 tools/build_development_patch.py --work poc/visibility/work-library-next --out poc/output/exe45_ko_development_library_next.gba
python -X utf8 tools/build_development_patch.py --chip-library --work poc/visibility/work-chip-library-next --out poc/output/exe45_ko_development_chip_library_next.gba
python -X utf8 tools/report_chip_library_runtime.py --out analysis/exe45_chip_library_ko_runtime_recheck.json
python -X utf8 -m unittest tools/test_text_catalog.py tools/test_korean_codec.py tools/test_tpl_literals.py tools/test_development_font.py tools/test_archive_scripts.py tools/test_fixedcell_font.py tools/test_lz10_literals.py tools/test_chip_library_extension.py tools/test_chip_library_runtime_report.py
```

`analysis/tpl_baseline`과 `analysis/txt_baseline`은 원본에서 추출한 저작권 자료이므로
배포·커밋하지 않는다.

`build_development_patch.py`가 현재 개발 빌드의 단일 진입점이다. 기존 산출물을
덮어쓰지 않으므로 재실행할 때는 새 작업·출력 이름을 지정한다. 예전
`build_visibility_poc.py`와 `build_extended_visibility_poc.py`는 조사 재현용이다.

## 현재 개발 빌드 (2026-10-03)

최신 누적본은 `poc/output/exe45_ko_development_roll_tactics_v1.gba`다.
SHA-256: `1ca65635bcfb92ff3845bf7b75cf6491a045f32cceda5ec16eca977d7d45f31f`.
이전756단위에 롤 전술 질문2개를 추가해 누적758단위다. 기존 문구 ID를 연결해 재사용했다.
새 ROM 콜드 경로와 롤 질문6/7의 진단용 stage/upload/BG3/픽셀, 기존 전술·도주·폴더 회귀 검사를 통과했다.
진단은 록맨 초상/플레이어를 유지하며 실제 롤 선택 플레이를 증명하지 않는다.
근거/재현/한계: `analysis/ROLL_TACTICS_ROM_SCREEN_HANDOFF.md`,
`analysis/exe45_roll_tactics758_runtime_v1.json`. 배포 금지 개발본이며 의미/표현 승인은 미완료다.

이전 롤 도주 단계는 `poc/output/exe45_ko_development_roll_escape_v1.gba`다.
SHA-256: `9762ba24860844b6bb4e5220a05fb7c0973bf9a4c9cdba456c96e16ea19b4096`.
이전750단위에 롤 도주 대사6개를 반영해 누적756단위다.
새 ROM 콜드 경로를 재실행하고 롤 진단 표시 및 기존 록맨·폴더·전술 질문 회귀를 검사했다.
실제 롤 선택/도주 판정이나 전 게임 완료는 아니다. 창 닫힘 중 메톨의 native 점멸 픽셀도 별도로 분류했다.
근거/재현/한계: `analysis/ROLL_ESCAPE_ROM_SCREEN_HANDOFF.md`,
`analysis/exe45_roll_escape_runtime_v1.json`. 배포 금지 개발본이며 문구/표현 승인은 미완료다.

이전 록맨 도주 단계는 `poc/output/exe45_ko_development_megaman_escape_v1.gba`다.
SHA-256: `0edaf04c993efcdeced55e743e9f7a4dbbbdabab53d1ced99e759e8e69c1e97e`.
이전744단위에 록맨 도주 대사6개를 반영해 누적750단위다.
실제 도주 불가 분기와 진단용 확인/성공/실패 표시, 기존 폴더·전술 질문의 화면 검사를 통과했다.
실제 도주 성공/실패 판정과 전체 게임 번역 완료를 뜻하지 않는다.
근거와 미검증 범위: `analysis/MEGAMAN_ESCAPE_ROM_SCREEN_HANDOFF.md`,
`analysis/exe45_megaman_escape_runtime_v2.json`. 배포 금지 개발본이다.

이전 추가 칩 이름 단계는 `poc/output/exe45_ko_development_chip_secondary_names_v1.gba`다.
SHA-256: `c0080a116f4966edbfa3cb9578526a39f6c25c45eec52e3eef99eb3530e950bf`.
이전 646단위에 추가 칩 이름 98개를 도감·폴더 전용으로 반영해 누적 744단위다.
원본 이름 풀/공유 포인터와 비선택 슬롯을 보존하며, 추가 칩 배틀 이름은 아직 원본이다.
대표 추가 이름 7개·설명 화면 및 기존 이름 스크롤의 픽셀 검사를 통과했다.
전체 이름의 실플레이 표시 검증이나 전체 게임 번역 완료를 뜻하지 않는다.
재현 해시와 한계는 `analysis/SECONDARY_NAMES_ROM_SCREEN_HANDOFF.md`,
실행 근거는 `analysis/exe45_secondary_names_runtime_v1.json`에 기록했다.
모든 번역은 검토 대기 중이며 배포 금지 개발본이다.

## 이전 도감 72단위 단계 기록

당시 선택형 로컬 실행 파일은 **`poc/output/exe45_ko_development_chip_library_v1.gba`**다.
SHA-256: `ce839b60c8125da7ca8ce0240bcdfc82a8e8f5604202449af1acffa80158cbff`.
`--chip-library`를 명시해야 이 72단위 경로를 선택한다. 옵션 없는 기본 빌드는
기존 69단위 `exe45_ko_development_library_v1.gba`의 범위를 유지한다.
이전 소개·PET·저장 개발본과 임시 고정폭 표시 PoC는 보존했다.

소개·재회 4개, PET 확인 대사·선택지 45개, 록맨 저장 대사 16개, 도감 제목 4개,
칩 이름 3개(캐논·에어슛·발칸1)를 더해 합계 **72개 번역 단위**를 재삽입했다.
전 게임의 번역률은 아니다. 도감 전용 사설 이름 풀과 행별 한글 캐시를 사용하며,
원본 칩 이름 풀 2개·공유 포인터 18개와 사설 풀 비선택 253개 스크립트는 보존한다.
구현·실행·남은 부하/아이콘 검증은 `analysis/CHIP_LIBRARY_PROGRESS.md`에 기록했다.
후속 56셀/7아이콘 격리 시험은 표준·메가·기가에서 글자/아이콘 공급을 통과했지만,
첫 진입의 한 프레임 추가 지연이 남았다. `analysis/CHIP_LIBRARY_TIMING_PROGRESS.md`와
`analysis/exe45_chip_library_stress_v1.json`에 정상 실행과 구분해 기록했다.
다른 728개 아카이브와 포인터,
공유 저장 아카이브에서 선택하지 않은 115개 스크립트는 원본 바이트를 보존한다.

이번 누적 ROM에서 첫 소개문, 세 칩 이름의 스크롤·지우기·입력 화면 이후 재진입,
네 도감 제목의 탭 왕복,
저장 확인·경고·완료와 파일 기반 콜드 부팅→이어하기를 확인했다.
PET 7개 확인창·아니요 및 덮어쓰기 예/아니요의 더 넓은 검증은 이전 save-v1
ROM의 증거이며 이번 실행 결과와 구분한다. 저장 검증은 프로젝트 내부의 별도
에뮬레이터/세이브 폴더에서 수행한다.
저장 오류·재시도 분기, 재회, 동적 이름 삽입, 같은 문구의 개별 분기 실행은 남았다.
통신 대전 및 전투를 검증했다는 뜻은 아니다.

한글 11,172자와 쉼표를 연속 문자열·문장 시작·`keyWait` 직후에서 왕복 검증했다.
수정한 TextPet 플러그인으로 원본 732개 페이로드도 모두 보존했다. 쉼표까지 포함한
**v3 검사**가 현재 근거이며, 코덱 전수 검사는 모든 글자의 게임 내 표시 증거가 아니다.

현재 진행·재현·남은 작업은 `analysis/CHIP_LIBRARY_PROGRESS.md`, 이번 실행 근거는
`analysis/exe45_chip_library_ko_runtime.json`이다. 이전 69단위 제목 단계는
`analysis/LIBRARY_PROGRESS.md`, `analysis/exe45_library_ko_runtime.json`에 보존했다.
이전 저장 단계는 `analysis/SAVE_PROGRESS.md`,
`analysis/exe45_save_ko_runtime.json`에 보존했다.
이전 단계는 `analysis/INTRO_CODEC_PROGRESS.md`, `analysis/PET_MENU_PROGRESS.md`에 남아 있다. 번역 검토 및
전체 게임 한글화는 미완료이며 모든 ROM은 배포 금지 개발본이다. 도감 세 항목 이외
칩 이름과 다른 메뉴의 한글화는 남았고 별도 소비 경로 조사 결과는
`analysis/exe45_library_font_consumers.json`에 기록했다.

도감 제목은 **F9 FC 확장 인코딩과 별도 8×16 한글 뱅크**로 구현했다.
기존 일본어 슬롯은 변경하지 않는다. 칩 이름 3개도 이 한글 뱅크를 재사용하지만
별도 7행 타일맵 소비자에만 적용한다. 나머지 칩 목록·mono 설명은 아직 일본어다.
한글 11,172자의 고정폭 코덱 경계 전수 근거는 `analysis/exe45_fixedcell_codec_v1_final.json`.
이전 두 음절 임시 슬롯 실험은 `analysis/FIXEDCELL_PROGRESS.md`에 역사적 근거로 남았다.

현재 위 일곱 테스트 모듈은 총 30개 테스트를 통과한다.

## 현재 PoC 결과

무변경 왕복은 732/732 아카이브에서 통과했다. 일반 대사 렌더러는 Mesen 2의
콜드 부팅·일반 패드 입력 경로에서 두 단계로 확인했다.

- 임시 코드 치환 PoC: 원본 크기를 유지한 채 `한글` 표시 및 글리프 레코드
  129/132 소비 확인.
- 확장 인코딩 PoC: `F9 FC + U+AC00 기준 16비트 음절 번호`와 11,172자 글꼴을
  추가해 `한글` 표시 및 레코드 11030/954 소비 확인.

증거는 `analysis/exe45_visibility_poc_runtime.json`과
`analysis/exe45_extended_dialogue_poc_runtime.json`에 고정했다. 두 ROM은 모두
배포 금지 개발 산출물이다.

## 다음 완료 조건

상세 결과와 현재 위험은 `analysis/INITIAL_SURVEY.md`가 정본이다.

1. 메뉴·전투·고정폭 UI·이름 입력 렌더러별 코드→글리프 경로를 확정한다.
2. 전체 한국어 코퍼스 수요와 총 글리프/동시 상주 예산을 따로 측정한다.
3. PET 동적 이름 삽입·재회·개별 재진입 분기 및 저장 오류 경로 검증을 확장한다.
4. 텍스트 카탈로그 밖 그래픽·고정폭 UI·플레이어 입력 문자열을 별도 모집단으로 조사한다.
