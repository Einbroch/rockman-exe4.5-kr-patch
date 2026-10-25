# Rockman EXE 4.5 한글화 작업 재개

이 프로젝트를 이어받을 때는 `CLAUDE_CODE_HANDOFF.md`를 먼저 읽는다.
진행 상태의 단일 권위는 다음 파일이다.

`analysis/pending500_070_v1/batch_status.json`

- 실제 실행 가능한 최신 ROM은 `poc/output/pending500_070_v1.gba`이다(30,359 ID, repro 바이트 동일). 067=PET 상단 요일, 068=한글 자판 설치, 069=고정 칸 출력(입력창·확인창) 한글 표시, 070=낱자모 확정 막기. 070부터 정상 진행 레시피 2구간은 「가」를 입력한다(`run_normal_keyboard070_v1.py`); 041 대비 비교는 의미가 없고 070 자체 실행이 새 기준이다.
- 065는 사용자 스크린샷 텍스트 수정(batch_label_v4), 066은 그림 전용 단계다(`tools/graphics_stage066_v1.py`+`graphics_fix_v1.py`, 생성 `make_graphics_stage066_v1.py`, 정상 진행 `run_normal_graphics066_v1.py`). `graphics_fix_v1.py`는 066 해시로 고정되어 있으니 새 그림 수정은 `graphics_fix_v2.py` 이후에 넣는다.
- 한글 자판: 068·069로 ROM 설치, 실기(격리 Mesen)에서 「한글」 입력·확정·확인창 표시 확인. 형식 A v3(`tools/hangul_record_v3.py`), 훅 `tools/hangul_keyboard_hooks_v1.py`(+v2 fcopy). `hooks_v1`·`graphics_fix_v1`처럼 빌드 명세가 해시로 고정한 파일은 고치지 말고 새 버전을 만든다. 상세는 `analysis/HANGUL_KEYBOARD_HANDOFF.md` 맨 위 절.
- 041~065를 ROM에 적용했다. 정규 draft 미반영은 187개다(분류는 상태 JSON 참고).
- 063·064는 창 폭·칸 수에 맞춰 문구를 다듬은 189건(`translations/wording_fit_v1_ko.json`, 검토표 `analysis/wording_fit_v1/REVIEW.md`)을 적용했다. 원래 초안은 각 유닛의 `canonical_wording`에 남아 있다.
- 061부터 `batch_label_v3.RedirectLabelComponent`를 쓴다. 778A4C(내비 이름표)·76C944는 리터럴 포인터를 새 사본으로 돌린다. 기본 감사·034~036 검사의 예외는 `REDIRECT_POINTERS`에만 둔다.
- 라벨은 고정 칸 렌더러 0x080554A4/0x080554DC 훅으로 들어간다. 057부터는 누적 빠른 조회(`tools/batch_label_v2.py`)를 쓰고, 056의 선형 래퍼는 우회한다.
- 054·055 995개는 이름·별명·프로필 문자열을 한글 4자(48px)로 가정한 완화 상한으로 들어갔다. 긴 이름이면 창을 넘을 수 있다(`analysis/pending500_055_v1/relaxed_name_bound_risk_v1.json`).
- 다음 묶음은 `python -X utf8 tools/next_batch_generic_v1.py NNN`(직전 묶음 위에 쌓음), 연속 실행은 `bash tools/run_batches_generic_v1.sh N`.
- 사용자 요청: **500개씩 ROM에 적용**한다. 배포용 패치는 요청할 때만 만든다(2026-10-25 요청으로 `patches/exe45_ko_development_20261025.zip`(064), 같은 날 갱신 요청으로 `patches/exe45_ko_development_20261025_r2.zip`(070, 한글 자판 포함) 생성. 도구 `tools/make_release_patch_v1.py`. 패키지 `verification.json`은 PowerShell 5.1이 읽으므로 반드시 ASCII로 쓴다).
- GitHub 공개: `Einbroch/rockman-exe4.5-kr-patch` v0.9.0 프리릴리즈(2026-10-25, 070 기준 r2 zip·bps·xdelta 첨부). 저장소 `source/`에 도구·번역·작업 기록(ROM·ROM 파생 그림 제외, 개인 경로는 `<user>`). 로컬 복제본 `release_repo/`, 커밋 작성자 Einbroke <30523510+Einbroch@users.noreply.github.com>.
- v0.9.2(2026-10-25, 074 기준 r4): 사용자 스크린샷 수정. 072=P.A메모 「패턴」(LZ 스프라이트 0x6D8188 제자리 재압축, `gba_lz77_v1.py`)·대사 이름표 포인터(0x51664/0x51668 칩, 778B08 아이템 6곳 — 065의 재지정은 실제로 적용되지 않았었다), 073=서브칩 화면 제목(LZ 0x6FB82C), 074=전투 팝업 「어택」「내비」(원시 OBJ 시트 0x770080). 화면 확인은 사용자 세이브 사본으로 격리 Mesen에서.
- 원본 ROM, 기존 결과, 사용자 저장, 사용자 mGBA를 보존한다.
- 기존 보고서가 해시로 참조하는 코드는 덮어쓰지 말고 새 버전으로 구현한다.
