"""Cursor-aware mixed editor HOST candidate, not ROM/state/save ABI.

Preserves native-token overwrite/delete and imported cursor0. New Hangul
composition follows the existing L/V/T model, replacing at the caret and
carrying into the next cell (overwrite, not insertion). Successful movement
seals composition without losing partial initials; confirmation rejects any
partial anywhere. Accepted-key undo runs before canonical Hangul deletion.
History consists of host snapshots (max70), NOT allocated game memory.
"""
from dataclasses import dataclass
from hangul_keyboard_model import Composer, State, transition, INITIALS, MEDIALS
from hangul_composer_thumb import state_from_rank, tail_rank, EMPTY
from hangul_native_tokens import tag, untag


def validate_word(word):
    if type(word) != int:
        raise ValueError('mixed word type')
    if 0 <= word < 11191:
        return
    untag(word)


@dataclass(frozen=True)
class Snapshot:
    cells: tuple
    cursor: int
    active: int | None


class MixedEditor:
    def __init__(self, capacity):
        if type(capacity) != int or not 1 <= capacity <= 10:
            raise ValueError('mixed capacity')
        self.capacity = capacity
        self.state = Snapshot((), 0, None)
        self.history = []

    def _validate(self, s):
        if type(s.cells) != tuple or len(s.cells) > self.capacity or type(s.cursor) != int or not 0 <= s.cursor <= len(s.cells):
            raise ValueError('mixed count/cursor')
        for w in s.cells:
            validate_word(w)
        if s.active is not None:
            if type(s.active) != int or not 0 <= s.active < len(s.cells) or s.cells[s.active] >= 11191 or s.cursor != s.active + 1:
                raise ValueError('mixed active cell')

    def load(self, cells):
        s = Snapshot(tuple(cells), 0, None)
        self._validate(s)
        if any(11172 <= w < 11191 for w in s.cells):
            raise ValueError('partial cannot be imported as committed')
        self.state = s
        self.history = []

    def move(self, delta):
        s = self.state
        if type(delta) != int or delta not in (-1, 1) or not 0 <= s.cursor + delta <= len(s.cells):
            return False
        self.state = Snapshot(s.cells, s.cursor + delta, None)
        self.history = []
        return True

    def press(self, key):
        if type(key) != str or key not in INITIALS + MEDIALS or len(self.history) >= 70:
            return False
        s = self.state
        p = s.cursor if s.active is None else s.active
        try:
            n = transition(State() if s.active is None else state_from_rank(s.cells[p]), key, 2)
            replacements = [ord(ch) - 0xAC00 for ch in n.committed] + [tail_rank(n)]
            if p + len(replacements) > self.capacity:
                return False
            cells = list(s.cells)
            for i, word in enumerate(replacements, p):
                if i < len(cells):
                    cells[i] = word
                else:
                    cells.append(word)
            active = p + len(replacements) - 1
            after = Snapshot(tuple(cells), active + 1, active)
            self._validate(after)
        except ValueError:
            return False
        self.history.append(s)
        self.state = after
        return True

    def write_native(self, token):
        s = self.state
        try:
            word = tag(token)
        except ValueError:
            return False
        if s.cursor >= self.capacity:
            return False
        cells = list(s.cells)
        if s.cursor < len(cells):
            cells[s.cursor] = word
        else:
            cells.append(word)
        self.state = Snapshot(tuple(cells), s.cursor + 1, None)
        self.history = []
        return True

    def backspace(self):
        s = self.state
        if s.active is not None and self.history:
            self.state = self.history.pop()
            return True
        if not s.cells:
            return False
        p = s.active if s.active is not None else max(0, s.cursor - 1)
        word = s.cells[p]
        cells = list(s.cells)
        if word >= 11191:
            cells.pop(p)
            after = Snapshot(tuple(cells), max(0, s.cursor - 1), None)
        else:
            c = Composer(1)
            c.state = state_from_rank(word)
            if not c.backspace():
                return False
            previous = tail_rank(c.state) if c.state.l is not None else EMPTY
            if previous == EMPTY:
                cells.pop(p)
                after = Snapshot(tuple(cells), min(p, len(cells)), None)
            else:
                cells[p] = previous
                after = Snapshot(tuple(cells), p + 1, p)
        self._validate(after)
        self.state = after
        self.history = []
        return True

    def candidate(self):
        self._validate(self.state)
        if not self.state.cells or any(11172 <= w < 11191 for w in self.state.cells):
            raise ValueError('empty/unfinished mixed answer')
        # Internal complete words only. This does NOT serialize a save record.
        return self.state.cells
