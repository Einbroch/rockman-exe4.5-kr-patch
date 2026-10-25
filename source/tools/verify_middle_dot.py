"""Same translated payloads, explicit normal middle-dot font and preserved jamo identities."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs
from verify_pending500_002_rom import clones,at_path,read_payload
from keyitem_rom_data import verify_final

def read(p):return json.loads(p.read_text(encoding='utf8'))

def main():
    bp=ROOT/'poc/output/exe45_ko_development_pending500_006_v1.gba';rp=ROOT/'poc/output/exe45_ko_development_middle_dot_v1.gba';old=read(bp.with_suffix('.json'));m=read(rp.with_suffix('.json'));require_hash(bp,old['output_sha256']);require_hash(rp,m['output_sha256']);base=bp.read_bytes();rom=rp.read_bytes()
    require_hash(rp.with_name(rp.stem+'_repro.gba'),sha(rom));cfg=read(ROOT/'project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    if m['translated_units']!=old['translated_units'] or m['translated_units']!=5837:raise ValueError('No new literal claim')
    current={r['archive']:r for r in m['archives']}
    for path,r in clones(old):
        n=current[r['archive']] if path[0]=='archives' else at_path(m,path)
        if read_payload(base,r)!=read_payload(rom,n):raise ValueError('Translated payload changed '+str(path))
    a,b=old['extension'],m['extension'];prefix=(a['legacy_index_view']+11173)*96
    if base[a['normal_font_offset']:a['normal_font_offset']+prefix]!=rom[b['normal_font_offset']:b['normal_font_offset']+prefix]:raise ValueError('Legacy/Hangul/comma changed')
    idx=b['legacy_index_view']+11173;record=rom[b['normal_font_offset']+idx*96:b['normal_font_offset']+(idx+1)*96]
    glyph=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],{'·'})['·']
    if record!=glyph or not any(glyph) or struct.unpack_from('<I',rom,b['advance_offset']+idx*4)[0]!=12:raise ValueError('Middle-dot glyph/advance')
    for ch,index in old['hangul_keyboard_glyphs']['mapping'].items():
        new_index=m['hangul_keyboard_glyphs']['mapping'][ch]
        if new_index!=index+1 or base[a['normal_font_offset']+(a['legacy_index_view']+index)*96:a['normal_font_offset']+(a['legacy_index_view']+index+1)*96]!=rom[b['normal_font_offset']+(b['legacy_index_view']+new_index)*96:b['normal_font_offset']+(b['legacy_index_view']+new_index+1)*96]:raise ValueError('Jamo identity after slot shift')
    verify_final(source,rom,m['keyitem_rom'])
    out=ROOT/'analysis/middle_dot_v1/integration.json'
    if out.exists():raise ValueError('Preserve evidence')
    result=dict(passed=True,rom=str(rp.relative_to(ROOT)),rom_sha256=sha(rom),source_unchanged=True,independent_rebuild_identical=True,total_units=5837,new_units=0,
        all_prior_payloads_identical=True,legacy_hangul_comma_font_identical=True,middle_dot_index=11173,normal_middle_dot_record_sha256=sha(record),jamo_identity_preserved=True,
        jamo_slot_shift=1,keyboard_input_hooks_installed=False,release_eligible=False,limits='Glyph support only. Pending19 literals and next500 merge still unapplied; normal runtime separately bound.')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS middle-dot normal glyph; all5837 prior payloads preserved; new literals0')

if __name__=='__main__':main()
