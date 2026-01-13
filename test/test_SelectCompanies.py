import unittest
from unittest.mock import patch, mock_open
import psycopg2
from src.kursovayasql.SelectCompanies import SelectCompanies


class TestSelectCompanies(unittest.TestCase):

    config_data = """
    [postgresql]
    host = localhost
    user = testuser
    password = testpassword
    port = 5432
    database = testdb
    """

    @patch('src.kursovayasql.SelectCompanies.psycopg2.connect')
    def test_select_companies_success(self, mock_connect):
        """Мокируем подключение к БД и результат запроса."""
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [('Company A',), ('Company B',)]

        with patch('src.kursovayasql.SelectCompanies.open', mock_open(read_data=self.config_data)):
            selector = SelectCompanies()
            companies = selector.select_companies()

        mock_cursor.execute.assert_called_once()
        self.assertEqual(companies, [('Company A',), ('Company B',)])
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.SelectCompanies.psycopg2.connect')
    def test_select_companies_connection_error(self, mock_connect):
        """Мокируем ошибку при подключении к БД."""
        mock_connect.side_effect = Exception("Connection failed")

        with patch('src.kursovayasql.SelectCompanies.open', mock_open(read_data=self.config_data)):
            selector = SelectCompanies()
            companies = selector.select_companies()
        self.assertIsNone(companies)
