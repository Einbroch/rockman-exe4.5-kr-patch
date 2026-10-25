"""NumberMan return/result display profiles, not event outcome or acquisition proof."""
import sys
import capture_pending500_004_alert as observer

def main():
    i=sys.argv.index('--number-case');case=sys.argv[i+1];del sys.argv[i:i+2]
    profiles={'return':('68787C',4,2),'draw':('68C2CC',5,3)}
    if case not in profiles:raise ValueError('Explicit NumberMan case')
    observer.TARGET_ARCHIVE,observer.SCRIPT_COUNT,script=profiles[case];observer.SCRIPTS=(script,)
    sys.argv+=['--alert-script',str(script)]
    return observer.main()

if __name__=='__main__':raise SystemExit(main())
