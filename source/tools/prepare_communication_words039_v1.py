"""Prefer existing LF/space-only layout policy; exclude every soft syllable break.

The preliminary500 included12 syllable-break candidates. There is a larger
word-boundary-only population, so no new word-internal layout is selected.
"""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
spec=[]
jobs=[('tools/prepare_profile_source039_v2.py','tools/survey_communication_words039_v1.py',[
 ('pending_insertion_500_039_profile_source_v2','pending_insertion_500_039_communication_words_survey_v1'),
 ("proposal=propose(u['translation'])","proposal=propose(u['translation'])\n                if proposal['soft_breaks']:raise ValueError('039 word-boundary-only cohort excludes syllable breaks')"),
 ("source_class='PET-profile'","source_class='communication-help'"),
 ("'tools/prepare_profile_source039_v2.py'","'tools/survey_communication_words039_v1.py'"),
 ('selected_ids=sorted(ids),groups=selected,','selected_ids=sorted(ids),groups=selected,candidate_groups=good,'),
 ]),('tools/prepare_communication039_v1.py','tools/register_communication_words039_v1.py',[
 ('pending_insertion_500_039_profile_source_v2','pending_insertion_500_039_communication_words_survey_v1'),
 ('pending_insertion_500_039_communication_source_v1','pending_insertion_500_039_communication_words_v1'),
 ('tools/prepare_communication039_v1.py','tools/register_communication_words039_v1.py'),
 ("s['planned_new_units']=500;s['new_network_connection_tested']=False","s['planned_new_units']=500;s['new_network_connection_tested']=False\n    if any(p['layout']['soft_breaks'] for g in s['groups'] for p in g['layout_proposals']):raise ValueError('No syllable breaks in selected500')\n    s['selected_layout_policy']='Existing LF/space-only word boundaries; all letters, spacing and protected edges preserved. Preliminary syllable-break alternative NOT selected.'"),
 ]),('tools/compile_communication039_v2.py','tools/compile_communication_words039_v1.py',[
 ('from prepare_communication039_v1 import OUT','from register_communication_words039_v1 import OUT'),
 ('tools/compile_communication039_v2.py','tools/compile_communication_words039_v1.py'),
 ("OUT/'compile_v2'","OUT/'compile_v1'"),
 ("OUT/'verification_v2.json'","OUT/'verification_v1.json'"),
 ("proposal=propose(u['translation'])","proposal=propose(u['translation'])"),
 ("u['canonical_wording']=u['translation']","if p['soft_breaks'] or value.replace('\\n',' ')!=u['translation'].replace('\\n',' '):raise ValueError('039 existing word-boundary-only policy')\n                u['canonical_wording']=u['translation']"),
 ])]
for srcname,dstname,changes in jobs:
    src=ROOT/srcname;dst=ROOT/dstname
    if dst.exists():raise ValueError('Preserve039 word-boundary branch')
    text=src.read_text(encoding='utf8');actual=[];counts=[]
    for a,b in changes:
        n=text.count(a)
        if not n:
            if a=="proposal=propose(u['translation'])":continue
            raise ValueError('039 word layout generation anchor '+a)
        actual.append([a,b]);counts.append(n);text=text.replace(a,b)
    dst.write_text(text,encoding='utf8');spec.append(dict(base=srcname,base_sha256=sha(src.read_bytes()),changes=actual,replacement_counts=counts,output=dstname,output_sha256=sha(dst.read_bytes())))
frozen_write(ROOT/'tools/specs/communication_words039_v1_version.json',dict(changes=spec,scope='Select exact500 using existing LF/space-only wording identity, no Hangul-syllable splits. All preliminary alternatives retained; no primary ROM writer or admission.'))
print('Prepared039 word-boundary-only source cohort tools')
