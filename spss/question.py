from . import syntax
from utils import function

origin_question = {
    'SA': [],
    'MA': [],
    'R': [],
    'T': [],
    'N': [],
}
spss_question = {
    'SA': [],
    'MA': [],
    'R': [],
    'T': [],
    'N': [],
}

def take_qinfo(info):
    q_type, q_code, q_text = info['type'], info['code'], info['text']
    try:
        options = info['answers']
    except:
        try:
            options = info['rows']
        except:
            print(f'{q_code} has no options')
            options = None

    return q_type, q_code, q_text, options
    

class sa:
    def __init__(self, info):
        self.var_label_command = []
        self.value_label_command = []

        self.q_type, self.q_code, self.q_text, self.options = take_qinfo(info)

        if self.q_type != 'multiplechoice_radio':
            raise ValueError(f'Question {self.q_type} is not a SA')

        self.json = info

        self.var_label_command.append(syntax.var_label(self.q_code, self.q_text))

        value_label_dict = {}
        for index, answer in enumerate(self.options):
            index = index + 1
            o_text = answer['text']
            value_label_dict[index+1] = function.parse_html(o_text)
        self.value_label_command.append(syntax.value_label(self.q_code, value_label_dict))


        self.commands = self.var_label_command + self.var_label_command
        origin_question['SA'].append(self.q_code)
        spss_question['SA'].append(self.q_code)

class ma:
    def __init__(self, info):
        self.q_type, self.q_code, self.q_text, self.options = take_qinfo(info)
        self.var_label_command = []
        self.value_label_command = []
        self.mrset_command = []
        self.option_codes = []

        if self.q_type != 'multiplechoice_checkbox':
            raise ValueError(f'Question {self.q_type} is not a MA')
        
        for index, answer in enumerate(self.options):
            index = index + 1
            o_text = function.parse_html(answer['text'])
            o_code = f'{self.q_code}A{index}'
            o_label = f'{self.q_text}_{o_text}'

            self.var_label_command.append(syntax.var_label(o_code, o_label))
            self.value_label_command.append(syntax.value_label(o_code, {1: o_text}))

            self.option_codes.append(o_code)
        self.mrset_command.append(syntax.mrset(o_code, o_text, self.option_codes))
        self.commands = self.var_label_command + self.value_label_command + self.mrset_command

        origin_question['MA'].append(self.q_code)
        spss_question['MA'] += self.option_codes

class rank:
    def __init__(self, info):
        self.q_type, self.q_code, self.q_text, self.options = take_qinfo(info)
        self.var_label_command = []
        self.value_label_command = []
        self.option_codes = []


        if self.q_type != 'rank_order_dropdown':
            raise ValueError(f'Question {self.q_type} is not a RANK')
        
        value_label_dict = {}
        for index, answer in enumerate(self.options):
            o_text = function.parse_html(answer['text'])
            index = index + 1
            o_code = f'{self.q_code}RANK{index}'
            o_label = f'{self.q_text}_RANK{index}'
            self.option_codes.append(o_code)
            value_label_dict[index] = o_text

            self.var_label_command.append(syntax.var_label(o_code, o_label))

        for a_code in self.option_codes:
            self.value_label_command.append(syntax.value_label(a_code, value_label_dict))

        self.commands = self.var_label_command + self.value_label_command
        
        origin_question['R'].append(self.q_code)
        spss_question['R'] += self.option_codes

class matrix:
    def __init__(self, info):
        self.q_type, self.q_code, self.q_text, self.options = take_qinfo(info)
        self.var_label_command = []
        self.value_label_command = []
        self.option_codes = []

        for index, row in enumerate(self.options):
            value_label_dict = {}
            r_text = function.parse_html(row['text'])
            index = index + 1
            o_code = f'{self.q_code}R{index}'
            o_label = f'{self.q_text}_{r_text}'
            self.var_label_command.append(syntax.var_label(o_code, o_label))

            self.option_codes.append(o_code)

            for col_index, column in enumerate(row['columns']):
                col_index = col_index + 1
                col_text = function.parse_html(column['text'])
                value_label_dict[col_index] = col_text
            self.value_label_command.append(syntax.value_label(o_code, value_label_dict))

            self.commands = self.var_label_command + self.value_label_command

            origin_question['R'].append(self.q_code)
            spss_question['R'] += self.option_codes

class text:
    pass

class numeric:
    pass


