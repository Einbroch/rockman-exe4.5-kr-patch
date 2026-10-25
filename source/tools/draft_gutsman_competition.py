"""Authored ten-literal GutsMan competition draft, not bulk prose generation."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals,validate_nickname_suffix

TPL_SHA='142b517fc402bcb024d5dfd814c78a1e5b070d0ac05520276bf229ebc566e434'
PAYLOAD_SHA='fc320d1c830dfa2984a693787f92e26d3c46421126a9a2f3af3f354ec44a1a7f'
DRAFT={1:['으그~!!\n분하거스!!','다음엔 반드시\n우승하겠거스!!'],2:['해냈거스!!\n우승이거스!!','、\n2명이 함께 이룬\n영광이거스!!','거츠、거츠、\n거츠츠ー!!'],10:['!\n참가 등록이 안 됐거스'],20:['거츠거츠!\n우승을 향해\n힘내겠거스!!'],21:['거츠거츠!\n우승을 향해\n힘내겠거스!!'],22:['거츠거츠!\n우승을 향해\n힘내겠거스!!'],23:['거츠거츠!\n우승을 향해\n힘내겠거스!!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/666D5C.tpl';require_hash(p,TPL_SHA);tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'666D5C:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('finite population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True));scope=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text())['archives']['666D5C'];validate_nickname_suffix(units,'666D5C',scope)
    out=ROOT/'translations/gutsman_competition_ko.json'
    if out.exists():raise ValueError('preserve translation')
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='666D5C',source_archive_sha256=PAYLOAD_SHA,consumer='normal-dialogue',context='GutsMan native group root03812C/intro+28. Defeat1,victory2,unregistered10,encouragement20..23. Native GutsMan unregistered10 observed on operations-v1; source25slots/473bytes/10literals.',voice='Existing development 거츠/거스 candidate voice; not human-approved for release.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='IDs/source/newline/numeral2/all commands/native nickname variables/keyWait/clear/cancel menu/flag3603 unchanged.',semantic_review=['Nickname と replaced by non-growing comma11px; next row explicitly says 2 people achieved together, preserving cooperative meaning without value-dependent Korean particle.','No player-name edit/save/unlock/tournament result proof by static analysis. NumberMan4649 approval not reused.'],units=units)
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('Guts competition10 serialized')

if __name__=='__main__':main()
