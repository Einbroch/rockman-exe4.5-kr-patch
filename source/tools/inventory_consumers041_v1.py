"""Finite selected lookup inventory and unresolved native boundaries, no hooks."""
import struct
from collections import defaultdict,Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from compare_archive_payloads import payload_of
from consumer_links040_v1 import contracts,CLASSES

SOURCE='analysis/pending_insertion_500_041_source_v7'


def main():
    s=read(SOURCE+'/selection.json');cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();contracts(source);groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    rows=[];counts=Counter()
    for arc,gs in sorted(groups.items()):
        row=gs[0]['source_row'];native=payload_of(source,row);refs=[]
        if sha(native)!=gs[0]['source_archive_sha256']:raise ValueError('041 immutable selected native payload')
        for p in row['pointers']:
            old=struct.unpack_from('<I',source,p)[0];now=struct.unpack_from('<I',rom,p)[0]
            if old!=0x08000000+row['offset']:raise ValueError('041 source pointer coordinate '+arc)
            refs.append(dict(pointer=p,original_target=old,current040_target=now,changed_in040=old!=now))
        ps=row['pointers'];known=None
        if arc=='6E93C8':family='tournament-main';known=CLASSES['compressed-normal']
        elif arc=='7028FC':family='battle-BBS';known=CLASSES['battle-BBS-trial']
        elif arc=='6DD0B8':family='mail-notification-table41140'
        elif ps and all(0x3C5BC<=p<=0x3C614 for p in ps):family='equipment-table3C5BC'
        elif ps and all(0x41F38<=p<=0x41F90 for p in ps):family='folder-table41F38'
        elif arc=='6EAD18':family='tournament-secondary-table479F8'
        elif ps and all(0x53E00<=p<0x54000 for p in ps):family='field-source-table53Exx'
        elif not ps:family='pointerless-source-unresolved'
        else:family='other-source-references-unresolved'
        n=sum(g['units'] for g in gs);counts[family]+=n;rows.append(dict(archive=arc,new_units=n,scripts=[g['script'] for g in gs],source_classes=sorted({g['source_class'] for g in gs}),source_row=row,native_bytes=len(native),native_sha256=sha(native),source_lookup_references=refs,family_by_finite_pointer_membership=family,previous040_source_ABI=known,qualified041_runtime_verified=False,product_admitted=False,next_required='Bind real original loader/caller/RAM lifetime/default geometry to exact current native payload; qualify new layouts on cumulative041 after primary/repro. Known040 ABI alone does not prove new041 positions/branches.'))
    if sum(counts.values())!=500 or len(rows)!=54:raise ValueError('041 source family denominator')
    frozen_write(ROOT/SOURCE/'consumer_inventory_v1.json',dict(status='041_SELECTED_SOURCE_LOOKUP_INVENTORY_NOT_RUNTIME_ADMISSION',baseline_sha256=s['baseline_sha256'],source_sha256=sha(source),new_units=500,archives=54,family_unit_counts=dict(counts),rows=rows,rom_written=False,product_admitted=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in [SOURCE+'/selection.json','tools/inventory_consumers041_v1.py','tools/consumer_links040_v1.py']},limits=['Pointer-table membership labels are not complete caller/runtime proofs.','7794EC has no adopted TPI pointer: actual lookup/reader remains unresolved and must not be silently omitted.','Default quick origin, new positioned windows, choice input/outcomes, shared RAM and prior consumers require connected proof before500 admission.']))
    print('041 finite source lookup families',dict(counts),'NO ROM/hooks/runtime admission')


if __name__=='__main__':main()
