"""Materialize conditional500 wording unchanged; no compiler/ROM admission."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
from prepare_batch500_016_inputs import prepare

SELECTION='analysis/pending_insertion_500_019_selection_v1/selection.json'
OUT='analysis/pending_insertion_500_019_inputs_v1'

def main():
    inputs=prepare(SELECTION,OUT,allow_carry=True)
    frozen_write(ROOT/(OUT+'/inputs.json'),dict(schema=1,selection=dict(path=SELECTION,sha256=sha((ROOT/SELECTION).read_bytes())),inputs=inputs,total_new_units=sum(r['units'] for r in inputs),source_wording_unchanged=True,rom_written=False,consumer_admission=False,release_eligible=False,policy='development-draft; NON-DISTRIBUTION',pending=['Native nickname aggregate specification and product compiler gate','Source-only compilation/full script preservation','Cumulative primary-writer ancestry and build registration','New integrated ROM/repro/CPU selection/aggregate runtime verification']))
    print('Materialized',len(inputs),'archives,',sum(r['units'] for r in inputs),'conditional units; no ROM admission')

if __name__=='__main__':main()
