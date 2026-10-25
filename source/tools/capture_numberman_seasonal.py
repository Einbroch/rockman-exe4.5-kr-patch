"""Read-only actual seasonal pool/glyph observer (no script/RTC intervention)."""
import sys
import capture_roll_pet as pet

if __name__=='__main__':
    pet.ARCHIVE='68BBB4'
    if '--seasonal-archive' in sys.argv:
        i=sys.argv.index('--seasonal-archive');pet.ARCHIVE=sys.argv[i+1];del sys.argv[i:i+2]
        if pet.ARCHIVE not in ('65E438','6648D0','66A234','68BBB4'):raise ValueError('unregistered seasonal archive')
    raise SystemExit(pet.main())
