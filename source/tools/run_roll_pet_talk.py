"""Fresh same-ROM cumulative chain plus normal PET R conversation."""
import run_roll_subjects as subjects
import run_roll_fortune_matrix as matrix
STEM='exe45_ko_development_roll_pet_talk_v2'
PREFIX='roll-pet-talk-v1-'
OUTDIR='roll_pet_talk_v1'
ACTIONS='none:1:7,r:2:180,none:1:180'

def main():
    previous=subjects.STEM,subjects.PREFIX
    try:subjects.STEM=STEM;subjects.PREFIX=PREFIX;subjects.main(OUTDIR)
    finally:subjects.STEM,subjects.PREFIX=previous
    matrix.STEM=STEM
    matrix.segment('capture_roll_pet_talk.py',PREFIX+'talk',PREFIX+'roll-intro',ACTIONS)

if __name__=='__main__':main()
