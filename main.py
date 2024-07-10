from utils import function
from utils import spss

class Processor:
    def __init__(self, api_key, env, survey_id):
        self.question_json = function.getjson(api_key, env, survey_id)
        self.SPSS_syntax, self.SPSS_quesion = spss.get_SPSS_syntax(self.question_json)
        self.topbottom_question = []
        self.scale_question = []

    def all_question(self, block_order):
        self.block_order = block_order
        all_question = []
        for type, question_list in self.SPSS_quesion.items():
            all_question += question_list
        return sorted(
            all_question,
            key = lambda item: function.custom_sort(item, block_order)
        )

    def add_SPSS_question(self, question, type):
        if self.block_order:
            self.SPSS_question[type] = sorted(
                self.SPSS_quesion[type].append(question),
                key = function.custom_sort
            )
        else:
            self.SPSS_question[type] = self.SPSS_question[type].append(question)

    def add_SPSS_syntax(self, syntax, pre=True):
        if pre:
            self.SPSS_syntax = syntax + self.SPSS_syntax
        else:
            self.SPSS_syntax += syntax


    def create_topbottom(self, question_list, type='1-5'):
        for question in question_list:
            if question not in self.SPSS_question:
                raise ValueError('Question not in SPSS Question List')
            
            self.SPSS_syntax.append(spss.compute_topbottom(question, type))
            self.topbottom_question.append(question)
            self.add_SPSS_question(question)

    def create_scale(self, question_list):
        for question in question_list:
            if question not in self.SPSS_question:
                raise ValueError('Question not in SPSS Question List')
            self.SPSS_syntax.append(spss.compute_scale(question))
            self.scale_question.append(question)
            self.add_SPSS_question(question)

