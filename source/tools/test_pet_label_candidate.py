import unittest
from build_visibility_poc import ROOT
from qa_pet_label_candidate import inspect_candidate

class PetCandidateGate(unittest.TestCase):
    def test_native_reference_and_rejected_candidate(self):
        folder=ROOT/'analysis/pet_labels_v1';ref=folder/'native_reference_8x.png'
        self.assertTrue(inspect_candidate(ref,ref)['technical_pass'])
        result=inspect_candidate(ref,folder/'candidate_01.png')
        self.assertFalse(result['technical_pass'])
        self.assertFalse(result['checks']['canvas_equal'])
        self.assertFalse(result['rom_injection_authorized_by_this_report'])

if __name__=='__main__':unittest.main()
