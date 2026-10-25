"""Compile the65-unit correction subset from source, not a500/product build."""
import re
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from textpet_korean import prepare_plugins,command
from verify_tpi_index import parse_tpi
from build_development_patch import compile_archive
from korean_codec import EXTRA_CHARACTER_INDICES

INPUT='analysis/pending_insertion_500_020_wording_v1/report.json'
OUT='analysis/pending_insertion_500_020_wording_preflight_v1'

def main():
    report=read(INPUT);cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();require_hash(ROOT/report['baseline_rom'],report['baseline_sha256']);require_hash(ROOT/report['decisions']['path'],report['decisions']['sha256'])
    rows={f"{r['offset']:06X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])};require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);out=ROOT/OUT
    if out.exists():raise ValueError('Preserve preflight attempt')
    items=[];extras=set()
    for item in report['assets']:
        require_hash(ROOT/item['path'],item['sha256']);a=read(item['path']);row=rows[item['archive']]
        if row['compressed'] or row['size_header'] or not row['pointers'] or row['pointers']==[0]:raise ValueError('Raw source scope')
        tpl=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');require_hash(ROOT/a['source_tpl']['path'],a['source_tpl']['sha256']);count=int(re.search(r'^@size\s+(\d+)',tpl,re.M).group(1))
        scope=dict(consumer='normal-dialogue',literal_language='mmbn45',complete_literal_scope=False,literal_scripts=item['scripts'],literal_ids=item['selected_ids'],script_count=count,max_literal_rows=3,max_line_advance=132,max_compiled_bytes=65535,preserve_literal_numerals=True,nickname_capacity_profiles=item['nickname_capacity_profiles'])
        extras.update(c for u in a['units'] for c in u['translation'] if c in EXTRA_CHARACTER_INDICES);items.append((item,a,row,scope))
    out.mkdir();plugins=out/'plugins';prepare_plugins(plugins,extras);common=command(plugins);results=[]
    for item,a,row,scope in items:
        raw,proof=compile_archive(source,row,a,scope,common,plugins,out/a['archive']);results.append(dict(archive=a['archive'],asset_path=item['path'],asset_sha256=item['sha256'],selected_ids=item['selected_ids'],selected_units=len(a['units']),compiled_bytes=len(raw),compiled_sha256=sha(raw),proof=proof));print('Correction preflight',a['archive'],len(a['units']),'PASS',flush=True)
    if sum(r['selected_units'] for r in results)!=report['selected_script_units']:raise ValueError('Correction denominator')
    frozen_write(out/'preflight.json',dict(schema=1,policy='development-draft; NON-DISTRIBUTION',input=dict(path=INPUT,sha256=sha((ROOT/INPUT).read_bytes())),source_sha256=sha(source),baseline_rom=report['baseline_rom'],baseline_sha256=report['baseline_sha256'],individual_wording_changes=report['individual_wording_changes'],selected_script_units=sum(r['selected_units'] for r in results),archives=results,rom_written=False,runtime_tested=False,release_eligible=False,limits='Source-only correction subset, not500. Binary/control/unselected-script/semantic roundtrips only. Cumulative carry/single writer/product build/runtime/human review pending.'))
    print('PASS correction subset source-only compile; no ROM write')

if __name__=='__main__':main()
