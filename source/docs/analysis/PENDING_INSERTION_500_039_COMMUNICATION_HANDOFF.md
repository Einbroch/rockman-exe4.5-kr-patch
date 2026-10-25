# 039 통신 안내500 — source/CPU/원본경계 준비 완료, 아직 ROM 미반영

## 현재 권위와 결과

- 현재 권위는 `pending_insertion_500_039_communication_words_v1/batch_status.json`. **현재 ROM은038/20,122ID**, SHA `97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b`. 새039 ROM 적용0/패키지0/모든 자체명령·Mesen 종료/사용자 mGBA·원본·저장 불변.
- 정확500 미반영 정규초안 /372script /17개 통신 대전 안내 archive 선정. source original 전체 byte roundtrip, target semantic/control/binary 왕복, 미선택source script 보존, 제어명령/숫자/기존한글 문구 보존, 실제038 글꼴310개 확인 PASS. source-only compiler 결과를 제품 ROM 적용으로 세지 말것.
- `selection.json` SHA `966a22eca30229b56984dead96e05d4c71bf0f3a8e464225432ea9ae3bdb1c08`; `verification_v1.json` SHA `c838e808f881b49a936fa218c9b73ddefb09982098c426bebf95200934918576`. ROM 미반영정규초안 **10,424에 이500 포함**. 나머지 미선정9,924는 실제ROM pending 감소가 아니다. 전체게임/이미지 잔여수도 아니다.
- 최종묶음은 **기존 어절 단위 LF/space 규칙만 사용**, 새 음절내 줄바꿈0/새문구작성0/페이지·wait명령 변화0. source-only 단위 전체는 needs_review/NON-DISTRIBUTION. 처음 검토한 음절내줄바꿈12개 포함 대안은 **비선택 이력**으로보존했다. 최종권위 `communication_words_v1`를쓰고 `communication_source_v1`와혼동금지.

## 새 소비자와 원본 실행 증거

- 본문은 **통신 대전 모드/설정 안내**다. 초기 `profile` 임시분류는 source전체의 VS Real Operation/EXE4, single/triple, Chip Gate 문구로 정정. 이름에profile이남은 geometry분석도구는이력에서파생했지만 operator-profile질문으로 해석하지말것. **mmbn45s 고정셀 메뉴 라벨은 이500 대상이 아님**/여전히일본어.
- 원본 loader `080448C8`: 현재내비 getter→`080448E0`의23항목/21고유압축asset→LZ BL`080448D6`→공유RAM`02024000`. 원본literal`4493C`는 loader destination과reader root가 **공유**하므로 ROM주소로바꾸면안된다. RAM여유/재압축성장수용성미증명; 계획은원본LZ/RAM유지+readonlyROMclone선택.
- 원본 reader `080448BC`/BL`080448C2`→helper`0804F7B6`(outer LR`080448C7`)→BL`0804F7B8`→공통`0804FB4C`(inner LR`0804F7BD`). helper는 `{r4,r5,r6,r7,lr}`를push해서 공통entry원래SP+16에 `448C7` 저장. 공통초기화뒤 원본8byte preset copy도 유지해야한다. **4F7B6에서 분석을멈추고4FB4C를안거친다는초기설명은오류**다. 기존038의세typeddomain은root024000과일치하지않아정상fallback한다.
- 실제 자체038 normal입력 v1..v8에서 통신메뉴진입. v7: source`6F56B8` 원본1723byte 전체LZ→RAM검증. v8: 실제 script16 공통entry innerLR/저장outerLR 위값일치, F0001회/EDFF205회, origin92/110, 소비시점까지 원본RAM동일, B취소→PET대사로복귀. 별칭/게임RAM쓰기/PC·호출인자강제0. `baseline_boundary_v2.json` SHA `0761e337854b4a824bb5ec64c4c42bc86fd08ae583e3fd38d7a09b905efa09d4`. **038 일본어 원본경로 증거**이지039 한글실행증거아님.
- v7 checkpoint는원본통신첫로컬메뉴(동일result쌍). source6F56B8는내비0/13/14가공유하므로 payload만보고 개별내비ID를단정금지. **038 state를039에사용금지**. source컨트롤입력recipe만참고하고039자체coldboot에서진행할것. 039직접PET통신진입이가능하면불필요한전체field16재현을의무화하지말고변경영향범위로정할것.
- 초기v1..v6의commcall0은실제jackout기본No/나비프로필자발대화/장비확인등다른메뉴였음. 주소부재나통신미지원으로해석금지. 화면/PET대사 원본script65B9E8의형제질문은자체normalplay에서No를선택해닫았고user저장과무관하다. v7/8의정상경계가확정됐으니그이전추측동작을반복하지말것.

## Native 제어명령 CPU

- `native_controls_cpu_v1.json` SHA `cb32a06ed6dd0a889c9e2ce18ad1c6cc9f22df856539868a7a3d96597e0c2c31`. **768 RAM/readonlyROM쌍**: F000 zero-speed와EDFF visible-page hold의draw/width handler, 실제flag/timer helper 전부 native실행/모델0.
- F000: timer3byte0/contextflag0x800/advance3/continue1. EDFF: stream/페이지geometry유지/contextwait1+외부status8/return0. width는3/4advance/context·status불변. 이 고정 source/038 code범위의 명령인터페이스증거이며 새selector ABI/GBA성능/네트워크결과 증거아님.
- ordinary `pet_quick_capacity.py`는바꾸지않았다. 새sourcegeometry `profile_quick_geometry039_v1.py`가 **원래 zero-speed/화면을유지한EDFF홀드**를별도분석한다. ordinaryquick validator를느슨하게만들거나EDFF를keyWait/clear/end로바꾸지말것. 외부메뉴와한글3row/동적옵션중첩·입력은039실행에서추가검증필요.

## 다음 작업 — 제품 연결

1. 최종500 source/canonical/명시LF입력을 registry로등록. 새17owner에기존compiledowner/carry0인지다시binding확인. source통신21asset의full-native alias/prefix모호성 확인. 압축데이터/23 source포인터는그대로유지.
2. 기존4FB4C composedstub over038 체인에 **별도통신typedguard**를정밀연결하는방향이낮은변경비용이다: root024000 +innerLR4F7BD +원래saved outerLR448C7, unsignedscriptbounds를데이터읽기전에확인. 현재세fieldselector의scene조건을전역완화하거나rawROM/다른공유024000사용자를통째로허용하지말것. 원래helper4F7B6/8bytepreset/source448BC/LZ를그대로두는방법을먼저검토.
3. 실제outer/helper/common 호출stack의모든유효script 및wrongroot/innerLR/outerLR/u8script/nativebyte거부/구raw·fieldfallback/레지스터·stack·context·쓰기범위 CPU. sourceinitialization의216clear/8copy를모델하면그정확범위와限界를명시. ARMv4T 최종배치왕복/전체fixture현재입력동일성 확인.
4. **원본8MiB부터 누적039 primary/repro**.038wholeimagegate·old644consumer 및기존문구/미선택bytes를보존하고 신규500만증가. 사전ExpectedWrites/단일composedstub/append의전체차이검증. 이전ROM파일을primary입력으로패치하지말고비교기준으로만사용. parent wholeimagegate는정확038투영등검증된composition으로보존/삭제금지.
5. 실제039출력audit후 own039coldboot/PET 통신로컬메뉴→새help/font/OBJ/pixels/즉시표시·hold/위아래선택·페이지·B복귀/원래fixed-cell라벨미변경 확인. 실제링크대전/파트너접속은이로컬검사와별도범위. 네트워크·실기·오디오·전체500화면이나사람승인으로과장금지.

## 보존한 실패/정정

- 첫geometry ordinaryquick0후보는textSpeed/visiblehold미지원이정확히원인. 별도source-model로664후보/초기500을확보했지만12음절줄바꿈대안은비선택. 최종wordonly651후보에서500선정/372script/17archive.
- compiler_v1은PREFIX tuple의JSON배열표현차이를직접Python비교해서원본컴파일전에거부. v2는JSON표현만정규화/필드삭제0, 실패폴더/도구보존. 최종wordcompiler는같은보호규칙+softbreak0 강제.
- baselineverifier_v1의Windows경로suffix표현오류는v2에서slash표현만정규화;모든exacthash/동일ROM/state edge보호유지. 검사실패가제품ROM결함이라는뜻은아님.
- 한글commit/save/redisplay·일본어자판·지역명·다른이미지·전체게임/사람/실기/오디오未완료. 사용자에게패치를만들어달라는새요청이오기전 BPS/xdelta/ZIP 생성금지.
