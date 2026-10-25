# 록맨 EXE 4.5 한글패치 개발판 (2026-10-12)

현재 시험했던 `exe45_ko_development_save_keyboard_fonts_v1.gba`를 재현하는 개인 테스트용 BPS 및 xdelta 패치입니다. 완성본이나 공개 배포용 릴리스가 아닙니다. 두 패치는 대체 형식이므로 둘 중 하나만 무패치 원본에 적용하세요. 두 패치를 연달아 적용하지 마세요.

- 포함: 기존 빌드에 등록된 번역 2,596개, 저장 관련 UI, 한글 자모 글꼴 공급.
- 미포함: 추가 번역 초안 전체의 ROM 통합, 자동 조합 한글 자판, 한글 이름·별명 저장 지원. 실제 입력 화면은 여전히 일본어입니다.
- 검증 범위: 원본에 패치를 적용한 결과가 시험 ROM 전체와 바이트 단위로 동일함을 확인했습니다. 해당 ROM에서는 일본어 한 글자 이름으로 실제 저장·리셋·새 프로세스 불러오기를 시험했습니다. 전체 플레이·한글 저장·다른 저장 파일 호환성을 보증하지 않습니다.

## 적용 대상

일본판 무패치 원본 `Rockman EXE 4.5 Real Operation (J)(Independent).gba`

- 원본 크기: 8,388,608바이트
- 원본 SHA-256: `588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8`
- 적용 후 크기: 11,166,736바이트
- 적용 후 SHA-256: `ba12b55165e2c50c2779ba098b9066140cf95572241cb8dcf7ab04ae984489d7`

이전 한글패치 ROM에 덧씌우지 마세요. 원본 ROM과 기존 SAV/RTC를 먼저 백업하고, 결과는 새 파일 이름과 별도 테스트 저장 폴더로 사용하세요. 원본 ROM이나 세이브 파일은 이 패키지에 포함하지 않습니다.

## Windows 적용

ZIP을 풀고 [Floating IPS v198 공식 다운로드](https://github.com/Sir-Walrus/Flips/releases/tag/v198)에서 받은 `flips.exe`를 준비하세요. 실행 파일은 패키지에 포함하지 않습니다.

권장 방식은 아래 PowerShell 명령입니다. 경로는 실제 위치로 바꿔주세요. 스크립트가 원본·패치·결과의 SHA-256을 검사하며 기존 결과 파일을 덮어쓰지 않습니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\ApplyPatch.ps1 -SourceRom "D:\경로\원본.gba" -OutputRom "D:\경로\록맨45_한글_개발판.gba" -FlipsExe "D:\경로\flips.exe"
```

직접 Floating IPS의 Apply Patch 기능을 사용할 수도 있습니다. 패치 파일, 위 SHA-256이 일치하는 원본, 새 결과 파일을 순서대로 선택하세요. 체크섬 무시 옵션은 사용하지 마세요. 직접 적용한 경우 결과 SHA-256도 확인하세요.

`verification.json`에는 패치 해시, 전체 결과 동일성 검사, 잘못된 원본·손상 패치 거부 검사, 기존 런타임 증거의 식별값을 기록했습니다.

## xdelta 적용

[xdelta3 3.2.2 공식 다운로드](https://github.com/jmacd/xdelta/releases/tag/v3.2.2)의 Windows x86_64 ZIP에서 `xdelta3.exe`를 준비하세요. 실행 파일은 이 패키지에 포함하지 않습니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\ApplyXdelta.ps1 -SourceRom "D:\경로\원본.gba" -OutputRom "D:\경로\록맨45_한글_개발판.gba" -XdeltaExe "D:\경로\xdelta3.exe"
```

이 스크립트도 원본·패치·결과 SHA-256 및 크기를 검증하고 덮어쓰기를 방지합니다. xdelta 파일은 응용 헤더와 보조 압축을 사용하지 않는 VCDIFF 형식으로 생성했으며, 창 체크섬을 유지했습니다. 구형 GUI 도구의 호환성은 별도로 시험하지 않았습니다. 직접 적용한 경우에도 위의 원본 및 결과 SHA-256을 확인하세요.

## 글꼴 고지

게임용 변환 글꼴에는 Galmuri 원본 글꼴에서 변환한 데이터가 포함됩니다. 원저작자 고지와 SIL Open Font License 1.1은 동봉된 `LICENSE-font.txt`를 참고하세요. 변환 글꼴의 표시 이름은 EXE45 Korean Development Font입니다. 이 패치는 권리자와 무관한 비공식 개발판입니다.
