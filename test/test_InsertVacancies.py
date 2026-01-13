import unittest
from unittest.mock import patch, mock_open
import psycopg2
from src.kursovayasql.InsetrVacancies import EntryIntoVacancies
from src.kursovayasql.GetVacancies import GetVacancies


class TestEntryIntoVacancies(unittest.TestCase):

    config_data = """
    [postgresql]
    host = localhost
    user = testuser
    password = testpassword
    port = 5432
    database = testdb
    """

    @patch('src.kursovayasql.InsetrVacancies.psycopg2.connect')
    @patch.object(GetVacancies, 'get_vacancies')
    def test_insert_vacancies_success(self, mock_get_vacancies, mock_connect):
        """Мокируем подключение к БД и получение данных о вакансиях."""
        mock_vacancies = [{'id': '1', 'name': 'Vacancy A', 'salary': {'from': 100, 'to': 200}}]
        mock_get_vacancies.return_value = mock_vacancies

        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = (1,)

        with patch('src.kursovayasql.InsetrVacancies.open', mock_open(read_data=self.config_data)):
            entry = EntryIntoVacancies()
            entry.insert_vacancies("Test Company")

        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.InsetrVacancies.psycopg2.connect')
    @patch.object(GetVacancies, 'get_vacancies')
    def test_insert_vacancies_no_vacancies(self, mock_get_vacancies, mock_connect):
        mock_get_vacancies.return_value = None
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        with patch('src.kursovayasql.InsetrVacancies.open', mock_open(read_data=self.config_data)):
            entry = EntryIntoVacancies()
            entry.insert_vacancies("Test Company")

        self.assertEqual(mock_cursor.execute.call_count, 0)
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.InsetrVacancies.psycopg2.connect')
    @patch.object(GetVacancies, 'get_vacancies')
    def test_insert_vacancies_no_company_id(self, mock_get_vacancies, mock_connect):
        """Мокируем подключение к БД и получение данных о вакансиях."""
        mock_vacancies = [{'id': '1', 'name': 'Vacancy A', 'salary': {'from': 100, 'to': 200}}]
        mock_get_vacancies.return_value = mock_vacancies

        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None

        with patch('src.kursovayasql.InsetrVacancies.open', mock_open(read_data=self.config_data)):
            entry = EntryIntoVacancies()
            entry.insert_vacancies("Test Company")

        self.assertEqual(mock_cursor.execute.call_count, 1)
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.InsetrVacancies.psycopg2.connect')
    @patch.object(GetVacancies, 'get_vacancies')
    def test_insert_vacancies_duplicate_database(self, mock_get_vacancies, mock_connect):
        """Мокируем подключение к БД и получение данных о вакансиях."""
        mock_vacancies = [{'id': '1', 'name': 'Vacancy A', 'salary': {'from': 100, 'to': 200}}]
        mock_get_vacancies.return_value = mock_vacancies

        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.execute.side_effect = psycopg2.errors.DuplicateDatabase("Duplicate")

        with patch('src.kursovayasql.InsetrVacancies.open', mock_open(read_data=self.config_data)):
            entry = EntryIntoVacancies()
            entry.insert_vacancies("Test Company")

        mock_conn.close.assert_called_once()
        