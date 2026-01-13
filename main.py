from src.kursovayasql.DatabaseCreate import DatabaseCreate
from src.kursovayasql.CreateTablesCompanies import CreateTableCompanies
from src.kursovayasql.CreateTablesVacancies import CreateTableVacancies
from src.kursovayasql.InsertCompanies import EntryIntoCompanies
from src.kursovayasql.InsetrVacancies import EntryIntoVacancies
from src.kursovayasql.SelectCompanies import SelectCompanies
from src.kursovayasql.DBManager import DBManager

user = input("Введите свое имя: \n")

print(f"Привет {user}, меня зовут sql_hh, я познакомлю тебя с программой знакомства с программой")


def user_db():
    print("Далее мы с тобой создадим БД и необходимые таблицы, приступим да/нет: \n")

    db = input("Введите ваш ответ: \n")
    if db == 'Да':
        print(f"Приступим {user} \n")
        print("Запускаю модуль для создания БД")
        try:
            DatabaseCreate().create_database()
            print(f"Поздравляю Вас {user} первый шаг сделан, я создал БД, теперь приступим к созданию таблиц")
            print("Приступим к созданию таблиц в БД")
            CreateTableCompanies().create_table_companies()
            CreateTableVacancies().create_table_vacancies()
            print(f"Поздравляю {user}! Таблицы были созданы.")
            print("Теперь приступим к получению данных о компаний и заполнению таблицы")
            EntryIntoCompanies().insert_companies()
            print(f"{user} данные успешно получены и занесены в таблицу")
            print(f"Теперь {user}, получим вакансии которые интересуют Вас, выбранной компании и запишем их в таблицу")
            print("""Для начала я покажу Вам названия компаний которы мы получили ранее, 
                  что-бы Вы смогли выбрать компанию с вакансиями, которая интересует""")
            result = SelectCompanies().select_companies()
            for company in result:
                print(company[0])

            print(f"{user} теперь выберите из списка интересующую Вас компанию")

            company_name = input("Введите или скопируйте интересующую Вас компанию и вставьте в это поле: \n")

            EntryIntoVacancies().insert_vacancies(company_name)
            print(f"{user}, вакансии по данной компании получены и занесены в таблицу")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            print("Программа будет завершена")
    else:
        print(f"Хорошо буду ждать когда будите готовы {user}")

    print(f"{user}, можете выбрать действие которое Вас интересует \n")

    while True:
        print("1. Вернуть компании и количество вакансий")
        print("2. Вернуть список всех вакансий")
        print("3. Вернуть среднюю зарплату")
        print("4. Вакансии с зп выше среднего")
        print("5. Вакансии, содержащие ключевое слово")

        keyword = input("Выберите действие: \n")

        if keyword == "1":
            get_count = DBManager().get_companies_and_vacancies_count()
            for count in get_count:
                print(count)
        elif keyword == "2":
            get_count = DBManager().get_all_vacancies()
            for count in get_count:
                print(count)
        elif keyword == "3":
            get_count = DBManager().get_avg_salary()
            for count in get_count:
                print(count)
        elif keyword == "4":
            get_count = DBManager().get_vacancies_with_high_salary()
            for count in get_count:
                print(count)
        elif keyword == "5":
            name_keyword = input("Введите название вакансии: \n")
            get_count = DBManager().get_vacancies_with_keyword(name_keyword)
            for count in get_count:
                print(count)
        else:
            print("Данного пункта нет.")


if __name__ == "__main__":
    user_db()
