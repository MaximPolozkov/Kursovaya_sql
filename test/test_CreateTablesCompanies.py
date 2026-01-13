import unittest
from unittest.mock import patch, mock_open
import configparser
import psycopg2
import os

from src.kursovayasql.CreateTablesCompanies import CreateTableCompanies


class TestCreateTableCompanies(unittest.TestCase):

    @patch('src.kursovayasql.CreateTablesCompanies.psycopg2.connect')
    def test_create_table_success(self, mock_connect):
        """Тест успешного создания таблицы."""
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Создаем фиктивный файл конфигурации
        config_data = """
        [postgresql]
        host = localhost
        user = testuser
        password = testpassword
        port = 5432
        database = testdb
        """
        with patch('src.kursovayasql.CreateTablesCompanies.open', mock_open(read_data=config_data)):
            creator = CreateTableCompanies(config_file='datebase.ini')
            creator.create_table_companies('test_table')

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.kursovayasql.CreateTablesCompanies.psycopg2.connect', side_effect=psycopg2.errors.DuplicateDatabase("Table exists"))
    def test_create_table_duplicate(self, mock_connect):
        """Тест, когда таблица уже существует."""
        config_data = """
        [postgresql]
        host = localhost
        user = testuser
        password = testpassword
        port = 5432
        database = testdb
        """
        with patch('src.kursovayasql.CreateTablesCompanies.open', mock_open(read_data=config_data)):
            creator = CreateTableCompanies(config_file='datebase.ini')
            creator.create_table_companies('test_table')

    @patch('src.kursovayasql.CreateTablesCompanies.psycopg2.connect', side_effect=Exception("Connection Error"))
    def test_create_table_connection_error(self, mock_connect):
        """Тест ошибки подключения к БД."""
        config_data = """
        [postgresql]
        host = localhost
        user = testuser
        password = testpassword
        port = 5432
        database = testdb
        """
        with patch('src.kursovayasql.CreateTablesCompanies.open', mock_open(read_data=config_data)):  # Замените your_module
            creator = CreateTableCompanies(config_file='datebase.ini')
            creator.create_table_companies('test_table')
