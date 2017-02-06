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
    Expand a nonterminal *randomly* based on a seed, stopping when reaching an excessive recursion
    Parameters
    ----------
    symbol : Nonterminal
        The starting symbol
    seed : str
        A string used as seed to choose a random element
    counter : int
        depth of the recursion, used to operate the deterministic choice
    max_depth : int
        the maximum recursion depth, if reached
    """
    def _produce(self, symbol, seed, counter, max_depth, max_depth_token):
        words = []
        productions = self.grammar.productions(lhs=symbol)
        production = self._deterministic_choice(productions, seed + str(counter))
        if counter > max_depth:
            # print(' --max recursion reached--')
            words.append(max_depth_token)
            return True, words
        # print('picked expansion ' + str(production) + ' for ' + str(symbol) + ' at counter ' + str(counter))
        is_truncated = False
        for (i, sym) in enumerate(production.rhs()):
            if isinstance(sym, str):
                words.append(sym)
            else:
                trunc, extension = self._produce(sym, seed, counter + 1 + i,  max_depth, max_depth_token)
                is_truncated = is_truncated or trunc
                words.extend(extension)
        return is_truncated, words

    def generate(self, seed, max_depth=100, max_depth_token=' --max recursion reached-- '):
        return self._produce(self.gr.start(), seed, 0, max_depth, max_depth_token)



