import re
from lark import Lark, Tree, Token
from lark.visitors import Interpreter


parser = '''
    start: list_tour_query
                    | run_time_query
                    | count_tour_query
                    | transport_query
                    | list_day_query
                
    list_tour_query : QDET_LIST PLURAL tour_wh Q_MARK
    run_time_query  : DEPART city_np ARRIVE city_np TAKE run_time_wh Q_MARK
    count_tour_query: HAVE tour_how_many ARRIVE city_np Q_MARK
    transport_query : tour_np TRAVEL transport_wh Q_MARK
    list_day_query  : ARRIVE city_np HAVE PLURAL day_wh Q_MARK
    
    tour_wh         : TOUR
    run_time_wh     : QDET_HOW_LONG
    tour_how_many   : QDET_HOW_MANY tour_np
    transport_wh    : TRANSPORT QDET_WHICH
    day_wh          : DAY QDET_WHICH
    
    city_np         : CITY_NAME
    tour_np         : TOUR
                    | TOUR CITY_NAME
                    | TOUR ARRIVE CITY_NAME
    
'''
lexer = '''
    QDET_LIST       : "nhắc lại tất cả"
    QDET_HOW_LONG   : "bao lâu"
    QDET_HOW_MANY   : "bao nhiêu"
    QDET_WHICH      : "gì" | "nào"
    
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
    TAKE            : "hết"
    
    Q_MARK          : "?"
'''
mixin = '''
    %ignore " " | "em có thể" | "được không" | "vậy" | "nhỉ" | "bạn"
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

class LogicalFormVisitor(Interpreter): pass

class SemanticProcedureGenerator(Interpreter): pass

class ModelQuery(): pass
    