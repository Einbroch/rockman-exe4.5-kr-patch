# 2026-10-03 — user requested translation → ROM integration → screen verification

## Result

New immutable-source development ROM: poc/output/exe45_ko_development_chip_batch09_v1.gba.
Repro: poc/output/exe45_ko_development_chip_batch09_v1_repro.gba.
Both SHA256: 8f3a8a3e81db24304f606b930b0ebdf6e249379c85f3cb98964ae77d4ed7ab1f.
571 selected translation units:249 primary names +251 primary descriptions +71 earlier dialogue/menu/header/save/TACTICS units. This is a selected unit count, not a count of distinct authored wordings.
195/196 actual generic DarkChip descriptions added; identical-source draft wording from187 reused by stable wording ID. No fabricated names. Primary source holes stay native.
Secondary98-name drafts remain outside this ROM; secondary descriptions, other dialogue/menus/graphics and whole game remain incomplete.
All wording states remain needs_review. NON-DISTRIBUTION development build, not a completed Korean release.

## Integration

Existing primary library/folder/full Hangul mono/battle/Tactics changes retained. Battle helper now accepts explicit sparse IDs1..194 and201..255; holes195..200 return native. Original contiguous scopes retain original emitted gate logic.
New sparse gate passed native differential CPU comparison over512 IDs, six callers plus high-bit vectors, including ABI/stack/flags. Actual new-ROM battle screen regression still pending.
571-unit build checks source identity, controls, line geometry, numerals, glyph mapping, pointers, final protected ranges and all writes; six archives relocated,726 untouched. Source/header preserved.
First attempt incorrectly requested the temporary Japanese-glyph visibility flag; builder rejected it before ROM output. Failed work directory preserved. Corrected build uses normal full Korean font provider, not temporary glyph substitution.
Repro command uses the same translation assets/options with fresh work/output names. Build recipes follow tools/build_development_patch.py flags recorded in the retained assets and build metadata.

## Evidence

83 automated tests pass, including new two-description reuse and sparse gate differential checks.
CPU native parser: all251 descriptions at9x3 and10x3,502 vectors; all249 battle names at8x1,249 vectors. These are CPU bench fixtures, not emulator route evidence.
Exact new-ROM cold boot13 actions +initial dialogue40 actions; own new save/RTC generated, no old ROM checkpoint/SAV imported.
Normal folder16 actions: Cannon/Airshot/Vulcan sentences and seven existing visible name rows checked against stage/font/upload/VRAM/OBJ/BG/screenshots.
Diagnostic representative17-of251 descriptions:49 actions,21 screenshots, all17 stable pixels verified. Scripts121,123,150,180,194,195,196,201,202,205,218,220,227,236,242,251,255.
Diagnostic representative7-of249 names:10 actions,2 held screenshots,2793 observed row records. Scripts187,201,202,219,236,251,255. Includes full-eight-cell 무라마사블레이드 and 우드맨SP.
Diagnostic CPU-read aliases select real compiled ROM text; no source/name-byte/progress/save-RAM mutation. Diagnostic checkpoints quarantined and ineligible for normal play continuation. These pages do not prove acquired chips or matching chip portraits/stats.
Runtime v1 description/normal report preserved; v2 adds name-page pixel evidence: analysis/exe45_chip_batch09_runtime_v2.json.
Other build save files unchanged. This ROM's own RTC changed during normal emulator execution and is recorded separately from SAV contents.

## Remaining

Full251/249 emulator population coverage is not claimed; current screenshot evidence is representative. Unobserved consumers, battle screen regression, save commit/reboot, timing/lifetime behavior, secondary pool integration, all remaining text/graphics, human meaning/presentation review, audio/hardware/full game and release remain open.
Continue untranslated secondary descriptions next; finish their source/context/technical integration before claiming them rendered. Retain these completed primary-ROM results instead of reusing foreign checkpoints.
