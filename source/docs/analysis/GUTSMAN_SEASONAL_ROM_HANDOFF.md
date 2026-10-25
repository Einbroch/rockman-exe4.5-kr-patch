# 거츠맨 기념일·생일 대사 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

ROM: `poc/output/exe45_ko_development_gutsman_seasonal_v1.gba`.
SHA256 `6af4aad8403d878fc1a4ebf035cb0e0b665c721e5aacfd1a4a66e3a3c8437b56`.
이전 seasonal_trio_v1의 29개 선택 archive 및 번역/이미지 자산을 유지하고 66A234를 추가했다. 누적1,461선택 literal,30선택·702원본 유지 archive.
신규49 literal 중47개 번역 문구/2개 원본 유지 인용 부호이다. 새해·절분·발렌타인 성별 분기·히나마쓰리·5월5일·칠석·성탄절·연말·생일·창립 기념일·이벤트 안내를 포함한다.
기존 저장 대사의 후보 말투 ‘거츠/거스’를 사용했다. 문화 설명과 말투는 검토 필요 초안이며 배포 승인된 번역이 아니다.
‘거츠 머신건’은 장비 이름 초안 ‘거츠머신건’과 같은 기술을 가리키는 대사 내 띄어쓰기 표현이다. 정식 명칭/용어·표현 승인은 아직 없으며 리뷰 대상으로 남긴다.

## 보호와 빌드

원본66A234:1395bytes,21script slots,root038144,source payload SHA `9b548394870d71a7f4db521f21c026c6be3568eb8c930de276a7c81153dc9e71`.
intro665EB8의 화자 원문으로 거츠맨을 식별했고 같은60byte native Navi group의 +52 seasonal slot에 연결된다.
source/IDs/21slots/명령/줄 수/모든 숫자/global22 성별 분기/anniversary buffer 및 반복/인용 부호를 보존했다. RTC·게임 날짜·저장 형식·이름 입력 코드는 변경하지 않았다.
3줄/132px 채택 범위 내이며 전체49 literal에서 최대128px. 모든 글자 인코딩과 glyph 공급, native/semantic/binary roundtrip 검사 통과.
자산 `translations/gutsman_seasonal_ko.json`; source 기반 직렬화와 수동 초안은 `tools/draft_gutsman_seasonal.py`에 있다. 기계적인 문장 변환이 아니라 개별 문맥 초안을 source stable ID에 연결한 것이다.
이전 누적 flags와 `--numberman-seasonal --seasonal-companions`를 유지하고 `--gutsman-seasonal`을 더해 원본에서 재생성한다. 기존 patched ROM을 입력으로 사용하지 않는다.
관련 테스트95개 통과. 재빌드와 source/tool identity는 `analysis/gutsman_seasonal_v1/final_identity_audit.json` 참조.
최종 도구 정합용 독립 빌드 suffix는 `_current_repro_r2`이다. 먼저 생성한 `_current_repro`는 report 보강 전 도구 identity로 남겨 두었으며 최종 감사에 사용하지 않는다. 원본 및 이전 후보/실패 시도/검증 자료는 모두 보존했다.

## 실제 실행과 미검증 범위

`tools/run_gutsman_seasonal.py`는 자체 cold 시작→넘버맨 최초 선택→정상 게임 저장→checkpoint 없는 cold 이어하기→내비 선택까지 controller 입력만 수행한다.
같은 ROM의 넘버맨 새해3페이지 회귀와 거츠맨 선택/대사 진행을 관찰한다. 정확한 신규 문구별 검증 결과는 `analysis/gutsman_seasonal_v1/runtime.json`, 화면은 `analysis/gutsman_seasonal_v1/new_year_pages.png` 참조.
거츠맨 새해2페이지 및 종료와 넘버맨 새해3페이지 회귀 검사 모두 통과했다. 자체 저장 성공script58을 확인하고 64KiB native save가 FF 초기 상태에서 `83c1913553524a5903b6aa1e0c537196528d5d7512b9ae3be79ef0672de603c8`로 바뀐 뒤 유지됨을 검사했다. 한글 이름 저장 성공을 뜻하지 않는다.
font CPU read→ROM glyph→OBJ VRAM→화면 픽셀, 실제 포인터/stream, 페이지 순서·빈 영역 지워짐·종료를 검사한다. RAM/ROM 직접 쓰기·날짜 변경·script alias 없이 실행했다.
다른 기념일 날짜/성별 분기/동적 이벤트 이름 출력은 아직 실제 실행되지 않았다. 정상 새해 결과를 다른 모든 분기의 검증으로 확대하지 않는다.

전체 catalogue backlog는 `analysis/full_scope_gutsman_v1/inventory.json`, `literal_backlog.json`이다. 미선택 일본어 포함28,531개/기타 미선택1,915개. 전체 완역 분모나 완료율이 아니다.
다음 대사 묶음: 윈드맨66F78C. 전체 그래픽/inline/string population, 한글 이름 입력→committed record→모든 재표시→영구 재로드→기존 save 호환과 이전 대기 화살표53pixel 차이는 여전히 미해결이다.
