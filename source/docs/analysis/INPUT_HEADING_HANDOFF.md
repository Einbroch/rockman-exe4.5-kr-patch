# 입력창 제목33 — 2026-10-09

현재 작업 기준. 전체 미번역/이미지·한글입력·ROM검증 요청은 미완료다. 개발 전용 needs_review, NON-DISTRIBUTION, release_eligible=false.

## 현재 제품과 적용분

현행 `poc/output/exe45_ko_development_input_heading_v1_r2.gba`,11156628bytes, SHA256 `5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4`.
최초 `_v1.gba`/독립 `_v1_repro.gba`/도구고정 `_v1_r2.gba`의 전체bytes 동일. 실행은 최초_v1에 귀속되며 r2로는 전체byte identity로 연결한다.
이전 입력확인창ROM SHA `68260ec96c118939efa66f24f077dd06d375bdebffb8246529bcdfd6c45e87a6`는 이전 제품/일본어 입력저장 관찰 기준으로 보존한다.

`translations/input_heading_ko.json` SHA256 `3aeea8e1b6d5956e0ba2d6a635d6b2932e45c82223bd7cc46eddf7334107e884`.
신규1literal `6368E8:33:0`: `にがてな かもくは?` → `어려운 과목은?`.
거츠맨 정상질문667044:29의 기존 `어려운 과목은`과 의미를 맞춘 공용UI 초안이며 거츠맨 말투는 붙이지 않는다. 인간 문구/표현 검토는 별도 미완료.
parent16 `input_confirmation_ko.json` SHA `94272bf515ad3d177ef44a0bfffd5ddcd322165b3e9e4758ef4f778a797b6a17`의 문구/원문/상태를 완전히 유지한다.
누적2549literal/60선택·672원본유지archive. Catalog732/31907: 미선택일본어27499/기타1859/errors0.
현행catalog `analysis/full_scope_input_heading_v1_r2/`; 최초 `_v1/`은 이전 도구해시 기록이다.

## 적용 방식과 빌드

기존 mixed-renderer 공용archive 체인을 유지하고 신규33만 mmbn45s/mono로 선택한다.
`tools/input_heading.py`는 parent16 identity/원문/언어/제목10cell·한줄·control skeleton을 검증한다. registry `input-heading-v1`은 mono80px를 별도로 지정하고 mono/preset provider가 없으면 빌드를 거부한다.
제목의 실제 호출은 width2/height10이며20개의64byte glyph를 전송한다. 첫10개의8x16cell만 제목에 보이고 나머지10은 native blank다. 대사 normal renderer와 혼동하지 않는다.
F9FC 한글은 기존 mono font provider를 사용한다. 폰트 새제작/키보드/입력 ABI 변경은 없다.

새 name으로 원본에서 재현:
`python -X utf8 tools/build_keyitem_full_rom.py --name UNIQUE --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading`
이미 있는 work/output는 덮어쓰지 않는다. 원본ROM SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변.

## 검증

`analysis/input_heading_v1/runtime.json` PASS, SHA `09757c83f23ad0dc24e5e837bbddb89005b7b078217321dddbbaa636f5c1a081`.
화면 `analysis/input_heading_v1/heading_pages.png`는 원문/한글/native No복귀 비교이며 직접 확인했다.
`report_input_heading.py`가 원본 Expected Write·비중첩·전체diff/append/header/재현2빌드를 감사한다. 기존16unit/254공용scripts와59다른archive payload, normal/big/mono font banks·advance·주요이미지/keyitem39가 동일하다. 공용15root와 원본공용archive 보존 PASS.
새 ROM의 자체 cold/profile/넘버맨/native save58/cold continue→거츠맨PET→인터넷→정상질문29 경로에서 제목33을 확인했다. 이전ROM checkpoint/save를 들여오지 않았다.
stage0201C800→VRAM0600B800의1280bytes는 정확한 한글/원문문장부호/공백20cell와 같고, 실제 glyph-provider 선택도 일치한다.
BG2/charbase8000/mapF000/palettebank10, 원점(24,32),10visiblecells의1280pixels가 native palette 기반으로 정확히 일치한다. No복귀 후 동일제목crop 유지 PASS.
일본어「あ」입력/B삭제/재입력→한글확인창→No(편집값 유지·record 미확정)/Yes(019be57ee50000·반응93) PASS.
`analysis/input_heading_v1_cpu.json`: native copier를 실행하는 big/mono 전체11172글자씩 및경계/tint/legacy22390벡터 PASS. CPU fixture는 실제화면검증과 별도다.
heading7/confirmation10/keyitem4/profile5/catalog1=27fixture PASS;748Python AST PASS. 현행r2의748Python tool pins와 실제hash drift=[]을 PowerShell로 비교했다.
정상save-commit step13 script58, native QA전용65536byteSAV SHA `fb82d51b06fadc2d37d3e87990edc0d1104b5abb9ee99df461803769915f65ca`; native coldcontinue state_origin=null/complete=true. 이 저장은 새 답변입력 전의 회귀다.
이전제품 `input_entry_v1/native_input_persistence.json`의 일본어4글자 영구저장증거를 새 제품의 입력값저장 증거로 자동이전하지 않는다.

## 다음 작업 / 미완료

공용 invalid-input11, 다른 제목20..42와 실제 진입분기, NAVISELECT 확인창, 일본어 입력그리드/편집·결정 라벨은 아직미번역이다.
다른 제목은 같은 lookup/mono/지움 경로 및 의미를 확인한 범위에서만 확대한다. 가족호칭의 형/오빠·누나/언니처럼 입력주체에 따라 달라지는 의미는 기존 대화문맥과 함께 판별한다.
한글 입력은 native byte copier의E5/98중간절단·marker01/각record 경계·정규화08032AC6/02014E74·descriptor writer/정상대화재표시·native영구저장·기존save호환을 함께 설계해야 한다.
원래 byte writer34FA0..35050/32AC6..32AD8은 source와동일.32AD8..32ADC는 relocated commonroot data literal이며 code동일성 검사에 넣지 않는다.
전체미번역/이미지·RTC/실제상점·인간검토/배포검증은 미완료다.
