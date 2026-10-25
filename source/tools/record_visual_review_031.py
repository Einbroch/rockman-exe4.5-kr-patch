"""Record completed direct inspection of exact031 four contact sheets."""
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    out=ROOT/'analysis/pending500_031_v1';v=read(out/'visual_inputs.json');m=read('poc/output/pending500_031_v1.json');h=m['output_sha256'];require_hash(ROOT/'poc/output/pending500_031_v1.gba',h)
    if v['rom_sha256']!=h or {s['kind']:s['screens'] for s in v['sheets']}!={'startup':22,'mail':23,'opponent':6,'calendar':7}:raise ValueError('031 inspected screenshot denominator')
    for s in v['sheets']:require_hash(ROOT/s['path'],s['sha256'])
    conditions=list(read('analysis/pending500_030_v1/visual_review.json')['open_conditions'])
    conditions+=['Calendar meal7 native next-action prompt, schedule heading and weekday kanji remain Japanese. New calendar50 deletion prose/options do not translate every calendar menu or event route.','Event205/title110px is conditional native producer evidence. Anniversary/imported/universal writers and all source guards/loops/natural histories remain outside runtime coverage.','Only nine new literal IDs observed in actual031 runtime; all500 structure/font/cumulative carry checked, not all500 semantics or natural speaker/caller approval.']
    observations=[
        'Directly viewed all four exact031 contact sheets,58screens. Title 처음부터, date input/confirmation, gender/age/job and Navi selection Korean labels remain visible and readable. Native kana/kana/Latin keyboard pages and Japanese nickname/suffix remain; Hangul automatic input is not integrated.',
        'Boot9 inherited welcome bitmap still has overlapping rows. Known unresolved defect, not repaired or accepted as complete. Japanese title logo, mail header, native schedule header and weekday kanji remain visible.',
        'All23 first-mail body pages are Korean with frame/advance arrow and no newly observed clipping. Separate normal runtime verifier binds23ordered waits, three archive loads, four Navi cards and reentry.',
        'GutsMan62 diagnostic first page: 넷배틀에서는/ワイドショット1 칩이/꽤 편리하지. Second: 단, 장비는/방어를 충분히/갖춰 둬야 해! GutsMan71 first: ワイドショット1 칩은/대결에서,/꽤 효과적이야. Second: 사용할 타이밍이나/그때의 장비에/따라 달라지지만. Four pages fit; prior name/page cleared and both return to 자, 뭘 할까?. Native chip-name value stays Japanese. Own Rockman host is quarantined diagnostic, not permanent character reassignment or natural battle history.',
        'Actual normal calendar first page shows 2:00 AM 1회만 and quoted 식사, then 일정을 삭제할게. Confirmation 괜찮아? with 예/아니요 is readable, separated from its cursor, and clears previous title row. No highlights 아니요; No and B preserve the listed meal, Yes removes it; reentry redraws the preserved meal correctly.',
        'Calendar meal7 still shows original Japanese next-action prompt. This is explicitly outside the four new calendar50 literals and remains work, not hidden by the new deletion screenshots.',
        'Direct visual observations agree with exact ROM/fontCPU/RAM/OBJ/pixel proofs, conditional aggregate geometry, choice outcomes and source-preserved controls. No full500 semantic, full playthrough, save/reset/fresh reload, hardware or audio approval.'
    ]
    frozen_write(out/'visual_review.json',dict(schema=1,passed=True,rom_sha256=h,visual_reviewed=True,meaning_of_pass='Directly viewed58 exact031 screens; bounded development regression and nine new literal IDs, not release or whole-game completion.',sheets_viewed=v['sheets'],observations=observations,open_conditions=conditions,semantic_human_approved=False,release_eligible=False))
    print('031 direct visual review recorded,58screens; unresolved conditions retained')


if __name__=='__main__':main()
