# 작업 소스 (도구 · 번역)

록맨 에그제 4.5 한글패치를 만들 때 쓴 빌드·검증 도구와 한국어 번역 파일입니다.
**ROM은 들어 있지 않습니다.** 빌드하려면 직접 가진 원본 일본판 ROM이 필요합니다(해시는 저장소 첫 화면 README의 표 참고).

## 구성

| 폴더 | 내용 |
|---|---|
| `tools/` | 빌드·검증 스크립트(Python). `tools/specs/`에 빌드 명세가 있습니다. |
| `translations/` | 한국어 번역 파일(`*_ko.json`, 대사 묶음 초안, 문구 다듬기 `wording_fit_v1_ko.json` 등) |
| `docs/` | 작업 기록. `CLAUDE_CODE_HANDOFF.md`(최신 상태), `WORK_NOTES.md`, `HANDOFF.md`, `analysis/`(분야별 인수인계·진행 기록, 그중 한글 자판은 `analysis/HANGUL_KEYBOARD_HANDOFF.md`) |

번역 파일에는 대조용 원문 일본어 문자열이 함께 들어 있습니다.

## 빌드 흐름 요약

- 묶음 빌드: `tools/next_batch_generic_v1.py NNN`
  - 직전 묶음 위에 쌓습니다.
  - 생성된 `tools/build_development_patch_NNN_v1.py`가 원본에서 처음부터 다시 빌드합니다.
- 그림 전용 단계와 한글 자판 단계: `tools/make_graphics_stage06x_v1.py`, `tools/make_keyboard_stage06x/070_v1.py`로 빌드 파일을 만든 뒤 같은 명령으로 빌드합니다.
- 한글 자판 핵심 파일:
  - `hangul_record_v3.py`(저장 형식)
  - `hangul_editor_v1.py`(조합 규칙)
  - `hangul_keyboard_hooks_v1/v2/v3.py`(ROM 훅)
  - `keyboard_page_v1.py`(자판 그림)
- 배포 패치: `tools/make_release_patch_v1.py`

## 빌드에 필요하지만 들어 있지 않은 것

- 원본 일본판 ROM
- [TextPet](https://github.com/Prof9/TextPet)과 EXE4.5용 플러그인
- 한글 글꼴 [Galmuri](https://github.com/quiple/galmuri)(OFL 1.1)
- keystone·capstone·unicorn(파이썬), 화면 확인용 Mesen 2
- 코덱스 작업에서 원본 그래픽으로 만든 자판 쪽 후보 데이터(`analysis/hangul_keyboard_v1/kana_replacement/`): ROM에서 나온 그림이라 넣지 않았습니다. PET 그래픽 원본 블록(`native_obj_block.bin`)도 같은 이유로 뺐습니다.

경로는 작업 PC 기준으로 적혀 있어 그대로는 돌지 않습니다(`C:\Users\<user>\...` 등은 자리표시).
