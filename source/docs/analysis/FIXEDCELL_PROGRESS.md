# 고정폭 글꼴·도감 표시 경로 (2026-09-24)

2026-09-25: 도감 제목의 실제 번역을 추가한 최신 개발본과 현재 작업은
`LIBRARY_PROGRESS.md`로 옮겼다. 이 문서는 임시 표시 PoC의 역사적 근거다.

## 당시 판정과 산출물

**8×16 셀에서 한글 두 음절의 표시 PoC 통과. 정식 메뉴/칩 이름 번역은 미구현.**
대사 렌더러의 성공을 다른 UI에 자동 적용하지 않고, 실제 도감의 서로 다른 두
소비 경로에서 ROM→VRAM→화면을 확인했다. 프로젝트 전체 한글화는 계속 미완료다.

이 조사 당시 일반 테스트용 개발본은
`poc/output/exe45_ko_development_save_v1.gba`이며 SHA-256은
`077eb3d017fef5c0b2ab39c49fb5d887f673a270ca91ac18a88296522cd84a35`다.
소개·PET·저장 누적 65개 번역 단위였다. 당시 빌더의 기본 옵션으로 다시
만든 `exe45_save_fixedcell_default_regression.gba`가 이 파일과 바이트까지 일치한다.

별도 진단본 `poc/output/exe45_fixedcell_visibility_v1.gba`의 SHA-256:
`8dfa1b94c94d7dc06d8064777e98248996978fe034b59f602f89f130b6b44bd6`.
동일 빌드 재현본 `_repro.gba`와 해시가 같다. 원본 ROM에서 주 빌더로 재생성하며
65개 기존 번역을 포함한다. **이 파일은 일반 플레이용·배포용이 아니다.**

진단본은 이미 사용 중인 `ス/タ/キ/ャ` 네 글리프만 `한/글/한/글`로 임시 교체한다.
따라서 분류 제목과 캐논 이름 앞에 한글이 나타나지만 의미에 맞는 번역이 아니다.
이 네 칸의 다른 소비자도 영향을 받으므로 임시 매핑을 제품 인코딩으로 채택하지 않는다.
기본 개발본과의 차이는 네 64바이트 레코드 안에만 있으며 코드·문자열·전송량은 같다.
명시적 `--fixedcell-visibility` 옵션 없이는 이 치환을 적용하지 않는다.

## 새로 확정한 경계

일본어 비교 기준은 저장 검증본의 정상 PET 대기 상태에서 도감에 진입한
`poc/runtime/fixedcell-save-v1-library-idle`이다. 진단본은 별도 콜드 부팅에서
일반 패드 입력으로 소개·PET를 거친 다음 도감에 들어갔다. 외부 세이브나
게임 진행 RAM 주입을 사용하지 않았다.

| 구분 | 분류 제목 | 칩 이름 목록 |
|---|---|---|
| 현재 공급 | 호출 때 필요한 글리프를 순서대로 복사 | 원본 폰트 앞 160레코드를 미리 적재 |
| 확인한 ROM 공급 | `0x601738 + index×64` | `0x601738..0x603F38` |
| RAM/VRAM | RAM `0x0201F000` 등 → VRAM `0x06009000` 등 | VRAM `0x06004000..0x06006800` |
| 표시 | BG0, 문자 블록 `0x8000`, 맵 `0xE000` | BG1, 문자 블록 `0x4000`, 맵 `0xE800` |
| 대표 위치 | 화면 `(96,16)`의 두 셀 | 화면 `(136,32)`의 두 셀 |
| 한 셀 | 위 8×8 타일 + 아래 8×8 타일, 4bpp, 64바이트 | 동일 |

제목의 원본 스크립트는 압축 아카이브 `6D9EC0`(저장 51바이트, 해제 50바이트)의
script 0~3이다. 원본 해제 결과와 실행 RAM `0x02024000`의 50바이트가 일치한다.
현재 파서는 9셀×1행을 그리며 부족한 칸은 원본 공백 글리프로 채운다.
제목 네 건 모두 576바이트의 ROM 공급→RAM 생성→VRAM 도착이 일치했다.

다섯 번째 호출은 `0x619EF8`의 별도 mono 폰트로 칩 설명을 그리는 10셀×3행,
1,920바이트 OBJ 공급이다. 이 경로의 원본 바이트 전달도 일치하지만 **mono 폰트의
한글 표시를 검증한 것은 아니다.**

칩 이름은 이 다섯 글리프 복사 호출로 생성되지 않는다. 표준 도감의 캐논 이름
앞 두 글자에서 BG1 맵 값 `E022/E023`, `E0B4/E0B5`가 미리 적재한 폰트의
인덱스 `0x11`, `0x5A` 상하 타일을 선택함을 확인했다. 160은 관찰한 현재 적재
범위이며 엔진 전체 글리프 최대 개수나 사용 가능한 여유 슬롯 수가 아니다.

GBA 타일/맵 해석은 [Tonc의 BG 설명](https://gbadev.net/tonc/regbg.html)을 참조하되
게임의 실제 레지스터·맵·VRAM으로 대조했다. 읽기 전용으로 캡처한 IO 중 BG 스크롤
레지스터는 write-only라 값으로 사용하지 않고, Mesen 상태의 `scrollX/Y=0`을 확인했다.

## 글꼴 후보와 검증 범위

갈무리11 Condensed v2.40.4 태그의 BDF를 후보로 사용했다.
출처: [고정된 upstream 커밋](https://github.com/quiple/galmuri/tree/bdb86ae89466a361eb8df861222736b81ff975ef).
파일 내부 FONT_VERSION은 `2.403`; 입력 신원은 태그 이름만이 아니라 아래 해시로 고정한다.

- 입력: `external/fonts/Galmuri11-Condensed-v2.40.4.bdf`
- SHA-256: `5c19d39413241e272810e115ee810feaea6c4b5684bfa3e17a98ef1cb3a7df63`
- 라이선스: `external/fonts/LICENSE-Galmuri-v2.40.4.md` (SIL OFL 1.1, 저작자 고지 포함)
- 표현: 7×11 원래 비트맵, 기준선 14, 오른쪽 아래 한 픽셀 그림자, 8×16 셀
- 크기 변형·보간·누락 대체 없음. 배경/본문/그림자 니블은 big 폰트의 `0/1/2`다.

한글 11,172자의 셀·그림자 경계 및 픽셀 패킹 검사는 모두 통과했다.
전부 저장하면 715,008바이트이지만 **이를 전부 VRAM에 동시에 올린다는 뜻이 아니다.**
실제 게임 내 표시 증거는 `한`, `글` 두 음절뿐이며 글꼴 미감의 사람 승인도 아직 없다.

정본 실행 보고서: `analysis/exe45_fixedcell_visibility_runtime.json`.
직접 본 19장과 여섯 실행의 결과·환경 해시는
`analysis/fixedcell_runtime_observations_v1.json`에 고정했다.
정적 후보 전체 글리프 검사와 두 음절의 런타임 증거를 별도 항목으로 보고한다.

제목과 목록의 대표 셀을 VRAM 타일맵에서 재구성한 후 화면 캡처의 본문/그림자
픽셀 마스크와 대조했다. 진입·Down·탭 왕복·재진입의 다섯 캡처에서 두 영역이
일치했다. 나머지 확인은 직접 관찰로 기록하며 자동 검사의 통과로 미감을 승인하지 않는다.
일본어와 한글 대사, 선택 화살표, 설명 영역 지우기, PET 복귀도 관찰했다.

## 실패·미도달 기록

- `fixedcell-save-v1-library`: 재시작 직후 신년/목표 대화 중이었다. 글꼴 복사 호출
  0건이며 도감에 도달하지 못했다. 미도달을 소비자가 없다는 증거로 사용하지 않는다.
- `fixedcell-v1-reentry`: 도감 종료 뒤 취미 질문/이름 입력이 시작됐다. 이 캡처는
  도감 재진입이나 한글 이름 입력 검증이 아니다. B로 입력을 취소한 뒤 PET 대기에서
  시작한 `fixedcell-v1-reentry-settled`가 실제 도감 재진입 근거다.

격리 Mesen/세이브 폴더만 사용했다. 기존 격리 `.sav` 해시는 각 실행 전후 동일하며
진단본 이름의 빈 테스트 `.sav`는 최초 실행 때 에뮬레이터가 새로 만들었다.
RTC 파일은 정상 시간 진행으로 달라졌다. 사용자 원본 ROM·외부 세이브는 수정하지 않았다.

## 재현

```powershell
python -X utf8 -m unittest tools/test_text_catalog.py tools/test_korean_codec.py tools/test_tpl_literals.py tools/test_development_font.py tools/test_archive_scripts.py tools/test_fixedcell_font.py
python -X utf8 tools/build_development_patch.py --translations translations/megaman_intro_ko.json --translations translations/megaman_pet_menu_ko.json --translations translations/megaman_save_ko.json --fixedcell-visibility --work poc/visibility/work-fixedcell-next --out poc/output/exe45_fixedcell_next.gba
python -X utf8 tools/report_fixedcell_runtime.py --out analysis/exe45_fixedcell_runtime_recheck.json
```

26개 단위 테스트 통과. 마지막 명령은 보존된 실행 증거의 재검사이며 새 게임 실행이
아니다. 모든 출력 이름은 새 경로로 지정해야 한다. 실행 재현 명령·입력·진단 체크포인트
부모는 각 `result.json`에 있다. 관찰기는 고정된 기존 실행기를 변경하지 않고 읽기 전용
콜백을 추가한다. 자체 해시와 실행 Lua도 결과에 묶여 있다.

## 다음 판별과 작업

2026-09-25 후속: 제목의 정식 F9 FC 경로와 압축 재삽입은 `LIBRARY_PROGRESS.md`에서
구현·검증했다. 아래 항목은 그 이전 조사 계획이며, 칩 이름 경로는 여전히 미완료다.

당시 가장 큰 미완료 조건은 **일반 한글 문자열을 기존 일본어/숫자와 충돌 없이 표시하는 것**이었다.
현재 임시 슬롯 치환을 확대하거나 배포 매핑으로 승격하지 않는다.

1. 칩 이름의 문자열→타일 인덱스 파서를 추적한다. 현재 160슬롯 적재 범위와 실제
   화면별 동시 글리프·숫자·기호·선택 상태의 수명을 분리하여 재사용 가능한 슬롯을 판정한다.
   동적 공급이 필요하면 페이지 전환/재진입의 기존 슬롯 참조를 보존하는 설계로 진행한다.
2. 이미 확인한 고정폭 루프 `0x03006824`의 F9 디스패치에 일반 대사와 같은 한글
   이스케이프를 추가할 수 있는지 ABI와 원래 `printString` 경로를 대조한다.
3. 제목 아카이브의 압축 재삽입·참조·해제 버퍼 경계를 확정한 뒤 제목부터 실제 번역을
   적용한다. 제목과 칩 이름은 서로 다른 작업이며 하나의 성공을 다른 쪽에 이전하지 않는다.
4. mono 설명·메뉴 이름·전투·이름 입력·그래픽 문구의 소비자 모집단을 계속 분리해 조사한다.

이 기술적 표시 결과는 채택 가능한 경로의 근거다. 임시 매핑은 폐기 대상이며 기본
제품 빌드는 변하지 않았다. 정식 구현과 사람의 글꼴/번역 검토 전에는 완성 패치를 주장하지 않는다.
