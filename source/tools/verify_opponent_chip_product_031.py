"""Actual030 four ordered pages, valid native standard/Giga max8 names."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels
from capture_opponent_chip_product_031 import CASES
from bench_opponent_chips_product_031 import FIELDS
from inspect_profile_chip_pools_030 import OUT as CENSUS
from chip_profile_bounds_030 import bounds


def main():
    rp=ROOT/'poc/output/pending500_031_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();limits={name:dict(field=f['record']+1) for name,f in FIELDS.items()}
    # Native initializer stores caller r1=0 before the aliased header read.
    # The diagnostic redirects only that table offset, not the saved script ID.
    guard=bytes.fromhex('286369704900415a4018e8626863')
    if source[0x4FB70:0x4FB7E]!=guard or rom[0x4FB70:0x4FB7E]!=guard:raise ValueError('030 native stored-index-before-alias contract')
    selection=read('analysis/pending_insertion_500_031_selected500_v1/selection.json');manifest=read('analysis/pending_insertion_500_031_carry_v1/preflight.json');pages=[];receipts=[];images=[]
    for case,(arc,script,provider) in CASES.items():
        folder=ROOT/'poc/runtime'/('pending500-031-v1-opponent-'+case);receipt=read(folder/'result.json')
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] or (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists():raise ValueError('030 diagnostic artifact/quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
        record=next(r for r in manifest['archives'] if r['archive']==arc);asset=read(record['merged_asset']['path']);pool,units,ee,streams,ends=model(rom,m,cfg,arc,script,record['script_count'],asset=asset)
        if receipt['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('030 exact root/script')
        g=next(g for g in selection['groups'] if g['archive']==arc and g['script']==script);geometry=g['geometry'][0]['pages'];cap=8;by={u['id']:u for u in units}
        if len(geometry)!=2:raise ValueError('030 finite three-page cases')
        font=m['extension']['normal_font_offset'];census=read(CENSUS)
        chip_base=struct.unpack_from('<I',source,0x1A8A0)[0]-0x08000000;kind=2 if provider=='printFavGigaChip' else 0
        fixture=next(r for r in census['names'] if r['chip_id']==9)
        encoded=bytes.fromhex(fixture['raw_hex'])
        if len(encoded)!=9 or encoded[-1]!=0xE5:raise ValueError('030 finite max chip fixture')
        for index in encoded[:-1]:
            if rom[font+index*96:font+(index+1)*96]!=source[0x608758+index*96:0x608758+(index+1)*96] or struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]!=11:raise ValueError('030 native chip glyph/metric')
        for ordinal,page in enumerate(geometry):
            step=3+ordinal*2;cp=f'step_{step:03}';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'));events=read(folder/(cp+'_profile_trace.json'))['events']
            if len(events)!=1 or events[0]['cap']!=cap or events[0]['field']!=limits[provider]['field'] or not events[0]['hex'].lower().startswith(encoded.hex()) or not events[0]['restored']:raise ValueError('030 native field copy/restoration')
            event=events[0];ids=[p['id'] for p in page['parts'] if 'id' in p];expected={s:ee[s] for k in ids for s in streams[k]};offsets={};row=0;width=0;observed_widths=[]
            for part in page['parts']:
                if 'id' in part:
                    u=by[part['id']];it=iter(streams[u['id']])
                    for ch in u['translation']:
                        if ch=='\n':observed_widths.append(width);row+=1;width=0;continue
                        s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+ee[s]['index']*4)[0]
                elif part.get('kind')==provider and ordinal==0:
                    if part['bound']!=cap*11:raise ValueError('030 logical cap/width bound')
                    for n,index in enumerate(encoded[:-1]):
                        glyph=rom[font+index*96:font+(index+1)*96]
                        s=event['output']+n;expected[s]=dict(ch='native-chip',index=index,record=glyph,id=provider);offsets[s]=row*10752+width*4;width+=11
                else:raise ValueError('030 unmodeled runtime sample provider')
            observed_widths.append(width)
            if observed_widths!=page['widths']:raise ValueError('030 complete aggregate row widths')
            draws={d['stream']:d for d in trace['draws'] if d['stream'] in expected}
            if set(draws)!=set(expected) or any(d['context']!=0x0200FA20 or d['glyph_index']!=expected[s]['index'] or d['offset']!=offsets[s] for s,d in draws.items()):raise ValueError('030 complete literal/RAM-provider glyphs and offsets')
            if tuple(ram[0xFA38:0xFA3A])!=(92,110) or ram[0xFA21]!=0 or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or struct.unpack_from('<I',ram,0xFA4C)[0]!=ends[ids[-1]]:raise ValueError('030 ordered script/page/wait')
            end=ends[ids[-1]]-0x08000000
            if rom[end:end+2]!=b'\xE6\x00':raise ValueError('030 exact native keyWait')
            counts=Counter(e['index'] for e in expected.values());reads={e['index']:e['reads'] for e in trace['font_reads']}
            if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('030 font CPU read coverage')
            proof=pixels(folder,step,list(draws.values()),expected,rom,m,origin=(92,110));im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
            for s,e in expected.items():
                rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e['index']*4)[0]
                occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(92+xx//4,92+xx//4+w))
            vacant={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138)}-occupied
            if any(im.getpixel(pt)!=im.getpixel((233,110)) for pt in vacant):raise ValueError('030 prior-page/provider stale background')
            images.append(im);pages.append(dict(case=case,step=step,ids=ids,provider=provider if ordinal==0 else None,native_cap=cap if ordinal==0 else None,aggregate_widths=observed_widths,record_temporarily_seeded_and_restored=True,vacant_pixels=len(vacant),exact_ordered_wait=True,**proof))
        exitram=(folder/'step_007_gbaExtWorkRam.bin').read_bytes();own=next(r for r in m['archives'] if r['archive']=='65A608')
        if struct.unpack_from('<I',exitram,0xFA50)[0]!=0x08000000+own['rom_offset']:raise ValueError('030 native normal PET return')
    out=ROOT/'analysis/pending500_031_v1';sheet=Image.new('RGB',(720,320))
    for i,im in enumerate(images):sheet.paste(im,(i%3*240,i//3*160))
    sheet.save(out/'opponent_samples.png')
    frozen_write(out/'opponent_runtime.json',dict(schema=1,passed=True,rom_sha256=sha(rom),pages=pages,receipts=receipts,contact_sheet_sha256=sha((out/'opponent_samples.png').read_bytes()),both_normal_pet_returns=True,checker=dict(path='tools/verify_opponent_chip_product_031.py',sha256=sha((ROOT/'tools/verify_opponent_chip_product_031.py').read_bytes())),stored_caller_script_index=0,runtime_tested=True,release_eligible=False,limits='Quarantined GutsMan62/71 read aliases on own Rockman host. Valid native chip9 max8 names are temporarily seeded and restored after real F90C. Four new Korean pages, RAM/font/OBJ/pixels, row widths, clearing, waits and PET return only. Native chip names themselves remain Japanese. Not natural speaker/caller, acquisition/default/import/all writers, persistence, whole500 approval, Hangul or hardware/audio evidence.'))
    print('PASS030 four ordered pages/native8 standard+Giga chip names/RAM-font-OBJ-pixels/clearing/waits/PET returns')


if __name__=='__main__':main()
