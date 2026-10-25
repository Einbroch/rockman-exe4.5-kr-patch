"""Ten-cell/70-undo temporary backend candidate, not game RAM or ROM hook.

Reuse the verified rank transition/deletion tables; expand only state layout.
Header4 +10 rank words20 +70 undo pairs280 =304 bytes. Original eight-cell
backend and its pinned artifacts remain unchanged.
"""
import struct
import hangul_composer_thumb as base

STATE_BYTES = 304
MAX_CELLS = 10
MAX_HISTORY = 70


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('extended backend source applicability')
    return source.replace(old, new, 1)


VALIDATE = base.VALIDATE
for old, new in [('cmp r1, #8', 'cmp r1, #10'), ('cmp r2, #64', 'cmp r2, #70'),
                 ('cmp r7, #8', 'cmp r7, #10')]:
    VALIDATE = replace_once(VALIDATE, old, new)
FEED = replace_once(base.FEED, base.VALIDATE, VALIDATE)
UNDO = replace_once(base.UNDO, base.VALIDATE, VALIDATE)
FEED = replace_once(FEED, 'movs r0, #69', 'movs r0, #76')
UNDO = replace_once(UNDO, 'movs r0, #69', 'movs r0, #76')
FEED = replace_once(FEED, 'cmp r0, #64', 'cmp r0, #70')
FEED = replace_once(FEED, 'adds r1, #20', 'adds r1, #24')
UNDO = replace_once(UNDO, 'adds r5, #20', 'adds r5, #24')


def encode_state(c):
    def words(s):
        return [ord(ch) - 0xAC00 for ch in s.committed] + ([] if s.l is None else [base.tail_rank(s)])
    w = words(c.state)
    if len(w) > MAX_CELLS or len(c.history) > MAX_HISTORY:
        raise ValueError('extended fixture bounds')
    history = bytearray()
    for prior in c.history:
        old = words(prior)
        history.extend(struct.pack('<HH', len(old) | (int(prior.l is not None) << 8), old[-1] if old else base.EMPTY))
    return (bytes([len(w), c.limit, len(c.history), int(c.state.l is not None)])
            + struct.pack('<10H', *(w + [base.EMPTY] * (10 - len(w))))
            + history + b'\xFF' * (MAX_HISTORY * 4 - len(history)))
