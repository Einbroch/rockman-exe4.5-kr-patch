# 도감 칩 이름 1차 묶음 — 개발 초안, 비배포

2026-10-02, 원본 588a77da…의 이름 풀 765190에서 scripts 1..30을
직접 디코딩하고 raw bytes를 대조했다. 실제 라이브러리 번호와 source script
번호는 다르며, 전체 게임의 이름 소비자 범위로 확대하지 않는다.

새 asset: `translations/library_chip_names_batch01_ko.json`.
이전 3개 asset와 개발 ROM, 실패 및 성공 증거는 덮어쓰지 않았다.
빌드에는 `--chip-name-translations`로 새 비배포 asset을 명시한다.
선택된 30개 외 226개 source script와 원래 이름 풀/공유 포인터는 유지된다.
숫자 접미사, E5 종료, 8셀 경계와 전 음절 글리프 공급을 검사했다.
표현은 전부 needs_review다. 8셀 초과 문구를 자동 축약하지 않는다.

EXE3 `translations/chip_names_ko.json`의 동일 원문 이름을 후보 용어로 참고했다.
캐논/하이캐논/메가캐논, 스프레드건, 히트·버블 계열과 미니봄을 대조했다.
EXE4.5의 エアシュート에는 숫자가 없으므로 EXE3 エアシュート1의 숫자를
상속하지 않았다. 참고 파일은 이 타이틀의 용어 승인이나 실제 코드 주소 근거가 아니다.

제품 경로에서 원본부터 새로 빌드한 후보:
`poc/output/exe45_ko_development_chip_names_batch01_v1.gba`
SHA256 `16afa15fb530f1aded001691767f39fecb44394fab0e20760eeedd9408833241`.
초안 총 99단위 = 기존 69 + 칩 이름 30, 이름 초안은 27단위 증가.
다른 이름 소비자, mono 설명, 배틀 및 입력 화면은 여전히 native다.
`_repro.gba`의 ROM 해시가 동일하다. 완성본/배포본이 아니다.

검증:

- CPU 34,054벡터 / 22,972복사, late-wait guard 288벡터 통과.
- 기존 49 + 새 보호 원문/숫자/길이 검사 5 = 54 unit tests 통과.
  첫 새 검사는 unselected_scripts가 목록인 것을 정수와 비교하는 테스트 오류로
  실패했다. 실제 코드/번역 수정 없이 목록 길이 226을 검사하도록 바로잡았다.
- 동일 후보 자체 콜드 부팅(53입력)과 일반 도감 탭을 통과했다. 기존에 획득한
  세 이름의 실제 글리프·cache/ABI와 화면 픽셀을 다시 검사했다.
- `all30`은 descriptor와 acquisition 판단의 CPU read만 대체한다. 원래
  descriptor RAM은 변경하지 않고 새 ROM의 실제 private clone 문자열을 소비했다.
  314갱신 / 2,198행에서 30 source script 모두 renderer를 통과했다.
  게임 진행·획득 조건을 우회한 diagnostic이므로 30개 정상 획득 경로 증거는 아니다.
- 매 프레임 바뀌는 diagnostic 화면은 이전 scanout과 새 VRAM이 다를 수 있다.
  따라서 `all30-stable`은 페이지를 30갱신씩 유지하고 7/8번 캡처에서
  14개 행의 Hangul/숫자/패딩 및 화면 ink/shadow mask를 별도로 대조했다.
  한두 화면이 전체 30개 이름의 사용자 미감 승인을 뜻하지 않는다.

통합 보고서: `analysis/exe45_chip_names_batch01_runtime_v1.json`.
재검사 코드: `tools/report_chip_name_batch.py` (기존 보고서 덮어쓰기 거부).
모든 diagnostic 체크포인트는 별도 이름으로 격리되어 정상 경로에 재사용하지 않는다.

다음 전체 제품 불확실성은 다른 이름 소비자 및 mono 설명의 한글 공급 경로다.
원본의 9개 이름 root-pair를 대상으로 `exe45_chip_name_consumers_static_v1.json`
후보 연결도를 작성했다. 코드/데이터 경계나 첫 근처 BL만으로 함수 역할을
단정하지 않는다. 예를 들어 0801F7DA는 0801F7E8에서 이미 복귀하여,
그 뒤 080083FC BL은 이 이름 선택기 자체의 호출 근거가 아니다.
0803CB64는 0803CB76→0803CBB0의 별도 8셀 1바이트 tilemap parser를 사용한다.
이 경로는 아직 runtime 소유권/진입 화면을 확인하지 않았으므로 새 후크를 설치하지 않았다.
