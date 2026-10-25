"""Controlled contracts for LF-only aggregate proposals; no product claim."""
from build_visibility_poc import ROOT, sha
from cumulative_batch500 import frozen_write
from survey_aggregate_pet_033 import aggregate, replace_exact, variants
from pet_nickname_capacity_025 import validate
from tpl_literals import literals, skeleton

PREFIX = '''@archive ABCDEF
script 1 mmbn45 {
	positionBox
		left = 10
		top = 12
		type = 1
	msgOpenQuick
	positionText
		left = 92
		top = 110
		arrowDistance = 3
	positionArrow
		left = 225
		top = 141
	printPlayerNickname
		capitalizeFirst = false
		capitalizeAll = false
		printN = false
'''
SUFFIX = '''	keyWait
		any = false
	clearMsg
	waitHold
}
'''


def fixture(value):
    return PREFIX + '\t"' + value.replace('\n', '\\n') + '"\n' + SUFFIX


def main():
    cases = []
    for text, bound in [('aa aa aa aa', 99), (' aa aa\naa aa', 99), ('aa\n\n ', 66)]:
        old = fixture(text); unit = dict(id='ABCDEF:1:0', source=text, translation=text)
        values = aggregate(old, [unit], bound); new = replace_exact(old, values)
        proof = validate(old, new, [1], {unit['id']}, bound)
        if values[unit['id']].replace('\n', ' ') != text.replace('\n', ' ') or skeleton(old) != skeleton(new):
            raise ValueError('033 controlled wording/control mutation')
        cases.append(dict(label='bounded-prefix-'+repr(text), passed=True, widths=proof[0]['pages'][0]['widths']))
    # 99+two22px words do not fit the initial row. A legal interword
    # break must be selected, not a smaller provider bound or a cut word.
    old = fixture('aa aa aa aa'); unit = dict(id='ABCDEF:1:0', source='aa aa aa aa', translation='aa aa aa aa')
    new = replace_exact(old, aggregate(old, [unit], 99))
    if literals(new)[0].text == unit['translation']:
        raise ValueError('033 missing aggregate layout regression')
    cases.append(dict(label='aggregate-not-individual-width', passed=True))
    for source, canonical in [('\naa\n ', '\naa\n '), ('aa aa  ', 'aa aa  '), (' aa aa', ' aa aa')]:
        for value in variants(source, canonical):
            if value.replace('\n', ' ') != canonical.replace('\n', ' '):
                raise ValueError('033 variants changed word spaces')
            for strip in (lambda s: s.lstrip('\n'), lambda s: s.rstrip('\n'), lambda s: s.rstrip(' ')):
                if len(source)-len(strip(source)) != len(value)-len(strip(value)):
                    raise ValueError('033 variants changed protected edge')
        cases.append(dict(label='protected-edges-'+repr(source), passed=True))
    rejected = []
    def refusal(label, thunk):
        try:
            thunk()
        except ValueError as ex:
            rejected.append(dict(label=label, rejected=True, error=str(ex))); return
        raise ValueError('033 invalid controlled input accepted '+label)
    refusal('uncuttable-overflow', lambda: aggregate(fixture('a'*20), [dict(id='ABCDEF:1:0', source='a'*20, translation='a'*20)], 99))
    refusal('unknown-provider', lambda: aggregate(old.replace('printPlayerNickname', 'printUnknown'), [unit], 99))
    refusal('provider-arguments', lambda: aggregate(old.replace('printN = false', 'printN = true'), [unit], 99))
    refusal('different-origin', lambda: aggregate(old.replace('left = 92', 'left = 93'), [unit], 99))
    refusal('target-control-mutation', lambda: validate(old, new.replace('any = false', 'any = true'), [1], {unit['id']}, 99))
    refusal('terminal-hold-with-live-page', lambda: validate(old.replace('\tclearMsg\n', ''), new.replace('\tclearMsg\n', ''), [1], {unit['id']}, 99))
    refusal('unknown-encoding-representation', lambda: replace_exact(old, {unit['id']: 'a\\b'}))
    out = ROOT/'analysis/pending_insertion_500_033_aggregate_models_v1/result.json'
    frozen_write(out, dict(schema=1, passed=True, positive_cases=len(cases), negative_cases=len(rejected),
                           cases=cases+rejected, dependencies={p: sha((ROOT/p).read_bytes()) for p in
                           ('tools/test_aggregate_pet_033.py', 'tools/survey_aggregate_pet_033.py',
                            'tools/pet_nickname_capacity_025.py', 'tools/canonical_literals_031.py')},
                           rom_written=False, release_eligible=False,
                           limits='Synthetic LF proposal/replacement/unchanged validator contracts only; no real ROM runtime or semantic approval.'))
    print('PASS033 aggregate controlled', len(cases), 'positive', len(rejected), 'refusals')


if __name__ == '__main__':
    main()
