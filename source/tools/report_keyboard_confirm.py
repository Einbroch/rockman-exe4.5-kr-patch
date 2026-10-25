"""Bound native normal confirmation and explicit incomplete hook contract."""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import read,verify_route
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
import json

def main():
    base=ROOT/'analysis/hangul_keyboard_v1';route=ROOT/'poc/runtime/hangul-keyboard-v1-confirm'
    identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4'
    result=verify_route(route,identity,set());env=read(route/'confirm_environment.json')
    if not env['observer_only'] or not env['no_RAM_or_save_injection']:raise ValueError('confirm intervention')
    for n,k in [('capture_keyboard_confirm.py','tool_sha256'),('capture_keyboard_native.py','native_observer_sha256')]:require_hash(ROOT/'tools'/n,env[k])
    baseline=verify_route(ROOT/'poc/runtime/hangul-keyboard-v1-buffer-writers',identity,set())
    for k in ('rom_sha256','emulator_sha256','state_sha256','actions','total_frames','capture_steps'):
        if result[k]!=baseline[k]:raise ValueError('confirm route baseline')
    trace=route/'step_023_confirm.json';events=read(trace)['events'];counts=Counter(e['pc'] for e in events)
    if counts[0x08034F84]!=212 or counts[0x08034FA8]!=1 or counts[0x08034FA0]!=1 or counts[0x08035000]!=1 or counts[0x08034FB0]!=2:raise ValueError('normal confirmation population')
    entries=[e for e in events if e['pc']==0x08034F84]
    if any(e['r5']!=0x0200FC40 or e['sp']!=0x030076CC for e in entries):raise ValueError('normal handler ABI')
    no=next(e for e in events if e['pc']==0x08034FA8);yes=next(e for e in events if e['pc']==0x08034FA0)
    conclusions=[]
    for first,choice,state in [(no,1,12),(yes,0,20)]:
        frame_events=[e for e in events if e['frame']==first['frame']]
        decision=next(e for e in frame_events if e['pc']==0x08034F92)
        before=next(e for e in frame_events if e['pc']==0x08034FB0)
        after=next(e for e in frame_events if e['pc']==0x08034FB2)
        if decision['r0']!=choice or before['r0']!=state or bytes.fromhex(after['ui_hex'])[:2]!=struct.pack('<H',state):raise ValueError('native choice/state boundary')
        if state==12 and any(e['record_hex']!=first['record_hex'] for e in frame_events):raise ValueError('No changed record')
        if state==20:
            commit=next(e for e in frame_events if e['pc']==0x08035000)
            finished=next(e for e in frame_events if e['pc']==0x08034FA4)
            raw=bytes.fromhex(commit['editor_hex'])
            if commit['lr']!=0x08034FA5 or commit['sp']!=0x030076C8 or struct.unpack_from('<I',raw,28)[0]!=0x020010A6 or raw[64:66]!=b'\x9B\x98':raise ValueError('native commit source/destination')
            if finished['r0']!=1 or after['record_hex']!='019be57ee50000000000':raise ValueError('native commit completion')
        conclusions.append(dict(frame=first['frame'],choice=choice,state=state,record_before=first['record_hex'],record_after=after['record_hex']))
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(product,identity);current=product.read_bytes()
    raw=rom[0x34F84:0x34FB4]
    if current[0x34F84:0x34FB4]!=raw:raise ValueError('confirm source identity')
    table=struct.unpack_from('<I',rom,0x34F78)[0]
    if table!=0x08034F7C or current[0x34F78:0x34F84]!=rom[0x34F78:0x34F84] or struct.unpack_from('<2I',rom,0x34F7C)!=(0x08034F85,0x08034FB5):raise ValueError('native confirm dispatch table')
    if any(e['lr']!=0x08034F74 for e in entries):raise ValueError('native confirm indirect dispatch return')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ins=list(cs.disasm(raw,0x08034F84))
    if sum(i.size for i in ins)!=len(raw):raise ValueError('confirm body coverage')
    for i in ins:
        if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('confirm ISA')
    candidates=[]
    for at in range(0,len(rom)-3,2):
        a,b=struct.unpack_from('<HH',rom,at)
        if a&0xF800!=0xF000 or b&0xF800!=0xF800:continue
        delta=(a&2047)<<12|(b&2047)<<1
        if delta&0x400000:delta-=0x800000
        if 0x08000000+at+4+delta==0x08035000:candidates.append(hex(0x08000000+at))
    report=dict(id='exe45.hangul-keyboard.native-confirm-observation.v1',passed=True,rom_integrated=False,
                source_sha256=profile['sha256'],rom_sha256=identity,handler_entries=len(entries),
                handler_r5='0x0200FC40',handler_sp='0x030076CC',commit_sp='0x030076C8',
                handler_sha256=sha(raw),choices=conclusions,direct_commit_BL_encoding_candidates=candidates,
                original_ignores_commit_return=True,
                bounded_dispatch_table=dict(literal_offset=0x34F78,table_address=hex(table),entries=['0x08034F85','0x08034FB5'],observed_entry_index=0,handler_entry_LR='0x08034F74',pointer0_hex=rom[0x34F7C:0x34F80].hex(),installed=False),
                tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ('capture_keyboard_confirm.py','report_keyboard_confirm.py','capture_keyboard_native.py')},
                artifacts={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in (route/'result.json',route/'confirm_environment.json',trace)},
                limits=['Normal Japanese cap4/oneNo/oneYes route, no Hangul UI or save/fresh-load.',
                        'Direct BL aligned encoding candidates may include data; not complete indirect callers or control-flow graph.',
                        'Original Yes path calls commit then unconditionally writes state14. New mixed format needs coordinated confirmation rejection and downstream reader replacement.'])
    (base/'native_confirm.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS native confirm212 entries, No/Yes state0C/14; direct commit candidates',candidates,flush=True)

if __name__=='__main__':main()
