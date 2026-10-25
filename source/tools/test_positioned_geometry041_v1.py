"""Finite positioned analysis contract fixtures; no current-product proof."""
from positioned_normal_geometry041_v1 import validate


def fixture(top=14,portrait=34,box=0,distance=4,arrow=45,x=225):
    return ('@archive TEST\n@size 1\nscript 0 mmbn45 {\n'
        '\tpositionMugshot\n\t\tleft = 27\n\t\ttop = '+str(portrait)+'\n'
        '\tpositionBox\n\t\tleft = 0\n\t\ttop = '+str(box)+'\n\t\ttype = 0\n'
        '\tmsgOpen\n\tpositionText\n\t\tleft = 52\n\t\ttop = '+str(top)+'\n\t\tarrowDistance = '+str(distance)+'\n'
        '\tpositionArrow\n\t\tleft = '+str(x)+'\n\t\ttop = '+str(arrow)+'\n'
        '\tmugshotShow\n\t\tmugshot = MegaMan\n\t"안녕"\n\tkeyWait\n\t\tany = false\n\tend\n}\n')


def main():
    count=0
    for args in [(),(110,130,12,3,141),(30,50,2,3,61,221)]:
        source=fixture(*args);p=validate(source,source,[0],{'TEST:0:0'})
        assert p[0]['origin']==[52,args[0] if args else 14];count+=1
    valid=fixture()
    bad=[fixture(top=15),fixture(arrow=46),fixture(x=221),fixture(distance=3),fixture(box=1),fixture(portrait=50),valid.replace('\tmsgOpen\n','\tmsgOpenQuick\n'),valid.replace('\tend\n','\tpositionText\n\t\tleft = 52\n\t\ttop = 14\n\t\tarrowDistance = 4\n\tend\n'),valid.replace('안녕','가'*16),valid.replace('\tend\n','\tprintCurrentNavi\n\tend\n')]
    for text in bad:
        try:validate(text,text,[0],{'TEST:0:0'})
        except ValueError:count+=1
        else:raise AssertionError('unsafe positioned fixture accepted')
    try:validate(valid,valid.replace('top = 14','top = 110'),[0],{'TEST:0:0'})
    except ValueError:count+=1
    else:raise AssertionError('source geometry mutation accepted')
    print('PASS041 positioned analysis fixtures',count,'(no runtime/product claim)')


if __name__=='__main__':main()
