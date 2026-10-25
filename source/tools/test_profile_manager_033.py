"""Controlled exact profile-manager model fixtures, no native input claim."""
import re
from build_visibility_poc import ROOT, sha
from cumulative_batch500 import frozen_write
from tpl_literals import literals
from survey_aggregate_pet_033 import replace_exact
from profile_manager_capacity_033 import validate


def main():
    path = 'analysis/full_scope_v1/source_tpl/7CC6A0.tpl'; full = (ROOT/path).read_text(encoding='utf-8-sig'); cases = []; fixtures = {}
    for script in (0, 7, 15):
        one = '@archive 7CC6A0\n'+re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)', full, re.M)[0]
        values = {u.key: '가'+'\n'*u.text.count('\n')+' '*(len(u.text)-len(u.text.rstrip(' '))) for u in literals(one)}
        new = replace_exact(one, values); ids = set(values); validate(one, new, [script], ids); fixtures[script] = (one, new, ids)
        cases.append(dict(label='short-six-literal-'+str(script), accepted=True))
    def reject(label, change):
        old, new, ids = fixtures[0]; old, new, ids = change(old, new, set(ids))
        try: validate(old, new, [0], ids)
        except ValueError as ex: cases.append(dict(label=label, rejected=True, error=str(ex))); return
        raise ValueError('033 invalid manager fixture accepted '+label)
    def both(before, after): return lambda a, b, i: (a.replace(before, after), b.replace(before, after), i)
    reject('unregistered-root', both('@archive 7CC6A0', '@archive 7B67C8'))
    reject('different-portrait', both('mugshot = MrProgGreen', 'mugshot = Rockman'))
    reject('different-name-provider', both('printPlayerName', 'printPlayerNickname'))
    reject('provider-uppercase', both('capitalizeAll = false', 'capitalizeAll = true'))
    reject('changed-width', both('width = 7', 'width = 8'))
    reject('different-native-space', both('count = 1', 'count = 2'))
    reject('different-select-clearing', both('clear = false', 'clear = true'))
    reject('different-B-contract', both('BSeparate = false', 'BSeparate = true'))
    reject('wrong-default', both('default = 0', 'default = 1'))
    reject('wrong-no-branch', both('jump = 95', 'jump = 94'))
    reject('wrong-editor-jump', both('target = 20', 'target = 21'))
    reject('target-only-control-change', lambda a, b, i: (a, b.replace('width = 7', 'width = 8'), i))
    reject('missing-selected-ID', lambda a, b, i: (a, b, set(sorted(i)[1:])))
    reject('literal-overflow', lambda a, b, i: (a, replace_exact(b, {sorted(i)[-1]: '가'*20}), i))
    frozen_write(ROOT/'analysis/pending_insertion_500_033_manager_models_v1/result.json', dict(schema=1, passed=True,
                  positive_cases=3, negative_cases=len(cases)-3, cases=cases,
                  dependencies={p: sha((ROOT/p).read_bytes()) for p in (path, 'tools/test_profile_manager_033.py', 'tools/profile_manager_capacity_033.py')},
                  rom_written=False, release_eligible=False,
                  limits='Synthetic short targets on finite source templates. Not native name ownership/cache, nonclearing selection/jump20/95 input execution, editor/save/renderer transition, product or semantic approval.'))
    print('PASS033 manager model3 positive', len(cases)-3, 'refusals')


if __name__ == '__main__': main()
