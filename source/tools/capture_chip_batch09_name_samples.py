"""Seven held real primary clone names, diagnostic descriptor read aliases."""
from pathlib import Path
import capture_chip_folder_names_batch as previous

SCRIPTS=[187,201,202,219,236,251,255]

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    old='local id=(math.floor((folderBatchEpoch-1)/30)*7+row)%30+1'
    new='local choices={'+','.join(map(str,SCRIPTS))+'}\n local id=choices[row+1]'
    changes={old:new,'range(1,31)':'list(range(1,195))+list(range(201,256))',
             "d['epochs']>150":"d['epochs']>=30",'covered==selected':'covered==set('+repr(SCRIPTS)+')',
             '1..30':'representative7-of249','pages held 30 updates':'fixed sample page; real clone bytes'}
    for old,new in changes.items():
        if old not in code:raise ValueError('name sample anchor:'+old)
        code=code.replace(old,new)
    ns={'__name__':'batch09_name_samples','__file__':__file__}
    exec(compile(code,previous.__file__+' [seven real names]','exec'),ns)
    return ns['main']()

if __name__=='__main__':raise SystemExit(main())
