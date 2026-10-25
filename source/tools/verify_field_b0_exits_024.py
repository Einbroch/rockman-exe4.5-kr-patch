"""Read existing own-ROM snapshots: native end activation and removed text OBJ."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    rp=ROOT/'poc/output/pending500_024_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    folder=ROOT/'poc/runtime/pending500-024-v1-natural-b0-hint';receipt=read(folder/'result.json');display=read('analysis/pending500_024_v1/natural_b0_runtime.json')
    if not display['passed'] or receipt['rom_sha256']!=sha(rom) or display['rom_sha256']!=sha(rom):raise ValueError('Own023 exit applicability')
    for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
    pages={p['step']:p for p in display['pages']};proof=[]
    for before,after in ((7,9),(11,13)):
        ram=(folder/f'step_{after:03}_gbaExtWorkRam.bin').read_bytes();oam=(folder/f'step_{after:03}_gbaSpriteRam.bin').read_bytes()
        ptr,root=struct.unpack_from('<2I',ram,0xFA4C)
        # TextPet mmbn45 end=E5; F1 is clearMsg, not script termination.
        if ram[0xFA20]!=0 or root!=pages[before]['root'] or ptr!=pages[before]['wait_pointer']+2 or rom[ptr-0x08000000]!=0xE5:
            raise ValueError('Native end/inactive context/retained root')
        active=[]
        for i in range(128):
            a,b,k=struct.unpack_from('<3H',oam,i*8)
            if not a&0x2300 and k>>12==14:active.append(i)
        if active:raise ValueError('Dialog font/cursor OBJ persists after close')
        proof.append(dict(step=after,native_context_inactive=True,end_pointer=ptr,all128_OAM_entries_checked=True,active_dialog_palette14_objects=0))
    frozen_write(ROOT/'analysis/pending500_024_v1/exit_runtime.json',dict(schema=1,passed=True,rom_sha256=sha(rom),display_report_sha256=sha((ROOT/'analysis/pending500_024_v1/natural_b0_runtime.json').read_bytes()),exits=proof,release_eligible=False,limits='Same two normal default-hint exits only; inactive context and all dialog OBJ removed. Does not assert every UI palette or all state transitions.'))
    print('PASS two natural hint exits: native context inactive, end opcode reached, dialog/cursor OBJ absent')


if __name__=='__main__':main()
