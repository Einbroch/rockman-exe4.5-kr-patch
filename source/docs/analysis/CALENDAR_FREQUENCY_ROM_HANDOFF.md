# 달력 빈도 그래픽5문구 번역

2026-10-04. development-draft; NON-DISTRIBUTION; needs_review; release_eligible=false.

ROM `poc/output/exe45_ko_development_calendar_frequency_v1.gba`.
SHA256 `43f7305a20ccc4acfff75815e9cde450fb22642a9c2012bd7d08ac97cd7da6ac`.
원본 SHA256 `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`.
누적1,090선택 텍스트단위 /14그래픽 문구 /21선택·711미선택 archive. 전체게임 완역률 아님.

## 새로 확인한 경계

기존119..123 source/relocated read 관찰은 실제 빈도 화면 소비경로를 증명하지 못했다.
동일 SHA의 calendar_types_v2 정상 own-roll-intro에서 read-only VRAM write/중간 RAM 관찰을 추가했다.
`calendar-frequency-loader-v1`, `calendar-frequency-upload-v1/v2/v3` 증거와 시행 도구는 보존했다.
초기RAM 관찰은 먼저 로드된 다른 블록63861C를 포착했다. 이를 빈도 asset으로 오인하지 않았다.
로더29164의 소스/대상 테이블과 raw항목의 추가 size word를 따라 실제63673C를 확인했다.

원본63673C LZ10 스트림은425소비바이트, 다음 archive6368E8까지428-byte 슬롯이다.
해제1284bytes: 첫4byte `00040500`은 그대로 보존, 뒤1280bytes는5×256-byte 타일이다.
정상 selector 경로의 소스테이블080327CC와 대상080327FC,
raw항목 처리 뒤 실제관찰 table080327D0/index16에서 source0863673C를 선택한다.
0802918A에서 native decompression source와stage0201B800을 관찰,
080291A0에서 stage+4=0201B804→06013800/1280bytes를 확인했다.
BIOS 해제 결과1284bytes와 독립 디코더 결과가 원본/새ROM 각각 정확히 일치한다.
원본5타일 전체와 VRAM13800..13CFF의 일치도 확인했다.

같은 포인터의 정확한 literal reference는327E0/32D44/33080/343E8 네 곳이다.
이 숫자는 모든 공유경로가 검증됐다는 뜻이 아니다. 실제 로더 링크 증명은 selector의 첫 경로만 한다.
나머지 로더/확정/등록·조회 소비경로의 전체 상태별 검증은 열린 항목이다.

## 번역과 보호

1回のみ→1회만, 毎日→매일, 毎週→매주, 毎月→매월, 毎年→매년.
기존 PET/장비에서 채택한 BDF 글꼴·라이선스 해시를 재사용한 코드 기반 타일 조합이다.
새 그림이나 임의 획을 생성하지 않으며 글꼴을 축소하지 않는다.
각32×16 canvas의 y4..14 안에서만 일본어 ink3/shadow9를 제거하고,
투명 background0 위에 한글 ink3/shadow9를 같은 팔레트 역할로 배치한다.
다른 행/첫4byte/타일순서/캔버스/포인터/네이티브코드/입력·등록·저장 데이터는 유지한다.
344-byte 스트림+84byte zero padding으로 같은428-byte 슬롯에 반영한다.
파일 전체 비교로 직전 calendar_date_v1 ROM과 이 슬롯 밖 모든 바이트가 동일하다.
문자열119..123, 기본이름62/63, 키보드2/3/4는 변경하지 않는다.

## 검증

새 ROM own-cold/date/profile/Roll/intro/PET/장비/달력/등록/조회/종류스크롤/날짜 경로를 정상 패드로 수행했다.
이전SHA checkpoint나 read alias, CPU/ROM/RAM/register 개입은 사용하지 않았다.
같은 ROM own-roll-intro부터 selector를13단계 실행해 step6/7/9/11/13의5개 선택을 확인했다.
전체5문구1280bytes VRAM 일치, sprite16의 native geometry와 tile1C0/1C8/1D0/1D8/1E0 진행,
32×16 canvas 전체의 background/ink/shadow 색·픽셀 마스크 검사 통과.
5화면 contact sheet와 meal/step5 확정화면을 직접 시각 확인했다.
확정화면의 `1회만`은 관찰됐지만 해당 로더의 독립 압축해제 trace 증명으로 합산하지 않는다.
확정화면 기본명 `ごはん`은 아직 일본어다.

새 빈도1 + 기존 날짜/종류/등록안내/달력메뉴/소개/PET/기본대사/장비/등록시각조회9 = 집중10정상보고서 통과.
관련47개 unittest(13.265초) 통과. 역사적 capture fixture 테스트를 새ROM 실제 플레이로 합산하지 않는다.
장비 selector32건 CPU bench는 실제32퀘스트 플레이가 아니다.
main/_repro/_current_repro 3독립 빌드의 ROM SHA 동일,419Python도구 drift=[],원본 SHA 보존.
`analysis/calendar_frequency_v1/final_identity_audit.json` 참조.

## 남은 완료 조건

가장 중요한 기본이름/한글입력 경계는 미해결이다. E5종료 복사·바이트길이·편집·glyph공급·확정레코드·저장/재로드를 연결해야 한다.
공유 빈도4reference 전체 검증, 다른 미번역 텍스트·이미지, RTC/알람·전체게임·실기·오디오·인간검토도 미완료다.
이번5개 선택기 성공을 제품 전체의 완성이나 배포 승인으로 확대하지 않는다.

증거: `analysis/calendar_frequency_v1/frequency_runtime.json`, `selector_contact_sheet.png`, 각 회귀 보고서.
