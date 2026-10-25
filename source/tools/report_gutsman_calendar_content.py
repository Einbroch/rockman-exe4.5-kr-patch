"""Four strict native input-question pages; two new literal questions."""
from report_gutsman_calendar_prompts import main as report
from run_gutsman_calendar_content import STEM,PREFIX,OUTDIR
def main():return report(stem=STEM,prefix=PREFIX,outdir=OUTDIR,content=True)
if __name__=='__main__':main()
