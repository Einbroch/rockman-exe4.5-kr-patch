"""Pinned Guts13 printChip104 topology; native and localized insertion budgets."""
import json
from archive_scripts import script_spans
from build_visibility_poc import ROOT,sha
from korean_codec import encode_character
PARENT_SHA='f742943f19f7feda1eea55531b76b8f2dd862fb7acb6f301edbb7031a86c373a'
FIRST='거츠、거츠!!\n「'
LAST='」를\n얻겠거스!'
WINDOW=bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')
NATIVE13=bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d3b591c3b591c8383e892f90068019300c9e83e591ea7c3d83b1783e600f1edff0000')

def encoded_prefix():
    table={v:bytes.fromhex(k) for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2 and len(v)==1}
    return WINDOW+b''.join(b'\xe8' if ch=='\n' else encode_character(ch) if '\uac00'<=ch<='\ud7a3' else table[ch] for ch in FIRST)

def validate_parent(asset):
    p=ROOT/'translations/gutsman_pet_talk_ko.json'
    if sha(p.read_bytes())!=PARENT_SHA or asset.get('parent_asset')!={'path':'translations/gutsman_pet_talk_ko.json','sha256':PARENT_SHA,'carry_units':31}:raise ValueError('Guts31 parent identity')
    old=json.loads(p.read_text(encoding='utf8'))['units'];carry=[u for u in asset['units'] if u['id'].split(':')[1]!='13']
    if carry!=old:raise ValueError('Guts31 inherited units changed')

def validate_layout(source,units,layout,scope):
    if scope.get('chipquest_variable_profile')!='gutsman-chip104-native-and-ko-v1':raise ValueError('Guts chip model profile')
    if script_spans(source[0x66a844:0x66a844+2191],255)[13]!=NATIVE13 or script_spans(source[0x765190:0x765190+2437],256)[104]!=bytes.fromhex('4b593d243a298202e5'):raise ValueError('Guts chip native topology/name')
    a,b=[next(u for u in units if u['id']==f'66A844:13:{i}') for i in range(2)];la,lb=[next(l for l in layout if l['id']==f'66A844:13:{i}') for i in range(2)]
    if a['source']!='ガッツガッツ!!\n「' or b['source']!='」 を\nゲットするでガス!' or a['translation']!=FIRST or b['translation']!=LAST or la['line_advance_pixels']!=[81,11] or lb['line_advance_pixels']!=[23,59]:raise ValueError('Guts chip wording/three-row anchors')
    native=11+88+23;localized=11+47+23
    if max(native,localized,*la['line_advance_pixels'],*lb['line_advance_pixels'])>scope['max_line_advance']:raise ValueError('Guts chip insertion overflow')
    lb.update(native_chip104_name_width=88,korean_chip104_name_width=47,native_combined_second_row=native,korean_combined_second_row=localized,variable_three_row_page=True)
    return dict(native_combined_second_row=native,korean_combined_second_row=localized)
