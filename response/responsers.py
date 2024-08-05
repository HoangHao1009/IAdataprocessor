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
    
    def extract_info(self, feature, extract_name, function,scale=False):
        if feature in self.dataframes.dimResponser:
            self.dataframes.dimResponser[extract_name] = self.dataframes.dimResponser[feature].map(function)
        else:
            info_df = self.dataframes.Fact.query('questionCode == @feature')
            if not scale:
                info_df[extract_name] = info_df['answerText'].map(function)
            else:
                info_df[extract_name] = info_df['answerScale'].map(function)
            info_df = info_df.groupby(['responseID'])[extract_name].apply(list).reset_index()
            is_list = False
            for i in info_df[extract_name]:
                if isinstance(i, list) and len(i) > 1:
                    is_list = True
                    break
            print(f'is_list: {is_list}')
            if is_list == False:
                info_df[extract_name] = info_df[extract_name].apply(lambda x: x[0] if isinstance(x, list) else x)
            self.dataframes.dimResponser = pd.merge(self.dataframes.dimResponser, info_df[['responseID', extract_name]],
                                                    how='left', on='responseID')
