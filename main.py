from utils import function
from utils import spss

class Processor:
    def __init__(self, api_key, env, survey_id):
        self.question_json = function.getjson(api_key, env, survey_id)
        self.SPSS_syntax, self.SPSS_quesion = spss.get_SPSS_syntax(self.question_json)
        self.topbottom_question = []
        self.scale_question = []

    def create_topbottom(self, question_list):
        for question in question_list:
            if question not in self.SPSS_question:
                raise ValueError('Question not in SPSS Question List')
            self.SPSS_syntax.append(spss.compute_topbottom(question))
            self.topbottom_question.append(question)
            self.add_SPSS_question(question)
    def create_scale(self, question_list):
        for question in question_list:
            if question not in self.SPSS_question:
                raise ValueError('Question not in SPSS Question List')
            self.SPSS_syntax.append(spss.compute_scale(question))
            self.scale_question.append(question)
            self.add_SPSS_question(question)

    def sort_SPSS_question(self, block_order):
        self.block_order = block_order
        self.SPSS_question = sorted(
            self.SPSS_quesion,
            key = lambda item: function.custom_sort(item, block_order)
        )

    def add_SPSS_question(self, question):
        if self.block_order:
            self.SPSS_question = sorted(
                self.SPSS_quesion.append(question),
                key = lambda item: function.custom_sort(item, self.block_order)
            )
        else:
            self.SPSS_question = self.SPSS_question.append(question)

    def add_SPSS_syntax(self, syntax, pre=True):
        if pre:
            self.SPSS_syntax = syntax + self.SPSS_syntax
        else:
            self.SPSS_syntax += syntax