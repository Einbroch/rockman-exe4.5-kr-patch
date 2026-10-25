"""Correct only unchanged035 validator import in generated037 product v2."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_native_product037_v1 import create


def main():
    spec=read('tools/specs/primary037_v1_version.json'); records=[]
    for r in spec['changes']: require_hash(ROOT/r['output'],r['output_sha256'])
    base='tools/field_native_rom_product_037_v1.py'
    records.append(create('tools/field_native_rom_product_037_v2.py',base,(ROOT/base).read_text(encoding='utf8'),[
        ('from survey_new_storage_036 import VALIDATORS','from survey_new_storage_035 import VALIDATORS',1),
        ("result['primary_entry']='tools/build_development_patch_037_v1.py'","result['primary_entry']='tools/build_development_patch_037_v2.py'",1),
    ]))
    base='tools/build_development_patch_037_v1.py'
    text=(ROOT/base).read_text(encoding='utf8')
    records.append(create('tools/build_development_patch_037_v2.py',base,text,[('field_native_rom_product_037_v1','field_native_rom_product_037_v2',2)]))
    frozen_write(ROOT/'tools/specs/primary037_v2_version.json',dict(generator_sha256=sha((ROOT/'tools/prepare_native_product037_v2.py').read_bytes()),changes=records,predecessor=sha((ROOT/'tools/specs/primary037_v1_version.json').read_bytes())))
    print('PASS037 v2 validator import/primary identity corrected; no ROM')


if __name__=='__main__': main()
