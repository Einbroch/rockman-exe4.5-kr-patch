"""Exact756-unit prompt regression, frozen native5x2 verifier."""
from pathlib import Path
import report_tactics_prompt_runtime as previous

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    changes={'exe45_ko_development_tactics_prompts_v1.gba':'exe45_ko_development_roll_escape_v1.gba',
        "asset = ROOT/'translations/megaman_tactics_prompts_ko.json'":"asset = ROOT/'translations/rockman_roll_escape_ko.json'",
        'units = resolve_units(read(asset))':'units = [u for u in resolve_units(read(asset)) if int(u["id"].split(":")[1]) in (0,1)]',
        'other142 scripts unchanged':'Rockman2..5 and Roll8..11 translated with separate normal renderer; other134 scripts unchanged'}
    for old,new in changes.items():
        if code.count(old)!=1:raise ValueError('prompt verifier binding:'+old)
        code=code.replace(old,new)
    ns={'__name__':'roll_tactics_verifier_bound'}
    exec(compile(code,previous.__file__+' [exact756 ROM]','exec'),ns);ns['main']()

if __name__=='__main__':main()
