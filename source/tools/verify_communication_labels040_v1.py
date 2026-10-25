"""039 Japanese small-label consumer observation; NOT Korean-label runtime."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();rp=ROOT/'poc/output/pending500_039_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);native=lz77_decompress(source,0x6F56B8)[0];d=ROOT/'poc/runtime/pending500-039-label-trace040-v2';r=read(d/'result.json');q=ROOT/'poc/runtime/pending500-039-label-trace040-v1';r1=read(q/'result.json')
    for folder,receipt in [(d,r),(q,r1)]:
        if not receipt['complete'] or receipt['return_code']!=0 or receipt['rom_sha256']!=m['output_sha256'] or len(receipt['loaded_rom_guards'])!=6:raise ValueError('040 label source observation artifact')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        origin=read(receipt['state_origin']);require_hash(ROOT/'poc/runtime/pending500-039-communication-v1-06/checkpoint.mss',receipt['state_sha256'])
        if origin['rom_sha256']!=m['output_sha256'] or receipt['state_sha256']!=origin['artifacts']['checkpoint.mss']:raise ValueError('040 own039 before-LZ checkpoint')
    trace=read(d/'communication_labels.json');entries=trace['entries'];glyphs=trace['glyphs'];starts={}
    for i in range(59):starts.setdefault(0x02024000+struct.unpack_from('<H',native,2*i)[0],[]).append(i)
    if len(entries)!=5 or len(glyphs)!=59:raise ValueError('040 finite source-menu parser observation')
    observed=[]
    for x in entries:
        regs=x['registers'];p=regs['0']
        if p not in starts or regs['14']!=0x080554BA or regs['6'] not in (0x08601738,0x08619EF8):raise ValueError('040 original small parser/provider contract')
        observed.append(dict(source_stream=p,source_script_aliases=starts[p],provider=regs['6'],caller_lr=regs['14'],incoming_r4=regs['4'],incoming_r5=regs['5'],incoming_r7=regs['7']))
    providers=Counter(x['registers']['6'] for x in glyphs)
    if providers!={0x08601738:52,0x08619EF8:7}:raise ValueError('040 finite original glyph providers')
    for step in (1,2):
        mem=(d/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();iw=(d/f'step_{step:03}_gbaIntWorkRam.bin').read_bytes()
        if mem[0x24000:0x24000+len(native)]!=native or iw[0x6840:0x6880]!=source[0x1EF740:0x1EF780]:raise ValueError('040 original RAM/copy-resident parser identity')
    watch=read(q/'textread_final.json')
    if watch['watch_start']!=0x020240A3 or watch['watch_end']!=0x020240BF or not any(x['pc']=='0x0300684E' and x['reads']==28 for x in watch['sites']):raise ValueError('040 actual original script5/6 small-text reads')
    paths=['tools/verify_communication_labels040_v1.py','tools/run_communication_label_trace040_v1.py','tools/run_communication_label_trace040_v2.py','tools/capture_communication_labels040_v1.py'];receipts={str((p/'result.json').relative_to(ROOT)):sha((p/'result.json').read_bytes()) for p in (d,q)}
    frozen_write(ROOT/'analysis/pending_insertion_500_040_source_v2/communication_labels_boundary_v1.json',dict(passed=True,scope=__doc__,rom_sha256=m['output_sha256'],source_sha256=sha(source),native_archive='6F56B8',native_RAM_bytes=len(native),observed_source_small_parser_entry=0x03006824,observed_source_glyph_copier=0x0300689C,read_callback_PC=0x0300684E,copied_instruction_identity=dict(RAM_start=0x03006840,ROM_offset=0x1EF740,bytes=64,sha256=sha(source[0x1EF740:0x1EF780])),entry_observations=observed,source_glyph_provider_counts={hex(k):v for k,v in providers.items()},watch=watch,receipts=receipts,no_game_RAM_or_ROM_writes=True,no_forced_calls=True,normal_same039_state_before_loader=True,labels_are_text_scripts_not_baked_bitmap=True,ROM_written=False,new_units_applied=0,Korean_label_runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},limits=['Original Japanese source labels only. Entry r4/r5/r7 are observations, not a confirmed capacity contract.','Stats and option labels use different native providers; Korean glyph role/color and metrics need consumer-specific verification.','Reader caller/root mapping and ROM clone relocation for labels not implemented. No font or global parser hook has been changed.','The new040500 selection currently excludes small-label IDs; changing that selection requires a separate pinned cohort and full revalidation.']))
    print('PASS040 original labels: same039 native RAM -> small parser -> two original glyph providers; NOT Korean labels')


if __name__=='__main__':main()
