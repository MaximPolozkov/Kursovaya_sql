import unittest
from unittest.mock import patch, mock_open
import psycopg2
from src.kursovayasql.DatabaseCreate import DatabaseCreate


class TestDatabaseCreate(unittest.TestCase):
    @patch('src.kursovayasql.DatabaseCreate.psycopg2.connect')
    def test_create_database_success(self, mock_connect):
        """Тест успешного создания БД."""
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        config_data = """
        [postgresql]
        host = localhost
        user = testuser
        password = testpassword
        port = 5432
        """
        with patch('src.kursovayasql.DatabaseCreate.open', mock_open(read_data=config_data)):
            creator = DatabaseCreate(config_file='datebase.ini')
            creator.create_database('test_db')

        mock_cursor.execute.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.DatabaseCreate.psycopg2.connect', side_effect=psycopg2.errors.DuplicateDatabase("Database exists"))
    def test_create_database_duplicate(self, mock_connect):
        """Тест, когда БД уже существует."""
        config_data = """
        [postgresql]
        host = localhost
        user = testuser
        password = testpassword
        port = 5432
        """
        with patch('src.kursovayasql.DatabaseCreate.open', mock_open(read_data=config_data)):
            creator = DatabaseCreate(config_file='datebase.ini')
            creator.create_database('test_db')

    @patch('src.kursovayasql.DatabaseCreate.psycopg2.connect', side_effect=Exception("Connection Error"))
    def test_create_database_connection_error(self, mock_connect):
        """Тест ошибки подключения к БД."""
        config_data = """
        [postgresql]
        host = localhost
        user = testuser
        password = testpassword
        port = 5432
        """
        with patch('src.kursovayasql.DatabaseCreate.open', mock_open(read_data=config_data)):
            creator = DatabaseCreate(config_file='datebase.ini')
            creator.create_database('test_db')