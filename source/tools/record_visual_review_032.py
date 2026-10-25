"""Record completed direct viewing of64 exact032 capture screens."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref


def main():
    out=ROOT/'analysis/pending500_032_v1';m=read('poc/output/pending500_032_v1.json');h=m['output_sha256'];require_hash(ROOT/'poc/output/pending500_032_v1.gba',h);v=read(out/'visual_inputs.json');clear=read(out/'calendar_clear_runtime.json')
    if v['rom_sha256']!=h or {s['kind']:s['screens'] for s in v['sheets']}!={'startup':22,'mail':23,'menus':12,'anniversary':7}:raise ValueError('032 viewed screen denominator')
    if not clear['passed'] or clear['rom_sha256']!=h:raise ValueError('032 clearing evidence identity')
    require_hash(ROOT/clear['checker']['path'],clear['checker']['sha256'])
    for s in v['sheets']:require_hash(ROOT/s['path'],s['sha256'])
    observations=[
        'Directly viewed allfour exact032 contacts:startup22/mail23/menus12/anniversary7=64screens. Initial date, gender, age, occupation, confirmation and Navi selection Korean remain readable; native kana/kana/Latin keyboard pages remain Japanese/Latin.',
        'The inherited boot9 welcome bitmap still has overlapping rows. This is not repaired or accepted as complete. Japanese title logo, first-mail Eメール header, native nickname/suffix and calendar weekday/header elements remain visible.',
        'All23 first-mail body pages are Korean with their frame and advance arrow. Separate runtime checks bind23ordered waits, four selectable Navi cards, three archive loads and reentry; no new observed clipping.',
        'Calendar home now shows 오늘은 1월1일이야 and 자, 뭘 할까?. New 뭘 등록할까? / 일정 / 기념일 is readable; cursor changes between rows without covering the text. B returns to the correct original date-selection prompt 어느 날의 일정을 입력할까?, not calendarhome0.',
        'The clock/content panels remain readable:몇 시부터 시작해?, TV방송/친구와약속/식사/학원, and new 이대로 OK? with 예/아니요. Accepting the meal returns to Korean home. Native time formatting and fixed weekday kanji remain unchanged.',
        'Possessions page shows new 이것은 plus the native いくん nickname, 의/소지품이야 and 키 아이템 확인. B returns to PET 자, 뭘 할까?; reentry redraws the caption; A opens the preserved key-item empty message. No character reassignment or read-alias/memory intervention was used.',
        'Anniversary editor accepts ten native E406glyphs and rejects theeleventh. Registered title displays within quotes with00/1/1(土), followed by new 기념일을 삭제할게. Confirmation 괜찮아? with 예/아니요 clears the prior title row. No preserves the listed title; Yes removes it. The title fixture and keyboard are native Japanese, not Hangul composition or save/reload support.',
        'Direct views agree with16new Korean literal IDs,fontCPU/ROM/BDF/RAM/OBJ/pixel proofs, exactcurrentdate/provider positions and4248cleared pixels. Source-preserved choices/controls and conditional geometry do not constitute all500 natural speaker/context/meaning approval.'
    ]
    conditions=[
        'Automatic Hangul composition/commit/save/freshredisplay remains unfinished. Native anniversary10glyph/21byte/110px evidence is not permission for10four-byte Hangul syllables in the22byte record field.',
        'Inherited welcome bitmap row overlap remains unresolved. Native kana keyboard, title logo, mail/calendar headers, weekday kanji and player nickname/suffix remain untranslated or unintegrated. Shared stats chip-name values also remain Japanese.',
        'Calendar inventory513 original Japanese literals covered21declared roots only, not whole-game/images. These500 leave13inventory literals (AquaMan50/51/52 extraSFX families plus onecaption); no full-game completion percentage is claimed.',
        'All500 canonical needs_review wording, spacing/voice/context and previous open phrasing issues still require semantic/human review. Runtime samples cover16new IDs on normal Rockman0/2/10/24/51, not allNavi/natural scenes.',
        'Nativeyear00..99/month1..12/day1..31/weekday0..6 and legacy nickname/title bounds are conditional. All title producers/default/import/corrupt/writer states, natural52annual route and FireMan7width natural gameplay are not universally covered by these samples.',
        'No full playthrough, native save/reset/freshreload, old-save compatibility, hardware/audio completion or release approval. No newBPS/xdelta/ZIP.'
    ]
    frozen_write(out/'visual_review.json',dict(schema=1,passed=True,rom_sha256=h,visual_reviewed=True,meaning_of_pass='Directly viewed64exact032screens; bounded development regression and16newliteral IDs, not fullgame/semantic/Hangul/persistence/release approval.',sheets_viewed=v['sheets'],observations=observations,open_conditions=conditions,technical_clear_report=ref(out/'calendar_clear_runtime.json'),checker=dict(path='tools/record_visual_review_032.py',sha256=sha((ROOT/'tools/record_visual_review_032.py').read_bytes())),semantic_human_approved=False,release_eligible=False))
    print('032 direct64screen review recorded; open conditions retained')


if __name__=='__main__':main()
