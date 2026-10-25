"""Controlled blank-row space reproduction, no product artifact claim."""
from canonical_literals_031 import canonical_literals
from tpl_literals import literals


def main():
    values=[')\n ',')\n  ',')\n \n','\n \nA ','A\n\n',' A\n B','일정\n ']
    for value in values:
        source='@archive ABCDEF\n@size 1\nscript 0 mmbn45 {\n\t"'+value.replace('\n','\\n')+'"\n\tend\n}\n'
        actual=canonical_literals(source)
        if literals(actual)[0].text!=value or canonical_literals(actual)!=actual:raise ValueError('031 explicit LF/space fixture')
    print('031 lossless literal representation PASS',len(values),'controlled fixtures; binary roundtrip remains separate')


if __name__=='__main__':main()
