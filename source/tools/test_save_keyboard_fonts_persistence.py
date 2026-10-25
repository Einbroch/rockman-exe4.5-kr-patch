import unittest
from report_save_keyboard_fonts_persistence import validate_reload


class ReloadContract(unittest.TestCase):
    def setUp(self):
        self.result = dict(complete=True, return_code=0, state_origin=None, state_sha256=None)
        self.record = bytes([1, 0x9B, 0xE5]) + bytes(11)
        self.save = bytes(65536)

    def check(self, **changes):
        args = dict(result=self.result, before=self.record, snapshots=[self.record], saved=self.save, after=self.save)
        args.update(changes)
        return validate_reload(**args)

    def test_native_reload(self):
        self.check()

    def test_saved_state_is_not_native_reload(self):
        for key in ('state_origin', 'state_sha256'):
            with self.assertRaises(ValueError):
                self.check(result=dict(self.result, **{key: 'fixture'}))

    def test_different_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.check(snapshots=[self.record, bytes(14)])

    def test_changed_or_short_battery_is_rejected(self):
        for other in (bytes(65535), b'\x01' + self.save[1:]):
            with self.assertRaises(ValueError):
                self.check(after=other)

    def test_incomplete_run_is_rejected(self):
        with self.assertRaises(ValueError):
            self.check(result=dict(self.result, complete=False))


if __name__ == '__main__':
    unittest.main()
