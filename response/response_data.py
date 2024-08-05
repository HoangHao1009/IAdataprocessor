import pandas as pd

class ResponseData:
    def __init__(self, json):
        self.json = json
        self.dimResponser, self.Fact = self.get_data()

    def get_data(self):
        dimResp = pd.DataFrame(self.json)
        for i in ['country', 'region', 'latitude', 'longitude', 'radius', 'countryCode']:
            dimResp[f'location_{i}'] = dimResp['location'].apply(lambda x: x[i])
        
        Fact = dimResp.loc[:, ['responseID', 'responseSet']].explode('responseSet')

        dimResp.drop(['responseSet', 'location'], axis=1, inplace=True)


        for i in ['questionID', 'questionCode', 'answerValues']:
            Fact[i] = Fact['responseSet'].apply(lambda x: x[i])
        Fact = Fact.explode('answerValues')
        Fact['answerID'] = Fact['answerValues'].apply(lambda x: x['answerID'] if isinstance(x, dict) else x)
        Fact['answerText'] = Fact['answerText'].apply(lambda x: x['answerText'] if isinstance(x, dict) else x)
        Fact['answerScale'] = Fact['answerValues'].apply(lambda x: x['value']['scale'] if isinstance(x, dict) else x)
        Fact['answerdynamicExplodeText'] = Fact['answerValues'].apply(lambda x: x['value']['dynamicExplodeText'] if isinstance(x, dict) else x)
        Fact['answerValuesText'] = Fact['answerValues'].apply(lambda x: x['value']['text'] if isinstance(x, dict) else x)
        Fact['answerValuesText'] = Fact['answerValuesText'].map(lambda x: None if (x == '' or x == 'N/A') else x)
        Fact.drop(['responseSet', 'answerValues'], axis=1, inplace=True)
        Fact.dropna(subset=['answerID'], inplace=True)

        return dimResp, Fact
