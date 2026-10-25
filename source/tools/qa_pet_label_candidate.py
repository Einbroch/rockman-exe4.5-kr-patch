"""Fail-closed candidate geometry/palette/protection gate; no image edits."""
import json
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha

def inspect_candidate(source,candidate):
    a=Image.open(source).convert('RGBA');b=Image.open(candidate).convert('RGBA')
    checks={'canvas_equal':a.size==b.size,'palette_subset':set(b.get_flattened_data())<=set(a.get_flattened_data()),
        'protected_pixels_equal':None,'alpha_equal':None,'nearest_neighbor_8x_grid':None}
    if checks['canvas_equal']:
        checks['alpha_equal']=a.getchannel('A').tobytes()==b.getchannel('A').tobytes()
        checks['protected_pixels_equal']=all(a.getpixel((x,y))==b.getpixel((x,y))
            for y in range(a.height) for x in range(a.width) if x<128 or x>=640)
        checks['nearest_neighbor_8x_grid']=all(b.getpixel((x,y))==b.getpixel((x//8*8,y//8*8))
            for y in range(b.height) for x in range(b.width))
    return {'source_size':list(a.size),'candidate_size':list(b.size),'checks':checks,
        'technical_pass':all(checks.values()),'not_evaluated_reason':'Protection, alpha alignment and pixel-grid checks require equal canvas sizes' if a.size!=b.size else None,
        'source_sha256':sha(Path(source).read_bytes()),
        'candidate_sha256':sha(Path(candidate).read_bytes()),'release_eligible':False,
        'wording_and_native_size_readability':'needs_review; technical pass alone never proves Hangul readability',
        'rom_injection_authorized_by_this_report':False}

def main():
    folder=ROOT/'analysis/pet_labels_v1';report=inspect_candidate(folder/'native_reference_8x.png',folder/'candidate_01.png')
    report.update(policy='development-draft; NON-DISTRIBUTION',tool_sha256=sha(Path(__file__).read_bytes()),
        generator='built-in image_gen; local original preserved',
        generator_original='C:/Users/<user>/.codex/generated_images/01a0ce89-71de-7110-8cdb-aef5aa012c8d/exec-9b3eecab-a60f-4bb7-b6a8-6a71f1e1a6a4.png')
    (folder/'candidate_01_qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))

if __name__=='__main__':main()
