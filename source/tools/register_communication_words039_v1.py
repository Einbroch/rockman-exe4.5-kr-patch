"""Correct semantic class from whole source: communication battle help, not profile Q&A."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

OLD='analysis/pending_insertion_500_039_communication_words_survey_v1/selection.json'
OUT='analysis/pending_insertion_500_039_communication_words_v1'

def main():
    s=deepcopy(read(OLD))
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    if s['selected_proposed_units']!=500 or len(s['selected_ids'])!=500:raise ValueError('039 exact500 source proposal prerequisite')
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    for g in s['groups']:
        require_hash(ROOT/g['source_tpl']['path'],g['source_tpl']['sha256'])
        text=(ROOT/g['source_tpl']['path']).read_text(encoding='utf-8-sig')
        if not all(x in text for x in ('VS リアルオペレーション','シングルバトル','トリプルバトル')):raise ValueError('Communication whole-archive semantic context')
        g['source_class']='communication-help';g['profile']='communication-quick-zero-speed-visible-hold132'
        g['explicit_layouts']={x['id']:x['layout']['target'] for x in g['layout_proposals']}
        g['geometry_ids']=g['ids']
        g['semantic_context']='Navi-specific local communication battle mode explanation and settings help. Not operator/profile questions.'
    s['status']='EXACT500_COMMUNICATION_HELP_SOURCE_LAYOUT_PROPOSALS_NOT_ROM'
    s['semantic_context']='Local communication menu: Real Operation / Rockman EXE4, single/triple battle and Chip Gate settings. mmbn45s menu labels are NOT among these500 normal-dialogue IDs.'
    s['classification_correction']='v1/v2 temporary profile label was disproved by whole-archive menu labels and help text. Source addresses, canonical wording and layout proposals unchanged; those reports retained as history.'
    s['dependencies'].update({OLD:sha((ROOT/OLD).read_bytes()),'tools/register_communication_words039_v1.py':sha((ROOT/'tools/register_communication_words039_v1.py').read_bytes())})
    s['source_proposal_parent']=dict(path=OLD,sha256=sha((ROOT/OLD).read_bytes()))
    s['planned_new_units']=500;s['new_network_connection_tested']=False
    if any(p['layout']['soft_breaks'] for g in s['groups'] for p in g['layout_proposals']):raise ValueError('No syllable breaks in selected500')
    s['selected_layout_policy']='Existing LF/space-only word boundaries; all letters, spacing and protected edges preserved. Preliminary syllable-break alternative NOT selected.'
    frozen_write(ROOT/OUT/'selection.json',s)
    print('039 corrected communication-help exact500 /',len({g['archive'] for g in s['groups']}),'archives; not ROM')

if __name__=='__main__':main()
