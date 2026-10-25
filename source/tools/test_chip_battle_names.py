"""Exhaustive native helper differential ABI/flags and precise selection gate."""
import json
import unittest
from build_visibility_poc import ROOT,require_hash
from chip_battle_name_extension import construct
from bench_chip_library import REGS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T


class BattleNameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=json.loads((ROOT/'tools/specs/exe45_chip_battle_names_v1.json').read_text())
        source_path=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']
        require_hash(source_path,cls.spec['source_sha256']);cls.source=source_path.read_bytes()

    def test_scope_and_expected_bytes_fail_closed(self):
        for ids in (set(),{0,1},set(range(1,257)),[1,1]):
            with self.assertRaises(ValueError): construct(self.source,self.spec,b'',0xA00000,ids)
        changed=bytearray(self.source);changed[0x1F7D4]^=1
        with self.assertRaises(ValueError): construct(bytes(changed),self.spec,b'',0xA00000,set(range(1,91)))

    def test_machine_code_and_write_extent(self):
        appended,patches,m=construct(self.source,self.spec,b'',0xA00000,set(range(1,91)))
        self.assertEqual(len(patches),1);self.assertEqual((patches[0][0],len(patches[0][1])),(0x1F7D4,8))
        self.assertEqual(m['extra_stack_bytes'],8)
        self.assertTrue(all(p['final_placement_roundtrip'] for p in m['machine_code']))
        self.assertEqual(m['machine_code'][0]['literal_values']['caller'],0x080166AD)

    def test_all512_ids_all_six_callers_native_differential(self):
        self.check_differential(set(range(1,91)))

    def test_sparse249_all512_ids_all_six_callers_native_differential(self):
        self.check_differential(set(range(1,195))|set(range(201,256)))

    def check_differential(self,selected):
        appended,patches,m=construct(self.source,self.spec,b'',0xA00000,selected)
        modified=bytearray(self.source+appended)
        for at,data,_ in patches: modified[at:at+len(data)]=data
        engines=[];stop=[0]
        for blob in (self.source,bytes(modified)):
            uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB);uc.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
            uc.mem_map(0x08000000,0x1000000);uc.mem_write(0x08000000,blob)
            uc.mem_map(0x03000000,0x8000)
            uc.hook_add(UC_HOOK_CODE,lambda u,a,s,d: u.emu_stop() if a==stop[0] else None)
            engines.append(uc)
        callers=[0x08000000+x+5 for x in (0x15BC2,0x166A8,0x17500,0x1F53A,0x1F65E,0x20C80)]
        for caller in callers:
            stop[0]=caller&~1
            for raw in list(range(512))+[0xFFFFFFFF,0x12345601,0x12345701,0x1000001D,0x80000000]:
                results=[]
                values=[raw,0x11223344]+[0x10203040+i for i in range(2,13)]+[0x03007F00,caller]
                for uc in engines:
                    uc.mem_write(0x03007EF4,bytes([0xA7])*24);uc.reg_write(UC_ARM_REG_CPSR,0xA0000030)
                    for reg,value in zip(REGS,values): uc.reg_write(reg,value)
                    uc.emu_start(0x0801F7D5,stop[0],count=120)
                    self.assertEqual(uc.reg_read(UC_ARM_REG_PC),stop[0])
                    self.assertEqual(bytes(uc.mem_read(0x03007EF4,4)),bytes([0xA7])*4)
                    self.assertEqual(bytes(uc.mem_read(0x03007F00,12)),bytes([0xA7])*12)
                    results.append([uc.reg_read(reg) for reg in REGS]+[uc.reg_read(UC_ARM_REG_CPSR)])
                expected=list(results[0]);script=raw&511
                if caller==0x080166AD and script in selected: expected[0]=0x08A00000
                self.assertEqual(results[1],expected,(hex(caller),hex(raw)))


if __name__=='__main__': unittest.main()
