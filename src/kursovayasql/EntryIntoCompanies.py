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

    def into_companies(self):
        r = []
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
            #r.append(api_companies)

            for company in api_companies:
                print(company)
                #hh_id = (company['id'])
                #print(hh_id)
                #cursor.execute(f"""
                #INSERT INTO companies (id, hh_id, name) VALUES(%s, %s, %s) ON CONFLICT (hh_id) DO NOTHING
                #""", (hh_id, compani['name']))

            conn.commit()

            print("Записи внесены успешно")

        except psycopg2.errors.DuplicateDatabase:
            print(f" Записи не внесены.")
        except Exception as e:
            print(f"Ошибка при записи в таблицу: {e}")
        #finally:
            #if conn:#
                #cursor.close()
                #conn.close()


if __name__ == "__main__":
    pol = EntryIntoCompanies()
    pol.into_companies()
