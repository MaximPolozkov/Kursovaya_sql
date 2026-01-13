import unittest
from unittest.mock import patch, mock_open
import psycopg2
from src.kursovayasql.InsertCompanies import EntryIntoCompanies
from src.kursovayasql.ApiCompanies import ApiCompanies


class TestEntryIntoCompanies(unittest.TestCase):

    config_data = """
    [postgresql]
    host = localhost
    user = testuser
    password = testpassword
    port = 5432
    database = testdb
    """

    @patch('src.kursovayasql.InsertCompanies.psycopg2.connect')
    @patch.object(ApiCompanies, 'get_companies')
    def test_insert_companies_success(self, mock_get_companies, mock_connect):
        """Мокируем подключение к БД и получение данных о компаниях из API."""
        mock_companies = [{'id': '1', 'name': 'Company A'}, {'id': '2', 'name': 'Company B'}]
        mock_get_companies.return_value = mock_companies

        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        with patch('src.kursovayasql.InsertCompanies.open', mock_open(read_data=self.config_data)):
            entry = EntryIntoCompanies()
            entry.insert_companies()

        # Проверяем, что execute был вызван нужное количество раз с верными аргументами.
        self.assertEqual(mock_cursor.execute.call_count, 2)
        # Проверяем, что commit был вызван.
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.InsertCompanies.psycopg2.connect')
    @patch.object(ApiCompanies, 'get_companies')
    def test_insert_companies_duplicate_database(self, mock_get_companies, mock_connect):
        mock_get_companies.return_value = []
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.side_effect = psycopg2.errors.DuplicateDatabase("Duplicate")

        with patch('src.kursovayasql.InsertCompanies.open', mock_open(read_data=self.config_data)):
            entry = EntryIntoCompanies()
            entry.insert_companies()

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.InsertCompanies.psycopg2.connect')
    @patch.object(ApiCompanies, 'get_companies')
    def test_insert_companies_exception(self, mock_get_companies, mock_connect):
        mock_get_companies.return_value = []
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.execute.side_effect = Exception("Generic error")

        with patch('src.kursovayasql.InsertCompanies.open', mock_open(read_data=self.config_data)):
            entry = EntryIntoCompanies()
            entry.insert_companies()

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()