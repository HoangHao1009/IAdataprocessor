from spss import utils
import spss

class Processor:
    def __init__(self, api_key, env, survey_id):
        self.question_json = utils.getjson(api_key, env, survey_id)
        self.origin_question = {'SA': [], 'MA': [], 'R': [], 'T': [],'N': []}
        self.spss_question = {'SA': [], 'R': [], 'T': [], 'N': [], 'TB_S': []}
        self.spss_question['MA'] = {}
        self.question_objects = []
        self.commands = []

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
                self.spss_question['MA'][f'${q_obj.q_code}'] = q_obj.option_codes

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

    def get_question_code(self, block_order, type='all'):
        result = []
        for q_type, value in self.spss_question.items():
            if type == 'all':
                try:
                    result.extend(value)
                except:
                    result.extend(value.keys())
            elif type == 'ctab':
                if q_type in ['SA', 'MA', 'R']:
                    try:
                        result.extend(value)
                    except:
                        result.extend(value.keys())
        return sorted(result, key=lambda item: utils.custom_sort(item, block_order))
    
    def get_all_command(self):
        for q_obj in self.question_objects:
            self.commands.extend(q_obj.commands)
        
    #topbottom, mean, std, ctab
    def get__topbottom_scale(self, question_list=[], topbottom_range='1-5', compute_std=True):

        for q_obj in self.question_objects:
            if q_obj.q_code in question_list:
                if isinstance(spss.sa, q_obj):
                    tb_new_question, tb_command = q_obj.get_topbottom(topbottom_range)
                    mean_new_question, mean_command = q_obj.get_scale('mean')
                    std_new_question, std_command = q_obj.get_scale('std')
                    self.spss_question['TB_S'].extend([tb_new_question, mean_new_question])
                    self.commands.extend([tb_command, mean_command])
                    if compute_std:
                        self.spss_question['TB_S'].append(std_new_question)
                        self.commands['TB_S'].append(std_command)



