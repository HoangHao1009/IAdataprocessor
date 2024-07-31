import os

from dataclasses import dataclass
from question import Questionnaire
from response import Responsers

@dataclass
class survey_config:
    survey_id: str
    api_key: str
    env: str
    response_pages = 1

    def get_survey_url(self):
        return f'https://api.questionpro.{self.env}/a/api/v2/surveys/{self.survey_id}'

class Survey:
    def __init__(self, config):
        self.questionaire = Questionnaire(config)
        self.response = Responsers(config)

    def get_SPSS(self):
        return Questionnaire.get_all_command()
    
    def get_responseDf(self):
        return Responsers.dfs
    
    def get_sql(self, folder_path):
        qa = Questionnaire.qa.to_csv(os.path.join(folder_path, 'qa.csv'))
        resp_info = Responsers.dfs['resp_info'].to_csv(os.path.join(folder_path, 'resp_info.csv'))
        resp_answers = Responsers.dfs['resp_answers'].to_csv(os.path.join(folder_path, 'resp_answers.csv'))
