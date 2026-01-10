import requests
import json


class ApiCompanies:

    @staticmethod
    def get_companies():
        BASE_URL = 'https://api.hh.ru/'
        companies = requests.get(BASE_URL + 'employers').json()['items']
        return json.dumps(companies, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    api = ApiCompanies()
    r = api.get_companies()
    print(r)
