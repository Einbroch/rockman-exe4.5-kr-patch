"""Normal no-event schedule and cumulative exact-ROM regression checks."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,static,verify_route
from report_gutsman_pet import main as pet_regression
from report_numberman_return import pages
from run_gutsman_schedule import STEM,PREFIX
def main():
    baseline=pet_regression(stem=STEM,prefix=PREFIX,expected_counts=(2241,54,678),oldstem='exe45_ko_development_gutsman_competition_v1',outdir='gutsman_schedule_v1/pet_regression',inventory_outdir='full_scope_gutsman_schedule_v1',added_literal_units=0)
    m,rom,e,s,c=static(STEM,'666F38');pool=0x8000000+next(a for a in m['archives'] if a['archive']=='666F38')['rom_offset'];rt=ROOT/'poc/runtime';p=rt/(PREFIX+'today');r=verify_route(p,m['output_sha256'],set())
    if r['state_origin']!=str(rt/(PREFIX+'select-gutsman')/'result.json') or r.get('normal_play_checkpoint_eligible') is False or any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('normal schedule ancestry/intervention')
    q=pages(p,10,10,m,rom,e,s,pool,exit_step=6)
    if len(q)!=2:raise ValueError('no-event native scope')
    final=read(p/'step_007_roll_pet.json');petpool=0x8000000+next(a for a in m['archives'] if a['archive']=='665F3C')['rom_offset'];ram=(p/'step_007_gbaExtWorkRam.bin').read_bytes()
    if len(final['calls'])!=1 or final['calls'][0]['root']!=pool or final['calls'][0]['script']!=10 or ram[0xFA21]!=1 or struct.unpack_from('<I',ram,0xFA50)[0]!=petpool:raise ValueError('normal L entry/menu return')
    suffix=next(x for x in next(a for a in m['archives'] if a['archive']=='666F38')['layout'] if x['id']=='666F38:11:2')
    if not suffix['non_growing_dynamic_suffix'] or suffix['source_suffix_width']!=30 or suffix['line_advance_pixels']!=[24,0]:raise ValueError('clock layout guard')
    out=ROOT/'analysis/gutsman_schedule_v1';out.mkdir(parents=True,exist_ok=True);sheet=Image.new('RGB',(480,160))
    for i,x in enumerate(q):sheet.paste(Image.open(p/f"step_{x['step']:03}.png"),(i*240,0))
    sheet.save(out/'normal_today_no_events.png');covered={x['unit'] for x in q};result=dict(passed=True,policy='development-draft; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],added_literal_units=12,new_translated_expressions=6,retained_punctuation_units=6,selected_text_units=2241,static=c,native_schedule_binding=dict(root_offset=0x38134,rom_pointer=pool),clock_suffix_static=suffix,pet_regression=baseline,normal_pages=q,normal_runtime_units=sorted(covered),static_only_units=sorted(set(s)-covered),native_menu_return_step=7,remaining_catalog=baseline['remaining_catalog'],limits=['Native GutsMan L/today10 no-event2literals only. Upcoming1->2->3 and registered11 clock/AMPM/event loops->12 not runtime proved. Six original punctuation literals retained.','Clock suffix24px <= source30px, original controls/format preserved; static non-growth does not prove arbitrary time/event name population or persistence.','Own NumberMan save/cold continue/3pages,Guts intro2/PET8scenes22units regression; previous53 payloads/graphics identical. Prior competition/Jack-In/mail/return/seasonal not rerun on this ROM.','Whole text/images/inline/fixed population and Hangul name editing/committed records/all redisplays/persistence/old-save compatibility unresolved, native wait-arrow53pixel difference open, human wording review pending; no release.'])
    (out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print('Guts schedule12 static / native today no-event2pages / PET return PASS');return result
if __name__=='__main__':main()
