from nltkgen.sample_generator import sample_generator
import string, random
import re
digits_pattern = re.compile("^[0-9]+$")


# generate a random seed
def seed_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


with open('titoli_giornali.fcfg', 'r', encoding='utf8') as grammar_file:
    gram = grammar_file.read()
    gen = sample_generator.SampleGenerator(gram)


def to_clean_text(tokens):
    clean_tokens = []
    for i, t in enumerate(tokens):
        if i > 0:
            if digits_pattern.match(t) and digits_pattern.match(tokens[i - 1]):
                clean_tokens.extend(t)
                continue
            if t[0] == ',':
                clean_tokens.extend(t)
                continue
        clean_tokens.extend(' ' + t)
    return ''.join(clean_tokens)


for xx in range(10):
    seed = seed_generator()
    print(seed)
    print('     ', to_clean_text(gen.generate(seed)[1]))
