# 넘버맨 저장 문구 후속 실험 — 2026-10-05

functional-poc; development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

## 추가 번역과 보호 범위

`poc/output/exe45_ko_development_numberman_save_poc_v1.gba`
SHA256 `7431216a52a62898fad57984cf17b6bd5566c9eb26282b30e9886f9666100345`.
추가16개, 누적1,145선택 텍스트 /15기존 그래픽 /21선택·711미선택 archive. 전체 완역률이 아니다.
`four_navi_save_ko.json`은 이전 록맨/롤/거츠맨53단위를 필드 동일하게 유지하고 넘버맨55..59의16단위만 추가한다.
script0 checkNaviAll jumpIfNumberMan=55, 확인55/덮어쓰기56/저장 중·실패57/완료58/잘못 변경된 데이터59이다.
원문です/ます에 맞춘 정중한 초안: `저장하시겠어요?`, `저장이 끝났어요`.
의미/말투·독립 리뷰·인간 승인 대기이며 기술 검사 통과가 배포 승인이나 공식 한국어 명칭 승인은 아니다.
원본 줄 수·마지막 빈 줄·선택 공백, flag3651/7686·callSave·성공58/invalid59·실패/재시도 분기를 보존한다.
56은 세 줄 안내→keyWait→clearMsg→별도 선택 행. 기존 standalone_choice_rows 검증을 사용하며 안내/선택을 합치지 않는다.
variant `four-navi-save-v1`:69단위/25scripts/14prompt groups/2standalone rows.
원본6DA21C9008bytes·95미선택slots, 이전115slots(55..59외)·다른20archive payload·저장 제목6333A4의256bytes 보호 검사를 적용한다.
새 코드 hook/저장 포맷/이름 입력 변경 없음. 기존 누적 flags에 `--numberman-save` 추가하며 retained `--gutsman-save` 없이 선택하면 거부한다.
원본/기존 ROM/캡처/테스트 save는 보존한다.

## 정적·재현 검증

관련62unittest 통과(17.260초). historical fixtures는 새 ROM 실행 증거와 구분한다.
정적69단위 normal-font 공급,95미선택slot·archive round-trip 검증 통과.
이 normal-font 검사는 fixed-cell label의 실제 glyph 공급 검증을 대신하지 않는다.
main/_repro/최종 _current_repro_r2 동일 SHA,현재439Python 도구 drift=[]와 원본 SHA 보존 최종 검사 통과.
_current_repro도 같은 ROM이지만 최종 캡처시점 report 수정 전 tool manifest다. 이전 후보도 보존한다.
`numberman_save_poc_v1/final_identity_audit.json` 참조.

## 실행 증거 계약

새 ROM own-cold→date→profile→navi-menu→select-numberman→intro 경로의 정상 right3회로 넘버맨을 선택한다.
다른 ROM state/RAM/save import 없이 같은 ROM의 로드 이전 checkpoint에서 저장 메뉴에 진입한다.
`report_numberman_save.py`는 정확한 ROM/도구 hash·ancestry·native archive root/script·glyph CPU read→OBJ VRAM→pixel mask를 확인한다.
확인55, 세 줄 안내56, 별도 선택56, 전원 경고57, 완료58의 정상8단위와 실제 disk save·덮어쓰기 아니요를 검증 대상으로 삼는다.
전원 경고는 새 native save의 frame-step 관측에서 완성된3행을 검사한다. 수동 RAM/코드/wait 수정은 없다.
검증 결과는 `numberman_save_poc_v1/save_runtime.json`, `save_pages.png`에 기록한다.

## 실제 실행 결과

정상8단위의 actual stream→CPU glyph read→OBJ VRAM→screen pixel 검사, disk save와 overwrite ‘아니요’ 검사가 통과했다.
save-enter step11(script55,3단위), overwrite step6(script56 안내1단위)/step9(선택2단위), save-commit step9(script57 전원 경고1단위)/step13(script58 완료1단위).
이 다섯 페이지와 step11 ‘아니요’ focus/step12 PET 복귀를 직접 화면 검토했다. 기존 `저장/시간/칩/컵/크레딧/0개`도 유지한다.
같은 정상 save 실행에서 step8은19glyph의 draw/VRAM 기록은 있으나 완성 화면의 role 색상이 일치하지 않았다.
steps9..12는19glyph/2,592pixels의 glyph/VRAM/화면이 일치했다. 최초 실패 프레임을 보존하며, ROM/control/wait를 수정하거나 별도 save를 재실행하지 않았다.
step9를 완성된 전원 경고의 증거로 채택했다. 육안상 거의 완성된 이전 프레임을 픽셀 일치로 주장하지 않는다.
첫 save는 새 전용64KB allFF 파일을 정상 callSave로 갱신해 완료58로 전환했다. snapshot·hash는 save_runtime.json에 있다.
overwrite ‘아니요’의 해당 파일 hash 불변, 다른 모든 테스트 save 불변을 확인했다. 기존 save 호환/영구 재로드 증거가 아니다.

## 남은 완료 위험

57:1..4/59:0..3의 오류 관련8단위는 정적 구조·인코딩·글꼴·레이아웃만 검증하며 실제 저장 오류를 유발하지 않는다.
넘버맨 일반 소개·PET 대사 및 다른 Navi 문구는 아직 미번역이다.
한글 이름 입력/편집/저장·재표시 소비자 전체와 기존 save 호환성이 가장 큰 미해결이다.
영구 재로드·모든 Navi·전체게임·RTC/alarm·오디오·실기·독립 의미 검토/인간 승인·배포는 미완료다.
완역/출시후보/새 save 호환 지원으로 승격하지 않는다.
