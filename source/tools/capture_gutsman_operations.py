"""Native observer only; no read aliases or ROM/RAM writes."""
import sys
import capture_roll_pet as pet
if '--operation-archive' not in sys.argv:raise ValueError('explicit archive required')
i=sys.argv.index('--operation-archive');pet.ARCHIVE=sys.argv[i+1];del sys.argv[i:i+2]
if pet.ARCHIVE not in ('6663B8','6664D0','666820'):raise ValueError('unregistered scope')
if __name__=='__main__':raise SystemExit(pet.main())
