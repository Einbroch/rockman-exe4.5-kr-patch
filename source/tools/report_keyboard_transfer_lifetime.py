"""Verify normal native editor font/pixels/queue/VRAM; no Hangul integration."""
import json, struct
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read, verify_route
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB


def main():
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    route=ROOT/'poc/runtime/hangul-keyboard-v1-transfer-lifetime'
    result=verify_route(route,identity,set());product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba'
    require_hash(product,identity);rom=product.read_bytes()
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    env=read(route/'transfer_lifetime_environment.json')
    if not env['observer_only'] or not env['no_RAM_or_save_injection']:raise ValueError('unexpected intervention')
    for n,key in [('capture_keyboard_transfer_lifetime.py','tool_sha256'),('capture_keyboard_native.py','native_observer_sha256')]:require_hash(ROOT/'tools'/n,env[key])
    rows=read(route/'step_023_transfer_lifetime.json')['transfers']
    if len(rows)!=860 or len({r['id'] for r in rows})!=len(rows):raise ValueError('observed transfer population')
    tints=set();streams=set();frames=set()
    for i,row in enumerate(rows,1):
        if row['id']!=i or row['not_enqueued'] or row['consumed_frame']!=row['frame']+1 or row['return_frame']!=row['consumed_frame']:raise ValueError('native delayed queue consumption')
        if (row['source'],row['cell_stage'],row['target'],row['bytes'],row['font'],row['cell_counter'])!=(0x0201E800,0x0201E800,0x0600B000,1280,0x08619EF8,0):raise ValueError('native editor render boundary')
        if not 0<=row['queue_count_before']<96 or row['queue_count_after']!=row['queue_count_before']+1 or row['entry']!=0x02012730+20*row['queue_count_before']:raise ValueError('queue entry identity')
        expected=(row['source'],row['target'],row['bytes'],0xFFFFFFFF,2)
        if struct.unpack('<5I',bytes.fromhex(row['entry_hex']))!=expected or (row['consume_source'],row['consume_target'],row['consume_bytes'])!=expected[:3]:raise ValueError('queue -> native transfer arguments')
        pixels=bytes.fromhex(row['stage_at_enqueue'])
        if len(pixels)!=1280 or row['stage_at_consume']!=row['stage_at_enqueue'] or row['vram_after']!=row['stage_at_consume']:raise ValueError('stage lifetime/VRAM transfer')
        stream=bytes.fromhex(row['stream']);end=stream.index(0xE5)
        if end!=4 or any(b>=0xE4 for b in stream[:end]):raise ValueError('outside observed native singles')
        indices=list(stream[:end])+[0]*16;at=row['font']-0x08000000
        cells=b''.join(rom[at+index*64:at+(index+1)*64] for index in indices)
        matches=[]
        for tint in range(4):
            transformed=b''.join(struct.pack('<I',(struct.unpack_from('<I',cells,k)[0]+0x44444444*tint)&0xFFFFFFFF) for k in range(0,1280,4))
            if transformed==pixels:matches.append(tint)
        if len(matches)!=1:raise ValueError('native font -> stage pixels')
        tints.add(matches[0]);streams.add(stream.hex());frames.add(row['frame'])
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for start,end in [(0x7D4,0x846),(0x848,0x880)]:
        data=original[start:end]
        if rom[start:end]!=data:raise ValueError('queue consumer changed')
        instructions=list(cs.disasm(data,0x08000000+start))
        if sum(i.size for i in instructions)!=len(data):raise ValueError('queue instruction extent')
        for ins in instructions:
            if ins.size not in (2,4) or ins.size==4 and (ins.mnemonic!='bl' or int.from_bytes(ins.bytes[:2],'little')&0xF800!=0xF000 or int.from_bytes(ins.bytes[2:],'little')&0xF800!=0xF800):raise ValueError('queue ISA')
            if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+ins.mnemonic+' '+ins.op_str,ins.address)[0])!=ins.bytes:raise ValueError('queue instruction roundtrip')
        regions.append(dict(source_offset=hex(start),bytes=len(data),sha256=sha(data)))
    report=dict(id='exe45.hangul-keyboard.transfer-lifetime-observation.v1',passed=True,rom_integrated=False,
        source_sha256=profile['sha256'],rom_sha256=identity,route=str(route.relative_to(ROOT)).replace('\\','/'),
        observed_transfers=len(rows),distinct_frames=len(frames),font='0x08619EF8',cell_advance=8,
        stage='0x0201E800',target='0x0600B000',transfer_bytes=1280,render_cells=20,
        queue=dict(counter='0x02010724',entries='0x02012730',entry_bytes=20,nominal_limit=96,type=2,enqueue='0x08000850',consume_call='0x0800082E',return_pc='0x08000832',observed_delay_frames=1),
        original_font_pixels_match=True,stage_unchanged_at_consume=True,native_VRAM_pixels_match=True,tints=sorted(tints),streams=sorted(streams),
        bounded_native_code=regions,tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['capture_keyboard_transfer_lifetime.py','report_keyboard_transfer_lifetime.py','capture_keyboard_native.py']},
        artifacts={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in [route/'result.json',route/'transfer_lifetime_environment.json',route/'step_023_transfer_lifetime.json']},
        limits=['Observed native Japanese four-cell draft only; not Hangul or extended41-byte descriptor0 support.','Snapshots of source at enqueue/consume do not prove absence of intermediate write-and-restore or complete writer ownership.','Twenty-cell native render extent and next-frame consumption are route facts, not free RAM/other-route lifetime proof.','Type0/1 queues, queue saturation, full consumer/caller population and hardware timing outside Mesen remain unverified.','No keyboard hooks, save format changes, fresh-load or Korean screen claim.'])
    (ROOT/'analysis/hangul_keyboard_v1/transfer_lifetime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);require_hash(product,identity)
    print('PASS observed native editor font -> stage -> queue -> next-frame VRAM',len(rows),'transfers; not Hangul integration')


if __name__=='__main__':main()
