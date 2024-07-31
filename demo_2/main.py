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