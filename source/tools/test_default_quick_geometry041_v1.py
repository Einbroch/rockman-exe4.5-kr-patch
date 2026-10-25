"""Conditional layout contract fixtures, NOT caller or runtime evidence."""
from default_quick_geometry041_v1 import validate


def main():
    s='@archive TEST\n@size 1\nscript 0 mmbn45 {\n\tcallSkipMugshotFadeIn\n\tmsgOpenQuick\n\ttextSpeed\n\t\tdelay = 0\n\tmugshotShow\n\t\tmugshot = MegaMan\n\t"메일이 왔어"\n\tkeyWait\n\t\tany = false\n\tend\n}\n'
    p=validate(s,s,[0],{'TEST:0:0'})[0]
    assert p['assumed_origin']==[52,110] and p['caller_default_origin_binding_required'] and p['product_admitted'] is False
    tests=[s.replace('\tcallSkipMugshotFadeIn\n',''),s.replace('\tmsgOpenQuick\n','\tmsgOpen\n'),s.replace('\ttextSpeed\n','\tmsgOpenQuick\n\ttextSpeed\n'),s.replace('\ttextSpeed\n','\tpositionText\n\t\tleft = 52\n\t\ttop = 110\n\t\tarrowDistance = 3\n\ttextSpeed\n'),s.replace('\tend\n','\tprintCurrentNavi\n\tend\n'),s.replace('메일이 왔어','가'*16)]
    for t in tests:
        try:validate(t,t,[0],{'TEST:0:0'})
        except ValueError:pass
        else:raise AssertionError('unsafe quick fixture accepted')
    print('PASS041 default quick conditional geometry fixtures',1+len(tests),'no caller/runtime claim')


if __name__=='__main__':main()
