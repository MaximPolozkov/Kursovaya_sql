import configparser
import os

import psycopg2


class CreateTableVacancies:

    def __init__(self, config_file='datebase.ini'):
        self.config = configparser.ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, config_file)
        try:
            self.config.read(config_path)
        except Exception as e:
            print(f"Ошибка при чтении файла конфигурации: {e}")
            raise

    def create_table_vacancies(self, name_table: str = 'vacancies'):
        """Создает таблицу вакансии в БД"""
        conn = None
        try:
            host = self.config['postgresql']['host']
            user = self.config['postgresql']['user']
            password = self.config['postgresql']['password']
            port = self.config['postgresql']['port']
            database = self.config['postgresql']['database']

            conn = psycopg2.connect(host=host, user=user, password=password, port=port, database=database)

            cursor = conn.cursor()

            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {name_table} (
            id SERIAL PRIMARY KEY,
            company_id INTEGER REFERENCES companies(id),
            hh_id INTEGER UNIQUE,
            name VARCHAR(255),
            salary_from INTEGER,
            salary_to INTEGER
            );
            """)

            conn.commit()

            print(f"Таблица '{name_table}' успешно создана.")

        except psycopg2.errors.DuplicateDatabase:
            print(f" Таблица '{name_table}' уже существует.")
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    table = CreateTableVacancies()
    table.create_table_vacancies()
