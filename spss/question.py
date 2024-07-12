from . import syntax
from . import utils

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

    q_text = utils.parse_html(q_text)

    return q_type, q_code, q_text, options

class question:
    def __init__(self, info):
        self.commands = []
        self.option_codes = []
        self.q_type, self.q_code, self.q_text, self.options = take_qinfo(info)
        self.json = info

    def get_option_codes(self):
        return sorted(self.option_codes, utils.custom_sort)

class sa(question):
    def __init__(self, info):
        super().__init__(info)

        if self.q_type != 'multiplechoice_radio':
            raise ValueError(f'Question {self.q_type} is not a SA')

        var_label_command = syntax.var_label(self.q_code, self.q_text)

        value_label_dict = {}
        for index, answer in enumerate(self.options):
            index = index + 1
            o_text = answer['text']
            value_label_dict[index] = o_text
        value_label_command = syntax.value_label(self.q_code, value_label_dict)

        self.commands.extend([var_label_command, value_label_command])
    
    def get_topbottom(self, topbottom_scale='1-5'):
        return syntax.compute_topbottom(self.q_code, topbottom_scale)
    
    def get_scale(self, type):
        return syntax.compute_topbottom(self.q_code, type)


class ma(question):
    def __init__(self, info):
        super().__init__(info)
        if self.q_type != 'multiplechoice_checkbox':
            raise ValueError(f'Question {self.q_type} is not a MA')
        
        var_label_command = []
        value_label_command = []
        
        for index, answer in enumerate(self.options):
            index = index + 1
            o_text = answer['text']
            o_code = f'{self.q_code}A{index}'
            o_label = f'{self.q_text}_{o_text}'

            var_label_command.append(syntax.var_label(o_code, o_label))
            value_label_command.append(syntax.value_label(o_code, {1: o_text}))

            self.option_codes.append(o_code)
        mrset_command = syntax.mrset(o_code, o_text, self.option_codes)
        self.commands.extend(var_label_command)
        self.commands.extend(value_label_command)
        self.commands.append(mrset_command)

class rank(question):
    def __init__(self, info):
        super().__init__(info)

        if self.q_type != 'rank_order_dropdown':
            raise ValueError(f'Question {self.q_type} is not a RANK')
        
        var_label_command = []
        value_label_command = []
        
        value_label_dict = {}
        for index, answer in enumerate(self.options):
            o_text = utils.parse_html(answer['text'])
            index = index + 1
            o_code = f'{self.q_code}RANK{index}'
            o_label = f'{self.q_text}_RANK{index}'
            self.option_codes.append(o_code)
            value_label_dict[index] = o_text

            var_label_command.append(syntax.var_label(o_code, o_label))

        for a_code in self.option_codes:
            value_label_command.append(syntax.value_label(a_code, value_label_dict))

        self.commands.extend(var_label_command + value_label_command)
        
class matrix(question):
    def __init__(self, info):
        super().__init__(info)

        if self.q_type != 'matrix_radio':
            raise ValueError(f'Question {self.q_type} is not a RANK')
        
        var_label_command = []
        value_label_command = []


        for index, row in enumerate(self.options):
            value_label_dict = {}
            r_text = row['text']
            index = index + 1
            o_code = f'{self.q_code}R{index}'
            o_label = f'{self.q_text}_{r_text}'
            var_label_command.append(syntax.var_label(o_code, o_label))

            self.option_codes.append(o_code)

            for col_index, column in enumerate(row['columns']):
                col_index = col_index + 1
                col_text = column['text']
                value_label_dict[col_index] = col_text
            value_label_command.append(syntax.value_label(o_code, value_label_dict))

            self.commands.extend(var_label_command + value_label_command)

class text:
    pass

class numeric:
    pass

class topbottom(question):
    def __init__(info):
        super().__init__()

