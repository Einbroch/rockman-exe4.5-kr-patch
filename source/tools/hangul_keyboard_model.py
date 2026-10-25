"""Host reference for automatic Hangul composition; NOT ROM-integrated code.

User selected automatic composition. Final native field format/capacity and
UI mapping remain unadopted; logical_limit is an explicit caller parameter.
Input domain: 19 consonant selectors, 21 vowel selectors, B and confirmation.
Incomplete standalone vowels/consonants cannot enter a committed record.
"""
from dataclasses import dataclass,replace

INITIALS=tuple('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
MEDIALS=tuple('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
FINALS=('',*tuple('ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ'))
FINAL_MERGE={('ㄱ','ㅅ'):'ㄳ',('ㄴ','ㅈ'):'ㄵ',('ㄴ','ㅎ'):'ㄶ',('ㄹ','ㄱ'):'ㄺ',('ㄹ','ㅁ'):'ㄻ',('ㄹ','ㅂ'):'ㄼ',('ㄹ','ㅅ'):'ㄽ',('ㄹ','ㅌ'):'ㄾ',('ㄹ','ㅍ'):'ㄿ',('ㄹ','ㅎ'):'ㅀ',('ㅂ','ㅅ'):'ㅄ'}
FINAL_SPLIT={c:ab for ab,c in FINAL_MERGE.items()}
MEDIAL_MERGE={('ㅗ','ㅏ'):'ㅘ',('ㅗ','ㅐ'):'ㅙ',('ㅗ','ㅣ'):'ㅚ',('ㅜ','ㅓ'):'ㅝ',('ㅜ','ㅔ'):'ㅞ',('ㅜ','ㅣ'):'ㅟ',('ㅡ','ㅣ'):'ㅢ',('ㅘ','ㅣ'):'ㅙ',('ㅝ','ㅣ'):'ㅞ'}
INITIAL_MERGE={(c,c):d for c,d in [('ㄱ','ㄲ'),('ㄷ','ㄸ'),('ㅂ','ㅃ'),('ㅅ','ㅆ'),('ㅈ','ㅉ')]}
LOADED_MEDIAL_PREVIOUS={combined:first for (first,second),combined in MEDIAL_MERGE.items()}
LOADED_INITIAL_PREVIOUS={combined:first for (first,second),combined in INITIAL_MERGE.items()}

def syllable(l,v,t=0):
    if any(type(x)!=int for x in [l,v,t]) or not (0<=l<19 and 0<=v<21 and 0<=t<28):raise ValueError('invalid syllable indices')
    return chr(0xac00+(l*21+v)*28+t)

@dataclass(frozen=True)
class State:
    committed:tuple[str,...]=()
    l:int|None=None
    v:int|None=None
    t:int=0

    def validate(self,limit):
        if type(limit)!=int or not 1<=limit<=64 or type(self.committed)!=tuple or len(self.committed)>limit:raise ValueError('logical capacity')
        if any(type(c)!=str or len(c)!=1 or not 0xac00<=ord(c)<=0xd7a3 for c in self.committed):raise ValueError('invalid committed character')
        if self.l is None:
            if self.v is not None or self.t!=0:raise ValueError('partial state without initial')
        elif type(self.l)!=int or not 0<=self.l<19 or len(self.committed)>=limit:raise ValueError('initial/occupied slots')
        if self.v is None:
            if self.t!=0:raise ValueError('final without medial')
        elif type(self.v)!=int or not 0<=self.v<21:raise ValueError('medial')
        if type(self.t)!=int or not 0<=self.t<28:raise ValueError('final')

    @property
    def display(self):
        tail='' if self.l is None else INITIALS[self.l] if self.v is None else syllable(self.l,self.v,self.t)
        return ''.join(self.committed)+tail

def transition(s,key,limit):
    """Pure atomic step; raises on invalid action, leaving caller state intact."""
    s.validate(limit)
    if type(key)!=str or key not in INITIALS+MEDIALS:raise ValueError('inactive/unknown selector')
    if key in INITIALS:
        l=INITIALS.index(key)
        if s.l is None:n=replace(s,l=l)
        elif s.v is None:
            merged=INITIAL_MERGE.get((INITIALS[s.l],key))
            if merged is None:raise ValueError('initial needs medial')
            n=replace(s,l=INITIALS.index(merged))
        elif s.t==0 and key in FINALS:n=replace(s,t=FINALS.index(key))
        elif s.t!=0 and (FINALS[s.t],key) in FINAL_MERGE:n=replace(s,t=FINALS.index(FINAL_MERGE[FINALS[s.t],key]))
        else:n=State(s.committed+(syllable(s.l,s.v,s.t),),l,None,0)
    else:
        v=MEDIALS.index(key)
        if s.l is None:raise ValueError('medial needs initial')
        if s.v is None:n=replace(s,v=v)
        elif s.t==0:
            merged=MEDIAL_MERGE.get((MEDIALS[s.v],key))
            if merged is None:raise ValueError('medial cannot combine')
            n=replace(s,v=MEDIALS.index(merged))
        else:
            final=FINALS[s.t]
            retained,moved=FINAL_SPLIT.get(final,('',final))
            n=State(s.committed+(syllable(s.l,s.v,FINALS.index(retained)),),INITIALS.index(moved),v,0)
    n.validate(limit);return n

class Composer:
    def __init__(self,logical_limit):
        self.limit=logical_limit;self.state=State();self.state.validate(self.limit);self.history=[]
    def press(self,key):
        try:n=transition(self.state,key,self.limit)
        except ValueError:return False
        self.history.append(self.state);self.state=n;return True
    def backspace(self):
        if self.history:
            self.state=self.history.pop();return True
        s=self.state
        if s.l is None:
            if not s.committed:return False
            s=self._loaded_state(''.join(s.committed))
        if s.t:
            prior=FINAL_SPLIT.get(FINALS[s.t],('',))[0]
            n=replace(s,t=FINALS.index(prior))
        elif s.v is not None:
            prior=LOADED_MEDIAL_PREVIOUS.get(MEDIALS[s.v])
            n=replace(s,v=None if prior is None else MEDIALS.index(prior))
        else:
            prior=LOADED_INITIAL_PREVIOUS.get(INITIALS[s.l])
            n=replace(s,l=INITIALS.index(prior)) if prior else State(s.committed)
        n.validate(self.limit);self.state=n;return True
    def _loaded_state(self,text):
        if type(text)!=str or len(text)>self.limit or any(not 0xac00<=ord(c)<=0xd7a3 for c in text):raise ValueError('invalid loaded Hangul text')
        if not text:return State()
        index=ord(text[-1])-0xac00
        n=State(tuple(text[:-1]),index//588,(index%588)//28,index%28)
        n.validate(self.limit);return n
    def load(self,text):
        """Host import only. Validate atomically; no native save decoding.

        Original key history is unknowable after load. B then removes canonical
        final/medial/initial components, e.g. 괙->괘->과->고->ㄱ->empty.
        Newly accepted input still uses exact action-history undo first.
        """
        n=self._loaded_state(text);self.state=n;self.history=[]
    def candidate(self):
        """No mutation; native confirmation cancel can retain exact edit state."""
        self.state.validate(self.limit);s=self.state
        if s.l is not None and s.v is None:raise ValueError('unfinished initial cannot confirm')
        chars=s.committed+(() if s.l is None else (syllable(s.l,s.v,s.t),))
        if not chars:raise ValueError('empty answer cannot confirm')
        return ''.join(chars)
    @property
    def display(self):return self.state.display
