# 020 개발 ROM: 신규500개 반영·재현·표본renderer/정상경로 검증

## 현행 정확500개 통합 작업: 이전 후보 조사 상태 갱신

**020 신규500개 실제 반영/독립repro/전체artifact 감사/정상경로 회귀/표본renderer6쪽 PASS. 전체의미·자연루트·한글입력·저장·release는미완료.** `poc/output/pending500_020_v1.gba`,SHA256 `1e595b2113e446fa74be2c2e0c7737a0bf13bcbd7984114eb1c1df79b4580788`,11,945,892bytes,누적11,122units/404primary archive/328untouched. 원본기반빌드종료0이며019/원본/ZIP보존. `pending500_020_v1/lineage.json`PASS:actualnew500,이전IDs/carry/source·layout·nickname/fullbox proof/hashboundarguments검증. `selector_cpu.json`3,195 composedABI vector PASS. 아래‘빌드중/검증전’은역사적단계기록이며이현행상태를대체하지않는다.

`pending500_020_v1_repro.gba`독립productbuild종료0,전체11,945,892bytes가020과동일함을직접비교했다. `verify_cumulative500_020.py`→`pending500_020_v1/integration.json` PASS:실제500delta/전체포인터/Expected Writes/header/ISA/ancestry/repro/합성CPU binding. `verify_first_mail_runtime.py`→`normal_runtime.json`:같은020boot/pagecycle/complete/read/selection5segment80capture에서native3keyboardpage VRAM/map/초기설정,21namebank/4selectable OAM,firstIPC23ordered keyWait/3RAMarchive/pagebookmarks/복귀·재열기PASS. receipt성공을검증PASS로오인하지않고각검사를실행했다. firstmail23쪽비교표와6개새대사표본을직접봤으며normal/integration/fullbox/name보고서가동일ROM SHA에묶임도대조했다.

다음500개기준은이020 ROM이다. 현재fullbox180 범위에서아직선택하지않은문구,동일문구줄배치/다른변수·선택지·별도renderer/storage의미적용을현재ID기준으로다시대조한다. 500묶음마다원본기반재빌드·carry보존·동일제품화면검증을이어가며,이번500을다시세지않는다. native일본어이름/호칭은그대로이므로자동한글조합·저장통합과sourcecaller별자연route/독립의미·자연스러움검수는주요미완료조건이다. 새patch는사용자다시요청전금지.

`pending500_020_v1/mail_stream_runtime_v2.json`은전체startup/artifactQA와분리한firstmail-only검증PASS:23개orderedkeyWait/pagebookmark/3nativeRAMarchive동일/목록복귀·재열기. `first_mail_pages_v1.png`23쪽직접검사. 첫`mail_stream_runtime.json`은독립helper호출seed에서limits필드를누락해보고서write전KeyError로실패한시도이며보존했다. 같은보호검사를정상schema seed/v2에서재실행한것이며ROM/capture/gate변경없음. 최종normal_runtime전체보고서대체가아니다.

`pending500_020_v1/fullbox_runtime.json` PASS:실제020의7A7000:15 두page(180/180→짧은3행),7A8EC0:41 두page(짧은dots→180px),7B6F9C:13 3행대사. CPUfontreads/actualdrawoffset/ROMfont/OBJVRAM→pixels/nativekeyWait/52,110origin/이전페이지빈영역잔상검증. `fullbox_pages_v1.png`5page비교표직접검사. 이표본에서개발용180폭이실제작동함을보였으나모든435개문구/다른consumer/자연NPCroute/저장증거는아니다. 각런은PET root/table readalias진단1회,원래scriptportrait/명령실행,ownNavi0유지,checkpoint격리다.

`...name-six-entry`/`...name-six-complete`은019의action문자열만재사용하고020boot부터새state를만들었다. `...name-possessive`→`pending500_020_v1/name_runtime.json` PASS:66CA84:21:3 새‘의’문구,원래native6glyph+ちゃん99px/소유suffix합111px,CPU/font/OBJ/pixels/keyWait/잔상. step009직접검사. 원래WindManprofile사건이나provider를자연선택한것이아니며ownNavi0/female진단이다. 한글입력·저장/임의값/모든20수정문구화면·독립의미/자연스러움humanreview는미완료다. 이표시PASS를‘의/님은/님이’의최종의미승인으로보고하지않는다. release_eligible=false.

`pending_insertion_500_020_selection_v1/selection.json`에서52archive/194script/정확500개를고정했다. 개별20수정문구를포함한65whole-script unit와문구불변full-box435unit다. `prepare_pending500_020.py`→`pending_insertion_500_020_preflight_v1/preflight.json`전체500source-only compile/roundtrip PASS. 아직최종ROM반영을의미하지않는다. 원문/이전고정draft/019ROM보존,새patch없음.

fullbox는기존132px제약을전역해제하지않는다. `fullbox_capacity.py`에서source첫mugshotShow→msgOpen/단일초기화,변수·선택지·position·quick전환금지,페이지당literal1개/clear/exactIDs를고정하고개발용row180/180/168(원점52,110과마지막줄arrow영역고려)을검사한다. 작은quick/기존carry의literal profile은132px그대로다. 8fixture에서경계수용/overflow·arrow·quick·variable·composite·unselected거부PASS. **새폭의runtime은아직검증전개발가설**이며source-only PASS를consumer/runtime/release승인으로세지않는다. 통합ROM에서180px2행→짧은다음page,짧은page→180px,3행/clear/복귀를실측한다. 검증전development/NON-DISTRIBUTION.

PROFILE020은019기존398archive를보존하고새6(7B7AF0/7B7EF8/7B9104/7BA26C/7BBE54/7C0668)을추가한다. carry46+new6. `cumulative_batch500_020.py`→`pending_insertion_500_020_cumulative_v1/preflight.json` 종료0/PASS,이전parent byte재현/비신규scripts/consumer보존을검증했다. 새name/fullbox profiles는parent재컴파일에서제외해이전제품계약을보존한다. 실제new IDs500/중복0/이전layout ID와교집합0도별도확인했다. layout ID합계와manifest translated_units는같은분모가아니므로같은수로강제하지않았다(이전layout unique10,275/manifest10,622).

원본기반 `build_keyitem_full_rom.py --name pending500_020_v1`에기존전체019 flags와`--pending-batch500-020`을추가해productbuild실행중이다. output목표 `poc/output/pending500_020_v1.gba`,work `poc/build/pending500_020_v1`. 020flag/019prerequisite/누적writer/최종fullbox·nickname proofbinding/first_mail新pointer6개auditor를등록했다. 시작/중간로그를제품성공으로세지않는다. 다음은완료ROM의hash/실제delta검증→독립repro순차build와같은020normalboot/초기설정/첫메일→`capture_cumulative500_020_display.py`의wide/clear/third진단과`verify_cumulative500_020_displays.py`→6nativeglyph이름의possessive진단/`verify_cumulative500_020_name.py`다. 다른ROM checkpoint이식금지. 이전019정상경로녹화는입력action만참고하며state/ROM은새020에서생성한다. long full-box runtime실패시이제품의개발가설은미승인으로유지하고원인을분리한다.

## 이전 단계 기록: 개별 번역 보완20개·source-only compile

`translations/pending_insertion_500_020_wording_v1.json`은20개ID별before/제안translation/문맥별rationale의유일한수정문구권위다. ‘の/ノ’의소유표현,‘は/ハ’의주제,‘が/ガ’의주어를원래nickname삽입과연결해개별제안했다. source와고정초안은변경하지않았다. 전역치환규칙은적용하지않았다. ‘께서도,’의추가‘도’와‘의 경우,’도해당문맥에서개별재검토했다. native99px와의첫행결합은‘의’111px,‘님은/님이’123px. 어미/대명사등나머지말투는기존문구를유지했다. human_approved=false,NON-DISTRIBUTION,독립의미검수/사용자승인미완료다.

`prepare_wording_020.py`→`pending_insertion_500_020_wording_v1/report.json`:20개실제미적용ID/부모before문구/고정draft·sourceTPLhash/source literals/전체script단위보존/command skeleton/LF/edge/padding/3행132px/nativecapacitytemplate검사PASS. 20script의주변문구를포함한65unit을9archive의별도derived개발입력으로materialize했다.65개전부새번역수정이아니며20개만문구수정이다.

`preflight_wording_020.py`→`pending_insertion_500_020_wording_preflight_v1/preflight.json`:원본source에서9archive/65unit TextPetcompile PASS,source native roundtrip/한국어semantic·binaryroundtrip/제어명령/unselected script/nativecapacityproof를기존compile_archive가검증했다. 별도원본기반분석용subset이며500묶음·cumulativewriter등록·제품build/runtime가아니다. 019ROM/원본/이전고정초안/패키지는그대로다. 아직ROM수정0,500개완료0,새patch0.

다음은이개별wording입력의부모연결을020선택기/누적병합에서소비할수있게하고,새prefix/다른변수소비계약을분석해정확500개의비중복묶음을구성하는단계다. 이름앞‘가자,’7script는99+36=135px이므로current132px검사를무시하지않는다. 자동한글조합/commit/save/redisplay와전체자연사건·인간검수는여전히미완료다.

## 이전 조사 기록: 변수 재분류

`survey_batch500_020_variables.py`→`pending_insertion_500_020_variable_survey_v1/survey.json`은019 ROM/source 및 integration/name_display_runtime에묶인새조사다. donor018 CPU결과를019에서재실행한것으로보고하지않는다. 현재019의원래6개native code range·7literal·21byte descriptor·441metrics·42suffix lookup/record가source와byte동일함을검사하고기존채택native_bound를재계산해99px 확인했다. own019 이름진단2개가같은99px 이름출력을관찰한보고서와hashbinding을대조했다. 이applicability는 native6glyph 조건이며한글자동조합/저장/모든내비임의값/runtime의승격이아니다.

실제미적용variable-only는1,631script/4,550unit. conditionalnickname 후보2script/2unit. 다른/복수변수1,563script,미선택suffix16,same-rowprefix7,조사/단어문맥37,줄/폭5,중간명령1을별도미해결로분류했다. 기존static/layout14와2개의조건부후보는16개의조사대상일뿐compiler-admitted500이나게임전체잔여수아니다. readonly ROM/prose변경0.

`test_native_applicability_020.py -v`7fixture PASS:actual019 bound99 positive,code/literal/descriptor/width/suffixpointer/suffixbody 변경6가지거부. test는메모리상의복사본만변경하고source/ROM/evidence파일은보존한다.

주요다음관찰: same-rowprefix‘가자,’12+12+12=36px+native99px=135px로현재132px범위를넘는7개script가있다. widthgate를끄지않고정확문구/line assignment를개별검토해야한다. word suffix37에는66CA84:21:3 원문‘の\nそんけいする じんぶつは\nダレだ?’→초안‘ 말이다\n존경하는 인물은\n누구냐?’처럼소유의미를재검토할항목도있다. 현초안의미/폭을확인하기전그대로삽입하지않는다. 일괄prose치환규칙을채택하지않으며원본초안수정0. 다른변수의선택/공급/최대길이/renderer를분석해다음500개범위를만드는것과한글입력/저장통합이남았다.

기준 `poc/output/pending500_019_v1.gba`,SHA25638118847f8deeec0586b7c5b400a9dd15ec32a1875c174657fad3ee8029b8042,10,622units. `analysis/pending500_019_v1/integration.json`의실제500delta/artifact감사/독립repro에묶여있다. 신규이름runtime의개별표본/진단제한은019HANDOFF가권위며500개전체자연runtime완료로보고하지않는다.

`survey_batch500_016.py --base poc/output/pending500_019_v1.gba --proof analysis/pending500_019_v1/integration.json --out analysis/pending_insertion_500_020_survey_v1/survey.json` 완료. 원본/TPI/고정draft-first coverage/실제productlayout IDs와대조,변경된고정초안0. 기존raw/knownpointer/normaldialogue/비선택지·비변수/3행132px 범위의미적용candidate1script/1unit,exact500=false. 동일문구줄배치/protectededge 모델 `survey_batch500_017_layout.main(preserve_edges=True)`을새SURVEY/OUT에서실행해 `pending_insertion_500_020_layout_survey_v1/survey.json`에14script/14unit(untouched4,줄배치변경13)의구조후보를남겼다. ROM/prose변경0,compileradmission=false에해당하는조사상태이며전체게임미번역개수는아니다.

기존019516개조건후보나018586개를현행500개로재사용하지않는다. 다음은현재실제019에서적용된ID를제외한nickname/다른변수·choice/caller/storage/renderer 소비계약을분류하고그중미해결경계에대한증거를확장하는것이다. `survey_batch500_019_variables.py`는018evidence/baselineproof를명시적으로고정했으므로baseline문자열만바꾸어019에일반화하지않는다. 변수값공급/한글이름자동입력·commit/save/redisplay는주요미완료조건이다. 가능한candidate14를500개로부풀리거나안전검사를끄지않는다.

사용자500개단위/ROM반영정책유지.020선택/번역/compile/ROM/배포patch없음. 새BPS/xdelta/ZIP은사용자요청전금지. 원본·019·018·이전증거/세이브/ZIP보존. 다음재개는변수조사모델의실제019source/provideridentity·입력계약증거를연결해나머지미적용동적문구를분류하는단계다.
