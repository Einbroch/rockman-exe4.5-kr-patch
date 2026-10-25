"""Bounded027 max8/cap4 profile ROM/RAM glyph -> OBJ -> screen checks."""
import struct
from collections import Counter
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels
from capture_profile_display_027 import CASES
from profile_provider_bounds_027_v2 import bounds


def main():
    rp=ROOT/'poc/output/pending500_027_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();limits=bounds(source,rom)
    selection=read('analysis/pending_insertion_500_027_selection_v1/selection.json');manifest=read('analysis/pending_insertion_500_027_carry_v2/preflight.json');pages=[];receipts=[];images=[]
    for case,(arc,script,provider) in CASES.items():
        folder=ROOT/'poc/runtime'/('pending500-027-v1-raw-'+case);receipt=read(folder/'result.json')
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt['normal_play_checkpoint_eligible'] or (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists():raise ValueError('027 diagnostic artifact/quarantine')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        receipts.append(dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())))
        record=next(r for r in manifest['archives'] if r['archive']==arc);asset=read(record['merged_asset']['path'])
        pool,units,ee,streams,ends=model(rom,m,cfg,arc,script,record['script_count'],asset=asset)
        if receipt['display_diagnostic']!=dict(roots=1,entries=1,navi=0,root=pool,script=script):raise ValueError('027 exact root/script')
        g=next(g for g in selection['groups'] if g['archive']==arc and g['script']==script);page=g['geometry'][0]['pages'][0]
        cp='step_003';ram=(folder/(cp+'_gbaExtWorkRam.bin')).read_bytes();trace=read(folder/(cp+'_roll_pet.json'));field=read(folder/(cp+'_profile_trace.json'))['events']
        cap=limits[provider]['logical_cap'];expected_bytes=bytes.fromhex('e406')*cap+b'\xE5'
        if len(field)!=1 or field[0]['cap']!=cap or field[0]['field']!=limits[provider]['source_field'] or field[0]['hex'].lower()!=expected_bytes.hex() or not field[0]['restored']:raise ValueError('027 native reader copy/restoration')
        info=field[0];ids=[p['id'] for p in page['parts'] if 'id' in p];by={u['id']:u for u in units};expected={s:ee[s] for k in ids for s in streams[k]};offsets={};row=0;width=0
        index=234;font=m['extension']['normal_font_offset'];glyph=rom[font+index*96:font+(index+1)*96]
        if glyph!=source[0x608758+index*96:0x608758+(index+1)*96] or struct.unpack_from('<I',rom,m['extension']['advance_offset']+index*4)[0]!=11:raise ValueError('027 source native provider glyph/width')
        for part in page['parts']:
            if 'id' in part:
                u=by[part['id']];it=iter(streams[u['id']])
                for ch in u['translation']:
                    if ch=='\n':row+=1;width=0;continue
                    s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+ee[s]['index']*4)[0]
            elif part.get('kind')==provider:
                if part['bound']!=cap*11:raise ValueError('027 logical provider bound')
                for n in range(cap):
                    s=info['output']+n*2;expected[s]=dict(ch='native-max',index=index,record=glyph,id=provider);offsets[s]=row*10752+width*4;width+=11
            else:raise ValueError('027 sample unmodeled provider')
        draws={d['stream']:d for d in trace['draws'] if d['stream'] in expected}
        if set(draws)!=set(expected) or any(d['context']!=0x0200FA20 or d['glyph_index']!=expected[s]['index'] or d['offset']!=offsets[s] for s,d in draws.items()):raise ValueError('027 complete literal/provider glyphs and independent aggregate offsets')
        if tuple(ram[0xFA38:0xFA3A])!=(92,110) or struct.unpack_from('<I',ram,0xFA50)[0]!=pool or struct.unpack_from('<I',ram,0xFA4C)[0]!=ends[ids[-1]]:raise ValueError('027 native page origin/wait')
        end=ends[ids[-1]]-0x08000000
        if rom[end:end+2]!=b'\xE6\x00':raise ValueError('027 exact keyWait')
        counts=Counter(e['index'] for e in expected.values());reads={e['index']:e['reads'] for e in trace['font_reads']}
        if any(reads.get(i,0)<24*n for i,n in counts.items()):raise ValueError('027 font CPU reads')
        proof=pixels(folder,3,list(draws.values()),expected,rom,m,origin=(92,110))
        im=Image.open(folder/(cp+'.png')).convert('RGB');occupied=set()
        for s,e in expected.items():
            rr,xx=divmod(offsets[s],10752);w=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e['index']*4)[0]
            occupied.update((x,y) for y in range(110+rr*14,122+rr*14) for x in range(92+xx//4,92+xx//4+w))
        vacant={(x,y) for y in range(110,150) for x in range(92,234) if not(x>=224 and y>=138)}-occupied
        if any(im.getpixel(pt)!=im.getpixel((233,110)) for pt in vacant):raise ValueError('027 background outside composed text')
        last=7 if case=='school-max' else 5;exitram=(folder/f'step_{last:03}_gbaExtWorkRam.bin').read_bytes();own=next(r for r in m['archives'] if r['archive']=='65A608')
        if struct.unpack_from('<I',exitram,0xFA50)[0]!=0x08000000+own['rom_offset']:raise ValueError('027 normal PET return')
        images.append(im);pages.append(dict(case=case,ids=ids,provider=provider,native_cap=cap,provider_pixels=cap*11,record_temporarily_seeded_and_restored=True,exact_wait_and_independent_aggregate_offsets=True,vacant_pixels=len(vacant),normal_pet_return=True,**proof))
    out=ROOT/'analysis/pending500_027_v1';sheet=Image.new('RGB',(480,160))
    for i,im in enumerate(images):sheet.paste(im,(i*240,0))
    sheet.save(out/'profile_samples.png')
    frozen_write(out/'profile_runtime.json',dict(schema=1,passed=True,rom_sha256=sha(rom),pages=pages,receipts=receipts,contact_sheet_sha256=sha((out/'profile_samples.png').read_bytes()),runtime_tested=True,release_eligible=False,limits='Two quarantined root/table-alias pages and temporary max-width valid native profile records, restored after real F90C copy. Source record acquisition/defaults/import, natural caller, all500 semantics, other six providers in GBA, persistence, Hangul input and hardware/audio remain unverified.'))
    print('PASS027 max8/max4 real F90C/RAM->font->OBJ/pixels/aggregate offsets/wait/PET return')


if __name__=='__main__':main()
