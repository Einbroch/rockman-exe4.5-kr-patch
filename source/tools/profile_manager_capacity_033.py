"""Exact7CC6A0:0..15 profile-manager pages/name66/nonclearing2-choice model."""
import re
from field_hint_capacity import events
from tpl_literals import skeleton
from nickname_capacity import advance, ARGS

TOKENS = 'mugshotShow msgOpen @literal printPlayerName @literal keyWait clearMsg @literal keyWait clearMsg @literal positionOptionHorizontal option space @literal option space @literal select jump'.split()


def validate(original, target, scripts, selected_ids, nickname_bound=99):
    if skeleton(original) != skeleton(target) or len(scripts) != 1 or scripts[0] not in range(16) or not selected_ids:
        raise ValueError('033 manager protected finite script scope')
    arc = re.search(r'^@archive (\w+)', original, re.M)[1]
    if arc != '7CC6A0': raise ValueError('033 manager finite source root')
    script = scripts[0]; match = re.search(r'^script '+str(script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)', target, re.M)
    if match is None: raise ValueError('033 manager normal language')
    seq = events('@archive '+arc+'\n'+match[0])
    if [d[0] if k == 'command' else '@literal' for _, k, d in seq] != TOKENS: raise ValueError('033 manager exact event topology')
    args = {i: d[1] for i, (_, k, d) in enumerate(seq) if k == 'command'}
    exact = {0:'\t\tmugshot = MrProgGreen\n', 1:'', 3:ARGS, 5:'\t\tany = false\n', 6:'', 8:'\t\tany = false\n', 9:'',
             11:'\t\twidth = 7\n', 13:'\t\tcount = 1\n', 16:'\t\tcount = 1\n', 19:'\t\ttarget = 20\n'}
    for i, want in exact.items():
        if args[i] != want: raise ValueError('033 manager exact command arguments '+str(i))
    for i, nav in [(12, (1, 1, 0, 0)), (15, (0, 0, 1, 1))]:
        if args[i] != '\t\tbrackets = false\n'+''.join('\t\t'+k+' = '+str(v)+'\n' for k, v in zip(('left', 'right', 'up', 'down'), nav)):
            raise ValueError('033 manager exact source navigation')
    wanted = ('\t\tdefault = 0\n\t\tlastCancelSFX = false\n\t\tnoDelay = false\n\t\tBSeparate = false\n\t\tdisableB = false\n\t\tclear = false\n'
              '\t\ttargets = [\n\t\t\tjump = continue,\n\t\t\tjump = 95,\n\t\t\tjump = continue\n\t\t]\n')
    if args[18] != wanted: raise ValueError('033 manager exact nonclearing select/targets')
    first = [0]; seen = set()
    def add(value, rows):
        seen.add(value.key)
        for i, line in enumerate(value.text.split('\n')):
            if i: rows.append(0)
            rows[-1] += advance(line)
    add(seq[2][2], first); first[-1] += 66; add(seq[4][2], first)
    second = []; second = [0]; add(seq[7][2], second)
    prompt = [0]; add(seq[10][2], prompt)
    for rows in (first, second, prompt):
        if len(rows) > 3 or any(w > (168 if i == 2 else 180) for i, w in enumerate(rows)): raise ValueError('033 manager aggregate page width '+str(rows))
    if len(prompt) != 3 or prompt[-1] != 0: raise ValueError('033 manager empty third choice row')
    labels = [seq[i][2] for i in (14, 17)]
    if any('\n' in v.text for v in labels) or sum(8+advance(v.text) for v in labels) > 82: raise ValueError('033 manager native82px choice allocation')
    seen.update(v.key for v in labels)
    if seen != set(selected_ids): raise ValueError('033 manager exact six-literal identity')
    return [dict(script=script, origin=[52, 110], row_limits=[180, 180, 168], pages=[dict(widths=first, player_name_bound=66), dict(widths=second),
                 dict(kind='horizontal-two-choice', prompt_widths=prompt, row=2, native_width=7, allocated_advance=82,
                      target_advance=sum(8+advance(v.text) for v in labels), default=0, clear=False, BSeparate=False, targets=['continue', '95', 'continue'])],
                 terminal='source-jump20-after-nonclearing-select', conditional_native_player_name=True,
                 clear_false_and_jump20_95_runtime_pending=True, product_admitted=False, runtime_pending=True)]
