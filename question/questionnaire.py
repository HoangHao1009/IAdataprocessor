import requests
from .spss_processor import SPSS_Processor
from .qa_data import QuestionData


class Questionnaire(SPSS_Processor):
    def __init__(self, config):
        self.config = config
        self.json = self.get_json()
        
        super().__init__(self.json)

        self.dataframes = QuestionData(self.json)

    def get_json(self):
        question_url = self.config.get_survey_url() + '/questions?page=1&perPage=500'
        payload = {}
        headers = {
            'api-key': self.config.api_key
            }
        
        return  requests.request("GET", question_url , headers=headers, data=payload).json()['response']
