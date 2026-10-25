"""Explicit development adoption of immutable39-unit authored draft."""
import json
from build_visibility_poc import ROOT,sha,require_hash

def main():
    p=ROOT/'analysis/keyitem_translation_draft_v1/draft.json'
    require_hash(p,'a83c2de2991efc47028ec07a784a9c9a53ea547469b376dcba74944e5b535da0')
    d=json.loads(p.read_text(encoding='utf8'))
    result=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',
        source_sha256='588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8',
        archive='709408',source_archive_sha256='15bbcb0dc3e2fa083d55b00fb4180312836bef14fbd2d9f63e2d82f05760d793',
        consumer='normal-dialogue',context='Key-item and shared item descriptions/names; raw-ROM selector development input. Source controls/mugshots/item IDs unchanged.',
        draft_provenance=dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()),wording_changed=False),
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=d['units'])
    out=ROOT/'translations/keyitem_full_rom_ko.json';text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if out.exists() and out.read_text(encoding='utf8')!=text:raise ValueError('preserve authored input')
    if not out.exists():out.write_text(text,encoding='utf8')
    print(out)
if __name__=='__main__':main()
