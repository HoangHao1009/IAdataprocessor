import requests


class Responsers:
    def __init__(self, config):
        survey_url = config.get_survey_url()
        self.api_key = config.api_key
        self.response_urls = [survey_url + f'/responses?page={i+1}&perPage=100' for i in range(config.response_pages)]
        self.json = self.get_requests()

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
