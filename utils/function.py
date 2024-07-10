import re
from bs4 import BeautifulSoup
import requests

def getjson(api_key, env, survey_id):
    survey_url = f'https://api.questionpro.{env}/a/api/v2/surveys/{survey_id}'
    question_url = survey_url + '/questions?page=1&perPage=500'
    payload = {}
    headers = {
        'api-key': api_key
        }
    return requests.request("GET", question_url , headers=headers, data=payload).json()['response']


def custom_sort(item, priority_list):
    # # Loại bỏ ký tự '$'
    # item = item.lstrip('$')

    # # Tìm vị trí của chữ số đầu tiên
    # match = re.search(r'\d+', item)
    # if match:
    #     # Tách phần chữ cái và phần số
    #     prefix = item[:match.start()]
    #     number = int(match.group())

    #     # Lấy thứ tự ưu tiên của phần chữ cái từ priority_list
    #     prefix_priority = priority_list.index(prefix) if prefix in priority_list else len(priority_list)

    #     # Trả về tuple (thứ tự ưu tiên, số)
    #     return prefix_priority, number
    # else:
    #     # Nếu không có số, trả về phần chữ cái và 0
    #     return priority_list.index(item) if item in priority_list else len(priority_list), 0

    item = item.lstrip('$').upper()

    parts = re.findall()

    key = []
    for letter, number in parts:
        if letter in priority_list:
            key.append(priority_list.index(letter))
        else:
            print(f'{letter} not in block order')
            key.append(len(priority_list))
        if number:
            key.append(int(number))
    
    return key



    
def parse_html(text):
    if '<' in text and '>' in text:
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
    return text

