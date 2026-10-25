"""AquaMan50..52 exact early FD09 spatial projection, not control rewriting."""
import re
from tpl_literals import skeleton
from calendar_delete_capacity_031 import validate as ordinary
from calendar_date_delete_capacity_032 import validate as dates


def projection(tpl, script):
    match = re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)', tpl, re.M)
    header = re.search(r'^@archive (\w+)', tpl, re.M)
    if header is None or header[1] != '697B70' or match is None or script not in (50, 51, 52): raise ValueError('033 Aqua exact source root/script')
    one = header[0]+'\n'+match[0]
    prefix = ('\tcallSkipMugshotFadeIn\n\tmsgOpenQuick\n\tmugshotShow\n\t\tmugshot = AquaMan\n'
              '\ttextSpeed\n\t\tdelay = 0\n\tsoundDisableChoiceSFX\n')
    if one.count(prefix) != 1 or one.count('\tsoundDisableChoiceSFX\n') != 1 or '\tsoundEnableChoiceSFX\n' in one:
        raise ValueError('033 Aqua exact early FD09 topology')
    # Only a spatial-model view is normalized. Actual target/source commands
    # and compiled FD09 position must remain completely unchanged.
    projected = one.replace(prefix, prefix.removesuffix('\tsoundDisableChoiceSFX\n'))
    anchor = '\tpositionOptionHorizontal\n\t\twidth = 8\n'
    if projected.count(anchor) != 1 or '\t\tflag = 3611\n' not in projected: raise ValueError('033 Aqua exact native selector/flag')
    return projected.replace(anchor, '\tsoundDisableChoiceSFX\n'+anchor)


def validate(original, target, scripts, selected_ids, nickname_bound=99):
    if len(scripts) != 1 or skeleton(original) != skeleton(target): raise ValueError('033 Aqua protected actual control skeleton')
    script = scripts[0]; so = projection(original, script); st = projection(target, script)
    proof = (ordinary if script == 50 else dates)(so, st, scripts, selected_ids, nickname_bound)
    proof[0]['spatial_projection_only'] = 'exact697B70 early FD09; native whole216byte context proof, no actual command moved'
    proof[0]['original_FD09_event_index'] = 4
    proof[0]['choice_audio_and_outcomes_runtime_pending'] = True
    return proof
