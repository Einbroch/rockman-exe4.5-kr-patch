"""Same independent mechanical checks at90 units; previous60 untouched."""
from pathlib import Path
import test_chip_batch02 as previous

code=Path(previous.__file__).read_text(encoding='utf-8')
for old,new in {
    'prepare_chip_batch02_assets':'prepare_chip_batch03_assets',
    'Batch02Tests':'Batch03Tests',
    "batch01_ko.json":"batch02_ko.json",
    "batch02_ko.json'))":"batch03_ko.json'))",
    "batch02_ko.json');units":"batch03_ko.json');units",
    "batch02_ko.json'),table":"batch03_ko.json'),table",
    'new[:30]':'new[:60]', 'len(new),60':'len(new),90',
    'range(1,61)':'range(1,91)', 'len(layout),60':'len(layout),90',
    "len(report['units']),60":"len(report['units']),90",
    "len(report['unselected_scripts']),196":"len(report['unselected_scripts']),166",
}.items():
    if old not in code: raise ValueError('missing test binding anchor: '+old)
    code=code.replace(old,new)
# Fix the prior-unit input after the sequential file-name substitutions.
code=code.replace("old=resolve_units(read(f'translations/{stem}_batch03_ko.json'))",
                  "old=resolve_units(read(f'translations/{stem}_batch02_ko.json'))")
exec(compile(code,previous.__file__+' [90-unit binding]','exec'),globals())
