"""Mechanical selection refinement to two source-proven field consumer classes.

Preserves the first500 preparation and unresolved reward evidence. Chooses a
different exact500 canonical subset, without changing any translated wording.
"""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    base=ROOT/'tools/prepare_source500_037_v1.py';s=read('analysis/pending_insertion_500_037_source_only_v1/selection.json');require_hash(base,s['dependencies']['tools/prepare_source500_037_v1.py']);text=base.read_text(encoding='utf8');dest=ROOT/'tools/prepare_source500_037_v2.py'
    if dest.exists():raise ValueError('Preserve source preparation version')
    helper='''def board_lookup(source):
    out=defaultdict(list)
    for scene in (0xA0,0xA1,0xA2,0xA3):
        top=0x537CC+(scene-0x80)*4;table=struct.unpack_from('<I',source,top)[0]-0x08000000
        need(0<=table<=len(source)-16,'037 board subtable range')
        for sub in range(4):
            at=table+sub*4;off=struct.unpack_from('<I',source,at)[0]-0x08000000
            need(0<=off<len(source) and source[off]==0x10,'037 board native compressed source')
            payload,_=lz77_decompress(source,off)
            out[f'{off:X}'].append(dict(scene=scene,sub=sub,pointer=at,root=0x0203C800,native_bytes=len(payload)))
    return out

'''
    changes=[("OUT='analysis/pending_insertion_500_037_source_only_v1'","OUT='analysis/pending_insertion_500_037_source_only_v2'"),('def select():',helper+'def select():'),('lookup=native_lookup(source)','lookup=native_lookup(source);boards=board_lookup(source)'),("and g['profile'] in ('normal-pages','normal-horizontal')]","and g['profile'] in ('normal-pages','normal-horizontal') and (g['archive'] in lookup or g['archive'] in boards)]"),("g['source_native_lookup_candidates']=lookup.get(arc,[])","g['source_native_lookup_candidates']=lookup.get(arc,[]);g['source_board_lookup_candidates']=boards.get(arc,[])"),('other_compressed_loader_unestablished_units=other_units','field_board_lookup_classified_units=other_units'),('other loader unestablished','board lookup'),('tools/prepare_source500_037_v1.py','tools/prepare_source500_037_v2.py'),("deps+=['tools/'+fn.__module__+'.py' for _,fn in VALIDATORS]","deps+=['analysis/pending_insertion_500_037_source_only_v1/selection.json','tools/specs/source037_v2_version.json'];deps+=['tools/'+fn.__module__+'.py' for _,fn in VALIDATORS]"),('wording_changed=False','supersedes_source_only_selection=ref(ROOT/\'analysis/pending_insertion_500_037_source_only_v1/selection.json\'),candidate_policy=\'Only original native-NPC and field-board source lookup classes; no reward/tournament/A4 hint targets\',wording_changed=False'),('A2/static lookup and additional compressed loader classes require boundary/admission evidence before any037 ROM build.','A2 and field-board root0203C800/caller/consumer boundaries require admission and exact-ROM verification before any037 ROM build.')]
    for old,new in changes:
        if text.count(old)!=1:raise ValueError('Source037 v2 exact mechanical anchor '+old)
        text=text.replace(old,new,1)
    dest.write_text(text,encoding='utf8');frozen_write(ROOT/'tools/specs/source037_v2_version.json',dict(base=str(base.relative_to(ROOT)),base_sha256=sha(base.read_bytes()),changes=changes,output=str(dest.relative_to(ROOT)),output_sha256=sha(dest.read_bytes()),scope='Selection/ref classification refinement, not wording transformation or ROM writer'))
    print('Generated037v2 preparation for only two source-proven field classes')

if __name__=='__main__':main()
