import requests
from .spss_processor import SPSS_Processor


class Questionnaire():
    def __init__(self, config):
        self.config = config
        self.json = self.get_json()
        
        self.spss = SPSS_Processor(self.json)

        self.dataframes = QuestionData(self.json)

    def get_json(self):
        question_url = self.config.get_survey_url() + '/questions?page=1&perPage=500'
        payload = {}
        headers = {
            'api-key': self.config.api_key
            }
        
        return  requests.request("GET", question_url , headers=headers, data=payload).json()['response']
