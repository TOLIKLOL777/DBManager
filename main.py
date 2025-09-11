from src.db_creator import create_db
from src.db_manager import DBManager


def main():
    print("Приветствую в программе для работы с вакансиями в hh.ru")
    print("Пожалуйста подождите, создаётся база данных...")
    create_db()
    dbmanager = DBManager()
    print("База данных готова к работе")
    while True:
        print(
            """\nВыберите что хотите сделать (для выбора напишите номер действия):
    1:Получить список всех работодателей и их кол-во открытых вакансий.
    2:Получить список всех доступных вакансий.
    3:Получить среднее по всем вакансиям.
    4:Получить список всех вакансий у которых зарплата выше среднего значения.
    5:Сделать поиск вакансий по заданному слову.
    6:Выход."""
        )
        try:
            answer = int(input())
        except Exception:
            print("Введите корректный ответ")
        if answer == 1:
            companies = dbmanager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"Работодатель: {company[0]}, кол-во открытых вакансий {company[1]}")

        if answer == 2:
            vacancies = dbmanager.get_all_vacancies()
            for vacancy in vacancies:
                print(
                    f"Работодатель: {vacancy[0]}, Вакансия: {vacancy[1]}, зарплата от {vacancy[2]} до {vacancy[3]}, ссылка {vacancy[4]}"
                )

        if answer == 3:
            avg = dbmanager.get_avg_salary()
            print(f"Среднее по всем вакансиям {round(avg[0][0], 2)}")

        if answer == 4:
            high_vacancies = dbmanager.get_vacancies_with_higher_salary()
            for vacancy in high_vacancies:
                print(
                    f"Работодатель: {vacancy[0]}, Вакансия: {vacancy[1]}, зарплата от {vacancy[2]} до {vacancy[3]}, ссылка {vacancy[4]}"
                )

        if answer == 5:
            key_word = input("Введите слово для поиска: ")
            key_vacancies = dbmanager.get_vacancies_with_keyword(key_word)
            for vacancy in key_vacancies:
                print(
                    f"Работодатель: {vacancy[0]}, Вакансия: {vacancy[1]}, зарплата от {vacancy[2]} до {vacancy[3]}, ссылка {vacancy[4]}"
                )

        if answer == 6:
            break

        if answer > 6 or answer <= 0:
            print("Введите корректный ответ")


main()
