"""Bind native field loads to 021; deliberately no grown-payload safety claim."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress,parse_tpi

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rp=ROOT/'poc/output/pending500_021_v1.gba';meta=read(rp.with_suffix('.json'));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    paths=['poc/runtime/pending500-022-weekday-complete-trace','poc/runtime/pending500-022-weekday-complete'];receipts=[]
    for path in paths:
        folder=ROOT/path;r=read(folder/'result.json')
        if not r['complete'] or r['rom_sha256']!=meta['output_sha256'] or r['return_code'] or r['steps_expected']!=r['steps_captured']:raise ValueError('Native runtime binding')
        for n,h in r['artifacts'].items():require_hash(folder/n,h)
        receipts.append(dict(path=path+'/result.json',sha256=sha((folder/'result.json').read_bytes()),probe=r['probe'],state_origin=r['state_origin']))
    trace=read(ROOT/paths[0]/'exectrace_final.json');sites={x['pc']:x for x in trace['sites']}
    if sites['0x0804F712']['hits']!=1:raise ValueError('Field loader crossing not observed')
    ram=(ROOT/paths[1]/'step_034_gbaExtWorkRam.bin').read_bytes();rows=parse_tpi(ROOT/cfg['text_catalog']['path']);loads=[]
    for pc,dest in [('0x0804F724',0x02039800),('0x0804F730',0x0203C800),('0x0804F744',0x0203D800)]:
        event=sites[pc]
        if event['hits']!=1 or event['first_regs']['cpu.r1']!=dest:raise ValueError('Native destination observation')
        address=event['first_regs']['cpu.r0'];at=address-0x08000000;payload,used=lz77_decompress(rom,at)
        if source[at:at+used]!=rom[at:at+used]:raise ValueError('Observed native source changed')
        if ram[dest-0x02000000:dest-0x02000000+len(payload)]!=payload:raise ValueError('Separate same-route snapshot load bytes')
        loads.append(dict(pc=pc,source_rom_offset=at,destination=dest,payload_bytes=len(payload),stored_consumed_bytes=used,payload_sha256=sha(payload),same_rom_same_input_snapshot_matches=True,catalog_rows=[r['line'] for r in rows if r['offset']==at],capacity_verified=False))
    frozen_write(ROOT/'analysis/pending_insertion_500_022_storage_v1/native_loader.json',dict(schema=1,rom_sha256=meta['output_sha256'],source_sha256=sha(source),receipts=receipts,loads=loads,consumer_hits=sites['0x0804F7FC']['hits'],normal_input_only=True,ram_or_flag_injection=False,new500_installed=False,capacity_verified=False,release_eligible=False,limits='Trace and snapshot are separate 021 executions from the same weekday-pagecycle checkpoint and identical complete actions. Actual native three-load call arguments and matching snapshot payloads observed. No enlarged Korean load, every map/Navi lifetime, hint consumer execution, or RAM capacity proof. Two observed compressed source coordinates have no exact TPI row; retain unresolved inventory candidates, do not silently add/exclude them.'))
    print('PASS native three-load observations; grown candidate capacity remains UNVERIFIED')

if __name__=='__main__':main()
