import re
from lark import Lark, Tree, Token
from lark.visitors import Interpreter


PARSER = '''
    start: list_tour_query
                    | run_time_query
                    | count_tour_query
                    | transport_query
                    | list_day_query
                
    list_tour_query : service_np service_vp Y_N_PHRASE Q_MARK
    run_time_query  : tour_vp time_vp Q_MARK
    count_tour_query: tour_np tour_vp Q_PHRASE PPRO Q_MARK
    transport_query : tour_np tour_vp Q_PHRASE Q_MARK
    list_day_query  : tour_vp day_vp Q_PHRASE Q_MARK
    
    service_np      : PRO
    tour_np         : ALL tour_cnp
                    | tour_cnp
    tour_cnp        : PLURAL TOUR_N
                    | CITY_NAME
                    | TOUR_N CITY_NAME
                    | tour_how_many
    time_np         : time_cnp
    time_cnp        : run_time_wh
    transport_np    : transport_cnp
    transport_cnp   : transport_wh
    day_np          : PLURAL day_cnp
    day_cnp         : day_wh
    
    
    service_vp      : AUX service_vp
                    | SERVICE_V tour_np
    time_vp         : TIME_V time_np
    tour_vp         : TOUR_V tour_pp
                    | TOUR_V tour_np
                    | TOUR_V transport_pp
    day_vp          : DAY_V day_np
    
    
    tour_pp         : tour_pp tour_pp
                    | P tour_np
    transport_pp    : P transport_np
    
    run_time_wh     : QDET_HOW_LONG
    tour_how_many   : QDET_HOW_MANY TOUR_N
    transport_wh    : TRANSPORT QDET_WHICH
    day_wh          : DAY QDET_WHICH
'''
LEXER = '''
    QDET_HOW_LONG   : "bao lâu"
    QDET_HOW_MANY   : "có bao nhiêu"
    QDET_WHICH      : "gì" | "nào"
    
    SERVICE_V       : REPEAT
    TIME_V          : TAKE
    TOUR_V          : GO
    DAY_V           : HAVE
    
    P               : FROM | TO | BY
    
    TOUR_N          : "tour"
    TRANSPORT       : "phương tiện"
    DAY             : "ngày"
    CITY_NAME       : "Hồ Chí Minh" | "Đà Nẵng" | "Nha Trang" | "Phú Quốc"
    
    DEPART          : GO " " FROM
    ARRIVE          : GO | TO
    TRAVEL          : GO " " BY
    
    GO              : "đi"
    FROM            : "từ"
    TO              : "tới"
    BY              : "bằng"
    
    HAVE            : "có"
    PLURAL          : "các" | "những"
    ALL             : "tất cả"
    TAKE            : "hết"
    REPEAT          : "nhắc lại"
    PRO             : "em"
    PPRO            : "bạn"
    AUX             : "có thể"
    
    Y_N_PHRASE      : "được không"
    Q_PHRASE        : "vậy" | "nhỉ"
    Q_MARK          : "?"
'''
MIXIN = '''
    %ignore " "
'''

class ParserUtil:
    rules = LEXER + PARSER + MIXIN
    parser = Lark(rules)
    
    @staticmethod
    def parse(input):
        return ParserUtil.parser.parse(input)
    
    @staticmethod
    def get_semantic_tree(input):
        tree = ParserUtil.parse(input)
        formatted_tree = PrintTreeVisitor().visit(tree).replace('_', '-')
        # print(formatted_tree)
        return formatted_tree
    
    @staticmethod
    def get_logical_form(input):
        tree = ParserUtil.parse(input)
        logical_form = LogicalFormVisitor().visit(tree)
        # print(logical_form)
        return logical_form
        
    @staticmethod
    def get_semantic_procedure(input):
        tree = ParserUtil.parse(input)
        logical_form = LogicalFormVisitor().visit(tree)
        semantic_procedure = SemanticProcedureGenerator().get_semantic_procedure(logical_form)
        # print(semantic_procedure)
        return semantic_procedure
    
    @staticmethod
    def get_answer(input):
        tree = ParserUtil.parse(input)
        logical_form = LogicalFormVisitor().visit(tree)
        semantic_procedure = SemanticProcedureGenerator().get_semantic_procedure(logical_form)
        answer = ModelQuery().execute(semantic_procedure)
        # print(answer)
        return answer
    
class PrintTreeVisitor(Interpreter):
    def start(self, tree):
        return self.tree_to_string(tree.children[0])

    def tree_to_string(self, tree):
        rule = tree.data.upper()
        children = tree.children
        result = ""

        for i, child in enumerate(children):
            if isinstance(child, Token):
                result += "(" + child.type + " " + child.value + ")"
            if isinstance(child, Tree):
                result += self.tree_to_string(child)
            if i < len(children) - 1:
                result += " "
        return rule + "(" + result + ")"

class LogicalFormVisitor(Interpreter):
    def start(self, tree):
        return self.get_logical_form(tree)
        
    def get_logical_form(self, tree):
        propositions = self.visit(tree.children[0])
        sentence_type = propositions.pop(0)
        event = propositions.pop(0)

        result = ""
        for prop in propositions:
            result += "[{}]".format(prop)
        result = "({} ({} {}))".format(sentence_type, event, result).replace("TOUR_N", "TOUR")
        return result
        
    def list_tour_query(self, tree):
        agent = self.visit(tree.children[0])[0].replace("ROLE", "AGENT")
        theme = self.visit(tree.children[1])[0].replace("ROLE", "THEME")
        return ["COMMAND", "REPEAT e", agent, theme]
    
    def run_time_query(self, tree):
        theme = self.visit(tree.children[1])[0].replace("ROLE", "THEME")
        from_loc = self.visit(tree.children[0])[0].replace("ROLE", "FROM-LOC")
        to_loc = self.visit(tree.children[0])[1].replace("ROLE", "TO-LOC")
        return ["WH-QUERY", "TAKE e", theme, from_loc, to_loc]

    def count_tour_query(self, tree):
        theme = self.visit(tree.children[0])[0].replace("ROLE", "THEME")
        to_loc = self.visit(tree.children[1])[0].replace("ROLE", "TO-LOC")
        return ["WH-QUERY", "GO e", theme, to_loc]
    
    def transport_query(self, tree): 
        theme = self.visit(tree.children[0])[1].replace("ROLE", "THEME")
        to_loc = self.visit(tree.children[0])[0].replace("ROLE", "TO-LOC")
        instr = self.visit(tree.children[1])[0].replace("ROLE", "INSTR")
        return ["WH-QUERY", "GO e", theme, to_loc, instr]
    
    def list_day_query(self, tree): 
        theme = self.visit(tree.children[1])[0].replace("ROLE", "THEME")
        to_loc = self.visit(tree.children[0])[0].replace("ROLE", "TO-LOC")
        return ["WH-QUERY", "HAVE e", theme, to_loc]
        
    def service_np(self, tree):
        constant = tree.children[0].type
        value = tree.children[0].value.upper()
        variable = constant[0].lower()
        return ["ROLE ({} {} {})".format(constant, variable, value)]
    
    def tour_np(self, tree):
        if len(tree.children) > 1:
            quantifier = tree.children[0].type
            return ["ROLE <{} {}>".format(quantifier, self.visit(tree.children[-1])[0])]
        else:
            return self.visit(tree.children[-1])
    
    def tour_cnp(self, tree):
        if isinstance(tree.children[0], Tree):
            return self.visit(tree.children[0])
        elif tree.children[0].type == "PLURAL":
            constant = tree.children[-1].type
            variable = constant[0].lower()
            return ["{} {}".format(variable, constant)]
        constant = tree.children[-1].type.replace('_', '-')
        value = tree.children[-1].value
        variable = value[0].lower()
        result = ['ROLE ({} {} "{}")'.format(constant, variable, value)]
        if len(tree.children) > 1:
            constant2 = tree.children[0].type
            variable2 = constant2[0].lower()
            result += ["ROLE ({} {})".format(constant2, variable2)]
        return result
            
    def time_np(self, tree):
        return self.visit(tree.children[0])
    
    def time_cnp(self, tree):
        return self.visit(tree.children[0])
    
    def transport_np(self, tree):
        return self.visit(tree.children[0])
    
    def transport_cnp(self, tree):
        return self.visit(tree.children[0])
    
    def day_np(self, tree):
        return self.visit(tree.children[-1])
    
    def day_cnp(self, tree):
        return self.visit(tree.children[-1])
    
    def service_vp(self, tree):
        return self.visit(tree.children[-1])
    
    def time_vp(self, tree):
        return self.visit(tree.children[-1])
    
    def tour_vp(self, tree):
        return self.visit(tree.children[-1])
    
    def day_vp(self, tree):
        return self.visit(tree.children[-1])
    
    def tour_pp(self, tree):
        if isinstance(tree.children[0], Tree):
            from_pp = self.visit(tree.children[0])
            to_pp = self.visit(tree.children[-1])
            return from_pp + to_pp
        else:
            return self.visit(tree.children[-1])
    
    def transport_pp(self, tree):
        return self.visit(tree.children[-1])
    
    def run_time_wh(self, tree):
        return ["ROLE <WH w RUN-TIME>"]
    
    def tour_how_many(self, tree):
        constant = tree.children[-1].type
        variable = constant[0].lower()
        return ["ROLE <HOW-MANY {} {}>".format(variable, constant)]
    
    def transport_wh(self, tree):
        constant = tree.children[0].type
        return ["ROLE <WH w {}>".format(constant)]
    
    def day_wh(self, tree):
        constant = tree.children[0].type
        return ["ROLE <WH w {}>".format(constant)]
        

class SemanticProcedureGenerator(Interpreter):
    
    def __init__(self):
        self.symbol_table = {
            "TOUR": "?t",
            "RUN-TIME": "?r",
            "TRANSPORT": "?ts",
            "ATIME": "?a",
            "DAY": "?a",
            "CITY-NAME": "?cn",
            "CITY-CODE": "?cc",
        }
        self.query_mapping = {
            "TOUR": "TOUR",
            "RUN-TIME": "RUN-TIME",
            "TRANSPORT": "BY",
            "DAY": "ATIME"
        }
        self.city_code = {
            "Hồ Chí Minh": "HCM",
            "Phú Quốc": "PQ",
            "Đà Nẵng": "DN",
            "Nha Trang": "NT",
        }
    
    def transform(self, logical_form):
        propositions = re.findall("\[(.*?)\]", logical_form)
        if "COMMAND" in logical_form:
            propositions.pop(0)
        
        query = "PRINT-ALL"
        tokens = []
        constant = ""
        var = ""
        if "HOW-MANY" in logical_form:
            query = "COUNT"
        
        for prop in propositions:
            q = re.findall("<(.*?)>", prop)
            if q != []:
                constant = self.query_mapping[q[0].split(' ')[2]]
                var = self.symbol_table[q[0].split(' ')[2]]
            else:    
                p = re.findall("\"(.*?)\"", prop)
                if p == []: continue
                tokens += [p[0]]
        
        literals = []    
        if len(tokens) == 0:
            literals += ["({} {} ?cn)".format(constant, var)]
        elif len(tokens) == 2:
            literals += ["({} ?t {} {} {})".format(constant, self.city_code[tokens[0]], self.city_code[tokens[1]], var)]
        elif len(tokens) == 1 and query == "COUNT":
            literals += ["({} {} {})".format(constant, var, tokens[0].replace(' ', '_'))]
        elif len(tokens) == 1 and constant == "BY":
            literals += ["(TOUR ?t {})".format(tokens[0].replace(' ', '_'))]
            literals += ["({} ?t {})".format(constant, var)]
        else: # len(tokens) == 1 and constant == "ATIME"
            literals += ["(TOUR ?t {})".format(tokens[0].replace(' ', '_'))]
            literals += ["({} ?t ?cc {})".format(constant, var)]
        
        res = ""
        for lit in literals:
            res += ' ' + lit     
        return query + ' ' + var + res
                
    def get_semantic_procedure(self, logical_form):            
        return self.transform(logical_form)           
                


class ModelQuery(): 
    def __init__(self):
        self.answers = {}
        self.variables = ["?t", "?cn", "?r", "?ts", "?a", "?cc"]
        for var in self.variables:
            self.answers[var] = []
            
        self.database = None
        with open("input/data.txt", "r", encoding="utf-8") as file:
            self.database = file.readlines()
            
    def execute(self, sem_pro):
        request = sem_pro.split(' ')[0]
        question = sem_pro.split(' ')[1]
        literals = re.findall("\((.*?)\)", sem_pro)
        for lit in literals:
            self.search_answers(lit)
        
        if request == "COUNT":
            return str(len(self.answers[question]))
        
        res = ""
        # print('ans', self.answers)
        for ans in self.answers[question]:
            res += ans + ' '
        return res
    
    def search_answers(self, literal):
        lit_tokens = literal.split(' ')
        for data in self.database:
            data_tokens = data.strip()[1:-1].split(' ')
            # print(data_tokens)
            # print(lit_tokens)
            if data_tokens[0] == lit_tokens[0]:
                if data_tokens[0] == "TOUR" and data_tokens[2] == lit_tokens[2]:
                    self.answers[lit_tokens[1]] += [data_tokens[1]]
                    
                elif data_tokens[0] == "TOUR" and lit_tokens[2] == "?cn":
                    self.answers[lit_tokens[1]] += [data_tokens[1]]
                    self.answers[lit_tokens[2]] += [data_tokens[2]]
                    
                elif data_tokens[0] == "RUN-TIME" and data_tokens[2] == lit_tokens[2] and data_tokens[3] == lit_tokens[3]:
                    self.answers[lit_tokens[1]] += [data_tokens[1]]
                    self.answers[lit_tokens[4]] += [data_tokens[4] + ' ' + data_tokens[5]]
                    
                elif data_tokens[0] == "BY":
                    if data_tokens[1] in self.answers[lit_tokens[1]]:
                        self.answers[lit_tokens[2]] += [data_tokens[2]]
                        
                elif data_tokens[0] == "ATIME":
                    if data_tokens[1] in self.answers[lit_tokens[1]]:
                        self.answers[lit_tokens[3]] += [data_tokens[3] + ' ' + data_tokens[4]]