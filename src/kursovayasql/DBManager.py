import configparser

import psycopg2


class DBManager:

    def __init__(self, config_file='datebase.ini'):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file)
            self.conn = None
        except Exception as e:
            print(f"Ошибка при чтении файла конфигурации: {e}")
            raise

    def connect(self):
        params = self.config['postgresql']
        self.conn = psycopg2.connect(**params)

    def close(self):
        if self.conn:
            self.conn.close()

    def get_companies_and_vacancies_count(self):
        """Возвращает компании и количество вакансий"""
        self.connect()
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT companies.name, COUNT(vacancies.id)
                    FROM companies
                    LEFT JOIN vacancies ON companies.id = vacancies.id
                    GROUP BY companies.name
                    ORDER BY companies.name
                """)

                return cur.fetchall()

        finally:
            self.close()

    def get_all_vacancies(self):
        """Возвращает список всех вакансий"""
        self.connect()
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT companies.name, vacancies.name, vacancies.salary_from, vacancies.salary_to
                    FROM vacancies
                    JOIN companies ON vacancies.company_id = companies.id; 
                """)

                return cur.fetchall()
        finally:
            self.close()

    def get_avg_salary(self):
        """Возвращает среднюю зарплату"""
        self.connect()
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT avg((salary_from + salary_to)/2) FROM vacancies
                    WHERE salary_from > 0 and salary_to > 0
                """)

                return cur.fetchall()[0]

        finally:
            self.close()

    def get_vacancies_with_high_salary(self):
        """Вакансии с зп выше среднего"""
        self.connect()
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM vacancies
                    WHERE (salary_from + salary_to)/2 > 
                    (SELECT avg((salary_from + salary_to)/2) FROM vacancies
                    WHERE salary_from > 0 and salary_to > 0)
                """)
                return cur.fetchall()
        finally:
            self.close()

    def get_vacancies_with_keyword(self, keyword):
        """Вакансии, содержащие ключевое слово."""
        self.connect()
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"""
                    SELECT * FROM vacancies WHERE name LIKE '%{keyword}%';
                """)

                return cur.fetchall()

        finally:
            self.close()


if __name__ == "__main__":
    manager = DBManager()
    result_manager = manager.get_vacancies_with_keyword('Водитель')
    print(result_manager)
