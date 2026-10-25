"""Finite224 raw explicit-normal vertical-menu population, NOT admission."""
import re
from collections import defaultdict, Counter
from build_visibility_poc import ROOT, sha, require_hash
from cumulative_batch500 import read, frozen_write
from prepare_repartition500 import layout_records
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from field_hint_capacity import events
from tpl_literals import literals
from survey_aggregate_pet_033 import BASE, BASE_SHA, SURVEY

OUT = 'analysis/pending_insertion_500_033_vertical_inventory_v1/census.json'
ALLOWED = set('mugshotShow mugshotHide msgOpen textSpeed keyWait clearMsg positionOptionVertical option space select end flagSet flagClear flagSetNavi flagClearNavi wait waitSkip printPlayerNickname'.split())


def main():
    cfg = read('project.json'); sp = ROOT/cfg['source_profile']['filename']; require_hash(sp, cfg['source_profile']['sha256']); source = sp.read_bytes()
    require_hash(ROOT/BASE, BASE_SHA); m = read(BASE.replace('.gba', '.json')); applied = {u['id'] for r in layout_records(m) for u in r['layout']}
    survey = read(SURVEY)
    if survey['baseline_sha256'] != BASE_SHA or survey['pinned_changed_inputs']: raise ValueError('033 vertical actual032 baseline')
    require_hash(ROOT/cfg['text_catalog']['path'], cfg['text_catalog']['sha256']); catalog = {f"{r['offset']:X}": r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    coverage = read(survey['pinned_coverage']['path']); require_hash(ROOT/survey['pinned_coverage']['path'], survey['pinned_coverage']['sha256']); pool = defaultdict(list)
    for p, h in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/p, h); a = read(p)
        for u in a['units']: pool[u['id']].append((p, h, u, a))
    groups = []; cache = {}; deps = {SURVEY: sha((ROOT/SURVEY).read_bytes()), 'tools/inspect_vertical_population_033.py': sha((ROOT/'tools/inspect_vertical_population_033.py').read_bytes())}
    prepared = set(read('analysis/pending_insertion_500_033_preflight272_v2/status.json')['selected_ids'])
    for g in survey['unresolved_groups']+survey['candidates']:
        arc = g['archive']; row = catalog[arc]
        if not g['ids'] or set(g['ids'])&(applied|prepared) or row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers'] == [0] or 'different_renderer' in g.get('reasons', []): continue
        options = pool[g['ids'][0]]
        if not options: raise ValueError('033 vertical missing canonical source')
        src = options[0][3]['source_tpl']
        if arc not in cache:
            require_hash(ROOT/src['path'], src['sha256']); deps[src['path']] = src['sha256']; text = (ROOT/src['path']).read_text(encoding='utf-8-sig')
            cache[arc] = {int(x[1]): x[0] for x in re.finditer(r'^script (\d+) \w+ \{[\s\S]*?(?=^script\s|\Z)', text, re.M)}
        one = '@archive '+arc+'\n'+cache[arc][g['script']]; commands = [d for _, kind, d in events(one) if kind == 'command']; names = {d[0] for d in commands}
        if not {'positionOptionVertical', 'msgOpen'} <= names or not names <= ALLOWED: continue
        refs = []; old = {u.key: u for u in literals(one)}; native_sha = sha(payload_of(source, row))
        for key in g['ids']:
            choices = pool[key]
            if not choices or len({(u['source'], u['translation'], u['state']) for _, _, u, _ in choices}) != 1: raise ValueError('033 vertical wording conflict')
            p, h, u, a = choices[0]
            if u['source'] != old[key].text or a['source_tpl'] != src or a['source_archive_sha256'] != native_sha: raise ValueError('033 vertical source/wording provenance')
            refs.append(dict(id=key, path=p, sha256=h))
        widths = [int(re.fullmatch(r'\t\twidth = (\d+)\n', args)[1]) for name, args in commands if name == 'positionOptionVertical']
        groups.append(dict(archive=arc, script=g['script'], ids=g['ids'], units=len(g['ids']), source_tpl=src,
                           source_row=row, source_archive_sha256=native_sha, drafts=refs, commands=commands,
                           vertical_widths=widths, option_count=sum(name == 'option' for name, _ in commands),
                           selectors=sum(name == 'select' for name, _ in commands),
                           current_primary_present=any(r['archive'] == arc for r in m['archives']), product_admitted=False))
    ids = [k for g in groups for k in g['ids']]
    if len(ids) != len(set(ids)): raise ValueError('033 duplicate vertical inventory')
    frozen_write(ROOT/OUT, dict(schema=1, status='FINITE_VERTICAL_MENU_POPULATION_ONLY_NOT_PREPARED_OR_ADMITTED',
                  baseline_rom=BASE, baseline_sha256=BASE_SHA, source_sha256=cfg['source_profile']['sha256'],
                  literal_units=len(ids), script_groups=len(groups), archives=len({g['archive'] for g in groups}),
                  by_archive=dict(Counter({arc: sum(g['units'] for g in groups if g['archive'] == arc) for arc in sorted({g['archive'] for g in groups})})),
                  native_widths=sorted({w for g in groups for w in g['vertical_widths']}), groups=groups, dependencies=deps,
                  rom_written=False, new_units_applied=0, release_eligible=False,
                  limits=['Finite RAW explicit-msgOpen scripts with the declared existing commands only, not all vertical choices or whole-game remainder.',
                          '224is a candidate population, not guaranteed-fitting translations, prepared units or an exact228 supplement.',
                          'Width13, two/three-option navigation/default/BSeparate/disableB/targets and prompt-versus-cleared-row placement need dedicated native CPU/model/runtime evidence.',
                          'Canonical wording/protected edges, aggregate layout, source-only/carry/primary source gates and exact500 still required.']))
    print('033 vertical inventory', len(ids), 'units', len(groups), 'scripts', len({g['archive'] for g in groups}), 'archives;NOT admitted')


if __name__ == '__main__': main()
