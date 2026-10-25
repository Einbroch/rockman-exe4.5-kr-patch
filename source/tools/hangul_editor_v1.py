"""Host reference for the Korean keyboard page on the native editor (words at 0x0200FC60, overwrite at cursor).

Only the word before the cursor is ever composed. Rules follow hangul_keyboard_model.transition (Codex model):
a medial needs an initial, a lone initial merges only into its tense pair, an unmergeable consonant after a
syllable starts a new syllable, a medial after a final moves the final (or its second half) to a new syllable.
B on a Hangul word removes one jamo in canonical order (괙->괘->과->고->ㄱ->deleted); B on a native word is the
native delete (not modelled here). A new word follows native placement: rejected when count == limit, otherwise
written at the cursor (appending when the cursor is at the end) and the cursor advances.
"""
import hangul_record_v3 as R
from hangul_keyboard_model import INITIALS, MEDIALS, FINALS, FINAL_MERGE, FINAL_SPLIT, MEDIAL_MERGE, INITIAL_MERGE, LOADED_MEDIAL_PREVIOUS, LOADED_INITIAL_PREVIOUS

SELECTORS = bytes.fromhex('000102030405060708090a0b0c0d0e0f101112' + 'ff' * 11 + '131415161718191a1b1c1d1e1f2021222324252627' + 'ff' * 39)


def syll(l, v, t=0):return (l * 21 + v) * 28 + t


def parse(w):
    """(l, v, t) for a syllable word, (l, None, 0) for a lone initial word, None otherwise."""
    try:v = R.unword(w)
    except ValueError:return None
    if v < R.NATIVE_BASE:return (v // 588, v % 588 // 28, v % 28)
    if R.JAMO_BASE <= v < R.JAMO_BASE + 19:return (v - R.JAMO_BASE, None, 0)
    return None


def make(l, v, t=0):
    return R.word(syll(l, v, t) if v is not None else R.JAMO_BASE + l)


class Editor:
    def __init__(self, limit, words=(), cursor=None):
        self.limit = limit;self.words = list(words);self.cursor = len(self.words) if cursor is None else cursor

    def _put(self, w):
        if self.cursor == len(self.words):self.words.append(w)
        else:self.words[self.cursor] = w
        self.cursor += 1

    def press(self, jamo):
        """jamo index 0..39 (R.JAMO order). Returns True when accepted (state changed)."""
        key = R.JAMO[jamo];full = len(self.words) >= self.limit
        prev = parse(self.words[self.cursor - 1]) if self.cursor else None
        if key in INITIALS:
            k = INITIALS.index(key)
            if prev is None:
                if full:return False
                self._put(make(k, None));return True
            l, v, t = prev
            if v is None:
                m = INITIAL_MERGE.get((INITIALS[l], key))
                if m is None:return False
                self.words[self.cursor - 1] = make(INITIALS.index(m), None);return True
            if t == 0 and key in FINALS:self.words[self.cursor - 1] = make(l, v, FINALS.index(key));return True
            if t and (FINALS[t], key) in FINAL_MERGE:self.words[self.cursor - 1] = make(l, v, FINALS.index(FINAL_MERGE[FINALS[t], key]));return True
            if full:return False
            self._put(make(k, None));return True
        m = MEDIALS.index(key)
        if prev is None:return False
        l, v, t = prev
        if v is None:self.words[self.cursor - 1] = make(l, m);return True
        if t == 0:
            merged = MEDIAL_MERGE.get((MEDIALS[v], key))
            if merged is None:return False
            self.words[self.cursor - 1] = make(l, MEDIALS.index(merged));return True
        if full:return False
        retained, moved = FINAL_SPLIT.get(FINALS[t], ('', FINALS[t]))
        self.words[self.cursor - 1] = make(l, v, FINALS.index(retained));self._put(make(INITIALS.index(moved), m));return True

    def backspace(self):
        """True when the word before the cursor is Hangul (handled here); False -> native B."""
        prev = parse(self.words[self.cursor - 1]) if self.cursor else None
        if prev is None:return False
        l, v, t = prev
        if t:self.words[self.cursor - 1] = make(l, v, FINALS.index(FINAL_SPLIT.get(FINALS[t], ('',))[0]))
        elif v is not None:
            p = LOADED_MEDIAL_PREVIOUS.get(MEDIALS[v])
            self.words[self.cursor - 1] = make(l, MEDIALS.index(p) if p else None)
        else:
            p = LOADED_INITIAL_PREVIOUS.get(INITIALS[l])
            if p:self.words[self.cursor - 1] = make(INITIALS.index(p), None)
            else:del self.words[self.cursor - 1];self.cursor -= 1
        return True

    def tokens(self):
        out = []
        for w in self.words:
            try:out.append(R.token_of(R.unword(w)))
            except ValueError:out.append(0xE400 | w >> 8 if (w & 0xFF) == 0xE4 else w & 0xFF)
        return out


def tables():
    """Byte tables for the Thumb composer (0xFF = none)."""
    FF = 0xFF
    fin_of_cons = bytes(FINALS.index(c) if c in FINALS else FF for c in INITIALS)
    final_merge = bytes(FINALS.index(FINAL_MERGE[(FINALS[t], INITIALS[k])]) if t and (FINALS[t], INITIALS[k]) in FINAL_MERGE else FF for t in range(28) for k in range(19))
    split = b''.join(bytes([FINALS.index(FINAL_SPLIT.get(FINALS[t], ('', FINALS[t]))[0]), INITIALS.index(FINAL_SPLIT.get(FINALS[t], ('', FINALS[t]))[1]) if t else FF]) for t in range(28))
    medial_merge = bytes(MEDIALS.index(MEDIAL_MERGE[(MEDIALS[a], MEDIALS[b])]) if (MEDIALS[a], MEDIALS[b]) in MEDIAL_MERGE else FF for a in range(21) for b in range(21))
    medial_prev = bytes(MEDIALS.index(LOADED_MEDIAL_PREVIOUS[m]) if m in LOADED_MEDIAL_PREVIOUS else FF for m in MEDIALS)
    tense = bytes(INITIALS.index(INITIAL_MERGE[(c, c)]) if (c, c) in INITIAL_MERGE else FF for c in INITIALS)
    initial_prev = bytes(INITIALS.index(LOADED_INITIAL_PREVIOUS[c]) if c in LOADED_INITIAL_PREVIOUS else FF for c in INITIALS)
    return dict(fin_of_cons=fin_of_cons, final_merge=final_merge, split=split, medial_merge=medial_merge, medial_prev=medial_prev,
                tense=tense, initial_prev=initial_prev, selectors=SELECTORS)
