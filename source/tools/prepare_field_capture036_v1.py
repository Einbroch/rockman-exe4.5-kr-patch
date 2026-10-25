"""Mechanical version expansion of the verified read-only035 observation probe."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import frozen_write

def main():
    base=ROOT/'tools/capture_field_loader_035_v7.py';require_hash(base,'66161087717149a36eb9291cd4b05df55041ab3bfef446685065c4a1f78d2f5b');text=base.read_text(encoding='utf8');dest=ROOT/'tools/capture_field_loader_036_v1.py'
    if dest.exists():raise ValueError('preserve generated capture')
    if text.count("npc=m['keyitem_rom']['npc035']")!=1:raise ValueError('036 metadata hook anchor')
    # Identical observation contracts; only current selector/glyph-placement
    # metadata and explanatory version labels change. No gameplay writes.
    count=text.count('035');new=text.replace('035','036');dest.write_text(new,encoding='utf8')
    frozen_write(ROOT/'tools/specs/field_capture036_v1_version.json',dict(base=str(base.relative_to(ROOT)),base_sha256=sha(base.read_bytes()),replacement=['035','036'],occurrences=count,output=str(dest.relative_to(ROOT)),output_sha256=sha(dest.read_bytes()),scope='Read-only current036 selector entry/exit, source loads, actor entries, new clone glyph consumption; no aliases'))
    print('Generated read-only036 capture',count,'mechanical version replacements')

if __name__=='__main__':main()
