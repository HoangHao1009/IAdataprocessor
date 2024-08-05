import os
import numpy as np

from dataclasses import dataclass
from question import Questionnaire
from response import Responsers

@dataclass
class survey_config:
    survey_id: str
    api_key: str
    env: str
    response_pages: 1

    def get_survey_url(self):
        return f'https://api.questionpro.{self.env}/a/api/v2/surveys/{self.survey_id}'

class Survey:
    def __init__(self, config):
        self.questionaire = Questionnaire(config)
        self.responsers = Responsers(config)

    def get_SPSS(self):
        return self.questionaire.commands
    
    def get_datasets(self, folder_path=False, spss_format=False):

        if not folder_path:
            result = {
                'dimResponser': self.responsers.dataframes.dimResponser.map(lambda x: None if x == '' else x),
                'dimQuestion': self.questionaire.dataframes.dimQuestion.map(lambda x: None if x == '' else x),
                'dimAnswer': self.questionaire.dataframes.dimAnswer.map(lambda x: None if x == '' else x),
                'Fact': self.responsers.dataframes.Fact.map(lambda x: None if x == '' else x)
            }

            return result
            
        else:
            self.responsers.dataframes.dimResponser.to_csv(os.path.join(folder_path, 'dimReponser.csv'))
            self.questionaire.dataframes.dimQuestion.to_csv(os.path.join(folder_path, 'dimQuestion.csv'))
            self.responsers.dataframes.dimAnswer.to_csv(os.path.join(folder_path, 'dimAnswer.csv'))
            self.responsers.dataframes.Fact.to_csv(os.path.join(folder_path, 'Fact.csv'))

        #spssformat: concat questioncode + scale -> spss question -> pivot


