"""Native040 fast-warning initializer and hardware-input observations, not041 ROM QA."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB

SOURCE='analysis/pending_insertion_500_041_source_v8'


def main():
    s=read(SOURCE+'/selection.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes();deps={}
    def receipt(base):
        r=read(base+'/result.json')
        if not r['complete'] or r['return_code']!=0 or r['rom_sha256']!=s['baseline_sha256'] or len(r['loaded_rom_guards'])!=8 or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('041 own exact040 ordinary input observation')
        if (ROOT/base/'loaded_rom_guard_failed.txt').exists():raise ValueError('041 hardware/quick loaded guard')
        deps[base+'/result.json']=sha((ROOT/base/'result.json').read_bytes())
        for name,h in r['artifacts'].items():require_hash(ROOT/base/name,h);deps[base+'/'+name]=h
        parent=read(r['state_origin']);require_hash(ROOT/r['state_origin'],sha((ROOT/r['state_origin']).read_bytes()))
        if not parent['complete'] or parent['rom_sha256']!=s['baseline_sha256'] or parent.get('normal_play_checkpoint_eligible') is False:raise ValueError('041 same-ROM normal parent')
        return r
    base='poc/runtime/pending500-040-native041-equipment-error-v9';r=receipt(base);t=read(base+'/native_consumers041.json');native=lz77_decompress(source,0x6E1068)[0]
    load=[x for x in t['loads'] if x['source']==0x086E1068 and x['destination']==0x0202BA7C]
    calls=[x for x in t['calls'] if x['registers']['0']==0x0202BA7C and x['registers']['1']==70 and x['registers']['14']==0x0804F7BD and x['stack_lr16']==0x0803EFBF]
    if len(load)!=1 or len(calls)!=1 or (ROOT/base/calls[0]['native_dump']).read_bytes()!=native:raise ValueError('041 fast-warning original loader/root/script/native payload')
    call=calls[0];d=[x for x in t['defaults'] if x['frame']==call['frame'] and x['root']==0x0202BA7C];draws=[x for x in t['draws'] if x['root']==0x0202BA7C]
    if len(d)!=1 or (d[0]['x'],d[0]['y'])!=(52,110) or not draws or any((x['x'],x['y'])!=(52,110) for x in draws):raise ValueError('041 fast-warning initialized and actual draw coordinates')
    if not 0<=call['frame']-load[0]['frame']<1000:raise ValueError('041 warning preserved native lifetime')
    helper=source[0x3EFA4:0x3EFC0]
    if rom[0x3EFA4:0x3EFC0]!=helper or struct.unpack_from('<I',source,0x3EFC0)[0]!=0x0202BA7C:raise ValueError('041 warning provider code/root applicability')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ins=list(cs.disasm(helper,0x0803EFA4))
    if sum(i.size for i in ins)!=len(helper):raise ValueError('041 complete warning helper extent')
    for i in ins:
        if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('041 warning helper Thumb1 roundtrip')
    spans=script_spans(native,76);prefix=bytes.fromhex('fc06e702f00000f40017')
    if any(not spans[n].startswith(prefix) for n in range(70,76)):raise ValueError('041 exact same finite source fast initializer')
    selected={u for g in s['groups'] if g['archive']=='6E1068' and g['script'] in range(71,76) for u in g['ids']}
    if len(selected)!=5:raise ValueError('041 exact same-prefix new equipment literals')
    for step in (5,6,7):
        ram=(ROOT/base/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0x2BA7C:0x2BA7C+len(native)]!=native or ram[0xFA38:0xFA3A]!=bytes((52,110)) or struct.unpack_from('<I',ram,0xFA50)[0]!=0x0202BA7C:raise ValueError('041 source warning page/choice clear and native RAM residency')
    inputbase='poc/runtime/pending500-040-native041-input-v1';receipt(inputbase);reads=read(inputbase+'/hardware_inputs041.json')['reads'];byframe={x['frame']:x for x in reads}
    # Actual active-low GBA KEYINPUT at original039A: excludes failed input mapping as explanation.
    if not reads or any(x['address']!=0x04000130 or x['pc']!=0x0800039A for x in reads):raise ValueError('041 native KEYINPUT consumer')
    if any(byframe.get(f,{}).get('value')!=0x03F7 for f in range(31,41)):raise ValueError('041 ten actual Start polls')
    if any(byframe.get(f,{}).get('value')!=0x03FF for f in range(5,25)):raise ValueError('041 no-input hardware negative control')
    result=dict(passed=True,status='041_NATIVE040_QUICK_WARNING_GEOMETRY_AND_INPUT_PROOF_NOT_NEW_ROM',baseline_sha256=s['baseline_sha256'],warning=dict(archive='6E1068',script=70,root=0x0202BA7C,common_lr=0x0804F7BD,outer_lr=0x0803EFBF,default_xy=[52,110],actual_draw_xy=[52,110],glyph_draw_events=len(draws),native_payload_sha256=sha(native),native_parent_loader=True,source_helper_sha256=sha(helper),source_helper_instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str,hex=i.bytes.hex()) for i in ins],new_selected_same_initializer_IDs=sorted(selected),same_initializer_scope='First10 source bytes match exactly for70..75, including original mugshot argument. Does not prove caller/acquisition of71..75.',page_and_choice_source_residency_verified=True),hardware_input=dict(original_key_poll_pc=0x0800039A,start_frames=list(range(31,41)),actual_start_value=0x03F7,idle_value=0x03FF,field_menu_not_acquired=True,conclusion='Start is delivered correctly to the original key poll. Remaining field transition conditions, not controller API, need investigation; no game defect claimed.'),new_ROM_applied_units=0,rom_written=False,product_admitted=False,release_eligible=False,dependencies={**deps,**{p:sha((ROOT/p).read_bytes()) for p in [SOURCE+'/selection.json','tools/verify_quick_native041_v1.py','tools/capture_native_inputs041_v1.py','tools/run_native_inputs041_v1.py','tools/run_native_consumers041_v9.py']}},limits=['Only existing native Japanese warning70 runtime; new041 Korean error strings71..75 not rendered.','No save or normal checkpoint after modified own folder promoted; user saves remain untouched.','Same prefix proves initializer equivalence in this source archive, not every18-Navi caller or all193 quick units.','Tutorial14/secondary50/mail alerts and remaining consumers still need original selection/runtime evidence.'])
    frozen_write(ROOT/SOURCE/'quick_native_v1.json',result);print('PASS041 actual native warning70 default/draw52,110, page/choice RAM lifetime; Start hardware confirmed; NOT new041 ROM')


if __name__=='__main__':main()
