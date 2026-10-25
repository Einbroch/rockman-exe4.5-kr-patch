"""Bind observed040 equipment/mail providers; do not admit unobserved041 paths."""
import re
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from prepare_repartition500 import layout_records

SOURCE='analysis/pending_insertion_500_041_source_v8'


def main():
    s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v3.json')
    require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();m=read(s['baseline_rom'].replace('.gba','.json'))
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);original=(ROOT/cfg['source_profile']['filename']).read_bytes()
    evidence={};details=[]
    def pin(path):
        p=ROOT/path;evidence[str(p.relative_to(ROOT))]=sha(p.read_bytes());return p
    parent='poc/runtime/pending500-040-communication-v1-05'
    p=read(parent+'/result.json');pin(parent+'/result.json');pin(parent+'/checkpoint.mss')
    if not p['complete'] or p['rom_sha256']!=s['baseline_sha256'] or p.get('normal_play_checkpoint_eligible') is False:raise ValueError('041 native normal040 parent')
    for family,arc,script,ram,outer,loadlr,folder in [
        ('equipment','6E1068',60,0x0202BA7C,0x0803C485,0x0803C5B7,'equipment-v2'),
        ('mail-intro','6DD0B8',9,0x02024000,0x08040D67,0x0804113B,'mail-v6')]:
        base='poc/runtime/pending500-040-native041-'+folder;r=read(base+'/result.json');t=read(base+'/native_consumers041.json');pin(base+'/result.json');pin(base+'/native_consumers041.json')
        if not r['complete'] or r['return_code']!=0 or r['rom_sha256']!=s['baseline_sha256'] or r['state_sha256']!=sha((ROOT/parent/'checkpoint.mss').read_bytes()) or len(r['loaded_rom_guards'])!=8:raise ValueError('041 exact040 owned route')
        if (ROOT/base/'loaded_rom_guard_failed.txt').exists() or (ROOT/base/'loaded.txt').read_text().strip()!='true':raise ValueError('041 loaded artifact guards')
        for name,h in r['artifacts'].items():require_hash(pin(base+'/'+name),h)
        loads=[x for x in t['loads'] if x['archive']==arc and x['destination']==ram and x['lr']==loadlr]
        if len(loads)!=1:raise ValueError('041 unique observed provider')
        load=loads[0];payload=lz77_decompress(rom,load['source']-0x08000000)[0]
        if len(payload)!=load['bytes']:raise ValueError('041 loader decode extent')
        calls=[x for x in t['calls'] if x['frame']==load['frame'] and x['registers']['1']==script and x['registers']['14']==0x0804F7BD and x['stack_lr16']==outer]
        if len(calls)!=1:raise ValueError('041 actual native common/outer caller')
        call=calls[0];root=call['registers']['0']
        if family=='equipment':
            if load['source']!=0x086E1068 or payload!=lz77_decompress(original,0x6E1068)[0]:raise ValueError('041 equipment native decode identity')
            expected=m['equipment_guides']['selector']['clone_offset']+0x08000000
            if root!=expected:raise ValueError('041 existing guide preselected ROM root')
            for step in range(1,7):
                snap=(ROOT/base/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();at=ram-0x02000000
                if snap[at:at+len(payload)]!=payload:raise ValueError('041 native equipment RAM identity/lifetime')
        else:
            a=next(x for x in read(SOURCE+'/carry_verification_v2.json')['archives'] if x['archive']==arc)
            prior=ROOT/a['target_tpl']['path'];prior=prior.parent/(arc+'_prior.msg')
            if payload!=prior.read_bytes() or root!=ram or not call['native_dump'] or (ROOT/base/call['native_dump']).read_bytes()!=payload:raise ValueError('041 independently authored old mail RAM consumer')
            pin(str(prior.relative_to(ROOT)))
        default=[x for x in t['defaults'] if x['frame']==call['frame'] and x['root']==root]
        if len(default)!=1 or (default[0]['x'],default[0]['y'])!=(52,110):raise ValueError('041 observed initializer coordinates')
        draws=[x for x in t['draws'] if x['root']==root]
        if not draws or any((x['x'],x['y'])!=(92,110) for x in draws):raise ValueError('041 actual positioned draws')
        src=next(a for a in v['archives'] if a['archive']==arc)['source_tpl'];require_hash(ROOT/src['path'],src['sha256']);text=(ROOT/src['path']).read_text(encoding='utf-8-sig')
        match=re.search(r'^script '+str(script)+r' \w+ \{(.*?)(?=^script |\Z)',text,re.M|re.S)
        if not match or not re.search(r'positionText\s+left = 92\s+top = 110',match[1]):raise ValueError('041 explicit source positioning explains observed draws')
        details.append(dict(family=family,archive=arc,script=script,load=load,actual_root=root,common_lr=call['registers']['14'],outer_lr=outer,native_payload_sha256=sha(payload),default_xy=[52,110],explicit_script_xy=[92,110],observed_draws=len(draws),native_source_and_carry_verified=True,new041_units_runtime_verified=0))
    # Reject numeric-script-only attribution: PET archive65B9E8 also uses script23.
    pet=next(x for x in layout_records(m) if x.get('rom_offset')==0x803460)
    if pet['archive']!='65B9E8':raise ValueError('041 distinct PET root attribution')
    result=dict(passed=True,status='041_OBSERVED040_NATIVE_PROVIDERS_ONLY_NOT_NEW500_ADMISSION',baseline_sha256=s['baseline_sha256'],observations=details,rejected_hypotheses=['Equipment60/mail9 drawing at92 does not refute default52: both original scripts explicitly positionText92. No geometry changed on this evidence.','Mail exit script23 at08803460 belongs to65B9E8, NOT selected raw6FE8D4 whose existing consumer is0888A440. Script number alone is not archive identity.','No selected loads in field/PET exploratory runs does not prove absence, unused source or a game defect.'],new_ROM_applied_units=0,rom_written=False,product_admitted=False,release_eligible=False,dependencies={**evidence,**{p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_native_observations041_v1.py',SOURCE+'/selection.json',SOURCE+'/verification_v3.json',SOURCE+'/carry_verification_v2.json']}},limits=['Equipment60 and mailbox intro9 only: unpositioned quick/guarded mail14/77 and equipment errors71..75 remain unobserved.','No native admission for raw9, secondary tournament, subchip live route or B2 natural acquisition.','Current040 evidence is not041 Korean rendering, saving or whole-game QA.'])
    frozen_write(ROOT/SOURCE/'native_observations_v1.json',result);print('PASS041 exact040 equipment60/mail9 providers; default52 then explicit92; NOT041500 runtime')


if __name__=='__main__':main()
