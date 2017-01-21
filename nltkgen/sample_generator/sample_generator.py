from nltk import CFG
from nltk import ChartParser
import xxhash

__all__ = ['SampleGenerator']

class SampleGenerator:
    def __init__(self, grammar):
        self.grammar = CFG.fromstring(grammar)
        parser = ChartParser(self.grammar)
        self.gr = parser.grammar()

    """
    Deterministic *random* choice based on a seed
    Parameters
    ----------
    choices : array
        List of elements, it must have a length and the get operation
    seed : str
        A string used as seed to choose a random element

    """
    @staticmethod
    def _deterministic_choice(choices, seed):
        xh = xxhash.xxh32()
        xh.update(seed)
        return choices[xh.intdigest() % len(choices)]

    """
    Expand a nonterminal *randomly* based on a seed
    Parameters
    ----------
    symbol : Nonterminal
        The starting symbol
    seed : str
        A string used as seed to choose a random element
    counter : int
        depth of the recursion, used to operate the deterministic choice
    """
    def _produce(self, symbol, seed, counter):
        words = []
        productions = self.grammar.productions(lhs=symbol)
        production = self._deterministic_choice(productions, seed + str(counter))
        for (i,sym) in enumerate(production.rhs()):
            if isinstance(sym, str):
                words.append(sym)
            else:
                words.extend(self._produce(sym, seed + str(i) + ' ', counter + 1))
        return words

    def generate(self, seed):
        return self._produce(self.gr.start(), seed, 0)



