from utils import function
from . import spss

class Processor:
    def __init__(self, api_key, env, survey_id):
        self.question_json = function.getjson(api_key, env, survey_id)
        self.origin_question = {'SA': [], 'MA': [], 'R': [], 'T': [],'N': []}
        self.spss_question = {'SA': [], 'MA': [], 'R': [], 'T': [],'N': []}
        self.question_objects = []

    def get_SPSS(self):
        for question in self.question_json:
            q_type = question['type']
            if q_type == 'multiplechoice_radio':
                q_obj = spss.sa(question)
                self.origin_question['SA'].append(q_obj.q_code)
                self.spss_question['SA'].append(q_obj.q_code)
            
            elif q_type == 'multiplechoice_checkbox':
                q_obj = spss.ma(question)
                self.origin_question['MA'].append(q_obj.q_code)
                self.spss_question['MA'].extend(q_obj.option_codes)

            elif q_type == 'rank_order_dropdown':
                q_obj = spss.rank(question)
                self.origin_question['R'].append(q_obj.q_code)
                self.spss_question['R'].extend(q_obj.option_codes)

            elif q_type == 'matrix_radio':
                q_obj = spss.matrix(question)
                self.origin_question['R'].append(q_obj.q_code)
                self.spss_question['R'].extend(q_obj.option_codes)

            #T and N
            self.question_objects.append(q_obj)

    def get_all_question_code(self, block_order):
        result = []
        for type, question_list in self.spss_question:
            result.extend(question_list)
        return sorted(result, key=lambda item: function.custom_sort(item, block_order))

    def get_all_command(self):
        commands = []
        for q_obj in self.question_objects:
            commands.extend(q_obj.commands)
        return commands
        
    #topbottom, mean, std, ctab
