"""Final immutable-source/current tools/rebuild/runtime identity audit."""
import ast,json
from build_visibility_poc import ROOT,sha,require_hash
from report_keyitem_full_rom import STEM,static

def main():
    m=json.loads((ROOT/f'poc/output/{STEM}_current_repro_r2.json').read_text(encoding='utf8'));outputs={}
    for suffix in ['', '_repro','_current_repro','_current_repro_r2']:
        p=ROOT/f'poc/output/{STEM}{suffix}.gba';require_hash(p,m['output_sha256']);outputs[p.name]=sha(p.read_bytes())
    proof=static()[-1];tools={p.name:sha(p.read_bytes())for p in (ROOT/'tools').glob('*.py')}
    drift=sorted(set(tools)^set(m['build_tools_sha256'])|{k for k in tools.keys()&m['build_tools_sha256'].keys()if tools[k]!=m['build_tools_sha256'][k]})
    if drift:raise ValueError('final tool drift '+str(drift))
    for p in (ROOT/'tools').glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
    reports={}
    for name in ['static.json','runtime.json','selector_runtime.json','renderer_matrix.json','statistics_runtime.json']:
        p=ROOT/'analysis/keyitem_full_rom_v1'/name;r=json.loads(p.read_text(encoding='utf8'))
        if not r['passed']or r['rom_sha256']!=m['output_sha256']:raise ValueError('exact runtime report identity '+name)
        reports[name]=sha(p.read_bytes())
    cpu=ROOT/'analysis/keyitem_full_rom_v1/cpu/report.json';r=json.loads(cpu.read_text())
    if not r['passed']or not r['integrated_artifact_final_bytes_checked']or r['baseline_rom_sha256']!=m['output_sha256']:raise ValueError('final CPU evidence')
    result=dict(passed=True,rom_sha256=m['output_sha256'],outputs=outputs,tool_count=len(tools),tool_drift=drift,python_AST=True,
        product_static_proof=proof,runtime_reports=reports,cpu_report_sha256=sha(cpu.read_bytes()),release_eligible=False,
        limits=['Other02031000 normal route/fallback not observed; CPU is not GBA proof.','Renderer matrix uses documented read aliases, not normal acquisition.','Whole project/Hangul input and persistence/old-save compatibility/human review unfinished.'])
    out=ROOT/'analysis/keyitem_full_rom_v1/final_identity.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Final four-build/tool/source/write/input/runtime identity PASS',len(tools))
if __name__=='__main__':main()
