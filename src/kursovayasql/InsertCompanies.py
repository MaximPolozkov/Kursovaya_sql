import configparser

import psycopg2

from ApiCompanies import ApiCompanies


class EntryIntoCompanies:

    def __init__(self, config_file='datebase.ini'):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file)
        except Exception as e:
            print(f"Ошибка при чтении файла конфигурации: {e}")
            raise

    def insert_companies(self):
        """Заносит данные в таблицу компании"""
        conn = None
        try:
            host = self.config['postgresql']['host']
            user = self.config['postgresql']['user']
            password = self.config['postgresql']['password']
            port = self.config['postgresql']['port']
            database = self.config['postgresql']['database']

            conn = psycopg2.connect(host=host, user=user, password=password, port=port, database=database)

            cursor = conn.cursor()

            api_companies = ApiCompanies().get_companies()

            for company in api_companies:
                hh_id = company.get('id')
                name = company.get('name')
                cursor.execute(f"""
                INSERT INTO companies (hh_id, name) VALUES( %s, %s)
                """, (hh_id, name))

            conn.commit()

            print("Записи внесены успешно")

        except psycopg2.errors.DuplicateDatabase:
            print(f" Записи не внесены.")
        except Exception as e:
            print(f"Ошибка при записи в таблицу: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()


if __name__ == "__main__":
    pol = EntryIntoCompanies()
    pol.insert_companies()
