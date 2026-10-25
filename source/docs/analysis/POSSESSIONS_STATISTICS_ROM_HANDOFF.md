# 소지품 통계 제목 ROM 적용 — 2026-10-09

개발 초안 / NON-DISTRIBUTION / needs_review / release_eligible=false.
사용자의 전체 미번역 번역·반영 요청은 아직 완료되지 않았다.

## 적용본

ROM: `poc/output/exe45_ko_development_possessions_statistics_v1.gba`

SHA256: `f932c28e3de1459424eee2407be1a75b5bcb3c4ca2f33fe202c7a2a1f8b1c556`.

6368E8:80:0의 네 제목을 `컵 / 크레딧 / 버그 조각 / 대전 전적`으로 번역했다.
크레딧은 기존 저장 화면, 버그 조각은 기존 보상 문구의 개발 용어와 일치한다.
원본 literal1개에 네 제목이 들어 있다. 누적2,350선택literal/59선택·673원본유지archive다.
직전 빈 키 아이템판의 나머지58archive payload/입력/이미지/‘통신’은 보존했다.
원본 ROM은 변경하지 않았다.

## 적용 구조와 오류 정정

새 `possessions_statistics_ko.json`은 부모 `calendar_frequency_names_ko.json`12문구를
해시 고정하여 그대로 이어받고 새64칸 literal만 추가한다. 기존 입력을 덮어쓰지 않았다.
네 행 각각16칸이며 앞10칸만 BG2 타일맵에 표시된다. 여섯 숨은 공백은 그대로 유지했다.
4096바이트 stage0201B800→VRAM0600A000..AFFF를 유지한다.
숫자/Z와 대전 수치 소비자81/82의 바이트와 별도 stage/VRAM은 변경하지 않았다.
15개 archive root를 동일 새 pool로 옮긴다. 한국어는 기존11172음절 fixed-cell-big 공급자를 사용한다.
새 폰트 전략/새 RAM 버퍼/추가 렌더 후킹은 없다.

초기 메타데이터의 `prefix64` 해석은 잘못이었다. 원본 시작0x40은 일본어 カ의 글자 코드이며,
64칸은 호출부의 width16×height16 조건이 지정한다. 실제 번역 바이트에 잘못된 접두어를 넣은 적은 없다.
정확한 compiled literal+E5와 실제 호출 경계를 검사하여 보고서를 수정했다.
정책 문장만 정정한 뒤 fresh `_current_repro_r2`를 생성했다. ROM 바이트가 완전히 같음을 검사한 후
최신 builder 생성 manifest를 main의 같은 ROM에 연결했다. 첫 manifest는
`possessions_statistics_v1/initial_build_manifest.json`에 보존하고 `manifest_refresh.json`에 이유/해시를 남겼다.
runtime의 적용 ROM 해시는 변하지 않았으며 기존 세이브/체크포인트는 조작하지 않았다.

## 검증

- 새 제목5, 달력20, keyitem9, archive4, LZ10 literal3 테스트 PASS (41개; 별도 frequency3 재검사도 PASS).
- primary builder source/제어코드/roundtrip/글꼴/전체 최종 쓰기·겹침·원본 유지 검사 PASS.
- 자체 새 cold→넘버맨 저장58→체크포인트 없는 cold 이어하기→거츠맨 정상 선택 PASS.
- 거츠맨 인사2페이지/PET8화면22literal·선택커서·취소/넘버맨 귀환3페이지 회귀 PASS.
- 정상 소지품 진입과 빈 아이템 B복귀 각각64decoded cells/4096바이트 stage→VRAM 일치.
- 실제 BG2control1E4A/native scroll0/4행 타일맵/원점32,24 검증.
- 각각40visible cells·5,120픽셀 전체(공백 포함)가 font/tint/palette/source 색 역할과 일치.
- source tint4→roles4/5/6 검증; 일본어 잔상/칸 밀림 없음. 숫자/Z/전적 source stage·VRAM 불변.
- 기존 빈 아이템 LZ/RAM/lookup/CPU/font/VRAM/픽셀·180프레임 대기/B/재진입 PASS.
- 날짜/종류/확인/삭제 및 동적1회만의 RAM/font/VRAM/pixels 대표 회귀 PASS.
- 달력 검사 초기 cursor 가정은 실제 OAM16(type)/OAM2(confirmation)으로 수정했다.
  숫자1은 Hangul encoder가 아닌 기존 native02를 사용하도록 검사 코드만 수정했다.
  ROM 변경이나 픽셀 허용오차 추가는 없었다.
- 합성 소지품2화면과 단일 진입 화면을 직접 확인했다.
- main/repro/current_repro/current_repro_r2 동일SHA. 최종695Python AST/tool pins drift=[].
- 원본 불변/헤더/append/최종 계획 쓰기/번역 입력 해시 감사 PASS.
- catalog732/31,907literal/parse errors0: 선택2,350, 미선택일본어27,698, 기타검토1,859.

증거: `possessions_statistics_v1/runtime.json`, `statistics_runtime.json`, `calendar_regression.json`,
`final_identity.json`, `possessions_statistics.png`, `empty_item.png`.
새 이름 재현: `possessions_statistics_v1/rebuild.ps1 -BuildName <새 이름>`.

## 다음 작업과 미해결

키 아이템39개 초안 중 나머지38개는 ROM 미반영이다. 전체2477바이트/원본1291바이트의
차이는 기존 동일 설명10/11 공유45바이트만으로 해결되지 않는다. 두 RAM 소비자02020800/02031000의
수명·중첩·재배치 또는 다른 표현 설계를 검증해야 한다. 후자의 정상 화면 도달도 아직 미검증이다.
한글 입력/편집→커밋 레코드→모든 재표시→새 실행 영구 재로딩→기존 세이브 호환성은
전역 완료의 가장 중요한 미해결 조건이다. 날짜·요일·휴일/전체이미지·inline·fixed population,
RTC/기존 시각차이/인간 번역·화면 검토도 남는다.
이번 전적 수치는0인 경로만 정상 관찰했다. 비영 전적/전체 달력/알림 회귀를 완료했다고 주장하지 않는다.
catalog 집계는 전체 ROM 번역 완료율의 분모가 아니다.
