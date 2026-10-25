"""Controlled encoding, protected-source and clone preservation contracts."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chip_library_extension import compile_clone, decode_name, encode_name, sha
from archive_scripts import script_spans

TABLE = {0: " ", 1: "0", 2: "1", 3: "2", 0x11: "キ", 0x90: "X"}


def fixture():
    payload = bytes.fromhex("060007000a00e51102e503e5")
    spec = {"pool": {"offset": 0, "bytes": len(payload), "scripts": 3, "sha256": sha(payload)}}
    asset = {"schema": 2, "policy": "development-draft; NON-DISTRIBUTION", "archive": "0",
             "source_sha256": sha(payload), "source_archive_sha256": sha(payload),
             "consumer": "library-seven-row-tilemap", "review": {"release_eligible": False},
             "source_script_hex": {"1": "1102e5"},
             "wordings": [{"id": "chip", "translation": "칩1", "state": "needs_review"}],
             "units": [{"id": "0:1:0", "source": "キ1", "wording_id": "chip"}]}
    return payload, spec, asset


class ChipLibraryTests(unittest.TestCase):
    def test_boundary_and_mixed_roundtrip(self):
        for text in ("가", "힣", "괜찮1", "가힣괜찮칩012"):
            self.assertEqual(decode_name(encode_name(text, TABLE), TABLE), text)
        self.assertEqual(decode_name(b"\xe5", TABLE), "")

    def test_rejects_width_and_nonresident_glyph(self):
        for text in ("", "가" * 9, "X", "a", "\n", "ᄀ"):
            with self.assertRaises(ValueError):
                encode_name(text, TABLE)

    def test_rejects_bad_boundaries_and_controls(self):
        for blob in (b"", b"\x01", b"\xe5\x00", b"\xf9", b"\xf9\xfc\0", b"\xf9\xfc\xff\xff\xe5", b"\x02" * 9 + b"\xe5", b"\xe4\x01\xe5"):
            with self.assertRaises(ValueError):
                decode_name(blob, TABLE)

    def test_clone_preserves_other_scripts(self):
        source, spec, asset = fixture()
        clone, report = compile_clone(source, spec, asset, TABLE)
        original, translated = script_spans(source, 3), script_spans(clone, 3)
        self.assertEqual(translated[0], original[0])
        self.assertEqual(translated[2], original[2])
        self.assertEqual(decode_name(translated[1], TABLE), "칩1")
        self.assertEqual(len(report["unselected_scripts"]), 2)

    def test_rejects_protected_changes(self):
        source, spec, good = fixture()
        edits = [lambda a: a["source_script_hex"].update({"1": "1103e5"}),
                 lambda a: a["wordings"][0].update(translation="칩2"),
                 lambda a: a["units"][0].update(source="キ2"),
                 lambda a: a["review"].update(release_eligible=True),
                 lambda a: a["wordings"][0].update(state="untranslated")]
        for edit in edits:
            asset = copy.deepcopy(good)
            edit(asset)
            with self.assertRaises(ValueError):
                compile_clone(source, spec, asset, TABLE)


if __name__ == "__main__":
    unittest.main()
