"""Mechanical scope version for existing quarantined PET display diagnostic."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write


def main():
    base=ROOT/'tools/capture_npc_displays_035_v2.py';out=ROOT/'tools/capture_npc_displays_036_v1.py';text=base.read_text(encoding='utf8')
    edits=[
    ('from field_npc_rom_product_035 import verify_final','from field_npc_rom_product_036_v1 import verify_final'),
    ("CASES={'plaza':('7A32A8',255,21,None),'portraits':('79D650',255,61,None),'weekend':('7A4DD4',255,30,None)}", "CASES={'a0':('79CF04',255,30,None),'a1':('7AAF94',255,0,None),'a3':('7B469C',255,0,None)}"),
    ("m['keyitem_rom']['npc035']","m['keyitem_rom']['npc036']"),
    ('actual035 new NPC clone','actual036 new NPC clone'),
    ]
    for before,after in edits:
        count=text.count(before)
        if count!=(2 if before=="m['keyitem_rom']['npc035']" else 1):raise ValueError('036 display scope expansion anchor')
        text=text.replace(before,after)
    text=text.replace('NOT native A0 loader/NPC selector/caller','NOT native A0/A1/A3 loader/NPC selector/caller')
    if out.exists() and out.read_text(encoding='utf8')!=text:raise ValueError('Preserve036 display tool')
    if not out.exists():out.write_text(text,encoding='utf8',newline='\n')
    frozen_write(ROOT/'tools/specs/capture036_v1_version.json',dict(base=str(base.relative_to(ROOT)),base_sha256=sha(base.read_bytes()),output=str(out.relative_to(ROOT)),output_sha256=sha(out.read_bytes()),edits=[dict(before=a,after=b) for a,b in edits],scope='Own-ROM PET root/script aliases to036 three scene-class examples, not natural acquisition'))
    print('036 quarantined display tool generated; no emulator or ROM run')


if __name__=='__main__':main()
