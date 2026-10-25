"""Four individually authored greetings; source-pinned serialization only."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFT={1:['거츠, 거츠!!','처음 뵙겠거스!!\n거츠맨이거츠!'],2:['오랜만이거스!!','다시 함께\n힘내겠거스!!']}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    p=ROOT/'analysis/full_scope_v1/source_tpl/665EB8.tpl';require_hash(p,'554c04d09092b0c9f5384a606a7e257a80dc8d1f6e1cb2ddcf1aa996b34805d0');tpl=p.read_text(encoding='utf-8-sig');items=literals(tpl)
    if {x.key for x in items}!={f'665EB8:{s}:{i}' for s,rows in DRAFT.items() for i in range(len(rows))}:raise ValueError('source population')
    units=[dict(id=x.key,source=x.text,translation=DRAFT[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
    replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='665EB8',source_archive_sha256='ba5d7653dfd99d0c80bc1a5b2eeae3ca2ecbceb03809d30d2bfaa10112ef31b8',consumer='normal-dialogue',context='GutsMan first meeting script1/reselection greeting script2 to operator, explicit ガッツマン speaker. Original root038110=08665EB8; same native group seasonal root038144. Portrait92,110; flag3585/waits/clears retained, no variables.',voice='Existing GutsMan seasonal/save development drafts use 거츠/거스. Reused candidate voice, human review pending.',evidence='analysis/full_scope_v1/source_tpl/665EB8.tpl; translations/gutsman_seasonal_ko.json; native roots038110/038144',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='Complete four literals/4slots; original IDs/source,numerals,newline boundaries/commands/flag3585 preserved. No save/name/gameplay/RTC changes.',semantic_review=['First-meeting vs long-time-no-see kept distinct. Guts catchphrase retained in both name and ending; wording/voice human review pending. NumberMan4649 adaptation not reused.'],units=units)
    out=ROOT/'translations/gutsman_intro_ko.json'
    if out.exists():raise ValueError('preserve existing translation')
    out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print('GutsMan intro4 serialized')

if __name__=='__main__':main()
