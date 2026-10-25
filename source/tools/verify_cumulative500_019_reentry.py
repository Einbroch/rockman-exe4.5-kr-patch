"""Native R/B reentry after a single quarantined name-display selection."""
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_005_displays import model
from report_roll_pet import pixels

def main():
    rp=ROOT/'poc/output/pending500_019_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes()
    folder=ROOT/'poc/runtime/pending500-019-v1-name-food-reentry';r=read(folder/'result.json')
    food=next(a for a in m['archives'] if a['archive']=='66BF44');diagnostic={'roots':1,'entries':1,'navi':0,'root':0x08000000+food['rom_offset'],'script':23}
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r['normal_play_checkpoint_eligible'] is not False or r['display_diagnostic']!=diagnostic:raise ValueError('Reentry diagnostic binding')
    if (folder/'checkpoint.mss').exists() or not (folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Checkpoint quarantine')
    for name,h in r['artifacts'].items():require_hash(folder/name,h)
    pool,units,expected,streams,ends=model(rom,m,cfg,'65E8B8',10,255,asset_folder='analysis/pending_insertion_500_019_cumulative_v1')
    if len(units)!=1:raise ValueError('Native reentry literal population')
    if struct.unpack_from('<I',source,0x380D0)[0]!=0x0865E8B8 or struct.unpack_from('<I',rom,0x380D0)[0]!=pool:raise ValueError('Original mail-alert lookup')
    u=units[0];e={s:expected[s] for s in streams[u['id']]};offsets={};row=0;width=0;it=iter(streams[u['id']])
    for ch in u['translation']:
        if ch=='\n':row+=1;width=0;continue
        s=next(it);offsets[s]=row*10752+width*4;width+=struct.unpack_from('<I',rom,m['extension']['advance_offset']+e[s]['index']*4)[0]
        if width>132 or row>2:raise ValueError('Reentry layout')
    # The food-root probe is intentionally not retargeted. Reentry is a
    # different native archive; recover glyph pixels from recorded ROM bytes
    # and the consumer's native VRAM positions, rather than inventing draws.
    frames=[]
    for step in (9,10):
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if read(folder/f'step_{step:03}_display_alias.json')!=diagnostic:raise ValueError('Unexpected repeated read alias')
        if root!=pool or ptr!=ends[u['id']] or rom[ptr-0x08000000:ptr-0x08000000+3]!=bytes.fromhex('E600F1') or tuple(ram[0xFA38:0xFA3A])!=(92,110):raise ValueError('Native reentry root/wait')
        # These positions are independently derived from the compiled literal.
        # They verify ROM->OBJ->screen pixels, not CPU renderer observations.
        draws=[dict(stream=s,glyph_index=g['index'],offset=offsets[s],context=0x0200FA20,color=0) for s,g in e.items()]
        proof=pixels(folder,step,draws,e,rom,m,origin=(92,110))
        frames.append(dict(step=step,id=u['id'],root=root,wait_stream=ptr,cpu_glyph_trace_verified=False,**proof))
    pet=next(a for a in m['archives'] if a['archive']=='65A608');petroot=0x08000000+pet['rom_offset'];owner=None
    for step in (7,8,11,12):
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if root!=petroot or ptr!=petroot+0x57 or tuple(ram[0xFA38:0xFA3A])!=(92,110):raise ValueError('Own PET return boundary')
        if read(folder/f'step_{step:03}_display_alias.json')!=diagnostic:raise ValueError('Return alias population')
        if owner is None:owner=ram[0xE50:0xE5E]
        if owner!=ram[0xE50:0xE5E]:raise ValueError('Native name owner changed')
    region=(92,110,224,150);before=Image.open(folder/'step_007.png').convert('RGB').crop(region).tobytes()
    for step in (8,11,12):
        if Image.open(folder/f'step_{step:03}.png').convert('RGB').crop(region).tobytes()!=before:raise ValueError('PET return text residue or drift')
    frozen_write(ROOT/'analysis/pending500_019_v1/name_reentry_runtime.json',dict(schema=1,passed=True,rom_sha256=m['output_sha256'],receipt_sha256=sha((folder/'result.json').read_bytes()),frames=frames,own_pet_return_text_identical=True,native_name_owner_unchanged=True,read_alias_roots=1,read_alias_entries=1,read_alias_diagnostic=True,natural_event_verified=False,release_eligible=False,limits='R reopens native mail-alert script10 and B restores own PET after one forced food-script selection. Not food-event reentry, natural acquisition, all221 profiles, CPU glyph trace of reentry archive, Hangul input/save or human semantic approval.'))
    print('PASS one-shot diagnostic -> native R reentry -> B PET return, ROM/OBJ/pixels and owner unchanged')

if __name__=='__main__':main()
