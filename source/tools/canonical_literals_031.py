"""Lossless explicit-LF TPL representation, including trailing blank-row spaces.

Binary equivalence remains a mandatory native whole-archive compiler check.
"""
from tpl_literals import literals,skeleton


def canonical_literals(tpl):
    before=literals(tpl);out=tpl
    for item in reversed(before):
        if not item.text:continue
        if any(c in item.text for c in ('"','\\','\r','\t')):raise ValueError('031 unsupported literal representation')
        encoded='"'+item.text.replace('\n','\\n')+'"'
        out=out[:item.start]+encoded+out[item.end:]
    if [(i.key,i.language,i.text) for i in literals(out)]!=[(i.key,i.language,i.text) for i in before] or skeleton(out)!=skeleton(tpl):raise ValueError('031 canonical representation changed protected content')
    return out
