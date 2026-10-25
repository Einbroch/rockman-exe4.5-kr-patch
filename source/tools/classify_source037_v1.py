"""Independent current-source lookup/root classes for the prepared500 IDs.

References establish static applicability, never normal runtime reachability.
The pointerless256-script reward archive remains unresolved, not guessed.
"""
import struct
from collections import Counter,defaultdict
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress

def main():
    out='analysis/pending_insertion_500_037_source_only_v1';s=read(out+'/selection.json');v=read(out+'/verification_v1.json');require_hash(ROOT/v['selection']['path'],v['selection']['sha256']);cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();rp=ROOT/s['baseline_rom'];require_hash(rp,s['baseline_sha256']);rom=rp.read_bytes();decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    if not v['passed'] or v['units']!=500 or v['rom_written']:raise ValueError('037 source-only verification prerequisite')
    def word(a):return struct.unpack_from('<I',source,a)[0]
    calls={}
    for pc in (0x4F724,0x4F730,0x4F744,0x47976):
        code=source[pc:pc+4];ins=list(decoder.disasm(code,0x08000000+pc))
        if rom[pc:pc+4]!=code or len(ins)!=1 or ins[0].mnemonic!='bl' or ins[0].op_str!='#0x80ec158':raise ValueError('037 original compression caller applicability')
        calls[hex(pc)]=dict(source_bl=code.hex(),target=0x080EC158)
    roots={'native-NPC':word(0x4F750),'field-board':word(0x4F758),'navi-hint':word(0x4F760),'tournament':word(0x47964)}
    if roots!={'native-NPC':0x02039800,'field-board':0x0203C800,'navi-hint':0x0203D800,'tournament':0x02024000} or word(0x479DC)!=roots['tournament']:raise ValueError('Source literal root contract')
    refs=defaultdict(list)
    for scene in (0xA0,0xA1,0xA2,0xA3):
        native=word(0x53700+(scene-0x80)*4)-0x08000000;board=word(0x537CC+(scene-0x80)*4)-0x08000000
        for sub in range(4):
            days=word(native+sub*4)-0x08000000
            for slot in range(7):
                at=days+slot*4;refs[word(at)-0x08000000].append(dict(kind='native-NPC',scene=scene,sub=sub,weekday=slot,pointer=at,root=roots['native-NPC'],load_call=0x0804F724))
            at=board+sub*4;refs[word(at)-0x08000000].append(dict(kind='field-board',scene=scene,sub=sub,pointer=at,root=roots['field-board'],load_call=0x0804F730))
    # Enumerate only these explicit source tables; a null NPC table for A4
    # prevents us from pretending its hint pointers prove normal field entry.
    for scene in (0xA0,0xA1,0xA2,0xA3,0xA4,0xB0,0xB1):
        table=word(0x53FA0+(scene-0x80)*4)-0x08000000
        if not 0<=table<len(source)-23*4:raise ValueError('037 explicit hint-table range')
        for navi in range(23):
            at=table+navi*4;refs[word(at)-0x08000000].append(dict(kind='navi-hint',scene=scene,navi=navi,pointer=at,root=roots['navi-hint'],load_call=0x0804F744,natural_scene_entry_proved=False))
    for navi in range(23):
        at=0x47980+4*navi;refs[word(at)-0x08000000].append(dict(kind='tournament',navi=navi,pointer=at,root=roots['tournament'],load_call=0x08047976,reader_entry=0x08047958,reader_return_lr=0x08047963))
    units=Counter();records=[];unresolved=[];compiled={r['archive']:r for r in v['archives']};grouped=defaultdict(list)
    for g in s['groups']:grouped[g['archive']].append(g)
    for arc,gs in sorted(grouped.items()):
        r=compiled[arc];off=int(arc,16);native,used=lz77_decompress(source,off);count=(native[0]|native[1]<<8)//2;found=refs.get(off,[]);kinds={x['kind'] for x in found};n=sum(g['units'] for g in gs)
        if len(kinds)>1:raise ValueError('037 ambiguous root classes: '+arc)
        kind=next(iter(kinds)) if kinds else 'unresolved-pointerless'
        declared={p for g in gs for p in g['source_row']['pointers']};matched={x['pointer'] for x in found}
        if found and declared!=matched:raise ValueError('037 complete explicit source pointer membership '+arc)
        if sha(native)!=r['source_payload_sha256'] or rom[off:off+used]!=source[off:off+used] or any(rom[p:p+4]!=source[p:p+4] for p in declared):raise ValueError('037 immutable/current compressed source')
        if kind=='native-NPC' and count!=255 or kind=='tournament' and count!=254:raise ValueError('037 independent script-count domain')
        if kind=='unresolved-pointerless':
            if arc!='7794EC' or declared or count!=256:raise ValueError('037 unexpected unresolved source population')
            unresolved.append(dict(archive=arc,ids=[k for g in gs for k in g['ids']],reason='No TPI references, no direct little-endian compressed ROM-pointer word in source; that search does not prove unreachable. Native acquisition/reader/root still unresolved.'))
        units[kind]+=n;records.append(dict(archive=arc,units=n,script_count=count,native_bytes=len(native),compiled_bytes=r['compiled_bytes'],class_name=kind,static_references=found,runtime_admitted=False))
    if sum(units.values())!=500 or dict(units)!={'tournament':21,'unresolved-pointerless':1,'navi-hint':69,'field-board':46,'native-NPC':363}:raise ValueError(('037 finite source class accounting',dict(units)))
    frozen_write(ROOT/out/'loader_classification_v1.json',dict(passed=True,scope='Static current-source lookup/root classes only; no product admission or runtime claim',source_sha256=sha(source),baseline_sha256=s['baseline_sha256'],selection_sha256=sha((ROOT/out/'selection.json').read_bytes()),compile_sha256=sha((ROOT/out/'verification_v1.json').read_bytes()),units=500,classes=dict(units),archives=records,unresolved=unresolved,source_roots=roots,native_load_calls=calls,native_A4_NPC_table_is_null=word(0x53700+(0xA4-0x80)*4)==0,product_admitted=False,rom_written=False,new_units_applied=0,release_eligible=False,limits=['A4 hint table references are real but its NPC lookup table is null; no normal A4 field acquisition is inferred.','363 NPC units need A2 plus remaining scene/ABI applicability;69 hints/46 boards use distinct root/caller conditions,21 tournament units use254 scripts/root02024000.','The one256-script reward literal7794EC must remain blocked until its actual native loader/reference/consumer is established.'],dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/classify_source037_v1.py','tools/prepare_source500_037_v1.py','tools/compile_source500_037_v1.py']}))
    print('PASS037 static classes',dict(units),'one unresolved reward source blocks whole037 ROM admission')

if __name__=='__main__':main()
