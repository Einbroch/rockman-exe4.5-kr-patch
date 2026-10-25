# 공용 입력 UI21 ROM 반영 — 2026-10-11

개발 후보: `poc/output/exe45_ko_development_input_remaining_v1.gba`,11156960bytes.
SHA256 `56a26c612a2fbfc08a57fb9ae4c9e3d43dcbaaddccfd9f654b16d64bf3369a15`.
이전 검증 ROM `input_heading_v1_r2`를 덮어쓰지 않았다. 새 ROM의21문구 화면/저장 회귀가 끝나기 전까지 runtime 기준을 자동 교체하지 않는다.

## 번역과 빌드

`translations/input_remaining_draft_ko.json`의21개 수동 초안을 선택했다.
6368E8:11 오류 안내,21/23..32/34..42 제목20개.20/22의 형/오빠·누나/언니 문제는 원문 유지한다.
‘불편한 사람은?’과 ‘지금 원하는 것은?’ 등은 의미/표현 인간 검토 대기다.
입력 오류 안내는 `입력 내용이\n적절하지 않습니다`로 두 줄 배치하며 keyWait/end를 유지한다.
기존 parent17을 유지해 common38선택literal이 된다. 누적 제품2570선택문구/60archive·672원본유지archive.
원작 일본어 자판/입력 record ABI와 후보F8 저장코드는 이번 변경 대상이 아니다.

번역 authority는 delta JSON, parent authority는 기존 input_heading JSON이다.
누적 `analysis/input_remaining_v1/selected_asset.json`은 명시적 빌드가 재생성하는 read-only 파생 입력이다.
이 파일을 직접 수정하지 않는다. delta와의 불일치, parent 변경, ID누락/중복, 원문/언어 변경, 범위 초과는 빌드 거부다.
builder의 `selected_scope`에서 input-remaining-v1을 등록하며 기존 registry의 heading scope를 상속해20mono/1normal을 명시한다.

원본에서 재빌드:

```powershell
python -X utf8 tools/build_keyitem_full_rom.py --name UNIQUE --gutsman-plugout --gutsman-profile --gutsman-profile-questions --gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist --input-confirmation --input-heading --input-remaining
```

이미 있는 이름을 쓰면 artifact 보존 오류가 난다. 원본SHA `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8` 불변.
도구5개 py_compile, 신규contract5/기존heading7/confirmation10 테스트 PASS.

## 증거 경계

`analysis/input_remaining_v1/artifact_audit.json`: Expected Write/비중첩/전체diff/append/header, common15root,
binary/semantic roundtrip/control,234기존script/59다른archivepayload, normal/big/mono font/advance, 주요이미지/keyitem39 보호 PASS.
font/consumer geometry는 빌드가 검사했지만 실제 화면을 검사한 것과 다르다.

`poc/runtime/input-remaining-v1-coldboot`는3capture를 완료했으나CAPCOM logo 단계만 관측했다.
동일ROM ancestry로 이어진 `input-remaining-v1-title`의3capture에서 타이틀 ‘처음부터’ 선택을 관측했다.
Mesen SHA `af60a18859e3253f09c8fd32f6b1c04637efbd98780f1427dd94d4629474f640`, 정상controller/readonlysnapshot, 이전ROM state 미사용.
두 route artifacts 및checkpoint ancestry hash 검증 PASS. 새로운21문구를 표시한 증거는 아니다.

`create-kr-patch`의 원본보호/재현빌드·소비자 구분 기준을 적용했다.
독립 `_v1_repro.gba` 재빌드 완료: 같은SHA256 및11156960bytes 전체byte identity PASS. 재빌드 후 ROM 정적 감사 재실행 PASS.
전체catalog backlog는 아직 갱신하지 않았다.
새문구 정상caller/mono·normal provider/VRAM/pixels/지움·취소복귀, 저장/freshcontinue 및 인간 검토 미완료.
전체미번역/이미지/한글입력·저장/배포는 미완료다. NON-DISTRIBUTION; needs_review; release_eligible=false.
