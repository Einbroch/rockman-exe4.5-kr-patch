"""Versioned independent artifact audit, retaining036 tool byte identity."""
from build_visibility_poc import ROOT,require_hash,sha
from cumulative_batch500 import read,frozen_write
from prepare_native_product037_v1 import create


def main():
    base='tools/verify_npc_product_036_v1.py';m=read('poc/output/pending500_036_v1.json');require_hash(ROOT/base,m['build_tools_sha256']['verify_npc_product_036_v1.py']);text=(ROOT/base).read_text(encoding='utf8')
    deps="deps=[MANIFEST,'tools/verify_native_product037_v1.py','tools/field_native_rom_product_037_v2.py','analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json','analysis/pending500_036_v1/natural_cached_display_v1.json','analysis/pending500_036_v1/native_boundaries_v1.json','tools/specs/primary037_v2_version.json']"
    original_deps=next(l.strip() for l in text.splitlines() if l.strip().startswith('deps='))
    edits=[
        ('036','037',text.count('036')),
        ('035','036',text.count('035')),
        ('prepare_source500_037_v1','prepare_source500_037_v2',1),
        ('field_npc_rom_product_037_v1','field_native_rom_product_037_v2',2),
        ('verify_npc_product_037_v1','verify_native_product037_v1',1),
        ('len(before)+20','len(before)+70',1),
        ("payload,255,set(r['new_scripts'])","payload,r['scope']['script_count'],set(r['new_scripts'])",1),
        ("n['descriptor_offset']+20*16","n['descriptor_offset']+70*28",1),
        ('pending_insertion_500_037_selector_cpu_v1','pending_insertion_500_037_selector_cpu_v2',3),
        ('all8423-vector','all18415-vector',1),
        ('CPU8423_fixture','CPU18415_fixture',1),
        ('new_consumers=20','new_consumers=70',1),
    ]
    # The dependencies are replaced after the preceding version substitutions.
    d=original_deps
    for a,b,n in edits:d=d.replace(a,b)
    edits.append((d,deps,1))
    r=create('tools/verify_native_product037_v1.py',base,text,edits)
    frozen_write(ROOT/'tools/specs/verify_native037_v1_version.json',dict(change=r,generator_sha256=sha((ROOT/'tools/prepare_verify_native037_v1.py').read_bytes())))
    print('PASS037 independent audit generated')


if __name__=='__main__':main()
