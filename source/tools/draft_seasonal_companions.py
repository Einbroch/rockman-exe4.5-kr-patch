"""Manual Rockman/Roll holiday drafts, source-derived serialization only."""
import json
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals,replace_literals
from build_development_patch import validate_literal_numerals

DRAFTS={
'65E438':{
1:['새해 복 많이 받아!\n올해도 잘 부탁해!','새로운 1년이\n시작됐어!!','1년의 계획은\n새해 첫날에 세우자!','올해 목표는\n뭘까?'],
2:['오늘은 절분이네\n콩을 뿌려야지!','도깨비는 밖으로!\n복은 집 안으로!'],
3:['오늘은 발렌타인데이!\n초콜릿을,\n받을 수 있을까?','두근두근하네!'],
4:['오늘은 발렌타인데이!\n초콜릿을,\n누구에게 줄 거야?','두근두근하네!'],
5:['오늘은 3월3일,\n복숭아꽃 명절이야!\n여자아이들의 날이지!','히나아라레는 맛있지'],
6:['오늘은 5월5일\n어린이날이야!!','마음껏\n놀아 보자!!'],
7:['오늘은 칠석이네!\n은하수는 보일까?'],
8:['오늘은 성탄절 전야!\n저녁은 진수성찬?','산타 할아버지가,\n오시면 좋겠다!'],
9:['메리 크리스마스!!','성탄절은 오늘이야!\n하지만 전날 밤이\n제일 신나지!'],
10:['오늘은 섣달그믐・・・\n올해도 오늘로\n끝이네','대청소를 해야지!'],
11:['생일을,\n축하해!!','새로운 네가\n시작되는 날이야!'],
12:['창립 기념일이야\n오늘은 학교,\n쉬려나?'],
17:['오늘은'],18:['「','」'],19:['이야!']},
'6648D0':{
1:['아, 해피\n뉴 이어!','우후후,\n올해도 잘 부탁해!!'],
2:['오늘은 절분이네!','콩을 뿌린 다음엔,\n나이만큼\n콩을 먹자!'],
3:['우후후!\n오늘은 발렌타인데이!','남자애도 떨리지만\n여자아이들은\n더 두근두근한다고'],
4:['야호!','발렌타인데이가\n찾아왔네!','초콜릿, 줄 거야!?','꺄아! 두근두근!'],
5:['짜자잔!','오늘이 무슨 날인지\n알고 있어!?','오늘은 3월3일!\n히나마쓰리야!!','그-러-니-까,','여자아이들의 날!!','오늘은 여자아이들이\n주인공이야!'],
6:['오늘은 5월5일\n어린이날이야!!','잉어 깃발처럼,\n느긋하게 놀아 보자!','아, 맞다!\n치마키도 먹어야지!'],
7:['오늘은 칠석이네!','오늘은 직녀와\n견우가 데이트하는\n일년에1번뿐인 날이야','낭만적이야~'],
8:['랄랄라~\n랄랄라~\n랄랄라라라~','오늘은 성탄절 전야!','거리를 수놓는\n장식 조명과,','행복해 보이는\n사람들의 얼굴・・・','난 1년 중 오늘이\n가장 좋아・・・'],
9:['메리 크리스마스!!','산타 할아버지는\n오셨어?','크리스마스는\n사실 오늘이\n본날이야'],
10:['오늘은 섣달그믐,\n올해의 마지막 날!','내일부터는 내년이야\n왠지 이상한 느낌이야'],
11:['해피 버스데이!!','생일을,\n축하해!!','뭔가 좋은 일이,\n생기면 좋겠다!'],
12:['창립 기념일이야','학교의 생일\n같은 거지!'],
17:['오늘은'],18:['「','」'],19:['이야!']}}

def main():
    inv=json.loads((ROOT/'analysis/full_scope_v1/inventory.json').read_text(encoding='utf8'));cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    for ar,authored in DRAFTS.items():
        r=next(x for x in inv['archives'] if x['archive']==ar);p=ROOT/f'analysis/full_scope_v1/source_tpl/{ar}.tpl';require_hash(p,r['source_tpl_sha256']);tpl=p.read_text(encoding='utf-8-sig');source=literals(tpl)
        keys={f'{ar}:{s}:{i}' for s,rows in authored.items() for i in range(len(rows))}
        if keys!={x.key for x in source}:raise ValueError('complete draft denominator')
        units=[dict(id=x.key,source=x.text,translation=authored[int(x.key.split(':')[1])][int(x.key.split(':')[2])],state='needs_review') for x in source]
        replace_literals(tpl,units);validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive=ar,source_archive_sha256=r['source_payload_sha256'],consumer='normal-dialogue',context=('Rockman' if ar=='65E438' else 'Roll')+' seasonal/birthday operator greetings. Native per-Navi pointer group seasonal slot+52 from pinned introduction slot; all pages use portrait92,110,3rows. All original holidays/dates, gender global22 branch and anniversary buffer/loop preserved. Needs exact-ROM normal triggers/renderer evidence.',voice='Existing friendly informal Rockman/Roll operator voice; independent development drafts, not global replacement of NumberMan wordings.',evidence=f'analysis/full_scope_v1/source_tpl/{ar}.tpl; native pointer{r["pointers"][0]:06X}/intro pointer{r["pointers"][0]-52:06X}',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),protected_policy='Complete literal population including source-identical quotes. Numerals/newline counts/commands/variables/loop/events preserved. No RTC or gameplay calendar date adaptation.',semantic_review=['Japanese Setsubun/Hinamatsuri/koinobori/chimaki retained with Korean-readable descriptions/transliteration. Human cultural wording review pending; no approved scope exclusions.'],units=units)
        name='rockman' if ar=='65E438' else 'roll';out=ROOT/f'translations/{name}_seasonal_ko.json'
        if out.exists():
            if json.loads(out.read_text(encoding='utf8'))!=asset:raise ValueError('refusing translation overwrite')
            print(ar,'existing identical draft verified',flush=True);continue
        out.write_text(json.dumps(asset,ensure_ascii=False,indent=2),encoding='utf8');print(ar,len(units),flush=True)

if __name__=='__main__':main()
