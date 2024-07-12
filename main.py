from spss import utils
import spss

class Processor:
    def __init__(self, api_key, env, survey_id):
        self.question_json = utils.getjson(api_key, env, survey_id)
        self.spss_question = {'SA': [], 'T': [], 'N': [], 'TB': [], 'S': [],
                              'MA': {}, 'R': {}, 'MT': {}}
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

    def get_question_code(self, block_order):
        def custom_extend(result_list, item):
            if isinstance(item, list):
                result_list.extend(item)
            else:
                for v in item.values():
                    result_list.extend(v)
            return result_list
        result = []
        for q_type, value in self.spss_question.items():
            if q_type in ['SA', 'MT', 'R', 'TB', 'S']:
                result = custom_extend(result, value)
            elif q_type == 'MA':    
                result.extend(value.keys())    

        return sorted(result, key=lambda item: utils.custom_sort(item, block_order))
    
    def get_all_command(self):
        commands = []
        for q_obj in self.question_objects:
            commands.extend(q_obj.commands)
        self.commands = commands
        
    #topbottom, mean, std, ctab
    def get_topbottom_scale(self, question_list=[], topbottom_range='1-5'):

        for q_obj in self.question_objects:
            if q_obj.q_code in question_list:
                tb_new_question, tb_command = q_obj.get_topbottom(topbottom_range)
                scale_new_question, scale_command = q_obj.get_scale()

                if isinstance(q_obj, spss.sa):
                    self.spss_question['TB'].append(tb_new_question)
                    self.spss_question['S'].append(scale_new_question)
                    self.commands.extend([tb_command, scale_command])
                elif isinstance(q_obj, spss.matrix):
                    self.spss_question['TB'].extend(tb_new_question)
                    self.spss_question['S'].extend(scale_new_question)
                    for i in [tb_command, scale_command]:
                        self.commands.extend(i)

    # Columns -> Ctab: compute new var
    def calculate_dict(self, rows_code=None, col_perc=False, std=False, block_order=None):
        if rows_code == None and block_order == None:
            raise ValueError('You must specify rows_code or block_order')
        elif rows_code == None:
            print('if2')
            rows_code = self.get_question_code(block_order)
        else:
            print('else')
        
        result = {}
        for question in rows_code:
            print(question)
            if question in self.spss_question['S']:
                if std:
                    result[question] = ['Mean', 'Std']
                else:
                    result[question] = ['Mean']
            else:
                if col_perc:
                    result[question] = ['ColPct']
                else:
                    result[question] = ['Count']
        return result
