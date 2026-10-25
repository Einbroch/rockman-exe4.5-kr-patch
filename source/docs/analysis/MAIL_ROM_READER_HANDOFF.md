# 메일 ROM 직접 읽기 경로 PoC (2026-10-13)

이 기록은 이전 PoC의 결과다. 현재 추가43개 적용과 통합 검증은 `analysis/FULL_MAIL_BODY_HANDOFF.md`를 따른다. 아래 당시 미완료 조건과 증거는 이력으로 보존한다.

## 작업 방식과 범위

사용자 지시: ROM 작업만 진행하며, 별도 요청 전에는 새 BPS/xdelta/ZIP을 만들지 않는다. 이번에는 패키징을 실행하지 않았다. 기존 패키지는 보존한다.
가장 어려운 잔여 조건은 전체 메일120개를 같은 RAM 해제 버퍼에 넣을 때339바이트 초과하는 문제다. 단순히 한도를 늘리면 다음 자산을 침범한다.
이번 ROM은 이를 해결하기 위한 직접 읽기 경로의 통합 PoC다. 신규 번역 문구는0개, 기존 누적2,732개/66아카이브 및 메일 본문77개를 그대로 유지한다. 남은43개 적용 완료를 의미하지 않는다.

## 정확한 산출물

`poc/output/exe45_ko_development_mail_rom_reader_v1.gba`, 11,237,488바이트.
SHA256 `0e25d98bd1ff7c5cda5516a475f49b2936c55ed9bfa1aa8c9640f010a1cae683`.
동일 플래그의 독립 `_repro.gba` 전체 바이트 동일.
기존 뉴스 ROM 빌드 플래그에 `--mail-rom-reader`를 추가했다. primary immutable-source builder에서만 clone/selector를 생성한다.
원본 ROM/사용자 SAV/기존 ROM/패키지를 변경하지 않았다. development-draft; NON-DISTRIBUTION, 공개 릴리스가 아니다.

## 조사와 채택한 제한된 경로

원본 `08040548`은 `[r5+10]` 내비 번호로 body 포인터 표 `080405F8`을 선택한다. 앞24개 포인터가 같은 `086DD9AC`를 가리키며 뒤5개는 다른 내비용 본문이다. 메일 ID별 표가 아니므로 기존 포인터만 나누는 단순 뉴스/오피셜 분리 설계는 채택하지 않았다.
본문 진입 경로 `0803FD04`→`0804F7B6`, 이어서 `0804F7B8`의 원본 BL→`0804FB4C`, reader에 들어오는 LR은 `0804F7BD`다.

기존 key-item selector와 하나의 writer로 조합한 guard:

- RAM 루트 `0202B2F4`, LR `0804F7BD`, unsigned8bit script0..31, 현재 로딩된16바이트 헤더가 모두 맞을 때만 본문 기준 주소를 `08AB5C1C`의 raw ROM clone으로 바꾼다.
- 헤더 `4000ef06c608880c1110111011101110`, clone7,005바이트 SHA256 `a371a2cb2b0378fddb258b66c294a50da683ed927ac9f28cf8d0b0489932c813`.
- 키 아이템의 두 루트/네 호출/헤더/49script guard는 유지한다. 그 외 호출·헤더·루트·범위는 원래 reader로 돌아간다.
- 원본 reader의 덮인12바이트 효과를 재현하고 `0804FB58`에서 재개한다. ARM7TDMI/ARMv4T Thumb-1 생성/역어셈블/최종 위치의 분기·리터럴 검사를 사용한다.
- 기존 압축 로더와 RAM 목적지/해제7,005바이트는 그대로다. 영구 RAM 상태·새 RAM 버퍼·추가 압축 해제는 없다.

## 증거와 한계

`analysis/mail_rom_reader_v1/cpu_verification_r2.json`: 최종 ROM selector867조건 PASS.
메일32·키 아이템196·변경 헤더160·범위 밖15·미확인 호출18·미확인 루트1·다른 키 아이템180·다른 내비 메일265조건.
원본과 레지스터/flags/context를 비교하고 루트/stream 변경만 허용했다. 텍스트 RAM/ROM clone 불변, 원래 stack/context 밖 쓰기 없음.
native216바이트 zero helper를 계약으로 대체한 합성 CPU 벤치이므로 실제 GBA 타이밍/수신/플레이 증거가 아니다.
기존 selector fixture7개와 새 source/input 거부 fixture4개 PASS.

정상 입력 경로의 새 게임/초기 설정/자판 기능 버튼/네 내비 선택 및 첫 메일23쪽/종료/재열기 PASS.
첫 본문 화면에서 context wait/base/bookmark=`08AB5CB3/08AB5C1C/08AB5C5C`로 ROM 직접 읽기를 관측했고 페이지마다 RAM 해제 데이터는 기존과 동일했다.
오피셜32쪽은 같은 ROM의 원래 renderer 격리 진단에서 페이지/화살표/종료/전체 해제 바이트 PASS.
뉴스22쪽도 전 페이지 직접 화면 확인 및 ROM stream/page/종료 검사 PASS. 최종 검증 파일 `analysis/mail_rom_reader_v1/runtime_verification.json`의 `mail_rom_reader_first_letter_verified`와 `mail_rom_reader_diagnostic_verified`가 모두true다.
진단은 script0 표 읽기 한 번만 alias하며 해당 본문의 발신자/제목·정상 수신·퀘스트 진행·저장 호환을 증명하지 않는다. 진단 코드는 ROM에 포함하지 않는다.
현재 ROM에서 키 아이템의 실제 메뉴 경로는 다시 실행하지 않았으며 해당 guard 회귀는 CPU 벤치 범위다.

기존 뉴스 ROM과 비교해 reader veneer12바이트 및 기존 selector가 시작되던 append tail 이후만 바뀐다. 모든 기존 번역/폰트/이미지와 key-item raw clone은 동일하다.

## 다음 실제 번역 반영 작업

1. 현재 guard가 로딩된 본문 헤더와 ROM clone의 헤더를 동일하게 사용하는 PoC다. 전체120개를 적용할 때는 안전한 RAM 로딩 payload와 별도의 전체 raw-ROM clone을 명시적으로 분리하고 각 헤더/참조/제어 보존을 검증해야 한다. 현재처럼 전체 payload를 압축 해제하는 빌드에서는339바이트 초과가 그대로 발생한다. 이 조건은 아직 해결 완료가 아니다.
2. `analysis/mail_rom_reader_v1/remaining43_layout_demand.json`:43개 초안 중 `11:0`, `12:0`, `12:8`, `14:4`가 literal-only 폭/화살표 영역 초과. 개별 문구/줄 배치를 검토하며 자동 축약하지 않는다.
3. 플레이어 이름 삽입5쪽: script11 literal5+6/7+8, script12 literal1+2, script13 literal2+3, script14 literal0 앞. 실제 이름 표현/최대 advance/합산 행 폭을 확인해야 한다. 한 글자 이름 샘플을 최대 용량으로 간주하지 않는다.
4. 전체 clone의 원본 제어/퀘스트/이름 삽입/페이지 순서·최종 RAM extent·native loader→ROM reader를 통합 검증한 뒤 남은43개를 적용한다. 발신자/제목 및 다른 내비 메일함 분기, 한글 자동 조합/이름 저장, 다른 미선택 초안 통합도 여전히 미완료다.
