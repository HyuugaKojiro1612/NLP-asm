from model.parser import ParserUtil

def get_dividers(index):
    return "======== Cau " + str(index) + " ========\n"

def main():
    with open("input/questions.txt", "r", encoding="utf-8") as file:
        questions = file.readlines()
    
    i = 0
    print(questions[i].strip())
    print(ParserUtil.get_semantic_tree(questions[i].strip()))
    
    with open("output/p2-q-$2.txt", "w", encoding="utf-8") as file:
        for question in questions:
            # print(question.strip())
            file.write(ParserUtil.get_semantic_tree(question.strip()))
            file.write('\n')
        
            
        

main()