import configparser

import psycopg2


class CreateTableCompanies:

    def __init__(self, config_file='datebase.ini'):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file)
        except Exception as e:
            print(f"Ошибка при чтении файла конфигурации: {e}")
            raise

    def create_table_companies(self, name_table: str = 'companies'):
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
            CREATE TABLE IF NOT EXISTS {name_table}(
            id SERIAL PRIMARY KEY,
            hh_id INTEGER,
            name VARCHAR(255)
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
    table = CreateTableCompanies()
    table.create_table_companies()
