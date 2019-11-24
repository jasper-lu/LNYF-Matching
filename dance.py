import random

class Dance:

    def __init__(self, dance_name, quota):
        self.name = dance_name
        self.quota = quota
        self.preferences = []
        self.matched = []
        self.unmatched = []
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
            self.rankings[ranking].append(dancer.email)

        # Keep track of what score the dancer got.
        dancer.add_score(self.name, ranking)

    # Creates the preference list once the dance is done collecting dancers and rankings.
    # Once this method is called, the class is in a fundamentally different state than before.
    # I think this is poor design, but whatever.
    def ready(self):
        # Again, like with dancers, if a dance ranked n people as the same score,
        # then we can just shuffle the list to get an ordering from 1 to n.
        for x in self.rankings:
            random.shuffle(x)

        # Flatten the list of lists.
        self.rankings = [item for sublist in self.rankings for item in sublist]

        self.ready = True
