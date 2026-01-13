import unittest
from unittest.mock import patch
import requests
from src.kursovayasql.GetVacancies import GetVacancies # Замените


class TestGetVacancies(unittest.TestCase):

    @patch('src.kursovayasql.GetVacancies.requests.get')
    def test_find_company_id_success(self, mock_get):
        """Тест успешного получения ID компании."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': [{'id': '12345'}]}

        company_id = GetVacancies.find_company_id('Test Company')

        self.assertEqual(company_id, '12345')
        mock_get.assert_called_once()

    @patch('src.kursovayasql.GetVacancies.requests.get')
    def test_find_company_id_no_results(self, mock_get):
        """Тест, когда не найдено компании."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': []}

        company_id = GetVacancies.find_company_id('Nonexistent Company')

        self.assertIsNone(company_id)

    @patch('src.kursovayasql.GetVacancies.requests.get')
    def test_find_company_id_request_failed(self, mock_get):
        """Тест, когда запрос завершился неудачно."""
        mock_response = mock_get.return_value
        mock_response.status_code = 400

        company_id = GetVacancies.find_company_id('Test Company')

        self.assertIsNone(company_id)

    @patch('src.kursovayasql.GetVacancies.GetVacancies.find_company_id', return_value='12345')
    @patch('src.kursovayasql.GetVacancies.requests.get')
    def test_get_vacancies_success(self, mock_get, mock_find_id):
        """Тест успешного получения вакансий."""
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': [{'name': 'Test Vacancy'}]}

        vacancies = GetVacancies.get_vacancies('Test Company')

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['name'], 'Test Vacancy')

    @patch('src.kursovayasql.GetVacancies.GetVacancies.find_company_id', return_value=None)
    def test_get_vacancies_no_company_id(self, mock_find_id):
        """Тест, когда не найден ID компании."""
        vacancies = GetVacancies.get_vacancies('Nonexistent Company')
        self.assertIsNone(vacancies)
