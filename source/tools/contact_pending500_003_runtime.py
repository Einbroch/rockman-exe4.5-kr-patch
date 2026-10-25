"""Review montage of exact-ROM native screenshots; not translated graphics."""
import argparse,json
from PIL import Image
from build_visibility_poc import ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--folder',default='analysis/pending_insertion_500_003_rom');parser.add_argument('--prefix',default='pending500-003-v2');parser.add_argument('--report',default='normal_runtime_v1.json');a=parser.parse_args()
    p=ROOT/a.folder;r=json.loads((p/a.report).read_text(encoding='utf8'))
    pages=r['first_mail_body_pages'][:23];sheet=Image.new('RGB',(1200,800))
    for i,page in enumerate(pages):
        sheet.paste(Image.open(ROOT/f"poc/runtime/{a.prefix}-read/step_{page['step']:03}.png"),(i%5*240,i//5*160))
    out=p/'first_mail_pages_v1.png'
    if out.exists():raise ValueError('Preserve prior screenshot montage')
    sheet.save(out);print(out)

if __name__=='__main__':main()
