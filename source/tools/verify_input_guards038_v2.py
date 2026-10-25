"""Controlled in-memory038 input failures, no source/ROM/file mutation.

Reuse one valid admission snapshot for these INPUT-boundary tests only. This
does not replace admission enforcement in the actual running primary builds.
"""
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read,frozen_write
import field_native_rom_product_038_v2 as product
from prepare_source500_038_v5 import baseline

def main():
    cfg,source,base,meta=baseline();admission=product.require_admission();valid=product.load_inputs(source);manifest=read(product.MANIFEST);asset_path=manifest['archives'][0]['asset']['path'];asset=read(asset_path);rows=[];oldread=product.read;oldadmit=product.require_admission
    product.require_admission=lambda:deepcopy(admission)
    def test(name,path,original,mutate):
        bad=deepcopy(original);mutate(bad)
        product.read=lambda p:deepcopy(bad) if str(p).replace('\\','/')==path.replace('\\','/') else oldread(p)
        try:
            product.load_inputs(source)
        except (ValueError,KeyError,IndexError,SystemExit) as e:rows.append(dict(name=name,rejected=True,error=str(e)))
        else:raise ValueError('038 invalid input accepted '+name)
        finally:product.read=oldread
    try:
        for key,value in [('new_units',499),('inherited_units',495),('baseline_sha256','0'*64),('source_sha256','0'*64),('rom_written',True)]:test('manifest-'+key,product.MANIFEST,manifest,lambda x,k=key,v=value:x.update({k:v}))
        test('duplicate-archive',product.MANIFEST,manifest,lambda x:x['archives'].append(deepcopy(x['archives'][0])))
        test('missing-archive',product.MANIFEST,manifest,lambda x:x['archives'].pop())
        test('wrong-native-root',product.MANIFEST,manifest,lambda x:x['archives'][0]['scope'].update(native_root=0x02039800))
        test('wrong-real-caller-LR',product.MANIFEST,manifest,lambda x:x['archives'][0]['scope'].update(guarded_reader_return_lr=0x0804F773))
        test('wrong-script-count',product.MANIFEST,manifest,lambda x:x['archives'][0]['scope'].update(script_count=254))
        test('compiled-hash',product.MANIFEST,manifest,lambda x:x['archives'][0]['compiled'].update(sha256='0'*64))
        test('source-reference',product.MANIFEST,manifest,lambda x:x['archives'][0]['source_row']['pointers'].__setitem__(0,0x100))
        test('duplicate-asset-unit',asset_path,asset,lambda x:x['units'].append(deepcopy(x['units'][0])))
        test('missing-asset-unit',asset_path,asset,lambda x:x['units'].pop())
        test('protected-source-literal',asset_path,asset,lambda x:x['units'][0].update(source='changed'))
        test('unknown-unit-state',asset_path,asset,lambda x:x['units'][0].update(state='untranslated'))
        test('unrecorded-wording',asset_path,asset,lambda x:x['units'][0].update(translation='원문과 다른 미등록 번역'))
        test('missing-nondistribution-policy',asset_path,asset,lambda x:x.update(policy='release'))
        test('silent-release-promotion',asset_path,asset,lambda x:x['review'].update(release_eligible=True))
        product.read=oldread
        bad=bytearray(source);bad[0xC0]^=1
        try:product.load_inputs(bytes(bad))
        except ValueError as e:rows.append(dict(name='unsupported-source-image',rejected=True,error=str(e)))
        else:raise ValueError('038 altered source accepted')
    finally:product.read=oldread;product.require_admission=oldadmit
    frozen_write(ROOT/'analysis/pending_insertion_500_038_native_inputs_v1/guards_v1.json',dict(passed=True,scope=__doc__,source_sha256=sha(source),baseline_sha256=sha(base),valid_input_archives=len(valid),valid_input_new_IDs=sum(len(r['new_ids']) for r,_ in valid),rejected_fixture_count=len(rows),fixtures=rows,dependencies={p:sha((ROOT/p).read_bytes()) for p in ['tools/verify_input_guards038_v2.py','tools/field_native_rom_product_038_v2.py',product.MANIFEST]},rom_written=False,runtime_tested=False,release_eligible=False))
    print('PASS038 source/input acceptance and',len(rows),'controlled refusals; no files mutated')

if __name__=='__main__':main()
