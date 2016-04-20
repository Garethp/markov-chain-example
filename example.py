from collections import defaultdict, Counter
from numpy import cumsum, sum, searchsorted
from numpy.random import rand
from random import randint
import urllib2

class MarkovChain(object):
    # Initiate our MarkovChain
    def __init__(self, order=1):

        # Create our transitions
        self._transitions = defaultdict(int)

        # Set our order
        self._order = order

        # Create an empty list of letters
        self._symbols = list()

    # Train our chain on words
    def train(self, sequence):
        # Turn our words in to a list of characters
        sequence_list = list(set(sequence))

        # Add our sequence passed in to our chain
        self._symbols.extend(sequence_list)

        # For each character in our chain
        for i in range(len(sequence)-self._order):
            # "Letters i to i + 2 will be once more likely to be followed by i + 3"
            self._transitions[sequence[i:i+self._order], sequence[i+self._order]] += 1

    # Takes in input a string and predicts the next character.
    def predict(self, symbol):
        # We expect a certain amount of letters to get started
        if len(symbol) != self._order:
            raise ValueError('Expected string of %d chars, got %d' % (self._order, len(symbol)))

        # Grab the probably letters that come after the symbol passed in
        probs = [self._transitions[(symbol, s)] for s in self._symbols]

        # Add some weighted randomness to the result
        return self._symbols[self._weighted_pick(probs)]

    # Generates n characters from start.
    def generate(self, start, n):
        result = start

        # Foreach in n
        for i in range(n):
            # Get the next letter
            new = self.predict(start)

            # Add that letter to our output
            result += new

            # Our next start should be the new, minus the first letter of the old. So "abc" -> "abcd" -> "bcd"
            start = start[1:] + new
        return result

    # Weighted random selection returns n_picks random indexes. The chance to pick the index i is given by weights[i].
    @staticmethod
    def _weighted_pick(weights):
        return searchsorted(cumsum(weights), rand()*sum(weights))

# book = urllib2.urlopen('https://www.gutenberg.org/files/521/521-0.txt') # Robinson Crusoe
order = 15

in_text = ''

sherlock = open('sherlock.txt')
robinson_crusoe = open('robinsonCrusoe.txt')
shakespeare = open('shakespeare.txt')

in_text += sherlock.read()

mc = MarkovChain(order=order)
mc.train(in_text)
# mc.train(sherlock.read())
# mc.train(robinson_crusoe.read())

pos = randint(0, len(in_text) - order + 1)
start = in_text[pos:pos+order]
print(mc.generate(start, 10000))