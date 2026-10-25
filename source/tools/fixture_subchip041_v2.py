"""CPU-memory consumer of actual component write plan; never primary ROM input."""
from fixture_subchip041_v1 import construct as comparison,SOURCE
from subchip_rom_component041_v1 import plan
from keyitem_rom_selector import INSTALL
from build_visibility_poc import sha


def construct():
    source,base,meta,expected,guards,f=comparison();p=plan(source,sha(source),len(base),f['previous_wrapper_address'],guards)
    if p['expected_predecessor_stub']!=base[INSTALL:INSTALL+12]:raise ValueError('041 component actual predecessor identity')
    image=bytearray(base);image[INSTALL:INSTALL+12]=p['stub'];image.extend(p['tail']);image=bytes(image)
    if image!=expected or p['audit']['code_address']!=f['code_address'] or p['audit']['descriptor_address']!=f['descriptor_address']:raise ValueError('041 component plan and independently built fixture disagree')
    f=dict(f,component_plan=p['audit'],independent_component_plan_equal=True)
    return source,base,meta,image,guards,f
