import pytest
from nltkgen.sample_generator import sample_generator

class TestGenerator:
    def test_instantiate(self):
        self.gen = sample_generator.SampleGenerator("""
        S -> EXP
        EXP -> DIGIT | EXP ' + ' EXP | EXP ' * ' EXP | FUN '(' EXP ')' | DIGIT '.' DIGIT
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

    def check_determinism(self):
        assert self.gen.generate('aaa') == self.gen.generate('aaa')
        assert self.gen.generate('aasdf') == self.gen.generate('aasdf')

        for x in range(10):
            print(''.join(self.gen.generate('ser' + str(x))))
