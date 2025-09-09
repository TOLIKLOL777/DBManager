import os
from abc import ABC, abstractmethod
from typing import Any, Optional

import psycopg2
import requests
from dotenv import load_dotenv
from psycopg2 import OperationalError, extensions

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
        self.cur.execute(
            """SELECT name,open_vacancies
                        FROM employers;"""
        )
        data = self.cur.fetchall()
        return data

    def get_all_vacancies(self) -> list:
        self.cur.execute(
            """SELECT employer_name,name,salary_from,salary_to,url
                        FROM vacancies;"""
        )
        data = self.cur.fetchall()
        return data

    def get_avg_salary(self) -> list:
        self.cur.execute(
            """SELECT AVG(salary_from)
                        FROM vacancies
                        WHERE salary_from > 0;"""
        )
        data = self.cur.fetchall()
        return data

    def get_vacancies_with_higher_salary(self) -> list:
        avg = self.get_avg_salary()
        avg = avg[0][0]
        self.cur.execute(
            f"""SELECT name,salary_from
                        FROM vacancies
                        WHERE salary_from > {avg};"""
        )
        data = self.cur.fetchall()
        return data

    def get_vacancies_with_keyword(self, keyword: str) -> list:
        self.cur.execute(
            """
            SELECT vacancy_id, name, salary_from, salary_to, url, employer_name, url
            FROM vacancies
            WHERE name ILIKE %s
            ORDER BY name
        """,
            (f"%{keyword}%",),
        )

        vacancies = self.cur.fetchall()
        return vacancies
