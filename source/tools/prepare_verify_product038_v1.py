"""Version the full final-image auditor for explicit full-carry supersession."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
src=ROOT/'tools/verify_native_product037_v1.py';dst=ROOT/'tools/verify_native_product038_v1.py';m=read('poc/output/pending500_037_v2.json');require_hash(src,m['build_tools_sha256'][src.name])
if dst.exists():raise ValueError('Preserve verifier version')
text=src.read_text(encoding='utf8')
old_owners="""        owners=[x for x in m['translation_assets'] if x.get('archive')==arc and not x.get('scope','').startswith('read-only inherited')]
        if len(owners)!=1 or {k:owners[0][k] for k in ['path','sha256']}!=r['asset']:raise ValueError('037 unique new owner')
"""
new_owners="""        active=m['active_fullcarry_owners038'].get(arc)
        if active!=dict(asset=r['asset'],supersedes=r['parent_asset_lineage']):raise ValueError('038 explicit current owner/supersession')
        owners=[x for x in m['translation_assets'] if x.get('archive')==arc and {k:x[k] for k in ['path','sha256']}==r['asset']]
        if len(owners)!=1:raise ValueError('038 one new active owner')
"""
old_untouched="""        if verify_untouched_scripts(payload_of(source,r['source_row']),payload,r['scope']['script_count'],set(r['new_scripts']))!=r['unselected_scripts']:raise ValueError('037 untouched script drift')"""
new_untouched="""        parent=r['parent_record'];before_payload=read_payload(base,parent) if parent else payload_of(source,r['source_row'])
        if verify_untouched_scripts(before_payload,payload,r['scope']['script_count'],set(r['new_scripts']))!=r['parent_unselected_scripts']:raise ValueError('038 full inherited/unselected script drift')"""
changes=[
    ('prepare_source500_037_v2','prepare_source500_038_v5'),('field_native_rom_product_037_v2','field_native_rom_product_038_v1'),
    ('len(after)!=len(before)+70','len(after)!=len(before)+66'),('70*28','66*28'),
    (old_owners,new_owners),(old_untouched,new_untouched),
    ("['npc037']","['npc038']"),("['cumulative037']","['cumulative038']"),
    ('analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json','analysis/pending_insertion_500_038_selector_cpu_v1/cpu.json'),
    ("cpu['fixture_only']['sha256']","cpu['fixture_only']['fixture_sha256']"),
    ('tools/verify_native_product037_v1.py','tools/verify_native_product038_v1.py'),
    ('tools/specs/primary037_v2_version.json','tools/specs/primary038_v1_version.json'),
    ('new_consumers=70','new_consumers=66'),('CPU18415_fixture_whole_image_byte_identical','CPU14388_fixture_whole_image_byte_identical'),
    ('old036_prefix_except_stub_preserved','old037_prefix_except_stub_preserved'),
    ('036 natural evidence closes preceding036 changed-path gate only;037 A0/A1/A3 display/acquisition/timing/reentry still needs exact-ROM runtime.','037 normal and qualified evidence covers the predecessor only;038 three consumer paths/full carry need exact-ROM runtime.'),
]
for old,new in changes:
    count=text.count(old)
    expected=2 if old in ('field_native_rom_product_037_v2','analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json') else 1
    if count!=expected:raise ValueError('038 audit exact anchor '+old[:60]+':'+str(count))
    text=text.replace(old,new)
text=text.replace('PASS037','PASS038').replace('Actual cumulative037','Actual cumulative038').replace('all18415-vector','all14388-vector')
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/verify_product038_v1_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),changes=changes,output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Whole-source writes/header/pointers/append/old-consumer/repro audit retained; explicit new active owner supersession and inherited bytes checked against current parent.'))
print('Generated038 final full-write/old578/carry/repro auditor')
