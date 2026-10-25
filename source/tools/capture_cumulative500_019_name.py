"""Guarded PET read aliases for two name-boundary pages, not event proof."""
import capture_pending500_005_display as capture
from capture_roll_return import PROBE
capture.CASES={'comma':('65B74C',25,2,bytes.fromhex('f6000a0c01e702f6025c6e03')),'honorific':('6B5A70',4,1,bytes.fromhex('f6000a0c01e702f6025c6e03')),'food':('66BF44',28,23,bytes.fromhex('f4002be700'))}
capture.pet.PROBE+=PROBE.replace('RETURN_POOL','PET_POOL')
anchor='local function capture(name)\n'
if capture.pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('RAM nickname capture anchor')
capture.pet.runner.LUA_TEMPLATE=capture.pet.runner.LUA_TEMPLATE.replace(anchor,anchor+' dumpReturn(name)\n',1)
if __name__=='__main__':raise SystemExit(capture.main())
