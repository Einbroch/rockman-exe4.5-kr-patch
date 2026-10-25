"""Six loaded-ROM sentinel ranges; NOT a complete loaded-ROM hash claim."""
from native038_loaded_guards import arguments as prior
from build_visibility_poc import ROOT


def arguments(rom,meta):
    result=prior(rom,meta);blob=(ROOT/rom).read_bytes();n=meta['keyitem_rom']['communication039']
    for at,size in [(n['code_offset'],n['code_bytes']),(n['descriptor_offset'],len(n['placements'])*16)]:result+=['--guard',hex(at)+':'+blob[at:at+size].hex()]
    return result
