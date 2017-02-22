from nltk import FeatureEarleyChartParser, Variable
from nltk import grammar as nltkgr
import xxhash

__all__ = ['SampleGenerator']


class SampleGenerator:
    def __init__(self, grammar):
        self.grammar = nltkgr.FeatureGrammar.fromstring(grammar)
        parser = FeatureEarleyChartParser(self.grammar)
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
    Checks that the left side of a production respects a feature dictionary.
    Parameters
    ----------
    production : Production
        the production to check
    features : dict
        the feature dictionary that the production LHS must not contradict
    """
    @staticmethod
    def _respects(production, features):
        return all(map(lambda feat:
                       feat not in features or isinstance(production.lhs()[feat], Variable) or features[feat] == production.lhs()[feat],
                       production.lhs().keys()))

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
    max_depth_token : str
        the replacement string to use when reaching maximum depth
    bound_features : dict
        the features to consider bound when expanding this nonterminal
    """
    def _produce(self, symbol, seed, counter, max_depth, max_depth_token, bound_features):
        words = []
        productions = list(filter(lambda p : self._respects(p, bound_features), self.grammar.productions(lhs=symbol)))
        if len(productions) == 0:
            if len(bound_features) > 0:
                raise Exception('Cannot find a production for ' + str(symbol) + ' with the features ' + str(bound_features))
            else:
                raise Exception('Cannot find a production for ' + str(symbol))
        production = self._deterministic_choice(productions, seed + str(counter))
        # by picking a production, was a feature bound?
        # For example, symbol had GEN=?x and a production lhs with GEN=m was picked
        # in that case th value will be returner to the caller to bound the next nonterminal in its RHS
        bound_variables = {}
        for bound_candidate in production.lhs().keys():
            if bound_candidate not in symbol:
                continue
                # raise Exception('cannot find feature "' + str(bound_candidate) + '" to be bound, among the ones of the nonterminal ' + symbol.unicode_repr() )
            if isinstance(symbol[bound_candidate], Variable):
                bound_variables[bound_candidate] = production.lhs()[bound_candidate]
        if counter > max_depth:
            # print(' --max recursion reached--')
            words.append(max_depth_token)
            return True, words
        # print('picked expansion ' + str(production) + ' for ' + str(symbol) + ' at counter ' + str(counter))
        is_truncated = False
        # additionally, the lhs may have had variables, like NN[NUM=?x, GEN=?y] -> SOMETHING[NUM=?x] ...
        # in that case these has to be bound, too
        bound_placeholders = {}
        for bound_candidate in production.lhs().keys():
            if bound_candidate not in bound_features.keys():
                continue
            if isinstance(symbol[bound_candidate], Variable):
                bound_placeholders[bound_candidate] = bound_features[bound_candidate]
        for (i, sym) in enumerate(production.rhs()):
            if isinstance(sym, str):
                words.append(sym)
            else:
                # if sym has a key like '?x' and that is in bound placeholders, set it as a bounded valued in recursive call
                nonterminal_bound_feats = {}
                for key, value in sym.items():
                    if value in bound_placeholders.keys():
                        nonterminal_bound_feats[key] = bound_placeholders[value]
                    if not isinstance(value, Variable):
                        nonterminal_bound_feats[key] = value
                    else:
                        if key in bound_placeholders:
                            nonterminal_bound_feats[key] = bound_placeholders[key]

                trunc, extension, bounded_variables = self._produce(sym, seed, counter + 1 + i,  max_depth, max_depth_token, nonterminal_bound_feats)
                for key, value in bounded_variables.items():
                    bound_placeholders[sym[key]] = value
                is_truncated = is_truncated or trunc
                words.extend(extension)
        return is_truncated, words, bound_variables

    def generate(self, seed, max_depth=100, max_depth_token=' --max recursion reached-- '):
        return self._produce(self.gr.start(), seed, 0, max_depth, max_depth_token, {})



