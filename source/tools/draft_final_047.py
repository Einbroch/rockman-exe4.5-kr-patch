"""13 manually authored remaining literals; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
    "7B450C": ["966e262389c67c4a35d375944a8d097051973aebf14d725ea08e173da45b37f4",1,"translations/final_047_remaining_7B450C_draft_ko.json"],
    "7B5110": ["3b7dcc0d61ab37a7861919933135d84d87024fd8e448474ee2004045c49566d8",1,"translations/final_047_remaining_7B5110_draft_ko.json"],
    "7B5AA8": ["6f658b5e7d85e6a16610078bb4c8d1803386c84a0dc702642dd80f10630f82d6",1,"translations/final_047_remaining_7B5AA8_draft_ko.json"],
    "7C0970": ["2e139591c63fe2e51dd520cea5d5b2b0c868cb585c3d67131d4e6af9ef71a4a2",1,"translations/final_047_remaining_7C0970_draft_ko.json"],
    "7C0F8C": ["edf11d34b1b2274c04e6db071af44634953839431adc02c2f660dbeb7fd85092",1,"translations/final_047_remaining_7C0F8C_draft_ko.json"],
    "7C416C": ["9b0d61ddec947152e09eded2b82625bbcf44957c58eed5222d3386f3a5c5ab64",2,"translations/final_047_remaining_7C416C_draft_ko.json"],
    "7C9C44": ["eeeaa9510dc7c6ae82b96eeb2acd556bbe177ee38850f62bd6e6f71186327b79",2,"translations/final_047_remaining_7C9C44_draft_ko.json"],
    "7CAF40": ["fe245cacc8563907812065f23d0d61f99902ff6c98696ba75638321ccea6ff42",4,"translations/final_047_remaining_7CAF40_draft_ko.json"],
}
DRAFT={
  "7B450C": {
    "0:0": "전뇌 세계,\n인터넷에 오신 걸 환영합니다!\n여기는 아키하라 에리어예용"
  },
  "7B5110": {
    "0:0": "전뇌 세계,\n인터넷에 오신 걸 환영합니다!\n여기는 아키하라 에리어예용"
  },
  "7B5AA8": {
    "0:0": "전뇌 세계,\n인터넷에 오신 걸 환영합니다!\n여기는 아키하라 에리어예용"
  },
  "7C0970": {
    "0:0": "미니게임을 실행합니다\n(임시)"
  },
  "7C0F8C": {
    "0:0": "배틀 테스트1(임시)\n배틀 시작 DEATH!"
  },
  "7C416C": {
    "1:0": "후아~\n당했소이다",
    "1:1": "와아 와아 이겼다 이겼다\n(임시)"
  },
  "7C9C44": {
    "0:0": "여기는 영원한\n증오가 소용돌이치는 세계···",
    "0:1": "밉다···밉다···\n이 세계, 모든 것이···"
  },
  "7CAF40": {
    "0:0": "레이저맨을\n삭제했나···",
    "0:1": "네놈은···나를\n만족시켜 줄 수 있나···",
    "0:2": "싸움에 굶주린\n내 마음을···",
    "22:0": "나와···싸워라···"
  }
}
EXCLUDED={'6368E8:2:0','6368E8:3:0'}
CHOICES=set([])
LABELS=set([])
CONTEXT={
  "7B450C": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B5110": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7B5AA8": "NPC weekday/elemental viruses/shopping/patrol/classes/Official meetings/student ambition or legacyAkihara greeting. Local portraits established perliteral, source facts/suspicions kept; actual route unverified.",
  "7C0970": "Provisional minigame/battle-test startup message; temporary marker retained; no test functionality changed or executed.",
  "7C0F8C": "Provisional minigame/battle-test startup message; temporary marker retained; no test functionality changed or executed.",
  "7C416C": "Provisional aftermath: MrProgGreen defeat thenKnightMan celebratory victory; NOT swapped portraits. Temporarymarker retained.",
  "7C9C44": "No local portrait: hatred-filled world/narrator unidentified; contextual meaning literal, no inferred speaker approval.",
  "7CAF40": "No local portrait for0, explicithide22: asks aboutLaserMan deletion and battle hunger; no forced Navi identity. Prior branch context retained."
}
SEMANTIC_REVIEW=[
  "Remaining515catalog units reconciled:500manual drafts(batch046)+13manual drafts(final047);2kana selector arrays remain unresolved structural input targets, not silently excluded from denominator. Not513unique sentences; no ROM writes.",
  "All selected source literals and native selected-script skeletons read, exact repeated WAIT_FALSE/CLEAR blocks abbreviated only in read-only logical view. Allsource IDs/TPL/payload/digits/brackets/line topology/padding/native commands preserved.",
  "Manual source-conditioned free prose. No automated prose generation, selection or shortening. New voices/terms/cultural names/honorifics/packed field segmentation need independent/human review; allneeds_review releasefalse.",
  "513translated strings include developer/prototype/soul-unison/legacy labels. Presence inROM is not proof of normal reachability or support; debug granting/save-affecting commands never executed.",
  "Packed BBS/profile/PA/Latin table byte/cell boundaries unresolved. Draft-first assets are not insertion-ready; 132px heuristic cannot approve/shorten or establish actual capacity.",
  "Name-entry source6368E8scripts2/3 are originalkana selector arrays; adopted40jamo page/composer is separate. Changing literal text cannot integrate selectors/rendering/commit/redisplay/persistence. Keep2original units untranslated until structural integration.",
  "Explicit portraits, hide transitions and player choices preserved; no portrait inferred solely from text.source768800MrProgGreen/Lan;7C416CMrProgGreen thenKnightMan.7C9C44/7CAF40speakerunknown.",
  "Source digits:+30/3turn/1chip/STA002103203303/HP memory33/itemgrant etc immutable. Developerallchip/currency/profile flags and minigameflag5059 unchanged. No emulator/save/ROM/image/keyboard modifications.",
  "Current draft-first sequence continues into whole-corpus consumer/font/layout readiness then cumulativeROM/screen/save regression; human wording review/graphics/keyboard integration/persistence/release remainopen."
]
def authored(archive):return DRAFT[archive]
def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    remaining={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}
    ids={archive+':'+k for k in authored(archive)}
    if not ids<=remaining or ids & EXCLUDED:raise ValueError('batch selected-ID scope '+archive)
    values={archive+':'+k:v for k,v in authored(archive).items()}
    selected=[x for x in literals(original) if x.key in ids]
    if len(selected)!=count or set(values)!=ids:raise ValueError('batch scope '+archive+' missing '+str(ids-set(values))+' extra '+str(set(values)-ids))
    units=[]
    scripts={int(m.group(1)):m.group(2) for m in re.finditer(r'script (\d+) \w+ \{(.*?)(?=\nscript |\Z)',original,re.S)}
    for x in selected:
        suffix=':'.join(x.key.split(':')[1:]);t=values[x.key];s=int(suffix.split(':')[0])
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('batch topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('batch tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('batch padding '+x.key)
        if len(x.text)-len(x.text.lstrip(' '))!=len(t)-len(t.lstrip(' ')):raise ValueError('batch leadingpadding '+x.key)
        if any(len(src)-len(src.lstrip(' '))!=len(dst)-len(dst.lstrip(' ')) for src,dst in zip(x.text.split('\n'),t.split('\n'))):raise ValueError('batch perline leadingpadding '+x.key)
        prefix=original[original.index('script '+str(s)+' '):x.start]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',prefix))
        portrait=events[-1].group(1) if events and events[-1].group(1) else None
        visibility='shown' if portrait else 'hidden' if events else 'not-shown-in-script'
        speaker_evidence='explicit local portrait' if portrait else 'unestablished local speaker'
        if x.key in LABELS:
            speaker='ui-label';speaker_evidence='source UI/data/debug label; not normal spoken dialogue; consumer context in asset'
        elif x.key in CHOICES:
            speaker='player-choice';speaker_evidence='native option literal'
        else:
            speaker=portrait or 'speaker-unestablished'
            if False:raise AssertionError('no inherited portrait exception')
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait=portrait,portrait_visibility=visibility,speaker_evidence=speaker_evidence,context=CONTEXT[archive],
            variable_context='Native dynamic inserts/branch/choice/portrait/HP commands immutable; inline grammar/geometry/reachability/runtime unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='remaining-contextual-ui-debug-npc',
        context=CONTEXT[archive],voice='Manual source-conditioned drafts;explicit portrait where shown;unapproved terms and voices.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Source IDs/text/TPL/payload,commands,variables,newline/padding and unselected source immutable; no ROM/save writes.',
        batch_id='final-047',semantic_review=SEMANTIC_REVIEW,units=units)

def main():
    if sum(v[1] for v in SOURCES.values())!=13:raise ValueError('13 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
