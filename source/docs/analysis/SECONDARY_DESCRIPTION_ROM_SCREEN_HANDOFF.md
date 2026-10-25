# 2026-10-03 —75 untranslated secondary chip/PA descriptions integrated

New cumulative development ROM: poc/output/exe45_ko_development_chip_secondary_desc_v1.gba.
Repro: poc/output/exe45_ko_development_chip_secondary_desc_v1_repro.gba.
Both SHA2569a2a0be8342bad1c37c57213b3d322bcc6cd4240be707fa94f0f71a2ec30d424.
646 selected units=571 previous +75 new secondary descriptions. Count is selected entries, not distinct authored wording decisions.
All75 actual literals in secondary archive76BC60 drafted;113 total scripts with38 nonliteral slots preserved. Original3255-byte pool and four source pointer roots bound to immutable source and catalog, all relocated pointers checked by builder.
Seven selected archives,725 untouched; original ROM/header unchanged; final diff audited. Existing primary249 name/251 description/71 other units remain selected unchanged.
Assets remain needs_review and NON-DISTRIBUTION. Not completed whole-game Korean localization or release approval.

## Translation evidence

translations/chip_secondary_descriptions_ko.json binds source image/pool/TPL/seed/composer hashes and stable entry identities.
translations/CHIP_SECONDARY_DESCRIPTIONS_REVIEW.md shows all75 source/target pairs.
Protected controls, source line counts, numeric sequence and adopted nine-cell width checked; full Hangul mapping checked.
Meaning/naturalness review pending: グリグリタップ attack-name candidate, tape core wording at2.5 squares, BlueMoon phrasing. No automatic rewrite of prior translated assets.

## Runtime evidence

New-ROM cold boot13 actions and initial dialogue40 actions; no foreign SAV/checkpoint reuse. Own save/RTC created normally; other build saves hash-identical across verified routes.
All75 new descriptions executed by actual native parser in a CPU fixture at9x3 and10x3,150 vectors. CPU fixture is bench evidence, not emulator route evidence.
Native descriptor read080D2922 received diagnostic source IDs256+script. Native helper080D4CE0 chose relocated secondary root080D4D10, normalized ID and called unchanged fixed-cell parser/mono provider. No ROM/text-byte/progress/save-RAM injection.
Scripts0,1,7,16,22,29,88 rendered in16-action diagnostic run;8 held screenshots. Exact stream identity,30-glyph/1920-byte stage, Hangul/native glyph providers, VRAM upload and27 visible OBJ cells checked. All screenshot pixels match expected glyph role masks with uniform observed per-page RGB/BGR555 colors; ink/background contrast checked. Includes two-line LaserMan description and preserved2.5/+40/2-by3 cases.
Do not transfer Cannon's fixed palette colors to other chip pages: these native pages differ. Report records each page's observed palette and consistent scanout masks, not an independently modeled BGR555-to-RGB color transform or human style approval.
Diagnostic checkpoints quarantined, not normal-play continuation or acquired-chip proof. Description results do not claim translated secondary names or matching diagnostic name/photo/stats fields.
Normal primary folder16-action regression: Cannon/Airshot/Vulcan sentences pass stage/OBJ/pixel checks; folder copy/cache/ABI observer passes.
Detailed report: analysis/exe45_secondary_description_runtime_v1.json.

## Retained unsuccessful observations

First native-samples run aliased name-row descriptor reads only, found zero secondary description calls, and was marked incomplete with diagnostic checkpoint quarantine. Not credited as a runtime pass.
R2 also observed real description input, but querying CPU state on every EWRAM read made it slow. Interrupted that owned test; no remaining emulator process found. Artifacts preserved and uncredited.
R3 filters known descriptor addresses before querying CPU state. Same ROM, same native consumer, successful verified descriptions. No ROM rebuild to conceal observation failure.
Initial screenshot verifier incorrectly assumed Cannon's fixed colors; failed native palette assertion was retained in the work history. Corrected verifier preserves geometry/glyph/stage/VRAM checks and observes role colors per page. It does not waive a glyph or upload mismatch.
Selection-path notes: analysis/SECONDARY_DESCRIPTION_SELECTION_PATH.md.

## Remaining

Secondary98-name drafts still not integrated; Japanese names remain. Source strings beyond descriptor script93 are absent here; later name-only slots need separate consumer analysis, not invented descriptions.
All75 runtime coverage not claimed:7 screenshot representatives plus full75 CPU coverage. Other pointer consumers, new-ROM battle/reentry/save-commit/lifetime/timing regressions, remaining dialogue/UI/graphics, human wording/presentation review, full-game/audio/hardware/release remain pending.
Next scoped work: integrate additional name pool through confirmed individual consumers while preserving blank/???? slots, then verify new names on a cumulative build; do not move every shared pointer without consumer evidence.
