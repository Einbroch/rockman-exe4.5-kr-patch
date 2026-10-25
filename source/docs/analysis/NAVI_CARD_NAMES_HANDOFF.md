# 내비 카드 이름 그래픽 한글화 후속

## 누적 산출물과 범위

원본에서 `poc/output/exe45_ko_development_navi_card_names_v1.gba`를 재빌드했다.
SHA256 `0fb840efacfb3d90bdb0a752f459e3ea2065e1911233d46f9b7a9cb6cc77a00c`.
크기 11,218,012바이트. 독립 `_repro.gba`와 전체 바이트 동일.
직전 `native_keyboard_labels_v1`에서 변경된 곳은 원본 오프셋 `0x639208`의 1,045바이트 압축 슬롯 한 곳뿐이다.
기존 텍스트 2,648개/63개 아카이브, 초기 설정 이미지, 날짜 버튼, 가나 기능 버튼 18개를 보존했다.
추가 변경은 내비 이름 그림 글자 21개이며 텍스트 유닛 수에는 포함하지 않는다.
development-draft; NON-DISTRIBUTION, needs_review, 공개 배포 승인은 아니다.

## 저장·소비 경로

- 원본 압축 묶음: `0x639208`, 1,045바이트, SHA256 `5bbe6f4b6e224c43e8d4cf16b62930e764cf3604d439feebc00deabbcd5ebeb2`.
- 해제 결과: 헤더 `00 84 0A 00` + 21×128바이트, 전체 2,692바이트.
- 각 라벨은 32×8픽셀/4bpp/네 개 타일이며 원래 배열 순서 유지.
- 원본 절대 포인터 한 곳 `0x39760` → `08639208`, 변경 없음.
- 로드 경로 `08039648`은 소스 표 `0803974C`와 대상 표 `08039770`을 공용 로더 `08029164`에 전달한다.
- 실제 원래 OBJ VRAM `06015000`에서 21개 전체 타일이 해제 결과 본체와 바이트 동일하다.
- 선택 루틴 `080395AE..080395D2`는 원래 내비 ID가 12보다 크면 2를 빼고 네 타일 단위로 선택한다. 이 코드와 캐릭터/해금/초상화는 변경하지 않았다.
- Galmuri7 원본 글꼴 7픽셀과 그림자, 원래 팔레트13의 잉크6/그림자12를 사용했다. 최대 네 음절도 32×8 안에 모두 들어간다.
- 새 압축 데이터 884바이트 + 소비되지 않는 제로 패딩으로 원래 슬롯 크기를 유지한다. 독립 디코더 왕복과 보호 헤더 동일성 확인.

입력 `translations/navi_card_graphics_ko.json`, 구현 `tools/navi_card_graphics.py`.
압축 후보 조사는 `tools/inspect_navi_card_storage.py`와 `analysis/navi_card_graphics_v1/storage_candidates.json`에 보존한다.
원본/한글 폰트 비교 `analysis/navi_card_graphics_v1/comparison.png`.

## 검증

핀 고정 Mesen의 일반 패드 입력만 사용했다. RAM·진행도·해금·초상화 치환은 하지 않았다.

- `poc/runtime/navi-card-names-v1-boot`: 처음부터/날짜/PET 환영/이름 입력 진입.
- `...-pagecycle`: 가나 세 페이지 전환과 재진입, 실제 VRAM 타일 및 BG2 맵 검사.
- `...-complete`: 원래 가나 한 글자 이름 확정, 성별/나이/직업/프로필, 록맨 선택과 초기 안내/메일.
- `...-selection`: 23 록맨, 26 롤, 29 거츠맨, 32 넘버맨. 24/27/30/33 선택 확인, 25/28/31/34 B취소, 35/36/37 역순 이동으로 록맨 복귀.
- 선택한 이름의 OAM 타일은 각각 640/644/648/672, 32×8/팔레트13이며 한글 전체 은행과 같은 VRAM 묶음을 소비한다.
- 21개 전체 은행 업로드는 매 선택/취소 후 검증했다. 17개 잠긴 내비의 실제 해금·선택·플레이를 검증한 것은 아니다.
- 실제 화면에서 네 이름과 해당 초상화/확인 대사를 검토했다. 넘버맨은 넘버맨으로 유지된다.

기계 검증 `tools/verify_navi_card_runtime.py`, 결과 `analysis/navi_card_graphics_v1/runtime_verification.json`.
잘못된 소스/문구 입력은 올바르게 거부되었다. 초기 설정 누적 감사도 통과했다.

## 재현 빌드

`tools/build_keyitem_full_rom.py --name NEW_NAME`에 다음 플래그를 모두 지정한다.

```
--gutsman-plugout --gutsman-profile --gutsman-profile-questions
--gutsman-profile-family --gutsman-profile-answers --gutsman-profile-wishlist
--input-confirmation --input-heading --input-remaining --calendar-date-save
--save-initialize --hangul-keyboard-glyphs --title-weekend-menu --startup-ui
--native-keyboard-labels --navi-card-graphics
```

패키지: `patches/exe45_ko_development_navi_card_names_20261012.zip` 및 동명 폴더.
BPS 또는 xdelta 하나를 지정 원본 ROM에 적용한다. 이전 패치 ROM에 겹쳐 적용하지 않는다.
ROM/SAV/에뮬레이터 실행 파일은 패키지에 넣지 않는다.
ZIP SHA256 `352cf396a4b482c2b77312d178a21430b0c7a0d6108ae0f6f568222574c4b855`.
BPS SHA256 `8f452798243a376624b63fe37496dd229e19e93fab276f2688a9ea11c92062ce`.
xdelta SHA256 `2609ec9059c8594f3e1c052dcaf62b62f0c5af28754fd355dae23e9125ce1b15`.
두 형식은 모두 재적용 전체 바이트 동일/확장 크기/결정적 생성/다른 원본·손상 패치 거부를 통과했다.
동봉 적용 스크립트도 전체 바이트 동일성을 검증했으며 기존 출력 덮어쓰기는 거부한다.

## 재개 지점과 남은 작업

직전 검증 지점은 `poc/runtime/navi-card-names-v1-selection/checkpoint.mss`의 록맨 선택 카드 화면이다.
동일 ROM SHA256과 `result.json`을 원점으로 지정해야 하며 다른 ROM의 상태로 테스트 결과를 이전하지 않는다.
검증 후 PET 시작 지점은 `...-complete/checkpoint.mss`에 있다.

NAVI SELECT 제목은 원래 영문이다. 실제 가나 글자판과 원본 입력/저장 코드는 여전히 그대로이며 한글 자동 조합·한글 이름 저장은 미완료다.
전체 번역 초안의 ROM 통합 및 다른 화면/대사/그래픽의 남은 일본어도 별도 작업해야 한다.
이번 완료 범위는 카드 이름 그래픽과 관련 회귀 검증이며 전체 게임 한글화 완료가 아니다.
