# 033 exact500 build checkpoint — 2026-10-17

## Authority and scope

- User decision: exactly500 new units per ROM application; no partial253/272/419 adoption. No BPS/xdelta/ZIP requested.
- Accepted previous product remains `poc/output/pending500_032_v1.gba`, SHA256 `cc2d02d3fda6ab27601d1735015b24b11d869308dff3e08f0fd4f06f31518f64`,17,122 units until033 product audits/runtime complete.
- `analysis/pending_insertion_500_033_exact500_selection_v1/selection.json`:500 nonduplicate IDs,153 scripts,37 existing RAW carry archives.272 previous candidates+144 operator three-option literals+84 profile-manager literals. Reserved15 IDs are NOT selected.
- Compile500: both source and target roundtrips, unselected source bytes,427 actual used font glyphs PASS. Carry500:3,126 previous units retained, layouts/controls/canonical wording preserved. Inputs11 positive consumer types/77 refusals PASS. Preallocation:21 previous appended roots/20 changed/222 new IDs,4 refusals PASS.

## Primary build in progress

- Immutable original is the ONLY primary build source.032 ROM is comparison evidence, not a patched input.
- `tools/build_layout500_033.py`: initial session20355; `--repro`: session49427. Work/output directories distinct; do not start duplicates or overwrite failed evidence. At01:32 KST both active, primary307 archive directories/repro174. Counts are not completion percentages.
- Expected if successful: `poc/output/pending500_033_v1.gba` and `_repro.gba`,17,622 metadata units. This expectation is NOT a verified output claim.
- Recipe `tools/specs/primary033_version.json`, generated primary `tools/build_development_patch_033.py`, adapters `layout500_inputs_033.py`/`layout500_product_033.py`. These and prior032 tools are frozen/pinned. Repair through new versions, not in-place edits.
- Run independent `verify_layout500_product_033.py --out analysis/pending500_033_v1/integration_pre_repro.json` after initial build. After repro exists run `--repro poc/output/pending500_033_v1_repro.gba` with default final output. No result exists yet at this checkpoint.

## Runtime preparation and correction

- `run_runtime_033.py`/`capture_choices_033.py` were never executed: their script766134:5 two-choice case is NOT new in this cohort and its new-script guard correctly would reject it. Preserve these unused versions.
- Corrected prepared tools `run_runtime_033_v2.py`/`capture_choices_033_v2.py` select newly inserted766134:6 three-choice and7CC6A0:0 manager only. Syntax checked; actual runtime still pending.
- `run_runtime_033_v2.py`: own coldboot, kana keyboard3pages/fourNavi/first-mail; then quarantined read-alias diagnostics3choice B result3, A results0/1/2, manager B retained target95. Native initialization/width/EA/EC execute. Do NOT enter manager Yes/editor via the alias; caller/editor prerequisites not established. No natural battle acquisition or gameplay effect claim.
- Prepared `verify_choices_samples_033.py` is not executed and may need evidence-driven versioned repair. It checks literal/font CPU/OBJ pixels/native selected index/return result; horizontal manager centering must be independently reconciled with source/native geometry rather than observed offsets accepted blindly. Receipt artifact hashes/quarantine are mandatory.
- `verify_layout500_normal_033.py` ready.9 fresh product CPU tools45,680 fixtures, A3/B0 vectors11,993, integrity16 refusals plus early-FD09 2,048 and wide vertical144 prepared. These must run against exact033 output, not inherited032 reports.
- Mesen strictly serial; isolated CLI executable only, do not touch user's mGBA. Direct screenshot review still required. Read-alias states are diagnostic-only and must never become normal gameplay parents.

## Known open limits

Plain player-name model66px is conditional on valid source-native <=6 glyph records with max source metric11. Do not extend this to arbitrary/imported/Hangul records. Full Hangul composition/commit/save/fresh redisplay, Japanese keyboard/logo/other images, welcome overlap, natural manager editor/confirm/save, semantics/voices remain incomplete. This is development-only, needs_review, NON-DISTRIBUTION. Whole-game release is not approved.
