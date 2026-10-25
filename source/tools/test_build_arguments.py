"""Lossless argv transport fixtures, independent of current ROM values."""
import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import build_arguments as arguments
class ArgumentTests(unittest.TestCase):
    def test_lossless_unicode_whitespace_quotes_and_repeated_flags(self):
        values=['--translations','번역 경로/a.json','--translations','quoted"path','--work','back\\slash','']
        with tempfile.TemporaryDirectory() as td,patch.object(arguments,'ROOT',Path(td)):
            path=Path(td)/'args.json';digest=arguments.save(path,values)
            result,link=arguments.expand(['--argument-file','args.json','--argument-file-sha256',digest])
            self.assertEqual(result,values);self.assertEqual(link['sha256'],digest)
            with self.assertRaises(ValueError):arguments.save(path,['changed'])
    def test_unknown_fields_and_types_reject(self):
        for value in [{'schema':True,'args':[]},{'schema':1,'args':[2]},{'schema':1,'args':['\0']},{'schema':1,'args':[],'extra':True}]:
            with self.subTest(value=value),self.assertRaises(ValueError):arguments.validate(value)
    def test_nested_and_mixed_invocations_reject(self):
        with self.assertRaises(ValueError):arguments.expand(['--argument-file','file','--out','foo'])
        with tempfile.TemporaryDirectory() as td,patch.object(arguments,'ROOT',Path(td)):
            digest=arguments.save(Path(td)/'args.json',['--argument-file'])
            with self.assertRaises(ValueError):arguments.expand(['--argument-file','args.json','--argument-file-sha256',digest])
    def test_direct_arguments_unchanged(self):
        self.assertEqual(arguments.expand(['--out','a']),(['--out','a'],None))
if __name__=='__main__':unittest.main()
