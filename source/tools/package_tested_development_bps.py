"""Package the exact tested intermediate, not the unfinished full integration."""
import hashlib
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

from audit_save_keyboard_fonts import audit

ROOT = Path(__file__).resolve().parents[1]
NAME = 'exe45_ko_development_20261012_r3'
SOURCE_SHA = '588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8'
TARGET_SHA = 'ba12b55165e2c50c2779ba098b9066140cf95572241cb8dcf7ab04ae984489d7'
FLIPS_SHA = 'ca6b364ccb23ab83ff0f4458f589eac001e7baf74315decde73c878a8eb519fd'
FLIPS_URL = 'https://github.com/Sir-Walrus/Flips/releases/tag/v198'
XDELTA_SHA = '732980d52f9220dc81817ccdd0c295eadce8a0048a24c2a771a73f791ac824e9'
XDELTA_URL = 'https://github.com/jmacd/xdelta/releases/tag/v3.2.2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(flips, *args, success=True):
    env = dict(os.environ)
    env.pop('XDELTA', None)
    if str(flips).lower() == 'powershell.exe':
        # Do not inherit PowerShell Core's module search path in Windows PS 5.1.
        for key in list(env):
            if key.lower() == 'psmodulepath':
                del env[key]
    result = subprocess.run([str(flips), *map(str, args)], capture_output=True,
                            text=True, encoding='utf-8', errors='replace', env=env)
    if (result.returncode == 0) != success:
        raise ValueError(f'Unexpected tool status: {result.returncode}: {result.stdout} {result.stderr}')
    return dict(exit_code=result.returncode, stdout=result.stdout.strip(), stderr=result.stderr.strip())


def main():
    global NAME, TARGET_SHA
    parser=argparse.ArgumentParser()
    parser.add_argument('--name', default=NAME)
    parser.add_argument('--rom', default='poc/output/exe45_ko_development_save_keyboard_fonts_v1.gba')
    parser.add_argument('--runtime-evidence', default='poc/runtime/save-keyboard-fonts-v1-save-regression/persistence.json')
    args=parser.parse_args()
    if not args.name.replace('_','').isalnum():raise ValueError('Simple package name required')
    NAME=args.name
    profile = json.loads((ROOT / 'project.json').read_text(encoding='utf-8'))['source_profile']
    source = ROOT / profile['filename']
    target = ROOT / args.rom
    manifest=json.loads(target.with_suffix('.json').read_text(encoding='utf-8'))
    TARGET_SHA=manifest['output_sha256']
    baseline = ROOT / 'poc/output/exe45_ko_development_save_initialize_v1.gba'
    flips = ROOT / 'external/flips-v198/bin/flips.exe'
    xdelta = ROOT / 'external/xdelta3-v3.2.2/bin/xdelta3-3.2.2-windows-x86_64/xdelta3.exe'
    for path, expected in [(source, SOURCE_SHA), (target, TARGET_SHA), (flips, FLIPS_SHA),
                           (xdelta, XDELTA_SHA)]:
        if sha(path) != expected:
            raise ValueError(f'Pinned input mismatch: {path}')
    if source.stat().st_size != profile['size'] or profile['sha256'] != SOURCE_SHA:
        raise ValueError('Source profile mismatch')
    if manifest.get('startup_renderer'):
        from audit_startup_ui import audit as audit_startup
        static = audit_startup(target)
    else:
        static = audit(target, baseline)
    persistence = ROOT / args.runtime_evidence
    runtime = json.loads(persistence.read_text(encoding='utf-8'))
    if runtime['rom_sha256'] != TARGET_SHA or not (runtime.get('fresh_process_reload_verified') or runtime.get('title_menu_verified')):
        raise ValueError('Missing exact-artifact declared runtime verification')
    if 'title_menu_graphics' in manifest and not runtime.get('title_menu_verified'):
        raise ValueError('Title menu requires exact-artifact runtime evidence')
    if manifest.get('startup_renderer') and not runtime.get('startup_ui_verified'):
        raise ValueError('Startup UI requires exact-artifact runtime evidence')
    if manifest.get('native_keyboard_labels') and not runtime.get('native_keyboard_labels_verified'):
        raise ValueError('Native keyboard labels require exact-artifact runtime evidence')
    if manifest.get('navi_card_graphics') and not runtime.get('navi_card_graphics_verified'):
        raise ValueError('Navi card graphics require exact-artifact runtime evidence')
    if any(a['archive']=='6DD9AC' for a in manifest['archives']) and not runtime.get('first_mail_verified'):
        raise ValueError('First mail requires exact-artifact full page/runtime evidence')
    news=any(a['path'].replace('\\','/')=='analysis/news_mail_v1/6DD9AC_selected_asset.json' for a in manifest['translation_assets'])
    official=news or any(a['path'].replace('\\','/')=='analysis/official_mail_v1/6DD9AC_selected_asset.json' for a in manifest['translation_assets'])
    if official and not runtime.get('official_mail_display_diagnostic_verified'):
        raise ValueError('Official bodies require exact-artifact declared diagnostic evidence')
    if news and not runtime.get('news_mail_display_diagnostic_verified'):
        raise ValueError('News bodies require exact-artifact declared diagnostic evidence')
    for relative, expected in runtime['artifacts'].items():
        if sha(ROOT / relative) != expected:
            raise ValueError(f'Runtime evidence changed: {relative}')
    destination = ROOT / 'patches' / NAME
    archive = destination.with_suffix('.zip')
    if destination.exists() or archive.exists():
        raise ValueError('Preserve existing patch package')
    with tempfile.TemporaryDirectory(prefix='exe45-bps-') as scratch:
        work = Path(scratch)
        patch = work / (NAME + '.bps')
        run(flips, '--create', '--exact', '--bps', source, target, patch)
        rebuilt = work / 'reapplied.gba'
        run(flips, '--apply', '--exact', patch, source, rebuilt)
        if sha(rebuilt) != TARGET_SHA or rebuilt.read_bytes() != target.read_bytes():
            raise ValueError('Complete expanded target differs')
        patch2 = work / 'repeated.bps'
        run(flips, '--create', '--exact', '--bps', source, target, patch2)
        if patch.read_bytes() != patch2.read_bytes():
            raise ValueError('Patch not deterministic')
        wrong = work / 'wrong-source.gba'
        data = bytearray(source.read_bytes())
        data[0xA0] ^= 1
        wrong.write_bytes(data)
        rejected = work / 'rejected.gba'
        wrong_test = run(flips, '--apply', '--exact', patch, wrong, rejected, success=False)
        if rejected.exists():
            raise ValueError('Wrong source emitted an output')
        corrupt = work / 'corrupt.bps'
        data = bytearray(patch.read_bytes())
        data[-1] ^= 1
        corrupt.write_bytes(data)
        corrupt_test = run(flips, '--apply', '--exact', corrupt, source, rejected, success=False)
        if rejected.exists():
            raise ValueError('Corrupt patch emitted an output')
        xdpatch = work / (NAME + '.xdelta')
        # Legacy VCDIFF, no application filenames or secondary compression.
        # Keep window checksums; wrapper supplies strict whole-file SHA-256.
        encode = ['-e', '-a', '-A', '-S', 'none', '-9', '-s', source, target]
        run(xdelta, *encode, xdpatch)
        xdrebuilt = work / 'xdelta-reapplied.gba'
        run(xdelta, '-d', '-s', source, xdpatch, xdrebuilt)
        if sha(xdrebuilt) != TARGET_SHA or xdrebuilt.read_bytes() != target.read_bytes():
            raise ValueError('xdelta complete expanded target differs')
        xdpatch2 = work / 'repeated.xdelta'
        run(xdelta, *encode, xdpatch2)
        if xdpatch.read_bytes() != xdpatch2.read_bytes():
            raise ValueError('xdelta patch not deterministic')
        xdwrong = run(xdelta, '-d', '-s', wrong, xdpatch, work / 'xdwrong.gba', success=False)
        xdbad = work / 'corrupt.xdelta'
        data = bytearray(xdpatch.read_bytes())
        data[0] ^= 1
        xdbad.write_bytes(data)
        xdcorrupt = run(xdelta, '-d', '-s', source, xdbad, work / 'xdbad.gba', success=False)
        report = dict(schema=1, status='LOCAL_DEVELOPMENT_ONLY_NOT_RELEASE',
                      patch=dict(filename=patch.name, bytes=patch.stat().st_size, sha256=sha(patch)),
                      source=dict(filename=source.name, bytes=source.stat().st_size,
                                  sha256=SOURCE_SHA, header_hex=source.read_bytes()[0xA0:0xAC].hex()),
                      target=dict(filename=target.name, bytes=target.stat().st_size, sha256=TARGET_SHA),
                      tool=dict(name='Floating IPS v198', sha256=FLIPS_SHA, upstream=FLIPS_URL),
                      xdelta_patch=dict(filename=xdpatch.name, bytes=xdpatch.stat().st_size,
                                        sha256=sha(xdpatch)),
                      xdelta_tool=dict(name='xdelta3 3.2.2 Windows x86_64',
                                       sha256=XDELTA_SHA, upstream=XDELTA_URL),
                      xdelta_checks=dict(byte_identical_application=True, expanded_target_verified=True,
                                         deterministic_patch=True, wrong_source_rejected=xdwrong,
                                         corrupt_patch_rejected=xdcorrupt,
                                         encode_options=['-e', '-a', '-A', '-S', 'none', '-9']),
                      checks=dict(byte_identical_application=True, expanded_target_verified=True,
                                  deterministic_patch=True, wrong_source_rejected=wrong_test,
                                  corrupt_patch_rejected=corrupt_test, source_unchanged=sha(source) == SOURCE_SHA),
                      translated_units=static['translated_units'],
                      native_save_reload_previously_verified=runtime.get('fresh_process_reload_verified', False),
                      title_menu_verified=runtime.get('title_menu_verified', False),
                      weekend_menu_verified=runtime.get('weekend_menu_verified', False),
                      startup_ui_verified=runtime.get('startup_ui_verified', False),
                      native_keyboard_labels_verified=runtime.get('native_keyboard_labels_verified', False),
                      navi_card_graphics_verified=runtime.get('navi_card_graphics_verified', False),
                      first_mail_verified=runtime.get('first_mail_verified', False),
                      official_mail_display_diagnostic_verified=runtime.get('official_mail_display_diagnostic_verified', False),
                      official_mail_acquisition_verified=False,
                      news_mail_display_diagnostic_verified=runtime.get('news_mail_display_diagnostic_verified',False),
                      news_mail_acquisition_verified=False,
                      news_mail_quest_progression_verified=False,
                      runtime_evidence=dict(path=str(persistence.relative_to(ROOT)), sha256=sha(persistence)),
                      automatic_hangul_keyboard_installed=False, hangul_persistence_verified=False,
                      full_translation_integrated=False, public_release_eligible=False)
        (work / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        for filename in ['README.ko.md', 'ApplyPatch.ps1', 'ApplyXdelta.ps1']:
            shutil.copyfile(ROOT / 'tools/development_patch_bundle' / filename, work / filename)
        readme=work/'README.ko.md'
        text=readme.read_text(encoding='utf-8')
        text=text.replace('exe45_ko_development_save_keyboard_fonts_v1.gba',target.name)
        text=text.replace('ba12b55165e2c50c2779ba098b9066140cf95572241cb8dcf7ab04ae984489d7',TARGET_SHA)
        text=text.replace('2,596개',f"{manifest['translated_units']:,}개")
        text=text.replace('11,166,736바이트',f"{target.stat().st_size:,}바이트")
        if runtime.get('title_menu_verified'):
            text=text.replace('저장 관련 UI, 한글 자모 글꼴 공급.', '저장 관련 UI, 한글 자모 글꼴 공급, 메인 메뉴 처음부터·이어하기 그래픽.')
            text=text.replace('해당 ROM에서는 일본어 한 글자 이름으로 실제 저장·리셋·새 프로세스 불러오기를 시험했습니다.',
                              '이번 ROM에서는 무저장 처음부터 진입, 저장 상태의 두 메뉴 선택 표시와 이어하기 진입을 시험했습니다. 이전 기준 ROM의 게임 생성 SAV를 격리 테스트 폴더에 복사했으며, 이번 회귀에서 새 저장은 수행하지 않았습니다.')
        if runtime.get('weekend_menu_verified'):
            text=text.replace('메인 메뉴 처음부터·이어하기 그래픽.', '메인 메뉴 처음부터·이어하기·주말 대회 그래픽.')
            text+='\n이번 추가 반영: `どにちのたいかい` → `주말 대회`. 대회 참가 조건은 원본 그대로이며 이번 시험 저장의 조건에서 메뉴 표시와 커서 이동을 확인했습니다. 첨부 초기 설정·프로필·록맨 대사의 일본어는 이번 패치에서 추가 번역하지 않았습니다.\n'
        if runtime.get('startup_ui_verified'):
            text=text.replace('이번 ROM에서는 무저장 처음부터 진입, 저장 상태의 두 메뉴 선택 표시와 이어하기 진입을 시험했습니다. 이전 기준 ROM의 게임 생성 SAV를 격리 테스트 폴더에 복사했으며, 이번 회귀에서 새 저장은 수행하지 않았습니다.',
                              '이번 ROM에서는 무저장 처음부터 진입을 시험했습니다. 저장 상태의 이어하기와 저장·재로드는 이전 기준 ROM의 검증 범위이며, 이번 회귀에서 새 저장이나 이어하기는 수행하지 않았습니다.')
            start=text.index('- 검증 범위:');end=text.index('\n\n## 적용 대상',start)
            text=text[:start]+'- 검증 범위: 이번 ROM의 새 게임 경로를 일반 버튼 입력으로 시험했습니다. 날짜·성별·나이·직업·프로필 확인·록맨 선택·PET 첫 안내 및 초기 메일 알림을 확인했습니다. 원본 적용 결과의 전체 바이트 동일성을 검증했습니다. 전체 플레이와 한글 이름 저장은 검증 완료가 아닙니다.'+text[end:]
            text+='\n이번 추가 반영: 초기 설정 텍스트 41개, 선택 가능한 내비 이름 4개, 록맨 메일 알림 7개 및 PET 첫 안내/날짜 버튼 그래픽. 남은 일본어: 이름 입력의 가나 자판·기능 버튼, 내비 카드의 그림 글자 등. 초기 메뉴 전체 한글화 완료본은 아닙니다.\n'
        if runtime.get('native_keyboard_labels_verified'):
            text=text.replace('이름 입력의 가나 자판·기능 버튼, 내비 카드의 그림 글자 등.', '이름 입력의 가나 글자판, 내비 카드의 그림 글자 등.')
            text+='\n이름 입력 세 페이지의 기능 버튼 18개를 추가 한글화했습니다. 가타카나/히라가나/기호 전환, 오른쪽/왼쪽/공백/확인 표시는 원래 가나 입력 기능에 대응합니다. 한글 자동 조합 자판으로 바뀐 것이 아닙니다. 세 페이지의 실제 전환·재진입·일본어 한 글자 이름 확정/프로필 표시를 확인했습니다.\n'
        if runtime.get('navi_card_graphics_verified'):
            text=text.replace('내비 카드의 그림 글자 등.', 'NAVI SELECT 영문 제목 등.')
            text+='\n내비 카드 이름 그림 글자 21개를 추가 한글화했습니다. 실제 선택 가능한 록맨·롤·거츠맨·넘버맨의 이동/확인/취소를 일반 입력으로 시험했습니다. 잠긴 다른 내비는 공유 그래픽 묶음의 업로드를 검증했지만 실제 해금·선택 플레이는 시험하지 않았습니다.\n'
        if runtime.get('first_mail_verified'):
            text+='\n첫 I.P.C. 안내 메일 본문 23쪽과 일반 메일함/참가 확인/록맨 안내/고객 여러분께/제목: 문구 등 7개를 추가 적용했습니다. 본문 23쪽의 읽기·완료·목록 복귀·재열기를 확인했습니다. 다른 메일 본문과 다른 내비의 메일함 대사는 아직 원문이 남아 있습니다.\n'
        if runtime.get('official_mail_display_diagnostic_verified'):
            text+='\n오피셜 메일 본문 3통(32개)을 추가 적용했습니다. 원래 메일 로더의 해제 데이터와 출력기로 전 페이지를 격리 진단했습니다. 진단은 스크립트 표 읽기 한 번을 바꿔 접근하며, 실제 수신/진행 조건·해당 발신자/제목·저장 호환을 검증한 것은 아닙니다. 진단 개입은 이 패치에 들어 있지 않습니다. 원래 플래그 명령은 보존했습니다. 문구 한 곳의 새 번역 후보는 의미와 표시의 사람 검토가 필요하며 공개 릴리스가 아닙니다.\n'
        if runtime.get('news_mail_display_diagnostic_verified'):
            text+='\n메일 뉴스1~3호 본문22개를 추가 적용했습니다. 실제 원래 로더/출력기의 격리 진단에서 모든 쪽의 표시·넘김·종료를 확인했습니다. 원래 퀘스트 명령은 유지하지만, 일반 진행에서 수신·퀘스트 시작/완료·해당 발신자/제목 연결은 검증하지 않았습니다. 진단 개입은 패치에 포함되지 않습니다. 뉴스4~6호와 초대장43개 본문, 기타 일본어가 남아 있습니다.\n'
        readme.write_text(text,encoding='utf-8')
        wrapper_checks = {}
        for script, option, tool in [('ApplyPatch.ps1', '-FlipsExe', flips),
                                      ('ApplyXdelta.ps1', '-XdeltaExe', xdelta)]:
            output = work / (script + '.gba')
            command = ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', work / script,
                       '-SourceRom', source, '-OutputRom', output, option, tool]
            run('powershell.exe', *command)
            if sha(output) != TARGET_SHA:
                raise ValueError('Application wrapper differs')
            run('powershell.exe', *command, success=False)
            # Both wrappers must reject an already patched source before output.
            command[command.index('-SourceRom') + 1] = target
            wrong_output = work / (script + '-wrong.gba')
            command[command.index('-OutputRom') + 1] = wrong_output
            run('powershell.exe', *command, success=False)
            if wrong_output.exists():
                raise ValueError('Wrapper accepted wrong source')
            wrapper_checks[script] = dict(exact_target=True, overwrite_rejected=True,
                                         wrong_source_rejected=True)
        report['application_wrapper_checks'] = wrapper_checks
        (work / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        shutil.copyfile(ROOT / 'external/fonts/LICENSE-Galmuri.txt', work / 'LICENSE-font.txt')
        members = [patch.name, xdpatch.name, 'README.ko.md', 'ApplyPatch.ps1', 'ApplyXdelta.ps1',
                   'verification.json', 'LICENSE-font.txt']
        bundle = work / (NAME + '.zip')
        with zipfile.ZipFile(bundle, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for filename in sorted(members):
                info = zipfile.ZipInfo(filename, (2026, 10, 12, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, (work / filename).read_bytes())
        destination.mkdir(parents=True)
        for filename in members:
            shutil.copyfile(work / filename, destination / filename)
        shutil.copyfile(bundle, archive)
        print(json.dumps(dict(package=str(archive), package_sha256=sha(archive),
                              patch=str(destination / patch.name), patch_sha256=sha(patch),
                              patch_bytes=patch.stat().st_size,
                              xdelta=str(destination / xdpatch.name), xdelta_sha256=sha(xdpatch),
                              xdelta_bytes=xdpatch.stat().st_size, checks='PASS'), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
