"""Fail closed on native printChip104 insertion and adopted two-row layout."""
from archive_scripts import script_spans

def validate_layout(source,units,layout,scope):
    if scope.get('chipquest_variable_profile')!='roll-chip104-native-name-v1':raise ValueError('unknown chip quest variable model')
    native=script_spans(source[0x765190:0x765190+2437],256)[104]
    if native!=bytes.fromhex('4b593d243a298202e5'):raise ValueError('chip104 native name source changed')
    span=script_spans(source[0x664E28:0x664E28+2158],255)[13]
    if not span.startswith(bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d92f900680193')):raise ValueError('chip104 insertion/source quote changed')
    u=next(u for u in units if u['id']=='664E28:13:1');l=next(l for l in layout if l['id']==u['id'])
    if u['source']!='」 を\nさがしに行こう!' or not u['translation'].startswith('」\n') or len(l['line_advance_pixels'])!=2 or l['line_advance_pixels'][0]!=11:raise ValueError('chip104 two-row quote boundary changed')
    width=11+8*11+l['line_advance_pixels'][0]
    if width>scope['max_line_advance'] or max(l['line_advance_pixels'])>scope['max_line_advance']:raise ValueError('chip104 combined line overflow')
    l.update(native_chip104_name_width=88,combined_first_row_advance_pixels=width,native_name_localization_pending=True)
    return {'native_name_hex':native.hex(),'native_name_width':88,'combined_first_row':width,'native_name_localization_pending':True}
