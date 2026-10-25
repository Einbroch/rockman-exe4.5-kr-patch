"""Controlled finite normal2/3-node vertical source-preserved model tests."""
import re
from build_visibility_poc import ROOT, sha
from cumulative_batch500 import read, frozen_write
from tpl_literals import literals
from survey_aggregate_pet_033 import replace_exact
from normal_vertical_choices_033 import validate


def main():
    census = read('analysis/pending_insertion_500_033_vertical_inventory_v1/census.json'); fixtures = {}; cases = []
    for arc, script in [('766134', 5), ('766134', 6), ('71551C', 51), ('71A66C', 8)]:
        group = next(g for g in census['groups'] if (g['archive'], g['script']) == (arc, script)); text = (ROOT/group['source_tpl']['path']).read_text(encoding='utf-8-sig')
        section = re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)', text, re.M)[0]; old = '@archive '+arc+'\n'+section
        values = {u.key: '가'+'\n'*u.text.count('\n')+' '*(len(u.text)-len(u.text.rstrip(' '))) for u in literals(old) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]', u.text)}
        new = replace_exact(old, values); ids = set(values)
        try: proof = validate(old, new, [script], ids, 99, 88)
        except ValueError:
            if arc != '766134': continue
            raise
        fixtures[(arc, script)] = (old, new, ids); cases.append(dict(label=arc+':'+str(script), accepted=True, pages=proof[0]['pages']))
    def reject(label, change, key=('766134', 6)):
        a, b, ids = fixtures[key]; a, b, ids = change(a, b, set(ids))
        try: validate(a, b, [key[1]], ids, 99, 88)
        except ValueError as ex: cases.append(dict(label=label, rejected=True, error=str(ex))); return
        raise ValueError('033 invalid vertical input accepted '+label)
    def both(before, after): return lambda a, b, i: (a.replace(before, after), b.replace(before, after), i)
    reject('undeclared-root', both('@archive 766134', '@archive 123456'))
    reject('unmodeled-wide-width', both('width = 13', 'width = 14'))
    reject('mismatched-target-control', lambda a, b, i: (a, b.replace('width = 13', 'width = 12', 1), i))
    reject('inconsistent-centering', lambda a, b, i: (a.replace('width = 13', 'width = 12', 1), b.replace('width = 13', 'width = 12', 1), i))
    reject('unsupported-space', both('count = 1', 'count = 2'))
    reject('invalid-navigation', both('down = 2', 'down = 3'))
    reject('default-outside-three', both('default = 0', 'default = 3'))
    reject('nonclearing-select', both('clear = true', 'clear = false'))
    reject('different-source-delay', both('delay = 0', 'delay = 1'))
    reject('unbound-ID', lambda a, b, i: (a, b, {'766134:6:999'}))
    def too_wide(a, b, ids):
        values = {u.key: '가'*14+('\n' if u.text.endswith('\n') else '') for u in literals(b) if u.key in ids}
        return a, replace_exact(b, values), ids
    reject('labels-exceed151px', too_wide)
    def no_final_target(a, b, ids):
        token = '\t\t\tjump = continue,\n'
        return a.replace(token, '', 1), b.replace(token, '', 1), ids
    reject('missing-cancel-target', no_final_target)
    def inaccessible(a, b, ids):
        for text in (a, b):
            pass
        def change(t):
            return re.sub(r'(\t\t(?:left|right|up|down) = )\d', r'\g<1>0', t)
        return change(a), change(b), ids
    reject('inaccessible-options', inaccessible)
    first = fixtures[('766134', 5)]
    key = next(u.key for u in literals(first[1]) if u.key in first[2] and u.text.endswith('\n'))
    reject('prompt-missing-empty-option-row', lambda a, b, ids: (a, replace_exact(b, {key: '가'}), ids), ('766134', 5))
    positive = sum(c.get('accepted', False) for c in cases); negative = sum(c.get('rejected', False) for c in cases)
    frozen_write(ROOT/'analysis/pending_insertion_500_033_vertical_models_v1/result.json',
                 dict(schema=1, passed=True, positive_cases=positive, negative_cases=negative, cases=cases,
                      dependencies={p: sha((ROOT/p).read_bytes()) for p in ('tools/test_vertical_choices_033.py', 'tools/normal_vertical_choices_033.py',
                          'analysis/pending_insertion_500_033_vertical_inventory_v1/census.json')}, rom_written=False, release_eligible=False,
                      limits='Synthetic short Korean fixtures exercise geometry/navigation contract acceptance/refusal; not native EA/EC branch execution or actual target147 runtime/semantic approval.'))
    print('PASS033 vertical model', positive, 'positive', negative, 'refusals')


if __name__ == '__main__': main()
