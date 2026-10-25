"""Explicit script31 scope, keeping the seven original diagnostic tools unchanged."""
import json,sys
from pathlib import Path
import capture_gutsman_pet_talk_diagnostic as diagnostic
from build_visibility_poc import sha

def main():
    if int(sys.argv[sys.argv.index('--talk-script')+1])!=31:raise ValueError('nickname diagnostic31 only')
    diagnostic.SCRIPTS=[31]
    rc=diagnostic.main();out=Path(sys.argv[sys.argv.index('--out')+1]);p=out/'talk_environment.json';env=json.loads(p.read_text(encoding='utf8'))
    env['nickname_scope_tool_sha256']=sha(Path(__file__).read_bytes())
    p.write_text(json.dumps(env,indent=2),encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
