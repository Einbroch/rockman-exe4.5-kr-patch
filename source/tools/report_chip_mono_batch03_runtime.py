"""Exact249-unit source binding, reusing preserved strict checks, not results."""
from pathlib import Path
import report_chip_mono_batch02_runtime as previous


def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    for old,new in {
        'batch02':'batch03', 'range(1,61)':'range(1,91)',
        '==189':'==249', '==196':'==166', "'draft_units':189":"'draft_units':249",
        "'description_units':60":"'description_units':90",
        "'unselected_description_scripts':196":"'unselected_description_scripts':166",
        'all60':'all90', 'protected60':'protected90', 'bounded60':'bounded90',
        'prove60':'prove90', 'mono60_runtime_bound':'mono90_runtime_bound',
        '189-unit':'249-unit',
    }.items():
        if old not in code: raise ValueError('missing249-unit anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'batch03_runtime_binding'}
    # Only the credited normal route changes: generic capture omitted folder ABI QA.
    code=code.replace("'chip-mono-batch01-v1-':'chip-mono-batch03-v1-',",
                      "'chip-mono-batch01-v1-normal-scroll':'chip-mono-batch03-v1-normal-scroll-r2',\n        'chip-mono-batch01-v1-':'chip-mono-batch03-v1-',")
    exec(compile(code,previous.__file__+' [249-unit binding]','exec'),ns)
    ns['main']()


if __name__=='__main__': main()
