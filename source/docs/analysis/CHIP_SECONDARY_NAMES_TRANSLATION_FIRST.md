# 2026-10-03 — untranslated-first secondary chip names

New assets: translations/chip_secondary_names_draft_seed.json and chip_secondary_names_ko.json.
Source pool 0x765B18, 1103 bytes, 137 script slots; 100 literal-bearing entries.
Selected 98 real names; preserve source ???? (113), blank literal (132), and 37 empty slots.
Source ROM pinned to 588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8.
Asset binds full source pool hash, extraction TPL hash and selected raw script bytes, seed and composer hashes.

Independent codec/source checks prove selected source bytes decode to extracted source names, translations round-trip under the existing Hangul codec, numeric sequences and SP/DS suffixes remain, adopted name width <=8 cells, TPL controls stay identical, and all 39 unselected script payloads remain byte-identical in an in-memory test clone.
81 tests pass: python -X utf8 -m unittest discover -s tools -p 'test_*.py' -q.
No ROM write/build or emulator launch. In-memory codec tests are bench evidence only.

98 new needs_review wordings; cumulative drafts 667 (569 prior +98). Existing prior assets unchanged. Actual current development ROM remains the 311-wording artifact.
Eight-cell draft range does not prove all secondary consumers accept it. Secondary-name relocation, font consumer reachability and runtime QA remain pending. Descriptions are not included in this name-only scope.
Human wording/presentation approval and full game translation remain incomplete. No distribution claim.
Review sheet: translations/CHIP_SECONDARY_NAMES_REVIEW.md.
Meaning review flags: カカリゲイコ -> 연속수련 candidate, ボーイズボム -> 보이즈봄 referent. Source labels rather than invented gameplay descriptions were translated.
