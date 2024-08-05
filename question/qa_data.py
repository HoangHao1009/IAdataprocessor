import pandas as pd
from .spss import utils

class QuestionData:
    def __init__(self, json):
        self.json = json
        self.dimQuestion, self.dimAnswer = self.get_data()
    
    def get_data(self):
        root_df = pd.DataFrame(self.json)
        root_df['text'] = root_df['text'].apply(lambda x: utils.parse_html(x) if isinstance(x, str) else x)

        dimQuestion_col = ['questionID', 'blockID', 'type', 'text', 'code', 'orderNumber', 'required', 'randomizedRows', 'notApplicableAnswer', 'matrixType', 'minValue', 'maxValue']
        dimAnswer_col = ['questionID', 'code', 'rows', 'columns', 'answers']

        try:
            dimQuestion = root_df.loc[:, dimQuestion_col]
        except:
            dimQuestion = root_df.loc[:, ['questionID', 'blockID', 'type', 'text', 'code', 'orderNumber', 'required']]

        try:
            dimAnswer = root_df.loc[:, dimAnswer_col]
        except:
            dimAnswer = root_df.loc[:, ['questionID', 'code', 'rows', 'answers']]
            dimAnswer['columns'] = None

        dimAnswer = dimAnswer.explode('rows').explode('columns').explode('answers')

        dimAnswer['matrixOption'] = dimAnswer['rows'].apply(lambda x: x['text'] if isinstance(x, dict) else x)

        dimAnswer['columnText'] = dimAnswer['columns'].apply(lambda x: x['text'] if isinstance(x, dict) else x)
        dimAnswer['columnID'] = dimAnswer['columns'].apply(lambda x: x['columnID'] if isinstance(x, dict) else x)

        dimAnswer['answerID'] = dimAnswer['answers'].apply(lambda x: x['answerID'] if isinstance(x, dict) else x)
        dimAnswer['answerText'] = dimAnswer['answers'].apply(lambda x: x['text'] if isinstance(x, dict) else x)
        dimAnswer['answerOrderNumber'] = dimAnswer['answers'].apply(lambda x: x['orderNumber'] if isinstance(x, dict) else x)

        dimAnswer['answerText'] = dimAnswer['answerText'].fillna(dimAnswer['columnText'])
        dimAnswer['answerID'] = dimAnswer['answerID'].fillna(dimAnswer['columnID'])

        dimAnswer.drop(['rows', 'columns', 'answers', 'columnText', 'columnID'], axis=1, inplace=True)

        for i in ['answerText', 'matrixOption']:
            dimAnswer[i] = dimAnswer[i].apply(lambda x: utils.parse_html(x) if isinstance(x, str) else x)

        dimAnswer.rename(columns={'code': 'questionCode'})
        dimQuestion.rename(columns={'code': 'questionCode'})
        return dimQuestion, dimAnswer


