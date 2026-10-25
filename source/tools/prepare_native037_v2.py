"""Mechanical version bump: exclude unrelated callers before scene pointer read."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    reg=read('analysis/pending_insertion_500_037_native_inputs_v1/manifest.json')
    cpu=read('analysis/pending_insertion_500_037_selector_cpu_v1/cpu.json')
    changes={
      'tools/field_native_rom_selector_037_v1.py':[
        ("code = '''pop {r3}\npush {r0,r1,r2,r3,r4,r5,r6,r7}\nmov r2,r10", "code = '''pop {r3}\npush {r0,r1,r2,r3,r4,r5,r6,r7}\nmov r2,lr\nldr r3,npc_caller\ncmp r2,r3\nbne board_gate\nldr r3,npc_root\ncmp r0,r3\nbne fallback\nb script_gate\nboard_gate:\nldr r3,board_caller\ncmp r2,r3\nbne fallback\nldr r3,board_root\ncmp r0,r3\nbne fallback\nscript_gate:\nlsrs r2,r1,#8\nbne fallback\nmov r2,r10"),
        ("dict(descriptors=table, previous=previous_entry|1)","dict(descriptors=table, previous=previous_entry|1, npc_caller=abi['native-NPC']['caller_lr'], npc_root=abi['native-NPC']['root'], board_caller=abi['field-board']['caller_lr'], board_root=abi['field-board']['root'])"),
      ],
      'tools/bench_native_selector037_v1.py':[
        ('field_native_rom_selector_037_v1','field_native_rom_selector_037_v2'),
        ('bench_native_selector037_v1','bench_native_selector037_v2'),
        ('pending_insertion_500_037_selector_cpu_v1','pending_insertion_500_037_selector_cpu_v2'),
        ('blob=None,sub=0,day=2):','blob=None,sub=0,day=2,scene_ready=True):'),
        ("u.mem_write(glob+64,struct.pack('<I',0x02000200))","u.mem_write(glob+64,struct.pack('<I',0x02000200 if scene_ready else 0))"),
        ("for kind,kw in cases:", "cases += [('uninitialized-scene-unrelated-caller',dict(caller=0x0804F785,scene_ready=False)),('uninitialized-scene-wrong-root',dict(root=0x02038000,scene_ready=False)),('uninitialized-scene-invalid-script',dict(script=256,scene_ready=False))]\n        for kind,kw in cases:"),
      ],
      'tools/prepare_native_inputs037_v1.py':[
        ('field_native_rom_selector_037_v1','field_native_rom_selector_037_v2'),
        ('prepare_native_inputs037_v1','prepare_native_inputs037_v2'),
        ('pending_insertion_500_037_native_inputs_v1','pending_insertion_500_037_native_inputs_v2'),
        ('pending_insertion_500_037_selector_cpu_v1','pending_insertion_500_037_selector_cpu_v2'),
      ],
    }
    oldhash=dict(reg['dependencies']);oldhash.update({r['path'].replace('\\','/'):r['sha256'] for r in cpu['tools']}); records=[]
    for name,edits in changes.items():
        require_hash(ROOT/name,oldhash[name]); original=(ROOT/name).read_text(encoding='utf8'); text=original
        for a,b in edits:
            expected=2 if a == 'field_native_rom_selector_037_v1' else 1
            # Import plus explicit tool-dependency reference occur twice.
            if text.count(a)!=expected: raise ValueError((name,a,text.count(a),expected))
            text=text.replace(a,b)
        output=name.replace('_v1.py','_v2.py'); path=ROOT/output
        if path.exists() and path.read_text(encoding='utf8')!=text: raise ValueError('Preserve existing v2')
        if not path.exists(): path.write_text(text,encoding='utf8',newline='\n')
        records.append(dict(base=name,base_sha256=sha((ROOT/name).read_bytes()),output=output,output_sha256=sha(path.read_bytes()),edits=[dict(before=a,after=b) for a,b in edits]))
    frozen_write(ROOT/'tools/specs/native037_v2_version.json',dict(generator_sha256=sha((ROOT/'tools/prepare_native037_v2.py').read_bytes()),changes=records,scope='Pre-scene caller/root/unsigned8-bit guards; CPU rejects unrelated and invalid inputs without dereferencing unavailable scene'))
    print('PASS037 typed selector v2 versioned; prior v1 preserved')


if __name__=='__main__': main()
