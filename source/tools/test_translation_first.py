"""Fail-closed authored draft tests; no build, save, or gameplay writes."""
import copy,json,re,unittest
from build_visibility_poc import ROOT,sha
from prepare_translation_first import check_draft
from verify_tpi_index import parse_tpi
from tpl_literals import literals
import draft_remaining_navi_save as save
import draft_tournament_dialogue as tournament
import draft_protoman_missions as missions
import draft_story_mail as mail
import draft_starman_fortune as fortune
import draft_gold_bbs as bbs
import draft_battle_bbs as battle
import draft_plaza_npcs as plaza
import draft_mystery_data as mystery
import draft_official_prelim as prelim
import draft_blackworks_routes as blackworks
import draft_official_entry as entry
import draft_undernet_routes as under
import draft_hard_access_tests as hard
import draft_profile_editor as profile
import draft_everyday_venue as venue
import draft_appliance_routes as appliance
import draft_golf_routes as golf
import draft_car_garden_routes as car
import draft_background_venue as background
import draft_factory_heel_routes as heel
import draft_napalm_media_market as media
import draft_homepage_organ_routes as organ
import draft_fallen_dark_routes as dark
import draft_windman_field_routes as field
import draft_navi_rewards_strengthening as rewards
import draft_virus_practice_routes as practice
import draft_shademan_coffin as coffin
import draft_shademan_victory as victory
import draft_laserman_encounter as laser
import draft_laserman_aftermath as aftermath
import draft_bass_encounter as bass
import draft_bass_victory as basswin
import draft_profile_data_manager as manager
import draft_credits as credits
import draft_minigame_results as miniresult
import draft_schedule_reminders as reminder
import draft_mail_alerts as alert
import draft_quick_box_routes as quick
import draft_progress_roll_menu as hintmenu
import draft_remaining_roll_profile as rollprofile
import draft_quick_results_guts_reminders as quickresult
import draft_windman_menu_remaining as windmenu
import draft_quick_wind_routes as windquick
import draft_batch500_001 as batch500
import draft_batch500_002 as batch500b
import draft_batch500_003 as batch500c
import draft_batch500_004 as batch500d
import draft_batch500_005 as batch500e
import draft_batch500_006 as batch500f
import draft_batch500_007 as batch500g
import draft_batch500_008 as batch500h
import draft_batch500_009 as batch500i
import draft_batch500_010 as batch500j
import draft_batch500_011 as batch500k
import draft_batch500_012 as batch500l
import draft_batch500_013 as batch500m
import draft_batch500_014 as batch500n
import draft_batch500_015 as batch500o
import draft_batch500_016 as batch500p
import draft_batch500_017 as batch500q
import draft_batch500_018 as batch500r
import draft_batch500_019 as batch500s
import draft_batch500_020 as batch500t
import draft_batch500_021 as batch500u
import draft_batch500_022 as batch500v
import draft_batch500_023 as batch500w
import draft_batch500_024 as batch500x
import draft_batch500_025 as batch500y
import draft_batch500_026 as batch500z
import draft_batch500_027 as batch500aa
import draft_batch500_028 as batch500ab
import draft_batch500_029 as batch500ac
import draft_batch500_030 as batch500ad
import draft_batch500_031 as batch500ae
import draft_batch500_032 as batch500af
import draft_batch500_033 as batch500ag
import draft_batch500_034 as batch500ah
import draft_batch500_035 as batch500ai
import draft_batch500_036 as batch500aj
import draft_batch500_037 as batch500ak
import draft_batch500_038 as batch500al
import draft_batch500_039 as batch500am
import draft_batch500_040 as batch500an
import draft_batch500_041 as batch500ao
import draft_batch500_042 as batch500ap
import draft_batch500_043 as batch500aq
import draft_batch500_044 as batch500ar
import draft_batch500_045 as batch500as
import draft_batch500_046 as batch500at
import draft_final_047 as final047


class TranslationFirstTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
        cls.catalog=json.loads((ROOT/cls.plan['source_inventory']['path']).read_text(encoding='utf8'))
        cls.base={u['id']:u for u in cls.catalog['units']}
        cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
        cls.rom=(ROOT/cfg['source_profile']['filename']).read_bytes()
        cls.rows={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
        cls.available={int(x.split()[1]) for x in (ROOT/cfg['development_dependencies']['font']['path']).read_text(encoding='utf8').splitlines() if x.startswith('ENCODING ')}
        cls.assets=[save.create(),tournament.create(),missions.create(),mail.create(),fortune.create(),bbs.create(),battle.create(),plaza.create(),mystery.create(),prelim.create(),blackworks.create('7AF6D0'),blackworks.create('7B09F4'),entry.create('7B1FF4'),entry.create('7B0638'),*[under.create(a) for a in under.SOURCES],*[hard.create(a) for a in hard.SOURCES],profile.create(),*[venue.create(a) for a in venue.SOURCES],*[appliance.create(a) for a in appliance.SOURCES],*[golf.create(a) for a in golf.SOURCES],*[car.create(a) for a in car.SOURCES],*[background.create(a) for a in background.SOURCES],*[heel.create(a) for a in heel.SOURCES],*[media.create(a) for a in media.SOURCES],*[organ.create(a) for a in organ.SOURCES],*[dark.create(a) for a in dark.SOURCES],*[field.create(a) for a in field.SOURCES],*[rewards.create(a) for a in rewards.SOURCES],*[practice.create(a) for a in practice.SOURCES],*[coffin.create(a) for a in coffin.SOURCES],*[victory.create(a) for a in victory.SOURCES],*[laser.create(a) for a in laser.SOURCES],*[aftermath.create(a) for a in aftermath.SOURCES],*[bass.create(a) for a in bass.SOURCES],*[basswin.create(a) for a in basswin.SOURCES],*[manager.create(a) for a in manager.SOURCES],*[credits.create(a) for a in credits.SOURCES],*[miniresult.create(a) for a in miniresult.SOURCES],*[reminder.create(a) for a in reminder.SOURCES],*[alert.create(a) for a in alert.SOURCES],*[quick.create(a) for a in quick.SOURCES],*[hintmenu.create(a) for a in hintmenu.SOURCES],*[rollprofile.create(a) for a in rollprofile.SOURCES],*[quickresult.create(a) for a in quickresult.SOURCES],*[windmenu.create(a) for a in windmenu.SOURCES],*[windquick.create(a) for a in windquick.SOURCES],*[batch500.create(a) for a in batch500.SOURCES],*[batch500b.create(a) for a in batch500b.SOURCES],*[batch500c.create(a) for a in batch500c.SOURCES],*[batch500d.create(a) for a in batch500d.SOURCES],*[batch500e.create(a) for a in batch500e.SOURCES],*[batch500f.create(a) for a in batch500f.SOURCES]]

        cls.assets.extend(batch500g.create(a) for a in batch500g.SOURCES)
        cls.assets.extend(batch500h.create(a) for a in batch500h.SOURCES)
        cls.assets.extend(batch500i.create(a) for a in batch500i.SOURCES)
        cls.assets.extend(batch500j.create(a) for a in batch500j.SOURCES)
        cls.assets.extend(batch500k.create(a) for a in batch500k.SOURCES)
        cls.assets.extend(batch500l.create(a) for a in batch500l.SOURCES)
        cls.assets.extend(batch500m.create(a) for a in batch500m.SOURCES)
        cls.assets.extend(batch500n.create(a) for a in batch500n.SOURCES)
        cls.assets.extend(batch500o.create(a) for a in batch500o.SOURCES)
        cls.assets.extend(batch500p.create(a) for a in batch500p.SOURCES)
        cls.assets.extend(batch500q.create(a) for a in batch500q.SOURCES)
        cls.assets.extend(batch500r.create(a) for a in batch500r.SOURCES)
        cls.assets.extend(batch500s.create(a) for a in batch500s.SOURCES)
        cls.assets.extend(batch500t.create(a) for a in batch500t.SOURCES)
        cls.assets.extend(batch500u.create(a) for a in batch500u.SOURCES)
        cls.assets.extend(batch500v.create(a) for a in batch500v.SOURCES)
        cls.assets.extend(batch500w.create(a) for a in batch500w.SOURCES)
        cls.assets.extend(batch500x.create(a) for a in batch500x.SOURCES)
        cls.assets.extend(batch500y.create(a) for a in batch500y.SOURCES)
        cls.assets.extend(batch500z.create(a) for a in batch500z.SOURCES)
        cls.assets.extend(batch500aa.create(a) for a in batch500aa.SOURCES)
        cls.assets.extend(batch500ab.create(a) for a in batch500ab.SOURCES)
        cls.assets.extend(batch500ac.create(a) for a in batch500ac.SOURCES)
        cls.assets.extend(batch500ad.create(a) for a in batch500ad.SOURCES)
        cls.assets.extend(batch500ae.create(a) for a in batch500ae.SOURCES)
        cls.assets.extend(batch500af.create(a) for a in batch500af.SOURCES)
        cls.assets.extend(batch500ag.create(a) for a in batch500ag.SOURCES)
        cls.assets.extend(batch500ah.create(a) for a in batch500ah.SOURCES)
        cls.assets.extend(batch500ai.create(a) for a in batch500ai.SOURCES)
        cls.assets.extend(batch500aj.create(a) for a in batch500aj.SOURCES)
        cls.assets.extend(batch500ak.create(a) for a in batch500ak.SOURCES)
        cls.assets.extend(batch500al.create(a) for a in batch500al.SOURCES)
        cls.assets.extend(batch500am.create(a) for a in batch500am.SOURCES)
        cls.assets.extend(batch500an.create(a) for a in batch500an.SOURCES)
        cls.assets.extend(batch500ao.create(a) for a in batch500ao.SOURCES)
        cls.assets.extend(batch500ap.create(a) for a in batch500ap.SOURCES)
        cls.assets.extend(batch500aq.create(a) for a in batch500aq.SOURCES)
        cls.assets.extend(batch500ar.create(a) for a in batch500ar.SOURCES)
        cls.assets.extend(batch500as.create(a) for a in batch500as.SOURCES)
        cls.assets.extend(batch500at.create(a) for a in batch500at.SOURCES)
        cls.assets.extend(final047.create(a) for a in final047.SOURCES)










    def test_batch500af_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-032']
        self.assertEqual([a['archive'] for a in aa],['7AB4B4','7A5604','7A4A8C'])
        self.assertEqual([len(a['units']) for a in aa],[325,134,41])
        self.assertEqual(self.plan['draft_assets'][-393:-390],[v[2] for v in batch500af.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-16]
        self.assertEqual(b['id'],'batch500-032');self.assertEqual(b['player_choices'],66)
        self.assertEqual(b['punctuation_literals'],8);self.assertFalse(b['rom_applied'])
        self.assertEqual(batch500af.EXCLUDED,set())

    def test_batch500af_choices_portraits_and_padding(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-032']
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),66)
        for k in batch500af.CHOICES:
            self.assertEqual(u[k]['speaker'],'player-choice')
            src=u[k]['source'];dst=u[k]['translation']
            self.assertEqual(len(src)-len(src.rstrip(' ')),len(dst)-len(dst.rstrip(' ')))
        self.assertEqual(u['7AB4B4:16:1']['speaker'],'NormalNaviYellow')
        self.assertEqual(u['7AB4B4:26:1']['speaker'],'HeelNaviPurple')
        self.assertEqual(u['7AB4B4:36:2']['speaker'],'NaviGirlOrange')
        self.assertIsNone(u['7AB4B4:20:4']['origin_portrait'])
        self.assertIsNone(u['7AB4B4:221:0']['origin_portrait'])

    def test_batch500af_gold_criteria_and_fragment_fee(self):
        a=batch500af.create('7AB4B4');u={x['id']:x for x in a['units']}
        self.assertIn('30초 이내',u['7AB4B4:16:7']['translation'])
        self.assertIn('레벨8 이상',u['7AB4B4:26:7']['translation'])
        self.assertIn('칩을 얻',u['7AB4B4:36:5']['translation'])
        self.assertIn('20개',u['7AB4B4:5:9']['translation'])
        self.assertEqual(u['7AB4B4:10:4']['translation'],'」\n소지하고 계신가요?')
        t=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(t,r'checkTakeBugFrags\s+amount = 20')
        self.assertRegex(t,r'startWindManMinigame\s+hard = false')
        self.assertNotIn('7AB4B4:10:3',u)
        self.validate(a)

    def test_batch500af_silver_fees_and_directions(self):
        a=batch500af.create('7A5604');u={x['id']:x for x in a['units']}
        self.assertIn('500제니',u['7A5604:0:4']['translation'])
        self.assertIn('690z',u['7A5604:5:4']['translation'])
        self.assertIn('인터넷2',u['7A5604:6:2']['translation'])
        self.assertIn('인터넷1',u['7A5604:6:6']['translation'])
        self.assertTrue(u['7A5604:70:0']['translation'].endswith('\n'))
        self.assertTrue(u['7A5604:70:1']['translation'].startswith('!\n'))
        self.assertEqual(u['7A5604:74:0']['speaker'],'Roll')
        self.validate(a)

    def test_batch500af_friday_poems_animation_and_timing(self):
        a=batch500af.create('7A4A8C');u={x['id']:x for x in a['units']}
        dots=['30:3','30:4','70:4','70:5','71:3','71:4','71:5']
        for k in dots:self.assertEqual(u['7A4A8C:'+k]['translation'],'.')
        for k in ('70:7','71:7'):
            x=u['7A4A8C:'+k]
            self.assertEqual(x['translation'].count('\n'),2)
            self.assertTrue(all(line.startswith(' ') for line in x['translation'].split('\n')[1:]))
        self.assertIn('금요일',u['7A4A8C:21:0']['translation'])
        self.assertIn('토요일',u['7A4A8C:90:1']['translation'])
        t=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(len(re.findall(r'wait\s+frames = 20',t)),8)
        self.validate(a)

    def test_batch500af_reproducible_and_not_release(self):
        for archive,(_,count,path) in batch500af.SOURCES.items():
            a=batch500af.create(archive)
            self.assertEqual(json.loads((ROOT/path).read_text(encoding='utf8')),a)
            self.assertEqual(len(a['units']),count);self.assertFalse(a['review']['release_eligible'])
            self.assertTrue(all(x['state']=='needs_review' for x in a['units']))
            self.validate(a)

    def test_batch500ae_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-031']
        self.assertEqual([a['archive'] for a in aa],['7C416C','7C5CE0','776650','7B0328'])
        self.assertEqual([len(a['units']) for a in aa],[172,141,184,3])
        self.assertEqual(self.plan['draft_assets'][-397:-393],[v[2] for v in batch500ae.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-17]
        self.assertEqual(b['id'],'batch500-031');self.assertEqual(b['player_choices'],126)
        self.assertEqual(b['punctuation_reaction_literals'],2);self.assertFalse(b['rom_applied'])
        self.assertEqual(batch500ae.EXCLUDED,{'7C416C:1:0','7C416C:1:1'})

    def test_batch500ae_choices_padding_and_context(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-031']
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),126)
        for k in batch500ae.CHOICES:
            self.assertEqual(u[k]['speaker'],'player-choice')
            src=u[k]['source'];target=u[k]['translation']
            self.assertEqual(len(src)-len(src.rstrip(' ')),len(target)-len(target.rstrip(' ')))
        self.assertEqual(u['7B0328:0:0']['speaker'],'HeelNaviPurple')

    def test_batch500ae_knight_nickname_and_held_placeholder(self):
        a=batch500ae.create('7C416C');u={x['id']:x for x in a['units']}
        self.assertTrue(u['7C416C:3:0']['translation'].startswith('님께서'))
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),40)
        self.assertFalse(set(u)&batch500ae.EXCLUDED)
        self.validate(a)

    def test_batch500ae_bass_reactions_and_choices(self):
        a=batch500ae.create('7C5CE0');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7C5CE0:10:1']['translation'],'...!!')
        self.assertEqual(u['7C5CE0:19:0']['translation'],'......')
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),40)
        self.validate(a)

    def test_batch500ae_communication_inherited_speakers_and_after_end(self):
        a=batch500ae.create('776650');u={x['id']:x for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),46)
        for root in range(0,92,4):
            for s in (root+1,root+2):
                x=u[f'776650:{s}:0']
                self.assertEqual(x['speaker'],u[f'776650:{root}:0']['speaker'])
                self.assertIsNone(x['origin_portrait'])
                self.assertIn('inherited from script',x['speaker_evidence'])
            self.assertIn('저장',u[f'776650:{root+2}:0']['translation'])
        self.assertEqual(u['776650:42:0']['translation'].count('\n'),2)
        self.assertFalse(any(x['source']=='4' for x in a['units']))
        self.validate(a)

    def test_batch500ae_reproducible_drafts_not_release(self):
        for archive,(_,count,path) in batch500ae.SOURCES.items():
            a=batch500ae.create(archive)
            self.assertEqual(json.loads((ROOT/path).read_text(encoding='utf8')),a)
            self.assertEqual(len(a['units']),count);self.assertFalse(a['review']['release_eligible'])
            self.assertTrue(all(x['state']=='needs_review' for x in a['units']))
            self.validate(a)

    def test_batch500ad_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-030']
        self.assertEqual([a['archive'] for a in aa],['71A66C','7C2954','7A9EE4'])
        self.assertEqual([len(a['units']) for a in aa],[218,212,70])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-400:-397],[v[2] for v in batch500ad.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-18]
        self.assertEqual(b['id'],'batch500-030');self.assertEqual(b['player_choices'],12)
        self.assertEqual(b['animated_punctuation_literals'],2)
        self.assertFalse(b['rom_applied']);self.assertEqual(batch500ad.EXCLUDED,set())

    def test_batch500ad_choices_portraits_and_hidden_reward_givers(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-030']
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),12)
        for k in batch500ad.CHOICES:
            self.assertEqual(u[k]['speaker'],'player-choice')
            if self.base[k]['source'].endswith('  '):self.assertTrue(u[k]['translation'].endswith('  '))
        for k in ('7:0','7:1','7:2','7:3','11:0','11:1','11:2','12:0','12:1','12:2','13:0','13:1','13:2'):
            self.assertEqual(u['71A66C:'+k]['speaker'],'mission-reward-giver-unestablished')
            self.assertIsNone(u['71A66C:'+k]['origin_portrait'])
        for k in ('7:4','11:3','12:3','13:3'):self.assertEqual(u['71A66C:'+k]['speaker'],'NapalmMan')
        for k in ('11:4','12:4','12:5','13:4','13:5'):
            self.assertEqual(u['71A66C:'+k]['speaker'],'reward-narration')
            self.assertEqual(u['71A66C:'+k]['portrait_visibility'],'hidden')
        for k,v in (('23:0','OfficialNavi'),('23:2','ShadowMan'),('23:3','OfficialNavi'),('39:0','ShadowMan'),('39:1','HeelNaviPurple'),('39:2','ShadowMan'),('39:3','HeelNaviPurple'),('39:5','ShadowMan')):
            self.assertEqual(u['7C2954:'+k]['speaker'],v)
        self.assertNotIn('7C2954:14:0',u)

    def test_batch500ad_napalm_controls_limits_and_reward_buffers(self):
        d=batch500ad.DRAFT['71A66C']
        for k,v in (('0:2','십자버튼'),('0:3','A버튼'),('0:5','B버튼'),('0:7','R버튼'),('0:8','A버튼'),('0:11','게이지는 0'),('14:2','40'),('18:2','45'),('22:4','50'),('26:4','55'),('27:2','55'),('30:0','40'),('31:0','55'),('27:7','심판'),('18:6','동료'),('19:7','부하')):
            self.assertIn(v,d[k])
        for n in range(14,29):
            text='\n'.join(v for k,v in d.items() if k.startswith(str(n)+':'))
            self.assertIn('60초',text);self.assertIn('5초',text)
        self.assertEqual(d['12:4'],'네이팜맨은');self.assertEqual(d['12:5'],'제니를\n얻었다!')
        self.assertTrue(d['13:4'].endswith('\n'));self.assertEqual(d['13:5'],'개 얻었다!')
        s=(ROOT/'analysis/full_scope_v1/source_tpl/71A66C.tpl').read_text(encoding='utf-8-sig')
        for v in ('item = 33','buffer = 3','minLength = 1','amount = 4294967295','frames = 50','flag = 6191'):
            self.assertIn(v,s)
        self.assertEqual(s.count('amount = 4294967295'),2)
        self.assertEqual(s.count('select\n'),3)

    def test_batch500ad_shadow_mission_roles_and_afterend(self):
        d=batch500ad.DRAFT['7C2954']
        s=(ROOT/'analysis/full_scope_v1/source_tpl/7C2954.tpl').read_text(encoding='utf-8-sig')
        for v in ('storeGlobal16','global = 16','value = 513','flag = 6049','flag = 7701'):
            self.assertEqual(s.count(v),32)
        for k,v in (('23:2','변장'),('25:5','진짜'),('33:1','150000'),('33:2','가짜'),('37:2','1명'),('37:4','모른다'),('39:3','바로 나다'),('39:4','동생'),('39:5','의뢰인이 누구든')):
            self.assertIn(v,d[k])
        for n,k in ((29,'29:5'),(37,'37:7'),(37,'37:8')):
            literal=next(x for x in literals(s) if x.key=='7C2954:'+k)
            self.assertIn('\tend',s[s.index('script '+str(n)+' '):literal.start])
            self.assertIn(k,d)
        self.assertIn('있다니께',d['40:1']);self.assertNotIn('startBattle',s)

    def test_batch500ad_npcs_battle_chipgate_flags_and_dots(self):
        d=batch500ad.DRAFT['7A9EE4']
        for k,v in (('0:1','인터넷7'),('0:2','인터넷8'),('1:0','인터넷9'),('1:1','관리'),('30:0','드르렁'),('43:0','100만'),('44:1','100만'),('50:2','사용 횟수'),('50:3','회복'),('62:0','셰이드맨'),('105:1','명령이 없는 한')):
            self.assertIn(v,d[k])
        for k in ('60:1','60:2'):self.assertEqual(d[k],'.')
        s=(ROOT/'analysis/full_scope_v1/source_tpl/7A9EE4.tpl').read_text(encoding='utf-8-sig')
        for v in ('navi = 20','jumpIfTrue = 44','width = 11','width = 9','value = 146','value = 41','value = 42','value = 1803','flag = 1806','callClearBattleChipGateHistory','track = 154'):
            self.assertIn(v,s)
        self.assertEqual(s.count('frames = 30'),3)
        scripts={int(m.group(1)):m.group(2) for m in re.finditer(r'script (\d+) \w+ \{(.*?)(?=\nscript |\Z)',s,re.S)}
        first=[2,6,10,14,18,22,26,30,34,38,42,46,50,62,66,70,74,78,82,86,90]
        second=[1,5,9,13,17,21,25,29,33,37,41,45,49,61,65,69,73,77,81,85,89]
        for n,target in ((60,62),(100,102),(103,105)):
            branches=re.findall(r'checkFlag\s+flag = (\d+)\s+jumpIfTrue = (\d+)',scripts[n])
            self.assertEqual(branches,[(str(v),str(target)) for v in first]+[(str(v),str(target-1)) for v in second])
        self.assertNotIn('chipGive',scripts[50]);self.assertNotIn('checkGiveZenny',scripts[50])

    def test_batch500ad_complete_validation_and_reproduction(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-030'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            self.assertEqual(json.loads((ROOT/batch500ad.SOURCES[a['archive']][2]).read_text(encoding='utf8')),a)
            self.assertFalse(a['review']['release_eligible'])

    def test_batch500ac_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-029']
        self.assertEqual([a['archive'] for a in aa],['707450','707C30','79E148','79975C'])
        self.assertEqual([len(a['units']) for a in aa],[191,191,68,50])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-404:-400],[v[2] for v in batch500ac.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-19]
        self.assertEqual(b['id'],'batch500-029');self.assertEqual(b['player_choices'],100)
        self.assertEqual(b['animated_punctuation_literals'],2)
        self.assertFalse(b['rom_applied']);self.assertEqual(batch500ac.EXCLUDED,set())

    def test_batch500ac_shop_choices_portraits_and_source_equivalence(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-029']
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),100)
        for k in batch500ac.CHOICES:
            self.assertEqual(u[k]['speaker'],'player-choice')
            if self.base[k]['source'].endswith('  '):self.assertTrue(u[k]['translation'].endswith('  '))
        self.assertEqual(u['707450:0:0']['origin_portrait'],'PurpleNavi')
        self.assertEqual(u['707C30:0:0']['origin_portrait'],'NormalNaviPink')
        for a in ('707450','707C30'):
            for k in ('4:0','14:0','15:0','17:0'):self.assertNotIn(a+':'+k,u)
            for k in ('13:0','18:0','21:0','24:0'):
                self.assertEqual(u[a+':'+k]['speaker'],'shop-system-message')
                self.assertIsNone(u[a+':'+k]['origin_portrait'])
            self.assertEqual(u[a+':100:1']['origin_portrait'],'NumberMan')
        d=batch500ac.DRAFT['707450']
        self.assertEqual(d,batch500ab.DRAFT['706498'])
        for k in d:self.assertEqual(self.base['707450:'+k]['source'],self.base['706498:'+k]['source'])

    def test_batch500ac_exchange_payment_and_native_controls(self):
        d=batch500ac.DRAFT['707C30']
        self.assertFalse(any('제니' in v or '구입' in v or '구매' in v for v in d.values()))
        for n in (6,7,12,19,20,23,31,32,35,41,42,45,51,52,55,61,62,65,71,72,75,81,82,85,91,92,95,101,102,105,111,112,115,121,122,125,131,132,135,141,142,145,151,152,155,161,162,165,171,172,175,181,182,185,191,192,195,201,202,205,211,212,215,221,222,225):
            self.assertIn('교환',d[f'{n}:1'])
        for n in (8,21,33,43,53,63,73,83,93,103,113,123,133,143,153,163,173,183,193,203,213,223):
            self.assertIn('「버그 조각」',d[f'{n}:0'])
        self.assertEqual(d['13:0'],'개');self.assertEqual(d['24:0'],'장')
        self.assertFalse(d['111:1'].endswith('...'));self.assertEqual(d['141:1'],d['145:1'])
        self.assertTrue(d['63:0'].startswith(',\n'))
        for a in ('707450','707C30'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            self.assertEqual(len(re.findall(r'(?m)^\s*select\s*$',s)),25)
            for v in ('width = 8','disableB = true','disableB = false','printItem','printChip','printNaviCustProgram','printPlayerNickname','minLength = 6','jumpIfFalse = 230','jumpIfFalse = 235'):
                self.assertIn(v,s)
            self.assertEqual(s.count('soundDisableChoiceSFX'),3 if a=='707C30' else 2)

    def test_batch500ac_thursday_context_portraits_and_animated_dots(self):
        a=next(a for a in self.assets if a['archive']=='79E148')
        u={x['id'].split(':',1)[1]:x for x in a['units']}
        d=batch500ac.DRAFT['79E148']
        for k,v in (('60:0','NormalNaviYellow'),('60:2','NormalNaviPink'),('60:3','NormalNaviYellow'),('61:1','NormalNaviPink'),('61:2','NormalNaviYellow')):
            self.assertEqual(u[k]['speaker'],v);self.assertEqual(u[k]['origin_portrait'],v)
        for k in ('0:3','0:4'):self.assertEqual(d[k],'.')
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(s.count('frames = 10'),3)
        self.assertEqual(s.count('checkNetTime'),12)
        self.assertEqual(s.count('upperHour = 25'),2);self.assertIn('upperHour = 29',s)
        for k,v in (('0:6','초록색'),('20:0','목요일'),('23:1','금요일'),('30:0','한 아이'),('32:0','유치원'),('60:4','「디스코드」'),('70:0','1개'),('71:0','「블라인드」'),('80:1','나무 속성')):
            self.assertIn(v,d[k])
        self.assertNotIn('우리 가족',d['30:2'])
        self.assertNotIn('itemGive',s)

    def test_batch500ac_security_unlock_and_debris_reward_routes(self):
        a=next(a for a in self.assets if a['archive']=='79975C')
        u={x['id'].split(':',1)[1]:x for x in a['units']}
        for k,v in (('4:0','NumberMan'),('5:0','ProtoMan'),('6:0','ShadowMan')):
            self.assertEqual(u[k]['speaker'],v)
        for k in ('7:0','7:1'):
            self.assertEqual(u[k]['speaker'],'security-system-message')
            self.assertEqual(u[k]['portrait_visibility'],'hidden')
        for k in ('0:0','1:0','10:2','14:2'):self.assertEqual(u[k]['speaker'],'scene-narration')
        d=batch500ac.DRAFT['79975C'];self.assertIn('밀서',d['6:1'])
        for n in (10,11,12,13,14,15):self.assertTrue(d[f'{n}:2'].startswith(','))
        self.assertIn('1개',d['16:2']);self.assertIn('2개',d['17:2'])
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for v in ('navi = 8','navi = 7','navi = 16','jumpIfTrue = 4','jumpIfTrue = 5','jumpIfTrue = 6','flag = 861','item = 7','jumpIfContents8 = 17','chip = 29','chip = 49','chip = 135','chip = 133','amount = 240','amount = 430','buffer = 3'):
            self.assertIn(v,s)
        self.assertEqual(s.count('code = A'),4)
        self.assertEqual(s.count('animation = 24'),8);self.assertEqual(s.count('animation = 25'),8)
        self.assertNotIn('itemTake',s)

    def test_batch500ac_complete_validation_and_reproduction(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-029'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            self.assertEqual(json.loads((ROOT/batch500ac.SOURCES[a['archive']][2]).read_text(encoding='utf8')),a)
            self.assertFalse(a['review']['release_eligible'])

    def test_batch500ab_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-028']
        self.assertEqual([a['archive'] for a in aa],['706498','706C78','79D650','701ED8','78B6F4'])
        self.assertEqual([len(a['units']) for a in aa],[191,191,51,65,2])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-409:-404],[v[2] for v in batch500ab.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-20]
        self.assertEqual(b['id'],'batch500-028');self.assertEqual(b['player_choices'],100)
        self.assertFalse(b['rom_applied']);self.assertEqual(batch500ab.EXCLUDED,set())
        self.assertTrue(all(a['archive']!='7794EC' for a in aa))

    def test_batch500ab_choices_portraits_and_held_slots(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-028']
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),100)
        for k in batch500ab.CHOICES:self.assertEqual(u[k]['speaker'],'player-choice')
        for a in ('706498','706C78'):
            for k in ('4:0','5:0','14:0','15:0','17:0'):self.assertNotIn(a+':'+k,u)
            for k in ('13:0','18:0','19:1','21:0','24:0'):
                self.assertEqual(u[a+':'+k]['speaker'],'shop-system-message')
                self.assertIsNone(u[a+':'+k]['origin_portrait'])
            self.assertEqual(u[a+':100:0']['origin_portrait'],'NumberMan')
            self.assertEqual(u[a+':100:1']['origin_portrait'],'NumberMan')
            self.assertEqual(u[a+':100:1']['translation'],'예  ')
        self.assertEqual(u['706498:0:0']['origin_portrait'],'NormalNaviYellow')
        self.assertEqual(u['706C78:0:0']['origin_portrait'],'HeelNaviBlack')
        for n in range(13,48):self.assertNotIn(f'701ED8:{n}:0',u)
        self.assertTrue(all(x['speaker']=='bbs-post-author-unestablished' for x in aa[3]['units']))
        self.assertTrue(all(x['speaker']=='SearchMan' for x in aa[4]['units']))

    def test_batch500ab_shop_native_controls_and_source_reuse(self):
        for a in ('706498','706C78'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            self.assertEqual(len(re.findall(r'(?m)^\s*select\s*$',s)),25)
            for tok in ('@size 230','width = 8','disableB = true','disableB = false','printItem','printChip','printNaviCustProgram','printPlayerNickname','minLength = 6','jumpIfFalse = 230','jumpIfFalse = 235'):
                self.assertIn(tok,s)
            self.assertEqual(batch500ab.DRAFT[a]['13:0'],'개')
            self.assertEqual(batch500ab.DRAFT[a]['24:0'],'장')
            for k in batch500ab.CHOICES:
                if k.startswith(a+':') and self.base[k]['source'].endswith('  '):
                    self.assertTrue(batch500ab.DRAFT[a][k[len(a)+1:]].endswith('  '))
        lhs=batch500ab.DRAFT['706498'];rhs=batch500ab.DRAFT['706C78']
        changed={k for k in lhs if lhs[k]!=rhs[k]}
        self.assertEqual(changed,{'0:0','1:0','3:0','4:1','5:1','10:0','11:1'})
        for k in lhs:
            if k not in changed:self.assertEqual(self.base['706498:'+k]['source'],self.base['706C78:'+k]['source'])
        self.assertIn('감사',lhs['10:0']);self.assertIn('미안',rhs['10:0'])
        self.assertIn('거스',lhs['41:1']);self.assertIn('퓨',lhs['131:1'])
        self.assertTrue(lhs['63:0'].startswith(',\n'))
        self.assertNotEqual(lhs['141:1'],lhs['145:1'])

    def test_batch500ab_timed_npc_roles_and_portrait_changes(self):
        a=next(a for a in self.assets if a['archive']=='79D650')
        u={x['id'].split(':',1)[1]:x for x in a['units']}
        for k,v in (('60:0','NormalNaviYellow'),('60:1','NormalNaviPink'),('60:2','NormalNaviYellow'),('61:1','NormalNaviPink'),('61:2','NormalNaviYellow')):
            self.assertEqual(u[k]['speaker'],v);self.assertEqual(u[k]['origin_portrait'],v)
        d=batch500ab.DRAFT['79D650']
        for k,v in (('0:1','실직'),('20:2','퇴치'),('30:0','3명'),('32:2','유치원'),('60:3','「흡입」'),('61:2','「응원가」'),('90:1','오퍼레이터')):
            self.assertIn(v,d[k])
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(s.count('upperHour = 25'),2)
        self.assertEqual(s.count('upperMinutes = 25'),2)
        self.assertNotIn('itemGive',s);self.assertNotIn('itemTake',s)

    def test_batch500ab_bbs_semantics_and_search_warning(self):
        d=batch500ab.DRAFT['701ED8']
        for k,v in (('0:0','이나리'),('3:4','여성 전용'),('4:6','버그 조각'),('4:7','1번'),('7:1','같은 내비'),('7:2','강해져'),('8:4','언더인터넷4'),('9:3','무사C'),('10:1','셰이드맨'),('11:3','목적')):
            self.assertIn(v,d[k])
        s=(ROOT/'analysis/full_scope_v1/source_tpl/701ED8.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(s.count('palette = 9'),13)
        self.assertEqual(s.count('left = 32'),48);self.assertEqual(s.count('left = 202'),48)
        self.assertNotIn('mugshotShow',s);self.assertNotIn('startBattle',s)
        w=batch500ab.DRAFT['78B6F4'];self.assertIn('측정할 수 없는',w['0:0']);self.assertIn('주의',w['0:1'])

    def test_batch500ab_complete_validation_and_reproduction(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-028'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            self.assertEqual(json.loads((ROOT/batch500ab.SOURCES[a['archive']][2]).read_text(encoding='utf8')),a)
            self.assertFalse(a['review']['release_eligible'])

    def test_batch500aa_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-027']
        self.assertEqual([a['archive'] for a in aa],['67D708','683054','6999F4','7028FC'])
        self.assertEqual([len(a['units']) for a in aa],[135,132,174,59])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-413:-409],[v[2] for v in batch500aa.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-21]
        self.assertEqual(b['id'],'batch500-027');self.assertEqual(b['player_choices'],72)
        self.assertFalse(b['rom_applied'])

    def test_batch500aa_choices_unknown_speakers_and_held_labels(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-027']
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(batch500aa.EXCLUDED,set())
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),72)
        for k in batch500aa.CHOICES:
            self.assertEqual(u[k]['speaker'],'player-choice')
            self.assertEqual(u[k]['portrait_visibility'],'not-shown-in-script')
            self.assertIsNone(u[k]['origin_portrait'])
        for a in aa[:3]:
            self.assertTrue(all(x['origin_portrait'] is None for x in a['units']))
            self.assertEqual(sum(x['speaker']=='player-choice' for x in a['units']),24)
            self.assertTrue(all(x['speaker'] in ('player-choice','quick-box-speaker-unestablished') for x in a['units']))
        self.assertTrue(all(x['speaker']=='bbs-post-author-unestablished' for x in aa[3]['units']))
        for k in ('67D708:15:2','67D708:27:0','67D708:29:0'):self.assertNotIn(k,u)
        for s in range(13,48):
            k=f'7028FC:{s}:0';self.assertNotIn(k,u);self.assertIn('BBS',self.base[k]['source'])
        for a in aa:self.assertFalse(a['review']['release_eligible'])

    def test_batch500aa_native_registration_and_blanklines(self):
        for a in ('67D708','683054','6999F4'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            self.assertNotIn('mugshotShow',s)
            self.assertEqual(len(re.findall(r'(?m)^\s*select\s*$',s)),12)
            for t in ('variable = 22','value = 1','jumpIfEqual = 19','variable = 23','jumpIfEqual = 33','jumpIfEqual = 34','printStringBuffer1','printStringBuffer2','printStringBuffer3','count = 16','count = 24','flag = 3585','flag = 3605','flag = 3606','flag = 3735','flag = 3749'):
                self.assertIn(t,s)
            d=batch500aa.DRAFT[a]
            for k in batch500aa.CHOICES:
                if k.startswith(a+':') and self.base[k]['source'].endswith('  '):
                    self.assertTrue(d[k[len(a)+1:]].endswith('  '))
            for i in (41,44,47,50,53,56,59,62):
                self.assertEqual(d[f'{i}:0'].count('\n'),2)
                self.assertTrue(d[f'{i}:0'].endswith('\n'))
        d=batch500aa.DRAFT['683054'];self.assertTrue(d['31:2'].startswith('\n'))

    def test_batch500aa_profile_voice_and_nonmechanical_claims(self):
        e=batch500aa.DRAFT['67D708'];p=batch500aa.DRAFT['683054'];w=batch500aa.DRAFT['6999F4']
        for k,t in (('1:0','전기를'),('15:0','쟁취'),('25:4','아니다'),('31:3','한다면'),('83:1','농담'),('93:1','개성'),('94:0','외쳐라')):
            self.assertIn(t,e[k])
        for k,t in (('17:3','여자'),('19:3','남자'),('80:0','부럽'),('81:1','아무것도'),('86:1','도전')):
            self.assertIn(t,p[k])
        for k,t in (('11:1','물양갱'),('13:2','수영'),('15:4','태평양'),('17:8','거리'),('19:8','거리'),('25:3','일본, 샘물 여행'),('27:4','해 보고 싶어'),('29:4','해 보고 싶어'),('31:0','샤워 세트'),('31:1','되면 좋겠어'),('82:0','나도 누나'),('89:1','들어 본 적 없어')):
            self.assertIn(t,w[k])
        self.assertIn('아직',w['17:5']);self.assertIn('아직',w['19:5'])

    def test_batch500aa_bbs_posts_progression_and_native_consumer(self):
        d=batch500aa.DRAFT['7028FC']
        for k,t in (('3:1','다크로이드'),('4:1','관'),('5:3','랭크'),('6:1','건 델 솔'),('7:1','태양소년'),('8:3','규칙'),('9:3','벌써'),('9:4','헛수고'),('10:1','신참'),('11:0','1체'),('12:0','에리어4'),('12:5','있다더군')):
            self.assertIn(t,d[k])
        self.assertEqual(d['3:3'].split('\n')[0][-1],' ')
        s=(ROOT/'analysis/full_scope_v1/source_tpl/7028FC.tpl').read_text(encoding='utf-8-sig')
        self.assertNotIn('mugshotShow',s);self.assertNotIn('storeGlobal',s);self.assertNotIn('shop',s)
        self.assertEqual(s.count('palette = 9'),13)
        self.assertEqual(s.count('left = 32'),48);self.assertEqual(s.count('top = 68'),48)
        self.assertEqual(s.count('left = 202'),48);self.assertEqual(s.count('top = 108'),48)
        self.assertIn('BBS00 ID0D',s);self.assertIn('BBS03 ID13',s)

    def test_batch500aa_complete_validation_and_reproduction(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-027'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            self.assertEqual(json.loads((ROOT/batch500aa.SOURCES[a['archive']][2]).read_text(encoding='utf8')),a)

    def test_batch500z_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-026']
        self.assertEqual([len(a['units']) for a in aa],[211,194,67,28])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-417:-413],[v[2] for v in batch500z.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-22]
        self.assertEqual(b['id'],'batch500-026');self.assertEqual(b['player_choices'],4)
        self.assertFalse(b['rom_applied'])

    def test_batch500z_held_errors_other_slots_and_choices(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-026']
        ids={u['id'] for a in aa for u in a['units']}
        self.assertEqual(batch500z.EXCLUDED,{'6842F8:0:0','69B134:0:0'})
        for k in batch500z.EXCLUDED:
            self.assertNotIn(k,ids);self.assertIn('エラー',self.base[k]['source'])
        for a in aa[:2]:
            self.assertTrue(all(u['origin_portrait'] is None and u['speaker']=='quick-box-speaker-unestablished' for u in a['units']))
        for k in ('6842F8:8:2','6842F8:26:0','6842F8:29:0','6842F8:45:0','6842F8:49:0','6842F8:51:0','6842F8:53:0','6842F8:54:0','6842F8:58:0','6842F8:69:0','6842F8:71:0','69B134:43:1','69B134:45:0','69B134:54:1','69B134:61:0','69B134:83:0'):
            self.assertNotIn(k,ids)
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),4)
        for k in batch500z.CHOICES:
            self.assertEqual(u[k]['speaker'],'player-choice')
            self.assertEqual(u[k]['portrait_visibility'],'hidden')
            self.assertIsNone(u[k]['origin_portrait'])
        for a in aa:self.assertFalse(a['review']['release_eligible'])

    def test_batch500z_profile_semantics_and_variables(self):
        p=batch500z.DRAFT['6842F8'];w=batch500z.DRAFT['69B134']
        for key,t in (('3:0','1명'),('27:2','사랑의 카운터'),('29:3','베어'),('53:4','2명'),('57:1','L버튼, R버튼'),('83:1','3번째'),('87:0','1가지')):
            self.assertIn(t,p[key])
        for key,t in (('15:1','좋다나'),('27:0','수조'),('30:2','수신 거부'),('39:1','존경을'),('46:2','누군가'),('59:0','R버튼'),('82:0','물기'),('90:1','수조'),('91:0','탁해져')):
            self.assertIn(t,w[key])
        self.assertLess(w['59:0'].index('R버튼'),w['59:0'].index('L버튼'))
        for arch in ('6842F8','69B134'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{arch}.tpl').read_text(encoding='utf-8-sig')
            for t in ('printDream','printWish','printCrush','printPlayerEnemy','printLostToOpponent','printDefeatedOpponent','printMostLostToOpponentsChip','printMostDefeatedOpponentsChip','printFavStandardChip3'):
                self.assertIn(t,s)
            self.assertNotIn('mugshotShow',s)
        s=(ROOT/'analysis/full_scope_v1/source_tpl/6842F8.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(s.count('callCheckDefinedMPChip1'),2)
        self.assertEqual(s.count('jumpIfUndefined = 63'),2)
        s=(ROOT/'analysis/full_scope_v1/source_tpl/69B134.tpl').read_text(encoding='utf-8-sig')
        self.assertIn('callBufferRandomFriend',s);self.assertIn('jumpIfUndefined = 19',s)

    def test_batch500z_internet_numberman_native_routes(self):
        a=next(a for a in self.assets if a['archive']=='79F30C')
        u={x['id']:x for x in a['units']}
        for k,p in (('0:0','MrProgGreen'),('4:0','OfficialNavi'),('10:0','MrProgGreen'),('20:0','NormalNaviBrown'),('30:0','NumberMan'),('33:0','NumberMan'),('34:0','NumberMan')):
            self.assertEqual(u['79F30C:'+k]['origin_portrait'],p)
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(len(re.findall(r'(?m)^\s*checkNetTime\s*$',s)),8)
        self.assertEqual(len(re.findall(r'(?m)^\s*checkNetDateWeekday\s*$',s)),5)
        for t in ('navi = 8','jumpIfTrue = 34','lowerHour = 24','upperHour = 29','upperMinutes = 59','value = 136','value = 31','value = 32','value = 1793','flag = 1806','flag = 7701'):
            self.assertIn(t,s)
        self.assertEqual(s.count('jump = 33,'),2);self.assertEqual(s.count('jump = continue'),4)
        d=batch500z.DRAFT['79F30C']
        self.assertEqual((d['30:3'],d['34:5']),('예  ','예  '))
        self.assertEqual((d['30:4'],d['34:6']),('아니요','아니요'))
        self.assertIn('계산 실수',d['31:1']);self.assertIn('넘버맨식',d['33:0'])
        self.assertIn('입니댜',d['10:1']);self.assertIn('계단',d['10:2'])
        self.assertIn('토요일',d['26:2']);self.assertIn('예약 녹화',d['26:4'])

    def test_batch500z_weekday_poetry_time_and_portraits(self):
        a=next(a for a in self.assets if a['archive']=='7A47A0')
        u={x['id']:x for x in a['units']}
        for k,p in (('30:0','NormalNaviYellow'),('70:0','NormalNaviBrown'),('71:0','NormalNaviBrown'),('90:0','NormalNaviPink')):
            self.assertEqual(u['7A47A0:'+k]['origin_portrait'],p)
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(len(re.findall(r'(?m)^\s*checkNetTime\s*$',s)),3)
        self.assertEqual(s.count('frames = 20'),6)
        d=batch500z.DRAFT['7A47A0']
        for k in ('70:3','70:4','70:5','71:4','71:5','71:6'):self.assertEqual(d[k],'·')
        self.assertIn('첫 경기',d['30:0']);self.assertIn('120',d['32:0'])
        self.assertIn('토요일과 일요일 밤',d['71:1'])
        self.assertIn('프로그램 커플',d['71:2']);self.assertIn('초록색',d['90:1'])
        for k in ('70:7','71:8'):
            self.assertEqual(d[k].count('\n '),2)

    def test_batch500z_complete_validation_and_reproduction(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-026'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            self.assertEqual(json.loads((ROOT/batch500z.SOURCES[a['archive']][2]).read_text(encoding='utf8')),a)

    def test_batch500y_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-025']
        self.assertEqual([len(a['units']) for a in aa],[213,211,49,27])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-421:-417],[v[2] for v in batch500y.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-23]['id'],'batch500-025')
        self.assertFalse(self.plan['batch_policy']['completed_batches'][-23]['rom_applied'])

    def test_batch500y_held_errors_other_slots_and_portraits(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-025']
        ids={u['id'] for a in aa for u in a['units']}
        self.assertEqual(batch500y.EXCLUDED,{'69561C:0:0','67EA58:0:0'})
        for k in batch500y.EXCLUDED:
            self.assertNotIn(k,ids);self.assertIn('エラー',self.base[k]['source'])
        for a in aa[:2]:
            self.assertTrue(all(u['origin_portrait'] is None and u['speaker']=='quick-box-speaker-unestablished' for u in a['units']))
        self.assertEqual(sum(u['speaker']=='player-choice' for a in aa for u in a['units']),0)
        for k in ('69561C:2:0','69561C:26:3','69561C:38:1','69561C:43:1','69561C:46:2','69561C:49:1','69561C:55:1','69561C:73:0','67EA58:5:0','67EA58:55:0'):
            self.assertNotIn(k,ids)
        for a in aa:self.assertFalse(a['review']['release_eligible'])

    def test_batch500y_profile_semantics_and_variables(self):
        j=batch500y.DRAFT['69561C'];e=batch500y.DRAFT['67EA58']
        self.assertIn('아마',j['15:4']);self.assertIn('착각',j['35:4'])
        self.assertIn('농담',j['54:4']);self.assertIn('L버튼',j['62:2'])
        self.assertIn('허리',j['90:3']);self.assertIn('무서워',j['89:1'])
        self.assertIn('무리',e['13:2']);self.assertIn('입을',e['15:3'])
        self.assertIn('느낌',e['31:2']);self.assertIn('아니냐',e['45:3'])
        self.assertIn('두 배',e['49:4']);self.assertIn('기분',e['49:4'])
        self.assertIn('1위',e['74:3']);self.assertIn('산초',e['82:0'])
        for arch in ('69561C','67EA58'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{arch}.tpl').read_text(encoding='utf-8-sig')
            for t in ('printDream','printWish','printCrush','printPlayerEnemy','printLostToOpponent','printDefeatedOpponent','printMostLostToOpponentsChip','printMostDefeatedOpponentsChip','printFavStandardChip3'):
                self.assertIn(t,s)
            self.assertNotIn('mugshotShow',s)

    def test_batch500y_daily_npc_portraits_and_time(self):
        a=next(a for a in self.assets if a['archive']=='79D108')
        u={x['id']:x for x in a['units']}
        for k,p in (('0:0','MrProgGreen'),('20:0','PurpleNavi'),('30:0','NormalNaviPink'),('40:0','HeelNaviPurple'),('50:0','NormalNaviBrown'),('80:0','NaviGirlOrange'),('90:0','HeelNaviPurple')):
            self.assertEqual(u['79D108:'+k]['origin_portrait'],p)
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(len(re.findall(r'(?m)^\s*checkNetTime\s*$',s)),10)
        for t in ('lowerHour = 24','upperHour = 29','upperMinutes = 59','lowerMinutes = 15','lowerMinutes = 20','lowerMinutes = 40','frames = 10'):
            self.assertIn(t,s)
        d=batch500y.DRAFT['79D108']
        self.assertEqual((d['0:2'],d['0:3']),('.','.'))
        self.assertIn('엄마',d['30:0']);self.assertIn('남편',d['30:1'])
        self.assertIn('유치원',d['32:2']);self.assertIn('목수',d['90:1'])
        self.assertIn('갤럭티카',d['40:2'])

    def test_batch500y_saturday_comedy_and_midnight(self):
        a=next(a for a in self.assets if a['archive']=='7A1170')
        u={x['id']:x for x in a['units']}
        for k,p in (('0:0','NaviGirlOrange'),('30:0','OfficialNavi'),('50:0','NormalNaviBrown'),('60:0','PurpleNavi')):
            self.assertEqual(u['7A1170:'+k]['origin_portrait'],p)
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(len(re.findall(r'(?m)^\s*checkNetTime\s*$',s)),5)
        for t in ('lowerHour = 24','upperHour = 28','upperMinutes = 15','lowerMinutes = 45','upperMinutes = 50'):
            self.assertIn(t,s)
        d=batch500y.DRAFT['7A1170']
        self.assertIn('엉뚱한 말',d['30:2']);self.assertIn('딴지',d['30:2'])
        self.assertIn('PET',d['30:3']);self.assertIn('검은 녀석',d['50:0'])
        self.assertIn('토요일',d['61:0']);self.assertIn('12시',d['61:1'])
        self.assertIn('일요일',d['61:1'])

    def test_batch500y_complete_validation_and_reproduction(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-025'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            self.assertEqual(json.loads((ROOT/batch500y.SOURCES[a['archive']][2]).read_text(encoding='utf8')),a)

    def test_batch500x_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-024']
        self.assertEqual([len(a['units']) for a in aa],[219,215,66])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-424:-421],[v[2] for v in batch500x.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-24]['id'],'batch500-024')
        self.assertFalse(self.plan['batch_policy']['completed_batches'][-24]['rom_applied'])

    def test_batch500x_held_errors_portrait_and_choices(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-024']
        ids={u['id'] for a in aa for u in a['units']}
        for k in batch500x.EXCLUDED:
            self.assertNotIn(k,ids);self.assertIn('エラー',self.base[k]['source'])
        for a in aa:
            self.assertTrue(all(u['origin_portrait'] is None and u['portrait_visibility']=='not-shown-in-script' for u in a['units']))
            self.assertFalse(a['review']['release_eligible'])
        self.assertEqual(sum(u['speaker']=='player-choice' for a in aa for u in a['units']),20)
        for a in aa[:2]:
            self.assertTrue(all(u['speaker']=='quick-box-speaker-unestablished' for u in a['units']))

    def test_batch500x_profile_semantics_and_variables(self):
        w=batch500x.DRAFT['6A0640'];i=batch500x.DRAFT['6C40AC']
        self.assertIn('입술',w['13:2']);self.assertIn('배처럼',w['14:2'])
        self.assertIn('나한테',w['27:3']);self.assertIn('넷 배틀',w['30:2'])
        self.assertIn('모르겠다',w['38:2']);self.assertIn('안 될',w['42:2'])
        self.assertIn('2시간',w['18:0']);self.assertIn('1장 1장',w['78:0'])
        self.assertIn('아이스맨',i['9:1']);self.assertIn('플러그 아웃',i['8:1'])
        self.assertIn('좋아하는 분',i['19:1']);self.assertIn('원래 빨갛',i['27:4'])
        self.assertIn('프리즈 봄',i['59:3']);self.assertIn('통째로',i['61:2'])
        for arch in ('6A0640','6C40AC'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{arch}.tpl').read_text(encoding='utf-8-sig')
            for t in ('printDream','printWish','printCrush','printPlayerEnemy','printMostLostToOpponent','printMostLostToOpponentsChip','printDefeatedOpponent','printMostDefeatedOpponentsChip','printFavStandardChip3'):
                self.assertIn(t,s)
            self.assertNotIn('mugshotShow',s)

    def test_batch500x_trader_quantities_and_branch_controls(self):
        s=(ROOT/'analysis/full_scope_v1/source_tpl/6FE8D4.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(len(re.findall(r'(?m)^\s*option\s*$',s)),20)
        for t in ('amount = 3','amount = 10','startBugFragTrader','jumpIfNotEnoughBugFrags = 16','flag = 1760','flag = 1759','amount = 4294967295','buffer = 1','buffer = 3','jumpIfEqual = 27','jumpIfEqual = 28','jumpIfNone = 29','jumpIfSome = 29'):
            self.assertIn(t,s)
        d=batch500x.DRAFT['6FE8D4']
        for k in batch500x.CHOICES:
            self.assertEqual(d[k],'네  ' if d[k].endswith('  ') else '아니요')
        self.assertIn('3장',d['0:0']);self.assertIn('10장',d['6:0']);self.assertIn('10개',d['12:1'])
        self.assertTrue(d['28:0'].endswith(' '));self.assertEqual(d['16:0'],'버그 조각이')

    def test_batch500x_prizes_capacity_and_narration(self):
        d=batch500x.DRAFT['6FE8D4']
        self.assertIn('우승',d['26:0']);self.assertIn('제니',d['26:2'])
        for k in ('3:2','9:2','15:3','27:2'):self.assertIn('칩 데이터',d[k])
        for k in ('13:0','24:0','25:0'):self.assertIn('부족',d[k])
        self.assertIn('가득',d['29:0']);self.assertNotIn('부족',d['29:0'])
        self.assertIn('융합',d['15:1']);self.assertEqual(d['31:0'].count('\n'),2)

    def test_batch500x_complete_validation_and_reproduction(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-024'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            path=batch500x.SOURCES[a['archive']][2]
            self.assertEqual(json.loads((ROOT/path).read_text(encoding='utf8')),a)

    def test_batch500w_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-023']
        self.assertEqual([len(a['units']) for a in aa],[222,225,53])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-427:-424],[v[2] for v in batch500w.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-25]['id'],'batch500-023')
        self.assertFalse(self.plan['batch_policy']['completed_batches'][-25]['rom_applied'])

    def test_batch500w_held_errors_and_nonjapanese(self):
        ids={u['id'] for a in self.assets if a.get('batch_id')=='batch500-023' for u in a['units']}
        self.assertEqual(batch500w.EXCLUDED,{'6ACCA8:0:0','673770:0:0'})
        for k in batch500w.EXCLUDED:
            self.assertNotIn(k,ids);self.assertIn('エラー',self.base[k]['source'])
        for k in ('6ACCA8:25:3','6ACCA8:31:1','6ACCA8:34:0','6ACCA8:79:0','6ACCA8:89:0','673770:2:0','673770:49:1'):
            self.assertNotIn(k,ids)

    def test_batch500w_portrait_identity_and_choices(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-023']
        for a in aa[:2]:
            self.assertTrue(all(u['origin_portrait'] is None and u['speaker']=='quick-box-speaker-unestablished' for u in a['units']))
        d={u['id']:u for u in aa[2]['units']}
        for k,portrait in [('0:0','MrProgGreen'),('10:0','NormalNaviYellow'),('20:0','PurpleNavi'),('30:0','NormalNaviPink'),('80:0','NaviGirlOrange'),('90:0','HeelNaviPurple')]:
            self.assertEqual(d['79E890:'+k]['origin_portrait'],portrait)
        for k in ('10:1','10:2'):
            self.assertEqual(d['79E890:'+k]['speaker'],'player-choice');self.assertEqual(d['79E890:'+k]['portrait_visibility'],'hidden')

    def test_batch500w_friday_time_and_battle_controls(self):
        s=(ROOT/'analysis/full_scope_v1/source_tpl/79E890.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(len(re.findall(r'(?m)^\s*checkNetTime\s*$',s)),9)
        for token in ('lowerMinutes = 15','upperMinutes = 30','lowerMinutes = 20','lowerMinutes = 40','upperMinutes = 59','width = 8','default = 0','jump = 11','value = 149','value = 12','value = 13','value = 627','flag = 1806','flag = 7701'):
            self.assertIn(token,s)
        d=batch500w.DRAFT['79E890']
        self.assertEqual(d['10:1'],'네  ');self.assertEqual(d['10:2'],'아니요')
        self.assertIn('금요일',d['10:0']);self.assertIn('금요일',d['21:0']);self.assertIn('금요일',d['90:1'])
        self.assertIn('다음 주',d['3:1']);self.assertIn('아이',d['32:1'])

    def test_batch500w_profile_semantics_and_variables(self):
        n=batch500w.DRAFT['6ACCA8'];p=batch500w.DRAFT['673770']
        self.assertIn('10년',n['14:1']);self.assertIn('1명',n['19:2']);self.assertIn('병량환',n['13:1'])
        self.assertIn('손으로',n['25:5']);self.assertIn('보장',n['26:3']);self.assertIn('평생',n['42:3'])
        self.assertIn('R버튼',n['61:0']);self.assertIn('L버튼',n['63:0']);self.assertIn('R버튼',n['63:0'])
        self.assertIn('가능성',p['26:4']);self.assertIn('잘못',p['27:2']);self.assertIn('1번째',p['85:2'])
        for a in ('6ACCA8','673770'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            for t in ('printDream','printWish','printMostLostToOpponentsChip','printDefeatedOpponent','printMostDefeatedOpponentsChip','printFavStandardChip3'):
                self.assertIn(t,s)
        s=(ROOT/'analysis/full_scope_v1/source_tpl/673770.tpl').read_text(encoding='utf-8-sig')
        self.assertIn('printMostLostToOpponent',s);self.assertIn('printMostDefeatedOpponent',s)

    def test_batch500w_complete_validation(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-023'):
            self.assertEqual(len(self.validate(a)),len(a['units']))

    def test_batch500v_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-022']
        self.assertEqual([len(a['units']) for a in aa],[264,225,11])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-430:-427],[v[2] for v in batch500v.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-26]['id'],'batch500-022')
        self.assertFalse(self.plan['batch_policy']['completed_batches'][-26]['rom_applied'])

    def test_batch500v_held_errors_and_nonjapanese(self):
        ids={u['id'] for a in self.assets if a.get('batch_id')=='batch500-022' for u in a['units']}
        self.assertEqual(batch500v.EXCLUDED,{'6B8478:0:0','679424:0:0'})
        for k in batch500v.EXCLUDED:
            self.assertNotIn(k,ids);self.assertIn('エラー',self.base[k]['source'])
        for k in ('6B8478:7:0','6B8478:8:0','6B8478:27:0','6B8478:50:0','6B8478:55:0','6B8478:69:0','679424:6:3','679424:7:1','679424:21:1','679424:53:0','679424:57:0','679424:69:2'):
            self.assertNotIn(k,ids)

    def test_batch500v_no_portrait_identity_guess(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-022']
        for a in aa:
            self.assertTrue(all(u['origin_portrait'] is None and u['portrait_visibility']=='not-shown-in-script' for u in a['units']))
            self.assertFalse(a['review']['release_eligible'])
        for a in aa[:2]:
            self.assertTrue(all(u['speaker']=='quick-box-speaker-unestablished' for u in a['units']))

    def test_batch500v_bugfrag_choice_padding_and_effects(self):
        d=batch500v.DRAFT['69360C']
        self.assertEqual(d['1:1'],'버그조각 ')
        self.assertEqual(d['1:3'],'줄게  ');self.assertEqual(d['1:4'],'싫어')
        self.assertTrue(d['1:2'].endswith('\n'))
        self.assertIn('모자라',d['2:0']);self.assertIn('힘이',d['3:3'])
        s=(ROOT/'analysis/full_scope_v1/source_tpl/69360C.tpl').read_text(encoding='utf-8-sig')
        for token in ('flag = 3585','buffer = 3','amount = 4294967295','jumpIfAll = 3','jumpIfNone = continue','jumpIfSome = continue','item = 33','amount = 1','callJunkManDailyBugFragIncrement','default = 0','jump = 2'):
            self.assertIn(token,s)
        self.assertEqual(len(re.findall(r'(?m)^\s*option\s*$',s)),2)

    def test_batch500v_profile_semantics_and_variables(self):
        a=batch500v.DRAFT['6B8478'];b=batch500v.DRAFT['679424']
        self.assertIn('매진',a['23:2']);self.assertIn('훈수',a['63:4'])
        self.assertIn('3번째',a['83:1']);self.assertIn('갑옷',a['90:0'])
        self.assertIn('우드',b['42:1']);self.assertIn('아쿠아',b['47:1'])
        self.assertIn('농담',b['26:4']);self.assertIn('농담',b['45:4'])
        self.assertIn('기억',b['77:1']);self.assertIn('위험',b['91:3'])
        for arch in ('6B8478','679424'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{arch}.tpl').read_text(encoding='utf-8-sig')
            for token in ('printDream','printWish','printMostLostToOpponent','printMostLostToOpponentsChip','printDefeatedOpponent','printMostDefeatedOpponent','printMostDefeatedOpponentsChip','printFavStandardChip3'):
                self.assertIn(token,s)

    def test_batch500v_complete_validation(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-022'):
            self.assertEqual(len(self.validate(a)),len(a['units']))

    def test_batch500u_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-021']
        self.assertEqual([len(a['units']) for a in aa],[238,241,21])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-433:-430],[v[2] for v in batch500u.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-27]['id'],'batch500-021')
        self.assertFalse(self.plan['batch_policy']['completed_batches'][-27]['rom_applied'])

    def test_batch500u_held_errors_and_unselected_quotes(self):
        ids={u['id'] for a in self.assets if a.get('batch_id')=='batch500-021' for u in a['units']}
        self.assertEqual(batch500u.EXCLUDED,{'68FB1C:0:0','6BE52C:0:0'})
        for k in batch500u.EXCLUDED:
            self.assertNotIn(k,ids);self.assertIn('エラー',self.base[k]['source'])
        for k in ('6BE52C:14:1','6BE52C:87:0','799A3C:2:0','799A3C:13:2','799A3C:14:0'):
            self.assertNotIn(k,ids)

    def test_batch500u_portraits_and_hidden_narration(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-021']
        for a in aa[:2]:
            self.assertTrue(all(u['origin_portrait'] is None and u['speaker']=='quick-box-speaker-unestablished' for u in a['units']))
        d={u['id']:u for u in aa[2]['units']}
        self.assertEqual(d['799A3C:8:0']['origin_portrait'],'WindMan')
        self.assertEqual(d['799A3C:9:0']['origin_portrait'],'Bass')
        for k in ('10:0','11:0'):
            self.assertIsNone(d['799A3C:'+k]['origin_portrait']);self.assertEqual(d['799A3C:'+k]['portrait_visibility'],'hidden')
        self.assertIn('천천히',d['799A3C:10:0']['translation']);self.assertIn('거친 힘',d['799A3C:11:0']['translation'])

    def test_batch500u_passage_flags_items_and_exception(self):
        s=(ROOT/'analysis/full_scope_v1/source_tpl/799A3C.tpl').read_text(encoding='utf-8-sig')
        for token in ('flag = 1345','flag = 1437','flag = 1460','flag = 862','item = 2','item = 19','item = 7','itemTake','amount = 1','jumpIfLess = 7','jumpIfLess = 13'):
            self.assertIn(token,s)
        d=batch500u.DRAFT['799A3C']
        self.assertIn('자격',d['0:0']);self.assertIn('예외',d['13:3']);self.assertIn('미소지',d['13:1'])
        self.assertIn('두 손',d['3:1']);self.assertIn('전용 통로',d['6:0'])

    def test_batch500u_profile_variable_roles_and_caveats(self):
        a=batch500u.DRAFT['68FB1C'];b=batch500u.DRAFT['6BE52C']
        self.assertIn('100명',a['2:0']);self.assertIn('1000명',a['2:1']);self.assertIn('100장',a['58:1'])
        self.assertIn('1장',a['86:0']);self.assertIn('미안',a['70:4']);self.assertIn('같다',a['82:3'])
        self.assertIn('3끼',b['13:1']);self.assertIn('3끼',b['13:2']);self.assertIn('가능하다면',b['31:4'])
        self.assertIn('개조',b['50:2']);self.assertIn('아닌가',b['51:3']);self.assertIn('위험',b['91:0'])
        s=(ROOT/'analysis/full_scope_v1/source_tpl/68FB1C.tpl').read_text(encoding='utf-8-sig')
        self.assertIn('callBufferRandomMPChip',s);self.assertIn('printMostLostToOpponentsChip',s);self.assertIn('printMostDefeatedOpponentsChip',s)
        s=(ROOT/'analysis/full_scope_v1/source_tpl/6BE52C.tpl').read_text(encoding='utf-8-sig')
        self.assertIn('printMostDefeatedOpponent',s);self.assertIn('printFavMegaChip',s)

    def test_batch500u_complete_validation(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-021'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
            self.assertTrue(all(u['state']=='needs_review' for u in a['units']))

    def test_batch500t_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-020']
        self.assertEqual([len(a['units']) for a in aa],[258,240,2])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-436:-433],[v[2] for v in batch500t.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-28]['id'],'batch500-020')
        self.assertFalse(self.plan['batch_policy']['completed_batches'][-28]['rom_applied'])

    def test_batch500t_held_errors_and_punctuation(self):
        ids={u['id'] for a in self.assets if a.get('batch_id')=='batch500-020' for u in a['units']}
        self.assertEqual(batch500t.EXCLUDED,{'6684B0:0:0','689DF8:0:0'})
        for k in batch500t.EXCLUDED:
            self.assertNotIn(k,ids);self.assertIn('エラー',self.base[k]['source'])
        for k in ('2:0','12:1','16:2','56:0','67:1','75:1','76:1','77:1','86:0'):
            self.assertNotIn('6684B0:'+k,ids)
        self.assertIn('6684B0:29:0',ids)

    def test_batch500t_unknown_quickbox_vs_explicit_thunder(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-020']
        for a in aa[:2]:
            self.assertTrue(all(u['origin_portrait'] is None and u['speaker']=='quick-box-speaker-unestablished' for u in a['units']))
        self.assertTrue(all(u['origin_portrait']=='ThunderMan' and u['speaker']=='ThunderMan' for u in aa[2]['units']))
        self.assertIn('거츠맨',batch500t.DRAFT['6684B0']['9:0']);self.assertIn('넘버맨',batch500t.DRAFT['689DF8']['79:2'])
        self.assertIn('방심하지',batch500t.DRAFT['78B804']['0:1'])

    def test_batch500t_number_jokes_and_pi_exact(self):
        d=batch500t.DRAFT['689DF8']
        self.assertEqual(re.findall(r'\d+',d['81:0']),['3','1415926535','897932384626','433832'])
        self.assertIn('아니에요',d['27:4']);self.assertIn('거짓말',d['29:1'])
        self.assertIn('거짓말',d['46:2']);self.assertIn('거짓말',d['47:3']);self.assertIn('거짓말',d['75:1'])
        self.assertIn('10',d['86:1']);self.assertIn('아마',d['86:2']);self.assertEqual(d['90:1'],'넘버원!!')
        self.assertIn('과목',d['13:3']);self.assertIn('먹는',d['15:1'])

    def test_batch500t_profile_variable_controls(self):
        for a in ('6684B0','689DF8'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            self.assertIn('msgOpenQuick',s);self.assertNotIn('mugshotShow',s)
            self.assertIn('printMostLostToOpponentsChip',s);self.assertIn('printMostDefeatedOpponentsChip',s)
            self.assertIn('printFavGigaChip',s);self.assertNotIn('option',s)
        s=(ROOT/'analysis/full_scope_v1/source_tpl/689DF8.tpl').read_text(encoding='utf-8-sig')
        self.assertIn('callBufferRandomMPChip',s);self.assertIn('printBestSubject',s)
        d=batch500t.DRAFT['6684B0'];self.assertIn('DHA',d['14:1']);self.assertIn('안 들었',d['14:2'])
        self.assertIn('거스',d['1:0']);self.assertEqual(d['51:0'],'거츠거츠!')

    def test_batch500t_complete_validation_and_unselected_preservation(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-020'):
            self.assertEqual(len(self.validate(a)),len(a['units']))
            self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
            self.assertTrue(all(u['state']=='needs_review' for u in a['units']))

    def test_batch500s_exact500_authority_and_no_choices(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-019'];u=[x for a in aa for x in a['units']]
        self.assertEqual(len(u),500);self.assertEqual(len({x['id'] for x in u}),500)
        self.assertEqual(self.plan['draft_assets'][-439:-436],[v[2] for v in batch500s.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-29]['id'],'batch500-019')
        self.assertFalse(any(x['speaker']=='player-choice' for x in u))
        self.assertTrue(all(x['state']=='needs_review' for x in u))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500s_name_suffixes_duplicates_and_blank_slot(self):
        a=next(x for x in self.assets if x['archive']=='767E0C');d=batch500s.DRAFT['767E0C']
        self.assertEqual(len(d),255);self.assertNotIn('127:0',d);self.assertEqual(self.base['767E0C:127:0']['source'],' ')
        self.assertEqual(self.base['767E0C:127:0']['status'],'unselected_non_japanese_review')
        for u in a['units']:
            for suffix in ('EX','V2','V3','SP','XX'):
                if u['source'].endswith(suffix):self.assertTrue(u['translation'].endswith(suffix))
            self.assertEqual(u['speaker'],'enemy-or-navi-name-label');self.assertIsNone(u['origin_portrait'])
        self.assertEqual(d['0:0'],'록맨');self.assertEqual(d['128:0'],'롤')
        self.assertEqual(d['229:0'],d['231:0']);self.assertEqual(d['231:0'],d['255:0'])
        self.assertEqual(d['230:0'],'포르테XX');self.assertEqual(d['200:0'],d['203:0'])
        self.assertEqual(d['204:0'],d['223:0']);self.assertEqual(d['207:0'],'힐 내비SP')

    def test_batch500s_name_family_order_and_existing_navi_candidates(self):
        d=batch500s.DRAFT['767E0C']
        for k,v in [('1:0','메톨'),('4:0','메톨2EX'),('6:0','메톨3EX'),('113:0','엘렘프라5'),('114:0','엘렘프라EX'),('121:0','윈드박스'),('122:0','버큠팬'),('125:0','윈드박스3'),('126:0','버큠팬3'),('176:0','탭맨'),('212:0','켄도맨')]:self.assertEqual(d[k],v)
        self.assertNotEqual(d['43:0'],d['44:0']);self.assertNotEqual(d['73:0'],d['74:0'])
        for k,v in [('136:0','윈드맨'),('140:0','서치맨'),('156:0','넘버맨'),('224:0','네이팜맨'),('232:0','스타맨'),('236:0','섀도맨')]:self.assertEqual(d[k],v)

    def test_batch500s_profile_variables_unknown_speaker_and_hypothetical_choices(self):
        a=next(x for x in self.assets if x['archive']=='6A6C64');d=batch500s.DRAFT['6A6C64'];s=(ROOT/'analysis/full_scope_v1/source_tpl/6A6C64.tpl').read_text(encoding='utf-8-sig')
        for u in a['units']:self.assertEqual(u['speaker'],'quick-box-speaker-unestablished');self.assertIsNone(u['origin_portrait'])
        self.assertNotIn('mugshotShow',s);self.assertNotIn('positionOption',s)
        for cmd in ('printSchool','printCrush','printBestSubject','printWorstSubject','printMostLostToOpponent','printMostLostToOpponentsChip','printMostDefeatedOpponent','printMostDefeatedOpponentsChip','printFavStandardChip3','printFavMegaChip','printFavGigaChip'):self.assertIn(cmd,s)
        self.assertEqual(d['21:2'],' 라는\n꿈인가?');self.assertEqual(d['38:3'],'한테\n물어보자!!')
        self.assertEqual(d['42:3'],'실력에');self.assertEqual(d['73:2'],'쪽이려나')

    def test_batch500s_jokes_forecast_caveats_and_variable_line_boundaries(self):
        d=batch500s.DRAFT['6A6C64']
        self.assertIn('농담',d['9:1']);self.assertIn('농담',d['31:2']);self.assertIn('농담',d['87:2'])
        self.assertIn('그럴지도',d['91:2']);self.assertIn('안 돼!',d['91:0']);self.assertIn('별님',d['11:1'])
        self.assertIn('효험',d['49:5']);self.assertIn('1',d['53:1']);self.assertIn('1',d['85:1']);self.assertIn('1',d['85:3'])
        for k in ('26:0','27:2','43:0','59:1'):self.assertTrue(d[k].startswith('\n'))
        for k in ('21:1','23:3','25:2','50:1','51:1','73:1','74:0','85:0'):self.assertTrue(d[k].endswith('\n'))

    def test_batch500s_dark_warning_explicit_megaman_and_preservation(self):
        a=next(x for x in self.assets if x['archive']=='78B50C');u=a['units'][0]
        self.assertEqual(u['speaker'],'MegaMan');self.assertEqual(u['origin_portrait'],'MegaMan')
        self.assertIn('어둠의 힘',u['translation']);self.assertIn('조심해서',u['translation'])
        self.assertEqual(u['translation'].count('\n'),2);self.assertEqual(batch500s.EXCLUDED,set())
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-019'):
            self.assertEqual(len(check_draft(a,self.base,self.available,self.rom,self.rows)),len(a['units']))

    def test_batch500r_exact500_authority_and_eight_choices(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-018'];u=[x for a in aa for x in a['units']]
        self.assertEqual(len(u),500);self.assertEqual(len({x['id'] for x in u}),500)
        self.assertEqual(self.plan['draft_assets'][-442:-439],[v[2] for v in batch500r.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-30]['id'],'batch500-018')
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u),8)
        self.assertTrue(all(x['state']=='needs_review' for x in u))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500r_perliteral_portraits_and_hidden_rewards(self):
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-018'):
            for u in a['units']:
                s,i=map(int,u['id'].split(':')[1:])
                if a['archive']!='71551C':
                    self.assertIsNone(u['origin_portrait']);self.assertEqual(u['speaker'],'quick-box-speaker-unestablished')
                elif u['speaker']=='player-choice':self.assertIsNone(u['origin_portrait']);self.assertEqual(u['portrait_visibility'],'hidden')
                elif s in (7,8,9):self.assertEqual(u['speaker'],'system-reward');self.assertIsNone(u['origin_portrait'])
                else:self.assertEqual(u['origin_portrait'],'WindMan' if s in (0,1,2,3,4,31,46,51,60) else 'MrProgGreen')

    def test_batch500r_wind_ritual_buttons_conditions_and_destination_distances(self):
        d=batch500r.DRAFT['71551C'];s=(ROOT/'analysis/full_scope_v1/source_tpl/71551C.tpl').read_text(encoding='utf-8-sig')
        self.assertIn('초록색',d['1:5']);self.assertIn('B버튼',d['1:6']);self.assertIn('작아지고',d['1:10'])
        self.assertIn('최대',d['1:11']);self.assertIn('A버튼',d['1:12']);self.assertIn('해방',d['1:13'])
        for k,n in [('11:0','4000'),('12:0','6200'),('13:0','7800'),('14:0','9600'),('15:0','11000'),('16:2','12300'),('17:1','13000'),('18:2','16000'),('19:4','20000'),('20:2','28000'),('21:1','33000'),('22:0','40000'),('23:1','44000'),('24:3','65000'),('25:3','70000'),('26:2','80000'),('27:2','85000'),('28:3','95000'),('29:4','100000')]:self.assertIn(n,d[k])
        self.assertIn('인터넷8',d['17:1']);self.assertIn('인터넷8',d['18:1'])
        self.assertIn('인터넷12',d['22:1']);self.assertIn('인터넷12',d['23:1'])
        self.assertIn('flag = 4954',s);self.assertIn('flag = 4955',s)

    def test_batch500r_special_doll_staged_waits_and_reward_buffers(self):
        d=batch500r.DRAFT['71551C'];s=(ROOT/'analysis/full_scope_v1/source_tpl/71551C.tpl').read_text(encoding='utf-8-sig')
        s=' '.join(s.split())
        self.assertIn('특제',d['47:2']);self.assertIn('특제',d['52:2']);self.assertIn('망가져',d['60:1'])
        self.assertEqual(d['59:3'],'마음이\n');self.assertEqual(d['59:4'],'두근\n');self.assertEqual(d['59:5'],'했어요')
        self.assertEqual(s.count('wait frames = 60'),2);self.assertEqual(s.count('buffer = 1'),2)
        self.assertEqual(s.count('buffer = 3'),2);self.assertEqual(s.count('amount = 4294967295'),2)
        self.assertIn('item = 33',s);self.assertIn('HP 메모리',d['7:0']);self.assertEqual(d['9:1'],'개 얻었다!')

    def test_batch500r_profile_variables_order_and_particle_safe_candidates(self):
        d=batch500r.DRAFT['662C5C'];s=(ROOT/'analysis/full_scope_v1/source_tpl/662C5C.tpl').read_text(encoding='utf-8-sig')
        for cmd in ('printSchool','printCrush','printFavFood','printDream','printWish','printMostLostToOpponentsChip','printFavStandardChip3','printFavMegaChip','printFavGigaChip','printString'):self.assertIn(cmd,s)
        self.assertEqual(d['26:1'],'한테');self.assertEqual(d['66:0'],'하고\n넷 배틀 하고 싶어~')
        self.assertEqual(d['71:3'],'쪽이려나\n그렇게 생각하지 않아?')
        self.assertEqual(d['92:1'],'위만\n노리다 보면,');self.assertIn('index = 121',s)
        self.assertIn('꿈',d['52:1']);self.assertIn('...아니었나?',d['74:2']);self.assertIn('선제공격',d['88:1'])

    def test_batch500r_internal_error_and_nonjapanese_fragments_preserved(self):
        self.assertEqual(batch500r.EXCLUDED,{'662C5C:0:0'});self.assertIn('エラー',self.base['662C5C:0:0']['source'])
        self.assertNotIn('0:0',batch500r.DRAFT['662C5C'])
        for k in ('1:1','25:0','48:1','59:0','71:1','78:1','88:3'):self.assertNotIn(k,batch500r.DRAFT['662C5C'])
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-018'):
            self.assertEqual(len(check_draft(a,self.base,self.available,self.rom,self.rows)),len(a['units']))

    def test_batch500q_exact500_authority_14choices_and_names(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-017'];u=[x for a in aa for x in a['units']]
        self.assertEqual(len(u),500);self.assertEqual(len({x['id'] for x in u}),500)
        self.assertEqual(self.plan['draft_assets'][-444:-442],[v[2] for v in batch500q.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-31]['id'],'batch500-017')
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u),14)
        self.assertTrue(all(x['state']=='needs_review' for x in u));self.assertTrue(all(not a['review']['release_eligible'] for a in aa))
        d=batch500q.DRAFT['778A4C'];self.assertEqual(len(d),21)
        self.assertEqual([d[f'{i}:0'] for i in (4,7,8,22)],['서치맨','브루스','넘버맨','포르테'])
        self.assertNotIn('13:0',d);self.assertNotIn('14:0',d)

    def test_batch500q_perliteral_portraits_hidden_command_and_choices(self):
        a=next(a for a in self.assets if a.get('batch_id')=='batch500-017' and a['archive']=='716DE4')
        for u in a['units']:
            sc,i=map(int,u['id'].split(':')[1:])
            hidden=sc in (1,7,76,77,78,102,117,134) or (sc==8 and i>0)
            self.assertEqual(u['portrait_visibility'],'hidden' if hidden else 'shown')
            if hidden:self.assertIsNone(u['origin_portrait'])
            elif sc<14 or sc>=79:self.assertEqual(u['origin_portrait'],'SearchMan')
            if sc in (76,77,78):self.assertEqual(u['speaker'],'system-reward' if i>=4 else 'operation-command-speaker-unestablished')
            if sc==7:self.assertEqual(u['speaker'],'operation-command-speaker-unestablished')
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('mugshot = HeelNaviBlack',s);self.assertIn('mugshot = MrProgGreen',s);self.assertIn('mugshot = NaviGirlOrange',s)

    def test_batch500q_controls_gauge_and_contact_goal_distinction(self):
        d=batch500q.DRAFT['716DE4']
        self.assertIn('십자 버튼',d['0:2']);self.assertIn('A버튼',d['0:3'])
        self.assertIn('접촉',d['0:4']);self.assertIn('저격',d['0:4'])
        self.assertIn('B버튼',d['0:5']);self.assertIn('R버튼',d['0:8'])
        self.assertIn('조금이라도',d['0:10']);self.assertIn('줄어드니',d['0:11']);self.assertIn('0',d['0:12']);self.assertIn('회복',d['0:13'])
        self.assertIn('서치 모드',d['0:7']);self.assertIn('서치 스코프',d['140:6'])
        self.assertIn('프로그램을',d['83:6']);self.assertIn('보호',d['83:6']);self.assertIn('체포',d['84:7']);self.assertIn('저격',d['92:6'])
        self.assertIn('200퍼센트',d['43:1']);self.assertIn('고소',d['32:0']);self.assertIn('완벽',d['71:1'] if '71:1' in d else d['71:0'])

    def test_batch500q_all20_briefing_time_targets_and_penalties(self):
        d=batch500q.DRAFT['716DE4']
        counts=[4,10,4,13,6,5,15,8,5,10,15,15,15,15,15,15,15,18,18,18]
        for sc,n in zip(range(79,99),counts):
            self.assertIn('60초',d[f'{sc}:1'])
            text=' '.join(t for k,t in d.items() if k.startswith(str(sc)+':'))
            self.assertIn(str(n)+('인조' if sc==87 else '체'),text)
        for sc in (79,81,83,84,86,87,88):
            text=' '.join(t for k,t in d.items() if k.startswith(str(sc)+':'))
            self.assertIn('5초가 줄어',text);self.assertIn('표적 이외',text)
        self.assertIn('검은 몸',d['79:4']);self.assertIn('움직임',d['81:5'])
        self.assertIn('가방',d['84:7']);self.assertIn('폭발하기 전에',d['84:6'])
        self.assertIn('행동 프로그램',d['87:6']);self.assertIn('버그',d['87:6'])

    def test_batch500q_test_training_polite_routes_and_redirects(self):
        d=batch500q.DRAFT['716DE4'];s=(ROOT/'analysis/full_scope_v1/source_tpl/716DE4.tpl').read_text(encoding='utf-8-sig')
        for sc in (100,101):
            self.assertIn('60초',d[f'{sc}:1']);self.assertIn('15체',d[f'{sc}:2'])
            self.assertIn('시험에 합격',d[f'{sc}:'+str(4 if sc==100 else 6)])
        for sc in range(107,117):
            self.assertIn('60초',d[f'{sc}:0']);self.assertIn(('15' if sc<=113 else '18')+'체',d[f'{sc}:1'])
            self.assertIn('60초',d[f'{sc+17}:0']);self.assertIn(('15' if sc<=113 else '18')+'체',d[f'{sc+17}:1'])
        for flag in (5114,5115,5116,5258,5259,5260,5261,5263,5264,5265,5266,5267,5268,5269,5270):
            self.assertIn(f'flag = {flag}',s)
        self.assertIn('jumpIfTrue = 134',s);self.assertIn('frames = 120',s);self.assertIn('disableB = true',s)
        self.assertIn('스카우트',d['119:2']);self.assertIn('실패',d['122:0']);self.assertIn('님의',d['137:2'])

    def test_batch500q_hidden_rewards_and_unselected_source_integrity(self):
        s=(ROOT/'analysis/full_scope_v1/source_tpl/716DE4.tpl').read_text(encoding='utf-8-sig');d=batch500q.DRAFT['716DE4']
        self.assertIn('item = 33',s);self.assertIn('amount = 1',s);self.assertEqual(s.count('amount = 4294967295'),2)
        self.assertEqual(s.count('buffer = 3'),2);self.assertEqual(s.count('padLeft = true'),2)
        self.assertIn('HP 메모리',d['76:4']);self.assertEqual(d['77:4'],'서치맨은')
        self.assertTrue(d['78:4'].endswith('\n'));self.assertEqual(d['78:5'],'개 얻었다!')
        self.assertTrue(d['7:1'].startswith('\n'));self.assertTrue(d['3:2'].startswith('\n'))
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-017'):
            self.assertEqual(len(check_draft(a,self.base,self.available,self.rom,self.rows)),len(a['units']))

    def test_batch500p_exact500_authority_and_four_choices(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-016'];u=[x for a in aa for x in a['units']]
        self.assertEqual(len(u),500);self.assertEqual(len({x['id'] for x in u}),500)
        self.assertEqual(self.plan['draft_assets'][-451:-444],[v[2] for v in batch500p.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][-32]['id'],'batch500-016')
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u),4)
        self.assertTrue(all(x['state']=='needs_review' for x in u))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500p_mailbox_portraits_global29_and_quick_routes(self):
        a=next(a for a in self.assets if a['archive']=='6DD0B8');d=batch500p.DRAFT['6DD0B8']
        portraits={10:'MegaMan',11:'MegaMan',13:'Roll',14:'Roll',16:'GutsMan',17:'GutsMan',19:'WindMan',20:'WindMan',22:'SearchMan',23:'SearchMan',24:'SearchMan',25:'FireMan',26:'FireMan',28:'ThunderMan',29:'ThunderMan',31:'ProtoMan',32:'ProtoMan',33:'ProtoMan',34:'NumberMan',35:'NumberMan',37:'MetalMan',38:'MetalMan',40:'JunkMan',41:'JunkMan',43:'AquaMan',44:'AquaMan',46:'WoodMan',47:'WoodMan',55:'StarMan',56:'StarMan',58:'ShadowMan',59:'ShadowMan',60:'ShadowMan',61:'KnightMan',62:'KnightMan',64:'NapalmMan',65:'NapalmMan',66:'NapalmMan',67:'IceMan',68:'IceMan',70:'ElecMan',71:'ElecMan',73:'PlantMan',74:'PlantMan',76:'Bass',77:'Bass'}
        for u in a['units']:
            s=int(u['id'].split(':')[1]);self.assertEqual(u['origin_portrait'],portraits.get(s))
            self.assertEqual(u['portrait_visibility'],'shown' if s in portraits else 'not-shown-in-script')
        s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('checkNaviAll',s);self.assertEqual(s.count('variable = 29'),69)
        self.assertEqual(s.count('printPlayerNickname'),3)
        self.assertEqual([d[f'{i}:0'] for i in range(6)],['일반 메일','참가 확인','오피셜 지령','암살 의뢰','임무 메일','파괴 지령'])
        self.assertIn('가스',d['102:0']);self.assertIn('뿌',d['111:0'])

    def test_batch500p_military20_routes_goals_and_location(self):
        a=next(a for a in self.assets if a['archive']=='6DF988');s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');d=batch500p.DRAFT['6DF988']
        self.assertEqual(s.count('callSearchManMissionActivate'),20)
        for i in range(20):
            self.assertIn(f'flag = {9760+i}',s);self.assertIn(f'jumpIfFalse = {32+i}',s)
            self.assertIn('작전 사령부',d[f'{32+i}:0'])
        for sc,loc in [(32,'인터넷1'),(33,'인터넷2'),(34,'인터넷3'),(35,'인터넷4'),(36,'인터넷4'),(37,'인터넷5'),(38,'인터넷6'),(39,'인터넷6'),(40,'인터넷7'),(41,'인터넷8'),(42,'인터넷9'),(43,'인터넷10'),(44,'인터넷11'),(45,'인터넷11'),(46,'인터넷12'),(47,'언더 인터넷1'),(48,'언더 인터넷2'),(49,'언더 인터넷2'),(50,'언더 인터넷3'),(51,'언더 인터넷3')]:
            self.assertIn(loc,' '.join(t for k,t in d.items() if k.startswith(str(sc)+':')))
        self.assertIn('일제 체포',d['32:1']);self.assertIn('변장',d['37:1']);self.assertIn('탈환',d['38:2'])
        self.assertIn('프로그램의 보호',d['41:3']);self.assertIn('프로그램의 보호',d['46:3'])
        self.assertIn('내비의 보호',d['51:1']);self.assertIn('파괴에는 성공',d['50:4']);self.assertIn('생겨난',d['50:5'])
        self.assertTrue(all(u['origin_portrait'] is None and u['portrait_visibility']=='inherited-from-caller' for u in a['units']))

    def test_batch500p_destruction15_conditions_private_request_and_tenyears(self):
        a=next(a for a in self.assets if a['archive']=='6E01AC');s=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');d=batch500p.DRAFT['6E01AC']
        self.assertEqual(s.count('callNapalmManMissionActivate'),15)
        for i in range(15):
            self.assertIn(f'flag = {9792+i}',s);self.assertIn(f'jumpIfFalse = {32+i}',s)
            text=' '.join(t for k,t in d.items() if k.startswith(str(32+i)+':'))
            self.assertIn('성공하면',text);self.assertIn('보상',text)
            self.assertIn(('인터넷'+str(i+1)) if i<12 else ('언더 인터넷'+str(i-11)),text)
        self.assertIn('10년',d['40:6']);self.assertIn('개인',d['41:0']);self.assertIn('꿈',d['41:9'])
        self.assertIn('양지',d['42:3']);self.assertIn('뒷세계',d['42:2']);self.assertIn('선을 지켜',d['43:7'])
        self.assertIn('탐색 프로그램',d['44:6']);self.assertIn('가장 많이',d['45:3'])
        self.assertTrue(all(u['origin_portrait'] is None for u in a['units']))

    def test_batch500p_equipment_limits_buffer_and_raw_abbreviations(self):
        for a in ('6E1068','6E12DC'):
            d=batch500p.DRAFT[a];s=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            self.assertIn('3장',d['71:0']);self.assertIn('1장',d['72:0']);self.assertIn('1장',d['73:0'])
            self.assertIn('5장',d['74:0']);self.assertIn('1장',d['75:0'])
            self.assertEqual(d['70:0'],'칩 폴더가\n');self.assertEqual(d['70:1'],'장이 아니야!')
            self.assertIn('buffer = 1',s);self.assertNotIn('30',d['70:0']+d['70:1'])
            self.assertEqual([d[f'{n}:0'] for n in (27,28,35,36)],['킹덤C','로열WB','슈팅B','D오버로드'])
            self.assertEqual(d['70:3'],'예  ');self.assertEqual(d['0:0'],'   칩 폴더');self.assertEqual(d['2:0'],'  칩 폴더   ')
            self.assertTrue(all(f'{n}:0' not in d for n in (38,39,60,61,62,63)))
            asset=next(x for x in self.assets if x.get('batch_id')=='batch500-016' and x['archive']==a)
            for u in asset['units']:
                sc=int(u['id'].split(':')[1]);self.assertEqual(u['origin_portrait'],('MegaMan' if a=='6E1068' else 'Roll') if sc>=70 else None)
            self.assertIn('width = 8',s);self.assertIn('default = 0',s)

    def test_batch500p_headers_plugin_and_unselected_preservation(self):
        d=batch500p.DRAFT['6DD864'];self.assertEqual(len(d),42)
        for i in range(20):self.assertEqual(d[f'{2*i}:0'],'작전 사령부');self.assertEqual(d[f'{2*i+1}:0'],'임무 지령')
        self.assertEqual(d['41:0'],'제목:');self.assertEqual(d['65:0'],'제목:')
        self.assertNotIn('40:0',d);self.assertNotIn('64:0',d)
        s=(ROOT/'analysis/full_scope_v1/source_tpl/677318.tpl').read_text(encoding='utf-8-sig')
        self.assertIn('flag = 3603',s);self.assertIn('flag = 3651',s);self.assertIn('frames = 30',s)
        self.assertEqual(batch500p.DRAFT['677318']['1:0'],'플러그인!\n파이어맨.EXE,\n트랜스미션!!')
        for a in (x for x in self.assets if x.get('batch_id')=='batch500-016'):
            source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');check_draft(a,self.base,self.available,self.rom,self.rows)

    def test_batch500o_exact_scope_authority_and_original_error(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-015'];u=[u for a in aa for u in a['units']]
        self.assertEqual(len(u),500);self.assertEqual(len({x['id'] for x in u}),500)
        self.assertEqual(self.plan['draft_assets'][-463:-451],[v[2] for v in batch500o.SOURCES.values()])
        self.assertEqual(batch500o.EXCLUDED,{'6D44D4:0:0'});self.assertNotIn('0:0',batch500o.DRAFT['6D44D4'])
        self.assertTrue(all(x['state']=='needs_review' for x in u));self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500o_portrait_and_hidden_mission_rewards(self):
        aa={a['archive']:a for a in self.assets if a.get('batch_id')=='batch500-015'}
        for a in aa.values():
            for u in a['units']:
                s,i=map(int,u['id'].split(':')[1:])
                self.assertEqual(u['origin_portrait'],'Bass' if a['archive']=='6D27EC' and s>=21 else None)
                self.assertNotEqual(u['speaker'],'player-choice')
                if a['archive']=='6DED88':
                    reward=s in (29,30) or (s==28 and i>0)
                    self.assertEqual(u['speaker'],'system-reward' if reward else 'mission-message-speaker-unestablished')
                    self.assertEqual(u['portrait_visibility'],'hidden' if reward else 'inherited-from-caller')

    def test_batch500o_all32_mission_destinations_deadlines(self):
        d=batch500o.DRAFT['6DED88']
        mission=[(1,60),(2,60),(3,40),(4,40),(1,40),(2,40),(3,40),(4,30),(5,50),(6,50),(7,35),(8,35),(5,35),(6,35),(7,30),(8,30),(9,40),(10,30),(11,30),(12,30),(9,30),(10,25),(11,25),(12,25),(1,30),(2,30),(3,30),(4,30),(1,20),(2,20),(3,20),(4,20)]
        for s,(area,minutes) in enumerate(mission,33):
            text=''.join(v for k,v in d.items() if int(k.split(':')[0])==s)
            self.assertIn(('언더 인터넷' if s>=57 else '인터넷')+str(area),text)
            self.assertIn(str(minutes)+'분',text);self.assertIn('성공하면',text);self.assertIn('메일',text)
        src=(ROOT/'analysis/full_scope_v1/source_tpl/6DED88.tpl').read_text(encoding='utf-8-sig')
        for n in range(1,33):self.assertIn(f'jumpIfMission{n} = {n+32}',src)
        self.assertIn('jumpIfNone = 65',src);self.assertIn('종료',d['65:0'])

    def test_batch500o_mission_target_clues_and_reward_branches(self):
        d=batch500o.DRAFT['6DED88'];s=(ROOT/'analysis/full_scope_v1/source_tpl/6DED88.tpl').read_text(encoding='utf-8-sig')
        for k,v in [('38:1','여자'),('40:5','같은 냄새'),('43:2','빨간색'),('43:3','열흘에 일할'),('48:5','검은색 힐'),('50:4','오피셜'),('53:6','죽음의 선물'),('56:3','가짜'),('57:1','검은색 소녀'),('57:4','프로그램째'),('58:3','갈색'),('60:1','초록색'),('61:4','1개'),('63:3','사투리'),('64:3','검은색 힐')]:self.assertIn(v,d[k])
        for t in ('flag = 9756','jumpIfFalse = 31','checkShadowManMissionReward','jumpIfZenny = 29','jumpIfBugFrags = 30','callShadowManMissionErase','mugshotHide','item = 33','amount = 1','amount = 4294967295','printCurrentNavi','buffer = 3'):self.assertIn(t,s)
        self.assertEqual(d['30:1'],'개 획득!!');self.assertIn('버그 조각',d['30:0'])

    def test_batch500o_followup_joke_hunger_and_chip_comparison(self):
        d=batch500o.DRAFT['6D44D4'];s=(ROOT/'analysis/full_scope_v1/source_tpl/6D44D4.tpl').read_text(encoding='utf-8-sig')
        for c in ('printSchool','printOlderBro','printYoungerSis','printDream','printCrush','printPlayerEnemy','printMostLostToOpponent','printMostLostToOpponentsChip','printFavStandardChip2','printFavStandardChip1'):self.assertIn(c,s)
        self.assertIn('농담',d['27:3']);self.assertIn('제일 먼저',d['31:2']);self.assertIn('배를 채울',d['13:1'])
        self.assertIn('1명',d['46:1']);self.assertIn('네놈',d['5:0']);self.assertIn('패배',d['90:2'])
        p=s.split('script 78 mmbn45 {')[1].split('script 79')[0];self.assertLess(p.index('printFavStandardChip2'),p.index('printFavStandardChip1'))

    def test_batch500o_alert_reminder_and_calendar_controls(self):
        for a,first in [('6D2B34',9080),('6C7D04',9064)]:
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            for n in range(first,first+7):self.assertIn('flag = '+str(n),s)
            for c in ('flag = 680','flag = 681','callTournamentReceiveMail','track = 155','frames = 96'):self.assertIn(c,s)
        d=batch500o.DRAFT['6D27EC']
        for a,b in [(1,21),(2,22),(3,23),(4,24),(5,25),(6,26)]:
            for k in (k for k in d if int(k.split(':')[0])==a):self.assertEqual(d[k],d[str(b)+':'+k.split(':')[1]])
        self.assertIn('싸우는',d['2:1']);self.assertIn('불쾌',d['3:2']);self.assertIn('학원',d['4:0'])
        for a in ('6D31E4','6C83BC'):
            s=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            for c in ('callFindSoonEvent','callFindTodayEvent','callBufferEventHour','callBufferEventMinutes','callBufferEventAMPM','callBufferEventName','padZeros = true'):self.assertIn(c,s)
        self.assertIn('충전',batch500o.DRAFT['6C8230']['2:1']);self.assertIn('꽃',batch500o.DRAFT['6D0A08']['1:1'])

    def test_batch500n_population_and_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-014'];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(self.plan['draft_assets'][-478:-463],[v[2] for v in batch500n.SOURCES.values()])
        self.assertTrue(all(u['state']=='needs_review' for u in uu))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))
        for k in batch500n.EXCLUDED:self.assertNotIn(k,{u['id'] for u in uu})
        self.assertEqual(self.base['6D2700:0:0']['source'],'かりです');self.assertNotIn('6D2700',batch500n.SOURCES)

    def test_batch500n_portrait_and_plugin_boundaries(self):
        aa={a['archive']:a for a in self.assets if a.get('batch_id')=='batch500-014'}
        for a in aa.values():
            for u in a['units']:
                self.assertEqual(u['origin_portrait'],'ElecMan' if a['archive']=='6C7A34' and int(u['id'].split(':')[1])>=21 else None)
                self.assertNotEqual(u['speaker'],'player-choice')
        for a,n in [('6CD068','플랜트맨.EXE'),('6D27A0','포르테.EXE'),('6C231C','아이스맨.EXE')]:
            self.assertIn(n,batch500n.DRAFT[a]['1:0']);self.assertEqual(aa[a]['units'][0]['speaker'],'plugin-call-speaker-unestablished')
        self.assertIn('플랜트맨',batch500n.DRAFT['6CC808']['1:1'])

    def test_batch500n_electrical_units_and_variables(self):
        d=batch500n.DRAFT['6C982C'];s=(ROOT/'analysis/full_scope_v1/source_tpl/6C982C.tpl').read_text(encoding='utf-8-sig')
        for c in ('printSchool','printOlderBro','printYoungerBro','printOlderSis','printYoungerSis','printFavFood','printHobby','printPlayerEnemy','printMostLostToOpponentsChip','printMostDefeatedOpponentsChip','printFavGigaChip'):self.assertIn(c,s)
        for k,v in [('6:0','3호'),('6:1','4호'),('8:1','버튼'),('10:0','30만'),('73:0','60볼트'),('77:0','50볼트'),('81:0','40볼트')]:self.assertIn(v,d[k])
        self.assertIn('100만',batch500n.DRAFT['6CB6C0']['2:0']);self.assertIn('전류',d['35:0']);self.assertIn('전압',d['9:0'])

    def test_batch500n_plant_food_weakness_and_life(self):
        d=batch500n.DRAFT['6CF0A0']
        for k,v in [('45:0','어쩔 수 없는'),('45:3','노력'),('14:3','카로틴'),('15:3','날것'),('10:1','비료'),('82:0','냉이'),('53:0','라이벌'),('30:2','받지 않을')]:self.assertIn(v,d[k])
        self.assertIn('엽록소',batch500n.DRAFT['6CCD40']['2:1'])

    def test_batch500n_training_rewards_and_placeholder(self):
        s=(ROOT/'analysis/full_scope_v1/source_tpl/6CCDC0.tpl').read_text(encoding='utf-8-sig');d=batch500n.DRAFT['6CCDC0']
        for v in ('minigame = 0','item = 33','amount = 1','amount = 4294967295','buffer = 3','padLeft = true','padLeft = false'):self.assertIn(v,s)
        self.assertNotIn('0:0',d);self.assertIn('계산',d['50:0']);self.assertIn('문제집',d['52:2'])
        self.assertEqual(d['52:3'],'제니군');self.assertEqual(d['53:3'],'버그 조각');self.assertEqual(d['53:4'],'개군')

    def test_batch500n_alert_reminder_schedule_and_tournament(self):
        s=(ROOT/'analysis/full_scope_v1/source_tpl/6CD48C.tpl').read_text(encoding='utf-8-sig')
        for v in ('flag = 680','flag = 681','flag = 623','flag = 626','flag = 9072','flag = 9078','frames = 96','callTournamentReceiveMail'):self.assertIn(v,s)
        s=(ROOT/'analysis/full_scope_v1/source_tpl/6C7A34.tpl').read_text(encoding='utf-8-sig')
        for v in ('jumpIfTVShow = 1','jumpIfPromise = 2','jumpIfMeal = 3','jumpIfSchool = 4','jumpIfOther = 5','mugshot = ElecMan','flag = 3658'):self.assertIn(v,s)
        d=batch500n.DRAFT['6C7A34']
        for a,b in [(1,21),(2,22),(3,23),(4,24),(5,25),(6,26)]:
            for k in (k for k in d if int(k.split(':')[0])==a):self.assertEqual(d[k],d[str(b)+':'+k.split(':')[1]])
        self.assertIn('아니',d['3:0']);self.assertIn('불호령',d['4:1'])
        s=(ROOT/'analysis/full_scope_v1/source_tpl/6CDBC8.tpl').read_text(encoding='utf-8-sig')
        for c in ('callBufferEventHour','callBufferEventMinutes','callBufferEventAMPM','callBufferEventName','callFindTodayEvent'):self.assertIn(c,s)
        self.assertIn('벚꽃',batch500n.DRAFT['6CD9E4']['1:0']);self.assertIn('다시 피어',batch500n.DRAFT['6CD9E4']['1:2'])
        self.assertIn('callCancelMenuTransition',(ROOT/'analysis/full_scope_v1/source_tpl/6CD9E4.tpl').read_text(encoding='utf-8-sig'))

    def test_batch500m_exact_population_authority_and_portrait_scope(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-013'];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(self.plan['draft_assets'][-485:-478],[v[2] for v in batch500m.SOURCES.values()])
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),93)
        for a in aa:
            self.assertTrue(all(u['origin_portrait']==('Bass' if a['archive']=='6D1984' else None) for u in a['units']))
            self.assertTrue(all(u['state']=='needs_review' for u in a['units']))
            self.assertFalse(a['review']['release_eligible'])

    def test_batch500m_profile_controls_and_exceptional_confirmation(self):
        for a in (a for a in self.assets if a.get('batch_id')=='batch500-013' and a['archive'] in batch500m.PROFILES):
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertRegex(src,r'variable = 22\s+value = 1\s+jumpIfEqual = 19')
            for v in range(1,10):self.assertRegex(src,rf'variable = 23\s+value = {v}\s+jumpIfEqual = {33 if v<=5 else 34}')
            choices=[u for u in a['units'] if u['speaker']=='player-choice']
            self.assertEqual(len(choices),24);self.assertEqual(src.count('select\n'),12)
            for u in choices:self.assertEqual(u['translation'],'있어  ' if u['source'].endswith('  ') else '없어')
            for token in ('flag = 3605','flag = 3606','printStringBuffer1','printStringBuffer2','printStringBuffer3','variable = 5'):self.assertIn(token,src)
        d=batch500m.DRAFT['6D32EC']
        self.assertTrue(d['41:0'].endswith('\n'));self.assertFalse(d['41:0'].endswith('\n\n'));self.assertTrue(d['44:0'].endswith('\n\n'))
        src=(ROOT/next(a for a in self.assets if a['archive']=='6D32EC')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(src.split('script 41 mmbn45 {')[1].split('script 42')[0],r'spacePx\s+count = 16')

    def test_batch500m_profile_semantics_power_flower_and_vulnerability(self):
        e=batch500m.DRAFT['6C84C8'];f=batch500m.DRAFT['6CDCD0'];b=batch500m.DRAFT['6D32EC']
        self.assertIn('화력',e['11:3']);self.assertIn('풍력',e['31:3']);self.assertIn('짜릿',e['17:3'])
        self.assertIn('만약',e['31:0']);self.assertIn('있다면',e['31:1']);self.assertIn('있다면',f['31:1'])
        self.assertEqual(f['17:0'],f['19:0']);self.assertNotIn('여자',f['17:0']);self.assertNotIn('남자',f['19:0'])
        self.assertIn('100송이',f['92:0']);self.assertIn('은방울꽃',f['83:1']);self.assertIn('해바라기',f['81:1'])
        self.assertIn('약점',b['17:2']);self.assertIn('강자',b['15:1']);self.assertIn('욕망',b['31:2'])
        for s in (1,3,5,7):self.assertIn('1인 독학',b[f'{s}:0'])

    def test_batch500m_explicit_bass_menu_and_deletion_controls(self):
        a=next(a for a in self.assets if a.get('batch_id')=='batch500-013' and a['archive']=='6D1984')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');d=batch500m.DRAFT['6D1984']
        self.assertEqual(src.count('mugshot = Bass'),29)
        self.assertEqual(sum(u['speaker']=='player-choice' for u in a['units']),21)
        self.assertIn('삭제',d['4:1']);self.assertIn('덮어',d['30:0']);self.assertIn('같은 시간',d['25:0'])
        for token in ('callBufferCurrentMonth','callBufferCurrentDay','callBufferEventYear','callBufferEventFrequency','callBufferEventAMPM','printScheduleBuffer','flag = 3611','track = 467','mugshotHide','msgCloseQuick','BSeparate = true','default = 1'):self.assertIn(token,src)
        self.assertIn('서브 칩',d['40:0']);self.assertIn('저장할 수',d['45:0'])

    def test_batch500m_training_original_placeholder_and_rewards(self):
        a=next(a for a in self.assets if a.get('batch_id')=='batch500-013' and a['archive']=='6C7608')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');d=batch500m.DRAFT['6C7608']
        self.assertEqual(batch500m.EXCLUDED,{'6C7608:0:0'});self.assertEqual(self.base['6C7608:0:0']['source'],'かりです');self.assertNotIn('0:0',d)
        for token in ('minigame = 0','minigame = 2','item = 33','amount = 1','checkGiveZenny','checkGiveBugFrags','amount = 4294967295','buffer = 3','padLeft = true'):self.assertIn(token,src)
        for s in (53,73):
            part=src.split(f'script {s} mmbn45 {{')[1].split('\nscript ')[0]
            self.assertLess(part.index('"バグのかけら"'),part.index('printBuffer'))
        self.assertIn('문제집',d['52:2']);self.assertIn('HP 메모리',d['71:2']);self.assertIn('강해진',d['51:3'])

    def test_batch500m_tournament_metaphor_and_plugin_target(self):
        aa={a['archive']:a for a in self.assets if a.get('batch_id')=='batch500-013'};d=batch500m.DRAFT['6C2B8C']
        self.assertIn('냉동 보관',d['2:1']);self.assertIn('등록',d['10:0']);self.assertIn('분해',d['1:1'])
        src=(ROOT/aa['6C2B8C']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('callCancelMenuTransition',src);self.assertEqual(src.count('flag = 3603'),4)
        for s in (20,21,22,23):self.assertTrue(d[f'{s}:0'].startswith('!\n'))
        src=(ROOT/aa['6C79E8']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('type = 3','flag = 3603','flag = 3651','frames = 30'):self.assertIn(token,src)
        self.assertNotIn('mugshotShow',src);self.assertIn('일렉맨.EXE',batch500m.DRAFT['6C79E8']['1:0'])

    def test_batch500l_population_authority_and_unapproved_states(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-012'];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(self.plan['draft_assets'][-491:-485],[v[2] for v in batch500l.SOURCES.values()])
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),72)
        self.assertTrue(all(u['origin_portrait'] is None and u['state']=='needs_review' for u in uu))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500l_profile_branches_and_choices(self):
        for a in (a for a in self.assets if a.get('batch_id')=='batch500-012' and a['archive'] in batch500l.PROFILES):
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertRegex(src,r'variable = 22\s+value = 1\s+jumpIfEqual = 19')
            for v in range(1,10):self.assertRegex(src,rf'variable = 23\s+value = {v}\s+jumpIfEqual = {33 if v<=5 else 34}')
            choices=[u for u in a['units'] if u['speaker']=='player-choice']
            self.assertEqual(len(choices),24);self.assertEqual(src.count('select\n'),12)
            for u in choices:self.assertEqual(u['translation'],'있어  ' if u['source'].endswith('  ') else '없어')
            for token in ('flag = 3605','flag = 3606','printStringBuffer1','printStringBuffer2','printStringBuffer3','variable = 5','BSeparate = false','clear = true'):self.assertIn(token,src)

    def test_batch500l_knight_candidate_meanings_and_punctuation(self):
        d=batch500l.DRAFT['6B6CA4']
        self.assertIn('충성심',d['15:4']);self.assertIn('꿈',d['15:4'])
        self.assertIn('예의',d['23:0']);self.assertIn('경의',d['23:1'])
        self.assertIn('잔 다르크',d['82:0']);self.assertIn('용기',d['82:1']);self.assertIn('지켜',d['83:3'])
        self.assertIn('어깨',d['95:1']);self.assertNotIn('코',d['95:1'])
        self.assertNotIn('83:1',d);self.assertEqual(self.base['6B6CA4:83:1']['source'],'、')

    def test_batch500l_fictional_explosions_firefighter_and_numeral(self):
        d=batch500l.DRAFT['6BCFBC']
        self.assertIn('전뇌 화약',d['11:3']);self.assertIn('전뇌 가솔린',d['11:4'])
        self.assertIn('화학',d['27:2']);self.assertIn('화학',d['29:2'])
        self.assertIn('될 수 없으려나',d['15:1']);self.assertIn('소방관',d['15:5']);self.assertIn('꺼 버릴',d['15:6'])
        self.assertIn('1개',d['13:3'])
        for s in (80,81,82,83):self.assertIn('없을 때',d[f'{s}:1'])
        self.assertNotIn('9:2',d);self.assertEqual(self.base['6BCFBC:9:2']['source'],'、')

    def test_batch500l_freezer_memory_not_gift_and_nickname(self):
        d=batch500l.DRAFT['6C2E4C']
        self.assertIn('주마등',d['31:1']);self.assertIn('휴대용 냉동고',d['31:2']);self.assertIn('떠오른',d['31:2'])
        self.assertIn('넷 내비',d['15:1']);self.assertIn('언젠가는',d['94:0'])
        self.assertNotIn('31:4',d);self.assertEqual(self.base['6C2E4C:31:4']['source'],'、')
        a=next(a for a in self.assets if a.get('batch_id')=='batch500-012' and a['archive']=='6C2E4C')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        s=src.split('script 31 mmbn45 {')[1].split('script 32')[0]
        self.assertIn('printPlayerNickname',s);self.assertNotIn('itemGive',s)
        for k in ('41:0','44:0','47:0','50:0','53:0','56:0','59:0','62:0'):self.assertTrue(d[k].endswith('\n\n'))

    def test_batch500l_mail_schedule_and_explicit_self_intro(self):
        aa={a['archive']:a for a in self.assets if a.get('batch_id')=='batch500-012'}
        src=(ROOT/aa['6B6474']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for n in range(9040,9047):self.assertIn('flag = '+str(n),src)
        for token in ('track = 155','frames = 96','flag = 3585','flag = 680','flag = 681','callTournamentReceiveMail','"!!"'):self.assertIn(token,src)
        src=(ROOT/aa['6B6B98']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('callFindSoonEvent','callFindTodayEvent','jumpIfExists = 2','jumpIfNone = 3','jumpIfExists = 11','jumpIfNone = 12','callBufferEventHour','callBufferEventMinutes','callBufferEventAMPM','padZeros = true','padZeros = false'):self.assertIn(token,src)
        g=batch500l.DRAFT['6B5A70'];self.assertIn('나이트맨',g['1:0']);self.assertIn('충성',g['1:2']);self.assertIn('변함없습니다',g['2:2'])
        src=(ROOT/aa['6B5A70']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('printPlayerNickname',src);self.assertNotIn('mugshotShow',src)

    def test_batch500k_population_and_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-011'];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(self.plan['draft_assets'][-499:-491],[v[2] for v in batch500k.SOURCES.values()])
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),72)
        self.assertTrue(all(u['state']=='needs_review' and u['origin_portrait'] is None for u in uu))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500k_profile_branches_choices_and_numeric_meaning(self):
        for a in (a for a in self.assets if a.get('batch_id')=='batch500-011' and a['archive'] in batch500k.PROFILES):
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertRegex(src,r'variable = 22\s+value = 1\s+jumpIfEqual = 19')
            for v in range(1,10):self.assertRegex(src,rf'variable = 23\s+value = {v}\s+jumpIfEqual = {33 if v<=5 else 34}')
            choices=[u for u in a['units'] if u['speaker']=='player-choice']
            self.assertEqual(len(choices),24);self.assertEqual(src.count('select\n'),12)
            for u in choices:self.assertEqual(u['translation'],'있어  ' if u['source'].endswith('  ') else '없어')
            for token in ('flag = 3605','flag = 3606','printStringBuffer1','printStringBuffer2','printStringBuffer3','variable = 5','BSeparate = false','clear = true'):self.assertIn(token,src)
        d=batch500k.DRAFT['6AB70C']
        for s in (1,3,5,7):self.assertIn('1인 독학',d[f'{s}:0']);self.assertNotIn('1가지씩',d[f'{s}:0'])
        self.assertIn('1인분',d['93:1']);self.assertNotIn('1명',d['93:1'])

    def test_batch500k_profile_context_wishes_not_grants(self):
        d=batch500k.DRAFT
        self.assertIn('없을지도',d['69F220']['31:3']);self.assertIn('찾아보기만',d['69F220']['31:4'])
        self.assertIn('소원을 빌기만',d['6A5814']['31:4'])
        self.assertIn('농담',d['6AB70C']['23:5']);self.assertIn('살생',d['6AB70C']['23:5']);self.assertIn('의뢰라면',d['6AB70C']['23:6'])
        aa={a['archive']:a for a in self.assets if a.get('batch_id')=='batch500-011'}
        src=(ROOT/aa['6A5814']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        star=src.split('script 94 mmbn45 {')[1].split('script 95')[0]
        self.assertIn('printEntryBuffer',star);self.assertNotIn('printPlayerNickname',star);self.assertNotIn('itemGive',star)
        src=(ROOT/aa['69F220']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        last=src.split('script 95 mmbn45 {')[1].split('script 96')[0]
        self.assertRegex(last,r'keyWait\s+any = false\s+end\s+waitHold');self.assertNotIn('clearMsg',last)

    def test_batch500k_mail_and_unresolved_source_retention(self):
        aa={a['archive']:a for a in self.assets if a.get('batch_id')=='batch500-011'}
        for arc,start in (('69EA0C',9000),('6A504C',9024)):
            src=(ROOT/aa[arc]['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for n in range(start,start+7):self.assertIn('flag = '+str(n),src)
            for token in ('track = 155','flag = 3585','flag = 680','flag = 681','callTournamentReceiveMail','"!!"'):self.assertIn(token,src)
            self.assertTrue(all(u['id'].endswith(':1') for u in aa[arc]['units']))
        self.assertEqual(batch500k.EXCLUDED,{'6AA730:0:0'})
        self.assertEqual(self.base['6AA730:0:0']['source'],'かりです')
        self.assertNotIn('0:0',batch500k.DRAFT['6AA730'])
        self.assertEqual(self.base['69F220:9:0']['source'],'、');self.assertNotIn('9:0',batch500k.DRAFT['69F220'])

    def test_batch500k_mission_and_training_reward_controls(self):
        a=next(a for a in self.assets if a.get('batch_id')=='batch500-011' and a['archive']=='6AA730')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');d=batch500k.DRAFT['6AA730']
        for token in ('callShadowManMissionComplete','callShadowManMissionFail','flag = 9244','flag = 9243','flag = 6051','flag = 6052','flag = 3632','flag = 3613','printShadowManMissionMinutes','jumpIfLittleTime = 13','minigame = 2','item = 33','amount = 1','checkGiveZenny','checkGiveBugFrags','amount = 4294967295'):self.assertIn(token,src)
        z=src.split('script 72 mmbn45 {')[1].split('script 73')[0]
        bug=src.split('script 73 mmbn45 {')[1]
        self.assertLess(z.index('printBuffer'),z.index('"ゼニー'))
        self.assertLess(bug.index('"バグのかけら"'),bug.index('printBuffer'));self.assertIn('padLeft = true',bug)
        self.assertEqual(d['12:1'],'분이다');self.assertIn('서둘러',d['13:0']);self.assertIn('HP 메모리',d['71:3'])
        self.assertEqual(d['73:3'],'버그 조각');self.assertEqual(d['73:4'],'개군...')

    def test_batch500k_schedule_and_plugin_target(self):
        aa={a['archive']:a for a in self.assets if a.get('batch_id')=='batch500-011'}
        src=(ROOT/aa['6AB600']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('callFindSoonEvent','callFindTodayEvent','jumpIfExists = 2','jumpIfNone = 3','jumpIfExists = 11','jumpIfNone = 12','callBufferEventHour','callBufferEventMinutes','callBufferEventAMPM','padZeros = true','padZeros = false','printScheduleBuffer'):self.assertIn(token,src)
        self.assertTrue(batch500k.DRAFT['6AB600']['1:0'].startswith('\n'));self.assertTrue(batch500k.DRAFT['6AB600']['11:2'].endswith('\n'))
        src=(ROOT/aa['6AAB08']['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('type = 3','flag = 3603','flag = 3651','frames = 30'):self.assertIn(token,src)
        self.assertNotIn('mugshotShow',src);self.assertIn('섀도맨.EXE',batch500k.DRAFT['6AAB08']['1:0'])

    def test_batch500i_exact_population_and_unshown_speakers(self):
        aa=[batch500i.create(a) for a in batch500i.SOURCES];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(self.plan['draft_assets'][-515:-508],[v[2] for v in batch500i.SOURCES.values()])
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),72)
        self.assertTrue(all(u['origin_portrait'] is None and u['portrait_visibility']=='not-shown-in-script' for u in uu))
        self.assertTrue(all(u['state']=='needs_review' for u in uu))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500i_profile_gender_and_education_branches(self):
        import re
        for a in batch500i.PROFILES:
            src=(ROOT/batch500i.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            d=batch500i.DRAFT[a]
            self.assertRegex(src,r'variable = 22\s+value = 1\s+jumpIfEqual = 19')
            for v in range(1,10):self.assertRegex(src,rf'variable = 23\s+value = {v}\s+jumpIfEqual = {33 if v<=5 else 34}')
            sexidx={'66CA84':3,'672238':2,'677F64':4}[a]
            self.assertIn('여',d[f'17:{sexidx}']);self.assertIn('남',d[f'19:{sexidx}'])
            edu={'66CA84':(2,2,2),'672238':(5,5,5),'677F64':(3,2,2)}[a]
            for s,i,t in zip((32,33,34),edu,('유치원','학교','회사')):self.assertIn(t,d[f'{s}:{i}'])
            self.assertNotIn('mugshotShow',src)

    def test_batch500i_profile_buffers_choices_and_input_flags(self):
        for a in batch500i.PROFILES:
            src=(ROOT/batch500i.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            choices=[u for u in batch500i.create(a)['units'] if u['speaker']=='player-choice']
            self.assertEqual(len(choices),24);self.assertEqual(src.count('select\n'),12)
            for u in choices:self.assertEqual(u['translation'],'있어  ' if u['source'].endswith('  ') else '없어')
            for token in ('printStringBuffer1','printStringBuffer2','printStringBuffer3','variable = 5','flag = 3605','flag = 3606','BSeparate = false','clear = true','flag = 3735','flag = 3736','flag = 3737','flag = 3738','flag = 3739','flag = 3741','flag = 3746','flag = 3749'):self.assertIn(token,src)

    def test_batch500i_mail_mission_and_original_exclamation(self):
        for a,start,count in (('66C264',8928,14),('671958',8936,15)):
            asset=batch500i.create(a);src=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(len(asset['units']),count)
            self.assertTrue(all(u['id'].endswith(':1') for u in asset['units']))
            for n in range(start,start+7):self.assertIn('flag = '+str(n),src)
            self.assertIn('track = 155',src);self.assertIn('callTournamentReceiveMail',src)
            self.assertIn('"!!"',src)
            for s in (1,2,3):self.assertTrue(batch500i.DRAFT[a][f'{s}:1'].startswith(',\n'))
        src=(ROOT/batch500i.create('671958')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('callSearchManMissionBegin','callSearchManMissionReceiveMail','flag = 3767','flag = 3613','flag = 3785'):self.assertIn(t,src)
        self.assertIn('미션 지령',batch500i.DRAFT['671958']['10:1'])

    def test_batch500i_tournament_outcomes_and_plugin_target(self):
        d=batch500i.DRAFT['671F24'];a=batch500i.create('671F24')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('실패',d['1:0']);self.assertIn('99퍼센트',d['1:1']);self.assertIn('컴플리트',d['2:0'])
        self.assertIn('등록을 하지 않았습니다',d['10:0']);self.assertIn('callCancelMenuTransition',src)
        self.assertEqual(sum('록온' in t for t in d.values()),4)
        src=(ROOT/batch500i.create('65AF54')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('type = 3','flag = 3603','flag = 3651','frames = 30'):self.assertIn(t,src)
        self.assertEqual(batch500i.DRAFT['65AF54']['1:0'],'플러그인!\n록맨.EXE,\n트랜스미션!!')

    def test_batch500i_metaphors_and_non_japanese_source_preservation(self):
        self.assertIn('풍경',batch500i.DRAFT['66CA84']['13:1'])
        self.assertIn('사랑에 불타다',batch500i.DRAFT['677F64']['88:0'])
        self.assertIn('타 버릴 만큼',batch500i.DRAFT['677F64']['88:1'])
        self.assertIn('태우지는',batch500i.DRAFT['677F64']['23:4'])
        self.assertIn('1명',batch500i.DRAFT['677F64']['90:0'])
        for a,keys in (('672238',('11:0','32:2','33:2','34:2')),('677F64',('1:2','3:2','5:2','7:2'))):
            asset=batch500i.create(a);u={x['id']:x for x in asset['units']}
            for k in keys:
                self.assertEqual(self.base[a+':'+k]['source'],'、');self.assertNotIn(a+':'+k,u)
            self.assertEqual(len(self.validate(asset)),len(asset['units']))

    def test_batch500j_exact_population_authority_and_unapproved_states(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-010'];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(aa),9);self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(self.plan['draft_assets'][-508:-499],[v[2] for v in batch500j.SOURCES.values()])
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),72)
        self.assertTrue(all(u['state']=='needs_review' for u in uu))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500j_profile_controls_gender_education_and_padding(self):
        for a in (a for a in self.assets if a.get('batch_id')=='batch500-010' and a['archive'] in batch500j.PROFILES):
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig');arc=a['archive'];d=batch500j.DRAFT[arc]
            self.assertEqual(src.count('select\n'),12);self.assertNotIn('mugshotShow',src)
            self.assertRegex(src,r'variable = 22\s+value = 1\s+jumpIfEqual = 19')
            for v in range(1,10):self.assertRegex(src,rf'variable = 23\s+value = {v}\s+jumpIfEqual = {33 if v<=5 else 34}')
            for t in ('printStringBuffer1','printStringBuffer2','printStringBuffer3','variable = 5','flag = 3605','flag = 3606','BSeparate = false','clear = true'):self.assertIn(t,src)
            for u in a['units']:
                if u['source'].endswith('  '):self.assertEqual(u['translation'],'있어  ');self.assertEqual(u['speaker'],'player-choice')
                self.assertIsNone(u['origin_portrait'])
            i=4 if arc=='688A10' else 2
            self.assertIn('여',d[f'17:{i}']);self.assertIn('남',d[f'19:{i}'])
            for s,t in ((32,'유치원'),(33,'학교'),(34,'회사')):self.assertIn(t,d[f'{s}:{2 if arc=="68E8C4" else 1}'])
        for k in ('17:3','19:3'):
            self.assertEqual(self.base['688A10:'+k]['source'],'、');self.assertNotIn(k,batch500j.DRAFT['688A10'])

    def test_batch500j_profile_specific_arithmetic_training_junk_and_affection(self):
        n=batch500j.DRAFT['688A10'];m=batch500j.DRAFT['68E8C4'];j=batch500j.DRAFT['6942F0']
        self.assertIn('더하',n['13:0']);self.assertIn('곱하',n['13:1']);self.assertIn('피타고라스',n['21:2'])
        self.assertIn('계산할 수 없',n['15:0']);self.assertIn('온천',m['13:2']);self.assertIn('주먹',m['15:0'])
        self.assertIn('버그 조각',j['11:2']);self.assertIn('쓰레기',j['13:1']);self.assertIn('아이돌',j['15:1'])
        self.assertIn('노력할게',j['23:3']);self.assertIn('너를',j['88:1']);self.assertIn('가르칠 수',j['29:3'])
        self.assertTrue(j['1:0'].startswith('나, 나'));self.assertTrue(j['95:0'].startswith('나, 나'))

    def test_batch500j_mail_flags_and_original_alerts(self):
        for arc,start in (('6881C4',8968),('68E0B4',8976),('693AA4',8984)):
            a=next(a for a in self.assets if a.get('batch_id')=='batch500-010' and a['archive']==arc)
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(len(a['units']),14);self.assertTrue(all(u['id'].endswith(':1') and u['origin_portrait'] is None for u in a['units']))
            for n in range(start,start+7):self.assertIn('flag = '+str(n),src)
            for t in ('track = 155','frames = 96','flag = 680','flag = 681','callTournamentReceiveMail','"!!"'):self.assertIn(t,src)
            for s in (1,2,3):self.assertTrue(batch500j.DRAFT[arc][f'{s}:1'].startswith(',\n'))

    def test_batch500j_reminder_explicit_portraits_nickname_and_loops(self):
        for arc,portrait,count in (('687E88','NumberMan',20),('6937C4','JunkMan',18)):
            a=next(a for a in self.assets if a.get('batch_id')=='batch500-010' and a['archive']==arc)
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(len(a['units']),count)
            for u in a['units']:
                shown=21<=int(u['id'].split(':')[1])<=26
                self.assertEqual(u['origin_portrait'],portrait if shown else None)
                self.assertEqual(u['portrait_visibility'],'shown' if shown else 'not-shown-in-script')
            for t in ('callBufferReminders','callBufferEventName','printScheduleBuffer','callCheckNowEvent','jumpIfTVShow','jumpIfPromise','jumpIfMeal','jumpIfSchool','jumpIfOther','flag = 3658'):self.assertIn(t,src)
            self.assertIn('학원',batch500j.DRAFT[arc]['4:0']);self.assertTrue(batch500j.DRAFT[arc]['2:0'].startswith('\n'))
        self.assertIn('수학',batch500j.DRAFT['687E88']['24:2']);self.assertIn('긴장',batch500j.DRAFT['6937C4']['22:1'])
        self.assertTrue(batch500j.DRAFT['687E88']['3:0'].startswith(',\n'))
        self.assertFalse(batch500j.DRAFT['6937C4']['3:0'].startswith(','))

    def test_batch500j_tournament_loss_effort_victory_and_registration(self):
        d=batch500j.DRAFT['693FEC'];a=next(a for a in self.assets if a.get('batch_id')=='batch500-010' and a['archive']=='693FEC')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('오퍼레이트',d['1:1']);self.assertIn('졌어',d['1:2']);self.assertIn('우승했어',d['2:0'])
        self.assertIn('등록을 안 했어',d['10:0']);self.assertIn('callCancelMenuTransition',src)
        self.assertEqual(src.count('flag = 3603'),4)
        for s in (20,21,22,23):self.assertIn('최선을 다해',d[f'{s}:0']);self.assertIn('부탁해',d[f'{s}:0'])
        self.assertTrue(all(u['origin_portrait'] is None for u in a['units']))
        self.assertEqual(len(self.validate(a)),10)

    def validate(self,a,available=None):
        return check_draft(a,self.base,self.available if available is None else available,self.rom,self.rows)

    def altered(self):return copy.deepcopy(self.assets[0])

    def test_quick_results_actor_and_nickname_boundary(self):
        a=quickresult.create('664D84');u={x['id']:x for x in a['units']}
        self.assertTrue(all(x['origin_portrait'] is None for x in a['units']))
        self.assertTrue(u['664D84:2:0']['translation'].endswith(chr(10)))
        self.assertTrue(u['664D84:2:1']['translation'].startswith(','+chr(10)))
        self.assertIn('결판',u['664D84:3:0']['translation'])

    def test_guts_remaining_voice_and_scope(self):
        a=quickresult.create('66651C');u={x['id']:x for x in a['units']}
        self.assertEqual(len(u),14)
        self.assertEqual(u['66651C:21:0']['origin_portrait'],'GutsMan')
        self.assertIsNone(u['66651C:1:0']['origin_portrait'])
        self.assertIn('거스',u['66651C:21:0']['translation'])
        self.assertIn('거츠',u['66651C:21:1']['translation'])
        self.assertIn('학원',u['66651C:24:0']['translation'])
        self.assertNotIn('66651C:3:0',u)

    def test_quick_placeholder_drafted_without_speaker_or_rom_claim(self):
        self.assertEqual(self.base['666430:0:0']['source'],'かりです')
        self.assertEqual(self.base['666430:0:0']['status'],'unselected_japanese')
        self.assertTrue(any(u['id']=='666430:0:0' for a in self.assets for u in a['units']))
        provisional=batch500at.create('666430')['units'][0]
        self.assertEqual(provisional['state'],'needs_review')
        self.assertEqual(provisional['speaker'],'speaker-unestablished')
        self.assertEqual(provisional['translation'],'임시 문구입니다')

    def test_windman_menu_portraits_and_choices(self):
        a=windmenu.create('66B0D4')
        self.assertEqual(len(a['units']),57)
        self.assertTrue(all(u['origin_portrait']=='WindMan' and u['portrait_visibility']=='shown' for u in a['units']))
        self.assertEqual(sum(u['speaker']=='player-choice' for u in a['units']),21)
        self.assertEqual({u['id'] for u in a['units'] if u['speaker']=='player-choice'},{'66B0D4:'+str(s)+':'+str(i) for s,i in windmenu.CHOICES})

    def test_windman_menu_warnings_and_event_categories(self):
        u={x['id']:x for x in windmenu.create('66B0D4')['units']}
        self.assertIn('지났',u['66B0D4:3:0']['translation'])
        self.assertIn('삭제',u['66B0D4:4:1']['translation'])
        self.assertIn('같은 시간',u['66B0D4:25:0']['translation'])
        self.assertIn('덮어쓰',u['66B0D4:30:0']['translation'])
        self.assertIn('일정을',u['66B0D4:50:5']['translation'])
        for k in ('51:6','52:3'):self.assertIn('기념일을',u['66B0D4:'+k]['translation'])
        for k in ('24:1','30:1','33:1','50:7','51:8','52:5'):self.assertTrue(u['66B0D4:'+k]['translation'].endswith('  '))

    def test_windman_menu_control_and_dynamic_names(self):
        a=windmenu.create('66B0D4');src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('callBufferEventAMPM','callBufferEventFrequency','callBufferEventYear','callBufferEventDayName','flag = 3611','track = 467','minLength = 2','BSeparate = true','BSeparate = false'):self.assertIn(token,src)
        u={x['id']:x for x in a['units']}
        self.assertTrue(u['66B0D4:10:1']['translation'].startswith('의'+chr(10)))
        self.assertEqual(u['66B0D4:0:0']['translation'],'오늘은 ')
        self.assertEqual(u['66B0D4:0:1']['translation'],'월')

    def test_quick_menu_b_save_and_actor(self):
        a=windquick.create('66B950');u={x['id']:x for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in a['units']),28)
        self.assertTrue(all(x['origin_portrait'] is None for x in a['units']))
        self.assertIn('저장 화면',u['66B950:8:0']['translation'])
        self.assertNotIn('화면',u['66B950:16:0']['translation'])
        self.assertTrue(u['66B950:20:0']['translation'].startswith(chr(10)))
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('global = 30','value = 120','flag = 3615','count = 24','jumpIfSave = 16','jumpIfSave = 8'):self.assertIn(t,src)

    def test_quick_wind_reminder_portraits_and_topology(self):
        a=windquick.create('66BF44');u={x['id']:x for x in a['units']}
        self.assertEqual(sum(x['origin_portrait']=='WindMan' for x in a['units']),9)
        self.assertIsNone(u['66BF44:1:0']['origin_portrait'])
        self.assertIn('멀리서',u['66BF44:21:1']['translation'])
        self.assertIn('남기지',u['66BF44:23:1']['translation'])
        self.assertIn('학원',u['66BF44:24:0']['translation'])
        self.assertEqual(self.base['66BE58:0:0']['source'],'かりです')
        self.assertTrue(any(x['id']=='66BE58:0:0' for a in self.assets for x in a['units']))
        provisional=batch500at.create('66BE58')['units'][0]
        self.assertEqual(provisional['state'],'needs_review')
        self.assertEqual(provisional['speaker'],'speaker-unestablished')
        self.assertEqual(provisional['translation'],'임시 문구입니다')

    def test_quick_wind_return_and_jackin(self):
        a=windquick.create('66BDE0');u={x['id']:x for x in a['units']}
        self.assertIn('전뇌 바람',u['66BDE0:1:0']['translation'])
        self.assertIn('바람 방향',u['66BDE0:2:0']['translation'])
        a=windquick.create('66BEF8');x=a['units'][0]
        self.assertEqual(x['speaker'],'operator-jackin-call')
        self.assertIsNone(x['origin_portrait'])
        self.assertIn('윈드맨.EXE',x['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('type = 3','flag = 3603','flag = 3651','frames = 30'):self.assertIn(t,src)

    def test_batch500_exact_policy_and_population(self):
        aa=[batch500.create(a) for a in batch500.SOURCES];u=[x for a in aa for x in a['units']]
        self.assertEqual(len(u),500);self.assertEqual(len({x['id'] for x in u}),500)
        self.assertEqual(self.plan['batch_policy']['target_literals'],500)
        self.assertEqual(self.plan['batch_policy']['completed_batches'][0]['authored_literals'],500)
        self.assertEqual(sum(x['speaker']=='equipment-label' for x in u),342)
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u),18)
        self.assertTrue(all(a['batch_id']=='batch500-001' and not a['review']['release_eligible'] for a in aa))

    def test_batch500_equipment_numeric_limits_and_dynamic_count(self):
        for a in batch500.ACTORS:
            aa=batch500.create(a);u={x['id']:x for x in aa['units']}
            for s,n in ((71,'3'),(72,'1'),(73,'1'),(74,'5'),(75,'1')):
                self.assertIn(n,u[f'{a}:{s}:0']['translation'])
            self.assertNotIn('30',u[a+':70:1']['translation'])
            src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertIn('buffer = 1',src);self.assertIn('minLength = 1',src)
            self.assertEqual(u[a+':70:3']['translation'],'예  ')
            self.assertEqual(u[a+':70:4']['translation'],'아니오')

    def test_batch500_equipment_portrait_boundaries(self):
        for a,actor in batch500.ACTORS.items():
            aa=batch500.create(a);u={x['id']:x for x in aa['units']}
            self.assertEqual(sum(x['origin_portrait']==actor for x in aa['units']),10)
            for s in (60,61,62):self.assertIsNone(u[f'{a}:{s}:0']['origin_portrait'])
            self.assertTrue(all(u[f'{a}:{s}:0']['speaker']==actor for s in range(71,76)))

    def test_batch500_equipment_candidate_terms_abbreviations_and_padding(self):
        for a in batch500.ACTORS:
            u={x['id']:x for x in batch500.create(a)['units']}
            self.assertEqual(u[a+':0:0']['translation'],'   칩 폴더')
            self.assertEqual(u[a+':2:0']['translation'],'  칩 폴더   ')
            for s,v in ((27,'킹덤C'),(28,'로열WB'),(35,'슈팅B'),(36,'D오버로드')):
                self.assertEqual(u[f'{a}:{s}:0']['translation'],v)
            self.assertNotIn(a+':38:0',u);self.assertNotIn(a+':39:0',u)

    def test_batch500_progress_branches_and_area_numbers(self):
        a=batch500.create('66FD14');u={x['id']:x for x in a['units']}
        self.assertTrue(all(x['origin_portrait'] is None for x in a['units']))
        for s,n in ((16,'3'),(18,'5'),(19,'7'),(20,'9'),(21,'10'),(22,'12')):
            self.assertIn('인터넷'+n,u[f'66FD14:{s}:0']['translation'])
        self.assertIn('관',u['66FD14:27:1']['translation'])
        self.assertIn('1',u['66FD14:24:0']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('chip = 104','item = 11','flag = 9446','lower = 6','jumpIfInRange = 34'):self.assertIn(t,src)

    def test_batch500_tournament_formula_and_unregistered_cancel(self):
        a=batch500.create('6886F0');u={x['id']:x for x in a['units']}
        self.assertTrue(all(x['origin_portrait'] is None for x in a['units']))
        self.assertIn('방정식',u['6886F0:1:1']['translation'])
        self.assertIn('오류는 없',u['6886F0:1:2']['translation'])
        self.assertIn('신청을 안',u['6886F0:10:0']['translation'])
        for s in (20,21,22,23):self.assertIn('다치지',u[f'6886F0:{s}:0']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('callCancelMenuTransition',src)

    def test_batch500b_exact_population_and_policy(self):
        aa=[batch500b.create(a) for a in batch500b.SOURCES];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(sum(u['speaker']=='equipment-label' for u in uu),342)
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),18)
        self.assertTrue(all(a['batch_id']=='batch500-002' and not a['review']['release_eligible'] for a in aa))
        self.assertEqual(self.plan['batch_policy']['completed_batches'][1]['authored_literals'],500)

    def test_batch500b_numeric_limits_and_choices(self):
        for a in batch500b.ACTORS:
            aa=batch500b.create(a);u={x['id']:x for x in aa['units']}
            for s,n in ((71,'3'),(72,'1'),(73,'1'),(74,'5'),(75,'1')):
                self.assertIn(n,u[f'{a}:{s}:0']['translation'])
            self.assertNotIn('30',u[a+':70:1']['translation'])
            self.assertTrue(u[a+':70:0']['translation'].endswith('\n'))
            self.assertEqual(u[a+':70:3']['translation'],'예  ')
            self.assertEqual(u[a+':70:4']['translation'],'아니오')
            src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertIn('buffer = 1',src);self.assertIn('minLength = 1',src)

    def test_batch500b_portrait_boundary_and_register(self):
        for a,actor in batch500b.ACTORS.items():
            u={x['id']:x for x in batch500b.create(a)['units']}
            self.assertEqual(sum(x['origin_portrait']==actor for x in u.values()),10)
            for s in (60,61,62):self.assertIsNone(u[f'{a}:{s}:0']['origin_portrait'])
            for s in range(71,76):self.assertEqual(u[f'{a}:{s}:0']['speaker'],actor)
        self.assertIn('고르거라',batch500b.DRAFT['6E32FC']['61:0'])
        self.assertIn('주세요',batch500b.DRAFT['6E3574']['61:0'])
        self.assertIn('거예요',batch500b.DRAFT['6E3A64']['60:0'])
        self.assertIn('골라라...',batch500b.DRAFT['6E41C4']['61:0'])

    def test_batch500b_label_padding_and_abbreviations(self):
        for a in batch500b.ACTORS:
            u={x['id']:x for x in batch500b.create(a)['units']}
            self.assertEqual(u[a+':0:0']['translation'],'   칩 폴더')
            self.assertEqual(u[a+':2:0']['translation'],'  칩 폴더   ')
            for s,v in ((27,'킹덤C'),(28,'로열WB'),(35,'슈팅B'),(36,'D오버로드')):
                self.assertEqual(u[f'{a}:{s}:0']['translation'],v)
            for s in (38,39,63):self.assertNotIn(f'{a}:{s}:0',u)

    def test_batch500b_progress_pages_and_dynamic_context(self):
        a=batch500b.create('68097C');u={x['id']:x for x in a['units']}
        self.assertTrue(all(x['origin_portrait'] is None for x in u.values()))
        self.assertIn('수고',u['68097C:15:0']['translation'])
        self.assertIn('플러그아웃',u['68097C:15:1']['translation'])
        self.assertEqual(u['68097C:26:0']['translation'],'오피셜\n토너먼트의')
        self.assertIn('접수 장소',u['68097C:26:1']['translation'])
        self.assertTrue(u['68097C:33:0']['translation'].startswith(',\n'))
        self.assertIn('읽지 않은',u['68097C:33:0']['translation'])
        for s,n in ((16,'3'),(18,'5'),(19,'7'),(20,'9'),(21,'10'),(22,'12')):
            self.assertIn('인터넷'+n,u[f'68097C:{s}:0']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('chip = 104','item = 11','lower = 6','jumpIfInRange = 34'):
            self.assertIn(t,src)

    def test_batch500b_tournament_resolve_not_formula(self):
        a=batch500b.create('68E5E0');u={x['id']:x for x in a['units']}
        self.assertTrue(all(x['origin_portrait'] is None for x in u.values()))
        self.assertIn('전력을 다해',u['68E5E0:1:0']['translation'])
        self.assertIn('포기하지',u['68E5E0:1:1']['translation'])
        self.assertIn('거머쥘 때까지',u['68E5E0:1:2']['translation'])
        self.assertFalse(any('방정식' in x['translation'] for x in u.values()))
        for s in (20,21,22,23):self.assertIn('주먹',u[f'68E5E0:{s}:0']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('callCancelMenuTransition',src);self.assertIn('flag = 3603',src)

    def test_batch500c_exact_population_and_unshown_actors(self):
        aa=[batch500c.create(a) for a in batch500c.SOURCES];u=[x for a in aa for x in a['units']]
        self.assertEqual(len(u),500);self.assertEqual(len({x['id'] for x in u}),500)
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u),308)
        self.assertTrue(all(x['origin_portrait'] is None for x in u))
        self.assertTrue(all(a['batch_id']=='batch500-003' and not a['review']['release_eligible'] for a in aa))
        self.assertEqual(self.plan['batch_policy']['completed_batches'][2]['authored_literals'],500)

    def test_batch500c_menu_options_and_control_routes(self):
        for a in batch500c.MENUS:
            aa=batch500c.create(a);u={x['id']:x for x in aa['units']}
            self.assertEqual(len(u),44)
            for s in (*range(2,9),*range(10,17)):
                self.assertEqual(u[f'{a}:{s}:1']['translation'],'예  ')
                self.assertEqual(u[f'{a}:{s}:2']['translation'],'아니오')
                self.assertTrue(u[f'{a}:{s}:0']['translation'].endswith('\n'))
            src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for t in ('jumpIfSave = 8','jumpIfSave = 16','global = 30','value = 120','count = 24','flag = 3615'):
                self.assertIn(t,src)
            self.assertEqual(src.count('jump = 9,'),14)
            self.assertEqual(src.count('lastCancelSFX = true'),14)

    def test_batch500c_save_entry_and_source_statement(self):
        for a in batch500c.MENUS:
            self.assertIn('화면',batch500c.DRAFT[a]['8:0'])
            self.assertIn('데이터',batch500c.DRAFT[a]['16:0'])
            self.assertNotIn('화면',batch500c.DRAFT[a]['16:0'])
        self.assertEqual(batch500c.DRAFT['681B3C']['16:0'],'지금까지의 데이터를\n저장하겠습니다\n')
        self.assertIn('참가',batch500c.DRAFT['6B5B1C']['10:0'])

    def test_batch500c_voice_and_nickname_boundaries(self):
        for a in ('670E9C','67C578','681B3C','6930F8','69E12C','6B5B1C'):
            self.assertTrue(batch500c.DRAFT[a]['1:0'].startswith(',\n'))
        self.assertTrue(batch500c.DRAFT['6930F8']['20:0'].startswith(',\n'))
        self.assertIn('무, 무엇',batch500c.DRAFT['6930F8']['1:0'])
        self.assertIn('퓨',batch500c.DRAFT['698508']['20:0'])
        self.assertIn('닌자',batch500c.DRAFT['6AA214']['20:0'])
        self.assertIn('성급',batch500c.DRAFT['69E12C']['20:0'])
        self.assertIn('이 몸',batch500c.DRAFT['676BA8']['4:0'])

    def test_batch500c_training_dynamic_rewards_and_placeholder(self):
        a=batch500c.create('6713B8');u={x['id']:x for x in a['units']}
        self.assertEqual(len(u),15);self.assertNotIn('6713B8:0:0',u)
        self.assertEqual(self.base['6713B8:0:0']['source'],'かりです')
        self.assertTrue(any(x['id']=='6713B8:0:0' for a in self.assets for x in a['units']))
        provisional=batch500at.create('6713B8')['units'][0]
        self.assertEqual(provisional['state'],'needs_review')
        self.assertEqual(provisional['speaker'],'speaker-unestablished')
        self.assertEqual(provisional['translation'],'임시 문구입니다')
        self.assertIn('군에서',u['6713B8:72:2']['translation'])
        self.assertEqual(u['6713B8:73:4']['translation'],'버그 조각')
        self.assertEqual(u['6713B8:73:5']['translation'],'개를\n획득했습니다!')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('minigame = 2','item = 33','buffer = 3','amount = 4294967295','jumpIfEqual = 73'):
            self.assertIn(t,src)

    def test_batch500c_jackin_destination_not_speaker(self):
        a=batch500c.create('671638');u=a['units'][0]
        self.assertEqual(u['speaker'],'operator-jackin-call');self.assertIsNone(u['origin_portrait'])
        self.assertEqual(u['translation'],'플러그인!\n서치맨.EXE,\n트랜스미션!!')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('type = 3','flag = 3603','flag = 3651','frames = 30'):self.assertIn(t,src)

    def test_batch500d_exact_population(self):
        aa=[batch500d.create(a) for a in batch500d.SOURCES];u=[x for a in aa for x in a['units']]
        self.assertEqual(len(u),500);self.assertEqual(len({x['id'] for x in u}),500)
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u),140)
        self.assertTrue(all(x['origin_portrait'] is None for x in u))
        self.assertTrue(all(a['batch_id']=='batch500-004' and not a['review']['release_eligible'] for a in aa))
        self.assertEqual(self.plan['batch_policy']['completed_batches'][3]['authored_literals'],500)

    def test_batch500d_menu_structure_and_save(self):
        for a in batch500d.MENUS:
            aa=batch500d.create(a);u={x['id']:x for x in aa['units']}
            for s in (*range(2,9),*range(10,17)):
                self.assertEqual(u[f'{a}:{s}:1']['translation'],'예  ')
                self.assertEqual(u[f'{a}:{s}:2']['translation'],'아니오')
            self.assertIn('화면',u[a+':8:0']['translation'])
            self.assertIn('데이터',u[a+':16:0']['translation'])
            src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('jump = 9,'),14)
            for t in ('global = 30','value = 120','count = 24','flag = 3615'):self.assertIn(t,src)
        self.assertEqual(batch500d.DRAFT['6CC8D0']['2:0'],'토너먼트에\n참가할게\n')
        self.assertIn('꽃',batch500d.DRAFT['6CC8D0']['20:0'])
        self.assertIn('훌쩍',batch500d.DRAFT['6C1710']['20:0'])
        self.assertEqual(batch500d.DRAFT['6D2230']['20:0'],'네놈...')

    def test_batch500d_progress_variables_areas_and_weekday(self):
        for a in tuple(batch500d.SOURCES)[5:]:
            aa=batch500d.create(a);u={x['id']:x for x in aa['units']}
            for s,n in ((16,'3'),(18,'5'),(19,'7'),(20,'9'),(21,'10'),(22,'12')):
                self.assertIn('인터넷'+n,u[f'{a}:{s}:0']['translation'])
            self.assertIn('1',u[a+':24:0']['translation'])
            self.assertIn('인터넷9',u[a+':25:0']['translation'])
            self.assertIn('관',u[a+':27:1']['translation'])
            src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for t in ('chip = 104','item = 11','lower = 0','lower = 6','jumpIfInRange = 34'):
                self.assertIn(t,src)

    def test_batch500d_progress_page_differences(self):
        self.assertIn('손쉬운',batch500d.DRAFT['6AEE68']['23:1'])
        self.assertNotIn('25:1',batch500d.DRAFT['6C05C4'])
        self.assertIn('플러그아웃',batch500d.DRAFT['6D5F34']['15:0'])
        self.assertIn('MAX',batch500d.DRAFT['6CB75C']['29:1'])
        self.assertIn('무대',batch500d.DRAFT['6D10F0']['30:1'])
        self.assertIn('탐색',batch500d.DRAFT['6BA9F8']['31:1'])
        self.assertEqual(batch500d.DRAFT['6A911C']['34:1'],'참가 접수 장소로\n가자')

    def test_batch500d_source_motifs_and_register(self):
        self.assertIn('닌자의 극의',batch500d.DRAFT['6AEE68']['29:0'])
        self.assertIn('차갑게 타오',batch500d.DRAFT['6C5FCC']['30:0'])
        self.assertIn('더 쏘고',batch500d.DRAFT['6C05C4']['31:0'])
        self.assertIn('피우기에',batch500d.DRAFT['6D10F0']['30:1'])
        self.assertIn('투지',batch500d.DRAFT['6BA9F8']['30:0'])
        self.assertIn('심심풀이',batch500d.DRAFT['6D5F34']['11:0'])
        self.assertIn('우리가 빛나',batch500d.DRAFT['6A911C']['30:0'])

    def test_batch500d_nickname_and_structural_quotes_unselected(self):
        for a,s in (('6C1710','1'),('6C05C4','10'),('6BA9F8','31'),('6A911C','11'),('6A276C','31')):
            self.assertTrue(batch500d.DRAFT[a][s+':0'].startswith(',\n'))
        a=batch500d.create('6C5FCC')
        self.assertNotIn('6C5FCC:13:0',{u['id'] for u in a['units']})
        self.assertEqual(self.base['6C5FCC:13:0']['source'],'、\n「')
        self.assertEqual(self.base['6C5FCC:13:0']['status'],'unselected_non_japanese_review')
        self.assertNotIn('6C05C4:28:0',{u['id'] for u in batch500d.create('6C05C4')['units']})

    def test_batch500e_population_policy(self):
        aa=[batch500e.create(a) for a in batch500e.SOURCES]
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(sum(len(a['units']) for a in aa if a['archive'] in batch500e.PROGRESS),226)
        self.assertEqual(sum(len(a['units']) for a in aa if a['archive'] in batch500e.REMINDERS),190)
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))
        self.assertEqual(self.plan['batch_policy']['completed_batches'][4]['authored_literals'],500)

    def test_batch500e_portrait_boundary(self):
        for a,actor in batch500e.REMINDERS.items():
            aa=batch500e.create(a);src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('mugshot = '+actor),6)
            for u in aa['units']:
                shown=21<=int(u['id'].split(':')[1])<=26
                self.assertEqual(u['origin_portrait'],actor if shown else None)
                self.assertEqual(u['speaker'],actor if shown else 'unshown-quick-voice')

    def test_batch500e_reminder_pairing_and_variables(self):
        for a in batch500e.REMINDERS:
            d=batch500e.DRAFT[a]
            for key,t in d.items():
                s,i=map(int,key.split(':'))
                if 1<=s<=6:self.assertEqual(t,d[f'{s+20}:{i}'])
            src=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            for token in ('printScheduleBuffer','callCheckNowEvent','flag = 3658','frames = 96','track = 155'):
                self.assertIn(token,src)

    def test_batch500e_progress_semantic_distinctions(self):
        d=batch500e.DRAFT
        for a,key,word in (('675A20','11:0','흥미'),('67B47C','30:0','활활'),('6861B8','12:0','합격'),('68C368','27:0','썩 내키지'),('692020','30:0','주먹'),('697310','15:0','재미'),('697310','30:0','인기쟁이'),('69D020','27:2','퓨')):
            self.assertIn(word,d[a][key])
        self.assertNotIn('뿌',''.join(d['69D020'].values()))
        for a in batch500e.PROGRESS:
            src=(ROOT/f'analysis/full_scope_v1/source_tpl/{a}.tpl').read_text(encoding='utf-8-sig')
            for t in ('chip = 104','item = 11','lower = 6','jumpIfInRange = 34'):self.assertIn(t,src)

    def test_batch500e_training_rewards_placeholders_and_options(self):
        for a in batch500e.CHOICE_IDS:
            aa=batch500e.create(a);u={x['id']:x for x in aa['units']}
            self.assertNotIn(a+':0:0',u);self.assertEqual(self.base[a+':0:0']['source'],'かりです')
            for key in batch500e.CHOICE_IDS[a]:self.assertEqual(u[a+':'+key]['speaker'],'player-choice')
            src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for t in ('variable = 5','buffer = 3','amount = 4294967295','item = 33','amount = 5'):self.assertIn(t,src)
        src=(ROOT/'analysis/full_scope_v1/source_tpl/6C1BFC.tpl').read_text(encoding='utf-8-sig')
        self.assertIn('amount = 1',src);self.assertIn('flag = 3667',src)
        self.assertEqual(batch500e.DRAFT['6C1BFC']['10:5'],'물론!  ')
        self.assertTrue(batch500e.DRAFT['6C1BFC']['20:0'].startswith('\n'))
        self.assertIn('뜨거워',batch500e.DRAFT['6C1BFC']['24:1'])

    def test_batch500e_reminder_semantic_candidates(self):
        d=batch500e.DRAFT
        for a,key,word in (('677364','3:1','농부'),('67CB70','4:2','무작정'),('6A4CC8','3:2','매실 장아찌'),('6AAB54','3:2','병량환'),('6B613C','3:1','식당'),('6BC344','4:2','네이팜탄'),('6CD0B4','1:3','꽃꽂이'),('6CD0B4','3:1','햇빛')):
            self.assertIn(word,d[a][key])

    def test_batch500f_exact_population_and_authority_order(self):
        aa=[batch500f.create(a) for a in batch500f.SOURCES];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),184)
        self.assertEqual(self.plan['draft_assets'][-541:-532],[v[2] for v in batch500f.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][5]['authored_literals'],500)
        self.assertTrue(all(u['state']=='needs_review' for u in uu))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500f_explicit_actors_and_choice_context(self):
        for a,actor in batch500f.ACTORS.items():
            aa=batch500f.create(a);src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('mugshot = '+actor),31)
            self.assertTrue(all(u['origin_portrait']==actor and u['portrait_visibility']=='shown' for u in aa['units']))
            self.assertEqual(sum(u['speaker']=='player-choice' for u in aa['units']),23)
        self.assertTrue(all(u['origin_portrait'] is None for u in batch500f.create('66C7D8')['units']))

    def test_batch500f_schedule_buffers_and_delete_warning(self):
        for a in batch500f.ACTORS:
            aa=batch500f.create(a);src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for t in ('callBufferCurrentMonth','callBufferCurrentDay','callBufferEventAMPM','callBufferEventFrequency','callBufferEventYear','callBufferEventDayName','flag = 3611','track = 467','minLength = 2','padZeros = true','BSeparate = true','BSeparate = false'):
                self.assertIn(t,src)
            d=batch500f.authored(a)
            self.assertIn('일정을',d['50:5'])
            for k in ('51:6','52:3'):self.assertIn('기념일을',d[k])
            for k in ('24:1','30:1','33:1','50:7','51:8','52:5',f'{batch500f.TRAINING[a]}:1'):
                self.assertEqual(d[k],'예  ')
            self.assertIn('덮어',d['30:0']);self.assertIn('삭제',d['4:1'])

    def test_batch500f_training_prompts_actual_source_not_actor(self):
        for a in ('670568','6762A8','6A9970','6BB2A4'):
            self.assertIn('저격',batch500f.DRAFT[a]['62:0'])
        for a in ('686A60','6CBFC0'):
            self.assertIn('계산',batch500f.DRAFT[a]['60:0'])
        for a in ('697B70','6C0E38'):
            self.assertIn('얼음 편지',batch500f.DRAFT[a]['61:0'])
        self.assertIn('기록',batch500f.DRAFT['6A9970']['45:0'])
        self.assertIn('소인',batch500f.DRAFT['6A9970']['40:0'])

    def test_batch500f_aqua_voice_exception_and_nickname(self):
        d=batch500f.DRAFT['697B70']
        self.assertIn('퓨',d['0:2']);self.assertNotIn('퓨',d['25:0'])
        self.assertNotIn('뿌',''.join(d.values()))
        self.assertTrue(batch500f.DRAFT['670568']['3:0'].startswith(',\n'))
        self.assertTrue(batch500f.DRAFT['670568']['10:1'].startswith(' 님의\n'))
        for a in batch500f.ACTORS:
            self.assertTrue(batch500f.DRAFT[a]['10:1'].endswith('\n'))
            self.assertTrue(batch500f.DRAFT[a]['25:0'].startswith(',\n'))

    def test_batch500f_tournament_wind_and_control_boundaries(self):
        aa=batch500f.create('66C7D8');d=batch500f.DRAFT['66C7D8']
        self.assertEqual(len(aa['units']),12)
        self.assertIn('맞바람',d['1:0']);self.assertIn('순풍',d['2:0'])
        self.assertIn('참가 신청을 안',d['10:0'])
        for s in (20,21,22,23):
            self.assertEqual(d[f'{s}:0'],'가자,')
            self.assertTrue(d[f'{s}:1'].startswith('\n'))
        src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('callCancelMenuTransition',src)
        self.assertEqual(src.count('flag = 3603'),4)

    def test_batch500g_exact_population_and_authority(self):
        aa=[batch500g.create(a) for a in batch500g.SOURCES];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),180)
        self.assertEqual(self.plan['draft_assets'][-532:-522],[v[2] for v in batch500g.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][6]['authored_literals'],500)
        self.assertTrue(all(u['state']=='needs_review' for u in uu))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500g_portraits_and_unshown_voice(self):
        for a,actor in batch500g.ACTORS.items():
            aa=batch500g.create(a);src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('mugshot = '+actor),32 if a in batch500g.TRAINING else 29)
            self.assertEqual(sum(u['speaker']=='player-choice' for u in aa['units']),25 if a in batch500g.TRAINING else 21)
            self.assertTrue(all(u['origin_portrait']==actor for u in aa['units']))
        for a in ('6C2660','698424'):
            self.assertTrue(all(u['origin_portrait'] is None for u in batch500g.create(a)['units']))
        greeting=batch500g.create('698424')['units']
        self.assertTrue(all(u['speaker']=='AquaMan-self-identified' for u in greeting if u['id'].startswith('698424:1:')))
        self.assertTrue(all(u['speaker']=='unshown-quick-voice' for u in greeting if u['id'].startswith('698424:2:')))

    def test_batch500g_schedule_types_and_buffers(self):
        for a in batch500g.ACTORS:
            d=batch500g.authored(a);src=(ROOT/batch500g.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertIn('일정을',d['50:5'])
            for k in ('51:6','52:3'):self.assertIn('기념일을',d[k])
            for k in ('24:1','30:1','33:1','50:7','51:8','52:5'):self.assertEqual(d[k],'예  ')
            for token in ('callBufferCurrentMonth','callBufferEventAMPM','callBufferEventFrequency','callBufferEventYear','callBufferEventDayName','flag = 3611','track = 467','padZeros = true','BSeparate = true','BSeparate = false'):self.assertIn(token,src)
            self.assertIn('덮어',d['30:0']);self.assertIn('삭제',d['4:1'])

    def test_batch500g_actual_training_and_nickname_exception(self):
        for a in ('6811F0','6A2FBC'):
            self.assertIn('계산 문제집',batch500g.DRAFT[a]['60:0'])
            self.assertIn('얼음 편지',batch500g.DRAFT[a]['61:0'])
        self.assertIn('저격 훈련',batch500g.DRAFT['6C6828']['62:0'])
        for a in batch500g.ACTORS:
            src=(ROOT/batch500g.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            script3=src.split('script 3 mmbn45 {')[1].split('}')[0]
            self.assertEqual('printPlayerNickname' in script3,a=='6811F0')
            self.assertTrue(batch500g.DRAFT[a]['10:1'].startswith('의\n'))
            self.assertTrue(batch500g.DRAFT[a]['25:0'].startswith(',\n'))

    def test_batch500g_mail_flags_nickname_and_untouched_exclamations(self):
        aa=batch500g.create('6C2660');src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(len(aa['units']),14)
        self.assertEqual(src.count('callTournamentReceiveMail'),1)
        self.assertEqual(src.count('printPlayerNickname'),3)
        for flag in (680,681,623,624,625,626,9056,9057,9058,9059,9060,9061,9062):self.assertIn('flag = '+str(flag),src)
        self.assertEqual(sum(u['translation'].startswith(',\n') for u in aa['units']),3)
        self.assertTrue(all(u['id'].endswith(':1') and u['translation'].endswith('!!') for u in aa['units']))
        self.assertEqual(sum(x.text=='!!' for x in literals(src)),14)

    def test_batch500g_source_conditioned_stutters_and_aqua_greeting(self):
        d=batch500g.DRAFT['692874']
        for key,fragment in [('0:2','뭐, 뭘'),('3:0','그, 그날'),('4:0','더, 더'),('20:0','며, 몇'),('22:0','어, 어떤'),('31:0','어, 어떤')]:self.assertIn(fragment,d[key])
        self.assertEqual(d['0:0'],'오늘은,\n')
        self.assertIn('아쿠아맨',batch500g.DRAFT['698424']['1:1'])
        self.assertIn('버림받은',batch500g.DRAFT['698424']['2:4'])
        self.assertTrue(all('퓨' in v for v in batch500g.DRAFT['698424'].values()))


    def test_batch500h_exact_population_and_authority(self):
        aa=[batch500h.create(a) for a in batch500h.SOURCES];uu=[u for a in aa for u in a['units']]
        self.assertEqual(len(uu),500);self.assertEqual(len({u['id'] for u in uu}),500)
        self.assertEqual(sum(u['speaker']=='player-choice' for u in uu),27)
        self.assertEqual(self.plan['draft_assets'][-522:-515],[v[2] for v in batch500h.SOURCES.values()])
        self.assertEqual(self.plan['batch_policy']['completed_batches'][7]['authored_literals'],500)
        self.assertTrue(all(u['state']=='needs_review' for u in uu))
        self.assertTrue(all(not a['review']['release_eligible'] for a in aa))

    def test_batch500h_unresolved_internal_errors_remain_source(self):
        for a in ('65CC78','66DDD0'):
            aa=batch500h.create(a);src=(ROOT/aa['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertIn('シートでのほうこく',src)
            self.assertNotIn(a+':0:0',{u['id'] for u in aa['units']})
            self.assertEqual(self.base[a+':0:0']['status'],'unselected_japanese')
            self.assertTrue(all(u['origin_portrait'] is None for u in aa['units']))
        self.assertEqual(batch500h.EXCLUDED,{'65CC78:0:0','66DDD0:0:0'})

    def test_batch500h_profile_and_chip_insertion_commands(self):
        for a in ('65CC78','66DDD0'):
            src=(ROOT/batch500h.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for command in ('printSchool','printOlderBro','printYoungerBro','printOlderSis','printYoungerSis','printFriend','printFavFood','printHobby','printDream','printCrush','printPlayerEnemy','printFavShow','printIdol','printBestSubject','printWorstSubject','printWish','printMostFrequentOpponent','printLostToOpponent','printDefeatedOpponent','printMostLostToOpponentsChip','printMostDefeatedOpponentsChip','printFavStandardChip1','printFavStandardChip2','printFavStandardChip3','printFavMegaChip','printFavGigaChip'):
                self.assertIn(command,src)
            self.assertNotIn('mugshotShow',src)
        windsrc=(ROOT/batch500h.create('66DDD0')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('printMostDefeatedOpponent',windsrc)
        self.assertIn('1장',batch500h.DRAFT['66DDD0']['61:1'])

    def test_batch500h_wind_and_hypothetical_reward_meaning(self):
        w=batch500h.DRAFT['66DDD0'];d=batch500h.DRAFT['65CC78']
        self.assertIn('남서쪽',w['77:1']);self.assertIn('북북동쪽',w['86:3'])
        self.assertIn('풍수',w['62:2']);self.assertIn('순풍',w['91:2']);self.assertIn('맞바람',w['91:2'])
        self.assertIn('그럴 수 있으면',d['50:5'])
        self.assertIn('브루스',d['53:3'])
        self.assertIn('R 버튼',d['61:0']);self.assertIn('R 버튼',d['63:0'])
        self.assertTrue(w['43:0'].endswith(' '));self.assertTrue(w['45:1'].endswith(' '));self.assertTrue(w['55:0'].endswith(' '))

    def test_batch500h_explicit_menu_and_reminder_portraits(self):
        menu=batch500h.create('659CB8')
        self.assertTrue(all(u['origin_portrait']=='MegaMan' for u in menu['units']))
        src=(ROOT/menu['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('mugshot = MegaMan'),33)
        for s,term in ((60,'계산 문제집'),(61,'얼음 편지'),(62,'저격 훈련')):
            self.assertIn(term,batch500h.DRAFT['659CB8'][f'{s}:0'])
        for u in batch500h.create('671684')['units']:
            script=int(u['id'].split(':')[1])
            self.assertEqual(u['origin_portrait'],'SearchMan' if 21<=script<=26 else None)
        for a in ('66A160','66C978','65AA80'):
            self.assertTrue(all(u['origin_portrait'] is None for u in batch500h.create(a)['units']))

    def test_batch500h_event_branches_and_today_list_controls(self):
        src=(ROOT/batch500h.create('671684')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for command in ('jumpIfTVShow','jumpIfPromise','jumpIfMeal','jumpIfSchool','jumpIfOther','callCheckNowEvent','flag = 3658','track = 155','frames = 96'):
            self.assertIn(command,src)
        src=(ROOT/batch500h.create('66C978')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for command in ('callFindSoonEvent','callFindTodayEvent','jumpIfNone = 3','jumpIfNone = 12','callBufferEventAMPM','padZeros = true'):
            self.assertIn(command,src)
        self.assertIn('아무것도',batch500h.DRAFT['66C978']['10:1'])
        self.assertTrue(batch500h.DRAFT['66C978']['11:2'].endswith('\n'))
        self.assertIn('주말',batch500h.DRAFT['66A160']['1:1'])
        self.assertIn('토너먼트 날',batch500h.DRAFT['66A160']['2:0'])
        self.assertIn('키 아이템',batch500h.DRAFT['66A160']['3:1'])
        self.assertIn('다음에는',batch500h.DRAFT['65AA80']['2:0'])


    def test_all_archives_validate(self):
        for a in self.assets:self.assertEqual(len(self.validate(a)),len(a['units']))

    def test_exact_remaining_archive_scope(self):
        for a,count in zip(self.assets,(271,290,253,120,129,90,125,95,90,117,92,130,124,38,18,21,21,41,36,55,67,24,11,30,2,1,1,22,19,19,3,26,16,24,6,8,23,20,3,4,10,24,3,17,4,28,2,26,36,5,4,22,21,18,19,3,18,2,10,106,21,7,2,8,21,1,130,55,102,98,73,95,73,132,128,71,31,12,14,12,6,136,31,51,6,11,102,5,4,14,57,44,2,1,18,51,51,51,51,51,51,51,51,51,31,10,51,51,51,51,51,51,51,51,51,31,10,44,44,44,44,44,44,44,44,44,44,44,15,1,44,44,44,44,44,31,31,30,32,33,30,33,30,30,32,33,34,32,30,33,32,32,24,32,30,22,24,30,52,28,61,61,61,61,61,61,61,61,12,57,57,57,57,57,64,64,64,14,9,196,205,67,18,6,6,2,139,162,158,14,15,11,1,142,132,136,14,14,14,18,10,20,145,144,149,14,14,27,6,1,187,163,124,14,6,6,138,141,126,56,28,10,1,194,209,8,3,6,4,16,1,14,15,6,20,2,1,1,183,220,26,14,8,5,7,3,14,8,6,6,1,77,42,153,131,48,48,479,21,253,243,4,255,244,1,258,240,2,238,241,21,264,225,11,222,225,53,219,215,66,213,211,49,27,211,194,67,28,135,132,174,59,191,191,51,65,2,191,191,68,50,218,212,70,172,141,184,3,325,134,41,270,84,80,30,36,42,42,42,42,42,42,42,42,42,42,42,9,29,42,43,42,42,42,42,42,42,42,42,79,14,46,39,22,32,29,52,38,34,43,38,13,52,27,21,18,24,26,63,25,29,24,41,72,37,36,27,26,9,19,24,29,29,28,27,27,27,27,28,28,27,27,28,27,27,27,27,27,27,6,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,27,27,27,6,77,42,45,306,16,33,5,3,27,1,22,81,46,278,23,4,7,27,5,29,482,4,8,5,1,377,27,29,45,5,8,7,2,3,4,7,4,5,3,6,7,7,6,4,17,14,10,6,7,4,5,3,1,14,9,6,6,4,5,4,28,1,16,15,9,5,6,3,4,6,8,4,4,2,1,20,6,5,4,6,3,1,6,7,4,2,14,1,56,14,10,6,6,5,5,2,1,20,6,7,15,5,6,4,5,7,6,6,4,2,3,15,9,5,6,4,1,10,7,5,6,3,12,1,15,11,6,7,5,4,3,18,6,6,3,5,3,3,5,22,16,10,10,32,15,14,3,2,2,2,2,3,1,2,1,20,4,6,4,4,3,3,5,8,8,3,2,1,7,3,12,3,2,4,5,9,49,20,6,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,28,13,12,49,13,1,34,10,1,1,1,1,26,1,1,67,1,1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,6,4,3,2,9,4,4,4,2,4,5,4,1,3,2,7,5,5,3,1,1,1,10,14,1,1,1,1,1,2,2,4)):
            expected={k for k,u in self.base.items() if u['archive']==a['archive'] and u['status']=='unselected_japanese'}
            expected-=batch500e.EXCLUDED
            expected-=batch500h.EXCLUDED
            expected-=batch500k.EXCLUDED
            expected-=batch500m.EXCLUDED
            expected-=batch500n.EXCLUDED
            expected-=batch500o.EXCLUDED
            expected-=batch500r.EXCLUDED
            expected-=batch500t.EXCLUDED
            expected-=batch500u.EXCLUDED
            expected-=batch500v.EXCLUDED
            expected-=batch500w.EXCLUDED
            expected-=batch500x.EXCLUDED
            expected-=batch500y.EXCLUDED
            expected-=batch500z.EXCLUDED
            expected-=batch500aa.EXCLUDED
            expected-=batch500ab.EXCLUDED
            expected-=batch500ac.EXCLUDED
            expected-=batch500ad.EXCLUDED
            expected-=batch500ae.EXCLUDED
            expected-=batch500af.EXCLUDED
            expected-=batch500an.EXCLUDED
            expected-=batch500ao.EXCLUDED
            if a.get('batch_id')=='batch500-042':expected={a['archive']+':'+k for k in batch500ap.DRAFT[a['archive']]}
            if a.get('batch_id')=='batch500-043':expected={a['archive']+':'+k for k in batch500aq.DRAFT[a['archive']]}
            if a.get('batch_id')=='batch500-044':expected={a['archive']+':'+k for k in batch500ar.DRAFT[a['archive']]}
            if a.get('batch_id')=='batch500-045':expected={a['archive']+':'+k for k in batch500as.DRAFT[a['archive']]}
            if a['archive']=='6713B8':expected.discard('6713B8:0:0')
            if a['archive']=='65AAE0':expected.discard('65AAE0:0:0')
            if a['archive']=='7CAF40':expected-={'7CAF40:0:0','7CAF40:0:1','7CAF40:0:2','7CAF40:22:0'}
            if a['archive']=='7C9C44':expected-= {'7C9C44:0:0','7C9C44:0:1'}
            if a['archive']=='7C0F8C':expected.discard('7C0F8C:0:0')  # Unresolved provisional test retained in ledger.
            if a.get('batch_id')=='batch500-046':expected={a['archive']+':'+k for k in batch500at.DRAFT[a['archive']]}
            if a.get('batch_id')=='final-047':expected={a['archive']+':'+k for k in final047.DRAFT[a['archive']]}
            self.assertEqual({u['id'] for u in a['units']},expected)
            self.assertEqual(len(a['units']),count)

    def test_reproducible_authority_assets(self):
        for a,name in zip(self.assets,self.plan['draft_assets']):
            self.assertEqual(a,json.loads((ROOT/name).read_text(encoding='utf8')))

    def test_background_b_types_and_grid(self):
        a=next(a for a in self.assets if a['archive']=='7BEB18');u={x['id']:x for x in a['units']}
        self.assertEqual([u[f'7BEB18:11:{i}']['translation'] for i in (1,2,3,4)],['메툴','브루스\n','푸른 하늘','그만두기\n'])
        self.assertTrue(all(u[f'7BEB18:11:{i}']['speaker']=='player-choice' for i in (1,2,3,4)))
        self.assertTrue(all(u[f'7BEB18:11:{i}']['portrait_visibility']=='hidden' for i in (1,2,3,4)))
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for v in (3,4,5):self.assertIn(f'callSetHomepageBG\n\t\ttype = {v}',src)
        self.assertIn('disableB = true',src)
        self.assertIn('count = 24',src)
        old=next(a for a in self.assets if a['archive']=='7BB878')
        self.assertEqual([x['translation'] for x in a['units'] if x['id'].split(':')[1]=='10'],[x['translation'] for x in old['units'] if x['id'].split(':')[1]=='10'])

    def test_purple_pink_battle_voices_and_result_boundaries(self):
        a=next(a for a in self.assets if a['archive']=='7BF018');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7BF018:0:0']['origin_portrait'],'NaviGirlPurple')
        self.assertEqual(u['7BF018:4:0']['origin_portrait'],'NormalNaviPink')
        self.assertIn('일주일에 한 번',u['7BF018:0:0']['translation'])
        self.assertIn('먹이',u['7BF018:4:1']['translation']);self.assertIn('목숨',u['7BF018:7:0']['translation'])
        for s in (0,4):
            for i in (2,3):self.assertEqual(u[f'7BF018:{s}:{i}']['speaker'],'player-choice')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for v in (195,196,673,674):self.assertIn(f'value = {v}',src)

    def test_organ_decline_and_tournament_branch_protection(self):
        a=next(a for a in self.assets if a['archive']=='7BF258');u={x['id']:x for x in a['units']}
        self.assertIn('쉰 소리',u['7BF258:0:2']['translation']);self.assertIn('망가져',u['7BF258:0:4']['translation'])
        self.assertIn('삭제해라',u['7BF258:12:0']['translation']);self.assertIn('삭제',u['7BF258:14:0']['translation'])
        self.assertIn('양지',u['7BF258:15:0']['translation'])
        self.assertEqual(u['7BF258:20:0']['origin_portrait'],'HeelNaviPurple')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertLess(src.index('flag = 1929'),src.index('checkNetTime'))
        for h in (9,13,16,20):
            self.assertIn(f'lowerHour = {h}',src);self.assertIn(f'upperHour = {h}',src)
        self.assertEqual(src.count('upperMinutes = 59'),4)

    def test_fallen_navi_hidden_observation(self):
        a=next(a for a in self.assets if a['archive']=='7BF8C0');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7BF8C0:0:0']['translation'],'......')
        self.assertEqual(u['7BF8C0:0:0']['portrait_visibility'],'visible')
        for i in (1,2):
            self.assertEqual(u[f'7BF8C0:0:{i}']['speaker'],'system-observation')
            self.assertEqual(u[f'7BF8C0:0:{i}']['portrait_visibility'],'hidden')
        self.assertIn('숨이 끊어진 것 같다',u['7BF8C0:0:2']['translation'])
        self.assertIn('animation = 0',(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig'))

    def test_dark_battles_options_and_rhetoric(self):
        a=next(a for a in self.assets if a['archive']=='7BFC50');u={x['id']:x for x in a['units']}
        for s,i in ((0,2),(0,3),(4,1),(4,2)):
            self.assertEqual(u[f'7BFC50:{s}:{i}']['speaker'],'player-choice')
            self.assertEqual(u[f'7BFC50:{s}:{i}']['portrait_visibility'],'hidden')
        self.assertIn('어둠의 힘',u['7BFC50:4:0']['translation'])
        self.assertIn('통하지 않다니',u['7BFC50:6:0']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for v in (197,198,675,676):self.assertIn(f'value = {v}',src)
        for w in (8,9):self.assertIn(f'width = {w}',src)

    def test_windman_nickname_and_offer(self):
        a=next(a for a in self.assets if a['archive']=='7C0668');u={x['id']:x for x in a['units']}
        self.assertTrue(u['7C0668:0:3']['translation'].startswith(','))
        self.assertEqual(u['7C0668:0:3']['speaker'],'WindMan')
        self.assertEqual(u['7C0668:0:6']['speaker'],'MrProgGreen')
        for i in (4,5):
            self.assertEqual(u[f'7C0668:0:{i}']['speaker'],'player-choice')
            self.assertEqual(u[f'7C0668:0:{i}']['portrait_visibility'],'hidden')
        self.assertIn('인터넷1',u['7C0668:0:8']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('printPlayerNickname',src);self.assertIn('flag = 4929',src)

    def test_field_mid_script_portraits_and_reports(self):
        a=next(a for a in self.assets if a['archive']=='7C0F8C');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7C0F8C:12:0']['speaker'],'ProtoMan')
        self.assertEqual(u['7C0F8C:12:1']['speaker'],'NormalNaviYellow')
        self.assertEqual(u['7C0F8C:13:1']['speaker'],'NaviGirlPurple')
        self.assertEqual(u['7C0F8C:36:1']['speaker'],'ProtoMan')
        self.assertEqual(u['7C0F8C:36:2']['speaker'],'NormalNaviPink')
        self.assertIn('완수했습니다',u['7C0F8C:1:0']['translation'])
        self.assertIn('실패',u['7C0F8C:2:0']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('value = 513'),32)
        self.assertEqual(src.count('flag = 5473'),32)

    def test_field_surrender_unnamed_place_and_gang_candidates(self):
        a=next(a for a in self.assets if a['archive']=='7C0F8C');u={x['id']:x for x in a['units']}
        self.assertIn('붙잡혀 주지',u['7C0F8C:25:1']['translation'])
        self.assertIn('할 줄 알았냐',u['7C0F8C:25:2']['translation'])
        self.assertIn('그곳',u['7C0F8C:28:2']['translation'])
        self.assertIn('삭제되는 편',u['7C0F8C:28:3']['translation'])
        self.assertIn('그림자 군단',u['7C0F8C:32:3']['translation'])
        self.assertIn('언더인터넷',u['7C0F8C:39:1']['translation'])

    def test_provisional_consumers_drafted_but_not_rom_selected(self):
        ids={u['id'] for a in self.assets for u in a['units']}
        self.assertIn('7C0F8C:0:0',ids);self.assertIn('7C0970:0:0',ids)
        for arc in ('7C0F8C','7C0970'):
            asset=final047.create(arc);self.assertFalse(asset['review']['release_eligible'])
            self.assertIn('임시',asset['units'][0]['translation'])
        ledger=json.loads((ROOT/'analysis/translation_first_v1/worklist.json').read_text(encoding='utf8'))
        for u in ledger['units']:
            if u['id'] in ('7C0F8C:0:0','7C0970:0:0'):
                self.assertEqual(u['draft_stage'],'authored_draft_not_in_rom')
                self.assertEqual(u['authored_translation'],final047.DRAFT[u['archive']][u['id'].split(':',1)[1]])
        a=next(a for a in self.assets if a['archive']=='7BFE4C')
        self.assertEqual([u['translation'] for u in a['units']],['기시시...','니시시...'])

    def test_heart_star_reward_fragments_and_actors(self):
        for arc,actor,erase in (('7C6BC0','Roll','callRollHeartDataErase'),('7C6F90','StarMan','callStarManStarDataErase')):
            a=next(a for a in self.assets if a['archive']==arc);u={x['id']:x for x in a['units']}
            for s in (0,1,2):
                self.assertEqual(u[f'{arc}:{s}:0']['speaker'],actor)
                self.assertEqual(u[f'{arc}:{s}:6']['speaker'],actor)
                for i in (1,2,3,4,5):
                    self.assertEqual(u[f'{arc}:{s}:{i}']['speaker'],'system-narration')
                    self.assertEqual(u[f'{arc}:{s}:{i}']['portrait_visibility'],'hidden')
                self.assertEqual([u[f'{arc}:{s}:{i}']['translation'] for i in (2,3)],['.','.'])
                self.assertTrue(u[f'{arc}:{s}:1']['translation'].startswith(','))
            self.assertIn('강화 프로그램',u[f'{arc}:0:4']['translation'])
            self.assertIn('제니',u[f'{arc}:1:5']['translation'])
            self.assertIn('버그 조각',u[f'{arc}:2:4']['translation'])
            self.assertTrue(u[f'{arc}:2:5']['translation'].startswith('개'))
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('frames = 10'),9)
            self.assertEqual(src.count(erase),3)
            self.assertEqual(src.count('amount = 4294967295'),2)

    def test_strengthening_unshown_system_and_spoken_hints(self):
        for arc,actor in (('7C6D7C','ThunderMan'),('7C6E94','WoodMan')):
            a=next(a for a in self.assets if a['archive']==arc);u={x['id']:x for x in a['units']}
            self.assertEqual(u[f'{arc}:0:0']['speaker'],actor)
            self.assertEqual(u[f'{arc}:1:0']['speaker'],'system-narration')
            self.assertEqual(u[f'{arc}:1:0']['portrait_visibility'],'not-shown-in-script')
            self.assertIsNone(u[f'{arc}:1:0']['origin_portrait'])
            self.assertEqual(u[f'{arc}:2:0']['speaker'],'system-narration')
            self.assertEqual(u[f'{arc}:2:0']['portrait_visibility'],'not-shown-in-script')
            last=2 if arc=='7C6D7C' else 3
            self.assertEqual(u[f'{arc}:2:{last}']['speaker'],'system-narration')
            self.assertEqual(u[f'{arc}:2:{last}']['portrait_visibility'],'hidden')
            self.assertIn('강화되었다',u[f'{arc}:2:{last}']['translation'])
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertIn('item = 33',src);self.assertIn('playerResetScene',src)

    def test_strengthening_variable_phrasing_and_source_imagery(self):
        thunder=next(a for a in self.assets if a['archive']=='7C6D7C');wood=next(a for a in self.assets if a['archive']=='7C6E94')
        t={x['id']:x['translation'] for x in thunder['units']};w={x['id']:x['translation'] for x in wood['units']}
        self.assertTrue(t['7C6D7C:0:1'].startswith(':'))
        self.assertTrue(t['7C6D7C:2:0'].startswith('에서'))
        self.assertIn('전기',t['7C6D7C:2:0'])
        self.assertTrue(w['7C6E94:0:2'].startswith(':'))
        self.assertTrue(w['7C6E94:1:0'].startswith(':'))
        self.assertIn('음이온',w['7C6E94:2:0'])
        self.assertIn('치유의 힘',w['7C6E94:2:3'])

    def test_failed_return_matches_formal_mission_report(self):
        a=next(a for a in self.assets if a['archive']=='7C6E50');u={x['id']:x for x in a['units']}
        self.assertTrue(all(x['speaker']=='ProtoMan' for x in a['units']))
        self.assertIn('실패',u['7C6E50:0:0']['translation'])
        self.assertIn('귀환하겠습니다',u['7C6E50:0:1']['translation'])
        old=next(a for a in self.assets if a['archive']=='7C0F8C')
        self.assertTrue(any(x['translation']=='면목이... 없습니다' for x in old['units']))
        self.assertEqual(len(a['units']),2)

    def test_practice_all_navi_actor_routes(self):
        names=['MegaMan','Roll','GutsMan','WindMan','SearchMan','FireMan','ThunderMan','ProtoMan','NumberMan','MetalMan','JunkMan','AquaMan','WoodMan','StarMan','ShadowMan','KnightMan','NapalmMan','IceMan','ElecMan','PlantMan','Bass']
        intro=next(a for a in self.assets if a['archive']=='7C7188');success=next(a for a in self.assets if a['archive']=='7C802C')
        for a in (intro,success):
            for u in a['units']:
                s=int(u['id'].split(':')[1]);self.assertEqual(u['speaker'],names[s%21])
                self.assertEqual(u['portrait_visibility'],'visible')
        src=(ROOT/intro['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('flag = 3863'),42)
        self.assertEqual(src.count('jumpIfUnused1 = continue'),2)
        self.assertEqual(src.count('jumpIfUnused2 = continue'),2)
        self.assertNotIn('flag = 3863',(ROOT/success['source_tpl']['path']).read_text(encoding='utf-8-sig'))

    def test_practice_retry_is_not_a_choice(self):
        a=next(a for a in self.assets if a['archive']=='7C7188');u={x['id']:x for x in a['units']}
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertNotIn('select',src);self.assertNotIn('option',src)
        self.assertIn('다시 한 번',u['7C7188:35:1']['translation'])
        self.assertIn('기회를',u['7C7188:28:0']['translation'])
        self.assertIn('납득할 수 없다고요',u['7C7188:29:1']['translation'])
        self.assertIn('발목',u['7C7188:37:1']['translation'])

    def test_practice_success_nickname_and_tics(self):
        a=next(a for a in self.assets if a['archive']=='7C802C');u={x['id']:x for x in a['units']}
        for s,i in ((0,0),(1,1),(2,0),(4,1),(7,0),(10,0),(13,0)):
            self.assertTrue(u[f'7C802C:{s}:{i}']['translation'].startswith(','))
        self.assertIn('가스',u['7C802C:2:0']['translation'])
        self.assertIn('퓨',u['7C802C:11:0']['translation'])
        self.assertIn('것 같아',u['7C802C:11:1']['translation'])
        self.assertIn('임무 완료',u['7C802C:4:0']['translation'])

    def test_practice_images_and_threats_remain_source_meaning(self):
        a=next(a for a in self.assets if a['archive']=='7C7188');u={x['id']:x for x in a['units']}
        self.assertIn('삭제되느냐',u['7C7188:10:1']['translation'])
        self.assertIn('오퍼레이터',u['7C7188:20:0']['translation'])
        self.assertIn('그 몸',u['7C7188:20:2']['translation'])
        self.assertIn('꽃피우기',u['7C7188:19:2']['translation'])
        s=next(a for a in self.assets if a['archive']=='7C802C');v={x['id']:x for x in s['units']}
        self.assertIn('기초',v['7C802C:3:0']['translation'])
        self.assertIn('꽃',v['7C802C:19:2']['translation'])

    def test_shadow_request_failure_separate_from_practice(self):
        a=next(a for a in self.assets if a['archive']=='7C714C')
        self.assertEqual(len(a['units']),1)
        self.assertEqual(a['units'][0]['speaker'],'ShadowMan')
        self.assertIn('의뢰',a['units'][0]['translation'])
        self.assertIn('실패',a['units'][0]['translation'])
        self.assertNotIn('flag = 3863',(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig'))

    def test_fortune_wait_dots_not_prose_or_timing(self):
        a=rollprofile.create('65FF3C')
        self.assertEqual(len(a['units']),6)
        self.assertTrue(all(x['source']=='・' and x['translation']=='.' for x in a['units']))
        self.assertTrue(all(x['speaker']=='fortune-wait-punctuation' for x in a['units']))
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('frames = 30'),8)
        self.assertIn('checkHeartDataLocation',src)
        self.assertIn('amount = 4294967295',src)

    def test_roll_reminder_remaining_name_and_actor(self):
        a=rollprofile.create('660D90');u={x['id']:x for x in a['units']}
        self.assertNotIn('660D90:3:0',u)
        self.assertNotIn('660D90:4:0',u)
        self.assertNotIn('660D90:6:0',u)
        for x in a['units']:
            s=int(x['id'].split(':')[1])
            self.assertEqual(x['origin_portrait'],'Roll' if s>=20 else None)
        for s in (1,21):self.assertTrue(u[f'660D90:{s}:0']['translation'].startswith(' 시작할'))
        for s in (2,22):self.assertTrue(u[f'660D90:{s}:0']['translation'].startswith(chr(10)+'약속'))
        self.assertIn('학원',u['660D90:24:0']['translation'])

    def test_roll_reminder_remaining_event_structure(self):
        a=rollprofile.create('660D90');src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('flag = 3658','flag = 3585','callBufferEventName','printScheduleBuffer',
                  'jumpIfTVShow = 1','jumpIfTVShow = 21','jumpIfExists = 6','jumpIfExists = 26',
                  'left = 92','top = 110','mugshot = Roll'):self.assertIn(t,src)
        self.assertEqual(src.count('track = 155'),2)
        self.assertEqual(src.count('frames = 96'),2)

    def test_profile_b_partial_scope_and_choices(self):
        a=rollprofile.create('661858');u={x['id']:x for x in a['units']}
        self.assertEqual(len(u),102)
        for s in (1,3,5,7,11,27,29):self.assertNotIn(f'661858:{s}:0',u)
        self.assertTrue(all(x['origin_portrait'] is None for x in a['units']))
        for s,i in rollprofile.CHOICES:
            self.assertEqual(u[f'661858:{s}:{i}']['speaker'],'player-choice')
            if i==1:self.assertTrue(u[f'661858:{s}:{i}']['translation'].endswith('  '))
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('printStringBuffer1','printStringBuffer2','printStringBuffer3','variable = 22',
                  'variable = 23','variable = 5','flag = 3605','flag = 3606'):self.assertIn(t,src)
        self.assertNotIn('mugshotShow',src)

    def test_profile_b_gender_guess_and_self_correction(self):
        u={x['id']:x for x in rollprofile.create('661858')['units']}
        for key,t in (('40:0','형이나 오빠'),('46:0','누나나 언니'),('17:2','여자아이'),
                      ('19:3','남자아이'),('85:0','아삭아삭'),('85:1','아니었나'),
                      ('91:1','털북숭이'),('91:2','아니었어'),('13:1','1'),('94:0','유행')):
            self.assertIn(t,u['661858:'+key]['translation'])

    def test_progress_hint_destinations_and_uncertainty(self):
        a=hintmenu.create('65E8B8');u={x['id']:x for x in a['units']}
        for s,n in ((16,3),(18,5),(19,7),(20,9),(21,10),(22,12)):
            self.assertIn(f'인터넷{n}',u[f'65E8B8:{s}:0']['translation'])
        self.assertIn('것 같',u['65E8B8:17:0']['translation'])
        self.assertIn('것 같',u['65E8B8:24:0']['translation'])
        self.assertIn('인터넷9',u['65E8B8:25:0']['translation'])
        self.assertTrue(u['65E8B8:13:1']['translation'].startswith('」 칩을'))
        self.assertTrue(all(x['origin_portrait'] is None for x in a['units']))

    def test_progress_hint_priority_and_calendar_routes(self):
        a=hintmenu.create('65E8B8');src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('bitmask = 4','chip = 104','item = 1','item = 11','lower = 0','lower = 6',
                  'jumpIfInRange = 34','jumpIfInRange = 30','jumpIfTrue = 33','flag = 2'):
            self.assertIn(t,src)
        for f in (*range(8904,8911),*range(9416,9423)):self.assertIn(f'flag = {f}',src)
        self.assertNotIn('mugshotShow',src)

    def test_roll_menu_unselected_only_and_portraits(self):
        a=hintmenu.create('65F11C');u={x['id']:x for x in a['units']}
        self.assertEqual(len(u),51)
        for key in ('0:0','1:0','2:0','20:0','21:0','22:0','23:0','24:0'):
            self.assertNotIn('65F11C:'+key,u)
        self.assertEqual(len(hintmenu.CHOICES),21)
        self.assertTrue(all(x['origin_portrait']=='Roll' for x in a['units']))
        for s,i in hintmenu.CHOICES:
            x=u[f'65F11C:{s}:{i}']
            self.assertEqual(x['speaker'],'player-choice')
            self.assertEqual(x['portrait_visibility'],'visible')

    def test_roll_menu_warnings_and_deletion_fragments(self):
        u={x['id']:x for x in hintmenu.create('65F11C')['units']}
        self.assertIn('이미 지났',u['65F11C:3:0']['translation'])
        self.assertIn('더는 등록',u['65F11C:4:0']['translation'])
        self.assertIn('같은 시간',u['65F11C:25:1']['translation'])
        self.assertIn('덮어쓰',u['65F11C:30:0']['translation'])
        self.assertIn('일정',u['65F11C:50:5']['translation'])
        for s,i in ((51,6),(52,3)):self.assertIn('기념일',u[f'65F11C:{s}:{i}']['translation'])
        self.assertEqual(u['65F11C:10:0']['translation'],'이건:')
        self.assertIn('계산 문제집',u['65F11C:60:0']['translation'])

    def test_roll_menu_options_buffers_and_no_action(self):
        a=hintmenu.create('65F11C');src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('width = 7','width = 8','default = 1','BSeparate = true','BSeparate = false',
                  'callBufferEventYear','callBufferEventFrequency','callBufferEventDayName',
                  'callBufferEventAMPM','flag = 3611','frames = 1','track = 467'):
            self.assertIn(t,src)
        for x in a['units']:
            if x['source'].endswith('  '):self.assertEqual(x['translation'][-2:],'  ')
        self.assertFalse(a['review']['release_eligible'])
        self.assertIn('not selected by ROM builder',a['insertion_state'])

    def test_quick_tournament_status(self):
        a=quick.create('65B74C');u={x['id']:x for x in a['units']}
        self.assertIn('우승',u['65B74C:2:0']['translation'])
        self.assertIn('신청을 안',u['65B74C:10:0']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('callCancelMenuTransition',src)
        self.assertEqual(src.count('flag = 3603'),4)
        self.assertEqual(src.count('printPlayerNickname'),6)

    def test_quick_agenda_time_boundary(self):
        a=quick.create('65B8E4');u={x['id']:x for x in a['units']}
        self.assertEqual(u['65B8E4:11:2']['translation'],'부터'+chr(10))
        self.assertEqual(u['65B8E4:3:0']['translation'],' 일정이 있어!')
        self.assertEqual(u['65B8E4:12:0']['translation'],' 일정이야!')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('callBufferEventHour','callBufferEventMinutes','callBufferEventAMPM','padZeros = true',
                  'padZeros = false','jumpIfNone = 2','jumpIfNone = 3','jumpIfExists = 11','jumpIfNone = 12'):
            self.assertIn(t,src)

    def test_quick_profile_siblings_and_liked_person(self):
        u={x['id']:x for x in quick.create('65B9E8')['units']}
        for key,text in (('1:4','형이나 오빠'),('5:4','누나나 언니'),('3:5','남동생'),
                         ('7:4','여동생'),('17:1','여자아이'),('19:1','남자아이'),('23:2','불편한 사람')):
            self.assertIn(text,u['65B9E8:'+key]['translation'])

    def test_quick_profile_twenty_four_choices(self):
        u={x['id']:x for x in quick.create('65B9E8')['units']}
        self.assertEqual(len(quick.CHOICES),24)
        for s,i in quick.CHOICES:self.assertEqual(u[f'65B9E8:{s}:{i}']['speaker'],'player-choice')
        for s in (41,44,47,50,53,56,59,62):
            self.assertTrue(u[f'65B9E8:{s}:0']['translation'].endswith(chr(10)*2))
            self.assertEqual(u[f'65B9E8:{s}:1']['translation'],'있어  ')
            self.assertEqual(u[f'65B9E8:{s}:2']['translation'],'없어')

    def test_quick_profile_route_buffers(self):
        a=quick.create('65B9E8');src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('variable = 22','jumpIfEqual = 19','variable = 23','jumpIfEqual = 33','jumpIfEqual = 34',
                  'variable = 5','printStringBuffer1','printStringBuffer2','printStringBuffer3','flag = 3605',
                  'flag = 3606','flag = 3735','flag = 3749'):self.assertIn(t,src)
        u={x['id']:x for x in a['units']}
        for s,i,t in ((32,2,'유치원'),(33,1,'학교'),(34,1,'회사')):
            self.assertIn(t,u[f'65B9E8:{s}:{i}']['translation'])

    def test_quick_actor_and_nonselected_literals(self):
        from tpl_literals import literals
        for archive in quick.SOURCES:
            a=quick.create(archive);selected={x['id'] for x in a['units']}
            self.assertTrue(all(x['origin_portrait'] is None for x in a['units']))
            src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertNotIn('mugshotShow',src)
            indexed={x.key:x.text for x in literals(src)}
            for script,values in quick.DRAFT[archive].items():
                for i,value in enumerate(values):
                    key=f'{archive}:{script}:{i}'
                    self.assertIn(key,indexed)
                    if key not in selected:self.assertEqual(value,indexed[key])

    def test_reminder_event_meaning_and_name_suffix(self):
        a=next(a for a in self.assets if a['archive']=='65AFA0');u={x['id']:x for x in a['units']}
        for s in (1,21):
            self.assertTrue(u[f'65AFA0:{s}:0']['translation'].startswith(' 시작할'))
            self.assertIn('TV',u[f'65AFA0:{s}:0']['translation'])
        for s in (2,22):self.assertEqual(u[f'65AFA0:{s}:0']['translation'],'\n약속 시간이야!\n기대되네!')
        for s in (4,24):self.assertIn('학원',u[f'65AFA0:{s}:0']['translation'])
        self.assertEqual(u['65AFA0:5:0']['translation'],'\n시간이야!')
        self.assertEqual(u['65AFA0:25:0']['translation'],' 시간이야!')
        for x in a['units']:
            script=int(x['id'].split(':')[1])
            self.assertEqual(x['origin_portrait'],'MegaMan' if script>=20 else None)
            self.assertEqual(x['speaker'],'MegaMan' if script>=20 else 'unshown-reminder-voice')

    def test_reminder_dispatch_flags_and_coordinates(self):
        a=next(a for a in self.assets if a['archive']=='65AFA0')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('callBufferReminders','callBufferEventName','printScheduleBuffer','callCheckNowEvent',
                      'jumpIfTVShow = 1','jumpIfPromise = 2','jumpIfMeal = 3','jumpIfSchool = 4','jumpIfOther = 5',
                      'jumpIfTVShow = 21','jumpIfExists = 6','jumpIfExists = 26','flag = 3658',
                      'left = 92','top = 110','left = 225','top = 141'):
            self.assertIn(token,src)
        self.assertEqual(src.count('track = 155'),2)
        self.assertEqual(src.count('frames = 96'),2)

    def test_mail_alert_nickname_and_no_inferred_actor(self):
        a=next(a for a in self.assets if a['archive']=='65B220');u={x['id']:x for x in a['units']}
        for s in (1,2,3):self.assertEqual(u[f'65B220:{s}:1']['translation'],',\n메일이야!!')
        self.assertTrue(all(x['origin_portrait'] is None and x['speaker']=='unshown-mail-alert-voice' for x in a['units']))
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('"!!"'),14)
        self.assertEqual(src.count('printPlayerNickname'),3)
        self.assertEqual(src.count('track = 155'),28)
        self.assertEqual(src.count('frames = 96'),28)
        for f in (3585,680,681,623,624,625,626,*range(8904,8911)):self.assertIn(f'flag = {f}',src)
        self.assertIn('callTournamentReceiveMail',src)
        self.assertNotIn('mugshotShow',src)

    def test_miniresult_reward_sources_and_fragments(self):
        a=next(a for a in self.assets if a['archive']=='65AAE0');u={x['id']:x for x in a['units']}
        self.assertIn('문제집',u['65AAE0:52:1']['translation'])
        self.assertIn('편지 사이',u['65AAE0:62:1']['translation'])
        self.assertIn('데이터',u['65AAE0:72:1']['translation'])
        for s in (53,63,73):
            self.assertEqual(u[f'65AAE0:{s}:2']['translation'],'버그 조각이 ')
            self.assertTrue(u[f'65AAE0:{s}:3']['translation'].startswith('개'+chr(10)))
        self.assertIn('실패',u['65AAE0:50:0']['translation'])
        self.assertIn('퍼즐',u['65AAE0:60:1']['translation'])
        self.assertIn('미션',u['65AAE0:70:1']['translation'])

    def test_miniresult_commands_and_layout_preserved(self):
        a=next(a for a in self.assets if a['archive']=='65AAE0')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('flag = 3585'),3)
        self.assertEqual(src.count('callBufferRecordMinigameResults'),3)
        self.assertEqual(src.count('amount = 4294967295'),6)
        self.assertEqual(src.count('item = 33'),3)
        self.assertEqual(src.count('buffer = 3'),6)
        for token in ('minigame = 0','minigame = 1','minigame = 2','left = 92','top = 110','left = 225','top = 141'):
            self.assertIn(token,src)

    def test_miniresult_unshown_actor_and_provisional_pending(self):
        a=next(a for a in self.assets if a['archive']=='65AAE0')
        for u in a['units']:
            self.assertEqual(u['speaker'],'unshown-result-voice')
            self.assertIsNone(u['origin_portrait'])
            self.assertEqual(u['portrait_visibility'],'not-shown-in-script')
        self.assertNotIn('65AAE0:0:0',{u['id'] for u in a['units']})
        ledger=json.loads((ROOT/'analysis/translation_first_v1/worklist.json').read_text(encoding='utf8'))
        u=next(x for x in ledger['units'] if x['id']=='65AAE0:0:0')
        self.assertEqual(u['draft_stage'],'authored_draft_not_in_rom')
        self.assertEqual(u['authored_translation'],'임시 문구입니다')
        provisional=batch500at.create('65AAE0')['units'][0]
        self.assertEqual(provisional['speaker'],'speaker-unestablished')
        self.assertEqual(provisional['state'],'needs_review')

    def test_credits_exact_alignment_and_no_portrait(self):
        a=next(a for a in self.assets if a['archive']=='7CE5C8')
        for u in a['units']:
            for side in ('left','right'):
                src=u['source'];dst=u['translation']
                trim=str.lstrip if side=='left' else str.rstrip
                self.assertEqual(len(src)-len(trim(src,' ')),len(dst)-len(trim(dst,' ')))
            self.assertIsNone(u['origin_portrait'])
            self.assertEqual(u['portrait_visibility'],'not-shown-in-script')
        self.assertFalse(any(u['id'].startswith('7CE5C8:52:') for u in a['units']))

    def test_credits_time_chip_and_title_preservation(self):
        a=next(a for a in self.assets if a['archive']=='7CE5C8');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7CE5C8:64:0']['translation'],'클리어 시간     ')
        self.assertEqual(u['7CE5C8:65:0']['translation'],'데이터 라이브러리 S  ')
        for s,i in ((65,1),(66,1),(67,1)):self.assertEqual(u[f'7CE5C8:{s}:{i}']['translation'],'장')
        self.assertIn('4.5',u['7CE5C8:68:0']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('printBuffer'),5)
        self.assertEqual(src.count('minLength = 2'),2)
        self.assertEqual(src.count('minLength = 3'),3)
        self.assertEqual(src.count('padZeros = true'),2)
        self.assertIn('"         M  "',src)
        self.assertIn('"         G  "',src)

    def test_credits_staff_attribution_and_roles(self):
        a=next(a for a in self.assets if a['archive']=='7CE5C8');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7CE5C8:1:0']['translation'],'        야스마 마사히로')
        self.assertIn('코나미JPN 코지마 히데오',u['7CE5C8:57:0']['translation'])
        self.assertIn('두 번째 개발부',u['7CE5C8:60:0']['translation'])
        self.assertIn('이나후네 케이지',u['7CE5C8:63:0']['translation'])
        self.assertEqual(u['7CE5C8:43:0']['translation'],'버그 검사 총괄')

    def test_manager_names_choices_and_variable_boundaries(self):
        a=next(a for a in self.assets if a['archive']=='7CC6A0');u={x['id']:x for x in a['units']}
        for s in range(16):
            self.assertTrue(u[f'7CC6A0:{s}:0']['translation'].endswith(chr(10)))
            self.assertEqual(u[f'7CC6A0:{s}:1']['translation'],' 님의')
            for i in (4,5):
                self.assertEqual(u[f'7CC6A0:{s}:{i}']['speaker'],'player-choice')
                self.assertEqual(u[f'7CC6A0:{s}:{i}']['portrait_visibility'],'visible')
            self.assertEqual(u[f'7CC6A0:{s}:4']['translation'],'예 ')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('printPlayerName'),16)
        self.assertEqual(src.count('buffer = true'),4)
        for token in ('printSchool','printOlderBro4','printYoungerSis4','printFriend8','printWish3','width = 11','width = 7'):
            self.assertIn(token,src)

    def test_manager_edit_delete_no_action_and_labels(self):
        a=next(a for a in self.assets if a['archive']=='7CC6A0');u={x['id']:x for x in a['units']}
        self.assertEqual([u[f'7CC6A0:22:{i}']['translation'] for i in (2,3,4)],['수정 ','삭제'+chr(10),'아무것도 안 함'])
        for i in (2,3,4):self.assertEqual(u[f'7CC6A0:22:{i}']['speaker'],'player-choice')
        self.assertIn('수정하시겠습니까',u['7CC6A0:23:1']['translation'])
        self.assertIn('삭제하시겠습니까',u['7CC6A0:24:1']['translation'])
        self.assertIn('삭제했습니다',u['7CC6A0:25:1']['translation'])
        for s in range(75,93):
            self.assertEqual(u[f'7CC6A0:{s}:0']['consumer_status'],'unresolved-profile-label-consumer')
            self.assertEqual(u[f'7CC6A0:{s}:0']['speaker'],'profile-field-label')
            self.assertIsNone(u[f'7CC6A0:{s}:0']['origin_portrait'])

    def test_manager_sibling_person_and_school_meaning(self):
        a=next(a for a in self.assets if a['archive']=='7CC6A0');u={x['id']:x for x in a['units']}
        self.assertIn('형·오빠',u['7CC6A0:1:2']['translation'])
        self.assertIn('누나·언니',u['7CC6A0:3:2']['translation'])
        self.assertIn('학교나 직장',u['7CC6A0:0:2']['translation'])
        self.assertEqual(u['7CC6A0:75:0']['translation'],'유치원')
        self.assertEqual(u['7CC6A0:84:0']['translation'],'좋아하는 사람')
        self.assertEqual(u['7CC6A0:86:0']['translation'],'불편한 사람')

    def test_bass_victory_actor_routes_and_shadow(self):
        a=next(a for a in self.assets if a['archive']=='7CB850')
        names=['MegaMan','Roll','GutsMan','WindMan','SearchMan','FireMan','ThunderMan','ProtoMan','NumberMan','MetalMan','JunkMan','AquaMan','WoodMan','StarMan','ShadowMan','KnightMan','NapalmMan','IceMan','ElecMan','PlantMan','Bass']
        for u in a['units']:
            s=int(u['id'].split(':')[1])
            self.assertEqual(u['speaker'],'Bass' if s<2 else names[s-2])
            self.assertEqual(u['portrait_visibility'],'visible')
        u={x['id']:x for x in a['units']}
        self.assertIn('멸망하지 않는다',u['7CB850:1:0']['translation'])
        self.assertIn('그림자',u['7CB850:22:0']['translation'])
        self.assertIn('오리지널',u['7CB850:22:1']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('jumpIfUnused1 = continue',src)
        self.assertIn('jumpIfUnused2 = continue',src)

    def test_bass_victory_number_operator_missing_factor(self):
        a=next(a for a in self.assets if a['archive']=='7CB850');u={x['id']:x for x in a['units']}
        self.assertIn('0、00001퍼센트',u['7CB850:10:2']['translation'])
        self.assertIn('제 데이터만',u['7CB850:10:5']['translation'])
        self.assertIn('당신의 존재',u['7CB850:10:6']['translation'])
        self.assertIn('계산으로는 산출할 수 없는',u['7CB850:10:8']['translation'])
        self.assertIn('산수 공부',u['7CB850:10:10']['translation'])
        self.assertIn('1명의 힘',u['7CB850:2:2']['translation'])
        self.assertIn('1부터',u['7CB850:11:4']['translation'])
        self.assertIn('1그루',u['7CB850:14:4']['translation'])
        self.assertIn('1개',u['7CB850:20:2']['translation'])

    def test_bass_victory_gratitude_hypothetical_and_wishes(self):
        a=next(a for a in self.assets if a['archive']=='7CB850');u={x['id']:x for x in a['units']}
        self.assertIn('네 마음',u['7CB850:3:6']['translation'])
        self.assertIn('네 나비여서',u['7CB850:12:1']['translation'])
        self.assertIn('예뻐해',u['7CB850:13:4']['translation'])
        self.assertIn('홍염',u['7CB850:15:0']['translation'])
        self.assertIn('행운의 별',u['7CB850:15:3']['translation'])
        self.assertIn('부활할지도',u['7CB850:5:2']['translation'])
        self.assertIn('되살아난다고 해도',u['7CB850:6:4']['translation'])
        self.assertIn('자신을 달랠',u['7CB850:18:7']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertNotIn('playerResetScene',src)
        self.assertNotIn('select',src)

    def test_bass_two_navi_routes_and_special_jumps(self):
        a=next(a for a in self.assets if a['archive']=='7CAF40')
        names=['MegaMan','Roll','GutsMan','WindMan','SearchMan','FireMan','ThunderMan','ProtoMan','NumberMan','MetalMan','JunkMan','AquaMan','WoodMan','StarMan','ShadowMan','KnightMan','NapalmMan','IceMan','ElecMan','PlantMan','Bass']
        for u in a['units']:
            s=int(u['id'].split(':')[1])
            self.assertEqual(u['speaker'],'Bass' if s==44 else names[s-1 if s<22 else s-23])
            self.assertEqual(u['portrait_visibility'],'visible')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('jumpIfUnused1 = continue'),2)
        self.assertEqual(src.count('jumpIfUnused2 = continue'),2)
        for s in (27,28):
            segment=src.split(f'script {s} mmbn45')[1].split(f'script {s+1} mmbn45')[0]
            self.assertIn('target = 22',segment)
            self.assertNotIn('target = 44',segment)

    def test_bass_probability_prayer_and_metaphors(self):
        a=next(a for a in self.assets if a['archive']=='7CAF40');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7CAF40:31:2']['translation'],'......\n0、00001퍼센트!')
        self.assertIn('자기장',u['7CAF40:7:0']['translation'])
        self.assertIn('원자력 발전소',u['7CAF40:19:1']['translation'])
        self.assertIn('나무 하치만 대보살',u['7CAF40:37:1']['translation'])
        self.assertIn('그림자',u['7CAF40:43:0']['translation'])
        self.assertIn('피로',u['7CAF40:44:0']['translation'])

    def test_bass_unshown_voices_remain_pending(self):
        a=next(a for a in self.assets if a['archive']=='7CAF40');ids={u['id'] for u in a['units']}
        ledger=json.loads((ROOT/'analysis/translation_first_v1/worklist.json').read_text(encoding='utf8'))
        for key in ('7CAF40:0:0','7CAF40:0:1','7CAF40:0:2','7CAF40:22:0'):
            self.assertNotIn(key,ids)
            u=next(x for x in ledger['units'] if x['id']==key)
            self.assertEqual(u['draft_stage'],'authored_draft_not_in_rom')
            self.assertEqual(u['authored_translation'],final047.DRAFT['7CAF40'][key.split(':',1)[1]])
            draft=next(x for x in final047.create('7CAF40')['units'] if x['id']==key)
            self.assertEqual(draft['speaker'],'speaker-unestablished')
            self.assertEqual(draft['state'],'needs_review');self.assertIsNone(draft['origin_portrait'])

    def test_aftermath_hidden_warning_and_sound(self):
        a=next(a for a in self.assets if a['archive']=='7CA474');u={x['id']:x for x in a['units']}
        for i in (2,3):
            self.assertEqual(u[f'7CA474:6:{i}']['speaker'],'system-sfx')
            self.assertEqual(u[f'7CA474:6:{i}']['portrait_visibility'],'hidden')
            self.assertEqual(u[f'7CA474:6:{i}']['origin_portrait'],'SearchMan')
        self.assertEqual(u['7CA474:6:4']['speaker'],'SearchMan')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('track = 284','soundDisableTextSFX','soundEnableTextSFX','jumpIfUnused1 = continue','jumpIfUnused2 = continue'):
            self.assertIn(token,src)

    def test_aftermath_warning_and_reaction_not_actions(self):
        a=next(a for a in self.assets if a['archive']=='7CA474');u={x['id']:x for x in a['units']}
        self.assertIn('사라지지',u['7CA474:0:1']['translation'])
        self.assertIn('공포',u['7CA474:1:1']['translation'])
        self.assertIn('삭제',u['7CA474:1:2']['translation'])
        self.assertIn('플러그아웃',u['7CA474:10:3']['translation'])
        self.assertIn('함께라면',u['7CA474:12:2']['translation'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertNotIn('playerResetScene',src)
        self.assertNotIn('select',src)

    def test_aftermath_material_and_heart_freezing(self):
        a=next(a for a in self.assets if a['archive']=='7CA474');u={x['id']:x for x in a['units']}
        self.assertIn('물질',u['7CA474:19:1']['translation'])
        self.assertIn('마음을 얼리는',u['7CA474:19:2']['translation'])
        self.assertIn('레이저맨의 것이 아냐',u['7CA474:7:3']['translation'])
        self.assertIn('바닥났겠지',u['7CA474:20:1']['translation'])
        self.assertIn('추한 꽃',u['7CA474:21:3']['translation'])

    def test_laser_mid_script_scream_actor(self):
        a=next(a for a in self.assets if a['archive']=='7C9C44');u={x['id']:x for x in a['units']}
        self.assertEqual([u[f'7C9C44:10:{i}']['speaker'] for i in range(4)],['NumberMan','NumberMan','LaserMan','NumberMan'])
        self.assertIn('살려 주세요',u['7C9C44:10:3']['translation'])
        self.assertTrue(all(x['portrait_visibility']=='visible' for x in a['units']))

    def test_laser_memory_empathy_and_battle_life(self):
        a=next(a for a in self.assets if a['archive']=='7C9C44');u={x['id']:x for x in a['units']}
        self.assertIn('기억나지',u['7C9C44:1:4']['translation'])
        self.assertIn('본래의',u['7C9C44:1:7']['translation'])
        self.assertIn('불안하지',u['7C9C44:12:1']['translation'])
        self.assertIn('살아 있다는 실감',u['7C9C44:18:2']['translation'])
        self.assertIn('S랭크',u['7C9C44:9:1']['translation'])
        self.assertIn('100만 볼트',u['7C9C44:20:3']['translation'])

    def test_laser_unknown_intro_remains_in_denominator(self):
        a=next(a for a in self.assets if a['archive']=='7C9C44')
        self.assertFalse(any(x['id'].startswith('7C9C44:0:') for x in a['units']))
        ledger=json.loads((ROOT/'analysis/translation_first_v1/worklist.json').read_text(encoding='utf8'))
        for key in ('7C9C44:0:0','7C9C44:0:1'):
            u=next(x for x in ledger['units'] if x['id']==key)
            self.assertEqual(u['draft_stage'],'authored_draft_not_in_rom')
            self.assertEqual(u['authored_translation'],final047.DRAFT['7C9C44'][key.split(':',1)[1]])
            draft=next(x for x in final047.create('7C9C44')['units'] if x['id']==key)
            self.assertEqual(draft['speaker'],'speaker-unestablished')
            self.assertEqual(draft['state'],'needs_review');self.assertIsNone(draft['origin_portrait'])
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('target = 2',src)
        self.assertIn('jumpIfUnused1 = continue',src)
        self.assertIn('jumpIfUnused2 = continue',src)

    def test_victory_actor_routes(self):
        a=next(a for a in self.assets if a['archive']=='7C90E0')
        names=['ShadeMan','MegaMan','Roll','GutsMan','WindMan','SearchMan','FireMan','ThunderMan','ProtoMan','NumberMan','MetalMan','JunkMan','AquaMan','WoodMan','StarMan','ShadowMan','KnightMan','NapalmMan','IceMan','ElecMan','PlantMan','Bass']
        for u in a['units']:
            self.assertEqual(u['speaker'],names[int(u['id'].split(':')[1])])
            self.assertEqual(u['portrait_visibility'],'visible')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('jumpIfUnused1 = continue',src)
        self.assertIn('jumpIfUnused2 = continue',src)

    def test_victory_return_registration_is_spoken(self):
        a=next(a for a in self.assets if a['archive']=='7C90E0')
        for s in range(1,22):
            text=' '.join(u['translation'] for u in a['units'] if int(u['id'].split(':')[1])==s)
            self.assertIn('인터넷12',text)
            self.assertIn('오피셜',text)
            self.assertIn('토너먼트',text)
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertNotIn('flagSet',src)
        self.assertNotIn('playerResetScene',src)

    def test_victory_threat_report_and_gratitude(self):
        a=next(a for a in self.assets if a['archive']=='7C90E0');u={x['id']:x for x in a['units']}
        self.assertIn('무한',u['7C90E0:0:1']['translation'])
        self.assertIn('생각하지 마라',u['7C90E0:0:0']['translation'])
        self.assertIn('보고',u['7C90E0:16:2']['translation'])
        self.assertIn('등록',u['7C90E0:16:3']['translation'])
        self.assertIn('네 덕분',u['7C90E0:11:1']['translation'])
        self.assertIn('겁을',u['7C90E0:17:2']['translation'])

    def test_victory_prayer_typo_and_numeral_protection(self):
        a=next(a for a in self.assets if a['archive']=='7C90E0');u={x['id']:x for x in a['units']}
        self.assertIn('나무',u['7C90E0:15:2']['translation'])
        self.assertIn('オフィシャルトーメント',u['7C90E0:15:4']['source'])
        self.assertIn('오피셜 토너먼트',u['7C90E0:15:4']['translation'])
        self.assertIn('2번 다시',u['7C90E0:20:2']['translation'])
        self.assertIn('건곤일척',u['7C90E0:10:0']['translation'])

    def test_coffin_navi_routes_and_shared_jumps(self):
        a=next(a for a in self.assets if a['archive']=='7C8570')
        names=['MegaMan','Roll','GutsMan','WindMan','SearchMan','FireMan','ThunderMan','ProtoMan','NumberMan','MetalMan','JunkMan','AquaMan','WoodMan','StarMan','ShadowMan','KnightMan','NapalmMan','IceMan','ElecMan','PlantMan','Bass']
        for u in a['units']:
            s=int(u['id'].split(':')[1])
            if s<21:self.assertEqual(u['speaker'],names[s])
            elif 24<=s<=44:self.assertEqual(u['speaker'],names[s-24])
            else:self.assertEqual(u['speaker'],'ShadeMan')
        src=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('target = 21'),21)
        self.assertEqual(src.count('target = 45'),21)
        self.assertEqual(src.count('jumpIfUnused1 = continue'),2)
        self.assertEqual(src.count('jumpIfUnused2 = continue'),2)
        self.assertIn('target = 24',src)

    def test_coffin_hidden_voice_not_previous_navi(self):
        a=next(a for a in self.assets if a['archive']=='7C8570');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7C8570:21:0']['speaker'],'ShadeMan')
        self.assertIsNone(u['7C8570:21:0']['origin_portrait'])
        self.assertEqual(u['7C8570:21:0']['portrait_visibility'],'hidden')
        self.assertIn('잠을',u['7C8570:21:0']['translation'])
        self.assertEqual(u['7C8570:22:0']['origin_portrait'],'ShadeMan')
        self.assertIn('inferred',a['semantic_review'][0])

    def test_coffin_numerals_and_element_boasts(self):
        a=next(a for a in self.assets if a['archive']=='7C8570');u={x['id']:x for x in a['units']}
        self.assertIn('100만 년',u['7C8570:40:0']['translation'])
        self.assertIn('100만 볼트',u['7C8570:42:0']['translation'])
        self.assertIn('화장',u['7C8570:16:2']['translation'])
        self.assertIn('자기장',u['7C8570:18:1']['translation'])
        self.assertIn('관째로',u['7C8570:17:1']['translation'])
        self.assertIn('꽃잎',u['7C8570:43:0']['translation'])

    def test_coffin_spell_rhetoric_and_speaker_gender(self):
        a=next(a for a in self.assets if a['archive']=='7C8570');u={x['id']:x for x in a['units']}
        self.assertIn('여자 체면',u['7C8570:25:1']['translation'])
        self.assertIn('심두멸각',u['7C8570:33:1']['translation'])
        self.assertIn('젠!!',u['7C8570:38:0']['translation'])
        self.assertIn('철구',u['7C8570:39:0']['translation'])
        self.assertEqual(u['7C8570:31:0']['translation'],'베겠다!!')
        self.assertIn('어둠의 심연',u['7C8570:45:0']['translation'])

    def test_duplicate_id_rejected(self):
        a=self.altered();a['units'].append(copy.deepcopy(a['units'][0]))
        with self.assertRaisesRegex(ValueError,'immutable'):self.validate(a)

    def test_source_mutation_rejected(self):
        a=self.altered();a['units'][0]['source']+='!'
        with self.assertRaisesRegex(ValueError,'immutable'):self.validate(a)

    def test_wrong_rom_revision_rejected(self):
        a=self.altered();a['source_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'revision'):self.validate(a)

    def test_wrong_payload_rejected(self):
        a=self.altered();a['source_archive_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'payload'):self.validate(a)

    def test_japanese_residual_rejected(self):
        a=self.altered();a['units'][0]['translation']+='あ'
        with self.assertRaisesRegex(ValueError,'untranslated'):self.validate(a)

    def test_unapproved_state_rejected(self):
        a=self.altered();a['units'][0]['state']='approved'
        with self.assertRaisesRegex(ValueError,'state'):self.validate(a)

    def test_newline_mutation_rejected(self):
        a=self.altered();a['units'][0]['translation']+='\n'
        with self.assertRaisesRegex(ValueError,'topology'):self.validate(a)

    def test_numeric_mutation_rejected(self):
        a=self.altered();a['units'][0]['translation']+='123'
        with self.assertRaisesRegex(ValueError,'numbers'):self.validate(a)

    def test_font_missing_rejected(self):
        with self.assertRaisesRegex(ValueError,'glyph'):self.validate(self.assets[0],set())

    def test_release_claim_rejected(self):
        a=self.altered();a['review']['release_eligible']=True
        with self.assertRaisesRegex(ValueError,'policy'):self.validate(a)

    def test_ledger_denominator(self):
        result=json.loads((ROOT/'analysis/translation_first_v1/coverage.json').read_text(encoding='utf8'))
        self.assertEqual(result['new_authored_drafts'],27450)
        self.assertEqual(result['japanese_still_without_selected_draft'],2)
        self.assertEqual(result['rom_unselected_japanese'],27452)
        self.assertFalse(result['draft_complete']);self.assertFalse(result['rom_integration_started'])

    def test_baseline_rom_unchanged(self):
        self.assertEqual(sha((ROOT/self.plan['baseline_rom']['path']).read_bytes()),self.plan['baseline_rom']['sha256'])
        self.assertEqual(sha(self.rom),self.assets[0]['source_sha256'])

    def test_negative_temperature_sign_rejected(self):
        a=copy.deepcopy(self.assets[3]);u=next(x for x in a['units'] if x['id']=='6DD9AC:13:6')
        u['translation']=u['translation'].replace('-40','40')
        with self.assertRaisesRegex(ValueError,'numbers'):self.validate(a)

    def test_mission_destinations_and_times(self):
        units={u['id']:u for u in self.assets[2]['units']}
        self.assertIn('인터넷4',units['6DE3E0:40:2']['translation'])
        self.assertIn('30분',units['6DE3E0:40:3']['translation'])
        self.assertIn('20분',units['6DE3E0:56:3']['translation'])
        self.assertIn('40분',units['6DE3E0:57:5']['translation'])

    def test_mission_optional_vs_mandatory(self):
        units={u['id']:u for u in self.assets[2]['units']}
        self.assertIn('삭제해도 좋네',units['6DE3E0:36:4']['translation'])
        self.assertNotIn('삭제해도',units['6DE3E0:40:3']['translation'])
        for s in range(60,65):
            self.assertTrue(any('체포하거나 삭제해' in u['translation'] for u in units.values() if u['id'].startswith(f'6DE3E0:{s}:')))

    def test_mission_criminal_appearance_distinctions(self):
        units={u['id']:u for u in self.assets[2]['units']}
        self.assertIn('검은 여성형',units['6DE3E0:36:5']['translation'])
        self.assertIn('여자아이형',units['6DE3E0:47:5']['translation'])
        self.assertIn('남자',units['6DE3E0:47:6']['translation'])
        self.assertIn('빨간',units['6DE3E0:59:8']['translation'])
        self.assertIn('초록색',units['6DE3E0:60:5']['translation'])

    def test_reward_portrait_context(self):
        units={u['id']:u for u in self.assets[2]['units']}
        self.assertEqual(units['6DE3E0:28:0']['speaker'],'SciLabMan')
        self.assertEqual(units['6DE3E0:28:3']['speaker'],'system-reward')
        self.assertEqual(units['6DE3E0:30:1']['speaker'],'system-reward')

    def test_mail_variable_suffixes(self):
        units={u['id']:u for u in self.assets[3]['units']}
        self.assertEqual(units['6DD9AC:11:6']['translation'],'님!')
        self.assertEqual(units['6DD9AC:12:2']['translation'],'님께서')
        self.assertEqual(units['6DD9AC:13:3']['translation'],'님에 의해\n쓰러졌습니다')
        self.assertEqual(units['6DD9AC:14:0']['translation'],'님')

    def test_mail_uncertain_revival_retained(self):
        units={u['id']:u for u in self.assets[3]['units']}
        self.assertIn('되살아날지도',units['6DD9AC:3:3']['translation'])
        self.assertIn('그 에어리어',units['6DD9AC:3:6']['translation'])

    def test_global_draft_identity_unique(self):
        ids=[u['id'] for a in self.assets for u in a['units']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),27450)

    def test_fortune_numeric_range_delimiter_rejected(self):
        a=copy.deepcopy(self.assets[4]);u=next(x for x in a['units'] if x['id']=='6A3DD0:20:0')
        u['translation']=u['translation'].replace('1~4','1/4')
        with self.assertRaisesRegex(ValueError,'ranges'):self.validate(a)

    def test_fortune_rank_and_hint_groups(self):
        units={u['id']:u for u in self.assets[4]['units']}
        for script,rank in ((5,4),(8,1),(9,5),(12,2),(13,6),(16,3)):
            self.assertIn(f'{rank}등성',units[f'6A3DD0:{script}:0']['translation'])
        for script,numbers in ((20,'1~4'),(21,'5~8'),(22,'9~12')):
            self.assertIn(numbers,units[f'6A3DD0:{script}:0']['translation'])

    def test_fortune_timed_dot_literals_remain_separate(self):
        units={u['id']:u for u in self.assets[4]['units']}
        for script,indices in ((0,(3,4,5,9,10)),(1,(3,4,5,9,10)),(7,(3,4,5))):
            for i in indices:self.assertEqual(units[f'6A3DD0:{script}:{i}']['translation'],'.')

    def test_fortune_rewards_and_name_boundary(self):
        units={u['id']:u for u in self.assets[4]['units']}
        self.assertEqual(units['6A3DD0:61:0']['translation'],'해냈어!\n')
        self.assertEqual(units['6A3DD0:61:1']['translation'],',\n멋진 오퍼레이팅이야!')
        self.assertIn('HP 메모리',units['6A3DD0:61:4']['translation'])
        self.assertIn('제니',units['6A3DD0:62:4']['translation'])
        self.assertEqual(units['6A3DD0:63:4']['translation'],'버그 조각')

    def test_bbs_instruction_and_restoration(self):
        units={u['id']:u for u in self.assets[5]['units']}
        self.assertIn('셀렉트 버튼',units['7011F0:27:3']['translation'])
        self.assertIn('순서대로',units['7011F0:27:4']['translation'])
        self.assertIn('3개',units['7011F0:27:4']['translation'])
        self.assertIn('사용 횟수를',units['7011F0:24:3']['translation'])
        self.assertIn('회복',units['7011F0:24:3']['translation'])

    def test_bbs_no_invented_author(self):
        units={u['id']:u for u in self.assets[5]['units']}
        self.assertIn('author not inferred',units['7011F0:17:0']['speaker'])
        self.assertEqual(units['7011F0:20:0']['speaker'],'Tesshin-self-identified')
        self.assertEqual(units['7011F0:27:0']['speaker'],'Koetsu-self-identified')

    def test_bbs_placeholders_remain_review_not_excluded(self):
        data=json.loads((ROOT/'analysis/translation_first_v1/worklist.json').read_text(encoding='utf8'))
        rows=[u for u in data['units'] if u['archive']=='7011F0' and u['source'].startswith('BBS01 ID')]
        self.assertTrue(rows)
        self.assertTrue(all(u['draft_stage']=='non_japanese_review_not_excluded' and u['authored_translation'] is None for u in rows))

    def test_battle_equipment_assignment_counts(self):
        units={u['id']:u for u in self.assets[6]['units']}
        self.assertIn('3종류',units['7000AC:1:1']['translation'])
        self.assertIn('2종류',units['7000AC:1:2']['translation'])
        self.assertIn('R 버튼',units['7000AC:1:3']['translation'])
        self.assertIn('버스터',units['7000AC:1:3']['translation'])

    def test_battle_counter_and_escape_conditions(self):
        units={u['id']:u for u in self.assets[6]['units']}
        self.assertIn('막 공격하려는',units['7000AC:4:3']['translation'])
        self.assertIn('칩 공격',units['7000AC:4:4']['translation'])
        self.assertIn('L 버튼',units['7000AC:7:0']['translation'])
        self.assertIn('파란색까지',units['7000AC:7:1']['translation'])
        self.assertIn('없어',units['7000AC:7:2']['translation'])

    def test_battle_gauge_spend_vs_gain(self):
        units={u['id']:u for u in self.assets[6]['units']}
        self.assertIn('소모',units['7000AC:2:2']['translation'])
        self.assertIn('늘어나',units['7000AC:20:1']['translation'])
        self.assertIn('줄지 않는',units['7000AC:34:1']['translation'])

    def test_battle_gate_folder_and_recovery_exception(self):
        units={u['id']:u for u in self.assets[6]['units']}
        self.assertIn('30장',units['7000AC:8:3']['translation'])
        self.assertIn('플러그아웃하지 않으면',units['7000AC:8:7']['translation'])
        self.assertIn('회복해 주는 곳',units['7000AC:9:1']['translation'])
        self.assertIn('3장',units['7000AC:19:1']['translation'])
        self.assertIn('셀렉트 버튼',units['7000AC:19:2']['translation'])

    def test_battle_nested_event_quote(self):
        units={u['id']:u for u in self.assets[6]['units']}
        self.assertTrue(units['7000AC:9:4']['translation'].startswith('「'))
        self.assertTrue(units['7000AC:9:9']['translation'].endswith('」'))
        self.assertIn('전기레인지',units['7000AC:9:5']['translation'])
        self.assertIn('필요 없습니다',units['7000AC:9:7']['translation'])
        self.assertIn('아무 관계도 없습니다',units['7000AC:9:8']['translation'])

    def test_plaza_native_portraits_distinguished(self):
        units={u['id']:u for u in self.assets[7]['units']}
        for s,p in ((0,'PurpleNavi'),(10,'OfficialNavi'),(20,'HeelNaviBlack'),(40,'NaviGirlOrange'),(50,'MrProgGreen'),(70,'NormalNaviBrown'),(110,'HeelNaviPurple')):
            self.assertEqual(units[f'7A32A8:{s}:0']['speaker'],p)

    def test_plaza_uncertain_romance_and_punctuation(self):
        units={u['id']:u for u in self.assets[7]['units']}
        self.assertIn('안 되는 건가',units['7A32A8:51:0']['translation'])
        self.assertIn('허락되지 않는다면',units['7A32A8:60:0']['translation'])
        for i in (2,3,4):self.assertEqual(units[f'7A32A8:20:{i}']['translation'],'.')

    def test_plaza_verse_numbers_and_weekday(self):
        units={u['id']:u for u in self.assets[7]['units']}
        for s in (70,71):self.assertEqual(units[f'7A32A8:{s}:6']['translation'].count('\n'),2)
        self.assertIn('1, 2, 3',units['7A32A8:32:2']['translation'])
        self.assertIn('월요일',units['7A32A8:80:0']['translation'])


    def test_mystery_search_tense_and_timed_dots(self):
        units={u['id']:u for u in self.assets[8]['units']}
        for s in (0,6,10,16,20,26,30,36,40,46,56,66,70,76):
            self.assertTrue(units[f'778CC0:{s}:0']['translation'].endswith('조사했다.'))
            for i in (1,2):self.assertEqual(units[f'778CC0:{s}:{i}']['translation'],'.')

    def test_mystery_trap_and_capacity_distinctions(self):
        units={u['id']:u for u in self.assets[8]['units']}
        for s in (56,66):self.assertIn('삭제되었다',units[f'778CC0:{s}:5']['translation'])
        for s in (59,69):self.assertIn('바이러스였다',units[f'778CC0:{s}:0']['translation'])
        for s,i in ((18,1),(48,0)):self.assertIn('더 못 가진다',units[f'778CC0:{s}:{i}']['translation'])

    def test_mystery_reward_categories(self):
        units={u['id']:u for u in self.assets[8]['units']}
        for key,label in (('9:0','배틀 칩'),('19:0','서브 칩'),('29:1','제니'),('49:0','버그 조각'),('79:0','강화 프로그램')):
            self.assertIn(label,units['778CC0:'+key]['translation'])
        self.assertIn('효과 발휘',units['778CC0:3:1']['translation'])
        self.assertIn('필요',units['778CC0:7:1']['translation'])

    def test_new_source_only_quotes_remain_unselected(self):
        data=json.loads((ROOT/'analysis/translation_first_v1/worklist.json').read_text(encoding='utf8'))
        units={u['id']:u for u in data['units']}
        for key in ('778CC0:18:0','7AE0A0:3:3','7AE0A0:3:19','7AE0A0:3:21','7AE0A0:5:4'):
            self.assertEqual(units[key]['draft_stage'],'non_japanese_review_not_excluded')
            self.assertIsNone(units[key]['authored_translation'])

    def test_prelim_aptitude_and_key_route(self):
        units={u['id']:u for u in self.assets[9]['units']}
        self.assertIn('내비 6체 삭제',units['7AE0A0:1:2']['translation'])
        self.assertIn('2개의 열쇠',units['7AE0A0:3:5']['translation'])
        self.assertIn('인터넷10, 11',units['7AE0A0:3:17']['translation'])
        self.assertIn('인터넷12',units['7AE0A0:3:18']['translation'])
        self.assertIn('그대로 가지고',units['7AE0A0:5:5']['translation'])

    def test_prelim_portrait_actor_vs_hidden_choice_reward(self):
        units={u['id']:u for u in self.assets[9]['units']}
        for key,speaker in (('0:0','NormalNaviBrown'),('0:3','player-choice'),('5:7','system-reward'),('50:0','ThunderMan'),('54:0','ThunderMan'),('220:0','NormalNaviPink'),('221:0','NormalNaviPink')):
            self.assertEqual(units['7AE0A0:'+key]['speaker'],speaker)
        self.assertEqual(units['7AE0A0:5:7']['portrait_visibility'],'hidden')

    def test_prelim_challenge_outcomes_separate(self):
        units={u['id']:u for u in self.assets[9]['units']}
        self.assertIn('쓰러뜨리다니',units['7AE0A0:51:0']['translation'])
        self.assertIn('잘못 생각',units['7AE0A0:52:0']['translation'])
        self.assertIn('기묘',units['7AE0A0:54:1']['translation'])
        self.assertIn('품절',units['7AE0A0:222:0']['translation'])

    def test_prelim_choice_spacing_and_cancel(self):
        units={u['id']:u for u in self.assets[9]['units']}
        self.assertEqual(units['7AE0A0:0:3']['translation'],'예  ')
        self.assertEqual(units['7AE0A0:0:4']['translation'],'아니요')
        self.assertEqual(units['7AE0A0:50:3']['translation'],'그래  ')
        self.assertEqual(units['7AE0A0:50:4']['translation'],'그만둘래')


    def test_blackworks_family_roles_and_locations(self):
        younger={u['id']:u for u in self.assets[10]['units']}
        elder={u['id']:u for u in self.assets[11]['units']}
        self.assertIn('인터넷11',younger['7AF6D0:1:4']['translation'])
        self.assertIn('우리 형',younger['7AF6D0:1:4']['translation'])
        self.assertIn('보스',younger['7AF6D0:1:5']['translation'])
        self.assertIn('인터넷10',elder['7B09F4:4:4']['translation'])
        self.assertIn('내 동생',elder['7B09F4:4:4']['translation'])
        self.assertIn('정신을 차리게',younger['7AF6D0:3:1']['translation'])
        self.assertIn('막아 줘',elder['7B09F4:4:5']['translation'])

    def test_blackworks_second_defeat_and_reward_context(self):
        younger={u['id']:u for u in self.assets[10]['units']}
        elder={u['id']:u for u in self.assets[11]['units']}
        self.assertIn('형도 쓰러뜨렸다고',younger['7AF6D0:2:1']['translation'])
        self.assertIn('내 동생도',elder['7B09F4:5:1']['translation'])
        for key,i,a in (('7AF6D0:2',4,younger),('7B09F4:5',5,elder)):
            self.assertEqual(a[f'{key}:{i}']['speaker'],'system-reward')
            self.assertEqual(a[f'{key}:{i}']['translation'],',\n「')
            self.assertEqual(a[f'{key}:{i+1}']['translation'],'」\n획득!!')
            self.assertEqual(a[f'{key}:{i+2}']['speaker'],'HeelNaviBlack')

    def test_blackworks_search_test_constraints(self):
        units={u['id']:u for u in self.assets[10]['units']}
        for s,i in ((70,7),(72,2)):self.assertIn('인터넷2',units[f'7AF6D0:{s}:{i}']['translation'])
        for s,i in ((70,8),(72,3)):
            self.assertIn('제한 시간',units[f'7AF6D0:{s}:{i}']['translation'])
            self.assertIn('모두 저격',units[f'7AF6D0:{s}:{i}']['translation'])
        for s,i in ((70,11),(72,6)):
            self.assertIn('한 번이라도 플러그아웃',units[f'7AF6D0:{s}:{i}']['translation'])
            self.assertIn('실패',units[f'7AF6D0:{s}:{i}']['translation'])
        self.assertIn('인터넷2로 돌아가라',units['7AF6D0:74:4']['translation'])

    def test_blackworks_native_navi_and_outcome_voices(self):
        for idx,prefix,scripts in ((10,'7AF6D0',((50,'WoodMan'),(54,'WoodMan'),(70,'SearchMan'))),(11,'7B09F4',((50,'SearchMan'),(53,'KnightMan'),(58,'SearchMan'),(59,'KnightMan'),(60,'IceMan')))):
            units={u['id']:u for u in self.assets[idx]['units']}
            for s,p in scripts:self.assertEqual(units[f'{prefix}:{s}:0']['speaker'],p)
        elder={u['id']:u for u in self.assets[11]['units']}
        self.assertIn('패배를 인정',elder['7B09F4:54:1']['translation'])
        self.assertIn('용기는 인정',elder['7B09F4:55:1']['translation'])
        self.assertIn('예상대로',elder['7B09F4:52:1']['translation'])

    def test_blackworks_iceman_conditional_passage(self):
        units={u['id']:u for u in self.assets[11]['units']}
        self.assertIn('만약',units['7B09F4:60:4']['translation'])
        self.assertIn('길을 열어',units['7B09F4:60:5']['translation'])
        self.assertIn('약속대로',units['7B09F4:61:1']['translation'])
        self.assertIn('지나가게 할 수 없어요',units['7B09F4:62:1']['translation'])

    def test_blackworks_shop_choice_visible_portrait_not_actor(self):
        units={u['id']:u for u in self.assets[11]['units']}
        for s,indices in ((223,(1,2)),(224,(3,4)),(225,(4,5))):
            self.assertEqual(units[f'7B09F4:{s}:0']['speaker'],'NormalNaviYellow')
            for i in indices:
                u=units[f'7B09F4:{s}:{i}']
                self.assertEqual(u['speaker'],'player-choice')
                self.assertEqual(u['origin_portrait'],'NormalNaviYellow')
                self.assertEqual(u['portrait_visibility'],'visible')
        self.assertEqual(units['7B09F4:221:0']['speaker'],'NormalNaviYellow')

    def test_blackworks_source_option_spaces_and_blank_row(self):
        for a in self.assets[10:]:
            for u in a['units']:
                if u['source'].endswith('  '):self.assertTrue(u['translation'].endswith('  '),u['id'])
        units={u['id']:u for u in self.assets[11]['units']}
        for key in ('223:0','224:2','225:3'):self.assertTrue(units['7B09F4:'+key]['translation'].endswith('\n'))

    def test_blackworks_hearsay_not_guaranteed_requirement(self):
        units={u['id']:u for u in self.assets[11]['units']}
        self.assertIn('들은 이야기',units['7B09F4:13:0']['translation'])
        self.assertTrue(units['7B09F4:13:1']['translation'].endswith('한대!'))
        self.assertIn('레이디스 데이',units['7B09F4:224:0']['translation'])
        self.assertNotIn('%',units['7B09F4:224:1']['translation'])


    def test_entry_free_vs_later_fee_and_insufficient_funds(self):
        units={u['id']:u for u in self.assets[12]['units']}
        self.assertIn('무료',units['7B1FF4:3:9']['translation'])
        self.assertIn('1000제니',units['7B1FF4:8:3']['translation'])
        self.assertIn('1000제니',units['7B1FF4:4:0']['translation'])
        self.assertIn('돈이 부족',units['7B1FF4:6:0']['translation'])
        self.assertNotIn('1000',units['7B1FF4:5:0']['translation'])

    def test_entry_admin_mixup_and_coffin_hearsay(self):
        units={u['id']:u for u in self.assets[12]['units']}
        self.assertIn('언더인터넷4',units['7B1FF4:0:10']['translation'])
        self.assertIn('관...',units['7B1FF4:0:18']['translation'])
        self.assertIn('하더군요',units['7B1FF4:0:18']['translation'])
        self.assertIn('저희 실수',units['7B1FF4:3:5']['translation'])
        self.assertIn('초S급',units['7B1FF4:3:6']['translation'])
        self.assertIn('셰이드맨',units['7B1FF4:3:6']['translation'])

    def test_entry_weekday_and_clock(self):
        units={u['id']:u for u in self.assets[12]['units']}
        self.assertIn('주말에는',units['7B1FF4:9:1']['translation'])
        self.assertIn('월요일부터 금요일',units['7B1FF4:9:2']['translation'])
        for phrase in ('평일','아침6시','밤12시'):self.assertIn(phrase,units['7B1FF4:90:0']['translation'])

    def test_entry_radio_sound_not_player_choice(self):
        units={u['id']:u for u in self.assets[12]['units']}
        self.assertEqual(units['7B1FF4:0:3']['speaker'],'system-communication-sfx')
        self.assertEqual(units['7B1FF4:0:3']['portrait_visibility'],'hidden')
        self.assertEqual(units['7B1FF4:3:11']['speaker'],'player-choice')
        self.assertEqual(units['7B1FF4:3:13']['speaker'],'OfficialNavi')

    def test_entry_gold_count_recovery_and_uncertain_darkloid(self):
        units={u['id']:u for u in self.assets[12]['units']}
        self.assertIn('사용 횟수',units['7B1FF4:70:2']['translation'])
        self.assertIn('회복',units['7B1FF4:70:3']['translation'])
        self.assertIn('어렵군',units['7B1FF4:81:0']['translation'])
        self.assertIn('있다고 하는',units['7B1FF4:81:1']['translation'])
        for i in (1,2,3):self.assertEqual(units[f'7B1FF4:80:{i}']['translation'],'.')

    def test_entry_native_self_navi_voices_and_refusal(self):
        units={u['id']:u for u in self.assets[12]['units']}
        for s,p in ((60,'NapalmMan'),(68,'NapalmMan'),(63,'ProtoMan'),(69,'ProtoMan')):
            self.assertEqual(units[f'7B1FF4:{s}:0']['speaker'],p)
        self.assertIn('브루스',units['7B1FF4:69:2']['translation'])
        self.assertIn('공격 범위',units['7B1FF4:63:3']['translation'])
        self.assertEqual(units['7B1FF4:60:3']['translation'],'그만둘래')

    def test_generic_feigned_acquaintance_and_hyperbole(self):
        units={u['id']:u for u in self.assets[13]['units']}
        self.assertIn('나야, 나',units['7B0638:8:0']['translation'])
        self.assertIn('여름 방학',units['7B0638:8:2']['translation'])
        self.assertEqual(units['7B0638:8:5']['translation'],'오해예요!')
        self.assertIn('100만 번',units['7B0638:7:1']['translation'])
        self.assertIn('나야 나',units['7B0638:9:0']['translation'])
        self.assertIn('살법',units['7B0638:10:0']['translation'])

    def test_new_entry_generic_choice_trailing_spaces(self):
        for asset in self.assets[12:]:
            for u in asset['units']:
                if u['source'].endswith('  '):
                    self.assertTrue(u['translation'].endswith('  '),u['id'])
                    self.assertEqual(u['speaker'],'ui-label' if u['id'] in batch500ah.LABELS or u['id'] in batch500ai.LABELS or u['id'] in batch500ap.LABELS or u['id'] in batch500at.LABELS else 'speaker-unestablished' if asset['archive']=='700F6C' else 'system-label' if asset['archive'] in ('6E1068','6E12DC') and u['id']==asset['archive']+':2:0' else 'credits-label' if asset['archive']=='7CE5C8' else 'equipment-label' if (asset['archive'] in batch500.ACTORS or asset['archive'] in batch500b.ACTORS) and u['id']==asset['archive']+':2:0' else 'player-choice')


    def test_under_fee_is_not_official_fee(self):
        units={u['id']:u for u in self.assets[18]['units']}
        for key in ('0:3','2:2','3:0','4:2'):self.assertIn('2000제니',units['7B4A6C:'+key]['translation'])
        self.assertIn('돈이 부족',units['7B4A6C:4:0']['translation'])
        self.assertFalse(any('무료' in u['translation'] for u in units.values()))

    def test_under_weekday_time_and_sleep(self):
        units={u['id']:u for u in self.assets[18]['units']}
        self.assertIn('주말에는',units['7B4A6C:6:1']['translation'])
        self.assertIn('월요일부터 금요일',units['7B4A6C:6:2']['translation'])
        for p in ('평일','아침6시','밤12시'):self.assertIn(p,units['7B4A6C:110:0']['translation'])
        self.assertIn('드르렁',units['7B4A6C:111:0']['translation'])
        self.assertEqual(units['7B4A6C:111:0']['speaker'],'MrProgGreen')

    def test_under_visible_shop_choices_and_inherited_actor(self):
        units={u['id']:u for u in self.assets[15]['units']}
        self.assertEqual(units['7B3490:221:0']['speaker'],'PurpleNavi')
        for s,indices in ((223,(2,3)),(224,(4,5))):
            for i in indices:
                u=units[f'7B3490:{s}:{i}']
                self.assertEqual(u['speaker'],'player-choice')
                self.assertEqual(u['origin_portrait'],'PurpleNavi')
                self.assertEqual(u['portrait_visibility'],'visible')
        self.assertIn('서브 칩',units['7B3490:222:0']['translation'])
        self.assertIn('품절',units['7B3490:222:1']['translation'])

    def test_under_chip_count_recovery_not_hp(self):
        units={u['id']:u for u in self.assets[15]['units']}
        self.assertIn('사용 횟수',units['7B3490:70:2']['translation'])
        self.assertIn('회복',units['7B3490:70:3']['translation'])
        self.assertNotIn('HP',units['7B3490:70:3']['translation'])
        self.assertIn('지옥의 1번지',units['7B3490:0:0']['translation'])

    def test_under_compressed_battle_call_and_ironic_defeat(self):
        units={u['id']:u for u in self.assets[14]['units']}
        self.assertEqual(units['7B32B0:5:0']['translation'],'...배틀오페세인!')
        self.assertIn('승부에선 졌지만',units['7B32B0:6:0']['translation'])
        self.assertIn('싸움에선 이겼다',units['7B32B0:6:0']['translation'])
        self.assertEqual(units['7B32B0:1:2']['translation'],'인!!')

    def test_under_smell_proverb_and_surface_contrast(self):
        units={u['id']:u for u in self.assets[16]['units']}
        self.assertIn('일반 인터넷',units['7B39D0:0:0']['translation'])
        self.assertIn('언더의 규칙',units['7B39D0:1:0']['translation'])
        self.assertIn('냄새',units['7B39D0:4:0']['translation'])
        self.assertIn('군자는 위험한 곳',units['7B39D0:4:6']['translation'])
        self.assertEqual(units['7B39D0:4:0']['speaker'],'HeelNaviPurple')

    def test_under_actor_variety_forced_and_polite_encounters(self):
        units={u['id']:u for u in self.assets[17]['units']}
        self.assertEqual(units['7B469C:4:0']['speaker'],'NormalNaviYellow')
        self.assertIn('매료되어',units['7B469C:4:0']['translation'])
        self.assertEqual(units['7B469C:12:0']['speaker'],'HeelNaviPurple')
        self.assertFalse(any(u['speaker']=='player-choice' for u in units.values() if u['id'].startswith('7B469C:12:')))
        self.assertIn('블러디 파티',units['7B469C:16:0']['translation'])
        self.assertIn('마음에 드셨습니까',units['7B469C:18:0']['translation'])

    def test_under_choice_spaces_and_shop_final_newline(self):
        for a in self.assets[14:]:
            for u in a['units']:
                if u['source'].endswith('  '):self.assertTrue(u['translation'].endswith('  '),u['id'])
        units={u['id']:u for u in self.assets[15]['units']}
        for key in ('223:1','224:3'):self.assertTrue(units['7B3490:'+key]['translation'].endswith('\n'))


    def test_profile_variable_suffix_and_options(self):
        u={x['id']:x for x in next(a for a in self.assets if a['archive']=='7B67C8')['units']}
        self.assertEqual(u['7B67C8:16:1']['translation'],' 님의')
        self.assertEqual(u['7B67C8:16:4']['translation'],'예 ')
        for i in (4,5):
            self.assertEqual(u[f'7B67C8:16:{i}']['speaker'],'player-choice')
            self.assertEqual(u[f'7B67C8:16:{i}']['portrait_visibility'],'visible')

    def test_profile_unresolved_labels_not_runtime_claim(self):
        u={x['id']:x for x in next(a for a in self.assets if a['archive']=='7B67C8')['units']}
        for s in range(20,36):
            self.assertEqual(u[f'7B67C8:{s}:0']['consumer_status'],'unresolved-input-before-label')
            self.assertTrue(u[f'7B67C8:{s}:0']['translation'].endswith('\n입력 전'))
        self.assertIn('형·오빠',u['7B67C8:21:0']['translation'])
        self.assertIn('누나·언니',u['7B67C8:23:0']['translation'])
        self.assertIn('TV',u['7B67C8:32:0']['translation'])

    def test_venue_variable_rewards_and_unselected_quote(self):
        a=next(a for a in self.assets if a['archive']=='7B6F9C');u={x['id']:x for x in a['units']}
        self.assertNotIn('7B6F9C:14:1',u)
        self.assertEqual(u['7B6F9C:14:2']['translation'],'」,\n받을 수 있대!!')
        self.assertEqual(u['7B6F9C:20:1']['translation'],' 선수,\n또 도전해 줘!!')

    def test_venue_choice_visibility_and_inherited_merchant(self):
        u={x['id']:x for x in next(a for a in self.assets if a['archive']=='7B6F9C')['units']}
        for s,indices in ((223,(2,3)),(224,(4,5))):
            for i in indices:
                self.assertEqual(u[f'7B6F9C:{s}:{i}']['speaker'],'player-choice')
                self.assertEqual(u[f'7B6F9C:{s}:{i}']['portrait_visibility'],'visible')
        self.assertEqual(u['7B6F9C:221:0']['portrait_visibility'],'inherited-from-caller')

    def test_training_result_and_venue_native_gates(self):
        u={x['id']:x for x in next(a for a in self.assets if a['archive']=='7B6E20')['units']}
        self.assertIn('연습',u['7B6E20:3:0']['translation'])
        self.assertIn('오퍼레이션',u['7B6E20:2:0']['translation'])
        self.assertEqual(u['7B6E20:0:2']['translation'],'좋아!  ')
        s=(ROOT/next(a for a in self.assets if a['archive']=='7B6F9C')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('item = 19','navi = 1','lower = 3','shop = 8','shop = 18','flag = 1854'):
            self.assertIn(token,s)

    def test_appliance_factory_source_meanings(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        for key,text in (('7B76D4:0:1','메탈 패널'),('7B7AF0:0:0','열정'),('7B7EF8:0:0','자동차')):
            self.assertIn(text,u[key]['translation'])

    def test_appliance_trainee_vs_virus_owner(self):
        a=next(a for a in self.assets if a['archive']=='7B827C');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7B827C:0:0']['speaker'],'NormalNaviYellow')
        self.assertEqual(u['7B827C:4:0']['speaker'],'PurpleNavi')
        self.assertIn('위팔 두갈래근',u['7B827C:3:0']['translation'])
        for key in ('0:4','0:5','4:3','4:4'):
            self.assertEqual(u['7B827C:'+key]['speaker'],'player-choice')
            self.assertEqual(u['7B827C:'+key]['portrait_visibility'],'hidden')

    def test_appliance_toy_special_shop_and_visible_choices(self):
        a=next(a for a in self.assets if a['archive']=='7B84C8');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7B84C8:221:0']['origin_portrait'],'NormalNaviYellow')
        self.assertEqual(u['7B84C8:221:0']['portrait_visibility'],'inherited-from-caller')
        for s,indices in ((223,(1,2)),(224,(3,4)),(225,(4,5))):
            for i in indices:
                self.assertEqual(u[f'7B84C8:{s}:{i}']['speaker'],'player-choice')
                self.assertEqual(u[f'7B84C8:{s}:{i}']['portrait_visibility'],'visible')
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('variable = 7','value = 2','variable = 6','value = 1','jumpIfEqual = 225','shop = 3','shop = 13'):
            self.assertIn(t,source)

    def test_appliance_radio_broken_partner_and_name_boundary(self):
        a=next(a for a in self.assets if a['archive']=='7B8AB4');u={x['id']:x for x in a['units']}
        self.assertIn('튜너 담당',u['7B8AB4:0:1']['translation'])
        self.assertIn('고장',u['7B8AB4:0:1']['translation'])
        self.assertEqual(u['7B8AB4:20:1']['translation'],' 선수,\n또 도전해 줘!!')
        self.assertEqual(u['7B8AB4:1:0']['speaker'],'MrProgGreen')
        self.assertIn('재충전',u['7B8AB4:16:1']['translation'])

    def test_golf_administrators_distinct_jobs(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        for key,text in (('7B9104:0:0','잔디'),('7B9748:0:0','골프 코스'),('7B9C94:0:0','고객 정보')):
            self.assertIn(text,u[key]['translation'])
            self.assertEqual(u[key]['speaker'],'MrProgGreen')
        self.assertIn('흘려서는 안',u['7B9C94:0:1']['translation'])

    def test_golf_battle_portraits_choices_and_taunt(self):
        a=next(a for a in self.assets if a['archive']=='7B94AC');u={x['id']:x for x in a['units']}
        for s,actor in ((0,'NormalNaviYellow'),(4,'HeelNaviPurple'),(8,'HeelNaviBlack')):
            self.assertEqual(u[f'7B94AC:{s}:0']['speaker'],actor)
        self.assertIn('사교댄스',u['7B94AC:11:0']['translation'])
        self.assertIn('뛰는 놈',u['7B94AC:6:0']['translation'])
        for s,indices in ((0,(1,2)),(4,(2,3)),(8,(2,3))):
            for i in indices:self.assertEqual(u[f'7B94AC:{s}:{i}']['speaker'],'player-choice')

    def test_golf_shop19_not_prior18(self):
        a=next(a for a in self.assets if a['archive']=='7B9748');u={x['id']:x for x in a['units']}
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('shop = 19',source)
        self.assertNotIn('shop = 18',source)
        self.assertEqual(u['7B9748:221:0']['origin_portrait'],'PurpleNavi')
        for s,indices in ((223,(2,3)),(224,(4,5))):
            for i in indices:
                self.assertEqual(u[f'7B9748:{s}:{i}']['speaker'],'player-choice')
                self.assertEqual(u[f'7B9748:{s}:{i}']['portrait_visibility'],'visible')

    def test_golf_homepage_not_hitpoints_color_order(self):
        a=next(a for a in self.assets if a['archive']=='7B9C94');u={x['id']:x for x in a['units']}
        self.assertIn('홈페이지',u['7B9C94:10:1']['translation'])
        self.assertIn('바닥색',u['7B9C94:10:2']['translation'])
        for i,t in enumerate(('파랑','빨강\n','초록','그만두기\n'),1):
            self.assertEqual(u[f'7B9C94:11:{i}']['translation'],t)
            self.assertEqual(u[f'7B9C94:11:{i}']['speaker'],'player-choice')
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('disableB = true','count = 24','count = 12','callSetHomepageFloor','type = 0','type = 1','type = 2'):
            self.assertIn(t,source)

    def test_golf_floor_sfx_page_and_commands_preserved(self):
        a=next(a for a in self.assets if a['archive']=='7B9C94');u={x['id']:x for x in a['units']}
        for s in (12,13,14):
            self.assertEqual(u[f'7B9C94:{s}:1']['translation'],'...샤라랑!!')
            self.assertEqual(u[f'7B9C94:{s}:1']['speaker'],'MrProgGold')
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(source.count('soundDisableTextSFX'),3)
        self.assertEqual(source.count('track = 150'),3)
        self.assertEqual(source.count('soundEnableTextSFX'),3)

    def test_car_controls_reciprocal_and_optional_sunroof(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        self.assertIn('브레이크',u['7BA26C:0:1']['translation'])
        self.assertIn('멈출 수 없',u['7BA26C:0:2']['translation'])
        self.assertIn('가속',u['7BA26C:1:1']['translation'])
        self.assertIn('움직일 수 없',u['7BA26C:1:2']['translation'])
        self.assertIn('없어도',u['7BA7A0:0:1']['translation'])

    def test_car_patterns_order_not_golf_plain_colors(self):
        a=next(a for a in self.assets if a['archive']=='7BA7A0');u={x['id']:x for x in a['units']}
        for i,t in enumerate(('빨강&파랑','흰색&검정\n','무지개','그만두기\n'),1):
            self.assertEqual(u[f'7BA7A0:11:{i}']['translation'],t)
            self.assertEqual(u[f'7BA7A0:11:{i}']['speaker'],'player-choice')
        self.assertIn('홈페이지',u['7BA7A0:10:1']['translation'])
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('type = 3','type = 4','type = 5','disableB = true'):
            self.assertIn(t,source)
        self.assertEqual(source.count('spacePx\n\t\tcount = 24'),2)

    def test_car_rival_boast_and_pink_player_choices(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        self.assertIn('너한테는 졌지만',u['7BACD8:2:0']['translation'])
        self.assertIn('저쪽 내비',u['7BACD8:6:1']['translation'])
        self.assertEqual(u['7BA660:0:0']['speaker'],'NormalNaviPink')
        for key in ('7BA660:0:1','7BA660:0:2','7BACD8:0:1','7BACD8:4:2'):
            self.assertEqual(u[key]['speaker'],'player-choice')
            self.assertEqual(u[key]['portrait_visibility'],'hidden')
        self.assertEqual(u['7BACD8:0:1']['translation'],'좋아!  ')

    def test_car_garden_blades_water_and_native_battles(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        self.assertIn('잡초',u['7BAEF8:0:2']['translation'])
        self.assertIn('막힐 걱정',u['7BB31C:0:1']['translation'])
        for archive,battles in (('7BA660',(185,)),('7BACD8',(186,187))):
            a=next(a for a in self.assets if a['archive']==archive)
            source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for n in battles:self.assertIn('value = '+str(n),source)
            for t in ('flag = 1806','flag = 7701'):self.assertIn(t,source)

    def test_background_comic_moth_not_butterfly(self):
        a=next(a for a in self.assets if a['archive']=='7BB6C8');u={x['id']:x for x in a['units']}
        self.assertIn('나방',u['7BB6C8:1:1']['translation'])
        self.assertIn('모기',u['7BB6C8:1:1']['translation'])
        self.assertNotIn('나비',u['7BB6C8:1:1']['translation'])
        self.assertEqual(u['7BB6C8:0:1']['speaker'],'player-choice')

    def test_background_types_not_floor_and_grid(self):
        a=next(a for a in self.assets if a['archive']=='7BB878');u={x['id']:x for x in a['units']}
        for i,t in enumerate(('록맨','벚꽃\n','전뇌','그만두기\n'),1):
            self.assertEqual(u[f'7BB878:11:{i}']['translation'],t)
            self.assertEqual(u[f'7BB878:11:{i}']['speaker'],'player-choice')
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(source.count('callSetHomepageBG'),3)
        self.assertNotIn('callSetHomepageFloor',source)
        for t in ('count = 46','count = 12','type = 0','type = 1','type = 2','disableB = true'):
            self.assertIn(t,source)
        self.assertIn('배경색',u['7BB878:10:2']['translation'])

    def test_background_device_jobs_and_venue_name(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        self.assertIn('탈취력',u['7BB878:0:1']['translation'])
        self.assertIn('바늘구멍',u['7BBE54:0:1']['translation'])
        self.assertEqual(u['7BC27C:0:0']['translation'],'추, 추워...')
        self.assertEqual(u['7BC27C:20:1']['translation'],' 선수,\n또 도전해 줘!!')
        self.assertEqual(u['7BC27C:14:0']['speaker'],'NormalNaviBrown')
        self.assertIn('혈관',u['7BC27C:14:0']['translation'])

    def test_background_native_time_battle_and_sfx(self):
        for archive,tokens in (('7BB6C8',('value = 188','value = 666','flag = 1806')),('7BC27C',('flag = 1906','lowerHour = 9','lowerHour = 13','lowerHour = 16','lowerHour = 20'))):
            a=next(a for a in self.assets if a['archive']==archive)
            source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for t in tokens:self.assertIn(t,source)
        a=next(a for a in self.assets if a['archive']=='7BB878')
        self.assertEqual((ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig').count('track = 150'),3)

    def test_factory_heel_result_subjects(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        self.assertIn('내 패배',u['7BCC34:6:0']['translation'])
        self.assertIn('네 패배',u['7BCC34:7:0']['translation'])
        self.assertIn('내 바이러스',u['7BCC34:0:0']['translation'])
        self.assertIn('철판',u['7BC870:0:1']['translation'])

    def test_factory_disabled_program_hidden_observation(self):
        a=next(a for a in self.assets if a['archive']=='7BCEBC');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7BCEBC:0:0']['translation'],'......')
        self.assertEqual(u['7BCEBC:0:1']['speaker'],'system-observation')
        self.assertEqual(u['7BCEBC:0:1']['portrait_visibility'],'hidden')
        self.assertIn('당한 것 같다',u['7BCEBC:0:1']['translation'])
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('mugshotAnimation\n\t\tanimation = 0',source)

    def test_factory_same_portrait_different_voices_and_silence(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        for s in (0,4):self.assertEqual(u[f'7BD240:{s}:0']['speaker'],'HeelNaviPurple')
        self.assertIn('구먼',u['7BD240:4:0']['translation'])
        self.assertEqual(u['7BD240:8:3']['translation'],'......')
        self.assertEqual(u['7BD240:9:0']['translation'],'.........')
        self.assertEqual(u['7BD240:10:0']['translation'],'기 기 기 기 기...')
        self.assertEqual(u['7BCC34:9:0']['translation'].count('\n'),2)

    def test_factory_six_battles_native_and_choices(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        for archive,keys,battles in (('7BCC34',('0:3','0:4','4:1','4:2','8:2','8:3'),(189,190,191)),('7BD240',('0:1','0:2','4:3','4:4','8:1','8:2'),(192,193,194))):
            for key in keys:
                self.assertEqual(u[archive+':'+key]['speaker'],'player-choice')
                self.assertEqual(u[archive+':'+key]['portrait_visibility'],'hidden')
            a=next(a for a in self.assets if a['archive']==archive)
            source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for n in battles:self.assertIn('value = '+str(n),source)

    def test_media_napalm_normal_destination_and_command(self):
        a=next(a for a in self.assets if a['archive']=='7BD4B0');u={x['id']:x for x in a['units']}
        for key in ('0:8','2:2','3:0'):self.assertIn('인터넷1',u['7BD4B0:'+key]['translation'])
        self.assertFalse(any('언더인터넷2' in x['translation'] for x in a['units']))
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('startNapalmManMinigame\n\t\thard = false',source)
        self.assertIn('flag = 6194',source)
        self.assertIn('빌려주마',u['7BD4B0:0:11']['translation'])
        self.assertFalse(any('빌려' in x['translation'] for x in a['units'] if x['id'].startswith('7BD4B0:2:')))

    def test_media_napalm_plugout_failure_hidden_retry(self):
        a=next(a for a in self.assets if a['archive']=='7BD4B0');u={x['id']:x for x in a['units']}
        for key in ('0:13','2:5'):self.assertIn('절대로 플러그아웃',u['7BD4B0:'+key]['translation'])
        for i in (2,3):
            self.assertEqual(u[f'7BD4B0:4:{i}']['speaker'],'player-choice')
            self.assertEqual(u[f'7BD4B0:4:{i}']['portrait_visibility'],'hidden')
        self.assertIn('지나가라',u['7BD4B0:3:2']['translation'])

    def test_media_old_tv_vs_stereo_register(self):
        u={x['id']:x for a in self.assets for x in a['units']}
        self.assertIn('스·테·레·오',u['7BDC90:0:1']['translation'])
        self.assertEqual(u['7BDC90:0:4']['translation'],'땡큐!')
        self.assertIn('낡은 TV',u['7BE0CC:0:2']['translation'])
        self.assertIn('액정도 아니',u['7BE0CC:0:3']['translation'])

    def test_media_black_market_shops_and_visible_choices(self):
        a=next(a for a in self.assets if a['archive']=='7BE518');u={x['id']:x for x in a['units']}
        self.assertEqual(u['7BE518:221:0']['origin_portrait'],'HeelNaviBlack')
        self.assertEqual(u['7BE518:221:0']['portrait_visibility'],'inherited-from-caller')
        for s,ii in ((223,(4,5)),(224,(6,7)),(225,(4,5))):
            for i in ii:
                self.assertEqual(u[f'7BE518:{s}:{i}']['speaker'],'player-choice')
                self.assertEqual(u[f'7BE518:{s}:{i}']['portrait_visibility'],'visible')
        source=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for t in ('shop = 4','shop = 14','variable = 7','variable = 6','jumpIfEqual = 225','navi = 1'):
            self.assertIn(t,source)

    def test_hard_native_six_speakers(self):
        for idx,archive,scripts in ((19,'7B5328',((0,'NumberMan'),(5,'MetalMan'),(10,'SearchMan'))),(20,'7B5CC0',((0,'IceMan'),(10,'NapalmMan'),(20,'WindMan')))):
            units={u['id']:u for u in self.assets[idx]['units']}
            for s,p in scripts:self.assertEqual(units[f'{archive}:{s}:0']['speaker'],p)

    def test_hard_search_destination_not_easy_test(self):
        units={u['id']:u for u in self.assets[19]['units']}
        for key in ('10:7','12:2','14:4'):self.assertIn('인터넷7',units['7B5328:'+key]['translation'])
        for key in ('10:8','12:3'):
            self.assertIn('모두 저격',units['7B5328:'+key]['translation'])
            self.assertIn('제한 시간',units['7B5328:'+key]['translation'])
        for key in ('10:11','12:6'):self.assertIn('한 번이라도 플러그아웃',units['7B5328:'+key]['translation'])

    def test_hard_napalm_under_destination_and_plugout(self):
        units={u['id']:u for u in self.assets[20]['units']}
        for key in ('10:8','12:2','13:0'):self.assertIn('언더인터넷2',units['7B5CC0:'+key]['translation'])
        for key in ('10:9','12:3'):
            self.assertIn('모두 날려',units['7B5CC0:'+key]['translation'])
            self.assertIn('제한 시간',units['7B5CC0:'+key]['translation'])
        for key in ('10:13','12:5'):self.assertIn('절대로 플러그아웃하지 마라',units['7B5CC0:'+key]['translation'])
        self.assertIn('빌려주마',units['7B5CC0:10:11']['translation'])

    def test_hard_operator_not_navi_test(self):
        a={u['id']:u for u in self.assets[19]['units']};b={u['id']:u for u in self.assets[20]['units']}
        self.assertIn('네 오퍼레이터',a['7B5328:5:2']['translation'])
        self.assertIn('나를 오퍼레이팅',a['7B5328:5:2']['translation'])
        self.assertIn('네가 아니라',b['7B5CC0:20:2']['translation'])
        self.assertIn('네 오퍼레이터',b['7B5CC0:20:2']['translation'])
        self.assertIn('나를 오퍼레이팅',b['7B5CC0:20:3']['translation'])

    def test_hard_ice_passage_success_vs_failure(self):
        units={u['id']:u for u in self.assets[20]['units']}
        self.assertIn('만약',units['7B5CC0:0:4']['translation'])
        self.assertIn('약속대로',units['7B5CC0:1:1']['translation'])
        self.assertIn('지나가게 할 수 없어요',units['7B5CC0:2:1']['translation'])
        self.assertIn('1명',units['7B5CC0:0:3']['translation'])

    def test_hard_visible_retry_options_not_actor(self):
        units={u['id']:u for u in self.assets[20]['units']}
        for i in (2,3):
            u=units[f'7B5CC0:14:{i}']
            self.assertEqual(u['speaker'],'player-choice')
            self.assertEqual(u['origin_portrait'],'NapalmMan')
            self.assertEqual(u['portrait_visibility'],'visible')
        self.assertEqual(units['7B5CC0:14:4']['speaker'],'NapalmMan')

    def test_hard_source_calls_still_true_and_flags(self):
        for asset,calls in ((self.assets[19],('NumberMan','MetalMan','SearchMan')),(self.assets[20],('IceMan','NapalmMan','WindMan'))):
            source=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for name in calls:self.assertIn('start'+name+'Minigame\n\t\thard = true',source)
        self.assertEqual(len(self.validate(self.assets[19])),55)
        self.assertEqual(len(self.validate(self.assets[20])),67)

    def test_hard_choices_preserve_two_spaces_and_refusal(self):
        for asset in (a for a in self.assets[19:] if a['archive']!='7CE5C8'):
            for u in asset['units']:
                if u['source'].endswith('  '):
                    self.assertTrue(u['translation'].endswith('  '),u['id'])
                    self.assertEqual(u['speaker'],'ui-label' if u['id'] in batch500ah.LABELS or u['id'] in batch500ai.LABELS or u['id'] in batch500ap.LABELS or u['id'] in batch500at.LABELS else 'speaker-unestablished' if asset['archive']=='700F6C' else 'system-label' if asset['archive'] in ('6E1068','6E12DC') and u['id']==asset['archive']+':2:0' else 'equipment-label' if (asset['archive'] in batch500.ACTORS or asset['archive'] in batch500b.ACTORS) and u['id']==asset['archive']+':2:0' else 'player-choice')
        units={u['id']:u for u in self.assets[20]['units']}
        self.assertIn('다른 길',units['7B5CC0:11:0']['translation'])
        self.assertEqual(units['7B5CC0:11:0']['translation'],units['7B5CC0:15:0']['translation'])


    def test_batch500ag_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-033']
        self.assertEqual([a['archive'] for a in aa],['7A152C','7A8EC0','778338','700F6C','7A0354'])
        self.assertEqual([len(a['units']) for a in aa],[270,84,80,30,36])
        self.assertEqual(self.plan['draft_assets'][-390:-385],[v[2] for v in batch500ag.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-15]
        self.assertEqual(b['id'],'batch500-033');self.assertEqual(b['player_choices'],98)
        self.assertEqual(b['punctuation_literals'],5);self.assertFalse(b['rom_applied'])
        self.assertEqual(batch500ag.EXCLUDED,set())

    def test_batch500ag_choice_padding_and_roundtrip(self):
        for a in batch500ag.SOURCES:
            asset=batch500ag.create(a)
            self.assertEqual(asset,json.loads((ROOT/batch500ag.SOURCES[a][2]).read_text(encoding='utf8')))
            check_draft(asset,self.base,self.available,self.rom,self.rows)
            for u in asset['units']:
                self.assertEqual(u['speaker']=='player-choice',u['id'] in batch500ag.CHOICES)
                for side in ('lstrip','rstrip'):
                    self.assertEqual(len(u['source'])-len(getattr(u['source'],side)(' ')),len(u['translation'])-len(getattr(u['translation'],side)(' ')))
                self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
        self.assertEqual(len(batch500ag.CHOICES),98)

    def test_batch500ag_quiz_wrong_answers_and_original_controls(self):
        d=batch500ag.DRAFT['7A152C'];t=(ROOT/'analysis/full_scope_v1/source_tpl/7A152C.tpl').read_text(encoding='utf-8-sig')
        quiz=t.split('script 132 ')[1].split('\nscript 133 ')[0]
        self.assertEqual(quiz.count('disableB = true'),10)
        self.assertIn('더플 딜리트',' '.join(d.values()))
        self.assertIn('더블 딜리트',' '.join(d.values()))
        for k in ['132:51','132:52','132:53','132:64','132:65','132:66']:
            self.assertNotIn(k,d)
        self.assertIn('amount = 100',t);self.assertIn('amount = 1500',t)
        self.assertIn('chip = 104',t);self.assertIn('code = A',t)
        anomaly=t.split('script 39 ')[1].split('\nscript 40 ')[0]
        self.assertIn('jump = 36',anomaly)

    def test_batch500ag_internet6_native_trials(self):
        a=batch500ag.create('7A8EC0');u={x['id']:x for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),14)
        self.assertEqual(u['7A8EC0:41:0']['translation'],'.........')
        t=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('hard = false',t)
        self.assertIn('startMetalManMinigame',t)
        self.assertIn('MetalMan',t);self.assertIn('PlantMan',t)

    def test_batch500ag_plugout_preserves_selected_and_names(self):
        d=batch500ag.DRAFT['778338'];a=batch500ag.create('778338')
        self.assertEqual(sum(x['speaker']=='player-choice' for x in a['units']),38)
        for s in [6,7,26,27]:
            self.assertFalse(any(k.startswith(str(s)+':') for k in d))
        t=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('default = 1',t);self.assertIn('flag = 7711',t)
        self.assertTrue(d['19:0'].endswith('\n\n'))
        self.assertEqual(d['10:0'],'뭐야 ')
        self.assertTrue(d['13:1'].startswith('\n'))

    def test_batch500ag_bbs_and_gossip_punctuation(self):
        d=batch500ag.DRAFT['700F6C']
        self.assertEqual(len(d),30);self.assertIn('사무조',d['28:0'])
        a=batch500ag.create('700F6C')
        self.assertTrue(all(u['origin_portrait'] is None for u in a['units']))
        d=batch500ag.DRAFT['7A0354']
        for k in ['10:2','10:3','20:3','20:4']:
            self.assertEqual(d[k],'.')
        self.assertTrue(d['10:5'].startswith('\n'));self.assertTrue(d['20:6'].startswith('\n'))
        t=(ROOT/'analysis/full_scope_v1/source_tpl/7A0354.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(t.count('frames = 20'),6)


    def test_batch500ah_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-034']
        self.assertEqual([a['archive'] for a in aa],list(batch500ah.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[42]*11+[9,29])
        self.assertEqual(self.plan['draft_assets'][-385:-372],[v[2] for v in batch500ah.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-14]
        self.assertEqual(b['id'],'batch500-034');self.assertEqual(b['ui_labels'],119)
        self.assertEqual(b['player_choices'],0);self.assertEqual(b['punctuation_literals'],2)
        self.assertFalse(b['rom_applied']);self.assertEqual(batch500ah.EXCLUDED,set())

    def test_batch500ah_labels_portraits_and_repro(self):
        total=labels=0
        for a in batch500ah.SOURCES:
            asset=batch500ah.create(a)
            self.assertEqual(asset,json.loads((ROOT/batch500ah.SOURCES[a][2]).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(asset)),len(asset['units']))
            for u in asset['units']:
                total+=1;labels+=u['speaker']=='ui-label'
                self.assertEqual(u['speaker']=='ui-label',u['id'] in batch500ah.LABELS)
                self.assertNotEqual(u['speaker'],'player-choice')
                if a in batch500ah.COMMUNICATION_ARCHIVES:
                    self.assertIsNone(u['origin_portrait'])
                    self.assertEqual(u['speaker'],'ui-label' if u['id'] in batch500ah.LABELS else 'speaker-unestablished')
        self.assertEqual((total,labels),(500,119));self.assertEqual(batch500ah.CHOICES,set())

    def test_batch500ah_modes_counters_and_padding(self):
        for a in batch500ah.COMMUNICATION_ARCHIVES:
            d=batch500ah.DRAFT[a];t=(ROOT/batch500ah.SOURCES[a][2]).read_text(encoding='utf8')
            self.assertEqual(d['1:0'],'전적 ');self.assertEqual(d['1:1'],'전');self.assertEqual(d['1:2'],'승')
            self.assertEqual(d['7:0'],'싱글 배틀      ');self.assertEqual(d['8:0'],'트리플 배틀      ')
            self.assertEqual(d['9:0'],'배틀 칩 게이트 사용 ');self.assertEqual(d['10:0'],'배틀 칩 게이트 미사용 ')
            self.assertIn('4.5',d['15:0']);self.assertIn('4',d['16:0'])
            self.assertEqual(re.findall(r'\d+',d['18:0']),['3','2'])
            for k in ('19:0','34:0','55:0','57:0'):self.assertIn('쓰고',d[k])
            for k in ('20:0','35:0','56:0','58:0'):self.assertIn('없이',d[k])
            self.assertIn('뺀 다음',d['35:1'])
            for k in ('31:0','51:0'):self.assertIn('통신 케이블',d[k])
            src=(ROOT/batch500ah.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertIn('buffer = 0',src);self.assertIn('buffer = 1',src)
            self.assertEqual(src.count('minLength = 3'),2)

    def test_batch500ah_native_pointer_and_quick_layout(self):
        import struct
        self.assertEqual(list(struct.unpack_from('<11I',self.rom,0x448E0)),[0x08000000+int(a,16) for a in batch500ah.COMMUNICATION_ARCHIVES])
        for a in batch500ah.COMMUNICATION_ARCHIVES:
            src=(ROOT/batch500ah.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('msgOpenQuick'),24);self.assertEqual(src.count('waitHold'),24)
            for token in ('left = 10','top = 12','left = 92','top = 110','left = 225','top = 141','delay = 0'):
                self.assertIn(token,src)
            self.assertNotIn('mugshotShow',src);self.assertNotIn('\n\toption\n',src)

    def test_batch500ah_distinct_source_voice_and_folders(self):
        d=batch500ah.DRAFT
        self.assertIn('거스',d['6F5D38']['15:0']);self.assertIn('거츠',d['6F5D38']['17:0'])
        self.assertIn('바람',d['6F605C']['40:0']);self.assertIn('미션 실패',d['6F63A8']['45:0'])
        self.assertIn('완전 연소',d['6F66C8']['41:0']);self.assertIn('뇌신',d['6F6A04']['41:0'])
        self.assertIn('0%',d['6F7084']['46:0']);self.assertIn('영혼',d['6F73C4']['41:0'])
        self.assertIn('나, 나',d['6F76FC']['40:0'])
        self.assertEqual([d['708FF0'][str(s)+':0'] for s in (2,6,7)],['허접 폴더']*3)
        self.assertEqual(d['708FF0']['10:0'],'배낭')

    def test_batch500ah_timed_npc_portraits_and_animation(self):
        asset=batch500ah.create('7A0734');u={x['id']:x for x in asset['units']}
        self.assertEqual(u['7A0734:0:0']['origin_portrait'],'NaviGirlOrange')
        self.assertEqual(u['7A0734:20:0']['origin_portrait'],'NormalNaviPink')
        self.assertEqual(u['7A0734:40:0']['origin_portrait'],'NormalNaviYellow')
        self.assertIn('수요일',u['7A0734:12:1']['translation'])
        self.assertIn('5',u['7A0734:12:0']['translation'])
        for k in ('7A0734:10:3','7A0734:10:4'):self.assertEqual(u[k]['translation'],'.')
        self.assertTrue(u['7A0734:10:6']['translation'].startswith('\n'))
        src=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('frames = 20'),3)
        self.assertIn('lowerHour = 18',src);self.assertIn('lowerMinutes = 25',src)


    def test_batch500ai_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-035']
        self.assertEqual([a['archive'] for a in aa],list(batch500ai.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[42,43]+[42]*8+[79])
        self.assertEqual(self.plan['draft_assets'][-372:-361],[v[2] for v in batch500ai.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-13]
        self.assertEqual((b['id'],b['authored_literals'],b['communication_menus'],b['saturday_plaza_npcs']),('batch500-035',500,421,79))
        self.assertEqual((b['ui_labels'],b['player_choices'],b['punctuation_literals']),(100,0,9))
        self.assertFalse(b['rom_applied']);self.assertEqual(batch500ai.EXCLUDED,set())

    def test_batch500ai_labels_portraits_repro_codec(self):
        total=labels=0
        for a,(_,count,path) in batch500ai.SOURCES.items():
            asset=batch500ai.create(a)
            self.assertEqual(asset,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(asset)),count)
            self.assertFalse(asset['review']['release_eligible'])
            for u in asset['units']:
                total+=1;labels+=u['speaker']=='ui-label'
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['speaker']=='ui-label',u['id'] in batch500ai.LABELS)
                self.assertNotEqual(u['speaker'],'player-choice')
                for original,translated in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(original)-len(original.lstrip(' ')),len(translated)-len(translated.lstrip(' ')))
                if a in batch500ai.COMMUNICATION_ARCHIVES:
                    self.assertIsNone(u['origin_portrait'])
                    self.assertEqual(u['speaker'],'ui-label' if u['id'] in batch500ai.LABELS else 'speaker-unestablished')
        self.assertEqual((total,labels),(500,100));self.assertEqual(batch500ai.CHOICES,set())

    def test_batch500ai_modes_counters_padding(self):
        for a in batch500ai.COMMUNICATION_ARCHIVES:
            d=batch500ai.DRAFT[a]
            self.assertEqual(d['1:0'],'전적 ');self.assertEqual(d['1:1'],'전');self.assertEqual(d['1:2'],'승')
            self.assertEqual(d['7:0'],'싱글 배틀      ');self.assertEqual(d['8:0'],'트리플 배틀      ')
            self.assertEqual(d['9:0'],'배틀 칩 게이트 사용 ');self.assertEqual(d['10:0'],'배틀 칩 게이트 미사용 ')
            self.assertIn('4.5',d['15:0']);self.assertIn('4',d['16:0'])
            self.assertEqual(re.findall(r'\d+',d['18:0']),['3','2'])
            for k in ('19:0','34:0','55:0','57:0'):self.assertIn('쓰고',d[k])
            for k in ('20:0','35:0','56:0','58:0'):self.assertIn('없이',d[k])
            self.assertIn('뺀 다음',d['35:1'])
            for k in ('31:0','51:0'):self.assertIn('통신 케이블',d[k])
            src=(ROOT/batch500ai.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('minLength = 3'),2)
            for token in ('buffer = 0','buffer = 1','padLeft = true','padZeros = false'):self.assertIn(token,src)
        self.assertEqual(re.findall(r'\d+',batch500ai.DRAFT['6F8698']['17:0']),['1','1'])
        self.assertEqual(re.findall(r'\d+',batch500ai.DRAFT['6F89D0']['50:0']),['1'])

    def test_batch500ai_pointer_quick_layout_wood_join(self):
        import struct
        words=struct.unpack_from('<23I',self.rom,0x448E0)
        self.assertEqual([words[i] for i in (11,12,15,16,17,18,19,20,21,22)],[0x08000000+int(a,16) for a in batch500ai.COMMUNICATION_ARCHIVES])
        self.assertEqual(words[13],words[0]);self.assertEqual(words[14],words[0])
        for a in batch500ai.COMMUNICATION_ARCHIVES:
            src=(ROOT/batch500ai.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('msgOpenQuick'),24);self.assertEqual(src.count('waitHold'),24)
            for token in ('left = 10','top = 12','left = 92','top = 110','left = 225','top = 141','delay = 0'):
                self.assertEqual(src.count(token),24)
            self.assertNotIn('mugshotShow',src);self.assertNotIn('\n\toption\n',src)
        asset=batch500ai.create('6F7D10');src=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
        block=re.search(r'script 41 \w+ \{(.*?)(?=\nscript )',src,re.S).group(1)
        self.assertNotIn('clearMsg',block)
        u=[x for x in literals(src) if x.key.startswith('6F7D10:41:')]
        self.assertEqual(len(u),2);self.assertTrue(u[1].text.endswith('\n'))
        self.assertTrue(batch500ai.DRAFT['6F7D10']['41:1'].endswith('\n'))
        self.assertEqual(batch500ai.DRAFT['6F9698']['37:0'].count('\n'),2)

    def test_batch500ai_source_voice_candidates_not_approval(self):
        d=batch500ai.DRAFT
        self.assertIn('퓨',d['6F7A04']['41:0']);self.assertIn('알 수 없는',d['6F7A04']['45:0'])
        self.assertIn('대지',d['6F7D10']['40:0']);self.assertIn('초신성',d['6F8018']['41:0'])
        self.assertIn('암살',d['6F8344']['40:0']);self.assertIn('소인',d['6F8344']['45:0'])
        self.assertIn('나이트맨',d['6F8698']['41:0']);self.assertIn('미션 컴플리트',d['6F89D0']['41:0'])
        self.assertIn('빙수',d['6F8D00']['41:0']);self.assertNotEqual(d['6F8D00']['31:0'],d['6F8D00']['51:0'])
        self.assertIn('전압',d['6F9038']['40:0']);self.assertIn('꽃다발이라도',d['6F9358']['40:0'])
        self.assertIn('파괴 충동',d['6F9698']['45:0'])
        self.assertTrue(all(a['review']['wording']=='needs_review' for a in self.assets if a.get('batch_id')=='batch500-035'))

    def test_batch500ai_saturday_time_anomaly_poems_dots(self):
        asset=batch500ai.create('7A4DD4');u={x['id']:x for x in asset['units']}
        src=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
        expected={0:'PurpleNavi',10:'OfficialNavi',20:'HeelNaviBlack',30:'NormalNaviYellow',40:'NaviGirlOrange',50:'MrProgGreen',60:'MrProgGreen',70:'NormalNaviBrown',90:'NormalNaviPink',110:'HeelNaviPurple'}
        for script,portrait in expected.items():self.assertEqual(u['7A4DD4:'+str(script)+':0']['origin_portrait'],portrait)
        self.assertEqual(sum(x['source']=='・' for x in u.values()),9)
        self.assertEqual(src.count('frames = 20'),9)
        for x in u.values():
            if x['source']=='・':self.assertEqual(x['translation'],'.')
        for k in ('70:6','71:7'):
            self.assertTrue(all(line.startswith(' ') for line in u['7A4DD4:'+k]['translation'].split('\n')[1:]))
        block=re.search(r'script 10 \w+ \{(.*?)(?=\nscript )',src,re.S).group(1)
        self.assertEqual(re.findall(r'jumpIfInRange = (\d+)',block),['1','2'])
        self.assertIn('토요일',u['7A4DD4:21:0']['translation'])
        self.assertIn('플러그아웃',u['7A4DD4:22:0']['translation'])
        self.assertIn('S라이선스',u['7A4DD4:110:1']['translation'])
        self.assertIn('후회',u['7A4DD4:60:1']['translation'])
        self.assertNotIn('itemGive',src)


    def test_batch500aj_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-036']
        self.assertEqual([a['archive'] for a in aa],list(batch500aj.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[14,46,39,22,32,29,52,38,34,43,38,13,52,27,21])
        self.assertEqual(self.plan['draft_assets'][-361:-346],[v[2] for v in batch500aj.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-12]
        self.assertEqual((b['id'],b['authored_literals'],b['timed_npcs'],b['battle_npcs'],b['school_npcs']),('batch500-036',500,338,149,13))
        self.assertEqual((b['player_choices'],b['punctuation_literals'],b['poems']),(24,33,6))
        self.assertFalse(b['rom_applied']);self.assertEqual(batch500aj.EXCLUDED,set());self.assertEqual(batch500aj.LABELS,set())

    def test_batch500aj_repro_source_codec_padding_portraits(self):
        total=choices=0
        for a,(_,count,path) in batch500aj.SOURCES.items():
            asset=batch500aj.create(a)
            self.assertEqual(asset,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(asset)),count)
            self.assertFalse(asset['review']['release_eligible'])
            for u in asset['units']:
                total+=1;choices+=u['speaker']=='player-choice'
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['speaker']=='player-choice',u['id'] in batch500aj.CHOICES)
                if u['id'] in batch500aj.CHOICES:
                    self.assertIsNone(u['origin_portrait']);self.assertEqual(u['portrait_visibility'],'hidden')
                else:
                    self.assertEqual(u['speaker'],u['origin_portrait']);self.assertEqual(u['portrait_visibility'],'shown')
                for source,target in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(source)-len(source.lstrip(' ')),len(target)-len(target.lstrip(' ')))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
        self.assertEqual((total,choices),(500,24))

    def test_batch500aj_time_roles_numbers_midnight(self):
        d=batch500aj.DRAFT
        self.assertIn('일요일',d['79CF04']['0:0']);self.assertIn('수요일',d['79DC10']['20:0'])
        self.assertIn('토요일',d['79EE9C']['0:0']);self.assertIn('7시',d['79FFF4']['1:0'])
        self.assertIn('4번',d['79DC10']['24:3'])
        self.assertIn('월, 수, 목, 토',d['79DC10']['24:3'])
        self.assertIn('금요일',d['7A0D18']['10:0']);self.assertIn('토요일',d['7A0D18']['12:1'])
        self.assertIn('월요일',d['7A3C0C']['20:1']);self.assertIn('목요일',d['7A0A44']['22:0'])
        asset=batch500aj.create('79EE9C');u={x['id']:x for x in asset['units']}
        self.assertEqual([u['79EE9C:60:'+str(i)]['origin_portrait'] for i in range(4)],['NormalNaviYellow','NormalNaviYellow','NormalNaviPink','NormalNaviYellow'])
        self.assertEqual([u['79EE9C:71:'+str(i)]['origin_portrait'] for i in range(5)],['NormalNaviPink','NormalNaviYellow','NormalNaviPink','NormalNaviYellow','NormalNaviYellow'])
        self.assertIn('에리어 스틸',d['79EE9C']['60:1'])
        self.assertEqual([re.findall(r'\d+',d['79EE9C'][k]) for k in ('71:3','71:4')],[['1000'],['1000']])
        src=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('lowerHour = 25','upperHour = 29','lowerMinutes = 26'):self.assertIn(token,src)
        self.assertNotIn('itemGive',src);self.assertNotIn('itemGiveChip',src)

    def test_batch500aj_animation_poems_and_segmented_speech(self):
        waits={'79EE9C':1,'79FFF4':4,'7A0A44':6,'7A0D18':9,'7A3C0C':6,'7A4010':6,'7A4348':9}
        dots=0
        for a in batch500aj.SOURCES:
            asset=batch500aj.create(a);src=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('frames = 20'),waits.get(a,0))
            for u in asset['units']:
                if u['source']=='・':
                    dots+=1;self.assertEqual(u['translation'],'.')
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
        self.assertEqual(dots,33)
        poems={'7A3C0C':['70:6','71:6'],'7A4010':['70:7','71:7'],'7A4348':['70:6','71:7']}
        for a,keys in poems.items():
            for k in keys:
                self.assertEqual(batch500aj.DRAFT[a][k].count('\n'),2)
                self.assertTrue(all(l.startswith(' ') for l in batch500aj.DRAFT[a][k].split('\n')[1:]))
        self.assertEqual([batch500aj.DRAFT['7A0D18']['40:'+str(i)] for i in range(3)],['하이!!','텐!!','셔---언!!'])

    def test_batch500aj_battle_choices_globals_and_routes(self):
        groups={'7A0D18':[(71,150,628)],'7A6BC8':[(1,151,629),(5,153,631),(9,152,630)],'7AAF94':[(1,158,636),(6,159,637),(11,160,638),(16,161,639)],'7A7FC4':[(1,154,632),(6,155,633)],'7B1D40':[(1,168,646),(5,169,647)]}
        for a,triples in groups.items():
            src=(ROOT/batch500aj.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(src.count('\n\toption\n'),len(triples)*2)
            self.assertEqual(src.count('default = 0'),len(triples))
            self.assertNotIn('itemGive',src)
            for script,battle_id,event_id in triples:
                block=re.search(r'script '+str(script)+r' \w+ \{(.*?)(?=\nscript |\Z)',src,re.S).group(1)
                self.assertRegex(block,r'global = 24\s+value = '+str(battle_id)+r'\b')
                self.assertRegex(block,r'global = 27\s+value = '+str(event_id)+r'\b')
                for flag in (1806,7701):self.assertIn('flag = '+str(flag),block)
        d=batch500aj.DRAFT
        self.assertIn('그만할래',d['7AAF94']['4:1'])
        self.assertIn('컨디션',d['7A7FC4']['9:0'])
        self.assertIn('갈 길이 먼',d['7B1D40']['2:0'])
        self.assertIn('내가 졌다',d['7A0D18']['72:0'])
        self.assertIn('최강',d['7A0D18']['73:0'])

    def test_batch500aj_humour_culture_and_voice_review_pending(self):
        d=batch500aj.DRAFT
        self.assertIn('엉뚱한 소리',d['79FCC8']['31:2']);self.assertIn('태클',d['79FCC8']['31:2'])
        self.assertIn('새우튀김',d['7A0D18']['10:1']);self.assertIn('일본 문화',d['7A3C0C']['71:1'])
        self.assertIn('미니봄',d['7A4010']['71:1']);self.assertIn('소인',d['7A6BC8']['0:1'])
        self.assertIn('필살기',d['7AAF94']['14:1']);self.assertIn('저, 저랑',d['7AAF94']['15:1'])
        self.assertIn('지고 도망',d['7AAF94']['19:0'])
        self.assertIn('명태',d['7AF164']['10:0']);self.assertIn('일본',d['7AF164']['10:0'])
        self.assertIn('사회',d['7AF164']['14:0'])
        self.assertTrue(all(a['review']['wording']=='needs_review' for a in self.assets if a.get('batch_id')=='batch500-036'))


    def test_batch500ak_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-037']
        self.assertEqual([a['archive'] for a in aa],list(batch500ak.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[18,24,26,63,25,29,24,41,72,37,36,27,26,9,19,24])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-346:-330],[v[2] for v in batch500ak.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-11]
        self.assertEqual((b['id'],b['authored_literals'],b['obstacles_inspection_rewards'],b['tournament_hosts']),('batch500-037',500,457,43))
        self.assertEqual((b['ui_labels'],b['player_choices'],b['punctuation_literals']),(1,8,3))
        self.assertFalse(b['rom_applied']);self.assertEqual(batch500ak.EXCLUDED,set())

    def test_batch500ak_repro_source_codec_and_padding(self):
        choices=labels=0
        for a,(_,count,path) in batch500ak.SOURCES.items():
            asset=batch500ak.create(a)
            self.assertEqual(asset,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(asset)),count)
            self.assertFalse(asset['review']['release_eligible'])
            for u in asset['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['speaker']=='player-choice',u['id'] in batch500ak.CHOICES)
                self.assertEqual(u['speaker']=='ui-label',u['id'] in batch500ak.LABELS)
                choices+=u['speaker']=='player-choice';labels+=u['speaker']=='ui-label'
                if u['id'] in batch500ak.CHOICES:self.assertIsNone(u['origin_portrait'])
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for source,target in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(source)-len(source.lstrip(' ')),len(target)-len(target.lstrip(' ')))
        self.assertEqual((choices,labels),(8,1))

    def test_batch500ak_named_voices_and_gate_identity(self):
        u={x['id']:x for a in self.assets if a.get('batch_id')=='batch500-037' for x in a['units']}
        portraits={'799314:4:0':'GutsMan','799314:5:0':'MetalMan','799314:6:0':'KnightMan','7994EC:7:0':'WoodMan','7994EC:8:0':'PlantMan','799CAC:6:0':'FireMan','799CAC:7:0':'NapalmMan','799CAC:8:0':'AquaMan','799CAC:9:0':'IceMan','799F58:4:0':'NumberMan','799F58:5:0':'ProtoMan','799F58:6:0':'ShadowMan','79A340:6:0':'ThunderMan','79A340:7:0':'ElecMan','79A340:9:0':'WindMan','79A340:10:0':'Bass'}
        for k,v in portraits.items():self.assertEqual(u[k]['origin_portrait'],v);self.assertEqual(u[k]['speaker'],v)
        for k in ('79C084:0:0','79C084:7:0','799314:7:0','799CAC:10:0'):self.assertIsNone(u[k]['origin_portrait'])
        self.assertIn('거스',u['799314:4:1']['translation'])
        self.assertIn('자장가',u['7994EC:8:1']['translation'])
        self.assertIn('타 버려라',u['7994EC:10:1']['translation'])
        self.assertIn('셰이드맨',u['79B750:3:1']['translation'])
        self.assertIn('최강',u['79B750:16:0']['translation'])
        self.assertIn('풀어',u['79C084:7:1']['translation'])

    def test_batch500ak_dynamic_boundaries_without_fixed_particles(self):
        d=batch500ak.DRAFT
        for a,k in [('7994EC','0:0'),('799F58','24:2'),('79AF64','3:0'),('79B45C','13:0'),('79BB10','2:2')]:
            self.assertEqual(d[a][k],':\n「')
        self.assertEqual(d['79AF64']['3:6'],':')
        self.assertEqual(d['79B750']['16:1'],':\n')
        self.assertEqual(d['79B750']['16:2'],',\n내밀었다!!')
        for a,k in [('79A340','8:0'),('79A8E4','10:0'),('79AF64','13:0'),('79B750','8:0'),('79BB10','14:0')]:
            self.assertTrue(d[a][k].startswith('의 손으로,\n'))
        self.assertEqual(d['799F58']['20:2'],': 배틀 칩\n「')
        self.assertEqual(d['799F58']['20:3'],'」\n획득했다!!')
        self.assertEqual(d['79AF64']['34:3'],'제니」\n획득했다!!')
        for a,k in [('799314','2:1'),('7994EC','3:1'),('799CAC','4:1'),('799F58','2:1'),('79A340','4:1'),('79A8E4','2:1'),('79AF64','4:1'),('79B750','4:1'),('79BB10','3:1'),('79BDE4','2:1')]:
            self.assertEqual(d[a][k],'」이다\n절로 손을 모으고 싶어진다')

    def test_batch500ak_payments_rewards_and_consumption(self):
        d=batch500ak.DRAFT
        self.assertIn('세금 포함10000제니',d['7994EC']['2:2'])
        self.assertIn('20개를 바쳐',d['79AB58']['2:3']);self.assertIn('20개를 바쳤',d['79AB58']['2:8'])
        self.assertIn('부족',d['79AB58']['18:0'])
        for a,start,frags,chip_ids,zenny in [('799F58',20,[2,3],[29,119,8,46],[490,670]),('79AF64',30,[3,4],[29,95,121,55],[560,770])]:
            src=(ROOT/batch500ak.create(a)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            blocks={int(m.group(1)):m.group(2) for m in re.finditer(r'script (\d+) \w+ \{(.*?)(?=\nscript |\Z)',src,re.S)}
            for i,chip in enumerate(chip_ids):
                self.assertRegex(blocks[start+i],r'itemGiveChip\s+chip = '+str(chip)+r'\s+code = A\s+amount = 1')
            for i,n in enumerate(zenny):self.assertIn('amount = '+str(n),blocks[start+4+i])
            for i,n in enumerate(frags):
                self.assertIn('amount = '+str(n),blocks[start+6+i])
                self.assertIn(str(n)+'개 획득',d[a][str(start+6+i)+':2'])
        src=(ROOT/batch500ak.create('79A340')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(src,r'itemTake\s+item = 20\s+amount = 1')
        src=(ROOT/batch500ak.create('79AF64')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(src,r'checkChipCode\s+chip = 85\s+code = A\s+amount = 1')
        self.assertNotIn('itemTakeChip',src)
        src=(ROOT/batch500ak.create('79AB58')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(src,r'checkTakeBugFrags\s+amount = 20')
        src=(ROOT/batch500ak.create('79B45C')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertNotIn('itemTake',src)
        self.assertIn('플러스 잠금',d['79B45C']['17:0']);self.assertIn('작동 중',d['79B45C']['17:0'])

    def test_batch500ak_tournament_schedule_choices_dots_and_temporary_label(self):
        d=batch500ak.DRAFT
        for a,tournament_id,completion,portrait in [('79C2C4',4,1854,'PurpleNavi'),('79C608',5,1877,'NormalNaviYellow')]:
            asset=batch500ak.create(a);src=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(re.findall(r'lowerHour = (\d+)',src),['9','13','16','20'])
            self.assertEqual(re.findall(r'upperMinutes = (\d+)',src),['59']*4)
            self.assertIn('tournament = '+str(tournament_id),src);self.assertIn('flag = '+str(completion),src)
            self.assertEqual(src.count('\n\toption\n'),2);self.assertIn('width = 8',src)
            self.assertIn('flag = 7736',src)
            self.assertEqual(next(x for x in asset['units'] if x['id']==a+':2:0')['origin_portrait'],portrait)
            for x in asset['units']:
                if 'PM4:00' in x['source']:self.assertEqual(x['source'].split('\n')[:2],x['translation'].split('\n')[:2])
        self.assertIn('에·브·리',d['79C2C4']['2:0'])
        self.assertIn('다시 와',d['79C2C4']['3:0'])
        self.assertIn('참가하시겠어요',d['79C608']['2:6'])
        self.assertIn('시작한다',d['79C608']['2:10'])
        self.assertIn('2등도3등도',d['79C608']['2:12'])
        self.assertEqual([d['79C608']['2:'+str(i)] for i in (7,8,9)],['.']*3)
        src=(ROOT/batch500ak.create('79C608')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(src.count('frames = 30'),3)
        self.assertEqual(d['79C608']['0:0'],'노멀 트레이더(임시)')
        self.assertTrue(all(a['review']['wording']=='needs_review' for a in self.assets if a.get('batch_id')=='batch500-037'))


    def test_batch500al_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-038']
        self.assertEqual([a['archive'] for a in aa],list(batch500al.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[29,29,28,27,27,27,27,28,28,27,27,28,27,27,27,27,27,27,6])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-330:-311],[v[2] for v in batch500al.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-10]
        self.assertEqual((b['id'],b['authored_literals'],b['progress_hints'],b['weekend_ninja_npc']),('batch500-038',500,494,6))
        self.assertEqual(b['player_choices'],0);self.assertFalse(b['rom_applied'])
        self.assertEqual(batch500al.EXCLUDED,set())

    def test_batch500al_repro_source_codec_and_topology(self):
        for a,(_,count,path) in batch500al.SOURCES.items():
            asset=batch500al.create(a)
            self.assertEqual(asset,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(asset)),count)
            self.assertFalse(asset['review']['release_eligible'])
            for u in asset['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for source,target in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(source)-len(source.lstrip(' ')),len(target)-len(target.lstrip(' ')))

    def test_batch500al_native_portraits_and_voice_distinctions(self):
        portraits=['MegaMan','Roll','GutsMan','WindMan','SearchMan','FireMan','ThunderMan','ProtoMan','NumberMan','MetalMan','JunkMan','AquaMan','WoodMan','StarMan','ShadowMan','KnightMan','NapalmMan','IceMan','HeelNaviBlack']
        for a,portrait in zip(batch500al.SOURCES,portraits):
            asset=next(x for x in self.assets if x['archive']==a)
            self.assertTrue(all(u['speaker']==portrait and u['origin_portrait']==portrait for u in asset['units']))
        d=batch500al.DRAFT
        self.assertIn('거츠거츠',d['787418']['13:0']);self.assertIn('거스',d['787418']['13:1'])
        self.assertIn('나, 인기쟁이',d['788F40']['30:0']);self.assertIn('나, 나 힘낸다',d['788F40']['12:0'])
        self.assertIn('썩 내키지는',d['788858']['27:0']);self.assertIn('영혼',d['788858']['30:0'])
        self.assertIn('무섭지만퓨',d['7892C8']['27:0']);self.assertIn('주먹',d['788BD8']['30:0'])
        self.assertIn('닌자의 극의',d['789D00']['29:0']);self.assertIn('무사의 피',d['78A088']['30:0'])
        self.assertIn('차갑게 불타',d['78A7A8']['30:0']);self.assertIn('더 쏘고',d['78A420']['31:0'])
        self.assertIn('우리가 빛나기에',d['789998']['30:0'])

    def test_batch500al_dynamic_chip_and_nickname_boundaries(self):
        for a in list(batch500al.SOURCES)[:-1]:
            src=(ROOT/batch500al.SOURCES[a][2]).read_text(encoding='utf8')
            native=(ROOT/('analysis/full_scope_v1/source_tpl/'+a+'.tpl')).read_text(encoding='utf-8-sig')
            self.assertRegex(native,r'printChip\s+buffer = 0\s+chip = 104')
            self.assertTrue(batch500al.DRAFT[a]['13:1'].startswith('」\n'))
            self.assertNotRegex(batch500al.DRAFT[a]['13:1'],r'^」 ?[을를]')
            self.assertNotIn('player-choice',src)
        for a,k in [('786D38','28:0'),('7870A8','10:0'),('787418','12:0'),('78776C','28:0'),('787ACC','14:0'),('7884E8','17:1'),('788F40','10:0'),('78963C','31:0')]:
            self.assertTrue(batch500al.DRAFT[a][k].startswith(',\n'))
        for a,k in [('7884E8','30:0'),('78A088','30:0'),('78A088','32:0')]:
            self.assertTrue(batch500al.DRAFT[a][k].startswith('\n'))
        self.assertEqual(batch500al.DRAFT['7870A8']['28:1'],'참가 신청하러 가자!')
        self.assertEqual(batch500al.DRAFT['7884E8']['15:1'],'조금\n쉬시겠습니까?')

    def test_batch500al_case_key_and_weekday_priority(self):
        for a in list(batch500al.SOURCES)[:-1]:
            native=(ROOT/('analysis/full_scope_v1/source_tpl/'+a+'.tpl')).read_text(encoding='utf-8-sig')
            blocks={int(m.group(1)):m.group(2) for m in re.finditer(r'script (\d+) \w+ \{(.*?)(?=\nscript |\Z)',native,re.S)}
            start=blocks[10]
            self.assertLess(start.index('bitmask = 4'),start.index('flag = 4270'))
            self.assertLess(start.index('flag = 4270'),start.index('flag = 1322'))
            self.assertLess(start.index('flag = 1322'),start.index('flag = 1298'))
            self.assertRegex(start,r'checkItem\s+item = 11\s+amount = 1\s+jumpIfEqual = 25')
            self.assertRegex(blocks[27],r'checkSubArea\s+lower = 0\s+upper = 3\s+jumpIfInRange = 35')
            for s in (26,28,29):
                self.assertEqual(re.findall(r'lower = (\d+)',blocks[s]),['0','6'])
                self.assertIn('jumpIfInRange = '+('30' if s==29 else '34'),blocks[s])
            for s,n in [(16,3),(18,5),(19,7),(20,9),(21,10),(22,12)]:
                self.assertIn('인터넷'+str(n),batch500al.DRAFT[a][str(s)+':0'])
            self.assertIn('인터넷9',batch500al.DRAFT[a]['25:0'])
            self.assertIn('관',batch500al.DRAFT[a]['35:0'])
            self.assertNotIn('callTournament',native)
        self.assertIn('아직 읽지 않은',batch500al.DRAFT['788198']['33:0'])
        self.assertIn('태세를 가다듬기',batch500al.DRAFT['789D00']['17:1'])
        self.assertIn('합격했군',batch500al.DRAFT['788BD8']['15:0'])

    def test_batch500al_weekend_ninja_npc_is_not_shadowman(self):
        a=next(x for x in self.assets if x['archive']=='7A6F0C')
        native=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(native,r'checkNetTime\s+lowerHour = 15\s+lowerMinutes = 30\s+upperHour = 19\s+upperMinutes = 45\s+jumpIfInRange = 1')
        self.assertEqual([x['origin_portrait'] for x in a['units']],['HeelNaviBlack']*6)
        d=batch500al.DRAFT['7A6F0C']
        self.assertIn('주말',d['0:0']);self.assertIn('오퍼레이터도',d['0:1'])
        self.assertIn('쉬지 않소',d['0:1']);self.assertIn('휴일은 없소',d['0:2'])
        self.assertIn('부족하오',d['1:0']);self.assertIn('최강의 닌자 내비',d['1:1'])
        self.assertEqual(d['1:2'],'닌닌!!')


    def test_batch500am_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-039']
        self.assertEqual([a['archive'] for a in aa],list(batch500am.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[16]*21+[27]*3+[6,77])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-311:-285],[v[2] for v in batch500am.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-9]
        self.assertEqual((b['id'],b['authored_literals'],b['subchip_descriptions_use'],b['progress_hints'],b['official_npcs'],b['internet4_npcs']),('batch500-039',500,336,81,6,77))
        self.assertEqual((b['ui_labels'],b['player_choices']),(126,52))
        self.assertFalse(b['rom_applied']);self.assertEqual(batch500am.EXCLUDED,set())

    def test_batch500am_repro_source_codec_and_topology(self):
        for a,(_,count,path) in batch500am.SOURCES.items():
            asset=batch500am.create(a)
            self.assertEqual(asset,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(asset)),count)
            self.assertFalse(asset['review']['release_eligible'])
            for u in asset['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for source,target in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(source)-len(source.lstrip(' ')),len(target)-len(target.lstrip(' ')))

    def test_batch500am_subchip_labels_portraits_and_effect_limits(self):
        portraits=['MegaMan','Roll','GutsMan','WindMan','SearchMan','FireMan','ThunderMan','ProtoMan','NumberMan','MetalMan','JunkMan','AquaMan','WoodMan','StarMan','ShadowMan','KnightMan','NapalmMan','IceMan','ElecMan','PlantMan','Bass']
        for a,portrait in zip(batch500am.SOURCES,portraits):
            asset=next(x for x in self.assets if x['archive']==a)
            units={u['id'].split(':',1)[1]:u for u in asset['units']}
            for s in range(6):
                self.assertEqual(units[str(s)+':0']['speaker'],'ui-label')
                self.assertIsNone(units[str(s)+':0']['origin_portrait'])
            for k in ('6:0','7:1','11:1','12:0','13:0'):
                self.assertEqual(units[k]['origin_portrait'],portrait)
            for k in ('8:0','9:0','10:1'):
                self.assertIsNone(units[k]['origin_portrait'])
                self.assertEqual(units[k]['speaker'],'speaker-unestablished')
            d=batch500am.DRAFT[a]
            self.assertIn('50',d['0:0']);self.assertIn('최대치',d['1:0'])
            self.assertIn('약한 바이러스',d['2:0']);self.assertIn('잠시',d['2:0'])
            self.assertIn('함정',d['3:0']);self.assertIn('쉬워진다',d['4:0'])
            self.assertIn('보안',d['5:0'])
        self.assertNotIn('나, 나',batch500am.DRAFT['6FA910']['6:0'])

    def test_batch500am_dynamic_items_choices_and_padding(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-039']
        choices=[u for a in aa for u in a['units'] if u['speaker']=='player-choice']
        self.assertEqual(len(choices),52)
        for a in aa[:21]:
            native=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertRegex(native,r'printItem\s+buffer = 1\s+item = 0')
            self.assertRegex(native,r'positionOptionHorizontal\s+width = 8')
            d=batch500am.DRAFT[a['archive']]
            self.assertTrue(d['7:1'].startswith('」\n'));self.assertTrue(d['7:1'].endswith('\n'))
            self.assertTrue(d['7:2'].endswith('  '))
            self.assertNotRegex(d['10:1'],r'^」 ?[을를]')
            self.assertTrue(all(u['origin_portrait'] is not None for u in a['units'] if u['speaker']=='player-choice'))
        for a in ('6FA0B8','6FA4E4'):
            self.assertTrue(batch500am.DRAFT[a]['6:0'].startswith(',\n'))
        npc=next(a for a in aa if a['archive']=='7A7000')
        self.assertEqual(sum(u['speaker']=='player-choice' for u in npc['units']),10)
        self.assertTrue(all(u['origin_portrait'] is None for u in npc['units'] if u['speaker']=='player-choice'))
        self.assertEqual(batch500am.DRAFT['7A7000']['84:2'],':\n「')

    def test_batch500am_last_three_progression_contexts(self):
        for a,p in [('78AAF0','ElecMan'),('78AE58','PlantMan'),('78B1C0','Bass')]:
            asset=next(x for x in self.assets if x['archive']==a)
            self.assertTrue(all(u['origin_portrait']==p for u in asset['units']))
            native=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig')
            blocks={int(m.group(1)):m.group(2) for m in re.finditer(r'script (\d+) \w+ \{(.*?)(?=\nscript |\Z)',native,re.S)}
            self.assertLess(blocks[10].index('bitmask = 4'),blocks[10].index('flag = 4270'))
            self.assertRegex(blocks[10],r'checkItem\s+item = 11\s+amount = 1\s+jumpIfEqual = 25')
            self.assertRegex(native,r'printChip\s+buffer = 0\s+chip = 104')
            self.assertRegex(blocks[27],r'checkSubArea\s+lower = 0\s+upper = 3\s+jumpIfInRange = 35')
            self.assertNotRegex(batch500am.DRAFT[a]['13:1'],r'^」 ?[을를]')
            for s,n in [(16,3),(18,5),(19,7),(20,9),(21,10),(22,12)]:
                self.assertIn('인터넷'+str(n),batch500am.DRAFT[a][str(s)+':0'])
            self.assertIn('인터넷9',batch500am.DRAFT[a]['25:0'])
        self.assertIn('MAX',batch500am.DRAFT['78AAF0']['29:0'])
        self.assertIn('꽃',batch500am.DRAFT['78AE58']['29:0'])
        self.assertIn('시시한 여흥',batch500am.DRAFT['78B1C0']['15:0'])
        bass_native=(ROOT/'analysis/full_scope_v1/source_tpl/78B1C0.tpl').read_text(encoding='utf-8-sig')
        bass33=re.search(r'script 33 \w+ \{(.*?)(?=\nscript |\Z)',bass_native,re.S).group(1)
        self.assertNotIn('print',bass33)
        self.assertFalse(batch500am.DRAFT['78B1C0']['33:0'].startswith(','))

    def test_batch500am_internet4_battle_trade_and_rumours(self):
        a=next(x for x in self.assets if x['archive']=='7A7000')
        native=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(native,r'checkNavi\s+navi = 5\s+jumpIfTrue = 38')
        self.assertRegex(native,r'checkNavi\s+navi = 15\s+jumpIfTrue = 39')
        self.assertRegex(native,r'checkTakeZenny\s+amount = 500\s+jumpIfAll = continue\s+jumpIfNone = 82\s+jumpIfSome = 82')
        self.assertRegex(native,r'itemGive\s+item = 5\s+amount = 1')
        self.assertRegex(native,r'checkItem\s+item = 5\s+amount = 1\s+jumpIfEqual = 83')
        d=batch500am.DRAFT['7A7000']
        self.assertIn('1명',d['38:2']);self.assertIn('3명',d['39:0'])
        self.assertIn('500제니',d['80:4']);self.assertIn('인터넷2',d['80:3'])
        self.assertIn('인터넷3',d['80:3']);self.assertIn('부족',d['82:0'])
        self.assertIn('살아날지도',d['53:2']);self.assertIn('정보가 있지만',d['52:0'])
        self.assertIn('참가 자격',d['10:1'])
        self.assertEqual(d['36:2'],'인!!')
        self.assertIn('그럴 리가',batch500am.DRAFT['7A6990']['0:2'])


    def test_batch500an_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-040']
        self.assertEqual([a['archive'] for a in aa],list(batch500an.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[42,45,306,16,33,5,3,27,1,22])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-285:-275],[v[2] for v in batch500an.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-8]
        self.assertEqual((b['id'],b['authored_literals'],b['battle_commands_escape'],b['bbs_reactions'],b['npcs']),('batch500-040',500,306,42,53))
        self.assertEqual((b['player_choices'],b['ui_labels']),(218,94))
        self.assertFalse(b['rom_applied'])
        self.assertEqual(batch500an.EXCLUDED,{'7097D8:0:0'})

    def test_batch500an_repro_codec_topology_and_exclusion(self):
        for a,(_,count,path) in batch500an.SOURCES.items():
            asset=batch500an.create(a)
            self.assertEqual(asset,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(asset)),count)
            self.assertFalse(asset['review']['release_eligible'])
            for u in asset['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for source,target in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(source)-len(source.lstrip(' ')),len(target)-len(target.lstrip(' ')))
        excluded=next(u for u in self.base.values() if u['id']=='7097D8:0:0')
        self.assertEqual(excluded['source'],'xうそメッセージです')
        self.assertNotIn('0:0',batch500an.DRAFT['7097D8'])

    def test_batch500an_bbs21_portraits_not_mail(self):
        a=next(x for x in self.assets if x['archive']=='704368')
        self.assertEqual(len(a['units']),42)
        self.assertEqual(len({u['origin_portrait'] for u in a['units']}),21)
        self.assertTrue(all(u['speaker']==u['origin_portrait'] for u in a['units']))
        d=batch500an.DRAFT['704368']
        self.assertIn('같',d['0:0']);self.assertIn('하나도',d['1:0'])
        self.assertIn('거스',d['11:0']);self.assertIn('퓨',d['20:0'])
        self.assertTrue(d['49:0'].startswith('흥...\n'))
        self.assertTrue(all('메일' not in u['translation'] for u in a['units']))
        native=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(native,r'positionText\s+left = 80\s+top = 60')
        self.assertIn('jumpIfBass = 49',native)

    def test_batch500an_battle_escape_and_options_preserved(self):
        a=next(x for x in self.assets if x['archive']=='766134')
        native=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        blocks={int(m.group(1)):m.group(2) for m in re.finditer(r'script (\d+) \w+ \{(.*?)(?=\nscript |\Z)',native,re.S)}
        d=batch500an.DRAFT['766134']
        self.assertEqual(sum(u['speaker']=='player-choice' for u in a['units']),212)
        self.assertEqual(sum(u['source']=='・' for u in a['units']),6)
        for s in (1,2):
            self.assertEqual(re.findall(r'frames = (\d+)',blocks[s]),['18']*4)
            for l in range(3):self.assertEqual(d[f'{s}:{l}'],'.')
        self.assertIn('도망쳤어',d['1:3']);self.assertIn('도망칠 수 없어',d['2:3'])
        self.assertIn('아니야',d['3:0']);self.assertIn('넷토',d['0:0'])
        self.assertIn('같은 줄',d['5:2']);self.assertIn('쫓아',d['5:1'])
        self.assertIn('돌풍',d['18:2']);self.assertIn('흡입',d['18:3'])
        self.assertEqual(d['34:1'],'실드\n');self.assertEqual(d['34:2'],'롱 소드\n')
        self.assertIn('BSeparate = true',blocks[6]);self.assertIn('disableB = true',blocks[7])
        self.assertRegex(blocks[4],r'positionOptionHorizontal\s+width = 8')
        self.assertRegex(blocks[5],r'positionOptionVertical\s+width = 13')
        for u in a['units']:
            if u['source']=='はい  ':self.assertEqual(u['translation'],'예  ')
        for s in (65,66,67,69,70,71,73,74,75,77,78,79,81,82,83,85,86,87,89,90,91,93,94,95):
            self.assertIn('mugshot = WoodMan',blocks[s])
            self.assertTrue(all(u['origin_portrait']=='WoodMan' for u in a['units'] if u['id'].split(':')[1]==str(s)))
        self.assertEqual(d['94:2'],'데스 포레스트\n')
        self.assertIn('mugshot = Bass',blocks[92])

    def test_batch500an_labels_and_player_hp_suffix(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-040']
        labels=[u for a in aa for u in a['units'] if u['speaker']=='ui-label']
        self.assertEqual(len(labels),94);self.assertTrue(all(u['origin_portrait'] is None for u in labels))
        d=batch500an.DRAFT
        self.assertEqual(d['7097D8']['19:0'],'의 HP')
        self.assertEqual(d['7097D8']['12:0'],'인터넷12')
        self.assertEqual(d['7097D8']['36:0'],'공장의 전뇌4')
        self.assertEqual(d['768764']['11:0'],'수도관1')
        self.assertEqual(d['768764']['12:0'],'수도관')
        self.assertEqual(d['768764']['13:0'],'수도관2')
        self.assertEqual(d['778B08']['11:0'],'마이너스키')
        self.assertEqual(d['778B08']['14:0'],'합격 데이터C')
        self.assertEqual(d['778B08']['37:0'],'레귤러UP3')

    def test_batch500an_gate_dynamic_item_and_success_flag(self):
        a=next(x for x in self.assets if x['archive']=='79C1D8')
        native=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertTrue(all(u['origin_portrait'] is None for u in a['units']))
        self.assertRegex(native,r'checkItem\s+item = 3\s+amount = 1')
        self.assertRegex(native,r'printItem\s+buffer = 0\s+item = 3')
        self.assertRegex(native,r'flagSetNavi\s+flag = 1713')
        self.assertEqual(batch500an.DRAFT['79C1D8']['0:2'],':\n「')
        self.assertEqual(batch500an.DRAFT['79C1D8']['0:3'],'」\n제시했다!!')
        self.assertIn('물러가라',batch500an.DRAFT['79C1D8']['1:1'])

    def test_batch500an_npc_wind_virus_and_classroom(self):
        wind=next(x for x in self.assets if x['archive']=='7A82D8')
        native=(ROOT/wind['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(native,r'checkNavi\s+navi = 3\s+jumpIfTrue = 54')
        self.assertRegex(native,r'global = 24\s+value = 131')
        self.assertRegex(native,r'global = 27\s+value = 1788')
        self.assertEqual(sum(u['speaker']=='player-choice' for u in wind['units']),4)
        self.assertTrue(all(u['origin_portrait'] is None for u in wind['units'] if u['speaker']=='player-choice'))
        d=batch500an.DRAFT
        self.assertIn('인터넷8',d['7A82D8']['0:1']);self.assertIn('인터넷7',d['7A82D8']['1:0'])
        self.assertIn('맞바람',d['7A82D8']['52:0'])
        self.assertIn('인적',d['7A8218']['0:1']);self.assertNotIn('인기',d['7A8218']['0:1'])
        npc=next(x for x in self.assets if x['archive']=='7AF3E8')
        nt=(ROOT/npc['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertRegex(nt,r'global = 24\s+value = 164')
        self.assertRegex(nt,r'global = 28\s+value = 1')
        self.assertIn('수소 원자2개',d['7AF3E8']['10:1']);self.assertIn('산소 원자1개',d['7AF3E8']['10:1'])
        self.assertEqual(d['7AF3E8']['13:2'],'혹시, 수면 학습?')
        self.assertIn('1등',d['7AF3E8']['13:1'])


    def test_batch500ao_exact500_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-041']
        self.assertEqual([a['archive'] for a in aa],list(batch500ao.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[81,46,278,23,4,7,27,5,29])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-275:-266],[v[2] for v in batch500ao.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-7]
        self.assertEqual((b['id'],b['authored_literals'],b['minigame_explanations'],b['busting_tutorial'],b['battle_target_range_escape'],b['npcs_everyday_tournament']),('batch500-041',500,81,46,278,95))
        self.assertEqual((b['player_choices'],b['ui_labels'],b['split_wait_dots']),(58,38,126))
        self.assertFalse(b['rom_applied'])
        self.assertEqual(batch500ao.EXCLUDED,{'71BE98:2:0'})

    def test_batch500ao_repro_codec_topology_and_exclusion(self):
        for a,(_,count,path) in batch500ao.SOURCES.items():
            asset=batch500ao.create(a)
            self.assertEqual(asset,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(asset)),count)
            self.assertFalse(asset['review']['release_eligible'])
            for u in asset['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for source,target in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(source)-len(source.lstrip(' ')),len(target)-len(target.lstrip(' ')))
        self.assertNotIn('2:0',batch500ao.DRAFT['71BE98'])
        self.assertIn('ネオバリアブル',self.base['71BE98:2:0']['source'])
        self.assertEqual(self.base['71BE98:2:0']['status'],'unselected_japanese')

    def test_batch500ao_minigame_thresholds_reward_and_routes(self):
        a=next(x for x in self.assets if x['archive']=='71BE98')
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertTrue(all(u['origin_portrait'] is None for u in a['units']))
        self.assertEqual(sum(u['speaker']=='player-choice' for u in a['units']),10)
        self.assertRegex(nt,r'flag = 6452\s+jumpIfTrue = 6')
        self.assertRegex(nt,r'checkNavi\s+navi = 19\s+jumpIfTrue = 7')
        self.assertRegex(nt,r'printBuffer\s+buffer = 3')
        self.assertRegex(nt,r'checkGiveZenny\s+amount = 4294967295')
        d=batch500ao.DRAFT['71BE98']
        self.assertIn('1체',d['1:3']);self.assertIn('1 줄어',d['1:3'])
        self.assertIn('0',d['1:4']);self.assertIn('3번',d['1:20'])
        self.assertIn('강제로',d['1:21']);self.assertIn('3장',d['1:27'])
        self.assertIn('1번',d['1:30']);self.assertIn('3체 이상',d['1:30'])
        self.assertIn('1턴',d['1:32']);self.assertIn('1카운트',d['1:32'])
        self.assertIn('3줄',d['1:36']);self.assertIn('9개',d['1:37'])
        self.assertIn('다음 턴',d['1:18']);self.assertIn('다음 턴',d['1:19'])
        self.assertIn('감염되어',d['6:2']);self.assertIn('것 같아요',d['7:6'])
        self.assertTrue(d['0:3'].endswith('\n'));self.assertEqual(d['1:42'],'응\n')

    def test_batch500ao_tutorial_button_roles_gauge_and_portrait(self):
        a=next(x for x in self.assets if x['archive']=='768BD0')
        self.assertTrue(all(u['origin_portrait']=='MrProgGold' for u in a['units']))
        d=batch500ao.DRAFT['768BD0']
        self.assertIn('조작할 수는 없습니다',d['0:5'])
        self.assertIn('알아서 움직',d['0:6'])
        self.assertIn('R버튼',d['3:0']);self.assertIn('설명',d['3:0'])
        self.assertIn('L버튼',d['3:1']);self.assertIn('반드시',d['3:1'])
        self.assertIn('R버튼',d['6:2']);self.assertIn('L버튼',d['6:2'])
        self.assertIn('노란색',d['10:0']);self.assertIn('파란색',d['11:0'])
        self.assertIn('빨간색',d['12:0']);self.assertIn('가득',d['12:0'])
        self.assertIn('처음에는 노란색',d['7:4'])
        self.assertIn('무작위',d['9:0']);self.assertIn('A버튼',d['13:1'])
        self.assertIn('B버튼',d['13:2']);self.assertIn('줄어듭니다',d['13:3'])
        self.assertIn('위',d['14:1']);self.assertIn('아래',d['14:2'])
        self.assertIn('되도록',d['5:1'])

    def test_batch500ao_battle_shortlabels_dots_and_source_dispatch(self):
        a=next(x for x in self.assets if x['archive']=='76C944')
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        blocks={int(m.group(1)):m.group(2) for m in re.finditer(r'script (\d+) \w+ \{(.*?)(?=\nscript |\Z)',nt,re.S)}
        self.assertEqual(sum(u['speaker']=='ui-label' for u in a['units']),38)
        self.assertEqual(sum(u['speaker']=='player-choice' for u in a['units']),38)
        self.assertEqual(sum(u['source']=='・' for u in a['units']),126)
        for u in a['units']:
            if u['source']=='・':self.assertEqual(u['translation'],'.')
            if u['speaker']=='ui-label':self.assertIsNone(u['origin_portrait'])
            if u['source']=='はい  ':self.assertEqual(u['translation'],'예  ')
        for s in [3,4,9,10]+[n+j for n in list(range(12,78,6))+list(range(90,138,6)) for j in (3,4)]:
            self.assertEqual(re.findall(r'frames = (\d+)',blocks[s]),['18']*4)
        self.assertIn('jumpIfBass = 138',blocks[138])
        self.assertIn('jumpIfBass = 143',blocks[143])
        d=batch500ao.DRAFT['76C944']
        self.assertNotIn('2:0',d);self.assertNotIn('8:0',d)
        self.assertIn('가로막히',d['100:3']);self.assertIn('가로막혔',d['112:3'])
        self.assertIn('목숨',d['137:0']);self.assertIn('거츠',d['16:3'])
        self.assertIn('퓨',d['69:3']);self.assertIn('꽃',d['126:0'])

    def test_batch500ao_everyday_hours_variables_entry_and_cancel(self):
        a=next(x for x in self.assets if x['archive']=='79C8F8')
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(re.findall(r'lowerHour = (\d+)',nt),['9','13','16','20'])
        self.assertEqual(re.findall(r'upperMinutes = (\d+)',nt),['59']*4)
        self.assertRegex(nt,r'printItem\s+buffer = 0\s+item = 7')
        self.assertRegex(nt,r'checkFlagNavi\s+flag = 1906\s+jumpIfTrue = 4')
        self.assertRegex(nt,r'flag = 7736\s+callTournament\s+tournament = 6')
        self.assertEqual(sum(u['speaker']=='player-choice' for u in a['units']),2)
        d=batch500ao.DRAFT['79C8F8']
        self.assertTrue(d['0:0'].endswith('\n「'))
        self.assertIn('강함',d['2:3']);self.assertIn('아니야',d['2:2'])
        self.assertEqual(d['4:4'],'PM4:00~PM5:00\nPM8:00~PM9:00\n이야!!')

    def test_batch500ao_npc_portrait_switch_and_battle_voice(self):
        merchant=next(x for x in self.assets if x['archive']=='7A89E4')
        u={x['id'].split(':',1)[1]:x for x in merchant['units']}
        self.assertEqual(u['1:0']['origin_portrait'],'NaviGirlOrange')
        self.assertEqual(u['1:1']['origin_portrait'],'PurpleNavi')
        self.assertEqual(u['3:0']['origin_portrait'],'NormalNaviYellow')
        d=batch500ao.DRAFT
        self.assertIn('수요일',d['7A89E4']['3:0'])
        self.assertIn('100만 광년',d['7A8B9C']['3:0'])
        self.assertIn('미, 자신감',d['7A8B9C']['7:1'])
        self.assertIn('갈비뼈',d['7A8B9C']['4:0'])
        self.assertIn('세대',d['7ADD74']['8:0'])
        self.assertIn('체력이',d['7ADD74']['9:1'])
        self.assertIn('나무 속성',d['7A9AC0']['1:1'])
        self.assertIn('범죄 예방',d['7A9AC0']['0:2'])
        for arc,expected in [('7A8B9C',['156','157']),('7ADD74',['162','163'])]:
            a=next(x for x in self.assets if x['archive']==arc)
            nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertEqual(re.findall(r'global = 24\s+value = (\d+)',nt),expected)
            self.assertEqual(sum(x['speaker']=='player-choice' for x in a['units']),4)


    def test_batch500ap_exact500_scope_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-042']
        self.assertEqual([a['archive'] for a in aa],list(batch500ap.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[482,4,8,5,1])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-266:-261],[v[2] for v in batch500ap.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-6]
        self.assertEqual((b['id'],b['authored_literals'],b['tournament_awards_roulette_interviews'],b['npcs']),('batch500-042',500,482,18))
        self.assertEqual((b['player_choices'],b['ui_labels'],b['split_wait_dots']),(0,3,6))
        self.assertFalse(b['rom_applied'])
        self.assertEqual(batch500ap.EXCLUDED,{'6EAD18:10:0'})

    def test_batch500ap_repro_codec_topology_unselected(self):
        for arc,(_,count,path) in batch500ap.SOURCES.items():
            a=batch500ap.create(arc)
            self.assertEqual(a,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(a)),count)
            self.assertFalse(a['review']['release_eligible'])
            for u in a['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for src,dst in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(src)-len(src.lstrip(' ')),len(dst)-len(dst.lstrip(' ')))
        self.assertNotIn('10:0',batch500ap.DRAFT['6EAD18'])
        self.assertEqual(self.base['6EAD18:10:0']['source'],' ヘ')
        self.assertEqual(self.base['6EAD18:10:0']['status'],'unselected_japanese')
        self.assertTrue(all(int(k.split(':')[0])<=77 for k in batch500ap.DRAFT['6EAD18']))

    def test_batch500ap_awards_tickets_and_conditional_routes(self):
        a=batch500ap.create('6EAD18')
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for item in (2,3,4,19,20):self.assertIn('item = '+str(item),nt)
        for flag in (7727,7729):self.assertIn('flag = '+str(flag),nt)
        self.assertIn('wait\n\t\tframes = 60',nt)
        d=batch500ap.DRAFT['6EAD18']
        for script in (4,12):
            self.assertIn('1회만',d[f'{script}:7'])
            self.assertIn('1번 플러그아웃',d[f'{script}:8'])
            self.assertIn('다시 닫히니',d[f'{script}:9'])
        uu={u['id'].split(':',1)[1]:u for u in a['units']}
        self.assertEqual(uu['0:0']['origin_portrait'],'Ribitta')
        self.assertEqual(uu['0:4']['origin_portrait'],'MrProgGold')
        self.assertEqual(uu['0:12']['origin_portrait'],'Ribitta')
        self.assertEqual(uu['48:0']['origin_portrait'],'Bass')
        self.assertEqual(uu['48:1']['origin_portrait'],'HeelNaviBlack')
        self.assertTrue(all(uu[k]['speaker']=='ui-label' for k in ('5:0','6:0','8:0')))

    def test_batch500ap_roulette_timing_inherited_host_and_rating(self):
        a=batch500ap.create('6EAD18')
        u={x['id'].split(':',1)[1]:x for x in a['units']}
        for script in (18,19,20,21,22):
            self.assertEqual(u[f'{script}:0']['speaker'],'Ribitta')
            self.assertIsNone(u[f'{script}:0']['origin_portrait'])
        for script in (53,54,55,56,57):
            self.assertEqual(u[f'{script}:0']['speaker'],'HeelNaviBlack')
            self.assertIsNone(u[f'{script}:0']['origin_portrait'])
        d=batch500ap.DRAFT['6EAD18']
        self.assertIn('A 버튼',d['16:0']);self.assertIn('A 버튼',d['51:0'])
        self.assertIn('조금만 더',d['17:1']);self.assertIn('아직',d['18:1'])
        self.assertIn('그럭저럭',d['19:1']);self.assertIn('꽤 좋은',d['20:1'])
        self.assertIn('정말 기쁘',d['21:1'])
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('textSpeed\n\t\tdelay = 0',nt);self.assertIn('waitHold',nt)

    def test_batch500ap_interview_portrait_switches_defined_variables(self):
        a=batch500ap.create('6EAD18')
        u={x['id'].split(':',1)[1]:x for x in a['units']}
        for s,portrait,index in [(65,'MegaMan',3),(66,'Roll',3),(67,'GutsMan',3),(68,'WindMan',3),(69,'SearchMan',3),(70,'FireMan',3),(71,'ThunderMan',3),(72,'ProtoMan',3),(73,'NumberMan',3),(74,'MetalMan',4),(75,'JunkMan',4),(76,'AquaMan',3),(77,'WoodMan',4)]:
            self.assertEqual(u[f'{s}:0']['origin_portrait'],'Ribitta')
            self.assertEqual(u[f'{s}:{index}']['origin_portrait'],portrait)
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for command in ('printPlayerName','printPlayerNickname','printCurrentNavi','printFavFood','printCrush','printSchool','printHobby','printDream','printFriend','printWish','printBestSubject','printWorstSubject','printFavShow','printPlayerEnemy'):
            self.assertIn(command,nt)
        for target in range(90,103):self.assertIn('jumpIfUndefined = '+str(target),nt)
        d=batch500ap.DRAFT['6EAD18']
        self.assertIn('짝사랑',d['66:14']);self.assertIn('공개',d['66:16'])
        self.assertIn('작전대로',d['69:14']);self.assertIn('오퍼레이션이었습니다',d['69:19'])
        self.assertIn('두뇌',d['73:7']);self.assertIn('허세',d['73:17'])
        self.assertIn('질투',d['75:19']);self.assertIn('방송',d['76:17'])
        self.assertIn('자연',d['77:11'])

    def test_batch500ap_bass_responses_and_native_anomalies(self):
        d=batch500ap.DRAFT['6EAD18']
        self.assertIn('오퍼레이터가 있는',d['3:0'])
        self.assertIn('없어도',d['47:0'])
        self.assertIn('살아남아라',d['48:0'])
        a=batch500ap.create('6EAD18');u={x['id'].split(':',1)[1]:x for x in a['units']}
        for s in (38,39):
            self.assertEqual(u[f'{s}:0']['origin_portrait'],'MegaMan')
            self.assertIn('푸른 불꽃',d[f'{s}:1'])
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for s in (69,73):
            body=re.search(r'script '+str(s)+r' mmbn45 \{(.*?)(?=\nscript |\Z)',nt,re.S).group(1)
            self.assertEqual(body.count('waitSkip\n\t\tframes = 30'),3)
            indices=(30,31,32) if s==69 else (12,13,14)
            self.assertEqual([d[f'{s}:{i}'] for i in indices],['.','.','.'])

    def test_batch500ap_npc_distinct_portraits_time_and_aspirations(self):
        for arc in ('7A6778','7A685C'):
            a=batch500ap.create(arc)
            self.assertTrue(all(u['origin_portrait']=='HeelNaviBlack' for u in a['units']))
            nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertIn('upperHour = 28',nt)
        d=batch500ap.DRAFT
        self.assertIn('쓰레기',d['7A685C']['0:1'])
        self.assertIn('벗어나고',d['7A685C']['1:2'])
        a=batch500ap.create('7A7E1C');u={x['id'].split(':',1)[1]:x for x in a['units']}
        self.assertEqual(u['0:0']['origin_portrait'],'NaviGirlOrange')
        self.assertEqual(u['1:0']['origin_portrait'],'NormalNaviPink')
        self.assertEqual(u['2:0']['origin_portrait'],'NormalNaviYellow')
        self.assertIn('수요일',d['7A7E1C']['2:0'])
        self.assertIn('맨즈 데이',d['7A7E1C']['2:1'])
        self.assertEqual(batch500ap.create('7A9954')['units'][0]['origin_portrait'],'MrProgGreen')


    def test_batch500aq_exact500_scope_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-043']
        self.assertEqual([a['archive'] for a in aa],list(batch500aq.SOURCES))
        self.assertEqual([len(a['units']) for a in aa],[377,27,29,45,5,8,7,2])
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-261:-253],[v[2] for v in batch500aq.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-5]
        self.assertEqual((b['id'],b['authored_literals'],b['player_choices'],b['ui_labels'],b['split_wait_dots']),('batch500-043',500,20,10,15))
        self.assertFalse(b['rom_applied'])
        self.assertEqual(batch500aq.EXCLUDED,{'6EAD18:10:0','71A37C:2:0'})

    def test_batch500aq_repro_codec_topology_and_exclusions(self):
        for arc,(_,count,path) in batch500aq.SOURCES.items():
            a=batch500aq.create(arc)
            self.assertEqual(a,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(a)),count)
            self.assertFalse(a['review']['release_eligible'])
            for u in a['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for src,dst in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(src)-len(src.lstrip(' ')),len(dst)-len(dst.lstrip(' ')))
        for k in batch500aq.EXCLUDED:
            self.assertEqual(self.base[k]['status'],'unselected_japanese')
            self.assertNotIn(k.split(':',1)[1],batch500aq.DRAFT[k.split(':')[0]])

    def test_batch500aq_native_interview_portraits_and_inherited_routes(self):
        a=batch500aq.create('6EAD18');u={x['id'].split(':',1)[1]:x for x in a['units']}
        for s,p,i in [(78,'StarMan',4),(79,'ShadowMan',4),(80,'KnightMan',3),(81,'NapalmMan',3),(82,'IceMan',4),(83,'ElecMan',5),(84,'PlantMan',4),(85,'Bass',5)]:
            self.assertEqual(u[f'{s}:0']['origin_portrait'],'Ribitta')
            self.assertEqual(u[f'{s}:{i}']['origin_portrait'],p)
        self.assertEqual(u['86:3']['origin_portrait'],'Ribitta')
        for s,p in [(90,'MegaMan'),(91,'Roll'),(93,'WindMan'),(94,'SearchMan'),(95,'FireMan'),(96,'ThunderMan'),(98,'NumberMan'),(99,'MetalMan'),(100,'JunkMan'),(101,'AquaMan'),(102,'WoodMan'),(103,'StarMan'),(104,'ShadowMan'),(105,'KnightMan'),(106,'NapalmMan'),(107,'IceMan'),(110,'Bass')]:
            self.assertEqual(u[f'{s}:0']['speaker'],p)
            self.assertIsNone(u[f'{s}:0']['origin_portrait'])
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for target in range(90,111):self.assertIn('jumpIfUndefined = '+str(target),nt)
        for command in ('printPlayerNickname','printCurrentNavi','printFriend','printFavFood','printSchool','printHobby'):self.assertIn(command,nt)
        self.assertIn('flag = 7729',nt)

    def test_batch500aq_distinct_profile_fallback_meanings(self):
        d=batch500aq.DRAFT['6EAD18']
        self.assertIn('약속',d['78:18']);self.assertIn('대청소',d['103:0'])
        self.assertIn('암살',d['79:17']);self.assertIn('표적',d['104:0'])
        self.assertIn('1일 3회',d['80:10']);self.assertIn('규칙적인',d['105:0'])
        self.assertIn('목욕',d['84:14']);self.assertIn('채소 주스',d['109:0'])
        self.assertIn('같은 활동',d['82:16']);self.assertIn('인터넷',d['107:0'])
        self.assertIn('바이러스',d['110:0']);self.assertIn('내비를 바꾼',d['98:6'])
        self.assertIn('허세',d['98:8']);self.assertIn('밥이 식어',d['101:2'])
        self.assertIn('짜릿',d['83:6']);self.assertIn('미션 컴플리트',d['94:13'])

    def test_batch500aq_training_choices_and_preserved_controls(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-043']
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),20)
        self.assertEqual(sum(x['speaker']=='ui-label' for x in u.values()),10)
        for k in batch500aq.CHOICES:self.assertEqual(u[k]['speaker'],'player-choice')
        for k in batch500aq.LABELS:self.assertEqual(u[k]['speaker'],'ui-label')
        a=batch500aq.create('71A37C');nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('flag = 5569','flag = 5570','width = 13','width = 8','disableB = true','jump = 1'):self.assertIn(token,nt)
        d=batch500aq.DRAFT['71A37C']
        self.assertIn('B 버튼',d['1:3']);self.assertIn('공격 범위',d['1:7'])
        self.assertIn('3개',d['1:9']);self.assertIn('1개',d['1:10'])
        self.assertIn('3번',d['1:11']);self.assertIn('부수지 않고',d['1:14'])

    def test_batch500aq_battle_dots_inherited_voice_and_hp_narration(self):
        d=batch500aq.DRAFT
        for arc,s,indices in [('775E90',3,(0,1,2)),('775E90',4,(0,1,2)),('775E90',50,(0,1,2)),('6EAD18',94,(9,10,11)),('6EAD18',98,(3,4,5))]:
            self.assertEqual([d[arc][f'{s}:{i}'] for i in indices],['.']*3)
        a=batch500aq.create('775E90');u={x['id'].split(':',1)[1]:x for x in a['units']}
        for s in (15,16):
            self.assertEqual(u[f'{s}:0']['speaker'],'MegaMan')
            self.assertIsNone(u[f'{s}:0']['origin_portrait'])
        self.assertIn('칩 게이트',d['775E90']['15:0']);self.assertIn('저장',d['775E90']['16:0'])
        self.assertEqual(d['775E90']['47:0'],'버그 조각 ')
        a=batch500aq.create('776198');u={x['id'].split(':',1)[1]:x for x in a['units']}
        for s in (3,7,11,15):
            self.assertEqual(u[f'{s}:0']['speaker'],'system-reward')
            self.assertIsNone(u[f'{s}:0']['origin_portrait'])
            self.assertIn('50pts',u[f'{s}:0']['translation'])
        for s,p in [(17,'KnightMan'),(18,'Bass'),(19,'GutsMan')]:self.assertEqual(u[f'{s}:0']['origin_portrait'],p)
        self.assertIn('10PTS',d['776198']['19:0'])
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(nt.count('flag = 7726'),7)
        self.assertEqual(nt.count('printChip'),5)

    def test_batch500aq_legacy_plugin_ui_npc_and_native_hour(self):
        d=batch500aq.DRAFT
        self.assertEqual(d['7782A8']['0:1'],'\n록맨.EXE,')
        self.assertEqual(d['778C6C']['7:0'],'언더T')
        a=batch500aq.create('7782A8');nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('controlLock',nt);self.assertIn('flag = 7710',nt)
        a=batch500aq.create('7A6A68');nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('lowerHour = 12',nt);self.assertIn('upperHour = 28',nt)
        self.assertTrue(all(x['origin_portrait']=='HeelNaviBlack' for x in a['units']))
        self.assertIn('닌자',d['7A6A68']['1:3'])
        self.assertTrue(d['7A7B74']['0:1'].endswith('?'))


    def test_batch500ar_exact500_scope_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-044']
        self.assertEqual([a['archive'] for a in aa],list(batch500ar.SOURCES))
        self.assertEqual(len(aa),67)
        self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-253:-186],[v[2] for v in batch500ar.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-4]
        self.assertEqual((b['id'],b['authored_literals'],b['timed_voice_literals']),('batch500-044',500,40))
        self.assertFalse(b['rom_applied'])
        self.assertEqual((b['player_choices'],b['ui_labels']),(0,0))

    def test_batch500ar_repro_codec_topology_exclusions(self):
        for arc,(_,count,path) in batch500ar.SOURCES.items():
            a=batch500ar.create(arc)
            self.assertEqual(a,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(a)),count)
            self.assertFalse(a['review']['release_eligible'])
            for u in a['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for src,dst in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(src)-len(src.lstrip(' ')),len(dst)-len(dst.lstrip(' ')))
        for k in batch500ar.EXCLUDED:
            self.assertEqual(self.base[k]['source'],'かりです')
            self.assertEqual(self.base[k]['status'],'unselected_japanese')
            self.assertNotIn(k.split(':',1)[1],batch500ar.DRAFT[k.split(':')[0]])

    def test_batch500ar_quick_alerts_and_explicit_portraits(self):
        for arc,portrait in [('682504','ProtoMan'),('68DD98','MetalMan'),('698CFC','AquaMan'),('69E708','WoodMan')]:
            a=batch500ar.create(arc)
            for u in a['units']:
                s=int(u['id'].split(':')[1])
                self.assertEqual(u['origin_portrait'],portrait if s>=21 else None)
                self.assertEqual(u['speaker'],portrait if s>=21 else 'speaker-unestablished')
        for arc in ('66B8B0','670DF4','676AE4','67C4CC','681AB8','68D3C8','69303C','69E088'):
            self.assertTrue(all(u['origin_portrait'] is None for u in batch500ar.create(arc)['units']))

    def test_batch500ar_aqua_separate_timed_voice_beats(self):
        a=batch500ar.create('698CFC')
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertEqual(nt.count('waitSkip\n\t\tframes = 30'),30)
        d=batch500ar.DRAFT['698CFC']
        for s in (1,2,3,4,5,21,22,23,24,25):
            self.assertEqual([d[f'{s}:{i}'] for i in range(4)],['퓨,','퓨,','퓨,','\n퓨~~~!'])
        self.assertEqual(sum(v in ('퓨,','\n퓨~~~!') for v in d.values()),40)

    def test_batch500ar_reward_controls_and_sentinel(self):
        for arc in ('6770B8','682054','698A2C'):
            a=batch500ar.create(arc)
            nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for token in ('variable = 5','value = 0','value = 1','value = 2','value = 3','item = 33','amount = 4294967295','buffer = 3'):
                self.assertIn(token,nt)
        d=batch500ar.DRAFT['682054']
        self.assertIn('문제집',d['52:1']);self.assertIn('문제집',d['53:1'])
        self.assertIn('분입니다',d['12:1'])
        nt=(ROOT/batch500ar.create('682054')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('callProtoManMissionComplete','flag = 5475','flag = 5476','flag = 3613'):
            self.assertIn(token,nt)

    def test_batch500ar_mail_flags_and_timing(self):
        for arc in ('677774','67CED8','6827F8','699194'):
            a=batch500ar.create(arc)
            nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for token in ('track = 155','frames = 96','flag = 680','flag = 681','callTournamentReceiveMail'):
                self.assertIn(token,nt)
            self.assertTrue(all(u['origin_portrait'] is None for u in a['units']))
        nt=(ROOT/batch500ar.create('6827F8')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('flag = 3613',nt);self.assertIn('flag = 3783',nt)

    def test_batch500ar_schedule_numeric_and_dynamic_padding(self):
        for arc in ('677E58','67D5F8','682F44','688900','68E7BC','6941DC','6998DC','69F11C'):
            nt=(ROOT/batch500ar.create(arc)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for token in ('callFindSoonEvent','callFindTodayEvent','callBufferEventAMPM','padZeros = true'):
                self.assertIn(token,nt)
        self.assertIn('99.9',batch500ar.DRAFT['675338']['2:1'])
        self.assertTrue(any('98' in v for v in batch500ar.DRAFT['67593C'].values()))


    def test_batch500as_exact500_scope_and_authority(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-045']
        self.assertEqual([a['archive'] for a in aa],list(batch500as.SOURCES))
        self.assertEqual(len(aa),76);self.assertEqual(sum(len(a['units']) for a in aa),500)
        self.assertEqual(self.plan['draft_assets'][-186:-110],[v[2] for v in batch500as.SOURCES.values()])
        b=self.plan['batch_policy']['completed_batches'][-3]
        self.assertEqual((b['id'],b['authored_literals'],b['navi_mail_folder'],b['npcs']),('batch500-045',500,366,134))
        self.assertEqual((b['player_choices'],b['ui_labels'],b['mail_labels']),(4,91,90))
        self.assertFalse(b['rom_applied'])

    def test_batch500as_repro_codec_topology_exclusions(self):
        for arc,(_,count,path) in batch500as.SOURCES.items():
            a=batch500as.create(arc)
            self.assertEqual(a,json.loads((ROOT/path).read_text(encoding='utf8')))
            self.assertEqual(len(self.validate(a)),count)
            self.assertFalse(a['review']['release_eligible'])
            for u in a['units']:
                self.assertEqual(u['state'],'needs_review')
                self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
                self.assertEqual(u['source'].startswith('\n'),u['translation'].startswith('\n'))
                self.assertEqual(u['source'].endswith('\n'),u['translation'].endswith('\n'))
                self.assertEqual(len(u['source'])-len(u['source'].rstrip(' ')),len(u['translation'])-len(u['translation'].rstrip(' ')))
                for src,dst in zip(u['source'].split('\n'),u['translation'].split('\n')):
                    self.assertEqual(len(src)-len(src.lstrip(' ')),len(dst)-len(dst.lstrip(' ')))
        self.assertEqual(batch500as.EXCLUDED,{'6BC0C8:0:0','79C240:1:0'})
        for k in batch500as.EXCLUDED:
            self.assertEqual(self.base[k]['status'],'unselected_japanese')
            self.assertNotIn(k.split(':',1)[1],batch500as.DRAFT[k.split(':')[0]])
        self.assertNotIn('79C8D8',batch500as.SOURCES)

    def test_batch500as_mail_labels_and_registration_flow(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-045']
        u={x['id']:x for a in aa for x in a['units']}
        self.assertEqual(sum(x['speaker']=='ui-label' for x in u.values()),91)
        self.assertEqual(sum(x['speaker']=='player-choice' for x in u.values()),4)
        for k in batch500as.LABELS:self.assertEqual(u[k]['speaker'],'ui-label')
        for k in batch500as.CHOICES:self.assertEqual(u[k]['speaker'],'player-choice')
        for arc in ('6DD63C','6DD718','6DD798','6DD804','6DD91C'):
            self.assertTrue(all(x['speaker']=='ui-label' for x in batch500as.create(arc)['units']))
        d=batch500as.DRAFT
        self.assertEqual(d['6DD718']['66:0'],'삭제됨')
        self.assertEqual(d['6DD798']['59:0'],'제목 없음')
        self.assertEqual(d['6DD804']['57:0'],'보수')
        self.assertEqual(u['6DE2C8:31:0']['speaker'],'SciLabMan')
        self.assertIsNone(u['6DE2C8:31:0']['origin_portrait'])
        self.assertEqual(u['6DE2C8:33:0']['speaker'],'speaker-unestablished')
        for s in range(1,6):
            self.assertEqual(d['6DE2C8'][f'{s}:0'],'의 참가를\n')
            self.assertEqual(d['6DE2C8'][f'{s}:1'],'에서\n등록을 접수하였습니다')
        nt=(ROOT/batch500as.create('6DE2C8')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('printBufferedNavi',nt);self.assertIn('printTournament',nt)

    def test_batch500as_ice_quick_portraits_and_aqua_folder(self):
        a=batch500as.create('6C2368')
        for u in a['units']:
            s=int(u['id'].split(':')[1])
            self.assertEqual(u['origin_portrait'],'IceMan' if s>=21 else None)
        a=batch500as.create('6E2B9C');u={x['id'].split(':',1)[1]:x for x in a['units']}
        for s in (60,61,62):self.assertIsNone(u[f'{s}:0']['origin_portrait'])
        for s in range(70,76):self.assertEqual(u[f'{s}:0']['origin_portrait'],'AquaMan')
        d=batch500as.DRAFT['6E2B9C']
        self.assertIn('R 버튼',d['61:0']);self.assertIn('L 버튼',d['62:0'])
        for k,n in [('71:0','3'),('72:0','1'),('73:0','1'),('74:0','5'),('75:0','1')]:self.assertIn(n,d[k])
        self.assertEqual(d['70:3'],'예  ')
        nt=(ROOT/a['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('width = 8','buffer = 1','default = 0','callSkipMugshotFadeIn'):
            self.assertIn(token,nt)

    def test_batch500as_mail_missions_reward_sentinel_and_schedule(self):
        nt=(ROOT/batch500as.create('6BC0C8')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('variable = 5','value = 0','value = 1','value = 2','value = 3','minigame = 2','item = 33','amount = 1','amount = 4294967295','buffer = 3'):self.assertIn(token,nt)
        for arc in ('6AAEB0','6BC74C'):
            nt=(ROOT/batch500as.create(arc)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for token in ('track = 155','frames = 96','flag = 680','flag = 681','flag = 3613'):self.assertIn(token,nt)
        nt=(ROOT/batch500as.create('6BC74C')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('callNapalmManMissionBegin',nt);self.assertIn('callNapalmManMissionReceiveMail',nt)
        for arc in ('6A570C','6BCEB4','6C2D3C'):
            nt=(ROOT/batch500as.create(arc)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            for token in ('callFindSoonEvent','callFindTodayEvent','callBufferEventAMPM','padZeros = true'):self.assertIn(token,nt)
            self.assertEqual(batch500as.DRAFT[arc]['11:2'],' 부터\n')

    def test_batch500as_npc_portrait_switches_and_fictional_law(self):
        for arc,k,p in [('7A9BA0','0:0','NaviGirlOrange'),('7A9BA0','0:1','HeelNaviPurple'),('7A9BA0','1:2','NaviGirlOrange'),('7AAD84','0:2','NormalNaviYellow'),('7AAD84','0:3','NaviGirlOrange'),('7ADA60','0:0','OfficialNavi'),('7ADA60','0:2','HeelNaviPurple'),('7ADA60','1:3','OfficialNavi')]:
            u={x['id'].split(':',1)[1]:x for x in batch500as.create(arc)['units']}
            self.assertEqual(u[k]['origin_portrait'],p)
        d=batch500as.DRAFT
        self.assertIn('제123조',d['7AABB0']['0:3'])
        self.assertIn('불법 투기',d['7AABB0']['0:4'])
        self.assertIn('남자 친구',d['7AAD84']['2:0'])
        self.assertIn('인터넷11',d['7AD978']['0:0'])
        self.assertIn('재활용',d['7A99C0']['1:1'])
        self.assertIn('지난주',d['7ADA60']['1:1'])
        self.assertIn('1초 1초',d['7AB420']['0:1'])
        self.assertIn('1일',d['7AB420']['0:1'])

    def test_batch500as_star_wordplay_gate_and_tournament(self):
        d=batch500as.DRAFT
        self.assertIn('6등성',d['6A3D48']['2:1'])
        self.assertIn('검은 별',d['6A907C']['1:0'])
        self.assertIn('하얀 별',d['6A907C']['2:0'])
        self.assertIn('회색 별',d['6A907C']['3:1'])
        self.assertIn('6할',d['6D1068']['3:0'])
        self.assertEqual(d['6AB458']['2:1'],d['6AED8C']['1:2'])
        nt=(ROOT/batch500as.create('79C240')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('lower = 190','upper = 190','flag = 1736'):self.assertIn(token,nt)
        nt=(ROOT/batch500as.create('79CCB0')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('tournament = 7','flag = 1929','flag = 7736','width = 8','item = 7'):self.assertIn(token,nt)
        self.assertEqual(re.findall(r'lowerHour = (\d+)',nt),['9','13','16','20'])


    def test_remaining046_047_scope_and_500_final13(self):
        aa=[a for a in self.assets if a.get('batch_id')=='batch500-046']
        bb=[a for a in self.assets if a.get('batch_id')=='final-047']
        self.assertEqual((len(aa),sum(len(a['units']) for a in aa)),(102,500))
        self.assertEqual((len(bb),sum(len(a['units']) for a in bb)),(8,13))
        self.assertEqual(self.plan['draft_assets'][-110:-8],[v[2] for v in batch500at.SOURCES.values()])
        self.assertEqual(self.plan['draft_assets'][-8:],[v[2] for v in final047.SOURCES.values()])
        self.assertEqual([(b['id'],b['authored_literals'],b['rom_applied']) for b in self.plan['batch_policy']['completed_batches'][-2:]],[('batch500-046',500,False),('final-047',13,False)])
        self.assertEqual(self.plan['structural_translation_pending']['ids'],['6368E8:2:0','6368E8:3:0'])
        self.assertFalse(self.plan['structural_translation_pending']['excluded_from_denominator'])

    def test_remaining046_047_repro_and_protected_line_padding(self):
        for mod in (batch500at,final047):
            for arc,(_,count,path) in mod.SOURCES.items():
                asset=mod.create(arc)
                self.assertEqual(asset,json.loads((ROOT/path).read_text(encoding='utf8')))
                self.assertEqual(len(self.validate(asset)),count)
                self.assertFalse(asset['review']['release_eligible'])
                for u in asset['units']:
                    self.assertEqual(u['state'],'needs_review')
                    self.assertEqual(len(u['source'].split('\n')),len(u['translation'].split('\n')))
                    for s,t in zip(u['source'].split('\n'),u['translation'].split('\n')):
                        self.assertEqual(len(s)-len(s.lstrip(' ')),len(t)-len(t.lstrip(' ')))
                        self.assertEqual(len(s)-len(s.rstrip(' ')),len(t)-len(t.rstrip(' ')))
        self.assertNotIn('2:0',batch500at.DRAFT['6368E8'])
        self.assertNotIn('3:0',batch500at.DRAFT['6368E8'])

    def test_remaining046_actual_portrait_and_choice_switches(self):
        for arc,suffix,portrait in [('768800','0:0','MrProgGreen'),('768800','1:0','Lan'),('7B1C78','0:2','NormalNaviYellow'),('7B1C78','1:1','OfficialNavi')]:
            u=next(u for u in batch500at.create(arc)['units'] if u['id']==arc+':'+suffix)
            self.assertEqual(u['origin_portrait'],portrait)
        u={x['id']:x for x in final047.create('7C416C')['units']}
        self.assertEqual(u['7C416C:1:0']['origin_portrait'],'MrProgGreen')
        self.assertEqual(u['7C416C:1:1']['origin_portrait'],'KnightMan')
        for arc in ('7C9C44','7CAF40'):
            for u in final047.create(arc)['units']:self.assertEqual(u['speaker'],'speaker-unestablished')
        for key in batch500at.CHOICES:
            arc=key.split(':')[0];u=next(x for x in batch500at.create(arc)['units'] if x['id']==key)
            self.assertEqual(u['speaker'],'player-choice')

    def test_remaining046_legacy_tutorial_mechanics_not_runtime_claim(self):
        d=batch500at.DRAFT['768800']
        for s,word in [('0:0','1'),('10:2','+30'),('11:4','3'),('11:2','레귤러'),('11:3','한 번'),('10:4','무적')]:self.assertIn(word,d[s])
        self.assertIn('NOT prove',batch500at.CONTEXT['768800'])
        t=(ROOT/batch500at.create('768800')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('mugshot = Lan',t);self.assertIn('mugshot = MrProgGreen',t)
        self.assertEqual(d['12:0'],'지금은 취소하지 않아도 된다')

    def test_remaining046_debug_grants_and_recipe_tables_not_executed(self):
        t=(ROOT/batch500at.create('7794EC')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        for token in ('itemGiveAllChips','amount = 100000','amount = 9999','itemTakeChip','flagMultiSet','callFindTournamentRegistration'):self.assertIn(token,t)
        d=batch500at.DRAFT['7794EC']
        self.assertIn('STA002',d['246:2']);self.assertIn('STA303',d['246:3'])
        self.assertIn('100',d['248:0']);self.assertIn('10',d['249:0'])
        self.assertIn('없어졌다',d['182:0'])
        self.assertEqual(batch500at.DRAFT['709A34']['125:0'].split('\n')[0].strip(),'건델솔1')
        self.assertIn('임시',batch500at.DRAFT['79C240']['1:0'])
        self.assertIn('임시',final047.DRAFT['7C0970']['0:0'])
        self.assertIn('DEATH!',final047.DRAFT['7C0F8C']['0:0'])

    def test_remaining046_native_battle_and_setup_buffers(self):
        for arc,width in [('7B3FF0',9),('7B4184',13)]:
            t=(ROOT/batch500at.create(arc)['source_tpl']['path']).read_text(encoding='utf-8-sig')
            self.assertIn('width = '+str(width),t)
            self.assertIn('flag = 1806',t);self.assertIn('flag = 7701',t)
        t=(ROOT/batch500at.create('7B4184')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('navi = 16',t);self.assertIn('width = 11',t)
        t=(ROOT/batch500at.create('70904C')['source_tpl']['path']).read_text(encoding='utf-8-sig')
        self.assertIn('printCurrentNavi',t);self.assertIn('item = 43',t);self.assertIn('item = 41',t)
        self.assertEqual(batch500at.DRAFT['70904C']['110:1'],'.\n이대로 정할까요?\n')

if __name__=='__main__':unittest.main()
