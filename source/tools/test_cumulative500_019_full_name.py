"""Reject mismatched receipts, glyph models and wait boundaries without editing evidence."""
import copy
import unittest
from unittest.mock import patch
import verify_cumulative500_019_full_name as qa

class FailClosed(unittest.TestCase):
    def receipt_change(self,key,value):
        original=qa.read
        def read(p):
            r=original(p)
            if str(p).replace('\\','/').endswith('pending500-019-v1-name-food/result.json'):
                r=copy.deepcopy(r)
                if key=='script':r['display_diagnostic']['script']=value
                else:r[key]=value
            return r
        with patch.object(qa,'read',read),self.assertRaisesRegex(ValueError,'Diagnostic identity'):
            qa.main()
    def test_foreign_rom_receipt(self):self.receipt_change('rom_sha256','0'*64)
    def test_wrong_script_receipt(self):self.receipt_change('script',24)
    def model_change(self,part):
        original=qa.model
        def model(*a,**k):
            p,u,e,s,w=original(*a,**k)
            if part=='glyph':
                first=s[u[0]['id']][0];e[first]=dict(e[first],index=e[first]['index']+1)
            else:w[u[0]['id']]+=1
            return p,u,e,s,w
        with patch.object(qa,'model',model),self.assertRaises(ValueError):qa.main()
    def test_wrong_glyph_model(self):self.model_change('glyph')
    def test_wrong_wait_model(self):self.model_change('wait')

if __name__=='__main__':unittest.main()
