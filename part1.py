import nltk
from nltk import CFG, grammar, parse
from nltk.parse.generate import generate


def fcfg_to_txt():
    with open("grammar.fcfg", "r", encoding='utf-8') as file:
        content = file.readlines()
    with open("output/grammar.txt", "w", encoding='utf-8') as file:
        file.writelines(content)


def generate_sentences():
    grammar_parser = parse.load_parser('grammar.fcfg')
    with open("output/samples.txt", "w", encoding='utf-8') as file:
        for sentence in generate(grammar_parser.grammar(), n=2000, depth=10):
            if grammar_parser.parse_one(sentence):
                file.write(' '.join(sentence))
                file.write('\n')
            
            
def parse_sentences():
    grammar_parser = parse.load_parser('grammar.fcfg')
    with open("input/sentences.txt", "r", encoding="utf-8") as file:
        sentences = file.readlines()
    
    with open("output/parse-results.txt", "w", encoding="utf-8") as file:
        for sentence in sentences:
            tokens = sentence.split()
            try:
                tree = grammar_parser.parse_one(tokens)
            except:
                tree = "()"
            # tree.draw()
            file.write(str(tree).replace('  ', '').replace('\n', ''))
            file.write('\n')


fcfg_to_txt()
generate_sentences()
parse_sentences()