import unittest
from pet_quick_capacity import validate, PREFIX
from survey_pet_quick_reflow_024 import place, replace_for_analysis
from tpl_literals import literals


def fixture(text='"짧은 말"', tail='\tkeyWait\n\t\tany = false\n\tclearMsg\n\twaitHold\n'):
    commands = ''.join('\t'+name+'\n'+args for name, args in PREFIX)
    return '@archive TEST\n@size 1\nscript 0 mmbn45 {\n'+commands+'\t'+text+'\n'+tail+'}\n'


class QuickTests(unittest.TestCase):
    def test_waited_cleared_hold(self):
        src = fixture()
        self.assertEqual(validate(src, src, [0], {'TEST:0:0'})[0]['pages'][0]['widths'], [44])

    def test_waited_end(self):
        src = fixture(tail='\tkeyWait\n\t\tany = false\n\tend\n')
        self.assertEqual(len(validate(src, src, [0], {'TEST:0:0'})), 1)

    def test_reject_overflow(self):
        src = fixture('"'+'가'*12+'"')
        with self.assertRaisesRegex(ValueError, 'aggregate'):
            validate(src, src, [0], {'TEST:0:0'})

    def test_composite_not_individual(self):
        src = fixture('"'+'가'*6+'"\n\twaitSkip\n\t\tframes = 30\n\t"'+'나'*6+'"')
        with self.assertRaisesRegex(ValueError, 'aggregate'):
            validate(src, src, [0], {'TEST:0:0', 'TEST:0:1'})

    def test_reject_four_rows(self):
        src = fixture('"가\\n나\\n다\\n라"')
        with self.assertRaisesRegex(ValueError, 'aggregate'):
            validate(src, src, [0], {'TEST:0:0'})

    def test_reject_unknown_command(self):
        src = fixture(tail='\tprintBuffer\n\tkeyWait\n\t\tany = false\n\tend\n')
        with self.assertRaisesRegex(ValueError, 'unmodeled'):
            validate(src, src, [0], {'TEST:0:0'})

    def test_reject_hold_before_clear(self):
        src = fixture(tail='\tkeyWait\n\t\tany = false\n\twaitHold\n')
        with self.assertRaisesRegex(ValueError, 'hold after clear'):
            validate(src, src, [0], {'TEST:0:0'})

    def test_reject_text_after_wait(self):
        src = fixture(tail='\tkeyWait\n\t\tany = false\n\t"다음"\n\tend\n')
        with self.assertRaisesRegex(ValueError, 'text after wait'):
            validate(src, src, [0], {'TEST:0:0'})

    def test_reject_changed_controls(self):
        src = fixture()
        with self.assertRaisesRegex(ValueError, 'protected'):
            validate(src, src.replace('frames = 30', 'frames = 31').replace('left = 92', 'left = 52'), [0], {'TEST:0:0'})

    def test_reject_unbound_ids(self):
        src = fixture()
        with self.assertRaisesRegex(ValueError, 'unbound'):
            validate(src, src, [0], {'TEST:0:0', 'TEST:1:0'})

    def test_line_expansion_keeps_words(self):
        text = '가나다라마 바사아자차 카타파하'
        value = place(text)
        self.assertIsNotNone(value)
        self.assertEqual(value.replace('\n', ' '), text)
        self.assertGreater(value.count('\n'), 0)
        src = fixture('"원문"')
        target = replace_for_analysis(src, [dict(id='TEST:0:0', source='원문', translation=value, state='needs_review')])
        self.assertEqual(literals(target)[0].text, value)
        validate(src, target, [0], {'TEST:0:0'})

    def test_reject_unbreakable_word(self):
        self.assertIsNone(place('가'*12))

    def test_reject_protected_padding(self):
        for value in (' 말', '말 ', '\n말', '말\n'):
            self.assertIsNone(place(value))

    def test_reject_source_mismatch(self):
        with self.assertRaisesRegex(ValueError, 'Source'):
            replace_for_analysis(fixture(), [dict(id='TEST:0:0', source='다른 원문', translation='말', state='needs_review')])


if __name__ == '__main__':
    unittest.main()
