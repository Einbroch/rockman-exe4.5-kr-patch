# 9번째 장비/칩 폴더 화면 미번역 반영

상태: development-draft; NON-DISTRIBUTION. 사용자 요청의 9번째 화면에 있던
`そうび` → `장비`, `チップフォルダ` → `칩 폴더`를 새 개발 ROM에 반영했다.
번역 문구는 needs_review이며 전체 게임 한글화/이미지 번역/배포 완료를 뜻하지 않는다.

## 현재 결과

- ROM: `poc/output/exe45_ko_development_folder_labels_v1.gba`
- SHA256: `b4afc0967d53276dd23fb5980014be4ecbc3eafabb79694a20d44b5e782d1360`
- 독립 재빌드: `poc/output/exe45_ko_development_folder_labels_v1_repro.gba`, 바이트 동일.
- 누적 텍스트 759단위, PET 그래픽 7라벨 + 장비 상단 그래픽 1라벨. 전체 분모 아님.
- 원본과 이전 개발 ROM은 보존. 7개 주 텍스트 아카이브 반영/725개 미선택 원본 보존.
- 실제 화면: `poc/runtime/folder-labels-v1-folder-regression/step_016.png`
- 전후 비교: `analysis/folder_labels_v1/before_after.png` (왼쪽 이전, 오른쪽 새 ROM).
- 기계 검증: `analysis/folder_labels_v1/runtime.json`.

## 구현 경계

상단 장비 글자는 원본 ROM 0x6330A4의 256바이트, 64x8 OBJ 그래픽이다.
기존 승인된 Galmuri7 픽셀폰트 경로로 장비를 작성했다. 수정 영역 x22..44,
y0..7 밖의 픽셀과 전체 타일 구조는 보존했다. 소스/폰트/라이선스 해시 검사,
원본 타일 무변경 왕복 및 네이티브 BIOS halfword 읽기 64건을 검증했다.
실제 OBJ VRAM 0x06010A00과 타일 0x50/0x54, 팔레트12, 좌표(86,2)/(118,2),
4개 폴더 화면의 글자/배경 픽셀 마스크가 일치한다. AI 이미지 시안 사용 아님.

칩 폴더는 고정 8x1 big-font 텍스트 경로다. 압축 원본 0x6E2B9C의 76개 스크립트
중 script1만 번역한 비압축 ROM 복제를 생성했다. 75개 나머지 스크립트는 동일하다.
원본 Navi 데이터 RAM의 확장 가능 공간을 가정하지 않았다. 독립 네이티브 함수
0x0803E45C에서 사용하는 데이터 루트 리터럴 0x3E474만 새 복제로 연결했다.
해당 함수 명령/원본 Navi 포인터 테이블/압축 데이터/공유 로더는 변경하지 않았다.
주변 Thumb 리터럴 참조는 0x3E460 한 곳이며, 23개 원본 Navi 풀의 script1이 동일하다.
이 경로의 전체 Navi 실행 검증은 아직 하지 않았으며 현재 Rockman 화면만 확인했다.

실행 기록은 root=새 ROM 복제, script=1, lr=0x0803E473, stage=0x0201FC00,
target=0x06007C00, font=0x08601738, width=8/height=1을 확인했다.
칩/공백/폴/더/공백4의 정확한 폰트 인덱스와 ROM 글리프→버퍼→VRAM→BG1
타일맵→화면의 ink/shadow/background 전 픽셀을 대조했다.
기존 Navi RAM 데이터는 해당 원본 Navi 풀과 계속 일치한다.

## 실행 검증

기존 ROM의 입력 문자열만 재사용하고, 새 ROM의 cold-part1→cold-part2에서
생성된 체크포인트만 사용했다. 4개 루트의 모든 아티팩트/상태 부모 해시를 검증했다.
폴더 4캡처의 정상 입력/스크롤, 캐시 checks=13107/hits=13090/resets=1,
실제 word copy17건 및 ABI 검사를 통과했다. 기존 PET 7개 선택 화면 전체 글자
픽셀 마스크도 통과했으며 `통신` 자형 교정이 유지된다. 통신 연결/저장 실행은 하지 않았다.

재현: 기존 PET 전체 빌드 인자에 `--folder-labels`를 추가하고 새 work/out 사용.
`tools/run_folder_labels_matrix.py`는 새 런타임 출력만 허용한다.
`python -X utf8 tools/report_folder_labels_runtime.py`로 남은 증거를 재검증할 수 있다.
`python -X utf8 -m unittest discover -s tools -p 'test_*.py'` 자동 테스트 실행.

추가 한계: 다른 이미지/메뉴의 미번역 전수 조사, 전체 플레이, 실제 기기,
오디오(현재 mute), 사용자 문구/미감 검토, 정식 이미지 단계 및 배포 QA는 미완료다.
