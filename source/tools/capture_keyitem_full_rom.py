"""Read-only full-ROM selector and native normal-font consumer observer."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
import capture_keyitem_empty as base
from build_visibility_poc import sha

def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());k=m['keyitem_rom'];root=0x08000000+k['rom_offset']
    old='if stream<PET_POOL or stream>=PET_END then return end'
    new=f'if not ((stream>=PET_POOL and stream<PET_END) or (stream>={root} and stream<{root+k["rom_bytes"]}) or (stream>=0x02000000 and stream<0x02040000)) then return end'
    if pet.PROBE.count(old)!=1:raise ValueError('full-ROM observer anchor')
    pet.PROBE=pet.PROBE.replace(old,new)
    # Use the same PET/fixed probes with a ROM-specific stream filter.
    import capture_gutsman_calendar_management as management
    import capture_gutsman_calendar_prompts as prompts
    management.main=prompts.main
    rc=base.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'keyitem_full_rom_environment.json').write_text(json.dumps(dict(observer_only=True,rom_sha256=m['output_sha256'],root=root,bytes=k['rom_bytes'],self_sha256=sha(Path(__file__).read_bytes())),indent=2)+'\n',encoding='utf8')
    return rc
if __name__=='__main__':raise SystemExit(main())
