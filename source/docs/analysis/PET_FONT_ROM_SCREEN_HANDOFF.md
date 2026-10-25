# PET 메뉴 한글 이미지 반영 및 새 ROM 검증

2026-10-03 / development-draft; NON-DISTRIBUTION

## 결과와 사용자 선택

사용자는 작은 글자 가독성 실패 보고 및 소형 픽셀폰트 재작성 권고에 대해
“검증하고 진행해줘.”라고 답했다. 그 방향으로 PET 메뉴 라벨 7개를 재작성·반영했다.
기존 불합격 imagegen 시안/변환 v2/v3는 보존했으며 사용하지 않았다.

원본 ROM은 변경하지 않았고, 기존 개발 ROM을 입력으로 패치하지 않았다.
기존 758문장 번역 입력을 유지한 원본 기반 주 빌드에 `--pet-menu-graphics` 옵션을 추가했다.

새 ROM: `poc/output/exe45_ko_development_pet_graphics_v1.gba`

재빌드: `poc/output/exe45_ko_development_pet_graphics_v1_repro.gba`

두 SHA256: `2ec5cf763c8cf063cc67e2e02609a3097de2471425792670c5172e523ae69f40`

원본 SHA256: `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`

## 타일·글꼴 및 통/동 구분

`translations/pet_menu_graphics_ko.json`은 7개 source ID/타일/문구/자간/글꼴과 사용자 방향을 기록한다.
공식 Galmuri v2.40.4 고정 커밋 `bdb86ae89466a361eb8df861222736b81ff975ef`의 Galmuri7 BDF를
사용한다. 다운로드 파일 및 기존 OFL 라이선스의 SHA256을 빌드에서 검증한다.
글꼴 파일 내부 버전 표기는 2.403이며, 파일 이름의 v2.40.4는 취득한 upstream 태그다.
출처: https://github.com/quiple/galmuri

소스 비트맵을 축소하지 않고 정확히 래스터화했다. 라이브러리만 자간7, 나머지는8이며
공백3으로 배치한다. 어떠한 문구도 축약/누락하지 않았다. 모든 글자가 63x8 원본 문자 띠에 들어간다.

표준 작은 통 글리프에서도 ㅌ이 뭉쳐 보이는 위험을 줄이기 위해 프로젝트 전용 통을 작성했다.
비트 행은 `7C 78 40 7C 10 FE 44 38`이며, 가운데 획과 아래 획 사이 왼쪽 세로줄 행을 명시했다.
동과 다른 글리프임을 검사하며, 기존 BDF 파일 자체는 변경하지 않았다.
이 override는 번역 입력에 명시돼 있고 빌드 및 테스트가 다른 비트 배열을 거부한다.
픽셀 검증은 정확한 글리프 공급을 증명하지만 최종 사용자 선호/가독성 판단까지 자동 승인하지 않는다.

원본 4bpp OBJ 블록 위치0x6303B8/길이0x1200과 palette role1/4를 유지했다.
7개 문자 pair의 x1..63/y1..8만 변경한다. 모든 아이콘/프레임/투명 픽셀 및 나머지 블록 바이트는
원본과 같고 무변경 decode/encode 왕복, 보호 픽셀, 빌드 writer 겹침, 헤더/최종 diff 검사를 통과했다.

## 실행 검증

`tools/run_pet_graphics_matrix.py`는 과거 receipt에서 컨트롤러 문자열만 취득한다.
새 ROM의 cold-part1부터 새 state를 만들고 cold-part2, focus, prompts, folder를 이어 실행했다.
과거 ROM checkpoint/save/progress RAM을 가져오지 않았고, source-read probe도 read-only다.

- cold-part1: 캡처2/2, cold-part2:1/1, 정상 종료.
- cold-part2 실제 BIOS PC0xC18에서 새 ROM 그래픽의 연속32비트 읽기160건을 검증했다.
  원본 source offset/VRAM destination0x06011000의32바이트 그룹 진행과 일치한다.
- focus: 메뉴7개 순회7/7. x137/palette8 선택 항목과 실제 OAM 타일을 검사했다.
- prompts: 확인 및 B취소14/14. 통신 대전 확인 화면은 step023이다. 실제 통신/저장 작업을 실행하지 않았다.
- 21장 각각7개 라벨: VRAM 전체0x1200바이트가 새 ROM 타일과 같고, 모든 문자 띠 픽셀은
  스크린샷의 foreground/background 색으로 정확히 분리된다. 문자/배경 색이 같거나 예상 마스크가
  다르면 실패한다. 이 검사에서 전역 LCD 색 변환 모델을 새로 입증했다고 주장하지 않는다.
- 폴더: 기존 normal controller route16입력/4캡처 정상 종료, 실제 copy/cache/ABI observer PASS.
  다른 폴더 이름 전체의 새 glyph pixel report를 작성한 것은 아니다.

`analysis/pet_font_v2/runtime_contact_sheet.png`는 새 ROM 스크린샷 9장을 붙인 검토용 표다.
위7장은 메뉴 순회, 8번째는 통신 확인, 9번째는 폴더 회귀 화면이다. 7개 메뉴 라벨 및 통신 확인,
폴더 화면을 직접 검토했다. 일본어 장비 헤더 등 이 범위 밖 이미지 텍스트가 남아 있음을 확인했다.

기존 758개 ROM과 비교해 **동일 길이이며 PET 블록 바깥의 모든 바이트가 같다**.
기존7개 번역 아카이브/725미변경 아카이브와 기존 코드·폰트 공급은 그대로다.
이 정적 보존 사실을 새 ROM의 모든 전투/이벤트 실행 검증이라고 확대하지 않는다.

최종 자동 테스트100개 통과. 추가 테스트는 보호 픽셀/무변경 왕복/통 글리프 및 잘못된
동신 문구·자간·글리프·원본 해시 거부, 새 ROM의21화면 픽셀 마스크 재검증을 포함한다.

## 미완료 범위

PET 밖 일본어 이미지 전체 목록/번역, 실제 통신·저장·실기기·오디오·전체 게임 진행,
전수 문구 사용자 검토 및 정식 gt-image pipeline prerequisites/release는 미완료다.
현재 결과는 758개 텍스트 + PET7개 그래픽 라벨의 **개발 검토용 ROM**이며 배포본이 아니다.
