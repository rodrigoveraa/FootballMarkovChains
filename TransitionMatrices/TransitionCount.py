from Defs import NewStates
import itertools

class TransitionCount:

    def __init__(self, states_used) -> None:
        self.counts = {}
        for t in list(itertools.product(states_used, repeat=2)):
            self.counts[t] = 0

    def get_amount(self, state1, state2):
        return self.counts[(state1, state2)]

    def add(self, state1, state2):
        self.counts[(state1, state2)] += 1

    def get_counts_from_state(self, state):
        state_counts = {}
        for k in self.counts:
            if k[0] == state:
                state_counts[k] = self.counts[k]
        return state_counts