"""Actual native writer adverse CPU fixtures; no game state or ROM edits."""
import json,struct
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from bench_hangul_record_decoder import Uc,UC_ARCH_ARM,UC_MODE_THUMB
from unicorn.arm_const import *
from korean_codec import encode_hangul

def main():
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';identity='5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4';require_hash(product,identity);rom=product.read_bytes()
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(rom)+4095)&~4095);u.mem_write(0x08000000,rom);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    source=0x0200fc80;destination=0x020010a6;temporary=0x02014e74;count=0;truncated=[]
    def run(body):
        u.mem_write(source,body);u.mem_write(destination,b'\xa7'*32);u.mem_write(temporary,b'\xa7'*64);u.mem_write(0x0200fc5c,struct.pack('<I',destination))
        u.reg_write(UC_ARM_REG_CPSR,0x30);u.reg_write(UC_ARM_REG_SP,0x03007f00);u.reg_write(UC_ARM_REG_LR,0x08001235)
        u.emu_start(0x08035001,0x08035030,count=1000)
        if u.reg_read(UC_ARM_REG_PC)!=0x08035030:raise ValueError('native writer observation boundary')
        return bytes(u.mem_read(destination,32)),bytes(u.mem_read(temporary,64))
    for rank in range(11172):
        text=chr(0xac00+rank);body=encode_hangul(text)+b'\xe5';record,temp=run(body)
        cut=next(i for i,value in enumerate(body) if value in [0xe5,0x98]);expected=body[:cut]+b'\xe5'
        if record!=b'\x01'+expected+b'\xa7'*(31-len(expected)) or not temp.startswith(expected):raise ValueError('native adverse result')
        if expected!=body:truncated.append(dict(rank=rank,character=text,input_hex=body.hex(),copied_hex=expected.hex()))
        count+=1
    wide=encode_hangul('가가가가')+b'\xe5';record,temp=run(wide)
    if record[:18]!=b'\x01'+wide or record[18:]!=b'\xa7'*14:raise ValueError('native overflow reproduction')
    out=ROOT/'analysis/hangul_keyboard_v1/native_storage_risks.json'
    report=dict(id='exe45.hangul-keyboard.native-storage-risk.v1',passed=True,meaning='risk reproduction assertions passed, NOT Hangul feature validation',rom_sha256=identity,tool_sha256=sha(Path(__file__).read_bytes()),writer_range_sha256=sha(rom[0x35000:0x35034]),vectors=count,truncated_syllables=len(truncated),truncated_examples=truncated,overflow=dict(input='가가가가',record_bytes_written=18,observed_field_stride=10,bytes_beyond_field=8,record_hex=record[:18].hex()),limits=['Synthetic CPU caller with source/destination fixture; not normal-play Hangul input or native save test.','Stops at08035030 before outer return; no whole-function ABI claim.','Expected failure of direct F9FC storage; no source/product/save mutation or repair installed.'])
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print('native storage risk reproduced:',len(truncated),'truncated syllables; four-syllable overflow8 bytes')

if __name__=='__main__':main()
