"""Three explicit source-ID page placements; no wording replacement or bulk wrapping."""
import json
from build_visibility_poc import ROOT,sha
from tpl_literals import literals,replace_literals,serialize,skeleton

SPEC='translations/pending_insertion_500_002_pages.json'
IDS={'6DED88:41:1','6DED88:49:1','6DED88:55:2'}
SEPARATOR='\n\tkeyWait\n\t\tany = false\n\tclearMsg\n\t'


def specification(archive=None):
    gear=archive in ('6E1CC0','6E21B0')
    path=ROOT/('translations/pending_insertion_500_003_pages.json' if gear else SPEC)
    spec=json.loads(path.read_text(encoding='utf8'))
    expected={'6E1CC0:70:1','6E21B0:70:1'} if gear else IDS
    if spec['release_eligible'] is not False or set(spec['pages'])!=expected:
        raise ValueError('Explicit page scope changed')
    return spec,sha(path.read_bytes())


def replace(tpl,units):
    """Return compiled TPL and original-ID -> fragment-ID map."""
    original=literals(tpl)
    archive=original[0].key.split(':')[0]
    spec,digest=specification(archive);active_ids=set(spec['pages'])
    spec_path='translations/pending_insertion_500_003_pages.json' if archive in ('6E1CC0','6E21B0') else SPEC
    language={x.key:x.language for x in original}
    target=tpl
    grouped={}
    for u in units:grouped.setdefault(language[u['id']],[]).append(u)
    for lang,subset in grouped.items():target=replace_literals(target,subset,language=lang)
    selected={x['id']:x for x in units}
    if not active_ids&set(selected):
        if skeleton(target)!=skeleton(tpl):raise ValueError('Native command skeleton changed')
        return target,{x.key:[x.key] for x in literals(target)},dict(path=spec_path,sha256=digest,
            selected_ids=[],extra_wait_clear_pairs=0,native_commands_preserved_after_exact_collapse=True,runtime_tested=False)
    before=literals(target)
    edits=[];fragments={}
    for item in before:
        pages=spec['pages'].get(item.key) if item.key in selected else None
        if pages is None:
            fragments[item.key]=[item.text]
            continue
        if not 1<=len(pages)<=2 or any(not p or p.count('\n')>2 for p in pages):
            raise ValueError('Explicit page extent')
        if ' '.join(p.replace('\n',' ') for p in pages)!=selected[item.key]['translation'].replace('\n',' '):
            raise ValueError('Explicit page changes words/order: '+item.key)
        if item.language!='mmbn45' or item.key not in active_ids:
            raise ValueError('Unregistered page consumer')
        fragments[item.key]=pages
        edits.append((item.start,item.end,SEPARATOR.join(serialize(p) for p in pages)))
    for start,end,value in reversed(edits):target=target[:start]+value+target[end:]
    after=literals(target)
    if len(after)!=sum(len(fragments[x.key]) for x in before):raise ValueError('Fragment denominator')
    mapping={};at=0
    for item in before:
        emitted=after[at:at+len(fragments[item.key])]
        if [x.text for x in emitted]!=fragments[item.key] or any(x.language!=item.language for x in emitted):
            raise ValueError('Fragment content/language mismatch')
        mapping[item.key]=[x.key for x in emitted]
        at+=len(emitted)
    # Collapse only the exact generated presentation fragments back into their
    # pre-transform literals. This must recover the complete translated TPL,
    # including every native command, variable, argument and original wait.
    collapsed=target
    chunks=[]
    indexed={x.key:x for x in after}
    for item in before:
        emitted=[indexed[k] for k in mapping[item.key]]
        if len(emitted)>1:
            between=target[emitted[0].end:emitted[1].start]
            if between!=SEPARATOR:raise ValueError('Unexpected inserted commands')
        chunks.append((emitted[0].start,emitted[-1].end,serialize(item.text)))
    for start,end,value in reversed(chunks):collapsed=collapsed[:start]+value+collapsed[end:]
    if skeleton(collapsed)!=skeleton(tpl):raise ValueError('Native command skeleton changed')
    if [(x.key,x.text) for x in literals(collapsed)]!=[(x.key,x.text) for x in before]:
        raise ValueError('Collapsed semantic mismatch')
    return target,mapping,dict(path=spec_path,sha256=digest,
        selected_ids=sorted(active_ids&set(selected)),extra_wait_clear_pairs=sum(len(spec['pages'][k])-1 for k in active_ids&set(selected)),
        native_commands_preserved_after_exact_collapse=True,runtime_tested=False)


def remap_layout(layout,mapping,selected_ids):
    indexed={x['id']:x for x in layout}
    records=[]
    for key in selected_ids:
        parts=[indexed[k] for k in mapping[key]]
        record=dict(parts[0],id=key)
        if len(parts)>1:
            record['pages']=[dict(fragment_id=x['id'],line_advance_pixels=x['line_advance_pixels']) for x in parts]
        records.append(record)
    return records
