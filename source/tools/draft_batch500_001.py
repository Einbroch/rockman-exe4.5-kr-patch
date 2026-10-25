"""Batch500-001: manually scoped equipment459, progress31, tournament10; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
'6E1554':('975e70d27680364267ecad2556cef3a6d6d8c564393842eb5ef2f98dd137fb53',51,'translations/batch500_001_equipment_guts_draft_ko.json'),
'6E17CC':('d2ff98339b8d265d45cc1eef0a40e8bc0f3cf0d3dccc0620b7c6cc3e1877f979',51,'translations/batch500_001_equipment_wind_draft_ko.json'),
'6E1A48':('75f37fa393c23daad298b83c55414560af33beb3c57425c961c24c5e8a9ffcef',51,'translations/batch500_001_equipment_search_draft_ko.json'),
'6E1CC0':('d80fc18e5eee6f10e30f68516c39592863f50be8c8d3b8136eb816cdaaabbf2a',51,'translations/batch500_001_equipment_fire_draft_ko.json'),
'6E1F38':('2aab0fa2aaf76d1b20e82c3fb0cde4c93c65077ef02fa9d26c204f5e24a0cdfe',51,'translations/batch500_001_equipment_thunder_draft_ko.json'),
'6E21B0':('4aa3a1d56f3783f5c6ca4782573986799a2a6c68018f5d81c4f25900d45377ef',51,'translations/batch500_001_equipment_proto_draft_ko.json'),
'6E2428':('93eb291fc6e5508b75e58dab2f447d363dab8b18d5496f7f5f76637ae83b7a19',51,'translations/batch500_001_equipment_number_draft_ko.json'),
'6E26A0':('23b00b9b6befbaf550c1fb3c377c3943a37e9dc6fbf82924041aab5acac11a07',51,'translations/batch500_001_equipment_metal_draft_ko.json'),
'6E2914':('0025e784bc22709280cff4c7fa4eec72b44cb5623cc5e0b541d78cfc2d3c8d4b',51,'translations/batch500_001_equipment_junk_draft_ko.json'),
'66FD14':('b45b5855df33ccf4536c700b9147210f8955e186bb34095fe2aaf53bf386f42d',31,'translations/batch500_001_quick_progress_draft_ko.json'),
'6886F0':('9c98774322c6706271cfcf29d4e88e979332d1e3b28da01c55123081722deae0',10,'translations/batch500_001_quick_tournament_draft_ko.json'),
}
ACTORS={'6E1554':'GutsMan','6E17CC':'WindMan','6E1A48':'SearchMan','6E1CC0':'FireMan','6E1F38':'ThunderMan','6E21B0':'ProtoMan','6E2428':'NumberMan','6E26A0':'MetalMan','6E2914':'JunkMan'}
# Explicit shared equipment-label candidates after reading all nine complete TPLs.
# This is not a source-string replacement rule or generated speaker prose.
LABELS={
'0:0':'   칩 폴더','1:0':'칩 폴더','2:0':'  칩 폴더   ',
'3:0':'록 버스터','4:0':'실드','5:0':'차지 샷','6:0':'버스터','7:0':'배리어',
'8:0':'롤 애로','9:0':'거츠머신건','10:0':'거츠 해머','11:0':'스이코미','12:0':'돌풍',
'13:0':'스코프 건','14:0':'파이어 암','15:0':'썬더 볼','16:0':'롱소드','17:0':'주사위 봄',
'18:0':'브레이크 버스터','19:0':'메탈 피스트','20:0':'메탈 블레이드','21:0':'폴터가이스트',
'22:0':'정크 프레스','23:0':'아쿠아 호스','24:0':'씨앗총','25:0':'데스 포레스트',
'26:0':'키라키라 메테오','27:0':'킹덤C','28:0':'로열WB','29:0':'인비저블','30:0':'수리검',
'31:0':'파이어 봄','32:0':'네이팜 봄','33:0':'프리즈 봄','34:0':'플랜트 위드',
'35:0':'슈팅B','36:0':'D오버로드','37:0':'썬더볼트',
}
DRAFT={
'6E1554':{
'60:0':'칩 폴더를\n편집하는거스','61:0':'R 버튼에 배정할\n무기를 고르는거스!','62:0':'L 버튼에 배정할\n무기를 고르는거스!',
'70:0':'칩 폴더가\n','70:1':'장이\n아닌거스!','70:2':'편집을\n그만두는거스?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지거스!','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있거스',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있거스','74:0':'메가 클래스 칩은\n5장만 넣을 수 있거스',
'75:0':'기가 클래스 칩은\n1장만 넣을 수 있거스',
},
'6E17CC':{
'60:0':'칩 폴더를\n편집하겠다','61:0':'R 버튼에 배정할\n무기를 골라 주거라...','62:0':'L 버튼에 배정할\n무기를 골라 주거라...',
'70:0':'칩 폴더가\n','70:1':'장이 아니구나','70:2':'편집을 그만두겠느냐?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지다...','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있다',
'75:0':'기가 클래스 칩은\n1장만 넣을 수 있다',
},
'6E1A48':{
'60:0':'칩 폴더를\n편집합니다','61:0':'R 버튼에 배정할\n무기를 골라 주세요','62:0':'L 버튼에 배정할\n무기를 골라 주세요',
'70:0':'칩 폴더가\n','70:1':'장이 아닙니다','70:2':'편집을 그만두시겠습니까?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지입니다','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있습니다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있습니다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있습니다',
'75:0':'기가 클래스 칩은\n1장만 넣을 수 있습니다',
},
'6E1CC0':{
'60:0':'칩 폴더를\n편집하자','61:0':'R 버튼에 배정할\n무기를 골라 줘','62:0':'L 버튼에 배정할\n무기를 골라 줘',
'70:0':'칩 폴더가\n','70:1':'장이 아니잖아','70:2':'편집을 그만둘까?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지야!','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있어',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있어','74:0':'메가 클래스 칩은\n5장만 넣을 수 있어',
'75:0':'기가 클래스 칩은\n1장만 넣을 수 있어',
},
'6E1F38':{
'60:0':'칩 폴더를\n편집하겠다','61:0':'R 버튼에 배정할\n무기를 골라 다오','62:0':'L 버튼에 배정할\n무기를 골라 다오',
'70:0':'칩 폴더가\n','70:1':'장이 아니구나','70:2':'편집을 그만두겠느냐?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지다...','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있다',
'75:0':'기가 클래스 칩은\n1장만 넣을 수 있다',
},
'6E21B0':{
'60:0':'칩 폴더를\n편집합니다','61:0':'R 버튼에 배정할\n무기를 선택해 주세요','62:0':'L 버튼에 배정할\n무기를 선택해 주세요',
'70:0':'칩 폴더가\n','70:1':'장이 아닙니다','70:2':'편집을 그만두시겠습니까?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지입니다','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있습니다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있습니다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있습니다',
'75:0':'기가 클래스 칩은\n1장만 넣을 수 있습니다',
},
'6E2428':{
'60:0':'칩 폴더를\n편집해요','61:0':'R 버튼에 배정할\n무기를 골라 주세요','62:0':'L 버튼에 배정할\n무기를 골라 주세요',
'70:0':'칩 폴더가\n','70:1':'장이 아니에요','70:2':'편집을 그만둘까요?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지예요','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있어요',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있어요','74:0':'메가 클래스 칩은\n5장만 넣을 수 있어요',
'75:0':'기가 클래스 칩은\n1장만 넣을 수 있어요',
},
'6E26A0':{
'60:0':'칩 폴더를\n편집하겠다','61:0':'R 버튼에 배정할\n무기를 골라 줘','62:0':'L 버튼에 배정할\n무기를 골라 줘',
'70:0':'칩 폴더가\n','70:1':'장이 아니다','70:2':'편집을 그만두겠나?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지다','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있다',
'75:0':'기가 클래스 칩은\n1장만 넣을 수 있다',
},
'6E2914':{
'60:0':'칩 폴더를\n편집한다...','61:0':'R 버튼에 배정할\n무기를 선택하라','62:0':'L 버튼에 배정할\n무기를 선택하라',
'70:0':'칩 폴더가\n','70:1':'장이\n아니다!','70:2':'편집을 중단하겠나?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지다','72:0':'같은 메가 클래스의\n칩은, 1장만\n넣을 수 있다...',
'73:0':'같은 기가 클래스의\n칩은, 1장만\n넣을 수 있다...','74:0':'메가 클래스 칩은\n5장만\n넣을 수 있다...',
'75:0':'기가 클래스 칩은\n1장만\n넣을 수 있다...',
},
'66FD14':{
'10:0':'인터넷을\n탐색해 볼까\n...',
'11:0':'견습 라이선스...\n도전해 볼까',
'12:0':'견습 라이선스 시험\n...합격하겠다',
'13:1':'」 칩을\n찾아볼까...',
'14:0':'견습 라이선스를\n받으러 가자...',
'15:0':'견습 라이선스 시험\n수고했구나...\n조금 쉬겠느냐?',
'16:0':'인터넷3에서\n일어난 사건이\n신경 쓰이는구나...',
'17:0':'방금 쓰러뜨린 내비가\n사건의 범인이었던\n모양이구나...',
'17:1':'후우...\n한숨 돌릴까...',
'18:0':'인터넷5에서\n일어난 사건이\n신경 쓰이는구나...',
'19:0':'인터넷7에서\n일어난 사건이\n신경 쓰이는구나...',
'20:0':'인터넷9에서\n일어난 사건이\n신경 쓰이는구나...',
'21:0':'인터넷10에서\n일어난 사건이\n신경 쓰이는구나...',
'22:0':'인터넷12에서\n일어난 사건이\n신경 쓰이는구나...',
'23:0':'블랙워크스에게서\n「마이너스 키」를\n되찾자...',
'24:0':'「마이너스 키」는,\n다른 내비 1명이\n가진 모양이구나...',
'25:0':'「마이너스 키」를\n인터넷9에 있는',
'25:1':'내비에게\n가져다주자...',
'26:0':'오피셜\n토너먼트 접수\n장소로 가자',
'27:0':'언더 인터넷으로\n가자...',
'27:1':'목표 내비를 찾을\n표식은\n관이었지...',
'28:0':'오피셜\n토너먼트에\n참가 신청하러 가자',
'29:0':'주말에는\n오피셜\n토너먼트다',
'29:1':'전력을 다해\n승부하겠다',
'30:0':'오피셜\n토너먼트에서\n우승해야만,',
'30:1':'최강의\n넷배틀러다...',
'31:0':'인터넷\n탐색을 계속할까\n...',
'32:0':'오피셜\n토너먼트의\n예선을 치르러 갈까',
'33:0':'아까 도착한\n메일을 읽어 볼까...',
'34:0':'주말이 지나면\n오피셜\n토너먼트에',
'34:1':'참가 신청하러 가자',
},
'6886F0':{
'1:0':'지, 지고 말았네요\n제, 제가 잘못한 건\n아니라고요!!',
'1:1':'저는 제가 가진\n승리의 방정식대로\n배틀했어요',
'1:2':'제 계산에\n오류는 없어요!',
'2:0':'해냈어요!!\n승리의 방정식에\n딱 들어맞았어요!',
'2:1':'계산대로 거둔\n승리예요!!',
'10:0':',\n참가 신청을 안 했어요!',
'20:0':'토너먼트,\n다치지 않을 정도로\n힘내도록 해요!',
'21:0':'토너먼트,\n다치지 않을 정도로\n힘내도록 해요!',
'22:0':'토너먼트,\n다치지 않을 정도로\n힘내도록 해요!',
'23:0':'토너먼트,\n다치지 않을 정도로\n힘내도록 해요!',
}}
CONTEXT={a:'Equipment fixed labels0..37, quick prompts60..62, explicit portrait folder warnings70..75; all current unselected entries.' for a in ACTORS}
CONTEXT.update({'66FD14':'Progress hint dispatcher10..34 with license/chip/event/mail/key/weekday/tournament branches; no portrait shown.',
'6886F0':'Quick defeat/victory/unregistered/tournament encouragement; calculation/denial meaning, no mugshot shown.'})

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    ids={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}
    authored={**LABELS,**DRAFT[archive]} if archive in ACTORS else DRAFT[archive]
    values={archive+':'+k:v for k,v in authored.items()}
    selected=[x for x in literals(original) if x.key in ids]
    if len(selected)!=count or set(values)!=ids:raise ValueError('batch scope '+archive)
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('batch topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('batch tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('batch padding '+x.key)
        equipment=archive in ACTORS;shown=equipment and s>=70;choice=shown and s==70 and i in (3,4)
        speaker='player-choice' if choice else ACTORS[archive] if shown else 'equipment-label' if equipment and s<60 else 'unshown-equipment-voice' if equipment else 'unshown-quick-voice'
        u=dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait=ACTORS[archive] if shown else None,portrait_visibility='shown' if shown else 'not-shown-in-script',
            context=CONTEXT[archive],variable_context='Folder required count is buffer1, not hardcoded30; button R/L and abbreviated C/WB/B/D retained. Chip104/name/calendar variables and literal/page boundaries unchanged; runtime/layout unverified.')
        if equipment and s<38:
            u['wording_lineage']='equipment_weapons_ko.json / equipment_labels_ko.json existing candidate; source-label context matched manually; not approval'
        units.append(u)
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    notes=[
        'Batch500-001 exact500 stable literals across11 full archives: equipment459 including342 label instances, progress31, tournament10. Not500 unique sentences.',
        'All first drafts needs_review/non-distribution. No wording approval, release/insertion/runtime closure inferred from checks.',
    ]
    if archive in ACTORS:
        notes+=['38 labels match shared equipment label candidates; manual context-based selection only. C/WB/B/D not expanded; R/L literals38/39 and printBuffer-only63 remain unchanged.',
            'Same chip limit3, same mega/giga limit1, total mega5/giga1 preserved. Folder size buffer remains dynamic. Stop-edit yes/no is not permission to mutate save; no menu input performed.',
            'Explicit portrait70..75 only. Quick60..62 speaker not confirmed merely by adjacent portrait; source speech register retained as candidate.',
            'Source Gutsガス→거스, Wind/Thunder elder-like, Search/Proto formal, Fire casual, Number polite, Metal direct, Junk clipped/robotic candidates kept distinct. Junk three-line class warnings and Guts count/stop-edit line split unchanged.',
            'Fixed-cell labels and dialogue are separate consumers; existing observed font/equipment paths do not prove this batch rendered. Width, abbreviation, dynamic count and choice geometry still need actual review.']
    elif archive=='66FD14':
        notes+=['Dispatcher priority and flags retained, chip104 and item11 distinct. Target coffin hint not silently changed to criminal description; source says target Navi.',
            'Areas3/5/7/9/10/12, another1Navi, key return internet9, official registration/prelim/weekend checks0/6 and post-weekend34 preserved. Quick actor not inferred as WindMan.']
    else:
        notes+=['Preserve stammer, denial of fault/calculation error, victory formula, no registration cancellation and injury-limited encouragement. Quick actor not inferred as NumberMan; no portrait.',
            'Nickname boundary, callCancelMenuTransition and20..23 flag3603 retained; no tournament/runtime verification.']
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='batch500-equipment-progress-tournament',
        context=CONTEXT[archive],voice='Source-conditioned manual candidates; distinct named portraits only where shown. Not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='All source fields/IDs/TPL/payload, commands, buffers, numerical limits, newlines, padding and current selected entries immutable; no ROM/save writes.',
        batch_id='batch500-001',semantic_review=notes,units=units)

def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
