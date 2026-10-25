"""Real clone name observer: source1..90; diagnostic, not acquired chips."""
from pathlib import Path
from build_visibility_poc import require_hash
import capture_chip_folder_names_batch as previous


def main():
    path=Path(previous.__file__);require_hash(path,'c0be95c44eab6f283eed6c7947d8bae16564e8350dd2aa2211726ddb9d05d049')
    code=path.read_text(encoding='utf-8')
    for old,new in {'%30+1':'%90+1','range(1,31)':'range(1,91)','1..30':'1..90'}.items():
        if old not in code: raise ValueError('missing90-name anchor: '+old)
        code=code.replace(old,new)
    ns={'__name__':'names90_bound','__file__':__file__}
    exec(compile(code,str(path)+' [protected90 binding]','exec'),ns)
    return ns['main']()


if __name__=='__main__': raise SystemExit(main())
