"""Reuse established pixel assertions with explicit v3 artifact bindings."""
from pathlib import Path
import report_chip_folder_pixels as pixels
import report_chip_folder_reentry as reentry


def main():
    substitutions={
        '6790782b403f07f5f850cb985e6aedf012dc8334736b4f9988e4f74379a6fd41':
        '980f26a3de796f96cc8089fbb04082714794dd4c799dac96917f328d6351af35',
        'chip_folder_v2':'chip_folder_v3',
        'chip-folder-v2-normal':'chip-folder-v3-normal-r1',
        'chip-folder-v2-':'chip-folder-v3-',
        'pixels_v2.json':'pixels_v3.json',
        'reentry_v2.json':'reentry_v3.json',
        'guard is source function/count/buffer/base/root; no explicit job/menu guard in v2':
        'explicit context/root-job/menu/phase owner guard; CPU positive and negative owner vectors verified separately',
    }
    for module in (pixels,reentry):
        code=Path(module.__file__).read_text(encoding='utf-8')
        for old,new in substitutions.items():
            code=code.replace(old,new)
        namespace={'__name__':'v3_report_adapter'}
        exec(compile(code,module.__file__+' [v3 bindings]','exec'),namespace)
        namespace['main']()


if __name__=='__main__':
    main()
