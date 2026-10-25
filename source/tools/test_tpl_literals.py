import unittest

from tools.tpl_literals import literals, replace_literals, skeleton, serialize, resolve_units


SOURCE = '@archive demo\n@size 3\nscript 1 mmbn45 {\n\t"""\n\tはじめまして!\n\tよろしくね!!\n\t"""\n\tkeyWait\n\t\tany = false\n}\nscript 2 mmbn45 {\n\t"ひさしぶり!"\n\tend\n}\n'


class ProtectedLiteralTests(unittest.TestCase):
    def test_fixedcell_requires_explicit_consumer(self):
        source = '@archive demo\nscript 0 mmbn45s { "スタンダード" end }'
        units = [{"id": "demo:0:0", "source": "スタンダード", "translation": "스탠더드", "state": "needs_review"}]
        with self.assertRaises(ValueError):
            replace_literals(source, units)
        result = replace_literals(source, units, language="mmbn45s")
        self.assertEqual(literals(result)[0].text, "스탠더드")
        self.assertEqual(skeleton(source), skeleton(result))
        with self.assertRaises(ValueError):
            replace_literals(source, units, language="unknown")

    def test_multiline_and_stable_ids(self):
        items = literals(SOURCE)
        self.assertEqual([x.key for x in items], ["demo:1:0", "demo:2:0"])
        self.assertEqual(items[0].text, "はじめまして!\nよろしくね!!")

    def test_replace_keeps_controls_and_other_text(self):
        result = replace_literals(SOURCE, [{"id": "demo:1:0", "source": "はじめまして!\nよろしくね!!",
                                            "translation": "처음 만나서 반가워!\n잘 부탁해!!", "state": "needs_review"}])
        self.assertEqual(skeleton(SOURCE), skeleton(result))
        self.assertEqual(literals(result)[1].text, "ひさしぶり!")

    def test_source_drift_fails(self):
        with self.assertRaises(ValueError):
            replace_literals(SOURCE, [{"id": "demo:1:0", "source": "wrong", "translation": "한글", "state": "needs_review"}])

    def test_missing_unit_fails(self):
        with self.assertRaises(ValueError):
            replace_literals(SOURCE, [{"id": "demo:9:0", "source": "wrong", "translation": "한글", "state": "needs_review"}])

    def test_escaped_control_injection_fails(self):
        with self.assertRaises(ValueError):
            replace_literals(SOURCE, [{"id": "demo:2:0", "source": "ひさしぶり!", "translation": '한글" end "', "state": "needs_review"}])

    def test_canonical_newline_escape_and_blank_line_roundtrip(self):
        source = '@archive demo\n@size 1\nscript 0 mmbn45 {\n\t"メールを見るよ!!\\n\\n"\n\tend\n}\n'
        value = literals(source)[0].text
        self.assertEqual(value, "メールを見るよ!!\n\n")
        rewritten = source.replace('"メールを見るよ!!\\n\\n"', serialize(value))
        self.assertEqual(literals(rewritten)[0].text, value)
        self.assertEqual(skeleton(source), skeleton(rewritten))

    def test_unknown_escape_rejected(self):
        with self.assertRaises(ValueError):
            literals('@archive demo\nscript 0 mmbn45 { "text\\xE5" }')

    def test_leading_newline_uses_explicit_escape(self):
        self.assertEqual(serialize("\n한글"), '"\\n한글"')
        self.assertEqual(literals('@archive demo\nscript 0 mmbn45 { ' + serialize("\n한글") + ' }')[0].text, "\n한글")

    def test_layout_token_loss_rejected(self):
        with self.assertRaises(ValueError):
            replace_literals(SOURCE, [{"id": "demo:1:0", "source": "はじめまして!\nよろしくね!!",
                                      "translation": "잘 부탁해!!", "state": "needs_review"}])

    def test_shared_wording_resolves_by_explicit_id(self):
        result = resolve_units({"schema": 2, "wordings": [{"id": "choice.yes", "translation": "예  ", "state": "needs_review"}],
                                "units": [{"id": "demo:1:0", "source": "はい  ", "wording_id": "choice.yes"}]})
        self.assertEqual(result[0]["translation"], "예  ")
        self.assertEqual(result[0]["source"], "はい  ")


if __name__ == "__main__":
    unittest.main()
