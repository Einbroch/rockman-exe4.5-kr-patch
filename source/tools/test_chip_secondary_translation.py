"""Source-bound secondary name drafts, not a runtime integration test."""
import struct
import unittest
from build_visibility_poc import ROOT,sha
from report_chip_library_runtime import read
from prepare_chip_secondary_names import prepare
from tpl_literals import resolve_units,literals,replace_literals,skeleton
from archive_scripts import script_spans,verify_untouched_scripts
from chip_library_extension import encode_name,decode_name

class SecondaryNames(unittest.TestCase):
    def test_all_real_names_preserve_source_and_codec(self):
        asset=read(ROOT/'translations/chip_secondary_names_ko.json')
        self.assertEqual(asset,prepare())
        self.assertEqual(len(asset['units']),98)
        self.assertFalse(asset['review']['release_eligible'])
        tpl=(ROOT/asset['extraction']['path']).read_text(encoding='utf-8-sig')
        source=ROOT/read(ROOT/'project.json')['source_profile']['filename']
        native=source.read_bytes()[0x765B18:0x765B18+1103]
        self.assertEqual(sha(native),asset['source_archive_sha256'])
        spans=script_spans(native,137);original=list(spans)
        table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
        selected=set()
        for unit in resolve_units(asset):
            i=int(unit['id'].split(':')[1]);selected.add(i)
            self.assertEqual(unit['state'],'needs_review')
            self.assertEqual(spans[i].hex(),asset['source_script_hex'][str(i)])
            self.assertEqual(decode_name(spans[i],table),unit['source'])
            encoded=encode_name(unit['translation'],table)
            self.assertEqual(decode_name(encoded,table),unit['translation'])
            spans[i]=encoded
        target=replace_literals(tpl,resolve_units(asset),language='mmbn45s')
        self.assertEqual(skeleton(tpl),skeleton(target))
        before={x.key:x.text for x in literals(tpl)};after={x.key:x.text for x in literals(target)}
        self.assertTrue(all(before[k]==after[k] for k in before if int(k.split(':')[1]) not in selected))
        self.assertEqual(after['765B18:113:0'],'????')
        self.assertEqual(after['765B18:132:0'],' ')
        offsets=bytearray();position=137*2
        for blob in spans:
            offsets.extend(struct.pack('<H',position));position+=len(blob)
        clone=bytes(offsets)+b''.join(spans)
        self.assertEqual(script_spans(clone,137),spans)
        self.assertEqual(len(verify_untouched_scripts(native,clone,137,selected)),39)
        self.assertEqual(original[113],spans[113]);self.assertEqual(original[132],spans[132])

if __name__=='__main__':unittest.main()
