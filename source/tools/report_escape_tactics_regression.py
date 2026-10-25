"""Bind frozen prompt verifier to new ROM and unchanged two mono units."""
from pathlib import Path
import report_tactics_prompt_runtime as previous

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    changes={'exe45_ko_development_tactics_prompts_v1.gba':'exe45_ko_development_megaman_escape_v1.gba',
        "asset = ROOT/'translations/megaman_tactics_prompts_ko.json'":"asset = ROOT/'translations/megaman_tactics_escape_ko.json'",
        'units = resolve_units(read(asset))':'units = [u for u in resolve_units(read(asset)) if int(u["id"].split(":")[1]) in (0,1)]',
        'other142 scripts unchanged':'escape2..5 translated with separate normal renderer; other138 scripts unchanged'}
    for old,new in changes.items():
        if code.count(old)!=1:raise ValueError('prompt verifier binding:'+old)
        code=code.replace(old,new)
    ns={'__name__':'escape_tactics_verifier_bound'}
    exec(compile(code,previous.__file__+' [exact new ROM/two mono units]','exec'),ns)
    ns['main']()

if __name__=='__main__':main()
