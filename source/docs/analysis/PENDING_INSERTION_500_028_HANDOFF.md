# 028: 실제500개 반영·독립재빌드·최대 프로필6쪽 표본 검증 완료

## 현재 상태

이전 검증 완료본은027(`poc/output/pending500_027_v1.gba`, SHA256 `2353a0077b7655abb0abb3f3ba8ca95d4242112931e3dddaccb16f27527f2a0d`,14,622개)이다. 실제028은 `poc/output/pending500_028_v1.gba`, SHA256 `66d93c8f0142f2d5e5a48e112af995af5f40e7d031627b9c362878573a95f3ef`,12,364,916bytes로 출력됐으며 신규500개를 더해15,122개다. 원본 기반 독립재빌드와 전체byte 동일하고, 독립 검사는 기존467개 소비자 비변경+2개 병합, 새 RAW9개/500개를 확인했다. 실제028의CPU/정상 초기설정·메일/최대 프로필6쪽·화면53개 표본 검증도 아래 범위에서 완료됐다. 현재 권위는 `analysis/pending500_028_v1/batch_status.json`이며 완성판/전체 요청 완료·배포 승인이 아니다. 이500개를 다시 선정하거나 적용하지 않는다.

- 신규500개 / 142개 whole script / 11archive / 문구 유지·명시적 줄배치28개.
- 기존027에서 새로 채택한`6842F8`,`69561C`의 기존41개를 보존하며23개를 추가한다.
- 새 RAW9개: `69B134`,`6A0640`,`6A6C64`,`6ACCA8`,`6B8478`,`6BE52C`,`6C40AC`,`6C982C`,`6CF0A0`에477개를 추가한다.
- 실제 누적15,122개, primary427/catalog 물리적 비변경305. 305는 잔여 미번역 수가 아니다.
- BPS/xdelta/ZIP은 사용자 재요청 전 만들지 않는다. 원본/이전 ROM/세이브/기존ZIP을 보존한다.

## 고정 입력과 빌드 경로

`survey_layout500_028_v1.py` → `prepare_layout500_028.py` → `compile_layout500_028.py` → `merge_layout500_carry_028.py` → `layout500_inputs_028.py` → `build_layout500_028.py`.

carry manifest: `analysis/pending_insertion_500_028_carry_v1/preflight.json`, SHA256 `25d95617e76f9ee8cf03d8356eac9be42a60986627def53dc59ec9adf1884f31`。

`tools/specs/primary028_version.json`은 frozen027 대비 정확한6개 변경을 검증한다. 027에서 새로 채택한11개는 main compile loop 뒤에 배치되므로, 그중2개에 대한028 누적 합성을 단순 main-loop 호출로 끝내면 안 된다. `layout500_product_028.append_prior027`이 source-derived027 compile payload에028을 합친 뒤 한 번만 배치한다. 새9개도 원본에서 별도 배치하며 ExpectedWrites에 모든 catalog pointer를 등록한다. 이전 patched ROM은 비교용이고 source input이 아니다.

## 이미 통과한 비-ROM 검사

- source/target/reverse/binary roundtrip,485개 실제027 글꼴, 비선택script 바이트 보존.
- 024→025→026→027 carry 재구성과 실제027 payload 비교; 기존41개 문구/메트릭/소비 계약 유지.
- 현재500개 입력 게이트, 실제 production group 손상 거부7개.
- native direct-profile 모델29개(기존027 고정 fixture), actual027 source+native cap/input/commit/reader CPU304개의 적용성 확인.
- 실제 append 함수의 source-derived 격리 블록 시험: 이전02711개+신규0289개, 합집합1000개, 변경2개가 배치 전에 병합됨, writer overlap 거부. 전체 ROM/런타임 증거는 별도다.

stdout의 일부025/026/027 명칭은 이전 버전의 진단 레이블이다. 기계 판독 JSON의baseline027 hash/manifest/selected IDs와 source applicability가 권위이며 옛 이름을 적용 수치나 아티팩트 식별자로 쓰지 않는다.

## 완료한 실제028 검증

전체 빌드 `python -X utf8 tools/build_layout500_028.py`, 독립 재빌드 `--repro`가 모두 완료됐으며 출력은 `poc/output/pending500_028_v1.gba`, `_repro.gba`다.

`verify_layout500_product_028.py`의pre-repro 및repro 대조 PASS, actual028 `bench_profile_product_028.py` source+028 CPU304/A3 CPU5,652/B0 CPU6,341/손상 거부16개/native-control byte identity PASS다. own028 coldboot/초기설정/자판3페이지/네 내비/메일23쪽 및재열기도 통과했다. `run_profile_runtime_028.py`는 새 WoodMan6A0640:25/AquaMan69B134:46을 격리 root/table alias로 표시하며 max8 crush/max4 worst-subject native record를 F90C에서 잠시 주입·복원했다. 두case 각3쪽/복귀 총8capture에서 신규7문구6쪽의 전체 줄좌표/font CPU→RAM/OBJ→pixels/잔상/순서/keyWait/PET복귀를 검사했다. 실제 화자는 own Rockman host이므로 자연 WoodMan/AquaMan caller나Navi교체 증거가 아니다. alias나임시필드주입은 ROM에 들어가지 않는다.

`prepare_layout500_visuals_028.py`의22startup/23mail/8raw 화면을 직접 확인하고 visual_review를 작성한 뒤 `finalize_layout500_028_v2.py`로 완료 체크포인트를 고정했다. 첫 `verify_profile_display_028.py`는 context+1에target body25/46을 기대해 실패했다. 원본0804FB72가caller r1=0을 먼저 저장하고0804FB76의header read만alias한다는14bytes와6개 실제wait pointer를 확인했다. 기존 도구를 보존한v2는정확한source/final코드와저장index0을검증하며다른root/body/글꼴/줄폭/정지/잔상/복귀검사를유지했다. ROM/캡처는바꾸지않았다. `checkpoint_alias_index_correction.json`에기록했다. 전체500개 문맥/사람의 승인·저장/재로드·하드웨어/음성·자연 이벤트 검수는 별도이며 NON-DISTRIBUTION이다.

## 다음 단계의 범위 주의

`analysis/pending_insertion_500_028_projected_remainder_v1/projection.json`은 이번500개를 논리적으로 제외한 후보 전망일 뿐 실제028 적용 검사가 아니다. 현재 direct-profile 모델에는119개, 미채택guard 등다른분석모델에는34개가 전망된다. 이것은 게임 전체 미번역 잔여 수가 아니며 다음500개를 맞추려고 미검증 배열/변수/renderer/혼합partial-script 계약을 완화하면 안 된다. `analysis/pending_insertion_500_028_array_candidates_v1/source_tables.json`은 다음 조사용8개 배열table 후보이며 cache producer/선택record/terminator/suffix가 미확인이라 width model이나제품입력으로 채택하지 않았다.

자동한글조합→확정→저장→재표시, native kana·일본어 호칭/날짜HUD/타이틀로고/메일머리글Eメール, inherited welcome bitmap 행간/겹침, 기존65CC78:43의“오늘은…과목은”문장 검수는 여전히 미완료다.

다음 실제028 survey에서 적용ID를 다시 대조한다. carry scope는cumulative028를우선하고source-based 재구성은024→025→026→027→028순서다. 다음 병합이028에서새로등록한9개 영역을건드리면main loop밖의등록단계에서도최종할당전에합성해야한다. 이전ROM을overlay하거나source-only payload로이미적용된단어를지우지않는다. 원본/이전ROM/세이브/ZIP보존, 새 BPS/xdelta/ZIP 없음.

한글 입력·저장 통합 시 이번 native field 폭을 그대로 재사용하면 안 된다. 실제028의advance table에서11,172개 한글 음절은 모두12px임을 확인했다. 현재 정상 native record의8글자 상한은88px지만 한글8음절을 같은 논리 글자 수로 지원할 경우96px이 된다(4글자도44→48px). 이는 향후 입력 표현·저장 형식·호칭/배열 cache·모든 재표시 경로와 해당 대사의 재배치 검증을 다시 연결해야 한다는 뜻이며 지금의native-only CPU/GBA 표본은 한글 저장 지원으로 승격되지 않는다. descriptor17/9bytes에서 한글 입력 가능 글자 수를 계산하거나 임의로 줄이지 않는다.
