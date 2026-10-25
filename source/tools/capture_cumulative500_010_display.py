"""010 native box diagnostics; new archive1/2 and retained archive20."""
import sys
import capture_pending500_004_alert as capture
CASES={'new-win':('6989B0',4,1),'new-loss':('6989B0',4,2),'carry':('6886F0',25,20)}
def main():
    index=sys.argv.index('--display-kind');kind=sys.argv[index+1];del sys.argv[index:index+2]
    if kind not in CASES:raise ValueError('Declared display case')
    archive,count,script=CASES[kind]
    capture.TARGET_ARCHIVE=archive;capture.SCRIPT_COUNT=count;capture.SCRIPTS=(script,)
    return capture.main()
if __name__=='__main__':raise SystemExit(main())
