import requests


class GetVacancies:

    @staticmethod
    def find_company_id(company_name):
        """Получает вакансии по id компании"""
        BASE_URL = 'https://api.hh.ru/'
        url_vacancies = f"{BASE_URL}employers?text={company_name}"
        response = requests.get(url_vacancies)
        if response.status_code == 200:
            items = response.json()['items']
            if items:
                return items[0]['id']
        return None

    @staticmethod
    def get_vacancies(company_name):
        """Получает вакансии по названию компании"""
        BASE_URL = 'https://api.hh.ru/'
        company_id = GetVacancies.find_company_id(company_name)
        if company_id:
            url = f"{BASE_URL}vacancies?employers_id={company_id}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()['items']
        return None


if __name__ == "__main__":
    vacancies = GetVacancies()
    pol = vacancies.get_vacancies('0000')
    print(pol)
