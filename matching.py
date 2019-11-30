from dancer import Dancer, Dancers
from dance import Dance
import random


# Our matching algorithm is basically just the hospital resident matching algorithm.
# https://en.wikipedia.org/wiki/Stable_marriage_problem
# Classes are named as such to reflect that.
class Player:

    def __init__(self, name):
        self.name = name
        self.prefs = None
        self.matching = None

    # Get the player's favorite in prefs that they are not currently matched with, or None
    def get_favorite(self):
        return self.prefs and self.prefs[0] or None

    def match(self, other):
        self.matching = other

    def unmatch(self, other):
        self.matching = None

    def set_preferences(self, prefs):
        self.prefs = prefs
        self.pref_names = [x.name for x in prefs]

    def forget(self, other):
        prefs = self.prefs[:]
        if other in prefs:
            prefs.remove(other)
        self.prefs = prefs


class Hospital(Player):

    def __init__(self, name, capacity):
        super().__init__(name)
        self.capacity = capacity
        self.matching = []

    def match(self, other):
        self.matching.append(other)
        self.matching.sort(key=self.prefs.index)

    def unmatch(self, other):
        matching = self.matching
        matching.remove(other)
        self.matching = matching


def match_pair(a, b):
    a.match(b)
    b.match(a)


def unmatch_pair(a, b):
    a.unmatch(b)
    b.unmatch(a)


def delete_pair(a, b):
    a.forget(b)
    b.forget(a)


def match_dancers(dancers, dances, shuffle=True):
    # The algorithm here biases toward dancer preferences
    # i.e. a dancer who ranks urban dance first, but gets a purple in
    # kpop and a green in urban dance will more likely be placed in
    # urban dance.
    dancer_players = [Player(x.email) for x in dancers]
    dance_players = [Hospital(x.name, x.quota) for x in dances]

    # Add in a little more randomness.
    if shuffle:
        random.shuffle(dancer_players)

    def set_prefs():
        dancer_players_dict = {x.name: x for x in dancer_players}
        dance_players_dict = {x.name: x for x in dance_players}

        for dancer_name, dancer in dancer_players_dict.items():
            dancer_obj = dancers[dancer_name]
            prefs = [dance_players_dict[x] for x in dancer_obj.preferences]
            dancer.set_preferences(prefs)

        for dance_name, dance in dance_players_dict.items():
            dance_obj = dances[dance_name]
            prefs = [dancer_players_dict[x.email] for x in dance_obj.rankings]
            dance.set_preferences(prefs)

    set_prefs()

    # Run the algorithm until the matching is stable.
    while dancer_players:
        dancer = dancer_players.pop()
        dance = dancer.get_favorite()

        # If the dancer is in the reds of the dance, or wasn't ranked, then remove them because
        # they will never be matched to that dance.
        # Keep going until we get a dance that the dancer can actually be ranked with.
        # This is to incentivize people to be true to their dance preferences, instead
        # of playing the game of "I didn't do well in soran auditions, so I should
        # rank it lower."
        while dance and dancer not in dance.prefs:
            dancer.forget(dance)
            dance = dancer.get_favorite()

        # Too bad lol. The dancer ran out of dances to be matched to.
        if not dance:
            continue

        match_pair(dance, dancer)

        # The dance is over capacity now, so kick out the person with the worst ranking
        if len(dance.matching) > dance.capacity:
            worst_match = dance.matching[-1]
            unmatch_pair(dance, worst_match)
            # Put the player back in consideration for other dances.
            dancer_players.append(worst_match)

        # Once a dance has reached capacity, it won't consider any dancers
        # ranked lower than the dancer with the current worst ranking.
        # So, delete those pairs.
        if len(dance.matching) == dance.capacity:
            worst_match = dance.matching[-1]
            to_forget = dance.prefs[dance.prefs.index(worst_match) + 1:]
            for dancer_to_forget in to_forget:
                delete_pair(dance, dancer_to_forget)

    # Algorithm has finished running. Return the matchings.
    return {d: d.matching for d in dance_players}
