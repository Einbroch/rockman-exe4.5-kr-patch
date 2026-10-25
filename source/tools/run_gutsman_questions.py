"""Fresh exact-ROM normal route, then quarantined question/reaction display QA."""
import run_gutsman_profile as normal
import run_gutsman_profile_diagnostics as diagnostic
from capture_gutsman_profile_diagnostic import QUESTION_SCRIPTS

STEM='exe45_ko_development_gutsman_questions_v1'
PREFIX='gutsman-questions-v1-'

def main():
    normal.STEM=STEM;normal.PREFIX=PREFIX;normal.main()
    diagnostic.STEM=STEM;diagnostic.PREFIX=PREFIX;diagnostic.ASSET='gutsman_profile_questions_ko.json'
    diagnostic.SCRIPTS=QUESTION_SCRIPTS;diagnostic.PAGE_COUNTS={11:5,88:1};diagnostic.main()

if __name__=='__main__':main()
