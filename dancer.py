from absl import logging as log
import numpy as np
import pandas as pd
import random

class Dancers:

    def __init__(self):
        self.dancers = {}
        self.anonymous_dancers = []
        self.duplicates = []

    def add_dancer(self, dancer):
        if dancer.email in self.dancers:
            log.info("Dancer with email %s is duplicated. Pls fix.", dancer.email)
            self.duplicates.append(dancer.email)
            
        self.dancers[dancer.email] = dancer

    # If dancer corresponding to the row exists, returns dancer.
    # Otherwise, creates a new, anonymous dancer.
    def get_dancer(self, email):
        dancer = self.dancers.get(email, None)
        if not dancer:
            dancer = Dancer.from_email(email)
            self.anonymous_dancers.append(dancer)
            self.add_dancer(dancer)
            log.info(
                "Could not find dance ranking for dancer with email %s!", email)
            log.info("Either they forgot to fill out a dance ranking form, or gave a different email to the choreographer. Will not match dancer with email %s...", email)

        return dancer

    def get_dancer_prefs(self, email):
        return self.dancers[email].preferences

    def to_pandas_df(self):
        dfs = [dancer.to_pandas_df() for dancer in self.dancers.values()]
        return pd.concat(dfs)

    def __contains__(self, email):
        return email in self.dancers

    def __getitem__(self, email):
        return self.get_dancer(email)

    def __iter__(self):
        return iter(self.dancers.values())

DANCER_OUTPUT_COLUMN_NAMES = np.array([
    "Email", "Name", "Year", "Gender", "T-Shirt Size", "Dance", "Ratings", "Nonaudition Dances", "Didn't Rank"
])
NUMBER_TO_COLOR = ["Purple", "Green", "Yellow", "Red"]

class Dancer:

    def __init__(self, email, name="", year=0, gender="?", tshirt_size="", pref_tier = {}, preferences=[], nonauditions=[]):
        self.email = email
        self.name = name
        self.year = year
        self.gender = gender
        self.tshirt_size = tshirt_size
        self.pref_tier = pref_tier
        self.preferences = preferences
        self.nonauditions = nonauditions
        self.didnt_pref = []
        self.dance = None
        self.ratings = {} 

    def preffed(self, dance_name):
        return dance_name in self.preferences

    def add_didnt_pref(self, dance_name):
        self.didnt_pref.append(dance_name)

    def to_pandas_df(self, mask=[]):
        index_mask = [np.where(DANCER_OUTPUT_COLUMN_NAMES == x)[0][0] for x in mask]
        mask = np.ones(len(DANCER_OUTPUT_COLUMN_NAMES), dtype=bool)
        mask[index_mask] = False

        columns = DANCER_OUTPUT_COLUMN_NAMES[mask,...]

        assigned_dance = self.dance if self.dance else ""
        
        other_dances = []
        for k, v in self.ratings.items():
            pref_tier = self.pref_tier.get(k, "didn't rank")
            other_dances.append("(%s, %s, %s)" %(k, NUMBER_TO_COLOR[v], pref_tier))
        other_dances = ', '.join(other_dances)

        nonaudition_dances = ', '.join(self.nonauditions)

        didnts = ', '.join(self.didnt_pref)

        row = np.array([self.email, self.name, self.year, self.gender, self.tshirt_size,
            assigned_dance, other_dances, nonaudition_dances, didnts])

        row = row[mask, ...]
        
        df = pd.DataFrame([row], columns=columns)
        return df

    @classmethod
    def from_pandas_row(cls, dancer_row):
        choices = [
            dancer_row["first_choice"], dancer_row["second_choice"],
            dancer_row["third_choice"]
        ]

        # i.e. "Haka, K-Pop" -> ["Haka", "K-Pop"]
        choices = list(filter(None, choices))
        choices = [[y.strip() for y in x.split(',')] for x in choices]
        
        pref_tier = {}
        for i, x in enumerate(choices):
            for y in x:
                pref_tier[y] = i

        # If a dancer puts two dances as first choice, we assume they care
        # about both equally. In that case, randomly choosing one to be their
        # first choice among all dances, and one to be second choice among all
        # dances is fine.
        # (Some dancers try to game the system by ranking two dances first,
        # but really it doesn't make a difference).
        for x in choices:
            random.shuffle(x)
        # Flatten the list of lists.
        preferences = [item for sublist in choices for item in sublist]

        email = dancer_row["email"].strip().lower()
        name = dancer_row["name"].strip()
        year = dancer_row["year"]
        gender = dancer_row["gender"]
        tshirt_size = dancer_row["tshirt_size"]
        nonauditions = [x.strip() for x in dancer_row["nonauditions"].split(',')]
        
        return cls(email, name, year, gender, tshirt_size, pref_tier, preferences, nonauditions)

    @classmethod
    def from_email(cls, email):
        dumb_dancer = cls(email)
        return dumb_dancer
