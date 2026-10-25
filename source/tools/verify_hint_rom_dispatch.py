"""Original script0/flag dispatcher in the actual ROM clone; diagnostic, not natural A3."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from archive_scripts import script_spans

def main():
    rp=ROOT/'poc/output/pending500_022_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();r=next(r for r in m['keyitem_rom']['hint_archives'] if r['archive']=='786D38');pool=0x08000000+r['rom_offset'];payload=rom[r['rom_offset']:r['rom_offset']+r['compiled_bytes']];native=rom[r['native_copy_offset']:r['native_copy_offset']+r['native_copy_bytes']]
    folder=ROOT/'poc/runtime/pending500-022-v2-hint-dispatch';receipt=read(folder/'result.json');d=receipt['hint_diagnostic']
    if not receipt['complete'] or receipt['rom_sha256']!=m['output_sha256'] or receipt['normal_play_checkpoint_eligible'] is not False or not receipt['original_dispatcher_preserved'] or receipt['table_read_value_changed'] is not False:raise ValueError('Original dispatcher intervention scope')
    if {k:v for k,v in d.items() if k!='wrapper_cycles'}!=dict(loads=1,scenes=2,entries=2,calls=2,root=pool,script=0):raise ValueError('Original dispatcher calls')
    for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
    if (folder/'checkpoint.mss').exists() or not(folder/'diagnostic_checkpoint.mss').exists():raise ValueError('Dispatcher checkpoint quarantine')
    spans=script_spans(payload,255);old=script_spans(native,255)
    if spans[0]!=old[0]:raise ValueError('Entry dispatcher changed')
    pages=[]
    for step in (52,56):
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        if root!=pool or rom[ptr-0x08000000:ptr-0x08000000+2]!=bytes.fromhex('e600') or ram[0x3D800:0x3D800+len(native)]!=native or ram[0x4AD4]!=0xB0 or ram[0x4AD1]!=0:raise ValueError('Dispatcher continuation/root/native RAM/world context')
        scripts=[i for i,b in enumerate(spans) if pool+int.from_bytes(payload[i*2:i*2+2],'little')<=ptr<pool+int.from_bytes(payload[i*2:i*2+2],'little')+len(b)]
        if scripts!=[10] or spans[10]!=old[10]:raise ValueError('Expected original flag checks/default script10 unchanged')
        pages.append(dict(step=step,script=10,wait_stream=ptr,root=root,original_default_body_retained=True))
    frozen_write(ROOT/'analysis/pending500_022_v2/hint_dispatch.json',dict(schema=1,passed=True,rom_sha256=m['output_sha256'],receipt_sha256=sha((folder/'result.json').read_bytes()),original_entry_script0_byte_identical=True,original_script10_byte_identical=True,pages=pages,wrapper_cycles=d['wrapper_cycles'],script_table_read_changed=False,read_alias_diagnostic=True,natural_A3_event_verified=False,additional_translated_units=0,release_eligible=False,limits='Same-ROM native loader and wrapper-scene read aliases. Original script0 jump and script10 flag checks/default Japanese body execute with no table-entry change. Not natural A3/progression/provider outcomes, every branch, or an additional translation.'))
    print('PASS original script0 -> flag dispatcher/default script10 in ROM clone; exit/reentry; no table-entry change')

if __name__=='__main__':main()
