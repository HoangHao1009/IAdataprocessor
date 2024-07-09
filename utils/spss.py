from . import function

question_type = {
    'T': ['text_single_row', 'text_numeric', 'static_presentation_text'],
    'N': ['numeric_slider'],
    'SA': ['multiplechoice_radio'],
    'MA': ['multiplechoice_checkbox'],
    'MT': ['matrix_radio'],
    'R': ['rank_order_dropdown']
}

def delete(question, delete_list, max_length=80):
    filter_condition = []
    current_line = ''
    for i in delete_list:
        new_line = current_line + f'{question} = {i} OR '
        if len(new_line) > max_length:
            filter_condition.append(current_line)
            current_line = ''
        current_line = new_line

        filter_condition.append(current_line)

        command = ' \n'.join(filter_condition).rstrip(' OR ')

        return f'''
SELECT IF NOT ({command}).
EXECUTE.
'''
    
def var_label(question, label):
    return f'VARIABLE LABELS {question} "{label}".'

def value_label(question, label_dict):
    lable = ''
    for i, v in label_dict.items():
        lable += f'{i} "{v}"\n'
    return f'VALUE LABELS {question} {lable.rstrip('\n')}.'

def mrset(question, question_label, list_answer):
    return f'''
MRSETS /MDGROUP NAME=${question}
LABEL="{question_label}"
CATEGORYLABELS=COUNTEDVALUES
VARIABLES={' '.join(list_answer)}
VALUE=1
/DISPLAY NAME=[${question}].
'''

def ctab(cols, calc_type=dict, comparetest_type=["MEAN"], alpha=0.1):
    def table_code(calc_type):
        code = '/TABLE '
        cal_command = {
            'Count': '[C][COUNT F40.0, TOTALS[COUNT F40.0]]',
            'ColPct': '[C][COLPCT.COUNT PCT40.0, TOTALS[COUNT F40.0]]',
            'Mean': '[MEAN COMMA40.2]',
            'Std': '[STDDEV COMMA40.2]'
        }

        for question, cal in calc_type.items():
            code += f'{question} {cal_command[cal]} + \n'
        return code.rstrip(' + \n')
    
    def by_code(cols):
        return f'BY + {' + '.join(cols)}'
    
    def compare_code(comparetest_type, alpha):
        code = '/COMPARE'
        for test in comparetest_type:
            code += f'''
TYPE={test} ALPHA={alpha} ADJUST=NONE ORIGIN=COLUMN INCLUDEMRSETS=YES
    CATEGORIES=ALLVISIBLE MEANSVARIANCE=TESTEDCATS MERGE=YES STYLE=SIMPLE SHOWSIG=NO
'''
    return f'''
CTABLES
{table_code(calc_type)}
{by_code(cols)}
/SLABELS POSITION=ROW VISIBLE=NO
/CATEGORIES VARIABLES=ALL
    EMPTY=INCLUDE TOTAL=YES POSITION=BEFORE
{compare_code(comparetest_type)}.
'''

def compute_topbottom(question):
    question_tb = f'{question}1TB'
    return f'''
COMPUTE {question_tb} = 0.
IF ({question} = 1 OR {question} = 2) {question_tb} = 1.
IF ({question} = 3) {question_tb} = 2.
IF ({question} = 4 OR {question} = 5) {question_tb} = 3.
{var_label(question_tb, f'{question}. Top to Bottom Boxes')}
{value_label(question_tb, {1: 'Bottom 2 boxes', 2: 'Neutral', 3: 'Top 2 boxes'})}
EXECUTE.
'''

def compute_scale(question):
    question_scale = f'{question}1S'
    return f'''
COMPUTE {question_scale} = {question}.
VARIABLE LEVEL {question_scale} (SCALE).
{var_label(question_scale, f'{question}. Scale')}
EXECUTE.
'''

def export(folder_path):
    return f'''
OUTPUT EXPORT
/CONTENTS  EXPORT=VISIBLE  LAYERS=PRINTSETTING  MODELVIEWS=PRINTSETTING
/XLSX  DOCUMENTFILE='{folder_path}'
    OPERATION=CREATEFILE
    LOCATION=LASTCOLUMN  NOTESCAPTIONS=NO.
'''

def get_SPSS_syntax(question_json=list):
    SPSS_syntax = []
    SPSS_question = []
    for question in question_json:
        q_type, q_code  = question['type'], question['code']
        q_text = function.parse_html(question['text']).split('?')[0]
        try:
            q_answer = question['answers']
        except:
            q_row = question['rows']

        if q_type in question_type['SA']:
            var_label_command = var_label(q_code, q_text)
            value_label_dict = {}
            for index, answer in enumerate(q_answer):
                a_text = answer['text']
                value_label_dict[index+1] = function.parse_html(a_text)
            value_label_command = value_label(q_code, value_label_dict)

            SPSS_question.append(q_code)
            SPSS_syntax += [var_label_command, value_label_command]

        elif q_type in question_type['MA']:
            a_list = []
            for index, answer in enumerate(q_answer):
                index = index + 1
                a_text = function.parse_html(answer['text'])
                a_code = f'{q_code}A{index}'
                a_label = f'{q_text}_{a_text}'

                var_label_command = var_label(a_code, a_label)
                value_label_command = value_label_command(a_code, {1: a_text})
                SPSS_syntax += [var_label_command, value_label_command]

                a_list.append(a_code)
            mrset_command = mrset(q_code, q_text, a_list)
            SPSS_syntax.append(mrset_command)
            SPSS_question.append(a_code)

        elif q_type in question_type['R']:
            a_list = []
            value_label_dict = {}
            for index, answer in enumerate(q_answer):
                a_text = function.parse_html(answer['text'])
                index = index + 1
                a_code = f'{q_code}RANK{index}'
                a_label = f'{q_text}_RANK{index}'
                a_list.append(a_code)
                value_label_dict[index] = a_text

                var_label_command = var_label(a_code, a_label)
                SPSS_syntax.append(var_label_command)

            for a_code in a_list:
                value_label_command = value_label(a_code, value_label_dict)
                SPSS_question.append(a_code)
                SPSS_syntax.append(var_label_command)
        
        elif q_type in question_type['MT']:
            for index, row in enumerate(question['rows']):
                value_label_dict = {}
                r_text = function.parse_html(row['text'])
                index = index + 1
                a_code = f'{q_code}R{index}'
                a_label = f'{q_text}_{r_text}'
                var_label_command = var_label(a_code, a_label)

                for col_index, column in enumerate(row['columns']):
                    col_index = col_index + 1
                    col_text = function.parse_html(column['text'])
                    value_label_dict[col_index] = col_text
                SPSS_syntax += [var_label_command, value_label_command]
                SPSS_question.append(a_code)

        return SPSS_syntax, SPSS_question
