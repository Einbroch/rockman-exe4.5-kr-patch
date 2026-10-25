"""Write analysis/pending500_<LAST>_v1/batch_status.json from the previous authority plus batches PREV+1..LAST.

Usage: write_batch_status_v1.py PREV LAST
Only facts from build metadata, manifests, CPU reports and coldboot comparisons; notes are passed through.
"""
import json,hashlib,sys
from pathlib import Path
from build_visibility_poc import ROOT


def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()


def main():
    prev_b,last=sys.argv[1],sys.argv[2];prev=json.loads((ROOT/f'analysis/pending500_{prev_b}_v1/batch_status.json').read_text(encoding='utf8'))
    rows=list(prev['batches']);added=0
    for n in range(int(prev_b)+1,int(last)+1):
        b=f'{n:03d}';m=json.loads((ROOT/f'poc/output/pending500_{b}_v1.json').read_text(encoding='utf8'));man=json.loads((ROOT/f'analysis/pending_insertion_500_{b}_v1/manifest.json').read_text(encoding='utf8'))
        a=ROOT/f'analysis/pending500_{b}_v1';cpu=json.loads((a/'selector_cpu_v1.json').read_text());lab=json.loads((a/'label_cpu_v1.json').read_text()) if (a/'label_cpu_v1.json').exists() else None;cmp=json.loads((a/'coldboot_compare_v1.json').read_text())
        rows.append(dict(batch=b,kind=man.get('kind','dialogue'),rom=f'poc/output/pending500_{b}_v1.gba',sha256=m['output_sha256'],integrated_IDs=m['translated_units'],new_units=man['new_units'],archives=len(man['archives']),repro_identical=sha(f'poc/output/pending500_{b}_v1_repro.gba')==m['output_sha256'],cpu_passed=cpu['passed'],label_cpu_passed=(lab or {}).get('passed'),label_max_instructions_per_call=(lab or {}).get('max_instructions_per_call'),coldboot_segments=16,coldboot_compare=dict(identical=cmp['identical'],timing_only=cmp['clock_only'],reviewed_by_eye=len(cmp['other'])),gate=man.get('gate'),redirects=m['keyitem_rom'].get('typed'+b,{}).get('redirects')))
        added+=man['new_units']
    m=json.loads((ROOT/f'poc/output/pending500_{last}_v1.json').read_text(encoding='utf8'))
    st=dict(prev,date='2026-10-24',status=f'BATCHES_041_{last}_APPLIED',current_ROM=f'poc/output/pending500_{last}_v1.gba',current_ROM_sha256=m['output_sha256'],current_ROM_bytes=m['output_bytes'],current_ROM_integrated_IDs=m['translated_units'],canonical_ROM_unapplied_draft_IDs=prev['canonical_ROM_unapplied_draft_IDs']-added,batches=rows,previous_authority=f'analysis/pending500_{prev_b}_v1/batch_status.json')
    notes=json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    st.update(notes)
    out=ROOT/f'analysis/pending500_{last}_v1/batch_status.json';out.write_text(json.dumps(st,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(st['current_ROM_integrated_IDs'],st['canonical_ROM_unapplied_draft_IDs'],out)


if __name__=='__main__':main()
