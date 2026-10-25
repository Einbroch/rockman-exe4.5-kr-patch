# 도감 제목 한글화 — 2026-09-25

> 이 문서는 69단위 제목 단계의 보존 기록이다. 2026-09-28 최신 선택형 72단위
> 개발본과 칩 이름 실행 결과는 `CHIP_LIBRARY_PROGRESS.md` 및
> `exe45_chip_library_ko_runtime.json`을 따른다. 옵션 없는 기본 빌드는 69단위다.

## 현재 결과와 완료 범위

기본 개발본은 `poc/output/exe45_ko_development_library_v1.gba`다.
10,276,712바이트, SHA-256
`68dd04f9e4b2a7db2e567cf5cc42ba3791a83ae378ef36cfef2f23f8d672dba4`.
원본·이전 개발본·격리 세이브는 보존했다. 배포 금지 개발본이며 전 게임 완성본이 아니다.

기존 65개 단위에 `6D9EC0`의 제목 4개를 추가해 69개 단위, 4개 아카이브가 됐다.
초안은 `스탠더드칩`, `메가클래스칩`, `기가클래스칩`, `P.A메모`다.
의미가 독립적인 도감 탭 문구이며 `needs_review`; 사람의 용어·문구·미감 승인은 없다.
728개 비선택 아카이브와 포인터, 저장 아카이브의 비선택 115개 스크립트,
도감 제목 아카이브의 미등록 항목용 스크립트 4는 원본 바이트를 보존한다.

이 단계 당시 다음 미완료 조건은 칩 이름의 별도 타일맵 경로에 일반 한글 문자열을
공급하는 것이었다. 이후 세 이름의 공급을 확인했으나 최대 부하·조건부 아이콘 등은
계속 미검증이다. 제목의 성공을 mono 설명·전투·이름 입력으로 일반화하지 않는다.

## 채택한 구현

기본 빌드 진입점은 계속 `tools/build_development_patch.py` 하나다.
`translations/library_headers_ko.json`과 아카이브 레지스트리가 제목 선택을 선언한다.
실험 중 사용했던 네 일본어 글리프 슬롯 치환은 새 ROM에 없다.
실제 한글 제목과 `--fixedcell-visibility` 임시 치환을 동시에 선택하면 빌드가 실패한다.

- 고정폭 파서: 런타임 `0x03006824`; 글리프 복사기 `0x0300689C`.
- 설치: 원본 ROM `0x1EF6FC`의 F9 디스패치 포인터 한 곳. 원래 값 `0x030069D9`.
- 인코딩: `F9 FC` 뒤 U+AC00 기준 uint16 LE 음절 번호. 일반 대사와 같은 문자표.
- 별도 한글 글꼴: 11,172×64 = 715,008바이트, ROM `0x91E634`, 버스 `0x0891E634`.
- 새 Thumb-1 처리기: ROM `0x9CCF34`, 52바이트(코드 38 + 정렬/리터럴).
- 셀은 8×16, 전진 8픽셀. 갈무리11 Condensed 7×11 원본에 기존 big 팔레트의
  본문/그림자 1/2를 사용한다. 전체 글꼴을 VRAM에 동시에 올리지 않는다.

원래 복사기를 호출하여 tint·패킹·셀 채우기·RAM→VRAM 업로드를 유지한다.
새 문자는 stream +4, stage +64, r4/r5/r9 +1이며 r3/r6/r7/r8/r10-r13을 보존한다.
기존 F9 하위 명령은 원래 처리기로 분기한다. 생성 코드는 고정된 Keystone/Capstone으로
ARM7TDMI Thumb-1 최종 배치의 명령 경계·분기·리터럴을 검사한다.
주소와 원본 코드 해시는 `tools/specs/exe45_fixedcell_extension_v1.json`에 있다.

## 압축·RAM 경계

원본 `6D9EC0`: 저장 51바이트 / 해제 50바이트. 번역: 저장 116 / 해제 99바이트.
원본 포인터 `0x428E0`을 새 압축 스트림 ROM `0x8007A0`으로 이동한다.
스크립트 오프셋은 TextPet이 다시 계산하고 모든 보호 명령과 비선택 스크립트를 검사한다.

대상 로더 `0x08042798`은 `0x080EC158`의 **SWI 11h**로 `0x02024000`에 해제한다.
그 다음 `0x080428F0`이 네 제목을 9×1셀로 그린다. 각 제목은 5/6/6/5셀이라
72픽셀 표시 범위 안이다. 별도 미등록 항목 소비자는 갱신된 오프셋 표의 스크립트 4를 읽는다.

장면 초기화 표 `0x08042884`의 다음 별도 자산 목적지는 `0x02025000`이다.
빌드는 보수적인 **160바이트 개발 상한**을 둔다. 이를 전역 빈 RAM이나 전체 게임의
버퍼 소유권 증명으로 취급하지 않는다. 실제 두 번의 로드에서 전체 256 KiB EWRAM을
직전/직후 비교했고, 정확히 예상 페이로드가 해제됐으며 그 99바이트 밖의 변경은 0이었다.
진입부터 탭 왕복·종료·재진입까지 해제본과 타일 소비의 수명도 확인했다.

압축 writer는 BIOS type-10의 literal-only 표현만 생성한다. 공개
[GBATEK LZ77 규격](https://rust-console.github.io/gbatek-gbaonly/#lz77uncompreadnormalwrite8bit-wram---swi-11h-gbands7nds9dsi7dsi9)의
24비트 출력 길이, MSB-first 플래그, 4바이트 정렬/0 패딩을 따른다.
원본 압축 바이트의 동일 재현은 요구하지 않는다. 자체 역변환, 기존 독립 디코더,
실제 BIOS 출력 비교를 각각 통과했다. 비선택 압축 아카이브는 재압축하지 않는다.

## 실행 근거와 회귀 검사

정본 보고서: `analysis/exe45_library_ko_runtime.json`.
직접 관찰과 해시: `analysis/library_runtime_observations_v1.json`.

- 새 ROM 콜드 부팅 → 첫 소개문 → 도감 진입. 네 제목의 탭 왕복·재진입.
- 2회 BIOS 해제 결과/전체 EWRAM 변경 범위 검사, 새 처리기 38회 ABI 검사 통과.
- 진입/재진입에서 4개 제목+1개 설명의 ROM 글리프→RAM staging→VRAM 연결을 확인.
- 제목 캡처 13장의 모든 제목 글자에 대해 타일맵과 본문/그림자 픽셀 마스크 일치.
- 원래 일본어 칩 이름용 160슬롯 적재 창은 원본과 바이트 동일. 칩 그림·설명 선택과 지우기 유지.
- 기존 F9 01 입력 재표시와 B 삭제/취소를 관찰했다. F9 00은 정적 호환 검증만 있고
  실제 실행 분기는 이번에 관찰하지 않았다. 한글 이름 입력을 구현한 것이 아니다.
- 새 ROM에서 저장 화면 이동 확인, 실제 저장 확인, 전원 차단 금지 경고, 저장 완료,
  PET 복귀와 파일 기반 새 프로세스 이어하기까지 확인.

도감 후속 대화가 취미 질문으로 이어져 초기 재진입/저장 이동 시도 일부는 목표에
도달하지 못했다. `reentry`라는 디렉터리 이름만으로 성공 판정하지 않는다.
미확정 일본어 입력을 B로 삭제/취소한 뒤 `reentry-settled`에서 실제 재진입했다.
모든 경로는 격리 Mesen/세이브와 정상 패드 입력만 사용했다. ROM/RAM/진행도 주입은 없다.

새 테스트 세이브의 완성 해시는
`a4535c6bea9dc97dfe56790b0572d38c916cc7bdb871cb2d18b3912d1370bdc4`이며
새 실행 전후 유지됐다. 기존 다른 `.sav`는 변경하지 않았다. RTC의 시간 진행은 별도다.
이전 save-v1의 덮어쓰기 예/아니요 및 PET 전체 메뉴 검증은 이전 ROM의 근거로 남기며,
이번 ROM에 그대로 전가하지 않는다. 저장 오류·재시도도 아직 미검증이다.

고정폭 문자표는 11,172자 각각을 스크립트 처음, F9 00 뒤, F9 01 00 뒤에서
독립 바이트 기대값·의미·바이너리 왕복으로 검사했다.
`analysis/exe45_fixedcell_codec_v1_final.json`은 정적 증거이며 게임 내 전 글자 표시가 아니다.
실제 표시된 고정폭 한글 음절 목록은 런타임 보고서에 따로 기록한다.

## 재현과 다음 작업

```powershell
python -X utf8 tools/build_development_patch.py --work poc/visibility/work-library-next --out poc/output/exe45_ko_development_library_next.gba
python -X utf8 tools/verify_fixedcell_codec.py --work poc/visibility/work-fixedcell-codec-next --report analysis/exe45_fixedcell_codec_next.json
python -X utf8 tools/report_library_runtime.py --out analysis/exe45_library_runtime_recheck.json
python -X utf8 -m unittest tools/test_text_catalog.py tools/test_korean_codec.py tools/test_tpl_literals.py tools/test_development_font.py tools/test_archive_scripts.py tools/test_fixedcell_font.py tools/test_lz10_literals.py
```

기본 선택과 명시적 4개 선택 모두 같은 ROM 해시를 재현했다. 기존 3개 선택도 원래
save-v1 해시 `077eb3d0…84a35`를 재현한다. 위 report 명령은 보존한 증거 재검사이며
새 에뮬레이터 실행이 아니다. 30개 단위 테스트 통과. 출력은 항상 새 경로를 사용한다.

후속 칩 이름 조사는 `CHIP_LIBRARY_PROGRESS.md`와
`exe45_chip_library_survey_v2.json`에 이어진다. 393개 물리적 이름 스크립트와
9쌍의 공유 포인터, `0x08042FB0`의 7행 타일 생성, 조건부 아이콘 공간,
도감→PET→이름 입력의 VRAM 재사용을 확인했다. 160셀 적재량을 번역 어휘 제한으로
취급하지 않으며, 56셀 도감 전용 캐시는 아직 후보다. 칩 이름 한글 후크/번역은
미적용이고 현재 69단위 빌드는 변하지 않았다. mono 설명, 다른 메뉴/전투/그래픽,
사용자 문자열은 별도 조사 범위다.
