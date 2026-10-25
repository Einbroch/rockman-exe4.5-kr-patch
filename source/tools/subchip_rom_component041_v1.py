"""Pure immutable-source subchip component write plan for eventual full041 build.

No existing patched-ROM file is read, and no output file is written here.
Caller supplies reconstructed predecessor extent/entry and authored target
payloads. This102 component is NOT permission to emit a partial-cohort ROM.
The primary full500 orchestrator must compose this with other041 writers.
"""
import struct
from build_visibility_poc import sha
from verify_tpi_index import lz77_decompress
from archive_scripts import verify_untouched_scripts
from subchip_rom_selector041_v1 import wrap
from extended_dialogue import assemble_verified
from keyitem_rom_selector import INSTALL


def plan(source,source_sha256,start_offset,previous_entry,rows):
    if sha(source)!=source_sha256 or type(start_offset)is not int or start_offset&3 or not len(source)<=start_offset<0x2000000 or type(previous_entry)is not int or not 0x08000000<=previous_entry<0x08000000+start_offset or previous_entry&1:raise ValueError('041 component immutable source/predecessor placement')
    if len(rows)!=21 or len({r['archive'] for r in rows})!=21:raise ValueError('041 component exact subchip archive population')
    tail=bytearray();guards=[];ids=set()
    def alloc(payload):
        tail.extend(b'\xff'*(-len(tail)%4));address=0x08000000+start_offset+len(tail);tail.extend(payload);return address
    for r in sorted(rows,key=lambda r:r['archive']):
        arc=r['archive'];native=lz77_decompress(source,int(arc,16))[0];target=r['target'];count=r['scripts'];scripts=r['selected_scripts'];keys=set(r['selected_ids'])
        if native!=r['native'] or not isinstance(target,bytes) or not 0<count<=32 or int.from_bytes(native[:2],'little')!=count*2 or not target or len(target)>65535 or len(keys)!=len(r['selected_ids']) or ids&keys or len(set(scripts))!=len(scripts) or any(not 0<=n<count for n in scripts):raise ValueError('041 component native/count/target bounds')
        if {int(k.split(':')[1]) for k in keys}!=set(scripts) or any(k.split(':')[0]!=arc for k in keys):raise ValueError('041 component stable selected IDs')
        verify_untouched_scripts(native,target,count,set(scripts));ids|=keys;np=alloc(native);cp=alloc(target)
        guards.append(dict(archive=arc,clone=cp,native_at=np,native_bytes=len(native),native_sha256=sha(native),target_bytes=len(target),target_sha256=sha(target),scripts=count,selected_scripts=list(scripts),selected_ids=sorted(keys),mask=sum(1<<n for n in scripts)))
    if len(ids)!=102:raise ValueError('041 component exact102 selected units')
    desc=alloc(b''.join(struct.pack('<5I',g['clone'],g['native_at'],g['native_bytes'],g['scripts'],g['mask']) for g in guards));tail.extend(b'\xff'*(-len(tail)%4));address=0x08000000+start_offset+len(tail);code,wrapper=wrap(address,previous_entry,desc,len(guards));tail.extend(code)
    stub,stubproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=address|1));oldstub,oldproof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=previous_entry|1))
    if len(stub)!=12 or len(oldstub)!=12 or start_offset+len(tail)>0x2000000:raise ValueError('041 component trampoline/GBA mapped-ROM extent')
    audit=dict(component='041-subchip102-normal',source_sha256=source_sha256,selected_units=102,source_archives=21,append_offset=start_offset,append_bytes=len(tail),append_sha256=sha(tail),final_extent=start_offset+len(tail),descriptor_address=desc,code_address=address,previous_entry=previous_entry,placements=guards,wrapper=wrapper,stub=stubproof,predecessor_stub_proof=oldproof,expected_writes=[dict(writer='041-subchip-composed-stub',offset=INSTALL,bytes=12,immutable_source_sha256=sha(source[INSTALL:INSTALL+12]),final_sha256=sha(stub),composition='Replace the declared predecessor trampoline as one final writer, preserving its entry as tail-call target.'),dict(writer='041-subchip-appended-data-and-code',offset=start_offset,bytes=len(tail),final_sha256=sha(tail),composition='Append after the complete independently reconstructed predecessor tail; no writes to its assets.')],native_LZ_tables_and_payloads_modified=False,distribution_output=False,full500_orchestrator_required=True,rom_written=False,product_integrated=False,release_eligible=False)
    return dict(tail=bytes(tail),stub=stub,expected_predecessor_stub=oldstub,audit=audit)
