"""Verify actual combined carry diagnostic artifacts; does not admit consumers."""
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read,frozen_write
from tpl_literals import literals,skeleton,resolve_units
from textpet_korean import command

SOURCE='analysis/pending_insertion_500_041_source_v7'


def main():
    r=read(SOURCE+'/carry_verification_v1.json');s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v2.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);m=read(s['baseline_rom'].replace('.gba','.json'));common=command(ROOT/SOURCE/'compile_v2/plugins')
    if not r['passed'] or r['new_units']!=500 or r['inherited_units']!=156 or r['rom_written']:raise ValueError('041 exact carry prerequisite')
    checked=set();new=set();old=set();details=[];newmetrics={u['id']:u for a in v['archives'] for u in a['layout']}
    for a in r['archives']:
        for key in ('asset','target_tpl','compiled'):require_hash(ROOT/a[key]['path'],a[key]['sha256'])
        asset=read(a['asset']['path']);units=resolve_units(asset);require_hash(ROOT/asset['source_tpl']['path'],asset['source_tpl']['sha256']);original=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig');target=(ROOT/a['target_tpl']['path']).read_text(encoding='utf-8-sig');wanted={u['id']:u['translation'] for u in units}
        if skeleton(target)!=skeleton(original) or {u.key:u.text for u in literals(target) if u.key in wanted}!=wanted or len(wanted)!=len(units):raise ValueError('041 combined authored target/controls')
        new.update(a['new_ids']);old.update(a['inherited_ids']);d=ROOT/a['target_tpl']['path'];d=d.parent
        if a['inherited_ids']:
            ep=d/'carry_reverse.tpl';bp=d/'carry_rebuilt.msg';run_textpet(common+['Read-Text-Archives',str(ROOT/a['compiled']['path']),'--format','bin','Write-Text-Archives',str(ep),'--format','tpl'],d/'carry_reverse.log');run_textpet(common+['Read-Text-Archives',str(ep),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],d/'carry_rebuild.log');exported=ep.read_text(encoding='utf-8-sig')
            if bp.read_bytes()!=(ROOT/a['compiled']['path']).read_bytes() or skeleton(exported)!=skeleton(original) or [(u.key,u.language,u.text) for u in literals(target)]!=[(u.key,u.language,u.text) for u in literals(exported)]:raise ValueError('041 combined carry exact text/control/binary roundtrip')
            details.append(dict(archive=a['archive'],reverse_sha256=sha(ep.read_bytes()),rebuilt_sha256=sha(bp.read_bytes()),inherited_units=len(a['inherited_ids'])))
        checked.update(a['new_ids'])
    if len(new)!=500 or len(old)!=156 or new&old or new!=set(s['selected_ids']) or checked!=set(newmetrics):raise ValueError('041 carry/new denominator')
    result=dict(passed=True,status='041_SOURCE500_PLUS156_CARRY_DIAGNOSTIC_ROUNDTRIP_PASS_NOT_ROM',baseline_sha256=s['baseline_sha256'],new_units=500,inherited_units=156,archives=54,recompiled_inherited_archives=details,new_units_source_roundtrip_and_font_verified=True,current_unselected_scripts_preserved=True,rom_written=False,product_admitted=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in [SOURCE+'/carry_verification_v1.json',SOURCE+'/verification_v2.json','tools/verify_carry500_041_v1.py']},limits=['Source/combined diagnostics only, NOT041 product ROM, native caller admission or screen verification.','Prior156 consumed payload bytes independently regenerated from authored inputs, not extracted ROM text.','Core041 source selection has445scripts/54archives and unresolved consumer bindings; no new units applied.'])
    frozen_write(ROOT/SOURCE/'carry_roundtrip_v1.json',result);print('PASS041 source500/carry156/8combined roundtrips; NOT ROM or consumer admission')


if __name__=='__main__':main()
