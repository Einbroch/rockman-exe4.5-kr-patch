"""Adopted native-six-glyph development contract; not Hangul name support."""
import re,struct
from dataclasses import replace
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from tpl_literals import literals
from korean_codec import EXTRA_CHARACTER_INDICES

ARGS='\t\tcapitalizeFirst = false\n\t\tcapitalizeAll = false\n\t\tprintN = false\n'
FORMS=frozenset(('의','도','님의','님은','님이','님께',' 님의',' 님은',' 님이',' 님께'))
CPU='analysis/pending_insertion_500_019_variable_survey_v1/native_nickname_v2.json'
RUNTIME='analysis/pending_insertion_500_019_variable_survey_v1/native_name_runtime.json'

def native_bound(source):
    cfg=read('project.json')
    if sha(source)!=cfg['source_profile']['sha256']:raise ValueError('nickname source revision')
    cpu=read(CPU);runtime=read(RUNTIME)
    if cpu['source_sha256']!=sha(source) or cpu['rom_sha256']!=runtime['rom_sha256'] or runtime['native_E406_renderer_index']!=234 or not all(runtime[k] for k in ('sixth_accepted','seventh_rejected','delete_reinsert_verified')):raise ValueError('nickname native evidence')
    for record in cpu['native_code']:
        if sha(source[record['offset']:record['offset']+record['bytes']])!=record['sha256']:raise ValueError('nickname native code')
    for address,value in cpu['literals'].items():
        if struct.unpack_from('<I',source,int(address,16))[0]!=int(value,16):raise ValueError('nickname native literal')
    if struct.unpack_from('<II',source,0x526D8)!=(0x02000E5F,21):raise ValueError('nickname descriptor')
    widths=struct.unpack_from('<441I',source,0x5290C);suffixes=[]
    for index in range(42):
        at=0x63720C+struct.unpack_from('<H',source,0x63720C+index*2)[0];end=source.index(0xE5,at)+1;raw=source[at:end]
        if raw.hex()!=cpu['suffix_hex'][index]:raise ValueError('nickname suffix provider')
        advance=0;pos=0
        while pos<len(raw)-1:
            glyph=raw[pos];pos+=1
            if glyph==0xE4:glyph=228+raw[pos];pos+=1
            if glyph>=441:raise ValueError('nickname source glyph')
            advance+=widths[glyph]
        suffixes.append(advance)
    return 6*max(widths)+max(suffixes)

def advance(text):return sum(12 if '\uAC00'<=c<='\uD7A3' or c in EXTRA_CHARACTER_INDICES else 8 if c==' ' else 11 for c in text)

def validate_templates(original,target,profiles,bound,selected_ids):
    if type(bound) is not int or bound<0:raise ValueError('nickname native bound')
    archive=re.search(r'^@archive (\w+)',original,re.M).group(1)
    source={i.key:i for i in literals(original)};translated={i.key:i for i in literals(target)};seen=set();proof=[]
    for profile in profiles:
        if set(profile)!={'script','suffix_id','source_first_line','first_line'}:raise ValueError('nickname capacity profile schema')
        script=profile['script'];key=profile['suffix_id']
        if type(script) is not int or script in seen or key not in selected_ids or key.split(':')[:2]!=[archive,str(script)]:raise ValueError('nickname capacity selected scope')
        seen.add(script)
        if source[key].text.split('\n')[0]!=profile['source_first_line'] or translated[key].text.split('\n')[0]!=profile['first_line']:raise ValueError('nickname pinned first line')
        first=profile['first_line']
        if first not in FORMS and not re.fullmatch(r'[、,!！?？ .…~]*',first):raise ValueError('nickname dependent suffix')
        section=re.search(r'^script '+str(script)+r'\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',target,re.M).group()
        if re.findall(r'^\t(print\w+)\b',section,re.M)!=['printPlayerNickname']:raise ValueError('nickname variable population')
        call=re.search(r'^\tprintPlayerNickname\n((?:\t\t[^\n]+\n)*)',section,re.M)
        if call.group(1)!=ARGS:raise ValueError('nickname command arguments')
        head='@archive '+archive+'\n';items=[replace(i,start=i.start-len(head),end=i.end-len(head)) for i in literals(head+section)]
        resets=list(re.finditer(r'^\t(?:msgOpen(?:Quick)?|clearMsg)\s*$',section[:call.start()],re.M))
        if not resets:raise ValueError('nickname page initialization')
        before=[i for i in items if resets[-1].end()<i.start<call.start()]
        after=[i for i in items if i.start>=call.end()]
        if len(before)>1 or before and not before[0].text.endswith('\n') or not after or after[0].key!=key or section[call.end():after[0].start].strip():raise ValueError('nickname column-zero template')
        suffix=after[0];reset=re.search(r'^\t(?:clearMsg|msgClose|end|waitHold|msgOpen(?:Quick)?)\s*$',section[suffix.end:],re.M)
        limit=suffix.end+reset.start() if reset else len(section)
        if any(suffix.end<=i.start<limit for i in items):raise ValueError('nickname unmodeled same-page literal')
        rows=(before[0].text.count('\n') if before else 0)+suffix.text.count('\n')+1
        if '\n' not in suffix.text or rows>3 or bound+advance(first)>132:raise ValueError('nickname aggregate capacity')
        proof.append(dict(script=script,suffix_id=key,native_advance_bound=bound,first_row_advance=bound+advance(first),rows=rows,source_command_unchanged=True,runtime_verification_pending=True))
    return proof

def validate(source,original,target,profiles,selected_ids):
    return validate_templates(original,target,profiles,native_bound(source),selected_ids)
