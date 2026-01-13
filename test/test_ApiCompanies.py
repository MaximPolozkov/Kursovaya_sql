import unittest
import requests
import requests_mock
from src.kursovayasql.ApiCompanies import ApiCompanies


class TestApiCompanies(unittest.TestCase):

    def test_get_companies_success(self):
        """Тест успешного получения списка компаний."""
        expected_companies = [{'id': '1', 'name': 'Company 1'}, {'id': '2', 'name': 'Company 2'}]
        with requests_mock.Mocker() as m:
            m.get('https://api.hh.ru/employers', json={'items': expected_companies})
            companies = ApiCompanies.get_companies()
            self.assertEqual(companies, expected_companies)

    def test_get_companies_empty_response(self):
        """Тест обработки пустого ответа API."""
        with requests_mock.Mocker() as m:
            m.get('https://api.hh.ru/employers', json={'items': []})
            companies = ApiCompanies.get_companies()
            self.assertEqual(companies, [])

    def test_get_companies_request_error(self):
        """Тест обработки ошибки при запросе к API."""
        with requests_mock.Mocker() as m:
            m.get('https://api.hh.ru/employers', exc=requests.exceptions.RequestException)
            # в данном случае лучше добавить обработку исключения в саму функцию get_companies
            # иначе тест не имеет смысла
            with self.assertRaises(requests.exceptions.RequestException):
                ApiCompanies.get_companies()