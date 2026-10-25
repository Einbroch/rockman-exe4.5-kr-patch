"""Own cold/native save/continue and normal key-item route on full-ROM build."""
import run_keyitem_empty as base
base.STEM='exe45_ko_development_keyitem_full_rom_v1'
base.PREFIX='keyitem-full-rom-v1-'
base.CAPTURE_TOOL='capture_keyitem_full_rom.py'
if __name__=='__main__':base.main()
