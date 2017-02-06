import pytest
from nltkgen.sample_generator import sample_generator
import string, random


# generate a random seed
def seed_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class TestGenerator:
    def test_instantiate(self):
        gen = sample_generator.SampleGenerator("""
        S -> EXP
        EXP -> DIGIT | EXP ' + ' EXP | EXP ' * ' EXP | FUN '(' EXP ')' | DIGIT '.' DIGIT | EXP '/' EXP
        DIGIT -> '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'| DIGIT DIGIT
        FUN -> 'sin'|'sqrt'
        """)
        # no assertion, just check it doesn't fail

        with pytest.raises(ValueError):
            # the ---> symbol is a syntax error
            sample_generator.SampleGenerator("""
                    S ---> EXP
                    DIGIT -> '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'| DIGIT DIGIT
                    """)

    def test_check_determinism(self):
        gen = sample_generator.SampleGenerator("""
                S -> EXP
                EXP -> DIGIT | EXP ' + ' EXP | EXP ' * ' EXP | FUN '(' EXP ')' | DIGIT '.' DIGIT | EXP '/' EXP
                DIGIT -> '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'| DIGIT DIGIT
                FUN -> 'sin'|'sqrt'
                """)
        assert gen.generate('aaa') == gen.generate('aaa')
        assert gen.generate('aasdf') == gen.generate('aasdf')
        assert gen.generate('something something !!!') == gen.generate('something something !!!')
        assert gen.generate('something') != gen.generate('something else')

