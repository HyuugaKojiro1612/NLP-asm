from model.parser import ParserUtil, PARSER, LEXER
from model.database import GrammaticalRelation

def get_header(text):
    return "======== " + text + " ========\n"

def solve1():
    grammar = PARSER + LEXER
    with open("output/p2-q-$1.txt", "w", encoding="utf-8") as file:
        file.write(grammar)

def solve2():
    with open("input/questions.txt", "r", encoding="utf-8") as file:
        questions = file.readlines()
    
    # i = 5
    # print(questions[i].strip())
    # print(ParserUtil.get_semantic_tree(questions[i].strip()))
    
    with open("output/p2-q-$2.txt", "w", encoding="utf-8") as file:
        for question in questions:
            # print(question.strip())
            file.write(ParserUtil.get_semantic_tree(question.strip()))
            file.write('\n')

def solve3():
    with open("input/data.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    with open("output/p2-q-$3.txt", "w", encoding="utf-8") as file:
        for line in lines:
            GramRel = GrammaticalRelation()
            rel = GramRel.get_grammatical_relation(line.strip()[1:-1])
            # print(rel)
            file.write(rel)
            file.write('\n')
            
def solve4():
    with open("input/questions.txt", "r", encoding="utf-8") as file:
        questions = file.readlines()
    # i = 5
    # print(questions[i].strip())
    # print(ParserUtil.get_logical_form(questions[i].strip()))
    
    with open("output/p2-q-$4.txt", "w", encoding="utf-8") as file:
        file.write(get_header("LOGICAL-FORM"))
        for question in questions:
            # print(question.strip())
            file.write(ParserUtil.get_logical_form(question.strip()))
            file.write('\n')
        
        file.write(get_header("SEMANTIC-PROCEDURE"))
        for question in questions:
            # print(question.strip())
            file.write(ParserUtil.get_semantic_procedure(question.strip()))
            file.write('\n')

def solve4_5():
    with open("input/questions.txt", "r", encoding="utf-8") as file:
        questions = file.readlines()
    i = 5
    print(questions[i].strip())
    print(ParserUtil.get_semantic_procedure(questions[i].strip()))
    
def solve5():
    with open("input/questions.txt", "r", encoding="utf-8") as file:
        questions = file.readlines()
    # i = 5
    # print(questions[i].strip())
    # print(ParserUtil.get_answer(questions[i].strip()))
    
    with open("output/p2-q-$5.txt", "w", encoding="utf-8") as file:
        for question in questions:
            # print(question.strip())
            file.write(ParserUtil.get_answer(question.strip()))
            file.write('\n')

solve1()
solve2()
solve3()
solve4()
solve5()
