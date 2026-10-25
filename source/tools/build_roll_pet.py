"""Explicit cumulative immutable-source Roll PET development build selection."""
import argparse,subprocess,sys
from build_visibility_poc import ROOT

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',required=True);ap.add_argument('--out',required=True);ap.add_argument('--roll-intro',action='store_true');ap.add_argument('--roll-fortune',action='store_true');ap.add_argument('--roll-fortune-results',action='store_true');ap.add_argument('--roll-minigame-results',action='store_true');ap.add_argument('--roll-minigame-rewards',action='store_true');ap.add_argument('--roll-fortune-complete',action='store_true')
    ap.add_argument('--startup-ui',action='store_true')
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
    ap.add_argument('--roll-jackin',action='store_true')
    ap.add_argument('--roll-return',action='store_true')
    ap.add_argument('--roll-plugout',action='store_true')
    ap.add_argument('--gutsman-plugout',action='store_true')
    ap.add_argument('--gutsman-profile',action='store_true')
    ap.add_argument('--gutsman-profile-questions',action='store_true')
    ap.add_argument('--gutsman-profile-family',action='store_true')
    ap.add_argument('--gutsman-profile-answers',action='store_true')
    ap.add_argument('--gutsman-profile-wishlist',action='store_true')
    ap.add_argument('--input-confirmation',action='store_true')
    ap.add_argument('--input-heading',action='store_true')
    ap.add_argument('--input-remaining',action='store_true')
    ap.add_argument('--calendar-date-save',action='store_true')
    ap.add_argument('--save-initialize',action='store_true')
    ap.add_argument('--hangul-keyboard-glyphs',action='store_true')
    ap.add_argument('--title-menu-graphics',action='store_true')
    ap.add_argument('--title-weekend-menu',action='store_true')
    ap.add_argument('--roll-family-sister',action='store_true')
    ap.add_argument('--roll-family-sisters',action='store_true')
    ap.add_argument('--roll-family-siblings',action='store_true')
    ap.add_argument('--roll-food',action='store_true')
    ap.add_argument('--roll-subjects',action='store_true')
    ap.add_argument('--roll-pet-talk',action='store_true')
    ap.add_argument('--roll-pet-license',action='store_true')
    ap.add_argument('--roll-pet-incident',action='store_true')
    ap.add_argument('--roll-pet-keyquest',action='store_true')
    ap.add_argument('--roll-pet-tournament',action='store_true')
    ap.add_argument('--roll-pet-events',action='store_true')
    ap.add_argument('--roll-pet-mail',action='store_true')
    ap.add_argument('--roll-pet-undernet',action='store_true')
    ap.add_argument('--roll-pet-weekday',action='store_true')
    ap.add_argument('--roll-mail-alert',action='store_true')
    ap.add_argument('--roll-pet-chipquest',action='store_true')
    ap.add_argument('--roll-dialogue-chip-name',action='store_true')
    ap.add_argument('--roll-competition',action='store_true')
    ap.add_argument('--roll-schedule',action='store_true')
    ap.add_argument('--roll-schedule-time',action='store_true')
    ap.add_argument('--roll-schedule-alarm',action='store_true')
    ap.add_argument('--calendar-menu',action='store_true')
    ap.add_argument('--calendar-types',action='store_true')
    ap.add_argument('--roll-calendar-dialogue',action='store_true')
    ap.add_argument('--roll-calendar-content',action='store_true')
    ap.add_argument('--roll-calendar-date',action='store_true')
    ap.add_argument('--calendar-frequency-graphics',action='store_true')
    ap.add_argument('--calendar-presets-poc',action='store_true')
    ap.add_argument('--roll-save',action='store_true')
    ap.add_argument('--save-labels',action='store_true')
    ap.add_argument('--save-surface',action='store_true')
    ap.add_argument('--gutsman-save',action='store_true')
    ap.add_argument('--numberman-save',action='store_true')
    ap.add_argument('--numberman-intro',action='store_true')
    ap.add_argument('--numberman-pet',action='store_true')
    ap.add_argument('--numberman-training-intro',action='store_true')
    ap.add_argument('--numberman-jackin',action='store_true')
    ap.add_argument('--numberman-drill-intro',action='store_true')
    ap.add_argument('--numberman-drill-bubbles',action='store_true')
    ap.add_argument('--numberman-training-results',action='store_true')
    ap.add_argument('--numberman-training-rewards',action='store_true')
    ap.add_argument('--numberman-drill-options',action='store_true')
    ap.add_argument('--numberman-drill-options-padding',action='store_true')
    ap.add_argument('--numberman-drill-options-spacing',action='store_true')
    ap.add_argument('--numberman-return',action='store_true')
    ap.add_argument('--numberman-seasonal',action='store_true')
    ap.add_argument('--seasonal-companions',action='store_true')
    ap.add_argument('--gutsman-seasonal',action='store_true')
    ap.add_argument('--windman-seasonal',action='store_true')
    ap.add_argument('--searchman-seasonal',action='store_true')
    ap.add_argument('--fireman-seasonal',action='store_true')
    ap.add_argument('--thunderman-seasonal',action='store_true')
    ap.add_argument('--blues-seasonal',action='store_true')
    ap.add_argument('--metalman-seasonal',action='store_true')
    ap.add_argument('--junkman-seasonal',action='store_true')
    ap.add_argument('--aquaman-seasonal',action='store_true')
    ap.add_argument('--woodman-seasonal',action='store_true')
    ap.add_argument('--starman-seasonal',action='store_true')
    ap.add_argument('--shadowman-seasonal',action='store_true')
    ap.add_argument('--knightman-seasonal',action='store_true')
    ap.add_argument('--napalmman-seasonal',action='store_true')
    ap.add_argument('--iceman-seasonal',action='store_true')
    ap.add_argument('--elecman-seasonal',action='store_true')
    ap.add_argument('--plantman-seasonal',action='store_true')
    ap.add_argument('--forte-seasonal',action='store_true')
    ap.add_argument('--gutsman-intro',action='store_true')
    ap.add_argument('--gutsman-pet',action='store_true')
    ap.add_argument('--gutsman-operations',action='store_true')
    ap.add_argument('--gutsman-competition',action='store_true')
    ap.add_argument('--gutsman-schedule',action='store_true')
    ap.add_argument('--gutsman-schedule-alarm',action='store_true')
    ap.add_argument('--gutsman-alarm-followup',action='store_true')
    ap.add_argument('--gutsman-alarm-meal',action='store_true')
    ap.add_argument('--gutsman-calendar-prompts',action='store_true')
    ap.add_argument('--gutsman-calendar-content',action='store_true')
    ap.add_argument('--gutsman-calendar-confirmation',action='store_true')
    ap.add_argument('--gutsman-calendar-home',action='store_true')
    ap.add_argument('--gutsman-calendar-register',action='store_true')
    ap.add_argument('--gutsman-calendar-anniversary',action='store_true')
    ap.add_argument('--gutsman-calendar-anniversary-confirmation',action='store_true')
    ap.add_argument('--gutsman-calendar-navigation',action='store_true')
    ap.add_argument('--gutsman-calendar-management',action='store_true')
    ap.add_argument('--gutsman-calendar-schedule-delete',action='store_true')
    ap.add_argument('--gutsman-calendar-inventory',action='store_true')
    ap.add_argument('--keyitem-empty',action='store_true')
    ap.add_argument('--calendar-frequency-names',action='store_true')
    ap.add_argument('--possessions-statistics',action='store_true')
    ap.add_argument('--keyitem-rom-translations')
    ap.add_argument('--gutsman-battle-results',action='store_true')
    ap.add_argument('--gutsman-pet-talk',action='store_true')
    ap.add_argument('--gutsman-pet-chipquest',action='store_true')
    a=ap.parse_args()
    if a.save_labels and not a.roll_save:raise ValueError('save labels require retained Roll save scope')
    if a.save_surface and not (a.save_labels and a.roll_save):raise ValueError('save surface requires retained labels and Roll save scope')
    if a.gutsman_save and not a.save_surface:raise ValueError('GutsMan save requires retained save surface scope')
    if a.numberman_save and not a.gutsman_save:raise ValueError('NumberMan save requires retained GutsMan save scope')
    if a.numberman_intro and not a.numberman_save:raise ValueError('NumberMan intro requires retained cumulative save scope')
    if a.numberman_pet and not a.numberman_intro:raise ValueError('NumberMan PET requires retained introduction/save scope')
    if a.numberman_training_intro and not a.numberman_pet:raise ValueError('NumberMan training requires retained PET scope')
    if a.numberman_jackin and not a.numberman_training_intro:raise ValueError('NumberMan Jack-In requires retained training/PET scope')
    if a.numberman_drill_intro and not a.numberman_jackin:raise ValueError('NumberMan drill requires retained Jack-In scope')
    if a.numberman_drill_bubbles and not a.numberman_drill_intro:raise ValueError('NumberMan bubbles require retained drill intro')
    if a.numberman_training_results and not a.numberman_drill_bubbles:raise ValueError('NumberMan results require retained drill bubbles')
    if a.numberman_training_rewards and not a.numberman_training_results:raise ValueError('NumberMan rewards require retained results')
    if a.numberman_drill_options and not a.numberman_training_rewards:raise ValueError('NumberMan options require retained rewards')
    if a.numberman_drill_options_padding and not a.numberman_drill_options:raise ValueError('NumberMan label padding requires retained options')
    if a.numberman_drill_options_spacing and not a.numberman_drill_options_padding:raise ValueError('NumberMan column spacing requires retained label padding')
    if a.roll_dialogue_chip_name and not a.roll_pet_chipquest:raise ValueError('Roll dialogue name requires chipquest scope')
    if a.gutsman_pet_chipquest and not (a.gutsman_pet_talk and a.roll_dialogue_chip_name):raise ValueError('Guts chipquest requires retained talk and Roll name selector')
    cmd=[sys.executable,'-X','utf8',str(ROOT/'tools/build_development_patch.py')]
    for name in ['megaman_intro_ko','megaman_pet_menu_ko','four_navi_save_ko' if a.numberman_save else 'rockman_roll_gutsman_save_ko' if a.gutsman_save else 'rockman_roll_save_surface_ko' if a.save_surface else 'rockman_roll_save_labels_ko' if a.save_labels else 'rockman_roll_save_ko' if a.roll_save else 'megaman_save_ko','library_headers_ko','chip_descriptions_batch09_ko','chip_secondary_descriptions_ko','rockman_roll_tactics_escape_ko','roll_pet_menu_ko']:cmd+=['--translations',f'translations/{name}.json']
    if a.roll_intro:cmd+=['--translations','translations/roll_intro_ko.json']
    if a.numberman_return:
        if not a.numberman_intro:raise ValueError('NumberMan return requires retained intro')
        cmd+=['--translations','translations/numberman_return_ko.json']
    elif a.numberman_intro:cmd+=['--translations','translations/numberman_intro_ko.json']
    if a.numberman_seasonal:cmd+=['--translations','translations/numberman_seasonal_ko.json']
    if a.gutsman_seasonal:cmd+=['--translations','translations/gutsman_seasonal_ko.json']
    if a.gutsman_intro:cmd+=['--translations','translations/gutsman_intro_ko.json']
    if a.gutsman_pet:cmd+=['--translations','translations/gutsman_pet_menu_ko.json']
    if a.gutsman_competition:cmd+=['--translations','translations/gutsman_competition_ko.json']
    if a.gutsman_schedule:cmd+=['--translations','translations/gutsman_schedule_ko.json']
    if a.gutsman_alarm_meal:
        if not a.gutsman_alarm_followup or not a.gutsman_schedule_alarm:raise ValueError('meal requires prior alarm selections')
        cmd+=['--translations','translations/gutsman_alarm_meal_ko.json']
    elif a.gutsman_alarm_followup:
        if not a.gutsman_schedule_alarm:raise ValueError('alarm followup requires prior alarm selection')
        cmd+=['--translations','translations/gutsman_alarm_followup_ko.json']
    elif a.gutsman_schedule_alarm:cmd+=['--translations','translations/gutsman_schedule_alarm_ko.json']
    if a.gutsman_battle_results:cmd+=['--translations','translations/gutsman_battle_results_ko.json']
    if a.gutsman_calendar_schedule_delete:
        if not a.gutsman_calendar_management:raise ValueError('schedule deletion requires retained calendar management chain')
        if not (a.gutsman_calendar_navigation and a.gutsman_calendar_anniversary_confirmation and a.gutsman_calendar_anniversary and a.gutsman_calendar_register and a.gutsman_calendar_home and a.gutsman_calendar_confirmation and a.gutsman_calendar_content and a.gutsman_calendar_prompts and a.calendar_presets_poc):raise ValueError('schedule deletion requires full calendar chain')
        if a.gutsman_calendar_inventory:
            cmd+=['--translations','translations/gutsman_calendar_inventory_ko.json']
        else:cmd+=['--translations','translations/gutsman_calendar_schedule_delete_ko.json']
    elif a.gutsman_calendar_inventory:raise ValueError('inventory requires full schedule deletion chain')
    elif a.gutsman_calendar_management:
        if not (a.gutsman_calendar_navigation and a.gutsman_calendar_anniversary_confirmation and a.gutsman_calendar_anniversary and a.gutsman_calendar_register and a.gutsman_calendar_home and a.gutsman_calendar_confirmation and a.gutsman_calendar_content and a.gutsman_calendar_prompts and a.calendar_presets_poc):raise ValueError('calendar management requires retained calendar chain')
        cmd+=['--translations','translations/gutsman_calendar_management_ko.json']
    elif a.gutsman_calendar_navigation:
        if not (a.gutsman_calendar_anniversary_confirmation and a.gutsman_calendar_anniversary and a.gutsman_calendar_register and a.gutsman_calendar_home and a.gutsman_calendar_confirmation and a.gutsman_calendar_content and a.gutsman_calendar_prompts and a.calendar_presets_poc):raise ValueError('calendar navigation requires full retained calendar chain')
        cmd+=['--translations','translations/gutsman_calendar_navigation_ko.json']
    elif a.gutsman_calendar_anniversary_confirmation:
        if not (a.gutsman_calendar_anniversary and a.gutsman_calendar_register and a.gutsman_calendar_home and a.gutsman_calendar_confirmation and a.gutsman_calendar_content and a.gutsman_calendar_prompts and a.calendar_presets_poc):raise ValueError('anniversary confirmation requires full retained calendar chain')
        cmd+=['--translations','translations/gutsman_calendar_anniversary_confirmation_ko.json']
    elif a.gutsman_calendar_anniversary:
        if not (a.gutsman_calendar_register and a.gutsman_calendar_home and a.gutsman_calendar_confirmation and a.gutsman_calendar_content and a.gutsman_calendar_prompts and a.calendar_presets_poc):raise ValueError('calendar anniversary requires retained register/home/confirmation/content/prompts/presets')
        cmd+=['--translations','translations/gutsman_calendar_anniversary_ko.json']
    elif a.gutsman_calendar_register:
        if not (a.gutsman_calendar_home and a.gutsman_calendar_confirmation and a.gutsman_calendar_content and a.gutsman_calendar_prompts):raise ValueError('calendar register requires retained home/confirmation/content/prompts')
        cmd+=['--translations','translations/gutsman_calendar_register_ko.json']
    elif a.gutsman_calendar_home:
        if not (a.gutsman_calendar_confirmation and a.gutsman_calendar_content and a.gutsman_calendar_prompts):raise ValueError('calendar home requires retained confirmation/content/prompts')
        cmd+=['--translations','translations/gutsman_calendar_home_ko.json']
    elif a.gutsman_calendar_confirmation:
        if not (a.gutsman_calendar_content and a.gutsman_calendar_prompts):raise ValueError('calendar confirmation requires retained content/prompts')
        cmd+=['--translations','translations/gutsman_calendar_confirmation_ko.json']
    elif a.gutsman_calendar_content:
        if not a.gutsman_calendar_prompts:raise ValueError('calendar content requires retained prompts')
        cmd+=['--translations','translations/gutsman_calendar_content_ko.json']
    elif a.gutsman_calendar_prompts:cmd+=['--translations','translations/gutsman_calendar_prompts_ko.json']
    if a.gutsman_pet_talk:cmd+=['--translations','translations/gutsman_pet_chipquest_ko.json' if a.gutsman_pet_chipquest else 'translations/gutsman_pet_talk_ko.json']
    if a.gutsman_operations:
        for name in ['gutsman_return_ko','gutsman_jackin_ko','gutsman_mail_alert_ko']:cmd+=['--translations',f'translations/{name}.json']
    if a.windman_seasonal:cmd+=['--translations','translations/windman_seasonal_ko.json']
    if a.searchman_seasonal:cmd+=['--translations','translations/searchman_seasonal_ko.json']
    if a.fireman_seasonal:cmd+=['--translations','translations/fireman_seasonal_ko.json']
    if a.thunderman_seasonal:cmd+=['--translations','translations/thunderman_seasonal_ko.json']
    if a.blues_seasonal:cmd+=['--translations','translations/blues_seasonal_ko.json']
    if a.metalman_seasonal:cmd+=['--translations','translations/metalman_seasonal_ko.json']
    if a.junkman_seasonal:cmd+=['--translations','translations/junkman_seasonal_ko.json']
    if a.aquaman_seasonal:cmd+=['--translations','translations/aquaman_seasonal_ko.json']
    if a.woodman_seasonal:cmd+=['--translations','translations/woodman_seasonal_ko.json']
    if a.starman_seasonal:cmd+=['--translations','translations/starman_seasonal_ko.json']
    if a.shadowman_seasonal:cmd+=['--translations','translations/shadowman_seasonal_ko.json']
    if a.knightman_seasonal:cmd+=['--translations','translations/knightman_seasonal_ko.json']
    if a.napalmman_seasonal:cmd+=['--translations','translations/napalmman_seasonal_ko.json']
    if a.iceman_seasonal:cmd+=['--translations','translations/iceman_seasonal_ko.json']
    if a.elecman_seasonal:cmd+=['--translations','translations/elecman_seasonal_ko.json']
    if a.plantman_seasonal:cmd+=['--translations','translations/plantman_seasonal_ko.json']
    if a.forte_seasonal:cmd+=['--translations','translations/forte_seasonal_ko.json']
    if a.seasonal_companions:
        cmd+=['--translations','translations/rockman_seasonal_ko.json','--translations','translations/roll_seasonal_ko.json']
    if a.numberman_pet:cmd+=['--translations','translations/numberman_pet_menu_ko.json']
    if a.numberman_training_rewards:cmd+=['--translations','translations/numberman_training_rewards_ko.json']
    elif a.numberman_training_results:cmd+=['--translations','translations/numberman_training_results_ko.json']
    elif a.numberman_training_intro:cmd+=['--translations','translations/numberman_training_intro_ko.json']
    if a.numberman_jackin:cmd+=['--translations','translations/numberman_jackin_ko.json']
    if a.numberman_drill_options_spacing:cmd+=['--translations','translations/numberman_drill_options_spaced_ko.json']
    elif a.numberman_drill_options_padding:cmd+=['--translations','translations/numberman_drill_options_padded_ko.json']
    elif a.numberman_drill_options:cmd+=['--translations','translations/numberman_drill_options_ko.json']
    elif a.numberman_drill_bubbles:cmd+=['--translations','translations/numberman_drill_bubbles_ko.json']
    elif a.numberman_drill_intro:cmd+=['--translations','translations/numberman_drill_intro_ko.json']
    if a.roll_mail_alert:cmd+=['--translations','translations/roll_mail_alert_ko.json']
    if a.roll_schedule_alarm:cmd+=['--translations','translations/roll_schedule_alarm_ko.json']
    if a.possessions_statistics:
        if not (a.calendar_frequency_names and a.gutsman_calendar_anniversary_confirmation and a.calendar_presets_poc and a.keyitem_empty):raise ValueError('statistics requires retained frequency/keyitem baseline')
        if a.input_heading and not a.input_confirmation:raise ValueError('heading retains confirmation baseline')
        if a.save_initialize:
            if not(a.calendar_date_save and a.input_remaining and a.input_heading):raise ValueError('initialization UI retains date/save and input baseline')
            from save_initialize import prepare
            selected_input=prepare()
        elif a.calendar_date_save:
            if not (a.input_remaining and a.input_heading):raise ValueError('date/save retains complete input UI baseline')
            from calendar_date_save import prepare
            selected_input=prepare()
        elif a.input_remaining:
            if not a.input_heading:raise ValueError('remaining UI requires heading baseline')
            from input_remaining import prepare
            selected_input=prepare()
        else:selected_input='translations/input_heading_ko.json' if a.input_heading else 'translations/input_confirmation_ko.json' if a.input_confirmation else 'translations/possessions_statistics_ko.json'
        cmd+=['--translations',selected_input]
    elif a.input_confirmation:raise ValueError('input confirmation requires retained possessions-statistics baseline')
    elif a.calendar_frequency_names:
        if not (a.gutsman_calendar_anniversary_confirmation and a.calendar_presets_poc):raise ValueError('frequency names require retained calendar preset/anniversary chain')
        cmd+=['--translations','translations/calendar_frequency_names_ko.json']
    elif a.gutsman_calendar_anniversary_confirmation:cmd+=['--translations','translations/calendar_anniversary_presets_ko.json']
    elif a.gutsman_calendar_anniversary:cmd+=['--translations','translations/calendar_anniversary_labels_ko.json']
    elif a.calendar_presets_poc:cmd+=['--translations','translations/calendar_presets_ko.json']
    elif a.calendar_types:cmd+=['--translations','translations/calendar_types_ko.json']
    elif a.calendar_menu:cmd+=['--translations','translations/calendar_menu_ko.json']
    if a.roll_calendar_date:cmd+=['--translations','translations/roll_calendar_date_ko.json']
    elif a.roll_calendar_content:cmd+=['--translations','translations/roll_calendar_content_ko.json']
    elif a.roll_calendar_dialogue:cmd+=['--translations','translations/roll_calendar_dialogue_ko.json']
    if a.roll_competition:cmd+=['--translations','translations/roll_competition_ko.json']
    if a.roll_schedule_time:cmd+=['--translations','translations/roll_schedule_time_ko.json']
    elif a.roll_schedule:cmd+=['--translations','translations/roll_schedule_ko.json']
    if a.roll_jackin:cmd+=['--translations','translations/roll_jackin_ko.json']
    if a.roll_return:cmd+=['--translations','translations/roll_return_ko.json']
    if a.gutsman_plugout:
        if not a.roll_plugout:raise ValueError('GutsMan plugout requires retained Roll input')
        cmd+=['--translations','translations/roll_gutsman_plugout_ko.json']
    elif a.roll_plugout:cmd+=['--translations','translations/roll_plugout_ko.json']
    if a.gutsman_profile_wishlist:
        if not (a.gutsman_profile_answers and a.gutsman_profile_family and a.gutsman_profile_questions and a.gutsman_profile and a.gutsman_plugout):raise ValueError('GutsMan wishlist requires retained answers/family/questions/profile/plugout baseline')
        cmd+=['--translations','translations/gutsman_profile_wishlist_ko.json']
    elif a.gutsman_profile_answers:
        if not (a.gutsman_profile_family and a.gutsman_profile_questions and a.gutsman_profile and a.gutsman_plugout):raise ValueError('GutsMan answers requires retained family/questions/profile/plugout baseline')
        cmd+=['--translations','translations/gutsman_profile_answers_ko.json']
    elif a.gutsman_profile_family:
        if not (a.gutsman_profile_questions and a.gutsman_profile and a.gutsman_plugout):raise ValueError('GutsMan family requires retained questions/profile/plugout baseline')
        cmd+=['--translations','translations/gutsman_profile_family_checked_ko.json']
    elif a.gutsman_profile_questions:
        if not (a.gutsman_profile and a.gutsman_plugout):raise ValueError('GutsMan profile questions require retained profile/plugout baseline')
        cmd+=['--translations','translations/gutsman_profile_questions_ko.json']
    elif a.gutsman_profile:
        if not a.gutsman_plugout:raise ValueError('GutsMan profile requires current plugout baseline')
        cmd+=['--translations','translations/gutsman_profile_ko.json']
    if a.roll_pet_chipquest:cmd+=['--translations','translations/roll_pet_chipquest_ko.json']
    elif a.roll_pet_weekday:cmd+=['--translations','translations/roll_pet_weekday_ko.json']
    elif a.roll_pet_undernet:cmd+=['--translations','translations/roll_pet_undernet_ko.json']
    elif a.roll_pet_mail:cmd+=['--translations','translations/roll_pet_mail_ko.json']
    elif a.roll_pet_events:cmd+=['--translations','translations/roll_pet_events_ko.json']
    elif a.roll_pet_tournament:cmd+=['--translations','translations/roll_pet_tournament_ko.json']
    elif a.roll_pet_keyquest:cmd+=['--translations','translations/roll_pet_keyquest_ko.json']
    elif a.roll_pet_incident:cmd+=['--translations','translations/roll_pet_incident_ko.json']
    elif a.roll_pet_license:cmd+=['--translations','translations/roll_pet_license_ko.json']
    elif a.roll_pet_talk:cmd+=['--translations','translations/roll_pet_talk_ko.json']
    if a.roll_subjects:cmd+=['--translations','translations/roll_subjects_ko.json']
    elif a.roll_food:cmd+=['--translations','translations/roll_food_ko.json']
    elif a.roll_family_siblings:cmd+=['--translations','translations/roll_family_siblings_ko.json']
    elif a.roll_family_sisters:cmd+=['--translations','translations/roll_family_sisters_ko.json']
    elif a.roll_family_sister:cmd+=['--translations','translations/roll_family_sister_ko.json']
    if a.roll_fortune_complete:cmd+=['--translations','translations/roll_fortune_complete_ko.json']
    elif a.roll_minigame_rewards:cmd+=['--translations','translations/roll_minigame_rewards_ko.json']
    elif a.roll_minigame_results:cmd+=['--translations','translations/roll_minigame_results_ko.json']
    elif a.roll_fortune_results:cmd+=['--translations','translations/roll_fortune_results_ko.json']
    elif a.roll_fortune:cmd+=['--translations','translations/roll_fortune_intro_blue_ko.json']
    cmd+=['--chip-library','--chip-word-copy','--chip-cache','--chip-burst-copy','--chip-library-late-wait','--chip-folder','--chip-folder-owner-guard','--mono-font-poc','--chip-battle-names','--chip-name-translations','translations/library_chip_names_batch08_ko.json','--chip-secondary-name-translations','translations/chip_secondary_names_ko.json','--pet-menu-graphics','--folder-labels','--equipment-labels','--equipment-guides','--equipment-weapons','--equipment-attack-caption','--roll-equipment-guides','--work',a.work,'--out',a.out]
    if a.roll_dialogue_chip_name:cmd+=['--roll-dialogue-chip-name']
    if a.gutsman_pet_chipquest:cmd+=['--gutsman-dialogue-chip-name']
    if a.calendar_frequency_graphics:cmd+=['--calendar-frequency-graphics']
    if a.calendar_presets_poc:cmd+=['--calendar-presets-poc']
    if a.hangul_keyboard_glyphs:cmd+=['--hangul-keyboard-glyphs']
    if a.title_menu_graphics:cmd+=['--title-menu-graphics']
    if a.title_weekend_menu:cmd+=['--title-weekend-menu']
    if a.save_surface:cmd+=['--save-title-graphics']
    if a.keyitem_empty:
        if not a.gutsman_calendar_inventory:raise ValueError('keyitem empty requires retained possessions chain')
        cmd+=['--translations','translations/keyitem_empty_ko.json']
    if a.keyitem_rom_translations:
        if not (a.keyitem_empty and a.possessions_statistics):raise ValueError('keyitem ROM requires latest possessions baseline')
        cmd+=['--keyitem-rom-translations',a.keyitem_rom_translations]
    if a.native_keyboard_labels:cmd+=['--native-keyboard-labels']
    if a.navi_card_graphics:cmd+=['--navi-card-graphics']
    if a.mail_rom_reader:cmd+=['--mail-rom-reader']
    if a.full_mail_body:
        if not a.news_mail or not a.mail_rom_reader:raise ValueError('full mail clone requires bounded news and ROM reader')
        from full_mail_body import prepare
        cmd+=['--full-mail-body',prepare()]
    if a.full_mail_header and not a.news_mail:raise ValueError('full mail header requires bounded news mail selection')
    if a.mission_mail_header:
        if not a.full_mail_header:raise ValueError('mission header requires retained story header')
        from mission_mail_header import prepare as prepare_mission
        cmd+=['--translations',prepare_mission()]
    if a.startup_ui:
        from startup_ui import prepare,prepare_followups
        cmd+=['--translations',prepare()]
        for path in prepare_followups():cmd+=['--translations',path]
    if a.pending_batch500:
        if not a.mission_mail_header or not a.full_mail_body:raise ValueError('500 requires cumulative header/body recipe')
        from batch500_rom import prepare as prepare500
        cmd+=['--pending-batch500']
        for path in prepare500():cmd+=['--translations',path]
    if a.first_mail or a.official_mail or a.news_mail:
        from first_mail import prepare
        for path in prepare('news' if a.news_mail else a.official_mail,a.full_mail_header):cmd+=['--translations',path]
    if a.pending_batch500_002:
        if not a.pending_batch500:raise ValueError('Batch002 requires preserved batch001')
        from batch500_002_rom import prepare as prepare500_002
        cmd+=['--pending-batch500-002']
        for path in prepare500_002():cmd+=['--translations',path]
    if a.pending_batch500_003:
        if not a.pending_batch500_002:raise ValueError('Batch003 requires cumulative002')
        from batch500_003_rom import prepare as prepare500_003
        cmd+=['--pending-batch500-003']
        for path in prepare500_003():cmd+=['--translations',path]
    if a.pending_batch500_004:
        if not a.pending_batch500_003:raise ValueError('Batch004 requires cumulative003')
        from batch500_004_rom import prepare as prepare500_004
        cmd+=['--pending-batch500-004']
        for path in prepare500_004():cmd+=['--translations',path]
    if a.pending_batch500_005:
        if not a.pending_batch500_004:raise ValueError('Batch005 requires cumulative004')
        from batch500_005_rom import prepare as prepare500_005
        cmd+=['--pending-batch500-005']
        for path in prepare500_005():cmd+=['--translations',path]
    if a.pending_batch500_006:
        if not a.pending_batch500_005:raise ValueError('Batch006 requires cumulative005')
        from batch500_006_rom import prepare as prepare500_006
        cmd+=['--pending-batch500-006']
        for path in prepare500_006():cmd+=['--translations',path]
    if a.pending_batch500_007:
        if not a.pending_batch500_006:raise ValueError('Cumulative007 requires retained006')
        from cumulative_batch500 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        for i,path in zip(indexes,replace_paths([cmd[i] for i in indexes])):cmd[i]=path
        cmd+=['--pending-batch500-007']
    if a.pending_batch500_008:
        if not a.pending_batch500_007:raise ValueError('Cumulative008 requires retained007')
        from cumulative_batch500_008 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        for i,path in zip(indexes,replace_paths([cmd[i] for i in indexes])):cmd[i]=path
        cmd+=['--pending-batch500-008']
    if a.pending_batch500_009:
        if not a.pending_batch500_008:raise ValueError('Cumulative009 requires retained008')
        from cumulative_batch500_009 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        for i,path in zip(indexes,replace_paths([cmd[i] for i in indexes])):cmd[i]=path
        cmd+=['--pending-batch500-009']
    if a.pending_batch500_010:
        if not a.pending_batch500_009:raise ValueError('Cumulative010 requires retained009')
        from cumulative_batch500_010 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-010']
    if a.pending_batch500_011:
        if not a.pending_batch500_010:raise ValueError('Cumulative011 requires retained010')
        from cumulative_batch500_011 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-011']
    if a.pending_batch500_012:
        if not a.pending_batch500_011:raise ValueError('Cumulative012 requires retained011')
        from cumulative_batch500_012 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-012']
    if a.pending_batch500_013:
        if not a.pending_batch500_012:raise ValueError('Cumulative013 requires retained012')
        from cumulative_batch500_013 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        for i,path in zip(indexes,replace_paths([cmd[i] for i in indexes])):cmd[i]=path
        cmd+=['--pending-batch500-013']
    if a.pending_batch500_014:
        if not a.pending_batch500_013:raise ValueError('Cumulative014 requires retained013')
        from cumulative_batch500_014 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-014']
    if a.pending_batch500_015:
        if not a.pending_batch500_014:raise ValueError('Cumulative015 requires retained014')
        from cumulative_batch500_015 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-015']
    if a.pending_batch500_016:
        if not a.pending_batch500_015:raise ValueError('Cumulative016 requires retained015')
        from cumulative_batch500_016 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-016']
    if a.pending_batch500_017:
        if not a.pending_batch500_016:raise ValueError('Cumulative017 requires retained016')
        from cumulative_batch500_017 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-017']
    if a.pending_batch500_018:
        if not a.pending_batch500_017:raise ValueError('Cumulative018 requires retained017')
        from cumulative_batch500_018 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-018']
    if a.pending_batch500_019:
        if not a.pending_batch500_018:raise ValueError('Cumulative019 requires retained018')
        from cumulative_batch500_019 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-019']
    if a.pending_batch500_020:
        if not a.pending_batch500_019:raise ValueError('Cumulative020 requires retained019')
        from cumulative_batch500_020 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-020']
    if a.pending_batch500_021:
        if not a.pending_batch500_020:raise ValueError('Cumulative021 requires retained020')
        from cumulative_batch500_021 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-021']
    if a.pending_batch500_022:
        if not a.pending_batch500_021:raise ValueError('Cumulative022 requires retained021')
        from cumulative_batch500_022 import prepare,replace_paths
        prepare()
        indexes=[i+1 for i,v in enumerate(cmd) if v=='--translations']
        retained=[cmd[i] for i in indexes];updated=replace_paths(retained)
        for i,path in zip(indexes,updated[:len(retained)]):cmd[i]=path
        for path in updated[len(retained):]:cmd+=['--translations',path]
        cmd+=['--pending-batch500-022']
    if len(subprocess.list2cmdline(cmd))>24000:
        from build_arguments import save
        from pathlib import Path
        argument_path=ROOT/'poc/build_arguments'/(Path(a.out).stem+'.json')
        digest=save(argument_path,cmd[4:])
        cmd=cmd[:4]+['--argument-file',str(argument_path.relative_to(ROOT)),'--argument-file-sha256',digest]
    return subprocess.call(cmd,cwd=ROOT)

if __name__=='__main__':raise SystemExit(main())
