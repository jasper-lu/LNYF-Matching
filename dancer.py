from absl import logging as log
import pandas as pd
import random

class Dancers:

    def __init__(self):
        self.dancers = {}
        self.anonymous_dancers = []

    def add_dancer(self, dancer):
        if dancer.email in self.dancers:
            log.info("Dancer with email %s is duplicated. Pls fix.")
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

    def __iter__(self):
        return iter(self.dancers.values())


class Dancer:

    def __init__(self):
        self.scores = {}

    def add_score(self, dance_name, score):
        self.scores[dance_name] = score
        self.preferences = []
        self.nonauditions = []

    @classmethod
    def from_pandas_row(cls, dancer_row):
        choices = [
            dancer_row["first_choice"], dancer_row["second_choice"],
            dancer_row["third_choice"]
        ]

        # i.e. "Haka, K-Pop" -> ["Haka", "K-Pop"]
        choices = list(filter(None, choices))
        print(choices)
        choices = [[y.strip() for y in x.split(',')] for x in choices]
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

        dancer = cls()
        dancer.email = dancer_row["email"].strip()
        dancer.name = dancer_row["name"].strip()
        dancer.year = dancer_row["year"]
        dancer.gender = dancer_row["gender"]
        dancer.tshirt_size = dancer_row["tshirt_size"]
        dancer.preferences = preferences
        dancer.nonauditions = [x.strip() for x in dancer_row["nonauditions"].split(',')]
        return dancer

    @classmethod
    def from_email(cls, email):
        dumb_dancer = cls()
        dumb_dancer.email = email
        return dumb_dancer
