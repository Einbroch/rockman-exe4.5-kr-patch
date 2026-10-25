"""Actual311-unit helper ABI differential; no old-ROM delta claim."""
import json
from pathlib import Path
import verify_battle_name_build as previous
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require


def main():
    rom=ROOT/'poc/output/exe45_ko_development_chip_batch04_v1.gba'
    m=read(rom.with_suffix('.json'));build=m['output_sha256'];require_hash(rom,build)
    require_hash(ROOT/'poc/output/exe45_ko_development_chip_batch04_v1_repro.gba',build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256'])
    native=source.read_bytes();blob=rom.read_bytes();ext=m['chip_battle_name_extension'];ids=set(ext['selected_scripts'])
    require(ids==set(range(1,121)) and m['translated_units']==311,'scope')
    require(all(p['final_placement_roundtrip'] for p in ext['machine_code']),'placement verification')
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    require_hash(ROOT/'external/arm_bench_python/unicorn/unicorn_py3/unicorn.py','b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb')
    require(previous.__version__=='2.1.4','CPU engine drift')
    code=Path(previous.__file__).read_text(encoding='utf-8')
    start='    engines=[];stop=[0]\n';end="    out=ROOT/'analysis/exe45_battle_names_build_cpu_v1.json'"
    require(code.count(start)==code.count(end)==1,'CPU body anchors')
    body=code[code.index(start):code.index(end)]
    import textwrap
    ns=dict(vars(previous));ns.update(native=native,blob=blob,ext=ext,ids=ids)
    exec(compile(textwrap.dedent(body),previous.__file__+' [actual120-scope CPU body]','exec'),ns)
    out=ROOT/'analysis/exe45_chip_batch04_battle_helper_cpu_v1_r2.json';require(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps({'status':'PASS actual120-scope helper native differential','rom_sha256':build,'vectors':ns['vectors'],'selected_vectors':ns['selected'],'source_sha256':m['source_sha256'],'scope':sorted(ids),'registers_flags_stack_match':True,'tool_sha256':sha(Path(__file__).read_bytes()),'limits':['CPU fixture only, no runtime battle120 reachability claim','No unchanged-prefix delta claim against prior251-unit build']},indent=2),encoding='utf-8')
    print('PASS actual120-scope helper:',ns['vectors'],'native differential vectors')


if __name__=='__main__':main()
