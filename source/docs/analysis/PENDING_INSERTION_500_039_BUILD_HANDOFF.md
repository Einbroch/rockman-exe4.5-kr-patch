# 039 실제 통신 안내500 적용 및 대표 런타임 종료

현재 권위는 `analysis/pending500_039_v1/batch_status.json`이다. 이전 `pending_insertion_500_039_communication_words_v1/batch_status.json`은 source-only 단계 이력으로 보존한다.

## 현재 결과

- ROM: `poc/output/pending500_039_v1.gba`, SHA256 `bfb80e29c8f72ed4595a0453ca43fa6445a94d98d6d2054158f886fde2b38430`, 12,930,632bytes, 누적20,622ID. 독립 `_repro.gba` 바이트 동일. 원본에서 누적 재생성한 primary이며 이전038은 비교용이다.
- 새500 /372scripts /17 communication-help archives. 기존644 consumer 보존, 총661. 기존 원본압축/table/shared4493C literal 불변. 캐리0. 문구변경0/음절내줄바꿈0, 기존 어절LF만. 정규 ROM미반영9,924는 전체게임/이미지 총잔여가 아니다.
- `integration.json` SHA `aa61ea43ae0bc3044802828158ac1d0c3873011de5fb8c810d7ef8d022fc283d`: 전체 source writes/append/header/참조/기존consumer bytes·metrics·owner/정확500/재현/CPU fixture 동일 PASS.
- `corruption_v1.json` SHA `a015bfc9241940e9dcae0bfdcadc42955922a38791f8bad0ef6548c7795f0398`: 정상 control 허용 +실제 이미지42손상 거부. 메모리 안에서만 변형, ROM파일쓰기0.
- `normal_path_v1.json` SHA `b16109b80639a49aadddb905595bdebd90429685e56cf85b8706285e35cba5d8`: 자체039 coldboot→정상16구간, 실제 원래field nativeLZ/기존NPC한글stream/닫기·이동 PASS. 도구 console의 PASS038은 상속된 출력문구일 뿐, 보고서 ROM해시·scope는039다. 핀된 도구를 표시문구만 바꾸려고 편집하지 말 것.
- `communication_runtime_v1.json` SHA `ec8dc4b0ed1f62abb1bf70264a50ed79dc729460b121acff0a1c5ad93b361873`: 자체039 정상16이후 통신8입력구간, 자연6F56B8 LZ1723bytes→02024000 원본 유지→실제448BC/4F7B6/4FB4C nestedLR4F7BD+저장outer448C7→새ROM clone→한글6F56B8:16:0→font읽기/OBJ/스크린픽셀/정확EDFF hold→B PET복귀 PASS. 강제PC/root/caller, readalias, gameRAM/ROM쓰기0. 실제 ROM의 원래initializer tail을 실행했고 CPU fixture의 skip은 GBA에 적용되지 않았다.
- `agent_visual_v1.json`: 실제7화면 직접검토, 사람승인/모든500화면검토 아님. 새 안내는 `록맨 에그제4와 칩 / 게이트를 연결해서 / 대전하는 모드야`, origin92/110, 3행. 원래source6F56B8 Navi0/13/14 공유이므로 단일Navi정체를 payload만으로 추정하지 않는다.

## 제품 경로/CPU 한계

`build_layout500_039_v1.py`→`build_development_patch_039_v1.py`와 `communication_rom_product039_v1.py`가 주 경로이다. 새 입력registry `analysis/pending_insertion_500_039_communication_inputs_v1/manifest.json`은 원본TPL+핀된 정규 authored 초안+선택된 LF로17asset을 재생성한다. 원본부터038 전체를 재생성하고 검증된038투영/hash로 기존whole-image gate를 유지한다. one12B 공통stub만 합성한다.

`communication_rom_selector039_v1.py`는 root024000+innerLR+u8script+저장outerLR+perarchive scriptbound+native전체바이트로 제한한다. 전역scene조건 완화/별도448BC hook/공유4493C 목적지 변경 없음. 전체23table/21unique원본 중 선택17은 모든21과 prefix모호성 없음.

CPU `selector_cpu_v2.json` 2,818조건: 선택유효2,006/미선택유효472/오류340. 원래0090C·00956 wrapper를 실행하되 두 CpuSet만 모델링하고 common initializer4FB90..4FC20은 epilogue로 skip한다. 전체초기화/타이밍/오디오 증거가 아닌 PREFIX fixture다. GBA대표실행이 별도실제전체초기화 경로를 확인한다. 초기 v1은 continuation의 두번째 preset copy를 만났는데 모델이 없어서 실패했고 모든 도구는 보존했다. v2초기진단의 even-PC 전환 오류는 모델의 ThumbPC지정으로 수정한 후 보고서를 동결했다. 핀된 도구 편집 금지.

## 재개

모든 자체명령/Mesen 종료. 배포 BPS/xdelta/ZIP 생성0, 사용자mGBA/원본/저장 불변. 최신 정상039 상태는 `poc/runtime/pending500-039-communication-v1-08/checkpoint.mss`와 같은 폴더 `result.json`이다. 통신취소 후 PET알림이며040 등 다른ROM에로드금지. 입력 recipe만 다른ROM 자체coldboot에서 재사용 가능하다.

040 정규초안 정확500 준비를 계속하되 현재661 consumer/모든owner/source압축/공유소비자를 보존한다. 현 통신fixed-cell `mmbn45s` 일본어옵션은500에 포함되지 않았고 실제로 일본어 표시됨을 확인했다. 이 라벨의 별도소비자 분석/추가 help page·재진입·분기검증도 남는다. 동일039의 이미 확립된 경계를 이유 없이 반복 조사하지 않는다.

전체게임/모든500스크린/모든Navi 자연획득, 통신파트너협상·멀티플레이·serialtraffic·실기·오디오, 한글입력확정/저장/재표시, 일본어자판/지역명/이미지잔여/사람검수는 미완료이다. 배포 패치는 다시 요청받기 전에는 만들지 않는다.
