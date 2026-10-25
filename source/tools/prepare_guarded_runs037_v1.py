"""Add loaded037 sentinels without changing existing runtime tools."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from prepare_native_product037_v1 import create


def main():
    records=[]
    for name in ['run_normal037_v1.py','run_qualified_native037_v1.py']:
        base='tools/'+name;new='tools/'+name.replace('_v1.py','_v2.py');text=(ROOT/base).read_text(encoding='utf8')
        edits=[('from cumulative_batch500 import read', 'from native037_loaded_guards import arguments as loaded_guards\nfrom cumulative_batch500 import read',1)]
        if name.startswith('run_normal'):
            edits.append(("        if parent:cmd+=", "        cmd+=loaded_guards(rom,m)\n        if parent:cmd+=",1))
        else:
            edits.append(('    subprocess.run(cmd,cwd=ROOT,check=True)','    cmd+=loaded_guards(rom,m)\n    subprocess.run(cmd,cwd=ROOT,check=True)',1))
        records.append(create(new,base,text,edits))
    frozen_write(ROOT/'tools/specs/guarded_runs037_v1_version.json',dict(generator_sha256=sha((ROOT/'tools/prepare_guarded_runs037_v1.py').read_bytes()),changes=records,scope='Actual Mesen loaded-ROM header/stub/wrapper/typed70 descriptor sentinels added to each own037 run; not full loaded-ROM hashing'))
    print('PASS037 loaded-memory guarded runtime invocations prepared')


if __name__=='__main__':main()
