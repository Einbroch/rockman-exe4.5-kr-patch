"""Bench-only compiled sizes/round trips; never patches a ROM or asserts capacity."""
import json
from build_visibility_poc import ROOT, run_textpet, sha, require_hash
from textpet_korean import prepare_plugins,command
from prepare_keyitem_translation_draft import prepare
from tpl_literals import literals,replace_literals,skeleton
from verify_tpi_index import lz77_decompress
from lz10_literals import encode,decode

def main():
    out=ROOT/'analysis/keyitem_translation_draft_v1/bench'
    if out.exists():raise ValueError('preserve keyitem bench evidence')
    out.mkdir()
    prepare_plugins(out/'plugins')
    common=command(out/'plugins')
    asset,full=prepare()
    original=(ROOT/'analysis/full_scope_v1/source_tpl/709408.tpl').read_text(encoding='utf-8-sig')
    source_path=ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba'
    require_hash(source_path,'588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8')
    source,_=lz77_decompress(source_path.read_bytes(),0x709408)
    empty=replace_literals(original,[u for u in asset['units']if u['id']=='709408:32:0'])
    results={}
    for name,tpl in [('source',original),('empty-only',empty),('full-draft',full)]:
        directory=out/name;directory.mkdir()
        inp=directory/'709408.tpl';inp.write_text(tpl,encoding='utf8')
        binary=directory/'709408.msg';reverse=directory/'reverse.tpl';rebuilt=directory/'rebuilt.msg'
        run_textpet(common+['Read-Text-Archives',str(inp),'--format','tpl','Write-Text-Archives',str(binary),'--format','bin'],directory/'compile.log')
        payload=binary.read_bytes()
        if name=='source' and payload!=source:raise ValueError('source binary roundtrip')
        run_textpet(common+['Read-Text-Archives',str(binary),'--format','bin','Write-Text-Archives',str(reverse),'--format','tpl'],directory/'reverse.log')
        back=reverse.read_text(encoding='utf-8-sig')
        if [(x.key,x.text)for x in literals(tpl)]!=[(x.key,x.text)for x in literals(back)] or skeleton(tpl)!=skeleton(back):
            raise ValueError('keyitem bench semantic roundtrip')
        run_textpet(common+['Read-Text-Archives',str(reverse),'--format','tpl','Write-Text-Archives',str(rebuilt),'--format','bin'],directory/'rebuild.log')
        if rebuilt.read_bytes()!=payload:raise ValueError('keyitem binary roundtrip')
        # A format-limit check, NOT an inferred runtime capacity.
        stored=encode(payload,limit=0xFFFFFF)
        independent,_=lz77_decompress(stored,0)
        if decode(stored,limit=0xFFFFFF)!=payload or independent!=payload:raise ValueError('bench compression roundtrip')
        results[name]=dict(payload_bytes=len(payload),growth_bytes=len(payload)-len(source),
            sha256=sha(payload),literal_only_stored_bytes=len(stored),
            semantic_roundtrip=True,binary_roundtrip=True,
            compression_self_and_independent_roundtrip=True,
            target_consumer_compatibility='NOT TESTED')
    report=dict(bench_only=True,rom_modified=False,release_eligible=False,
        warning='No runtime buffer capacity inferred from codec limit or bench success.',cases=results)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report))

if __name__=='__main__':main()
