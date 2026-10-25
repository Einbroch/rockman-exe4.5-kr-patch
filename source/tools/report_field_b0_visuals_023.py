"""Record the primary agent's sampled visual review; never human approval."""
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    rp=ROOT/'poc/output/pending500_023_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    folder=ROOT/'analysis/pending500_023_v1';refs=read(folder/'visual_sheet_inputs.json')
    sheets=[]
    for r in refs['contact_sheets']:
        p=ROOT/r['contact_sheet'];sheets.append(dict(path=r['contact_sheet'],sha256=sha(p.read_bytes()),source_count=len(r['sources'])))
    old=ROOT/'poc/runtime/pending500-022-v2-boot/step_009.png';new=ROOT/'poc/runtime/pending500-023-v1-boot/step_009.png'
    old_receipt=read(old.parent/'result.json');new_receipt=read(new.parent/'result.json')
    require_hash(old,old_receipt['artifacts'][old.name]);require_hash(new,new_receipt['artifacts'][new.name])
    box=(22,48,224,118);a=Image.open(old).convert('RGB').crop(box).tobytes();b=Image.open(new).convert('RGB').crop(box).tobytes()
    if a!=b:raise ValueError('Inherited welcome text crop differs; reopen visual cause investigation')
    result=dict(schema=1,passed=True,rom_sha256=m['output_sha256'],agent_sampled_visual_review_performed=True,human_approval=False,all500_semantic_or_visual_approval=False,contact_sheets=sheets,natural_hint_review=dict(unique_source_id='78BF28:10:0',display_count=2,exit_count=2,wording='인터넷을 좀 더\n탐색해 보자!',observed='Both normal B0 displays are legible, correct two-row wording; no clipping/occlusion/residue seen. Both exits return to network field without dialogue window. Source-preserved Navi0 portrait; no actor/script alias.'),startup_observation='Reviewed title/date entry/confirmation, native kana/katakana/Latin pages and Korean command labels, name confirmation, gender/age/occupation/profile, Navi selection and initial mailbox notification. Native input remains Japanese, not automatic Hangul.',first_mail_pages_reviewed=23,first_mail_observation='Reviewed the23 I.P.C. body panels; readable Korean text and expected page breaks/continuations. This is sampled first-letter presentation, not all500 language approval.',open_issues=[dict(id='welcome-tight-leading',state='OPEN_INHERITED',observation='Purchase/name request graphic lines remain visibly crowded/overlapping; unchanged versus022',old_crop_sha256=sha(a),new_crop_sha256=sha(b),crop=list(box)),dict(id='field-date-HUD',state='OPEN_INHERITED',observation='Normal Monday field HUD still displays Japanese month/day/weekday notation.'),dict(id='native-name-entry-suffix',state='OPEN',observation='Kana layout and native honorific remain; automatic Hangul composition/commit/save/redisplay is not installed.')],release_eligible=False,limits='Only these captured normal paths and source identities were visually reviewed by the primary agent. No human approval, every-page/Navi/progress-branch/variable display or complete localization claim.')
    frozen_write(folder/'visual_review.json',result)
    print('PASS sampled visual record: natural hint twice/exits, startup19, firstmail23; inherited welcome crop unchanged; NOT human approval')


if __name__=='__main__':main()
