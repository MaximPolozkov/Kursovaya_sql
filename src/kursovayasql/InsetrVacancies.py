import configparser
import os

import psycopg2

from src.kursovayasql.GetVacancies import GetVacancies


class EntryIntoVacancies:

    def __init__(self, config_file='datebase.ini'):
        self.config = configparser.ConfigParser()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, config_file)
        try:
            self.config.read(config_path)
        except Exception as e:
            print(f"Ошибка при чтении файла конфигурации: {e}")
            raise

    def insert_vacancies(self, get_vacancies: str):
        """Заносит данные в таблицу вакансии"""
        conn = None
        try:
            host = self.config['postgresql']['host']
            user = self.config['postgresql']['user']
            password = self.config['postgresql']['password']
            port = self.config['postgresql']['port']
            database = self.config['postgresql']['database']

            conn = psycopg2.connect(host=host, user=user, password=password, port=port, database=database)

            cursor = conn.cursor()

            api_vacancies = GetVacancies.get_vacancies(get_vacancies)

            if api_vacancies:
                cursor.execute("""
                SELECT id FROM companies WHERE name = %s
                """, (get_vacancies,))
                company_id_result = cursor.fetchone()

                if company_id_result:
                    company_id = company_id_result[0]

                    for vacancy in api_vacancies:
                        hh_id = vacancy.get('id')
                        name = vacancy.get('name')
                        salary = vacancy.get('salary')
                        salary_f = salary.get('from') if salary else None
                        salary_t = salary.get('to') if salary else None

                        if hh_id and name:
                            cursor.execute(f"""
                            INSERT INTO vacancies( company_id, hh_id, name, salary_from, salary_to)
                            VALUES( %s, %s, %s, %s, %s)
                            ON CONFLICT (hh_id) DO NOTHING;
                            """, (company_id, hh_id, name, salary_f, salary_t))

                    conn.commit()

                    print("Таблица вакансий заполнена успешно")

        except psycopg2.errors.DuplicateDatabase:
            print(f"Записи не внесены в таблицу вакансий.")
        except Exception as e:
            print(f"Ошибка при записи в таблицу вакансий: {e}")
        finally:
            if conn:
                cursor.close()
                conn.close()


if __name__ == "__main__":
    vacansy = EntryIntoVacancies()
    vacansy.insert_vacancies('0000')
