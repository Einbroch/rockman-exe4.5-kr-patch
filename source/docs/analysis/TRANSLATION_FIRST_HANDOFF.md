# 전체 번역 우선 작업 — 2026-10-11

사용자의 최신 요청에 따라 **남은 일본어 전체 초안 작성 → 기술 검증 → 누적 ROM 적용 → 실제 화면 검증** 순서로 전환했다. 이번 진행분은 전체 완료가 아니며, 새 ROM은 만들지 않았다.

## 번역 초안 진행

기준 목록은 `full_scope_save_initialize_v1/literal_backlog.json`이다. 732개 archive, 31,907개 literal 중 기존 ROM 선택 2,596개, 미선택 일본어 27,452개, 기타 검토 1,859개를 그대로 유지한다.

이번에 개별 작성한 초안:

- `translations/remaining_navi_save_draft_ko.json`: 6DA21C의 남은 17내비 저장 대사 271개. source0의 checkNaviAll 분기로 화자를 확인했다. 저장/덮어쓰기/오류/재시도/변조 데이터 거부 의미를 구분한다.
- `translations/tournament_dialogue_draft_ko.json`: 6E93C8 토너먼트의 미선택 일본어 290개. 원본 mugshotShow로 화자를 확인하고, 일반·언더 중계와 내비별 전투·승패 말투를 구분한다. 일본어 글자 범위에 포함되는 점뿐인 두 literal도 명시적으로 처리했다.

이전 초안561개에 임무·메일373개, 스타맨·골드게시판219개, 배틀게시판·광장220개, 미스터리데이터·오피셜예선207개,블랙워크스형제·NPC222개, 오피셜접수·일반배틀162개, 언더배틀·상점·접수137개, 고난도통행시험122개와 개인정보24개와 특훈·대회장41개, 공장·장난감·라디오64개, 골프장69개, 자동차·정원64개와 배경·대회장54개, 철판주문·배틀·정지프로그램60개, 네이팜시험·미디어·블랙마켓67개를 추가해 **2,666개**가 되었다. 초안 미작성 일본어 **24,786개**. ROM 미선택 일본어는 여전히 **27,452개**다. 초안 상태는 전부 needs_review이며 인간 승인·배포 적격 판정이 아니다. 기존 같은 문구는 화자와 stable ID가 확인되는 후보만 참고하고 자동 일괄 치환하지 않는다.

### 후속: 임무·메일 373개

- `translations/protoman_missions_draft_ko.json`: 6DE3E0의 미선택 일본어 전체253개. SciLabMan 초상화가 설정된 root0/27/28과 checkProtoManMission의32분기33..64, 종료65를 읽고 지령·실패·성공·보상을 개별 작성했다. 보상에서 mugshotHide와 내비/아이템/금액 변수를 유지했다. 이는 과학 연구소 직원의 지령이며 브루스가 직접 말한다고 간주하지 않는다.
- `translations/story_mail_draft_ko.json`: 6DD9AC의 미선택 일본어 전체120개. PET 구매 안내, 오피셜 기밀 통지, 뉴스1..6호, 예선 자격 안내를 전체 편지 단위로 읽었다. 기존 칩 이름의 탭맨/셰이드맨/스파크맨/비디오맨/버너맨/켄도맨 표기를 후보로 참고했다. 이름 변수에는 님/님께서/님에 의해를 사용하고, 명시되지 않은 장소는 그대로 두었다.

제한 시간60/50/40/30/20분, 인터넷·언더인터넷의 번호, 범인 외형, 필수 삭제/조건부 삭제/체포 또는 삭제, 뉴스의 전개·불확실한 부활 가능성을 구분한다. 새 조직명·장소명과 문체는 인간 검토 전 후보다. 뉴스13의 약-40도는 음수 부호 검사도 보강했다. 신규 편지·임무의 실제 화면은 검증하지 않았다.

## 추적 및 검증

### 후속: 스타맨·골드 게시판 219개

- `translations/starman_fortune_draft_ko.json`: 6A3DD0 미선택 일본어129개 전체. 본문의 스타맨 자기 명칭, 랜덤 분기, 행운 아이템 위치1~4/5~8/9~12와 언더넷 분기, 미니게임 결과·보상·별명 변수를 읽었다. 시간차 출력 점도 각각의 literal로 작성하고 waitSkip 경계를 그대로 보존했다. 원문의 별 등급1..6과 예측/가능성, HP 메모리/제니/버그 조각 보상을 구분했다.
- `translations/gold_bbs_draft_ko.json`: 7011F0 미선택 일본어90개 전체. 게시판 안내와 질문·답변/격려·복귀/게이트 사용 안내를 게시글 단위로 읽었다. 자기 소개가 있는 텟신20/21/23과 코에츠27만 명시적으로 연결하고, 나머지는 작성자 추정을 하지 않았다. ASCII BBS01 ID placeholder는 미번역 문장으로 오인해 치환하지 않고 기타검토 목록에 남겼다.

스타맨 우메보시(매실 절임)의 보시/별 말장난은 음역 보존 후보이며 문화적 표현·팅클 등의 구호는 인간 검토가 남는다. 게시판 이름·텟신의 임다/슴다 말투·19의 하오 말투는 후보이지 승인된 문체가 아니다. 화/수요일 속성 말장난은 유지했다. 셀렉트→접수 시간→정해진 순서로 칩3개 입력, 금색 프로그램군의 사용 횟수 회복을 구분했다. 원문 인물의 소문은 실제 게임 조건으로 확정하지 않았다.

`check_draft`에 숫자 범위 구분자 보존 검사를 추가했다. 숫자가 같아도1~4를1/4로 바꾸면 실패한다. 새7개 회귀 항목(범위/등급·힌트/시간차 점/보상·별명/게이트 순서·횟수/작성자/placeholder) 추가, 총30tests PASS. 신규 JSON 재생성 내용 동일, 두 ROM 해시 불변. 실제 표시·입력·보상 실행은 이번에 검증하지 않았다.

### 후속: 배틀 게시판·광장NPC 220개

- `translations/battle_bbs_draft_ko.json`: 7000AC의 미선택 일본어125개 전체. 장비·카운터·자동 이동·도주·게이트·P.A·바이러스 공략·게이지 게시글을 질문/답변/인용 메일 단위로 개별 작성했다. 내비마다3장비 중2개 배정/R기본버스터, 상대 공격 순간의 칩 카운터, 도주 실패 후 파란 게이지 재시도, 방어 비용과 성공 방어 게이지 증가를 구분했다. 게이트 폴더30칩/사용 횟수/플러그아웃 회복과 답글의 회복 장소 설명을 둘 다 유지했다. 셀렉트→접수 시간→순서대로3칩→P.A 메모를 보존하고, 전기레인지 전뇌의 에브리데이 대회 인용은 사전 접수 불필요/주말 대회 무관을 유지했다. 기존 크랙아웃/보이즈봄/마루모코 후보를 참고하고 사무조군 등의 새 이름은 검토 대상으로 남겼다.
- `translations/plaza_npcs_draft_ko.json`: 7A32A8 미선택 일본어95개 전체. 각 script의 mugshotShow 초상화를 직접 연결해 쇼핑/허세와 사과/토너먼트 패배/시골 출신/프로그램의 사랑/노인의 시/쓰레기 수거일/쇼핑객/상위 대회 대사를 작성했다. 시간 분기와 초상화는 수정하지 않았다. source10이1/2로 분기하는 점과21의 노란 아가씨 언급을 추측으로 고치지 않았다. 한국어 사투리·세 줄 시는 문화·문체 검토 후보이며 일본5/7/5 형식 재현을 주장하지 않는다. 프로그램의 연애 금지 여부는 질문/조건문으로 남겼다.

초안 자체 읽기에서 새 표현3개와 이름 사무조군을 개별 수정했다. 기존 승인 번역의 일괄 변환이 아니며 source 필드는 그대로다. 신규8개 회귀 항목(장비/카운터·도주/게이지/게이트/인용행사/초상화/조건문·점/시·요일) 추가, 총38tests PASS. 재생성 JSON 내용 동일 및 원본·기준ROM 해시 불변. 신규 실제 화면/시간분기/게임 동작은 이번에 실행·검증하지 않았다.

### 후속: 미스터리데이터·오피셜예선 207개

- `translations/mystery_data_draft_ko.json`: 778CC0 미선택 일본어90개 전체. 조사/잠금/서브칩 효과/칩·서브칩·제니·아이템·버그 조각·강화 프로그램 획득과 소지 한도 거부를 개별 작성했다. printCurrentNavi/printItem/printChip/printBuffer 순서를 보존하고 변수에 따라 달라지는 조사를 단정하지 않는 쉼표·명사형으로 작성했다. 조사 문구는 원문しらべた의 과거형을 유지해 조사했다로 다듬었다. 시간차 점 literal과 wait10 경계는 그대로다. item44 잠금 해제 요구와 item42 함정 제거, flag7690/7691 및56/66 바이러스 데이터 삭제와59/69 바이러스 발견·배틀 분기를 구분한다.18:0의 원문 따옴표만 있는 literal은 기타검토로 보존했다.
- `translations/official_prelim_draft_ko.json`: 7AE0A0 미선택 일본어117개 전체. 적성 시험 내비6체 삭제, 트윈 록의 두 열쇠10/11, 도난 열쇠11 회수 후 보유·열쇠10 지급, 인터넷10·11의 두 무리와 인터넷12 경유를 구분했다. NormalNaviBrown 시험관/주변NPC/썬더맨/교환상을 원문 초상화에 연결하고 hidden 선택지·시스템 보상을 별도로 기록했다. 썬더맨 checkNavi6의 자기 내비 분기54와 도전50/승리51/패배52/배틀53, 교환상220·호출 상속221·품절222를 구분했다. 트윈 록은 기존 keyitem 표현을 후보로 참고했으며 블랙워크스 등의 용어는 승인 전이다. 변수 열쇠 이름은 추측해 고정하지 않았다.

두 신규 작성기 재생성 내용 동일, 원문/TPL/payload·ID/숫자/줄 수/제어 skeleton/미선택 literal/BDF·codec 보호 검사 PASS. 추가8개 회귀 항목은 조사 과거형·시간차 점, 함정·한도, 보상종류, 원문 따옴표 보존, 예선 조건·경유, 초상화·선택지·보상, 승패·품절, 선택지 공백·거절이다. 누적46tests PASS. 원본·기준ROM 해시 불변. 신규 실제 화면/아이템·이름 최대 폭/이벤트·배틀·보상·저장 실행은 미검증이다.

### 후속: 블랙워크스형제·주변NPC 222개

- `translations/blackworks_younger_draft_ko.json`: 7AF6D0 미선택 일본어92개 전체. 인터넷10 동생의 방해·패배·반성·형 처치 요청·열쇠11 반환·자수와 주변NPC, 우드맨의 일반/동일내비 도전·승패 및 서치맨 통행 시험70..75를 개별 작성했다. 원문兄가 인터넷11의 보스라는 점을 상대 archive와 연결했다. 서치맨은 인터넷2의 모든 바이러스를 제한 시간 내 저격하라고 하며 시간 수치는 원문에 없어 추가하지 않았다. 한 번이라도 플러그아웃하면 실패, 재도전은 인터넷2 복귀, 성공해야 통과하는 조건을 유지한다.
- `translations/blackworks_elder_draft_ko.json`: 7B09F4 미선택 일본어130개 전체. 심복3명과 인터넷11의 형/보스, 인터넷10 동생 정지 요청·두 번째 처치시 열쇠11 지급, 후회·훈련 선언, 주변NPC와 서치맨/나이트맨 일반·동일내비 도전·승패, 아이스맨 도움·성공·실패·거절, 상점221..225를 작성했다. 형/동생 어느 쪽을 먼저 쓰러뜨렸는지 flag1230/1253 분기와 아이템11 소유 검사를 함께 읽고 고정 순서를 만들지 않았다. NPC13의 소문은 전언으로 보존한다. 상점 선택지6개는 초상화가 계속 보이지만 player-choice이며 출처 NormalNaviYellow와 visible 상태를 함께 기록한다.221 종료 인사는223/224/225 호출 초상화의 상속이다.

표현 후보는 기존 블랙워크스/오피셜/언더인터넷·타깃/록온/저격을 참고했다. 형의 악당조 말투/동생의 거친 반성/우드맨의 대지/나이트맨의 기사도/아이스맨의 공손한 도움을 구분했지만 새 용어·구호·문체의 인간 승인은 아니다. 나이트맨59의ナイト는 직업/고유명 단정을 피한 나이트 후보이며 괴성은 음역 후보다. 레이디스 데이의 할인율이나 한국 요일은 추측하지 않았고 native weekday3/navi1, global6/7, 일반shop2/특별shop12 선택은 그대로다. 선택지 끝 두 공백과 상점의 마지막 빈 줄을 보존했다.

신규8개 회귀 검사(형제 관계·위치, 두 번째 처치·보상/초상화 복귀, 저격 조건·재도전, 내비·승패 화자, 아이스맨 조건부 통과, visible 상점 선택지, 선택지 공백·빈 줄, 소문·서비스 비율 미추가)를 포함해 총54tests PASS. 신규 작성기의 JSON 재생성 내용 동일, 원본·기준ROM 해시 불변. 실제 처치 순서/열쇠 지급/통행/미니게임/배틀/상점/최대 변수 폭/저장 회귀 및 화면은 미검증이다.

### 후속: 오피셜접수·일반배틀 162개

- `translations/official_entry_draft_ko.json`: 7B1FF4 미선택 일본어124개 전체. 오피셜 접수0/2..9의 최초 실력시험·관 특징 전언·언더인터넷4·삭제 요청·사무 착오와 초S급 셰이드맨의 정체 설명, 무료3->5와 유료8->4/자금부족6을 각각 작성했다. 최초 통신 알림0:3은 초상화 숨김/track219/문자효과음 비활성의 시스템 알림이며 player-choice가 아니다. 주말 접수 불가, 월~금/아침6시~밤12시, 등록 마감·bitmask4와 문 개방flag1598은 그대로다. 주변NPC의 농담·두려움, 네이팜맨/브루스의 일반·동일내비 도전/승패, 금색 프로그램의 칩 사용 횟수 회복, 다크로이드의 보고·소멸 불확실성·움직일 수 없는 답답함을 구분했다. 시간차 점3개는 wait30 경계를 보존한다.
- `translations/generic_battlers_draft_ko.json`: 7B0638 미선택 일본어38개 전체. HeelNaviPurple의 매주 기다리는 배틀, 눈맞춤으로 시비 걸기, 옛 지인인 척하는 나야 나 배틀3그룹을 각각 acceptance/refusal/win/loss와 함께 읽었다. 매주 이날은 원문에 요일이 없으므로 추가하지 않았다. 여름 방학의 추억은 화자의 가장 대사이지 플레이어의 실제 과거로 확정하지 않는다.100万回의100은 유지해100만 번으로 작성하고, 팔 하나나 둘 위협은 원문 의미를 보존했다. 나야 나 살법은 오레오레 말장난을 연결한 초안 후보이며 문화·구호 검토는 남는다.

신규 작성기/JSON은 원본/TPL/payload 및 source/ID를 보존하며 기존 셰이드맨/다크로이드/브루스 등은 기존 자산 후보를 참고했다. 새로운 인간 승인·분포 완료 판정은 아니다. 사과·시험용 내비가 진짜 흉악범으로 잘못 전달된 의미를 숨기지 않았으며 금색 프로그램은 사용 횟수 회복이지 HP·칩 추가나 세이브 삭제가 아니다. 동작명령 callClearBattleChipGateHistory와 전투 데이터/선택지/초상화는 수정하지 않았다.

신규8검사(무료·유료·부족, 착오·관 전언·S급, 요일·시각, 통신/선택지 화자, 회복·불확실성·점, 동일내비/거절, 가장·과장·살법, 선택지 두 공백)를 포함해62tests PASS. 두 JSON 재생성 내용 동일와py_compile PASS, 원본·기준ROM 해시 불변. 새로운 실제접수·금액차감·주말/시각·배틀·게이트회복·저장·화면 검증은 수행하지 않았다.

### 후속: 언더인터넷 배틀·상점·접수 137개

- `translations/undernet_battlers_a_draft_ko.json`: 7B32B0 일본어18개 전체. HeelNaviPurple 두 배틀의 선택·거절·시작·승패를 작성했다. 짧게 뭉친バトオペセイン을 배틀오페세인 후보로 유지하고, 승부에 졌으나 싸움에는 이겼다는 자기합리화도 실제 승패를 뒤집지 않고 보존한다.
- `translations/undernet_shop_draft_ko.json`: 7B3490 일본어21개 전체. 지옥의1번지 위협·프로그램의 웃음, 금색 프로그램의 게이트 칩 사용 횟수 회복, 서브칩 상점의 일반shop7/특별shop17과 품절·종료 인사를 작성했다. 원문weekday3와navi1 분기는 그대로이며 할인율을 만들어 넣지 않았다.223/224 선택지4개는 초상화 PurpleNavi가 visible여도 player-choice로 기록한다.221은 상점 caller의 초상화를 상속한다. 마지막 빈 줄을 보존했다.
- `translations/undernet_battlers_b_draft_ko.json`: 7B39D0 일본어21개 전체. 일반 인터넷/언더 대비의 HeelNaviBlack과 냄새로 실력을 판별한다는 HeelNaviPurple을 구분했다. 군자는 위험한 곳을 가까이하지 않는다는 속담, 존대·익살 말투는 초안 후보이며 승인 전이다.
- `translations/undernet_battlers_c_draft_ko.json`: 7B469C 일본어41개 전체. 검은 내비의 위협, NormalNaviYellow의 어둠 추종, 끊기는 말투, 선택지 없는12 전투와 공손한 블러디 파티15..18를 구분했다.12와16의 native battle178/global27=656 공유는 원문 그대로이며 임의로 고치지 않았다. 플레이어도 같은 부류라는 말은 화자의 주장이지 새로운 플레이어 설정으로 확정하지 않는다.
- `translations/undernet_entry_draft_ko.json`: 7B4A6C 일본어36개 전체. 진짜 실력 요구와 원문flags2..50 검사,flag1762 이후 안내,등록비2000제니와 자금부족·거절·접수마감,월~금/아침6시~밤12시,프로그램 수면을 작성했다. 오피셜의 무료 최초/1000제니 정책을 옮겨 넣지 않았으며 bitmask8과 주말0/6 거절을 보존했다. 실제 요구 승수·보스 수를 추측해 대사에 추가하지 않았다.

신규137개는 needs_review/NON-DISTRIBUTION이며 원본/TPL/payload·source/ID/숫자/줄 수/제어 skeleton/미선택 원문·글리프/codec 보호 검사 PASS. 신규8검사(2000제니,요일·시간·수면,visible 상점선택·상속,칩횟수회복,축약구호·아이러니,냄새·속담·대비,화자·강제전투·공손말투,공백·빈줄)를 포함해70tests PASS. 재생성5JSON 내용 동일 및py_compile PASS, 원본·기준ROM 해시 불변. 새 배틀/상점/회복/접수차감/조건·clock/저장·실제화면은 미검증이다. 언더/일반 인터넷·지옥의1번지·봉주르·블러디 파티·문화/말투 후보는 인간 검토가 남는다.

### 후속: 고난도 통행시험 122개

- `translations/hard_access_tests_a_draft_ko.json`: 7B5328 미선택 일본어55개 전체. 넘버맨의 학력 시험/성공·실패·거절, 메탈맨의 오퍼레이터 조작 실력/주먹 떨림/재훈련, 서치맨의 인터넷7 저격 시험·반복 설명·성공/실패/재도전을 작성했다. 이전 쉬운 인터넷2 시험과 목적지를 섞지 않았으며 제한 시간의 실제 숫자는 원문에 없어서 추가하지 않았다. 원문SearchMan 초상화/메시지 중복 명령도 그대로 보존했다.
- `translations/hard_access_tests_b_draft_ko.json`: 7B5CC0 미선택 일본어67개 전체. 아이스맨의 조건부 도움/통과/실패, 네이팜맨의 언더인터넷2 바이러스 전멸과 프로그램 대여·플러그아웃금지/성공·실패·재도전, 윈드맨의 오퍼레이터 조작/바람·감탄 시험과 결과를 작성했다. 네이팜맨14 재도전 선택지는 mugshotHide 없이 표시되므로 visible 초상화와 player-choice를 함께 기록했다.12 반복 안내에는 원문에 없는 프로그램 대여 문구를 덧붙이지 않았다. 메탈맨/윈드맨은 내비 상대 일반배틀이 아니라 오퍼레이터가 화자를 조작하는 시험이다.

전체6미니게임의 hard=true 및flags5507/5571/5140/6403/6217/4958/선택·취소·통과·실패 분기와숫자1/7/2를 보호했다. 넘버맨がくりょく의 학력은 학업 실력 문맥의 초안 후보이지 졸업 자격 조건 확정이 아니며 기능 표현·문체 인간 검토는 남는다. 네이팜 프로그램은 기존 이름 후보를 참고했다. 기존 번역을 화자와무관하게 일괄 치환하지 않고 각ID별로 작성했다.

신규8검사(6화자,서치인터넷7,네이팜언더2·금지,오퍼레이터대상,아이스성공·실패,visible재도전선택,hard=true소스보존,공백·거절) 포함78tests PASS. 신규2JSON 재생성 내용 동일 및py_compile PASS, 원본/TPL/payload/source/ID·미선택원문·제어skeleton·글리프/codec 검사 PASS, 원본·기준ROM 불변. 새 시험 입력/성공·실패·시간제한·플러그아웃/통행·저장·실제화면은 미검증이다.

### 후속: 개인정보 수정 안내와 입력 전 항목명 24개

7B67C8 전체 일본어24개를 `translations/profile_editor_draft_ko.json`에 작성했다. MrProgGreen의 개인정보 관리/이름·직업 수정/설정 화면/거절 안내와20..35 항목명을 개별 작성했다. 플레이어 이름 삽입 경계16:0/1 및 님의 연결, visible 초상화의 플레이어 선택지·단일 후행 공백, startProfileEdit/targets17/40/global21/flags512/7701을 보존했다. アニ/アネ는 플레이어 성별을 추측하지 않고 형·오빠/누나·언니 후보로 남겼다. TV 및 학교명? 회사명? 원문의 불확정 구분도 유지했다.

입력 전 라벨16개는 번역 후보만 작성했으며 consumer_status=unresolved-input-before-label이다. 일반 대사/실제 사용 여부를 확정하지 않으며 자판 hook·조합·저장/재로드가 구현됐다는 뜻도 아니다. 신규2검사 포함80tests PASS, 재생성 JSON 동일 및py_compile PASS. 원본/TPL/payload/source/ID/줄 수·제어 skeleton·미선택 원문·글리프/codec 보호 검사 PASS, 원본·기준 ROM 불변. 개인정보2문구 추가 배치 검토 대상이며 실제 이름 삽입 폭/설정 실행/화면·저장은 미검증이다.

### 후속: 비밀 특훈·에브리데이 대회장 41개

`translations/secret_training_draft_ko.json`은7B6E20 일본어11개 전체: NormalNaviYellow의 비밀 특훈/넷배틀 수락·거절/오퍼레이션 칭찬·추가 연습을 작성했다. 배틀globals24=179/27=657, flags1806/7701과 초상화 없는 선택지 후행2공백을 보존했다.

`translations/everyday_venue_draft_ko.json`은7B6F9C 일본어30개 전체: 전기레인지 프로그램, 대회장·관중, item19 보상 소문, 우승·패배 안내, 일반/레이디스 데이 상점을 작성했다.14:1의 원문 시작 인용부호는 미선택으로 유지했다. 아이템 뒤 조사 대신 인용부호+쉼표를 써 값에 따른 받침 문제를 피했으며 실제 표시 검토는 남는다.20 선수 호칭은 printCurrentNavi 뒤 별도 literal이다. 상점 선택지는 visible 초상화여도 player-choice로 기록했고221 거절 인사는223/224의 상인 초상화를 상속한다.

weekday3/Navi1과shop8/18 분기를 사용자 입력 성별로 바꾸지 않았다. 대회 시간9/13/16/20시의 원본 검사와flag1854, item19, 애니메이션·배틀·상점 명령은 그대로다. 할인율/상품값/자격을 추측하지 않는다. 뚝배기·중화팬·곰솥, 에브리데이 토너먼트·레이디스 데이 표기와 구호는 인간 검토 후보다. 신규3검사 포함83tests PASS,2JSON 재생성 동일/py_compile PASS. 원본/source/TPL/payload/ID/줄 수/제어/미선택원문/글리프·codec 보호 및 원본·기준ROM 불변 검사 PASS. 새4문구 배치 검토 추가. 실제 대회/배틀/상점 구매·시간·보상·저장·화면은 미검증이다.

### 후속: 공장·수련배틀·장난감상점·라디오 64개

공장7B76D4/7B7AF0/7B7EF8의4문구를 `factory_panels_draft_ko.json`/`factory_passion_draft_ko.json`/`factory_parts_draft_ko.json`에 작성했다. 철판 공장 전뇌 세계와 메탈 패널, 철도 녹일 열정의 비유, 배·자동차 부품을 구분한다.

`translations/appliance_battlers_draft_ko.json`:7B827C22문구. NormalNaviYellow 수련 내비의 ッス 말투 후보, 실전·거절·패배·위팔 두갈래근 자랑과PurpleNavi 바이러스 소유자의 심사위원 특별상·승패 대사를 개별 작성했다. 선택지 いやッス는 다른 화자의 장면에서도 원문 특성을 유지하고 player-choice로 기록했다. 배틀180/181, globals27=658/659, flags1806/7701 보존.

`translations/toy_parts_shop_draft_ko.json`:7B84C819문구. MrProgGreen 장난감 부품·로켓 펀치 관리와NormalNaviYellow 넷 상인, 품절·일반·레이디스 데이·기분 좋은 특별 판매를 작성했다. global7=2/global6=1은 weekday3/Navi1 검사보다 먼저225로 갈 수 있으며 실제 의미는 단정하지 않았다. 일반shop3/특별shop13, 선택지 후행2공백·visible 초상화,221 상인 초상화 상속을 보존한다. 할인율·새 상품을 추측하지 않는다.

`translations/radio_venue_draft_ko.json`:7B8AB419문구. 소리 담당 프로그램과 고장 난 튜너 동료·이상음, 대회장 안내·관중·스트레스 해소·응원·재충전 비유·우승/패배를 작성했다. flag1877과9/13/16/20시 검사, printCurrentNavi 뒤 선수 호칭·애니메이션 명령을 보존했다.

전체64개 needs_review/NON-DISTRIBUTION. 신규4검사 포함87tests PASS,6JSON 재생성 동일 및py_compile PASS. 원본/TPL/payload/source/ID·숫자/줄 수·미선택원문·제어skeleton·글리프/codec 검사 PASS, 원본·기준ROM 불변. 신규23문구 배치 검토 대상이며 실제 배틀·상점구매·특별조건·시간·이름 표시·저장·화면은 미검증이다. 임다/슴다 말투, 메탈 패널·위팔 두갈래근 용어, 뒷세계 심사회·에브리 응원·고장 이상음 후보는 인간 검토가 남는다.

### 후속: 골프장·배틀·서브칩상점·홈페이지 바닥 69개

- `translations/golf_lawn_draft_ko.json`:7B9104 일본어3개 전체. 잔디 성장/시듦을 살피는 MrProgGreen의 관리 업무와 주의를 작성했다.
- `translations/golf_battlers_draft_ko.json`:7B94AC 일본어26개 전체. NormalNaviYellow의 친근한 배틀, HeelNaviPurple의 매혹적인 배틀 세계/뛰는 놈 위에 나는 놈 비유, HeelNaviBlack의 기세·패배/사교댄스 도발을 구분했다. 선택지는 player-choice·hidden이며 후행2공백·native battles182/183/184, globals27=660/661/662, flags1806/7701을 보존했다.
- `translations/golf_course_shop_draft_ko.json`:7B9748 일본어16개 전체. 코스 난도 조절 업무, 서브칩 상인과 품절/일반/레이디스 데이·거절을 작성했다. weekday3/Navi1/일반shop8·특별shop19는 원문 그대로다. 이전 대회장의shop18로 바꾸지 않는다. visible 초상화 선택지와221 상인 초상화 상속을 따로 기록했다.
- `translations/golf_homepage_floor_draft_ko.json`:7B9C94 일본어24개 전체. 고객정보 기밀 업무와GoldProg 홈페이지 꾸미기·바닥색 변경/파랑·빨강·초록·취소/완성·거절을 작성했다. HP는 바닥색 문맥과callSetHomepageFloor로 홈페이지임을 확인했으며 체력 회복으로 번역하지 않는다. 대상12/13/14/15, 색상type0/1/2, disableB=true, grid spacePx24/12, 빨강·취소 후행줄바꿈과sound150/textSFX disable/enable을 보존했다.

신규5검사 포함92tests PASS,4JSON 재생성 동일/py_compile PASS. 원본/TPL/payload/source/ID/숫자·줄 수/제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 새19문구 배치 검토 추가. 속담·사교댄스 도발, 바닥색 구호·샤라랑 효과음은 인간 검토 후보이며 실제 배틀·상점 구매·바닥 적용·색상 재표시·저장/재로드·화면은 미검증이다.

### 후속: 자동차·배틀·홈페이지 무늬·정원 64개

- `translations/car_controls_draft_ko.json`:7BA26C6문구. 가속과 브레이크가 서로를 설명하는 위치·역할을 작성했다. 브레이크가 없으면 못 멈춤, 가속이 없으면 못 움직임을 구분한다.
- `translations/car_pink_battler_draft_ko.json`:7BA6608문구. NormalNaviPink 바이러스 배틀 권유/거절·시작·분함·웃음과 플레이어 선택지를 작성했다. 배틀185/global27=663 보존.
- `translations/car_homepage_patterns_draft_ko.json`:7BA7A023문구. 선루프 프로그램은 없어도 차는 달린다는 대사와GoldProg 홈페이지 바닥 변경을 작성했다. 빨강&파랑/흰색&검정/무지개/취소 순서, types3/4/5, spacePx24/24, disableB=true, 효과음150·textSFX 명령을 보존했다. 골프장의 단색types0/1/2와 섞지 않는다.
- `translations/car_rival_battlers_draft_ko.json`:7BACD820문구. NormalNaviYellow와HeelNaviPurple이 서로보다 강하다고 주장하는 대사, 플레이어에게 패배한 뒤에도 상대보다 강하다는 허세, 승리·수락·거절을 작성했다. 배틀186/187·global27=664/665,flags1806/7701 보존. 실제 순위로 확정하지 않는다.
- `translations/garden_blades_draft_ko.json`:7BAEF83문구. 고속 회전 칼날·잡초를 단칼에 베는 프로그램의 소리와 자랑을 작성했다.
- `translations/water_cleaning_draft_ko.json`:7BB31C4문구. 강력한 물살·막힘 방지·흘려보냄·세척을 작성했다. 원문이 기기를 명시하지 않으므로 변기/세탁기 설정을 추가하지 않았다.

신규4검사 포함96tests PASS,6JSON 재생성 동일/py_compile PASS. 원본/TPL/payload/source/ID/숫자·줄 수·선택지공백/제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 새17문구 배치 검토 대상. 핑크 웃음·분함, 제초·물소리와GoldProg 구호는 인간 검토 후보다. 실제 배틀·바닥 무늬 선택/반영·저장/재로드·화면은 미검증이다.

### 후속: 배틀·탈취·홈페이지 배경·물총·대회장 54개

- `translations/moth_battler_draft_ko.json`:7BB6C8 일본어10개 전체. NormalNaviYellow의 자기 실력 시험/거절을 강함으로 해석하는 허세/나방처럼 날고 모기처럼 쏜다는 익살/패배·꿈·최강 자랑을 작성했다. 원문ガ/カ를 나비/벌로 바꾸지 않았으며 battle188/global27=666/flags1806/7701 보존.
- `translations/homepage_background_draft_ko.json`:7BB878 일본어24개 전체. MrProgGreen의 탈취력과GoldProg 홈페이지 배경색 변경/록맨·벚꽃·전뇌·취소/효과음·완료·거절을 작성했다. callSetHomepageBG types0/1/2이며 이전 바닥callSetHomepageFloor와 구분한다. grid spacePx12/46,disableB=true와sound150/textSFX 경계·선택지 줄바꿈을 보존했다. サクラ는 테마명 벚꽃 후보이며 실제 배경 도안/표현 확인이 남는다.
- `translations/water_gun_draft_ko.json`:7BBE54 일본어3개 전체. 물총의 바늘구멍 정밀도·겨냥과 소리를 작성했다. 실제 기기명은 원문에 없어서 추가하지 않았다.
- `translations/cold_venue_draft_ko.json`:7BC27C 일본어17개 전체. 추운 프로그램 한마디와NaviGirlOrange 안내/우승·패배, 관중6화자의 흥분·혈관/코피 비유·응원·배틀 학습을 작성했다. flag1906/time9/13/16/20,printCurrentNavi 뒤 선수 호칭과 애니메이션 명령 보존. 냉장고 설정이나 체력 기능을 추측해 넣지 않는다.

신규4검사 포함100tests PASS,4JSON 재생성 동일/py_compile PASS. 원본/TPL/payload/source/ID/숫자·줄 수·선택지공백/제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 신규12문구 배치 검토 추가. 배틀 익살·관중 소리·벚꽃 테마/GoldProg 구호는 인간 검토 후보이며 실제 배틀/시간/배경 적용·재표시·저장·화면은 미검증이다.

### 후속: 철판 주문·공장배틀·정지프로그램·힐배틀 60항목

- `translations/factory_orders_draft_ko.json`:7BC8704문구. 공장에서 만든 철판 주문을 전 세계에서 받는 프로그램의 바쁜 말투를 작성했다.
- `translations/factory_battlers_draft_ko.json`:7BCC3428문구. NaviGirlOrange 바이러스와 플레이어의 강함 비교, HeelNaviPurple의 간결한 배틀 권유/내 패배·네 패배, HeelNaviBlack의 무술 기합·공격 칭찬·빈틈 도발을 구분했다. 배틀189/190/191,globals27=667/668/669·flags1806/7701·hidden 플레이어선택 보존.
- `translations/disabled_program_draft_ko.json`:7BCEBC2항목.6점 침묵과 움직이지 않고 바이러스에 당한 것 같다는 설명을 작성했다. mugshotAnimation0/초상화 숨김을 보존하고 hidden 설명을 system-observation으로 기록했다. 죽음/수리 방법을 단정하지 않는다.
- `translations/heel_battlers_draft_ko.json`:7BD24026항목. 첫 번째와 두 번째 HeelNaviPurple이 같은 초상화라도 두 번째 オラ/オメー의 구어 후보를 별도로 작성했다. HeelNaviBlack의 짧은 명령·6/9점 침묵·기/카 반복 소리를 보존했다. 배틀192/193/194,globals27=670/671/672·flags1806/7701·선택지 후행2공백·행/페이지 경계는 그대로다.

60항목에는 기존 일본어 범위 카탈로그가 중점 기호로 분류한 침묵도 포함된다. 모두 새 자연어 문장이라는 의미가 아니며 원본source와 분모를 보존했다. 신규4검사 포함104tests PASS,4JSON 재생성 동일/py_compile PASS. 원본/TPL/payload/source/ID·숫자/줄 수/선택지공백·제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 신규12문구 배치 검토 대상. 말투/무술기합/반복소리는 인간 검토 후보이며 실제6배틀·정지프로그램 경로·저장·화면은 미검증이다.

### 후속: 일반 네이팜 시험·스테레오·구형 TV·블랙마켓 67개

- `translations/napalm_normal_passage_draft_ko.json`:7BD4B036개 전체. 네이팜맨의 인터넷1 바이러스 전멸/제한시간·프로그램 대여·플러그아웃금지/반복 설명·성공/실패·재도전을 작성했다. hard=false/flag6194를 유지하고 이전 고난도 언더인터넷2/hard=true/flag6217과 구분했다. 반복2에는 원문에 없는 대여 문구를 추가하지 않았다. 재도전4의 선택지는 hidden이며 이전 고난도14의 visible과 다르다. 시간의 숫자는 원문에 없어서 추가하지 않는다.
- `translations/stereo_program_draft_ko.json`:7BDC905개 전체. 스테레오 프로그램의 오 예 베이비/끊어 부르기/좋은 소리/땡큐를 각 literal·페이지 경계를 유지해 작성했다.
- `translations/old_tv_program_draft_ko.json`:7BE0CC4개 전체. 채널 변경을 귀찮아하는 구형TV의 느슨한 반말, 얇지도 액정도 아니라는 불평을 작성했다. 같은MrProgGreen이라고 이전 공손한 관리 프로그램 말투를 일괄 적용하지 않았다.
- `translations/black_market_draft_ko.json`:7BE51822개 전체. HeelNaviBlack 어둠의 상인/돈·거래/품절·거절/일반·레이디스 데이·기분 좋은 특별 판매를 작성했다. shops4/14,global7=2/global6=1의225 우선 분기·weekday3/Navi1·visible 선택지/221 초상화 상속·후행2공백·빈줄 보존. 사용자 입력 성별이나 할인율을 추측하지 않는다.

신규4검사 포함108tests PASS,4JSON 재생성 동일/py_compile PASS. 원본/TPL/payload/source/ID·숫자/줄 수·선택지공백/제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 신규17문구 배치 검토 추가. 스테레오 리듬·TV 말투·블랙마켓 이름/서비스 표현은 인간 검토 후보이며 실제 시험·시간·플러그아웃·통행·상점구매·저장·화면은 미검증이다.

### 후속: 홈페이지 배경·바이러스 배틀·오르간·쓰러진 나비·어둠 배틀 79개

- `translations/homepage_background_b_draft_ko.json`:7BEB1821개 전체. 기존7BB878의 배경 안내와 동일한 문구를 유지하고 메툴/브루스/푸른 하늘 메뉴를 작성했다. BG타입3/4/5, spacePx12/24, disableB=true, sound150과 후행줄바꿈을 보존했다. 실제 그래픽 테마·메뉴 폭과 명칭의 인간 검토는 남는다.
- `translations/purple_pink_battlers_draft_ko.json`:7BF01818개 전체. 보라색 여자나비의 주간 모임/실력 시험과 핑크 일반나비의 먹이/목숨 위협을 다른 말투로 작성했다. 배틀195/196·global27=673/674, 결과2/3·6/7, 선택지공백·초상화숨김 보존. 주간 모임의 요일이나 실제 피해를 추가하지 않았다.
- `translations/organ_venue_draft_ko.json`:7BF25819개 전체. 파이프오르간의 과거 연주·현재 쉰 소리·망가짐을 기다리는 서술, 대회장 안내/응원·삭제 구호·칭찬·결과를 작성했다. flag1929가 시간9/13/16/20 검사에 우선하는 구조와 animation24/25를 유지했다. 수리 임무나 보상을 만들지 않았다. オモテ는 정확한 지역명을 추가하지 않은 ‘양지’ 후보다.
- `translations/fallen_navi_draft_ko.json`:7BF8C03개 전체. visible 침묵과 hidden 응답없음/오래전 숨이 끊어진 것 같다는 관찰을 분리했다. animation0과 ようだ의 추정 의미 보존. 이전7BCEBC의 바이러스에 당한 정지 프로그램과 다르다.
- `translations/dark_heel_battlers_draft_ko.json`:7BFC5018개 전체. 같은HeelNaviBlack 초상화의 두 별도 배틀 제안·거절·각 결과/어둠의 힘 구호를 작성했다. 배틀197/198·global27=675/676, 결과2/3·6/7, 선택지width9/8·후행2공백 보존. 새 기술명·다크칩·플레이어 피해/능력을 추측하지 않았다.

신규5검사 포함113tests PASS,5JSON 재생성 동일/py_compile PASS. 누적2745개 초안, 미작성24707개. 새22문구(보라/핑크배틀6·오르간대회장9·쓰러진나비1·어둠배틀6) 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·선택지공백/제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 초안은 needs_review이며 실제 BG변경·배틀·시간·관객·저장·화면 검증은 하지 않았다.

### 후속: 웃는 프로그램·윈드맨 비행 요청·브루스 임무 현장 118개

- `translations/chuckling_program_draft_ko.json`:7BFE4C2개 전체. MrProgGreen의 두 웃음만 작성했다. 짧은 원문에 없는 기기 정체나 임무를 추측하지 않았다.
- `translations/windman_flying_program_draft_ko.json`:7C066810개 전체. 날아오르려는 프로그램, 윈드맨의 도움 제안·수락/거절·인터넷1 의식 안내를 작성했다. printPlayerNickname 뒤 ‘よ’는 고정 받침 조사 대신 쉼표로 작성했으며 실제 이름 폭 검증은 남는다. 프로그램→윈드맨→hidden선택지→프로그램→윈드맨 초상화 경계, flag4929/7701·width8·후행2공백 유지. 의식 시간/보상을 추가하지 않는다.
- `translations/protoman_field_encounters_draft_ko.json`:7C0F8C의107개 일본어 literal 중106개 작성. 성공/실패 보고와10~41의 바이러스 발견·오피셜 불심검문·각 상대의 거절/공격 대사를 작성했다. 모든32개 현장 script의 global15=513/flag5473/7701을 유지한다. 브루스의 공식 보고 존댓말과 상대를 향한 단호한 말투를 구분하고, literal 직전 실제 초상화를 기준으로 화자를 지정했다.25의 거짓 투항 후 기습,28의 이름 없는 ‘그곳’,32 그림자 군단,30 바리바리본,33/36 언더와39 언더인터넷 구분을 보존했다. 7C0F8C:0:0은 임시 배틀 테스트이므로 소비 경로를 확인하기 전 선택하지 않았다.
- `7C0970:0:0` 임시 미니게임 시작 문구도 consumer 미해결로 원문 유지한다. 두 임시 항목은 전체 미번역 분모에서 제외하지 않는다. 이들은 번역 초안이 갖춰진 일반 현장 대사와 별도 상태로 추적한다.

신규4검사 포함117tests PASS,3JSON 재생성 동일/py_compile PASS. 누적2863개 초안, 미작성24589개. 새25문구(윈드맨3·브루스현장22) 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·선택지공백/제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 초안은 needs_review이며 실제 의식/닉네임/임무·검문·결과·저장·화면은 검증하지 않았다.

### 후속: 롤·스타맨 보상·썬더맨/우드맨 강화·브루스 귀환 59개

- `translations/roll_heart_rewards_draft_ko.json`:7C6BC021개 전체. 하트 발견/조사와 강화 프로그램·제니·버그 조각의3개 보상 경로, 닉네임 뒤 롤의 축하를 작성했다. printCurrentNavi/printPlayerNickname·item33·buffer3·수량4294967295와10프레임 점 대기9개, callRollHeartDataErase3개 유지.
- `translations/thunderman_strengthening_draft_ko.json`:7C6D7C7개 전체. 미약한 전기 감지·item7 안치·전기 유입·흡수 강화 작성. 아이템명은 printItem 그대로 유지하며 명칭을 추측하지 않는다. 삽입 뒤 에서/콜론으로 받침 의존 조사를 피했다.
- `translations/protoman_failed_return_draft_ko.json`:7C6E502개 전체. 임무 실패·사과·귀환을 공식 보고 말투로 작성했다. 성공/보상/재도전 선택지를 추가하지 않는다.
- `translations/woodman_strengthening_draft_ko.json`:7C6E948개 전체. 양분/전뇌 식물·item6 심기·빠른 성장·음이온/치유의 힘·우드맨 강화를 작성했다. 음이온은 원문의 게임 내 서술로 보존하며 외부 건강효과를 주장하지 않는다. item33·scene연출 유지.
- `translations/starman_star_rewards_draft_ko.json`:7C6F9021개 전체. 스타 데이터 조사와 같은3보상 경로, 스타맨의 운 좋은 발견 축하 작성. 롤의 닉네임 축하 문구와 혼동하지 않고 callStarManStarDataErase 및 object연출 유지.

system-narration은 hidden 또는 script 내 초상화 미표시(not-shown-in-script)인 실제 서술로 구분한다. 썬더맨/우드맨의1·2 script 앞부분에는 직전 초상화를 임의 상속하지 않는다. 변수 이름 뒤 쉼표·아이템명 뒤 콜론은 후보 표현이며 이름/아이템/수량의 실제 폭과 표시 검증은 남는다.

신규4검사 포함121tests PASS,5JSON 재생성 동일/py_compile PASS. 누적2922개 초안, 미작성24530개. 새12문구(롤3·썬더맨1·우드맨2·스타맨6) 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 초안은 needs_review이며 보상 한도·데이터 수집·아이템 안치/성장·강화·귀환·이름·저장·실제화면은 검증하지 않았다.

### 후속: 바이러스 버스팅 연습·재시도·성공·섀도맨 의뢰 실패 186개

- `translations/shadowman_failed_request_draft_ko.json`:7C714C1개 전체. 섀도맨의 의뢰 실패와 분함을 작성했다. 연습 재시도35와는 별도 장면이며 flag3863이나 보상을 추가하지 않았다.
- `translations/virus_practice_intro_retry_draft_ko.json`:7C7188130개 전체.0~20의21나비 첫 연습 안내와21~41의 실패 후 재시도 반응 작성. checkNaviAll 두 분기의21명·unused1/2 continue와42개 flag3863 유지. 수사 질문이 있어도 실제 메뉴가 없으므로 수락/거절·건너뛰기 선택지를 만들지 않는다.
- `translations/virus_practice_success_draft_ko.json`:7C802C55개 전체.21나비의 성공 평가·앞으로 나아가기·기초/실력/꽃 비유 작성.0/1/2/4/7/10/13의 nickname 뒤 쉼표 경계와7개 printPlayerNickname 유지. 성공 스크립트에 재시도 flag3863을 추가하지 않았다.

바이러스 버스팅/넷 배틀러/오퍼레이팅/오퍼레이터는 서로 다른 원문 용어의 후보 표현이다. 거츠맨 가스·아쿠아맨 퓨·정크맨의 더듬는 로봇 말투·아이스맨의 어린 존댓말, 포르테의 몸으로 익히라는 위협, 네이팜맨의 질책, 플랜트맨 꽃 비유를 구분했다. 윈드맨 いろは는 ‘기초’ 후보로 자연스럽게 옮겼다. 말투·어미·관용구는 아직 인간 승인 상태가 아니다. 아쿠아맨의 예측은 ‘것 같아’를 유지해 실제 무적 보장으로 바꾸지 않는다.

신규5검사 포함126tests PASS,3JSON 재생성 동일/py_compile PASS. 누적3108개 초안, 미작성24344개. 새57문구(연습/재시도37·성공20) 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 실제 인터넷 첫 진입·연습배틀·실패/성공·나비 해금·닉네임·저장·화면은 검증하지 않았다.

### 후속: 셰이드맨 관 조우 102개

`translations/shademan_coffin_encounter_draft_ko.json`:7C8570102개 전체.0~20의21나비 관/어둠 반응, hidden21·셰이드맨22/23,24~44의21나비 전투 반응,45의셰이드맨 위협을 작성했다. 두 checkNaviAll의21명·unused1/2 continue,21개 target21·21개 target45 및23→24, 페이지/초상화/대기·숫자100을 유지했다.

hidden21은 이전 활성 나비에게 임의 상속하지 않는다. 잠을 방해한다는21과 깨운 것을 후회하라는22의 문맥에서 셰이드맨으로 추정했지만,21에는 명시적 jump22가 없고 실제 장면전환은 미검증이다. speaker 후보ShadeMan·origin_portrait=None·hidden과 추정 근거/한계를 함께 보존했다.

윈드맨의 사악한 기운, 네이팜맨의 통조림/관째 화장 비유, 플랜트맨의 매장/아름다운 흩날림, 나이트맨의 철구 녹, 롤의 여자 체면 표현을 보존했다. 파이어맨의 괴물은 불에 약하다는 발언은 화자 허세이지 검증된 속성 공략이 아니다. 메탈맨 심두멸각·섀도맨9음절구 주문 음역은 인간 검토 후보이며 실제 기술명을 추가하지 않았다. 아이스맨 얼리기와 일렉맨100만 볼트/네이팜맨100만 년의 수치를 유지했다.

신규4검사 포함130tests PASS,JSON 재생성 동일/py_compile PASS. 누적3210개 초안, 미작성24242개. 새25문구 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어skeleton·미선택원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 실제 관 조우/숨겨진 목소리·출현·나비 분기·전투·저장·화면은 검증하지 않았다.

## 후속: 셰이드맨 승리 후 귀환98문구

`translations/shademan_victory_return_draft_ko.json`:7C90E0의22스크립트·98개 미선택 일본어 전체. 셰이드맨의 무한한 어둠 주장과21나비의 안도·허세·감사·공포, 인터넷12 귀환 및 오피셜 토너먼트 출전 등록 안내를 개별 작성했다. 나이트맨의 처치 보고/등록은 별도 페이지로 유지한다. 자동 귀환·등록이나 확정적인 부활/소멸을 추가하지 않는다.

`tools/draft_shademan_victory.py`에 수동 원문 대응을 기록했다.21나비 화자·visible 초상화·checkNaviAll/unused1/2 continue와 숫자12/2·줄바꿈·제어 skeleton을 보존했다. 메탈맨 건곤일척, 섀도맨 나무 기도 조각, 플랜트맨 꽃 무대는 인간 문맥/말투 검토 후보다. 섀도맨 원문 오피셜 명칭 오타는 source 필드에서 보존한다.

신규4검사 포함134tests PASS, JSON 재생성 동일/py_compile PASS. 누적3308개 초안, 미작성24144개. 새32문구 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어 skeleton·미선택 원문·글리프/codec 보호 검사 PASS. 원본·기준ROM 불변. 실제 셰이드맨전/21나비 분기·귀환·보고·등록·저장·화면 검증은 하지 않았다.

## 후속: 레이저맨 조우73문구

`translations/laserman_encounter_draft_ko.json`:7C9C44의1~22스크립트에서 초상화로 화자를 확인한73개 일본어 문구를 작성했다. 레이저맨의 기억 상실과 증오,21나비의 대결 반응을 개별 번역했다. 넘버맨10의 비명2는 LaserMan 화자이며 뒤의 구조 요청3은 NumberMan이다. 브루스의 오피셜 블랙리스트·스페셜 S랭크, 일렉맨100만 볼트와 정크맨의 불안 극복·네이팜맨의 싸움 속 생존 실감을 유지한다.

`tools/draft_laserman_encounter.py`에 수동 대응과 원본/TPL/payload 해시를 기록했다. 도입0의2문구는 초상화가 없고 화자가 미확인이라 원문/미작성 분모에 보존했다. 삭제하거나 셰이드맨/레이저맨 화자로 단정하지 않는다.21나비 checkNaviAll·unused1/2 continue·1→2 jump와 모든 페이지/초상화/제어 skeleton을 유지한다. 섀도맨의 저승 인도·나이트맨 철구의 녹 비유는 인간 문맥/말투 검토 후보다.

신규3검사 포함137tests PASS, JSON 재생성 동일/py_compile PASS. 누적3381개 초안, 미작성24071개. 새15문구 배치 검토 추가. 원본·기준ROM 불변. 실제 레이저맨 조우·전투·나비 분기·초상화·저장·화면은 검증하지 않았다. 현재는 번역 우선 단계이고 ROM 빌드하지 않았다.

## 후속: 레이저맨전 이후95문구

`translations/laserman_aftermath_draft_ko.json`:7CA474의23스크립트·95개 일본어 literal 전체를 작성했다. 레이저맨0/1의 증오가 사라지지 않는다는 주장과 앞 에리어의 공포/삭제 위협,21나비2~22의 승리 반응을 각각 보존한다. 다음 상대의 정체나 확정 부활을 추가하지 않았다. 넘버맨은 플러그아웃을 요청하고 아쿠아맨은 위험을 경고하지만 실제 선택지/이동 명령은 없다. 정크맨의 신뢰·나이트맨의 전진·아이스맨의 물질/마음 얼리기 대비·플랜트맨 꽃 비유도 유지한다.

`tools/draft_laserman_aftermath.py` 수동 대응으로 기록했다. 서치맨6:2는 hidden 침묵,6:3은 hidden 경고음으로 system-sfx를 기록하고 원초상화 SearchMan을 함께 보존한다.6:4부터 명시된 초상화로 복귀한다. track284·soundDisableTextSFX/soundEnableTextSFX·21나비 checkNaviAll/unused1/2 continue·페이지/제어 skeleton은 불변이다. 일본어 문자 범위에 잡힌 중점 침묵2개도 목록에서 제외하지 않고 별도 literal로 대응했다. 섀도맨 명부마도는 인간 문맥/말투 검토 후보다.

신규3검사 포함140tests PASS, JSON 재생성 동일/py_compile PASS. 누적3476개 초안, 미작성23976개. 새41문구 배치 검토 추가. 원본/TPL/payload/source/ID·줄 수·제어 skeleton·미선택 원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 실제 승리 후 장면/경고음·초상화·다음 에리어·저장·화면은 검증하지 않았다. 번역 우선 단계이므로 ROM 빌드하지 않았다.

## 후속: 포르테 조우73문구

`translations/bass_encounter_draft_ko.json`:7CAF40의43개 명시초상화 스크립트1~21/23~44에서73개 일본어 literal을 작성했다. 두21나비의 압도적 힘 접근/전투 직전 반응과 Bass44의 피로 적셔 달라는 위협을 보존했다. Bass21/43은 플레이어나비 반응,44는 상대 위협이라는 장면 역할을 구분한다. 같은 초상화 이름만으로 같은 개체라는 주장을 하지 않는다.

`tools/draft_bass_encounter.py` 수동 대응으로 기록했다. 두 checkNaviAll/unused1/2 continue, target22/44와27/28→22의 원문 특수 분기를 유지했다.0의3문구·hidden22의1문구는 화자 근거 미확인으로 원문/미작성 분모에 보존했다. 넘버맨 승률0、00001의 숫자/원문 구분자를 유지했다. 썬더맨 자기장·일렉맨 원자력발전소 질문은 실제 장소가 아닌 대사로 남긴다. 섀도맨의 특정 기도문은 나무 하치만 대보살 후보이며 인간 말투/표현 검토가 필요하다.

신규3검사 포함143tests PASS. 처음 추가한 검사에서 기대 문자열의 역슬래시/줄바꿈 표기만 잘못되어 수정했고, 번역 문구는 변하지 않았다. JSON 재생성 동일/py_compile PASS. 누적3549개 초안, 미작성23903개. 새24문구 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어 skeleton·미선택 원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 실제 조우/개체 정체·특수 분기·전투·저장·화면은 검증하지 않았다. 번역 우선 단계이므로 ROM 빌드하지 않았다.

## 후속: 포르테전 승리132문구

`translations/bass_victory_draft_ko.json`:7CB850의23스크립트·132개 일본어 literal 전체를 작성했다. 상대Bass0/1의 패배/소멸 부정과21나비2~22의 승리 후 안도·감사·강화 의지·허세·귀환 희망을 각각 보존했다. 플레이어Bass22의 그림자/오리지널 주장을 남기고 동일 초상화를 같은 개체로 단정하지 않는다. 넘버맨은 확률 계산에 자기 데이터만 넣고 오퍼레이터를 빠뜨렸음을 깨닫고 산수 공부를 제안한다.

`tools/draft_bass_victory.py`에 수동 원문 대응과 해시를 기록했다.21나비 checkNaviAll/unused1/2 continue·페이지/초상화/제어 skeleton·0、00001 승률 및1인/1부터/나무1그루/전구1개를 유지했다. 윈드맨·섀도맨의 부활 추측과 서치맨의 가정은 확정 부활/소멸이 아니다. 롤의 눈물·정크맨의 가까이 보고 싶은 마음·아쿠아맨의 애정 요구에 성별/연애 관계를 추가하지 않는다. 스타맨 홍염/행운의 별, 네이팜맨 싸움 속 자기 위안은 인간 표현/말투 검토 후보다. 귀환·나무 심기·치료 거절·훈련·칩 설치는 대사로만 유지한다.

신규3검사 포함146tests PASS, JSON 재생성 동일/py_compile PASS. 누적3681개 초안, 미작성23771개. 새50문구 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어 skeleton·미선택 원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 실제 승리 후 장면/21나비 분기·개체 정체·PET 귀환·저장·화면은 검증하지 않았다. 번역 우선 단계이므로 ROM 빌드하지 않았다.

## 후속: 개인정보 관리128문구

`translations/profile_data_manager_draft_ko.json`:7CC6A0의128개 일본어 literal 전체를 작성했다.16항목0~15의 관리 안내·수정 수락/거절,20/21 항목 선택,22 수정/삭제/아무것도 안 함,23/24 확인,25 삭제 완료,95 거절 응답 및75~92의18라벨이다. 학교/직장·친구/가족·음식/취미/희망·TV/과목을 구분했다. 항목 라벨의 의미는 초안으로 번역했지만 실제 표시 consumer는 미확인 상태로 유지한다.

`tools/draft_profile_data_manager.py` 수동 대응과 해시를 기록했다.16 printPlayerName 삽입과4 buffered printString(index0)·printSchool~printWish3 및 모든 입력 데이터 출력 명령을 그대로 보존한다. 님의/인용문 뒤 에 대해 표현으로 받침에 따라 달라지는 조사를 피했다. 인용문 열기 원문은 미선택 그대로이며 닫기/선택지는 별도 literal 경계를 유지한다. 선택지 초상화가 visible이더라도 화자는 player-choice이다. 폭7/11·기본값·취소·targets/95/20·waitHold·단일 후행 공백/줄바꿈을 변경하지 않았다.

형·오빠/누나·언니는 플레이어 성별을 추정하지 않는 후보이다. 스키나히토는 좋아하는 사람, 니가테나히토는 불편한 사람 후보로 작성했다. 기존7B67C8의 좋아하는 이성/싫어하는 사람 후보와 표현 차이가 있어 별도 인간 검토 대상으로 기록하며 기존 후보를 자동 정규화/덮어쓰지 않는다.75~92는 consumer_status=unresolved-profile-label-consumer로 기록한다. 앞서 기록한 입력 전 라벨16개의 실제 consumer도 아직 해결된 것이 아니다.

신규3검사 포함149tests PASS, JSON 재생성 동일/py_compile PASS. 누적3809개 초안, 미작성23643개. 새31문구 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어 skeleton·미선택 원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 실제 프로필 열기/수정·삭제·한글입력·이름 및 항목 합성폭·커밋·저장/재로드·화면은 검증하지 않았다. 번역 우선 단계이므로 ROM 빌드하지 않았다.

## 후속: 크레딧71문구

`translations/credits_draft_ko.json`:7CE5C8의71개 일본어 literal 전체를 작성했다. 기획/시나리오/디자인/프로그램/음악/효과음/설명서/검사/프로듀서 등의 역할과 가나로 적힌 인명을 각각 대응했다. 콘미JPN이 아니라 원문 コナミJPN의 코나미JPN 표기를 유지하고 개발부/클럽/캡콤의 감사 대상도 보존했다. 인명은 원문 가나에 근거한 음역 초안이지 외부 공식 한글 표기 승인이나 사람 신원 확인이 아니다. 원문52 스크립트는 없으므로 새 인명/항목을 만들지 않는다.

`tools/draft_credits.py` 수동 대응 및 해시를 기록했다. 원문에 있는 모든 선행/후행 ASCII 공백을 정확히 보존하고 별도 회귀검사로 검증한다.64 클리어 시간 buffer0/1 순서·minLength2·0패딩·콜론,65~67 칩수 minLength3·S/M/G 원문 접두어를 유지하고枚는 장으로 대응한다. 게임명4.5/리얼오퍼레이션·스태프도 후보로 작성했다. 원문 가나 다이니개발부는 두 번째 개발부로 옮겨 새 ASCII 숫자 토큰을 추가하지 않는다. 최초 작성한 제이개발부 후보를 같은 미완료 배치에서 두 번째 개발부로 다듬고 JSON/작성기 대응을 함께 갱신했다.

신규3검사 포함152tests PASS, JSON 재생성 동일/py_compile PASS. 기존 범용 선택지 검사에서 모든 두 칸 후행 공백을 player-choice로 보는 가정이 크레딧 정렬에는 맞지 않아 크레딧을 별도 정렬 검사로 분리했다. 누적3880개 초안, 미작성23572개. 새41문구 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어 skeleton·미선택 원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 실제 엔딩/크레딧 소비·스크롤·한글 정렬·클리어 결과·저장·화면은 검증하지 않았다. 번역 우선 단계이므로 ROM 빌드하지 않았다.

## 후속: 미니게임 결과31문구

`translations/minigame_result_rewards_draft_ko.json`:65AAE0의50~73 결과12스크립트에서31개 일본어 literal을 작성했다. minigame0 계산 문제집·1 퍼즐 편지·2 미션 데이터의 실패/성공과 힘 증가·제니·버그 조각 보상을 구분했다. 도리루는 계산 문맥에 맞춰 문제집 후보로 작성했다. 원문0의かりです 임시 문구는 실제 consumer가 미확인이라 원문/미작성 분모에 남겼다.

`tools/draft_minigame_results.py` 수동 대응과 해시를 기록했다. 명시초상화나 호출 화자 근거가 없어 speaker=unshown-result-voice, origin_portrait=None, portrait_visibility=not-shown-in-script로 기록한다. 현재나비/록맨 화자로 단정하지 않고 원문의 평이한 결과 말투를 후보로 남긴다. 버그 조각이 +buffer3+개와금액+제니가의 경계를 유지했다. 미니게임0/1/2 기록·flag3585·global5 결과0~3·item33·4294967295 sentinel·buffer3/padLeft·positionText92/110·box10/12/type1·arrow225/141·waitHold는 변경하지 않았다.

신규3검사 포함155tests PASS, JSON 재생성 동일/py_compile PASS. 누적3911개 초안, 미작성23541개. 새3문구 배치 검토 추가. 원본/TPL/payload/source/ID·숫자/줄 수·제어 skeleton·미선택 원문·글리프/codec 보호 검사 PASS, 원본·기준ROM 불변. 실제 미니게임 진입/결과/보상 지급·화자·저장·전용 결과 레이아웃/화면은 검증하지 않았다. 번역 우선 단계이므로 ROM 빌드하지 않았다.

### 후속: 일정·메일 알림26개

`translations/schedule_reminders_draft_ko.json`:65AFA0의 일정알림12개를 개별 작성했다. 방송/약속/식사/학원/기타/추가 알림을 구분했다. 원문じゅく는 API의 school 이름이 아닌 실제 학원 의미로 번역한다. 일정 이름 뒤의 시작할/약속 시간이야/시간이야 표현은 받침 의존 조사를 피한다. 1..6 quick-box는 명시초상화가 없어 unshown-reminder-voice,21..26은 원본 mugshotShow의 MegaMan으로 기록한다.

`translations/mail_alerts_draft_ko.json`:65B220의 메일도착14개를 작성했다. 별명 삽입1..3 뒤 쉼표와 줄바꿈을 유지하며 이름/화자/발신인/제목을 임의로 추가하지 않았다. script2 tournamentReceiveMail/flag680,나머지 flag681/623..626/8904..8910의 수신·알림 동작을 구분해 보존한다. 명시초상화가 없으므로 전부 unshown-mail-alert-voice로 기록했다.

두 수동 생성기 `tools/draft_schedule_reminders.py`/`tools/draft_mail_alerts.py`를 권한·해시 목록에 추가했다. schedule buffer/이름/대문자 옵션·다중일정 분기·flag3585/3658·sound155/wait96·positionText92/110·box10/12/type1·arrow225/141·end/waitHold·일본어 아닌 !! 원문을 보존했다. 신규3검사 포함158tests PASS, 생성기 동일/py_compile PASS. 누적3937개, 미작성23515개, 새2문구 배치 재검토 추가. 실제 시간발생/다중알림/메일수신/일정·별명 표시/저장/화면 검증은 아직 없으며 ROM 불변이다.

### 후속: 대회 즉시안내·일정 조회·프로필 질문154개

`tools/draft_quick_box_routes.py`의 개별 수동 대응으로65B74C12개·65B8E46개·65B9E8136개를 작성했다. 자산은 `translations/quick_tournament_draft_ko.json`, `translations/quick_agenda_draft_ko.json`, `translations/quick_profile_questions_draft_ko.json`이다. 원본 TPL 전체/원본 ROM/payload 해시와 대조하고 권한 목록에 추가했다.

대회는 패배 격려/우승/미신청/시작을 구분한다. nickname 경계·callCancelMenuTransition·flag3603과 원문 !를 보존했다. 일정은 곧 있을 일정 목록과 오늘의 시간표를 구분한다. hour/minute buffer1의 padZeros 차이, AMPM/name 순서,콜론/공백/인용부호, soon2/today11 반복을 그대로 유지했다. から는 시작시각 뒤부터로 후보 작성했다. 원문의 첫 soon jumpIfNone=2를 임의 수정하지 않았다. 오전오후 버퍼 자체의 번역과 표시 폭은 이 묶음에서 증명하지 않았다.

프로필은 형제자매/친구/음식/취미/꿈/좋아하는 사람/존경/불편한 사람/TV/과목/선물/소속 질문, 기존1~3개 string buffer와 추가 등록 선택지, 응답 감상을 구분했다. 사용자 성별을 단정하지 않는 형이나 오빠/누나나 언니 후보를 쓴다. 원문 여자아이/남자아이 분기(global22)는 구별해 남겼다. global23의1..5학교/6..9회사/그 외 유치원 분기와 global5 등록 수량/입력flag3605/3606/거절flags를 보존했다. 이름 뒤 고정 이/가/아/야를 넣지 않았으며 불편한 사람은 최근 관리자 초안과 동일 후보이고 이전 싫어하는 사람과의 통일은 아직 미승인이다.

모든 대사에 명시초상화가 없으므로 unshown-quick-box-voice/None/not-shown-in-script, 프로필24개 선택지는 player-choice로 분리했다. 숫자1·원문 줄 수/빈 줄·선택지 두 공백·미선택 기호는 보호한다. 새6검사 포함164tests PASS, 생성기 재현/py_compile PASS. 누적4091개, 미작성23361개. 새19문구 배치 검토 대상으로 기록했고 실제 consumer 예산/대회경로/알림/입력/저장/표시 검증은 미완료다. ROM 빌드/화면검증/세이브 변경 없음.

### 후속: 진행 힌트·롤 메뉴 잔여82개

`tools/draft_progress_roll_menu.py` 개별 수동 대응으로 `translations/quick_progress_hints_draft_ko.json`65E8B8의31개와 `translations/roll_menu_remaining_draft_ko.json`65F11C의51개를 작성했다. 전체 TPL과 ROM/payload 해시를 확인하고 기준 목록의 unselected_japanese ID만 선택한다. 롤의 기존 날짜·등록·시간·종류·기본 확인 문구는 보존한다.

진행힌트는 견습시험/칩104/사건지역3·5·7·9·10·12/마이너스키 회수 및 인터넷9 전달/관표식/오피셜 접수·예선·주말·미확인메일/탐색을 구분한다. 내비가 범인/다른 내비1명이 키 보유라는 원문의 추정은 유지한다. source10의 priority flags/items/tournament bitmask4,weekday0/6 분기34/30,9416..9422 unread 분기33를 보존하며 미표시 화자를 특정 내비로 단정하지 않는다. 이전 나비/내비 용어 후보 통일은 아직 미승인이다.

롤메뉴는 명시 Roll 초상화와21개 player-choice를 구별한다. 과거 날짜/등록 한도/중복 시각/덮어쓰기/삭제 경고를 따로 번역했다. 삭제50은 일정,51/52는 연도/날짜·기념일 문맥으로 후보 작성하고 인용부호 뒤 category를 붙여 사용자 문자열 받침 의존 을/를을 피한다. 소지품 도입은 이건: +별명+의 형태로 원문 경계의 trailing-space 제약을 유지하는 후보이며 실제 표시 검토가 필요하다. 계산 문제집과 얼음 편지 명칭은 후보 상태다.

원문 날짜·시간·요일·반복·이름 buffer 순서와0-padding,옵션width7/8/default0/1/BSeparate·두 공백·줄 수/빈 줄·flag3611·sound467/wait1·mugshotHide/close/end를 보존했다. 실제 등록/삭제/덮어쓰기/세이브/ROM 변경 없이 새5검사 포함169tests PASS, 생성기 재현/py_compile PASS. 누적4173개, 미작성23279개, 새롤문구3개 배치 검토 추가. 실제 게임 진행/힌트 우선순위/메뉴/시간발생/입력 저장/화면검증과 독립 번역 승인은 미완료다.

### 후속: 운세 점기호·일정알림 잔여·프로필 잔여B119항목

`tools/draft_remaining_roll_profile.py`의 개별 수동 대응으로65FF3C6항목·660D9011문구·661858102문구를 작성했다. 자산은 `translations/fortune_wait_dots_draft_ko.json`, `translations/roll_reminder_remaining_draft_ko.json`, `translations/quick_profile_remaining_b_draft_ko.json`이다. 전체 TPL을 읽고 원본/TPL/payload와 미선택 ID 집합을 확인했다. 이전 ROM 선택 문구를 재번역·덮어쓰지 않는다.

운세의 잔여6항목은 대사가 아닌0/1의 개별 중점 ・이며 ASCII . 후보로 처리했다. 각 intro의 waitSkip30 네 번과 분절, 원래 운세·하트·보상/확률/위치 분기를 보존했다. 일정알림은 이름 뒤 시작할/일정 시간/약속 시간 표현으로 받침 의존을 피하고 선행 줄바꿈·방송 서두름·약속 설렘·식사·학원 지각 경고를 유지했다. 21..26만 원문 명시Roll로 기록하며1/2/5는 미표시 화자 미확인이다.

프로필은 기존 가족/음식/과목 질문의 현재 ROM 선택분을 보존하고 친구/취미/꿈/성별 분기 좋아하는 사람/존경/불편한 사람/TV/선물/소속·기존 내용·추가 등록·감상만 추가했다. 모든 원문 초상화가 없어 이웃 archive/1인칭만으로 Roll 화자로 확정하지 않고 unshown-profile-voice로 기록했다. 추가등록16개 선택지는 player-choice다. 형이나 오빠/누나나 언니 후보·global22/23 및 global5 수량·stringBuffer1..3·입력flags3605/3606와 거절flags를 보존한다.

사랑의 메일은 러브러브 메일 후보로 작성하고 미도착과 이름을 알아야 즉시 식별한다는 이유를 유지했다. 음식의 아삭아삭/TV 털북숭이 괴물 발언 뒤 자기정정도 남겨 사용자 입력을 실제 아는 듯 확정하지 않는다. 라이벌시·낭만적/유행따름 후보의 감상 말투는 독립 검토가 필요하다. source 숫자1/줄 수/빈 줄/선택지 두 공백과 일정buffer/좌표/flag3585/3658/sound155/wait96/다중일정 분기 보존 검사를 통과했다.

새5검사 포함174tests PASS, 생성기 동일/py_compile PASS. 누적4292개 초안 항목(이번 대사113+기호6), 미작성23160개. 새프로필10문구 배치 검토 추가. 실제 운세 기호 간격·알림 발생/이름·프로필입력/저장/화면은 미검증이며 ROM 빌드·세이브 변경·번역 승인 없음.

## 후속: 대회 격려·배틀 결과·거츠맨 알림 잔여23개 (2026-10-11)

`tools/draft_quick_results_guts_reminders.py`로6648045개·664D844개·66651C14개를 개별 수동 작성했다. 자산은 `translations/quick_tournament_encouragement_draft_ko.json`, `translations/quick_battle_outcome_draft_ko.json`, `translations/guts_reminder_remaining_draft_ko.json`이다. 각 전체TPL/해시/payload/미선택ID 집합을 확인했으며 현재 ROM 선택 문구는 유지했다.

주말 대회 우승 격려·대회일 도착·키 아이템 확인, 패배 후 격려·승리와 오퍼레이션 칭찬·다음 완전 결판 메시지를 구별했다. 664804/664D84에는 초상화가 없어 특정 화자를 추정하지 않았다. 664D84의 닉네임 앞뒤 literal 경계/선행 쉼표/마지막 줄바꿈을 유지했다. script3의 외부 무승부 caller는 아직 입증하지 않았다.

거츠맨 알림은 방송 오프닝 놓침·약속 기대·식사·학원·기타/추가 일정 문맥과 거스/거츠 후보 말투를 유지했다. 21..26만 명시GutsMan이며 quick1/2/5는 초상화 미표시다. 일정명+시작할/일정 표현으로 받침 의존 조사를 피했다. 0/20 dispatch, sound155/wait96, flags3585/3658, 다중일정6/26, 좌표와 schedule/nickname 인수를 보존했다. 실제 시계/이름/알림 표시와 독립 문안 승인은 미검증이다.

666430도 전체 원문을 읽었으나 임시 `かりです`의 consumer가 불명확해 번역하지 않고 분모에 남겼다. 신규3검사 포함177tests PASS, 생성기 재실행 동일/py_compile PASS. 누적4315개 초안, 미작성23137개. 새2문구 배치검토 추가이며 전체1015개다. 원본/유지ROM 해시 불변, ROM 빌드·세이브 변경·화면검증 없음.

## 후속: 윈드맨 메뉴 잔여57개 (2026-10-11)

`tools/draft_windman_menu_remaining.py`에서66B0D4의 미선택일본어57개를 개별 수동 작성해 `translations/windman_menu_remaining_draft_ko.json`에 등록했다. 전체 TPL 문맥/명시WindMan 초상화/원본·TPL·payload 해시/미선택 ID 집합을 확인했고 비일본어 날짜·시간·인용부호 구조와 기존 선택분은 보존했다. 21개 선택지를 player-choice로 구분했다.

날짜 안내·일정/기념일 등록/삭제·과거 날짜 거절·등록용량 부족과 삭제 해결책·동일시간 일정 충돌·덮어쓰기 확인·키 아이템/서브 칩/장비/라이브러리/메일/저장 설명을 구별했다. 50의 시간/분/AMPM/빈도는 일정 삭제,51의 연월일/요일과52의 월일은 기념일 삭제로 명시했다. 실제 삭제나 덮어쓰기 실행은 하지 않았다.

윈드맨 기존 계절대화 후보와 맞춘 차분한 하겠느냐/하거라/하마 말투는 미승인이다. 닉네임+의와 인용된 일정명 뒤 일정/기념일 표현으로 받침 의존을 피했다. `이건` prefix는 원문これが의 끝 공백이 없어 새 공백을 추가하지 않았으며 실제 이름 결합 표시 검토가 필요하다. 모든 줄/선택지 두 공백/default/cancel/BSeparate/clear/target와 sound467/flag3611/wait1/close/end 및 날짜·시간 버퍼 인수를 유지했다.

신규3검사 포함180tests PASS, 생성기 재실행 동일/py_compile PASS. 누적4372개 초안, 미작성23080개. 66B0D4의9문구(3:0,4:0,6:0,20:0,24:0,25:0,33:0,51:6,52:3)가 보수적132px 검토 후보로 추가되어 전체1024개다. 실제 consumer 예산 확정이나 화면 오류 판정이 아니며 자동 축약은 하지 않았다. 원본/개발ROM 해시 불변. ROM 반영·화면/입력/일정/저장 검증·독립 문안 승인 없음.

## 후속: 메뉴 확인·귀환·플러그인 구호·알림65개 (2026-10-11)

`tools/draft_quick_wind_routes.py`에서66B95044개·66BDE02개·66BEF81개·66BF4418개를 개별 수동 작성했다. 각각 `translations/quick_menu_confirmation_b_draft_ko.json`, `translations/quick_wind_return_draft_ko.json`, `translations/windman_jackin_call_draft_ko.json`, `translations/windman_reminder_draft_ko.json`에 등록했다. 전체 원문/TPL·payload 해시·미선택 ID 집합을 확인했으며 기존 선택분/제어 데이터는 보존했다.

메뉴 확인은 토너먼트/인터넷/장비/라이브러리/메일/통신/저장과 말이 끝나지 않았다는20의 중단 응답을 구별했다. 8은 저장 화면 진입,16은 지금까지 데이터 저장 요청이다. 28선택지·2..8/10..16 dispatch·yes9/no취소1·global30=120/flags3584/3585/3588/3615·sound127/128·24px 위치·빈 줄·두 공백을 유지했다. 초상화 없는 화자를 이웃 archive만으로 WindMan이라고 확정하지 않았다.

귀환은 전뇌 바람과 바람 방향이 바뀌었다는 패배의 비유를 유지하고 임의 전술 원인을 추가하지 않았다. 구호는 원문에 명시된 윈드맨.EXE 목적지를 번역하되 캐릭터 자신의 발화로 보지 않았으며 operator-jackin-call로 기록했다. Type3/flags3603/3651/wait30/EXE 토큰/3줄을 보존했다.

알림은 TV를 멀리서 보기·약속 지각 방지·식사 남기지 않기·학원에서 배우기·기타/추가 일정 문맥을 유지했다. 21..26에만 명시WindMan 초상화가 있으며 quick1..6은 미표시다. 닉네임 쉼표·일정명+시작할/일정·선행 줄바꿈과0/20·6/26 dispatch/다중일정·flags3585/3658·sound155/wait96·버퍼 인수를 유지했다. 66BE58도 전체 원문을 읽었으나かりです 임시 consumer가 불명확해 원문과 미작성 분모에 남겼다.

신규3검사 포함183tests PASS, 생성기 재실행 동일/py_compile PASS. 누적4437개, 미작성23015개. 새geometry 검토 후보0개이며 전체1024개는 유지된다. 실제 메뉴/귀환/플러그인/시계·알림/화면·입력·저장·독립 문안 승인 미검증. 원본/개발ROM 불변, ROM 빌드·세이브 변경 없음.

## 500개 단위 묶음001: 장비459·진행힌트31·대회10 (2026-10-11)

사용자 요청 “번역 작업을 할때500개씩 끊어서 작업해줘”에 따라 `translations/full_translation_first_plan.json#batch_policy`에 목표500 stable literal 항목과 첫 묶음의 범위/개수를 고정했다. 문맥은 전체 archive 단위로 읽으며 같은 source라도 서로 다른 ID는 구별한다. 최종 잔여분만500미만을 허용하고, 임시/미확인 문구로 수량을 채우지 않는다.

`tools/draft_batch500_001.py`에서6E1554/6E17CC/6E1A48/6E1CC0/6E1F38/6E21B0/6E2428/6E26A0/6E2914 각51개,66FD1431개,6886F010개를 작성했다. 자산은 `translations/batch500_001_*.json`11개다. 정확히500개로, 기술명·라벨342개/선택지18개/대사·힌트140개다. 유일문장 수나 신규 승인 수를 뜻하지 않는다. 각 전체TPL을 읽고 원본/TPL/payload 해시·미선택 ID 집합을 대조했다.

장비의0..37 라벨은 기존 `equipment_weapons_ko.json`·`equipment_labels_ko.json`의 해당 문맥 후보를 명시 선택하고 원래3칸/2칸 선행 및3칸 후행 정렬 공백을 보존했다. C/WB/B/D 축약은 확장하지 않았다. 38/39 R/L 접두어와63의 buffer-only 및 모든 비일본어 literal은 그대로다. 이것은 source-string 정규화/변환 규칙이나 새 공식 용어 승인 작업이 아니다.

60..62의 R/L 무기 배정/폴더 편집 발화에는 원문 초상화가 없으므로 특정 화자라고 확정하지 않았다. 70..75는 원문에 명시GutsMan/WindMan/SearchMan/FireMan/ThunderMan/ProtoMan/NumberMan/MetalMan/JunkMan을 각각 기록하고70의2개 선택지만 player-choice로 구별했다. 원문 거스/차분한 고풍체/정중체/친근한 말투/직설체/정크맨 짧은 기계적 후보와 줄 수 차이를 개별 반영했다. 이웃 archive 또는 사용자 이전 NumberMan 화면 관찰만으로 다른 대사의 화자를 변경하지 않았다.

폴더 장수는 buffer1 동적 값 그대로이며30으로 고정하지 않았다. 동일칩3장/동일메가·기가1장/총메가5장·기가1장 제한과 편집중단 예·아니오의 의미/순서/두 공백/default/clear/cancel/target 인수를 보존했다. 실제 장비/폴더/입력/저장 실행은 하지 않았다.

진행힌트는 인터넷3/5/7/9/10/12 사건·다른 내비1명·칩104·item11 마이너스키·인터넷9 반환·목표 내비의 관 표식·견습 라이선스·오피셜 예선/접수/주말/주말 이후·메일 분기와 우선순위/flags/요일0/6을 보존했다. 대회는 패배의 말더듬/자기 잘못 부정/계산 오류 부정·승리 방정식·미등록으로 메뉴이동 취소·다치지 않을 정도의 격려를 그대로 살렸다. 두 quick archive의 초상화는 없으므로 WindMan/NumberMan 확정이 아니다.

신규6검사 포함189tests PASS, 생성기 재실행 동일/py_compile PASS. 초기 회귀2개는 “후행2공백 이상이면 선택지”라는 기존 테스트 가정이 장비2:0의3공백 정렬 제목에도 적용되어 실패했다. 원문 mmbn45s/end 라벨과 option 부재에 따라 해당9개 archive의 정확한2:0 ID에만 equipment-label 기대값을 적용했다. 번역/보호 데이터는 수정하지 않았고 다른 선택지 검사를 완화하지 않았다.

누적4937개 초안, 미작성22515개. 새geometry 검토14개(윈드장비2/서치장비5/브루스장비5/진행힌트1/대회1)를 더해1038개다. 보수적132px 추정이며 실제 consumer 용량 확정/자동 축약/화면 검증이 아니다. ROM·세이브 불변, 빌드·실행·독립 문안 승인·배포 없음. 다음도500개씩 작성한 뒤 전체 번역/구조 처리가 갖춰지면 누적 ROM 적용과 실제 화면/저장 검증을 진행한다.

## 500개 단위 묶음002: 장비459·진행힌트31·대회10 (2026-10-11)

`tools/draft_batch500_002.py`에서6E2E18/6E308C/6E32FC/6E3574/6E37EC/6E3A64/6E3CD8/6E3F4C/6E41C4 각51개와68097C31개·68E5E010개를 개별 초안 작성했다. `translations/batch500_002_*.json`11개를 권한 목록에 추가했다. 정확히500 stable literal이며 장비 라벨342·선택지18·대사/힌트140이다. 같은 라벨의 별도 ID를 포함하며 유일문장500개가 아니다.

11개 전체 TPL 원문을 읽고 원본·TPL·payload 해시/미선택 ID 집합을 대조했다. 장비0..37은 같은 consumer의 기존 명시 후보를 문맥 대조해 선택했고 정렬 공백과 C/WB/B/D 축약을 보존했다. 38/39와 buffer-only63은 변경하지 않았다. 60..62의 미표시 화자는 확정하지 않았으며70..75만 명시WoodMan/StarMan/ShadowMan/KnightMan/NapalmMan/IceMan/ElecMan/PlantMan/Bass로 기록했다. 직설체/친근체/고풍체/정중체/힘찬 말투/어린 존댓말/부드러운 말투/짧은 단정체는 문안 검토 전 후보다.

폴더 장수buffer1·동일칩3/동일메가·기가1/총메가5·기가1·R/L·예/아니오·두 공백과 줄 topology 및 모든 명령 인수는 유지했다. 진행힌트는15의 시험 수고와 플러그아웃 안내,26의 접수 장소 안내가 별도 페이지임을 유지하고33의 닉네임 뒤 미독 메일·관 표식·인터넷 지역/마이너스키 반환·칩104/item11·요일0/6/주말 이후를 구별했다. 이전66FD14 문안을 그대로 복사하지 않았다.

68E5E0는 패배의 사과·전력으로 싸웠음·포기하지 않음·주먹으로 승리를 얻겠다는 결의를 번역했다. 이전6886F0의 계산/방정식 표현을 이식하지 않았다. 닉네임/미등록/callCancelMenuTransition/20..23 flag3603을 보존했고 주먹 표현만으로 MetalMan이라고 확정하지 않았다.

신규6검사를 더해195tests PASS(41.360초), 재생성 동일/py_compile PASS. 누적5437개 needs_review 초안, 미작성22015개. 새geometry10개(나이트장비5/아이스장비3/진행힌트1/대회1)로 전체1048개다. 132px 보수적 추정이며 실제 오류 판정/자동 축약/문안 승인/삽입 준비 완료가 아니다. 원본/유지ROM SHA 불변. 이번 ROM 빌드·화면 검증·메뉴 입력·세이브 변경 없음.

## 500개 단위 묶음003: 메뉴484·훈련결과15·플러그인 구호1 (2026-10-11)

`tools/draft_batch500_003.py`에서670E9C/676BA8/67C578/681B3C/68D454/6930F8/698508/69E12C/6A38E8/6AA214/6B5B1C 각44개·6713B8 결과15개·671638 구호1개를 작성했다. `translations/batch500_003_*.json`13개를 권한 목록에 추가했다. 정확히500 stable literal(선택지308/서술192)이며 유일문장500개 또는 승인500개가 아니다.

670E9C 메뉴 원문 전체와 훈련/구호 전체 원문을 읽었다. 다른 메뉴는 모든 literal과 제어 skeleton의 전 토큰을 기준670E9C와 비교했다. 제어 차이는 닉네임 삽입 여부/위치와 textSpeed0뿐이며 각 원문대로 유지했다. source ID·원문/TPL/payload 해시·미선택 집합을 대조했다.

메뉴2..8/10..16의 토너먼트·인터넷·장비·라이브러리·메일·통신·저장 안내를 구별했다. 8은 저장 화면 진입,16은 누적 데이터 저장이다. 681B3C:16의 원문 평서문은 평서문으로 유지했다. 6B5B1C:10은 참가 동사가 생략되어 있지만 dispatcher와2의 대응 문맥을 근거로 참가 표현을 보완한 미승인 해석 후보다. 정중체/직설체/고풍체/말더듬·기계적 문체/퓨 어미/닌자 표현과20의 말 중단 반응을 각각 작성했다. 698508의퓨는 기존 aquaman_seasonal_ko.json 후보를 확인해 맞췄으며 공식 승인이나 화자 확정은 아니다.

28선택지씩의 예/아니오 순서·두 공백·빈 줄·24px·default/cancel/BSeparate/clear/target·sound127/128·flags3584/3585/3588/3615·global30=120/wait1·20→10을 보존했다. 닉네임 뒤 쉼표로 받침 의존을 피했고 모든 quick화자는 초상화 없음으로 기록했다. 저장/메뉴 입력 실행 없음.

6713B8 훈련결과는minigame2/global5=0..3, 실패의 사과/완료/성장item33/군에서 전송한 보상·제니/버그조각을 구별했다. buffer3과 sentinel4294967295, 라벨/수량 접미 경계를 보존했다. 0:0 임시かりです는 작성 범위에서만 제외하고 원문과 미작성 분모에 유지했다. 671638은 서치맨.EXE를 목적지로 명시하는 operator-jackin-call이며 캐릭터 자기 대사가 아니다. EXE·3줄·type3/flags3603/3651/wait30을 보존했다.

신규6검사를 더해201tests PASS(51.940초), 생성기 재실행 동일/py_compile PASS. 누적5937개 needs_review 초안, 미작성21515개. 새geometry15개(676BA8:1/67C578:2/681B3C:1/68D454:4/698508:2/69E12C:1/6A38E8:1/6AA214:2/6713B8:1)로 전체1063개다. 보수적132px 추정이며 실제 consumer 오류 판정·자동 축약·문안 승인·삽입 준비 완료가 아니다. 원본/유지ROM SHA 불변. ROM 빌드·화면/저장 검증·세이브 변경 없음.

## 500개 단위 묶음004: 메뉴220·진행힌트280 (2026-10-11)

`tools/draft_batch500_004.py`에서6BBBBC/6C1710/6C7128/6CC8D0/6D2230 각44개,6AEE68:31/6C5FCC:31/6C05C4:30/6CB75C:32/6D10F0:33/6D5F34:30/6BA9F8:33/6A911C:30/6A276C:30개를 개별 작성했다. `translations/batch500_004_*.json`14개를 권한 목록에 등록했다. 정확히500 stable literal(선택지140/서술360)이며 유일문장500개·승인500개가 아니다.

각 전체 literal과 canonical 제어 skeleton 전 토큰을 메뉴670E9C/진행68097C 원문 기준으로 대조했다. archive별 flags·닉네임 인쇄·페이지/keyWait/clear 차이와 source/TPL/payload 해시·미선택 ID 집합을 보존했다. 초상화 없는 quick 화자는 특정 캐릭터로 확정하지 않았다.

메뉴는8의 저장 화면 진입과16의 누적 저장·28선택지·두 공백·빈 줄·24px·예9/no1·20→10·global30=120/flags/sounds/cancel 인수를 유지했다. 6CC8D0의 평서 안내와 서둘러 피는 꽃의 비유,6C1710의 늘인 존댓말/훌쩍,6D2230의 짧은 네놈을 원문 범위대로 구별했다. 실제 메뉴/저장 입력 없음.

진행힌트는 견습 시험/라이선스 수령/휴식과 플러그아웃,칩104/item11,인터넷3/5/7/9/10/12·다른 내비1명·인터넷9 반환·관 표식·오피셜 접수/예선/주말0/6/주말 이후 안내를 구별했다. 닌자 극의/손쉬운 일,차갑게 타오름,발포 욕구와 불타오름,MAX파워와 짜릿한 이름,최고의 꽃을 피울 무대,우리가 빛날 무대,투지에 몸이 떨림,심심풀이와 시시한 여흥을 서로 이식하지 않았다.

12/15/17/23/25/28/29/30/31/34의 archive별 페이지 분절 차이를 유지했다. 6C5FCC:13:0의 닉네임 쉼표+인용부호 및6C05C4:28:0 쉼표는 일본어 서술이 아니어서 번역하지 않았다. 초기에6C5FCC:13:0을 초안 딕셔너리에 포함한 것은 scope 검사에서 거절되었고 자산 생성 전에 제거했다. 해당 source/제어 데이터와 미검토 분모는 그대로다. 이전 임시 문구도 제외/완료 처리하지 않았다.

신규6검사 포함207tests PASS(63.392초), 재생성 동일/py_compile PASS. 누적6437개 needs_review 초안, 미작성21015개. 새geometry21개(메뉴8/진행13), 전체1084개다. 세부6BBBBC1/6C1710 2/6C7128 1/6CC8D0 1/6D2230 3/6AEE68 3/6C5FCC 3/6C05C4 2/6D5F34 1/6BA9F8 3/6A911C 1. 보수적132px 계산으로 실제 화면 오류·자동 축약·문안 승인·삽입 준비 완료를 뜻하지 않는다. 원본/유지ROM 해시 불변. ROM 빌드·화면/저장 검증·세이브 변경 없음.

### 후속: 500묶음005 — 진행226·일정190·훈련84

이번 묶음은 stable catalog literal 정확히500개다. 진행 안내는675A20 32/67B47C33/6861B8 34/68C368 32/692020 30/697310 33/69D02032개로226개, 일정 알림은67736432/67CB7024/6A4CC830/6AAB5422/6B613C24/6BC34430/6CD0B428개로190개, 훈련·보상은68D96C32/6C1BFC52개로84개다. 16개 자산의 source/payload/TPL 해시와 ID를 고정했다. `tools/draft_batch500_005.py`의 문안은 원문 문맥을 읽고 ID별로 직접 작성했으며 자동 원문 문자열 치환이나 규칙 기반 대사 생성이 아니다.

각 archive의 모든 literal을 읽고 진행은68097C, 알림은67CB70의 기준 제어 skeleton과 다른 토큰을 비교했다. 알림67CB70과 훈련68D96C/6C1BFC TPL은 전체를 읽었다. 시험 흥미/도전/합격/재미/수령, 사건 지역3/5/7/9/10/12, 다른 내비와 키 반환 인터넷9, 관 표식, 참가 접수/신청/예선/주말0·6/주말 이후 분기, 닉네임·칩104 삽입과 페이지 차이를 유지했다. 697310의 원문은 ‘다른 쪽 내비’로 숫자1을 명시하지 않으므로 추가하지 않았다. 불타오름/영혼의 울림/근질거리는 주먹/말더듬/인기쟁이/무서움·놀이·퓨를 구별한다. 퓨는 기존 원문ぴゅ 후보와 일치시키며 뿌로 바꾸지 않았다.

알림의 quick1..6과 일반21..26을 따로 기록했다. 일반대사의 명시 FireMan/ThunderMan/StarMan/ShadowMan/KnightMan/NapalmMan/PlantMan 초상화만 화자 증거로 사용했고, quick에는 이름을 추정하지 않았다. 방송/약속/식사/학원/기타·추가 알림, TV 시작/시청 독려, 농부 감사/몸과 마음/매실 장아찌/병량환/식당/네이팜탄/꽃꽂이·식물의 양분·지식 흡수 비유를 유지했다. 임의의 일정명 뒤에 고정 이/가·은/는을 붙이지 않도록 TV는 ‘방송이’, 기타는 ‘일정의’ 후보로 작성했다. source 삽입 위치나 줄 수는 바꾸지 않았다. 문화어 음역·의역은 문안 검토 후보이며 인간 승인이 아니다. 알림flag3658·음155·wait96·추가알림6/26·end/waitHold 분기는 원형 유지다.

훈련은 근질거리는 주먹의 수련과 PET 열기/녹음/냉각·배틀 대비를 구별했다. 성공/실패/아이템·제니·버그 조각, 결과variable5의0..3, 보상buffer3, item33의 일반5와 기록1, 수량 sentinel4294967295, Ice분기flag3667, 선택지8px/24px와 두 공백 padding을 보존했다. 68D96C:0:0/6C1BFC:0:0 임시かりです는 원문·미작성 분모에 남겼다. 6B613C의 일본어 점 연출4개도 별도 stable literal로 처리했다. 이를 처음 누락한 딕셔너리는 scope 검사가 거절했고 해당 자산 생성 전에 보완했다.

누적6937개 needs_review 초안, 미작성20515개. 새geometry13개(진행8/알림2/훈련3), 전체1097개다. 세부67B47C2/68C3681/6920202/6973101/69D0202/6BC3442/68D96C2/6C1BFC1. 보수적132px 계산은 실제 consumer 용량이나 화면 오류의 증거가 아니므로 자동 축약하지 않았다. 원본/기준ROM 해시 불변, ROM 빌드·세이브 변경·실제 화면 검증 없음. 모든 문안은 NON-DISTRIBUTION/needs_review이며 전체 번역 완료나 배포 승인이 아니다.

신규6검사 포함213tests PASS(77.641초), 신규500개 독립 기술 검사/py_compile/자산 재생성 동일 PASS. 처음 전체검사에서 JSON 등록 순서가 숫자로만 된 archive ID를 재정렬해 자산순서 비교1건이 실패했다(213tests,74.935초). Python SOURCES 순서의 명시 리스트로 plan 등록순서를 복원한 뒤 전체검사를 다시 통과했다. 번역/source/ROM을 바꾸어 우회하지 않았다. 최종 worklist/coverage 재생성 전후 SHA256도 동일했다. worklist: `1c36e7a6384a7e3cb13869a719fb1fa01d6c7dad7709876968362b3f9cb47760`, coverage: `01e3706b625f4d7eebed8e49f74c1076bb0fb181ce97d0bb6ff5b343589b181e`. 이는 기술/재현 검사이며 독립 문안 승인이나 실제 화면 증거가 아니다.

### 후속: 500묶음006 — 일정 메뉴488·대회12

이번 묶음은 stable catalog literal 정확히500개다. 670568/6762A8/686A60/697B70/6A9970/6BB2A4/6C0E38/6CBFC0의 일정·메뉴 각61개(총488),66C7D8 대회12개다. 일정 메뉴는 선택지184개와 서술304개를 구별한다. `tools/draft_batch500_006.py`에서 ID별 문안을 직접 작성했다. 공통 고정 라벨/선택지 후보는 모든 원문 literal/소비 문맥을 대조해 명시 ID에만 연결했으며, 원문 문자열이나 화자별 규칙으로 대사를 자동 생성하지 않았다. source/payload/TPL 해시·기존 ROM 선택·미작성 분모를 보존했다.

670568과66C7D8의 TPL 전체를 읽었고 나머지는 모든 literal과670568 제어 skeleton의 차이 토큰을 읽었다. 일정/기념일 등록2·7 및 삭제5·8, 지난 날짜3/등록 용량4/동시 일정25/덮어쓰기30/기념일31·32·33/삭제50·51·52, 서브칩40/장비41/라이브러리42/메일43/키 아이템44/저장45의 소비 문맥을 유지했다. 삭제50은 일정,51은 연월일·요일을 표시하는 기념일,52는 월일 기념일이다. 가변 이름 뒤의 이/가·을/를 문제를 피하도록 명시 ‘일정/기념일’을 두는 후보를 사용했으며 변수/순서/줄은 바꾸지 않았다. 소유격 의/님의는 이름 종성과 무관한 후보로 유지했다. 시간·AMPM·빈도·년도·월·일·요일·일정명·닉네임 buffer와 수치/패딩, width7/8, default0/1, BSeparate·clear 차이, flag3611/음467/wait1 및 hide/close/end 원형을 유지했다.

각 메뉴의 명시 SearchMan/FireMan/NumberMan/AquaMan/ShadowMan/NapalmMan/IceMan/PlantMan 초상화만 화자 근거로 사용했다. 이전 넘버맨 스크린샷으로 다른 캐릭터의 문안을 바꾸지 않았다. 계산 문제60/얼음 편지61/저격 훈련62와 사용 불가63은 원문대로 구별했다. FireMan·NapalmMan 메뉴에도 원문 저격 훈련이 있으므로 캐릭터의 이미지에 맞춘 임의 교정을 하지 않았다. AquaMan25에는 원문ぴゅ가 없어서 퓨를 덧붙이지 않았고, ShadowMan의 소인/기록 및 각 화자 질문·경고 말투는 검토 후보다. 메뉴의 모든61개 literal이 명시초상화 아래 소비되지만 새 초상화 개수 테스트의 초기 가정32는 실제31개와 달라31로 바로잡았다. 소스·문안을 수정해 검사에 맞춘 것이 아니다.

66C7D8의 패배 맞바람/앞으로 바뀔 바람 방향과 승리 순풍, 미신청10/메뉴 취소와 격려20..23의 별도 stable ID를 유지했다. 닉네임 삽입·flag3603·대기 분기는 보존하고 초상화 없는 quick 화자를 WindMan이라고 추정하지 않았다.

누적7437개 needs_review 초안, 미작성20015개. 새geometry47개(일정 메뉴46/대회1), 전체1144개다. 세부6705689/6762A84/686A603/697B708/6A997010/6BB2A44/6C0E385/6CBFC03/66C7D81. 보수적132px 계산은 실제 consumer 용량이나 화면 오류의 증거가 아니므로 자동 축약·재배치하지 않았다. 원본/기준ROM 해시 불변, ROM 빌드·세이브 변경·실제 화면 검증 없음. 모든 문안은 NON-DISTRIBUTION/needs_review이며 전체 번역 완료나 인간 승인·배포 적격 판정이 아니다.

신규6검사 포함219tests PASS(84.586초), 신규500개 별도 기술 검사/py_compile/자산 재생성 동일 PASS. 초기 전체219검사에서 새 초상화 명령 개수 테스트의 예상32와 실제31 차이1건이 실패했다(82.955초). 실제 원문 명령을 재계수해 테스트만31로 수정한 뒤 전체검사를 통과했다. 이 테스트 파일 해시 갱신을 파생물 provenance에 반영한 최종 worklist/coverage의 재생성 전후 SHA256이 일치했다. worklist: `0b1fc98aa5b922b01593a17564e9a82dd1ae003ff6d533998a8e5ff477a74df9`, coverage: `6e6bbd813ca6ba3a7a2aeb9f59a920787a11e8aa8efb16fa5408a2b4d3698dac`. 새 ‘계산 문제’와 이전 롤 초안 ‘계산 문제집’은 같은ドリル의 미승인 문안 후보 차이로 남겨 통일 검토해야 한다. 이는 기술 검증이며 인간 문안 승인이나 실제 표시·저장 증거가 아니다.

## 500개 묶음007 — 일정·메뉴477 / 메일14 / 아쿠아맨 인사9

`tools/draft_batch500_007.py`로 정확히500개 stable literal 초안을 추가했다. 유일 문장500개가 아니며 선택지180개/서술320개다. 67BCF4·68CBFC·692874·69D8D4·6B525C는 각각57개,6811F0·6A2FBC·6C6828은 각각64개,6C2660은14개,698424는9개다. 계획 파일에007의 순서·정확한 ID별 자산을 기록했다.

전체6811F0/6C2660/698424 TPL과 나머지 메뉴의 모든 literal 및 제어 skeleton 차이를 읽고 source ID마다 수동 작성했다. 공통 선택지·고정 라벨은 기존 미승인 후보를 consumer별로 대조해 재사용했고, 대사는 원문 문자열 규칙으로 일괄 치환하지 않았다. 메뉴는 명시 ThunderMan/MetalMan/JunkMan/WoodMan/KnightMan/ProtoMan/StarMan/ElecMan 초상화로 구분한다. 메일에는 화자를 추정하지 않았고, 아쿠아맨 인사1만 발화의 자기소개로 식별했다. 귀환2는 초상화·명시 이름 없는 quick 화자로 남긴다. 이는 다른 캐릭터 대사를 넘버맨으로 교체하거나 임시로 게임 상태를 바꾸는 작업이 아니다.

일정/기념일 등록2/7·삭제5/8,과거3,용량4,중복25,덮어쓰기30,기념일31..33,일정삭제50/날짜있는기념일51/연례기념일52를 구분했다. script3의 닉네임은 ProtoMan에만 있고 나머지7명은 없으므로 추가하지 않았다. 닉네임 뒤 소유격 의/일정·기념일 명사를 사용해 가변 이름 받침에 의존하지 않는 후보를 작성했다. 실제 훈련은 ProtoMan/StarMan60계산·61얼음편지,ElecMan60계산·62저격이며 나머지5명에는 훈련 script가 없다. 새 계산 문제집은 기존 롤 후보를 참고하되006의 계산 문제 차이는 미승인 용어 검토로 유지한다. 정크맨의 더듬음은 실제0/3/4/20/22/31 원문에만 대응했다.

메일1..3 닉네임,2만 callTournamentReceiveMail,flag680/681/623..626 및9056..9062,원문 !!14개와 box/text/arrow 위치·sound155·wait96을 보존했다. 인사·귀환의 퓨/기억/울음/소란으로 버림받았다는 걱정도 개별 ID로 유지했다. 날짜·시간·AMPM·빈도·요일·일정명 버퍼,선택 폭7/8,default0/1,BSeparate/clear,flag3611/track467 및 미선택 구분자·공백·괄호는 바꾸지 않았다.

누적7937개 needs_review 초안, 미작성19515개. 새geometry38개(일정메뉴36/아쿠아맨인사2), 전체1182개다. 세부67BCF4:6/68CBFC:3/692874:2/69D8D4:3/6B525C:4/6811F0:9/6A2FBC:5/6C6828:4/6C2660:0/698424:2. 보수적132px 계산은 실제 consumer 용량이나 화면 오류 증거가 아니므로 자동 축약하지 않았다. 원본/기준ROM 불변, 빌드·세이브·화면 검증 없음. 모든 신규 문안은 NON-DISTRIBUTION/needs_review이며 전체 번역 완료·인간 승인·삽입 준비·배포 적격이 아니다.

신규6검사를 포함한 전체225tests PASS(100.799초). 신규500개 별도 기술 검사,py_compile,자산 재생성 동일 PASS. 초기225검사에서는 새 메일 검사에 literals 가져오기가 누락되어1건 오류(96.851초)가 발생했고, 검사 코드의 import만 보완한 뒤 전체 재검사를 통과했다. 초안·ROM 변경으로 오류를 우회하지 않았다. 파생물 재생성 전후 SHA256 동일: worklist `7c540da8dc59ebcce251827d58316eb6198642c28da3a3a5f3110c5e05a6ac2f`, coverage `947acefabd9bd4322d25c1e999b11a959fafd5a4fdd09c007aa8d7e7391f8a17`. 임시·디버그·글자판·화자 미확인 항목은 원문/미작성 분모에 남겨 두었다. 기술 통과는 실제 화면·저장 증거 또는 인간 문안 승인이 아니다.

## 500개 묶음008 — 개인정보·칩 대사401 / 메뉴67 / 알림24 / 짧은 대사8

`tools/draft_batch500_008.py`로 정확히500개 stable literal 초안을 추가했다. 65CC78:196/66DDD0:205/659CB8:67/671684:18/66A160:6/66C978:6/65AA80:2이며 유일 문장500개가 아니다. 선택지27개와 서술473개를 구별한다. 원문에 시트 보고를 요청하는 내부 오류65CC78:0:0/66DDD0:0:0은 consumer 미확인으로 보존하고 전체 미작성 분모에 남겼다.

모든 신규 literal과 전체 제어 skeleton을 읽었다. 65AA80/671684/66A160/66C978은 TPL 전체를 읽고, 두 대형 archive와659CB8은 literal 목록 및 모든 제어·변수·페이지 순서를 함께 읽었다. 학교·형제자매·친구·취미·꿈·좋아하는 사람·껄끄러운 사람·음식·방송·존경하는 사람·잘하는/못하는 과목·원하는 물건과 상대 전적·선호 칩의 실제 print 명령을 구분해 ID별로 수동 작성했다. 66DDD0:71의 사람은 실제 printMostDefeatedOpponent이며 인접한 다른 상대 변수로 바꾸지 않았다.

초상화 없는 대사는 바람/거츠 말투나 주소만으로 내비를 확정하지 않았다.659CB8의 명시MegaMan 메뉴와671684:21..26의 명시SearchMan 알림만 초상화 화자를 기록했다.659CB8에는 계산60/얼음편지61/저격62 모두 실제 존재한다. script3에는 닉네임이 없고10/25에는 있어 그대로 보존했다. 671684는quick1..6과초상화21..26,방송/약속/식사/학원/기타/추가알림을 분리했고flag3658·sound155·wait96 및 현재이벤트 반복을 유지했다.66C978은 곧 시작할 일정과 오늘 일정의 없음/여러항목 루프,시간·분·AMPM을 보존했다.66A160은 주말 토너먼트 준비/당일/키아이템을,65AA80은 수고 인사/패배 후 다음 도전을 구분했다.

원문 가변 삽입 앞뒤의 말이야/하고/에게/의 및 칩·과목·음식 등 문맥별 명사를 사용해 임의 이름 받침에 의존하는 조사를 피한 후보를 작성했다. 풍수·순풍/맞바람의 비유,남서쪽77/북북동쪽86,숫자1장과R버튼,프로그램 어드밴스를 보존했다.65CC78:50의 가상 선물은 실제 아이템 지급이라고 번역하지 않았다. 브루스 언급53:3은 원문에 있지만 그것만으로 화자를 확정하지 않았다. 이런 표현은 미승인 문안 후보이며 입력 값 전체의 실제 표시·저장·배치 검증이 필요하다.

누적8437개 needs_review 초안, 미작성19015개다. 새geometry30개(개인정보·칩24/메뉴5/짧은대사1), 전체1212개다. 세부65CC78:6/66DDD0:18/659CB8:5/671684:0/66A160:1/66C978:0/65AA80:0. 보수적132px 계산은 확정된 consumer 용량이나 화면 오류 증거가 아니므로 자동 축약·재배치하지 않았다. 원본/기준ROM 불변이며 ROM 빌드·세이브 변경·실제 화면 검증은 하지 않았다.

신규6검사를 포함한231tests PASS(101.325초),py_compile 및 자산 재생성 동일 PASS. 초안 작성 중66DDD0:59:1의 원문 줄 수와 후보 줄 수 차이를 발견해 원문에 맞게 후보를 수정한 뒤 생성했고,가변 이름 뒤의 선물 조건문과 만나러 가는 문장도 ID별로 검토·수정했다. 이전 배치 문안은 바꾸지 않았다. 초기231검사에서는 신규 선택지 수 예상28과 실제27 차이1건이 실패했다(99.692초). 원문을 재계수해 신규 테스트·계획·설명 메타데이터만27선택지/40메뉴서술로 정정하고 전체 재검사를 통과했다. 번역·ROM을 바꿔 검사를 우회하지 않았다. 파생물 재생성 전후 SHA256 동일: worklist `259aed2e43b198f588b16e1793d30089752babf792d4da855d4726e245c09c7d`, coverage `a3a59500a4b765454e7c1c35086da27bc87f744e07c797a625f82eff8af3f19b`. 모든 신규 문안은 NON-DISTRIBUTION/needs_review이며 기술 통과는 전체 번역 완료·인간 승인·삽입 준비·실제 화면/저장 증거·배포 적격 판정이 아니다.

### 후속: 500개 묶음009 — 개인정보459·메일29·대회11·플러그인1

`tools/draft_batch500_009.py`의7개 자산은 66CA84 개인정보139/672238 개인정보162/677F64 개인정보158/66C264 메일14/671958 메일·미션15/671F24 대회11/65AF54 플러그인1로 정확히500 stable literal이다. 선택지72/서술428개이며 유일 문장500개가 아니다. 누적8,937개 초안, 미작성18,515개. 이전 자산·현재 ROM 선택 항목은 변경하지 않았다.

세 프로필의 모든 literal,66CA84 전체 control skeleton과672238/677F64의 전체 skeleton 차이를 읽었고 나머지4개 TPL은 완문을 읽었다. 형제자매·친구·음식·취미·장래꿈·좋아하는 여성/남성·존경인물·니가테인물·TV·자신있는/없는 과목·희망물건·유치원/학교/회사 및 추가등록/응답감상을 ID별로 작성했다. 프로필17 global22 value1→19와32 global23 values1..5→33/6..9→34 분기를 보존했으며 실제 연령이나 플레이어 성별을 임의 확정하지 않았다. 12선택창×3프로필,default0/BSeparate/clear/targets,buffer1/2/3 및 count5 확인,3605/3606 입력 인계와 음수응답 플래그3735..3739/3741/3746/3749는 원문 그대로다.

모든 선택 대사는 초상화 없는 quick 화자로 기록했다. 바람/풍경,미션/데이터,불/열기 문체는 후보이며 화자 증명이 아니다. 기존 넘버맨 화면이나 인접 archive를 근거로 화자를 붙이지 않았다. `형이나 오빠`/`누나나 언니`는 플레이어 성별 추정을 피한 후보,風鈴의 `풍경`은 경치가 아닌 wind chime,恋焦がれる의 `사랑에 불타다`는 사랑/타는 열기 비유를 보존한 검토 전 후보이다. 이름 뒤에 의/말고/께서 등을 사용하되 실제 동적 이름 길이·가족 호칭·문체·말장난은 인간 및 화면 검토가 남는다.

메일29개는 닉네임 포함1..3/일반4..7/mailadd20..26,8928..8934 대8936..8942를 구별했다. 671958:10의 미션 지령과 실제 SearchManMissionBegin/ReceiveMail·3767 clear·3613/3785 set는 보존하되 초상화 증거로 확대하지 않았다. 대회실패의 우승확률99퍼센트·작전미비 가능성,성공,참가미등록/CancelMenuTransition,4개 시작의 록온을 구별했다. 플러그인 구호의 명시록맨.EXE는 전송 대상이지 화자 증명이 아니며 TYPE3/3603·3651/wait30도 그대로다. 일본어 없는 、와!! literal은 미번역 문장으로 치환하지 않았다. 미확인 임시/내부오류는 기존 원문/분모를 유지한다.

신규6검사 포함237tests PASS(117.045초),py_compile·초안 자산 재생성 동일·파생물 재집계 동일 PASS. 최초237검사에서는 신규 테스트의 효과음 인자명sound(실제track155)와 연속 플래그 번호 가정2건이 실패했다(110.225초). 원문을 다시 읽고 테스트만 track 및 실제 플래그 집합으로 정정했으며 번역/원문/ROM을 바꿔 검사를 우회하지 않았다. 초안 생성 전66CA84:17:2/19:2 마지막 줄바꿈 오류2개도 원문3줄에 맞춰 수정했다. 새40개 배치 재검토 표시(프로필12/8/4,메일14,대회2), 전체1,252개; 보수적132px 산식이며 실제 넘침/consumer예산 판정은 아니다.

파생물 재생성 전후 SHA256 동일: worklist `f7ee6dacb8eee1720fb4389e91c6ce7d06856c2ce1f1cea0e883f43ebf919e5b`, coverage `af074b4e424d3cfba79d75775410e9aba7ce0f1f1b6e5c35076b252c04c21701`. 원본8,388,608bytes 및 기준11,157,488bytes ROM SHA256 불변. ROM 빌드·삽입·에뮬레이터·저장·이미지 변경 없음. NON-DISTRIBUTION/needs_review이고 실제 화면/저장 검증이나 인간 승인·전체 완료·배포 적격 판정이 아니다.

### 후속: 500개 묶음010 — 개인정보410·메일42·일정알림38·대회10

`tools/draft_batch500_010.py`의9개 자산은 688A10 개인정보142/68E8C4 개인정보132/6942F0 개인정보136/6881C4 메일14/68E0B4 메일14/693AA4 메일14/6937C4 일정알림18/693FEC 대회10/687E88 일정알림20로 정확히500 stable literal이다. 선택지72/서술428개이며 유일 문장500개가 아니다. 누적9,437개 초안, 미작성18,015개. 이전 번역 자산·ROM 선택 항목은 변경하지 않았다.

세 프로필의 모든 literal과688A10 전체 control skeleton,68E8C4/6942F0 전체 skeleton 차이를 읽었다. 작은6개 TPL도 전체를 읽었으며693AA4 출력 잘림 부분은 공백을 압축한 완문으로 다시 읽었다. 개인정보17 global22 value1→19 여성/남성 질문 및32 global23 values1..5→33학교/6..9→34회사/그외유치원,12선택창×3프로필,buffer1/2/3/count5 확인 및3605/3606 입력 인계를 보존했다. 플레이어 성별·정확한 나이·화자를 임의 추정하지 않았다.

688A10은 공격력 덧셈/곱셈 취미와 피타고라스·계산 불가능한 배틀/미래를 구별했다. 68E8C4는 주먹 수련·온천·전뇌최강 꿈·휴식과 수련을,6942F0는 말더듬·버그 조각 식욕·쓰레기 수집·아이돌 내비 꿈·사용자 친밀감·공부를 가르치고 싶다는 문맥을 살렸다. 형이나 오빠/누나나 언니·수학자 표기·말투는 검토 전 후보이다. 좋아한다는 표현을 특정 연애 관계로 확정하지 않았고,버그 조각을 먹고 싶다는 말을 실제 지급으로 바꾸지 않았다. 님/말이다/말이야/의/말고와 방송·약속·일정 명사를 사용해 가변 이름의 받침 의존 조사를 피했다. 이름 길이·입력/저장·전체 배치는 실제 검증 전이다.

687E88 알림21..26만 명시NumberMan,6937C4 알림21..26만 명시JunkMan이다. quick1..6 및 프로필·메일·대회는 모두 미표시 화자로 유지했다. 기존 넘버맨 스크린샷이나 수학/주먹/쓰레기 모티프·archive 인접성은 화자 증명이 아니다. 메일3묶음의8968..8974/8976..8982/8984..8990 및680/681/수신call을 구별했다. 알림TV/약속/식사/학원/기타/추가3658 루프를 유지하며 넘버맨형 식사·학원·기타의 닉네임 삽입과 정크맨형의 미삽입을 구별했다. 대회 패배에는 열심히 오퍼레이트해 주었음에도 졌다는 의미를 유지하고 우승·참가미등록·20..23 최선/3603 clear를 구별했다. 일본어 없는!!,688A10:17:3/19:3 및687E88:5:0/25:0의 구두점은 원문 그대로다. 기존 미확인 임시/내부오류/구조항목도 분모에서 제외하지 않았다.

신규6검사 포함243tests PASS(106.325초),py_compile·초안 자산 재생성 동일·파생물 재집계 동일 PASS. 새로운37개 배치 재검토 표시(프로필8/10/12,정크알림2,대회5),전체1,289개. 보수적인132px advance 계산이며 실제 consumer별 예산이나 화면 넘침 판정이 아니다. 자동 축약·제어/페이지 이동은 하지 않았다.

파생물 재생성 전후 SHA256 동일: worklist `7a27639d1fdb82ec4b28be76531ddb4653ab94eff563ba5467cc20920a123153`,coverage `a11717536fe9467712ece9477f071a9228fb3d731d8e365392e8d0e0415e308f`. 원본8,388,608bytes 및 기준11,157,488bytes ROM SHA256 불변. ROM 빌드·삽입·에뮬레이터·저장·이미지 변경 없음. 모든 새 문안은 NON-DISTRIBUTION/needs_review이며 기술 통과는 인간 승인·실제 화면/저장 검증·전체 완료·배포 적격 판정이 아니다.

### 후속: 500개 묶음011 — 개인정보438·메일28·임무/훈련27·일정6·접속1

`tools/draft_batch500_011.py`의8개 자산은69F220 개인정보145/6A5814 개인정보144/6AB70C 개인정보149/69EA0C 메일14/6A504C 메일14/6AA730 임무·훈련27/6AB600 일정6/6AAB08 접속1로 정확히500 stable literal이다. 선택지72/서술428개이며 유일문장500개가 아니다. 누적9,937개 초안, 미작성17,515개. 이전 초안과 ROM 선택 항목은 변경하지 않았다.

세 프로필의 전체 literal 및 이전에 완독한688A10 기준 control skeleton과의 전체 차이, 작은5개 TPL 전체를 확인했다. 별똥별94와 irregular 형제자매 선택지, 개인정보17/19·32/33/34 분기를 별도로 확인했다. 모든 새 항목은 초상화 미표시 quick 화자이며 archive 인접성·기존 넘버맨 스크린샷·모티프만으로 화자를 확정하지 않았다. 접속 구호의 명시 섀도맨.EXE는 접속 대상이지 오퍼레이터 화자 증명이 아니다.

69F220의 야채·공유하는 꿈·인터넷에 없을지도 모르는 물건의 검색 약속을 유지했다. 6A5814는 운세 가능성·다음 주 배틀운과 별똥별에 소원만 빌어 준다는 대사를 실제 물건 지급과 구별했다.94는 닉네임이 아닌 printEntryBuffer 희망물건 삽입이다. 6AB70C는 위협 뒤의 농담·무익한 살생 금지·의뢰 예외를 모두 보존했다. 1人는 혼자 독학한다는 뜻이고1人前는 어엿한 실력을 갖춘다는 관용구로, 수량 의미를 추가하지 않았다. 숫자1은 원문 검증 정책에 맞춰1인/1인분 표현에 유지했으며 이 표현·시대극·수리검·소인/그대·가족 호칭은 인간 검토 전 후보이다.

각 프로필12선택창의 기본값·BSeparate·clear·대상,buffer1/2/3/count5 및3605/3606 입력 인계,gender22/education23 분기,69F220:95의end→waitHold를 유지했다. 원문 없는 구두점69F220:9:0은 그대로다.6AA730:0:0 임시かりです는 번역하지 않고 원문/미작성 분모에 남겼다.

메일9000..9006과9024..9030,수신call·680/681·track155·wait96을 구별했다. 임무 성공9244/6051/complete와 실패9243/6052/3632/fail,남은 분 출력과 긴급 메시지13,훈련minigame2의 결과71..73을 보존했다. HP 메모리 item33/amount1과 dynamic 제니·버그 조각 지급을 구별하며4294967295·buffer3·버그 조각 앞뒤의 출력 순서·padLeft를 유지했다. 일정soon/today 루프·시/분·AMPM과 접속TYPE3/3603/3651/wait30도 변경하지 않았다.

신규6검사 포함249tests PASS(118.090초). 초안 자산 재생성 동일,py_compile 통과. 이번47개(프로필8/20/16,임무·훈련2,일정1),전체1,336개가 보수적132px advance 검토 대상으로 표시되었다. 실제 consumer별 용량·화면 넘침 판정이 아니므로 자동 축약이나 제어/페이지 이동은 하지 않았다.

파생물 재생성 전후 SHA256 동일: worklist `8dbcee64188f80c8c7c7e79265fda0db932d031ff5ab907ec3c6f4d32448a0f3`,coverage `d2a91de869030549e0b1be3f38ce52bf9406e2478f80ac27e889346e77fd6d91`. 원본8,388,608bytes 및 기준11,157,488bytes ROM SHA256 불변.

ROM 빌드·삽입·에뮬레이터·저장·이미지 변경 없음. NON-DISTRIBUTION/needs_review이며 기계적 검증은 인간 승인·실제 화면/저장 검증·전체 완료·배포 적격 판정이 아니다.

### 후속: 500개 묶음012 — 개인정보474·메일14·일정6·인사6

`tools/draft_batch500_012.py`의6개 자산은6B6CA4 개인정보187/6BCFBC 개인정보163/6C2E4C 개인정보124/6B6474 메일14/6B6B98 일정6/6B5A70 인사6으로 정확히500 stable literal이다. 선택지72/서술428개,누적10,437개 초안·미작성17,015개이다. 원문 반복도 별도의 stable ID로 유지했으며 이전 초안과 ROM 선택 항목을 변경하지 않았다.

모든 profile literal과688A10 기준 전체 control skeleton 차이,작은3개 TPL 전체를 읽었다. 첫 skeleton diff는 공백 정규화로 잘렸으므로 TOKEN literal만 대체한 multiline 전체 diff를 다시 읽었다.6B6CA4:83/6BCFBC:9/6C2E4C:31의 닉네임과 구두점을 포함한 실제 TPL도 별도 확인했다. 세 프로필의12선택창·22성별1→19/23교육1..5학교·6..9회사·그외유치원·buffer1/2/3/count5·3605/3606·기본값/취소/clear·줄/공백을 보존했다.6B6CA4:83:1/6BCFBC:9:2/6C2E4C:31:4의 일본어 없는 구두점은 원문 그대로이며 임시/내부오류 항목도 분모에서 임의 제외하지 않았다.

기사풍 문맥의 충성심·꿈·예의·경의·어린 사람 보호·잔 다르크의 용기·관용구 ハナが高い의 자랑스러움을 유지했다. 전쟁영화 폭발·전뇌 화약/가솔린의 가상 식욕·화학·프로 배틀러 가능성·소방관에게 자신도 꺼질지 모른다는 농담·플레이어 부재 중 다른 가족에게 오퍼레이트를 부탁할까 하는 질문을 구별했다. 현실 폭탄 제조 지침이나 실제 가족 입력 이벤트를 추가하지 않았다. 부드러운 말투의 친구/칩 수집·세계 최고 넷 내비 꿈과 휴대용 냉동고를 주마등처럼 떠올리는 회상은 실제 보상 지급이 아니다. 가족 호칭·기사/나이트맨/잔 다르크 표기·세 말투는 승인 전 후보이다.

원문은 모두 초상화를 표시하지 않는다.6B5A70:1 자기소개만 명시 나이트맨이며 이를 adjacent profile·복귀 목소리의 화자 확정에 전이하지 않았다. 기존 넘버맨 스크린샷도 이 대사 화자 증명이 아니다. 님/의/말고로 가변 이름의 받침 의존 조사를 피했고6C2E4C의 좋아하는 사람·존경/대하기 어려운 사람·유치원/학교/회사 문구7곳은 작성 후 수동 재확인에서 님이 주어 형태로 고쳤다. 이름 길이·입력/저장·실제 배치는 아직 검증 전이다.

메일9040..9046/수신call·680/681/track155/wait96 및 일정soon/today 반복·시/분/AMPM·이벤트 이름을 보존했다. 인사에는 주군의 이름 삽입과 떠나 있었어도 변함없는 충성을 유지했다. 모든 새 문안은 NON-DISTRIBUTION/needs_review,실제 ROM builder 미선택이다.

신규6검사 포함255tests PASS(114.125초),py_compile·초안 재생성 동일 PASS. 이번38개(프로필26/5/6,일정1),전체1,374개가 보수적132px advance 재검토 표시이다. 실제 consumer별 용량·화면 넘침 판정이 아니며 자동 축약·페이지 이동은 하지 않았다. ROM 빌드·삽입·에뮬레이터·저장·이미지 변경 없음. 기술 통과는 인간 승인·실제 화면/저장 검증·전체 완료·배포 적격 판정이 아니다.

파생물 재생성 전후 SHA256 동일: worklist `749ee6ac0bf56388d785e454d55be8bd38be9f2ed42a43368df17c3c117f4fd8`,coverage `e43130517bc822bbe75016c64dc1b07b168861a16144f2c1762bde6787d98d45`. 원본8,388,608bytes 및 기준11,157,488bytes ROM SHA256 불변.

### 후속: 500개 묶음013 — 개인정보405·메뉴56·훈련28·대회10·접속1

`tools/draft_batch500_013.py`의7개 자산은6C84C8 개인정보138/6CDCD0 개인정보141/6D32EC 개인정보126/6D1984 일정메뉴56/6C7608 훈련결과28/6C2B8C 대회10/6C79E8 접속1로 정확히500 stable literal이다. 선택지93(프로필72/메뉴21)·서술407개,누적10,937개 초안·미작성16,515개이다. 이전 번역과 ROM 선택 항목을 변경하지 않았다.6C7608:0:0 임시かりです는 원문과 미작성 분모에 남겼다.

모든 프로필 literal 및 이전에 완독한688A10 기준 전체 control skeleton 차이를 읽었다.6C84C8:1/31,6CDCD0:17,6D32EC:41 실제 TPL도 독립 확인했고 다른4개 TPL은 전체를 읽었다.6C84C8:25:2의 최초 수동 초안 줄 수 차이는 생성 전에 원문2줄로 수정했다. 숫자·줄 수·시작/끝 줄바꿈·선택지 공백·ID·source·TPL/payload·기존 선택을 보존했다.

전기 대사는 화력과 풍력 발전소를 구별하고 사랑/짜릿함·건전지 수집·등줄기 전류 비유를 유지했다. 우승했을 때 원하는 것을 얻는다는 말은 조건부 가정이지 지급 보장이 아니다. 꽃 대사는 물/공기·꿀·삶의 윤기·거목/해바라기/장미/은방울꽃·100송이 장미 비교와 마음속 꽃·꿈의 꽃봉오리를 유지했다.17/19는 gender22분기가 있지만 원문 자체가 동일한 성별 중립 사랑의 이메일 문구이므로 임의 남녀 표현을 넣지 않았다. 거친 대사는 강자 추구·상대의 약점 잡기·욕망·라이브러리 완성자에 대한 경멸을 부드러운 친근함으로 바꾸지 않았다.1人는 혼자 단련한다는 뜻을1인 독학 표현에 보존했으며 말투·가족 호칭·비유·명칭은 승인 전 후보이다.

각12프로필 선택창과gender22/education23(1..5학교·6..9회사·그외유치원),3605/3606·buffer1/2/3/count5·기본값·취소·clear를 보존했다.6D32EC:41의 끝 줄바꿈1개/spacePx16과 다른 확인창2개/24를 구별했다.6D1984의29개 스크립트만 명시Bass 초상화이며 이를 인접 프로필 화자로 확정하지 않았다. 기존 넘버맨 스크린샷·전기/꽃/거친 모티프도 화자 증명이 아니다. 일렉맨.EXE 접속 구호는 명시 접속 대상이지 오퍼레이터 목소리 식별이 아니다.

메뉴 등록·과거 날짜·용량·동시간 충돌·덮어쓰기·기념일/일정 삭제·현재/이벤트 날짜·빈도·AMPM·이벤트 이름을 구별했다.21메뉴 선택지·TYPE/기본값·width7/8·BSeparate·3611 clear·wait1·mugshotHide/msgCloseQuick/end를 유지하며 실제 저장 기능 설명을 저장 실행으로 바꾸지 않았다. 삭제 검증을 위해 사용자 데이터를 지우지 않았다.

훈련 minigame0 문제집50..53과minigame2 집중력70..73의 실패/성공·HP 메모리 item33/amount1·제니/버그 조각 amount4294967295·buffer3·출력 순서/padLeft를 보존했다. 대회 패배와 우승·감동을 냉동 보관한다는 비유·미등록 취소·20..23격려/3603clear를 구별했다. 접속TYPE3·3603/3651·wait30은 원문대로다.

신규6검사 포함261tests PASS(112.771초),초안 재생성 동일·py_compile 통과. 이번55개(프로필10/6/22,메뉴11,훈련4,대회2),전체1,429개가 보수적인132px advance 재검토 표시이다. 실제 consumer 용량·화면 넘침 판정이 아니며 자동 축약·페이지 이동을 하지 않았다. NON-DISTRIBUTION/needs_review이고 인간 승인·ROM 삽입·실제 화면/저장 검증·전체 완료·배포 적격 판정이 아니다. ROM·에뮬레이터·저장·이미지 변경 없음.

파생물 재생성 전후 SHA256 동일: worklist `f022eb3b5cbdba9b2c63a529ec2c6ffee693bad94bccc926cb1b89963e0467c2`,coverage `df642586fad9e8e2b9c05f2fc53971d3654aff9385be4a1c0e775cad46197a45`. 원본8,388,608bytes 및 기준11,157,488bytes ROM SHA256 불변.


## 500개 묶음014 — 개인정보 후속·칩·안내 초안 (2026-10-11)

`tools/draft_batch500_014.py`의15개 자산:6C982C194/6CF0A0209/6CB0808/6CB6C03/6CC8086/6CCD404/6CCDC016/6CD0681/6CD48C14/6CD9E415/6CDBC86/6C7A3420/6D26A02/6D27A01/6C231C1로 정확히500 stable literal이다. 개인정보후속403·힌트8·배틀3·인사6·귀환6·훈련16·접속3·메일14·대회15·일정6·알림20이며 선택지 없이 서술500개다. 누적11,437개 초안·미작성16,015개. 원문/TPL/payload·이전 초안·현재ROM선택은 불변이다.

모든 원문 literal과 제어 skeleton을 읽었다. 큰 스크립트는 공백만 압축한 전체 명령/인수 보기로 확인하고 일정조회/귀환/플러그인은 실제TPL도 확인했다. 대량 prose 치환 없이 ID별로 작성했다.6C982C:0:0/6CF0A0:0:0 오류보고와6CCDC0:0:0 임시かりです는 원문/미작성 분모에 남긴다. 별도6D2700:0:0 임시문구도 읽었으나 번역하지 않았다.

전압과 전류,30만/100만 볼트와60/50/40볼트,3호/4호/버튼 전지와 찌릿함 비유를 구별했다. 식물의 꽃잎·비료·삶의 영양소·엽록소·불꽃 약점,인간의 어려운 과목과 노력을 통한 극복을 구별했다.카로틴/냉이/전지 규격은 용어 검토 전 후보이며 원문つくしい는 직전美しい 문맥에 따라 아름다운 후보로 작성하고 source 오기를 고치지 않았다. 메일 거부 대사는 서술 의미를 유지했으며 필터가 구현됐다는 증거로 보지 않는다.

실제 school/family/food/hobby/dream/enemy/TV/subject/opponent/chip print 명령과 페이지·숫자·줄·공백은 그대로다. 동적 삽입 뒤에는 말이다/말이야/의/하고 또는 주제 생략으로 받침 고정 조사를 피했다.6C7A34:21..26만 명시ElecMan 초상화를 연결했다.6CC808:1의 플랜트맨 자기소개는 그 script의 근거일 뿐,인접 quick 화자 확정 근거가 아니다. 플러그인의 내비 이름과 구호 화자는 별개로 기록했다.

훈련minigame0 결과1→HP메모리33/수량1,2→제니,3→버그조각·4294967295·buffer3 출력 순서/패딩을 보존했다. 메일680/681·623..626·9072..9078/수신처리·155음/96frame×2,일정 hour/minute/AMPM/name 조회 루프,TV/약속/식사/학원/기타 알림의3658,대회 미등록취소/3603·벚꽃 낙화/다시 피는 비유를 유지했다.

신규6개 포함267tests PASS(116.179초),초안 재생성 동일. 원문·제어·BDF글리프/codec 검증·py_compile 통과. 이번48개(개인정보후속22/15,힌트2,훈련4,대회5),전체1,477개는 보수적132px advance 재검토 표시이지 실제 consumer 용량이나 화면 넘침 판정이 아니다. 자동 축약/재배치를 하지 않았다. needs_review/NON-DISTRIBUTION이며 인간 승인·ROM삽입·실제화면/저장 검증·전체 완료·배포 적격이 아니다.

파생 worklist SHA256 `b7bcd45c08c8b939365930d9c21e43facaac2b0e0e1978fb9e002d65c3df5d41`,coverage SHA256 `2df9e02428f5a9434cc428381a8a211ab07aa74857692256f32e738762876c1b`. ROM·에뮬레이터·저장·이미지 변경 없음.


## 500개 묶음015 — 후속 대사·게임 내 의뢰·알림 초안 (2026-10-11)

`tools/draft_batch500_015.py`의12개 자산은6D44D4(183)/6DED88(220)/6D27EC(26)/6D2B34(14)/6D3050(8)/6D31E4(5)/6D59B8(7)/6D5EB0(3)/6C7D04(14)/6C8230(8)/6C83BC(6)/6D0A08(6)로 정확히500 stable literal이다. 후속183·의뢰220·알림26·메일28·대회16·일정11·힌트13·배틀3이며 선택지 없이 서술500개다. 누적11,937개 초안·미작성15,515개. 기존 초안/원문/현재ROM선택은 불변이며6D44D4:0:0 내부오류는 원문과 미작성 분모에 남겼다.

모든 원문 literal과 전체 제어 skeleton을 읽고 ID별로 직접 작성했다. 큰 스크립트는 공백만 압축한 전체명령/인수 보기로 확인하고 의뢰0/27..30의 실제TPL도 읽었다. 화자 identity를 저장 순서나 전기/꽃/경멸 비유로 확정하지 않았다.6D27EC:21..26만 명시Bass 초상화이며1..6quick은 별도다.6DED88의 의뢰 메시지는 호출자로부터 계승되는 화자 미확정 상태,28:1/2와29/30은mugshotHide뒤 시스템 획득 안내이다.

32개 가상 암살 의뢰(33..64)의 인터넷1..12/언더인터넷1..4·20/25/30/35/40/50/60분과 초록/빨강/갈색/검정·노멀/오피셜/힐/소녀 타입을 대조했다. 대신의 비밀방문/기업스파이/배신자·같은냄새 단서/정치인 선거/사채업자·빌려준돈의 아이러니/연적/음악가추방/대학병원장경쟁/가짜다크칩/프로그램째 제거/증인/범죄집단대립 문맥을 구별한다.43의トイチ는 열흘에 일할 이자,41의センセイ는 선거 문맥의 의원 나리 후보이다. source의いろか/しゅりょう/ノーマルビ 등 표기는 바꾸지 않고 문맥 해석 후보로만 번역했다. 새 용어·말투는 인간 검토 전이다.

의뢰 시작9728/분기32→33..64/없음65·실패27의erase,9756 false→31 무보상 응답,성공28HP메모리33/수량1·29제니·30버그조각4294967295/현재내비+buffer3/정렬·소거를 보존했다. 성공하면 보상을 메일로 보내겠다는 의뢰 문장과 실제 지급 메시지를 구별하며 실제 실행/배달을 증명한 것으로 보지 않는다.

후속 대사는 최강/배고픔/상대전적/칩타이밍/의존경고를 유지하고 메일 삭제27의 명시농담과31의 선언을 구별했다.78은 두번째 선호칩과 첫번째 선호칩의 비교이다. 학교/가족/과목/꿈/칩/상대 이름은 의/하고/말이다 또는 주제 생략으로 받침 고정 조사를 피하고 원래 줄/페이지/변수순서는 그대로다.46의1人은1명 단독 의미의 초안이며 자연스러움 재검토 대상이다.

메일9064..9070/9080..9086·680/681·623..626·155음/96frame×2·닉네임 분기,일정hour/minute/AMPM/name조회 루프/시간정렬·구두점,TV/약속/식사/학원/기타 알림과3658,대회 미등록취소/격려3603·승리후충전/큰꽃 비유를 유지했다. 배틀/실패 문구의 말줄임은 원래 literal/줄 경계를 보존한 후보이다.

신규6개 포함273개 회귀 검사 PASS(122.541초). 원문·제어·BDF글리프/codec 검증·py_compile 통과. 이번84개(후속28/의뢰43/알림4/대회8/일정1),전체1,561개는 보수적132px advance 재검토 표시이지 실제 consumer 용량·화면 넘침 판정이 아니다. 자동 축약·재배치를 하지 않았다. needs_review/NON-DISTRIBUTION이고 인간 승인·ROM삽입·실제화면/저장 검증·전체 완료·배포 적격 판정이 아니다.

파생 worklist SHA256 `2ea08c66ece6f08c168136dee5f410f497b40664278c9d706c8908513fe3da5d`,coverage SHA256 `048d0fb94642dc1c25e4c853904d8d4acbe07c3803b28a98000dd4276cadec5d`. ROM·에뮬레이터·저장·이미지 변경 없음.

## 500개 묶음016 — 메일함·임무 메일·장비 초안 (2026-10-11)

`tools/draft_batch500_016.py`의7개 자산은677318(1)/6DD0B8(77)/6DD864(42)/6DF988(153)/6E01AC(131)/6E1068(48)/6E12DC(48)로 정확히500 stable literal이다. 메일함77·메일헤더42·군임무153·파괴임무131·장비96·접속1이며 선택지4/그외496개다. 누적12,437개 초안·미작성15,015개. 기존 초안/원문/TPL/현재ROM선택은 불변이며 기존 임시·내부오류·자판/구조 미확인 항목을 분모에서 제외하지 않았다.

모든 원문 literal과 제어 skeleton을 읽고 ID별로 직접 작성했다. 큰 스크립트는 공백만 압축한 전체명령/인수 보기로 확인하고 출력이 잘린6DF988은 단독 전체 보기로 다시 읽었다. 장비2개와플러그인의 실제TPL도 읽었다. 메일함10..77의 명시초상화와9/101..120의checkNaviAll 미표시quick분기를 구별한다.6DF988의 샤로 군 작전 사령부는 원문 발신자이며SearchMan 임무활성화/positionMugshot은 발신자 초상화 identity를 증명하지 않는다.6E01AC도NapalmMan 활성화와 메일화자 identity를 분리했다. 이전 넘버맨 스크린샷은 이 화자의 근거가 아니다.

20군임무32..51의 인터넷1..12/언더인터넷1..3·9760..9779/활성화분기와 체포/변장간파/데이터탈환/감염내비 및 프로그램 보호/바이러스 삭제를 대조했다. 이미 파괴한 발생장치와 남아있는 바이러스,친선대사 공격위협,과학성의 도주바이러스 정보유출 위험을 구별했다.15파괴임무32..46의9792..9806/활성화·성공시보상·32..35실패위협을 유지했다. 보스 분노/개인의 마피아보스 대면꿈/10년후연구완성농담/양지와뒷세계마니아/운반물 비밀/바이러스모양 탐색프로그램/삭제대회/길드생계를 각각 번역했다. 샤로·겟단·닥터 디그·다크 길드와 과학성 표기는 승인 전 후보이다. sourceいしん/おかけ 등의 오기는 바꾸지 않고 문맥 해석 후보로만 작성했다. 보상 문장은 실제 지급/임무 실행의 검증이 아니다.

메일global29분기·6메일함 분류·특수메일90..93/닉네임3곳·waitHold/keyWait를 보존했다. 헤더20발신자/제목쌍·41/65제목 접두어를 번역하고40/64FROM:는 그대로다. 장비명은 기존equipment_weapons_ko.json의 의미가 일치하는 초안 후보를 참고했으며 승인으로 전환하지 않았다. C/WB/B/D 약어를 확장하지 않고R/L 접두어와이미선택60..62·buffer63은 그대로다.

장비70..75는6E1068명시MegaMan/6E12DC명시Roll이다. 동일칩3/동일메가1/동일기가1과메가전체5/기가전체1을 구별하고 필요한 전체 장수는buffer1로 출력한다(30을 임의 하드코딩하지 않음). 선택지width8/default0·예뒤2공백·헤더선행/후행공백·원래줄/페이지와제어를 보존했다. 플러그인은명시FireMan.EXE대상이며구호화자는미확정,TYPE3/3603/3651/wait30은그대로다.

신규6개 포함279개 회귀 검사 PASS(190.355초). 기존 generic trailing-space 검사2곳이 새2:0 칩폴더제목을 선택지로 오인하여 명시system-label 제목과player-choice를 구분하도록 보완했다. 원문·제어·BDF글리프/codec·py_compile 검사 통과,초안 재생성 동일. 이번52개(메일함18/군임무28/파괴임무6),전체1,613개는 보수적132px advance 재검토 표시이며 실제 consumer 용량·화면 넘침 판정이 아니다. 자동 축약·재배치하지 않았다. needs_review/NON-DISTRIBUTION이며 인간 승인·ROM삽입·실제화면/저장검증·전체완료·배포적격 판정이 아니다. 원본과기준ROM·에뮬레이터·저장·이미지 변경 없음.

검사 코드 보완 후 해당 tool SHA가 포함된 기준으로 파생물 재생성 전후 SHA256 동일: worklist `594dc3645485c88afd61c739fcc17b38e10df8aa31bcaad040fd9659f5cb0485`,coverage `db8a2a46743e060482ef32ef862144109cf20d968ccc7d56d5b9e17a55522f57`. 원본/기준ROM 및 catalog SHA256 불변.

## 500개 묶음017 — 서치 임무·저격 훈련·내비 이름 초안 (2026-10-11)

`tools/draft_batch500_017.py`의2개 자산은716DE4(479)/778A4C(21)로 정확히500 stable literal이다. 선택지14/그외486개를 구별하며 누적12,937개 초안·미작성14,515개다. 기존 초안/원문/TPL/현재ROM선택은 불변이고 이전 임시·내부오류·자판/구조 미확인 항목을 미작성 분모에 남겼다.

모든 원문 literal 및script0..140의전체제어 skeleton을 읽고ID별로 직접 작성했다. 최초 literal 보기에서 잘린87..91은 별도로 다시 읽었다. 큰 스크립트의 제어는0..78/79..106/107..140로 나눠 공백만 압축한 전체명령/인수 보기로 확인했다.778A4C실제TPL23슬롯도 읽었다. 14..73일반시민의오접촉항의/진범의변장발각/감염구조반응은 실제Heel/Normal/Official/Program/Girl초상화로 식별하며 외형으로 범죄자 여부를 확정하지 않는다. 통신속도200퍼센트상승농담은 실제측정이 아니다.

초상화는literal직전까지의show/hide상태를 기준으로 기록했다.7은지령문 전체가mugshotHide상태이며 마지막대사뒤의SearchMan표시는 앞문구화자증명이 아니다.76..78의사령부지령·보상도초상화숨김이고i>=4획득안내만system-reward다.8소개는SearchMan표시,8선택지는숨김이다.1/102/117/134메뉴도숨김이다. 이전넘버맨스크린샷이나인접메일순서는화자증명으로사용하지 않았다.

십자버튼록온/A저격또는접촉/B+십자고속이동/R서치모드·게이지가조금이라도있어야사용/사용중소모/0일때해제/시간회복을 보존했다.0의서치모드와140의서치스코프명칭을 임의로통일하지 않았다.20브리핑79..98의60초/표적4·10·4·13·6·5·15·8·5·10·15·15·15·15·15·15·15·18·18·18체(87은5인조),79/81/83/84/86/87/88오접촉5초감점을 대조했다. 검은몸/독특한움직임/가방·폭발전/과학성방어바이러스로생긴행동버그/투명바이러스 단서와체포·보호·저격목표를 구별했다.83은내비와프로그램보호,86은표적소개에프로그램포함/행동안내내비보호라는 원문구별을 유지한다. 모든 가상 임무의 실행/정상경로 검증은 미실시다.

100/101시험15체60초·모두저격하면합격,107..113/124..130훈련15체와114..116/131..133훈련18체·60초를 구별한다.5114/5115/5116·5258/5259·5260/5261/5263..5270·checkNavi4의비현재/현재내비말투와redirect를 보존했다.1/102/117/134메뉴5113·width11/default0/B금지,8선택width6,103wait120은그대로다. 훈련스카우트칭찬·시간초과·다음훈련격려는 실제입대/진행실행이 아니다.

76HP메모리33/수량1,77제니/78버그조각4294967295·buffer3/padLefttrue·출력순서는그대로다. 닉네임앞/뒤줄바꿈과페이지를 유지하고님의 또는원래줄경계로받침조사의존을피했다. source7의さくさんしれぶ는원문을수정하지않고작전사령부문맥후보로번역했다. 샤로/겟단/서치스코프/록온사이트/프로그램군인형·체단위·말투·이름은승인전후보다.778A4C이름21개는명시슬롯별라벨이며13/14XXXX는원문그대로다. 이 이름목록이 실제캐릭터선택화면에소비된다는주장은하지않는다.

신규6개 포함285개 회귀 검사 285개 통과. 원문·제어·BDF글리프/codec·py_compile 통과,초안재생성동일. 이번67개(서치임무·훈련),전체1,680개는보수적132px advance재검토표시이지실제consumer용량·화면넘침판정이아니다. 자동축약/재배치없음. needs_review/NON-DISTRIBUTION이며인간승인·ROM삽입·실제화면/저장검증·전체완료·배포적격판정이아니다. 원본과기준ROM·에뮬레이터·저장·이미지변경없음.

017 묶음 검증 기록: 이전 016 묶음의 마지막 위치 검사만 -2로 수정한 뒤 285개 전체 검사를 다시 통과했다. 같은 코드로 목록을 두 번 재생성해 SHA256 일치를 확인했다. coverage.json: `51cf99de80d0eaa7f1870e0a7063646211220a248628761e1f7f176de8777301`; worklist.json: `3883858d961c244f383d4f53abcfedc85c1974f05801f8455454736e6b983281`.

## 후속 500 묶음 018 — 윈드 의식·비행과 개인정보 후속

`tools/draft_batch500_018.py`의 3개 자산은 71551C(253)/662C5C(243)/65E384(4)로 정확히 500 stable literal이다. 누적 초안 13,437개, 미작성 일본어 14,015개. 모두 needs_review/NON-DISTRIBUTION이며 ROM에는 적용하지 않았다.

71551C 전체253문구와0..61 제어 skeleton을 읽었다. 몸이 초록빛일 때 B버튼으로 힘을 불어넣고 최대에서 A버튼으로 해방하는 조건을 유지했다. 11..29의19비행요청은 인터넷2..12/언더인터넷1..3과4000..100000전뇌미터를 원문대로 기록했다. 인터넷8의13000/16000,인터넷12의40000/44000은 서로 다른 요청이다. 4954/4955 분기에 따른 특제 인형47/52 및 측정48..58·감탄59·고장60/61은 일반 프로그램 비행과 별개다. 30/58 buffer1 비거리,59의60+60프레임 감탄 분할,숨긴7HP메모리33/수량1·8제니/9버그조각4294967295와buffer3/padLeft를 보존했다. literal별 명시초상화/숨김에 따라 윈드맨·프로그램·선택지8·시스템보상을 구별했다.

662C5C 전체원문과0..92 제어 skeleton을 읽고 큰출력에서 잘린33..52는 다시 읽었다. 학교·가족·친구·음식·취미·꿈·좋아하는사람·불편한사람·TV·동경대상·과목·희망물건과전적·칩·순위 변수를 원래순서/페이지로 유지했다. 한테/하고/말이야/같은 걸/의 표현으로 받침의존 조사를 피했다. 52꿈·74추측·82배틀흐름의견은 실제게임조건으로 단정하지 않았다. 88스탠더드후메가/89기가/92버퍼121순위도 구분했다. 초상화명령이 없는 quick-box 문구는 특정 내비 화자로 단정하지 않았다. 내부오류0은 원문/미작성분모에 그대로 두었으며7개의 비일본어조각도 원문유지했다. 65E384의4문구는 주말대회와키아이템안내이며 화자/실제레이아웃은 미확정이다.

신규6개 포함291개 회귀 검사 통과(223.812초). 초안재생성 동일,글리프/codec·숫자·줄바꿈·패딩·원문/제어 보존 검사 통과. 이번47개(윈드31/개인정보후속16),누적1,727개는 보수적132px advance 재검토표시이며 실제화면넘침 확정이 아니다. 자동축약 없음. 표현·용어·말투·의미/인간승인·실제소비자/레이아웃·ROM반영·화면/저장·한글자판·이미지·배포검증은 별도로 남는다.

018 검증 기록: 문맥 메모의 비행요청 수를19로 정정했다(번역문 변경없음). 최초검사의 오래된메모비교/줄바꿈된wait명령개수/보류오류범위 판정을 수정한 뒤 고정된코드·자산으로291개 전체검사 통과. 동일기준으로 목록을 두 번 재생성한 SHA256도 일치했다. coverage.json: `a51f6530719fb1e7aca441e619a2622cbee925b2bc28984dc1112776f9a8a56b`; worklist.json: `574de68623eb6f09ce8b1c9609f78885f13d7eb4845175f337cfd660129b7bf6`. 원본ROM·개발ROM·원문목록 SHA는 기존기준 그대로다.

## 후속 500 묶음 019 — 바이러스·내비 이름과 별 주제 개인정보

`tools/draft_batch500_019.py`의3개자산은767E0C(255)/6A6C64(244)/78B50C(1)로 정확히500 stable literal이다. 누적초안13,937개·미작성13,515개. needs_review/NON-DISTRIBUTION이며 이번에도ROM삽입없음. 기존초안과원문/현재ROM선택은그대로다.

767E0C의256슬롯과0..255 end-only제어를 전부읽었다. 0록맨·1..126바이러스·128..255내비/형태이름을 ID별로작성했으며127단일공백은other-review분모에그대로유지했다. EX/V2/V3/SP/XX·2..5표기와노멀내비/힐내비/포르테SP중복슬롯을합치지않았다. 록맨0과롤128,윈드박스/버큠팬121..126은구별했다. 메톨/볼켈기어/라라팟파등음역은새검토후보이며공식한국어표기승인이아니다. 기존내비이름후보는017이름라벨및secondary-chip/mail/credits문맥을참고했다. 이름라벨은대사화자가아니며실제표시화면/소비자규격을확정했다는주장을하지않는다.

6A6C64 전체244원문과1..92 skeleton을1..36/37..64/65..92로읽었다. 학교·가족·친구·음식·취미·꿈·좋아하는사람·불편한사람·TV·동경대상·과목·희망물건·대전상대·칩변수의순서/페이지를유지했다. 한테/하고/말이야/같은 걸/쪽/의로받침의존을피했다. 21:2앞공백,26/27/43/59앞줄바꿈과변수출력경계를보존했다. 최초작성중31:2/50:3의부족한줄경계는원문대로3줄로정정한후자산생성했다. 이archive에는초상화가없어별모티프만으로스타맨화자로단정하지않았다.

9친구자리·31메일·87칩소멸농담과11승리예언·35운세방송의견·49반복소원의효험·91별부담의추측을게임기능/사실로단정하지않았다. 21은희망사항을묻는대사로option명령이없다. 61최다패배상대칩/69최다승리상대칩,57장비/59상대무기,학교과목실력41..43/전투효과를구별했다. 78B50C는MegaMan명시초상화로어둠의힘·주의전진을말하며인접저장위치나이전넘버맨스크린샷으로특정보스장면을단정하지않았다.

신규6개 포함297개 회귀 검사 통과(206.172초). 숫자·줄바꿈·패딩·원문·제어·BDF글리프/codec검사통과. 이번14개(별개인정보13/주의안내1),전체1,741개는보수적132px advance재검토표시이며실제화면넘침확정이아니다. 이름폭0건표시도실제라벨소비자용량확인이아니다. 자동축약없음. 원본ROM/개발ROM/원문목록 SHA불변이며에뮬레이터·저장·이미지변경없음. 의미/말투/용어인간승인·레이아웃·실제소비자·ROM/화면/저장·한글자판·배포완료는아직아니다.

019 검증기록: 전체297개 검사가206.172초에통과했다. 이후문맥메모의범위를0록맨/1..126바이러스로명확히정정했으며번역문·제어·선택은변경없다. 정정된최종자산으로전체권위자산재현성검사1개를다시실행해76.512초에통과했다. 최종기준으로목록을두번재생성한SHA256도일치했다. coverage.json: `b7cb6cd889add1b147ddcdfcb58704f36d8a92f7afcfece5a76aa0db80b79fe9`; worklist.json: `c924d9549e1751fdbe47340b7d8778436ab0ff7285f6db6fb0f15f3cfd7863f9`. 초안재생성/py_compile통과,원본ROM·개발ROM·원문목록해시는기존그대로다.

## 후속 500 묶음 020 — 거츠·넘버 개인정보 후속과 썬더 주의

`tools/draft_batch500_020.py`는 6684B0(258)/689DF8(240)/78B804(2)로 정확히500 stable Japanese literal을 개별 작성했다. 누적초안14,437개·미작성13,015개. 모든 자산은 needs_review/NON-DISTRIBUTION·release_eligible=false이며 ROM빌드/선택변경없음.

두 개인정보 archive의 전체원문과0..92 제어 skeleton을 읽었으며, 잘린689DF8의57..68제어는별도로다시읽었다. 거츠맨/넘버맨 자기언급은 원문에 있지만 quick-box에초상화명령이 없어 실제화자·런타임소비자를 임의확정하지 않았다. ガス→거스 말끝과 ガッツ→거츠 구호의 기존검토후보를따랐다. 썬더주의0만 ThunderMan 명시초상화로식별했으며 불길한기운·방심금지를번역했다.

학교·가족·친구·음식·취미·꿈·좋아하는사람·불편한사람·TV·동경대상·과목·희망물건·전적상대·스탠더드1..3/메가/기가 변수와 줄/페이지를 보존했다. 66830의printCrush를친구로오인하지않았고,66866닉네임의전법/이긴상대비교,66880스탠더드2/1사용감비교,66892기가를구별했다. 68913음식다음변수는printBestSubject로원문의이상한단정을그대로유지했고,15두변수는음식이며닉네임이아니다. 68961임의MP칩분기·최다패배상대칩,63최다패배상대,69최다승리상대칩을구별했다.

넘버27의0퍼센트즉시부정·29장난메일거짓말·46문제집/47억지공부/75칩폐기농담과86의승률10퍼센트「아마」를 유지했다. 원주율3.1415926535/897932384626/433832는원문숫자열그대로이며수학적으로수정하지않았다. 90넘버맨→넘버원말장난을살렸다. DHA의66814주장/즉시반문,날달걀66815소문은게임캐릭터의발언이며건강조언이아니다. 66865いつもで의문맥은언제든으로번역한검토후보다.

내부오류6684B0:0:0/689DF8:0:0은원문/미작성분모에남기고9비일본어구두점조각도원문유지했다. 원문ID/TPL/payload/숫자/줄바꿈/패딩/제어/BDF/codec 정적검사통과. 303개 회귀 검사 통과. 이번35개(거츠18/넘버16/주의1),누적1,776개는보수적132px advance재검토표시이며실제화면넘침판정이아니다. 자동축약없음. 원본ROM·개발ROM·원문목록은불변이며에뮬레이터/저장/이미지는변경하지않았다. 인간승인·실제소비자/레이아웃·ROM반영/화면·저장·한글자판·배포검증은미완료다.

020 검증기록: 최초303개검사에서새원주율검사의re import누락1건을발견해검사코드만수정했다. 번역문변경없이최종303개전체검사가228.714초에통과했다. 최종고정기준으로목록을반복생성해SHA256일치를확인했다. coverage.json: `c33c081731fe6c3bb7aa38581a59ca9690f4580471e3fd9d2e762aed1e8997bd`; worklist.json: `f79fdf40cf4605deae1ea384db8d99115b8f029deafb94a4f2d5557fbcfbfa0e`. 초안재생성/py_compile통과,이전권위자산등록내용보존,원본ROM·기준개발ROM·원문목록해시기존값일치. 화면검증/ROM반영을했다는의미가아니다.

## 후속 500 묶음 021 — 주먹·거친 말투 개인정보와 통행 안내

`tools/draft_batch500_021.py`의3개자산은68FB1C(238)/6BE52C(241)/799A3C(21)로 정확히500 stable Japanese literal이다. 누적초안14,937개·미작성12,515개. needs_review/NON-DISTRIBUTION·release_eligible=false이며ROM삽입/빌드없음.

두개인정보의전체원문과0..92 skeleton을0..48/49..92로모두읽었다. 주먹·철·훈련·온천비유와거친배틀애호말투는원문에맞춘후보이며초상화/자기이름근거가없어메탈맨·네이팜맨·포르테등화자로단정하지않았다. 학교/가족/친구/음식/취미/꿈/사랑/불편한사람/TV/동경대상/과목/희망물건과전적·칩변수의순서·인수·페이지를유지했다.

68FB1C의100/1000인력·100패널·메가추가1장을보존하고23실제꿈대상목격은printDream이며printIdol로바꾸지않았다. 61/62임의MP칩미정시63분기와최다패배상대/칩,69..71최다승리상대/칩을구별했다. 13음식강철성분주장·82어깨결림추측은게임캐릭터발언이며건강/실제칩효과로단정하지않았다. 70톱니바퀴선물농담의자기반문과89기가위험을유지했다.

6BE52C의13하루3끼보다음식좋다모순/자기반문,15음식vs배틀의가상선택,18취미배틀용도단정,31메일첨부가정은기능확인으로해석하지않았다. 27좋아하는사람/29불편한사람은동일원문이어도변수를합치지않았다. 49희망물건을무기로표현/50개조가정/51UP후의문을유지했다. 69최다승리상대·칩과65..67최근이긴상대,87닉네임및두번의메가삽입을구별했다. 91기가위험을다크칩조건으로임의변경하지않았다.

799A3C 전체0..14실제TPL을읽었다. 0오피셜참가자격1345확인/1437설정,2아이템2보유/1460설정,7아이템19예외확인,13표지판설명,14아이템19한개소모/1460설정은서로다르다. 아이템2/7/19이름을추측으로대체하지않았다. 1내비3/22분기에따라8WindMan진정·9Bass제거,10/11숨긴초상화서술·12공통862설정을보존했다. 통행안내/나무/손모음은명시초상화없는문구이며장면상호작용이나실제통행완료를검증했다는의미가아니다.

내부오류68FB1C:0:0/6BE52C:0:0은원문/일본어미작성분모에유지했다. 6BE52C구두점2개와799A3C여는인용3개도other-review분모/원문그대로다. 원문·제어·숫자·줄바꿈/패딩·BDF/codec 정적검사통과. 309개 회귀 검사 통과. 이번42개(주먹24/거친12/통행6),누적1,818개는보수적132px advance배치재검토표시이며실제consumer용량/화면넘침확정이아니다. 자동축약없음. 원본ROM·기준개발ROM·원문목록해시는불변,에뮬레이터/저장/이미지변경없음. 인간승인·실제소비자/레이아웃·ROM/화면/저장·한글자판·배포완료는아니다.

021 검증기록: 신규6개포함309개전체회귀검사가133.115초에통과했다. 초안재생성/py_compile통과,이전권위자산등록내용보존,동일고정기준의목록반복생성SHA256일치를확인했다. coverage.json: `bc9f29a517032fe29a786715d48e8452efb83f5a43bf79d94584fce50fa64cdc`; worklist.json: `a19fa6bad18fcfd8c57a105a97b3c9583e1ed510fa472157cce4851f81804943`. 원본ROM·기준개발ROM·원문목록은기존해시그대로다. 정적검사결과는인간승인이나ROM/실제화면/저장검증이아니다.

## 후속 500 묶음 022 — 기사도·불꽃 개인정보와 버그조각 급식

`tools/draft_batch500_022.py`의3개자산은6B8478(264)/679424(225)/69360C(11)로 정확히500 stable Japanese literal이다. 누적초안15,437개·미작성12,015개. needs_review/NON-DISTRIBUTION·release_eligible=false이며ROM빌드/선택변경없음.

두개인정보의전체원문과0..92 제어 skeleton을 읽고, 잘린6B8478의39..52및679424의71..91원문은별도로다시읽었다. 기사도/갑옷의하오체와불꽃/뜨거운배틀의거친말투는원문에맞춘검토후보이며초상화명령이없으므로나이트맨/파이어맨화자로단정하지않았다. 학교·가족·친구·음식·취미·꿈·좋아하는사람·불편한사람·TV·동경대상·과목·희망물건과전적·칩변수의순서/인수/페이지를보존했다. 나이트의23まんしん은꿈을향한매진,63釈迦に説法은불필요한훈수에대한사과로옮겼다.

679424의26메일소각/45단독인터넷발언은뒤의농담취소까지유지했다. 42우드강점/47아쿠아약점은잘하는/못하는과목비유이며43학교공부무용론의과목예외·50마사지효험불확실성·77근접전기억불확실성을보존했다. 61..63최다패배상대/칩과65..67최근이긴상대,69..71최다승리상대/칩을합치지않았다. 음식/건강표현은캐릭터발언이며실제건강조언/게임효과확정이아니다.

69360C는전체실제TPL1..3을읽었다. flag3585·닉네임·buffer3의버그조각수량을보존하고줄게/싫어2선택지,default0·targets2/continue/continue,수락후checkTakeBugFrags4294967295의All3/None·Somecontinue를구별했다. 부족한수량의허기와섭취/트림/힘이솟는반응을번역하고item33amount1/callJunkManDailyBugFragIncrement는변경하지않았다. 수량상수의실제엔진해석·부분소모/환불·보상소비자는미확정이며호출명이초상화증거는아니다. 버그조각뒤공백1개·줄게뒤공백2개·선택지앞마지막줄바꿈을유지했다.

두내부오류0은원문/일본어미작성분모에남기고12개비일본어구두점/줄바꿈도other-review분모/원문그대로다. 최초315개검사에서선택지화자메타데이터2개누락과검사중정정된비일본어개수메모의구기준비교를발견했다. 번역문·제어변경없이player-choice분류와4→6/10→12문맥메모만정정한최종고정기준으로315개전체검사가138.615초에통과했다. 이번22개(기사11/불꽃11/급식0),누적1,840개는보수적132px advance배치재검토표시이며실제소비자규격/화면넘침확정이아니다. 자동축약없음. ROM/화면/저장/에뮬레이터/이미지변경없음. 인간승인·레이아웃·한글자판·배포완료는아니다.


022 검증기록: 수정된최종고정기준으로신규6개포함315개전체회귀검사가138.615초에통과했다. 초안재생성/py_compile통과,이전권위자산등록내용보존,목록반복생성SHA256일치를확인했다. coverage.json: `fcd665de24e388639255315e2aa746af01d221cbb3a1ec7f564ce62adf3e7282`; worklist.json: `224b5a43a555945129d0936e88bf4cc9c73c86228e5913af9dcd0b2c49d75f05`. 원본ROM·기준개발ROM·원문목록은기존해시그대로다. 정적검사는인간승인이나ROM/실제화면/저장검증이아니다. 다음은미작성12,015개에서다음500개원문범위를고르는단계다.


## 후속 500 묶음 023 — 닌자·저격 개인정보와 금요일 NPC

`tools/draft_batch500_023.py`의3개자산은673770(222)/6ACCA8(225)/79E890(53)로 정확히500 stable Japanese literal이다. 누적초안15,937개·미작성11,515개. needs_review/NON-DISTRIBUTION·release_eligible=false이며ROM빌드/선택변경없음.

두개인정보의전체원문과0..92 제어를읽었다. 반복quick-box헤더를읽기전용논리뷰에서같은템플릿으로묶고모든남은제어/인수와literal ID를읽었으며잘린6ACCA8의73..92및673770의0..16을별도로다시읽었다. 원문TPL은변경하지않았다. 닌자/잠입의고풍어조와저격/탐색/임무보고의정중한어조는원문조건에맞춘검토후보이며초상화가없으므로섀도맨/서치맨화자로임의확정하지않았다.

6ACCA8은학교칩탈취1..3·전량칩내기제안과실제기능을구별했다. 병량환은005음식알림의기존검토후보와일치하며공식용어승인이아니다. 10년숙성음식은캐릭터의허풍/건강주장,39동경대상격언은원문printIdol에연결한대사이며외부공식인용확정이아니다. 25손편지연서/26좋아하는사람위조메일/27자객함정/29불편한사람함정을구별했다. 42과목도움의즉시불확실성·49희망물건안고자기·50우승해도물건미지급·51내비라상가져오기불가·54메일속하급닌자가정·74일격필살희망을보존했다. 61R버튼조합/63L방어R견제후칩·상대전적/칩변수를유지했다.

673770은4학교내칩3위·5..8가족·9통신과친구중요성·10예절/11친분질문을구별했다. 17취미감상/닉네임눈빛,18취미와임무목표비유,21..23꿈/49..51희망물건을실제저격대상으로바꾸지않았다. 26좋아하는사람이닉네임에관심있을가능성/27긴급보고후정보오인정정을유지했다. 61..63최다패배상대/칩,65..67최근이긴상대,69..71최다승리상대/칩과스탠더드1..3/메가/기가를구별했다. 74적정지후록온은캐릭터추천이며모든칩효과를검증한것이아니다. 85메가추천1수치·89기가조준흔들림/90부담추측은다크칩조건으로임의변경하지않았다.

79E890 전체실제TPL의존재하는0..90 scripts를읽었다. 명시MrProgGreen0..3실직/낙관반전,NormalNaviYellow10..13금요일배틀, PurpleNavi20..24경비,NormalNaviPink30..32오퍼레이터/가정,NaviGirlOrange80주말,HeelNaviPurple90피로를구별했다. 시간9분기0(9..11/12..13/16..16:59),20(9:15..10:30/12..13/17:20..17:59/18..19:30),30(8..8:50/14:40..15:59)를보존했으며범위포함성/실제소비를확정하지않았다. 10네/아니요는숨긴초상화의player-choice/default0/11·continue·continue,11globals24..28및1806/7701배틀설정,12상대내비패배/13상대내비승리를구별했다. 30의darling오퍼레이터/부부표현은유지하되부부개별정체를창작하지않았다. 32아이픽업망각/아이가더야무짐을보존했다.

두내부오류0은일본어미작성분모,7비일본어구두점/줄바꿈은other-review분모/원문그대로다. 최초작성중줄경계3개를원문과같이수정한후자산생성했다. 원문·제어·숫자·줄바꿈/패딩·BDF/codec검사통과,321개전체회귀검사가136.597초에통과했다. 이번36개(닌자19/저격6/금요일11),누적1,876개는보수적132px advance재검토표시이며실제consumer용량/화면넘침확정이아니다. 자동축약없음. ROM/화면/저장/에뮬레이터/이미지변경없음. 인간승인·레이아웃·실제소비자·한글자판·배포완료는아니다.


023 검증기록: 신규6개포함321개전체회귀검사가136.597초에통과했다. 초안재생성/py_compile통과,이전권위자산등록내용보존,고정된최종기준의목록반복생성SHA256일치를확인했다. coverage.json: `b107a9237e0a84bd24dbd1ca4a7a931361a0e56c1d14888a42162c393f26049a`; worklist.json: `48d770e19b439c0a5f0a6f2ac9d319b29e6b89fa6f907c6c62ec3b4829553e60`. 원본ROM·기준개발ROM·원문목록은기존해시그대로다. 정적검사는인간승인이나ROM/실제화면/저장검증이아니다. 다음은미작성11,515개에서다음500개원문범위를고르는단계다.



## 후속 500 묶음 024 — 나무·얼음 개인정보와 트레이더·우승 보상

`tools/draft_batch500_024.py`의3개자산은6A0640(219)/6C40AC(215)/6FE8D4(66)로 정확히500 stable Japanese literal이다. 누적초안16,437개·미작성11,015개. needs_review/NON-DISTRIBUTION·release_eligible=false이며 ROM빌드/선택변경없음. 원문전체literal과제어를읽고,두quick-box개인정보는반복헤더를읽기전용논리뷰에서만요약했다. 원본TPL은변경하지않았다.

6A0640의나무/열매/다람쥐/뿌리/줄기비유,13입술과14배,18취미2시간의가정,23열정/소진,25데이트제안과27화자에게메일요청,29적의메일수용과30넷배틀명시를유지했다. 35방송안함/37아이돌얼굴철회/38선물받은칩존재불확실/39메가칩취향추측/42과목도움예외/43정의불확실을실제확정정보로바꾸지않았다. 꿈과희망물건,최다패배상대·칩과최근이긴상대·최다승리상대칩을구별했다. 이archive에화자이름/초상화증거는없으므로우드맨초상화로확정하지않는다.

6C40AC은9의자기소개에아이스맨이있지만literal초상화는없다. 이전넘버맨스크린샷과섞지않았다. 원문의어린존댓말을후보로작성하고8여동생플러그아웃문구를임의교정하지않았다. 19는취미를좋아하는사람모집이며연애상대가아니다. 25뜨거운짝사랑/27원래빨간볼농담/29앙금녹기/39노력의아이돌발언/49건강당부를게임내대사로유지했다. 59얼음에리어·프리즈봄,61상대폴더통째얼리기,62상대칩과의비교는캐릭터추천/주장이며신규전투기능을구현한것이아니다.

6FE8D4는칩3장/스페셜10장/버그조각10개·선택지20개·우승보상제니/칩/버그조각과29소지한도분기를구별했다. 칩보상buffer1과27buffer3,26/28수량buffer3,4294967295엔진인수·선택분기·flags1759/1760·애니메이션/효과음은보존했다. 16의원문은버그조각접두사만있으므로부족하다는말을창작하지않았다. 28마지막ASCIIspace와선택지네뒤2space를유지했다. 현재내비뒤의말이야는조사의받침의존을피한임시서술후보이며시스템서술의말투검토가필요하다. 버그피스트레이더는새용어후보,제니/버그조각/프리즈봄은기존후보를참고했으나인간승인은아니다.

두내부오류0은원문/일본어미작성분모에유지했다. 숫자·줄경계·패딩검사를통과해자산을생성했고초안재생성/py_compile도통과했다. 신규6개포함327개전체회귀검사가136.666초에통과했다. 최초실행에서검사등록인덱스/배치ID문자열변환8건과제어명오기로총9건실패해검사코드만수정했다. 원문/번역자산은변경하지않고전체재실행했다. 이번47개(나무19/얼음12/트레이더16),누적1,923개는보수적132px advance재검토표시이며실제consumer용량/화면넘침확정이아니다. 자동축약없음. ROM/화면/저장/에뮬레이터/이미지변경없음. 전체초안후ROM통합과실제화면/저장검증순서를유지한다.

024 목록반복생성SHA256일치: coverage.json `e82a2abf3f35644e0a9880e96d593a58c8adc73175f90154601ea2a77f46220a`; worklist.json `7d523216815eeeaad105857d1f3af437ab68b2cee5ceb870dae45ad999eb26bb`. 원본ROM·기준개발ROM·원문목록은기존해시그대로다. 정적검사는인간승인이나실제화면/저장검증이아니다.


## 후속 500 묶음 025 — 정크 말투·전기 개인정보와 일상 NPC

`tools/draft_batch500_025.py`의4개자산은69561C(213)/67EA58(211)/79D108(49)/7A1170(27)로 정확히500 stable Japanese literal이다. 누적초안16,937개·미작성10,515개. needs_review/NON-DISTRIBUTION·release_eligible=false이며 ROM빌드/선택변경없음. 네archive의원문literal/제어를모두읽었고두개인정보quick-box는반복헤더를읽기전용논리뷰에서만요약했다. 둘모두초상화/자기이름증거가없어정크맨/썬더맨초상화로확정하지않았다. 정크맨형더듬음과전기/엄격한조언은원문말투후보이다.

69561C의학교친구/형과놀기/친구와친해지는배틀,취미궁금증과화자에게관심요청,화자토너먼트꿈과플레이어꿈을구분했다. 14음식맵다는주장과15피곤한눈에음식문지르기/아마는부정확할수있는게임내캐릭터발언그대로이며건강안내가아니다. 25플레이어의짝사랑메일과27내비자신의메일요청,29적꺼림/35방송내용착각가능성,42과목응용기술추측/45재미없음/46배틀쓸모없음주장/47그래도공부를유지했다. 49희망물건이우승보상인지질문은지급확정이아니고50맛있어보이는이름은희망물건변수이다. 54다른오퍼레이터에게의뢰후농담,62L버튼장비/칩궁합,69빈틈/70효과가능성/71느낌,89기가두려움/90허리통증을구현된피해효과로바꾸지않았다.

67EA58의형제유대,13음식충전제안후불가능정정/15입부터필요/19취미에도움없음추측철회,26사랑의짜릿함을유지했다. 29적메일전기알림과54도전메일OK자동답장은캐릭터발언이며새로운메일기능구현이아니다. 31메일온것같은느낌/39아이돌말했는지반문/45공부추측정정/49희망물건이전력을두배로늘릴것같다는추측을유지했다. 61최다패배상대칩추정/62대응폴더,65최근이긴상대와실력비교,67진심배틀/69슬롯인타이밍과74사용률1위,82산초속담/폴더에묵혀두지말기,83필수칩반문/89정신피로를구분했다. 산초속담은원뜻보존후보이며한국속담으로자동치환하지않았다.

79D108 전체실제TPL의0..90존재scripts를읽었다. 명시MrProgGreen0..3실직프로그램, PurpleNavi20..24경비, NormalNaviPink30..32젊은엄마오퍼레이터/남편/아이, HeelNaviPurple40..41야간순찰과90목수오퍼레이터, NormalNaviBrown50버스팅, NaviGirlOrange80점심을구별했다. 같은HeelNaviPurple초상화라도야간순찰군대말투와목수오퍼레이터의편한말투를분리했다. 31할아버지를오퍼레이터로추정하지않았고32아이유치원픽업과40갤럭티카펀치후보를유지했다. 0의점literal2개/각wait10은연출단위이고유일문장으로세지않았다. 시간10분기에는24..29:59범위가있으며0..5로정규화하거나범위포함성을추정하지않았다.

7A1170의명시NaviGirlOrange0..2수줍은초보, OfficialNavi30..32개그맨, NormalNaviBrown50검은내비언급, PurpleNavi60..61주말야간생활을구분했다. 30만담의보케/츠코미는엉뚱한말/딴지후보이며오퍼레이터가PET에딴지거는역할을유지했다. 간사이말투는경상도풍후보로작성했으나인간승인은아니다. 31프로그램/32고향/50검은내비의이름이나오사카를창작하지않았다. 61토요일이라고말한후12시가넘어일요일로정정하는순서를유지했다. 시간5분기/24..28:15범위를원문그대로보존했다. 두NPCarchive에플레이어선택지나배틀시작명령은없다.

두내부오류0은원문/일본어미작성분모,10비일본어구두점·줄바꿈은other-review분모에남겼다. 최초자산생성후69561Ccontext의전체슬롯수오기만222(일본어214/비일본어8)로정정했고번역/source는변경하지않았다. 숫자·줄경계·패딩과초안재생성/py_compile검사통과,신규6개포함333개전체회귀검사가141.499초에통과했다. 이번59개(정크12/전기24/일상10/토요일13),누적1,982개는보수적132px advance재검토표시이며실제consumer용량/화면넘침확정이아니다. 자동축약없음. ROM/화면/저장/에뮬레이터/이미지변경없음. 전체초안후ROM통합과실제화면/저장검증순서를유지한다.

025 검증목록 반복생성SHA256일치: coverage.json `09ee3942894d78443811137f9fc6c8ec2257343f15375fa08e4c333999afbf75`; worklist.json `5c185bf53e826a8df7785144155155687a368e3a132c18b4f988b2c89c5fb278`. 기존번역권위자산/이전완료묶음기록을보존했고원본ROM·기준개발ROM·원문목록은기존해시그대로다. 정적검사는인간승인이나실제화면/저장검증이아니다.

## 500개 묶음026: 존대·물 주제 개인정보와 인터넷 NPC

이전 묶음025 이후 미작성 일본어 중 정확히 **500개 stable catalog literal**을 수동 번역했다. 6842F8 존대 개인정보 후속211개,69B134 물 주제 개인정보 후속194개,79F30C 인터넷1 NPC67개,7A47A0 평일 NPC28개이며4개 자산/4개 선택지를 등록했다. 누적 신규 초안은 **17,437개**, 초안 미작성 일본어는 **10,015개**다. 유일 문장 수가 아닌 catalog ID 기준이다. 이전 자산/등록/묶음 정보와 원본 ROM/TPL/catalog·기준 ROM은 보존했다.

전체 원문 literal와 제어를 읽고 개인정보는 이름/학교/가족/친구/취미/꿈/좋아하는 사람/싫어하는 사람/방송/존경하는 사람/과목/원하는 물건/상대전적/칩 삽입의 문맥으로 번역했다. 초상화 없는 두 quick-box의 화자 identity는 미확정이다. 원문 존대와 ぴゅ를 퓨로 옮긴 말투는 검토 전 후보이며 다른 화면의 넘버맨을 근거로 이 대사의 화자를 확정하지 않았다. 반대로79F30C30..34는 실제 NumberMan 초상화와33의 자기이름 근거로 넘버맨 대사로 연결했다. 선택지는 초상화 hidden/player-choice로 구별했다.

6842F8의 형제 강의·자매 인터넷 초대/기분 걱정,취미와 식물 성장/라이브러리 비유,꿈을 향한 기세,사랑의 카운터/원수 메일 베기 농담,국가대표 TV 출연,희망물건으로 스피드/파워/기술 강화 추측을 보존했다. 57의 L/R버튼,61/62의 미정의 칩->63 조건,83의3번째/87의1가지 및 기가 칩 반동을 유지했다. 캐릭터의 주장을 실제 이메일 기능/아이템 효과로 확정하지 않았다.

69B134의 물 수조 때문에 메일 읽기 어려움,친구 배틀/우정,날것·뜨거운 음식과 눈꺼풀에 음식 얹기 소문,소원/우승 비교,메일 수신 거부,방송 보조 진행자에게 반함,상대 내비와 라이벌 관계,몸으로 공부하라는 인터넷 발언의 인용,칩으로 갈증 해소하는 엉뚱한 주장,물 냄새/물세척/주스 쏟기/수조 파손/물 탁해짐을 보존했다. 음식·눈 관련 문구는 게임 캐릭터의 불확실한 주장이지 건강 안내가 아니다. 82의 물 관련 관용구 및85 메가/눈 말장난은 의미 중심의 검토 전 후보이며 원문과 같은 음성 말장난 재현으로 주장하지 않는다. 18의 랜덤 친구 미정의->19와 원문 R버튼 다음 L버튼의 장비 순서를 유지했다.

79F30C의 인터넷1 시간대 안내·밤 아르바이트 졸음,어린 말투 프로그램의 견습 시험장/계단 안내·슬립 모드,요일별 노인 걷기/토요일 애니 예약 녹화,넘버맨의 사고 능력 승부/자기 닮은 내비 분기를 보존했다. 8시간대 조건의24..29:59 및5요일 조건을 정규화하지 않았다. checkNavi8->34,두 예->33와 아니요/취소->continue,예 뒤 ASCII공백2개,배틀 설정 global24..28/값136·31·32·1793·0/flag1806·7701은 그대로다. 사고 능력/계산의 승패 대사와 입력 선택지를 구별했다.

7A47A0의 첫 경기 탈락과 매주 우승 호언,휴식/특훈·120퍼센트,광장/상점·주말 북적임,토요일과 일요일 밤 프로그램 커플,인기 좋던 시절의 회상과 시,조용한 점심을 원하는 내비의 초록 내비 불평을 유지했다. 여섯 개 연출점 literal을 각각 ·로 옮기고20프레임 wait6개/3시간대 조건을 보존했다. 두 시의3행과 내부 행 앞 공백은 그대로지만 한국어5-7-5 음수율을 구현한 것으로 주장하지 않는다. 초록 내비의 고유 identity를 임의 확정하지 않았다.

6842F8:0:0/69B134:0:0 내부 오류와16개 비일본어 프로필 슬롯은 원문/원래 분모에 남긴다. 이번500개는 needs_review/NON-DISTRIBUTION/release_eligible=false이며 ROM 반영/화면·저장 검증을 수행하지 않았다. 스킬에 따라 의미/말투/적응의 인간 검토와 정적 검사 결과를 분리했다. 기존 graphics/한글 자판/저장/릴리스 과제도 미완료 그대로다.

검증: 누적339개 회귀 검사 통과(133.357초). 원본/기준 ROM/catalog SHA 불변,prepare 집계 통과 및 serializer 재생성 일치를 확인했다. 보수적132px 경고가62개(존대19/물19/인터넷1NPC18/평일NPC6) 추가되어 총2044개다. 실제 consumer별 한도/삽입변수 길이/화면 확인이 아니므로 자동 축약하지 않았다. 파생 coverage SHA `96b8008d630d69d67307d0b35c39243fa0e7c5fd4d08659524e8fd448b53352f`,worklist SHA `6db338ca0ac909215a7ddb81055e94aff40a5024953967505826de30535e7fcc`.

## 500개 묶음027: 전기·존대·물 주제 등록 질문과 언더인터넷 게시판

이전 묶음026 이후 미작성 일본어 중 정확히 **500개 stable catalog literal**을 수동 번역했다. 67D708 전기 주제 등록 질문135개,683054 존대 등록 질문132개,6999F4 물 주제 등록 질문174개,7028FC 언더인터넷 게시판59개이며4개 자산/72개 선택지를 등록했다. 누적 신규 초안은 **17,937개**, 초안 미작성 일본어는 **9,515개**다. 유일 문장 수가 아닌 catalog ID 기준이다. 기존 자산/등록/묶음 정보·원본 ROM/TPL/catalog·기준 ROM은 보존했다.

원문 TPL의 모든 literal/제어와 질문·확인·감상을 읽었다. 세 질문 묶음은 가족 유무/이름·친구·음식·취미·꿈·좋아하는 사람·존경하는 사람·꺼리는 사람·TV·잘하는/어려운 과목·원하는 물건·유치원/학교/회사 등록과40..63 버퍼 확인/추가 등록,80..95 감상으로 구별했다. 초상화/자기이름이 없어 캐릭터 identity를 임의 확정하지 않고 원문에 조건화한 엄숙한 전기 말투·존대·퓨 말투를 검토 전 후보로 남겼다. 72개 선택지는 플레이어 응답이다.

세 묶음 각각12개2방향 선택지의 존재 여부/추가 입력을 구별했다. 긍정의 ASCII뒤공백2개,spacePx16/24,printPlayerNickname/printStringBuffer1..3,flag3585/3605/3606 및3735..3749의 원문 개별 사용을 보존했다. 성별 변수22값1의17->19에서 좋아하는 여자/남자 질문을 구별하고,교육단계 변수23값1..5->33 학교/6..9->34 회사/기본32 유치원 분기를 변경하지 않았다. 41/44/47/50/53/56/59/62의2줄바꿈과 끝줄바꿈 및68305431:2의 시작줄바꿈을 유지했다. 형·누나/형님·누님 호칭은 이전 초안의 후보 관례이며 플레이어 성별에 따른 자동 호칭 전환을 구현한 것으로 주장하지 않는다.

67D708은 인터넷 전기의 감각/배고픔 잊기·라이브러리 취미·승리와 미래 쟁취,TV가 보고 싶어서 묻는 게 아니라고 부인한 뒤91에서 TV 시청 의향,31우승 보상 가정,83자기 여동생 언급 후 농담임을 밝힘,음식이 맵겠다는 추측·약점과 개성·원하는 물건 이름을 집에서 외치라는 과장된 조언을 유지했다. 실제 보상 지급이나 물건 획득 기능으로 확정하지 않았다.

683054은 수줍은 좋아하는 사람 질문,라이브러리 자력 완성 시 존경받음과 플레이어가 존경하는 사람 질문의 주체를 구별했다. 31개인이 갖고 싶은 것,80형을 부러워함/81남동생을 바란 뒤 부인/83가족의 좋음/85과식 주의/86취미 도전/91방송으로 배움도 유지했다. 플레이어 선택지는 내비의 존대 대사와 분리했다.

6999F4은 물양갱·수영 취미/눈 피로·태평양만큼 큰 꿈,메일과 좋아하는 사람·거리 두는 水くさい 관용구,「일본, 샘물 여행」 방송명 후보와 샘물 정보 질문,사회/국어 과목 주장 다음의「그런 말을 해 보고 싶다」는 한정,샤워 세트가 토너먼트 상품이 되길 바람,자기 누나를 좋아한다는 표현·존경하는 사람을 모름/과목을 알아 기뻐함을 보존했다. 원문의 물 관련 음성 말장난을 그대로 재현한 것으로 주장하지 않으며 새 음식/프로그램명/말투는 인간 검토 전 후보이다.

7028FC는 palette9·텍스트32,68·화살표202,108을 쓰는 익명 게시판이다. 0환영/희귀 정보,1..4오피셜 조사 목적이 다크로이드 토벌이라는 소문과 관 암시,5바깥과 닮았지만 높은 랭크인 바이러스,6..8미스터리 데이터에서 건 델 솔 획득/태양소년 무기 연관/팬의 언더 규칙 거래 제안,9..11셰이드맨이 이미 쓰러짐/새 오피셜 경계/다른 다크로이드,12언더인터넷 에리어4 너머의 어둠과 미지 공간을 구별했다. 글 작성자를 다른 글/내비와 합치거나 신참이 반드시 플레이어라고 단정하지 않았다. 거래 제안은 게시글이지 새 상점/배틀 이벤트가 아니다. 헛수고/헛고생으로 옮긴 뼈 관용구는 검토 전 의미 중심 적응이다. 1체/에리어4 숫자,3:3의 첫 줄 끝 ASCII공백과 원문 페이지/대기/색/좌표를 보존했다.

비일본어 프로필 구두점3개와13..47의35개 BBS00/BBS03 ID 임시표시는 원문/원래 검토 분모에 남긴다. 일본어 항목을 이번 범위에서 새로 제외하지 않았다. 모든 신규 항목은 needs_review/NON-DISTRIBUTION/release_eligible=false이며 ROM 반영/화면·저장 검증을 수행하지 않았다. 스킬에 따라 정적 검사 통과와 표현/말투/의미의 인간 검토를 분리했다. 한글 자판/저장/graphics/전체 릴리스 과제는 그대로 미완료다.

검증: 누적345개 회귀 검사 통과(134.843초). prepare 집계·500개 serializer 재생성 및 원문 보호 검사를 통과했다. 보수적132px 경고55개(전기질문11/존대질문7/물질문12/언더게시판25)가 추가되어 총2099개다. 실제 BBS/quick-box 소비 경로의 한도를 확정한 결과가 아니므로 자동 축약하지 않았다. 파생 coverage SHA `d9960f1e9ef7e13b22210289329f6d4c3fe71c55c6c099aa44b1afeeb95ec31a`,worklist SHA `7ff6238310f15219df4c907821dc6163bb0e1f1d034598874446ef1131979c6e`.

## 500개 묶음028 — 상점·시간대 NPC·잡담 게시판·서치맨

묶음027 이후 남은 일본어 중 정확히 **500개 stable catalog literal**을 번역했다. 706498 일반 상점191개,706C78 힐 상점191개,79D650 시간대 NPC51개,701ED8 잡담 게시판65개,78B6F4 서치맨 경고2개이며5개 자산/100개 플레이어 선택지를 등록했다. 누적 신규 초안 **18,437개**, 초안 미작성 일본어 **9,015개**다. 모든 문안은 needs_review/NON-DISTRIBUTION/release_eligible=false이며 인간 승인·삽입 준비 완료가 아니다.

원문 전체 literal/제어를 읽고 두 상점 TPL의 전체 diff를 확인했다. 둘의 차이는 상인 초상화와7개 상인 문구뿐이다. 원문·내비·소비 제어가 동일한 거래 문구는 같은 수동 작성 번역을 각 stable ID에 재사용했고, 일반 상인의 존대/감사와 힐 상인의 거친 말투/품절 사과를 따로 번역했다. 21개 내비의 구입/제니 부족/소지한도 말투, 선택지의 두 칸 공백과 width8/default/disableB, item/chip/NaviCust의 buffer1, 서치맨 nickname63/64를 보존했다. 구입명 뒤는 조사 없는 문장으로 작성해 삽입명 받침에 따른 오류를 피했다. 「/」 쌍과 [z]/z/대시 원문도 유지했다. 13개수 개/24칩수 장의 작은 폰트 소비 경로는 실제 ROM에서 추가 검증해야 한다. Bass fallback230..235가 @size230 로컬 TPL 밖을 가리키는 원문도 변경하지 않았으며 실행 가능성이 입증됐다는 뜻이 아니다.

79D650 실직 프로그램/치안 담당/아이 픽업/노인/연인/점심 대사를 구분하고60/61의 Yellow↔Pink 초상화 전환을 literal별로 기록했다. 오퍼레이터·남편·아이3인 가족을 내비 가족으로 바꾸지 않았다. 흡입/응원가 칩 연애 비유는 후보 용어이며 인벤토리 변경을 의미하지 않는다. 23:30..25:25 원문 시간 범위는 정규화하지 않았다. 701ED8 이나리·아야의 자기소개와 기타 작성자 미확정 상태, 여성 할인 행사/버그 조각 트레이더/비밀 대회 소문, 재참가 시 같은 내비 조건과 언더인터넷4·무사C·더 강한 다크로이드 소문을 구별했다. 78B6F4는 명시 SearchMan의 레이더로 측정 불가한 어둠의 힘에 대한 경고만 번역했으며 보스/위치를 덧붙이지 않았다.

개발용 지급·등록·플래그·바닥/BG 설정 메시지가 섞인7794EC67개 일본어는 원문 전체를 읽었으나 실제 소비 경로가 불명확하여 이번500개에 넣지 않았다. 원문/미작성 분모에는 그대로 남아 있다. 일반 대사 후보로 대체했으며 내부 메시지로 수량을 채우지 않았다. 두 상점 비일본어144개와 BBS02 ASCII 임시표시35개도 원문 그대로다.

검증: 누적351개 회귀 검사 통과(135.818초). 신규 serializer 재생성, 변경3도구 py_compile, 원문/제어/숫자/공백/BDF/codec/미선택 보존 검사 PASS. plan 기존 자산·묶음 prefix 그대로다. prepare 두 번 재생성한 coverage/worklist의 해시가 일치했다. 보수적132px 경고131개(일반상점40/힐상점40/시간대NPC21/잡담게시판29/서치주의1)가 추가되어 총2230개다. 실제 consumer 한도를 확정한 결과가 아니므로 자동 축약하지 않았다. coverage SHA `5666c95064cd68cd275a1e034aa9ade12c7203d99b29d0b390a39604e1649485`,worklist SHA `f18e92485fdb7d44f391d3c2e57327cb32133996c9e991cd4abe34eee4ffff67`.

기존 모든 자산·plan 앞부분·원본 ROM/TPL/catalog·기준 ROM을 보존한다. 이번 묶음에서는 ROM 빌드/세이브 변경/에뮬레이터 조작/이미지 변경/화면 검증을 하지 않았다. 번역부터 마무리한 뒤 ROM 통합/실제 화면·저장 검증을 하는 요청 순서를 유지한다.


## 500개 묶음029 — 보라 상점·버그 조각 교환·목요일 NPC·잠금문/쓰레기 데이터

묶음028 이후 정확히 **500개 stable catalog literal**의 초안을 작성했다. 707450 보라 상점191개,707C30 버그 조각 교환191개,79E148 목요일 NPC68개,79975C 잠금문/쓰레기 데이터50개다.4개 자산/100개 플레이어 선택지/2개 연출점 literal이며 유일 문장500개가 아니다. 누적 신규 초안 **18,937개**, 초안 미작성 일본어 **8,515개**다. needs_review/NON-DISTRIBUTION/release_eligible=false를 유지하고 기존 초안/등록/원본 TPL·catalog를 보존했다.

보라 상점은706498과263개 원문 literal이 같고7개 상인 초상화만 PurpleNavi로 달라진다. 존대 상인/내비별 문맥에 맞는 기존 수동 초안 표현을 새로운 stable ID에 재사용했다. 버그 조각 교환점은NormalNaviPink 상인·89개 원문 literal 변경·script11 soundDisableChoiceSFX 추가를 모두 확인했다. 구매/제니 부족을 교환/버그 조각 부족으로 별도 작성하고 소지한도 경고·공백·각 내비 말투·원문 줄 수를 유지했다. 메탈맨과 우드맨 교환 결과의 말줄임표가 없는 원문 예외도 반영했다. 닉네임/아이템/칩/프로그램/수량 삽입과50개씩의 선택지를 보존했다. [z]/z/따옴표/대시144개 비일본어는 그대로이며 가격 소비 경로를 추측으로 고치지 않았다.13개/24장 작은 폰트와Bass fallback230..235는 실행 증거가 아니다.

79E148 전체 원문/제어를 읽고 실직 프로그램의 정체성 고민·일자리 찾기,목요일 피로/금요일 업무 마지막 날,아이의 엄마인 오퍼레이터,야간 경비,노인,연인,나무 속성에 약한 NPC,점심 대사를 구별했다. 0:3/4 연출점은각각 . 후보로 번역하되3개 wait10과 독립 literal을 유지했다. 목요일/금요일은 인물 대사이며 달력 체계 수정이 아니다. 12개 시간 분기 및24..29:59/23:30..25:25 원문 범위를 정규화하지 않았다. 60/61 Yellow↔Pink 전환을 literal별로 기록하고 디스코드/블라인드 칩 연애 비유와1개 버그 표현을 유지했다. 칩 이름과 말투는 검토 전 후보다.

79975C 전체 원문/제어를 읽고 일반 잠금문 설명→내비8넘버맨/7브루스/16섀도맨 해독→숨긴 기계 응답7/flag861 순서를 보존했다. 나머지 내비에 잠금 해제를 덧붙이지 않았다. printItem7 조각상은 아이템명을 추측해 고정하지 않았다. 쓰레기 비어 있음과contents1..8 보상 분기를 구별했다. 29/49/135/133의A코드 칩1개,240/430제니 실제 buffer3,버그 조각1/2개·animation24/25·reset과지급제어를 유지했다. 내비명 뒤는 고정 은/는 대신 쉼표를 사용했다. TPL에 없는 데이터 소모/무한 파밍 조건을 만들어 넣지 않았다.

검증: 누적357개 회귀 검사 통과(134.512초). 신규 serializer 재생성/원문·제어·숫자·공백·BDF·codec·미선택 보존 검사/변경3도구 py_compile PASS. 기존 plan 자산·묶음 prefix 보존,prepare 두 번 생성한 파생물 해시 일치. 보수적132px 경고115개(보라상점40/버그조각교환33/목요일NPC29/잠금문/쓰레기13)가 추가되어 총2345개다. 실제 consumer 한도 확정이 아니므로 자동 축약하지 않았다. coverage SHA `8c492eb8f5dcdd9c3e98e2944116f24afba3c6ff0942e092f16794bb28d81591`,worklist SHA `475a5edfe23fd838c17e7a8dcc85bdca8b17fc4a1203b9558ddd2780b1bad0a0`.

이번 묶음에서는 ROM 빌드·세이브 변경·에뮬레이터 조작·이미지 변경·실제 화면 검증을 하지 않았다. 내부 개발/오류/입력 글자판 등 앞서 남긴 항목도 원문과 미작성 분모에 유지한다. 번역부터 마무리한 뒤 ROM 통합과 실제 화면·저장 검증을 하는 요청 순서 및 배포 불가 상태를 유지한다.


### 후속: 500개 묶음030 — 네이팜 조작·임무, 섀도맨 임무 현장, 인터넷7 NPC (2026-10-12)

묶음029 이후 정확히 **500개 stable catalog literal**을 개별 작성했다. `translations/batch500_030_napalm_missions_71A66C_draft_ko.json`218개, `translations/batch500_030_shadow_encounters_7C2954_draft_ko.json`212개, `translations/batch500_030_internet7_npcs_7A9EE4_draft_ko.json`70개다. 선택지12개와 연출점2개를 포함하며 유일 문장500개가 아니다. 누적 신규 초안 **19,437개**, 초안 미작성 일본어 **8,015개**. needs_review/NON-DISTRIBUTION/release_eligible=false이며 원문·기존 초안·ROM 선택은 변경하지 않았다.

71A66C의 전체36슬롯 TPL을 읽고 십자버튼 조준·A 파이어 봄·B+십자버튼 고속 이동·게이지 충전 시 R 준비→A 네이팜 봄·1발 후0/시간 충전을 보존했다. 의뢰14..17 표적40/18..21 표적45/22..25 표적50/26..28 표적55,60초 제한/5초 감점과 시민·암상인 손님·연구소 직원·의뢰인 부하·대회 심판의 보호 대상을 구별했다.26은 바이러스 모양의 길드 탐색 프로그램이며25의 운반 물건 내용은 추측하지 않았다.27의 우승 조건은 원문 전언을 유지했다.30/31 훈련40/55와 시민 보호·메뉴 선택지8·기동 문구의 wait50/분절을 보존했다.

보상7:0..3/11..13:0..2는 초상화 없는 지급자이며 뒤의 네이팜맨 대사를 소급해 화자로 지정하지 않았다. 명시 네이팜맨의 반응과 숨긴 보상 내레이션을 분리했다. HP메모리 item33/제니·버그 조각 buffer3/minLength1 및4294967295 지급 명령 인수를 유지했다. 해당 인수는 표시 금액으로 번역하지 않았다. 제니는 `네이팜맨은`+변수+`제니를\n얻었다!`, 버그 조각은 `네이팜맨은 버그 조각을\n`+변수+`개 얻었다!`로 연결하며 실제 변수 길이·배치는 미검증이다.

7C2954의 전체255슬롯 TPL을 읽고32개 임무 현장10..41의 global16=513/flags6049,7701과 모든 초상화 전환을 보존했다. 암살 대상의 발언과 섀도맨의 발언을 literal별로 구별했다.23의 오피셜 초상화는 변장한 인물이며 실제 오피셜로 단정하지 않았다.19 오퍼레이터 배신 의혹/38 속임수의 주체는 원문처럼 확정하지 않았다.39는 대상 자신이 자기 암살을 의뢰하여 딜리트된 동생의 복수를 꾀하는 장면이다. 의뢰인을 동생으로 바꾸거나 외부 조직으로 추정하지 않았다.33 가짜 다크 칩150000제니/37 유언장 변조와1명 독차지/미상 의뢰인을 보존했다.

29:5 및37:7/8은 원문 end 뒤에도 존재하는 literal이다. 실행되지 않을 것이라는 가정으로 제거하지 않고 초안과 제어 구조에 남겼다. 실제 도달성은 미검증이다.14:0 비일본어 `!!`는 원문/기타 검토 분모에 그대로다.25 역순 업계 말장난은 의미와 섀도맨의 맞장구를 살린 방해/진짜 후보이며 역순 음성 장치는 보존되지 않아 인간 검토가 필요하다.40 혼합 사투리는 한국어 시골 말투 후보이지 특정 지역의 공식 등가 표현이나 승인된 손실이 아니다.

7A9EE4 전체255슬롯 TPL을 읽고 인터넷7의 좌우 대칭/8·9 안내/오피셜 관리, 운동 중·수면 꿈·명상 NPC와 일렉맨40/44 권유→43 승부/41·42 결과를 구별했다.100만 볼트의 원문 숫자100과 선택지4/긍정2공백·폭11/9·전투 globals24..28/flags1806,7701을 보존했다. 운동 과다/부유/챔피언 꿈은 인물의 발언이며 새 게임 기능이나 실제 운동 지침으로 바꾸지 않았다. 황금 프로그램50은 callClearBattleChipGateHistory/sound154로 배틀칩 게이트의 사용 횟수를 회복하는 내용이지 칩 신규 지급/유료 거래가 아니다.

오피셜60/100/103의 첫21플래그군→뒤21플래그군 우선순위와50→62 간격을 유지했다. 셰이드맨 격파 전언과 아직 남은 미상 다크로이드를 구별하고 명령 없이는 움직일 수 없다는105를 보존했다.60:1/2 연출점은 각각 . 후보로 쓰되 wait30의 분절을 유지했다. 명칭·말투·말장난은 모두 검토 전 후보다.

검증: 누적363개 회귀 검사 통과(134.455초). 변경3도구 py_compile PASS,500개 serializer 재생성 일치, 원문·제어·수치·공백·BDF·codec·미선택 보존 검사 PASS. prepare 두 번 생성한 coverage/worklist 바이트 해시 일치. 보수적132px 경고116개(네이팜22/섀도78/인터넷7NPC16)가 추가되어 총2461개다. 실제 consumer 폭 확정이 아니므로 자동 축약하지 않았다. coverage SHA `9aca16e0468566e0f5cf1232b2aa4faa77127c9a9a49267df94ec0dd15b49e79`,worklist SHA `a468362616eb4851cc525bcffeee097a3e628488b73da7f77d2b0bd5ea3f9eaa`.

원본 ROM·기준 ROM·카탈로그 SHA는 기존 값과 일치한다. 이번 묶음에서 ROM 빌드·세이브 변경·에뮬레이터 조작·이미지 변경·실제 화면 검증은 하지 않았다. 기존 내부 개발/오류/입력 글자판 항목도 원문과 미작성 분모에 유지했다. 전체 초안을 먼저 갖춘 뒤 삽입 준비를 검증하여 누적 ROM 통합과 실제 화면·저장 검증으로 진행한다.


## 500묶음031 — 나이트맨·포르테 배틀 / 통신 오류 / NPC 초안

7C416C 나이트맨 배틀172, 7C5CE0 포르테 배틀141, 776650 통신 오류184, 7B0328 NPC3으로 정확히500개를 개별 작성했다. 선택지126개·구두점 반응2개를 포함한 stable literal 수이며 유일문장 수가 아니다. 누적 신규 초안19,937개, 미작성 일본어7,515개다. 모든 신규 항목은 needs_review / development-draft / NON-DISTRIBUTION이며 release_eligible=false다.

원문4TPL의 대사·초상화 전환·제어를 읽었다. 나이트맨20배틀의 global8=4..23/global9=11..49/global10=6082..6101 및 flags6102/7701, 포르테20배틀의 global11=24..43/global12=1/global13=6594..6613/global14=6614..6633 및 flags6634/7701을 변경하지 않았다. 거절 선택지·닉네임 삽입·공백을 유지하고 나이트맨 닉네임 뒤는 ‘님께서’로 고정 조사 문제를 피한 후보를 작성했다. 포르테의 갈증/만족은 배틀 비유이며 실제 상태 게이지나 강제 배틀 구현을 뜻하지 않는다.

통신 오류23내비×4스크립트에서 칩 게이트 없이 재시도/배틀 종료 선택과 flags7730/7731, 재시도 jump, 저장 주의와 정크맨3행 예외를 보존했다. 로컬 초상화 없는 재시도/종료 대사는 확인된 루트 호출자 계승 화자로 기록하되 origin_portrait=None을 유지했다. 후반 중단/칩게이트 사용불가 안내의 end 뒤 ASCII ‘4’46개는 원문 유지했다. 실제 저장 수행이나 하드웨어 오류 원인을 단정하지 않는다. NPC 쓰레기 투기 자랑은 아이템 지급/제거 명령으로 해석하지 않았다.

7C416C:1:0/1:1 임시·맥락 불명 대사는 원문/미작성 분모에 유지했다. 기존 개발/오류/입력 글자판 및 catalog 밖 inline·폰트·이미지 범위도 미해결이다. 문체·용어·의미 검토와 별도 재검토는 아직 완료가 아니다.

serializer 재실행은 기존4JSON과 일치했다. 전체369개 회귀 검사 통과(145.152초), py_compile 통과, prepare 두 번 생성한 coverage/worklist 바이트 해시 일치. 이전304개 draft_assets와 완료 묶음 기록의 접두부도 그대로 보존했다. 보수적132px 경고89개(나이트27/포르테17/통신44/NPC1)가 추가되어 총2550개이며 실제 consumer 폭 판정이 아니다. 자동 축약하지 않았으며 닉네임 길이·선택지·실제 화면 검증이 필요하다. ROM/세이브/에뮬레이터는 변경하지 않았고 화면 검증도 이번에 수행하지 않았다.

coverage SHA `63507d0f3877b6928131d0d40789c3680e95b1b06a76e4c0caeaab546d5bf6d0`, worklist SHA `e81bed5ff4dee0a2293d95b91b05b8963745715f772a497ec05d7ece2d0f1ab1`. 원본 ROM·기준 ROM·catalog 해시는 기존과 동일하다.

## 500묶음032 — 골드·실버 접수/시험 / 금요일 NPC 초안

7AB4B4 골드 접수·시험·내비배틀·상인325, 7A5604 실버 접수·견습 시험·롤·상인134, 7A4A8C 금요일 NPC41로 정확히500 stable catalog literal을 개별 작성했다. 선택지66개, 구두점만 있는 항목8개(금요일 연출점7/실버61:3말줄임1)를 포함하며 유일문장500개가 아니다. 누적 신규 초안20,437개, 미작성 일본어7,015개다. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false 유지.

원문3TPL 전체 대사·제어를 읽었다. 골드는 실버 우승 item2 자격/평일 접수/심사위원3명, 30초 이내·버스팅 레벨8 이상·칩 획득 조건을 구별하고 합격 데이터 item12/13/14 각각1개와 등록비20버그조각을 보존했다. 실버 참가비500제니와 견습 응시료690z, item0수험/1라이선스, 인터넷1계단을 통한 인터넷2시험장 안내를 보존했다. 실제 비용 차감/보상/통과와 runtime 시험 성공을 새로 주장하지 않는다.

겐(매)·벨츠(기술의 마술사)·준(뜻밖의 행운)은 명시 Yellow/HeelPurple/Orange 심사위원의 문체·이름 후보다. 공식 명칭 승인이나 별도 의미 검토는 아직 아니다. 아이스맨·정크맨 동일 내비 예외, 정크맨 고철/외로움·더듬음, 롤 배틀 다이어트 농담을 유지했다. 윈드맨100은 내비가 아닌 오퍼레이터 조작 시험/hard=false이며 원래 globals/flags/분기를 변경하지 않았다.

동적 내비 이름 뒤 보상/제시는 콜론 제목형 후보로 조사 의존성을 피하고, 아이템 소지는 ‘소지하고 계신가요?’로 작성했다. source ID·원문·인수·토큰·줄·선택지 패딩을 보존했다. 골드10:3의 원문 여는 따옴표 단독은 비일본어 슬롯으로 그대로 유지했다. 숨긴 보상 메시지/221상인 응답은 로컬 초상화 미표시로 기록했으며 확인되지 않은 호출자 화자를 확정하지 않았다.

금요일의 겁먹은 힐 내비·마초 훈련·베테랑 회상·토요일 기대와 두3행 시를 구별했다. 시의 줄 앞 ASCII 공백과 연출점/20프레임 wait8회를 보존하되 한국어 후보가 일본어5-7-5 운율까지 재현한다는 주장은 하지 않는다. 실버 접수의 사투리 원문은 정중한 한국어 후보이며 문체 검토가 남았다.

py_compile과 원문/제어/한글 글리프·codec 검사를 통과했다. 375개 회귀 검사 통과(140.661초). serializer 재실행은 기존3JSON과 일치하며 prepare 두 번 생성한 coverage/worklist 해시 일치를 확인한다. 이전308 draft_assets 및 완료 묶음 기록은 보존한다. 보수적132px 경고96개(골드70/실버20/NPC6)가 더해져 총2646개다. 실제 consumer 용량 확정이 아니며 자동 축약하지 않았다.

coverage SHA `9169af4684ece69ac50f6b6693246990369c5e6b170a530133199440a7901a80`, worklist SHA `41978a81bb9efe75f7549279dce307efe2862cb67a7b45c9c02d2e87015106fa`. 원본 ROM·기준 ROM·catalog 해시 동일. ROM/세이브/에뮬레이터 변경 및 이번 화면 검증 없음. 모든 남은 일본어·개발/오류/입력 글자판·catalog 밖 inline/폰트/이미지·키보드 저장·의미/문체/레이아웃/별도 검토·통합 ROM/runtime/release 검증은 계속 열려 있다.

## 500묶음033 — 견습 시험 / 인터넷2·6 / 플러그아웃 / 배틀 게시판 제목

7A152C 견습 라이선스 시험·인터넷2 대사270, 7A8EC0 인터넷6·배틀·상점84, 778338 플러그아웃80, 700F6C 배틀 게시판 작성자/제목30, 7A0354 인터넷2 NPC36으로 정확히500 stable literal 초안을 작성했다. 선택지98개와 구두점만 있는 항목5개를 포함하며 유일문장500개가 아니다. 누적 신규 초안20,937개, 미작성 일본어6,515개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false 유지.

5개 원문 TPL 전체와 제어를 읽었다. 견습 시험의10문제 정답 분기/오답 차이를 보존했다. ‘더플 딜리트’와 ‘더블 딜리트’, PA·HP·콤보 오답을 구별하고 원문 ASCII 답10/S/Z·960z/530z/690z는 유지했다. 재시험100z, chip104/codeA/수량1, 인터넷3·4 안내와 인터넷3 라이선스 지급 목적지를 바꾸지 않았다. 위조 통행증 판매자의 정상가격10000z 주장과1500z 거래, item8 지급은 구별하며 판매자 말이 실제 안전성 보증이라는 뜻은 아니다. GutsMan39의 확인 분기가 Aqua 루트36으로 향하는 원문 이상점은 그대로 유지하고 consumer/runtime 확인 대상으로 남겼다.

MetalMan·PlantMan 배틀과 NumberMan·MetalMan 오퍼레이터 미니게임/hard=false, 동일 내비 예외와 globals/flags를 보존했다. 플러그아웃 기본 ‘아니요’와 확인 이후 내비별 응답, 닉네임 삽입, Shadow/Bass 빈 줄을 유지했다. 기존 ROM 선택 Roll/Guts 항목은 이번 초안에 중복 등록하지 않았다. 자기장 이상 오류7711을 통신 오류로 바꾸지 않았다. 로컬 초상화 없는 문구에 호출자 화자를 임의 계승하지 않았다.

게시판30개 작성자/제목은 본문7000AC와 연결해 읽고 기존 후보의 사무조·봄보이 등과 맞췄다. ASCII 임시표시17개와 헤더 앞뒤 공백을 보존했으며 이름/용어 승인을 뜻하지 않는다. 제목의 공백은 선택지라는 근거가 아니므로 기존 trailing-space 검사에 명시적인 헤더 예외를 추가했다. 인터넷2 잡담의 점 단독4개, 선두 줄바꿈, wait20 명령6개를 보존했다. MetalMan 반응은9점으로 유지했다.

py_compile, 한글 글리프/codec, 숫자/원문/제어/미선택 보존 검사 통과. 회귀381개 PASS(145.661초). 첫 검사의 기대값4곳(원문 jump 표기/점 길이 및 헤더 패딩을 선택지로 오인한 두 검사)을 수정 후 전체를 재실행했다. 번역이나 원문을 검사에 맞춰 변경하지 않았다. serializer 재실행 JSON 일치, prepare 두 번 coverage/worklist 해시 동일. 이전311개 draft_assets 및 완료 묶음 기록의 접두부 보존, 현재316자산.

보수적132px 경고112개(견습/인터넷2 40·인터넷6 21·플러그아웃15·게시판28·인터넷2NPC8)가 추가돼 총2758개다. 실제 consumer 폭 승인이나 자동 축약 근거가 아니다. coverage SHA `96bc14779b14f09aaa7054e9eeeb3c226769eeee7c60d9945ae10e8d4195e9bc`, worklist SHA `aecb6518dd3a1bedaf927815cd1ddacc598dcd4892b7d4568dbac506d3a7ed63`. 원본/기준 ROM/catalog 해시 동일. ROM·세이브·에뮬레이터 변경 및 이번 화면 검증 없음.

766134 전투 지시 자료에는 여러 내비 항목에 우드맨 ‘데스 포레스트’가 반복되는 불일치가 있다. 실제 소비 경로 확인 전 임의 교정/번역/완료 제외하지 않고 미작성 분모에 유지했다. 입력 글자판·개발/오류 항목·catalog 밖 inline/폰트/이미지·한글 입력 저장·의미/말투/레이아웃 검토·통합 ROM/runtime/release 검증은 계속 열려 있다.

## 500묶음034 — 통신 대전 메뉴11종 / 폴더 이름 / 인터넷2 NPC

6F56B8/6F59F8/6F5D38/6F605C/6F63A8/6F66C8/6F6A04/6F6D5C/6F7084/6F73C4/6F76FC 통신 메뉴 각42개(462), 708FF0 폴더/배낭9, 7A0734 시간대별 NPC29로 정확히500 stable catalog literal을 개별 작성했다. UI 라벨119개와 나머지381개(연출점 단독2개 포함)를 구별했다. native option 선택지는0개다. 누적 신규 초안21,437개, 초안 미작성 일본어6,015개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false 유지.

13개 원문 TPL 전체를 읽었다. 통신11archive는 원본 ROM0x448E0의 연속11포인터와 일치한다. 이 사실은 저장 테이블 연결의 증거이며 실제 실행/내비 선택 경로·초상화의 런타임 증명은 아니다. 로컬 quick script에 mugshotShow가 없으므로 미확정 화자로 기록하고, 원문의 거스/거츠·바람·불꽃·뇌신·군인식 보고·존대·계산·영혼/수련·정크 더듬음을 별도 문체 후보로 유지했다. 다른 화면에서 넘버맨으로 임시 표시됐다는 이유로 대사를 넘버맨 것으로 교체하지 않았다.

전적 buffer0/1의 minLength3·왼쪽 패딩과 전/승 단위, 에그제4.5 리얼 오퍼레이션과 에그제4 대전, 1판/3판·선취2승, 서로 칩 게이트를 쓰는/쓰지 않는 모드를 구별했다. 양쪽 칩 게이트와 통신 케이블의 연결 확인, 미사용 모드에서는 칩 게이트 분리 후 재시도, 상대와 같은 모드인지 확인을 유지했다. 승리/완승/패배/완패/무승부/통신 오류는 서로 다른 메시지다. 계산형 문구의 승률0%·바람/불꽃 비유를 실제 배틀 확률/기상/강제 효과로 단정하지 않는다.

mmbn45s 고정 라벨과 mmbn45 quick 설명은 서로 다른 소비 경로이므로 UI 라벨을 대사/선택지로 분류하지 않았다. 기존 공백 검사에 명시적 LABELS 근거의 ui-label 분기를 추가했으며 공백 검사는 유지했다. 좌표10/12·92/110·225/141, box type1, textSpeed0, waitHold/keyWait/clearMsg와 원래 문자열 패딩을 변경하지 않았다. 실제 라벨 셀 수/표시 폭은 아직 별도 검증이 필요하다.

폴더1/2와 허접 폴더의 중복3개는 서로 다른 stable ID로 유지했다. ‘명인 폴더’·‘덤 폴더’·‘배낭’은 문맥 후보이며 인명/용어 최종 승인이 아니다. 인터넷2의 수줍은 Orange 여자 내비, Pink 잡담 두 화자, Yellow 점심시간 내비를 로컬 초상화로 구별했다. 익명의 변호사 내비에 특정 인물 이름을 덧붙이지 않고 연근 구멍 잡담을 유지했다. 수요일 오퍼레이터 남편의 이른 귀가·5시·저녁 시간 분기, 연출점2개, 선두 줄바꿈, wait20 세 번을 보존했다.

py_compile 및 원문/제어/숫자/공백/한글 글리프·codec·미선택 보존 검사 PASS. 전체387개 회귀 검사 PASS(157.790초). serializer 재실행13JSON 일치, prepare 두 번 생성한 coverage/worklist 해시 동일. 이전316개 draft_assets 및 완료 묶음 기록 접두부 보존, 현재329개 자산이다.

보수적132px 경고77개(메뉴63/NPC14/폴더0)가 추가돼 총2835개다. 메뉴 순서별2/2/2/9/9/5/9/8/11/3/3개이며 실제 소비자 폭 승인이나 자동 축약 근거가 아니다. coverage SHA `7fff8c688bfff83536a69fcae022a777ed848803a8305b1923f7c2a9c57b8c48`, worklist SHA `76e2aed0d258e233bfd4b05ef08f3d715d3405677c62609a5b4ea34b1e899aaa`. 원본 ROM·기준 ROM·catalog 해시 동일. ROM/세이브/에뮬레이터 변경 및 이번 화면 검증 없음.

미해결 개발/오류/입력 글자판 및 전투 지시 자료의 내비/기술 불일치는 원문과 미작성 분모에 유지했다. catalog 밖 inline/폰트/이미지, 한글 이름 입력·영구 저장/기존 save 호환, 의미·용어·문체/레이아웃 검토와 통합 ROM/runtime/release 검증은 계속 열려 있다.

## 500묶음035 — 통신 대전 메뉴 잔여10종 / 토요일 광장 NPC

6F7A04/6F7D10/6F8018/6F8344/6F8698/6F89D0/6F8D00/6F9038/6F9358/6F9698 통신 메뉴421개(42/43/42×8)와 7A4DD4 토요일 광장 NPC79개로 정확히500 stable catalog literal 초안을 작성했다. UI 라벨100개와 나머지400개(점 단독9개 포함)를 구별했다. native option 선택지는0개다. 신규 초안 누적21,937개, 초안 미작성 일본어5,515개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false 유지.

11개 원문 TPL 전체를 읽었다. 통신 메뉴의 반복된 quick 좌표 블록만 정확한 가역 읽기용 별칭으로 표시하고 원래 블록과 전체 복원을 확인했다. 원본 파일은 바꾸지 않았다. 원본 ROM0x448E0 포인터 테이블의 index11/12/15..22와 연결되며13/14는 첫 메뉴를 재사용한다. 저장 연결 증거를 실행/내비 선택 경로 증명으로 확대하지 않았다. quick 대사에 로컬 초상화가 없어 화자는 speaker-unestablished로 유지하며 물주제 퓨·대지·별·닌자 고어·기사 존대·거친 임무·어린 얼음·전기·우아한 꽃·파괴충동 문체를 별도 후보로 기록했다.

전적 buffer0/1/minLength3/padLeft·padZeros, 에그제4.5/4 대전과3판 선취2승, 나이트1번 두 차례와 재대전1판, 양쪽 칩 게이트 사용/미사용, 케이블/상대 게임/모드 확인과 게이트 분리 후 재시도를 보존했다. 물 비유는 승부의 불확실성을 살리고 별의 승리·전압/배터리·꽃다발/파괴 비유를 새 시스템 효과나 실제 아이템 지급으로 만들지 않았다. 물 구호와 시구는 인간 문체 검토 전 후보다.

6F7D10 script41은 두 literal 사이 clearMsg가 없고 두 번째 literal 끝에 줄바꿈이 있어 그대로 보존했다. 6F9698 script37의 질책은3줄이다. quick 좌표10/12·92/110·225/141/type1/delay0와 각24개 msgOpenQuick/waitHold, mmbn45s 라벨 패딩은 유지했다. 고정 라벨과 quick 대사를 같은 소비자/폭으로 승인하지 않았다.

토요일 광장은 Purple/Official/HeelBlack/Yellow/Orange/MrProg/Brown/Pink/HeelPurple 로컬 초상화와 시간대를 구별했다. script10의 시간 분기가11/12가 아니라1/2인 원문 이상점은 수정하지 않고 runtime 확인 대상으로 남겼다. 시골 말투에 임의의 한국 지역을 부여하지 않았다. 프로그램 두 사랑 대사는 역할별로 번역하고 같은 초상화를 이유로 한 사람으로 합치지 않았다. 두 시구의2/3행 선두 공백, 연출점9개/wait20 아홉 번, 토요일/플러그아웃/S라이선스·상위 토너먼트 이야기를 유지했다. NPC의 자격 취득 발언과 실제 지급 명령을 구별했다.

검증: 전체393개 회귀 검사 PASS(167.568초). py_compile, 원문·제어·숫자·공백·한글 BDF 글리프/codec·미선택 보존 PASS. 첫 검사는 원문 초상화 NaviGirlOrange를 NormalNaviOrange로 잘못 적은 검사 기대값1곳에서 실패했고 이를 수정한 뒤 전체를 재실행했다. 번역이나 원문을 검사에 맞춰 바꾸지 않았다. serializer 재실행11JSON 일치, prepare 두 번 coverage/worklist 해시 일치. 이전329개 draft_assets 및 완료 묶음 접두부 보존, 현재340개 자산.

보수적132px 경고43개(통신28/NPC15)가 추가되어 총2878개다. 통신 순서별1/4/3/5/6/2/1/4/1/1개. 실제 소비자 폭 승인/자동 축약의 근거가 아니다. coverage SHA `0f0799be03e8a2f4cc7e26ed0ac68f646a7f35c6ef58733a572eb5ef050c04c5`, worklist SHA `1944d9ab6bd7a8876e04e052ed68afa2af4d7e907580e60a2bc72a14949bb608`. 원본 ROM·기준 ROM·catalog 해시는 동일하다. ROM/세이브/에뮬레이터/이미지 변경 및 이번 화면 검증 없음.

입력 글자판·개발/오류/전투 지시 불일치와 catalog 밖 inline/폰트/이미지, 한글 이름 조합/영구 저장·기존 save 호환, 의미·용어·문체/레이아웃 검토·통합 ROM/runtime/release 검증은 계속 열려 있다. 원문 보호와 초안/승인/삽입/런타임 증거 분리는 create-kr-patch 스킬 원칙에 따른다.

## 500묶음036 — 요일·시간대 NPC / 인터넷 배틀 / 인터넷 학원

79CF04(14)/79DC10(46)/79EE9C(39)/79FCC8(22)/79FFF4(32)/7A0A44(29)/7A0D18(52)/7A3C0C(38)/7A4010(34)/7A4348(43)/7A6BC8(38)/7AF164(13)/7AAF94(52)/7A7FC4(27)/7B1D40(21), 15개 archive의 정확히500 stable catalog literal 초안을 작성했다. 실제 범주는 요일·시간대 NPC338, 배틀 NPC149(7A0D18의11개 포함), 학원 NPC13이다. native 선택지24, 연출점33, 시구6개를 포함한다. 처음 범위 계산의100개 차이를 합산으로 발견하여7AAF94/7A7FC4/7B1D40 전체 문맥을 추가로 읽고 수량을 채웠다. 임시·미확인 문구로 수량을 채우지 않았다. 누적 신규 초안22,437개, 초안 미작성 일본어5,015개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false 유지.

15개 전체255-slot TPL을 읽어 대사·시간·초상화·선택지·배틀 분기를 함께 확인했다. 같은 MrProg/Pink/HeelPurple 초상화가 쓰여도 화자 역할을 합치지 않았다. 수요일 경비 안내의주4회 월·수·목·토, Orange의7시, 밤 순찰과 야간 오퍼레이터의24..29시간 범위를 원문 그대로 유지했다. unemployed MrProg의 요일 감각/일요일/멍함/토요일 애니메이션과 야간 순찰 경비원·집을 짓는 오퍼레이터는 서로 다른 문맥이다.

79EE9C의60/70/71 대화는 Yellow/Pink 초상화가 중간에 바뀐다. 연인의 에리어 스틸·마음 도둑·기가 칩1000장 두 차례 비유를 실제 칩 사용/지급으로 만들지 않았다. 경비원의 잔소리와 gossip 반복 출력의 선두 줄바꿈·wait20, 점 단독33개를 보존했다. 7A0D18의 하이/텐/션 구호는3개 literal 페이지를 유지했다.

Official 만담 내비의 엉뚱한 소리/태클 역할, 금요일/새우튀김 연결, 시골·거친 말투와 닌자 고어는 인간 검토 전 문체/각색 후보다. 특정 한국 지역이나 인물 이름을 덧붙이지 않았다. Brown의 하이쿠 설명은 일본 문화로 남기고,6개 시구의3줄 및2/3행 선두 공백을 보존했다. 한국어 시구가 원작의 정형 하이쿠와 동등하다고 승인한 것은 아니다. 미니봄을 던지다가 허리를 다친 이야기·캐논/소드·안전제일과 훈련 과장은 신규 능력치 효과로 해석하지 않았다.

배틀12개 루트의수락/거절·기본선택0·좌우 폭8/9/10·숨긴 초상화·승패/재대전 거절을 유지했다. nativeglobals24 값150/151/153/152/158/159/160/161/154/155/168/169, globals27 값628/629/631/630/636/637/638/639/632/633/646/647, flags1806/7701을 수정하지 않았다. ‘배틀=인사’, 친근/거친/닌자/바이러스 사육/청춘 문체를 구별하고, 수줍은 HeelPurple15가승리 후18/19에서 허세/패주 칭호를 말하는 차이를 남겼다. 닌자풍 HeelBlack을 섀도맨으로 임의 확정하지 않았다.

인터넷 학원은 원장/사회 교사/학습 후 말이 바르게 된 MrProg/졸고 있는 Purple/집중하는 Orange/사회 암기 어려운 Pink를 구별했다. 명태 어획량이 일본에서 가장 많다는 교사의 설명을 한국 지역으로 바꾸지 않았다. 이는 게임 대사 번역이며 실제 지리 통계 검증 주장이 아니다.

검증: 전체399개 회귀 검사 PASS(182.776초). py_compile·원문/제어/숫자/공백/BDF 한글 글리프/codec/미선택 보존 PASS. 신규15개 serializer 재생성JSON 일치, prepare 두 번 생성한 coverage/worklist 해시 동일. 기존340개 번역 자산 SHA와 plan 자산/완료묶음 접두부 보존, 현재355개 자산이다.

보수적132px 경고142개가 추가되어 총3020개다. archive순서별2/14/10/13/10/5/14/15/10/12/11/2/12/6/6개이며 실제 consumer폭 승인이나 자동 축약 근거가 아니다. coverage SHA `ebef76082e8a0b84f0ac21a953e3f292a5da6ac84391a7bd89f662c578b9428c`, worklist SHA `368244bc8f67a1d243040808f90a2dbbe01be0bddc6bf8449ec9399478592264`. 원본 ROM/기준 ROM/catalog 해시는 그대로다. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음.

남은 일본어 전체 초안 작성 후 제어/글꼴/consumer/레이아웃·누적 ROM 적용과 화면/저장 회귀 검증을 진행한다. 입력 글자판·개발/오류·전투 지시 불일치·catalog 밖 inline/폰트/이미지·한글 이름 조합/영구저장·기존save호환·의미/문체/용어 승인·통합 runtime/release는 미완료다. 원문 보호와 초안/승인/삽입/실행 증거 분리는 create-kr-patch 스킬 원칙을 적용했다.

## 500묶음037 — 인터넷 장애물·보안문·조사/보상 / 에브리데이 진행자

799314(18)/7994EC(24)/799CAC(26)/799F58(63)/79A340(25)/79A5F8(29)/79A8E4(24)/79AB58(41)/79AF64(72)/79B45C(37)/79B750(36)/79BB10(27)/79BDE4(26)/79C084(9)/79C2C4(19)/79C608(24), 16개 전체 TPL의 미작성 일본어500 stable literal 초안을 개별 작성했다. 장애물·문·조사·획득457, 에브리데이 진행자43이며, 선택지8·점 연출3·임시 표기1개를 포함한다. 누적 신규 초안22,937개, 미작성4,515개. 모든 초안은 needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false이며 ROM에 삽입하지 않았다.

전체 TPL의 원문, 내비 분기와 초상화, 동적 출력 앞뒤, 보상·차감·문 해제와 대회 호출을 확인했다. 거츠맨/메탈맨/나이트맨 바위, 우드맨/플랜트맨 그루터기, 파이어맨/네이팜맨 불길, 아쿠아맨/아이스맨 소화, 썬더맨/일렉맨 전류, 윈드맨/포르테 회오리, 넘버맨/브루스/섀도맨 전자 잠금 대사를 구별했다. 초상화 없는 결과 설명과 흡혈귀에 묶인 문은 임의로 특정 내비 대사로 바꾸지 않았다. 넘버맨 확인용 에뮬레이터 개입이나 대사·초상화 교체도 이번에는 없다.

printCurrentNavi·printItem·printChip·printBuffer가 끼어 있는 literal 경계·순서·기존 따옴표를 보존했다. 삽입 값 뒤의 은/는·을/를 고정 조사를 피하기 위해 이름 뒤 콜론/아이템명 뒤 쉼표·획득/사용 표현과 받침에 무관한 ‘의 손으로’를 초안에 사용했다. item7이 삽입되는 조사 대사10개는 받침에 관계없이 이어지는 ‘이다’로 개별 보완했다. 79B750:16:1의 끝 줄바꿈, 79AF64:3의 페이지 분리도 그대로다. 변수 길이/글꼴/실제 표시 예산 검증은 별도이며 이 표현이 화면 승인된 것은 아니다.

세금 포함10000제니 통행증 안내, 번역 도구/버그 조각20개 납부·부족/거절 분기, item20의1개 차감과 예외 통과, chip85A 확인·문에 제시(칩 차감으로 변경하지 않음), 플러스/마이너스 잠금의 작동/해제 상태를 구별했다. JunkData1..3의 칩29/119/8/46 코드A 각1개·제니490/670·버그 조각2/3개, JunkData4의 칩29/95/121/55 코드A 각1개·제니560/770·버그 조각3/4개의 원문 명령은 수정하지 않았다. 일반 인터넷 최강 칭호/item4와 셰이드맨 격파4270·문1644는 서로 다른 조건이며, 문이 말하는 다크로이드1체/2체 표현도 보존했다. 원문 제어의 동작까지 새로 런타임 승인한 것은 아니다.

에브리데이 대회4의 PurpleNavi는 친근한 반말·구호, 대회5의 Yellow는 존대에서 큰소리로 전환하는 문체를 유지했다. 9/13/16/20시와 각59분 분기·AM/PM 시간 표기, default0/폭8/선택·거절·우승 후 분기, flags1854/1877/7736 및 callTournament4/5를 보존했다. ‘2등도3등도’와 점3개/각wait30 연출은 원문 수량대로다. 79C608:0:0 ‘노멀 트레이더(임시)’는 원문 임시 표시용 대사이며 실제 트레이더 기능을 새로 구현하거나 승인했다는 뜻이 아니다.

검증: 최종 전체405개 회귀 검사 PASS(191.801초). 최초405개 검사12실패(192.285초)는 이전 묶음 ID 기대값 변경 실수10건과 실행 중 설명 메타데이터 갱신2건이었다. ID 복원 후 두 번째405개 검사1실패(193.795초)는 실행 중 서술어10곳을 보완하여 재생성 비교 기준이 달라진 결과였다. 두 실행은 최종 검증으로 인정하지 않고, 수정이 끝난 파일을 고정한 뒤 전체 검사를 다시 실행했다. 원문/제어 skeleton·숫자·범위·줄바꿈/공백·BDF 글리프·codec·미선택 보존 PASS. 신규16개 JSON 재생성 일치, 기존355개 번역 자산 SHA 및 plan 자산/완료묶음 접두부 보존, 현재371개 초안 자산. 최종 coverage/worklist를 두 번 생성한 해시 일치: coverage `a3e64f63ce3fecfe6e90a2951e8451a382a65585e4e7026132fec5d2c0fce099`, worklist `d5c9ff11e22ce1d54d44f79aa549f40fb1e6782c82e654b65e4af631f051940d`.

보수적132px 경고92개가 추가되어 총3112개다. archive 순서별2/7/3/12/6/6/2/7/21/0/4/6/3/1/7/5개이며 실제 consumer별 최대폭 확정이나 자동 축약 근거가 아니다. 기존 거츠맨 말투 거스/거츠, 넷/네트 용어 차이는 인간 용어·문체 검토 범위로 남겼고 이전 번역을 자동 통일하지 않았다. 기술명·의성어·문화/아이템 표기·일반 인터넷 최강 해석도 의미 검토/승인이 남는다.

원본 ROM/기준 개발 ROM/catalog 해시는 그대로다. ROM·세이브·에뮬레이터·이미지·자판 변경과 이번 화면 검증 없음. 전체 남은 초안 작성 후 글꼴·제어·소비 경로·레이아웃·삽입 준비를 검증하고 누적 ROM 적용/실제 화면·저장 회귀로 진행한다. catalog 밖 inline/폰트/이미지·한글 자판/조합/영구 저장·기존save호환·통합 runtime/release는 미완료다. 원문 보호와 초안/승인/삽입/실행 증거 분리는 create-kr-patch 스킬 원칙을 적용했다.

## 500묶음038 — 18내비 진행 안내 / 주말 닌자 NPC

786D38(29)/7870A8(29)/787418(28)/78776C(27)/787ACC(27)/787E18(27)/788198(27)/7884E8(28)/788858(28)/788BD8(27)/788F40(27)/7892C8(28)/78963C(27)/789998(27)/789D00(27)/78A088(27)/78A420(27)/78A7A8(27)/7A6F0C(6), 19개 전체 TPL의 미작성 일본어500 stable literal 초안을 개별 작성했다. 18내비 진행 안내494·주말 닌자 NPC6이며 선택지0개다. 누적 신규 초안23,437개, 미작성4,015개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false이며 ROM에 삽입하지 않았다.

18개 전체 archive의 literal을 읽고, 기준786D38·7870A8의 전체 제어와 나머지 archive의 각 script별 정확한 제어 차이를 비교하여 초상화·분기·페이지·변수 문맥을 확인했다. 7A6F0C는 전체 TPL을 읽었다. 록맨/롤/거츠맨/윈드맨/서치맨/파이어맨/썬더맨/브루스/넘버맨/메탈맨/정크맨/아쿠아맨/우드맨/스타맨/섀도맨/나이트맨/네이팜맨/아이스맨의 명시 초상화를 각각 유지했다. 닌자 NPC의 HeelNaviBlack은 섀도맨이 아니며, 검증을 위해 넘버맨 대사나 초상화로 바꾸는 개입도 없다. 기존 번역 문구나 말투를 자동 통일하지 않았다.

견습 라이선스 시험·합격 후 수령·chip104 획득, 인터넷3/5/7/9/10/12 사건과 범인 격파 후 휴식, 블랙워크스 마이너스키 회수/다른 내비1체 보유/인터넷9 전달을 구별했다. 출발 script10의 완료 플래그 → tournament bitmask4 → 셰이드맨4270 → 1322/1298 → item11 → 블랙워크스/메일/사건 → 견습 시험 조건의 우선순위를 보존했다. source의 닉네임별 플래그 수치도 변경하지 않았다. 26/28/29의 요일0/6 분기와 주말 대회/다음 주 참가 신청 안내, 27의 subarea0..3 → 35 관 표식 단서, 메일 확인 분기를 그대로 유지했다. 실제 대회 호출·시험 실행을 새로 추가하지 않았다.

원문13의 printChip(buffer0,chip104) 앞 「와 뒤 」 literal 경계/명령/순서를 보존했다. chip 이름 뒤 고정 을/를 대신 닫는 따옴표 뒤 줄바꿈과 구하기/찾기 절로 초안을 작성했다. nickname 뒤 쉼표를 사용하고, 브루스30·나이트맨30/32의 첫 빈 줄도 보존하여 받침 의존 호격을 임의 고정하지 않았다. 롤28의 참가 신청 권유 두 페이지와 브루스15의 수고/휴식 두 페이지는 병합하지 않았다. 삽입 변수 전체 길이·다시 표시되는 이름·글꼴·실제 화면 예산은 별도 검증이 필요하다.

넘버맨의 언더 인터넷 방문에 대한 망설임/영혼이 떨리는 대회, 정크맨의 더듬음/인기쟁이 소망과 수량 없는 ‘다른 쪽 내비’, 아쿠아맨의 두려움/퓨 말버릇, 메탈맨의 합격·근질거리는 주먹, 스타맨의 우리에게 어울리는 빛나는 무대, 섀도맨의 태세 정비/닌자의 극의, 나이트맨의 기사풍 말투, 파이어맨의 열기와 아이스맨의 차갑게 불타는 역설, 네이팜맨의 추가 발포 욕구를 개별 작성했다. 썬더맨33의 ‘아직 읽지 않은 메일’은 단순 새 메일 안내로 바꾸지 않았다. 이런 말투·비유·용어 후보는 인간 의미 검토/승인 전이며 기계 검사로 승인하지 않는다.

주말 닌자 NPC의15:30..19:45 → script1 시간 분기, 소인과 오퍼레이터 모두 쉬지 않음/닌자에게 휴일 없음, 수련 부족/최강 닌자 내비 목표/닌닌 구호를 보존했다. 닌자 화자라는 이유로 이름을 섀도맨으로 바꾸지 않았다.

검증: 전체411개 회귀 검사 PASS(204.359초). py_compile·원문 해시/제어 skeleton·숫자/범위·줄바꿈/공백·BDF 한글 글리프·codec·미선택 보존 PASS. 신규19개 JSON 재생성 일치, 기존371개 번역 자산 SHA와 plan 자산/완료묶음 접두부 보존, 현재390개 초안 자산. 수정이 끝난 번역/도구/plan/test를 고정한 뒤 전체 검사했으며 실행 중 authored 입력은 변경하지 않았다. 최종 coverage/worklist를 두 번 생성한 해시 일치: coverage `da248a1707f3eea29e24f09e6b8286678f2782ee47393f39c63daf978f3b04ad`, worklist `755e18ff8b5cff3e6a69a213098d5fb2498d88b427d78a4cd473bd4056080e9a`.

보수적132px 경고78개 추가, 총3190개다. archive 순서별0/1/8/5/5/6/1/4/1/3/4/7/2/2/8/6/6/8/1개이며 실제 consumer별 최대폭 확정이나 자동 축약 근거가 아니다. 기술 검증은 의미·인간 승인·실제 화면 검증을 대신하지 않는다.

원본 ROM/기준 개발 ROM/catalog SHA는 그대로다. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 남은 전체 초안 작성 후 글꼴·제어·소비 경로·레이아웃·삽입 준비를 검증하고 누적 ROM 적용/실제 화면·저장 회귀로 진행한다. catalog 밖 inline/폰트/이미지·한글 자판/조합/영구 저장·기존save호환·통합 runtime/release는 미완료다. create-kr-patch 스킬의 원문 보호와 초안/승인/삽입/실행 증거 분리를 적용했다.

## 500묶음039 — 서브칩 / 마지막 3내비 진행 안내 / 인터넷4 NPC

6F9B4C/6F9CA8/6F9E00/6F9F5C/6FA0B8/6FA228/6FA388/6FA4E4/6FA654/6FA7B8/6FA910/6FAA80/6FABEC/6FAD44/6FAEA0/6FB000/6FB164/6FB2C4/6FB41C/6FB574/6FB6D4 각16개, 78AAF0/78AE58/78B1C0 각27개, 7A6990(6)/7A7000(77)의26개 전체 TPL에서 미작성 일본어500 stable literal 초안을 개별 작성했다. 서브칩 설명/사용336·진행 안내81·오피셜 NPC6·인터넷4 NPC77이며 UI 라벨126/선택지52를 포함한다. 누적 신규 초안23,937개, 미작성3,515개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false이며 ROM에 삽입하지 않았다.

전체 원문 literal을 읽고 기준6F9B4C/78AAF0의 전체 제어와 다른20개 서브칩/2개 진행 archive의 각 script별 정확한 제어 차이를 비교했다. 7A6990/7A7000은 전체 TPL을 읽었다. 록맨부터 포르테까지21내비의 표시 초상화를 구별하고, 서브칩0..5의 mmbn45s 설명은 UI 라벨로 기록했다. 결과8/9/10에는 local 초상화가 없어 화자를 임의 확정하지 않았다. 정크맨 서브칩 원문에 없는 더듬음을 이전 진행 안내에서 가져오지 않았다. 검증용 넘버맨 대사/초상화 덮어쓰기 없음.

HP50 회복/최대 회복, 잠시 약한 바이러스 회피, 함정 해제, 직전 적을 다시 만날 확률 증가, 보안 미스터리 데이터 해석을 구별했다. 확률을 확정 배틀로 바꾸거나 모든 바이러스 회피로 확대하지 않았다. item0 buffer1 이름 앞뒤 따옴표 literal 경계·7의 마지막 줄바꿈/width8/default0/예 뒤 두 공백·변수/제어는 유지했다. 서치맨/브루스6의 닉네임 분절도 보존했다. 선택지42개에는 local 내비 초상화가 남아 있지만 화자는 player-choice이며, NPC 선택지10개는 숨김 상태로 구별했다.

일렉맨 MAX파워/짜릿함, 플랜트맨 최고의 꽃/무대 비유, 포르테의 시시한 여흥/경멸과 즉시 플러그아웃 의지를 각각 작성했다. 포르테33에는 원문에 없는 닉네임 삽입을 만들지 않았다. 진행 안내의 인터넷3/5/7/9/10/12 사건·chip104 동적 이름·마이너스키/다른 내비1체/인터넷9 전달·요일0/6 및 관 표식의 subarea0..3 분기·메일 우선순위/플래그 수치를 보존했다. 동적 이름 뒤 고정 조사나 받침 의존 호격 대신 따옴표 후 줄바꿈/쉼표 절을 사용했다.

인터넷4의 환영/시간대 프로그램, 프로그램의 대회 참가 자격 질문, 인터넷5로 가는 비탈길을 구별했다. 파이어맨/스타맨 배틀의 checkNavi5/15 → 같은 얼굴 전용38/39 분기, ‘나1명’/‘같은 얼굴3명’ 수치와 패배/승리/거절 반응을 유지했다. battle36/37의 globals24..28/flags1806·7701 및 시작 구호는 원문 제어 그대로이며 실제 배틀은 실행하지 않았다.

오피셜 NPC의 완료/라이선스 플래그 우선순위, 다크로이드 출몰/언더 잠복 정보/삭제 후 다시 살아날 가능성을 구별하고 가능성을 확정 사실로 바꾸지 않았다. 평화 NPC의 사건 희망 농담 뒤 즉각 부정도 보존했다. 상인의 item5 보유 →83, 인터넷2/3 사이 문 열쇠, 500제니 checkTakeZenny/부족82/1개 지급을 유지했다. currentNavi 이름 뒤 고정 은/는 대신 콜론을 사용했다. 실제 거래·아이템 지급·저장 실행 없음.

검증: 전체417개 회귀 검사 PASS(216.422초). py_compile·원문 해시/제어 skeleton·숫자/범위·줄바꿈/공백·BDF 한글 글리프·codec·미선택 보존 PASS. 신규26개 JSON 재생성 일치, 기존390개 번역 자산 SHA와 plan 자산/완료묶음 접두부 보존, 현재416개 초안 자산. 초기에 새 테스트가 checkNavi의 jumpIfTrue를 jumpIfEqual로 잘못 기대한 것을 확인하여 첫 실행을 조기 중단했다. 기대값 수정 후 번역/도구/plan/test를 고정하여 전체 검사를 실행했다. 최종 coverage/worklist 두 번 생성 해시 일치: coverage `2a798c7fc690de0628e0f84c7372cff74f61baf2a445f52d735ca35c67686ca1`, worklist `96fe739a500f7957053c7a4517026c6f89cc7b5f22da2b5983554b5e9acf405a`.

보수적132px 경고67개 추가, 총3257개다. archive 순서별1/1/2/2/2/1/2/2/1/2/2/2/2/1/3/1/1/1/1/1/2/2/0/6/2/24개이며 실제 consumer 최대폭이나 자동 축약 근거가 아니다. 기술 검증은 의미·인간 승인·실제 화면 검증을 대신하지 않는다. 열기/별/꽃 비유, 문화적 인사와 배틀 구호, 내비 이름/말투 및 기존 용어 차이는 검토 후보로 남긴다.

원본 ROM/기준 개발 ROM/catalog SHA는 그대로다. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 전체 초안 작성 후 글꼴·제어·소비 경로·레이아웃·삽입 준비를 검증하고 누적 ROM 적용/실제 화면·저장 회귀로 진행한다. catalog 밖 inline/폰트/이미지·한글 자판/조합/영구 저장·기존save호환·통합 runtime/release는 미완료다. create-kr-patch 스킬의 원문 보호와 초안/승인/삽입/실행 증거 분리를 적용했다.

## 500묶음040 — 배틀 작전·장비 / 게시판 반응 / 라벨 / NPC

704368(42)/7097D8(45)/766134(306)/768764(16)/778B08(33)/79C1D8(5)/7A8218(3)/7A82D8(27)/7A87FC(1)/7AF3E8(22)의10개 archive에서 미작성 일본어500 stable literal 초안을 개별 작성했다. 배틀 작전/장비/도주306·게시판 반응42·지역 라벨45·공격 라벨16·아이템 이름33·통행문5·NPC53이다. 선택지218/UI라벨94, 배틀의 분절된 대기 점6개를 포함하며 유일 문장500개는 아니다. 누적 신규 초안24,437개, 미작성3,015개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false이며 ROM에 삽입하지 않았다.

500개 전체 source literal과 배틀 외9개 전체 TPL을 읽었다. 배틀0..31의 literal을 분리한 정확한 제어 skeleton을 읽고,32..95의 모든 script를 기준4..7과 비교하여 초상화 외 제어 동일성을 확인했다. 숫자·선택지 order/width/default·BSeparate/disableB·명령/페이지/줄/공백을 보존했다. 내부 임시문구7097D8:0:0 xうそメッセージです는 번역 대상 선택에서 보류했으나 원문과 미작성 분모에는 남겨 두었다. 합쳐진 입력 라벨70904C 및 미니게임 이름71BE98도 임의 분절/번역하지 않았다.

배틀 도주 제안의 넷토 호칭과 성공/실패/도주 금지,18프레임 대기4회씩·분절 점6개를 구별했다. 작전 변경 여부와 실제 지시, 적 추적과 같은 줄 피하기, 윈드맨 돌풍/흡입, 브루스 실드/롱 소드, 칩 전송 대기를 각각 작성했다. 일반 메뉴 width8와 수직 선택 width13,0기본값/예 뒤 두 공백과 마지막 줄바꿈, 장비 쌍의 BSeparate/disableB 차이는 바꾸지 않았다.

원문 배틀65..67/69..71/73..75/77..79/81..83/85..87/89..91/93..95는 앞선 다른 내비의 작전 질문과 달리 WoodMan 초상화·데스 포레스트 장비가 반복된다. 이를 스타맨/섀도맨/나이트맨/네이팜맨/아이스맨/일렉맨/플랜트맨/포르테로 ‘수정’하지 않았다. 저장 순서나 앞선 질문만으로 이 반복 블록이 정상 플레이에 도달한다고 단정할 수 없으며, 미사용/임시/선택 경로 조사와 실제 소비 검증을 별도 미해결로 기록한다. 검증용 넘버맨 대사/초상화 덮어쓰기 없음.

게시판의21개 내비별 새 글이 있는 듯함/글이 전혀 없음 반응과 명시 초상화를 구별했다. 새 메일 안내로 바꾸지 않았다. positionText80,60/초상화54,80/arrow202,100/palette9/keyWait/waitHold를 그대로 유지했다. 거츠의 거츠/거스 및 아쿠아맨 퓨는 후보 말투로 유지하고 이전 초안을 자동 통일하지 않았다.

지역/공격/아이템 라벨은 대사가 아닌 mmbn45s UI라벨94개로 기록했다. 인터넷1..12/언더1..4/카오스1..2·전뇌명과 숫자 변형, 수도관1/무번호/2, 라이선스/열쇠/합격데이터ABC/서브칩 이름을 원문 의미에 맞춰 작성했다. printPlayerName 뒤 ‘의 HP’에는 받침 의존성이 없지만 동적 전체 이름 길이와 실제 label consumer 예산은 아직 미검증이다. 새 명칭·음역·띄어쓰기와 기존 번역의 일관성은 인간 용어 검토/승인 전 후보이며 자동 변경하지 않았다.

통행문 item3 수량1/부족→1/성공→flagSetNavi1713와 printCurrentNavi/printItem 경계를 보존했다. 동적 내비 이름 뒤 콜론과 item 닫는 따옴표 후 줄바꿈으로 고정 은/는·을/를을 피했다. local 초상화가 없어 안내/제시 결과를 특정 내비 화자로 확정하지 않았다. 실제 통과나 아이템/저장 변경 없음.

인터넷5 NPC의 인터넷8 골드 접수장·인터넷7 방향,1일 만에 건강이 되지 않음/아침과 다른 밤 산책/늦은 오퍼레이터를 구별했다. 윈드맨 동일 내비3→54와 hidden width9/default0 선택지4개,배틀53 globals24=131/25=51/26=52/27=1788/28=0 및 flags1806/7701을 보존했다. 주말 토너먼트 때문에 인터넷에 ‘인적이 드물다’는 문맥은 인기 하락으로 옮기지 않았다.

바이러스 사육 소녀의 자체 넷 배틀 약점/키운 바이러스 도전, 거절/승패 관점과 hidden 선택지2개·battle1 globals24=164/25=2/26=3/27=642/28=1을 보존했다. 학원 NPC의 수소 원자2개/산소 원자1개,늘 자지만 성적1등인 내비/수면 학습 가능성 질문, 듣는/자는/쉽다는 각각의 화자를 구별했다. 실제 배틀 실행/부상/보상 검증 없음.

검증: 전체424개 회귀 검사 PASS(220.703초). py_compile·원문 해시/제어 skeleton·숫자/범위·줄바꿈/공백·BDF 한글 글리프·codec·미선택 보존 PASS. 신규10개 JSON 재생성 일치, 기존416개 번역 자산 SHA와 plan 자산/완료묶음 접두부 보존, 현재426개 초안 자산. 수정이 끝난 번역/도구/plan/test를 고정하여 전체 검사를 실행했으며 실행 중 authored 입력 변경 없음. coverage/worklist 두 번 생성 해시 일치: coverage `f2fc6d42365217309143d7f0f488c55ccf8dc640e0e681e8ea2358fc25c3473e`, worklist `e504a6eace73a357c5212a4d47f974d59a0885ad6f61b8eac1ccaae3f026473f`.

보수적132px 경고108개 추가, 총3365개다. archive 순서별0/0/93/0/0/0/1/11/0/3개이며 실제 consumer 최대폭이나 자동 축약 근거가 아니다. 기술 검증은 의미·인간 승인·실제 화면 검증을 대신하지 않는다.

원본 ROM/기준 개발 ROM/catalog SHA는 그대로다. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 전체 초안 작성 후 글꼴·제어·소비 경로·레이아웃·삽입 준비를 검증하고 누적 ROM 적용/실제 화면·저장 회귀로 진행한다. catalog 밖 inline/폰트/이미지·한글 자판/조합/영구 저장·기존save호환·통합 runtime/release는 미완료다. create-kr-patch 스킬의 원문 보호와 초안/승인/삽입/실행 증거 분리를 적용했다.

## 500묶음041 — 배틀 대상·거리·도주 / 바이러스 미니게임 / 버스팅 튜토리얼 / NPC

71BE98(81)/768BD0(46)/76C944(278)/79C8F8(23)/7A8928(4)/7A89E4(7)/7A8B9C(27)/7A9AC0(5)/7ADD74(29)의9개 archive에서 미작성 일본어500 stable literal 초안을 개별 작성했다. 미니게임 설명81·버스팅 튜토리얼46·배틀 대상/거리/도주278·에브리데이 대회/NPC95다. 선택지58/UI라벨38/배틀 대기 점126개를 포함하며 유일 문장500개는 아니다. 누적 신규 초안24,937개, 미작성2,515개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false이며 ROM에 삽입하지 않았다.

500개 전체 source literal과 배틀 외8개 전체 TPL을 읽었다. 배틀0..53의 literal을 분리한 정확한 제어 skeleton을 읽고,54..137의 모든 존재하는 script를 기준0..5와 비교하여 초상화 외 제어 동일성을 확인했다. 분기표138..143은 전체 명령/대상을 따로 읽었다. 원문 ID/source/TPL/payload와 숫자·선택지 order/width/default·명령/페이지/줄/공백을 보존했다. 미니게임71BE98:2:0의 합쳐진 칩 이름 라벨은 임의 분절/번역하지 않고 원문/미작성 분모에 유지했다.

배틀 대상과 거리의 짧은 mmbn45s 라벨38개는 local 초상화 없는 UI라벨로 구별했다. 도주에는 원문 각 내비의 명시 초상화를 유지하며 선택지38개/default0/width8/예 뒤 두 공백/끝 줄바꿈을 보존했다. 성공·실패·도주 금지, 섀도맨/네이팜맨의 길 가로막힘, 썬더맨의 대대손손 수치, 넘버맨의 더듬음, 아쿠아맨 퓨, 플랜트맨 꽃 비유와 포르테의 잔챙이 경멸/목숨을 거두겠다는 의지를 각각 작성했다. 분절 점126개와 결과별18프레임 대기4회는 합치지 않았다. 이미 기준 ROM에서 선택된 록맨/롤 대사는 다시 초안화하거나 변경하지 않았다.

배틀138..143의 checkNaviAll 대상은 source상 offset 불일치와 포르테의 자기 script 이동을 포함한다(예:138의 Bass→138,143의 Bass→143). 저장된 텍스트의 local 초상화와 진입 분기표가 일치한다는 런타임 결론을 내리지 않았다. ‘고쳐 보이는’ 대상이나 앞선 내비 이름으로 원문을 교정하지 않고 실제 소비 경로/미사용 여부를 별도 검토 사항으로 유지했다. 번역용 문맥과 정상 플레이 도달 증거를 구별하며 검증용 넘버맨 대사/초상화 덮어쓰기 없음.

미니게임의 1체 삭제마다 수1 감소/0클리어,금이 간 큐브의 다음 턴 파괴와 바이러스의 다음 턴 공격,대미지3회 강제 종료,동일 칩3장 PA와 선 아래 전부 삭제를 구별했다. 한 번에3체 이상 삭제→카운트 봄,1턴마다1 감소/0폭발,아래3줄이 아이스 큐브로만 채워지면9개 파괴/보너스도 보존했다. 숫자를 HP량으로 오해하거나 설명을 새 효과 구현으로 바꾸지 않았다. 점수 보상의 printBuffer3/checkGiveZenny4294967295·20프레임 대기를 그대로 유지했다. flag6452/6401/6402 및 Navi19의 편지→script7 조건,6의 감염 단정과7의 감염 추정,삭제/설명 선택지10개·spacePx16/24·disableB를 구별했다. 프로그램이라는 자기소개만으로 특정 내비 초상화를 임의 확정하지 않았다.

MrProgGold의 버스팅 튜토리얼은 십자 버튼으로 내비를 직접 조작하지 않음/간단한 지시 후 자동 이동,목표/칸 거리와 ‘되도록’ 간격 유지,작전 화면의 R설명/L도주와 배틀 중 R/L장비 공격을 구별했다. 커스텀 게이지 시간 충전/노랑→파랑→가득 찬 빨강,시작 노랑/스탠더드·메가·기가 문턱/폴더에서 무작위 칩 선택,좌우로 칩 선택/A전송/B섞기의 게이지 비용과 위로 목표·아래로 간격 변경을 각각 작성했다. 원문 버튼·색·줄·페이지·위쪽 설명창 좌표는 변경하지 않았다. 설명 대사 작성은 실제 조작 경로나 게이지 동작 검증을 대신하지 않는다.

에브리데이 대회는 item7 동적 조각상 감상과09/13/16/20시 시간 분기,flagNavi1906→4 종료 안내,숨김 width8/default0 선택지/취소3,flag7736/callTournament6를 보존했다. 기존 비일본어 AM/PM 시간 literal은 그대로 두었고 마지막 ‘이야’가 포함된 시간 페이지의 숫자/범위를 유지했다. 금/플래티넘과 대비되는 세계 공통의 강함,성급한 참가자 반응·우승 후 재참가를 구별했다. 실제 대회·보상/저장 실행 없음.

순찰 노래/인터넷6 이상 없음,쇼핑 Pink/흥정 Orange→Purple 상인/구매 Purplegirl/수요일만 여자애가 되고 싶다는 Yellow의 화자를 나눴다. 달리며 순찰하여 범죄 예방·체력UP 일석이조와 오늘 나무 속성 불리 안내에 원문에 없는 원인을 추가하지 않았다. Yellow 배틀의 거친 갈비뼈 변명/100만 광년 과장과 영어 섞인 말투/자신감 상실,별도 Yellow 배틀의 오피셜 회피·기합MAX와 기름진 기술/베이비붐 세대/체력 없는 아저씨의 희극을 분리했다. source battle globals24=156/157/162/163 및 상대2/3·7/8/flags1806·7701은 유지했다. 문화적 노래·영어·세대 표현·새 용어와 말투는 인간 의미 검토/승인 전 후보이다.

검증: 전체431개 회귀 검사 PASS(226.164초). py_compile·원문 해시/제어 skeleton·숫자/범위·줄바꿈/공백·BDF 한글 글리프·codec·미선택 보존 PASS. 신규9개 JSON 재생성 일치, 기존426개 번역 자산 SHA와 plan 자산/완료묶음 접두부 보존, 현재435개 초안 자산. 수정이 끝난 번역/도구/plan/test를 고정하여 전체 검사를 실행했으며 실행 중 authored 입력 변경 없음. coverage/worklist 두 번 생성 해시 일치: coverage `6a1ed5af57f2942df27933fc6555f5393f2d816398047fde4c9e142be11d428e`, worklist `f0f41c730e96603797e1f9d6836102bc556ad6d55c5f5570d52a6325d3592d05`.

보수적132px 경고95개 추가, 총3460개다. archive 순서별2/32/40/7/0/3/4/2/5개이며 실제 consumer 최대폭이나 자동 축약 근거가 아니다. 기술 검증은 의미·인간 승인·실제 화면 검증을 대신하지 않는다.

원본 ROM/기준 개발 ROM/catalog SHA는 그대로다. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 전체 초안 작성 후 글꼴·제어·소비 경로·레이아웃·삽입 준비를 검증하고 누적 ROM 적용/실제 화면·저장 회귀로 진행한다. catalog 밖 inline/폰트/이미지·한글 자판/조합/영구 저장·기존save호환·통합 runtime/release는 미완료다. create-kr-patch 스킬의 원문 보호와 초안/승인/삽입/실행 증거 분리를 적용했다.

## 500묶음042 — 대회 시상식·룰렛·포르테전 후 대화·내비별 우승 인터뷰 / NPC

6EAD18(482)/7A6778(4)/7A685C(8)/7A7E1C(5)/7A9954(1)의5개 archive에서 미작성 일본어500 stable literal 초안을 개별 작성했다. 대회 시상/룰렛/포르테전 후 대화/인터뷰482·NPC18이며 UI랭크3/분절 대기 점6개를 포함한다. 유일 문장500개는 아니다. 누적 신규 초안25,437개, 미작성2,015개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false이며 ROM에 삽입하지 않았다.

500개 전체 source literal을 읽고,6EAD18의0..77 제어 skeleton과 비일본어 인접 literal을 확인했다. 인터뷰65..77의 개인정보 미등록 시90..102 fallback은 원문/제어를 문맥 확인용으로 읽었으나 이번 초안에는 포함하지 않았다. NPC4개 전체 TPL을 읽었다. 원문ID/source/TPL/payload·명령·분기/플래그·변수·숫자·페이지/줄/공백은 보존했다. 6EAD18:10:0의 printShortString 뒤 ‘ ヘ’는 실제 의미/소비 용도 미확정으로 번역하지 않고 원문/미작성 분모에 유지한다. 78이후 인터뷰와90이후 fallback은 다음 묶음으로 남기며 완료로 계산하지 않는다.

시상은 Ribitta→MrProgGold→Ribitta 전환과 item2/3/4·flag7727/60프레임 대기를 보존한다. 에브리데이 대회 item19/20 티켓은 해당 전뇌 문1회 열기/1번 플러그아웃 후 다시 닫힘,이미 소지한 경우와 global20의 별도 분기를 구별했다. 정상/언더 룰렛의 A타이밍 안내·textSpeed0/waitHold·global17 보상평가0..3/그 밖,칩buffer1과 이름/상대 내비 삽입을 유지했다. 18..22는17에서 Ribitta를,53..57은52에서 HeelNaviBlack을 계승하는 source jump chain 화자로 기록했으며 local 초상화 표시와 혼동하지 않았다. 랭크5/6/8은 mmbn45s UI라벨이다. 실제 룰렛/상품 지급/진입은 실행하지 않았다.

포르테 패배3→global18의25..47 내비별 답변→48 포르테 위협/HeelNaviBlack 언더 왕 안내를 읽었다. 오퍼레이터의 우정·유대·신뢰와 각 내비의 바람/투지/별/기사도/꽃 비유,섀도맨의 부정 뒤 인정·네이팜맨의 허세·아쿠아맨 퓨·정크맨 더듬음을 나눴다. 38/39는 원문상 MegaMan 초상화와 푸른 불꽃 대사이며 다른 화자로 임의 교정하지 않았다. 포르테47은 오퍼레이터 없이도 싸울 수 있다는 고집,48은 플레이어를 직접 쓰러뜨릴 때까지 살아남으라는 경고다. 이번 대사 검증을 위해 넘버맨 또는 다른 내비 대사/초상화를 덮어쓰지 않았다.

인터뷰65..77은 checkNavi0..12에 대응하는 록맨/롤/거츠/윈드/서치/파이어/썬더/브루스/넘버/메탈/정크/아쿠아/우드와 Ribitta의 명시 초상화 전환을 유지했다. flag7729 set/clear·이름/닉네임/현재내비·음식/짝사랑/학교/취미/꿈/친구/소원/특기/약점과목/방송/싫어하는 사람 삽입과 미등록 fallback 대상을 보존했다. 동적 변수에는 고정 이/가·을/를·와/과 대신 ‘의’·‘하고’·‘에게’ 또는 문맥 표현을 작성했다. 실제 값/경계 공백/연속 literal 흐름/유한 창 배치는 consumer별 재검토가 필요하며 정적 통과만으로 삽입 준비 완료로 보지 않는다.

롤의 짝사랑 폭로와 사과,거츠의 감격/학교 라이벌,윈드의 바람 은유와 휴식 권유,서치의 인터뷰어에게 무뚝뚝/오퍼레이터에게 존대와 꿈,파이어의 친한 강적/부담감 부정,썬더의 엄격함 속 소원 배려를 구별했다. 브루스는 잘하는/못하는 과목과 새로운 임무,넘버는 두뇌 자랑→내비 교체 위협→허세 철회,메탈은 취미 휴식 뒤 추가 특훈,정크는 짝사랑 상대에 대한 질투와 배틀 중 독점,아쿠아는 좋아하는 방송 시간,우드는 자연/대지와 자랑을 각각 작성했다. 서치69와 넘버73의 분절 점3개/30프레임 대기 각3회는 합치지 않았다. 희극·인물 호칭/말투·새 용어는 인간 의미 검토/승인 전 후보이다.

HeelNaviBlack NPC는 잠재 실력 평가와 쓰레기 심부름에서 벗어나려는 수련 희망을 나눴다. source checkNetTime18:00..28:59의 upperHour28은 정상화하지 않고 원문 이상점/consumer 검토 사항으로 남겼다. Orangegirl/Pink/Yellow의 쇼핑/서브칩 비축/수요일 레이디스 데이·맨즈 데이 희망과 MrProgGreen 주말 휴식을 별도 화자로 기록했다. NPC 말투만으로 섀도맨이라고 확정하지 않았다.

검증: 전체438개 회귀 검사 PASS(231.576초). 첫 전체438개 검사에서는 UI랭크의 후행 두 공백을 선택지로 가정하던 기존 검사2개가 실패했다(231.964초). 해당 테스트에042의 명시 UI라벨 집합을 추가했으며 번역·원문·초안 작성 도구·plan은 변경하지 않았다. 수정 후 전체438개를 다시 실행했다. py_compile·원문 해시/숫자/줄/공백·BDF 한글 글리프·codec·제어 skeleton·미선택 원문 보존 PASS. 신규5개 JSON 재생성 일치,기존435개 번역 자산 SHA와 plan 자산/완료묶음 접두부 보존,현재440개 초안 자산. 수정 완료한 authored 입력을 고정하여 전체 검사를 실행했다. coverage/worklist 두 번 생성 해시 일치: coverage `4f23ebe506c103c897f858942d7f883c85ffa66e41247bde406c0d323c43901d`,worklist `9df1f3378b8c5c0b7ef1d8367b1c30afc4f8c46ee988a1460bcf9db074275e63`.

보수적132px 경고126개 추가,총3586개다. archive 순서별120/1/1/3/1개이며 실제 consumer 최대폭이나 자동 축약 근거가 아니다. 기술 검증은 의미·인간 승인·실제 화면 검증을 대신하지 않는다.

원본 ROM/기준 개발 ROM/catalog SHA 불변. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 전체 초안 작성 후 글꼴·제어·소비 경로·레이아웃·삽입 준비를 검증하고 누적 ROM 적용/실제 화면·저장 회귀로 진행한다. catalog 밖 inline/폰트/이미지·한글 자판/조합/영구 저장·기존save호환·통합 runtime/release는 미완료다. create-kr-patch 스킬의 원문 보호와 초안/승인/삽입/실행 증거 분리를 적용했다.

### 후속: 500묶음043 — 남은 우승 인터뷰·수련·배틀·칩 강화 (2026-10-12)

정확히500개 stable catalog literal을 개별 작성했다. 6EAD18 인터뷰/프로필 미등록 fallback377,71A37C 메탈맨 수련27,775E90 기존 록맨 배틀29,776198 칩 강화45,7782A8 플러그인5,778C6C 대회명 UI8,7A6A68 닌자풍 NPC7,7A7B74 주말 NPC2다. 유일 문장500개가 아니며 전부 needs_review·development-draft; NON-DISTRIBUTION·release_eligible=false이다. 당시 누적25937개,초안 미작성1515개,자산448개/완료500묶음43개다.

원문500개와 전체 제어 흐름,인터뷰65..85의 미등록 조건/90..110의 호출자 계승을 읽고 수동 작성했다. Ribitta와 스타/섀도/나이트/네이팜/아이스/일렉/플랜트/포르테 전환 및 flag7729를 보존했다.86의 「해냈어」는 원문 실제 Ribitta 초상화 그대로이며 록맨/넘버맨으로 임의 고치지 않았다. 미등록 fallback의 첫 내비 대사는 local portrait와 호출자 계승 근거를 구별했다. 이름/현재 내비/학교/취미/친구/음식 삽입 위치와 고정 받침 조사 회피는 실제 값·경계 공백·연속 출력/layout 검토가 남는다.

스타의 불운한 연애 운세 회피(친구 약속/대청소),섀도의 암살 의뢰(학교/표적 에리어),나이트의 하루3회 음식/규칙적 생활,네이팜의 친구/인터넷 배틀,아이스의 취미/인터넷,일렉의 학교/인터넷 강적을 구별했다. 플랜트는 좋아하는 음식 목욕이라는 희극과 미등록 시 채소 주스 건강 권유를 섞지 않았다. 포르테의 친구/바이러스 비교,넘버의 오퍼레이터 불필요 허세→내비 교체 위협→철회,아쿠아의 식사 시간과 식어 버릴 밥도 구별했다. 말장난/새 말투/용어는 인간 의미 검토 전 후보이며 사용자 승인4649 인사는 다른 기존 기록 그대로 보존했다.

메탈맨은 위아래 이동/B 버스터·길게 눌러 차지/차지 시간에 따른 공격 범위/다가오는 석상 전부 파괴와 휠3개·실수/충돌1개 감소·3번 실수 실패·제니/버그 조각을 부수지 않고 회수하는 조건을 유지했다. 숨긴 선택지6개 width13/8/default0/disableBtrue/설명 반복1을 변경하지 않았다.71A37C:2:0의 숫자 글자표와6EAD18:10:0의 짧은 ヘ는 미작성 분모에 남기며 해결로 계산하지 않았다.

775E90은 넷토의 추가 칩 데이터1턴 대기/넷토 부재 flag7689/도망 성공·실패와 통신 오류·칩 게이트 없이 재시도15/종료16·저장 경고를 유지했다.15/16의 계승 MegaMan과 명시 초상화를 분리했다. buffer0 버그 조각/HP최대 UI와 buffer1 오류 코드를 보호했다.776198은 printChip buffer1 chip0의 화염/물/전기/나무 칩 삽입 제안과 거절/반응을 구별했다. msgClose 뒤의3/7/11/15 최대HP50pts 결과는 system-reward로 기록하고 명시 나이트/포르테50PTS·거츠10PTS와 분리했다. 실제 HP/플래그/배틀 상태를 쓰지 않았다.

총 선택지20/UI라벨10/분절 대기 점15개.30/18프레임 점 출력은 합치지 않았다. 기존 플러그인 flag7710/7711·controlLock·10/10/30대기·chapter0 엄마 문맥과8종 대회명/T라벨,HeelNaviBlack의 유대/닌자 오퍼레이터 및 nettime12:00..28:59 이상점,OfficialNavi의 토너먼트 참석 추측을 보존했다. 기존/레거시 archive의 정상 소비 경로는 실행 검증 전 미확정이다.

검증: 전체445개 회귀 검사 PASS(238.253초). 원문/숫자/토큰/줄바꿈/공백·한글 BDF 글리프/codec·제어 skeleton·미선택 원문 보존 PASS. 신규8개 JSON 재생성 일치,기존440개 번역 자산 SHA와 plan의 자산/완료묶음 접두부 보존. 고정 authored 입력에서 전체 검사를 실행했으며 py_compile PASS. coverage/worklist 두 번 재생성 해시 일치: coverage `e1f072d1670cdedcc56ec71b54e5573946695a68a337e0dc9b03dbe7a1afdcf5`,worklist `b5a840e19b498042b6e21a48ff45c11523df16707c6b252229f3da10cb56aa1a`.

보수적132px 경고96개 추가,총3682개다. 이번 archive 순서별73/1/5/14/1/0/2/0개이며 실제 consumer 최대폭 또는 자동 축약 근거가 아니다. 정적 검증은 의미·인간 승인·실제 화면 검증을 대신하지 않는다.

원본 ROM/기준 개발 ROM/catalog SHA 불변. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 남은 전체 초안 작성 후 consumer·글꼴·레이아웃·제어·삽입 준비 검증과 누적 ROM 적용/화면·저장 회귀로 진행한다. catalog 밖 inline/이미지·한글 자판/조합/영구 저장·기존save호환·통합 runtime/release는 미완료다. create-kr-patch 스킬의 원문 보호/초안·승인·삽입·실행 증거 분리를 적용했다.


## 500묶음044 — 내비 인사·귀환·훈련 결과·메일·일정·대회 잔여 문구

67개 archive에서 미작성 일본어500 stable literal 초안을 개별 작성했다. 내비별 인사/귀환/훈련 결과/메일/일정/대회 격려 및 배틀 결과를 포함하며 유일 문장500개는 아니다. 누적 신규 초안26,437개, 미작성1,015개. needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false이며 ROM 삽입 전이다.

이번 범위: 65E828(3) / 66B8B0(4) / 66F6A0(7) / 66FC98(4) / 670DF4(5) / 67133C(3) / 672124(6) / 675338(7) / 67593C(7) / 676AE4(6) / 677028(4) / 6770B8(17) / 677774(14) / 677C94(10) / 677E58(6) / 67AD3C(7) / 67B3D0(4) / 67C4CC(5) / 67C9FC(3) / 67CB24(1) / 67CED8(14) / 67D44C(9) / 67D5F8(6) / 680370(6) / 6808C4(4) / 681AB8(5) / 681FD4(4) / 682054(28) / 6824B8(1) / 682504(16) / 6827F8(15) / 682D68(9) / 682F44(5) / 685B7C(6) / 68611C(3) / 68787C(4) / 688900(6) / 68BAAC(8) / 68C2CC(4) / 68D3C8(4) / 68D8F8(2) / 68DD4C(1) / 68DD98(20) / 68E7BC(6) / 691994(5) / 691F80(4) / 69303C(6) / 693590(3) / 693778(1) / 6941DC(6) / 696CF4(7) / 697268(4) / 6989B0(2) / 698A2C(14) / 698CB0(1) / 698CFC(56) / 699194(14) / 6996DC(10) / 6998DC(6) / 69C8FC(6) / 69CF44(5) / 69E088(5) / 69E5A8(2) / 69E6BC(1) / 69E708(20) / 69F11C(6) / 6A207C(7).

500개 전체 원문 literal,67개 native 제어 skeleton과 인접 미선택 literal을 읽었다. 숫자/변수/명령/메일·보상/플래그/페이지/줄/공백을 보존했다. 6770B8:0:0,682054:0:0,698A2C:0:0의 임시かりです는 번역하거나 완료 처리하지 않고 원문/미작성 분모에 남겼다. 사용자 승인4649 인사는 변경하지 않았다.

윈드의 바람/풍신의 춤,서치의 생명 위탁/임무/승률99.9·98,파이어의 열기/불꽃,썬더의 긍지/청천벽력,브루스의 정중한 책임감,넘버의 계산,메탈의 주먹/수련,정크의 더듬음/버림받을 두려움,아쿠아의 퓨 말투/눈물,우드의 회복/영양을 문맥별로 구별했다. 새 용어/말투/의미는 인간 검토 전 후보이다.

초상화 없는 quick 알림은 speaker-unestablished로 기록하고 자기소개만으로 runtime 라우팅 또는 초상화를 확정하지 않았다. 682504/68DD98/698CFC/69E708의21..26은 각각 명시ProtoMan/MetalMan/AquaMan/WoodMan이며1..6 quick 알림과 분리했다. 아쿠아40개 분절 음성 literal과30개 waitSkip30을 합치지 않았다. 동적 이름/방송/약속/기타 일정/시간/보상 버퍼는 불변이며 실제 값과 연결된 문법·경계 공백·창 배치는 consumer 검토가 남는다.

미니게임 결과 global5=0..3,HP메모리item33/amount1,제니·버그조각amount4294967295/printBuffer3를 보존했다. 브루스 임무 성공/실패 메일과callProtoManMissionComplete/flags5475·5476·3613,계산 문제집/편지 결과를 구별했다. 메일 수신 소리155/96프레임·flags680/681과 대회 메일/일정 루프를 유지했다. 실제 보상·임무·메일·일정 실행은 하지 않았다.

검증: 전체452개 회귀 검사 PASS(279.745초). 첫452개 검사(280.572초)는 신규 검사2곳의 명령 필드명/global→variable 및 승률 literal ID 오류로 실패했다. 검사 수정 과정의 들여쓰기 오류는 py_compile에서 검출·수정했고,최종 py_compile 후 전체452개를 재실행했다. 번역 초안은 변경하지 않았다. py_compile·원문 해시/숫자/줄/공백·BDF 한글 글리프·codec·제어 skeleton·미선택 원문 보존 PASS. 신규67개 JSON 재생성 일치,기존448개 번역 자산 SHA와 plan 자산/완료묶음 접두부 보존,현재515개 초안 자산. 수정 완료한 authored 입력을 고정하여 전체 검사를 실행했다. coverage/worklist 두 번 생성 해시 일치: coverage `4f190eabf3be140e5cfd8ecc04c08134d999e94196d8241e3203eb00c441963e`,worklist `64912ce2b557499acef5a04deb8a626c23e17717d8e524e5c771eca645f021dd`.

보수적132px 경고33개 추가,총3715개다. 실제 consumer 최대폭이나 자동 축약 근거가 아니다. 정적 검증은 의미·인간 승인·실제 화면 검증을 대신하지 않는다.

원본 ROM/기준 개발 ROM/catalog SHA 불변. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 남은 전체 초안 작성 후 consumer·글꼴·레이아웃·제어·삽입 준비 검증과 누적 ROM 적용/화면·저장 회귀로 진행한다. catalog 밖 inline/이미지·한글 자판/조합/영구 저장·기존save호환·통합 runtime/release는 미완료다. create-kr-patch 스킬의 원문 보호/초안·승인·삽입·실행 증거 분리를 적용했다.

## 500묶음045 — 내비·메일 헤더·일상 NPC 잔여 초안

76개 archive의 미작성 일본어500 stable literal을 개별 작성했다. 내비·메일·폴더366개와 통행/석상/대회/NPC134개이며, 메일 제목·발신자90개와 폴더 라벨1개를 합한 UI 라벨91개, 플레이어 선택지4개를 포함한다. 누적 신규 초안26,937개, 미작성515개. 모든 신규 자산은 needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false이며 ROM 삽입 전이다.

500개 원문과76개 native 제어 skeleton, 인접 미선택 literal을 읽었다. 스타맨의 백성/흑성/회색 별 승패 비유와6등성, 플랜트맨의6할 개화, 섀도맨의 주문과 심두멸각, 나이트맨의 구호, 네이팜맨의 거친 말투, 아이스맨의 존대 등을 문맥별 후보로 작성했다. 새 용어·말장난·문화적 표현의 의미/말투 승인은 남는다.

명시 초상화와 초상화 없는 quick 알림을 구별했다. 6DE2C8:31은 script0의 점프 경로를 통해 SciLabMan 문맥을 상속하며 직접 초상화 명령이 있는 것으로 기록하지 않았다. 33의 화자는 미확정이다. 메일 헤더/폴더 라벨은 대사가 아니다. 동적 내비명/대회명과 연결되는 등록 문장은 받침에 의존하지 않는 후보로 작성하되 실제 값·배치 확인은 남는다. 자기소개만으로 실제 내비 라우팅을 증명하지 않는다.

HP item33/amount1, global variable5=0..3, 보상 sentinel4294967295/printBuffer3, 메일 소리155/96프레임 및 플래그, 일정/시간 루프를 보존했다. 폴더의 동일 칩3장·동일 메가/기가 각1장과 총 메가5장/기가1장을 구별했다. gate의 원문100+90 분절과 native190 조건, 토너먼트7 및9/13/16/20시 조건, 선택지 폭8/기본0과 기존 숫자·공백·줄·명령은 변경하지 않았다. NPC의 가상 사이버법123조는 현실 법률 설명이 아니며, 소문과 확정 사실도 구별했다.

6BC0C8:0:0의 임시かりです, 79C240:1:0의 バグピーストレーダー(かり), 79C8D8:0:0의 SPトレーダー(かり)는 미작성 분모에 남겼다. 입력 문자표·디버그/임시 구조를 정상 대사로 간주하거나 완료 처리하지 않는다.

검증: 전체459개 회귀 검사 PASS(327.052초). py_compile, 원문 해시·숫자·토큰·줄·경계 공백·BDF 한글 글리프/codec·제어 skeleton·미선택 원문 보존 PASS. 신규76개 JSON 재생성 일치, 기존515개 자산 SHA와 plan 자산/완료묶음 접두부 보존. 현재591개 자산·45개500묶음이다. 새 메타데이터의 메일 라벨 개수 설명을90메일+1폴더로 정정하면서500개 번역 unit은 그대로 유지했다. coverage/worklist 두 번 생성 해시 일치: coverage `9c0a4f39258f21fe12e8e47ff9ed71505d18b04b152b2be2e15e30d700f6d97f`, worklist `8be667afc1a3ab8bd0bdbc556e38e56252accacbece07640f364599aa0aee5db`.

보수적132px 배치 경고82개 추가, 총3797개다. 실제 consumer 최대폭/자동 축약 근거가 아니다. 정적 검증은 의미·인간 승인·실제 화면 검증을 대신하지 않는다.

원본 ROM/기준 개발 ROM/catalog SHA 불변. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 남은 초안 작성 후 consumer·글꼴·레이아웃·삽입 준비 검증과 누적 ROM 적용/실제 화면·저장 회귀로 진행한다. catalog 밖 inline/이미지와 한글 자판/조합/영구 저장/기존save호환/통합 runtime/release는 미완료다. create-kr-patch 스킬의 원문 보호와 초안·승인·삽입·실행 증거 분리를 적용했다.

## 남은515개 정리 — 500묶음046 + 최종047(13개)

요청 범위515 stable literal 중513개를 개별 번역 초안으로 작성했다. 046은102개 archive/500개, 최종047은8개 archive/13개이다. 누적 신규 초안27,450개, 미작성2개. 남은2개는 `6368E8:2:0` 히라가나와 `6368E8:3:0` 가타카나 입력키 배열이다. 미번역 분모에서 제외하거나 번역 완료로 바꾸지 않았다. `analysis/remaining515_reconciliation_v1.json`에513개 권위 자산과2개 구조 항목을 연결했다. 모든 신규 초안 needs_review / development-draft / NON-DISTRIBUTION / release_eligible=false, ROM 삽입 전이다.

두 원문은 입력키 문자 배열이며 인덱스/선택값 대응과 표시·레코드를 함께 검증해야 한다. 기존40자모/90셀 후보·페이지 그래픽·자동 조합 로직은 별도의 구조이다. 라틴/기호 표4:0의 가운데점 표기 후보도 구조/입력 consumer 검토 전이며 문자 입력 완료로 간주하지 않는다. 두 배열을 한국어 문장이나 자모 문자열로 치환하는 것만으로 입력/편집/확정/재표시/저장까지 연결되지 않는다. 사용자가 승인한 자동 조합 방향을 유지하며 자판 통합 과제로 남겼다. 스킬 name-entry 지침에 따라 문자 선택 표와 표시/레코드/저장 표면을 분리했다. 후보 plan SHA `a97117e3d20f15c433bf70b634a87cd5e5f2ae59f5bb3003a08a79ea74434a1b`, page graphics report SHA `0adb1322584f4e811d990b252ae92d647fcbe4d1d3f3ae39028b1f3295d7fcee`를 기록했다.

513개 원문과110개 archive의 선택 스크립트 전체 제어 skeleton을 읽고, 반복 WAIT_FALSE/CLEAR만 읽기 전용 보기에서 정확한 동등 템플릿으로 줄였다. PET/성별·나이·직업·날짜/대회·요일/존칭/프로필 및 내부 축약 라벨, 게시판 작성자/제목 결합 행, PA 재료 표, 아이템명, 내비별 어둠 지역 경고, NPC 순찰/수업/회의/쇼핑, 힐·섀도맨 배틀, 임시/내부 오류 보고를 구별했다. 원문 숫자·토큰·모든 줄/경계 공백·명령·초상화/숨김·분기를 보존했다. 새 인명·존칭·문화 행사·축약 라벨/역할은 인간 검토 전 후보다. 칩명 건델솔/히트샷/일렉쇼크 등은 기존 라이브러리 후보와 대조했다.

768800은 MrProgGreen/Lan 초상화의 레거시 소울 유니존 튜토리얼이다. 칩1장 제물, 레귤러 칩 사용 금지, 같은 소울은 배틀당 한 번,3턴 유지, 무속성/지형 파괴 +30과 B버튼 조작을 보존했다. 문자열 존재가 EXE4.5의 실제 소울 유니존 기능을 증명하지 않는다. 7794EC의 개발용 아이템 지급/회수·전체 칩·메일·홈페이지·대회/플래그·제니 지급 명령은 바꾸거나 실행하지 않았다. 임시 표시는 번역에서도 명시했다. debug/레거시 문구를 정상 진행 기능으로 바꾸지 않았다.

7B1C78의 오피셜↔견습 내비 전환,7C416C의 프로그램 패배→나이트맨 승리 초상화를 구별했다. 7C9C44/7CAF40은 로컬 초상화가 없어 화자를 미확정으로 유지한다. 섀도맨 Navi16 특수 분기와 선택지 폭13/11, 힐 내비 폭9, 배틀 globals/flags1806/7701을 보존했다. 일반 대사 번역은 플레이어 또는 넘버맨의 데이터/초상화를 바꾸는 작업이 아니다.

검증: 첫 전체465개 검사(394.227초)는9곳의 이전 미작성 상태/새 UI 라벨 분류 검사에서 실패했다. 초안 문구는 바꾸지 않고 검토 대기·화자 미확정·ROM 미반영 의미를 유지하도록 기존 검사를 갱신했으며, py_compile 후 전체465개를 재실행해 PASS(394.323초)를 확인했다. py_compile·원문/TPL/payload 해시·숫자/토큰/줄/공백·BDF 한글 글리프와 codec·제어 skeleton·미선택 원문 보존 PASS. 신규110개 JSON 재생성 일치, 기존591개 번역 자산 SHA와 plan 자산/45묶음 접두부 보존. 현재701개 자산·46개500묶음+최종13개. coverage/worklist 두 번 생성 해시 일치: coverage `c822fc69a9e321d8dec08ee1f9eb7ece89f5768d55ef8450d898d8ebe7f07b69`, worklist `8aef744acbd380f764f5454f5d46674c95463904c7fd0cf4c913d22ca88a515a`.

132px 보수적 배치 경고144개 추가, 총3941개다. 게시판/성별·직업 등 결합 표와 PA 재료의 byte/cell 경계·가변 문자열 문법·실제 consumer 폭은 별도 확인이 필요하다. 원문 경계 공백 보존이나 폰트 검사만으로 고정 필드 재삽입/정상 화면을 승인하지 않았다. 자동 축약/일괄 prose 치환 없음.

원본 ROM/기준 개발 ROM/catalog SHA 불변. ROM·세이브·에뮬레이터·이미지·자판 변경 및 이번 화면 검증 없음. 아직 일반 번역의 의미·표현 승인,2개 입력 구조와 전체 consumer·글꼴·레이아웃·삽입 준비 및 누적 ROM/화면·저장 회귀가 남아 있어 전체 완료/배포를 선언하지 않는다. create-kr-patch 스킬의 원문 보호와 초안·승인·구조/삽입·런타임 증거 분리를 적용했다.

`translations/full_translation_first_plan.json`에 기준 ROM/목록 해시와 이번 요청 순서를 고정했다. `tools/prepare_translation_first.py`는 기존 번역 JSON 후보와 신규 작성 자산을 구분해 `analysis/translation_first_v1/worklist.json` 및 `coverage.json`을 생성한다. 이 목록은 읽기 전용 파생물이며 직접 번역을 편집하는 곳이 아니다.

원본 ROM/TPL/payload 해시, ID·source·기존 선택 상태, 숫자·범위·토큰, 줄 수·마지막 줄바꿈, 한글 BDF 글리프·codec, literal 교체 후 제어 skeleton 및 미선택 원문 보존 검사를 통과했다. 이전 회귀 테스트459개 통과(327.052초); 현행 전체465개 통과(394.323초). 기존 ROM과 원본 ROM SHA가 그대로임을 확인했다. 초안 JSON 재생성은 기존 내용과 일치할 때만 허용한다.

132px를 기준으로 한 보수적 advance 계산에서 **3941개 literal**이 배치 재검토 대상으로 표시됐다(저장5/토너먼트73/임무25/메일30/스타맨5/골드게시판31/배틀게시판51/광장20/미스터리데이터6/오피셜예선37/블랙워크스동생30/형43/오피셜접수33/일반배틀12/언더배틀A7/언더상점5/언더배틀B11/언더배틀C14/언더접수12/고난도통행A16/B29/개인정보2/비밀특훈1/대회장3/공장열정1/공장부품1/수련배틀10/장난감상점4/라디오7/골프잔디1/골프배틀12/골프상점3/홈페이지바닥3/자동차제어4/핑크배틀1/홈페이지무늬2/라이벌배틀7/제초1/세척2/나방배틀6/물총1/추운대회장5/공장배틀5/정지프로그램1/힐배틀6/일반네이팜시험16/스테레오1/보라핑크배틀6/오르간대회장9/쓰러진나비1/어둠배틀6/윈드맨3/브루스현장22/롤3/썬더맨1/우드맨2/스타맨6/연습재시도37/연습성공20/셰이드맨관조우25/셰이드맨승리귀환32/레이저맨조우15/레이저맨전후41/포르테조우24/포르테승리50/개인정보관리31/크레딧41/미니게임결과3/일정알림2/프로필질문19/롤메뉴잔여3/프로필잔여B10/대회격려1/배틀결과1/윈드맨메뉴잔여9/500묶음윈드장비2/서치장비5/브루스장비5/진행힌트1/대회1/500묶음002나이트장비5/아이스장비3/진행힌트1/대회1/500묶음003메뉴14/훈련1/500묶음004메뉴8/진행13/500묶음005진행8/알림2/훈련3/500묶음006일정메뉴46/대회1/500묶음007일정메뉴36/인사2/500묶음008개인정보·칩24/메뉴5/짧은대사1/500묶음009개인정보24/메일14/대회2/500묶음010개인정보30/알림2/대회5/500묶음011개인정보44/임무훈련2/일정1/500묶음012개인정보37/일정1/500묶음013개인정보38/메뉴11/훈련4/대회2/500묶음014개인정보후속37/힌트2/훈련4/대회5/500묶음015후속28/의뢰43/알림4/대회8/일정1/500묶음016메일함18/군임무28/파괴임무6/500묶음017서치임무·훈련67/500묶음018윈드31·개인정보후속16/500묶음019별개인정보13·주의안내1/500묶음020거츠18·넘버16·주의1/500묶음021주먹24·거친12·통행6/500묶음022기사11·불꽃11·급식0/500묶음023닌자19·저격6·금요일11/500묶음024나무19·얼음12·트레이더16/500묶음025정크12·전기24·일상10·토요일13/500묶음026존대19·물19·인터넷1NPC18·평일NPC6/500묶음027전기질문11·존대질문7·물질문12·언더게시판25/500묶음028일반상점40·힐상점40·시간대NPC21·잡담게시판29·서치주의1/500묶음029보라상점40·버그조각교환33·목요일NPC29·잠금문/쓰레기13/500묶음030네이팜22·섀도78·인터넷7NPC16/500묶음031나이트27·포르테17·통신44·NPC1/500묶음032골드70·실버20·금요일NPC6/500묶음033견습/인터넷2 40·인터넷6 21·플러그아웃15·게시판28·인터넷2NPC8/500묶음034통신메뉴63·폴더0·인터넷2NPC14/500묶음035통신메뉴28·토요일광장NPC15/500묶음036전체142/500묶음037전체92/500묶음038전체78/500묶음039전체67/500묶음040전체108/500묶음041전체95/500묶음042전체126/500묶음043전체96/500묶음044전체33/500묶음045전체82/500묶음046전체137/최종047전체7). 실제 consumer별 예산을 확인한 결과가 아니므로 자동 축약·재배치하지 않았다. 변수 이름 길이, 선택지 폭, 줄 끝과 실제 표시를 검증한 뒤 적용해야 한다. 이 초안은 아직 삽입 준비 완료가 아니다.

저장 SearchMan의 완료 감탄사 실제 원문은 `コンプリート`; 초안 `완료!`와 뒤의 저장 완료 문장을 구분한다. 자산 semantic_review의 `完了` 표기는 설명 메타데이터의 오기로 실제 source 필드는 보존되어 있다. 새 기술명·케로·언더 표기와 ShadowMan 주문의 음역, KendoMan 반복 연습 표현, JunkMan 로봇 말투는 검토가 남는다.

## 다음 작업과 범위 한계

남은2개 입력키 배열은 한글 자동 조합의 selector·페이지·편집/확정 레코드·재표시·저장 구조를 함께 통합/검증한다. 일반 문자열513개는 초안이 갖춰졌으나 표 형태 consumer와 변수 문법/폰트/레이아웃·삽입 준비·의미 검토는 남는다. 입력 글자판과 내부 디버그 라벨은 일반 문장이 아니므로 실제 consumer를 확인하기 전 임의 번역하거나 완료 목록에서 제외하지 않는다. 732 archive 밖의 inline·폰트·이미지 글자 전체가 완전 조사됐다는 주장은 하지 않는다.

전체 초안이 갖춰진 뒤 글꼴·포인터·변수·배치·삽입 검증을 거쳐 ROM에 적용한다. 이후 실제 화면과 저장 회귀를 검증한다. 기존 런타임 기준과 QA 저장 파일은 보존하며, 저장 초기화 실행 등 파괴적 검증은 이번 작업에 포함하지 않는다. 실제 한글 자판 hook·저장 호환·이전 이미지 및 전체 배포 검증도 미완료 상태다.

원본 SHA256: `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
유지한 개발 ROM: `poc/output/exe45_ko_development_save_initialize_v1.gba`, SHA256 `906f374acaabe9a37c70fddcae364f07c55545ae1d81b57953d727bb881415be`.

적용 스킬 `create-kr-patch`: 원문·제어 데이터 보호, 초안/승인/삽입/런타임 증거 분리, 불명확한 구조 항목을 미해결로 유지하는 원칙을 적용했다.

### 2026-10-12 입력 배열 후속

`6368E8:2:0`/`6368E8:3:0` 두 kana 배열에 대해 한글 자동 조합용 구조 대체 후보를
`hangul_keyboard_v1/kana_replacement/report.json`에 기록했다. 각 페이지40자모/50비활성 selector와
보호 영역을 유지한 tile/map 자산 및 별도 action shim이 있다.
`cpu_kana_replacement/report.json`은 양쪽 페이지와 페이지 간 조합·undo 경로의 CPU 증거다.
상세 조건과 미해결은 `HANGUL_KEYBOARD_HANDOFF.md` 2026-10-12절을 따른다.
일반 번역 초안27,450/구조 미해결2의 분모와 상태는 유지한다. ROM·save·실제 화면 미변경이다.

후속: `cpu_kana_frame/report.json`에서 두 kana 페이지의 커서 skip 보정 및 native state12
입력→페이지/편집 glyph 전송→VRAM 소비 경로를 CPU 연결했다. 방향키/A/B로80자모 칸 도달,
R/L 페이지 전환을 포함한 복합 자모 조합/undo와2,367 frame 호출 PASS.
이는 CPU fixture 증거이며 ROM 설치·실제 화면·저장 지원 완료가 아니다. 상세 범위/다음 조건은
`HANGUL_KEYBOARD_HANDOFF.md`의 두 페이지 native 커서·입력·그림 전송 경로 절을 따른다.

후속: `keyboard_labels/report.json`에 세 페이지 기능 버튼18개 한글 후보와 native00 공백 키를 기록했다.
`cpu_keyboard_labels/report.json`: 3,231 native state12 CPU frames, 공백 경계855/조합9조건 PASS.
표시 후보와 실제 공간/입력 동작을 함께 검증했으나 native 확정/저장·실제 화면·인간 가독성 승인은 미완료다.
일반 초안27,450/구조 미해결2 유지. 상세 범위는 HANGUL_KEYBOARD_HANDOFF의 기능 버튼18개 절을 따른다.

후속: `latin_input/report.json`에 원본75token→90칸 중 영문26/숫자10/기호20 active와34 inactive 후보를
기록했다. 원본 picker75좌표 및 native skip graph를 검증했고 `cpu_latin_input/report.json`에서
5,389 native state12 CPU frames, 모든칸360/길이경계855/조합112/방향키56칸 선택을 통과했다.
기존 한글·공백5mode 회귀도 PASS. 모든 페이지 입력 CPU 연결은 ROM 설치·실제 화면·저장 지원 완료가 아니다.
일반 초안27,450/구조 미해결2 및 원본·개발ROM·사용자 save 유지. 상세 조건/다음 단계는
HANGUL_KEYBOARD_HANDOFF의 영문·숫자·기호 실제 선택 경로 절을 따른다.

## 2026-10-12 전체 ROM 통합 사전 검사

`tools/report_full_rom_integration.py` 및 scope 회귀 tests5개를 추가했다.
`full_rom_integration_v1/report.json`은 전체 초안27,450개 원문/제어/문자 검사와
현재 baseline manifest/registry/도구/후보 해시를 확인한 결과다.
초안 자산701개는 서로 다른660개 아카이브를 대상으로 한다(701개 아카이브가 아님).
현재 등록60개: 등록 밖26,586개, 등록 안이지만 선택 범위 밖864개.
새 초안 중 현재 빌드 선택 범위로 직접 적용 가능한 항목은0개다.
132px 모델의3,941개 경고는 미확정 소비자의 실제 clipping 증거가 아니다.
구조 미해결2개 및 소비자/포인터/레이아웃 등록이 남아 build_ready=false이다.

원본 writer에 F9FC 직접 저장하는 반례를 재검증했다:11172음절 중87개 잘림,
네 글자 입력에서10byte stride를8byte 초과한다. 이는 조건부 F8 versioned 후보의
실패 판정이 아니라 원본 writer 그대로 사용하는 통합을 거부하는 증거다.
한글 전체 저장/읽기/초기값/list/prefill/호환 및 RAM/IRQ 통합은 미완료다.
새 ROM은 생성/적용하지 않았다. 원본과 기준 ROM 해시 유지, 도구 py_compile/tests5 PASS.

실제 에뮬레이터는 **기존 기준 ROM만** 격리 coldboot하여 한글 `처음부터` 메뉴를 확인했다.
증거: `poc/runtime/full-rom-integration-baseline-v1/README.md` 및 PNG3장.
새 번역/자동 조합 자판 통합 실행 또는 save/reset/fresh-load 테스트가 아니다.

후속: 사용자는 저장 지원 통합을 계속 보완하도록 요청했다(저장 차단 시험 ROM 아님).
`cpu_calendar_versioned_prefill/report.json`에 native getter/default/prefill와 조건부 F8
reader를 CPU 연결했다.11,172음절을 세 슬롯 emitted writer로 저장 후 HOST 기록/pool
재작성 없이 읽는11,172왕복 경로,기존 문자484종,손상9/NULL1/필터9을 검사했다.
11,680 prefill경로/33,516 writer/45,196 whole-EWRAM 검사 PASS,실제 ROM 적용은 false.
전체 사전 검사 도구가 이 CPU 보고서 및 의존성 해시도 검증한다. 오류 UI/다른 소비자/
자판 확정 연결/메모리 배치/실제 저장 검증은 남아 있다. 번역27,450/구조미해결2 및
현재 빌드 범위 밖 초안 상태는 유지한다. 상세 범위는 HANGUL_KEYBOARD_HANDOFF 마지막 절.

후속:33334 읽기 경계는 직접 편집 진입이 아니라 native33100 일정 목록 초기화에서
호출됨을 확인했다. `cpu_calendar_prefill_guard/report.json`에서 실패가 native330C6
호출부까지 전달되어 제목/선택 초기화를 건너뛰고 기존 취소 반환2·오류음 요청으로
종료되는 후보를181경로에서 검증했다. 손상·NULL 거부26,보호 없는 실패 전진 반례1,
RAM/160byte stack PASS. native30F0C 부모의 취소 반환 소비도 이미 초기화된 substate4
fixture로 연결했다. 실제 ROM/화면/소리/부모 첫 진입·재진입/세이브 테스트는 아니다.
일반 번역27,450/구조미해결2 및 ROM integration=false 유지. 상세 제한/다음 단계는
HANGUL_KEYBOARD_HANDOFF의 prefill 실패 전달 절을 따른다.

후속: `bench_calendar_prefill_guard.py --reentry`에서 native 첫 진입,count,UI 초기화
요청,빈 목록 default 및 오류 후 연속 재호출을 연결했다.245경로/263 whole-EWRAM PASS,
18회 실패→재실패→emitted writer로record 수정→성공 재호출에서 HOST 기록/pool/UI/
parent/meta 재작성 없음. BIOS UI16byte clear 및graphics/audio 서비스는 modeled.
빈/전부 삭제된 목록4경로도 원본 default 분기 유지. 실제 메뉴 재선택/ROM/세이브 검증
아님. 일반 번역27,450/구조미해결2/ROM integration=false 유지. 상세 제한/다음 경계는
HANGUL_KEYBOARD_HANDOFF의 첫 진입·재호출 절을 따른다.
