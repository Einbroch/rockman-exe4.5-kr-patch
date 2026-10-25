"""011 keyWait literal diagnostics; native control skeleton unchanged."""
import sys
import capture_pending500_004_alert as capture
CASES={'ice':('6C5F28',5,1),'plant':('6D1068',5,3),'carry':('6B69A0',25,22)}
def main():
    index=sys.argv.index('--display-kind');kind=sys.argv[index+1];del sys.argv[index:index+2]
    if kind not in CASES:raise ValueError('Declared display case')
    archive,count,script=CASES[kind]
    capture.TARGET_ARCHIVE=archive;capture.SCRIPT_COUNT=count;capture.SCRIPTS=(script,)
    return capture.main()
if __name__=='__main__':raise SystemExit(main())
