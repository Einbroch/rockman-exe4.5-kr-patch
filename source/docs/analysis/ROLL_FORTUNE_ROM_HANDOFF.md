# 롤 운세 소개·블루 하트 — 13문구 개발 반영

2026-10-03. development-draft; NON-DISTRIBUTION.
문구/시각 needs_review, release_eligible=false. 완역·배포·인간 승인·실기·오디오
검증 주장이 아니다. 한글패치 스킬의 원본 보존/재현 빌드 및 실행 증거 분리 기준을 적용했다.

## 최신 결과

`poc/output/exe45_ko_development_roll_fortune_v1.gba`
SHA256 `aa37743f7e52e72106d6ac67dc74c96af4650d673efd23f99bc1779ef4e49860`.
`_repro.gba`, `_current_repro.gba` 모두 바이트 동일하다.
최종 `_current_repro.json`의 모든 tools/*.py 해시가 현재 도구와 일치한다.
불변 원본 SHA256
`588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`도 변경되지 않았다.
원본/이전 ROM/실패 작업 폴더는 보존했다. 패치 ROM을 다음 빌드 입력으로 쓰지 않았다.

누적863텍스트 단위(이번13), 기존 그래픽9개 유지. 전체 게임 분모/완료율이 아니다.
이전 롤 인사5/PET44/장비/칩/기존 그래픽 변경을 함께 선택한 누적 ROM이다.

## 입력과 기술 범위

`translations/roll_fortune_intro_blue_ko.json`.
원본65FF3C3434바이트 SHA256
`8d1f5550dd74fd813c38c32ade00cd73a572bf008fbefa31c50e9f81a3e74cf5`.
exe45.tpi의380E0 포인터229600으로 선택되는 롤 운세 풀이다.
새 풀3704바이트를 source 기반으로 재생성·재배치하고 원본 영역은 보존했다.
새 게임 코드 훅/진행 플래그 조작/램 버퍼 확장은 추가하지 않았다.

65스크립트 중0/1/4의13문구만 명시적으로 선택했다.
0/1의점6개와62다른 스크립트는 원문/원형 유지했다.
random 비율/분기, global6, flag3585/3661, heart-data-location 분기,
윈도92,110·줄 수·clearMsg·keyWait·waitSkip30을 변경하지 않았다.
기존132px/3행 개발 범위에서 최대132px이다. 포인터/문자 인코딩/모든 공급 글꼴/
보호 명령/원형 비선택 스크립트/재추출/의미·바이너리 roundtrip/final diff는 빌드 검사 대상이다.

| 범위 | 선택 문구 | 정상 실행 관측 | 남은 검증 |
|---|---:|---:|---|
| 첫 운세 소개 script0 | 5 | 5 | 인간 문구·시각 검토 |
| 반복 운세 소개 script1 | 4 | 0 | 정상 반복일 진입/표시 |
| 블루 하트 script4 | 4 | 4 | 인간 문구·시각 검토 |

블루 하트의 blue/depressed 말장난은 색상 이름 뒤의 ‘우울한 하루’ 의미로 초안화했다.
색상 말장난까지 완전히 재현한 것으로 승인하지 않았다. 이 의미/말투 선택은 인간 검토 대기다.
물로 인한 사고의 징조는 물 사고로 번역하며, 홍수만으로 의미를 한정하지 않는다.

최초 빌드는 줄 수/폭 보호 검사에 막혔다. 줄 수를 늘리지 않는 명시적인 개발 문구로
수정했으며 검사를 완화하거나 자동 생략하지 않았다. 최초 작업 폴더와 실패 폴더r2/r3를 보존했다.

## 실제 실행·화면

새 ROM 자체 cold boot→날짜/프로필 입력→정상 Navi Select→롤 설치/인사→운세.
이전 ROM에서는 버튼 입력 레시피만 재사용했다. 상태는 모두 해당 ROM의 자체
체크포인트/영수증이며, 게임 RAM/현재 스크립트/결과/난수를 주입하지 않았다.

`poc/runtime/roll-fortune-v1-fortune-select`의step8..14,
`roll-fortune-v1-fortune-intro`의step2..3에서 선택9문구를 관측했다.
각 현재 페이지의 stream/cursor/root/script, 글꼴 CPU 읽기,
ROM 글꼴→OBJ VRAM→스크린샷 픽셀 일치 및 빈 본문 영역의 잔상 제거를 확인했다.
점 세 개의 실제 프레임은1637/1670/1703이며 간격33/33프레임이다.
원래 waitSkip30 명령과 명령 사이의 출력 시간을 그대로 유지한다.
비교 화면 `analysis/roll_fortune_v1/fortune_pages.png`는9페이지다.
이를 단순 폰트 합성/벤치 화면으로 대신하지 않았다.

동일 ROM에서 기존 인사2페이지/페이지 지움/다음 풀 전환,
PET22문구와29선택 단계, 롤/록맨 장비·가이드·무기·폴더,
PET7이미지(‘통신’), 공격력 이미지의 native 해제/상주/업로드/OBJ 픽셀과
숫자 보존을 회귀 검증했다. 저장/통신의 실제 실행 Yes는 수행하지 않았다.

증거는 ROM/에뮬레이터/각 파일/자기 상태 부모의 재귀 해시에 묶인다.
보고서:

- `analysis/roll_fortune_v1/runtime.json`
- `analysis/roll_fortune_v1/greeting_regression/runtime.json`
- `analysis/roll_fortune_v1/pet_regression/runtime.json`
- `analysis/roll_fortune_v1/rockman_regression/runtime.json`
- `analysis/roll_fortune_v1/roll_caption/runtime.json`

자동 테스트138개,44.756초,OK. 새 테스트4개가13문구/62원형 슬롯/6점,
source·줄 수 실패 거부,9실행/4정적 분리, 누적 회귀를 검사한다.

## 재현

```powershell
python -X utf8 tools/build_roll_pet.py --roll-intro --roll-fortune --work NEW_WORK --out NEW_OUTPUT.gba
python -X utf8 tools/run_roll_fortune_matrix.py
python -X utf8 tools/report_roll_fortune.py
python -X utf8 -m unittest discover -s tools -p 'test_*.py'
```

기존 out/work/runtime 접두사를 덮어쓰지 않는다. 실행 도구의 기본 STEM/PREFIX는
이번 결과용이다. 다른 실행은 해당 모듈의 STEM/PREFIX를 새 결과/새 접두사로
지정하고 main()을 실행한다. report에도 같은 STEM/PREFIX를 지정하며,
static 검사를 위해 해당 STEM의 `_repro.gba`를 독립 빌드한다.
기존 builder 기본 선택은 바꾸지 않았고 --roll-fortune으로만 추가한다.

## 다음 미번역 작업

65FF3C의 다른 하트 결과 script3/5..18, 아이템 위치 힌트20..23은 일본어다.
미니게임 결과50..53/60..63은 별도 소비 문맥을 더 확인한 뒤 선택한다.
이번 반복 소개1의4문구는 정적 검증만 완료했다. 날짜/일 변경을 통한 정상
재진입 경로는 미검증이다. 이전 재회3/PET22의 미관측 분기도 계속 열려 있다.
타 내비/전체 미번역·전체 분모·실제 저장/통신·실기/오디오·인간 승인·배포 QA는 미완료다.
