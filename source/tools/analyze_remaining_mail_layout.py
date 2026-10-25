"""Remaining43 mail literal demand; variables are unresolved, not passed."""
import json
from first_mail import ROOT,SPECS,require_hash
from tpl_literals import literals

def main():
    s=SPECS['6DD9AC'];require_hash(ROOT/s['draft'],s['draft_sha'])
    draft=json.loads((ROOT/s['draft']).read_text(encoding='utf8'));tpl=draft['source_tpl'];require_hash(ROOT/tpl['path'],tpl['sha256'])
    source=(ROOT/tpl['path']).read_text(encoding='utf-8-sig')
    units=[u for u in draft['units'] if int(u['id'].split(':')[1]) in (11,12,13,14)]
    if {x.key:x.text for x in literals(source) if int(x.key.split(':')[1]) in (11,12,13,14)}!={u['id']:u['source'] for u in units}:raise ValueError('remaining literal source population')
    def width(line):return sum(12 if '\uac00'<=c<='\ud7a3' or c==',' else 8 if c==' ' else 11 for c in line)
    rows=[]
    for u in units:
        widths=list(map(width,u['translation'].split('\n')))
        rows.append(dict(id=u['id'],source=u['source'],translation=u['translation'],line_advance_pixels=widths,
            literal_only_overflow=len(widths)>3 or max(widths)>152 or len(widths)==3 and widths[2]>132))
    joins=[dict(script=11,literals=[5,6]),dict(script=11,literals=[7,8]),dict(script=12,literals=[1,2]),dict(script=13,literals=[2,3]),dict(script=14,literals=[0],player_name_before_first_literal=True)]
    result=dict(schema=1,scope='Literal-only layout demand; NOT approved wording or build inputs. Variable joins are NOT verified.',draft_sha256=s['draft_sha'],source_tpl=tpl,units=len(units),literal_rows=rows,overflow_ids=[r['id'] for r in rows if r['literal_only_overflow']],player_name_join_pages=joins,name_representation_and_max_advance='unresolved for whole full-body build; do not guess capacity from sample name',action='Per-page wording/layout review, finite native-name aggregate proof, full raw clone compilation and bounded loaded guard header required; no automatic prose rewrite')
    out=ROOT/'analysis/mail_rom_reader_v1/remaining43_layout_demand.json'
    if out.exists():raise ValueError('preserve analysis evidence')
    out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(units=result['units'],overflow_ids=result['overflow_ids'],variable_pages=len(joins)),ensure_ascii=False))

if __name__=='__main__':main()
