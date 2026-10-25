"""Latest possessions recipe plus explicitly selected full39 ROM clone."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,require_hash

def main():
    # This flag translates native kana actions, not automatic Hangul input.
    ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);ap.add_argument('--gutsman-plugout',action='store_true');ap.add_argument('--gutsman-profile',action='store_true');ap.add_argument('--gutsman-profile-questions',action='store_true');ap.add_argument('--gutsman-profile-family',action='store_true')
    ap.add_argument('--gutsman-profile-answers',action='store_true');ap.add_argument('--gutsman-profile-wishlist',action='store_true');ap.add_argument('--input-confirmation',action='store_true');ap.add_argument('--input-heading',action='store_true');ap.add_argument('--input-remaining',action='store_true');ap.add_argument('--hangul-keyboard-glyphs',action='store_true')
    ap.add_argument('--native-keyboard-labels',action='store_true')
    ap.add_argument('--navi-card-graphics',action='store_true')
    ap.add_argument('--first-mail',action='store_true')
    ap.add_argument('--official-mail',action='store_true')
    ap.add_argument('--news-mail',action='store_true')
    ap.add_argument('--mail-rom-reader',action='store_true')
    ap.add_argument('--full-mail-body',action='store_true')
    ap.add_argument('--full-mail-header',action='store_true')
    ap.add_argument('--mission-mail-header',action='store_true')
    ap.add_argument('--pending-batch500',action='store_true')
    ap.add_argument('--pending-batch500-002',action='store_true')
    ap.add_argument('--pending-batch500-003',action='store_true')
    ap.add_argument('--pending-batch500-004',action='store_true')
    ap.add_argument('--pending-batch500-005',action='store_true')
    ap.add_argument('--pending-batch500-006',action='store_true')
    ap.add_argument('--pending-batch500-007',action='store_true')
    ap.add_argument('--pending-batch500-008',action='store_true')
    ap.add_argument('--pending-batch500-009',action='store_true')
    ap.add_argument('--pending-batch500-010',action='store_true')
    ap.add_argument('--pending-batch500-011',action='store_true')
    ap.add_argument('--pending-batch500-012',action='store_true')
    ap.add_argument('--pending-batch500-013',action='store_true')
    ap.add_argument('--pending-batch500-014',action='store_true')
    ap.add_argument('--pending-batch500-015',action='store_true')
    ap.add_argument('--pending-batch500-016',action='store_true')
    ap.add_argument('--pending-batch500-017',action='store_true')
    ap.add_argument('--pending-batch500-018',action='store_true')
    ap.add_argument('--pending-batch500-019',action='store_true')
    ap.add_argument('--pending-batch500-020',action='store_true')
    ap.add_argument('--pending-batch500-021',action='store_true')
    ap.add_argument('--pending-batch500-022',action='store_true')
    ap.add_argument('--calendar-date-save',action='store_true');ap.add_argument('--save-initialize',action='store_true');ap.add_argument('--title-menu-graphics',action='store_true');ap.add_argument('--title-weekend-menu',action='store_true');ap.add_argument('--startup-ui',action='store_true');a=ap.parse_args()
    if not a.name.replace('_','').isalnum():raise ValueError('simple artifact name')
    recipe=json.loads((ROOT/'analysis/keyitem_empty_v1/build_recipe.json').read_text())
    require_hash(ROOT/recipe['parent_recipe'],recipe['parent_recipe_sha256'])
    parent=json.loads((ROOT/recipe['parent_recipe']).read_text())
    out=ROOT/f'poc/output/{a.name}.gba';work=ROOT/f'poc/build/{a.name}'
    if out.exists() or work.exists():raise ValueError('preserve prior builds')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/recipe['builder']),*parent['flags'],*recipe['additional_flags'],
        *(['--gutsman-plugout'] if a.gutsman_plugout else []),
        *(['--gutsman-profile'] if a.gutsman_profile else []),
        *(['--gutsman-profile-questions'] if a.gutsman_profile_questions else []),
        *(['--gutsman-profile-family'] if a.gutsman_profile_family else []),
        *(['--gutsman-profile-answers'] if a.gutsman_profile_answers else []),
        *(['--gutsman-profile-wishlist'] if a.gutsman_profile_wishlist else []),
        *(['--input-confirmation'] if a.input_confirmation else []),
        *(['--input-heading'] if a.input_heading else []),
        *(['--input-remaining'] if a.input_remaining else []),
        *(['--calendar-date-save'] if a.calendar_date_save else []),
        *(['--save-initialize'] if a.save_initialize else []),
        *(['--hangul-keyboard-glyphs'] if a.hangul_keyboard_glyphs else []),
        *(['--title-menu-graphics'] if a.title_menu_graphics else []),
        *(['--title-weekend-menu'] if a.title_weekend_menu else []),
        *(['--startup-ui'] if a.startup_ui else []),
        *(['--native-keyboard-labels'] if a.native_keyboard_labels else []),
        *(['--navi-card-graphics'] if a.navi_card_graphics else []),
        *(['--first-mail'] if a.first_mail else []),
        *(['--official-mail'] if a.official_mail else []),
        *(['--news-mail'] if a.news_mail else []),
        *(['--mail-rom-reader'] if a.mail_rom_reader else []),
        *(['--full-mail-body'] if a.full_mail_body else []),
        *(['--full-mail-header'] if a.full_mail_header else []),
        *(['--mission-mail-header'] if a.mission_mail_header else []),
        *(['--pending-batch500'] if a.pending_batch500 else []),
        *(['--pending-batch500-002'] if a.pending_batch500_002 else []),
        *(['--pending-batch500-003'] if a.pending_batch500_003 else []),
        *(['--pending-batch500-004'] if a.pending_batch500_004 else []),
        *(['--pending-batch500-005'] if a.pending_batch500_005 else []),
        *(['--pending-batch500-006'] if a.pending_batch500_006 else []),
        *(['--pending-batch500-007'] if a.pending_batch500_007 else []),
        *(['--pending-batch500-008'] if a.pending_batch500_008 else []),
        *(['--pending-batch500-009'] if a.pending_batch500_009 else []),
        *(['--pending-batch500-010'] if a.pending_batch500_010 else []),
        *(['--pending-batch500-011'] if a.pending_batch500_011 else []),
        *(['--pending-batch500-012'] if a.pending_batch500_012 else []),
        *(['--pending-batch500-013'] if a.pending_batch500_013 else []),
        *(['--pending-batch500-014'] if a.pending_batch500_014 else []),
        *(['--pending-batch500-015'] if a.pending_batch500_015 else []),
        *(['--pending-batch500-016'] if a.pending_batch500_016 else []),
        *(['--pending-batch500-017'] if a.pending_batch500_017 else []),
        *(['--pending-batch500-018'] if a.pending_batch500_018 else []),
        *(['--pending-batch500-019'] if a.pending_batch500_019 else []),
        *(['--pending-batch500-020'] if a.pending_batch500_020 else []),
        *(['--pending-batch500-021'] if a.pending_batch500_021 else []),
        *(['--pending-batch500-022'] if a.pending_batch500_022 else []),
        '--possessions-statistics','--keyitem-rom-translations','translations/keyitem_full_rom_ko.json',
        '--work',str(work.relative_to(ROOT)),'--out',str(out.relative_to(ROOT))],check=True,cwd=ROOT)
if __name__=='__main__':main()
