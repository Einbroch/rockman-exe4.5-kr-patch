"""Read-only calendar observer adding RAM glyph-stream visibility for event names."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
import capture_gutsman_calendar_prompts as base
from build_visibility_poc import sha
def main():
    old="if stream<PET_POOL or stream>=PET_END then return end"
    new="if not ((stream>=PET_POOL and stream<PET_END) or (stream>=0x02000000 and stream<0x02040000)) then return end"
    if pet.PROBE.count(old)!=1:raise ValueError('management RAM stream observer anchor')
    pet.PROBE=pet.PROBE.replace(old,new)
    rc=base.main();out=Path(sys.argv[sys.argv.index('--out')+1]);p=out/'calendar_prompts_environment.json';env=json.loads(p.read_text())
    env.update(management_observer_sha256=sha(Path(__file__).read_bytes()),additional_stream_range=[0x02000000,0x02040000],normal_draw_filter='archive OR EWRAM; observer only')
    p.write_text(json.dumps(env,indent=2),encoding='utf8');return rc
if __name__=='__main__':raise SystemExit(main())
