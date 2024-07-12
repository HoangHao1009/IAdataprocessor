from spss import utils
import spss

class Processor:
    def __init__(self, api_key, env, survey_id):
        self.question_json = utils.getjson(api_key, env, survey_id)
        self.spss_question = {'SA': [], 'T': [], 'N': [], 'TB_S': []}
        self.spss_question['MA'] = {}
        self.spss_question['R'] = {}
        self.spss_question['MT'] = {}
        self.question_objects = []
        self.commands = []

    def get_SPSS(self):
        for question in self.question_json:
            q_type = question['type']
            if q_type == 'multiplechoice_radio':
                q_obj = spss.sa(question)
                self.spss_question['SA'].append(q_obj.q_code)
            
            elif q_type == 'multiplechoice_checkbox':
                q_obj = spss.ma(question)
                self.spss_question['MA'][f'${q_obj.q_code}'] = q_obj.option_codes

            elif q_type == 'rank_order_dropdown':
                q_obj = spss.rank(question)
                self.spss_question['R'][q_obj.q_code] = q_obj.option_codes

            elif q_type == 'matrix_radio':
                q_obj = spss.matrix(question)
                self.spss_question['MT'][q_obj.q_code] = q_obj.option_codes

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
                if q_type in ['SA', 'MA', 'R', 'MT', 'TB_S']:
                    try:
                        result.extend(value)
                    except:
                        result.extend(value.keys())
        return sorted(result, key=lambda item: utils.custom_sort(item, block_order))
    
    def get_all_command(self):
        commands = []
        for q_obj in self.question_objects:
            commands.extend(q_obj.commands)
        self.commands = commands
        
    #topbottom, mean, std, ctab
    def get_topbottom_scale(self, question_list=[], topbottom_range='1-5', compute_std=True):

        for q_obj in self.question_objects:
            if q_obj.q_code in question_list:
                if isinstance(q_obj, spss.sa):
                    tb_new_question, tb_command = q_obj.get_topbottom(topbottom_range)
                    mean_new_question, mean_command = q_obj.get_scale('mean')
                    std_new_question, std_command = q_obj.get_scale('std')
                    self.spss_question['TB_S'].extend([tb_new_question, mean_new_question])
                    self.commands.extend([tb_command, mean_command])
                    if compute_std:
                        self.spss_question['TB_S'].append(std_new_question)
                        self.commands.append(std_command)
                elif isinstance(q_obj, spss.matrix):
                    tb_new_question, tb_command = q_obj.get_topbottom(topbottom_range)
                    mean_new_question, mean_command = q_obj.get_scale('mean')
                    std_new_question, std_command = q_obj.get_scale('std')
                    for i in [tb_new_question, mean_new_question]:
                        self.spss_question['TB_S'].extend(i)
                    for i in [tb_command, mean_command]:
                        self.commands.extend(i)
                    if compute_std:
                        self.spss_question['TB_S'].extend(std_new_question)
                        self.commands.extend(std_command)

    # Columns -> Ctab: compute new var
