import re
from lark import Lark, Tree, Token
from lark.visitors import Interpreter


parser = '''
    start: list_tour_query
                    | run_time_query
                    | count_tour_query
                    | transport_query
                    | list_day_query
                
    list_tour_query : service_np service_vp Y_N_PHRASE Q_MARK
    run_time_query  : tour_vp time_vp Q_MARK
    count_tour_query: tour_np tour_vp Q_PHRASE Q_MARK
    transport_query : tour_np tour_vp Q_PHRASE Q_MARK
    list_day_query  : tour_vp day_vp Q_PHRASE Q_MARK
    
    service_np      : PRO
    tour_np         : ALL tour_cnp
                    | tour_cnp
    tour_cnp        : PLURAL TOUR
                    | CITY_NAME
                    | TOUR CITY_NAME
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
    tour_how_many   : QDET_HOW_MANY TOUR
    transport_wh    : TRANSPORT QDET_WHICH
    day_wh          : DAY QDET_WHICH
'''
lexer = '''
    QDET_HOW_LONG   : "bao lâu"
    QDET_HOW_MANY   : "có bao nhiêu"
    QDET_WHICH      : "gì" | "nào"
    
    SERVICE_V       : REPEAT
    TIME_V          : TAKE
    TOUR_V          : GO
    DAY_V           : HAVE
    
    P               : FROM | TO | BY
    
    TOUR            : "tour"
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
    AUX             : "có thể"
    
    Y_N_PHRASE      : "được không"
    Q_PHRASE        : "vậy" | "vậy bạn" | "nhỉ"
    Q_MARK          : "?"
'''
mixin = '''
    %ignore " " | "được không" | "vậy" | "nhỉ" | "bạn"
'''

class ParserUtil:
    rules = lexer + parser + mixin
    parser = Lark(rules)
    
    @staticmethod
    def parse(input):
        return ParserUtil.parser.parse(input)
    
    @staticmethod
    def get_semantic_tree(input):
        tree = ParserUtil.parse(input)
        formatted_tree = PrintTreeVisitor().visit(tree)
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
        query, questions_pre, questions, literals = SemanticProcedureGenerator().parser(
            logical_form)
        answer = ModelQuery().execute(query, questions_pre, questions, literals)
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
        return self.get_logical_form(tree.children[0])
    
    def get_parts(self, tree):
        '''
        Return: [[agents], verb, [themes]]
        '''
        agents = []
        themes = []
        

class SemanticProcedureGenerator(Interpreter): pass

class ModelQuery(): pass
    