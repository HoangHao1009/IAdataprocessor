
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
    label = ''
    for i, v in label_dict.items():
        label += f'{i} "{v}"\n'
    label = label.rstrip('\n')
    return f"VALUE LABELS {question} {label}."

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
        return 'BY' + ' + '.join(cols)
    
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

def compute_topbottom(question, type = '1-5'):

    new_question = f'{question}TB'
    def take_command(type):
        if type == '1-5':
            if_command = f'''
IF ({question} = 1 OR {question} = 2) {new_question} = 1.
IF ({question} = 3) {question} = 2.
IF ({question} = 4 OR {question} = 5) {new_question} = 3.
    '''
            value_label_command = function.value_label(new_question, {1: 'Bottom 2 boxes', 2: 'Neutral', 3: 'Top 2 boxes'})
        elif type == '1-10':
            if_command = f'''
IF ({question} = 1 OR {question} = 2 OR {question} = 3 OR {question} = 4 OR {question} = 5) {new_question} = 1.
IF ({question} = 6 OR {question} = 7) {new_question} = 2.
IF ({question} = 8 OR {question} = 9 OR {question} = 10) {new_question} = 3.
    '''
            value_label_command = function.value_label(new_question, {1: 'Bottom 5 boxes', 2: 'Neutral', 3: 'Top 3 boxes'})
        return if_command, value_label_command

    if_command, value_label_command = take_command(type)

    return f'''
COMPUTE {question} = 0.
{if_command}
{function.var_label(new_question, f'{question} - Top to Bottom Boxes')}
{value_label_command}
EXECUTE.
'''

def compute_scale(question):
    question_scale = f'{question}S'
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
