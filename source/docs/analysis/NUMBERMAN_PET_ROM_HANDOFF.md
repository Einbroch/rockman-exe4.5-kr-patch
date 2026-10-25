# 넘버맨 PET 메뉴 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 결과와 번역 범위

`poc/output/exe45_ko_development_numberman_pet_v1.gba`
SHA256 `f590cc6fd38556ba85ca3b92101987019142b091d452b3485862feb79eb464f5`,11,074,572bytes.
추가44literal,누적1,196선택 텍스트 /15기존 그래픽 /23선택·709미선택 archive. 전체 완역률이 아니다.
6873F4의22slots 중16literal scripts 전체44단위와6nonliteral slots를 구분한다.
script1 대기 질문,2..8 메뉴 진입 질문/예/아니요,10..16 재진입 질문/예/아니요,20 대화중단 반응이다.
대회·인터넷 플러그인·장비 편집·데이터 라이브러리·메일·통신 대전·저장 화면 진입과즉시저장을 구분한다.
동일 문구는12개 wording identity를44source literal identity가 참조한다. 번역/용어/넘버맨 말투는 정중한 검토대기 초안이며 독립 의미·인간 승인 대기다.

최초 저장화면 문구 ‘저장 화면으로 갈까요?’는135px로 adopted132px를 초과해 빌드에서 거부했다.
두줄 배치 시도도 원본의 trailing blank row count를 바꿔 거부됐다.
최종 ‘저장 화면에 갈까요?’는 목적지 조사만 명시적으로 수정했으며 질문 의미·정중한 말투·원래 한 prose행+두 newline을 유지한다.
asset wording_history에 미선택 시도와 선택문구/관계를 보존했다. 임의 clipping·자동 축약·넓이기준 완화 없음.

## 소스와 primary build

Source6873F4:1160bytes/22slots, root03827C(32-bit GBA ROM pointer),source block SHA256 `61fc2167017de6bcccb7675fcc2404eee45110b40fbc3e1f3429012cb9ee4c88`.
TPI finite source catalog와 spec에 등록했고 complete_literal_scope=true로44전체source identity를 재추출해 대조한다.
normal-font consumer92,110,adopted132px/3rows,14choice scripts의24px prefix/예뒤2공백/선택 row capacity를 primary build가 검사한다.
최종 최대literal 폭124px,compiled1844bytes at0x807058,실제GBA root0x08807058.
원본 archive storage·commands/arguments/flags/branch order·newlines/blank rows·Yes spaces·6nonliteral script bytes 불변.
script1의 원본 printPlayerNickname은 질문 뒤 별도2행에 그대로 삽입된다. 화면의 일본어 닉네임은 테스트 과정에서 입력한 원본 사용자 이름이며 번역누락 처리나 한글입력 지원을 주장하지 않는다.
닉네임 입력/편집·committed record·전체재표시 소비자·저장/재로드·기존save호환은 여전히 최대 완료위험이다.
새 code hook·save format 변경 없이 기존 normal Hangul font/codec/pipeline을 사용한다.

`build_roll_pet.py`의 기존 누적flags에 `--numberman-pet`을 추가한다. `--numberman-intro` 및 기존 누적save scope 누락은 거부한다.
원본에서 각각 fresh work/out으로 main/_repro/_current_repro를 재생성했다. 세ROM 동일 SHA.
기존 intro v1의22archive payload hashes/bytes와6333A4 저장 제목256bytes를 비교해 동일성을 확인한다. relocation offsets는 현재 cumulative placement에서 산출한다.
원본 SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 보존.
원본·이전후보·거부된work·모든캡처·testsave 보존. 배포패치나출시후보 아님.

## 실행 증거

prefix `poc/runtime/numberman-pet-v1-`.
own cold-part1(state_origin=null)→date→profile→navi-menu→select-numberman(right3회)→intro→prompt-seed→prompts.
부모 checkpoint/artifact hashes와 exact ROM SHA,emulator/components를 검증한다. 타ROM state/RAM/save import나 조작 없음.
intro observer는PET load이전 자체select checkpoint에서 시작한다. `capture_numberman_pet.py`는6873F4에 한정한read-only root/normal glyph/font 관측이다.
31complete captured pages에서22unit(script1,2..8의질문과선택지)에실행 증거:ROMstream→glyphindex/normalfont→CPUfontreads→OBJ VRAM/OAM→화면59,196pixel 검사.
script1의빈영역검사는질문1행에한정해원래nickname2행을잘못소거검사하지않는다. 질문2행들밖빈영역은native option행을제외해현재glyph배치와대조한다.
native choice cursor의배경소유영역만허용하고 번역ink/shadow를가리면실패한다. 8종실제화면과저장완료화면을직접검토했다.
prompts29steps에서모든7메뉴의예기본위치108→아니요144→idle220복귀,첫질문B취소와후속재진입을검증한다.
script10..16의21unit과script20의1unit은finite structure/font/layout 검증만이며해당runtime branch는open22로명시한다. 다른메뉴‘예’의대회/접속/장비등결과나실제통신대전은수행하지않았다.

별도 own intro→save-enter→save-commit 정상입력 경로:
save-enter step10은PET script8,step11은6DA21C script55(root0x08807800)로전환돼‘예’의저장화면진입을검증한다.
commit은read-only saveobserver/isolateddiskinventory이며자체새64KBallFF save SHA71189f...→`f6b079ff340929ba55d0cc5bdd7f1830af1e2e941db7189f235b57c00def4170` 갱신.
다른save불변,step13 native completion58 확인. diskedge/완료전환이며영구재로드나기존save호환증거는아니다.
최초통합report 호출은save-enter 완료receipt가생기기전이라missingfile로중단;capture완료후같은ROM/도구의최종report가PASS했다. 누락receipt를통과처리하지않았다.

## 검증 기록과 남은 작업

`analysis/numberman_pet_v1/runtime.json`, `pet_prompts.png`, `final_identity_audit.json` 참조.
관련66unittest 통과(20.605초); historicalfixture test는새ROM실행증거와구분한다.
최종3독립ROM SHA동일/445현재Pythontools drift=[]/원본SHA보존.
넘버맨재선택숫자말장난6872B8script2,다른PET대화/다른Navi미번역은계속남아있다.
한글이름입력/편집/저장재표시·기존save호환·영구재로드·전체게임/RTC/alarm/오디오/실기/독립의미검토/인간승인/배포미완료.
