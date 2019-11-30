# LNYF-Matching
Matches dances to dancers using a variant of Gale-Shapley's stable marriage matching algorithm.

## Instructions

1. If you do not have python3 installed yet, install python 3 through [this link](https://docs.python-guide.org/starting/install3/osx/).

2. Install all dependencies using the command `pip3 install -r requirements.txt`

3. Run the script using the command `./match_dancers.sh --quotas=<quotas.csv> --dance_scores=<dance_scores.csv> --dancer_rankings=<dancer_rankings.csv>`

4. If there are any inconsistencies in the data (multiple submissions for the same dancer, or dancers forgetting to submit a dance rankings form are common mistakes), the script will let you know. You can fix them on your end and run the script again any number of times.

5. The script will output two files: a `matchings_by_dancer.csv` and a `matchings_by_dance.csv`. Each file will show you the dances that a dancer was placed in, along with the other dances a dancer ranked / was given a score for.

## Input file formats
The program assumes a pretty rigid format of the three input csvs. Specifically, the program expects three files to be pass in via a flag: a dancer rankings file, a dance scores file, and a quotas file. The files are all meant to be in csv format (so just take an excel file and export as csv).

### dancer rankings 
This file includes all the answers that a dancer gives to the lnyf dance ranking questionnaire. It expects 10 columns, but should be relatively easy to export if the questionnaire format is the same as previous years:
`timestamp`, `dancer email`, `dancer name`, `dancer year`, `gender`, `t-shirt size`, `first choice dances`, `second choice dances`, `third choice dances`, `non-audition dances`.

### dance scores
This file includes all the scores that a dance gives to each dancer that has auditioned for the dance. It expects 4 columns in its csv file: `dance name`, `dancer name`, `dancer email`, `score`, where score is one of: `0`, `1`, `2`, or `3`.

### quotas
This file specifies the dancer capacity for each dance. It expects 2 columns: `dance name`, `max number of dancers`.

## Extra Instructions
- If you need to split a dancer by gender, or by dancer affiliation (`Sayaw sa Bangko` or `K-Pop` are common dances that need this), just split the dance into two. For example, `Sayaw sa Bangko` can become `Sayaw sa Bangko-M` and `Sayaw sa Bangko-F`. Change the rankings in the dancer rankings and quotas csvs accordingly.
  

