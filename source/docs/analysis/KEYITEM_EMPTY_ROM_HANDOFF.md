# 빈 키 아이템 안내 ROM 적용

개발 초안 / NON-DISTRIBUTION / needs_review / release_eligible=false.
전체 미번역 번역 요청은 아직 완료되지 않았다.

## 빌드

ROM: `poc/output/exe45_ko_development_keyitem_empty_v1.gba`

SHA-256: `ab7182e1921f12c58031d2cfce2457587b09d657527c8476e8a9a3388c12f6b6`.

`709408:32:0`에 `키 아이템이\n1개도 없다・・・`를 반영했다.
원본 숫자1, 줄바꿈, 말줄임표3개, waitHold와 화자 없는 메시지 형태를 유지했다.
선택 문구 2,349개, 선택 archive59개, 원본 유지 archive673개.
기존58 archive의 모든 compiled payload 해시와 기존 번역 입력을 보존했다.
원본 ROM을 입력으로 기존 누적 빌드 플래그에 `--keyitem-empty`를 추가한다.

## 메모리 증가 없이 적용한 방법

원본 scripts10/11은 완전히 동일한45바이트 설명이다.
원본 엔진0804FB74..7C는 ID*2의16-bit 시작 오프셋을 읽고 root에 더한다.
다음 스크립트 오프셋으로 길이를 결정하지 않는다. 이 코드의 바이트와 역어셈블 결과를 검사한다.
원본에서도 IDs21..32가 같은 시작을 공유하며, IDs45..48도 같은 시작을 공유한다.

한국어 안내만 컴파일하면1,318바이트다. 정확히 일치하는 scripts10/11의 시작만 공유해
45바이트를 절약하면1,273바이트가 된다. 원본 해제 크기1,291보다18바이트 작다.
문구 축약, 새 RAM 버퍼, 코드 후킹, 원본 목적지 변경은 없다.
02020800과02031000 두 목적지 모두 원본보다 많은 바이트를 쓰지 않는다.
이는 최대 버퍼 용량이 확정되었다는 주장이 아니라 **기존 사용 범위 이내** 정책이다.

일반 TextPet TPL/바이너리 역변환은 저장 공유 전 단계에서 검증한다.
공유 후에는 네이티브처럼 시작 오프셋별 실제 스크립트를 해석하여
전체49개에 대해 공유 전후 소비 바이트 동일성을 검사한다.
원본의 빈 메시지 alias IDs21..32 외37개 소비 스크립트는 원본 바이트와 동일하다.
TextPet이 공유 오프셋의 앞 ID를 빈 span으로 내보내는 성질을 번역 유실로 착각하지 않는다.
manifest의 `native_storage_sharing`와 최종 current_repro의 `textpet_roundtrip_stage`를 참조한다.

원본 compressed blob은 그대로 남는다. adopted catalog의 두 root034A2C/04C5E8을
동일한 새 aligned literal-only BIOS LZ10 저장 블록으로 원자적으로 갱신한다.
독립 디코더/자체 디코더/최종 ROM 재해제 일치와 모든 계획 쓰기·겹침·원본 유지 archive를
primary builder가 검사한다.

## 검증 상태

- 신규 keyitem 관련9개, 달력 관련23개, archive4개, LZ10 literal3개 테스트 PASS.
- main/repro ROM 해시 일치 PASS.
- catalog732 / 추출 리터럴31,907 / parse errors0.
- 현재 선택2,349 / 미선택 일본어27,699 / 기타 검토1,859.
- 정상 cold→저장→cold 이어하기→거츠맨→소지품→빈 안내 PASS.
- 네이티브 새 LZ 블록 로드→전체1,273바이트 RAM 일치→script32 독립 lookup→CPU font reads→OBJ VRAM→화면 픽셀 PASS.
- 진입/재진입 각각15글리프·2,016픽셀 일치; 대기180프레임 데이터 유지, B→소지품10 복귀, 닉네임/일정 레코드 불변 PASS.
- 거츠맨 PET8화면22리터럴/Yes-No focus·B·복귀, 거츠맨 인사2페이지, 넘버맨 복귀3페이지, 저장58/cold 이어하기 PASS.
- `keyitem_empty_v1/empty_item.png` 합성3화면 직접 확인. `runtime.json` PASS.
- Python689개 AST PASS.
- 달력 날짜/종류/확인/삭제 및 동적 `1회만` RAM/font/VRAM/pixels 대표 회귀 PASS (`keyitem_empty_v1/calendar_regression.json`). 이전 전체 달력·알림·다섯 빈도 검증을 자동 이전한 것은 아니다.
- main/repro/current_repro/current_repro_r2 모두 동일 SHA. 최종 current_repro_r2의689개 도구 핀 drift=[]/번역 입력 해시/원본 불변/헤더/append/최종 계획 쓰기 감사 PASS (`keyitem_empty_v1/final_identity.json`).

재현: `analysis/keyitem_empty_v1/rebuild.ps1 -BuildName <새 이름>`.
원본 기반 부모 레시피 해시를 확인하고 `--keyitem-empty`만 추가한다.
첫 보고서의 loader 시점 가정은 실제 callback 결과로 바로잡았다. 로드는 소지품 소개10에 들어갈 때가 아니라
키 아이템 확인 A를 누른 다음 발생한다. ROM/입력/허용오차 변경 없이 실제 empty 경로의 로드 기록으로 검사했다.

## 미해결

다른38개 키 아이템 리터럴은39개 초안에 들어 있으나 이번 ROM에는 반영하지 않았다.
전체 초안2,477바이트는 이 중복45바이트 정리만으로 원본 범위에 들어가지 않는다.
02031000 별도 소비자의 정상 도달/런타임 증거도 이번 범위에서 아직 없다.
같은 압축 스트림과 BIOS 래퍼이며 저장/해제 크기는 원본 범위 이내지만, 이를 별도 소비자 화면 검증 완료로 세지 않는다.
화면에 없는 내용은 정적 검증과 런타임 검증을 구분한다.
전체 이미지/inline/fixed population, 날짜·요일·휴일, 기존 시각 차이, 인간 검토가 남는다.
한글 입력/편집→커밋 레코드→모든 재표시→새 실행 영구 재로딩→기존 세이브 호환성은
여전히 전역 완료의 미해결 조건이다.
