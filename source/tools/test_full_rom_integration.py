"""Scope eligibility contract fixtures; not current-ROM readiness tests."""
import unittest
from report_full_rom_integration import covered


class ScopeTests(unittest.TestCase):
    def test_unregistered_is_not_inferred_from_draft(self):
        self.assertFalse(covered(None,'AA:1:0'))

    def test_pinned_ids_are_authority(self):
        s={'literal_ids':['AA:1:0'],'literal_scripts':[1]}
        self.assertTrue(covered(s,'AA:1:0'))
        self.assertFalse(covered(s,'AA:1:1'))

    def test_explicit_empty_ids_are_not_all_scripts(self):
        self.assertFalse(covered({'literal_ids':[],'literal_scripts':[1]},'AA:1:0'))

    def test_script_scope_without_ids(self):
        s={'literal_scripts':[1,2]}
        self.assertTrue(covered(s,'AA:2:3'))
        self.assertFalse(covered(s,'AA:3:0'))

    def test_complete_flag_does_not_broaden_scope(self):
        self.assertFalse(covered({'complete_literal_scope':True,'literal_scripts':[0]},'AA:1:0'))


if __name__=='__main__':unittest.main()
