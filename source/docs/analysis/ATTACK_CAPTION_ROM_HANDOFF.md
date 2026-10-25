# 장비 공격력 이미지 한글화

development-draft; NON-DISTRIBUTION. 문구/미감 needs_review, 배포 승인 아님.
추가 범위는 장비 이미지 `バスター攻撃力` → `버스터 공격력` 한 개다.
798텍스트 단위는 유지, 번역 그래픽은 PET7 + 장비 제목1 + 공격력1의9개다.
전체 미번역 분모나 게임 완료 수치가 아니다.

## 현재 결과

- `poc/output/exe45_ko_development_attack_caption_v2.gba`
- SHA256 `cc3c18f31e3ce3f6dfadbe7fa75605526cbef67dc75d5ff7fdd03cb76c77294e`
- 독립 `_repro.gba` 및 최종 코드 `_current_repro.gba`와 동일.
- 전체 자동 테스트121개 통과 (121 tests, 33.663s, OK).
- `analysis/attack_caption_v2/runtime.json`: 실제 압축 해제·전송·화면 검사.
- `analysis/attack_caption_v2/before_after.png`: 왼쪽 이전 일본어, 오른쪽 반영본.
- `translations/equipment_attack_caption_ko.json`: 원문/문구/영역/폰트/검토 상태.
- `poc/runtime/attack-caption-v1-`: 동일 해시의 실행 기록.

v1/v2는 ROM 바이트 및 해시가 같다. v2는 자산 설명에 압축 해제 후 첫4바이트의
크기 관리 헤더를 native loader가 제거한다는 사실을 명확히 반영한 빌드다.
따라서 v1 cold-chain에서의 검증은 바이트 동일성을 통해 v2에도 적용된다.
원본/이전 ROM 및 조사 실행 v1..v5는 보존한다.

## 원본 공급 경로를 찾은 과정

VRAM06013C00..06013F00의768바이트는 ROM raw 검색으로 찾을 수 없었다.
관찰된 BIOS PC0C1C는 압축 해제가 아니라 CpuFastSet의32바이트 단위 전송이었다.
복사 원본은0202BF9C, 실제 호출은080EC140/r2=256/caller stack LR08000833,
원래 전송 크기는1024바이트였다. CPU/RAM/진행 상태 조작 없이 정상 입력으로
앞단을 추적해 ROM08512FA0의 LZ10 이미지를 확인했다.

원본 압축 슬롯은512FA0..5131A4의516바이트, 해제1156바이트다.
소스 저장 SHA256 `34e7af43c90dd7c80ea176df7bfcb83557673741380328d0853ab481daa46bff`.
첫36바이트는 sprite container 헤더다. 이어지는768바이트가3개의32x16 OBJ로
조립되는96x16 caption이며, 나머지 타일/메타데이터/팔레트는 보존한다.
원본 caption SHA256 `b1e27d350429769edf9350253bd6c470d0d77d62c1b56e9694abec0322910688`.

게임 로더0803C414는 table0803C424의 두 번째 literal3C42C를 통해 이 이미지를
읽는다. 08029164→080EC158(SWI11)에서 scratch0201C000으로 해제하고,
08029190..291A0는 첫4바이트의 크기 관리 필드를 제외한1152바이트를
0202BF7C로 복사한다. 그러므로 caption 타일은 payload+24h이지만 RAM root+20h,
즉0202BF9C다. 원래 코드/참조/출력 크기/버퍼 경로는 모두 유지했다.

## 번역과 보호 조건

캔버스96x16에서 원본 글자·그림자 전체를 포함하는 [7,4,60,11]만 수정했다.
기존 글자 역할F/그림자D를 배경E와 하단 테두리C로 복원한 clean reference를
결정적으로 재생성하고, 기존 PET 작업의 Galmuri7 픽셀 폰트로 한글을 그렸다.
원본 크기 그대로, x8/y5 시작, 글자 advance8/공백3, 잉크F/그림자D다.
청소 영역 밖의 alpha/비벨/테두리/배경/타일과 전체 payload의 나머지는 동일하다.
일본어 잉크를 남기고 그 위에 덧씌우지 않았다. 숫자 script63도 원본 경로다.

재압축은 결정적 greedy LZ10,4바이트 정렬456바이트로 원래516바이트에 들어갔다.
나머지는0 padding이다. 다음 자산을 덮어쓰거나 포인터/게임 명령을 바꾸지 않았다.
독립 decoder와 실제 BIOS가 모두 동일1156바이트를 복원했다.
원본 압축 스트림의 비트 단위 재현은 요구하지 않는다(비정규화 가능한 LZ10).
종료/출력/최대4096거리/중첩 match/용량 제한의 자동 검사를 추가했다.

## 실행 검증

새 ROM 자체 cold-part1→cold-part2를 거쳐 folder-regression/equipment/focus 및
weapon-cycle-r3를 정상 컨트롤러 입력으로 실행했다. 옛 ROM 상태는 옮기지 않았다.
equipment step7/9/11/15에서 caption3개 OBJ의128/160/192,y80,palette3 및 타일,
해제된 RAM1152바이트, caption VRAM768바이트, 비투명 팔레트 역할별 화면 픽셀을
대조했다. 진입·재진입에서 BIOS 해제 결과2개 모두1156바이트 전체를 덤프해 일치했다.
원래 값 `1`의192바이트 stage/VRAM/숫자 OBJ 및 잉크·그림자 마스크도 동일하다.
숫자가 caption의 마지막 배경 위에 겹치는 픽셀은 숫자 마스크로 별도 검사했다.

기존 무기33개 정적 검사와 실제 차지 샷 변경·복귀, 안내문3개와 반환 ABI,
폴더4캡처/캐시/word copy/ABI, PET `통신` 포함7선택도 같은 ROM에서 통과했다.
통신 연결/실제 저장/오디오 검증은 하지 않았다.

## 남은 작업과 재현

다른 Navi별 안내문과 전체 게임의 미번역이 남아 있다. 이 caption의 실제 플레이
샘플은 Rockman뿐이며 모든 Navi 화면/전체 플레이를 확인했다는 뜻은 아니다.
문구/미감 승인, 전체 기기/오디오/배포 QA 미완료다.

이전 weapons 빌드 인자에 `--equipment-attack-caption`을 더하고 새 work/out 사용.
기존 증거 재검사: `python -X utf8 tools/report_attack_caption_runtime.py`.
새 실행: `tools/run_attack_caption_matrix.py`는 v2 ROM/새 attack-caption-v2- 루트 사용.
그 실행은 `python -X utf8 tools/report_attack_caption_runtime.py --prefix attack-caption-v2- --outdir attack_caption_v2_rerun`으로 검사한다.
자동 검사: `python -X utf8 -m unittest discover -s tools -p 'test_*.py'`.
