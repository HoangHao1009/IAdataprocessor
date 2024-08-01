import requests
import pandas as pd
from .response_data import ResponseData

class Responsers:
    def __init__(self, config):
        self.config = config
        self.json = self.get_json()
        self.dataframes = ResponseData(self.json)

    def get_json(self):
        survey_url = self.config.get_survey_url()
        response_urls = [survey_url + f'/responses?page={i+1}&perPage=100' for i in range(self.config.response_pages)]

        responses = []
        for link in response_urls:
            payload = {}
            headers = {
                'api-key': f'{self.config.api_key}'
            }

            response = requests.request("GET", link, headers=headers, data=payload)
            responses.extend(response.json()['response'])
        return responses