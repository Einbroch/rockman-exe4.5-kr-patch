"""Actual029 four ordered pages, initialized max6/max8 arrays and clearing."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels
CASES={'initializer-older-bro':('65CC78',5,'printOlderBro'),'initializer-fav-show':('65CC78',35,'printFavShow')}
from array_provider_bounds_029 import bounds


def main():
    rp=ROOT/'poc/output/pending500_029_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();limits=bounds(source,rom)
    # Native initializer stores caller r1=0 before the aliased header read.
    # The diagnostic redirects only that table offset, not the saved script ID.
    guard=bytes.fromhex('286369704900415a4018e8626863')
    if source[0x4FB70:0x4FB7E]!=guard or rom[0x4FB70:0x4FB7E]!=guard:raise ValueError('029 native stored-index-before-alias contract')
    selection=read('analysis/pending_insertion_500_029_selection_v1/selection.json');manifest=read('analysis/pending_insertion_500_029_carry_v1/preflight.json');pages=[];receipts=[];images=[]
    for case,(arc,script,provider) in CASES.items():
        folder=ROOT/'poc/runtime'/('pending500-029-v1-raw-'+case);receipt=read(folder/'result.json')
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] or (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists():raise ValueError('029 diagnostic artifact/quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
        record=next(r for r in manifest['archives'] if r['archive']==arc);asset=read(record['merged_asset']['path']);pool,units,ee,streams,ends=model(rom,m,cfg,arc,script,record['script_count'],asset=asset)
        if receipt['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('029 exact root/script')
        g=next(g for g in selection['groups'] if g['archive']==arc and g['script']==script);geometry=g['geometry'][0]['pages'];cap=limits[provider]['logical_cap'];by={u['id']:u for u in units}
        if len(geometry)!=2:raise ValueError('029 finite three-page cases')
        index=234;font=m['extension']['normal_font_offset'];glyph=rom[font+index*96:font+(index+1)*96]
        if glyph!=source[0x608758+index*96:0x608758+(index+1)*96] or struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]!=11:raise ValueError('029 native max fixture glyph/metric')
        for ordinal,page in enumerate(geometry):
            step=37+ordinal*2;cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'));init=read(folder/(cp+'_initializer_trace.json'))
            if not init['seeded'] or not init['restored'] or init['after_writes']:raise ValueError('029 initializer/cache restoration/lifetime')
            event=dict(output=0x02010AC0);ids=[p['id'] for p in page['parts'] if 'id' in p];expected={s:ee[s] for k in ids for s in streams[k]};offsets={};row=0;width=0;observed_widths=[]
            for part in page['parts']:
                if 'id' in part:
                    u=by[part['id']];it=iter(streams[u['id']])
                    for ch in u['translation']:
                        if ch=='\n':observed_widths.append(width);row+=1;width=0;continue
                        s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+ee[s]['index']*4)[0]
                elif part.get('kind')==provider:
                    if part['bound']!=cap*11:raise ValueError('029 logical cap/width bound')
                    for n in range(cap):
                        s=event['output']+n*2;expected[s]=dict(ch='native-max',index=index,record=glyph,id=provider);offsets[s]=row*10752+width*4;width+=11
                else:raise ValueError('029 unmodeled runtime sample provider')
            observed_widths.append(width)
            if observed_widths!=page['widths']:raise ValueError('029 complete aggregate row widths')
            draws={d['stream']:d for d in trace['draws'] if d['stream'] in expected}
            if set(draws)!=set(expected) or any(d['context']!=0x0200FA20 or d['glyph_index']!=expected[s]['index'] or d['offset']!=offsets[s] for s,d in draws.items()):raise ValueError('029 complete literal/RAM-provider glyphs and offsets')
            if tuple(ram[0xFA38:0xFA3A])!=(92,110) or ram[0xFA21]!=0 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or struct.unpack_from('<I',ram,0xFA4C)[0]!=ends[ids[-1]]:raise ValueError('029 ordered script/page/wait')
            end=ends[ids[-1]]-0x08000000
            if rom[end:end+2]!=b'\xE6\x00':raise ValueError('029 exact native keyWait')
            counts=Counter(e['index'] for e in expected.values());reads={e['index']:e['reads'] for e in trace['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('029 font CPU read coverage')
            proof=pixels(folder,step,list(draws.values()),expected,rom,m,origin=(92,110));im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
            for s,e in expected.items():
                rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e['index']*4)[0]
                occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(92+xx//4,92+xx//4+w))
            vacant={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138)}-occupied
            if any(im.getpixel(pt)!=im.getpixel((233,110)) for pt in vacant):raise ValueError('029 prior-page/provider stale background')
            images.append(im);pages.append(dict(case=case,step=step,ids=ids,provider=provider if any(p.get('kind')==provider for p in page['parts']) else None,native_cap=cap if any(p.get('kind')==provider for p in page['parts']) else None,aggregate_widths=observed_widths,record_temporarily_seeded_and_restored=True,vacant_pixels=len(vacant),exact_ordered_wait=True,**proof))
        exitram=(folder/'step_041_gbaExtWorkRam.bin').read_bytes();own=next(r for r in m['archives'] if r['archive']=='65A608')
        if struct.unpack_from('<I',exitram,0xFA50)[0]!=0x08000000+own['rom_offset']:raise ValueError('029 native normal PET return')
    out=ROOT/'analysis/pending500_029_v1';sheet=Image.new('RGB',(720,320))
    for i,im in enumerate(images):sheet.paste(im,(i%3*240,i//3*160))
    sheet.save(out/'profile_samples.png')
    frozen_write(out/'profile_runtime.json',dict(schema=1,passed=True,rom_sha256=sha(rom),pages=pages,receipts=receipts,contact_sheet_sha256=sha((out/'profile_samples.png').read_bytes()),both_normal_pet_returns=True,checker=dict(path='tools/verify_profile_product_029.py',sha256=sha((ROOT/'tools/verify_profile_product_029.py').read_bytes())),stored_caller_script_index=0,runtime_tested=True,release_eligible=False,limits='Quarantined root/table aliases to GutsMan scripts5/35 while own Rockman remains PET host. Temporary max6/max8 valid native array records are seeded before actual startup initializer and restored immediately after it. Four ordered pages, native cache lifetime, font CPU/RAM/OBJ/pixels, row offsets, page clearing and PET return only. Not natural character/script selection, complete default/import/writer audit, persistence, whole500 approval, Hangul or hardware/audio evidence.'))
    print('PASS029 four ordered pages/max6 older-bro+max8 fav-show/RAM-font-OBJ-pixels/clearing/waits/PET returns')


if __name__=='__main__':main()


