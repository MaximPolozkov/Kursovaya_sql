import unittest
from unittest.mock import patch, mock_open
import psycopg2
from src.kursovayasql.DBManager import DBManager


class TestDBManager(unittest.TestCase):

    config_data = """
    [postgresql]
    host = localhost
    user = testuser
    password = testpassword
    port = 5432
    database = testdb
    """

    @patch('src.kursovayasql.DBManager.psycopg2.connect')
    def test_get_companies_and_vacancies_count(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.__enter__.return_value.fetchall.return_value = [('Company A', 10), ('Company B', 5)]

        with patch('src.kursovayasql.DBManager.open', mock_open(read_data=self.config_data)):
            db_manager = DBManager()
            result = db_manager.get_companies_and_vacancies_count()

        self.assertEqual(result, [('Company A', 10), ('Company B', 5)])
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.DBManager.psycopg2.connect')
    def test_get_all_vacancies(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.__enter__.return_value.fetchall.return_value = [('Company A', 'Vacancy 1', 10000, 20000)]
        with patch('src.kursovayasql.DBManager.open', mock_open(read_data=self.config_data)):
             db_manager = DBManager()
             result = db_manager.get_all_vacancies()

        self.assertEqual(result, [('Company A', 'Vacancy 1', 10000, 20000)])
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.DBManager.psycopg2.connect')
    def test_get_avg_salary(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.__enter__.return_value.fetchall.return_value = [(15000.0,)]

        with patch('src.kursovayasql.DBManager.open', mock_open(read_data=self.config_data)):
           db_manager = DBManager()
           result = db_manager.get_avg_salary()

        self.assertEqual(result, (15000.0,))
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.DBManager.psycopg2.connect')
    def test_get_vacancies_with_high_salary(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.__enter__.return_value.fetchall.return_value = [(1, 1, 'Vacancy', 20000, 30000)]

        with patch('src.kursovayasql.DBManager.open', mock_open(read_data=self.config_data)):
            db_manager = DBManager()
            result = db_manager.get_vacancies_with_high_salary()

        self.assertEqual(result, [(1, 1, 'Vacancy', 20000, 30000)])
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.DBManager.psycopg2.connect')
    def test_get_vacancies_with_keyword(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.__enter__.return_value.fetchall.return_value = [(1, 1, 'Vacancy with keyword', 10000, 20000)]

        with patch('src.kursovayasql.DBManager.open', mock_open(read_data=self.config_data)):
           db_manager = DBManager()
           result = db_manager.get_vacancies_with_keyword('keyword')

        self.assertEqual(result, [(1, 1, 'Vacancy with keyword', 10000, 20000)])
        mock_conn.close.assert_called_once()
