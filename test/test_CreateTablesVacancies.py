import unittest
from unittest.mock import patch, mock_open
import configparser
import psycopg2
import os

from src.kursovayasql.CreateTablesVacancies import CreateTableVacancies


class TestCreateTableVacancies(unittest.TestCase):

    @patch('src.kursovayasql.CreateTablesVacancies.psycopg2.connect')  # Мокируем psycopg2.connect
    def test_create_table_success(self, mock_connect):
        """Тест успешного создания таблицы."""
        mock_conn = mock_connect.return_value  # Получаем мок соединения
        mock_cursor = mock_conn.cursor.return_value  # Получаем мок курсора

        config_data = """
        [postgresql]
        host = localhost
        user = testuser
        password = testpassword
        port = 5432
        database = testdb
        """
        with patch('src.kursovayasql.CreateTablesVacancies.open', mock_open(read_data=config_data)): # Мокируем open для чтения конфига
            creator = CreateTableVacancies(config_file='datebase.ini')
            creator.create_table_vacancies('test_table')

        mock_cursor.execute.assert_called_once() # Проверяем, что execute был вызван
        mock_conn.commit.assert_called_once()  # Проверяем, что commit был вызван
        mock_conn.close.assert_called_once()  # Проверяем, что close был вызван

    @patch('src.kursovayasql.CreateTablesVacancies.psycopg2.connect', side_effect=psycopg2.errors.DuplicateTable("Table exists")) # Мокируем подключение, чтобы вызвать исключение
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
        with patch('src.kursovayasql.CreateTablesVacancies.open', mock_open(read_data=config_data)):
            creator = CreateTableVacancies(config_file='datebase.ini')
            creator.create_table_vacancies('test_table')

    @patch('src.kursovayasql.CreateTablesVacancies.psycopg2.connect', side_effect=Exception("Connection Error")) # Мокируем подключение, чтобы вызвать исключение
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
        with patch('src.kursovayasql.CreateTablesVacancies.open', mock_open(read_data=config_data)):
            creator = CreateTableVacancies(config_file='datebase.ini')
            creator.create_table_vacancies('test_table')