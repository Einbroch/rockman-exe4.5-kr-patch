"""Small exact-ROM loaded-memory sentinels, not a full loaded-ROM hash claim."""
from build_visibility_poc import ROOT,require_hash
from keyitem_rom_selector import INSTALL


def arguments(rom,meta):
    require_hash(ROOT/rom,meta['output_sha256']);blob=(ROOT/rom).read_bytes();n=meta['keyitem_rom']['npc037'];result=[]
    for at,size in [(0,0xC0),(INSTALL,12),(n['code_offset'],n['code_bytes']),(n['descriptor_offset'],len(n['placements'])*28)]:
        result+=['--guard',hex(at)+':'+blob[at:at+size].hex()]
    return result
