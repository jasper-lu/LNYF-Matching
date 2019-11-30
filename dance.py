import numpy as np
import pandas as pd
import random


class Dances:

    def __init__(self):
        self.dances = {}

    def __contains__(self, dance_name):
        return dance_name in self.dances

    def __getitem__(self, dance_name):
        return self.dances[dance_name]

    def __iter__(self):
        return iter(self.dances.values())

    def add_dance(self, dance):
        self.dances[dance.name] = dance

    def to_pandas_df(self):
        d = {dance.name: dance.to_pandas_df() for dance in self.dances.values()}
        return pd.concat(d)


class Dance:

    def __init__(self, dance_name, quota):
        self.name = dance_name
        self.quota = quota
        self.matchings = []
        self.unmatched = []
        self.scores = {}
        # First list is for purple rankings (0)
        # Second list is for green rankings (1), etc.
        self.rankings = [[], [], []]
        self.reds = []
        self.is_ready = False

    def add_dancer(self, dancer, ranking):
        assert self.is_ready == False, "Cannot add dancers after the dance is ready for matching."
        if ranking == 3:
            self.reds.append(dancer)
        else:
            self.rankings[ranking].append(dancer)

        self.scores[dancer.name] = ranking

        dancer.ratings[self.name] = ranking

    # Creates the preference list once the dance is done collecting dancers and rankings.
    # Really I should be using a builder class here, but whatever.
    def ready(self):
        assert self.is_ready == False
        # Again, like with dancers, if a dance ranked n people as the same score,
        # then we can just shuffle the list to get an ordering from 1 to n.
        for x in self.rankings:
            random.shuffle(x)

        # Flatten the list of lists.
        self.rankings = [item for sublist in self.rankings for item in sublist]

        self.ready = True

    def set_matchings(self, matching):
        self.matchings = matching

        for x in self.rankings:
            if x not in self.matchings:
                self.unmatched.append(x)

    def get_score(self, dancer_email):
        return self.original_score[dancer_email]

    def to_pandas_df(self, include_unmatched=True):
        matched_dfs = [
            x.to_pandas_df(mask=["Dance", "Nonaudition Dances"])
            for x in self.matchings
        ]

        matched_dfs = pd.concat(matched_dfs)

        d = {'Matched': matched_dfs}

        if include_unmatched and self.unmatched:
            unmatched_dfs = [
                x.to_pandas_df(mask=["Dance", "Nonaudition Dances"])
                for x in self.unmatched
            ]

            unmatched_dfs = pd.concat(unmatched_dfs)

            d['Unmatched'] = unmatched_dfs

        if self.reds:

            rejected_dfs = [
                x.to_pandas_df(mask=["Dance", "Nonaudition Dances"])
                for x in self.reds
            ]

            rejected_dfs = pd.concat(rejected_dfs)

            d['Rejected'] = rejected_dfs

        return pd.concat(d)
