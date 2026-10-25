# 033 준비272개 — 추가19개 소스·누적 병합 검증, ROM 적용0개

## 2026-10-17 현재 상태

- 실제 완료 ROM은 **`poc/output/pending500_032_v1.gba`**, SHA256 `cc2d02d3fda6ab27601d1735015b24b11d869308dff3e08f0fd4f06f31518f64`, 12,418,796바이트/**17,122개 적용** 그대로다. `analysis/pending500_032_v1/batch_status.json`이 제품 권위다.
- 다음033 준비 권위는 **`analysis/pending_insertion_500_033_preflight272_v2/status.json`**. 기존253개+추가19개=**272개/103전체스크립트/35아카이브**, 관련 기존번역 **3,035개** 소스 재구성·병합 보존. 추가로 안전한 **228개**가 필요하다. 준비272는 실제 ROM 적용 수가 아니다.
- 사용자 결정 `analysis/pending_insertion_500_033_batch_policy_v1/decision.json`: **정확500개가 준비되면 적용**. 부분253/272 ROM 생성 금지. 이 결정 파일의 준비253/부족247 숫자는 선택 시점 스냅샷이며 현재 준비 수는272상태 보고서를 본다. 정책은 여전히 유효하고 다시 묻지 않는다.
- 새 ROM/BPS/xdelta/ZIP 없음. 모든 실행 세션 종료. 원본/이전 보호 아티팩트/032 고정 도구 보존. 목표/자동화/서브에이전트 없음.

## 추가19개

- AquaMan **697B70:50,51,52**의12개 일본어 literal와 Bass **6D1984:32:0** 1개. 이는 기존21calendar루트의 남은13개다. **실제032에서는 아직 일본어**이며 일정 전체한글화/동적요일/이미지 완료가 아니다.
- 일반 대사 **7C8570:15** 3개, **7CA474:12** 3개. 이전에 분석만 통과했던6개다.
- 기존 고정 `needs_review` 번역 문장·단어 공백·보호되는 선후행 LF/패딩·제어 코드를 유지했다. 새 의미 번역 작성이나 사람의 의미/말투 승인으로 세지 않는다.

## FD09 차이와 근거

AquaMan50..52는 다른 네비와 달리 `soundDisableChoiceSFX`가 `textSpeed0` 직후에 있고 선택지 직전에 다시 나오지 않는다. 다른 네비의 엄격한 기존 모델에 그대로 넣으면 거부되는 정상 원본 차이였다.

- `tools/bench_choice_sfx_033.py` → `analysis/pending_insertion_500_033_choice_sfx_cpu_v1/cpu.json`: **2,048 source/실제032 native CPU 조건**,512flag패턴×draw/width×두이미지. FD09의 실제 dispatcher/handler/native helper를 실행했다. draw는 context+0x3E의0x80bit만 세우고 stream2바이트 전진, width는 context를 바꾸지 않고2바이트 전진. 전체216byte context/레지스터/CPSR/쓰기/스택·컨텍스트canary 비교 통과. helper/BIOS 대체 없음. 실제 소리/선택 결과/자연 caller나 새 한국어 실화면 증거는 아니다.
- `tools/calendar_aqua_capacity_033.py`: 오직697B70, AquaMan portrait,50..52, 정확한 초기 명령/한번의FD09/원본flag3611/width8만 허용한다. **공간 계산용 뷰에서만** FD09 위치를 기존 모양에 맞춰 기존 시간/날짜·제목/선택지 모델을 재사용한다. 실제 원문·번역·컴파일에는 명령을 옮기거나 제거하지 않는다. 원본/번역 skeleton 동일성은 별도로 강제한다. UI·음성 효과 결과는 여전히 runtime pending.
- `tools/test_calendar_aqua_033.py` → `analysis/pending_insertion_500_033_aqua_models_v1/result.json`: 합성 짧은표현 정상3, 다른루트/portrait/FD09중복·이동/FD08/대상만제어변경/flag/width/날짜포맷/provider/ID/선택지폭 오류 **12거부** 통과.
- `tools/reconcile_prepared272_033_v2.py`는 실제 원본·번역 바이너리의 세 script 첫12바이트가 **`fc06e702f40028f00000fd09`**로 일치하고 FD09가 각각한번임도 확인했다. 공간투영이 제품 명령 변경으로 새지 않았다.

## 컴파일·기존 번역 보존

- `tools/prepare_supplement19_033.py` → `analysis/pending_insertion_500_033_supplement19_selection_v1/selection.json`: 실제032 적용 ID와 기존253 준비 ID에 비중복, 고정된 canonical/source/native payload/whole-script Japanese literal 범위 확인. 기존 Bass menu와 일반창 검증 결과 재현.
- `tools/compile_supplement19_033_v2.py` → `analysis/pending_insertion_500_033_compile19_v2/verification.json`:19개/6스크립트/4아카이브의 전체 원본바이너리 왕복, 번역의미·제어·바이너리 왕복, 미선택 원문script 바이트,16bit오프셋, 실제032 내70사용글꼴/BDF 일치 통과. **미선택 일본어가 남는 소스 전용 바이너리를 누적 ROM에 직접 덮어쓰면 안 된다.**
- `tools/merge_supplement19_carry_033.py` → `analysis/pending_insertion_500_033_carry19_v1/preflight.json`:원본+고정된 누적032 입력에서 기존285개를 재구성해 실제032와 바이트 비교하고19개를 병합했다. 기존문구/풍부한배치메타데이터/소비계약/미선택부모script 바이트와 왕복검증 통과.032ROM은 비교용이지 빌드입력이 아니다.
- `tools/reconcile_prepared272_033_v2.py` → 현재272상태:253/19선정·컴파일·병합ID 및아카이브 비중복, 실제032부모와 풍부한배치메타데이터/미선택바이트/모든기존보호파일/고정도구해시 재검사. 두 준비집합은 아카이브도 겹치지 않는다. 기존253부분에는20prior-appended 합성 요구가 남아 있고, 추가19는 모두기존 일반주아카이브다.

과거실패 보존: `compile_supplement19_033.py` v1은4아카이브 컴파일 뒤 증거목록 작성에서 로컬 adapter함수의 `__module__='__main__'`을 파일명으로 취급해 중단했다. v2가 실제모듈과 checker를 명시하고 **새출력경로**에서 전체 성공했다. `reconcile_prepared272_033.py` v1은 초기FD09를9바이트prefix로 잘못 가정해 거부했다. 원본·번역 실바이트가동일하고 실제prefix가12바이트임을 확인한 뒤 v2에서 정확한바이트명세를 검사했다. 게임/ROM수정으로 해결한 문제가 아니다. 실패코드·출력은삭제/덮어쓰기하지않았다.

## 다음228개를 위한 세로선택지 조사

- `tools/inspect_vertical_population_033.py` → `analysis/pending_insertion_500_033_vertical_inventory_v1/census.json`:현재미적용·준비272와비중복, RAW/명시msgOpen/선언된기존명령만있는 **224literal/61script/3기존주아카이브** 후보.71551C=6,71A66C=3,766134=215.각script에select1개/선택지2또는3개,width7/8/13. **224는 조사집단이지 준비완료/폭적합/228보충분이 아니다.**
- `tools/bench_vertical_wide_033.py` → `analysis/pending_insertion_500_033_vertical_wide_cpu_v1/cpu.json`:폭11..13,flags2/0x82,origin52,normalmode0/1,rows0..2의F608 draw/width **144 source/032 CPU 조건**.원본dispatcher/nativehelper/context/레지스터/CPSR/쓰기/canary, width13 allocation151px/centering 통과.기존1..10증거를 임의로확대하지않고 새유효범위를명시했다.3노드EA/EC입력·커서·branch·번역label폭·clear/GBA승인은 아니다.
- 다음판별작업: 기존 `normal_vertical_choice_capacity_026.py`는폭1..10/정확2노드/빈페이지 조건만허용한다.766134에는width13과3노드/BSeparate, 또는row0prompt+rows1/2선택지가있다. **임의로 예외를 풀지 말고** 원본EA/EC3노드 레코드·navigation/default/BSeparate/disableB/cancel/target 및행위치를 확인하고 별도좁은 모델/회귀검사를 만든다.캐노니컬단어·패딩·page/wait를보존한 실제label폭을모두검사한다.224중적합수는아직모른다.

## 이후 제품 반영

정확500이 준비되면272+추가228의선정/컴파일/누적032소비범위를 결합하고새입력관문/주빌드recipe에등록한다.과거`layout500_inputs_033_partial`와`layout500_product_033_partial`은253분모의미채택준비일뿐500용이아니다.현재와새Aqua/일반/선택지게이트, 기존032guard,20prior-appended원본합성→단일배치, 전체ExpectedWrites/꼬리/독립재빌드, 새ROM의CPU/글꼴·OBJ·픽셀·지움/복귀/재진입을검증한다.이전032savestate를새ROM정상진행증거로혼용하지않는다.

모든입력/도구는각보고서해시에고정됐다.후속수정은새버전/새출력경로로진행한다.원본·기존ROM·저장·번역·패키지·증거보존,배포패키지별도요청전금지.한글자동조합→확정→저장→fresh재표시,환영문구겹침,남은UI/이미지/공유요일/전체진행·의미검수는미완료유지.
