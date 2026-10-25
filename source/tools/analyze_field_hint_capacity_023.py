"""Source-bound geometry/aggregate investigation; no ROM writer or admission."""
from collections import Counter
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from tpl_literals import replace_literals
from field_hint_capacity import validate
from nickname_capacity import CPU
from survey_batch500_020_variables import applicability
from archive_scripts import script_spans
from dialogue_chip_name import construct as construct_chip_selector, INSTALL


def main():
    base='analysis/pending_insertion_500_023_b0_reuse_v1'
    selection=read(base+'/selection.json');prepared=read(base+'/prepared_inputs.json')
    cpu_path='analysis/pending_insertion_500_023_guard_v1/native_guard_cpu.json';cpu=read(cpu_path)
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,selection['source_sha256']);source=sp.read_bytes()
    rp=ROOT/selection['baseline_rom'];require_hash(rp,selection['baseline_sha256']);rom=rp.read_bytes()
    if not cpu['passed'] or cpu['baseline_sha256']!=sha(rom) or cpu['source_sha256']!=sha(source):raise ValueError('Native guard baseline')
    for r in cpu['native_code']:
        at,n=r['offset'],r['bytes']
        if sha(source[at:at+n])!=r['sha256'] or source[at:at+n]!=rom[at:at+n]:raise ValueError('Native guard applicability')
    bound=applicability(source,rom,read(CPU))
    # F900 buffer0/chip104 resolves normal name table index1, not the big-font
    # battle/library table. Bind code/table/name/metrics on the actual baseline.
    for a,b in ((0x515C0,INSTALL),(INSTALL+12,0x51660),(0x51660,0x51668),(0x765190,0x765190+2437)):
        if source[a:b]!=rom[a:b]:raise ValueError('Native chip insertion path changed')
    h=read(rp.with_suffix('.json'))['dialogue_chip_name']
    require_hash(ROOT/h['wording_asset_path'],h['wording_asset_sha256'])
    ar=dict(rom_offset=h['command_stream']-0x08000000-17,script13_offset=0,script13_prefix_hex='f6000a0c01e702f6025c6e03f604e18d92f9006801')
    generated,patches,expected=construct_chip_selector(source,rom[len(source):h['name_offset']],ar,read(h['wording_asset_path']),guts_command=h['gutsman_command_stream'])
    if (generated!=rom[len(source):h['hook_offset']+h['hook_bytes']]
            or any(rom[a:a+len(b)]!=b for a,b,_ in patches)
            or any(expected[k]!=h[k] for k in expected)):
        raise ValueError('Actual chip selector regeneration/metadata contract')
    # Only two old exact command streams select Korean; new B0 source RAM
    # or future appended clone streams cannot equal either old ROM command.
    if not all(0x08800000<=p<0x08000000+len(rom) for p in (h['command_stream'],h['gutsman_command_stream'])):
        raise ValueError('Old exact stream range')
    if struct.unpack_from('<I',source,0x51664)[0]!=0x08765190:raise ValueError('Native chip archive table')
    name=script_spans(source[0x765190:0x765190+2437],256)[104]
    if name!=bytes.fromhex('4b593d243a298202e5'):raise ValueError('Native chip104 changed')
    metrics=struct.unpack_from('<441I',source,0x5290C)
    chip_bound=sum(metrics[ch] for ch in name[:-1])
    if bound!=99 or chip_bound>88:raise ValueError('Native variable advance bounds')
    records=[];passed=Counter();failures=[]
    for row in prepared['archives']:
        require_hash(ROOT/row['path'],row['sha256']);asset=read(row['path']);arc=asset['archive']
        require_hash(ROOT/asset['source_tpl']['path'],asset['source_tpl']['sha256']);original=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
        groups=[g for g in selection['groups'] if g['archive']==arc]
        # Explicit candidate layouts already recorded by the previous survey;
        # no new prose or extra page/line controls are generated here.
        layouts={key:value for g in groups for key,value in g['individual_layouts'].items()}
        units=[dict(u,translation=layouts.get(u['id'],u['translation'])) for u in asset['units']]
        target=replace_literals(original,units)
        proofs=[]
        for g in groups:
            try:
                p=validate(original,target,[g['script']],set(g['ids']),bound,chip_bound)
                proofs.extend(p);passed[g['technical_class']]+=g['units']
            except ValueError as ex:
                failures.append(dict(archive=arc,script=g['script'],ids=g['ids'],reason=str(ex)))
        records.append(dict(archive=arc,asset=row,profiles=proofs,individual_layouts=layouts))
    out='analysis/pending_insertion_500_023_capacity_v2/survey.json'
    deps=[base+'/selection.json',base+'/prepared_inputs.json',cpu_path,CPU,'analysis/pending_insertion_500_019_variable_survey_v1/native_name_runtime.json','tools/field_hint_capacity.py','tools/analyze_field_hint_capacity_023.py','tools/nickname_capacity.py','tools/dialogue_chip_name.py']
    result=dict(schema=1,status='STATIC_AGGREGATE_SURVEY_NOT_PRODUCT_ADMISSION',source_sha256=sha(source),baseline_sha256=sha(rom),dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},selected_units=500,capacity_candidate_units=sum(passed.values()),passed_by_previous_class=dict(passed),failures=failures,archives=records,native_nickname_bound=bound,native_chip104_bound=chip_bound,native_chip104_hex=name.hex(),guards_actual_cpu_vectors=sum(cpu['case_counts'].values()),rom_written=False,insertion_ready=False,release_eligible=False,limits='Current selected500 explicit full-box candidate layouts only. Native nickname applicability and chip104 original normal-name lookup remain bound to actual022; automatic Hangul names are NOT supported. Guard CPU evidence is separate from whole-prefix/source-selected-branch and GBA runtime. This survey has not registered any new product writer or B0 selector.')
    frozen_write(ROOT/out,result)
    print('capacity candidates',result['capacity_candidate_units'],'/500; nickname',bound,'chip104',chip_bound,'failures',len(failures))
    for f in failures:print(f)


if __name__=='__main__':main()
