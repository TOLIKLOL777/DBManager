import os
from abc import ABC, abstractmethod

import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_con = {
    "dbname": os.getenv("dbname"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "host": os.getenv("host"),
    "port": os.getenv("port"),
}


class BaseDB(ABC):  # pragma: no cover
    """Базовый класс для DBManager"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass


class DBManager(BaseDB):
    """Класс для работы с таблицами в базе данных"""

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=db_con["dbname"],
            user=db_con["user"],
            password=db_con["password"],
            host=db_con["host"],
            port=db_con["port"],
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list:
        """Возвращает список работодателей и количество открытых вакансий"""
        self.cur.execute(
            """SELECT e.name, COUNT(v.vacancy_id) as vacancy_count
               FROM employers e
               INNER JOIN vacancies v ON e.employer_id = v.employer_id
               GROUP BY e.name;"""
        )

        employers = self.cur.fetchall()
        return employers

    def get_all_vacancies(self) -> list:
        """Возвращает список всех вакансий в таблице"""
        self.cur.execute(
            """SELECT e.name,v.name,v.salary_from,v.salary_to,v.url
                        FROM vacancies v
                        INNER JOIN employers e ON e.employer_id = v.employer_id;"""
        )
        vacancies = self.cur.fetchall()
        return vacancies

    def get_avg_salary(self) -> list:
        """Возвращает среднее значение по зарплате всех вакансий"""
        self.cur.execute(
            """SELECT AVG(salary_from)
                        FROM vacancies
                        WHERE salary_from > 0;"""
        )
        data = self.cur.fetchall()
        return data

    def get_vacancies_with_higher_salary(self) -> list:
        """Возвращает список всех вакансий у которых зарплата выше среднего значения"""
        avg = self.get_avg_salary()
        avg = avg[0][0]
        self.cur.execute(
            f"""SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                        FROM vacancies v
                        INNER JOIN employers e ON e.employer_id = v.employer_id
                        WHERE salary_from > {avg};"""
        )
        high_vacancies = self.cur.fetchall()
        return high_vacancies

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        """Принимает на вход слово по которому будет произведён поиск по вакансиям"""
        self.cur.execute(
            """
            SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            INNER JOIN employers e ON e.employer_id = v.employer_id
            WHERE v.name ILIKE %s
            ORDER BY v.name
        """,
            (f"%{keyword}%",),
        )

        key_vacancies = self.cur.fetchall()
        return key_vacancies
