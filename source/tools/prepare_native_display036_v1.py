"""Mechanical current-artifact expansion of pinned035 native page verifier."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import frozen_write

def main():
    base=ROOT/'tools/verify_native_npc_display_035_v1.py';require_hash(base,'85925280c76d4c16e60bea38173bae887d35b05999ea7286de129fec55dd44c0');text=base.read_text(encoding='utf8');dest=ROOT/'tools/verify_native_npc_display_036_v1.py'
    if dest.exists():raise ValueError('preserve verifier version')
    replacements=[('field_npc_rom_product_035_v2','field_npc_rom_product_036_v1'),('pending500_035_v2.gba','pending500_036_v1.gba'),("['npc035']","['npc036']"),('pending_insertion_500_035_npc_inputs_v1','pending_insertion_500_036_npc_inputs_v1'),('verify_native_npc_display_035_v1.py','verify_native_npc_display_036_v1.py'),('capture_field_loader_035_v6.py','capture_field_loader_036_v1.py')]
    for old,new in replacements:
        if text.count(old)!=1:raise ValueError('036 native verifier exact version anchor '+old)
        text=text.replace(old,new)
    dest.write_text(text,encoding='utf8');frozen_write(ROOT/'tools/specs/native_display036_v1_version.json',dict(base=str(base.relative_to(ROOT)),base_sha256=sha(base.read_bytes()),replacements=replacements,output=str(dest.relative_to(ROOT)),output_sha256=sha(dest.read_bytes()),scope='Same original caller/timebranch/loaded-source/font/pixel contracts on actual036 A0, not A1/A3 route claim'))
    print('Generated036 native first-page verifier; unchanged proof contracts')

if __name__=='__main__':main()
