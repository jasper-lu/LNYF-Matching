from absl import app
from absl import flags
from absl import logging as log
from dance import Dance
from dancer import Dancers, Dancer
from matching.games import HospitalResident
import pandas as pd

flags.DEFINE_string("quotas", None, "Filename associated with dance quotas.")
flags.DEFINE_string("dance_scores", None,
                    "Filename associated with dancer scores.")
flags.DEFINE_string(
    "dancer_rankings", None,
    "Filename associated with dancer info and dancer rankings.")

FLAGS = flags.FLAGS


def create_dancers(dancers_df):
    dancers = Dancers()
    for _, row in dancers_df.iterrows():
        print(row)
        dancers.add_dancer(Dancer.from_pandas_row(row))

    return dancers


def create_dances(quotas_df, dance_scores_df, dancers):
    dances = {}
    for _, row in quotas_df.iterrows():
        dances[row['dance'].strip()] = Dance(row['dance'].strip(), int(row['quota']))

    for _, row in dance_scores_df.iterrows():
        dance = row['dance'].strip()
        dancer = dancers.get_dancer(row['email'])

        assert dance in dances, "Error. Dance with name %s not found in quotas file." % (
            dance)

        dances[dance].add_dancer(dancers.get_dancer(row['email']),
                                 row['score'])

    for dance in dances.values():
        dance.ready()

    print(len(dancers.anonymous_dancers))
    print(len(dancers.dancers.values()))

    return dances


QUOTAS_COLUMN_NAMES = ["dance", "quota"]
DANCE_SCORES_COLUMN_NAMES = ["dance", "name", "email", "score"]
DANCER_COLUMN_NAMES = [
    "timestamp", "email", "name", "year", "gender", "tshirt_size", "first_choice",
    "second_choice", "third_choice", "nonauditions"
]


def main(argv):
    assert len(argv) == 1, "Unrecognized arguments"

    # Make sure the files are passed in.
    assert FLAGS.quotas, "Must pass in a quotas file using --quotas=<filename>. \
        See quotas file for the format of the quotas file."

    assert FLAGS.dance_scores, "Must pass in a dance scores file using, \
        --dance_scores=<filename>. See dance_scores file for the format of the \
                dance_scores file."

    assert FLAGS.dancer_rankings, "Must pass in a dancer_rankings file using \
        --dancer_rankings=<filename>. See dance_scores file for the format of the \
        dance_scores file."

    # Load in all the files.
    quotas_df = pd.read_csv(FLAGS.quotas,
                            names=QUOTAS_COLUMN_NAMES,
                            keep_default_na=False, index_col=False)
    dance_scores_df = pd.read_csv(FLAGS.dance_scores,
                                  names=DANCE_SCORES_COLUMN_NAMES,
                            keep_default_na=False, index_col=False)
    dancer_rankings_df = pd.read_csv(FLAGS.dancer_rankings,
                                     names=DANCER_COLUMN_NAMES,
                            keep_default_na=False, index_col=False)

    # Make the data in an easier to work with format.
    dancers = create_dancers(dancer_rankings_df)
    dances = create_dances(quotas_df, dance_scores_df, dancers)

    # Set up the stable marriage preference list.
    dancer_prefs = {x.email: x.preferences for x in dancers}
    dance_prefs = {x.name: x.rankings for x in dances.values()}
    capacities = {x.name: x.quota for x in dances.values()}

    # Our matching algorithm is basically just the hospital matching algorithm.
    # https://en.wikipedia.org/wiki/Stable_marriage_problem
    for dance in dances:
        print(dance, dances[dance].rankings)


if __name__ == "__main__":
    app.run(main)
