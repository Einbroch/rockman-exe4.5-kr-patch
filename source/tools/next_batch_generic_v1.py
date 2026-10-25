"""Orchestrate one generic500 batch N over predecessor P: prepare, component, generated primary, builds, checks.

Usage: python -X utf8 tools/next_batch_generic_v1.py N [prepare component build check]
P = N-1 and must already be built. Never overwrites existing outputs.
"""
import sys,json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PY=[sys.executable,'-X','utf8']


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def names(b):
    if b=='041':return dict(mod='typed_rom_product041_v1',file='tools/build_development_patch_041_v1.py',rom='poc/output/pending500_041_v1.gba')
    return dict(mod=f'typed_rom_batch{b}_v1',file=f'tools/build_development_patch_{b}_v1.py',rom=f'poc/output/pending500_{b}_v1.gba')


def generate(n,p):
    pp=str(int(p)-1).zfill(3);P=names(p);N=names(n)
    changes=[
     (f"    from {P['mod']} import load_inputs as load_inputs{p},install as install_typed{p},finalize as finalize{p},predecessor_view as predecessor_view{p}",
      f"    from {P['mod']} import load_inputs as load_inputs{p},install as install_typed{p},finalize as finalize{p},predecessor_view as predecessor_view{p}\n    from {N['mod']} import load_inputs as load_inputs{n},install as install_typed{n},finalize as finalize{n},predecessor_view as predecessor_view{n}"),
     (f"    inputs{p}=load_inputs{p}(source)",f"    inputs{p}=load_inputs{p}(source)\n    inputs{n}=load_inputs{n}(source)"),
     (f"    for entry{p},*_ in inputs{p}:",f"    for entry{n},*_ in inputs{n}:\n        asset{n}=read_json(ROOT/entry{n}['asset']['path'])\n        needed.update(ch for u in asset{n}['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)\n    for entry{p},*_ in inputs{p}:"),
     (f"        appended,key_patches,keyitem_rom,typed_records{p}=install_typed{p}(source,appended,key_patches,keyitem_rom,inputs{p},common,work/'plugins',work/'typed{p}')",
      f"        appended,key_patches,keyitem_rom,typed_records{p}=install_typed{p}(source,appended,key_patches,keyitem_rom,inputs{p},common,work/'plugins',work/'typed{p}')\n        appended,key_patches,keyitem_rom,typed_records{n}=install_typed{n}(source,appended,key_patches,keyitem_rom,inputs{n},common,work/'plugins',work/'typed{n}')"),
     (f"        from {P['mod']} import verify_final",f"        from {N['mod']} import verify_final"),
     (f"    parent{pp}=predecessor_view{p}(source,target,result['keyitem_rom'])",f"    parent{p}=predecessor_view{n}(source,target,result['keyitem_rom'])\n    parent{pp}=predecessor_view{p}(source,parent{p},result['keyitem_rom'])"),
     (f"    finalize{p}(source,target,result,inputs{p},typed_records{p})",f"    finalize{p}(source,parent{p},result,inputs{p},typed_records{p})\n    finalize{n}(source,target,result,inputs{n},typed_records{n})"),
    ]
    if n=='056':
        # First label batch: the 034..036 finalizers compare the whole source extent except 4FB4C, so they
        # get a view with the label-renderer stub sites restored to source bytes.
        changes.append(("    finalize034(source,target,result,","    nolabel=bytearray(target)\n    for _site,_spec in __import__('batch_label_v1').SITES.items():nolabel[_site:_site+_spec['size']]=source[_site:_site+_spec['size']]\n    nolabel=bytes(nolabel)\n    finalize034(source,nolabel,result,"))
        changes.append(("    finalize035(source,target,result,inputs035,npc_records035)","    finalize035(source,nolabel,result,inputs035,npc_records035)"))
        changes.append(("    finalize036(source,target,result,inputs036,npc_records036)","    finalize036(source,nolabel,result,inputs036,npc_records036)"))
    if n=='061':
        # First redirect batch: the component (batch_label_v3) owns the redirected pointer words.
        changes.append(("            patches.append((pointer, (0x08000000 + products[row[\"offset\"]][0]).to_bytes(4, \"little\"),","            if pointer in __import__('batch_label_v3').REDIRECT_POINTERS:continue\n            patches.append((pointer, (0x08000000 + products[row[\"offset\"]][0]).to_bytes(4, \"little\"),"))
        changes.append(("                if at != dest or target[at:at + len(stored)] != stored:","                if (at != dest and pointer not in __import__('batch_label_v3').REDIRECT_POINTERS) or target[dest:dest + len(stored)] != stored:"))
        changes.append(("    nolabel=bytes(nolabel)\n","    nolabel=bytearray(nolabel)\n    for _v in result['keyitem_rom'].values():\n        for _r in (_v.get('redirects',[]) if isinstance(_v,dict) else []):nolabel[_r['offset']:_r['offset']+4]=bytes.fromhex(_r['base_hex'])\n    nolabel=bytes(nolabel)\n"))
    if n=='065':
        # First v4 batch: unmodified catalog rows may now have redirected pointer words (63720C, 778B08).
        changes.append(("                if source[pointer:pointer + 4] != target[pointer:pointer + 4]:","                if source[pointer:pointer + 4] != target[pointer:pointer + 4] and pointer not in __import__('batch_label_v3').REDIRECT_POINTERS:"))
    text=(ROOT/P['file']).read_text(encoding='utf8')
    for a,b in changes:
        if text.count(a)!=1:raise SystemExit('anchor missing: '+a[:80])
        text=text.replace(a,b)
    out=ROOT/N['file']
    if out.exists() and out.read_text(encoding='utf8')!=text:raise SystemExit('Preserve existing '+N['file'])
    out.write_text(text,encoding='utf8',newline='\n')
    spec=dict(base=P['file'],base_sha256=sha(ROOT/P['file']),output=N['file'],output_sha256=sha(out),changes=changes,component=dict(path=f"tools/{N['mod']}.py",sha256=sha(ROOT/f"tools/{N['mod']}.py")))
    (ROOT/f'tools/specs/primary{n}_v1_version.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')


COMPONENT='''"""Generic500 batch{n} component over {rom} (see batch_generic_v1)."""
from {cls_mod} import {cls} as Component
_c=Component('{n}','{rom}','{sha}','analysis/pending_insertion_500_{n}_v1/manifest.json','{mod}','typed{p}')
load_inputs=_c.load_inputs;install=_c.install;predecessor_view=_c.predecessor_view;verify_final=_c.verify_final;finalize=_c.finalize
'''


def main():
    n=sys.argv[1];p=str(int(n)-1).zfill(3);P=names(p);N=names(n);steps=sys.argv[2:] or ['prepare','component','build','check']
    pm=json.loads((ROOT/P['rom'].replace('.gba','.json')).read_text(encoding='utf8'))
    if 'prepare' in steps and not (ROOT/f'analysis/pending_insertion_500_{n}_v1/manifest.json').exists():
        subprocess.run(PY+['-c',f"import sys;sys.path.insert(0,'tools');from batch_generic_v1 import prepare;prepare('{n}','{P['rom']}','poc/work/pending500_041_v1/plugins',gate='{'generic_page_gate054_v1' if int(n)>=54 else 'generic_page_gate043_v1'}',kind='{'label' if int(n)>=56 else 'dialogue'}',redirect_ok={('778A4C','76C944') if int(n)>=62 else ('778A4C',) if int(n)>=61 else ()})"],cwd=ROOT,check=True)
    if 'component' in steps:
        mod=ROOT/f"tools/{N['mod']}.py";body=COMPONENT.format(n=n,p=p,rom=P['rom'],sha=pm['output_sha256'],mod=P['mod'],cls_mod=('batch_label_v4' if int(n)>=65 else 'batch_label_v3' if int(n)>=61 else 'batch_label_v2' if int(n)>=57 else 'batch_label_v1' if int(n)>=56 else 'batch_generic_v1'),cls=('FixLabelComponent' if int(n)>=65 else 'RedirectLabelComponent' if int(n)>=61 else 'FastLabelComponent' if int(n)>=57 else 'LabelComponent' if int(n)>=56 else 'Component'))
        if mod.exists() and mod.read_text(encoding='utf8')!=body:raise SystemExit('Preserve '+str(mod))
        mod.write_text(body,encoding='utf8');generate(n,p);print('GENERATED',n,flush=True)
    if 'build' in steps:
        old=pm['build_argument_manifest'];args=json.loads((ROOT/old['path']).read_text(encoding='utf8'))['args'];procs=[]
        for stem in (f'pending500_{n}_v1',f'pending500_{n}_v1_repro'):
            if any((ROOT/x).exists() for x in ['poc/work/'+stem,'poc/output/'+stem+'.gba']):raise SystemExit('Preserve '+stem)
            a=list(args);a[a.index('--work')+1]='poc/work/'+stem;a[a.index('--out')+1]='poc/output/'+stem+'.gba'
            path=ROOT/'poc/build_arguments'/(stem+'.json');data=(json.dumps(dict(schema=1,args=a),ensure_ascii=False,indent=2)+'\n').encode('utf8');path.write_bytes(data)
            log=open(ROOT/'poc/output'/(stem+'.log'),'w',encoding='utf8')
            procs.append(subprocess.Popen(PY+[N['file'],'--argument-file',str(path.relative_to(ROOT)),'--argument-file-sha256',hashlib.sha256(data).hexdigest()],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT))
        codes=[x.wait() for x in procs]
        if any(codes):raise SystemExit(f'build failed {codes}; see poc/output/pending500_{n}_v1*.log')
        if sha(ROOT/N['rom'])!=sha(ROOT/N['rom'].replace('.gba','_repro.gba')):raise SystemExit('repro differs')
        print('BUILT',n,sha(ROOT/N['rom']),flush=True)
    if 'check' in steps:
        (ROOT/f'analysis/pending500_{n}_v1').mkdir(parents=True,exist_ok=True)
        subprocess.run(PY+['tools/bench_generic_v1.py',N['rom'],'--key','typed'+n,'--out',f'analysis/pending500_{n}_v1/selector_cpu_v1.json'],cwd=ROOT,check=True)
        if int(n)>=56:subprocess.run(PY+['tools/'+('bench_label_v2.py' if int(n)>=57 else 'bench_label_v1.py'),N['rom'],'typed'+n,'--out',f'analysis/pending500_{n}_v1/label_cpu_v1.json'],cwd=ROOT,check=True)
        subprocess.run(PY+['tools/run_normal_generic_v1.py',N['rom'],n],cwd=ROOT,check=True)
        print('CHECKED',n,flush=True)


if __name__=='__main__':main()
