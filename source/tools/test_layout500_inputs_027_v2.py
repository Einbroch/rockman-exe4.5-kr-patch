"""Actual027 production gate with controlled in-memory invalid inputs.

No on-disk manifest/hash bypass. Mutations occur only after the real immutable
files pass their identities; this tests further structural checks, not every
malicious metadata possibility.
"""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
import layout500_inputs_027 as gate


def main():
    cfg=read('project.json');p=ROOT/cfg['source_profile']['filename'];require_hash(p,cfg['source_profile']['sha256']);source=p.read_bytes()
    inputs,summary=gate.load_inputs(source);cases=[];original_read=gate.read
    manifest=read(gate.MANIFEST);selection=read(gate.SELECTION);asset_path=manifest['archives'][0]['merged_asset']['path']
    def reject(name,path,mutate):
        value=deepcopy(original_read(path));mutate(value);path=path.replace('\\','/')
        def changed(p):
            normalized=str(p).replace('\\','/')
            if normalized==path:return deepcopy(value)
            try:
                if hasattr(p,'relative_to') and str(p.relative_to(ROOT)).replace('\\','/')==path:return deepcopy(value)
            except ValueError:pass
            return original_read(p)
        gate.read=changed
        try:gate.load_inputs(source)
        except (ValueError,KeyError,IndexError,TypeError) as ex:cases.append(dict(fixture=name,rejected=True,error=str(ex)))
        else:raise ValueError('027 invalid production input accepted '+name)
        finally:gate.read=original_read
        print('PASS027 refused',name,flush=True)
    for name,change in [
        ('missing-archive',lambda m:m['archives'].pop()),
        ('wrong-storage',lambda m:m['archives'][0].update(storage='raw-carry')),
        ('invented-parent',lambda m:m['archives'][0].update(old_record={})),
        ('invented-carry',lambda m:m['archives'][0].update(carry_units=1)),
        ('wrong-catalog-size',lambda m:m['archives'][0]['source_row'].update(size=1)),
        ('compressed-storage',lambda m:m['archives'][0]['source_row'].update(compressed=True)),
        ('wrong-unit-count',lambda m:m['archives'][0]['new_ids'].append(m['archives'][0]['new_ids'][0])),
        ('wrong-script-scope',lambda m:m['archives'][0].update(new_scripts=[])),
    ]:
        # Duplicate list entries are not an invalid set by themselves; bind
        # the count mismatch as well so this fixture violates actual scope.
        if name=='wrong-unit-count':
            change=lambda m:m['archives'][0].update(new_units=m['archives'][0]['new_units']+1)
        reject(name,gate.MANIFEST,change)
    reject('wrong-page-geometry',gate.SELECTION,lambda s:s['groups'][0].update(geometry=[]))
    reject('unknown-consumer',gate.SELECTION,lambda s:s['groups'][0].update(profile='unbounded'))
    reject('changed-selected-union',gate.SELECTION,lambda s:s['selected_ids'].pop())
    reject('changed-wording',asset_path,lambda a:a['units'][0].update(translation=a['units'][0]['translation']+'가'))
    reject('changed-review-state',asset_path,lambda a:a['units'][0].update(state='reviewed'))
    reject('missing-unit',asset_path,lambda a:a['units'].pop())
    deps=['tools/test_layout500_inputs_027_v2.py','tools/layout500_inputs_027.py',gate.MANIFEST]
    frozen_write(ROOT/'analysis/pending_insertion_500_027_gate_tests_v2/result.json',dict(schema=1,passed=True,valid_full500_inputs=summary,rejected_fixture_count=len(cases),fixtures=cases,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,limits=__doc__))
    print('PASS027 real full500 gate and',len(cases),'refusal fixtures')


if __name__=='__main__':main()
