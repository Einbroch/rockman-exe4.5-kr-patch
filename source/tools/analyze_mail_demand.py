"""Exact encoding-footprint accounting, NOT a compiled full-scope ROM proof."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from first_mail import SPECS,selected_units
from korean_codec import encode_character

def main():
    baseline=ROOT/'poc/output/exe45_ko_development_official_mail_v1_r2.gba'
    require_hash(baseline,'e4c56544b754c84f464797d20657f88f7562f017c874c74d7f3ca0af2f024fbd')
    m=json.loads(baseline.with_suffix('.json').read_text(encoding='utf8'))
    s=SPECS['6DD9AC'];require_hash(ROOT/s['draft'],s['draft_sha'])
    draft=json.loads((ROOT/s['draft']).read_text(encoding='utf8'))
    table_path=ROOT/'poc/build'/baseline.stem/'plugins/exe45-utf8.tbl'
    table={}
    for line in table_path.read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            key,value=line.split('=',1)
            if len(value)==1:table[value]=bytes.fromhex(key)
    def enc(text):return b''.join(b'\xE8' if c=='\n' else encode_character(c) if '\uac00'<=c<='\ud7a3' or c==',' else table[c] for c in text)
    def growth(units):return sum(len(enc(u['translation']))-len(enc(u['source'])) for u in units)
    native_bytes=next(r for r in m['archives'] if r['archive']=='6DD9AC')['source_bytes']
    observed=next(r for r in m['archives'] if r['archive']=='6DD9AC')['compiled_bytes']
    official=selected_units('6DD9AC',True);news=selected_units('6DD9AC','news')
    if native_bytes+growth(official)!=observed:raise ValueError('footprint oracle disagrees with compiled baseline')
    complete={u['id']:dict(u) for u in draft['units']}
    complete.update({u['id']:u for u in news})
    all_units=list(complete.values());all_bytes=native_bytes+growth(all_units)
    remaining=[u for u in all_units if int(u['id'].split(':')[1])>=11]
    report=dict(schema=1,scope='6DD9AC exact text-byte footprint; fixed source controls/table size presumed unchanged; not full candidate compilation/geometry/variable/runtime proof',source_sha256=m['source_sha256'],draft_sha256=s['draft_sha'],baseline_sha256=m['output_sha256'],encoding_table_sha256=sha(table_path.read_bytes()),native_bytes=native_bytes,observed_current_bytes=observed,current_prediction_exact=True,news1_to3_predicted_bytes=native_bytes+growth(news),full120_predicted_bytes=all_bytes,confirmed_buffer_cap=s['cap'],full_overflow_bytes=max(0,all_bytes-s['cap']),remaining_news_and_invitation_units=len(remaining),layout_inputs=[dict(path=p,sha256=sha((ROOT/p).read_bytes())) for p in ['translations/first_mail_layout_v2.json','translations/official_mail_layout_v1.json','translations/news_mail_layout_v1.json']],decision='Do not enlarge RAM extent into next asset. News1..3 candidate fits; full integration needs independently verified partition/ROM-reader or other consumer-safe design. No design adopted here.',alternative_news_only_pool_predicted_bytes=native_bytes+growth([u for u in all_units if int(u['id'].split(':')[1])>=8]),per_script_growth=[dict(script=i,units=len([u for u in all_units if int(u['id'].split(':')[1])==i]),delta=growth([u for u in all_units if int(u['id'].split(':')[1])==i])) for i in [0,1,2,3,8,9,10,11,12,13,14]])
    out=ROOT/'analysis/news_mail_v1/full_body_demand.json'
    if out.exists():raise ValueError('preserve demand report')
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print({k:report[k] for k in ['news1_to3_predicted_bytes','full120_predicted_bytes','full_overflow_bytes','remaining_news_and_invitation_units','alternative_news_only_pool_predicted_bytes']})

if __name__=='__main__':main()
