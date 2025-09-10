import os

import psycopg2
from dotenv import load_dotenv

from src.decoder import employers_info, vacancies_info

load_dotenv()
db_con = {
    "dbname": os.getenv("dbname"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "host": os.getenv("host"),
    "port": os.getenv("port"),
}


def create_db() -> None:
    """Создает базу данных, если она еще не существует."""
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_con["user"],
            password=db_con["password"],
            host=db_con["host"],
            port=db_con["port"],
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Проверка существует ли база данных
        db_name = db_con["dbname"]
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {db_name}")
        else:
            # Удаление старой базы данных и создание новой
            cur.execute(f"DROP DATABASE {db_name} WITH (FORCE)")
            cur.execute(f"CREATE DATABASE {db_name}")

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        create_tables()
        if cur:
            cur.close()
        if conn:
            conn.close()


def create_tables() -> None:
    """Создаёт таблицы с работодателями и вакансиями"""
    try:
        conn = psycopg2.connect(
            dbname=db_con["dbname"],
            user=db_con["user"],
            password=db_con["password"],
            host=db_con["host"],
            port=db_con["port"],
        )
        cur = conn.cursor()

        # Создаем таблицу с работодателями если её нет
        cur.execute(
            """CREATE TABLE IF NOT EXISTS employers (
                        employer_id INT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        url VARCHAR(255),
                        open_vacancies INTEGER)"""
        )

        # Создаем таблицу с вакансиями если её нет
        cur.execute(
            """CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id INT PRIMARY KEY,
                        employer_id INT NOT NULL,
                        employer_name VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        url VARCHAR(255),
                        FOREIGN KEY (employer_id) REFERENCES employers(employer_id))"""
        )
        conn.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    finally:
        add_data()
        if cur:
            cur.close()
        if conn:
            conn.close()


def add_data() -> None:
    """Вставляет данные из API-запроса в соответствующие таблицы"""
    try:
        conn = psycopg2.connect(
            dbname=db_con["dbname"],
            user=db_con["user"],
            password=db_con["password"],
            host=db_con["host"],
            port=db_con["port"],
        )
        cur = conn.cursor()

        employers = employers_info()
        vacancies = vacancies_info()

        # Добавляем данные работодателей в таблицу
        for employer in employers:
            query = """INSERT INTO employers (employer_id, name, url, open_vacancies)
            VALUES (%s, %s, %s, %s) ON CONFLICT (employer_id) DO NOTHING"""
            cur.execute(query, employer)

        # Добавляем данные вакансий в таблицу
        for vacancy in vacancies:
            query = """INSERT INTO vacancies (vacancy_id, employer_id, employer_name, name, salary_from, salary_to, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (vacancy_id) DO NOTHING"""
            cur.execute(query, vacancy)

        conn.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
