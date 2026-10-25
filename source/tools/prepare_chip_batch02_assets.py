"""Compose explicit new drafts without transforming existing translated prose.

Print artifact JSON to stdout; installation uses apply_patch, not this tool.
"""
import copy
import json
import re
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require
from tpl_literals import literals,resolve_units
from archive_scripts import script_spans


def prepare():
    seed_path=ROOT/'translations/chip_batch02_draft_seed.json';seed=read(seed_path)
    require(seed['policy']=='development-draft; NON-DISTRIBUTION' and seed['review']=='needs_review','seed policy')
    entries=seed['entries'];require([e['script'] for e in entries]==list(range(31,61)),'seed exact ordered denominator')
    names=copy.deepcopy(read(ROOT/'translations/library_chip_names_batch01_ko.json'))
    desc=copy.deepcopy(read(ROOT/'translations/chip_descriptions_batch01_ko.json'))
    original_names=resolve_units(names);original_desc=resolve_units(desc)
    project=read(ROOT/'project.json');source_path=ROOT/project['source_profile']['filename'];require_hash(source_path,names['source_sha256']);native=source_path.read_bytes()
    require(desc['source_sha256']==names['source_sha256'],'asset ROM identity')
    source_names={l.key:l.text for l in literals((ROOT/'analysis/tpl_baseline/765190.tpl').read_text(encoding='utf-8-sig'))}
    source_desc={l.key:l.text for l in literals((ROOT/'analysis/tpl_baseline/76937C.tpl').read_text(encoding='utf-8-sig'))}
    spans=script_spans(native[0x765190:0x765190+2437],256)
    reference_path=ROOT/'../록맨 에그제 3/translations/chip_names_ko.json';require_hash(reference_path,'f2b4625131f08d4844fdcf7fbe38ef87d7ebea29b6bfe8d17398e3428ca1a4ae');reference=read(reference_path);matches=[]
    for e in entries:
        i=e['script'];nk=f'765190:{i}:0';dk=f'76937C:{i}:0';name=e['name'];sentence=e['description']
        require(1<=len(name)<=8 and all(1<=len(line)<=9 for line in sentence.split('\n')),'draft cell overflow')
        require(source_desc[dk].count('\n')==sentence.count('\n') and len(sentence.split('\n'))<=3,'draft source line count changed')
        for source,target in ((source_names[nk],name),(source_desc[dk],sentence)):
            require(re.findall(r'\d+',source)==re.findall(r'\d+',target),'draft numeral identity changed')
        if source_names[nk] in reference:
            require(name==reference[source_names[nk]],'EXE3 exact common candidate changed without explicit note')
            matches.append({'script':i,'source':source_names[nk],'candidate':name,'approval':'needs_review'})
        nw=f'library.chip.batch02.{i}';dw=f'desc.batch02.{i}'
        names['wordings'].append({'id':nw,'translation':name,'state':'needs_review'})
        names['units'].append({'id':nk,'source':source_names[nk],'wording_id':nw});names['source_script_hex'][str(i)]=spans[i].hex()
        desc['wordings'].append({'id':dw,'translation':sentence,'state':'needs_review'})
        desc['units'].append({'id':dk,'source':source_desc[dk],'wording_id':dw})
    require(resolve_units(names)[:30]==original_names and resolve_units(desc)[:30]==original_desc,'batch01 prose/source/state changed')
    names['context']='First60 source chip-name scripts, guarded library/folder eight-cell clones. Battle names and other consumers remain native. Draft only.'
    names['protected_policy']='Keep all196 unselected scripts, source pool and shared pointers, terminal E5 and numeral identities. First30 prior draft units preserved verbatim.'
    names['reference']['sha256']=sha(reference_path.read_bytes());names['reference']['batch02_exact_common_candidates']=matches
    desc['scope_variant']='mono-descriptions-batch02'
    desc['context']='First60 description scripts, at most9 visible cells and3 source-matched rows. Prior30 drafts remain verbatim. New60-scope exact-ROM runtime required.'
    desc['protected_policy']='Keep source controls, numeric sequences and source line counts, plus196 unselected script bytes. Existing first30 units preserved verbatim.'
    desc['terminology_review']+=seed['terminology_review']
    for artifact in (names,desc): artifact['composition']={'seed_path':str(seed_path.relative_to(ROOT)),'seed_sha256':sha(seed_path.read_bytes()),'tool_path':'tools/prepare_chip_batch02_assets.py','tool_sha256':sha((ROOT/'tools/prepare_chip_batch02_assets.py').read_bytes()),'policy':'explicit added drafts; no prior translation rewriting','new_units':30,'prior_units_preserved':30}
    return {'names':names,'descriptions':desc}


if __name__=='__main__': print(json.dumps(prepare(),ensure_ascii=False,indent=2))
