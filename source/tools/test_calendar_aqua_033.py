"""Controlled Aqua-only source-preserved FD09 projection contracts."""
import re
from build_visibility_poc import ROOT, sha
from cumulative_batch500 import frozen_write
from tpl_literals import literals
from survey_aggregate_pet_033 import replace_exact
from calendar_aqua_capacity_033 import validate


def main():
    path = 'analysis/tpl_baseline/697B70.tpl'; full = (ROOT/path).read_text(encoding='utf-8-sig'); fixtures = {}; cases = []
    for script in (50, 51, 52):
        match = re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)', full, re.M)
        old = '@archive 697B70\n'+match[0]; units = [u for u in literals(old) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]', u.text)]
        values = {u.key: '가'+'\n'*u.text.count('\n')+' '*(len(u.text)-len(u.text.rstrip(' '))) for u in units}
        new = replace_exact(old, values); ids = set(values); validate(old, new, [script], ids); fixtures[script] = (old, new, ids)
        cases.append(dict(label='synthetic-short-Aqua-'+str(script), accepted=True))
    old, new, ids = fixtures[50]
    def reject(label, change, script=50):
        a, b, keys = fixtures[script]; a, b, keys = change(a, b, set(keys))
        try: validate(a, b, [script], keys)
        except ValueError as ex: cases.append(dict(label=label, rejected=True, error=str(ex))); return
        raise ValueError('033 Aqua invalid topology accepted '+label)
    def both(before, after): return lambda a, b, i: (a.replace(before, after), b.replace(before, after), i)
    reject('other-root', both('@archive 697B70', '@archive 659CB8'))
    reject('other-portrait', both('mugshot = AquaMan', 'mugshot = Rockman'))
    reject('duplicate-FD09', both('\tsoundDisableChoiceSFX\n', '\tsoundDisableChoiceSFX\n\tsoundDisableChoiceSFX\n'))
    reject('unexpected-FD08', both('\tsoundDisableChoiceSFX\n', '\tsoundDisableChoiceSFX\n\tsoundEnableChoiceSFX\n'))
    reject('target-only-command-change', lambda a, b, i: (a, b.replace('\tsoundDisableChoiceSFX\n', ''), i))
    def move(a, b, i):
        return tuple(t.replace('\tsoundDisableChoiceSFX\n', '').replace('\tmsgOpenQuick\n', '\tsoundDisableChoiceSFX\n\tmsgOpenQuick\n') for t in (a, b))+(i,)
    reject('FD09-wrong-lifetime-position', move)
    reject('wrong-flag', both('flag = 3611', 'flag = 3610'))
    reject('wrong-choice-allocation', both('width = 8', 'width = 7'))
    reject('wrong-date-formatter', both('padZeros = true', 'padZeros = false'), 51)
    reject('wrong-provider', both('callBufferEventAMPM', 'callBufferEventYear'))
    reject('unbound-ID', lambda a, b, i: (a, b, {'697B70:50:999'}))
    reject('selected-label-overflow', lambda a, b, i: (a, replace_exact(b, {sorted(i)[-1]: '가'*20}), i))
    frozen_write(ROOT/'analysis/pending_insertion_500_033_aqua_models_v1/result.json',
                 dict(schema=1, passed=True, positive_cases=3, negative_cases=len(cases)-3, cases=cases,
                      dependencies={p: sha((ROOT/p).read_bytes()) for p in (path, 'tools/test_calendar_aqua_033.py', 'tools/calendar_aqua_capacity_033.py',
                        'tools/calendar_delete_capacity_031.py', 'tools/calendar_date_delete_capacity_032.py')},
                      rom_written=False, release_eligible=False,
                      limits='Synthetic short target fixtures only; no GBA audio/choice/caller or new Korean product-runtime approval.'))
    print('PASS033 Aqua spatial model', 3, 'positive', len(cases)-3, 'refusals')


if __name__ == '__main__': main()
