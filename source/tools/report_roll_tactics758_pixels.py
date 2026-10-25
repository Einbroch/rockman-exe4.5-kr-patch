"""Bound existing5x2 pixel verifier to758-unit ROM, explicit mono IDs."""
from pathlib import Path
import report_tactics_prompt_runtime as previous

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    changes={'exe45_ko_development_tactics_prompts_v1.gba':'exe45_ko_development_roll_tactics_v1.gba',
        "asset = ROOT/'translations/megaman_tactics_prompts_ko.json'":"asset = ROOT/'translations/rockman_roll_tactics_escape_ko.json'",
        'units = resolve_units(read(asset))':'units = [u for u in resolve_units(read(asset)) if int(u["id"].split(":")[1]) in (0,1,6,7)]',
        'choices=(0,1)':'choices=(0,1,6,7)',
        'PASS bounded normal Rockman TACTICS prompts5x2':'PASS bounded TACTICS5x2 pixels;0/1 normal,6/7 require diagnostic receipt',
        'two Rockman prompts only, other142 scripts unchanged':'Four mono prompts only; Roll6/7 lookup diagnostics are not normal Roll selection. Other132 scripts unchanged'}
    for old,new in changes.items():
        if code.count(old)!=1:raise ValueError('prompt verifier binding:'+old)
        code=code.replace(old,new)
    ns={'__name__':'roll_tactics758_pixel_bound'}
    exec(compile(code,previous.__file__+' [758 mono IDs]','exec'),ns);ns['main']()

if __name__=='__main__':main()
