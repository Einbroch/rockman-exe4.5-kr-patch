"""Eight loaded-ROM sentinels including040 code/descriptors, NOT full ROM hash."""
from communication039_loaded_guards import arguments as prior
from build_visibility_poc import ROOT


def arguments(rom,meta):
    result=prior(rom,meta);blob=(ROOT/rom).read_bytes();n=meta['keyitem_rom']['typed040']
    for at,size in [(n['code_offset'],n['code_bytes']),(n['descriptor_offset'],len(n['placements'])*28)]:result+=['--guard',hex(at)+':'+blob[at:at+size].hex()]
    return result
