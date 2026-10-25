"""Quarantined Roll8..11 lookup samples, not Roll normal-play outcomes."""
from pathlib import Path
import capture_megaman_escape_samples as previous

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    old='choices=(2,3,4)'
    if code.count(old)!=1:raise ValueError('sample choices binding')
    code=code.replace(old,'choices=(8,9,10,11)')
    ns={'__name__':'roll_escape_sample_bound','__file__':__file__}
    exec(compile(code,previous.__file__+' [Roll8..11]','exec'),ns)
    rc=ns['main']()
    import json
    out=Path(previous.normal.fixed.value('--out'));path=out/'escape_alias_environment.json'
    env=json.loads(path.read_text());env['sampler_source_sha256']=previous.sha(Path(previous.__file__).read_bytes())
    path.write_text(json.dumps(env,indent=2),encoding='utf-8')
    return rc

if __name__=='__main__':raise SystemExit(main())
