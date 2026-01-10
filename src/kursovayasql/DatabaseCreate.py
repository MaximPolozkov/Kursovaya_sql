import psycopg2
import configparser


class DatabaseCreate:
    
    def __init__(self, config_file='datebase.ini'):
        self.config = configparser.ConfigParser()
        try:
            self.config.read(config_file)
        except Exception as e:
            print(f"Ошибка при чтении файла конфигурации: {e}")
            raise

    def create_database(self, database_name):
        conn = None
        try:
            host = self.config['postgresql']['host']
            user = self.config['postgresql']['user']
            password = self.config['postgresql']['password']
            port = self.config['postgresql']['port']

            conn = psycopg2.connect(host=host, user=user, password=password, port=port, database='postgres')

            conn.autocommit = True

            cursor = conn.cursor()

            sql_create_db = f"CREATE DATABASE {database_name}"

            cursor.execute(sql_create_db)

            print(f"База данных '{database_name}' успешно создана.")

        except psycopg2.errors.DuplicateDatabase:
            print(f"База данных '{database_name}' уже существует.")
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    create = DatabaseCreate()
    create.create_database(database_name='hh_sql')
