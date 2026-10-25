"""Native normal renderer middle-dot record/pixels through a quarantined rank read alias."""
import json,struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from report_roll_pet import pixels
from verify_pending500_005_displays import model

def main():
    rp=ROOT/'poc/output/exe45_ko_development_middle_dot_v1.gba';m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    folder=ROOT/'poc/runtime/middle-dot-v1-glyph';r=json.loads((folder/'result.json').read_text(encoding='utf8'));d=r['middle_dot_diagnostic']
    if not r['complete'] or r['rom_sha256']!=sha(rom) or r['normal_play_checkpoint_eligible'] is not False or d['aliases']<=0:raise ValueError('Rank alias binding')
    for name,h in r['artifacts'].items():require_hash(folder/name,h)
    root,units,expected,streams,ends=model(rom,m,cfg,'68C2CC',3,5,'analysis/pending_insertion_500_006_rom')
    token=d['stream'];dot_index=m['extension']['legacy_index_view']+11173
    if expected[token]['ch']!=',' or rom[token-0x08000000:token-0x08000000+4]!=bytes.fromhex('f9fca42b'):raise ValueError('Original comma preserved')
    glyph=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],{'·'})['·'];expected[token]=dict(expected[token],ch='·',index=dot_index,record=glyph)
    proofs=[]
    for ordinal,step in enumerate((2,4)):
        key=units[ordinal]['id'];state=json.loads((folder/f'step_{step:03}_roll_pet.json').read_text(encoding='utf8'));ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if struct.unpack_from('<2I',ram,0xFA4C)!=(ends[key],root):raise ValueError('Native wait/root')
        last={x['stream']:x for x in state['draws'] if x['stream'] in streams[key]}
        if set(last)!=set(streams[key]):raise ValueError('Literal glyph coverage')
        draws=[last[s] for s in streams[key]];counts=Counter(x['glyph_index'] for x in draws);reads={x['index']:x['reads'] for x in state['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('Font CPU reads')
        if step==2 and last[token]['glyph_index']!=dot_index:raise ValueError('Actual middle-dot selected')
        proofs.append(dict(step=step,**pixels(folder,step,draws,expected,rom,m)))
    result=dict(passed=True,rom_sha256=sha(rom),middle_dot_rank=11173,normal_font_index=dot_index,source_comma_bytes_unchanged=True,glyph_record_sha256=sha(glyph),pages=proofs,
        new_translated_units=0,release_eligible=False,limits='Quarantined one-byte rank read alias, normal renderer glyph-supply evidence only; pending19 translations remain unapplied and no keyboard/save claim.')
    out=ROOT/'analysis/middle_dot_v1/glyph_runtime.json'
    if out.exists():raise ValueError('Preserve evidence')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS actual middle-dot normal font consumption and OBJ screen pixels')

if __name__=='__main__':main()
