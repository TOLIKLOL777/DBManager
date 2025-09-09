from src.decoder import employers_info, vacancies_info
from src.db_creator import create_db,create_tables, add_data
from src.db_manager import DBManager


a = DBManager()
print(a.get_vacancies_with_keyword("разработчик"))

