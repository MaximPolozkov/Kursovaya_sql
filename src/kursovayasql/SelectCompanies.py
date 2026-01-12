import configparser

import psycopg2


class SelectCompanies:

    def __init__(self, config_file='datebase.ini'):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file)
        except Exception as e:
            print(f"Ошибка при чтении файла конфигурации: {e}")
            raise

    def select_companies(self):
        """Делает запрос в таблицу компании"""
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
            SELECT name FROM companies
            """)

            rows = cursor.fetchall()

            return rows

        except Exception as e:
            print(f"Данные не могут быть получены: {e}")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    select = SelectCompanies()
    companies = select.select_companies()
    print(companies)
