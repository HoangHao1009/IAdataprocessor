import requests
import pandas as pd

class Responsers:
    def __init__(self, config):
        survey_url = config.get_survey_url()
        self.api_key = config.api_key
        self.response_urls = [survey_url + f'/responses?page={i+1}&perPage=100' for i in range(config.response_pages)]
        self.json = self.get_requests()
        self.dimResp, self.Fact = self.get_data()

    def get_requests(self):
        responses = []
        for link in self.response_urls:
            payload = {}
            headers = {
            'api-key': f'{self.api_key}'
            }

            response = requests.request("GET", link, headers=headers, data=payload)
            responses.extend(response.json()['response'])
        return responses
    
    def get_data(self):
        dimResp = pd.DataFrame(self.json)
        for i in ['country', 'region', 'latitude', 'longitude', 'radius', 'countryCode']:
            dimResp[f'location_{i}'] = dimResp['location'].apply(lambda x: x[i])
        
        Fact = dimResp.loc[:, ['responseID', 'responseSet']].explode('responseSet')

        dimResp.drop(['responseSet', 'location'], axis=1, inplace=True)


        for i in ['questionID', 'questionCode', 'questionText', 'answerValues']:
            Fact[i] = Fact['responseSet'].apply(lambda x: x[i])
        Fact = Fact.explode('answerValues')
        Fact['answerID'] = Fact['answerValues'].apply(lambda x: x['answerID'] if isinstance(x, dict) else x)
        # Fact['answerText'] = Fact['answerValues'].apply(lambda x: x['answerText'] if isinstance(x, dict) else x)
        # Fact['answerScale'] = Fact['answerValues'].apply(lambda x: x['value']['scale'] if isinstance(x, dict) else x)
        # Fact['dynamicExplodeText'] = Fact['answerValues'].apply(lambda x: x['value']['dynamicExplodeText'] if isinstance(x, dict) else x)
        # Fact['answerValuesText'] = Fact['answerValues'].apply(lambda x: x['value']['text'] if isinstance(x, dict) else x)
        Fact.drop(['responseSet', 'answerValues'], axis=1, inplace=True)
        Fact.dropna(subset=['answerID'], inplace=True)

        return dimResp, Fact
