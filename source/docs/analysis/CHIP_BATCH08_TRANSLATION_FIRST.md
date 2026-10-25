# 2026-10-03 — untranslated-first continuation

Added 55 actual primary-pool chip names and 55 descriptions, scripts 201..255.
Assets: translations/library_chip_names_batch08_ko.json and chip_descriptions_batch08_ko.json.
Prior 194 pairs preserved verbatim; cumulative 249 pairs plus 71 existing other wordings = 569 development drafts.
All remain needs_review and non-release. Current ROM still has 311 selected wordings; no ROM rebuilt or emulator launched.

Source holes 195..200 preserved; no fabricated names. Script 0 remains native.
Sparse description scope registered explicitly; current contiguous battle-name helper cannot directly adopt this draft scope.
Secondary Navi-name pool and other untranslated dialogue remain outside this completion claim.

Verification: python -X utf8 -m unittest discover -s tools -p 'test_*.py' -q — 80 tests OK.
Checks cover composer reproducibility, prior wording identity, original ROM hash, source control skeleton, unchanged unselected literals, numeric sequences, source line counts, full Hangul codec layout, and name clone preservation. This is bench evidence, not runtime evidence or human translation approval.

Review: translations/CHIP_UNTRANSLATED_FIRST_201_255.md. Follow-up meaning review: per-panel DoublePoint gain, DarkLine axis, WindMan square scope, AquaMan pipe-origin range.
