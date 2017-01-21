from django.shortcuts import render
from django.http import HttpResponse
from sample_generator import sample_generator

def index(request):
    return render(request, 'generator/input_grammar.html', {
        'grammar_definition': """S -> EXP
EXP -> DIGIT | EXP ' + ' EXP | EXP ' * ' EXP | FUN '(' EXP ')' | DIGIT '.' DIGIT
DIGIT -> '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'| DIGIT DIGIT
FUN -> 'sin'|'sqrt'""",
    })

def generate(request):
    try:
        gen = sample_generator.SampleGenerator(request.POST['grammar_definition'])
        generated_text = ''.join(gen.generate(request.POST['seed']))
        return render(request, 'generator/input_grammar.html', {
            'grammar_definition': request.POST['grammar_definition'],
            'generated_text': generated_text,
            'seed': request.POST['seed'],
        })
    except ValueError:
        return render(request, 'generator/input_grammar.html', {
            'error_message': 'error in grammar definition',
            'grammar_definition': request.POST['grammar_definition'],
            'seed': request.POST['seed'],
        })
