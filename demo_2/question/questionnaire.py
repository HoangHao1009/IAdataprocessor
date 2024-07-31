import requests


class Questionnaire:
    def __init__(self, config):
        self.question_url = config.get_survey_url() + '/questions?page=1&perPage=500'
        payload = {}
        headers = {
            'api-key': config.api_key
            }
        
        self.json = requests.request("GET", self.question_url , headers=headers, data=payload).json()['response']
        
