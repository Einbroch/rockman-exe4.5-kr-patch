"""Three independently contextualized GutsMan archives; pinned serialization."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

PACKS={
'6663B8':dict(name='gutsman_return_ko',tpl_sha='3272f7060b455a882c8c6ab4c1abafe64327765d5c775018683e93934a021359',payload_sha='7c1410a2b14758a560a3ebc60abdbc7ae8fa99f5b9bfd7e1fe5418ae34f4fe5b',context='GutsMan normal internet return1 and defeated return2; original root038118/intro+8. Same native group explicitly names GutsMan. Portrait92,110,type1,3rows/keyWait/clear/waitHold retained.',draft={1:['다녀왔거스!!\n역시 인터넷은\n재미있거스!!'],2:['당해 버렸거스\n・・・하지만,다음엔\n힘내겠거츠!!']}),
'6664D0':dict(name='gutsman_jackin_ko',tpl_sha='4f8d7f78318d00838083600af2eae557948994d1978a9b2942eb137e160632bb',payload_sha='4e1ba8197589557b1eb2499289f9c3791a765028749f09bdc21cc227f54dbea6',context='GutsMan.EXE plugin/transmission slogan, explicit source name; original root038120/intro+16. Portrait92,110,type3,three rows,wait30 and flag3603/3651 set-clear unchanged. Timed delivery differs from keyWait dialogue.',draft={1:['플러그인!\n거츠맨.EXE、\n트랜스미션!!']}),
'666820':dict(name='gutsman_mail_alert_ko',tpl_sha='b60dd4aec45016515d02053f5cf45e9a83d8c5dd354bcbc9e96b726fc54a7ce5',payload_sha='d4cf2e86ad87ce890d855bf60b7e9ebf014981eae826dfb810eaac7845561540',context='GutsMan mail arrivals; original root038128/intro+24. Fourteen initial !! literals unchanged. Nickname scripts1/2/3 preserve first-row comma11px before newline. Sound155/wait96 twice,delivery flags,tournament receive and mail additions retained;255slots.',draft={1:['!!','、\n메일이거스!!'],2:['!!','、\n메일이거스!!'],3:['!!','、\n메일이거스!!'],4:['!!','메일이거스!!'],5:['!!','메일이거스!!'],6:['!!','메일이거스!!'],7:['!!','메일이거스!!'],20:['!!','메일이거스!!'],21:['!!','메일이거스!!'],22:['!!','메일이거스!!'],23:['!!','메일이거스!!'],24:['!!','메일이거스!!'],25:['!!','메일이거스!!'],26:['!!','메일이거스!!']})}

def main():
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    for ar,p in PACKS.items():
        path=ROOT/f'analysis/full_scope_v1/source_tpl/{ar}.tpl';require_hash(path,p['tpl_sha']);tpl=path.read_text(encoding='utf-8-sig');items=literals(tpl);d=p['draft']
        if {x.key for x in items}!={f'{ar}:{s}:{i}' for s,rows in d.items() for i in range(len(rows))}:raise ValueError('complete source population')
        units=[dict(id=x.key,source=x.text,translation=d[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in items]
        replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive=ar,source_archive_sha256=p['payload_sha'],consumer='normal-dialogue',context=p['context'],voice='Existing GutsMan development candidate 거츠/거스 voice; wording/terminology/presentation human review pending.',evidence=f'analysis/full_scope_v1/source_tpl/{ar}.tpl; native GutsMan group root038110; translations/gutsman_intro_ko.json',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='Complete finite literal population; IDs/source,numerals,newline boundaries,all commands/slots/native variables preserved. No RTC/save/input/gameplay-code changes.',semantic_review=['Defeated return remains defeat with resolve for next time, not successful return. Explicit .EXE identity retained.','Mail delivery branches/variable insertion are not normal execution proved by static font/geometry. NumberMan4649 approval not reused.'],units=units)
        out=ROOT/f"translations/{p['name']}.json"
        if out.exists():raise ValueError('preserve translation '+str(out))
        out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print(ar,len(units),'serialized')

if __name__=='__main__':main()
